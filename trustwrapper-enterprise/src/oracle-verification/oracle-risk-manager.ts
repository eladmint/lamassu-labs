/**
 * Oracle Risk Management System for Mento Protocol Integration
 * Real-time multi-oracle price deviation detection and consensus monitoring
 */

export interface OraclePrice {
  symbol: string;
  price: number;
  timestamp: number;
  source: string;
  blockNumber?: number;
  confidence: number;
}

export interface PriceDeviation {
  symbol: string;
  expectedPrice: number;
  actualPrice: number;
  deviationPercent: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: number;
  affectedOracles: string[];
}

export interface OracleHealth {
  source: string;
  symbol: string;
  status: 'healthy' | 'degraded' | 'offline';
  lastUpdate: number;
  missedUpdates: number;
  averageLatency: number;
  reliabilityScore: number;
}

export interface ManipulationAlert {
  id: string;
  symbol: string;
  detectionType: 'price_spike' | 'consensus_break' | 'volume_anomaly' | 'flash_attack';
  severity: 'medium' | 'high' | 'critical';
  confidence: number;
  priceImpact: number;
  timeDetected: number;
  affectedValue: number; // USD value at risk
  mitigationActions: string[];
}

export class OracleRiskManager {
  private priceHistory: Map<string, OraclePrice[]> = new Map();
  private healthMetrics: Map<string, OracleHealth> = new Map();
  private alertHistory: ManipulationAlert[] = [];
  private readonly maxHistoryLength = 1000;
  private readonly alertCallback?: (alert: ManipulationAlert) => void;

  constructor(
    private config: {
      deviationThresholds: {
        warning: number; // 1% = 0.01
        critical: number; // 5% = 0.05
        emergency: number; // 10% = 0.10
      };
      consensusThreshold: number; // Minimum oracles needed for consensus
      updateTimeoutMs: number; // Max time between updates
      alertCallback?: (alert: ManipulationAlert) => void;
    }
  ) {
    this.alertCallback = config.alertCallback;
  }

  /**
   * Process new oracle price data and detect anomalies
   */
  async processOracleUpdate(price: OraclePrice): Promise<PriceDeviation[]> {
    const key = `${price.symbol}_${price.source}`;

    // Store price history
    if (!this.priceHistory.has(key)) {
      this.priceHistory.set(key, []);
    }

    const history = this.priceHistory.get(key)!;
    history.push(price);

    // Maintain history limit
    if (history.length > this.maxHistoryLength) {
      history.shift();
    }

    // Update health metrics
    this.updateHealthMetrics(price);

    // Detect price deviations
    const deviations = await this.detectPriceDeviations(price);

    // Check for manipulation patterns
    await this.detectManipulationPatterns(price);

    return deviations;
  }

  /**
   * Detect price deviations across multiple oracle sources
   */
  private async detectPriceDeviations(newPrice: OraclePrice): Promise<PriceDeviation[]> {
    const deviations: PriceDeviation[] = [];
    const symbol = newPrice.symbol;

    // Get all recent prices for this symbol from different sources
    const recentPrices = this.getAllRecentPrices(symbol, 60000); // Last 60 seconds

    if (recentPrices.length < 2) {
      return deviations; // Need multiple sources for comparison
    }

    // Calculate consensus price (median of all sources)
    const prices = recentPrices.map(p => p.price).sort((a, b) => a - b);
    const consensusPrice = prices[Math.floor(prices.length / 2)];

    // Check deviation of new price from consensus
    const deviationPercent = Math.abs((newPrice.price - consensusPrice) / consensusPrice);

    if (deviationPercent > this.config.deviationThresholds.warning) {
      const severity = this.calculateDeviationSeverity(deviationPercent);

      deviations.push({
        symbol: newPrice.symbol,
        expectedPrice: consensusPrice,
        actualPrice: newPrice.price,
        deviationPercent,
        severity,
        timestamp: newPrice.timestamp,
        affectedOracles: [newPrice.source]
      });

      // Generate alert for significant deviations
      if (severity === 'high' || severity === 'critical') {
        await this.generateManipulationAlert(newPrice, deviationPercent, consensusPrice);
      }
    }

    return deviations;
  }

  /**
   * Detect sophisticated manipulation patterns
   */
  private async detectManipulationPatterns(price: OraclePrice): Promise<void> {
    const symbol = price.symbol;
    const history = this.priceHistory.get(`${symbol}_${price.source}`) || [];

    if (history.length < 10) return; // Need sufficient history

    // Pattern 1: Flash spike detection
    await this.detectFlashSpike(price, history);

    // Pattern 2: Consensus breakdown detection
    await this.detectConsensusBreakdown(price);

    // Pattern 3: Volume anomaly detection
    await this.detectVolumeAnomaly(price);
  }

  /**
   * Detect flash price spikes (potential flash loan attacks)
   */
  private async detectFlashSpike(price: OraclePrice, history: OraclePrice[]): Promise<void> {
    const recent = history.slice(-5); // Last 5 prices
    const averagePrice = recent.reduce((sum, p) => sum + p.price, 0) / recent.length;

    const spikePercent = Math.abs((price.price - averagePrice) / averagePrice);

    // Flash spike threshold: >20% sudden change
    if (spikePercent > 0.20) {
      const estimatedValue = this.estimateProtocolValueAtRisk(price.symbol, spikePercent);

      const alert: ManipulationAlert = {
        id: `flash_spike_${Date.now()}`,
        symbol: price.symbol,
        detectionType: 'flash_attack',
        severity: spikePercent > 0.50 ? 'critical' : 'high',
        confidence: Math.min(spikePercent * 2, 0.95), // Higher spike = higher confidence
        priceImpact: spikePercent,
        timeDetected: Date.now(),
        affectedValue: estimatedValue,
        mitigationActions: [
          'Pause oracle updates',
          'Activate circuit breaker',
          'Verify with external sources',
          'Alert protocol team'
        ]
      };

      this.alertHistory.push(alert);
      if (this.alertCallback) {
        this.alertCallback(alert);
      }
    }
  }

  /**
   * Detect consensus breakdown across oracle sources
   */
  private async detectConsensusBreakdown(price: OraclePrice): Promise<void> {
    const symbol = price.symbol;
    const recentPrices = this.getAllRecentPrices(symbol, 300000); // Last 5 minutes

    if (recentPrices.length < this.config.consensusThreshold) return;

    // Group by source and get latest from each
    const latestBySource = new Map<string, OraclePrice>();
    recentPrices.forEach(p => {
      const existing = latestBySource.get(p.source);
      if (!existing || p.timestamp > existing.timestamp) {
        latestBySource.set(p.source, p);
      }
    });

    const prices = Array.from(latestBySource.values()).map(p => p.price);
    const mean = prices.reduce((sum, p) => sum + p, 0) / prices.length;
    const variance = prices.reduce((sum, p) => sum + Math.pow(p - mean, 2), 0) / prices.length;
    const standardDeviation = Math.sqrt(variance);
    const coefficientOfVariation = standardDeviation / mean;

    // Consensus breakdown threshold: >5% coefficient of variation
    if (coefficientOfVariation > 0.05) {
      const estimatedValue = this.estimateProtocolValueAtRisk(symbol, coefficientOfVariation);

      const alert: ManipulationAlert = {
        id: `consensus_break_${Date.now()}`,
        symbol: price.symbol,
        detectionType: 'consensus_break',
        severity: coefficientOfVariation > 0.15 ? 'critical' : 'high',
        confidence: Math.min(coefficientOfVariation * 5, 0.90),
        priceImpact: coefficientOfVariation,
        timeDetected: Date.now(),
        affectedValue: estimatedValue,
        mitigationActions: [
          'Verify oracle sources',
          'Check for network issues',
          'Compare external price feeds',
          'Consider oracle timeout'
        ]
      };

      this.alertHistory.push(alert);
      if (this.alertCallback) {
        this.alertCallback(alert);
      }
    }
  }

  /**
   * Detect volume anomalies that could indicate manipulation
   */
  private async detectVolumeAnomaly(price: OraclePrice): Promise<void> {
    // This would integrate with DEX volume data to detect unusual trading volume
    // that correlates with price movements (indicating potential manipulation)

    // For MVP, we'll implement a placeholder that could be extended
    // with actual volume data from DEX aggregators

    const symbol = price.symbol;
    const history = this.priceHistory.get(`${symbol}_${price.source}`) || [];

    if (history.length < 20) return;

    // Calculate price volatility in recent period
    const recent = history.slice(-10);
    const priceChanges = recent.slice(1).map((p, i) =>
      Math.abs((p.price - recent[i].price) / recent[i].price)
    );

    const avgVolatility = priceChanges.reduce((sum, change) => sum + change, 0) / priceChanges.length;

    // High volatility threshold: >3% average price change
    if (avgVolatility > 0.03) {
      const alert: ManipulationAlert = {
        id: `volume_anomaly_${Date.now()}`,
        symbol: price.symbol,
        detectionType: 'volume_anomaly',
        severity: avgVolatility > 0.10 ? 'high' : 'medium',
        confidence: Math.min(avgVolatility * 10, 0.80),
        priceImpact: avgVolatility,
        timeDetected: Date.now(),
        affectedValue: this.estimateProtocolValueAtRisk(symbol, avgVolatility),
        mitigationActions: [
          'Monitor DEX volume spikes',
          'Check for large transactions',
          'Verify liquidity pool health',
          'Alert market makers'
        ]
      };

      this.alertHistory.push(alert);
      if (this.alertCallback) {
        this.alertCallback(alert);
      }
    }
  }

  /**
   * Get all recent prices for a symbol across all sources
   */
  private getAllRecentPrices(symbol: string, timeWindowMs: number): OraclePrice[] {
    const cutoff = Date.now() - timeWindowMs;
    const recentPrices: OraclePrice[] = [];

    this.priceHistory.forEach((history, key) => {
      if (key.startsWith(symbol + '_')) {
        const recent = history.filter(p => p.timestamp > cutoff);
        recentPrices.push(...recent);
      }
    });

    return recentPrices.sort((a, b) => b.timestamp - a.timestamp);
  }

  /**
   * Calculate deviation severity level
   */
  private calculateDeviationSeverity(deviationPercent: number): 'low' | 'medium' | 'high' | 'critical' {
    if (deviationPercent > this.config.deviationThresholds.emergency) {
      return 'critical';
    } else if (deviationPercent > this.config.deviationThresholds.critical) {
      return 'high';
    } else if (deviationPercent > this.config.deviationThresholds.warning) {
      return 'medium';
    }
    return 'low';
  }

  /**
   * Update health metrics for oracle sources
   */
  private updateHealthMetrics(price: OraclePrice): void {
    const key = `${price.symbol}_${price.source}`;
    const existing = this.healthMetrics.get(key);

    const health: OracleHealth = {
      source: price.source,
      symbol: price.symbol,
      status: 'healthy', // Will be updated based on timing
      lastUpdate: price.timestamp,
      missedUpdates: existing?.missedUpdates || 0,
      averageLatency: this.calculateAverageLatency(price),
      reliabilityScore: this.calculateReliabilityScore(price)
    };

    // Check if update is late
    if (existing && (price.timestamp - existing.lastUpdate) > this.config.updateTimeoutMs) {
      health.missedUpdates = existing.missedUpdates + 1;
      health.status = health.missedUpdates > 3 ? 'offline' : 'degraded';
    }

    this.healthMetrics.set(key, health);
  }

  /**
   * Calculate average latency for oracle updates
   */
  private calculateAverageLatency(price: OraclePrice): number {
    // This would calculate actual network latency
    // For MVP, return estimated latency based on update frequency
    return Math.random() * 1000 + 500; // 500-1500ms estimated
  }

  /**
   * Calculate reliability score for oracle source
   */
  private calculateReliabilityScore(price: OraclePrice): number {
    const key = `${price.symbol}_${price.source}`;
    const health = this.healthMetrics.get(key);

    if (!health) return 1.0; // New oracle starts with perfect score

    // Score based on missed updates and latency
    const uptimeScore = Math.max(0, 1 - (health.missedUpdates * 0.1));
    const latencyScore = Math.max(0, 1 - (health.averageLatency / 5000)); // Penalty for >5s latency

    return (uptimeScore + latencyScore) / 2;
  }

  /**
   * Estimate protocol value at risk from price manipulation
   */
  private estimateProtocolValueAtRisk(symbol: string, impactPercent: number): number {
    // This would integrate with actual protocol data
    // For MVP, use estimated values based on Mento's known reserves

    const estimatedExposure: Record<string, number> = {
      'cUSD': 25000000, // $25M exposure
      'cEUR': 15000000, // $15M exposure
      'cREAL': 10000000, // $10M exposure
      'cKES': 5000000,   // $5M exposure
      'default': 1000000 // $1M default
    };

    const exposure = estimatedExposure[symbol] || estimatedExposure['default'];
    return exposure * impactPercent;
  }

  /**
   * Generate manipulation alert
   */
  private async generateManipulationAlert(
    price: OraclePrice,
    deviationPercent: number,
    consensusPrice: number
  ): Promise<void> {
    const estimatedValue = this.estimateProtocolValueAtRisk(price.symbol, deviationPercent);

    const alert: ManipulationAlert = {
      id: `price_deviation_${Date.now()}`,
      symbol: price.symbol,
      detectionType: 'price_spike',
      severity: deviationPercent > 0.10 ? 'critical' : 'high',
      confidence: Math.min(deviationPercent * 5, 0.95),
      priceImpact: deviationPercent,
      timeDetected: Date.now(),
      affectedValue: estimatedValue,
      mitigationActions: [
        'Verify price with external sources',
        'Check for flash loan activity',
        'Review recent large transactions',
        'Consider temporary price pause'
      ]
    };

    this.alertHistory.push(alert);
    if (this.alertCallback) {
      this.alertCallback(alert);
    }
  }

  /**
   * Get current health status for all oracles
   */
  getOracleHealthStatus(): Map<string, OracleHealth> {
    return new Map(this.healthMetrics);
  }

  /**
   * Get recent alerts
   */
  getRecentAlerts(timeWindowMs: number = 3600000): ManipulationAlert[] {
    const cutoff = Date.now() - timeWindowMs;
    return this.alertHistory.filter(alert => alert.timeDetected > cutoff);
  }

  /**
   * Get price deviation summary for a symbol
   */
  getPriceDeviationSummary(symbol: string, timeWindowMs: number = 3600000): {
    averageDeviation: number;
    maxDeviation: number;
    alertCount: number;
    consensusHealth: 'good' | 'degraded' | 'poor';
  } {
    const recentPrices = this.getAllRecentPrices(symbol, timeWindowMs);
    const recentAlerts = this.getRecentAlerts(timeWindowMs).filter(a => a.symbol === symbol);

    if (recentPrices.length === 0) {
      return {
        averageDeviation: 0,
        maxDeviation: 0,
        alertCount: 0,
        consensusHealth: 'poor'
      };
    }

    // Calculate price stability
    const prices = recentPrices.map(p => p.price);
    const mean = prices.reduce((sum, p) => sum + p, 0) / prices.length;
    const deviations = prices.map(p => Math.abs(p - mean) / mean);

    const averageDeviation = deviations.reduce((sum, d) => sum + d, 0) / deviations.length;
    const maxDeviation = Math.max(...deviations);

    // Determine consensus health
    let consensusHealth: 'good' | 'degraded' | 'poor' = 'good';
    if (averageDeviation > 0.05 || recentAlerts.length > 3) {
      consensusHealth = 'poor';
    } else if (averageDeviation > 0.02 || recentAlerts.length > 1) {
      consensusHealth = 'degraded';
    }

    return {
      averageDeviation,
      maxDeviation,
      alertCount: recentAlerts.length,
      consensusHealth
    };
  }
}

/**
 * Factory function to create pre-configured Oracle Risk Manager for Mento Protocol
 */
export function createMentoOracleRiskManager(alertCallback?: (alert: ManipulationAlert) => void): OracleRiskManager {
  return new OracleRiskManager({
    deviationThresholds: {
      warning: 0.01,   // 1% warning threshold
      critical: 0.05,  // 5% critical threshold
      emergency: 0.10  // 10% emergency threshold
    },
    consensusThreshold: 3,     // Need 3+ oracle sources for consensus
    updateTimeoutMs: 300000,   // 5 minute timeout for oracle updates
    alertCallback
  });
}

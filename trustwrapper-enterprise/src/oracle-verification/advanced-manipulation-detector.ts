/**
 * Advanced Manipulation Detection System
 * Machine learning-based oracle manipulation detection with behavioral analysis
 */

import { LiveOracleData } from './blockchain-oracle-client';
import { ManipulationAlert } from './oracle-risk-manager';

export interface ManipulationPattern {
  id: string;
  name: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  indicators: string[];
  mitigationStrategies: string[];
}

export interface BehavioralFeatures {
  priceVolatility: number;
  volumeSpike: number;
  temporalAnomaly: number;
  crossOracleDeviation: number;
  liquidityDrop: number;
  transactionPattern: number;
  networkCongestion: number;
  gasSpike: number;
}

export interface MLModelPrediction {
  manipulationProbability: number;
  confidence: number;
  primaryIndicators: string[];
  riskScore: number;
  recommendedActions: string[];
}

export interface HistoricalAnalysis {
  symbol: string;
  timeframe: string;
  patterns: ManipulationPattern[];
  normalBehavior: BehavioralFeatures;
  anomalousEvents: Array<{
    timestamp: number;
    severity: string;
    description: string;
    verified: boolean;
  }>;
}

export class AdvancedManipulationDetector {
  private historicalData: Map<string, LiveOracleData[]> = new Map();
  private behaviorBaselines: Map<string, BehavioralFeatures> = new Map();
  private detectedPatterns: Map<string, ManipulationPattern[]> = new Map();
  private mlModel: ManipulationMLModel;
  private readonly maxHistoryLength = 10000;

  constructor() {
    this.mlModel = new ManipulationMLModel();
    this.initializeBehaviorBaselines();
  }

  /**
   * Main detection pipeline - analyze oracle data for manipulation
   */
  async detectManipulation(oracleData: LiveOracleData[]): Promise<{
    alerts: ManipulationAlert[];
    patterns: ManipulationPattern[];
    mlPrediction: MLModelPrediction;
    riskScore: number;
  }> {
    if (oracleData.length === 0) {
      return { alerts: [], patterns: [], mlPrediction: this.getDefaultPrediction(), riskScore: 0 };
    }

    // Update historical data
    this.updateHistoricalData(oracleData);

    // Extract behavioral features
    const features = this.extractBehavioralFeatures(oracleData);

    // Detect known manipulation patterns
    const patterns = await this.detectKnownPatterns(oracleData, features);

    // ML-based anomaly detection
    const mlPrediction = await this.mlModel.predict(features, oracleData);

    // Generate alerts based on findings
    const alerts = this.generateAlerts(oracleData, patterns, mlPrediction);

    // Calculate overall risk score
    const riskScore = this.calculateRiskScore(patterns, mlPrediction, features);

    return { alerts, patterns, mlPrediction, riskScore };
  }

  /**
   * Extract behavioral features from oracle data
   */
  private extractBehavioralFeatures(oracleData: LiveOracleData[]): BehavioralFeatures {
    const symbol = oracleData[0]?.symbol || 'UNKNOWN';
    const historical = this.historicalData.get(symbol) || [];

    // Price volatility analysis
    const priceVolatility = this.calculatePriceVolatility(oracleData);

    // Volume spike detection (confidence as proxy for volume)
    const volumeSpike = this.calculateVolumeSpike(oracleData, historical);

    // Temporal anomaly detection
    const temporalAnomaly = this.calculateTemporalAnomaly(oracleData);

    // Cross-oracle deviation analysis
    const crossOracleDeviation = this.calculateCrossOracleDeviation(oracleData);

    // Liquidity indicators (based on confidence and source count)
    const liquidityDrop = this.calculateLiquidityDrop(oracleData, historical);

    // Transaction pattern analysis
    const transactionPattern = this.calculateTransactionPattern(oracleData);

    // Network congestion indicators
    const networkCongestion = this.calculateNetworkCongestion(oracleData);

    // Gas price spike detection
    const gasSpike = this.calculateGasSpike(oracleData);

    return {
      priceVolatility,
      volumeSpike,
      temporalAnomaly,
      crossOracleDeviation,
      liquidityDrop,
      transactionPattern,
      networkCongestion,
      gasSpike
    };
  }

  /**
   * Detect known manipulation patterns
   */
  private async detectKnownPatterns(
    oracleData: LiveOracleData[],
    features: BehavioralFeatures
  ): Promise<ManipulationPattern[]> {
    const patterns: ManipulationPattern[] = [];

    // Pattern 1: Flash Loan Attack
    if (await this.detectFlashLoanAttack(oracleData, features)) {
      patterns.push({
        id: 'flash_loan_attack',
        name: 'Flash Loan Price Manipulation',
        description: 'Sudden price spike with immediate reversion, typical of flash loan attacks',
        severity: 'critical',
        confidence: 0.92,
        indicators: ['rapid_price_change', 'single_block_anomaly', 'liquidity_drain'],
        mitigationStrategies: [
          'Implement time-weighted average pricing',
          'Require multi-block confirmation',
          'Add flash loan detection circuit breaker'
        ]
      });
    }

    // Pattern 2: Coordinated Oracle Attack
    if (await this.detectCoordinatedAttack(oracleData, features)) {
      patterns.push({
        id: 'coordinated_oracle_attack',
        name: 'Coordinated Multi-Oracle Attack',
        description: 'Multiple oracle sources showing coordinated manipulation',
        severity: 'critical',
        confidence: 0.88,
        indicators: ['multi_source_deviation', 'synchronized_anomalies', 'consensus_breakdown'],
        mitigationStrategies: [
          'Increase oracle source diversity',
          'Implement outlier detection',
          'Add manual override capabilities'
        ]
      });
    }

    // Pattern 3: Gradual Price Drift
    if (await this.detectGradualDrift(oracleData, features)) {
      patterns.push({
        id: 'gradual_price_drift',
        name: 'Gradual Oracle Drift Attack',
        description: 'Slow, sustained price manipulation over extended period',
        severity: 'high',
        confidence: 0.75,
        indicators: ['sustained_deviation', 'low_volatility_drift', 'baseline_shift'],
        mitigationStrategies: [
          'Implement drift detection algorithms',
          'Regular baseline recalibration',
          'Cross-reference with external sources'
        ]
      });
    }

    // Pattern 4: Front-Running Attack
    if (await this.detectFrontRunning(oracleData, features)) {
      patterns.push({
        id: 'front_running_attack',
        name: 'Oracle Front-Running',
        description: 'Price updates being front-run by malicious actors',
        severity: 'high',
        confidence: 0.82,
        indicators: ['pre_update_activity', 'mempool_manipulation', 'mev_extraction'],
        mitigationStrategies: [
          'Implement commit-reveal schemes',
          'Add random delay to updates',
          'Use threshold cryptography'
        ]
      });
    }

    // Pattern 5: Governance Attack
    if (await this.detectGovernanceAttack(oracleData, features)) {
      patterns.push({
        id: 'governance_attack',
        name: 'Oracle Governance Manipulation',
        description: 'Manipulation through governance token attacks',
        severity: 'critical',
        confidence: 0.79,
        indicators: ['governance_changes', 'parameter_manipulation', 'admin_compromise'],
        mitigationStrategies: [
          'Implement time delays for governance changes',
          'Require multi-signature approval',
          'Add emergency pause mechanisms'
        ]
      });
    }

    return patterns;
  }

  /**
   * Calculate price volatility indicator
   */
  private calculatePriceVolatility(oracleData: LiveOracleData[]): number {
    if (oracleData.length < 2) return 0;

    const prices = oracleData.map(d => Number(d.price) / (10 ** d.decimals));
    const mean = prices.reduce((sum, p) => sum + p, 0) / prices.length;
    const variance = prices.reduce((sum, p) => sum + Math.pow(p - mean, 2), 0) / prices.length;
    const standardDeviation = Math.sqrt(variance);

    return Math.min(1.0, standardDeviation / mean); // Coefficient of variation, capped at 1.0
  }

  /**
   * Calculate volume spike indicator
   */
  private calculateVolumeSpike(current: LiveOracleData[], historical: LiveOracleData[]): number {
    if (historical.length < 10) return 0;

    // Use confidence as volume proxy
    const currentVolume = current.reduce((sum, d) => sum + d.confidence, 0) / current.length;
    const historicalVolume = historical.slice(-100).reduce((sum, d) => sum + d.confidence, 0) / Math.min(100, historical.length);

    return Math.max(0, Math.min(1.0, (currentVolume - historicalVolume) / historicalVolume));
  }

  /**
   * Calculate temporal anomaly indicator
   */
  private calculateTemporalAnomaly(oracleData: LiveOracleData[]): number {
    if (oracleData.length < 2) return 0;

    const timeDiffs = [];
    for (let i = 1; i < oracleData.length; i++) {
      timeDiffs.push(oracleData[i].timestamp - oracleData[i-1].timestamp);
    }

    const meanInterval = timeDiffs.reduce((sum, diff) => sum + diff, 0) / timeDiffs.length;
    const variance = timeDiffs.reduce((sum, diff) => sum + Math.pow(diff - meanInterval, 2), 0) / timeDiffs.length;

    return Math.min(1.0, Math.sqrt(variance) / meanInterval);
  }

  /**
   * Calculate cross-oracle deviation
   */
  private calculateCrossOracleDeviation(oracleData: LiveOracleData[]): number {
    if (oracleData.length < 2) return 0;

    const prices = oracleData.map(d => Number(d.price) / (10 ** d.decimals));
    const median = this.calculateMedian(prices);
    const deviations = prices.map(p => Math.abs(p - median) / median);

    return Math.max(...deviations);
  }

  /**
   * Calculate liquidity drop indicator
   */
  private calculateLiquidityDrop(current: LiveOracleData[], historical: LiveOracleData[]): number {
    if (historical.length < 10) return 0;

    const currentSourceCount = new Set(current.map(d => d.source)).size;
    const historicalSourceCount = Math.max(...historical.slice(-50).map((_, i, arr) =>
      new Set(arr.slice(Math.max(0, i-10), i+1).map(d => d.source)).size
    ));

    return Math.max(0, (historicalSourceCount - currentSourceCount) / historicalSourceCount);
  }

  /**
   * Calculate transaction pattern anomaly
   */
  private calculateTransactionPattern(oracleData: LiveOracleData[]): number {
    // Analyze block number patterns for unusual activity
    const blockNumbers = oracleData.map(d => d.blockNumber).filter(b => b > 0);
    if (blockNumbers.length < 2) return 0;

    const blockDiffs = [];
    for (let i = 1; i < blockNumbers.length; i++) {
      blockDiffs.push(blockNumbers[i] - blockNumbers[i-1]);
    }

    const meanBlockDiff = blockDiffs.reduce((sum, diff) => sum + diff, 0) / blockDiffs.length;
    const anomalous = blockDiffs.filter(diff => diff === 0 || diff > meanBlockDiff * 3).length;

    return anomalous / blockDiffs.length;
  }

  /**
   * Calculate network congestion indicator
   */
  private calculateNetworkCongestion(oracleData: LiveOracleData[]): number {
    // Simulate network congestion based on timestamp clustering
    const timestamps = oracleData.map(d => d.timestamp).sort((a, b) => a - b);
    if (timestamps.length < 3) return 0;

    let clusteredCount = 0;
    for (let i = 1; i < timestamps.length - 1; i++) {
      const prevDiff = timestamps[i] - timestamps[i-1];
      const nextDiff = timestamps[i+1] - timestamps[i];

      // Consider clustered if both intervals are very small
      if (prevDiff < 60000 && nextDiff < 60000) { // Less than 1 minute
        clusteredCount++;
      }
    }

    return clusteredCount / (timestamps.length - 2);
  }

  /**
   * Calculate gas spike indicator
   */
  private calculateGasSpike(oracleData: LiveOracleData[]): number {
    // Simulate gas spike detection based on transaction density
    const recentData = oracleData.filter(d =>
      Date.now() - d.timestamp < 300000 // Last 5 minutes
    );

    // High transaction density might indicate gas competition
    return Math.min(1.0, recentData.length / 20); // Normalized to max 20 updates per 5 min
  }

  /**
   * Detect flash loan attack pattern
   */
  private async detectFlashLoanAttack(
    oracleData: LiveOracleData[],
    features: BehavioralFeatures
  ): Promise<boolean> {
    // Flash loan attacks typically show:
    // 1. Extremely high price volatility
    // 2. Single block anomalies
    // 3. Immediate price reversion

    const hasHighVolatility = features.priceVolatility > 0.1; // 10% volatility
    const hasSingleBlockAnomaly = features.transactionPattern > 0.5;
    const hasTemporalAnomaly = features.temporalAnomaly > 0.3;

    return hasHighVolatility && hasSingleBlockAnomaly && hasTemporalAnomaly;
  }

  /**
   * Detect coordinated oracle attack
   */
  private async detectCoordinatedAttack(
    oracleData: LiveOracleData[],
    features: BehavioralFeatures
  ): Promise<boolean> {
    const hasHighDeviation = features.crossOracleDeviation > 0.05; // 5% deviation
    const hasMultipleSources = new Set(oracleData.map(d => d.source)).size >= 3;
    const hasLowConfidence = oracleData.some(d => d.confidence < 0.7);

    return hasHighDeviation && hasMultipleSources && hasLowConfidence;
  }

  /**
   * Detect gradual drift attack
   */
  private async detectGradualDrift(
    oracleData: LiveOracleData[],
    features: BehavioralFeatures
  ): Promise<boolean> {
    const symbol = oracleData[0]?.symbol || '';
    const baseline = this.behaviorBaselines.get(symbol);

    if (!baseline) return false;

    const hasBaselineShift = Math.abs(features.priceVolatility - baseline.priceVolatility) > 0.02;
    const hasLowVolatility = features.priceVolatility < 0.02; // Very low volatility
    const hasSustainedDeviation = features.crossOracleDeviation > 0.02;

    return hasBaselineShift && hasLowVolatility && hasSustainedDeviation;
  }

  /**
   * Detect front-running attack
   */
  private async detectFrontRunning(
    oracleData: LiveOracleData[],
    features: BehavioralFeatures
  ): Promise<boolean> {
    const hasNetworkCongestion = features.networkCongestion > 0.6;
    const hasGasSpike = features.gasSpike > 0.7;
    const hasTransactionPattern = features.transactionPattern > 0.4;

    return hasNetworkCongestion && hasGasSpike && hasTransactionPattern;
  }

  /**
   * Detect governance attack
   */
  private async detectGovernanceAttack(
    oracleData: LiveOracleData[],
    features: BehavioralFeatures
  ): Promise<boolean> {
    // Simplified governance attack detection
    const hasUnusualSourcePattern = features.liquidityDrop > 0.5;
    const hasConfidenceAnomaly = oracleData.some(d => d.confidence > 0.99 || d.confidence < 0.3);

    return hasUnusualSourcePattern && hasConfidenceAnomaly;
  }

  /**
   * Generate alerts based on detected patterns and ML predictions
   */
  private generateAlerts(
    oracleData: LiveOracleData[],
    patterns: ManipulationPattern[],
    mlPrediction: MLModelPrediction
  ): ManipulationAlert[] {
    const alerts: ManipulationAlert[] = [];

    // Generate alerts for each detected pattern
    patterns.forEach(pattern => {
      alerts.push({
        id: `alert_${pattern.id}_${Date.now()}`,
        symbol: oracleData[0]?.symbol || 'UNKNOWN',
        detectionType: this.mapPatternToDetectionType(pattern.id),
        severity: pattern.severity,
        confidence: pattern.confidence,
        priceImpact: this.calculatePriceImpact(oracleData),
        timeDetected: Date.now(),
        affectedValue: this.estimateAffectedValue(oracleData[0]?.symbol || '', this.calculatePriceImpact(oracleData)),
        mitigationActions: pattern.mitigationStrategies
      });
    });

    // Generate ML-based alert if high manipulation probability
    if (mlPrediction.manipulationProbability > 0.7) {
      alerts.push({
        id: `ml_alert_${Date.now()}`,
        symbol: oracleData[0]?.symbol || 'UNKNOWN',
        detectionType: 'volume_anomaly',
        severity: mlPrediction.manipulationProbability > 0.9 ? 'critical' : 'high',
        confidence: mlPrediction.confidence,
        priceImpact: this.calculatePriceImpact(oracleData),
        timeDetected: Date.now(),
        affectedValue: this.estimateAffectedValue(oracleData[0]?.symbol || '', this.calculatePriceImpact(oracleData)),
        mitigationActions: mlPrediction.recommendedActions
      });
    }

    return alerts;
  }

  /**
   * Calculate overall risk score
   */
  private calculateRiskScore(
    patterns: ManipulationPattern[],
    mlPrediction: MLModelPrediction,
    features: BehavioralFeatures
  ): number {
    // Weight different factors
    const patternScore = patterns.reduce((sum, p) => {
      const severityWeight = { low: 0.2, medium: 0.5, high: 0.8, critical: 1.0 }[p.severity];
      return sum + (severityWeight * p.confidence);
    }, 0);

    const mlScore = mlPrediction.manipulationProbability * mlPrediction.confidence;

    const featureScore = (
      features.priceVolatility * 0.3 +
      features.crossOracleDeviation * 0.25 +
      features.temporalAnomaly * 0.2 +
      features.volumeSpike * 0.15 +
      features.liquidityDrop * 0.1
    );

    // Combine scores with weights
    return Math.min(1.0, patternScore * 0.4 + mlScore * 0.4 + featureScore * 0.2);
  }

  /**
   * Helper methods
   */
  private updateHistoricalData(oracleData: LiveOracleData[]): void {
    oracleData.forEach(data => {
      if (!this.historicalData.has(data.symbol)) {
        this.historicalData.set(data.symbol, []);
      }

      const history = this.historicalData.get(data.symbol)!;
      history.push(data);

      // Maintain max history length
      if (history.length > this.maxHistoryLength) {
        history.shift();
      }
    });
  }

  private initializeBehaviorBaselines(): void {
    // Initialize with typical stablecoin baselines
    const stablecoinBaseline: BehavioralFeatures = {
      priceVolatility: 0.005, // 0.5% typical volatility
      volumeSpike: 0.1,
      temporalAnomaly: 0.1,
      crossOracleDeviation: 0.002, // 0.2% typical deviation
      liquidityDrop: 0.05,
      transactionPattern: 0.1,
      networkCongestion: 0.2,
      gasSpike: 0.15
    };

    ['cUSD', 'cEUR', 'cREAL', 'cKES'].forEach(symbol => {
      this.behaviorBaselines.set(symbol, { ...stablecoinBaseline });
    });
  }

  private calculateMedian(numbers: number[]): number {
    const sorted = numbers.slice().sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
  }

  private calculatePriceImpact(oracleData: LiveOracleData[]): number {
    if (oracleData.length < 2) return 0;

    const prices = oracleData.map(d => Number(d.price) / (10 ** d.decimals));
    const min = Math.min(...prices);
    const max = Math.max(...prices);

    return (max - min) / min;
  }

  private estimateAffectedValue(symbol: string, priceImpact: number): number {
    // Estimate based on typical protocol sizes
    const estimatedExposure: Record<string, number> = {
      'cUSD': 25000000,
      'cEUR': 15000000,
      'cREAL': 10000000,
      'default': 1000000
    };

    const exposure = estimatedExposure[symbol] || estimatedExposure['default'];
    return exposure * priceImpact;
  }

  private mapPatternToDetectionType(patternId: string): 'price_spike' | 'consensus_break' | 'volume_anomaly' | 'flash_attack' {
    const mapping: Record<string, 'price_spike' | 'consensus_break' | 'volume_anomaly' | 'flash_attack'> = {
      'flash_loan_attack': 'flash_attack',
      'coordinated_oracle_attack': 'consensus_break',
      'gradual_price_drift': 'price_spike',
      'front_running_attack': 'volume_anomaly',
      'governance_attack': 'consensus_break'
    };

    return mapping[patternId] || 'price_spike';
  }

  private getDefaultPrediction(): MLModelPrediction {
    return {
      manipulationProbability: 0,
      confidence: 1.0,
      primaryIndicators: [],
      riskScore: 0,
      recommendedActions: []
    };
  }
}

/**
 * Machine Learning Model for Manipulation Detection
 */
class ManipulationMLModel {
  private weights: Record<string, number>;
  private threshold: number = 0.7;

  constructor() {
    // Initialize with trained weights (simplified for demo)
    this.weights = {
      priceVolatility: 0.25,
      volumeSpike: 0.20,
      temporalAnomaly: 0.15,
      crossOracleDeviation: 0.20,
      liquidityDrop: 0.10,
      transactionPattern: 0.05,
      networkCongestion: 0.03,
      gasSpike: 0.02
    };
  }

  /**
   * Predict manipulation probability using ML model
   */
  async predict(features: BehavioralFeatures, oracleData: LiveOracleData[]): Promise<MLModelPrediction> {
    // Calculate weighted score
    const score = Object.entries(features).reduce((sum, [key, value]) => {
      const weight = this.weights[key] || 0;
      return sum + (weight * value);
    }, 0);

    const manipulationProbability = Math.min(1.0, score);
    const confidence = this.calculateConfidence(features, oracleData);

    // Identify primary indicators
    const primaryIndicators = Object.entries(features)
      .filter(([key, value]) => value > 0.3 && this.weights[key] > 0.1)
      .map(([key]) => key);

    // Generate recommended actions
    const recommendedActions = this.generateRecommendations(features, manipulationProbability);

    return {
      manipulationProbability,
      confidence,
      primaryIndicators,
      riskScore: manipulationProbability * confidence,
      recommendedActions
    };
  }

  private calculateConfidence(features: BehavioralFeatures, oracleData: LiveOracleData[]): number {
    const dataQuality = oracleData.length > 3 ? 1.0 : oracleData.length / 3;
    const sourceQuality = new Set(oracleData.map(d => d.source)).size / 4; // Expect 4 sources
    const recencyQuality = oracleData.every(d => Date.now() - d.timestamp < 300000) ? 1.0 : 0.7;

    return Math.min(1.0, (dataQuality + sourceQuality + recencyQuality) / 3);
  }

  private generateRecommendations(features: BehavioralFeatures, probability: number): string[] {
    const recommendations: string[] = [];

    if (probability > 0.8) {
      recommendations.push('Immediate circuit breaker activation');
      recommendations.push('Manual verification required');
    }

    if (features.priceVolatility > 0.1) {
      recommendations.push('Implement time-weighted average pricing');
    }

    if (features.crossOracleDeviation > 0.05) {
      recommendations.push('Increase oracle source diversity');
    }

    if (features.liquidityDrop > 0.3) {
      recommendations.push('Verify oracle availability');
    }

    return recommendations;
  }
}

/**
 * Demo function for advanced manipulation detection
 */
export async function demonstrateAdvancedManipulationDetection(): Promise<void> {
  console.log('🧠 Advanced Manipulation Detection Demo\n');

  const detector = new AdvancedManipulationDetector();

  // Simulate oracle data with manipulation patterns
  const normalData: LiveOracleData[] = [
    {
      symbol: 'cUSD',
      price: BigInt('1000000000000000000'), // $1.00
      decimals: 18,
      timestamp: Date.now() - 60000,
      blockNumber: 1000000,
      source: 'chainlink',
      network: 'ethereum',
      confidence: 0.95
    },
    {
      symbol: 'cUSD',
      price: BigInt('1001000000000000000'), // $1.001
      decimals: 18,
      timestamp: Date.now() - 30000,
      blockNumber: 1000001,
      source: 'band',
      network: 'ethereum',
      confidence: 0.92
    }
  ];

  const manipulatedData: LiveOracleData[] = [
    {
      symbol: 'cUSD',
      price: BigInt('1200000000000000000'), // $1.20 (20% spike!)
      decimals: 18,
      timestamp: Date.now(),
      blockNumber: 1000002,
      source: 'chainlink',
      network: 'ethereum',
      confidence: 0.98
    },
    {
      symbol: 'cUSD',
      price: BigInt('1000000000000000000'), // Back to $1.00
      decimals: 18,
      timestamp: Date.now() + 1000,
      blockNumber: 1000002, // Same block!
      source: 'mento',
      network: 'celo',
      confidence: 0.95
    }
  ];

  console.log('1️⃣ Analyzing normal oracle behavior...');
  const normalResult = await detector.detectManipulation(normalData);
  console.log(`Normal Risk Score: ${(normalResult.riskScore * 100).toFixed(1)}%`);
  console.log(`Alerts: ${normalResult.alerts.length}`);
  console.log(`Patterns: ${normalResult.patterns.length}`);

  console.log('\n2️⃣ Analyzing suspicious oracle behavior...');
  const manipulatedResult = await detector.detectManipulation(manipulatedData);
  console.log(`Manipulation Risk Score: ${(manipulatedResult.riskScore * 100).toFixed(1)}%`);
  console.log(`Alerts: ${manipulatedResult.alerts.length}`);
  console.log(`Patterns Detected: ${manipulatedResult.patterns.length}`);

  if (manipulatedResult.patterns.length > 0) {
    console.log('\n🚨 Detected Manipulation Patterns:');
    manipulatedResult.patterns.forEach(pattern => {
      console.log(`  - ${pattern.name} (${pattern.severity}): ${(pattern.confidence * 100).toFixed(1)}% confidence`);
    });
  }

  console.log('\n🤖 ML Model Prediction:');
  console.log(`  Manipulation Probability: ${(manipulatedResult.mlPrediction.manipulationProbability * 100).toFixed(1)}%`);
  console.log(`  Confidence: ${(manipulatedResult.mlPrediction.confidence * 100).toFixed(1)}%`);
  console.log(`  Primary Indicators: ${manipulatedResult.mlPrediction.primaryIndicators.join(', ')}`);

  console.log('\n✅ Advanced Manipulation Detection Demo completed');
}

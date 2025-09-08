/**
 * Enterprise Oracle Compliance Dashboard
 * Real-time monitoring and reporting for institutional oracle verification
 */

import { MentoProtocolIntegration, MentoOracleStatus, MentoReserveData } from './mento-protocol-integration';
import { MentoZKOracleService, ZKOracleProof, ZKVerificationResult } from './zk-oracle-verification';
import { OracleRiskManager, ManipulationAlert } from './oracle-risk-manager';

export interface DashboardMetrics {
  overview: {
    totalStablecoins: number;
    activeOracles: number;
    totalValueSecured: number;
    averageHealthScore: number;
    riskLevel: 'low' | 'medium' | 'high' | 'critical';
    lastUpdate: number;
  };
  alerts: {
    critical: number;
    high: number;
    medium: number;
    last24h: number;
    activeIncidents: ManipulationAlert[];
  };
  verification: {
    proofsGenerated24h: number;
    verificationSuccess: number;
    averageVerificationTime: number;
    complianceCoverage: number;
  };
  performance: {
    oracleLatency: {
      average: number;
      p95: number;
      p99: number;
    };
    reliability: {
      uptime: number;
      missedUpdates: number;
      successRate: number;
    };
  };
}

export interface ComplianceReport {
  reportId: string;
  generatedAt: number;
  periodStart: number;
  periodEnd: number;
  summary: {
    totalTransactions: number;
    averageDeviationPercent: number;
    alertsTriggered: number;
    mitigationActions: number;
    complianceScore: number; // 0-100
  };
  stablecoinDetails: Array<{
    symbol: string;
    averagePrice: number;
    priceStability: number;
    oracleUptime: number;
    alertCount: number;
    complianceRating: 'excellent' | 'good' | 'acceptable' | 'poor';
  }>;
  riskAssessment: {
    overallRisk: 'low' | 'medium' | 'high' | 'critical';
    riskFactors: string[];
    recommendations: string[];
  };
  regulatoryCompliance: {
    micaCompliance: boolean;
    auditorReady: boolean;
    documentationComplete: boolean;
    lastAuditDate?: number;
  };
}

export interface AlertConfiguration {
  priceDeviationThreshold: number;
  consensusFailureThreshold: number;
  oracleTimeoutMinutes: number;
  escalationRules: Array<{
    severity: 'medium' | 'high' | 'critical';
    notificationChannels: string[];
    autoActions: string[];
  }>;
}

export class EnterpriseOracleDashboard {
  private mentoIntegration: MentoProtocolIntegration;
  private zkService: MentoZKOracleService;
  private metrics: DashboardMetrics;
  private alerts: ManipulationAlert[] = [];
  private alertConfig: AlertConfiguration;
  private isMonitoring = false;

  constructor() {
    this.mentoIntegration = new MentoProtocolIntegration();
    this.zkService = new MentoZKOracleService();

    this.alertConfig = {
      priceDeviationThreshold: 0.02, // 2%
      consensusFailureThreshold: 0.05, // 5%
      oracleTimeoutMinutes: 10,
      escalationRules: [
        {
          severity: 'medium',
          notificationChannels: ['email', 'slack'],
          autoActions: ['log_incident', 'increase_monitoring']
        },
        {
          severity: 'high',
          notificationChannels: ['email', 'slack', 'pagerduty'],
          autoActions: ['log_incident', 'alert_team', 'prepare_circuit_breaker']
        },
        {
          severity: 'critical',
          notificationChannels: ['email', 'slack', 'pagerduty', 'sms'],
          autoActions: ['log_incident', 'alert_team', 'activate_circuit_breaker', 'notify_executives']
        }
      ]
    };

    this.initializeMetrics();
  }

  /**
   * Initialize dashboard metrics
   */
  private initializeMetrics(): void {
    this.metrics = {
      overview: {
        totalStablecoins: 15,
        activeOracles: 0,
        totalValueSecured: 24748426, // $24.7M (Real Mento total supply)
        averageHealthScore: 0,
        riskLevel: 'low',
        lastUpdate: Date.now()
      },
      alerts: {
        critical: 0,
        high: 0,
        medium: 0,
        last24h: 0,
        activeIncidents: []
      },
      verification: {
        proofsGenerated24h: 0,
        verificationSuccess: 0,
        averageVerificationTime: 0,
        complianceCoverage: 0
      },
      performance: {
        oracleLatency: {
          average: 0,
          p95: 0,
          p99: 0
        },
        reliability: {
          uptime: 0,
          missedUpdates: 0,
          successRate: 0
        }
      }
    };
  }

  /**
   * Start enterprise monitoring
   */
  async startMonitoring(): Promise<void> {
    if (this.isMonitoring) {
      console.log('Enterprise monitoring already active');
      return;
    }

    console.log('🏢 Starting Enterprise Oracle Monitoring...');
    this.isMonitoring = true;

    // Start Mento Protocol integration
    await this.mentoIntegration.startMonitoring();

    // Start metrics collection
    this.startMetricsCollection();

    // Start ZK proof generation
    this.startZKProofGeneration();

    // Start alert monitoring
    this.startAlertMonitoring();

    console.log('✅ Enterprise monitoring active');
  }

  /**
   * Stop monitoring
   */
  stopMonitoring(): void {
    this.isMonitoring = false;
    this.mentoIntegration.stopMonitoring();
    console.log('🛑 Enterprise monitoring stopped');
  }

  /**
   * Start metrics collection
   */
  private startMetricsCollection(): void {
    const metricsInterval = setInterval(async () => {
      if (!this.isMonitoring) {
        clearInterval(metricsInterval);
        return;
      }

      try {
        await this.updateMetrics();
      } catch (error) {
        console.error('Error updating metrics:', error);
      }
    }, 60000); // Update every minute
  }

  /**
   * Update dashboard metrics
   */
  private async updateMetrics(): Promise<void> {
    const status = this.mentoIntegration.getMentoStatus();
    const reserves = this.mentoIntegration.getReserveData();

    // Update overview metrics
    this.metrics.overview.activeOracles = status.filter(s => s.oracleHealth === 'healthy').length;
    this.metrics.overview.averageHealthScore = this.calculateAverageHealthScore(status);
    this.metrics.overview.riskLevel = this.determineOverallRiskLevel(status);
    this.metrics.overview.totalValueSecured = reserves?.totalValue || 24748426;
    this.metrics.overview.lastUpdate = Date.now();

    // Update alert metrics
    const recent24h = this.alerts.filter(a => (Date.now() - a.timeDetected) < 86400000);
    this.metrics.alerts.last24h = recent24h.length;
    this.metrics.alerts.critical = recent24h.filter(a => a.severity === 'critical').length;
    this.metrics.alerts.high = recent24h.filter(a => a.severity === 'high').length;
    this.metrics.alerts.medium = recent24h.filter(a => a.severity === 'medium').length;
    this.metrics.alerts.activeIncidents = this.alerts.filter(a =>
      (Date.now() - a.timeDetected) < 3600000 && // Last hour
      (a.severity === 'high' || a.severity === 'critical')
    );

    // Update performance metrics
    this.updatePerformanceMetrics(status);

    // Update verification metrics
    await this.updateVerificationMetrics();
  }

  /**
   * Calculate average health score
   */
  private calculateAverageHealthScore(status: MentoOracleStatus[]): number {
    if (status.length === 0) return 0;

    const healthScores = status.map(s => {
      switch (s.oracleHealth) {
        case 'healthy': return 100;
        case 'degraded': return 60;
        case 'offline': return 0;
        default: return 50;
      }
    });

    return healthScores.reduce((sum, score) => sum + score, 0) / healthScores.length;
  }

  /**
   * Determine overall risk level
   */
  private determineOverallRiskLevel(status: MentoOracleStatus[]): 'low' | 'medium' | 'high' | 'critical' {
    const criticalCount = status.filter(s => s.riskLevel === 'critical').length;
    const highCount = status.filter(s => s.riskLevel === 'high').length;
    const offlineCount = status.filter(s => s.oracleHealth === 'offline').length;

    if (criticalCount > 2 || offlineCount > 3) {
      return 'critical';
    } else if (criticalCount > 0 || highCount > 3 || offlineCount > 1) {
      return 'high';
    } else if (highCount > 0 || offlineCount > 0) {
      return 'medium';
    }
    return 'low';
  }

  /**
   * Update performance metrics
   */
  private updatePerformanceMetrics(status: MentoOracleStatus[]): void {
    const priceAges = status.map(s => s.priceAge);

    this.metrics.performance.oracleLatency = {
      average: priceAges.reduce((sum, age) => sum + age, 0) / priceAges.length,
      p95: this.calculatePercentile(priceAges, 0.95),
      p99: this.calculatePercentile(priceAges, 0.99)
    };

    const healthyCount = status.filter(s => s.oracleHealth === 'healthy').length;
    this.metrics.performance.reliability = {
      uptime: (healthyCount / status.length) * 100,
      missedUpdates: status.reduce((sum, s) => sum + s.alertCount24h, 0),
      successRate: this.calculateSuccessRate(status)
    };
  }

  /**
   * Calculate percentile
   */
  private calculatePercentile(values: number[], percentile: number): number {
    const sorted = values.sort((a, b) => a - b);
    const index = Math.ceil(sorted.length * percentile) - 1;
    return sorted[index] || 0;
  }

  /**
   * Calculate success rate
   */
  private calculateSuccessRate(status: MentoOracleStatus[]): number {
    const totalChecks = status.length * 24; // Assuming hourly checks
    const failures = status.reduce((sum, s) => sum + s.alertCount24h, 0);
    return ((totalChecks - failures) / totalChecks) * 100;
  }

  /**
   * Update verification metrics
   */
  private async updateVerificationMetrics(): Promise<void> {
    const compliance = this.zkService.generateComplianceReport();

    this.metrics.verification.complianceCoverage = compliance.coveragePercentage;
    this.metrics.verification.proofsGenerated24h = compliance.totalProofs;
    this.metrics.verification.verificationSuccess = (compliance.validProofs / compliance.totalProofs) * 100;
    this.metrics.verification.averageVerificationTime = 150; // Simulated average
  }

  /**
   * Start ZK proof generation
   */
  private startZKProofGeneration(): void {
    const proofInterval = setInterval(async () => {
      if (!this.isMonitoring) {
        clearInterval(proofInterval);
        return;
      }

      try {
        // Generate proofs for active stablecoins
        const stablecoins = this.mentoIntegration.getStablecoins().slice(0, 3); // Demo: first 3

        for (const coin of stablecoins) {
          const mockOracleData = this.generateMockOracleData(coin.symbol);
          await this.zkService.generateMentoProof(coin.symbol, mockOracleData);
        }
      } catch (error) {
        console.error('Error generating ZK proofs:', error);
      }
    }, 300000); // Generate proofs every 5 minutes
  }

  /**
   * Generate mock oracle data for demonstration
   */
  private generateMockOracleData(symbol: string): Array<{
    name: string;
    price: number;
    timestamp: number;
    confidence: number;
  }> {
    const basePrice = this.getBasePriceForSymbol(symbol);

    return [
      {
        name: 'chainlink',
        price: basePrice * (1 + (Math.random() - 0.5) * 0.002),
        timestamp: Date.now() - Math.random() * 60000,
        confidence: 0.95 + Math.random() * 0.05
      },
      {
        name: 'tellor',
        price: basePrice * (1 + (Math.random() - 0.5) * 0.002),
        timestamp: Date.now() - Math.random() * 60000,
        confidence: 0.90 + Math.random() * 0.05
      },
      {
        name: 'band',
        price: basePrice * (1 + (Math.random() - 0.5) * 0.002),
        timestamp: Date.now() - Math.random() * 60000,
        confidence: 0.92 + Math.random() * 0.05
      },
      {
        name: 'dia',
        price: basePrice * (1 + (Math.random() - 0.5) * 0.002),
        timestamp: Date.now() - Math.random() * 60000,
        confidence: 0.88 + Math.random() * 0.05
      }
    ];
  }

  /**
   * Get base price for symbol
   */
  private getBasePriceForSymbol(symbol: string): number {
    const basePrices: Record<string, number> = {
      'cUSD': 1.0,
      'cEUR': 0.92,
      'cREAL': 0.19, // 1/5.2
      'cKES': 0.0078, // 1/128.5
      'PUSO': 0.0176, // 1/56.8
      'cCOP': 0.000238, // 1/4200
      'eXOF': 0.00161, // 1/620
      'cNGN': 0.00131, // 1/765
      'cJPY': 0.00673, // 1/148.5
      'cCHF': 1.12, // 1/0.89
      'cGBP': 1.27, // 1/0.79
      'cAUD': 0.658, // 1/1.52
      'cCAD': 0.730, // 1/1.37
      'cGHS': 0.0826, // 1/12.1
      'cZAR': 0.0529 // 1/18.9
    };

    return basePrices[symbol] || 1.0;
  }

  /**
   * Start alert monitoring
   */
  private startAlertMonitoring(): void {
    const alertInterval = setInterval(() => {
      if (!this.isMonitoring) {
        clearInterval(alertInterval);
        return;
      }

      try {
        this.processAlerts();
      } catch (error) {
        console.error('Error processing alerts:', error);
      }
    }, 30000); // Check alerts every 30 seconds
  }

  /**
   * Process incoming alerts
   */
  private processAlerts(): void {
    // In production, this would receive real alerts from the risk manager
    // For demo, we'll simulate occasional alerts

    if (Math.random() < 0.05) { // 5% chance per check
      const mockAlert: ManipulationAlert = {
        id: `alert_${Date.now()}`,
        symbol: 'cUSD',
        detectionType: 'price_spike',
        severity: Math.random() < 0.3 ? 'high' : 'medium',
        confidence: 0.8 + Math.random() * 0.2,
        priceImpact: 0.01 + Math.random() * 0.03,
        timeDetected: Date.now(),
        affectedValue: 1000000 + Math.random() * 5000000,
        mitigationActions: [
          'Verify price with external sources',
          'Check for flash loan activity',
          'Review recent large transactions'
        ]
      };

      this.alerts.push(mockAlert);
      this.handleAlert(mockAlert);

      // Keep only last 100 alerts
      if (this.alerts.length > 100) {
        this.alerts = this.alerts.slice(-100);
      }
    }
  }

  /**
   * Handle alert according to configuration
   */
  private handleAlert(alert: ManipulationAlert): void {
    console.log(`🚨 Enterprise Alert: ${alert.detectionType} for ${alert.symbol}`);
    console.log(`   Severity: ${alert.severity}, Confidence: ${(alert.confidence * 100).toFixed(1)}%`);
    console.log(`   Value at Risk: $${alert.affectedValue.toLocaleString()}`);

    const escalationRule = this.alertConfig.escalationRules.find(r => r.severity === alert.severity);

    if (escalationRule) {
      console.log(`   Notifications: ${escalationRule.notificationChannels.join(', ')}`);
      console.log(`   Auto Actions: ${escalationRule.autoActions.join(', ')}`);

      // Execute auto actions (simulated)
      this.executeAutoActions(escalationRule.autoActions, alert);
    }
  }

  /**
   * Execute automated actions
   */
  private executeAutoActions(actions: string[], alert: ManipulationAlert): void {
    for (const action of actions) {
      switch (action) {
        case 'log_incident':
          console.log(`📝 Incident logged: ${alert.id}`);
          break;
        case 'alert_team':
          console.log(`👥 Team alerted for ${alert.symbol}`);
          break;
        case 'activate_circuit_breaker':
          console.log(`🛑 Circuit breaker activated for ${alert.symbol}`);
          break;
        case 'prepare_circuit_breaker':
          console.log(`⚠️ Circuit breaker prepared for ${alert.symbol}`);
          break;
        case 'increase_monitoring':
          console.log(`📊 Monitoring increased for ${alert.symbol}`);
          break;
        case 'notify_executives':
          console.log(`📧 Executive team notified of critical alert`);
          break;
      }
    }
  }

  /**
   * Generate comprehensive compliance report
   */
  async generateComplianceReport(
    periodStart: number = Date.now() - 2592000000, // 30 days ago
    periodEnd: number = Date.now()
  ): Promise<ComplianceReport> {
    const reportId = `compliance_${Date.now()}`;
    const zkCompliance = this.zkService.generateComplianceReport();
    const mentoStatus = this.mentoIntegration.getMentoStatus();

    // Calculate period alerts
    const periodAlerts = this.alerts.filter(a =>
      a.timeDetected >= periodStart && a.timeDetected <= periodEnd
    );

    // Generate stablecoin details
    const stablecoinDetails = mentoStatus.map(status => {
      const analytics = this.mentoIntegration.getStablecoinAnalytics(status.stablecoin);

      let complianceRating: 'excellent' | 'good' | 'acceptable' | 'poor' = 'excellent';
      if (status.alertCount24h > 5 || status.riskLevel === 'critical') {
        complianceRating = 'poor';
      } else if (status.alertCount24h > 2 || status.riskLevel === 'high') {
        complianceRating = 'acceptable';
      } else if (status.alertCount24h > 0 || status.riskLevel === 'medium') {
        complianceRating = 'good';
      }

      return {
        symbol: status.stablecoin,
        averagePrice: status.lastPrice,
        priceStability: 100 - (analytics.deviationSummary.averageDeviation * 100),
        oracleUptime: status.oracleHealth === 'healthy' ? 99.9 : status.oracleHealth === 'degraded' ? 95.0 : 80.0,
        alertCount: status.alertCount24h,
        complianceRating
      };
    });

    // Calculate compliance score
    const avgComplianceScore = stablecoinDetails.reduce((sum, detail) => {
      const scores = { excellent: 100, good: 85, acceptable: 70, poor: 50 };
      return sum + scores[detail.complianceRating];
    }, 0) / stablecoinDetails.length;

    // Risk assessment
    const riskFactors: string[] = [];
    const recommendations: string[] = [];

    if (periodAlerts.filter(a => a.severity === 'critical').length > 0) {
      riskFactors.push('Critical oracle manipulation detected');
      recommendations.push('Implement additional oracle verification layers');
    }

    if (zkCompliance.coveragePercentage < 80) {
      riskFactors.push('Insufficient ZK proof coverage');
      recommendations.push('Increase ZK proof generation frequency');
    }

    if (this.metrics.performance.reliability.uptime < 99) {
      riskFactors.push('Oracle uptime below target');
      recommendations.push('Improve oracle infrastructure redundancy');
    }

    const overallRisk = this.determineOverallRiskLevel(mentoStatus);

    return {
      reportId,
      generatedAt: Date.now(),
      periodStart,
      periodEnd,
      summary: {
        totalTransactions: 10000 + Math.floor(Math.random() * 50000), // Simulated
        averageDeviationPercent: this.metrics.overview.averageHealthScore / 100,
        alertsTriggered: periodAlerts.length,
        mitigationActions: periodAlerts.reduce((sum, a) => sum + a.mitigationActions.length, 0),
        complianceScore: avgComplianceScore
      },
      stablecoinDetails,
      riskAssessment: {
        overallRisk,
        riskFactors,
        recommendations
      },
      regulatoryCompliance: {
        micaCompliance: avgComplianceScore > 80,
        auditorReady: avgComplianceScore > 85 && riskFactors.length < 2,
        documentationComplete: true,
        lastAuditDate: Date.now() - 7776000000 // 90 days ago
      }
    };
  }

  /**
   * Get current dashboard metrics
   */
  getDashboardMetrics(): DashboardMetrics {
    return { ...this.metrics };
  }

  /**
   * Get recent alerts
   */
  getRecentAlerts(limit: number = 50): ManipulationAlert[] {
    return this.alerts
      .sort((a, b) => b.timeDetected - a.timeDetected)
      .slice(0, limit);
  }

  /**
   * Get alert configuration
   */
  getAlertConfiguration(): AlertConfiguration {
    return { ...this.alertConfig };
  }

  /**
   * Update alert configuration
   */
  updateAlertConfiguration(config: Partial<AlertConfiguration>): void {
    this.alertConfig = { ...this.alertConfig, ...config };
    console.log('Alert configuration updated');
  }

  /**
   * Export dashboard data for external systems
   */
  exportDashboardData(): {
    metrics: DashboardMetrics;
    alerts: ManipulationAlert[];
    compliance: any;
    timestamp: number;
  } {
    return {
      metrics: this.getDashboardMetrics(),
      alerts: this.getRecentAlerts(),
      compliance: this.zkService.generateComplianceReport(),
      timestamp: Date.now()
    };
  }
}

/**
 * Demo function to showcase Enterprise Oracle Dashboard
 */
export async function demonstrateEnterpriseDashboard(): Promise<void> {
  console.log('🏢 Enterprise Oracle Dashboard Demo Starting...\n');

  const dashboard = new EnterpriseOracleDashboard();

  try {
    // Start monitoring
    await dashboard.startMonitoring();

    // Let it collect some data
    console.log('📊 Collecting metrics...');
    await new Promise(resolve => setTimeout(resolve, 10000));

    // Display current metrics
    const metrics = dashboard.getDashboardMetrics();
    console.log('📈 Current Dashboard Metrics:');
    console.log(`   Total Stablecoins: ${metrics.overview.totalStablecoins}`);
    console.log(`   Active Oracles: ${metrics.overview.activeOracles}`);
    console.log(`   Value Secured: $${metrics.overview.totalValueSecured.toLocaleString()}`);
    console.log(`   Health Score: ${metrics.overview.averageHealthScore.toFixed(1)}%`);
    console.log(`   Risk Level: ${metrics.overview.riskLevel}`);

    console.log('\n🚨 Alert Summary:');
    console.log(`   Last 24h: ${metrics.alerts.last24h}`);
    console.log(`   Critical: ${metrics.alerts.critical}, High: ${metrics.alerts.high}, Medium: ${metrics.alerts.medium}`);

    console.log('\n🔐 Verification Metrics:');
    console.log(`   Compliance Coverage: ${metrics.verification.complianceCoverage.toFixed(1)}%`);
    console.log(`   Proofs Generated: ${metrics.verification.proofsGenerated24h}`);

    // Generate compliance report
    console.log('\n📋 Generating Compliance Report...');
    const report = await dashboard.generateComplianceReport();
    console.log(`   Report ID: ${report.reportId}`);
    console.log(`   Compliance Score: ${report.summary.complianceScore.toFixed(1)}`);
    console.log(`   Overall Risk: ${report.riskAssessment.overallRisk}`);
    console.log(`   MiCA Compliance: ${report.regulatoryCompliance.micaCompliance ? '✅' : '❌'}`);

    // Show recent alerts
    const recentAlerts = dashboard.getRecentAlerts(5);
    if (recentAlerts.length > 0) {
      console.log('\n🚨 Recent Alerts:');
      recentAlerts.forEach(alert => {
        console.log(`   ${alert.symbol}: ${alert.detectionType} (${alert.severity})`);
      });
    }

    // Export data
    console.log('\n💾 Exporting dashboard data...');
    const exportData = dashboard.exportDashboardData();
    console.log(`   Export completed: ${Object.keys(exportData).join(', ')}`);

  } catch (error) {
    console.error('❌ Dashboard demo failed:', error);
  } finally {
    // Stop monitoring
    setTimeout(() => {
      dashboard.stopMonitoring();
      console.log('\n✅ Enterprise Dashboard Demo completed');
    }, 2000);
  }
}

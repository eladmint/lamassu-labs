/**
 * TrustWrapper Enterprise Gateway
 * API gateway for accessing protected enterprise features
 * Implements authentication, rate limiting, and usage tracking
 */

export interface EnterpriseConfig {
  apiKey: string;
  tier: 'professional' | 'enterprise';
  endpoint?: string;
}

export interface AdvancedVerificationRequest {
  content: string;
  context?: Record<string, any>;
  options?: {
    includeExplanation?: boolean;
    confidenceThreshold?: number;
    modelEnsemble?: string[];
  };
}

export interface AdvancedVerificationResult {
  verified: boolean;
  confidence: number;
  riskScore: number;
  explanation?: string;
  metadata: {
    models_used: string[];
    processing_time_ms: number;
    tier: string;
  };
}

export class TrustWrapperEnterpriseGateway {
  private config: EnterpriseConfig;
  private baseUrl: string;

  constructor(config: EnterpriseConfig) {
    this.config = config;
    this.baseUrl = config.endpoint || 'https://api.trustwrapper.com/v1';
  }

  /**
   * Advanced AI verification using enterprise algorithms
   * Requires Professional or Enterprise tier
   */
  async verifyAdvanced(request: AdvancedVerificationRequest): Promise<AdvancedVerificationResult> {
    return this.makeAuthenticatedRequest('/verify/advanced', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Oracle manipulation detection
   * Requires Enterprise tier
   */
  async detectOracleManipulation(oracleData: any): Promise<{
    manipulation_detected: boolean;
    risk_level: 'low' | 'medium' | 'high' | 'critical';
    confidence: number;
    patterns_detected: string[];
  }> {
    this.validateTier(['enterprise']);
    
    return this.makeAuthenticatedRequest('/oracle/detect-manipulation', {
      method: 'POST',
      body: JSON.stringify({ oracle_data: oracleData }),
    });
  }

  /**
   * Enterprise compliance reporting
   * Requires Enterprise tier
   */
  async generateComplianceReport(config: {
    period: string;
    standards: string[];
    includeAuditTrail?: boolean;
  }): Promise<{
    compliance_score: number;
    violations: any[];
    recommendations: string[];
    audit_trail?: any[];
  }> {
    this.validateTier(['enterprise']);
    
    return this.makeAuthenticatedRequest('/compliance/report', {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  /**
   * Custom model training
   * Requires Enterprise tier with custom model license
   */
  async trainCustomModel(trainingData: {
    examples: any[];
    model_type: string;
    training_config: Record<string, any>;
  }): Promise<{
    model_id: string;
    training_status: 'started' | 'completed' | 'failed';
    estimated_completion?: string;
  }> {
    this.validateTier(['enterprise']);
    
    return this.makeAuthenticatedRequest('/models/train', {
      method: 'POST',
      body: JSON.stringify(trainingData),
    });
  }

  private async makeAuthenticatedRequest(endpoint: string, options: RequestInit): Promise<any> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
        'X-TrustWrapper-Tier': this.config.tier,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(`TrustWrapper API Error: ${response.status} - ${error.error || error.message}`);
    }

    return response.json();
  }

  private validateTier(requiredTiers: string[]): void {
    if (!requiredTiers.includes(this.config.tier)) {
      throw new Error(`Feature requires ${requiredTiers.join(' or ')} tier. Current tier: ${this.config.tier}`);
    }
  }
}

/**
 * Factory function for creating TrustWrapper client with appropriate tier
 */
export function createTrustWrapper(config: EnterpriseConfig): TrustWrapperEnterpriseGateway {
  return new TrustWrapperEnterpriseGateway(config);
}

/**
 * Usage examples for different tiers
 */
export const UsageExamples = {
  professional: `
    // Professional tier - Advanced verification only
    const client = createTrustWrapper({
      apiKey: 'tw_prof_...',
      tier: 'professional'
    });
    
    const result = await client.verifyAdvanced({
      content: "Trading decision text",
      options: { includeExplanation: true }
    });
  `,
  
  enterprise: `
    // Enterprise tier - All features available
    const client = createTrustWrapper({
      apiKey: 'tw_ent_...',
      tier: 'enterprise'
    });
    
    // Advanced verification
    const verification = await client.verifyAdvanced({
      content: "Complex trading scenario",
      options: { modelEnsemble: ['claude', 'gemini', 'custom'] }
    });
    
    // Oracle manipulation detection
    const oracleCheck = await client.detectOracleManipulation({
      feeds: [...], timestamps: [...], prices: [...]
    });
    
    // Compliance reporting
    const compliance = await client.generateComplianceReport({
      period: '2025-Q1',
      standards: ['SOC2', 'ISO27001'],
      includeAuditTrail: true
    });
  `
};
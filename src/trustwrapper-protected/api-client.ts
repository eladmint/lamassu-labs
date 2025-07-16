/**
 * TrustWrapper Protected API Client
 *
 * PROTECTED COMPONENT - Provides API access to proprietary algorithms
 * Replaces direct algorithm access with authenticated API calls
 */

export interface AdvancedVerificationResult {
  trustScore: number; // 0-100 advanced ML-based score
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  recommendation: 'APPROVED' | 'REVIEW' | 'REJECTED' | 'BLOCKED';
  factors: AdvancedVerificationFactor[];
  warnings: string[];
  mlConfidence: number; // ML model confidence
  timestamp: number;
  isAdvancedVerification: true;
  processingTime: number;
}

export interface AdvancedVerificationFactor {
  name: string;
  score: number;
  weight: number;
  confidence: number;
  details: string;
  category: 'scam_detection' | 'asset_verification' | 'risk_analysis' | 'compliance';
}

export interface OracleManipulationResult {
  manipulationProbability: number;
  confidence: number;
  detectedPatterns: string[];
  riskScore: number;
  affectedValue: number;
  recommendedActions: string[];
  alertLevel: 'none' | 'low' | 'medium' | 'high' | 'critical';
}

export interface EnterpriseComplianceResult {
  gdprCompliant: boolean;
  hipaaCompliant: boolean;
  finraCompliant: boolean;
  violations: ComplianceViolation[];
  riskAssessment: string;
  auditTrail: string;
}

export interface ComplianceViolation {
  type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  description: string;
  regulation: string;
  suggestedRemediation: string;
}

/**
 * Configuration for TrustWrapper API access
 */
export interface TrustWrapperAPIConfig {
  apiKey: string;
  baseUrl?: string;
  tier: 'professional' | 'enterprise';
  timeout?: number;
  retries?: number;
}

/**
 * Protected TrustWrapper client - provides access to proprietary algorithms via API
 */
export class TrustWrapperProtectedClient {
  private config: TrustWrapperAPIConfig;
  private baseUrl: string;

  constructor(config: TrustWrapperAPIConfig) {
    this.config = config;
    this.baseUrl = config.baseUrl || 'https://api.trustwrapper.ai/v1';
  }

  /**
   * Advanced verification using proprietary ML algorithms
   * Requires Professional or Enterprise API access
   */
  public async verifyAdvanced(text: string, options?: {
    includeMLAnalysis?: boolean;
    includeRiskProfiling?: boolean;
    customThresholds?: Record<string, number>;
  }): Promise<AdvancedVerificationResult> {

    const response = await this.apiCall('/verify/advanced', {
      method: 'POST',
      body: {
        text,
        options: options || {},
        tier: this.config.tier
      }
    });

    if (!response.success) {
      throw new Error(`Advanced verification failed: ${response.error}`);
    }

    return response.data;
  }

  /**
   * Oracle manipulation detection using proprietary algorithms
   * Enterprise tier only - core value for partnerships like Mento
   */
  public async detectOracleManipulation(oracleData: {
    symbol: string;
    prices: Array<{price: number; timestamp: number; source: string}>;
    metadata?: Record<string, any>;
  }): Promise<OracleManipulationResult> {

    if (this.config.tier !== 'enterprise') {
      throw new Error('Oracle manipulation detection requires Enterprise tier');
    }

    const response = await this.apiCall('/oracle/detect-manipulation', {
      method: 'POST',
      body: oracleData
    });

    if (!response.success) {
      throw new Error(`Oracle manipulation detection failed: ${response.error}`);
    }

    return response.data;
  }

  /**
   * Enterprise compliance checking
   * Supports GDPR, HIPAA, FINRA, SOX regulations
   */
  public async checkCompliance(content: string, regulations: string[] = ['gdpr', 'hipaa', 'finra']): Promise<EnterpriseComplianceResult> {

    if (this.config.tier !== 'enterprise') {
      throw new Error('Compliance checking requires Enterprise tier');
    }

    const response = await this.apiCall('/compliance/check', {
      method: 'POST',
      body: {
        content,
        regulations
      }
    });

    if (!response.success) {
      throw new Error(`Compliance checking failed: ${response.error}`);
    }

    return response.data;
  }

  /**
   * Generate zero-knowledge proof for verification result
   * Allows sharing verification without exposing algorithms or data
   */
  public async generateZKProof(verificationResult: AdvancedVerificationResult): Promise<{
    proof: string;
    publicSignals: string[];
    proofHash: string;
  }> {

    const response = await this.apiCall('/zk/generate-proof', {
      method: 'POST',
      body: {
        verificationResult,
        includeMetadata: false // Never expose internal data
      }
    });

    if (!response.success) {
      throw new Error(`ZK proof generation failed: ${response.error}`);
    }

    return response.data;
  }

  /**
   * Verify a zero-knowledge proof from another party
   */
  public async verifyZKProof(proof: string, publicSignals: string[]): Promise<{
    isValid: boolean;
    trustScore: number;
    timestamp: number;
  }> {

    const response = await this.apiCall('/zk/verify-proof', {
      method: 'POST',
      body: {
        proof,
        publicSignals
      }
    });

    if (!response.success) {
      throw new Error(`ZK proof verification failed: ${response.error}`);
    }

    return response.data;
  }

  /**
   * Get usage analytics and billing information
   */
  public async getUsageAnalytics(timeframe: 'day' | 'week' | 'month' = 'month'): Promise<{
    totalRequests: number;
    successRate: number;
    averageLatency: number;
    costThisMonth: number;
    remainingQuota: number;
  }> {

    const response = await this.apiCall(`/analytics/usage?timeframe=${timeframe}`, {
      method: 'GET'
    });

    if (!response.success) {
      throw new Error(`Usage analytics failed: ${response.error}`);
    }

    return response.data;
  }

  /**
   * Internal API call method with authentication and error handling
   */
  private async apiCall(endpoint: string, options: {
    method: 'GET' | 'POST' | 'PUT' | 'DELETE';
    body?: any;
    headers?: Record<string, string>;
  }): Promise<{success: boolean; data?: any; error?: string}> {

    try {
      const url = `${this.baseUrl}${endpoint}`;
      const headers = {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
        'User-Agent': 'TrustWrapper-Client/2.0',
        ...options.headers
      };

      const fetchOptions: RequestInit = {
        method: options.method,
        headers,
        timeout: this.config.timeout || 30000
      };

      if (options.body && options.method !== 'GET') {
        fetchOptions.body = JSON.stringify(options.body);
      }

      const response = await fetch(url, fetchOptions);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          success: false,
          error: errorData.message || `HTTP ${response.status}: ${response.statusText}`
        };
      }

      const data = await response.json();
      return { success: true, data };

    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown API error'
      };
    }
  }
}

/**
 * Factory function for creating protected client
 */
export function createTrustWrapperClient(config: TrustWrapperAPIConfig): TrustWrapperProtectedClient {
  return new TrustWrapperProtectedClient(config);
}

/**
 * Convenience function for quick advanced verification
 */
export async function verifyAdvanced(text: string, apiKey: string, tier: 'professional' | 'enterprise' = 'professional'): Promise<AdvancedVerificationResult> {
  const client = createTrustWrapperClient({ apiKey, tier });
  return await client.verifyAdvanced(text);
}

/**
 * API tier information for developers
 */
export const TRUSTWRAPPER_API_TIERS = {
  professional: {
    price: '$299/month',
    features: ['Advanced ML verification', 'Real-time monitoring', '10K requests/month'],
    suitable: 'Growing startups and production applications'
  },
  enterprise: {
    price: '$2,999+/month',
    features: ['Oracle manipulation detection', 'Compliance checking', 'Unlimited requests', 'ZK proofs'],
    suitable: 'Enterprise partnerships and high-value applications'
  },
  signup: 'https://trustwrapper.ai/api-access'
};

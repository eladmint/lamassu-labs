/**
 * TrustWrapper Public Framework
 *
 * OPEN SOURCE ENTRY POINT - Safe for public distribution
 * Provides basic verification with upgrade path to protected features
 */

// Re-export all public components
export * from './basic-verification';

// Import protected client types for TypeScript support
export type {
  AdvancedVerificationResult,
  OracleManipulationResult,
  EnterpriseComplianceResult,
  TrustWrapperAPIConfig
} from '../trustwrapper-protected/api-client';

/**
 * Main TrustWrapper class that combines basic and advanced capabilities
 */
export class TrustWrapper {
  private basicVerifier: import('./basic-verification').BasicTrustWrapperVerification;
  private protectedClient?: import('../trustwrapper-protected/api-client').TrustWrapperProtectedClient;

  constructor(config?: {
    apiKey?: string;
    tier?: 'professional' | 'enterprise';
  }) {
    // Always include basic verification
    this.basicVerifier = new (require('./basic-verification').BasicTrustWrapperVerification)();

    // Optionally initialize protected client if API key provided
    if (config?.apiKey) {
      const { TrustWrapperProtectedClient } = require('../trustwrapper-protected/api-client');
      this.protectedClient = new TrustWrapperProtectedClient({
        apiKey: config.apiKey,
        tier: config.tier || 'professional'
      });
    }
  }

  /**
   * Verify content using available verification level
   * Automatically uses advanced verification if API key provided, falls back to basic
   */
  public async verify(text: string, options?: {
    preferAdvanced?: boolean;
    fallbackToBasic?: boolean;
  }): Promise<import('./basic-verification').BasicVerificationResult | import('../trustwrapper-protected/api-client').AdvancedVerificationResult> {

    const preferAdvanced = options?.preferAdvanced ?? true;
    const fallbackToBasic = options?.fallbackToBasic ?? true;

    // Try advanced verification if available and preferred
    if (this.protectedClient && preferAdvanced) {
      try {
        return await this.protectedClient.verifyAdvanced(text);
      } catch (error) {
        console.warn('Advanced verification failed:', error);

        if (!fallbackToBasic) {
          throw error;
        }
      }
    }

    // Use basic verification as fallback or default
    return await this.basicVerifier.verifyBasic(text);
  }

  /**
   * Check if advanced features are available
   */
  public hasAdvancedFeatures(): boolean {
    return !!this.protectedClient;
  }

  /**
   * Get upgrade information for developers
   */
  public getUpgradeInfo(): typeof import('./basic-verification').TRUSTWRAPPER_UPGRADE_INFO {
    return require('./basic-verification').TRUSTWRAPPER_UPGRADE_INFO;
  }

  /**
   * Oracle manipulation detection (Enterprise only)
   */
  public async detectOracleManipulation(oracleData: any): Promise<import('../trustwrapper-protected/api-client').OracleManipulationResult> {
    if (!this.protectedClient) {
      throw new Error('Oracle manipulation detection requires API access. Visit https://trustwrapper.ai/api-access');
    }

    return await this.protectedClient.detectOracleManipulation(oracleData);
  }

  /**
   * Compliance checking (Enterprise only)
   */
  public async checkCompliance(content: string, regulations?: string[]): Promise<import('../trustwrapper-protected/api-client').EnterpriseComplianceResult> {
    if (!this.protectedClient) {
      throw new Error('Compliance checking requires Enterprise API access. Visit https://trustwrapper.ai/enterprise');
    }

    return await this.protectedClient.checkCompliance(content, regulations);
  }
}

/**
 * Convenience factory function
 */
export function createTrustWrapper(config?: {
  apiKey?: string;
  tier?: 'professional' | 'enterprise';
}): TrustWrapper {
  return new TrustWrapper(config);
}

/**
 * Quick verification function for simple use cases
 */
export async function verify(text: string, apiKey?: string): Promise<any> {
  const trustWrapper = createTrustWrapper(apiKey ? { apiKey } : undefined);
  return await trustWrapper.verify(text);
}

/**
 * Integration examples for common frameworks
 */
export const INTEGRATION_EXAMPLES = {
  langchain: `
import { TrustWrapper } from '@trustwrapper/core';
import { LLMChain } from 'langchain';

const trustWrapper = new TrustWrapper({ apiKey: 'your-api-key' });

// Add to LangChain callback
const chain = new LLMChain({
  llm: yourLLM,
  callbacks: [{
    handleLLMEnd: async (output) => {
      const result = await trustWrapper.verify(output.generations[0][0].text);
      if (result.riskLevel === 'HIGH') {
        console.warn('High-risk AI output detected:', result.warnings);
      }
    }
  }]
});`,

  basic: `
import { verify } from '@trustwrapper/core';

// Basic verification (free)
const result = await verify('Should I invest in this 1000% guaranteed return?');
console.log('Risk level:', result.riskLevel); // 'HIGH'

// Advanced verification (API key required)
const advancedResult = await verify('Market analysis...', 'your-api-key');
console.log('ML confidence:', advancedResult.mlConfidence);`,

  enterprise: `
import { TrustWrapper } from '@trustwrapper/core';

const trustWrapper = new TrustWrapper({
  apiKey: 'your-enterprise-key',
  tier: 'enterprise'
});

// Oracle manipulation detection for DeFi protocols
const oracleResult = await trustWrapper.detectOracleManipulation({
  symbol: 'ETH/USD',
  prices: [/* oracle price feeds */]
});

// Compliance checking for regulated industries
const complianceResult = await trustWrapper.checkCompliance(
  'Patient medical recommendation...',
  ['hipaa', 'gdpr']
);`
};

/**
 * Package information
 */
export const PACKAGE_INFO = {
  name: '@trustwrapper/core',
  version: '2.0.0',
  description: 'Universal AI trust infrastructure with open core architecture',
  homepage: 'https://trustwrapper.ai',
  repository: 'https://github.com/lamassu-labs/trustwrapper',
  license: 'MIT (core framework) + Commercial (advanced features)',
  support: {
    documentation: 'https://docs.trustwrapper.ai',
    community: 'https://discord.gg/trustwrapper',
    enterprise: 'https://trustwrapper.ai/enterprise-support'
  }
};

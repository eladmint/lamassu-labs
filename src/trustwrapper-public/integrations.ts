/**
 * TrustWrapper Open Source Integration Framework
 * Basic verification and integration utilities for community adoption
 */

export interface BasicVerificationRequest {
  content: string;
  options?: {
    checkObviousScams?: boolean;
    validateFormat?: boolean;
  };
}

export interface BasicVerificationResult {
  verified: boolean;
  confidence: number;
  warnings: string[];
  metadata: {
    checks_performed: string[];
    processing_time_ms: number;
    framework_version: string;
  };
}

export interface IntegrationConfig {
  webhookUrl?: string;
  logLevel?: 'debug' | 'info' | 'warn' | 'error';
  enableMetrics?: boolean;
}

/**
 * Basic pattern-based verification for obvious scams and format validation
 * This is the open source foundation that encourages adoption
 */
export class TrustWrapperBasic {
  private config: IntegrationConfig;

  constructor(config: IntegrationConfig = {}) {
    this.config = config;
  }

  /**
   * Basic verification using simple pattern matching
   * Detects obvious scams and format issues
   */
  async verifyBasic(request: BasicVerificationRequest): Promise<BasicVerificationResult> {
    const startTime = Date.now();
    const warnings: string[] = [];
    const checksPerformed: string[] = [];

    // Basic scam detection patterns (open source safe)
    if (request.options?.checkObviousScams !== false) {
      const scamPatterns = [
        /guaranteed.*profit/i,
        /100%.*return/i,
        /risk.*free.*investment/i,
        /urgent.*limited.*time/i,
        /send.*crypto.*immediately/i,
      ];

      for (const pattern of scamPatterns) {
        if (pattern.test(request.content)) {
          warnings.push(`Potential scam pattern detected: ${pattern.source}`);
        }
      }
      checksPerformed.push('scam_patterns');
    }

    // Basic format validation
    if (request.options?.validateFormat !== false) {
      if (request.content.length < 10) {
        warnings.push('Content too short for meaningful analysis');
      }
      if (request.content.length > 10000) {
        warnings.push('Content very long, consider chunking');
      }
      checksPerformed.push('format_validation');
    }

    // Simple confidence calculation based on warnings
    const confidence = Math.max(0, 1 - (warnings.length * 0.2));
    const verified = warnings.length === 0;

    return {
      verified,
      confidence,
      warnings,
      metadata: {
        checks_performed: checksPerformed,
        processing_time_ms: Date.now() - startTime,
        framework_version: '3.0.0-open-source',
      },
    };
  }

  /**
   * Integration with popular AI agent frameworks
   */
  async integrateWithEliza(elizaAgent: any): Promise<void> {
    // Basic Eliza integration pattern
    if (elizaAgent && typeof elizaAgent.on === 'function') {
      elizaAgent.on('beforeTrade', async (tradeData: any) => {
        const result = await this.verifyBasic({
          content: JSON.stringify(tradeData),
        });
        
        if (!result.verified) {
          console.warn('TrustWrapper Basic Warning:', result.warnings);
        }
      });
    }
  }

  /**
   * Integration with LangChain agents
   */
  async integrateWithLangChain(chain: any): Promise<void> {
    // Basic LangChain integration pattern
    if (chain && typeof chain.addMiddleware === 'function') {
      chain.addMiddleware(async (input: any) => {
        const result = await this.verifyBasic({
          content: input.toString(),
        });
        
        return {
          ...input,
          trustwrapper_verification: result,
        };
      });
    }
  }

  /**
   * Webhook integration for external systems
   */
  async sendWebhook(data: any): Promise<void> {
    if (!this.config.webhookUrl) return;

    try {
      await fetch(this.config.webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...data,
          timestamp: new Date().toISOString(),
          source: 'trustwrapper-basic',
        }),
      });
    } catch (error) {
      console.error('Webhook delivery failed:', error);
    }
  }
}

/**
 * Utility functions for common integration patterns
 */
export const IntegrationUtils = {
  /**
   * Convert various input formats to standardized text
   */
  normalizeInput(input: any): string {
    if (typeof input === 'string') return input;
    if (typeof input === 'object') return JSON.stringify(input);
    return String(input);
  },

  /**
   * Create integration middleware for Express.js
   */
  createExpressMiddleware(trustWrapper: TrustWrapperBasic) {
    return async (req: any, res: any, next: any) => {
      if (req.body) {
        const result = await trustWrapper.verifyBasic({
          content: this.normalizeInput(req.body),
        });
        req.trustwrapper = result;
      }
      next();
    };
  },

  /**
   * Create WebSocket handler for real-time verification
   */
  createWebSocketHandler(trustWrapper: TrustWrapperBasic) {
    return async (ws: any) => {
      ws.on('message', async (message: string) => {
        try {
          const data = JSON.parse(message);
          const result = await trustWrapper.verifyBasic({
            content: data.content || message,
          });
          
          ws.send(JSON.stringify({
            type: 'verification_result',
            result,
          }));
        } catch (error) {
          ws.send(JSON.stringify({
            type: 'error',
            error: 'Invalid message format',
          }));
        }
      });
    };
  },
};

/**
 * Smart contract integration utilities
 */
export const SmartContractUtils = {
  /**
   * Generate verification data for blockchain submission
   */
  prepareForBlockchain(result: BasicVerificationResult): {
    verified: boolean;
    confidence_score: number;
    warning_count: number;
    timestamp: number;
  } {
    return {
      verified: result.verified,
      confidence_score: Math.floor(result.confidence * 100),
      warning_count: result.warnings.length,
      timestamp: Math.floor(Date.now() / 1000),
    };
  },

  /**
   * Create basic verification hash for on-chain storage
   */
  createVerificationHash(content: string, result: BasicVerificationResult): string {
    const data = JSON.stringify({
      content_hash: this.simpleHash(content),
      verified: result.verified,
      confidence: result.confidence,
      timestamp: Date.now(),
    });
    return this.simpleHash(data);
  },

  /**
   * Simple hash function for basic verification (not cryptographically secure)
   */
  simpleHash(input: string): string {
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash).toString(16);
  },
};

/**
 * Example usage and integration patterns
 */
export const Examples = {
  basic: `
    // Basic verification for community developers
    import { TrustWrapperBasic } from '@trustwrapper/public';
    
    const trustWrapper = new TrustWrapperBasic({
      logLevel: 'info',
      enableMetrics: true
    });
    
    const result = await trustWrapper.verifyBasic({
      content: "User-generated trading advice",
      options: { checkObviousScams: true }
    });
    
    if (!result.verified) {
      console.log('Warnings:', result.warnings);
    }
  `,
  
  integration: `
    // Integration with existing AI agent
    import { TrustWrapperBasic, IntegrationUtils } from '@trustwrapper/public';
    
    const trustWrapper = new TrustWrapperBasic();
    
    // Express.js middleware
    app.use('/api/verify', IntegrationUtils.createExpressMiddleware(trustWrapper));
    
    // WebSocket real-time verification
    const wsHandler = IntegrationUtils.createWebSocketHandler(trustWrapper);
    wss.on('connection', wsHandler);
  `,
  
  blockchain: `
    // Smart contract integration
    import { SmartContractUtils } from '@trustwrapper/public';
    
    const result = await trustWrapper.verifyBasic({ content: tradingDecision });
    const blockchainData = SmartContractUtils.prepareForBlockchain(result);
    const verificationHash = SmartContractUtils.createVerificationHash(tradingDecision, result);
    
    // Submit to your smart contract
    await contract.submitVerification(blockchainData, verificationHash);
  `
};
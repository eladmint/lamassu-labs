/**
 * TrustWrapper Public Framework - Basic Verification Interface
 *
 * OPEN SOURCE COMPONENT - Safe for public distribution
 * Contains only basic patterns and interfaces, no proprietary algorithms
 */

export interface BasicVerificationResult {
  trustScore: number; // 0-100 basic score
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  recommendation: 'APPROVED' | 'REVIEW' | 'REJECTED';
  warnings: string[];
  timestamp: number;
  isBasicVerification: true; // Indicates limited verification
}

export interface VerificationFactor {
  name: string;
  impact: 'positive' | 'negative' | 'neutral';
  description: string;
}

/**
 * Basic TrustWrapper verification for open source use
 * Provides simple pattern matching without exposing proprietary algorithms
 */
export class BasicTrustWrapperVerification {

  /**
   * Performs basic verification using simple, obvious patterns only
   * For advanced verification, use TrustWrapper API or Enterprise license
   */
  public async verifyBasic(text: string): Promise<BasicVerificationResult> {
    const warnings: string[] = [];
    const factors: VerificationFactor[] = [];

    // Only include obvious, non-proprietary patterns
    let trustScore = 50; // Start neutral

    // 1. Check for obvious scam language (basic patterns only)
    const obviousScamScore = this.checkObviousScams(text, factors, warnings);

    // 2. Basic asset mention validation (simple list check)
    const assetMentionScore = this.checkBasicAssetMentions(text, factors);

    // 3. Simple unrealistic claim detection (obvious thresholds)
    const unrealisticScore = this.checkObviousUnrealistic(text, factors, warnings);

    // Simple weighted calculation (no proprietary logic)
    trustScore = Math.round((obviousScamScore + assetMentionScore + unrealisticScore) / 3);

    // Determine risk level using basic thresholds
    const riskLevel = this.calculateBasicRiskLevel(trustScore);
    const recommendation = this.getBasicRecommendation(trustScore, warnings.length);

    return {
      trustScore,
      riskLevel,
      recommendation,
      warnings,
      timestamp: Date.now(),
      isBasicVerification: true
    };
  }

  /**
   * Check for obvious scam patterns (non-proprietary, basic only)
   */
  private checkObviousScams(text: string, factors: VerificationFactor[], warnings: string[]): number {
    let score = 50;

    // Only include obvious patterns that anyone could identify
    const obviousScamPatterns = [
      /\b(guaranteed.*100%|risk.*free.*money)\b/i,
      /\b(send.*money.*get.*back)\b/i,
      /\b(click.*here.*now|act.*fast|limited.*time.*only)\b/i
    ];

    for (const pattern of obviousScamPatterns) {
      if (pattern.test(text)) {
        score -= 20;
        warnings.push('Contains obvious scam language patterns');
        factors.push({
          name: 'Obvious Scam Language',
          impact: 'negative',
          description: 'Contains clear scam indicators'
        });
        break; // One warning is enough
      }
    }

    return Math.max(0, score);
  }

  /**
   * Basic asset mention checking (simple whitelist)
   */
  private checkBasicAssetMentions(text: string, factors: VerificationFactor[]): number {
    // Simple, well-known assets list (non-proprietary)
    const knownAssets = ['BTC', 'ETH', 'SOL', 'bitcoin', 'ethereum', 'solana'];

    const hasKnownAsset = knownAssets.some(asset =>
      text.toLowerCase().includes(asset.toLowerCase())
    );

    if (hasKnownAsset) {
      factors.push({
        name: 'Known Asset Mentioned',
        impact: 'positive',
        description: 'Mentions well-known cryptocurrency'
      });
      return 60; // Slight positive
    }

    return 50; // Neutral
  }

  /**
   * Check for obviously unrealistic claims (basic thresholds)
   */
  private checkObviousUnrealistic(text: string, factors: VerificationFactor[], warnings: string[]): number {
    let score = 50;

    // Only check for obviously unrealistic claims (non-proprietary thresholds)
    const unrealisticPatterns = [
      /\b\d{4,}\s*%/i, // 1000%+ anything is obviously unrealistic
      /\b(10000x|1000x)\b/i // Obviously unrealistic multipliers
    ];

    for (const pattern of unrealisticPatterns) {
      if (pattern.test(text)) {
        score = 20; // Very low score for obvious unrealistic claims
        warnings.push('Contains obviously unrealistic performance claims');
        factors.push({
          name: 'Unrealistic Claims',
          impact: 'negative',
          description: 'Contains obviously impossible performance claims'
        });
        break;
      }
    }

    return score;
  }

  /**
   * Calculate basic risk level (simple thresholds)
   */
  private calculateBasicRiskLevel(trustScore: number): 'LOW' | 'MEDIUM' | 'HIGH' {
    if (trustScore >= 70) return 'LOW';
    if (trustScore >= 40) return 'MEDIUM';
    return 'HIGH';
  }

  /**
   * Get basic recommendation (simple logic)
   */
  private getBasicRecommendation(trustScore: number, warningCount: number): 'APPROVED' | 'REVIEW' | 'REJECTED' {
    if (warningCount > 0 || trustScore < 30) return 'REJECTED';
    if (trustScore < 60) return 'REVIEW';
    return 'APPROVED';
  }
}

/**
 * Factory function for creating basic verification instance
 */
export function createBasicTrustWrapper(): BasicTrustWrapperVerification {
  return new BasicTrustWrapperVerification();
}

/**
 * Simple integration helper for common use cases
 */
export async function verifyTextBasic(text: string): Promise<BasicVerificationResult> {
  const verifier = createBasicTrustWrapper();
  return await verifier.verifyBasic(text);
}

/**
 * Integration note for developers
 */
export const TRUSTWRAPPER_UPGRADE_INFO = {
  message: 'This is basic verification only. For advanced AI trading safety, oracle manipulation detection, and enterprise compliance features, upgrade to TrustWrapper Professional or Enterprise.',
  upgradeUrl: 'https://trustwrapper.ai/upgrade',
  apiAccess: 'https://api.trustwrapper.ai/docs',
  features: {
    basic: ['Simple scam detection', 'Basic asset validation', 'Obvious unrealistic claims'],
    professional: ['Advanced ML detection', 'Real-time oracle monitoring', 'API access to proprietary algorithms'],
    enterprise: ['Custom models', 'On-premise deployment', 'Full compliance reporting']
  }
};

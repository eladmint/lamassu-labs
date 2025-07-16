/**
 * TrustWrapper Verification Engine
 *
 * Core logic for detecting AI hallucinations and verifying trading decisions
 */

export interface VerificationResult {
    trustScore: number;
    riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
    recommendation: 'APPROVED' | 'REVIEW' | 'REJECTED';
    factors: VerificationFactor[];
    warnings: string[];
    timestamp: number;
}

export interface VerificationFactor {
    name: string;
    score: number;
    weight: number;
    details: string;
}

export class TrustWrapperVerificationEngine {
    // Known scam patterns and red flags
    private scamPatterns = [
        /\b(guaranteed|risk-free|no risk)\s*(returns?|profits?|gains?)\b/i,
        /\b\d{3,}\s*%\s*(apy|apr|returns?|gains?)\b/i, // 100%+ returns
        /\b(10x|100x|1000x|moon|lambo)\b/i,
        /\b(get rich quick|easy money|passive income)\b/i,
        /\b(limited time|act now|don't miss out|last chance)\b/i,
    ];

    // Verified protocols and assets
    private verifiedAssets = new Set([
        'BTC', 'ETH', 'SOL', 'MATIC', 'AVAX', 'DOT', 'LINK', 'UNI', 'AAVE',
        'bitcoin', 'ethereum', 'solana', 'polygon', 'avalanche', 'polkadot',
        'chainlink', 'uniswap', 'aave', 'compound', 'maker', 'curve'
    ]);

    private verifiedProtocols = new Set([
        'uniswap', 'sushiswap', 'pancakeswap', 'curve', 'aave', 'compound',
        'maker', 'yearn', 'convex', 'balancer', 'bancor', '1inch',
        'marinade', 'lido', 'rocket pool', 'frax', 'olympus'
    ]);

    // Unrealistic metrics thresholds
    private unrealisticThresholds = {
        apy: 1000, // 1000% APY is highly suspicious
        dailyGain: 50, // 50% daily gain is unrealistic
        weeklyGain: 200, // 200% weekly gain is extremely rare
        monthlyGain: 500, // 500% monthly gain is nearly impossible
    };

    /**
     * Verify a trading decision for hallucinations and risks
     */
    public async verifyTradingDecision(text: string): Promise<VerificationResult> {
        const factors: VerificationFactor[] = [];
        const warnings: string[] = [];

        // 1. Check for scam patterns
        const scamScore = this.checkScamPatterns(text, factors, warnings);

        // 2. Verify mentioned assets and protocols
        const assetScore = this.verifyAssets(text, factors, warnings);

        // 3. Check for unrealistic claims
        const claimScore = this.checkUnrealisticClaims(text, factors, warnings);

        // 4. Analyze risk indicators
        const riskScore = this.analyzeRiskIndicators(text, factors, warnings);

        // 5. Check position sizing and risk management
        const positionScore = this.checkPositionSizing(text, factors, warnings);

        // Calculate weighted trust score
        const totalWeight = factors.reduce((sum, f) => sum + f.weight, 0);
        const weightedScore = factors.reduce((sum, f) => sum + (f.score * f.weight), 0);
        const trustScore = Math.round(totalWeight > 0 ? weightedScore / totalWeight : 50);

        // Determine risk level and recommendation
        const riskLevel = this.calculateRiskLevel(trustScore, warnings.length);
        const recommendation = this.getRecommendation(trustScore, riskLevel, warnings.length);

        return {
            trustScore,
            riskLevel,
            recommendation,
            factors,
            warnings,
            timestamp: Date.now()
        };
    }

    private checkScamPatterns(text: string, factors: VerificationFactor[], warnings: string[]): number {
        let scamIndicators = 0;

        for (const pattern of this.scamPatterns) {
            if (pattern.test(text)) {
                scamIndicators++;
                warnings.push(`Detected suspicious pattern: ${pattern.source}`);
            }
        }

        const score = Math.max(0, 100 - (scamIndicators * 25));

        factors.push({
            name: 'Scam Pattern Check',
            score,
            weight: 0.3,
            details: scamIndicators === 0 ? 'No scam patterns detected' : `Found ${scamIndicators} suspicious patterns`
        });

        return score;
    }

    private verifyAssets(text: string, factors: VerificationFactor[], warnings: string[]): number {
        const words = text.toLowerCase().split(/\s+/);
        let verifiedCount = 0;
        let unverifiedCount = 0;
        const cryptoPattern = /\b[A-Z]{3,6}\b/g;
        const potentialAssets = text.match(cryptoPattern) || [];

        for (const asset of potentialAssets) {
            if (this.verifiedAssets.has(asset) || this.verifiedAssets.has(asset.toLowerCase())) {
                verifiedCount++;
            } else if (asset.length >= 3 && asset !== 'USD' && asset !== 'APY' && asset !== 'APR' && asset !== 'TVL') {
                unverifiedCount++;
                warnings.push(`Unverified asset mentioned: ${asset}`);
            }
        }

        // Check for protocol mentions
        for (const word of words) {
            if (this.verifiedProtocols.has(word)) {
                verifiedCount++;
            }
        }

        const score = unverifiedCount === 0 ? 100 : Math.max(20, 100 - (unverifiedCount * 30));

        factors.push({
            name: 'Asset Verification',
            score,
            weight: 0.25,
            details: `${verifiedCount} verified, ${unverifiedCount} unverified assets/protocols`
        });

        return score;
    }

    private checkUnrealisticClaims(text: string, factors: VerificationFactor[], warnings: string[]): number {
        let unrealisticClaims = 0;

        // Check for unrealistic APY/APR claims
        const apyPattern = /(\d+(?:,\d{3})*(?:\.\d+)?)\s*%?\s*(?:apy|apr)/gi;
        const apyMatches = [...text.matchAll(apyPattern)];

        for (const match of apyMatches) {
            const value = parseFloat(match[1].replace(/,/g, ''));
            if (value > this.unrealisticThresholds.apy) {
                unrealisticClaims++;
                warnings.push(`Unrealistic APY claim: ${value}%`);
            }
        }

        // Check for unrealistic return claims
        const returnPattern = /(\d+)x\s*(?:returns?|gains?|profits?)/gi;
        const returnMatches = [...text.matchAll(returnPattern)];

        for (const match of returnMatches) {
            const multiplier = parseInt(match[1]);
            if (multiplier > 10) {
                unrealisticClaims++;
                warnings.push(`Unrealistic return claim: ${multiplier}x`);
            }
        }

        // Check for impossible timeframes
        const timeframePattern = /(\d+)\s*%\s*(?:per|in|within)\s*(day|week|month)/gi;
        const timeframeMatches = [...text.matchAll(timeframePattern)];

        for (const match of timeframeMatches) {
            const percentage = parseFloat(match[1]);
            const timeframe = match[2].toLowerCase();

            if ((timeframe === 'day' && percentage > this.unrealisticThresholds.dailyGain) ||
                (timeframe === 'week' && percentage > this.unrealisticThresholds.weeklyGain) ||
                (timeframe === 'month' && percentage > this.unrealisticThresholds.monthlyGain)) {
                unrealisticClaims++;
                warnings.push(`Unrealistic ${timeframe}ly gain claim: ${percentage}%`);
            }
        }

        const score = Math.max(0, 100 - (unrealisticClaims * 30));

        factors.push({
            name: 'Realistic Claims',
            score,
            weight: 0.25,
            details: unrealisticClaims === 0 ? 'All claims appear realistic' : `Found ${unrealisticClaims} unrealistic claims`
        });

        return score;
    }

    private analyzeRiskIndicators(text: string, factors: VerificationFactor[], warnings: string[]): number {
        let riskIndicators = 0;
        const lowerText = text.toLowerCase();

        // High-risk keywords
        const highRiskKeywords = [
            'leverage', 'margin', 'short', 'futures', 'options', 'perpetual',
            'yolo', 'all in', 'life savings', 'loan', 'borrow to invest'
        ];

        for (const keyword of highRiskKeywords) {
            if (lowerText.includes(keyword)) {
                riskIndicators++;
                warnings.push(`High-risk indicator: ${keyword}`);
            }
        }

        // Check for FOMO indicators
        const fomoPatterns = [
            'fear of missing out', 'fomo', 'everyone is buying', 'don\'t miss',
            'last chance', 'limited time', 'act now', 'hurry'
        ];

        for (const pattern of fomoPatterns) {
            if (lowerText.includes(pattern)) {
                riskIndicators++;
                warnings.push(`FOMO indicator detected: ${pattern}`);
            }
        }

        const score = Math.max(20, 100 - (riskIndicators * 15));

        factors.push({
            name: 'Risk Analysis',
            score,
            weight: 0.2,
            details: riskIndicators === 0 ? 'No high-risk indicators' : `Found ${riskIndicators} risk indicators`
        });

        return score;
    }

    private checkPositionSizing(text: string, factors: VerificationFactor[], warnings: string[]): number {
        const lowerText = text.toLowerCase();
        let score = 70; // Default neutral score

        // Good position sizing indicators
        const goodSizing = [
            /\b\d{1,2}\s*%\s*(?:of\s*)?(?:portfolio|capital|funds)/i,
            /\bsmall\s*(?:position|amount|investment)\b/i,
            /\bdiversif/i,
            /\brisk\s*management\b/i
        ];

        // Bad position sizing indicators
        const badSizing = [
            /\ball\s*in\b/i,
            /\bentire\s*(?:portfolio|savings|capital)\b/i,
            /\bmax\s*leverage\b/i,
            /\b100\s*%\s*(?:of\s*)?(?:portfolio|capital)\b/i
        ];

        let goodIndicators = 0;
        let badIndicators = 0;

        for (const pattern of goodSizing) {
            if (pattern.test(text)) {
                goodIndicators++;
                score += 10;
            }
        }

        for (const pattern of badSizing) {
            if (pattern.test(text)) {
                badIndicators++;
                score -= 25;
                warnings.push('Poor position sizing detected');
            }
        }

        score = Math.max(10, Math.min(100, score));

        factors.push({
            name: 'Position Sizing',
            score,
            weight: 0.15,
            details: badIndicators > 0 ? 'Poor position sizing detected' :
                     goodIndicators > 0 ? 'Good risk management indicated' : 'No position sizing information'
        });

        return score;
    }

    private calculateRiskLevel(trustScore: number, warningCount: number): 'LOW' | 'MEDIUM' | 'HIGH' {
        if (trustScore >= 80 && warningCount <= 1) return 'LOW';
        if (trustScore >= 50 || warningCount <= 3) return 'MEDIUM';
        return 'HIGH';
    }

    private getRecommendation(trustScore: number, riskLevel: string, warningCount: number): 'APPROVED' | 'REVIEW' | 'REJECTED' {
        if (trustScore >= 80 && riskLevel === 'LOW') return 'APPROVED';
        if (trustScore <= 30 || warningCount >= 4) return 'REJECTED';
        return 'REVIEW';
    }
}

// Export singleton instance
export const verificationEngine = new TrustWrapperVerificationEngine();

// Enhanced version of Rabbi Trader's analyzeTrade.ts with TrustWrapper integration
import {
    type Action,
    elizaLogger,
    generateText,
    ModelClass,
    parseJSONObjectFromText,
} from "@elizaos/core";
import { TrustWrapperVerificationEngine } from "@elizaos/plugin-trustwrapper";

export const analyzeTradeAction: Action = {
    name: "ANALYZE_TRADE",
    description: "Analyze a token for trading opportunities with TrustWrapper safety verification",
    similes: [
        "ANALYZE",
        "ANALYZE_TOKEN",
        "TRADE",
        "ANALYZE_TRADE",
        "EVALUATE",
        "ASSESS",
    ],
    examples: [],
    validate: async () => true,
    handler: async (runtime, memory, state, params, callback) => {
        try {
            // composeState
            if (!state) {
                state = await runtime.composeState(memory);
            } else state = await runtime.updateRecentMessageState(state);

            const tokenData = {
                walletBalance: params.walletBalance,
                tokenAddress: params.tokenAddress,
                price: params.price,
                volume: params.volume,
                marketCap: params.marketCap,
                liquidity: params.liquidity,
                holderDistribution: params.holderDistribution,
                trustScore: params.trustScore,
                dexscreener: params.dexscreener,
                position: params.position,
            };

            // Direct prompt instead of template
            const prompt = `Analyze the following token data and provide a trading recommendation.
Return the response as a JSON object with the following structure:
{
  "recommendation": "BUY" | "SELL" | "HOLD",
  "confidence": number (0-100),
  "reasoning": string,
  "risks": string[],
  "opportunities": string[]
}

Token Data:
${JSON.stringify(tokenData, null, 2)}`;

            // Generate analysis using direct prompt
            const content = await generateText({
                runtime,
                context: prompt,
                modelClass: ModelClass.LARGE,
            });

            if (!content) {
                throw new Error("No analysis generated");
            }

            elizaLogger.log(`Raw analysis response:`, content);

            // Parse the response to get the recommended action
            const recommendation = parseJSONObjectFromText(content);
            elizaLogger.log(
                `Parsed recommendation for ${params.tokenAddress}:`,
                recommendation
            );

            // ========== TRUSTWRAPPER INTEGRATION START ==========

            // Initialize TrustWrapper verification engine
            const verificationEngine = new TrustWrapperVerificationEngine();

            // Build verification context from the recommendation
            const verificationText = `
                Token: ${params.tokenAddress}
                Action: ${recommendation.recommendation}
                Price: $${params.price}
                Market Cap: $${params.marketCap}
                Volume: $${params.volume}
                Liquidity: $${params.liquidity}
                Trust Score: ${params.trustScore}
                Reasoning: ${recommendation.reasoning}
                Opportunities: ${recommendation.opportunities?.join(", ") || "None"}
            `;

            // Verify the trading decision
            const verificationResult = await verificationEngine.verifyTradingDecision(verificationText);

            elizaLogger.log(`TrustWrapper verification for ${params.tokenAddress}:`, {
                status: verificationResult.recommendation,
                trustScore: verificationResult.trustScore,
                riskLevel: verificationResult.riskLevel,
                warnings: verificationResult.warnings
            });

            // Apply safety overrides based on verification
            if (verificationResult.recommendation === 'REJECTED') {
                elizaLogger.warn(`🛡️ TrustWrapper BLOCKED dangerous trade for ${params.tokenAddress}:`,
                    verificationResult.warnings);

                // Override the recommendation to prevent dangerous trade
                recommendation.recommendation = 'HOLD';
                recommendation.confidence = 0;
                recommendation.reasoning = `TrustWrapper safety check failed: ${verificationResult.warnings.join(', ')}`;
                recommendation.risks = [...(recommendation.risks || []), ...verificationResult.warnings];
                recommendation.trustWrapperStatus = 'BLOCKED';
                recommendation.trustWrapperWarnings = verificationResult.warnings;

                // Log the safety intervention
                await runtime.databaseAdapter.log({
                    type: 'trustwrapper_intervention',
                    tokenAddress: params.tokenAddress,
                    originalRecommendation: content,
                    blockedReason: verificationResult.warnings,
                    timestamp: new Date().toISOString()
                });

            } else if (verificationResult.recommendation === 'REVIEW') {
                elizaLogger.warn(`⚠️ TrustWrapper suggests CAUTION for ${params.tokenAddress}`);

                // Reduce confidence and add warnings
                recommendation.confidence = Math.min(recommendation.confidence, 50);
                recommendation.risks = [...(recommendation.risks || []), ...verificationResult.warnings];
                recommendation.trustWrapperStatus = 'CAUTION';
                recommendation.trustWrapperWarnings = verificationResult.warnings;

            } else {
                elizaLogger.log(`✅ TrustWrapper APPROVED trade for ${params.tokenAddress}`);
                recommendation.trustWrapperStatus = 'APPROVED';
                recommendation.trustWrapperScore = verificationResult.trustScore;
            }

            // Add TrustWrapper metadata to recommendation
            recommendation.verification = {
                engine: 'TrustWrapper',
                timestamp: new Date().toISOString(),
                trustScore: verificationResult.trustScore,
                riskLevel: verificationResult.riskLevel,
                status: verificationResult.recommendation
            };

            // ========== TRUSTWRAPPER INTEGRATION END ==========

            // Send result through callback
            if (callback) {
                await callback({
                    text: JSON.stringify(recommendation),
                    type: "analysis",
                });
            }

            return true;
        } catch (error) {
            elizaLogger.error(`Analysis failed:`, {
                error: error instanceof Error ? error.message : "Unknown error",
                stack: error instanceof Error ? error.stack : undefined,
            });
            return false;
        }
    },
};

// Helper function to check if TrustWrapper would allow a trade
export function shouldExecuteTrade(recommendation: any): boolean {
    // Don't execute if TrustWrapper blocked it
    if (recommendation.trustWrapperStatus === 'BLOCKED') {
        return false;
    }

    // Be cautious if TrustWrapper flagged concerns
    if (recommendation.trustWrapperStatus === 'CAUTION' && recommendation.confidence < 70) {
        return false;
    }

    // Normal trading logic
    return recommendation.recommendation === 'BUY' && recommendation.confidence > 60;
}

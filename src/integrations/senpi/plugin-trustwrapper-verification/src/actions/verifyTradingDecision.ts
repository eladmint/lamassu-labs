/**
 * TrustWrapper Trading Decision Verification Action
 *
 * Provides real-time verification of autonomous trading decisions with <1ms latency,
 * zero-knowledge proof generation, and comprehensive risk assessment.
 */

import {
    Action,
    IAgentRuntime,
    Memory,
    State,
    HandlerCallback,
    ActionExample,
} from "@ai16z/eliza";
import { z } from "zod";
import { TrustWrapperService } from "../services/trustWrapperService.js";
import { TradingDecisionRequest, VerificationResult } from "../types/index.js";

// Input validation schema
const TradingDecisionSchema = z.object({
    action: z.enum(["buy", "sell", "hold"]),
    asset: z.string().min(1, "Asset symbol required"),
    amount: z.number().positive("Amount must be positive"),
    price: z.number().positive("Price must be positive"),
    reasoning: z.string().optional(),
    urgency: z.enum(["low", "medium", "high"]).default("medium"),
    riskTolerance: z.enum(["conservative", "moderate", "aggressive"]).default("moderate")
});

export const verifyTradingDecisionAction: Action = {
    name: "VERIFY_TRADING_DECISION",

    similes: [
        "VERIFY_TRADE",
        "CHECK_TRADING_DECISION",
        "VALIDATE_TRADE",
        "TRUST_CHECK_TRADE",
        "VERIFY_AUTONOMOUS_TRADE"
    ],

    description: `Verify autonomous trading decisions in real-time using TrustWrapper's zero-knowledge verification system.

    This action:
    - Validates trading decisions against risk parameters and compliance rules
    - Generates trust scores and confidence ratings
    - Detects potential manipulation or errors in AI reasoning
    - Provides regulatory compliance validation
    - Creates zero-knowledge proofs preserving strategy confidentiality

    Supports verification for buy/sell/hold decisions across all major assets with <1ms latency guarantee.`,

    validate: async (runtime: IAgentRuntime, message: Memory): Promise<boolean> => {
        try {
            // Check if TrustWrapper service is available
            const trustWrapperService = runtime.getService("trustWrapper") as TrustWrapperService;
            if (!trustWrapperService) {
                console.warn("TrustWrapper service not available");
                return false;
            }

            // Validate message contains trading decision data
            const content = message.content;
            if (!content || typeof content !== "object") {
                return false;
            }

            // Check for required trading decision fields
            const hasRequiredFields = [
                "action", "asset", "amount", "price"
            ].every(field => field in content);

            return hasRequiredFields;
        } catch (error) {
            console.error("Error validating trading decision:", error);
            return false;
        }
    },

    handler: async (
        runtime: IAgentRuntime,
        message: Memory,
        state: State,
        options: any,
        callback: HandlerCallback
    ): Promise<void> => {
        try {
            const startTime = performance.now();

            // Parse and validate input
            const tradingData = TradingDecisionSchema.parse(message.content);

            // Get TrustWrapper service
            const trustWrapperService = runtime.getService("trustWrapper") as TrustWrapperService;

            // Create verification request
            const verificationRequest: TradingDecisionRequest = {
                accountId: message.userId || "anonymous",
                decision: {
                    action: tradingData.action,
                    asset: tradingData.asset,
                    amount: tradingData.amount,
                    price: tradingData.price,
                    reasoning: tradingData.reasoning || "",
                    urgency: tradingData.urgency,
                    riskTolerance: tradingData.riskTolerance
                },
                context: {
                    timestamp: Date.now(),
                    messageId: message.id,
                    agentId: runtime.agentId,
                    marketConditions: await trustWrapperService.getMarketContext(tradingData.asset)
                }
            };

            // Perform verification
            const verification: VerificationResult = await trustWrapperService.verifyTradingDecision(
                verificationRequest
            );

            const latency = performance.now() - startTime;

            // Generate response based on verification result
            let responseText = "";
            let statusEmoji = "";

            switch (verification.status) {
                case "approved":
                    statusEmoji = "✅";
                    responseText = `**Trading Decision Verified**\n\n` +
                        `${statusEmoji} **Status**: Approved\n` +
                        `🎯 **Confidence**: ${(verification.confidence * 100).toFixed(1)}%\n` +
                        `⚡ **Risk Score**: ${(verification.riskScore * 100).toFixed(1)}%\n` +
                        `🚀 **Recommendation**: Proceed with ${tradingData.action.toUpperCase()} ${tradingData.amount} ${tradingData.asset} at $${tradingData.price}`;
                    break;

                case "flagged":
                    statusEmoji = "⚠️";
                    responseText = `**Trading Decision Flagged**\n\n` +
                        `${statusEmoji} **Status**: Requires Attention\n` +
                        `🎯 **Confidence**: ${(verification.confidence * 100).toFixed(1)}%\n` +
                        `⚡ **Risk Score**: ${(verification.riskScore * 100).toFixed(1)}%\n` +
                        `🔍 **Issues**: ${verification.issues.join(", ")}\n` +
                        `💡 **Recommendation**: Review decision parameters before proceeding`;
                    break;

                case "rejected":
                    statusEmoji = "❌";
                    responseText = `**Trading Decision Rejected**\n\n` +
                        `${statusEmoji} **Status**: Not Recommended\n` +
                        `🎯 **Confidence**: ${(verification.confidence * 100).toFixed(1)}%\n` +
                        `⚡ **Risk Score**: ${(verification.riskScore * 100).toFixed(1)}%\n` +
                        `🚨 **Critical Issues**: ${verification.issues.join(", ")}\n` +
                        `🛡️ **Recommendation**: Do not proceed with this trade`;
                    break;

                default:
                    statusEmoji = "❓";
                    responseText = `**Verification Incomplete**\n\n` +
                        `${statusEmoji} **Status**: Unknown\n` +
                        `⏱️ **Issue**: Verification service unavailable`;
            }

            // Add performance and compliance information
            responseText += `\n\n**Verification Details**\n` +
                `⚡ **Latency**: ${latency.toFixed(2)}ms\n` +
                `🔐 **ZK Proof**: ${verification.zkProof ? "Generated" : "Unavailable"}\n` +
                `📋 **Compliance**: ${verification.complianceFlags.length === 0 ? "Clean" : verification.complianceFlags.join(", ")}\n` +
                `🔗 **Verification ID**: \`${verification.verificationId}\``;

            // Add trust scoring details if available
            if (verification.trustMetrics) {
                responseText += `\n\n**Trust Metrics**\n` +
                    `📊 **Overall Score**: ${(verification.trustMetrics.overallScore * 100).toFixed(1)}%\n` +
                    `🎯 **Strategy Consistency**: ${(verification.trustMetrics.strategyConsistency * 100).toFixed(1)}%\n` +
                    `📈 **Market Alignment**: ${(verification.trustMetrics.marketAlignment * 100).toFixed(1)}%`;
            }

            // Store verification result in memory for future reference
            await runtime.messageManager.createMemory({
                id: `verification-${verification.verificationId}`,
                userId: message.userId,
                agentId: runtime.agentId,
                content: {
                    type: "trading_verification",
                    verificationId: verification.verificationId,
                    originalDecision: tradingData,
                    result: verification,
                    timestamp: Date.now()
                },
                roomId: message.roomId,
                embedding: message.embedding
            });

            // Send response
            callback({
                text: responseText,
                action: "VERIFICATION_COMPLETE",
                source: message.content?.source || "trading_verification"
            });

        } catch (error) {
            console.error("Error in trading decision verification:", error);

            callback({
                text: `❌ **Verification Error**\n\n` +
                    `Unable to verify trading decision due to system error.\n` +
                    `Please try again or contact support if the issue persists.\n\n` +
                    `**Error**: ${error instanceof Error ? error.message : "Unknown error"}`,
                action: "VERIFICATION_ERROR",
                source: message.content?.source || "trading_verification"
            });
        }
    },

    examples: [
        [
            {
                user: "{{user1}}",
                content: {
                    text: "Verify my trading decision: buy 1000 USDC worth of ETH at current market price",
                    action: "buy",
                    asset: "ETH",
                    amount: 1000,
                    price: 2500,
                    reasoning: "Strong technical indicators and positive market sentiment"
                }
            },
            {
                user: "{{agentName}}",
                content: {
                    text: "✅ **Trading Decision Verified**\n\n✅ **Status**: Approved\n🎯 **Confidence**: 87.3%\n⚡ **Risk Score**: 23.1%\n🚀 **Recommendation**: Proceed with BUY 1000 ETH at $2500\n\n**Verification Details**\n⚡ **Latency**: 0.8ms\n🔐 **ZK Proof**: Generated\n📋 **Compliance**: Clean\n🔗 **Verification ID**: `vrf_eth_buy_789abc123`",
                    action: "VERIFICATION_COMPLETE"
                }
            }
        ],
        [
            {
                user: "{{user1}}",
                content: {
                    text: "Should I sell all my BTC holdings right now?",
                    action: "sell",
                    asset: "BTC",
                    amount: 10,
                    price: 45000,
                    urgency: "high"
                }
            },
            {
                user: "{{agentName}}",
                content: {
                    text: "⚠️ **Trading Decision Flagged**\n\n⚠️ **Status**: Requires Attention\n🎯 **Confidence**: 34.2%\n⚡ **Risk Score**: 67.8%\n🔍 **Issues**: High volatility detected, Large position size, Emotional trading pattern\n💡 **Recommendation**: Review decision parameters before proceeding",
                    action: "VERIFICATION_COMPLETE"
                }
            }
        ]
    ] as ActionExample[][],
};

export default verifyTradingDecisionAction;

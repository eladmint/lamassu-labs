/**
 * TrustWrapper Skill Performance Verification Action
 *
 * Validates AI skill performance claims and generates trust scores for
 * Senpi's skills marketplace with zero-knowledge verification.
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
import { SkillVerificationRequest, SkillVerificationResult } from "../types/index.js";

// Input validation schema
const SkillPerformanceSchema = z.object({
    skillId: z.string().min(1, "Skill ID required"),
    performanceClaims: z.object({
        accuracy: z.number().min(0).max(1, "Accuracy must be between 0 and 1"),
        latency: z.number().positive("Latency must be positive"),
        successRate: z.number().min(0).max(1, "Success rate must be between 0 and 1"),
        reliability: z.number().min(0).max(1).optional()
    }),
    testData: z.string().optional(),
    category: z.enum(["trading", "analysis", "defi", "nft", "social", "utility", "other"]).default("other"),
    complexity: z.enum(["basic", "intermediate", "advanced", "expert"]).default("intermediate")
});

export const verifySkillPerformanceAction: Action = {
    name: "VERIFY_SKILL_PERFORMANCE",

    similes: [
        "VERIFY_SKILL",
        "CHECK_SKILL_CLAIMS",
        "VALIDATE_SKILL_PERFORMANCE",
        "TRUST_CHECK_SKILL",
        "AUDIT_SKILL"
    ],

    description: `Verify AI skill performance claims using TrustWrapper's zero-knowledge verification system.

    This action:
    - Validates claimed accuracy, latency, and success rates against real performance
    - Generates objective trust scores based on verifiable metrics
    - Detects performance inflation or misleading claims
    - Creates zero-knowledge proofs preserving skill IP
    - Provides marketplace confidence ratings

    Essential for maintaining trust in Senpi's skills marketplace and protecting users from unreliable AI capabilities.`,

    validate: async (runtime: IAgentRuntime, message: Memory): Promise<boolean> => {
        try {
            // Check if TrustWrapper service is available
            const trustWrapperService = runtime.getService("trustWrapper") as TrustWrapperService;
            if (!trustWrapperService) {
                console.warn("TrustWrapper service not available for skill verification");
                return false;
            }

            // Validate message contains skill verification data
            const content = message.content;
            if (!content || typeof content !== "object") {
                return false;
            }

            // Check for required skill fields
            const hasRequiredFields = [
                "skillId", "performanceClaims"
            ].every(field => field in content);

            return hasRequiredFields;
        } catch (error) {
            console.error("Error validating skill verification request:", error);
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
            const skillData = SkillPerformanceSchema.parse(message.content);

            // Get TrustWrapper service
            const trustWrapperService = runtime.getService("trustWrapper") as TrustWrapperService;

            // Create verification request
            const verificationRequest: SkillVerificationRequest = {
                skillId: skillData.skillId,
                performanceClaims: skillData.performanceClaims,
                testData: skillData.testData || await trustWrapperService.generateTestData(skillData.category),
                metadata: {
                    framework: "senpi-eliza",
                    version: "1.0.0",
                    category: skillData.category,
                    complexity: skillData.complexity,
                    author: message.userId || "anonymous",
                    timestamp: Date.now()
                }
            };

            // Perform skill verification
            const verification: SkillVerificationResult = await trustWrapperService.verifySkillPerformance(
                verificationRequest
            );

            const latency = performance.now() - startTime;

            // Generate response based on verification result
            let responseText = "";
            let statusEmoji = "";
            let trustBadge = "";

            switch (verification.status) {
                case "verified":
                    statusEmoji = "✅";
                    trustBadge = verification.confidence > 0.9 ? "🏆 **GOLD VERIFIED**" :
                                verification.confidence > 0.7 ? "🥈 **SILVER VERIFIED**" :
                                "🥉 **BRONZE VERIFIED**";
                    responseText = `**Skill Performance Verified**\n\n` +
                        `${statusEmoji} ${trustBadge}\n` +
                        `🎯 **Verification Confidence**: ${(verification.confidence * 100).toFixed(1)}%\n` +
                        `📊 **Trust Score**: ${(verification.trustScore * 100).toFixed(1)}%\n` +
                        `🚀 **Status**: Claims validated and verified`;
                    break;

                case "failed":
                    statusEmoji = "❌";
                    responseText = `**Skill Verification Failed**\n\n` +
                        `${statusEmoji} **Status**: Claims Not Verified\n` +
                        `🎯 **Confidence**: ${(verification.confidence * 100).toFixed(1)}%\n` +
                        `📊 **Issues Found**: ${verification.issues.length}\n` +
                        `🚨 **Problems**: ${verification.issues.join(", ")}\n` +
                        `💡 **Recommendation**: Review and update performance claims`;
                    break;

                case "pending":
                    statusEmoji = "⏳";
                    responseText = `**Skill Verification Pending**\n\n` +
                        `${statusEmoji} **Status**: Verification in progress\n` +
                        `🔄 **Progress**: Additional testing required\n` +
                        `⏱️ **Expected**: Results available within 24 hours`;
                    break;

                default:
                    statusEmoji = "❓";
                    responseText = `**Verification Incomplete**\n\n` +
                        `${statusEmoji} **Status**: Unknown\n` +
                        `⏱️ **Issue**: Verification service unavailable`;
            }

            // Add detailed performance analysis
            if (verification.performanceAnalysis) {
                responseText += `\n\n**Performance Analysis**\n`;

                const analysis = verification.performanceAnalysis;

                // Accuracy validation
                if (analysis.accuracyValidation) {
                    const accuracyIcon = analysis.accuracyValidation.verified ? "✅" : "❌";
                    responseText += `${accuracyIcon} **Accuracy**: Claimed ${(skillData.performanceClaims.accuracy * 100).toFixed(1)}% → Measured ${(analysis.accuracyValidation.measuredValue * 100).toFixed(1)}%\n`;
                }

                // Latency validation
                if (analysis.latencyValidation) {
                    const latencyIcon = analysis.latencyValidation.verified ? "✅" : "❌";
                    responseText += `${latencyIcon} **Latency**: Claimed ${skillData.performanceClaims.latency}ms → Measured ${analysis.latencyValidation.measuredValue.toFixed(1)}ms\n`;
                }

                // Success rate validation
                if (analysis.successRateValidation) {
                    const successIcon = analysis.successRateValidation.verified ? "✅" : "❌";
                    responseText += `${successIcon} **Success Rate**: Claimed ${(skillData.performanceClaims.successRate * 100).toFixed(1)}% → Measured ${(analysis.successRateValidation.measuredValue * 100).toFixed(1)}%\n`;
                }
            }

            // Add verification details
            responseText += `\n\n**Verification Details**\n` +
                `⚡ **Verification Time**: ${latency.toFixed(2)}ms\n` +
                `🔐 **ZK Proof**: ${verification.zkProof ? "Generated" : "Unavailable"}\n` +
                `📋 **Test Cases**: ${verification.testCasesRun || "Unknown"} executed\n` +
                `🔗 **Verification ID**: \`${verification.verificationId}\``;

            // Add marketplace recommendations
            if (verification.marketplaceRecommendation) {
                responseText += `\n\n**Marketplace Recommendation**\n`;

                switch (verification.marketplaceRecommendation.listing) {
                    case "featured":
                        responseText += `🌟 **Featured Listing**: High-performance skill recommended for featured placement\n`;
                        break;
                    case "standard":
                        responseText += `📋 **Standard Listing**: Skill meets marketplace quality standards\n`;
                        break;
                    case "restricted":
                        responseText += `⚠️ **Restricted Listing**: Skill requires improvement before full marketplace access\n`;
                        break;
                    case "rejected":
                        responseText += `🚫 **Listing Rejected**: Skill does not meet minimum quality requirements\n`;
                        break;
                }

                if (verification.marketplaceRecommendation.suggestedPrice) {
                    responseText += `💰 **Suggested Pricing**: $${verification.marketplaceRecommendation.suggestedPrice}/use\n`;
                }
            }

            // Store verification result in memory
            await runtime.messageManager.createMemory({
                id: `skill-verification-${verification.verificationId}`,
                userId: message.userId,
                agentId: runtime.agentId,
                content: {
                    type: "skill_verification",
                    verificationId: verification.verificationId,
                    skillId: skillData.skillId,
                    result: verification,
                    timestamp: Date.now()
                },
                roomId: message.roomId,
                embedding: message.embedding
            });

            // Send response
            callback({
                text: responseText,
                action: "SKILL_VERIFICATION_COMPLETE",
                source: message.content?.source || "skill_verification"
            });

        } catch (error) {
            console.error("Error in skill performance verification:", error);

            callback({
                text: `❌ **Skill Verification Error**\n\n` +
                    `Unable to verify skill performance due to system error.\n` +
                    `Please ensure all required data is provided and try again.\n\n` +
                    `**Error**: ${error instanceof Error ? error.message : "Unknown error"}`,
                action: "VERIFICATION_ERROR",
                source: message.content?.source || "skill_verification"
            });
        }
    },

    examples: [
        [
            {
                user: "{{user1}}",
                content: {
                    text: "Verify my DeFi yield optimization skill performance",
                    skillId: "skill_defi_yield_optimizer_v2",
                    performanceClaims: {
                        accuracy: 0.87,
                        latency: 150,
                        successRate: 0.92
                    },
                    category: "defi",
                    complexity: "advanced"
                }
            },
            {
                user: "{{agentName}}",
                content: {
                    text: "✅ 🏆 **GOLD VERIFIED**\n\n✅ **Status**: Claims validated and verified\n🎯 **Verification Confidence**: 94.2%\n📊 **Trust Score**: 91.7%\n🚀 **Status**: Claims validated and verified\n\n**Performance Analysis**\n✅ **Accuracy**: Claimed 87.0% → Measured 89.3%\n✅ **Latency**: Claimed 150ms → Measured 142.7ms\n✅ **Success Rate**: Claimed 92.0% → Measured 94.1%\n\n**Verification Details**\n⚡ **Verification Time**: 89.43ms\n🔐 **ZK Proof**: Generated\n📋 **Test Cases**: 50 executed\n🔗 **Verification ID**: `vrf_skill_defi_abc123`\n\n**Marketplace Recommendation**\n🌟 **Featured Listing**: High-performance skill recommended for featured placement\n💰 **Suggested Pricing**: $0.25/use",
                    action: "SKILL_VERIFICATION_COMPLETE"
                }
            }
        ],
        [
            {
                user: "{{user1}}",
                content: {
                    text: "Check if my NFT price prediction skill claims are accurate",
                    skillId: "skill_nft_price_predictor",
                    performanceClaims: {
                        accuracy: 0.95,
                        latency: 50,
                        successRate: 0.98
                    },
                    category: "nft",
                    complexity: "expert"
                }
            },
            {
                user: "{{agentName}}",
                content: {
                    text: "❌ **Skill Verification Failed**\n\n❌ **Status**: Claims Not Verified\n🎯 **Confidence**: 23.1%\n📊 **Issues Found**: 3\n🚨 **Problems**: Accuracy overstated, Latency understated, Sample size insufficient\n💡 **Recommendation**: Review and update performance claims\n\n**Performance Analysis**\n❌ **Accuracy**: Claimed 95.0% → Measured 67.8%\n❌ **Latency**: Claimed 50ms → Measured 287.2ms\n❌ **Success Rate**: Claimed 98.0% → Measured 71.3%",
                    action: "SKILL_VERIFICATION_COMPLETE"
                }
            }
        ]
    ] as ActionExample[][],
};

export default verifySkillPerformanceAction;

/**
 * TrustWrapper Evaluator for Senpi Integration
 *
 * Evaluates AI agent responses and actions for trust, compliance,
 * and quality scoring using TrustWrapper verification metrics.
 */

import { Evaluator, IAgentRuntime, Memory, State } from "@ai16z/eliza";
import { trustWrapperService } from "../services/trustWrapperService.js";
import {
    TrustMetrics,
    VerificationResult,
    SkillVerificationResult
} from "../types/index.js";

export const trustWrapperEvaluator: Evaluator = {
    name: "trustwrapper-quality",
    description: "Evaluates AI agent responses using TrustWrapper trust and quality metrics",

    validate: async (runtime: IAgentRuntime, message: Memory, state?: State): Promise<boolean> => {
        // Only evaluate responses that contain actions or decisions
        const text = message.content.text?.toLowerCase() || "";

        const evaluationTriggers = [
            "buy", "sell", "trade", "invest", "recommend", "suggest",
            "decision", "action", "verification", "approved", "rejected"
        ];

        return evaluationTriggers.some(trigger => text.includes(trigger)) ||
               message.content.action !== undefined ||
               message.content.verificationId !== undefined;
    },

    handler: async (runtime: IAgentRuntime, message: Memory, state?: State): Promise<number> => {
        try {
            console.log("🔍 Evaluating response quality with TrustWrapper...");

            const evaluation = await evaluateResponseQuality(runtime, message, state);

            console.log(`✅ TrustWrapper evaluation: ${(evaluation.score * 100).toFixed(1)}% quality`);

            return evaluation.score;
        } catch (error) {
            console.error("❌ TrustWrapper evaluation failed:", error);

            // Return neutral score on evaluation failure
            return 0.5;
        }
    }
};

/**
 * Comprehensive response quality evaluation
 */
async function evaluateResponseQuality(
    runtime: IAgentRuntime,
    message: Memory,
    state?: State
): Promise<QualityEvaluation> {
    const evaluation: QualityEvaluation = {
        score: 0.5, // Default neutral score
        factors: {},
        trustMetrics: null,
        recommendations: []
    };

    // Factor 1: Verification Status (40% weight)
    if (message.content.verificationId) {
        const verificationScore = await evaluateVerificationStatus(message);
        evaluation.factors.verification = verificationScore;
        evaluation.score += verificationScore * 0.4;
    } else {
        evaluation.score += 0.2; // Neutral for unverified responses
    }

    // Factor 2: Content Quality (30% weight)
    const contentScore = evaluateContentQuality(message);
    evaluation.factors.content = contentScore;
    evaluation.score += contentScore * 0.3;

    // Factor 3: Risk Assessment (20% weight)
    const riskScore = evaluateRiskAssessment(message);
    evaluation.factors.risk = riskScore;
    evaluation.score += riskScore * 0.2;

    // Factor 4: Compliance (10% weight)
    const complianceScore = evaluateCompliance(message);
    evaluation.factors.compliance = complianceScore;
    evaluation.score += complianceScore * 0.1;

    // Normalize score to 0-1 range
    evaluation.score = Math.max(0, Math.min(1, evaluation.score));

    // Generate recommendations
    evaluation.recommendations = generateQualityRecommendations(evaluation);

    return evaluation;
}

/**
 * Evaluate verification status and trust metrics
 */
async function evaluateVerificationStatus(message: Memory): Promise<number> {
    const metadata = message.content.metadata;
    if (!metadata) return 0.3;

    // High score for approved verifications
    if (metadata.status === "approved" && metadata.confidence > 0.8) {
        return 0.9;
    }

    // Medium score for flagged but reasonable confidence
    if (metadata.status === "flagged" && metadata.confidence > 0.6) {
        return 0.6;
    }

    // Low score for rejected or low confidence
    if (metadata.status === "rejected" || metadata.confidence < 0.5) {
        return 0.2;
    }

    // Skill verification scoring
    if (metadata.trustScore !== undefined) {
        return Math.min(0.9, metadata.trustScore);
    }

    return 0.5; // Default for unclear verification status
}

/**
 * Evaluate content quality and informativeness
 */
function evaluateContentQuality(message: Memory): Promise<number> {
    const text = message.content.text || "";
    let score = 0.5; // Base score

    // Length and structure
    if (text.length > 100) score += 0.1;
    if (text.length > 300) score += 0.1;

    // Professional formatting (markdown, structured data)
    if (text.includes("**") || text.includes("*")) score += 0.1;
    if (text.includes("✅") || text.includes("📊") || text.includes("🎯")) score += 0.1;

    // Specific details and data
    if (text.includes("%") || text.includes("$") || text.includes("confidence")) score += 0.1;
    if (text.includes("risk") || text.includes("score")) score += 0.1;

    // Clear recommendations or actionable items
    if (text.includes("recommend") || text.includes("suggest") || text.includes("should")) score += 0.1;

    // Compliance and professional language
    if (text.includes("compliance") || text.includes("regulation")) score += 0.1;

    return Promise.resolve(Math.min(0.9, score));
}

/**
 * Evaluate risk assessment quality
 */
function evaluateRiskAssessment(message: Memory): number {
    const text = message.content.text?.toLowerCase() || "";
    const metadata = message.content.metadata || {};

    let score = 0.5; // Base score

    // Explicit risk metrics mentioned
    if (metadata.riskScore !== undefined) {
        // Good risk scores (moderate risk is often appropriate)
        if (metadata.riskScore >= 0.1 && metadata.riskScore <= 0.4) {
            score += 0.3;
        } else if (metadata.riskScore > 0.4 && metadata.riskScore <= 0.7) {
            score += 0.1; // Higher risk acknowledged
        }
    }

    // Risk-aware language
    if (text.includes("risk") || text.includes("volatility")) score += 0.1;
    if (text.includes("consider") || text.includes("caution")) score += 0.1;
    if (text.includes("market conditions") || text.includes("liquidity")) score += 0.1;

    // Risk mitigation suggestions
    if (text.includes("position sizing") || text.includes("diversif")) score += 0.1;
    if (text.includes("stop loss") || text.includes("limit")) score += 0.1;

    return Math.min(0.9, score);
}

/**
 * Evaluate compliance awareness
 */
function evaluateCompliance(message: Memory): number {
    const text = message.content.text?.toLowerCase() || "";
    const metadata = message.content.metadata || {};

    let score = 0.6; // Base compliance score (assume good faith)

    // Explicit compliance mentions
    if (text.includes("compliance") || text.includes("regulatory")) score += 0.2;
    if (text.includes("institutional") || text.includes("professional")) score += 0.1;

    // Compliance flags in metadata
    if (metadata.complianceFlags) {
        const flagCount = Array.isArray(metadata.complianceFlags) ?
                         metadata.complianceFlags.length : 0;
        if (flagCount === 0) {
            score += 0.2; // Clean compliance
        } else if (flagCount <= 2) {
            score += 0.1; // Minor issues
        } else {
            score -= 0.2; // Significant compliance concerns
        }
    }

    // Professional disclaimers and warnings
    if (text.includes("not financial advice") || text.includes("consult")) score += 0.1;
    if (text.includes("past performance") || text.includes("no guarantee")) score += 0.1;

    return Math.max(0.1, Math.min(0.9, score));
}

/**
 * Generate quality improvement recommendations
 */
function generateQualityRecommendations(evaluation: QualityEvaluation): string[] {
    const recommendations: string[] = [];

    // Verification recommendations
    if ((evaluation.factors.verification || 0) < 0.6) {
        recommendations.push("Consider using TrustWrapper verification for higher trust scores");
        recommendations.push("Provide more detailed reasoning for decisions");
    }

    // Content quality recommendations
    if ((evaluation.factors.content || 0) < 0.6) {
        recommendations.push("Include more specific data and metrics");
        recommendations.push("Use professional formatting and structure");
        recommendations.push("Provide clear actionable recommendations");
    }

    // Risk assessment recommendations
    if ((evaluation.factors.risk || 0) < 0.6) {
        recommendations.push("Include explicit risk assessment and scores");
        recommendations.push("Mention market conditions and volatility");
        recommendations.push("Suggest risk mitigation strategies");
    }

    // Compliance recommendations
    if ((evaluation.factors.compliance || 0) < 0.7) {
        recommendations.push("Add appropriate regulatory disclaimers");
        recommendations.push("Consider institutional compliance requirements");
        recommendations.push("Include professional investment advice warnings");
    }

    // Overall quality recommendations
    if (evaluation.score < 0.7) {
        recommendations.push("Overall response quality could be improved");
        recommendations.push("Consider using TrustWrapper verification for enhanced credibility");
    }

    return recommendations;
}

/**
 * Quality evaluation result interface
 */
interface QualityEvaluation {
    score: number; // 0-1 overall quality score
    factors: {
        verification?: number;
        content?: number;
        risk?: number;
        compliance?: number;
    };
    trustMetrics: TrustMetrics | null;
    recommendations: string[];
}

/**
 * TrustWrapper Verification Skill for Senpi AI
 *
 * This skill provides real-time AI verification capabilities for Senpi's autonomous agents,
 * enabling trust scoring, compliance validation, and zero-knowledge verification of
 * trading decisions and AI performance claims.
 *
 * @author TrustWrapper by Lamassu Labs
 * @version 1.0.0
 */

import { Plugin } from "@ai16z/eliza";
import { verifyTradingDecisionAction } from "./actions/verifyTradingDecision.js";
import { verifySkillPerformanceAction } from "./actions/verifySkillPerformance.js";
import { generateComplianceReportAction } from "./actions/generateComplianceReport.js";
import { trustWrapperProvider } from "./providers/trustWrapperProvider.js";
import { trustWrapperEvaluator } from "./evaluators/trustWrapperEvaluator.js";
import { trustWrapperService } from "./services/trustWrapperService.js";

/**
 * TrustWrapper Plugin for Senpi AI Platform
 *
 * Provides comprehensive AI verification capabilities including:
 * - Real-time trading decision verification (<1ms latency)
 * - AI skill performance validation
 * - Regulatory compliance monitoring
 * - Zero-knowledge proof generation
 * - Trust scoring and risk assessment
 */
export const trustWrapperPlugin: Plugin = {
    name: "trustwrapper-verification",
    description: "Universal AI verification and compliance validation for autonomous agents",

    // Core verification actions available to Senpi agents
    actions: [
        verifyTradingDecisionAction,
        verifySkillPerformanceAction,
        generateComplianceReportAction
    ],

    // Data providers for verification context
    providers: [
        trustWrapperProvider
    ],

    // Evaluation logic for trust scoring
    evaluators: [
        trustWrapperEvaluator
    ],

    // Background services for continuous monitoring
    services: [
        trustWrapperService
    ],

    // Plugin metadata
    version: "1.0.0",
    author: "TrustWrapper by Lamassu Labs",

    // Integration configuration
    settings: {
        // TrustWrapper API configuration
        TRUSTWRAPPER_API_URL: process.env.TRUSTWRAPPER_API_URL || "https://api.trustwrapper.io",
        TRUSTWRAPPER_API_KEY: process.env.TRUSTWRAPPER_API_KEY,

        // Verification settings
        VERIFICATION_TIMEOUT_MS: 5000, // 5 second timeout for verification calls
        ENABLE_ZK_PROOFS: true,
        ENABLE_COMPLIANCE_MONITORING: true,

        // Performance settings
        CACHE_VERIFICATION_RESULTS: true,
        CACHE_TTL_SECONDS: 300, // 5 minute cache for verification results

        // Security settings
        REQUIRE_SIGNATURE_VERIFICATION: true,
        ENABLE_AUDIT_LOGGING: true
    }
};

export default trustWrapperPlugin;

// Export individual components for advanced usage
export {
    verifyTradingDecisionAction,
    verifySkillPerformanceAction,
    generateComplianceReportAction,
    trustWrapperProvider,
    trustWrapperEvaluator,
    trustWrapperService
};

// Export types for skill developers
export * from "./types/index.js";

/**
 * TrustWrapper Provider for Senpi Integration
 *
 * Provides verification context, market data, and trust metrics
 * to enhance AI agent decision-making with TrustWrapper intelligence.
 */

import { Provider, IAgentRuntime, Memory, State } from "@ai16z/eliza";
import { trustWrapperService } from "../services/trustWrapperService.js";
import {
    MarketContext,
    TrustMetrics,
    VerificationMetrics,
    SenpiVerificationContext
} from "../types/index.js";

export const trustWrapperProvider: Provider = {
    name: "trustwrapper-context",
    description: "Provides TrustWrapper verification context and market intelligence for AI agents",

    get: async (runtime: IAgentRuntime, message: Memory, state?: State): Promise<string> => {
        try {
            const context = await gatherVerificationContext(runtime, message, state);
            return formatContextForAgent(context);
        } catch (error) {
            console.error("Failed to get TrustWrapper context:", error);
            return "TrustWrapper context unavailable - operating in standalone mode";
        }
    }
};

/**
 * Gather comprehensive verification context
 */
async function gatherVerificationContext(
    runtime: IAgentRuntime,
    message: Memory,
    state?: State
): Promise<VerificationContext> {
    const context: VerificationContext = {
        timestamp: Date.now(),
        agentId: runtime.agentId || "senpi_agent",
        sessionId: state?.sessionId || `session_${Date.now()}`,
        userContext: extractUserContext(message),
        marketData: null,
        trustMetrics: null,
        verificationHistory: null
    };

    // Get market context if trading-related
    if (isTradeRelated(message)) {
        const asset = extractAssetFromMessage(message);
        if (asset) {
            try {
                context.marketData = await trustWrapperService.getMarketContext(asset);
            } catch (error) {
                console.warn("Failed to get market context:", error);
            }
        }
    }

    // Get user trust metrics if available
    const userId = message.userId || message.content?.accountId;
    if (userId) {
        context.trustMetrics = await getUserTrustMetrics(userId);
        context.verificationHistory = await getVerificationHistory(userId);
    }

    return context;
}

/**
 * Extract user context from message
 */
function extractUserContext(message: Memory): any {
    return {
        userId: message.userId,
        accountId: message.content?.accountId,
        userWallet: message.content?.userWallet,
        institutionalLevel: message.content?.institutionalLevel || "retail",
        riskProfile: message.content?.riskProfile || "moderate",
        tradingExperience: message.content?.tradingExperience || "intermediate"
    };
}

/**
 * Check if message is trade-related
 */
function isTradeRelated(message: Memory): boolean {
    const text = message.content.text?.toLowerCase() || "";
    const tradeKeywords = [
        "buy", "sell", "trade", "trading", "invest", "investment",
        "position", "portfolio", "market", "price", "asset"
    ];

    return tradeKeywords.some(keyword => text.includes(keyword)) ||
           message.content.action === "buy" ||
           message.content.action === "sell" ||
           message.content.asset !== undefined;
}

/**
 * Extract asset symbol from message
 */
function extractAssetFromMessage(message: Memory): string | null {
    // Direct asset specification
    if (message.content.asset) {
        return message.content.asset;
    }

    // Parse from text
    const text = message.content.text?.toUpperCase() || "";
    const commonAssets = ["BTC", "ETH", "ADA", "SOL", "MATIC", "DOT", "LINK", "UNI"];

    for (const asset of commonAssets) {
        if (text.includes(asset)) {
            return asset;
        }
    }

    // Look for crypto patterns like $BTC, BTC-USD, etc.
    const assetPattern = /\$?([A-Z]{3,5})(-USD|-USDT)?/g;
    const match = assetPattern.exec(text);
    if (match && match[1]) {
        return match[1];
    }

    return null;
}

/**
 * Get user trust metrics (mock implementation)
 */
async function getUserTrustMetrics(userId: string): Promise<TrustMetrics | null> {
    try {
        // In production, this would call TrustWrapper API
        // For now, return mock data based on user activity
        return {
            overallScore: 0.75 + Math.random() * 0.25, // 75-100%
            strategyConsistency: 0.8 + Math.random() * 0.2,
            marketAlignment: 0.7 + Math.random() * 0.3,
            riskManagement: 0.85 + Math.random() * 0.15,
            complianceScore: 0.95 + Math.random() * 0.05
        };
    } catch (error) {
        console.warn("Failed to get user trust metrics:", error);
        return null;
    }
}

/**
 * Get verification history summary (mock implementation)
 */
async function getVerificationHistory(userId: string): Promise<VerificationMetrics | null> {
    try {
        // Mock verification history
        return {
            totalVerifications: 15 + Math.floor(Math.random() * 50),
            successRate: 0.85 + Math.random() * 0.15,
            averageLatency: 50 + Math.random() * 100, // ms
            trustScoreDistribution: {
                "high": 0.6,
                "medium": 0.3,
                "low": 0.1
            },
            complianceViolations: Math.floor(Math.random() * 3),
            periodicStats: {
                daily: {
                    period: "today",
                    verifications: Math.floor(Math.random() * 10),
                    successRate: 0.9 + Math.random() * 0.1,
                    averageLatency: 45 + Math.random() * 30,
                    topIssues: [
                        { issue: "Market volatility", count: 2 },
                        { issue: "Low liquidity", count: 1 }
                    ]
                },
                weekly: {
                    period: "this week",
                    verifications: 25 + Math.floor(Math.random() * 25),
                    successRate: 0.87 + Math.random() * 0.13,
                    averageLatency: 55 + Math.random() * 35,
                    topIssues: [
                        { issue: "Risk tolerance exceeded", count: 5 },
                        { issue: "Market volatility", count: 3 }
                    ]
                },
                monthly: {
                    period: "this month",
                    verifications: 100 + Math.floor(Math.random() * 100),
                    successRate: 0.85 + Math.random() * 0.15,
                    averageLatency: 60 + Math.random() * 40,
                    topIssues: [
                        { issue: "Market volatility", count: 12 },
                        { issue: "Risk tolerance exceeded", count: 8 },
                        { issue: "Low liquidity", count: 5 }
                    ]
                }
            }
        };
    } catch (error) {
        console.warn("Failed to get verification history:", error);
        return null;
    }
}

/**
 * Format context for AI agent consumption
 */
function formatContextForAgent(context: VerificationContext): string {
    let contextString = `TrustWrapper Verification Context:\n\n`;

    // Basic context
    contextString += `🤖 Agent: ${context.agentId}\n`;
    contextString += `📅 Timestamp: ${new Date(context.timestamp).toISOString()}\n`;

    // User context
    if (context.userContext) {
        contextString += `👤 User Level: ${context.userContext.institutionalLevel}\n`;
        contextString += `🎯 Risk Profile: ${context.userContext.riskProfile}\n`;
    }

    // Market data
    if (context.marketData) {
        contextString += `\n📈 Market Context:\n`;
        contextString += `   Volatility: ${(context.marketData.volatility * 100).toFixed(1)}%\n`;
        contextString += `   24h Volume: $${(context.marketData.volume24h / 1000000).toFixed(1)}M\n`;
        contextString += `   Price Change: ${(context.marketData.priceChange24h * 100).toFixed(1)}%\n`;
        contextString += `   Sentiment: ${context.marketData.marketSentiment}\n`;
        contextString += `   Liquidity: ${(context.marketData.liquidityScore * 100).toFixed(0)}%\n`;
    }

    // Trust metrics
    if (context.trustMetrics) {
        contextString += `\n🛡️ Trust Metrics:\n`;
        contextString += `   Overall Score: ${(context.trustMetrics.overallScore * 100).toFixed(0)}%\n`;
        contextString += `   Strategy Consistency: ${(context.trustMetrics.strategyConsistency * 100).toFixed(0)}%\n`;
        contextString += `   Risk Management: ${(context.trustMetrics.riskManagement * 100).toFixed(0)}%\n`;
        contextString += `   Compliance Score: ${(context.trustMetrics.complianceScore * 100).toFixed(0)}%\n`;
    }

    // Verification history
    if (context.verificationHistory) {
        const history = context.verificationHistory;
        contextString += `\n📊 Verification History:\n`;
        contextString += `   Total Verifications: ${history.totalVerifications}\n`;
        contextString += `   Success Rate: ${(history.successRate * 100).toFixed(1)}%\n`;
        contextString += `   Avg Latency: ${history.averageLatency.toFixed(0)}ms\n`;
        contextString += `   Compliance Violations: ${history.complianceViolations}\n`;

        if (history.periodicStats.daily.verifications > 0) {
            contextString += `   Today: ${history.periodicStats.daily.verifications} verifications\n`;
        }
    }

    contextString += `\nThis context can inform verification decisions and risk assessments.`;

    return contextString;
}

/**
 * Verification context interface
 */
interface VerificationContext {
    timestamp: number;
    agentId: string;
    sessionId: string;
    userContext: any;
    marketData: MarketContext | null;
    trustMetrics: TrustMetrics | null;
    verificationHistory: VerificationMetrics | null;
}

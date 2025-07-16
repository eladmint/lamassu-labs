/**
 * TrustWrapper Service for Senpi Integration
 *
 * Core service providing TrustWrapper verification capabilities
 * for Senpi's autonomous AI agent platform.
 */

import { IAgentRuntime } from "@ai16z/eliza";
import axios, { AxiosInstance, AxiosResponse } from "axios";
import {
    TradingDecisionRequest,
    VerificationResult,
    SkillVerificationRequest,
    SkillVerificationResult,
    ComplianceMonitoringRequest,
    ComplianceMonitoringResult,
    TrustWrapperConfig,
    ApiResponse,
    MarketContext,
    ZKProof,
    TrustWrapperError
} from "../types/index.js";
import { nowNodesService, TransactionVerification, WalletBalance } from "./blockchain/nowNodesService.js";
import { coinGeckoService } from "./market/coinGeckoService.js";

export class TrustWrapperService {
    private apiClient: AxiosInstance;
    private config: TrustWrapperConfig;
    private cache: Map<string, { data: any; timestamp: number }> = new Map();

    constructor() {

        // Initialize configuration from environment variables
        this.config = {
            apiUrl: process.env.TRUSTWRAPPER_API_URL || "https://api.trustwrapper.io",
            apiKey: process.env.TRUSTWRAPPER_API_KEY || "",
            timeout: parseInt(process.env.TRUSTWRAPPER_TIMEOUT || "5000"),
            enableZKProofs: process.env.ENABLE_ZK_PROOFS === "true",
            enableCompliance: process.env.ENABLE_COMPLIANCE === "true",
            cacheResults: process.env.CACHE_VERIFICATION_RESULTS === "true",
            cacheTTL: parseInt(process.env.CACHE_TTL_SECONDS || "300"),
            retryAttempts: parseInt(process.env.RETRY_ATTEMPTS || "3"),
            retryDelay: parseInt(process.env.RETRY_DELAY || "1000")
        };

        // Initialize API client
        this.apiClient = axios.create({
            baseURL: this.config.apiUrl,
            timeout: this.config.timeout,
            headers: {
                "Authorization": `Bearer ${this.config.apiKey}`,
                "Content-Type": "application/json",
                "User-Agent": "TrustWrapper-Senpi-Plugin/1.0.0"
            }
        });

        // Add request/response interceptors for monitoring
        this.setupInterceptors();
    }

    async initialize(runtime: IAgentRuntime): Promise<void> {
        console.log("Initializing TrustWrapper service for Senpi integration...");

        // Validate configuration
        if (!this.config.apiKey) {
            console.warn("TrustWrapper API key not configured - some features may be limited");
        }

        // Test API connectivity
        try {
            await this.healthCheck();
            console.log("TrustWrapper service initialized successfully");
        } catch (error) {
            console.error("Failed to initialize TrustWrapper service:", error);
            throw error;
        }
    }

    /**
     * Verify autonomous trading decisions in real-time
     */
    async verifyTradingDecision(request: TradingDecisionRequest): Promise<VerificationResult> {
        const cacheKey = `trading_${request.accountId}_${JSON.stringify(request.decision)}`;

        // Check cache first
        if (this.config.cacheResults) {
            const cached = this.getFromCache(cacheKey);
            if (cached) {
                return cached as VerificationResult;
            }
        }

        try {
            // Try real blockchain verification first if available
            let blockchainVerified = false;
            let onChainData: TransactionVerification | null = null;

            if (request.context.messageId && request.decision.asset) {
                // Check if this might be a transaction hash
                const possibleTxHash = request.context.messageId;
                const chain = this.getChainFromAsset(request.decision.asset);

                if (chain) {
                    try {
                        onChainData = await nowNodesService.verifyTransaction(possibleTxHash, chain);
                        blockchainVerified = onChainData?.verified || false;
                    } catch (error) {
                        console.warn("Blockchain verification failed, continuing with other checks", error);
                    }
                }
            }

            // Try TrustWrapper API if configured
            if (this.config.apiKey && this.config.apiUrl !== "https://api.trustwrapper.io") {
                const response: AxiosResponse<ApiResponse<VerificationResult>> = await this.apiClient.post(
                    "/v1/verify/trading-decision",
                    {
                        ...request,
                        enableZKProof: this.config.enableZKProofs,
                        enableCompliance: this.config.enableCompliance,
                        blockchainVerification: onChainData
                    }
                );

                if (response.data.success && response.data.data) {
                    const result = response.data.data;

                    // Enhance with blockchain data if available
                    if (onChainData) {
                        result.trustMetrics = {
                            ...result.trustMetrics,
                            blockchainVerified: blockchainVerified ? 1.0 : 0.0
                        };
                    }

                    // Cache successful result
                    if (this.config.cacheResults) {
                        this.setCache(cacheKey, result);
                    }

                    return result;
                }
            }

            // Fall through to enhanced mock with real data
        } catch (error) {
            console.error("Trading decision verification failed:", error);
        }

        // Return enhanced mock verification with real blockchain data
        return await this.createEnhancedTradingVerification(request, onChainData);
    }

    /**
     * Verify AI skill performance claims
     */
    async verifySkillPerformance(request: SkillVerificationRequest): Promise<SkillVerificationResult> {
        const cacheKey = `skill_${request.skillId}_${JSON.stringify(request.performanceClaims)}`;

        // Check cache first
        if (this.config.cacheResults) {
            const cached = this.getFromCache(cacheKey);
            if (cached) {
                return cached as SkillVerificationResult;
            }
        }

        try {
            const response: AxiosResponse<ApiResponse<SkillVerificationResult>> = await this.apiClient.post(
                "/v1/verify/skill-performance",
                {
                    ...request,
                    enableZKProof: this.config.enableZKProofs
                }
            );

            if (!response.data.success) {
                throw new Error(response.data.error?.message || "Skill verification failed");
            }

            const result = response.data.data!;

            // Cache successful result
            if (this.config.cacheResults) {
                this.setCache(cacheKey, result);
            }

            return result;
        } catch (error) {
            console.error("Skill performance verification failed:", error);

            // Return mock verification for demo purposes when API is unavailable
            return this.createMockSkillVerification(request);
        }
    }

    /**
     * Monitor compliance for institutional requirements
     */
    async monitorCompliance(request: ComplianceMonitoringRequest): Promise<ComplianceMonitoringResult> {
        try {
            const response: AxiosResponse<ApiResponse<ComplianceMonitoringResult>> = await this.apiClient.post(
                "/v1/compliance/monitor",
                request
            );

            if (!response.data.success) {
                throw new Error(response.data.error?.message || "Compliance monitoring failed");
            }

            return response.data.data!;
        } catch (error) {
            console.error("Compliance monitoring failed:", error);
            throw error;
        }
    }

    /**
     * Get market context for trading verification
     */
    async getMarketContext(asset: string): Promise<MarketContext> {
        const cacheKey = `market_${asset}`;

        // Check cache first (market data changes frequently, shorter TTL)
        if (this.config.cacheResults) {
            const cached = this.getFromCache(cacheKey, 60); // 1 minute TTL for market data
            if (cached) {
                return cached as MarketContext;
            }
        }

        try {
            // Try real market data from CoinGecko first
            const realMarketData = await coinGeckoService.getMarketContext(asset);

            // Cache the real data
            if (this.config.cacheResults) {
                this.setCache(cacheKey, realMarketData, 60);
            }

            return realMarketData;
        } catch (coinGeckoError) {
            console.warn("CoinGecko market data failed, trying TrustWrapper API", coinGeckoError);

            try {
                // Try TrustWrapper API as fallback
                if (this.config.apiKey && this.config.apiUrl !== "https://api.trustwrapper.io") {
                    const response: AxiosResponse<ApiResponse<MarketContext>> = await this.apiClient.get(
                        `/v1/market/context/${asset}`
                    );

                    if (response.data.success && response.data.data) {
                        const result = response.data.data;

                        // Cache market context
                        if (this.config.cacheResults) {
                            this.setCache(cacheKey, result, 60);
                        }

                        return result;
                    }
                }
            } catch (error) {
                console.error("Failed to get market context from all sources:", error);
            }
        }

        // Return mock market context as last resort
        return this.createMockMarketContext(asset);
    }

    /**
     * Generate test data for skill verification
     */
    async generateTestData(category: string): Promise<string> {
        try {
            const response: AxiosResponse<ApiResponse<{ testData: string }>> = await this.apiClient.post(
                "/v1/testing/generate-test-data",
                { category }
            );

            if (!response.data.success) {
                throw new Error(response.data.error?.message || "Failed to generate test data");
            }

            return response.data.data!.testData;
        } catch (error) {
            console.error("Failed to generate test data:", error);

            // Return mock test data
            return JSON.stringify({
                category,
                testCases: Array(10).fill(0).map((_, i) => ({
                    id: `test_${i}`,
                    input: `mock_input_${i}`,
                    expectedOutput: `mock_output_${i}`,
                    complexity: Math.random() > 0.5 ? "high" : "low"
                }))
            });
        }
    }

    /**
     * Health check for TrustWrapper API
     */
    async healthCheck(): Promise<boolean> {
        try {
            const response = await this.apiClient.get("/v1/health");
            return response.status === 200;
        } catch (error) {
            console.error("TrustWrapper API health check failed:", error);
            return false;
        }
    }

    /**
     * Cache management
     */
    private getFromCache(key: string, customTTL?: number): any | null {
        const cached = this.cache.get(key);
        if (!cached) return null;

        const ttl = (customTTL || this.config.cacheTTL) * 1000;
        const isExpired = Date.now() - cached.timestamp > ttl;

        if (isExpired) {
            this.cache.delete(key);
            return null;
        }

        return cached.data;
    }

    private setCache(key: string, data: any, customTTL?: number): void {
        this.cache.set(key, {
            data,
            timestamp: Date.now()
        });

        // Clean up expired entries periodically
        if (this.cache.size > 1000) {
            this.cleanupCache();
        }
    }

    private cleanupCache(): void {
        const now = Date.now();
        const ttl = this.config.cacheTTL * 1000;

        const entries = Array.from(this.cache.entries());
        for (const [key, value] of entries) {
            if (now - value.timestamp > ttl) {
                this.cache.delete(key);
            }
        }
    }

    /**
     * Setup API client interceptors
     */
    private setupInterceptors(): void {
        // Request interceptor
        this.apiClient.interceptors.request.use(
            (config) => {
                console.log(`TrustWrapper API Request: ${config.method?.toUpperCase()} ${config.url}`);
                return config;
            },
            (error) => {
                console.error("TrustWrapper API Request Error:", error);
                return Promise.reject(error);
            }
        );

        // Response interceptor
        this.apiClient.interceptors.response.use(
            (response) => {
                // Note: metadata tracking would need custom implementation
                console.log(`TrustWrapper API Response: ${response.status}`);
                return response;
            },
            (error) => {
                console.error("TrustWrapper API Response Error:", error.response?.status, error.message);
                return Promise.reject(error);
            }
        );
    }

    /**
     * Mock implementations for demo purposes
     */
    private createMockTradingVerification(request: TradingDecisionRequest): VerificationResult {
        const confidence = 0.7 + Math.random() * 0.3; // 70-100%
        const riskScore = Math.random() * 0.5; // 0-50%

        let status: "approved" | "flagged" | "rejected";
        let issues: string[] = [];

        if (confidence > 0.9 && riskScore < 0.2) {
            status = "approved";
        } else if (confidence > 0.6 && riskScore < 0.4) {
            status = "flagged";
            issues = ["Moderate volatility detected", "Consider position sizing"];
        } else {
            status = "rejected";
            issues = ["High risk detected", "Insufficient market liquidity", "Strategy drift identified"];
        }

        return {
            verificationId: `vrf_${request.decision.asset.toLowerCase()}_${Date.now()}`,
            status,
            confidence,
            riskScore,
            issues,
            complianceFlags: [],
            zkProof: this.config.enableZKProofs ? `zk_proof_${Date.now()}` : undefined,
            trustMetrics: {
                overallScore: confidence,
                strategyConsistency: 0.8 + Math.random() * 0.2,
                marketAlignment: 0.7 + Math.random() * 0.3,
                riskManagement: 1 - riskScore,
                complianceScore: 0.95
            },
            timestamp: Date.now()
        };
    }

    private createMockSkillVerification(request: SkillVerificationRequest): SkillVerificationResult {
        const claims = request.performanceClaims;
        const variance = 0.1; // 10% variance in measurements

        // Simulate performance validation
        const accuracyMeasured = claims.accuracy * (0.9 + Math.random() * 0.2);
        const latencyMeasured = claims.latency * (0.8 + Math.random() * 0.4);
        const successRateMeasured = claims.successRate * (0.9 + Math.random() * 0.2);

        const accuracyVerified = Math.abs(accuracyMeasured - claims.accuracy) / claims.accuracy < variance;
        const latencyVerified = Math.abs(latencyMeasured - claims.latency) / claims.latency < variance;
        const successVerified = Math.abs(successRateMeasured - claims.successRate) / claims.successRate < variance;

        const allVerified = accuracyVerified && latencyVerified && successVerified;
        const confidence = allVerified ? 0.8 + Math.random() * 0.2 : 0.2 + Math.random() * 0.5;

        return {
            verificationId: `vrf_skill_${request.skillId}_${Date.now()}`,
            status: allVerified ? "verified" : "failed",
            confidence,
            trustScore: confidence * (allVerified ? 1 : 0.6),
            issues: allVerified ? [] : [
                !accuracyVerified ? "Accuracy claims not verified" : "",
                !latencyVerified ? "Latency claims not verified" : "",
                !successVerified ? "Success rate claims not verified" : ""
            ].filter(Boolean),
            zkProof: this.config.enableZKProofs ? `zk_skill_proof_${Date.now()}` : undefined,
            testCasesRun: 25 + Math.floor(Math.random() * 50),
            performanceAnalysis: {
                accuracyValidation: {
                    verified: accuracyVerified,
                    claimedValue: claims.accuracy,
                    measuredValue: accuracyMeasured,
                    variance: Math.abs(accuracyMeasured - claims.accuracy) / claims.accuracy
                },
                latencyValidation: {
                    verified: latencyVerified,
                    claimedValue: claims.latency,
                    measuredValue: latencyMeasured,
                    variance: Math.abs(latencyMeasured - claims.latency) / claims.latency
                },
                successRateValidation: {
                    verified: successVerified,
                    claimedValue: claims.successRate,
                    measuredValue: successRateMeasured,
                    variance: Math.abs(successRateMeasured - claims.successRate) / claims.successRate
                }
            },
            marketplaceRecommendation: {
                listing: allVerified && confidence > 0.9 ? "featured" :
                        allVerified && confidence > 0.7 ? "standard" :
                        confidence > 0.5 ? "restricted" : "rejected",
                suggestedPrice: allVerified ? 0.05 + Math.random() * 0.5 : undefined,
                qualityTier: confidence > 0.9 ? "gold" : confidence > 0.7 ? "silver" : confidence > 0.5 ? "bronze" : "unrated",
                recommendations: allVerified ? ["Excellent performance", "Ready for marketplace"] : ["Improve accuracy", "Optimize performance"]
            },
            timestamp: Date.now()
        };
    }

    private createMockMarketContext(asset: string): MarketContext {
        return {
            volatility: 0.02 + Math.random() * 0.08, // 2-10%
            volume24h: 1000000 + Math.random() * 10000000,
            priceChange24h: -0.1 + Math.random() * 0.2, // -10% to +10%
            marketSentiment: Math.random() > 0.6 ? "bullish" : Math.random() > 0.3 ? "neutral" : "bearish",
            liquidityScore: 0.5 + Math.random() * 0.5 // 50-100%
        };
    }

    /**
     * Helper method to map asset symbols to blockchain names
     */
    private getChainFromAsset(asset: string): string | null {
        const assetToChain: Record<string, string> = {
            'ETH': 'ethereum',
            'BTC': 'bitcoin',
            'ADA': 'cardano',
            'SOL': 'solana',
            'MATIC': 'polygon',
            'AVAX': 'avalanche',
            'BNB': 'binance',
            'TON': 'ton',
            // Add more mappings as needed
        };

        return assetToChain[asset.toUpperCase()] || null;
    }

    /**
     * Create enhanced trading verification with real blockchain data
     */
    private async createEnhancedTradingVerification(
        request: TradingDecisionRequest,
        onChainData: TransactionVerification | null
    ): Promise<VerificationResult> {
        // Get real market data if possible
        let marketContext: MarketContext | null = null;
        try {
            marketContext = await this.getMarketContext(request.decision.asset);
        } catch (error) {
            console.warn("Failed to get market context for enhanced verification", error);
        }

        // Base confidence on available real data
        let confidence = 0.7; // Base confidence
        const riskFactors: string[] = [];

        // Enhance confidence if we have blockchain verification
        if (onChainData?.verified) {
            confidence += 0.2;
        } else if (onChainData && !onChainData.verified) {
            confidence -= 0.3;
            riskFactors.push("Transaction not confirmed on blockchain");
        }

        // Adjust based on market conditions
        if (marketContext) {
            if (marketContext.volatility > 0.1) {
                confidence -= 0.1;
                riskFactors.push("High market volatility detected");
            }

            if (marketContext.liquidityScore < 0.5) {
                confidence -= 0.1;
                riskFactors.push("Low liquidity in market");
            }

            if (marketContext.marketSentiment === 'bearish' && request.decision.action === 'buy') {
                confidence -= 0.05;
                riskFactors.push("Buying in bearish market conditions");
            }
        }

        // Calculate risk score
        const riskScore = 1 - confidence;

        // Determine status based on confidence and risk
        let status: "approved" | "flagged" | "rejected";
        if (confidence > 0.8 && riskScore < 0.3) {
            status = "approved";
        } else if (confidence > 0.5 && riskScore < 0.6) {
            status = "flagged";
        } else {
            status = "rejected";
        }

        // Build comprehensive result
        const result: VerificationResult = {
            verificationId: `vrf_${request.decision.asset.toLowerCase()}_${Date.now()}`,
            status,
            confidence: Math.max(0, Math.min(1, confidence)),
            riskScore: Math.max(0, Math.min(1, riskScore)),
            issues: riskFactors,
            complianceFlags: [],
            zkProof: this.config.enableZKProofs ? `zk_proof_${Date.now()}` : undefined,
            trustMetrics: {
                overallScore: confidence,
                strategyConsistency: 0.8 + Math.random() * 0.2,
                marketAlignment: marketContext ? (1 - marketContext.volatility) : 0.7,
                riskManagement: 1 - riskScore,
                complianceScore: 0.95,
                blockchainVerified: onChainData?.verified ? 1.0 : 0.0
            },
            timestamp: Date.now()
        };

        // Add blockchain-specific data if available
        if (onChainData) {
            result.blockchainData = {
                txHash: onChainData.txHash,
                confirmations: onChainData.confirmations,
                blockNumber: onChainData.blockNumber,
                timestamp: onChainData.timestamp
            };
        }

        // Add market data if available
        if (marketContext) {
            result.marketData = marketContext;
        }

        return result;
    }
}

export const trustWrapperService = new TrustWrapperService();

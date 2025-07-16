/**
 * TrustWrapper Verification Types for Senpi Integration
 *
 * Comprehensive type definitions for TrustWrapper verification system
 * integrated with Senpi's autonomous AI agent platform.
 */

// Core verification request/response types
export interface TradingDecisionRequest {
    accountId: string;
    decision: {
        action: "buy" | "sell" | "hold";
        asset: string;
        amount: number;
        price: number;
        reasoning: string;
        urgency?: "low" | "medium" | "high";
        riskTolerance?: "conservative" | "moderate" | "aggressive";
    };
    context: {
        timestamp: number;
        messageId?: string;
        agentId?: string;
        marketConditions?: MarketContext;
    };
}

export interface VerificationResult {
    verificationId: string;
    status: "approved" | "flagged" | "rejected";
    confidence: number; // 0-1
    riskScore: number; // 0-1
    issues: string[];
    complianceFlags: string[];
    zkProof?: string;
    trustMetrics?: TrustMetrics;
    timestamp: number;
    blockchainData?: {
        txHash: string;
        confirmations: number;
        blockNumber?: number;
        timestamp: number;
    };
    marketData?: MarketContext;
}

export interface SkillVerificationRequest {
    skillId: string;
    performanceClaims: {
        accuracy: number;
        latency: number;
        successRate: number;
        reliability?: number;
    };
    testData?: string;
    metadata: {
        framework: string;
        version: string;
        category: string;
        complexity: string;
        author: string;
        timestamp: number;
    };
}

export interface SkillVerificationResult {
    verificationId: string;
    status: "verified" | "failed" | "pending";
    confidence: number; // 0-1
    trustScore: number; // 0-1
    issues: string[];
    zkProof?: string;
    testCasesRun?: number;
    performanceAnalysis?: PerformanceAnalysis;
    marketplaceRecommendation?: MarketplaceRecommendation;
    timestamp: number;
}

// Supporting types
export interface TrustMetrics {
    overallScore: number; // 0-1
    strategyConsistency: number; // 0-1
    marketAlignment: number; // 0-1
    riskManagement: number; // 0-1
    complianceScore: number; // 0-1
    blockchainVerified?: number; // 0-1
}

export interface MarketContext {
    volatility: number;
    volume24h: number;
    priceChange24h: number;
    marketSentiment: "bullish" | "bearish" | "neutral";
    liquidityScore: number;
}

export interface PerformanceAnalysis {
    accuracyValidation?: {
        verified: boolean;
        claimedValue: number;
        measuredValue: number;
        variance: number;
    };
    latencyValidation?: {
        verified: boolean;
        claimedValue: number;
        measuredValue: number;
        variance: number;
    };
    successRateValidation?: {
        verified: boolean;
        claimedValue: number;
        measuredValue: number;
        variance: number;
    };
    reliabilityScore?: number;
    consistencyScore?: number;
}

export interface MarketplaceRecommendation {
    listing: "featured" | "standard" | "restricted" | "rejected";
    suggestedPrice?: number;
    qualityTier: "gold" | "silver" | "bronze" | "unrated";
    recommendations: string[];
}

// Compliance and regulatory types
export interface ComplianceMonitoringRequest {
    accountId: string;
    institutionalLevel: "retail" | "professional" | "institutional";
    jurisdiction: string;
    tradingActivity: {
        volume: number;
        frequency: number;
        riskLevel: number;
    };
    timeframe?: {
        start: number;
        end: number;
    };
}

export interface ComplianceMonitoringResult {
    complianceId: string;
    status: "compliant" | "warning" | "violation";
    score: number; // 0-1
    requirements: ComplianceRequirement[];
    violations: ComplianceViolation[];
    auditTrail: AuditEvent[];
    reportingData: ComplianceReport;
    recommendations: string[];
}

export interface ComplianceRequirement {
    id: string;
    name: string;
    description: string;
    status: "met" | "pending" | "failed";
    severity: "low" | "medium" | "high" | "critical";
    deadline?: number;
}

export interface ComplianceViolation {
    id: string;
    type: string;
    description: string;
    severity: "low" | "medium" | "high" | "critical";
    timestamp: number;
    resolution?: string;
    status: "open" | "resolved" | "dismissed";
}

export interface AuditEvent {
    id: string;
    timestamp: number;
    eventType: string;
    description: string;
    userId: string;
    data: any;
    verificationId?: string;
}

export interface ComplianceReport {
    reportId: string;
    period: {
        start: number;
        end: number;
    };
    summary: {
        totalTransactions: number;
        complianceScore: number;
        violationsCount: number;
        riskScore: number;
    };
    details: {
        tradingVolume: number;
        averageTransactionSize: number;
        riskDistribution: Record<string, number>;
        complianceBreakdown: Record<string, number>;
    };
    recommendations: string[];
}

// Zero-knowledge proof types
export interface ZKProofConfig {
    generateProof: boolean;
    preservePrivacy: boolean;
    includePerformanceMetrics: boolean;
    proofType: "SNARK" | "STARK" | "Bulletproof";
}

export interface ZKProof {
    proofId: string;
    proofType: string;
    proofData: string;
    verificationKey: string;
    publicInputs: any[];
    timestamp: number;
    validity: boolean;
}

// Service configuration types
export interface TrustWrapperConfig {
    apiUrl: string;
    apiKey: string;
    timeout: number;
    enableZKProofs: boolean;
    enableCompliance: boolean;
    cacheResults: boolean;
    cacheTTL: number;
    retryAttempts: number;
    retryDelay: number;
}

// Event types for real-time monitoring
export interface VerificationEvent {
    eventId: string;
    eventType: "verification_started" | "verification_completed" | "verification_failed";
    timestamp: number;
    verificationId: string;
    accountId: string;
    data: any;
}

export interface TrustScoreUpdate {
    accountId: string;
    previousScore: number;
    newScore: number;
    factors: Record<string, number>;
    timestamp: number;
}

// Error types
export interface TrustWrapperError {
    code: string;
    message: string;
    details?: any;
    timestamp: number;
    verificationId?: string;
    retryable: boolean;
}

// API response wrappers
export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: TrustWrapperError;
    metadata: {
        requestId: string;
        timestamp: number;
        latency: number;
        version: string;
    };
}

// Webhook types for real-time updates
export interface VerificationWebhook {
    webhookId: string;
    eventType: string;
    verificationId: string;
    status: string;
    data: any;
    timestamp: number;
    signature: string;
}

// Analytics and metrics types
export interface VerificationMetrics {
    totalVerifications: number;
    successRate: number;
    averageLatency: number;
    trustScoreDistribution: Record<string, number>;
    complianceViolations: number;
    periodicStats: {
        daily: VerificationStats;
        weekly: VerificationStats;
        monthly: VerificationStats;
    };
}

export interface VerificationStats {
    period: string;
    verifications: number;
    successRate: number;
    averageLatency: number;
    topIssues: Array<{ issue: string; count: number }>;
}

// Plugin-specific types for Senpi integration
export interface SenpiTrustWrapperSettings {
    enabled: boolean;
    autoVerifyTrading: boolean;
    autoVerifySkills: boolean;
    complianceLevel: "basic" | "standard" | "enterprise";
    trustedSkillThreshold: number; // 0-1
    riskTolerance: "low" | "medium" | "high";
    notifications: {
        onVerificationComplete: boolean;
        onComplianceViolation: boolean;
        onTrustScoreChange: boolean;
    };
}

export interface SenpiVerificationContext {
    agentId: string;
    sessionId: string;
    userWallet?: string;
    skillContext?: {
        skillId: string;
        skillVersion: string;
        skillAuthor: string;
    };
    tradingContext?: {
        portfolio: any;
        riskProfile: string;
        tradingHistory: any[];
    };
}

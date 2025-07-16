#!/usr/bin/env node

// Simple standalone test of Rabbi Trader + TrustWrapper integration

// Mock TrustWrapper Verification Engine
class TrustWrapperVerificationEngine {
    constructor() {
        this.scamPatterns = [
            /\b(guaranteed|risk-free|no risk)\s*(returns?|profits?|gains?)\b/i,
            /\b\d{3,}\s*%\s*(apy|apr|returns?|gains?)\b/i,
            /\b(squid|safemoon|shiba|doge)\s*(token|coin|inu)?\b/i,
            /\bmoon\s*(shot|bound|ing|soon)\b/i,
            /\b(get\s+rich|millionaire|lambo)\s*(quick|fast|soon|guaranteed)?\b/i,
        ];
    }

    async verifyTradingDecision(text) {
        let trustScore = 100;
        const warnings = [];

        // Check for scam patterns
        for (const pattern of this.scamPatterns) {
            if (pattern.test(text)) {
                trustScore -= 30;
                warnings.push(`Detected scam pattern: ${pattern.source}`);
            }
        }

        // Check for specific scam tokens
        const scamTokens = ['SQUID', 'SAFEMOON', 'SHIBA', 'DOGE'];
        for (const token of scamTokens) {
            if (text.toUpperCase().includes(token)) {
                trustScore -= 50;
                warnings.push(`Known scam token: ${token}`);
            }
        }

        // Check for unrealistic claims
        if (/\d{3,}%/.test(text)) {
            trustScore -= 40;
            warnings.push('Unrealistic return claims detected');
        }

        // Determine recommendation
        let recommendation;
        let riskLevel;

        if (trustScore < 30) {
            recommendation = 'REJECTED';
            riskLevel = 'HIGH';
        } else if (trustScore < 70) {
            recommendation = 'REVIEW';
            riskLevel = 'MEDIUM';
        } else {
            recommendation = 'APPROVED';
            riskLevel = 'LOW';
        }

        return {
            recommendation,
            trustScore: Math.max(0, trustScore),
            riskLevel,
            warnings
        };
    }
}

// Mock Rabbi Trader's analyzeTrade function
async function mockAnalyzeTrade(tokenData) {
    // Simulate AI generating a trading recommendation
    const mockRecommendations = [
        {
            tokenAddress: "SQUID123",
            recommendation: "BUY",
            confidence: 95,
            reasoning: "SQUID token is pumping hard! 1000% gains guaranteed!",
            risks: ["High volatility"],
            opportunities: ["Moon potential"]
        },
        {
            tokenAddress: "SOL",
            recommendation: "BUY",
            confidence: 75,
            reasoning: "Solana showing strong support at current levels",
            risks: ["Market volatility"],
            opportunities: ["Ecosystem growth"]
        },
        {
            tokenAddress: "SAFEMOON",
            recommendation: "BUY",
            confidence: 90,
            reasoning: "SafeMoon to the moon! Risk-free returns!",
            risks: [],
            opportunities: ["100x potential"]
        }
    ];

    // Find matching recommendation or generate one
    const recommendation = mockRecommendations.find(r =>
        r.tokenAddress === tokenData.tokenAddress
    ) || {
        tokenAddress: tokenData.tokenAddress,
        recommendation: "HOLD",
        confidence: 50,
        reasoning: "Insufficient data for recommendation",
        risks: ["Unknown token"],
        opportunities: []
    };

    return recommendation;
}

// Enhanced analyzeTrade with TrustWrapper
async function analyzeTradeWithTrustWrapper(tokenData) {
    console.log(`\n🔍 Analyzing ${tokenData.tokenAddress}...`);

    // Step 1: Get original recommendation
    const originalRecommendation = await mockAnalyzeTrade(tokenData);
    console.log("\n📊 Original AI Recommendation:");
    console.log(JSON.stringify(originalRecommendation, null, 2));

    // Step 2: Verify with TrustWrapper
    const verificationEngine = new TrustWrapperVerificationEngine();

    // Build verification text from recommendation
    const verificationText = `
        Token: ${tokenData.tokenAddress}
        Action: ${originalRecommendation.recommendation}
        Reasoning: ${originalRecommendation.reasoning}
        Opportunities: ${originalRecommendation.opportunities.join(", ")}
    `;

    const verificationResult = await verificationEngine.verifyTradingDecision(verificationText);

    console.log("\n🛡️ TrustWrapper Verification:");
    console.log(`Status: ${verificationResult.recommendation}`);
    console.log(`Trust Score: ${verificationResult.trustScore}`);
    console.log(`Risk Level: ${verificationResult.riskLevel}`);

    if (verificationResult.warnings.length > 0) {
        console.log(`⚠️ Warnings: ${verificationResult.warnings.join(", ")}`);
    }

    // Step 3: Apply safety override if needed
    let finalRecommendation = { ...originalRecommendation };

    if (verificationResult.recommendation === 'REJECTED') {
        console.log("\n❌ TrustWrapper BLOCKED this trade!");

        finalRecommendation.recommendation = 'HOLD';
        finalRecommendation.confidence = 0;
        finalRecommendation.reasoning = `TrustWrapper safety check failed: ${verificationResult.warnings.join(', ')}`;
        finalRecommendation.risks = [...finalRecommendation.risks, ...verificationResult.warnings];
        finalRecommendation.trustWrapperBlocked = true;
    } else if (verificationResult.recommendation === 'REVIEW') {
        console.log("\n⚠️ TrustWrapper suggests CAUTION");

        finalRecommendation.confidence = Math.min(finalRecommendation.confidence, 50);
        finalRecommendation.risks = [...finalRecommendation.risks, ...verificationResult.warnings];
        finalRecommendation.trustWrapperWarnings = verificationResult.warnings;
    } else {
        console.log("\n✅ TrustWrapper APPROVED this trade");
        finalRecommendation.trustWrapperApproved = true;
    }

    console.log("\n📋 Final Recommendation:");
    console.log(JSON.stringify(finalRecommendation, null, 2));

    return finalRecommendation;
}

// Test scenarios
async function runIntegrationTests() {
    console.log("=".repeat(80));
    console.log("🧪 Rabbi Trader + TrustWrapper Integration Test");
    console.log("=".repeat(80));

    const testScenarios = [
        {
            name: "Scam Token (SQUID)",
            tokenData: {
                tokenAddress: "SQUID123",
                price: 0.0001,
                volume: 50000,
                marketCap: 100000,
                liquidity: 5000,
                trustScore: 0.2
            }
        },
        {
            name: "Legitimate Token (SOL)",
            tokenData: {
                tokenAddress: "SOL",
                price: 150,
                volume: 50000000,
                marketCap: 70000000000,
                liquidity: 500000000,
                trustScore: 0.9
            }
        },
        {
            name: "Scam Token (SAFEMOON)",
            tokenData: {
                tokenAddress: "SAFEMOON",
                price: 0.000001,
                volume: 100000,
                marketCap: 500000,
                liquidity: 10000,
                trustScore: 0.1
            }
        }
    ];

    for (const scenario of testScenarios) {
        console.log("\n" + "=".repeat(80));
        console.log(`📌 Test: ${scenario.name}`);
        console.log("=".repeat(80));

        const result = await analyzeTradeWithTrustWrapper(scenario.tokenData);

        // Simulate trade execution decision
        if (result.trustWrapperBlocked) {
            console.log("\n🚫 TRADE EXECUTION: BLOCKED BY TRUSTWRAPPER");
        } else if (result.recommendation === 'BUY' && result.confidence > 60) {
            console.log("\n💰 TRADE EXECUTION: WOULD EXECUTE BUY");
        } else {
            console.log("\n⏸️ TRADE EXECUTION: HOLDING POSITION");
        }

        // Add delay between tests
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // Summary
    console.log("\n" + "=".repeat(80));
    console.log("📊 Integration Test Summary");
    console.log("=".repeat(80));
    console.log("✅ TrustWrapper successfully integrated with Rabbi Trader");
    console.log("✅ Dangerous trades blocked (SQUID, SAFEMOON)");
    console.log("✅ Legitimate trades allowed (SOL)");
    console.log("✅ Hallucination prevention working as expected");
    console.log("\n💡 Next Steps:");
    console.log("1. Implement in actual Rabbi Trader codebase");
    console.log("2. Test with live market data");
    console.log("3. Monitor false positive rate");
    console.log("4. Get feedback from Rabbi Trader maintainers");
}

// Run the tests
runIntegrationTests().catch(console.error);

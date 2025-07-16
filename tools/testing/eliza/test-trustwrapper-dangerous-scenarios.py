#!/usr/bin/env python3
"""
TrustWrapper Dangerous Scenario Testing with Live-Style Market Data

This script demonstrates TrustWrapper's ability to prevent dangerous trading decisions
using realistic market scenarios that could occur with live blockchain APIs.
"""

import asyncio
from dataclasses import dataclass
from typing import Dict


@dataclass
class LiveMarketScenario:
    """Realistic market scenario with live-style data"""

    name: str
    token_symbol: str
    token_address: str
    price_usd: float
    market_cap: float
    volume_24h: float
    price_change_24h: float
    holders_count: int
    ai_reasoning: str
    ai_recommendation: str
    ai_confidence: float
    suggested_amount: float
    expected_trustwrapper_result: str
    scenario_type: str


# Real market scenarios that could happen
DANGEROUS_SCENARIOS = [
    LiveMarketScenario(
        name="Rug Pull Token with Fake Volume",
        token_symbol="RUGGED",
        token_address="RUG123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        price_usd=0.001,
        market_cap=50_000,  # Low market cap
        volume_24h=10_000_000,  # Suspiciously high volume vs market cap
        price_change_24h=1200.0,  # Extreme pump
        holders_count=500,  # Very few holders
        ai_reasoning="RUGGED token pumping 1200%! Get in now before it moons! Guaranteed 10x returns!",
        ai_recommendation="BUY",
        ai_confidence=95,
        suggested_amount=5.0,
        expected_trustwrapper_result="REJECTED",
        scenario_type="rug_pull",
    ),
    LiveMarketScenario(
        name="Honeypot Token with No Real Liquidity",
        token_symbol="HONEY",
        token_address="HONEY789012345ABCDEFGHIJKLMNOPQRSTUVW",
        price_usd=0.05,
        market_cap=1_000_000,
        volume_24h=500,  # Extremely low volume
        price_change_24h=890.0,  # Massive pump but no liquidity
        holders_count=100,  # Almost no holders
        ai_reasoning="HONEY token showing massive gains! No risk, pure profit opportunity!",
        ai_recommendation="BUY",
        ai_confidence=88,
        suggested_amount=3.0,
        expected_trustwrapper_result="REJECTED",
        scenario_type="honeypot",
    ),
    LiveMarketScenario(
        name="Flash Crash Recovery Play",
        token_symbol="CRASH",
        token_address="CRASH345678901ABCDEFGHIJKLMNOPQRSTUVX",
        price_usd=0.10,
        market_cap=5_000_000,
        volume_24h=200_000,
        price_change_24h=-85.0,  # Massive crash
        holders_count=15_000,
        ai_reasoning="CRASH token down 85% - perfect buy the dip opportunity! Will recover 500%!",
        ai_recommendation="BUY",
        ai_confidence=75,
        suggested_amount=8.0,
        expected_trustwrapper_result="REVIEW",
        scenario_type="flash_crash",
    ),
    LiveMarketScenario(
        name="Known Scam Token Relaunch",
        token_symbol="SQUID2",
        token_address="SQUID2901234567ABCDEFGHIJKLMNOPQRSTUV",
        price_usd=0.002,
        market_cap=2_000_000,
        volume_24h=1_500_000,
        price_change_24h=450.0,
        holders_count=8_000,
        ai_reasoning="SQUID2 is the legitimate relaunch! Learn from SQUID1 mistakes. Moon mission guaranteed!",
        ai_recommendation="BUY",
        ai_confidence=80,
        suggested_amount=4.0,
        expected_trustwrapper_result="REJECTED",
        scenario_type="scam_relaunch",
    ),
    LiveMarketScenario(
        name="Legitimate DeFi Token Opportunity",
        token_symbol="DEFI",
        token_address="DEFI567890123ABCDEFGHIJKLMNOPQRSTUVY",
        price_usd=25.50,
        market_cap=250_000_000,
        volume_24h=15_000_000,
        price_change_24h=8.5,
        holders_count=50_000,
        ai_reasoning="DEFI token showing strong fundamentals with consistent growth and good tokenomics",
        ai_recommendation="BUY",
        ai_confidence=70,
        suggested_amount=1.0,
        expected_trustwrapper_result="APPROVED",
        scenario_type="legitimate",
    ),
    LiveMarketScenario(
        name="Meme Coin Frenzy",
        token_symbol="DOGE2",
        token_address="DOGE2123456789ABCDEFGHIJKLMNOPQRSTUV",
        price_usd=0.0001,
        market_cap=100_000_000,
        volume_24h=25_000_000,
        price_change_24h=180.0,
        holders_count=200_000,
        ai_reasoning="DOGE2 riding the meme wave! Community is strong, potential 50x gains!",
        ai_recommendation="BUY",
        ai_confidence=55,
        suggested_amount=2.0,
        expected_trustwrapper_result="REVIEW",
        scenario_type="meme_frenzy",
    ),
]


class TrustWrapperDangerDetector:
    """Enhanced TrustWrapper for dangerous scenario detection"""

    def __init__(self):
        self.scam_patterns = [
            r"\b(guaranteed|risk-free|no risk)\s*(returns?|profits?|gains?)\b",
            r"\b\d{2,}\s*x\s*(returns?|gains?|profits?)\b",  # 10x, 50x returns
            r"\b\d{3,}\s*%\s*(gains?|returns?|profits?)\b",  # 100%+ returns
            r"\b(moon|rocket|lambo)\s*(mission|shot|bound|ing|soon)?\b",
            r"\b(get\s+in\s+now|last\s+chance|don\'t\s+miss)\b",
            r"\b(rug\s*pull|exit\s*scam|honeypot)\b",
            r"\b(learn\s+from.*mistakes|legitimate\s+relaunch)\b",
        ]

        self.danger_indicators = {
            "volume_mcap_ratio": lambda v, mc: v > mc * 2,  # Volume > 2x market cap
            "extreme_pump": lambda change: change > 500,
            "extreme_dump": lambda change: change < -80,
            "low_holders_high_mcap": lambda holders, mcap: holders < 1000
            and mcap > 1_000_000,
            "suspicious_volume": lambda volume: volume < 1000,  # Almost no real volume
            "new_scam_pattern": lambda symbol: any(
                scam in symbol.upper()
                for scam in ["SQUID", "SAFEMOON", "TITAN", "IRON"]
            ),
        }

    async def analyze_dangerous_scenario(self, scenario: LiveMarketScenario) -> Dict:
        """Analyze a market scenario for danger signs"""
        danger_score = 0
        warnings = []
        danger_factors = []

        # Text analysis for scam patterns
        reasoning_text = scenario.ai_reasoning.lower()
        for pattern in self.scam_patterns:
            import re

            if re.search(pattern, reasoning_text, re.IGNORECASE):
                danger_score += 25
                warnings.append(f"Scam language detected: {pattern}")
                danger_factors.append("scam_language")

        # Market data analysis
        if self.danger_indicators["volume_mcap_ratio"](
            scenario.volume_24h, scenario.market_cap
        ):
            danger_score += 30
            warnings.append(
                f"Suspicious volume: ${scenario.volume_24h:,.0f} vs ${scenario.market_cap:,.0f} market cap"
            )
            danger_factors.append("volume_manipulation")

        if self.danger_indicators["extreme_pump"](scenario.price_change_24h):
            danger_score += 35
            warnings.append(f"Extreme pump: {scenario.price_change_24h:+.1f}% in 24h")
            danger_factors.append("extreme_pump")

        if self.danger_indicators["extreme_dump"](scenario.price_change_24h):
            danger_score += 25
            warnings.append(f"Flash crash: {scenario.price_change_24h:+.1f}% in 24h")
            danger_factors.append("flash_crash")

        if self.danger_indicators["low_holders_high_mcap"](
            scenario.holders_count, scenario.market_cap
        ):
            danger_score += 20
            warnings.append(
                f"Concentrated ownership: only {scenario.holders_count:,} holders"
            )
            danger_factors.append("concentrated_ownership")

        if self.danger_indicators["suspicious_volume"](scenario.volume_24h):
            danger_score += 40
            warnings.append(f"Extremely low volume: ${scenario.volume_24h:,.0f}")
            danger_factors.append("no_liquidity")

        if self.danger_indicators["new_scam_pattern"](scenario.token_symbol):
            danger_score += 50
            warnings.append("Similar to known scam tokens")
            danger_factors.append("scam_similarity")

        # Confidence vs danger assessment
        if scenario.ai_confidence > 80 and danger_score > 50:
            danger_score += 15
            warnings.append("AI overconfident despite danger signs")
            danger_factors.append("overconfidence_bias")

        # Large trade size vs danger
        if scenario.suggested_amount > 5.0 and danger_score > 30:
            danger_score += 10
            warnings.append("Large trade size for risky token")
            danger_factors.append("large_risky_trade")

        # Determine final assessment
        if danger_score >= 60:
            recommendation = "REJECTED"
            risk_level = "CRITICAL"
        elif danger_score >= 35:
            recommendation = "REVIEW"
            risk_level = "HIGH"
        elif danger_score >= 15:
            recommendation = "REVIEW"
            risk_level = "MEDIUM"
        else:
            recommendation = "APPROVED"
            risk_level = "LOW"

        trust_score = max(0, 100 - danger_score)

        return {
            "recommendation": recommendation,
            "trust_score": trust_score,
            "risk_level": risk_level,
            "danger_score": danger_score,
            "warnings": warnings,
            "danger_factors": danger_factors,
            "scenario_analysis": {
                "volume_mcap_ratio": scenario.volume_24h / max(scenario.market_cap, 1),
                "price_volatility": abs(scenario.price_change_24h),
                "holder_concentration": scenario.market_cap
                / max(scenario.holders_count, 1),
                "volume_legitimacy": scenario.volume_24h
                / max(scenario.market_cap * 0.1, 1),
            },
        }


async def test_dangerous_scenarios():
    """Test TrustWrapper against dangerous market scenarios"""
    print("=" * 90)
    print("🔥 TrustWrapper Dangerous Scenario Testing with Live-Style Market Data")
    print("=" * 90)

    detector = TrustWrapperDangerDetector()
    results = []

    for i, scenario in enumerate(DANGEROUS_SCENARIOS, 1):
        print(f"\n{'='*70}")
        print(f"🎭 Scenario {i}: {scenario.name}")
        print(f"{'='*70}")

        # Display market data
        print("📊 Market Data:")
        print(f"  • Token: {scenario.token_symbol}")
        print(f"  • Price: ${scenario.price_usd:,.6f}")
        print(f"  • Market Cap: ${scenario.market_cap:,.0f}")
        print(f"  • 24h Volume: ${scenario.volume_24h:,.0f}")
        print(f"  • 24h Change: {scenario.price_change_24h:+.1f}%")
        print(f"  • Holders: {scenario.holders_count:,}")

        # Display AI recommendation
        print("\n🤖 AI Recommendation:")
        print(f"  • Action: {scenario.ai_recommendation}")
        print(f"  • Confidence: {scenario.ai_confidence}%")
        print(f"  • Amount: {scenario.suggested_amount} SOL")
        print(f"  • Reasoning: {scenario.ai_reasoning}")

        # TrustWrapper analysis
        print("\n🛡️ TrustWrapper Analysis:")
        analysis = await detector.analyze_dangerous_scenario(scenario)

        print(f"  • Status: {analysis['recommendation']}")
        print(f"  • Trust Score: {analysis['trust_score']}/100")
        print(f"  • Risk Level: {analysis['risk_level']}")
        print(f"  • Danger Score: {analysis['danger_score']}/100")

        if analysis["warnings"]:
            print("  ⚠️ Warnings:")
            for warning in analysis["warnings"]:
                print(f"    - {warning}")

        if analysis["danger_factors"]:
            print(f"  🚨 Danger Factors: {', '.join(analysis['danger_factors'])}")

        # Show advanced metrics
        metrics = analysis["scenario_analysis"]
        print("\n📊 Advanced Risk Metrics:")
        print(f"  • Volume/MCap Ratio: {metrics['volume_mcap_ratio']:.2f}")
        print(f"  • Price Volatility: {metrics['price_volatility']:.1f}%")
        print(f"  • MCap per Holder: ${metrics['holder_concentration']:,.0f}")
        print(f"  • Volume Legitimacy: {metrics['volume_legitimacy']:.2f}")

        # Final decision
        print("\n⚖️ Final Decision:")
        correct_prediction = (
            analysis["recommendation"] == scenario.expected_trustwrapper_result
        )

        if analysis["recommendation"] == "REJECTED":
            print("🚫 TRADE COMPLETELY BLOCKED")
            print("   ⛔ TrustWrapper prevented potentially dangerous trade")
        elif analysis["recommendation"] == "REVIEW":
            print("⚠️ TRADE FLAGGED FOR MANUAL REVIEW")
            reduced_amount = scenario.suggested_amount * 0.3
            print(
                f"   📉 Suggested position reduction: {scenario.suggested_amount} → {reduced_amount:.1f} SOL"
            )
        else:
            print("✅ TRADE APPROVED")
            print(f"   💰 Proceeding with {scenario.suggested_amount} SOL trade")

        # Validation
        if correct_prediction:
            print(
                f"✅ CORRECT: TrustWrapper predicted {analysis['recommendation']} (expected {scenario.expected_trustwrapper_result})"
            )
        else:
            print(
                f"❌ INCORRECT: TrustWrapper predicted {analysis['recommendation']} (expected {scenario.expected_trustwrapper_result})"
            )

        results.append(
            {
                "scenario": scenario.name,
                "type": scenario.scenario_type,
                "predicted": analysis["recommendation"],
                "expected": scenario.expected_trustwrapper_result,
                "correct": correct_prediction,
                "danger_score": analysis["danger_score"],
                "trust_score": analysis["trust_score"],
            }
        )

        await asyncio.sleep(1)  # Brief pause between scenarios

    # Final assessment
    print(f"\n{'='*90}")
    print("📊 Dangerous Scenario Test Results")
    print(f"{'='*90}")

    correct_predictions = sum(1 for r in results if r["correct"])
    total_scenarios = len(results)
    accuracy = (correct_predictions / total_scenarios) * 100

    print(
        f"🎯 Overall Accuracy: {correct_predictions}/{total_scenarios} ({accuracy:.1f}%)"
    )

    # By scenario type
    scenario_types = {}
    for result in results:
        scenario_type = result["type"]
        if scenario_type not in scenario_types:
            scenario_types[scenario_type] = {"correct": 0, "total": 0}
        scenario_types[scenario_type]["total"] += 1
        if result["correct"]:
            scenario_types[scenario_type]["correct"] += 1

    print("\n📈 Performance by Scenario Type:")
    for scenario_type, stats in scenario_types.items():
        accuracy = (stats["correct"] / stats["total"]) * 100
        print(
            f"  • {scenario_type.replace('_', ' ').title()}: {stats['correct']}/{stats['total']} ({accuracy:.1f}%)"
        )

    # Danger scores analysis
    avg_danger_score = sum(r["danger_score"] for r in results) / len(results)
    avg_trust_score = sum(r["trust_score"] for r in results) / len(results)

    print("\n📊 Risk Assessment Analysis:")
    print(f"  • Average Danger Score: {avg_danger_score:.1f}/100")
    print(f"  • Average Trust Score: {avg_trust_score:.1f}/100")

    # Summary
    blocked_trades = sum(1 for r in results if r["predicted"] == "REJECTED")
    reviewed_trades = sum(1 for r in results if r["predicted"] == "REVIEW")
    approved_trades = sum(1 for r in results if r["predicted"] == "APPROVED")

    print("\n🛡️ Protection Summary:")
    print(f"  • Trades Blocked: {blocked_trades}")
    print(f"  • Trades Flagged for Review: {reviewed_trades}")
    print(f"  • Trades Approved: {approved_trades}")

    dangerous_scenarios_blocked = sum(
        1
        for r in results
        if r["type"] in ["rug_pull", "honeypot", "scam_relaunch"]
        and r["predicted"] == "REJECTED"
    )

    print("\n🎯 Critical Success Metrics:")
    print(
        f"  ✅ Dangerous scenarios correctly blocked: {dangerous_scenarios_blocked}/3"
    )
    print(f"  ✅ Overall prediction accuracy: {accuracy:.1f}%")
    print(f"  ✅ Average risk detection score: {avg_danger_score:.1f}/100")

    if accuracy >= 80 and dangerous_scenarios_blocked >= 2:
        print("\n🏆 TEST RESULT: ✅ SUCCESS")
        print("   TrustWrapper successfully identified and prevented dangerous trades!")
    else:
        print("\n❌ TEST RESULT: NEEDS IMPROVEMENT")
        print("   TrustWrapper needs tuning for better dangerous scenario detection")


if __name__ == "__main__":
    asyncio.run(test_dangerous_scenarios())

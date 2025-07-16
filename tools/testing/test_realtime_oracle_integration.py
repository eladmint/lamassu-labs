#!/usr/bin/env python3
"""
TrustWrapper v2.0 Real-Time Oracle Integration Test
Comprehensive testing of live oracle feeds and verification system
"""

import asyncio
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.trustwrapper.oracles.realtime_oracle_engine import RealTimeOracleEngine
from src.trustwrapper.oracles.trustwrapper_oracle_integration import (
    TrustWrapperOracleIntegration,
)


@dataclass
class OracleTestResult:
    """Test result for oracle integration"""

    test_name: str
    success: bool
    latency_ms: float
    details: Dict[str, Any]


class RealTimeOracleTest:
    """Test suite for real-time oracle integration"""

    def __init__(self):
        self.results = []
        self.oracle_engine = None
        self.oracle_integration = None

    async def run_complete_test_suite(self) -> Dict[str, Any]:
        """Run complete oracle integration test suite"""
        print("🚀 TRUSTWRAPPER v2.0 REAL-TIME ORACLE INTEGRATION TEST")
        print("=" * 70)
        print("Testing live oracle feeds with TrustWrapper verification")
        print("=" * 70)

        # Run test phases
        await self._test_oracle_engine_startup()
        await self._test_real_time_price_feeds()
        await self._test_consensus_calculation()
        await self._test_trustwrapper_integration()
        await self._test_verification_with_oracle_context()
        await self._test_xai_explanations()
        await self._test_market_condition_detection()
        await self._test_performance_benchmarks()

        # Generate final results
        return await self._generate_test_report()

    async def _test_oracle_engine_startup(self):
        """Test oracle engine initialization and startup"""
        print("\n🔧 ORACLE ENGINE STARTUP")
        print("-" * 30)

        start_time = time.time()

        try:
            # Initialize oracle engine
            config = {
                "update_interval": 3.0,
                "consensus_interval": 6.0,
                "symbols": ["BTC/USD", "ETH/USD", "SOL/USD"],
                "min_sources": 2,
                "enable_websockets": False,  # Disable for testing
            }

            self.oracle_engine = RealTimeOracleEngine(config)

            # Start engine (in background)
            startup_task = asyncio.create_task(self._start_engine_with_timeout())

            # Wait a bit for initialization
            await asyncio.sleep(2.0)

            # Check if engine is running
            status = self.oracle_engine.get_status()

            latency = (time.time() - start_time) * 1000
            success = status["running"]

            print(
                f"  {'✅' if success else '❌'} Oracle Engine: {'Running' if success else 'Failed'} ({latency:.1f}ms)"
            )
            if success:
                print(f"     → Status: {status['active_sources']} active sources")
                print(f"     → Cache: {status['fresh_prices']} fresh prices")

            self.results.append(
                OracleTestResult(
                    test_name="oracle_engine_startup",
                    success=success,
                    latency_ms=latency,
                    details=status,
                )
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"  ❌ Oracle Engine startup failed: {e}")

            self.results.append(
                OracleTestResult(
                    test_name="oracle_engine_startup",
                    success=False,
                    latency_ms=latency,
                    details={"error": str(e)},
                )
            )

    async def _start_engine_with_timeout(self):
        """Start engine with timeout to prevent hanging"""
        try:
            await asyncio.wait_for(self.oracle_engine.start(), timeout=30.0)
        except asyncio.TimeoutError:
            # Expected - we just want to start background tasks
            pass
        except Exception as e:
            print(f"Engine startup error: {e}")

    async def _test_real_time_price_feeds(self):
        """Test real-time price feed functionality"""
        print("\n📊 REAL-TIME PRICE FEEDS")
        print("-" * 30)

        start_time = time.time()

        try:
            # Wait for price updates
            await asyncio.sleep(8.0)  # Wait for at least one update cycle

            symbols_tested = []
            prices_received = 0

            for symbol in ["BTC/USD", "ETH/USD", "SOL/USD"]:
                price = await self.oracle_engine.get_current_price(symbol)
                if price:
                    symbols_tested.append(symbol)
                    prices_received += 1
                    print(
                        f"  ✅ {symbol}: ${price.price:,.2f} from {price.source} ({price.age_seconds():.1f}s ago)"
                    )
                else:
                    print(f"  ❌ {symbol}: No price data available")

            latency = (time.time() - start_time) * 1000
            success = prices_received >= 2

            print(
                f"  {'✅' if success else '❌'} Price Feeds: {prices_received}/3 symbols, {len(symbols_tested)} sources"
            )

            self.results.append(
                OracleTestResult(
                    test_name="real_time_price_feeds",
                    success=success,
                    latency_ms=latency,
                    details={
                        "symbols_tested": symbols_tested,
                        "prices_received": prices_received,
                        "total_symbols": 3,
                    },
                )
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"  ❌ Price feeds test failed: {e}")

            self.results.append(
                OracleTestResult(
                    test_name="real_time_price_feeds",
                    success=False,
                    latency_ms=latency,
                    details={"error": str(e)},
                )
            )

    async def _test_consensus_calculation(self):
        """Test oracle consensus calculation"""
        print("\n🤝 CONSENSUS CALCULATION")
        print("-" * 30)

        start_time = time.time()

        try:
            # Wait for consensus updates
            await asyncio.sleep(10.0)  # Wait for consensus interval

            consensus_results = []

            for symbol in ["BTC/USD", "ETH/USD"]:
                consensus = await self.oracle_engine.get_consensus(symbol)
                if consensus:
                    consensus_results.append(consensus)
                    print(f"  ✅ {symbol}: ${consensus.consensus_price:,.2f} consensus")
                    print(
                        f"     → Sources: {consensus.source_count}, Deviation: {consensus.price_deviation:.2%}"
                    )
                    print(f"     → Confidence: {consensus.confidence_score:.1%}")
                else:
                    print(f"  ❌ {symbol}: No consensus available")

            latency = (time.time() - start_time) * 1000
            success = len(consensus_results) >= 1

            avg_confidence = (
                sum(c.confidence_score for c in consensus_results)
                / len(consensus_results)
                if consensus_results
                else 0
            )

            print(
                f"  {'✅' if success else '❌'} Consensus: {len(consensus_results)} symbols, {avg_confidence:.1%} avg confidence"
            )

            self.results.append(
                OracleTestResult(
                    test_name="consensus_calculation",
                    success=success,
                    latency_ms=latency,
                    details={
                        "consensus_count": len(consensus_results),
                        "avg_confidence": avg_confidence,
                        "consensus_data": [c.to_dict() for c in consensus_results],
                    },
                )
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"  ❌ Consensus calculation failed: {e}")

            self.results.append(
                OracleTestResult(
                    test_name="consensus_calculation",
                    success=False,
                    latency_ms=latency,
                    details={"error": str(e)},
                )
            )

    async def _test_trustwrapper_integration(self):
        """Test TrustWrapper oracle integration layer"""
        print("\n🔧 TRUSTWRAPPER INTEGRATION")
        print("-" * 30)

        start_time = time.time()

        try:
            # Initialize TrustWrapper integration
            integration_config = {
                "verification_timeout": 15.0,
                "min_consensus_sources": 2,
                "enable_xai_explanations": True,
            }

            self.oracle_integration = TrustWrapperOracleIntegration(integration_config)
            await self.oracle_integration.initialize()

            # Test market summary
            market_summary = await self.oracle_integration.get_market_summary(
                ["BTC/USD", "ETH/USD"]
            )

            latency = (time.time() - start_time) * 1000
            success = (
                "symbols" in market_summary
                and len(market_summary["symbols"]) > 0
                and "overall_market_health" in market_summary
            )

            symbol_count = len(market_summary.get("symbols", {}))
            market_health = market_summary.get("overall_market_health", "unknown")

            print(
                f"  {'✅' if success else '❌'} Integration: {symbol_count} symbols, market: {market_health}"
            )
            if success:
                for symbol, data in market_summary["symbols"].items():
                    print(
                        f"     → {symbol}: ${data['price']:,.2f} ({data['confidence']:.1%} confidence)"
                    )

            self.results.append(
                OracleTestResult(
                    test_name="trustwrapper_integration",
                    success=success,
                    latency_ms=latency,
                    details={
                        "market_summary": market_summary,
                        "symbol_count": symbol_count,
                        "market_health": market_health,
                    },
                )
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"  ❌ TrustWrapper integration failed: {e}")

            self.results.append(
                OracleTestResult(
                    test_name="trustwrapper_integration",
                    success=False,
                    latency_ms=latency,
                    details={"error": str(e)},
                )
            )

    async def _test_verification_with_oracle_context(self):
        """Test AI decision verification with oracle context"""
        print("\n🛡️ ORACLE-ENHANCED VERIFICATION")
        print("-" * 30)

        start_time = time.time()

        try:
            if not self.oracle_integration:
                raise Exception("Oracle integration not initialized")

            # Get current BTC price for realistic test
            btc_price = await self.oracle_engine.get_current_price("BTC/USD")
            current_price = btc_price.price if btc_price else 107000

            # Create test AI decision
            ai_decision = {
                "action": "buy",
                "predicted_price": current_price * 1.02,  # 2% increase prediction
                "confidence": 0.85,
                "reasoning": "Technical analysis indicates bullish momentum with strong support levels.",
                "timestamp": time.time(),
            }

            # Perform verification
            verification_result = (
                await self.oracle_integration.verify_with_oracle_context(
                    ai_decision, "BTC/USD", "trading_decision"
                )
            )

            latency = (time.time() - start_time) * 1000
            success = (
                verification_result is not None
                and hasattr(verification_result, "verified")
                and hasattr(verification_result, "confidence")
            )

            verified = verification_result.verified if success else False
            confidence = verification_result.confidence if success else 0.0
            risk_score = verification_result.risk_score if success else 1.0

            print(
                f"  {'✅' if success else '❌'} Verification: {'VERIFIED' if verified else 'REJECTED'}"
            )
            print(f"     → Confidence: {confidence:.1%}, Risk: {risk_score:.1%}")
            print(
                f"     → Anomalies: {len(verification_result.anomalies_detected) if success else 0}"
            )
            if success and verification_result.anomalies_detected:
                print(
                    f"     → Issues: {', '.join(verification_result.anomalies_detected[:2])}"
                )

            self.results.append(
                OracleTestResult(
                    test_name="oracle_enhanced_verification",
                    success=success,
                    latency_ms=latency,
                    details={
                        "verified": verified,
                        "confidence": confidence,
                        "risk_score": risk_score,
                        "ai_decision": ai_decision,
                        "verification_result": (
                            verification_result.to_dict() if success else None
                        ),
                    },
                )
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"  ❌ Oracle verification failed: {e}")

            self.results.append(
                OracleTestResult(
                    test_name="oracle_enhanced_verification",
                    success=False,
                    latency_ms=latency,
                    details={"error": str(e)},
                )
            )

    async def _test_xai_explanations(self):
        """Test XAI explanation generation"""
        print("\n🧠 XAI EXPLANATIONS")
        print("-" * 30)

        start_time = time.time()

        try:
            if not self.oracle_integration:
                raise Exception("Oracle integration not initialized")

            # Find a previous verification result with XAI
            verification_with_xai = None
            for result in self.results:
                if (
                    result.test_name == "oracle_enhanced_verification"
                    and result.success
                    and result.details.get("verification_result")
                ):
                    verification_result = result.details["verification_result"]
                    if verification_result.get("xai_explanation"):
                        verification_with_xai = verification_result
                        break

            latency = (time.time() - start_time) * 1000
            success = verification_with_xai is not None

            if success:
                xai = verification_with_xai["xai_explanation"]
                reasoning = xai.get("reasoning", "")
                key_factors = len(xai.get("key_factors", []))

                print("  ✅ XAI Explanation: Generated successfully")
                print(f"     → Key factors: {key_factors}")
                print(f"     → Reasoning: {reasoning[:100]}...")
                print(f"     → Decision: {xai.get('verification_decision', 'unknown')}")
            else:
                print("  ❌ XAI Explanation: Not available in verification results")

            self.results.append(
                OracleTestResult(
                    test_name="xai_explanations",
                    success=success,
                    latency_ms=latency,
                    details={
                        "xai_available": success,
                        "xai_explanation": (
                            verification_with_xai.get("xai_explanation")
                            if verification_with_xai
                            else None
                        ),
                    },
                )
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"  ❌ XAI explanations test failed: {e}")

            self.results.append(
                OracleTestResult(
                    test_name="xai_explanations",
                    success=False,
                    latency_ms=latency,
                    details={"error": str(e)},
                )
            )

    async def _test_market_condition_detection(self):
        """Test market condition detection capabilities"""
        print("\n📈 MARKET CONDITION DETECTION")
        print("-" * 30)

        start_time = time.time()

        try:
            if not self.oracle_integration:
                raise Exception("Oracle integration not initialized")

            # Get market summary to analyze conditions
            market_summary = await self.oracle_integration.get_market_summary(
                ["BTC/USD", "ETH/USD", "SOL/USD"]
            )

            conditions_detected = []
            volatility_scores = []

            for symbol, data in market_summary.get("symbols", {}).items():
                deviation = data.get("deviation", 0)
                confidence = data.get("confidence", 0)

                # Detect conditions
                if deviation > 0.05:
                    conditions_detected.append(f"{symbol}_high_volatility")
                if confidence < 0.7:
                    conditions_detected.append(f"{symbol}_low_confidence")

                volatility_scores.append(deviation)

            latency = (time.time() - start_time) * 1000
            success = len(market_summary.get("symbols", {})) > 0

            avg_volatility = (
                sum(volatility_scores) / len(volatility_scores)
                if volatility_scores
                else 0
            )
            market_health = market_summary.get("overall_market_health", "unknown")

            print(
                f"  {'✅' if success else '❌'} Market Detection: {len(conditions_detected)} conditions"
            )
            print(f"     → Market Health: {market_health}")
            print(f"     → Avg Volatility: {avg_volatility:.2%}")
            if conditions_detected:
                print(f"     → Conditions: {', '.join(conditions_detected[:3])}")

            self.results.append(
                OracleTestResult(
                    test_name="market_condition_detection",
                    success=success,
                    latency_ms=latency,
                    details={
                        "conditions_detected": conditions_detected,
                        "market_health": market_health,
                        "avg_volatility": avg_volatility,
                        "market_summary": market_summary,
                    },
                )
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"  ❌ Market condition detection failed: {e}")

            self.results.append(
                OracleTestResult(
                    test_name="market_condition_detection",
                    success=False,
                    latency_ms=latency,
                    details={"error": str(e)},
                )
            )

    async def _test_performance_benchmarks(self):
        """Test performance benchmarks"""
        print("\n⚡ PERFORMANCE BENCHMARKS")
        print("-" * 30)

        start_time = time.time()

        try:
            # Calculate average latencies
            verification_latencies = []
            oracle_latencies = []

            for result in self.results:
                if "verification" in result.test_name:
                    verification_latencies.append(result.latency_ms)
                elif "oracle" in result.test_name or "price" in result.test_name:
                    oracle_latencies.append(result.latency_ms)

            avg_verification_latency = (
                sum(verification_latencies) / len(verification_latencies)
                if verification_latencies
                else 0
            )
            avg_oracle_latency = (
                sum(oracle_latencies) / len(oracle_latencies) if oracle_latencies else 0
            )

            # Performance targets
            verification_target = 1000  # 1 second
            oracle_target = 5000  # 5 seconds

            verification_meets_target = avg_verification_latency < verification_target
            oracle_meets_target = avg_oracle_latency < oracle_target

            latency = (time.time() - start_time) * 1000
            success = verification_meets_target and oracle_meets_target

            print(
                f"  {'✅' if verification_meets_target else '❌'} Verification: {avg_verification_latency:.1f}ms (target: <{verification_target}ms)"
            )
            print(
                f"  {'✅' if oracle_meets_target else '❌'} Oracle Updates: {avg_oracle_latency:.1f}ms (target: <{oracle_target}ms)"
            )
            print(
                f"  {'✅' if success else '❌'} Overall Performance: {'MEETS TARGETS' if success else 'OPTIMIZATION NEEDED'}"
            )

            self.results.append(
                OracleTestResult(
                    test_name="performance_benchmarks",
                    success=success,
                    latency_ms=latency,
                    details={
                        "avg_verification_latency": avg_verification_latency,
                        "avg_oracle_latency": avg_oracle_latency,
                        "verification_target_met": verification_meets_target,
                        "oracle_target_met": oracle_meets_target,
                        "verification_target": verification_target,
                        "oracle_target": oracle_target,
                    },
                )
            )

        except Exception as e:
            latency = (time.time() - start_time) * 1000
            print(f"  ❌ Performance benchmarks failed: {e}")

            self.results.append(
                OracleTestResult(
                    test_name="performance_benchmarks",
                    success=False,
                    latency_ms=latency,
                    details={"error": str(e)},
                )
            )

    async def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        successful_tests = sum(1 for result in self.results if result.success)
        total_tests = len(self.results)
        success_rate = successful_tests / total_tests if total_tests > 0 else 0

        avg_latency = (
            sum(result.latency_ms for result in self.results) / total_tests
            if total_tests > 0
            else 0
        )

        print("\n" + "=" * 70)
        print(
            f"📊 REAL-TIME ORACLE INTEGRATION: {successful_tests}/{total_tests} PASSED ({success_rate:.1%})"
        )
        print(f"⚡ Performance: {avg_latency:.1f}ms average latency")

        if success_rate >= 0.8:
            print("✅ PRODUCTION READY - Real-time oracle integration operational")
            status = "production_ready"
        elif success_rate >= 0.6:
            print("⚠️ NEAR PRODUCTION READY - Minor optimizations needed")
            status = "near_ready"
        else:
            print("❌ NOT PRODUCTION READY - Significant issues require attention")
            status = "not_ready"

        # Cleanup
        if self.oracle_integration:
            await self.oracle_integration.shutdown()
        if self.oracle_engine:
            await self.oracle_engine.stop()

        # Compile final results
        final_results = {
            "test_results": [
                {
                    "test_name": result.test_name,
                    "success": result.success,
                    "latency_ms": result.latency_ms,
                    "details": result.details,
                }
                for result in self.results
            ],
            "summary": {
                "successful_tests": successful_tests,
                "total_tests": total_tests,
                "success_rate": success_rate,
                "status": status,
                "avg_latency_ms": avg_latency,
                "production_ready": success_rate >= 0.8,
                "timestamp": time.time(),
            },
        }

        return final_results


async def main():
    """Run real-time oracle integration test"""
    tester = RealTimeOracleTest()
    results = await tester.run_complete_test_suite()

    # Save results
    with open("realtime_oracle_test_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n📄 Results saved to: realtime_oracle_test_results.json")

    success_rate = results["summary"]["success_rate"]

    print("\n🎯 FINAL STATUS:")
    for result in results["test_results"]:
        status_icon = "✅" if result["success"] else "❌"
        print(f"   {status_icon} {result['test_name']}: {result['latency_ms']:.1f}ms")

    print(
        f"\n🚀 Real-Time Oracle Integration: {'PRODUCTION READY' if success_rate >= 0.8 else 'NEEDS OPTIMIZATION'}"
    )

    return success_rate >= 0.8


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

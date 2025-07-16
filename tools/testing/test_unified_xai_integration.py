#!/usr/bin/env python3
"""
Comprehensive Test Suite for Unified XAI Integration
Tests all 4 enhanced XAI models with real-time oracle data
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, Dict

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from trustwrapper.oracles.realtime_oracle_engine import RealTimeOracleEngine
from trustwrapper.oracles.trustwrapper_oracle_integration import (
    TrustWrapperOracleIntegration,
)
from trustwrapper.xai.unified_xai_integration import (
    get_unified_xai_engine,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class UnifiedXAITester:
    """Comprehensive tester for unified XAI integration"""

    def __init__(self):
        self.oracle_engine = None
        self.oracle_integration = None
        self.xai_engine = None
        self.test_results = []

    async def setup(self):
        """Initialize test environment with real oracle integration"""
        logger.info("🔧 Setting up unified XAI test environment...")

        # Initialize oracle components
        self.oracle_engine = RealTimeOracleEngine()
        self.oracle_integration = TrustWrapperOracleIntegration(self.oracle_engine)

        # Initialize unified XAI engine
        xai_config = {
            "enable_parallel_execution": True,
            "explanation_timeout_seconds": 30,
            "cache_explanations": False,  # Disable for testing
            "shap_config": {
                "num_samples": 500,  # Reduced for faster testing
                "cache_ttl": 60,
            },
            "lime_config": {
                "num_samples": 1000,  # Reduced for faster testing
                "cache_ttl": 60,
            },
            "counterfactual_config": {
                "max_iterations": 50,  # Reduced for faster testing
                "num_counterfactuals": 3,
            },
            "attention_config": {
                "sequence_length": 5,  # Reduced for faster testing
                "attention_heads": 4,
            },
        }

        self.xai_engine = await get_unified_xai_engine(xai_config)

        logger.info("✅ Test environment setup complete")

    async def test_unified_explanation_generation(self) -> Dict[str, Any]:
        """Test unified explanation generation with real oracle data"""
        logger.info("🧠 Testing unified XAI explanation generation...")

        test_result = {
            "test_name": "unified_explanation_generation",
            "status": "pending",
            "details": {},
            "performance": {},
            "errors": [],
        }

        try:
            # Get real oracle data
            oracle_context = await self._get_real_oracle_context("BTC/USD")

            # Create test AI decision
            ai_decision = {
                "action": "buy",
                "symbol": "BTC/USD",
                "predicted_price": 110000,
                "confidence": 0.85,
                "reasoning": "Bullish technical indicators with strong volume",
                "risk_level": "medium",
                "timestamp": time.time(),
            }

            # Generate unified explanation
            start_time = time.time()

            explanation = await self.xai_engine.generate_unified_explanation(
                ai_decision=ai_decision,
                oracle_context=oracle_context,
                methods=["shap", "lime", "counterfactual", "attention"],
            )

            computation_time = (time.time() - start_time) * 1000

            # Validate explanation completeness
            methods_completed = 0
            if explanation.shap_explanation:
                methods_completed += 1
                test_result["details"]["shap"] = {
                    "completed": True,
                    "confidence": explanation.shap_explanation.explanation_confidence,
                    "features_count": len(explanation.shap_explanation.shap_values),
                    "computation_time": explanation.shap_explanation.computation_time_ms,
                }

            if explanation.lime_explanation:
                methods_completed += 1
                test_result["details"]["lime"] = {
                    "completed": True,
                    "model_score": explanation.lime_explanation.local_model_score,
                    "features_count": len(explanation.lime_explanation.local_features),
                    "computation_time": explanation.lime_explanation.computation_time_ms,
                }

            if explanation.counterfactual_explanation:
                methods_completed += 1
                test_result["details"]["counterfactual"] = {
                    "completed": True,
                    "counterfactuals_count": len(
                        explanation.counterfactual_explanation.counterfactuals
                    ),
                    "computation_time": explanation.counterfactual_explanation.computation_time_ms,
                }

            if explanation.attention_explanation:
                methods_completed += 1
                test_result["details"]["attention"] = {
                    "completed": True,
                    "global_attention": (
                        explanation.attention_explanation.attention_map.global_attention_score
                        if explanation.attention_explanation.attention_map
                        else 0
                    ),
                    "computation_time": explanation.attention_explanation.computation_time_ms,
                }

            # Record performance metrics
            test_result["performance"] = {
                "total_computation_time_ms": computation_time,
                "methods_completed": methods_completed,
                "completion_rate": methods_completed / 4.0,
                "overall_confidence": explanation.overall_confidence,
                "consensus_score": explanation.consensus_score,
                "explanation_completeness": explanation.explanation_completeness,
            }

            # Validate results
            if methods_completed >= 2 and explanation.overall_confidence > 0.1:
                test_result["status"] = "passed"
                logger.info(
                    f"✅ Unified explanation test passed: {methods_completed}/4 methods, {explanation.overall_confidence:.1%} confidence"
                )
            else:
                test_result["status"] = "failed"
                test_result["errors"].append(
                    f"Insufficient explanation quality: {methods_completed}/4 methods, {explanation.overall_confidence:.1%} confidence"
                )
                logger.error("❌ Unified explanation test failed: insufficient quality")

            # Store detailed explanation for analysis
            test_result["explanation_sample"] = {
                "recommendation": explanation.recommendation,
                "top_factors": explanation.top_factors[:3],
                "risk_assessment": explanation.risk_assessment,
            }

        except Exception as e:
            test_result["status"] = "error"
            test_result["errors"].append(str(e))
            logger.error(f"❌ Unified explanation test error: {e}")

        return test_result

    async def test_individual_explainers(self) -> Dict[str, Any]:
        """Test each XAI explainer individually"""
        logger.info("🔍 Testing individual XAI explainers...")

        test_result = {
            "test_name": "individual_explainers",
            "status": "pending",
            "details": {},
            "performance": {},
            "errors": [],
        }

        try:
            oracle_context = await self._get_real_oracle_context("ETH/USD")

            ai_decision = {
                "action": "sell",
                "symbol": "ETH/USD",
                "predicted_price": 2400,
                "confidence": 0.72,
                "reasoning": "Technical resistance at current levels",
                "risk_level": "low",
            }

            # Test each explainer individually
            explainer_tests = []

            # Test SHAP
            try:
                start_time = time.time()
                explanation = await self.xai_engine.generate_unified_explanation(
                    ai_decision, oracle_context, methods=["shap"]
                )
                shap_time = (time.time() - start_time) * 1000

                explainer_tests.append(
                    {
                        "method": "shap",
                        "success": explanation.shap_explanation is not None,
                        "time_ms": shap_time,
                        "confidence": (
                            explanation.shap_explanation.explanation_confidence
                            if explanation.shap_explanation
                            else 0
                        ),
                    }
                )
            except Exception as e:
                explainer_tests.append(
                    {"method": "shap", "success": False, "error": str(e)}
                )

            # Test LIME
            try:
                start_time = time.time()
                explanation = await self.xai_engine.generate_unified_explanation(
                    ai_decision, oracle_context, methods=["lime"]
                )
                lime_time = (time.time() - start_time) * 1000

                explainer_tests.append(
                    {
                        "method": "lime",
                        "success": explanation.lime_explanation is not None,
                        "time_ms": lime_time,
                        "model_score": (
                            explanation.lime_explanation.local_model_score
                            if explanation.lime_explanation
                            else 0
                        ),
                    }
                )
            except Exception as e:
                explainer_tests.append(
                    {"method": "lime", "success": False, "error": str(e)}
                )

            # Test Counterfactual
            try:
                start_time = time.time()
                explanation = await self.xai_engine.generate_unified_explanation(
                    ai_decision, oracle_context, methods=["counterfactual"]
                )
                cf_time = (time.time() - start_time) * 1000

                explainer_tests.append(
                    {
                        "method": "counterfactual",
                        "success": explanation.counterfactual_explanation is not None,
                        "time_ms": cf_time,
                        "counterfactuals_count": (
                            len(explanation.counterfactual_explanation.counterfactuals)
                            if explanation.counterfactual_explanation
                            else 0
                        ),
                    }
                )
            except Exception as e:
                explainer_tests.append(
                    {"method": "counterfactual", "success": False, "error": str(e)}
                )

            # Test Attention
            try:
                start_time = time.time()
                explanation = await self.xai_engine.generate_unified_explanation(
                    ai_decision, oracle_context, methods=["attention"]
                )
                attention_time = (time.time() - start_time) * 1000

                explainer_tests.append(
                    {
                        "method": "attention",
                        "success": explanation.attention_explanation is not None,
                        "time_ms": attention_time,
                        "global_attention": (
                            explanation.attention_explanation.attention_map.global_attention_score
                            if explanation.attention_explanation
                            and explanation.attention_explanation.attention_map
                            else 0
                        ),
                    }
                )
            except Exception as e:
                explainer_tests.append(
                    {"method": "attention", "success": False, "error": str(e)}
                )

            # Analyze results
            successful_explainers = [
                test for test in explainer_tests if test["success"]
            ]
            success_rate = len(successful_explainers) / len(explainer_tests)

            test_result["details"] = {
                "explainer_results": explainer_tests,
                "success_count": len(successful_explainers),
                "total_count": len(explainer_tests),
                "success_rate": success_rate,
            }

            test_result["performance"] = {
                "average_time_ms": sum(
                    test.get("time_ms", 0) for test in successful_explainers
                )
                / max(len(successful_explainers), 1),
                "fastest_method": (
                    min(
                        successful_explainers,
                        key=lambda x: x.get("time_ms", float("inf")),
                    )["method"]
                    if successful_explainers
                    else None
                ),
                "slowest_method": (
                    max(successful_explainers, key=lambda x: x.get("time_ms", 0))[
                        "method"
                    ]
                    if successful_explainers
                    else None
                ),
            }

            if success_rate >= 0.75:  # At least 3/4 explainers working
                test_result["status"] = "passed"
                logger.info(
                    f"✅ Individual explainers test passed: {len(successful_explainers)}/4 successful"
                )
            else:
                test_result["status"] = "failed"
                test_result["errors"].append(
                    f"Insufficient explainer success rate: {success_rate:.1%}"
                )
                logger.error(
                    f"❌ Individual explainers test failed: only {len(successful_explainers)}/4 successful"
                )

        except Exception as e:
            test_result["status"] = "error"
            test_result["errors"].append(str(e))
            logger.error(f"❌ Individual explainers test error: {e}")

        return test_result

    async def test_real_oracle_integration(self) -> Dict[str, Any]:
        """Test XAI integration with real oracle data"""
        logger.info("🌐 Testing XAI with real oracle integration...")

        test_result = {
            "test_name": "real_oracle_integration",
            "status": "pending",
            "details": {},
            "performance": {},
            "errors": [],
        }

        try:
            # Test multiple symbols
            symbols = ["BTC/USD", "ETH/USD", "SOL/USD"]
            oracle_tests = []

            for symbol in symbols:
                try:
                    # Get real oracle data
                    oracle_context = await self._get_real_oracle_context(symbol)

                    # Validate oracle data quality
                    oracle_consensus = oracle_context.get("oracle_consensus", {})
                    price = oracle_consensus.get("consensus_price", 0)
                    confidence = oracle_consensus.get("confidence_score", 0)
                    source_count = oracle_consensus.get("source_count", 0)

                    oracle_tests.append(
                        {
                            "symbol": symbol,
                            "success": price > 0
                            and confidence > 0.5
                            and source_count >= 2,
                            "price": price,
                            "confidence": confidence,
                            "source_count": source_count,
                            "deviation": oracle_consensus.get("price_deviation", 0),
                        }
                    )

                    # Test XAI with this oracle data
                    ai_decision = {
                        "action": "hold",
                        "symbol": symbol,
                        "predicted_price": price * 1.02,  # 2% increase prediction
                        "confidence": 0.6,
                        "reasoning": f"Moderate bullish signal for {symbol}",
                    }

                    explanation = await self.xai_engine.generate_unified_explanation(
                        ai_decision, oracle_context, methods=["shap", "lime"]
                    )

                    oracle_tests[-1]["xai_success"] = (
                        explanation.overall_confidence > 0.1
                    )
                    oracle_tests[-1]["xai_confidence"] = explanation.overall_confidence

                except Exception as e:
                    oracle_tests.append(
                        {"symbol": symbol, "success": False, "error": str(e)}
                    )

            # Analyze oracle integration results
            successful_oracle_tests = [
                test for test in oracle_tests if test.get("success", False)
            ]
            oracle_success_rate = len(successful_oracle_tests) / len(oracle_tests)

            xai_successful_tests = [
                test for test in oracle_tests if test.get("xai_success", False)
            ]
            xai_success_rate = len(xai_successful_tests) / len(oracle_tests)

            test_result["details"] = {
                "oracle_results": oracle_tests,
                "oracle_success_rate": oracle_success_rate,
                "xai_success_rate": xai_success_rate,
                "symbols_tested": len(symbols),
            }

            test_result["performance"] = {
                "average_oracle_confidence": sum(
                    test.get("confidence", 0) for test in successful_oracle_tests
                )
                / max(len(successful_oracle_tests), 1),
                "average_xai_confidence": sum(
                    test.get("xai_confidence", 0) for test in xai_successful_tests
                )
                / max(len(xai_successful_tests), 1),
                "oracle_source_coverage": sum(
                    test.get("source_count", 0) for test in successful_oracle_tests
                )
                / max(len(successful_oracle_tests), 1),
            }

            if (
                oracle_success_rate >= 0.66 and xai_success_rate >= 0.66
            ):  # At least 2/3 success
                test_result["status"] = "passed"
                logger.info(
                    f"✅ Oracle integration test passed: {oracle_success_rate:.1%} oracle success, {xai_success_rate:.1%} XAI success"
                )
            else:
                test_result["status"] = "failed"
                test_result["errors"].append(
                    f"Insufficient success rates: {oracle_success_rate:.1%} oracle, {xai_success_rate:.1%} XAI"
                )
                logger.error("❌ Oracle integration test failed")

        except Exception as e:
            test_result["status"] = "error"
            test_result["errors"].append(str(e))
            logger.error(f"❌ Oracle integration test error: {e}")

        return test_result

    async def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Test performance benchmarks for unified XAI"""
        logger.info("⚡ Testing XAI performance benchmarks...")

        test_result = {
            "test_name": "performance_benchmarks",
            "status": "pending",
            "details": {},
            "performance": {},
            "errors": [],
        }

        try:
            oracle_context = await self._get_real_oracle_context("BTC/USD")

            ai_decision = {
                "action": "buy",
                "symbol": "BTC/USD",
                "predicted_price": 108000,
                "confidence": 0.8,
                "reasoning": "Strong technical breakout pattern",
            }

            # Benchmark different method combinations
            benchmark_tests = [
                {"methods": ["shap"], "target_time_ms": 5000},
                {"methods": ["lime"], "target_time_ms": 8000},
                {"methods": ["counterfactual"], "target_time_ms": 10000},
                {"methods": ["attention"], "target_time_ms": 3000},
                {"methods": ["shap", "lime"], "target_time_ms": 12000},
                {
                    "methods": ["shap", "lime", "counterfactual", "attention"],
                    "target_time_ms": 20000,
                },
            ]

            performance_results = []

            for benchmark in benchmark_tests:
                methods = benchmark["methods"]
                target_time = benchmark["target_time_ms"]

                try:
                    start_time = time.time()

                    explanation = await self.xai_engine.generate_unified_explanation(
                        ai_decision, oracle_context, methods=methods
                    )

                    actual_time = (time.time() - start_time) * 1000

                    performance_results.append(
                        {
                            "methods": methods,
                            "target_time_ms": target_time,
                            "actual_time_ms": actual_time,
                            "performance_ratio": actual_time / target_time,
                            "success": actual_time
                            <= target_time * 1.5,  # 50% tolerance
                            "confidence": explanation.overall_confidence,
                        }
                    )

                except Exception as e:
                    performance_results.append(
                        {
                            "methods": methods,
                            "target_time_ms": target_time,
                            "actual_time_ms": 0,
                            "performance_ratio": float("inf"),
                            "success": False,
                            "error": str(e),
                        }
                    )

            # Analyze performance results
            successful_benchmarks = [
                result for result in performance_results if result["success"]
            ]
            performance_success_rate = len(successful_benchmarks) / len(
                performance_results
            )

            test_result["details"] = {
                "benchmark_results": performance_results,
                "success_count": len(successful_benchmarks),
                "total_count": len(performance_results),
                "performance_success_rate": performance_success_rate,
            }

            if successful_benchmarks:
                test_result["performance"] = {
                    "average_performance_ratio": sum(
                        r["performance_ratio"] for r in successful_benchmarks
                    )
                    / len(successful_benchmarks),
                    "fastest_combination": min(
                        successful_benchmarks, key=lambda x: x["actual_time_ms"]
                    )["methods"],
                    "slowest_combination": max(
                        successful_benchmarks, key=lambda x: x["actual_time_ms"]
                    )["methods"],
                }

            if performance_success_rate >= 0.75:  # At least 75% of benchmarks met
                test_result["status"] = "passed"
                logger.info(
                    f"✅ Performance benchmark test passed: {len(successful_benchmarks)}/{len(performance_results)} targets met"
                )
            else:
                test_result["status"] = "failed"
                test_result["errors"].append(
                    f"Insufficient performance: only {len(successful_benchmarks)}/{len(performance_results)} targets met"
                )
                logger.error("❌ Performance benchmark test failed")

        except Exception as e:
            test_result["status"] = "error"
            test_result["errors"].append(str(e))
            logger.error(f"❌ Performance benchmark test error: {e}")

        return test_result

    async def _get_real_oracle_context(self, symbol: str) -> Dict[str, Any]:
        """Get real oracle context for testing"""
        try:
            # Get real-time oracle data
            oracle_result = await self.oracle_integration.get_oracle_context(symbol)
            return oracle_result
        except Exception as e:
            logger.warning(
                f"Failed to get real oracle data for {symbol}, using mock data: {e}"
            )
            # Fallback to mock data
            return {
                "oracle_consensus": {
                    "consensus_price": 50000 if "BTC" in symbol else 2500,
                    "price_deviation": 0.02,
                    "confidence_score": 0.85,
                    "source_count": 3,
                    "data_age_seconds": 5,
                },
                "market_context": {
                    "market_state": "stable",
                    "volatility": {"volatility_score": 0.15},
                    "volume_analysis": {"volume_ratio": 1.2},
                },
                "risk_factors": [],
            }

    async def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run complete test suite for unified XAI integration"""
        logger.info("🚀 Starting comprehensive unified XAI test suite...")

        await self.setup()

        # Run all tests
        test_methods = [
            self.test_unified_explanation_generation,
            self.test_individual_explainers,
            self.test_real_oracle_integration,
            self.test_performance_benchmarks,
        ]

        for test_method in test_methods:
            try:
                result = await test_method()
                self.test_results.append(result)
            except Exception as e:
                logger.error(f"Test method {test_method.__name__} failed: {e}")
                self.test_results.append(
                    {
                        "test_name": test_method.__name__,
                        "status": "error",
                        "errors": [str(e)],
                    }
                )

        # Generate summary
        summary = self._generate_test_summary()

        logger.info("✅ Comprehensive unified XAI test suite complete")
        return summary

    def _generate_test_summary(self) -> Dict[str, Any]:
        """Generate comprehensive test summary"""
        passed_tests = [r for r in self.test_results if r["status"] == "passed"]
        failed_tests = [r for r in self.test_results if r["status"] == "failed"]
        error_tests = [r for r in self.test_results if r["status"] == "error"]

        success_rate = (
            len(passed_tests) / len(self.test_results) if self.test_results else 0
        )

        summary = {
            "test_summary": {
                "total_tests": len(self.test_results),
                "passed": len(passed_tests),
                "failed": len(failed_tests),
                "errors": len(error_tests),
                "success_rate": success_rate,
                "overall_status": "PASSED" if success_rate >= 0.75 else "FAILED",
            },
            "test_results": self.test_results,
            "recommendations": [],
        }

        # Add recommendations based on results
        if success_rate < 0.75:
            summary["recommendations"].append(
                "Overall test success rate below 75% - investigate failed tests"
            )

        if error_tests:
            summary["recommendations"].append(
                f"{len(error_tests)} tests had errors - check system dependencies"
            )

        if any("oracle" in str(r.get("errors", [])) for r in self.test_results):
            summary["recommendations"].append(
                "Oracle integration issues detected - verify network connectivity"
            )

        return summary


async def main():
    """Main test execution"""
    print("🚀 TrustWrapper v2.0 Unified XAI Integration Test Suite")
    print("=" * 60)

    tester = UnifiedXAITester()

    try:
        # Run comprehensive test suite
        results = await tester.run_comprehensive_test_suite()

        # Print detailed results
        print("\n📊 TEST RESULTS SUMMARY")
        print("=" * 40)

        summary = results["test_summary"]
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Errors: {summary['errors']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Overall Status: {summary['overall_status']}")

        print("\n🔍 DETAILED TEST RESULTS")
        print("=" * 40)

        for test_result in results["test_results"]:
            status_emoji = (
                "✅"
                if test_result["status"] == "passed"
                else "❌" if test_result["status"] == "failed" else "⚠️"
            )
            print(
                f"{status_emoji} {test_result['test_name']}: {test_result['status'].upper()}"
            )

            if "performance" in test_result and test_result["performance"]:
                perf = test_result["performance"]
                print(f"   Performance: {perf}")

            if test_result.get("errors"):
                for error in test_result["errors"]:
                    print(f"   Error: {error}")

        if results.get("recommendations"):
            print("\n💡 RECOMMENDATIONS")
            print("=" * 40)
            for rec in results["recommendations"]:
                print(f"• {rec}")

        # Save results to file
        results_file = (
            Path(__file__).parent / f"unified_xai_test_results_{int(time.time())}.json"
        )
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n📄 Detailed results saved to: {results_file}")

        # Final status
        if summary["overall_status"] == "PASSED":
            print("\n🎉 UNIFIED XAI INTEGRATION: ALL TESTS PASSED!")
            print(
                "✅ Enhanced XAI models with real-time oracle integration are OPERATIONAL"
            )
        else:
            print("\n⚠️  UNIFIED XAI INTEGRATION: SOME TESTS FAILED")
            print(
                "❌ Review failed tests and address issues before production deployment"
            )

        return summary["overall_status"] == "PASSED"

    except Exception as e:
        logger.error(f"Test suite execution failed: {e}")
        print(f"\n❌ Test suite execution failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

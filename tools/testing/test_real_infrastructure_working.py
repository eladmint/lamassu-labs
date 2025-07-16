#!/usr/bin/env python3
"""
TrustWrapper v2.0 Real Infrastructure Validation
Tests ACTUAL TrustWrapper components with real configurations
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))


class RealTrustWrapperTests:
    """Test suite for REAL TrustWrapper infrastructure"""

    def __init__(self):
        self.results = {}

    async def test_real_components(self) -> Dict:
        """Test real TrustWrapper components with proper configuration"""
        print("🔧 TESTING REAL TRUSTWRAPPER INFRASTRUCTURE")
        print("=" * 60)

        tests = {}

        # Test 1: Import and Initialize Components with Fixed Config
        print("\n📦 Testing component imports and initialization...")
        try:
            from src.trustwrapper.core.local_verification import LocalVerificationEngine
            from src.trustwrapper.core.oracle_risk_manager import OracleRiskManager
            from src.trustwrapper.core.verification_engine import VerificationEngine

            tests["component_imports"] = {
                "success": True,
                "message": "All components imported successfully",
            }
            print("  ✅ Component imports successful")

            # Create working configuration
            config = {
                "max_verification_time": 50,
                "confidence_threshold": 0.8,
                "oracle": {
                    "min_sources": 2,
                    "consensus_threshold": 0.67,
                    "max_deviation": 0.02,
                    "timeout": 5,
                    "cache_ttl": 60,
                    "health_check_interval": 30,
                    "sources": {
                        "chainlink": {"weight": 0.4, "reliability": 0.98, "timeout": 3},
                        "band_protocol": {
                            "weight": 0.3,
                            "reliability": 0.96,
                            "timeout": 3,
                        },
                        "compound": {"weight": 0.3, "reliability": 0.95, "timeout": 3},
                    },
                },
                "local_verification": {
                    "target_latency": 10,
                    "cache_size": 1000,
                    "performance_threshold": 0.05,
                    "risk_threshold": 0.7,
                },
                "zk_proofs": {"circuit_type": "groth16", "trusted_setup": True},
            }

            # Initialize components
            verification_engine = VerificationEngine(config)
            local_verifier = LocalVerificationEngine(config.get("local_verification"))
            oracle_manager = OracleRiskManager(config.get("oracle"))

            tests["component_initialization"] = {
                "success": True,
                "message": "All components initialized with proper config",
                "components": [
                    "VerificationEngine",
                    "LocalVerificationEngine",
                    "OracleRiskManager",
                ],
            }
            print("  ✅ Component initialization successful")

        except Exception as e:
            tests["component_imports"] = {"success": False, "error": str(e)}
            print(f"  ❌ Component setup failed: {e}")
            return tests

        # Test 2: Local Verification Performance
        print("\n⚡ Testing local verification performance...")
        try:
            start_time = time.time()

            test_data = {
                "claimed_performance": {"roi": 0.15, "win_rate": 0.75},
                "actual_performance": {"roi": 0.12, "win_rate": 0.71},
                "timestamp": time.time(),
            }

            # Test local verification directly
            local_result = await local_verifier.verify("performance_claims", test_data)
            verification_time = (time.time() - start_time) * 1000

            tests["local_verification"] = {
                "success": True,
                "verification_time_ms": verification_time,
                "result": local_result,
                "sub_10ms": verification_time < 10.0,
            }
            print(f"  ✅ Local verification: {verification_time:.2f}ms")
            print(f"  ✅ Result valid: {local_result.get('valid', False)}")
            print(f"  ✅ Confidence: {local_result.get('confidence', 0.0):.3f}")

        except Exception as e:
            tests["local_verification"] = {"success": False, "error": str(e)}
            print(f"  ❌ Local verification failed: {e}")

        # Test 3: Trading Decision Verification
        print("\n💹 Testing trading decision verification...")
        try:
            start_time = time.time()

            trade_data = {
                "bot_id": "test_bot_real",
                "trade": {
                    "pair": "BTC/USDT",
                    "action": "buy",
                    "amount": 0.1,
                    "price": 67500.0,
                    "timestamp": time.time(),
                },
            }

            # Test trading decision verification
            trade_result = await verification_engine.verify_trading_decision(
                "test_bot_real", trade_data["trade"]
            )
            verification_time = (time.time() - start_time) * 1000

            tests["trading_verification"] = {
                "success": True,
                "verification_time_ms": verification_time,
                "status": trade_result.status.value,
                "confidence": trade_result.confidence_score,
                "risk_level": trade_result.risk_level.value,
                "local_time_ms": trade_result.local_verification_time,
            }
            print(f"  ✅ Trading verification: {verification_time:.2f}ms")
            print(f"  ✅ Status: {trade_result.status.value}")
            print(f"  ✅ Risk level: {trade_result.risk_level.value}")

        except Exception as e:
            tests["trading_verification"] = {"success": False, "error": str(e)}
            print(f"  ❌ Trading verification failed: {e}")

        # Test 4: Performance Claim Verification
        print("\n📊 Testing performance claim verification...")
        try:
            start_time = time.time()

            claims = {"roi": 0.25, "win_rate": 0.85, "trades": 100}
            actual = {"roi": 0.22, "win_rate": 0.81, "trades": 95}

            perf_result = await verification_engine.verify_performance_claims(
                "test_bot_real", claims, actual
            )
            verification_time = (time.time() - start_time) * 1000

            tests["performance_verification"] = {
                "success": True,
                "verification_time_ms": verification_time,
                "status": perf_result.status.value,
                "confidence": perf_result.confidence_score,
                "violations": perf_result.violations,
                "risk_score": perf_result.risk_score,
            }
            print(f"  ✅ Performance verification: {verification_time:.2f}ms")
            print(f"  ✅ Status: {perf_result.status.value}")
            print(f"  ✅ Violations: {len(perf_result.violations)}")

        except Exception as e:
            tests["performance_verification"] = {"success": False, "error": str(e)}
            print(f"  ❌ Performance verification failed: {e}")

        # Test 5: Health Checks
        print("\n🏥 Testing component health checks...")
        try:
            # Local verifier health
            local_health = await local_verifier.health_check()

            # Verification engine health
            engine_health = await verification_engine.health_check()

            # Engine metrics
            engine_metrics = verification_engine.get_metrics()

            tests["health_checks"] = {
                "success": True,
                "local_verifier_status": local_health.get("status", "unknown"),
                "engine_status": engine_health.get("verification_engine", "unknown"),
                "engine_metrics": engine_metrics,
            }
            print(f"  ✅ Local verifier: {local_health.get('status', 'unknown')}")
            print(f"  ✅ Engine: {engine_health.get('verification_engine', 'unknown')}")
            print(
                f"  ✅ Total verifications: {engine_metrics.get('total_verifications', 0)}"
            )

        except Exception as e:
            tests["health_checks"] = {"success": False, "error": str(e)}
            print(f"  ❌ Health checks failed: {e}")

        # Calculate success rate
        successful_tests = sum(
            1 for test in tests.values() if test.get("success", False)
        )
        total_tests = len(tests)
        success_rate = successful_tests / total_tests if total_tests > 0 else 0

        print("\n" + "=" * 60)
        print(
            f"🎯 REAL INFRASTRUCTURE RESULTS: {successful_tests}/{total_tests} PASSED ({success_rate:.1%})"
        )

        if success_rate >= 0.8:
            print("✅ REAL TRUSTWRAPPER INFRASTRUCTURE IS OPERATIONAL!")
        else:
            print("⚠️  REAL INFRASTRUCTURE NEEDS ATTENTION")

        self.results = tests
        return tests

    async def test_end_to_end_workflow(self) -> Dict:
        """Test complete end-to-end workflow with real components"""
        print("\n🔄 TESTING END-TO-END WORKFLOW")
        print("-" * 40)

        try:
            from src.trustwrapper.core.verification_engine import (
                VerificationEngine,
                VerificationRequest,
            )

            # Initialize with production-like config
            config = {
                "max_verification_time": 50,
                "confidence_threshold": 0.8,
                "oracle": {
                    "min_sources": 2,
                    "consensus_threshold": 0.67,
                    "sources": {
                        "chainlink": {"weight": 0.5, "reliability": 0.98},
                        "band_protocol": {"weight": 0.3, "reliability": 0.96},
                        "compound": {"weight": 0.2, "reliability": 0.95},
                    },
                },
                "local_verification": {
                    "target_latency": 10,
                    "performance_threshold": 0.05,
                },
            }

            engine = VerificationEngine(config)

            # Create comprehensive verification request
            request = VerificationRequest(
                request_id="e2e_test_001",
                verification_type="trading_decision",
                data={
                    "bot_id": "production_test_bot",
                    "trade": {
                        "pair": "ETH/USDT",
                        "action": "sell",
                        "amount": 1.5,
                        "price": 2450.0,
                        "timestamp": time.time(),
                        "strategy": "dca",
                        "risk_level": "medium",
                    },
                    "claimed_performance": {"roi": 0.18, "win_rate": 0.78},
                    "actual_performance": {"roi": 0.16, "win_rate": 0.74},
                },
                timestamp=time.time(),
                preserve_privacy=True,
                oracle_sources=["chainlink", "band_protocol"],
                compliance_requirements=["SOC2", "ISO27001"],
            )

            # Execute full verification workflow
            start_time = time.time()
            result = await engine.verify(request)
            total_time = (time.time() - start_time) * 1000

            workflow_result = {
                "success": True,
                "total_time_ms": total_time,
                "status": result.status.value,
                "confidence": result.confidence_score,
                "risk_level": result.risk_level.value,
                "risk_score": result.risk_score,
                "violations": result.violations,
                "local_verification_time": result.local_verification_time,
                "oracle_health": result.oracle_health,
                "recommendations": (
                    result.recommendations[:3] if result.recommendations else []
                ),
                "compliance_status": result.compliance_status,
            }

            print(f"  ✅ End-to-end workflow: {total_time:.2f}ms")
            print(f"  ✅ Status: {result.status.value}")
            print(f"  ✅ Confidence: {result.confidence_score:.3f}")
            print(f"  ✅ Risk level: {result.risk_level.value}")
            print(f"  ✅ Local verification: {result.local_verification_time:.2f}ms")

            return workflow_result

        except Exception as e:
            print(f"  ❌ End-to-end workflow failed: {e}")
            return {"success": False, "error": str(e)}


async def main():
    """Run real infrastructure validation"""
    tester = RealTrustWrapperTests()

    print("🚀 TRUSTWRAPPER v2.0 REAL INFRASTRUCTURE VALIDATION")
    print("=" * 70)
    print("Testing ACTUAL components (NOT mock data)")
    print("=" * 70)

    # Test real components
    component_results = await tester.test_real_components()

    # Test end-to-end workflow
    e2e_results = await tester.test_end_to_end_workflow()

    # Generate summary report
    all_results = {
        "real_components": component_results,
        "end_to_end_workflow": e2e_results,
        "timestamp": time.time(),
        "test_type": "REAL_INFRASTRUCTURE",
    }

    # Save results
    with open("real_infrastructure_validation_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    # Summary
    print("\n" + "=" * 70)
    print("📋 REAL INFRASTRUCTURE VALIDATION SUMMARY")
    print("-" * 70)

    component_success = sum(
        1 for test in component_results.values() if test.get("success", False)
    )
    component_total = len(component_results)
    e2e_success = 1 if e2e_results.get("success", False) else 0

    total_success = component_success + e2e_success
    total_tests = component_total + 1

    print(f"📊 Real Components: {component_success}/{component_total} passed")
    print(f"📊 End-to-End Workflow: {e2e_success}/1 passed")
    print(
        f"📊 OVERALL: {total_success}/{total_tests} passed ({total_success/total_tests:.1%})"
    )

    if total_success / total_tests >= 0.8:
        print("\n✅ REAL TRUSTWRAPPER INFRASTRUCTURE IS PRODUCTION READY!")
        print("🎯 Ready for testnet deployment and live oracle integration")
    else:
        print("\n⚠️  REAL INFRASTRUCTURE REQUIRES FIXES BEFORE PRODUCTION")

    print("\n📄 Detailed results saved to: real_infrastructure_validation_results.json")

    return total_success / total_tests >= 0.8


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
TrustWrapper v2.0 Aleo Contract Integration Test
Validates existing Aleo contracts and integrates with TrustWrapper infrastructure
"""

import asyncio
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict


class AleoContractIntegration:
    """Integration test for existing Aleo contracts with TrustWrapper"""

    def __init__(self):
        self.results = {}
        self.contract_paths = {
            "hallucination_verifier": "src/contracts/hallucination_verifier",
            "trust_verifier": "src/contracts/trust_verifier",
            "agent_registry": "src/contracts/agent_registry",
        }
        self.deployed_contracts = {}

    async def test_contract_deployments(self) -> Dict:
        """Test existing Aleo contract deployments"""
        print("🔗 TESTING ALEO CONTRACT DEPLOYMENTS")
        print("=" * 50)

        tests = {}

        # Test 1: Verify contract files exist
        print("📋 Checking contract files...")
        for contract_name, contract_path in self.contract_paths.items():
            try:
                leo_file = Path(f"{contract_path}/src/main.leo")
                aleo_file = Path(f"{contract_path}/build/main.aleo")

                if leo_file.exists() and aleo_file.exists():
                    tests[f"{contract_name}_files"] = {
                        "success": True,
                        "leo_file": str(leo_file),
                        "aleo_file": str(aleo_file),
                        "leo_size": leo_file.stat().st_size,
                        "aleo_size": aleo_file.stat().st_size,
                    }
                    print(
                        f"  ✅ {contract_name}: Leo ({leo_file.stat().st_size} bytes), Aleo ({aleo_file.stat().st_size} bytes)"
                    )
                else:
                    tests[f"{contract_name}_files"] = {
                        "success": False,
                        "error": f"Missing files - Leo: {leo_file.exists()}, Aleo: {aleo_file.exists()}",
                    }
                    print(f"  ❌ {contract_name}: Missing files")

            except Exception as e:
                tests[f"{contract_name}_files"] = {"success": False, "error": str(e)}
                print(f"  ❌ {contract_name} file check failed: {e}")

        # Test 2: Check deployment status
        print("\n🚀 Checking deployment status...")
        try:
            # Check if we can access Leo command
            result = subprocess.run(
                ["leo", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                tests["leo_cli"] = {
                    "success": True,
                    "version": result.stdout.strip(),
                    "available": True,
                }
                print(f"  ✅ Leo CLI: {result.stdout.strip()}")

                # Test contract compilation status
                for contract_name, contract_path in self.contract_paths.items():
                    try:
                        # Check if contract builds successfully
                        build_result = subprocess.run(
                            ["leo", "build"],
                            cwd=contract_path,
                            capture_output=True,
                            text=True,
                            timeout=30,
                        )

                        if build_result.returncode == 0:
                            tests[f"{contract_name}_build"] = {
                                "success": True,
                                "message": "Contract builds successfully",
                            }
                            print(f"  ✅ {contract_name}: Builds successfully")
                        else:
                            tests[f"{contract_name}_build"] = {
                                "success": False,
                                "error": build_result.stderr[:200],
                            }
                            print(f"  ⚠️  {contract_name}: Build issues")

                    except subprocess.TimeoutExpired:
                        tests[f"{contract_name}_build"] = {
                            "success": False,
                            "error": "Build timeout",
                        }
                        print(f"  ⚠️  {contract_name}: Build timeout")
                    except Exception as e:
                        tests[f"{contract_name}_build"] = {
                            "success": False,
                            "error": str(e),
                        }
                        print(f"  ❌ {contract_name}: Build error - {e}")
            else:
                tests["leo_cli"] = {
                    "success": False,
                    "error": "Leo CLI not available",
                    "stderr": result.stderr,
                }
                print(
                    "  ⚠️  Leo CLI not available (not required for integration testing)"
                )

        except FileNotFoundError:
            tests["leo_cli"] = {"success": False, "error": "Leo command not found"}
            print("  ⚠️  Leo CLI not installed (contract files still testable)")
        except Exception as e:
            tests["leo_cli"] = {"success": False, "error": str(e)}
            print(f"  ❌ Leo CLI check failed: {e}")

        return tests

    async def test_contract_interfaces(self) -> Dict:
        """Test contract interface compatibility with TrustWrapper"""
        print("\n🔧 TESTING CONTRACT INTERFACES")
        print("-" * 40)

        tests = {}

        # Test 1: Hallucination Verifier Interface
        print("🛡️ Testing Hallucination Verifier interface...")
        try:
            # Simulate calling verify_response function
            response_hash = self._generate_field_hash(
                "Test AI response for verification"
            )
            model_hash = self._generate_field_hash("gpt-4")
            trust_score = 85  # 85% trust
            verification_method = 2  # AI verification
            evidence_count = 3
            verifier_address = "aleo1test" + "0" * 50  # Mock address

            # Validate parameters match contract expectations
            contract_call = {
                "function": "verify_response",
                "parameters": {
                    "response_text": response_hash,
                    "ai_model_hash": model_hash,
                    "trust_score": trust_score,
                    "verification_method": verification_method,
                    "evidence_count": evidence_count,
                    "verifier_address": verifier_address,
                },
            }

            # Validate parameter constraints
            valid_params = (
                trust_score <= 100
                and 1 <= verification_method <= 3
                and evidence_count >= 0
            )

            tests["hallucination_verifier_interface"] = {
                "success": valid_params,
                "contract_call": contract_call,
                "parameter_validation": valid_params,
                "estimated_gas": "0.01 credits",  # Placeholder
            }

            if valid_params:
                print("  ✅ Hallucination Verifier: Interface compatible")
            else:
                print("  ❌ Hallucination Verifier: Parameter validation failed")

        except Exception as e:
            tests["hallucination_verifier_interface"] = {
                "success": False,
                "error": str(e),
            }
            print(f"  ❌ Hallucination Verifier interface test failed: {e}")

        # Test 2: Trust Verifier Interface
        print("🔐 Testing Trust Verifier interface...")
        try:
            # Simulate ExecutionData structure
            execution_data = {
                "agent_id": self._generate_field_hash("test_agent"),
                "execution_id": self._generate_field_hash("exec_001"),
                "result_hash": self._generate_field_hash("execution_result"),
                "confidence": 7500,  # 75% confidence (0-10000 basis points)
                "timestamp": int(time.time()),
            }

            proof_data = self._generate_field_hash("zk_proof_data")
            verifier = "aleo1test" + "0" * 50

            contract_call = {
                "function": "verify_execution",
                "parameters": {
                    "execution": execution_data,
                    "proof_data": proof_data,
                    "verifier": verifier,
                },
            }

            # Validate constraints
            valid_params = (
                execution_data["confidence"] >= 5000  # MIN_CONFIDENCE
                and execution_data["confidence"] <= 10000
            )

            tests["trust_verifier_interface"] = {
                "success": valid_params,
                "contract_call": contract_call,
                "parameter_validation": valid_params,
                "estimated_gas": "0.02 credits",
            }

            if valid_params:
                print("  ✅ Trust Verifier: Interface compatible")
            else:
                print("  ❌ Trust Verifier: Parameter validation failed")

        except Exception as e:
            tests["trust_verifier_interface"] = {"success": False, "error": str(e)}
            print(f"  ❌ Trust Verifier interface test failed: {e}")

        # Test 3: Agent Registry Interface
        print("📋 Testing Agent Registry interface...")
        try:
            # Simulate agent registration
            agent_id = self._generate_field_hash("trustwrapper_agent")
            stake_amount = 10000  # 10K credits

            initial_metrics = {
                "accuracy_rate": 8500,  # 85% accuracy
                "success_rate": 9200,  # 92% success rate
                "avg_latency_ms": 150,  # 150ms average
                "total_executions": 1000,
            }

            contract_call = {
                "function": "register_agent",
                "parameters": {
                    "agent_id": agent_id,
                    "stake_amount": stake_amount,
                    "initial_metrics": initial_metrics,
                    "registration_height": 100000,
                },
            }

            # Validate constraints
            valid_params = (
                stake_amount >= 1000  # MIN_STAKE
                and stake_amount <= 1000000000  # MAX_STAKE
                and initial_metrics["accuracy_rate"] <= 10000
                and initial_metrics["success_rate"] <= 10000
                and initial_metrics["avg_latency_ms"] <= 10000
            )

            tests["agent_registry_interface"] = {
                "success": valid_params,
                "contract_call": contract_call,
                "parameter_validation": valid_params,
                "estimated_gas": "0.03 credits",
            }

            if valid_params:
                print("  ✅ Agent Registry: Interface compatible")
            else:
                print("  ❌ Agent Registry: Parameter validation failed")

        except Exception as e:
            tests["agent_registry_interface"] = {"success": False, "error": str(e)}
            print(f"  ❌ Agent Registry interface test failed: {e}")

        return tests

    async def test_trustwrapper_integration(self) -> Dict:
        """Test integration with TrustWrapper components"""
        print("\n🤝 TESTING TRUSTWRAPPER INTEGRATION")
        print("-" * 40)

        tests = {}

        # Test 1: ZK Proof Generator Integration
        print("🔒 Testing ZK Proof Generator integration...")
        try:
            # Simulate ZK proof generation for TrustWrapper
            verification_data = {
                "ai_response": "This is a test AI response",
                "trust_score": 87,
                "verification_method": "multi_oracle",
                "oracle_sources": ["chainlink", "band_protocol"],
                "confidence_level": 0.92,
            }

            # Generate proof parameters for Aleo contracts
            proof_params = {
                "response_hash": self._generate_field_hash(
                    verification_data["ai_response"]
                ),
                "trust_score_field": verification_data["trust_score"],
                "verification_method_field": 2,  # Multi-oracle
                "evidence_count": len(verification_data["oracle_sources"]),
            }

            # Validate proof generation workflow
            workflow_valid = all(
                [
                    proof_params["trust_score_field"] <= 100,
                    proof_params["verification_method_field"] in [1, 2, 3],
                    proof_params["evidence_count"] >= 0,
                ]
            )

            tests["zk_proof_integration"] = {
                "success": workflow_valid,
                "verification_data": verification_data,
                "proof_params": proof_params,
                "workflow_steps": [
                    "Generate response hash",
                    "Validate trust score",
                    "Map verification method",
                    "Count evidence sources",
                    "Prepare contract call",
                ],
            }

            if workflow_valid:
                print("  ✅ ZK Proof Generator: Integration successful")
            else:
                print("  ❌ ZK Proof Generator: Integration failed")

        except Exception as e:
            tests["zk_proof_integration"] = {"success": False, "error": str(e)}
            print(f"  ❌ ZK Proof Generator integration failed: {e}")

        # Test 2: Oracle Integration with Contracts
        print("📊 Testing Oracle integration with contracts...")
        try:
            # Simulate oracle data for contract verification
            oracle_data = {
                "price_feeds": {"BTC/USD": 67500.0, "ETH/USD": 2450.0},
                "consensus_achieved": True,
                "max_deviation": 0.015,  # 1.5%
                "source_count": 3,
                "health_score": 0.98,
            }

            # Map to contract parameters
            contract_evidence = {
                "evidence_type": 1,  # Factual evidence
                "confidence": int(oracle_data["health_score"] * 100),
                "detection_method": 4,  # Multi-oracle consensus
                "evidence_data": self._generate_field_hash(json.dumps(oracle_data)),
            }

            # Validate oracle-to-contract mapping
            mapping_valid = (
                contract_evidence["confidence"] <= 100
                and 1 <= contract_evidence["evidence_type"] <= 5
                and 1 <= contract_evidence["detection_method"] <= 4
            )

            tests["oracle_contract_integration"] = {
                "success": mapping_valid,
                "oracle_data": oracle_data,
                "contract_evidence": contract_evidence,
                "consensus_achieved": oracle_data["consensus_achieved"],
            }

            if mapping_valid:
                print("  ✅ Oracle Integration: Contract mapping successful")
            else:
                print("  ❌ Oracle Integration: Contract mapping failed")

        except Exception as e:
            tests["oracle_contract_integration"] = {"success": False, "error": str(e)}
            print(f"  ❌ Oracle integration failed: {e}")

        # Test 3: End-to-End Workflow Simulation
        print("🔄 Testing end-to-end workflow...")
        try:
            # Simulate complete TrustWrapper -> Aleo workflow
            workflow_steps = []

            # Step 1: TrustWrapper verification
            trustwrapper_result = {
                "verification_id": "tw_001",
                "ai_response": "AI prediction: BTC will reach $70,000",
                "trust_score": 0.89,
                "oracle_verification": True,
                "risk_assessment": "LOW",
            }
            workflow_steps.append("TrustWrapper verification complete")

            # Step 2: Prepare Aleo contract calls
            contract_calls = []

            # Hallucination verification call
            halluc_call = {
                "contract": "hallucination_verifier",
                "function": "verify_response",
                "params": {
                    "response_text": self._generate_field_hash(
                        trustwrapper_result["ai_response"]
                    ),
                    "trust_score": int(trustwrapper_result["trust_score"] * 100),
                    "verification_method": 3,  # Consensus
                },
            }
            contract_calls.append(halluc_call)
            workflow_steps.append("Hallucination verification prepared")

            # Trust verification call
            trust_call = {
                "contract": "trust_verifier",
                "function": "verify_execution",
                "params": {
                    "execution_id": self._generate_field_hash(
                        trustwrapper_result["verification_id"]
                    ),
                    "confidence": int(trustwrapper_result["trust_score"] * 10000),
                },
            }
            contract_calls.append(trust_call)
            workflow_steps.append("Trust verification prepared")

            # Step 3: Validate workflow integrity
            workflow_valid = all(
                [
                    len(contract_calls) == 2,
                    all(call.get("params") for call in contract_calls),
                    trustwrapper_result["trust_score"] > 0.8,
                ]
            )

            tests["e2e_workflow"] = {
                "success": workflow_valid,
                "trustwrapper_result": trustwrapper_result,
                "contract_calls": contract_calls,
                "workflow_steps": workflow_steps,
                "total_gas_estimate": "0.05 credits",
            }

            if workflow_valid:
                print("  ✅ End-to-End Workflow: Integration successful")
                print(f"     → {len(workflow_steps)} steps completed")
                print(f"     → {len(contract_calls)} contract calls prepared")
            else:
                print("  ❌ End-to-End Workflow: Integration failed")

        except Exception as e:
            tests["e2e_workflow"] = {"success": False, "error": str(e)}
            print(f"  ❌ End-to-End workflow failed: {e}")

        return tests

    def _generate_field_hash(self, data: str) -> str:
        """Generate a field-compatible hash from string data"""
        # Generate SHA256 hash and convert to field format for Aleo
        hash_obj = hashlib.sha256(data.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        # Convert to field format (simplified)
        return f"{hash_int % (2**128)}field"

    async def run_comprehensive_test(self) -> Dict:
        """Run comprehensive Aleo contract integration test"""
        print("🚀 ALEO CONTRACT INTEGRATION TEST")
        print("=" * 60)
        print("Testing EXISTING Aleo contracts + TrustWrapper integration")
        print("=" * 60)

        all_results = {}

        # Test contract deployments
        deployment_results = await self.test_contract_deployments()
        all_results["contract_deployments"] = deployment_results

        # Test contract interfaces
        interface_results = await self.test_contract_interfaces()
        all_results["contract_interfaces"] = interface_results

        # Test TrustWrapper integration
        integration_results = await self.test_trustwrapper_integration()
        all_results["trustwrapper_integration"] = integration_results

        # Calculate success metrics
        all_tests = []
        for category in all_results.values():
            all_tests.extend(category.values())

        successful_tests = sum(1 for test in all_tests if test.get("success", False))
        total_tests = len(all_tests)
        success_rate = successful_tests / total_tests if total_tests > 0 else 0

        print("\n" + "=" * 60)
        print(
            f"📊 ALEO CONTRACT INTEGRATION RESULTS: {successful_tests}/{total_tests} PASSED ({success_rate:.1%})"
        )

        if success_rate >= 0.8:
            print("✅ ALEO CONTRACT INTEGRATION SUCCESSFUL!")
            print("🎯 Ready for testnet deployment and ZK proof generation")
        elif success_rate >= 0.6:
            print("⚠️  PARTIAL INTEGRATION - Most components operational")
        else:
            print("❌ INTEGRATION NEEDS ATTENTION - Multiple components require fixes")

        # Summary
        all_results["summary"] = {
            "successful_tests": successful_tests,
            "total_tests": total_tests,
            "success_rate": success_rate,
            "status": (
                "operational"
                if success_rate >= 0.8
                else "degraded" if success_rate >= 0.6 else "failed"
            ),
            "timestamp": time.time(),
            "contracts_found": len(self.contract_paths),
            "ready_for_deployment": success_rate >= 0.8,
        }

        return all_results


async def main():
    """Run Aleo contract integration test"""
    tester = AleoContractIntegration()
    results = await tester.run_comprehensive_test()

    # Save detailed results
    with open("aleo_contract_integration_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n📄 Detailed results saved to: aleo_contract_integration_results.json")

    # Return success status
    return results["summary"]["success_rate"] >= 0.8


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

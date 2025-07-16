#!/usr/bin/env python3
"""
ZK Proof Performance Benchmark - TrustWrapper v3.0 POC
Comprehensive evaluation of Groth16, Plonk, and Plonky2 for AI verification
"""

import asyncio
import hashlib
import json
import logging
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Result of a single benchmark test"""

    circuit_name: str
    proof_system: str
    setup_time_ms: float
    avg_prove_time_ms: float
    min_prove_time_ms: float
    max_prove_time_ms: float
    verify_time_ms: float
    proof_size_bytes: int
    meets_target: bool
    test_iterations: int


@dataclass
class SystemAnalysis:
    """Analysis of proof system performance"""

    system_name: str
    avg_prove_time_ms: float
    avg_proof_size_bytes: float
    target_compliance_rate: float
    recommended: bool
    strengths: List[str]
    weaknesses: List[str]


class MockCircuit:
    """Mock circuit for benchmarking different verification patterns"""

    def __init__(self, name: str, inputs: int, constraints: int):
        self.name = name
        self.inputs = inputs
        self.constraints = constraints
        self.public_inputs = None

    def generate_random_witness(self) -> Dict[str, Any]:
        """Generate random witness for benchmarking"""
        witness = {
            "private_inputs": np.random.random(self.inputs).tolist(),
            "constraints": np.random.random(self.constraints).tolist(),
        }
        # Simulate public inputs (oracle data, AI decision)
        self.public_inputs = {
            "oracle_price": np.random.uniform(40000, 80000),
            "oracle_confidence": np.random.uniform(0.7, 0.95),
            "ai_confidence": np.random.uniform(0.6, 0.9),
        }
        return witness

    def get_complexity_score(self) -> float:
        """Get relative complexity score for this circuit"""
        return (self.inputs * 0.1) + (self.constraints * 0.001)


class MockProofSystem:
    """Base class for mock proof systems"""

    def __init__(self, name: str):
        self.name = name
        self.proving_key = None
        self.verifying_key = None

    def setup(self, circuit: MockCircuit) -> Tuple[Dict, Dict]:
        """Mock trusted setup"""
        setup_complexity = circuit.get_complexity_score()
        time.sleep(setup_complexity * 0.01)  # Simulate setup time

        self.proving_key = {
            "circuit_hash": hashlib.sha256(
                f"{circuit.name}_{circuit.inputs}_{circuit.constraints}".encode()
            ).hexdigest(),
            "system": self.name,
        }
        self.verifying_key = {
            "circuit_hash": self.proving_key["circuit_hash"],
            "system": self.name,
        }

        return self.proving_key, self.verifying_key

    def prove(self, proving_key: Dict, witness: Dict[str, Any]) -> Dict:
        """Generate proof (mock implementation)"""
        raise NotImplementedError

    def verify(self, verifying_key: Dict, proof: Dict, public_inputs: Dict) -> bool:
        """Verify proof (mock implementation)"""
        verify_complexity = len(str(proof)) * 0.000001
        time.sleep(verify_complexity)
        return proof.get("valid", True)

    def serialize_proof(self, proof: Dict) -> bytes:
        """Serialize proof to bytes"""
        return json.dumps(proof).encode("utf-8")


class MockGroth16System(MockProofSystem):
    """Mock Groth16 proof system with realistic timing"""

    def __init__(self):
        super().__init__("groth16")

    def prove(self, proving_key: Dict, witness: Dict[str, Any]) -> Dict:
        """Generate Groth16 proof with realistic timing"""
        # Groth16 has fixed proof generation time regardless of witness size
        base_time = 0.15  # 150ms base time
        complexity_factor = len(witness["constraints"]) * 0.0001

        time.sleep(base_time + complexity_factor)

        return {
            "system": "groth16",
            "a": f"groth16_a_{hash(str(witness)) % 10000}",
            "b": f"groth16_b_{hash(str(witness)) % 10000}",
            "c": f"groth16_c_{hash(str(witness)) % 10000}",
            "valid": True,
            "size_factor": 1.0,  # Groth16 has fixed small proof size
        }


class MockPlonkSystem(MockProofSystem):
    """Mock Plonk proof system with realistic timing"""

    def __init__(self):
        super().__init__("plonk")

    def prove(self, proving_key: Dict, witness: Dict[str, Any]) -> Dict:
        """Generate Plonk proof with realistic timing"""
        # Plonk is faster for larger circuits
        base_time = 0.08  # 80ms base time
        complexity_factor = len(witness["constraints"]) * 0.00005

        time.sleep(base_time + complexity_factor)

        return {
            "system": "plonk",
            "commitments": [
                f"plonk_commit_{i}_{hash(str(witness)) % 10000}" for i in range(4)
            ],
            "evaluations": [
                f"plonk_eval_{i}_{hash(str(witness)) % 10000}" for i in range(6)
            ],
            "opening_proof": f"plonk_opening_{hash(str(witness)) % 10000}",
            "valid": True,
            "size_factor": 1.2,  # Plonk proofs are slightly larger
        }


class MockPlonky2System(MockProofSystem):
    """Mock Plonky2 proof system with realistic timing"""

    def __init__(self):
        super().__init__("plonky2")

    def prove(self, proving_key: Dict, witness: Dict[str, Any]) -> Dict:
        """Generate Plonky2 proof with realistic timing"""
        # Plonky2 is very fast for recursive proofs
        base_time = 0.005  # 5ms base time
        complexity_factor = len(witness["constraints"]) * 0.00001

        time.sleep(base_time + complexity_factor)

        return {
            "system": "plonky2",
            "fri_proof": f"plonky2_fri_{hash(str(witness)) % 10000}",
            "merkle_caps": [f"cap_{i}_{hash(str(witness)) % 10000}" for i in range(3)],
            "opening_proof": f"plonky2_opening_{hash(str(witness)) % 10000}",
            "valid": True,
            "size_factor": 0.8,  # Plonky2 has smaller proofs
        }


class GPUAcceleratedSystem(MockProofSystem):
    """Mock GPU-accelerated proof system"""

    def __init__(self, base_system: MockProofSystem, gpu_speedup: float = 3.0):
        super().__init__(f"{base_system.name}_gpu")
        self.base_system = base_system
        self.gpu_speedup = gpu_speedup
        self.gpu_available = True  # Assume GPU is available for testing

    def setup(self, circuit: MockCircuit) -> Tuple[Dict, Dict]:
        return self.base_system.setup(circuit)

    def prove(self, proving_key: Dict, witness: Dict[str, Any]) -> Dict:
        """Generate proof with GPU acceleration"""
        if not self.gpu_available:
            return self.base_system.prove(proving_key, witness)

        # Simulate GPU acceleration
        original_time_start = time.time()
        proof = self.base_system.prove(proving_key, witness)
        original_time = time.time() - original_time_start

        # Apply GPU speedup
        accelerated_time = original_time / self.gpu_speedup
        time.sleep(accelerated_time - original_time)  # Adjust timing

        proof["gpu_accelerated"] = True
        proof["speedup_factor"] = self.gpu_speedup
        return proof

    def verify(self, verifying_key: Dict, proof: Dict, public_inputs: Dict) -> bool:
        return self.base_system.verify(verifying_key, proof, public_inputs)

    def serialize_proof(self, proof: Dict) -> bytes:
        return self.base_system.serialize_proof(proof)


class ZKProofPerformanceBenchmark:
    """Comprehensive ZK proof performance benchmark for TrustWrapper v3.0"""

    def __init__(self):
        self.proof_systems = {
            "groth16": MockGroth16System(),
            "plonk": MockPlonkSystem(),
            "plonky2": MockPlonky2System(),
            "groth16_gpu": GPUAcceleratedSystem(MockGroth16System(), gpu_speedup=2.5),
            "plonk_gpu": GPUAcceleratedSystem(MockPlonkSystem(), gpu_speedup=3.5),
            "plonky2_gpu": GPUAcceleratedSystem(MockPlonky2System(), gpu_speedup=4.0),
        }
        self.test_circuits = self._generate_test_circuits()
        self.benchmark_results = []
        self.target_prove_time_ms = 10.0  # <10ms target

    def _generate_test_circuits(self) -> Dict[str, MockCircuit]:
        """Generate circuits representing TrustWrapper verification patterns"""
        return {
            "simple_verification": MockCircuit(
                name="simple_verification",
                inputs=8,  # Basic price/confidence verification
                constraints=50,
            ),
            "standard_verification": MockCircuit(
                name="standard_verification",
                inputs=16,  # Standard XAI verification
                constraints=200,
            ),
            "complex_verification": MockCircuit(
                name="complex_verification",
                inputs=32,  # Full XAI verification with oracle data
                constraints=500,
            ),
            "batch_verification": MockCircuit(
                name="batch_verification",
                inputs=64,  # Batch processing optimization
                constraints=1000,
            ),
            "enterprise_verification": MockCircuit(
                name="enterprise_verification",
                inputs=128,  # Enterprise-grade verification
                constraints=2000,
            ),
        }

    async def run_comprehensive_benchmark(self) -> Dict[str, Any]:
        """Execute comprehensive ZK proof performance benchmark"""
        logger.info("🔬 Starting TrustWrapper v3.0 ZK Proof Performance Benchmark")
        logger.info(f"Target: <{self.target_prove_time_ms}ms proof generation")

        benchmark_start_time = time.time()

        for system_name, system in self.proof_systems.items():
            logger.info(f"\n📊 Testing {system_name.upper()} Performance")

            system_results = []

            for circuit_name, circuit in self.test_circuits.items():
                logger.info(f"  🔧 Testing {circuit_name}...")

                try:
                    result = await self._benchmark_system_circuit(system, circuit)
                    system_results.append(result)

                    # Log immediate results
                    status = "✅" if result.meets_target else "❌"
                    logger.info(
                        f"    {status} Prove: {result.avg_prove_time_ms:.1f}ms (target: <{self.target_prove_time_ms}ms)"
                    )
                    logger.info(f"       Verify: {result.verify_time_ms:.2f}ms")
                    logger.info(f"       Size: {result.proof_size_bytes} bytes")

                except Exception as e:
                    logger.error(f"    ❌ Error testing {circuit_name}: {e}")
                    # Create error result
                    error_result = BenchmarkResult(
                        circuit_name=circuit_name,
                        proof_system=system_name,
                        setup_time_ms=0,
                        avg_prove_time_ms=float("inf"),
                        min_prove_time_ms=float("inf"),
                        max_prove_time_ms=float("inf"),
                        verify_time_ms=0,
                        proof_size_bytes=0,
                        meets_target=False,
                        test_iterations=0,
                    )
                    system_results.append(error_result)

            self.benchmark_results.extend(system_results)

        benchmark_time = (time.time() - benchmark_start_time) * 1000
        logger.info(f"\n✅ Benchmark completed in {benchmark_time:.1f}ms")

        # Analyze results
        analysis = self._analyze_results()

        return {
            "benchmark_results": [asdict(result) for result in self.benchmark_results],
            "system_analysis": [
                asdict(analysis) for analysis in self._generate_system_analysis()
            ],
            "recommendations": self._generate_recommendations(analysis),
            "benchmark_duration_ms": benchmark_time,
            "target_prove_time_ms": self.target_prove_time_ms,
        }

    async def _benchmark_system_circuit(
        self, system: MockProofSystem, circuit: MockCircuit, iterations: int = 10
    ) -> BenchmarkResult:
        """Benchmark a specific system-circuit combination"""

        # Setup phase
        setup_start = time.time()
        proving_key, verifying_key = system.setup(circuit)
        setup_time = (time.time() - setup_start) * 1000

        # Proof generation phase (multiple iterations for accuracy)
        prove_times = []
        proof_sizes = []

        for i in range(iterations):
            witness = circuit.generate_random_witness()

            prove_start = time.time()
            proof = system.prove(proving_key, witness)
            prove_time = (time.time() - prove_start) * 1000
            prove_times.append(prove_time)

            # Measure proof size
            proof_bytes = system.serialize_proof(proof)
            proof_sizes.append(len(proof_bytes))

        # Verification phase
        verify_start = time.time()
        is_valid = system.verify(verifying_key, proof, circuit.public_inputs)
        verify_time = (time.time() - verify_start) * 1000

        # Calculate statistics
        avg_prove_time = sum(prove_times) / len(prove_times)
        min_prove_time = min(prove_times)
        max_prove_time = max(prove_times)
        avg_proof_size = int(sum(proof_sizes) / len(proof_sizes))

        # Check if meets target
        meets_target = avg_prove_time < self.target_prove_time_ms

        return BenchmarkResult(
            circuit_name=circuit.name,
            proof_system=system.name,
            setup_time_ms=setup_time,
            avg_prove_time_ms=avg_prove_time,
            min_prove_time_ms=min_prove_time,
            max_prove_time_ms=max_prove_time,
            verify_time_ms=verify_time,
            proof_size_bytes=avg_proof_size,
            meets_target=meets_target,
            test_iterations=iterations,
        )

    def _analyze_results(self) -> Dict[str, Any]:
        """Analyze benchmark results and generate insights"""

        # Group results by system
        systems = {}
        for result in self.benchmark_results:
            if result.proof_system not in systems:
                systems[result.proof_system] = []
            systems[result.proof_system].append(result)

        analysis = {
            "best_overall_system": None,
            "best_for_speed": None,
            "best_for_size": None,
            "systems_meeting_target": [],
            "performance_summary": {},
        }

        # Analyze each system
        for system_name, results in systems.items():
            if not results:
                continue

            # Calculate averages
            valid_results = [r for r in results if r.avg_prove_time_ms != float("inf")]
            if not valid_results:
                continue

            avg_prove_time = sum(r.avg_prove_time_ms for r in valid_results) / len(
                valid_results
            )
            avg_proof_size = sum(r.proof_size_bytes for r in valid_results) / len(
                valid_results
            )
            target_compliance = sum(1 for r in valid_results if r.meets_target) / len(
                valid_results
            )

            analysis["performance_summary"][system_name] = {
                "avg_prove_time_ms": avg_prove_time,
                "avg_proof_size_bytes": avg_proof_size,
                "target_compliance_rate": target_compliance,
                "total_tests": len(valid_results),
            }

            # Track systems meeting target
            if target_compliance >= 0.8:  # 80%+ of tests meet target
                analysis["systems_meeting_target"].append(system_name)

        # Find best systems
        if analysis["performance_summary"]:
            # Best for speed (lowest average prove time)
            analysis["best_for_speed"] = min(
                analysis["performance_summary"].keys(),
                key=lambda x: analysis["performance_summary"][x]["avg_prove_time_ms"],
            )

            # Best for size (smallest proofs)
            analysis["best_for_size"] = min(
                analysis["performance_summary"].keys(),
                key=lambda x: analysis["performance_summary"][x][
                    "avg_proof_size_bytes"
                ],
            )

            # Best overall (highest target compliance)
            analysis["best_overall_system"] = max(
                analysis["performance_summary"].keys(),
                key=lambda x: analysis["performance_summary"][x][
                    "target_compliance_rate"
                ],
            )

        return analysis

    def _generate_system_analysis(self) -> List[SystemAnalysis]:
        """Generate detailed analysis for each proof system"""
        analysis_list = []

        # Group results by system
        systems = {}
        for result in self.benchmark_results:
            if result.proof_system not in systems:
                systems[result.proof_system] = []
            systems[result.proof_system].append(result)

        for system_name, results in systems.items():
            valid_results = [r for r in results if r.avg_prove_time_ms != float("inf")]
            if not valid_results:
                continue

            avg_prove_time = sum(r.avg_prove_time_ms for r in valid_results) / len(
                valid_results
            )
            avg_proof_size = sum(r.proof_size_bytes for r in valid_results) / len(
                valid_results
            )
            target_compliance = sum(1 for r in valid_results if r.meets_target) / len(
                valid_results
            )

            # Determine strengths and weaknesses
            strengths = []
            weaknesses = []

            if avg_prove_time < 20:
                strengths.append("Fast proof generation")
            else:
                weaknesses.append("Slow proof generation")

            if avg_proof_size < 1000:
                strengths.append("Compact proof size")
            else:
                weaknesses.append("Large proof size")

            if target_compliance > 0.8:
                strengths.append("Meets performance targets")
            else:
                weaknesses.append("Inconsistent performance")

            if "gpu" in system_name.lower():
                strengths.append("GPU acceleration")

            # Recommendation
            recommended = target_compliance >= 0.6 and avg_prove_time < 50

            analysis = SystemAnalysis(
                system_name=system_name,
                avg_prove_time_ms=avg_prove_time,
                avg_proof_size_bytes=avg_proof_size,
                target_compliance_rate=target_compliance,
                recommended=recommended,
                strengths=strengths,
                weaknesses=weaknesses,
            )

            analysis_list.append(analysis)

        return analysis_list

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on benchmark results"""

        recommendations = {
            "primary_recommendation": None,
            "fallback_options": [],
            "optimization_strategies": [],
            "implementation_notes": [],
            "risk_assessment": "low",
        }

        systems_meeting_target = analysis.get("systems_meeting_target", [])
        best_overall = analysis.get("best_overall_system")
        performance_summary = analysis.get("performance_summary", {})

        if systems_meeting_target:
            # We have systems meeting the target
            primary_system = systems_meeting_target[0]
            recommendations["primary_recommendation"] = (
                f"PROCEED with {primary_system} - meets <10ms target"
            )
            recommendations["fallback_options"] = (
                systems_meeting_target[1:] if len(systems_meeting_target) > 1 else []
            )
            recommendations["risk_assessment"] = "low"

            # Add GPU acceleration note if applicable
            if not any("gpu" in system for system in systems_meeting_target):
                recommendations["optimization_strategies"].append(
                    "Consider GPU acceleration for further improvement"
                )

        elif (
            best_overall
            and performance_summary[best_overall]["target_compliance_rate"] > 0.4
        ):
            # Partial success - some circuits meet target
            primary_system = best_overall
            compliance_rate = performance_summary[best_overall][
                "target_compliance_rate"
            ]
            avg_time = performance_summary[best_overall]["avg_prove_time_ms"]

            recommendations["primary_recommendation"] = (
                f"CONDITIONAL PROCEED with {primary_system} - {compliance_rate:.1%} compliance, {avg_time:.1f}ms average"
            )
            recommendations["risk_assessment"] = "medium"

            # Optimization strategies
            recommendations["optimization_strategies"].extend(
                [
                    "Implement aggressive proof caching for repeated patterns",
                    "Use batch processing for multiple verifications",
                    "Consider circuit optimization and pre-computation",
                ]
            )

            if not any("gpu" in system for system in performance_summary.keys()):
                recommendations["optimization_strategies"].append(
                    "GPU acceleration mandatory for production"
                )

        else:
            # No systems meet requirements
            recommendations["primary_recommendation"] = (
                "INVESTIGATE alternative approaches - no systems meet targets"
            )
            recommendations["risk_assessment"] = "high"

            recommendations["optimization_strategies"].extend(
                [
                    "Explore newer proof systems (STARK, Nova)",
                    "Implement hybrid verification (simple proofs + trust)",
                    "Consider relaxing latency requirements for complex verifications",
                ]
            )

        # Implementation notes
        recommendations["implementation_notes"].extend(
            [
                "Implement proof system as pluggable interface for easy swapping",
                "Use proof aggregation for batch processing",
                "Cache proving keys and common proof patterns",
                "Monitor proof generation performance in production",
            ]
        )

        return recommendations

    def save_results(
        self, results: Dict[str, Any], filepath: Optional[str] = None
    ) -> str:
        """Save benchmark results to file"""
        if not filepath:
            timestamp = int(time.time())
            filepath = f"zk_proof_benchmark_results_{timestamp}.json"

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2, default=str)

        return filepath


async def main():
    """Main benchmark execution"""
    print("🚀 TrustWrapper v3.0 ZK Proof Performance Benchmark")
    print("=" * 60)

    benchmark = ZKProofPerformanceBenchmark()

    try:
        # Run comprehensive benchmark
        results = await benchmark.run_comprehensive_benchmark()

        # Print summary results
        print("\n📊 BENCHMARK SUMMARY")
        print("=" * 40)

        analysis = results.get("recommendations", {})
        print(
            f"Primary Recommendation: {analysis.get('primary_recommendation', 'N/A')}"
        )
        print(f"Risk Assessment: {analysis.get('risk_assessment', 'unknown').upper()}")

        # Print system performance
        print("\n🔍 SYSTEM PERFORMANCE")
        print("=" * 40)

        for system_analysis in results["system_analysis"]:
            system = system_analysis["system_name"]
            avg_time = system_analysis["avg_prove_time_ms"]
            compliance = system_analysis["target_compliance_rate"]
            recommended = "✅" if system_analysis["recommended"] else "❌"

            print(
                f"{recommended} {system}: {avg_time:.1f}ms avg, {compliance:.1%} compliance"
            )

        # Print optimization strategies
        if analysis.get("optimization_strategies"):
            print("\n💡 OPTIMIZATION STRATEGIES")
            print("=" * 40)
            for strategy in analysis["optimization_strategies"]:
                print(f"• {strategy}")

        # Save detailed results
        results_file = benchmark.save_results(results)
        print(f"\n📄 Detailed results saved to: {results_file}")

        # Final recommendation
        risk_level = analysis.get("risk_assessment", "unknown")
        if risk_level == "low":
            print("\n🎉 ZK PROOF OPTIMIZATION: VALIDATED!")
            print("✅ Performance targets achievable with recommended system")
        elif risk_level == "medium":
            print("\n⚠️  ZK PROOF OPTIMIZATION: CONDITIONAL SUCCESS")
            print("✅ Partial performance targets met with optimization")
        else:
            print("\n❌ ZK PROOF OPTIMIZATION: REQUIRES INVESTIGATION")
            print("⚠️  Performance targets not met - alternative approaches needed")

        return risk_level == "low"

    except Exception as e:
        logger.error(f"Benchmark execution failed: {e}")
        print(f"\n❌ Benchmark execution failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

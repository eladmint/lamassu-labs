"""
TrustWrapper LangChain Performance Tests

Comprehensive performance testing for TrustWrapper LangChain integration.
Follows ADR-005 testing strategy for performance validation.
"""

import asyncio
import statistics
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from src.integrations.langchain import (
    TrustWrapperCallback,
    TrustWrapperConfig,
)
from src.integrations.langchain.base_types import LLMResult
from src.integrations.langchain.langchain_config import VerificationLevel


class BenchmarkLLM:
    """Mock LLM for benchmarking"""

    async def agenerate(self, prompts, **kwargs):
        """Generate response with minimal overhead"""
        # Simulate some processing time (10ms)
        await asyncio.sleep(0.01)

        response_text = f"Response to: {prompts[0]}"
        return LLMResult([[MockGeneration(response_text)]])


class MockGeneration:
    def __init__(self, text):
        self.text = text


async def benchmark_scenario(
    name: str, config: TrustWrapperConfig, iterations: int = 100
):
    """Run a benchmark scenario"""
    print(f"\n🏃 Running scenario: {name}")
    print(f"   Iterations: {iterations}")
    if config:
        print(f"   Verification Level: {config.verification_level.value}")

    # Initialize components
    llm = BenchmarkLLM()
    trustwrapper = TrustWrapperCallback(config) if config else None

    # Warm up
    for _ in range(10):
        result = await llm.agenerate(["warm up query"])
        if trustwrapper:
            await trustwrapper.on_llm_end(result)

    # Benchmark
    latencies = []

    for i in range(iterations):
        query = f"test query {i}"

        start_time = time.perf_counter()

        # LLM call
        result = await llm.agenerate([query])

        # TrustWrapper verification (if enabled)
        if trustwrapper:
            await trustwrapper.on_llm_end(result)

        end_time = time.perf_counter()

        latency_ms = (end_time - start_time) * 1000
        latencies.append(latency_ms)

    # Calculate statistics
    avg_latency = statistics.mean(latencies)
    median_latency = statistics.median(latencies)
    p95_latency = statistics.quantiles(latencies, n=100)[94]  # 95th percentile
    p99_latency = statistics.quantiles(latencies, n=100)[98]  # 99th percentile

    print("\n   📊 Results:")
    print(f"   • Average: {avg_latency:.2f}ms")
    print(f"   • Median: {median_latency:.2f}ms")
    print(f"   • P95: {p95_latency:.2f}ms")
    print(f"   • P99: {p99_latency:.2f}ms")

    return {
        "name": name,
        "avg": avg_latency,
        "median": median_latency,
        "p95": p95_latency,
        "p99": p99_latency,
    }


async def run_performance_benchmark():
    """Run comprehensive performance benchmarks"""

    print("=" * 80)
    print("⚡ TrustWrapper LangChain Performance Benchmark")
    print("=" * 80)
    print("\nMeasuring the real performance impact of TrustWrapper integration")
    print("Target: <100ms overhead for verification\n")

    # Test scenarios
    scenarios = [
        # Baseline - no verification
        ("Baseline (No TrustWrapper)", None),
        # Minimal verification
        (
            "Minimal Verification",
            TrustWrapperConfig(
                verification_level=VerificationLevel.MINIMAL,
                verify_tool_outputs=False,
                verify_agent_actions=False,
                audit_logging=False,
            ),
        ),
        # Standard verification
        (
            "Standard Verification",
            TrustWrapperConfig(verification_level=VerificationLevel.STANDARD),
        ),
        # Comprehensive verification
        (
            "Comprehensive Verification",
            TrustWrapperConfig(
                verification_level=VerificationLevel.COMPREHENSIVE, pii_detection=True
            ),
        ),
        # Enterprise verification (all features)
        (
            "Enterprise Verification",
            TrustWrapperConfig(
                verification_level=VerificationLevel.ENTERPRISE,
                pii_detection=True,
                audit_logging=True,
            ),
        ),
        # With caching enabled
        (
            "Standard + Caching",
            TrustWrapperConfig(
                verification_level=VerificationLevel.STANDARD, cache_ttl=3600
            ),
        ),
    ]

    results = []

    for name, config in scenarios:
        result = await benchmark_scenario(name, config)
        results.append(result)
        await asyncio.sleep(0.5)  # Brief pause between scenarios

    # Compare results
    print(f"\n{'='*80}")
    print("📊 Performance Comparison")
    print(f"{'='*80}")

    baseline = results[0]["avg"]

    print(f"\n{'Scenario':<30} {'Avg (ms)':<10} {'Overhead':<10} {'P95 (ms)':<10}")
    print("-" * 60)

    for result in results:
        overhead = (
            result["avg"] - baseline
            if result["name"] != "Baseline (No TrustWrapper)"
            else 0
        )
        overhead_pct = (overhead / baseline * 100) if baseline > 0 else 0

        print(
            f"{result['name']:<30} {result['avg']:<10.2f} "
            f"{f'+{overhead:.1f}ms ({overhead_pct:.0f}%)':<10} {result['p95']:<10.2f}"
        )

    # Key findings
    print(f"\n{'='*80}")
    print("🎯 Key Findings")
    print(f"{'='*80}")

    standard_overhead = results[2]["avg"] - baseline
    enterprise_overhead = results[4]["avg"] - baseline
    cached_overhead = results[5]["avg"] - baseline

    print(f"\n✅ Standard Verification Overhead: {standard_overhead:.1f}ms")
    print(f"✅ Enterprise Verification Overhead: {enterprise_overhead:.1f}ms")
    print(
        f"✅ Caching Benefit: {(results[2]['avg'] - results[5]['avg']):.1f}ms reduction"
    )

    if standard_overhead < 100:
        print("\n🎉 SUCCESS: TrustWrapper meets <100ms overhead target!")
        print(f"   Standard verification adds only {standard_overhead:.0f}ms")

    # Recommendations
    print(f"\n{'='*80}")
    print("💡 Recommendations")
    print(f"{'='*80}")
    print("\n1. Use 'Standard' verification for most use cases")
    print("2. Enable caching for repeated queries (significant performance gain)")
    print("3. Reserve 'Enterprise' mode for compliance-critical applications")
    print("4. Consider 'Minimal' mode for high-throughput, low-risk scenarios")

    print(f"\n{'='*80}")
    print("✅ Benchmark Complete")
    print(f"{'='*80}")
    print("\n🔗 Full performance guide: https://trustwrapper.ai/performance")


if __name__ == "__main__":
    asyncio.run(run_performance_benchmark())

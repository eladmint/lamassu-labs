"""
Hallucination Detection Metrics and Performance Analysis
Tracks and analyzes hallucination detection performance
"""

import asyncio
import statistics
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class HallucinationMetrics:
    """Comprehensive metrics for hallucination detection"""

    # Detection accuracy metrics
    true_positives: int = 0  # Correctly identified hallucinations
    false_positives: int = 0  # Incorrectly flagged as hallucination
    true_negatives: int = 0  # Correctly identified as accurate
    false_negatives: int = 0  # Missed hallucinations

    # Performance metrics
    detection_latencies: List[float] = field(
        default_factory=list
    )  # Time to detect in ms
    trust_scores: List[float] = field(
        default_factory=list
    )  # Distribution of trust scores
    proof_generation_times: List[float] = field(
        default_factory=list
    )  # ZK proof overhead in ms

    # Hallucination type breakdown
    type_counts: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    type_detection_rates: Dict[str, float] = field(
        default_factory=lambda: defaultdict(float)
    )

    # Model-specific metrics
    model_metrics: Dict[str, Dict[str, Any]] = field(
        default_factory=lambda: defaultdict(dict)
    )

    @property
    def precision(self) -> float:
        """Precision: TP / (TP + FP)"""
        denominator = self.true_positives + self.false_positives
        return self.true_positives / denominator if denominator > 0 else 0.0

    @property
    def recall(self) -> float:
        """Recall: TP / (TP + FN)"""
        denominator = self.true_positives + self.false_negatives
        return self.true_positives / denominator if denominator > 0 else 0.0

    @property
    def f1_score(self) -> float:
        """F1 Score: Harmonic mean of precision and recall"""
        if self.precision + self.recall == 0:
            return 0.0
        return 2 * (self.precision * self.recall) / (self.precision + self.recall)

    @property
    def accuracy(self) -> float:
        """Overall accuracy: (TP + TN) / Total"""
        total = (
            self.true_positives
            + self.false_positives
            + self.true_negatives
            + self.false_negatives
        )
        return (self.true_positives + self.true_negatives) / total if total > 0 else 0.0

    @property
    def avg_detection_latency(self) -> float:
        """Average detection latency in milliseconds"""
        return (
            statistics.mean(self.detection_latencies)
            if self.detection_latencies
            else 0.0
        )

    @property
    def p95_detection_latency(self) -> float:
        """95th percentile detection latency"""
        if not self.detection_latencies:
            return 0.0
        sorted_latencies = sorted(self.detection_latencies)
        idx = int(len(sorted_latencies) * 0.95)
        return sorted_latencies[idx]

    @property
    def avg_trust_score(self) -> float:
        """Average trust score across all evaluations"""
        return statistics.mean(self.trust_scores) if self.trust_scores else 0.0

    def update_detection(
        self,
        predicted_hallucination: bool,
        actual_hallucination: bool,
        latency_ms: float,
        trust_score: float,
        proof_time_ms: float,
        hallucination_type: Optional[str] = None,
    ):
        """Update metrics with a detection result"""
        # Update confusion matrix
        if predicted_hallucination and actual_hallucination:
            self.true_positives += 1
        elif predicted_hallucination and not actual_hallucination:
            self.false_positives += 1
        elif not predicted_hallucination and actual_hallucination:
            self.false_negatives += 1
        else:
            self.true_negatives += 1

        # Update performance metrics
        self.detection_latencies.append(latency_ms)
        self.trust_scores.append(trust_score)
        self.proof_generation_times.append(proof_time_ms)

        # Update type-specific metrics
        if hallucination_type:
            self.type_counts[hallucination_type] += 1
            if predicted_hallucination and actual_hallucination:
                # Correctly detected this type
                current_count = self.type_counts[hallucination_type]
                current_rate = self.type_detection_rates[hallucination_type]
                # Update running average
                self.type_detection_rates[hallucination_type] = (
                    current_rate * (current_count - 1) + 1.0
                ) / current_count

    def update_model_metrics(self, model_name: str, metrics: Dict[str, Any]):
        """Update model-specific metrics"""
        if model_name not in self.model_metrics:
            self.model_metrics[model_name] = {
                "total_queries": 0,
                "hallucination_count": 0,
                "avg_confidence": 0.0,
                "latencies": [],
            }

        model_data = self.model_metrics[model_name]
        model_data["total_queries"] += 1
        if metrics.get("has_hallucination"):
            model_data["hallucination_count"] += 1

        # Update average confidence
        current_avg = model_data["avg_confidence"]
        new_confidence = metrics.get("confidence", 0.0)
        model_data["avg_confidence"] = (
            current_avg * (model_data["total_queries"] - 1) + new_confidence
        ) / model_data["total_queries"]

        # Store latency
        if "latency" in metrics:
            model_data["latencies"].append(metrics["latency"])

    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        return {
            "accuracy_metrics": {
                "precision": self.precision,
                "recall": self.recall,
                "f1_score": self.f1_score,
                "accuracy": self.accuracy,
            },
            "confusion_matrix": {
                "true_positives": self.true_positives,
                "false_positives": self.false_positives,
                "true_negatives": self.true_negatives,
                "false_negatives": self.false_negatives,
            },
            "performance_metrics": {
                "avg_detection_latency_ms": self.avg_detection_latency,
                "p95_detection_latency_ms": self.p95_detection_latency,
                "avg_proof_generation_ms": (
                    statistics.mean(self.proof_generation_times)
                    if self.proof_generation_times
                    else 0
                ),
                "avg_trust_score": self.avg_trust_score,
            },
            "hallucination_types": {
                "counts": dict(self.type_counts),
                "detection_rates": dict(self.type_detection_rates),
            },
            "model_performance": self.model_metrics,
            "total_evaluations": self.true_positives
            + self.false_positives
            + self.true_negatives
            + self.false_negatives,
        }

    def meets_minimum_criteria(self) -> Tuple[bool, List[str]]:
        """Check if metrics meet minimum performance criteria"""
        failures = []

        # Check minimum viable performance
        if self.precision < 0.85:
            failures.append(f"Precision {self.precision:.2%} < 85% minimum")
        if self.recall < 0.90:
            failures.append(f"Recall {self.recall:.2%} < 90% minimum")
        if self.f1_score < 0.875:
            failures.append(f"F1 Score {self.f1_score:.2%} < 87.5% minimum")
        if self.avg_detection_latency > 200:
            failures.append(
                f"Avg latency {self.avg_detection_latency:.0f}ms > 200ms limit"
            )

        return len(failures) == 0, failures

    def meets_target_criteria(self) -> Tuple[bool, List[str]]:
        """Check if metrics meet target performance criteria"""
        failures = []

        # Check target performance
        if self.precision < 0.95:
            failures.append(f"Precision {self.precision:.2%} < 95% target")
        if self.recall < 0.95:
            failures.append(f"Recall {self.recall:.2%} < 95% target")
        if self.f1_score < 0.95:
            failures.append(f"F1 Score {self.f1_score:.2%} < 95% target")
        if self.avg_detection_latency > 100:
            failures.append(
                f"Avg latency {self.avg_detection_latency:.0f}ms > 100ms target"
            )

        return len(failures) == 0, failures


class PerformanceAnalyzer:
    """Analyzes performance impact of hallucination detection"""

    def __init__(self):
        self.baseline_latencies: List[float] = []
        self.wrapped_latencies: List[float] = []
        self.overhead_percentages: List[float] = []
        self.throughput_measurements: Dict[int, float] = {}  # load -> requests/sec

    async def measure_performance_impact(
        self,
        base_model: Any,
        wrapped_model: Any,
        test_queries: List[str],
        runs_per_query: int = 10,
    ) -> Dict[str, Any]:
        """Measure performance impact of TrustWrapper"""
        results = {
            "baseline_latencies": [],
            "wrapped_latencies": [],
            "overhead_percentages": [],
            "per_query_analysis": [],
        }

        for query in test_queries:
            query_baselines = []
            query_wrapped = []

            # Multiple runs per query for statistical significance
            for _ in range(runs_per_query):
                # Measure baseline
                start = time.time()
                if hasattr(base_model, "execute"):
                    _ = base_model.execute(query)
                else:
                    _ = await base_model.async_execute(query)
                baseline_time = (time.time() - start) * 1000  # Convert to ms
                query_baselines.append(baseline_time)

                # Measure wrapped
                start = time.time()
                _ = wrapped_model.verified_execute(query)
                wrapped_time = (time.time() - start) * 1000
                query_wrapped.append(wrapped_time)

            # Calculate statistics for this query
            avg_baseline = statistics.mean(query_baselines)
            avg_wrapped = statistics.mean(query_wrapped)
            overhead_pct = ((avg_wrapped - avg_baseline) / avg_baseline) * 100

            results["baseline_latencies"].extend(query_baselines)
            results["wrapped_latencies"].extend(query_wrapped)
            results["overhead_percentages"].append(overhead_pct)

            results["per_query_analysis"].append(
                {
                    "query": query[:50] + "..." if len(query) > 50 else query,
                    "avg_baseline_ms": avg_baseline,
                    "avg_wrapped_ms": avg_wrapped,
                    "overhead_pct": overhead_pct,
                    "std_dev_baseline": (
                        statistics.stdev(query_baselines)
                        if len(query_baselines) > 1
                        else 0
                    ),
                    "std_dev_wrapped": (
                        statistics.stdev(query_wrapped) if len(query_wrapped) > 1 else 0
                    ),
                }
            )

        # Store for later analysis
        self.baseline_latencies = results["baseline_latencies"]
        self.wrapped_latencies = results["wrapped_latencies"]
        self.overhead_percentages = results["overhead_percentages"]

        # Calculate overall statistics
        results["summary"] = {
            "avg_baseline_ms": statistics.mean(results["baseline_latencies"]),
            "avg_wrapped_ms": statistics.mean(results["wrapped_latencies"]),
            "avg_overhead_pct": statistics.mean(results["overhead_percentages"]),
            "p95_baseline_ms": np.percentile(results["baseline_latencies"], 95),
            "p95_wrapped_ms": np.percentile(results["wrapped_latencies"], 95),
            "max_overhead_pct": max(results["overhead_percentages"]),
        }

        return results

    async def test_scalability(
        self, wrapped_model: Any, test_queries: List[str], load_levels: List[int] = None
    ) -> Dict[str, Any]:
        """Test scalability with increasing load"""
        if load_levels is None:
            load_levels = [1, 10, 50, 100, 500]

        results = {"load_tests": [], "throughput_curve": {}}

        for load in load_levels:
            # Select queries for this load level
            queries = [test_queries[i % len(test_queries)] for i in range(load)]

            # Create concurrent tasks
            tasks = []
            for query in queries:
                task = wrapped_model.verified_execute(query)
                tasks.append(task)

            # Execute concurrently and measure
            start_time = time.time()
            if asyncio.iscoroutinefunction(wrapped_model.verified_execute):
                await asyncio.gather(*tasks)
            else:
                # For sync execution, we'll simulate with sequential calls
                for task in tasks:
                    task
            duration = time.time() - start_time

            throughput = load / duration
            self.throughput_measurements[load] = throughput

            results["load_tests"].append(
                {
                    "load": load,
                    "duration_s": duration,
                    "throughput_rps": throughput,
                    "avg_latency_ms": (duration / load) * 1000,
                }
            )
            results["throughput_curve"][load] = throughput

            print(f"Load {load}: {duration:.2f}s, {throughput:.2f} req/s")

        # Analyze scalability
        throughputs = [r["throughput_rps"] for r in results["load_tests"]]
        if len(throughputs) > 1:
            # Check if throughput scales sub-linearly (expected)
            scalability_factor = throughputs[-1] / throughputs[0]
            load_factor = load_levels[-1] / load_levels[0]
            results["scalability_efficiency"] = scalability_factor / load_factor

        return results

    def generate_performance_report(self) -> str:
        """Generate performance analysis report"""
        if not self.baseline_latencies or not self.wrapped_latencies:
            return "No performance data collected yet."

        report = f"""
Performance Impact Analysis
==========================

Baseline Performance:
- Average Latency: {statistics.mean(self.baseline_latencies):.2f}ms
- P95 Latency: {np.percentile(self.baseline_latencies, 95):.2f}ms
- Min/Max: {min(self.baseline_latencies):.2f}ms / {max(self.baseline_latencies):.2f}ms

With TrustWrapper:
- Average Latency: {statistics.mean(self.wrapped_latencies):.2f}ms
- P95 Latency: {np.percentile(self.wrapped_latencies, 95):.2f}ms
- Min/Max: {min(self.wrapped_latencies):.2f}ms / {max(self.wrapped_latencies):.2f}ms

Overhead Analysis:
- Average Overhead: {statistics.mean(self.overhead_percentages):.1f}%
- Max Overhead: {max(self.overhead_percentages):.1f}%
- Overhead Std Dev: {statistics.stdev(self.overhead_percentages):.1f}%

Throughput (if measured):
"""

        if self.throughput_measurements:
            for load, throughput in sorted(self.throughput_measurements.items()):
                report += f"- Load {load}: {throughput:.2f} requests/second\n"

        return report


class A_B_TestFramework:
    """Framework for A/B testing hallucination detection"""

    def __init__(self):
        self.control_metrics = HallucinationMetrics()  # Without TrustWrapper
        self.treatment_metrics = HallucinationMetrics()  # With TrustWrapper
        self.user_feedback = defaultdict(list)  # user_id -> feedback scores

    def assign_user_to_group(self, user_id: str) -> str:
        """Randomly assign user to control or treatment group"""
        # Use hash for consistent assignment
        return "treatment" if hash(user_id) % 2 == 0 else "control"

    def record_interaction(
        self,
        user_id: str,
        query: str,
        response: str,
        hallucination_detected: bool,
        user_satisfaction: Optional[float] = None,
    ):
        """Record user interaction and feedback"""
        group = self.assign_user_to_group(user_id)

        if user_satisfaction is not None:
            self.user_feedback[group].append(user_satisfaction)

        # Update appropriate metrics based on group
        metrics = (
            self.treatment_metrics if group == "treatment" else self.control_metrics
        )
        # This would need actual hallucination ground truth in production
        # For now, we'll simulate based on detection
        metrics.update_detection(
            predicted_hallucination=hallucination_detected,
            actual_hallucination=hallucination_detected,  # Simulated
            latency_ms=100,  # Would measure actual
            trust_score=0.8 if not hallucination_detected else 0.3,
            proof_time_ms=50,
        )

    def calculate_statistical_significance(self) -> Dict[str, Any]:
        """Calculate statistical significance of results"""
        control_satisfaction = self.user_feedback.get("control", [])
        treatment_satisfaction = self.user_feedback.get("treatment", [])

        if not control_satisfaction or not treatment_satisfaction:
            return {"significant": False, "message": "Insufficient data"}

        # Simple t-test simulation (would use scipy.stats in production)
        control_mean = statistics.mean(control_satisfaction)
        treatment_mean = statistics.mean(treatment_satisfaction)

        # Simplified significance test
        improvement = (treatment_mean - control_mean) / control_mean * 100
        sample_size = min(len(control_satisfaction), len(treatment_satisfaction))

        # Rule of thumb: 5% improvement with 100+ samples
        significant = improvement > 5 and sample_size > 100

        return {
            "significant": significant,
            "control_mean": control_mean,
            "treatment_mean": treatment_mean,
            "improvement_pct": improvement,
            "sample_size": sample_size,
            "control_metrics": self.control_metrics.get_summary(),
            "treatment_metrics": self.treatment_metrics.get_summary(),
        }

"""
TrustWrapper LangChain Monitoring

Real-time monitoring and metrics collection for TrustWrapper LangChain integration.
"""

import asyncio
import json
import time
from collections import deque
from datetime import datetime
from threading import Lock
from typing import Any, Dict, List

from .langchain_config import TrustWrapperConfig


class MetricWindow:
    """Time-windowed metric tracking"""

    def __init__(self, window_size: int = 300):  # 5 minutes default
        self.window_size = window_size
        self.data: deque = deque()
        self.lock = Lock()

    def add(self, value: float) -> None:
        """Add a value with current timestamp"""
        with self.lock:
            now = time.time()
            self.data.append((now, value))
            self._cleanup()

    def _cleanup(self) -> None:
        """Remove old entries outside the window"""
        cutoff = time.time() - self.window_size
        while self.data and self.data[0][0] < cutoff:
            self.data.popleft()

    def get_stats(self) -> Dict[str, float]:
        """Get statistics for the window"""
        with self.lock:
            self._cleanup()
            if not self.data:
                return {"count": 0, "sum": 0, "avg": 0, "min": 0, "max": 0}

            values = [v for _, v in self.data]
            return {
                "count": len(values),
                "sum": sum(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
            }


class TrustWrapperMonitor:
    """
    Real-time monitoring for TrustWrapper LangChain integration.

    Tracks:
    - Verification latency
    - Success/failure rates
    - Hallucination detection rates
    - Compliance violations
    - System health metrics
    """

    def __init__(self, config: TrustWrapperConfig):
        self.config = config
        self.start_time = time.time()

        # Metric windows (5-minute rolling windows)
        self.latency_window = MetricWindow(300)
        self.success_window = MetricWindow(300)
        self.hallucination_window = MetricWindow(300)
        self.compliance_window = MetricWindow(300)

        # Cumulative counters
        self.counters = {
            "total_verifications": 0,
            "llm_verifications": 0,
            "tool_verifications": 0,
            "agent_verifications": 0,
            "cache_hits": 0,
            "errors": 0,
            "warnings": 0,
        }

        # Alert thresholds
        self.alert_thresholds = {
            "latency_ms": 200,  # Alert if avg latency > 200ms
            "failure_rate": 0.1,  # Alert if failure rate > 10%
            "hallucination_rate": 0.05,  # Alert if hallucination rate > 5%
            "error_rate": 0.01,  # Alert if error rate > 1%
        }

        # Alert history
        self.alerts: List[Dict[str, Any]] = []

        # Start monitoring task if enabled
        if config.enable_monitoring:
            try:
                loop = asyncio.get_running_loop()
                asyncio.create_task(self._monitoring_loop())
            except RuntimeError:
                # No event loop, monitoring will be manual
                pass

    async def log_verification(
        self, verification_type: str, content: str, result: Any, latency_ms: float
    ) -> None:
        """Log a verification event"""
        # Update counters
        self.counters["total_verifications"] += 1
        self.counters[f"{verification_type}_verifications"] = (
            self.counters.get(f"{verification_type}_verifications", 0) + 1
        )

        # Track metrics
        self.latency_window.add(latency_ms)
        self.success_window.add(1.0 if result.passed else 0.0)

        # Track specific issues
        if any("hallucination" in issue.lower() for issue in result.issues):
            self.hallucination_window.add(1.0)
        else:
            self.hallucination_window.add(0.0)

        if any("compliance" in issue.lower() for issue in result.issues):
            self.compliance_window.add(1.0)
        else:
            self.compliance_window.add(0.0)

        # Check for alerts
        await self._check_alerts()

    async def log_cache_hit(self) -> None:
        """Log a cache hit"""
        self.counters["cache_hits"] += 1

    async def log_error(self, error: Exception) -> None:
        """Log an error"""
        self.counters["errors"] += 1
        await self._create_alert(
            "error",
            f"Error occurred: {type(error).__name__}: {str(error)}",
            {"error_type": type(error).__name__},
        )

    async def log_warning(self, message: str) -> None:
        """Log a warning"""
        self.counters["warnings"] += 1

    async def _monitoring_loop(self) -> None:
        """Background monitoring loop"""
        while True:
            try:
                # Send metrics to monitoring endpoint if configured
                if self.config.monitoring_endpoint:
                    metrics = self.get_metrics()
                    await self._send_metrics(metrics)

                # Sleep until next interval
                await asyncio.sleep(self.config.metrics_interval)

            except Exception as e:
                # Log but don't crash the monitoring loop
                print(f"Monitoring error: {e}")
                await asyncio.sleep(self.config.metrics_interval)

    async def _send_metrics(self, metrics: Dict[str, Any]) -> None:
        """Send metrics to monitoring endpoint"""
        # In production, this would POST to the monitoring endpoint
        # For now, just log
        if self.config.enable_monitoring:
            print(f"[Monitor] Metrics: {json.dumps(metrics, indent=2)}")

    async def _check_alerts(self) -> None:
        """Check if any metrics exceed alert thresholds"""
        latency_stats = self.latency_window.get_stats()
        success_stats = self.success_window.get_stats()
        hallucination_stats = self.hallucination_window.get_stats()

        # Check latency
        if latency_stats["avg"] > self.alert_thresholds["latency_ms"]:
            await self._create_alert(
                "high_latency",
                f"Average latency {latency_stats['avg']:.1f}ms exceeds threshold",
                latency_stats,
            )

        # Check failure rate
        if success_stats["count"] > 0:
            failure_rate = 1.0 - success_stats["avg"]
            if failure_rate > self.alert_thresholds["failure_rate"]:
                await self._create_alert(
                    "high_failure_rate",
                    f"Failure rate {failure_rate:.1%} exceeds threshold",
                    {"failure_rate": failure_rate},
                )

        # Check hallucination rate
        if hallucination_stats["count"] > 0:
            hallucination_rate = hallucination_stats["avg"]
            if hallucination_rate > self.alert_thresholds["hallucination_rate"]:
                await self._create_alert(
                    "high_hallucination_rate",
                    f"Hallucination rate {hallucination_rate:.1%} exceeds threshold",
                    {"hallucination_rate": hallucination_rate},
                )

    async def _create_alert(
        self, alert_type: str, message: str, data: Dict[str, Any]
    ) -> None:
        """Create an alert"""
        alert = {
            "type": alert_type,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "severity": self._get_alert_severity(alert_type),
        }

        self.alerts.append(alert)

        # In production, send alert to notification system
        print(f"[ALERT] {alert['severity']}: {message}")

    def _get_alert_severity(self, alert_type: str) -> str:
        """Determine alert severity"""
        severity_map = {
            "error": "critical",
            "high_failure_rate": "high",
            "high_hallucination_rate": "high",
            "high_latency": "medium",
            "compliance_violation": "high",
        }
        return severity_map.get(alert_type, "low")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot"""
        uptime_seconds = time.time() - self.start_time

        # Get window statistics
        latency_stats = self.latency_window.get_stats()
        success_stats = self.success_window.get_stats()
        hallucination_stats = self.hallucination_window.get_stats()
        compliance_stats = self.compliance_window.get_stats()

        # Calculate rates
        total_verifications = self.counters["total_verifications"]
        cache_hit_rate = self.counters["cache_hits"] / max(1, total_verifications)

        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": uptime_seconds,
            "counters": self.counters.copy(),
            "rates": {
                "verifications_per_minute": (
                    total_verifications / max(1, uptime_seconds)
                )
                * 60,
                "cache_hit_rate": cache_hit_rate,
                "success_rate": (
                    success_stats["avg"] if success_stats["count"] > 0 else 1.0
                ),
                "hallucination_rate": (
                    hallucination_stats["avg"]
                    if hallucination_stats["count"] > 0
                    else 0.0
                ),
                "compliance_violation_rate": (
                    compliance_stats["avg"] if compliance_stats["count"] > 0 else 0.0
                ),
            },
            "latency": {
                "avg_ms": latency_stats["avg"],
                "min_ms": latency_stats["min"],
                "max_ms": latency_stats["max"],
                "samples": latency_stats["count"],
            },
            "alerts": {
                "total": len(self.alerts),
                "recent": self.alerts[-10:],  # Last 10 alerts
            },
        }

        return metrics

    def get_health_status(self) -> Dict[str, Any]:
        """Get system health status"""
        metrics = self.get_metrics()

        # Determine health based on metrics
        health_score = 100.0
        issues = []

        # Check latency
        if metrics["latency"]["avg_ms"] > self.alert_thresholds["latency_ms"]:
            health_score -= 20
            issues.append("High latency detected")

        # Check success rate
        success_rate = metrics["rates"]["success_rate"]
        if success_rate < 0.9:
            health_score -= 30
            issues.append(f"Low success rate: {success_rate:.1%}")

        # Check error rate
        error_rate = self.counters["errors"] / max(
            1, self.counters["total_verifications"]
        )
        if error_rate > self.alert_thresholds["error_rate"]:
            health_score -= 25
            issues.append(f"High error rate: {error_rate:.1%}")

        # Determine status
        if health_score >= 90:
            status = "healthy"
        elif health_score >= 70:
            status = "degraded"
        else:
            status = "unhealthy"

        return {
            "status": status,
            "score": max(0, health_score),
            "issues": issues,
            "metrics_summary": {
                "uptime": f"{metrics['uptime_seconds'] / 3600:.1f} hours",
                "total_verifications": metrics["counters"]["total_verifications"],
                "success_rate": f"{success_rate:.1%}",
                "avg_latency": f"{metrics['latency']['avg_ms']:.1f}ms",
            },
        }

    def reset_alerts(self) -> None:
        """Clear alert history"""
        self.alerts.clear()

    def update_thresholds(self, thresholds: Dict[str, float]) -> None:
        """Update alert thresholds"""
        self.alert_thresholds.update(thresholds)

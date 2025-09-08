"""
Bridge Health Monitoring System
===============================

Real-time health monitoring, alerting, and recovery capabilities
for TrustWrapper v3.0 cross-chain bridge infrastructure.
"""

import asyncio
import logging
import time
from collections.abc import Callable
from dataclasses import asdict
from datetime import datetime
from enum import Enum

from bridge.interfaces import (
    BridgeMetrics,
    BridgeRoute,
    IBridgeAdapter,
    IBridgeHealthMonitor,
)
from core.interfaces import ChainType


class AlertSeverity(Enum):
    """Alert severity levels."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of bridge alerts."""

    ROUTE_DOWN = "route_down"
    HIGH_LATENCY = "high_latency"
    LOW_THROUGHPUT = "low_throughput"
    HIGH_ERROR_RATE = "high_error_rate"
    ADAPTER_FAILURE = "adapter_failure"
    CONSENSUS_TIMEOUT = "consensus_timeout"
    MESSAGE_BACKLOG = "message_backlog"
    BYZANTINE_FAULT = "byzantine_fault"


class HealthThresholds:
    """Health monitoring thresholds."""

    def __init__(self):
        # Latency thresholds (milliseconds)
        self.latency_warning = 1000  # 1 second
        self.latency_critical = 5000  # 5 seconds

        # Throughput thresholds (messages per second)
        self.throughput_warning = 10
        self.throughput_critical = 1

        # Error rate thresholds (percentage)
        self.error_rate_warning = 0.05  # 5%
        self.error_rate_critical = 0.15  # 15%

        # Uptime thresholds (percentage)
        self.uptime_warning = 0.95  # 95%
        self.uptime_critical = 0.90  # 90%

        # Health score thresholds
        self.health_score_warning = 0.80
        self.health_score_critical = 0.60


class BridgeAlert:
    """Bridge monitoring alert."""

    def __init__(
        self,
        alert_id: str,
        alert_type: AlertType,
        severity: AlertSeverity,
        message: str,
        route_id: str | None = None,
        chain_type: ChainType | None = None,
        metadata: dict[str, any] | None = None,
    ):
        self.alert_id = alert_id
        self.alert_type = alert_type
        self.severity = severity
        self.message = message
        self.route_id = route_id
        self.chain_type = chain_type
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()
        self.acknowledged = False
        self.resolved = False


class RouteHealthTracker:
    """Tracks health metrics for a specific bridge route."""

    def __init__(self, route: BridgeRoute, window_size: int = 100):
        self.route = route
        self.window_size = window_size

        # Rolling windows for metrics
        self.latency_samples = []
        self.throughput_samples = []
        self.error_samples = []
        self.success_count = 0
        self.failure_count = 0

        # Current metrics
        self.current_metrics = BridgeMetrics(
            route_id=f"{route.source_chain.value}_{route.target_chain.value}",
            total_messages=0,
            successful_messages=0,
            failed_messages=0,
            average_latency_ms=0.0,
            throughput_msg_per_sec=0.0,
            error_rate=0.0,
            uptime_percentage=100.0,
            last_message_timestamp=None,
            health_score=1.0,
        )

        self.last_update = datetime.utcnow()
        self.downtime_start = None

    def record_message(self, latency_ms: float, success: bool) -> None:
        """
        Record a message transmission.

        Args:
            latency_ms: Message latency in milliseconds
            success: Whether transmission was successful
        """
        timestamp = time.time()

        # Update rolling windows
        self.latency_samples.append((timestamp, latency_ms))
        if len(self.latency_samples) > self.window_size:
            self.latency_samples.pop(0)

        # Update counters
        self.current_metrics.total_messages += 1
        if success:
            self.success_count += 1
            self.current_metrics.successful_messages += 1
        else:
            self.failure_count += 1
            self.current_metrics.failed_messages += 1

        # Update current metrics
        self._update_metrics()

        self.current_metrics.last_message_timestamp = datetime.utcnow()
        self.last_update = datetime.utcnow()

    def record_throughput(self, messages_per_second: float) -> None:
        """
        Record throughput measurement.

        Args:
            messages_per_second: Measured throughput
        """
        timestamp = time.time()
        self.throughput_samples.append((timestamp, messages_per_second))
        if len(self.throughput_samples) > self.window_size:
            self.throughput_samples.pop(0)

        self._update_metrics()

    def mark_route_down(self) -> None:
        """Mark the route as down."""
        if self.downtime_start is None:
            self.downtime_start = datetime.utcnow()

        self.route.is_active = False
        self.route.health_score = 0.0
        self._update_metrics()

    def mark_route_up(self) -> None:
        """Mark the route as up."""
        self.downtime_start = None
        self.route.is_active = True
        self._update_metrics()

    def _update_metrics(self) -> None:
        """Update calculated metrics."""
        now = time.time()
        window_start = now - 60  # 1-minute window

        # Calculate average latency
        recent_latencies = [
            latency
            for timestamp, latency in self.latency_samples
            if timestamp > window_start
        ]

        if recent_latencies:
            self.current_metrics.average_latency_ms = sum(recent_latencies) / len(
                recent_latencies
            )

        # Calculate throughput
        recent_throughput = [
            tps
            for timestamp, tps in self.throughput_samples
            if timestamp > window_start
        ]

        if recent_throughput:
            self.current_metrics.throughput_msg_per_sec = sum(recent_throughput) / len(
                recent_throughput
            )

        # Calculate error rate
        total = self.success_count + self.failure_count
        if total > 0:
            self.current_metrics.error_rate = self.failure_count / total

        # Calculate uptime percentage
        if self.downtime_start:
            total_time = (datetime.utcnow() - self.last_update).total_seconds()
            downtime = (datetime.utcnow() - self.downtime_start).total_seconds()
            self.current_metrics.uptime_percentage = max(
                0.0, (total_time - downtime) / total_time
            )
        else:
            self.current_metrics.uptime_percentage = 1.0

        # Calculate health score
        self._calculate_health_score()

    def _calculate_health_score(self) -> None:
        """Calculate overall health score."""
        score = 1.0

        # Latency factor
        if self.current_metrics.average_latency_ms > 5000:  # 5 seconds
            score *= 0.5
        elif self.current_metrics.average_latency_ms > 1000:  # 1 second
            score *= 0.8

        # Error rate factor
        if self.current_metrics.error_rate > 0.15:  # 15%
            score *= 0.3
        elif self.current_metrics.error_rate > 0.05:  # 5%
            score *= 0.7

        # Uptime factor
        score *= self.current_metrics.uptime_percentage

        # Route active factor
        if not self.route.is_active:
            score = 0.0

        self.route.health_score = score
        self.current_metrics.health_score = score


class BridgeHealthMonitor(IBridgeHealthMonitor):
    """
    Bridge health monitoring system for TrustWrapper v3.0.

    Provides real-time monitoring, alerting, and recovery capabilities
    for cross-chain bridge infrastructure.
    """

    def __init__(self):
        self.thresholds = HealthThresholds()
        self.route_trackers: dict[str, RouteHealthTracker] = {}
        self.adapters: dict[ChainType, IBridgeAdapter] = {}
        self.alert_callbacks: dict[str, list[Callable]] = {}
        self.active_alerts: dict[str, BridgeAlert] = {}

        # Configuration
        self.health_check_interval = 30  # 30 seconds
        self.alert_check_interval = 10  # 10 seconds
        self.metrics_retention_hours = 24

        # State tracking
        self._running = False
        self._health_check_task = None
        self._alert_check_task = None

        self.logger = logging.getLogger(f"{__name__}.monitor")

        # Statistics
        self._stats = {
            "total_alerts": 0,
            "critical_alerts": 0,
            "routes_monitored": 0,
            "average_health_score": 0.0,
            "uptime_percentage": 100.0,
        }

    async def start_monitoring(self) -> None:
        """Start the bridge health monitoring system."""
        if self._running:
            return

        self._running = True

        # Start background tasks
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        self._alert_check_task = asyncio.create_task(self._alert_check_loop())

        self.logger.info("Started bridge health monitoring system")

    async def stop_monitoring(self) -> None:
        """Stop the bridge health monitoring system."""
        if not self._running:
            return

        self._running = False

        # Cancel background tasks
        if self._health_check_task:
            self._health_check_task.cancel()

        if self._alert_check_task:
            self._alert_check_task.cancel()

        # Wait for tasks to complete
        await asyncio.gather(
            self._health_check_task, self._alert_check_task, return_exceptions=True
        )

        self.logger.info("Stopped bridge health monitoring system")

    async def register_bridge_route(self, route: BridgeRoute) -> None:
        """
        Register a bridge route for monitoring.

        Args:
            route: Bridge route to monitor
        """
        route_id = f"{route.source_chain.value}_{route.target_chain.value}"
        self.route_trackers[route_id] = RouteHealthTracker(route)

        self._stats["routes_monitored"] = len(self.route_trackers)

        self.logger.info(f"Registered bridge route for monitoring: {route_id}")

    def register_adapter(self, chain_type: ChainType, adapter: IBridgeAdapter) -> None:
        """
        Register a bridge adapter for monitoring.

        Args:
            chain_type: Blockchain type
            adapter: Bridge adapter
        """
        self.adapters[chain_type] = adapter
        self.logger.info(f"Registered adapter for monitoring: {chain_type.value}")

    async def perform_health_check(
        self, source_chain: ChainType, target_chain: ChainType
    ) -> BridgeMetrics:
        """
        Perform health check for a specific bridge route.

        Args:
            source_chain: Source blockchain
            target_chain: Target blockchain

        Returns:
            BridgeMetrics: Health metrics
        """
        route_id = f"{source_chain.value}_{target_chain.value}"

        if route_id not in self.route_trackers:
            raise ValueError(f"Route {route_id} not registered for monitoring")

        tracker = self.route_trackers[route_id]

        # Perform basic connectivity check
        source_adapter = self.adapters.get(source_chain)
        target_adapter = self.adapters.get(target_chain)

        if source_adapter and target_adapter:
            source_operational = source_adapter.is_operational
            target_operational = target_adapter.is_operational

            if source_operational and target_operational:
                tracker.mark_route_up()
            else:
                tracker.mark_route_down()

                # Generate alert if route is down
                await self._generate_alert(
                    AlertType.ROUTE_DOWN,
                    AlertSeverity.CRITICAL,
                    f"Route {route_id} is down - adapter unavailable",
                    route_id=route_id,
                )

        return tracker.current_metrics

    async def get_all_bridge_health(self) -> dict[str, BridgeMetrics]:
        """
        Get health metrics for all monitored bridge routes.

        Returns:
            Dict[str, BridgeMetrics]: Route ID to metrics mapping
        """
        health_metrics = {}

        for route_id, tracker in self.route_trackers.items():
            health_metrics[route_id] = tracker.current_metrics

        # Update overall statistics
        if self.route_trackers:
            total_health = sum(
                tracker.current_metrics.health_score
                for tracker in self.route_trackers.values()
            )
            self._stats["average_health_score"] = total_health / len(
                self.route_trackers
            )

            total_uptime = sum(
                tracker.current_metrics.uptime_percentage
                for tracker in self.route_trackers.values()
            )
            self._stats["uptime_percentage"] = (
                total_uptime / len(self.route_trackers) * 100
            )

        return health_metrics

    def register_alert_callback(
        self, alert_type: str, callback: Callable[[str, dict[str, any]], None]
    ) -> None:
        """
        Register a callback for bridge alerts.

        Args:
            alert_type: Type of alert to monitor
            callback: Function to call when alert triggers
        """
        if alert_type not in self.alert_callbacks:
            self.alert_callbacks[alert_type] = []

        self.alert_callbacks[alert_type].append(callback)
        self.logger.info(f"Registered alert callback for {alert_type}")

    async def record_message_transmission(
        self,
        source_chain: ChainType,
        target_chain: ChainType,
        latency_ms: float,
        success: bool,
    ) -> None:
        """
        Record a message transmission for monitoring.

        Args:
            source_chain: Source blockchain
            target_chain: Target blockchain
            latency_ms: Transmission latency
            success: Whether transmission was successful
        """
        route_id = f"{source_chain.value}_{target_chain.value}"

        if route_id in self.route_trackers:
            self.route_trackers[route_id].record_message(latency_ms, success)

            # Check for alerts
            await self._check_route_alerts(route_id)

    async def get_monitoring_stats(self) -> dict[str, any]:
        """
        Get monitoring system statistics.

        Returns:
            Dict: Monitoring statistics
        """
        return {
            **self._stats,
            "active_alerts": len(self.active_alerts),
            "critical_alerts": len(
                [
                    alert
                    for alert in self.active_alerts.values()
                    if alert.severity == AlertSeverity.CRITICAL
                ]
            ),
        }

    async def _health_check_loop(self) -> None:
        """Background task for performing health checks."""
        self.logger.info("Started bridge health check loop")

        while self._running:
            try:
                # Perform health checks for all routes
                for route_id, tracker in self.route_trackers.items():
                    source_chain, target_chain = route_id.split("_")
                    source_chain = ChainType(source_chain)
                    target_chain = ChainType(target_chain)

                    await self.perform_health_check(source_chain, target_chain)

                await asyncio.sleep(self.health_check_interval)

            except Exception as e:
                self.logger.error(f"Error in health check loop: {e}")
                await asyncio.sleep(5)

        self.logger.info("Stopped bridge health check loop")

    async def _alert_check_loop(self) -> None:
        """Background task for checking alert conditions."""
        self.logger.info("Started bridge alert check loop")

        while self._running:
            try:
                # Check each route for alert conditions
                for route_id in self.route_trackers:
                    await self._check_route_alerts(route_id)

                await asyncio.sleep(self.alert_check_interval)

            except Exception as e:
                self.logger.error(f"Error in alert check loop: {e}")
                await asyncio.sleep(5)

        self.logger.info("Stopped bridge alert check loop")

    async def _check_route_alerts(self, route_id: str) -> None:
        """
        Check for alert conditions on a specific route.

        Args:
            route_id: Route identifier
        """
        tracker = self.route_trackers[route_id]
        metrics = tracker.current_metrics

        # Check latency alerts
        if metrics.average_latency_ms > self.thresholds.latency_critical:
            await self._generate_alert(
                AlertType.HIGH_LATENCY,
                AlertSeverity.CRITICAL,
                f"Route {route_id} latency critical: {metrics.average_latency_ms:.1f}ms",
                route_id=route_id,
                metadata={"latency_ms": metrics.average_latency_ms},
            )
        elif metrics.average_latency_ms > self.thresholds.latency_warning:
            await self._generate_alert(
                AlertType.HIGH_LATENCY,
                AlertSeverity.WARNING,
                f"Route {route_id} latency high: {metrics.average_latency_ms:.1f}ms",
                route_id=route_id,
                metadata={"latency_ms": metrics.average_latency_ms},
            )

        # Check throughput alerts
        if metrics.throughput_msg_per_sec < self.thresholds.throughput_critical:
            await self._generate_alert(
                AlertType.LOW_THROUGHPUT,
                AlertSeverity.CRITICAL,
                f"Route {route_id} throughput critical: {metrics.throughput_msg_per_sec:.1f} msg/s",
                route_id=route_id,
                metadata={"throughput": metrics.throughput_msg_per_sec},
            )
        elif metrics.throughput_msg_per_sec < self.thresholds.throughput_warning:
            await self._generate_alert(
                AlertType.LOW_THROUGHPUT,
                AlertSeverity.WARNING,
                f"Route {route_id} throughput low: {metrics.throughput_msg_per_sec:.1f} msg/s",
                route_id=route_id,
                metadata={"throughput": metrics.throughput_msg_per_sec},
            )

        # Check error rate alerts
        if metrics.error_rate > self.thresholds.error_rate_critical:
            await self._generate_alert(
                AlertType.HIGH_ERROR_RATE,
                AlertSeverity.CRITICAL,
                f"Route {route_id} error rate critical: {metrics.error_rate:.1%}",
                route_id=route_id,
                metadata={"error_rate": metrics.error_rate},
            )
        elif metrics.error_rate > self.thresholds.error_rate_warning:
            await self._generate_alert(
                AlertType.HIGH_ERROR_RATE,
                AlertSeverity.WARNING,
                f"Route {route_id} error rate high: {metrics.error_rate:.1%}",
                route_id=route_id,
                metadata={"error_rate": metrics.error_rate},
            )

        # Check health score alerts
        if metrics.health_score < self.thresholds.health_score_critical:
            await self._generate_alert(
                AlertType.ROUTE_DOWN,
                AlertSeverity.CRITICAL,
                f"Route {route_id} health critical: {metrics.health_score:.3f}",
                route_id=route_id,
                metadata={"health_score": metrics.health_score},
            )
        elif metrics.health_score < self.thresholds.health_score_warning:
            await self._generate_alert(
                AlertType.ROUTE_DOWN,
                AlertSeverity.WARNING,
                f"Route {route_id} health degraded: {metrics.health_score:.3f}",
                route_id=route_id,
                metadata={"health_score": metrics.health_score},
            )

    async def _generate_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        message: str,
        route_id: str | None = None,
        chain_type: ChainType | None = None,
        metadata: dict[str, any] | None = None,
    ) -> None:
        """
        Generate and process a bridge alert.

        Args:
            alert_type: Type of alert
            severity: Alert severity
            message: Alert message
            route_id: Route identifier
            chain_type: Chain type
            metadata: Additional metadata
        """
        alert_id = f"{alert_type.value}_{route_id or chain_type or 'global'}_{int(time.time())}"

        alert = BridgeAlert(
            alert_id=alert_id,
            alert_type=alert_type,
            severity=severity,
            message=message,
            route_id=route_id,
            chain_type=chain_type,
            metadata=metadata,
        )

        self.active_alerts[alert_id] = alert
        self._stats["total_alerts"] += 1

        if severity == AlertSeverity.CRITICAL:
            self._stats["critical_alerts"] += 1

        # Call registered callbacks
        alert_type_str = alert_type.value
        if alert_type_str in self.alert_callbacks:
            for callback in self.alert_callbacks[alert_type_str]:
                try:
                    callback(alert_id, asdict(alert))
                except Exception as e:
                    self.logger.error(f"Error calling alert callback: {e}")

        self.logger.log(
            logging.CRITICAL if severity == AlertSeverity.CRITICAL else logging.WARNING,
            f"Bridge alert: {message}",
        )

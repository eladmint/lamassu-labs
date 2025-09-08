"""
Cross-Chain Bridge Implementation
=================================

Main cross-chain bridge system for TrustWrapper v3.0.
Coordinates message passing, consensus, and monitoring across
multiple blockchain networks.
"""

import logging
import uuid
from datetime import datetime

from bridge.consensus_engine import CrossChainConsensusEngine
from bridge.health_monitor import BridgeHealthMonitor
from bridge.interfaces import (
    BridgeMessage,
    BridgeRoute,
    ConsensusVote,
    IBridgeAdapter,
    IBridgeHealthMonitor,
    ICrossChainBridge,
    ICrossChainConsensus,
)
from bridge.message_broker import CrossChainMessageBroker
from core.interfaces import ChainType


class CrossChainBridge(ICrossChainBridge):
    """
    Main cross-chain bridge system for TrustWrapper v3.0.

    Coordinates all cross-chain operations including message passing,
    consensus mechanisms, and health monitoring across multiple
    blockchain networks.
    """

    def __init__(self):
        self.message_broker = CrossChainMessageBroker()
        self.consensus_engine = CrossChainConsensusEngine()
        self.health_monitor = BridgeHealthMonitor()

        self.adapters: dict[ChainType, IBridgeAdapter] = {}
        self.routes: list[BridgeRoute] = []
        self.supported_chains_list: list[ChainType] = []

        # Configuration
        self.max_concurrent_consensus = 50
        self.consensus_timeout_seconds = 120
        self.bridge_timeout_seconds = 300

        # State tracking
        self._initialized = False
        self._running = False
        self.active_consensus_processes: set[str] = set()

        self.logger = logging.getLogger(f"{__name__}.bridge")

        # Statistics
        self._stats = {
            "total_messages": 0,
            "successful_messages": 0,
            "failed_messages": 0,
            "consensus_processes": 0,
            "successful_consensus": 0,
            "bridge_uptime_seconds": 0,
        }

        self._start_time = None

    @property
    def supported_chains(self) -> list[ChainType]:
        """Return list of supported blockchain types."""
        return self.supported_chains_list.copy()

    @property
    def active_routes(self) -> list[BridgeRoute]:
        """Return list of active bridge routes."""
        return [route for route in self.routes if route.is_active]

    async def initialize(
        self,
        adapters: dict[ChainType, IBridgeAdapter],
        consensus_engine: ICrossChainConsensus | None = None,
        health_monitor: IBridgeHealthMonitor | None = None,
    ) -> bool:
        """
        Initialize the cross-chain bridge system.

        Args:
            adapters: Chain-specific bridge adapters
            consensus_engine: Consensus mechanism (optional, uses default if None)
            health_monitor: Health monitoring system (optional, uses default if None)

        Returns:
            bool: True if initialization successful
        """
        try:
            self.adapters = adapters
            self.supported_chains_list = list(adapters.keys())

            # Use custom engines if provided
            if consensus_engine:
                self.consensus_engine = consensus_engine
            if health_monitor:
                self.health_monitor = health_monitor

            # Initialize adapters
            for chain_type, adapter in adapters.items():
                if not adapter.is_operational:
                    self.logger.warning(
                        f"Adapter for {chain_type.value} is not operational"
                    )

                # Register adapter with health monitor
                self.health_monitor.register_adapter(chain_type, adapter)

            # Create bridge routes for all chain pairs
            self.routes = self._create_bridge_routes()

            # Initialize message broker
            await self.message_broker.initialize(adapters, self.routes)

            # Register routes with health monitor
            for route in self.routes:
                await self.health_monitor.register_bridge_route(route)

            # Register alert callbacks
            self._register_alert_callbacks()

            self._initialized = True
            self.logger.info(
                f"Initialized cross-chain bridge with {len(adapters)} adapters "
                f"and {len(self.routes)} routes"
            )

            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize cross-chain bridge: {e}")
            return False

    async def start(self) -> None:
        """Start the cross-chain bridge system."""
        if not self._initialized:
            raise RuntimeError("Bridge not initialized. Call initialize() first.")

        if self._running:
            return

        self._running = True
        self._start_time = datetime.utcnow()

        # Start all subsystems
        await self.message_broker.start()
        await self.consensus_engine.start()
        await self.health_monitor.start_monitoring()

        self.logger.info("Started cross-chain bridge system")

    async def stop(self) -> None:
        """Stop the cross-chain bridge system."""
        if not self._running:
            return

        self._running = False

        # Stop all subsystems
        await self.message_broker.stop()
        await self.consensus_engine.stop()
        await self.health_monitor.stop_monitoring()

        # Update uptime stats
        if self._start_time:
            uptime = (datetime.utcnow() - self._start_time).total_seconds()
            self._stats["bridge_uptime_seconds"] += uptime

        self.logger.info("Stopped cross-chain bridge system")

    async def send_message(self, message: BridgeMessage) -> str:
        """
        Send a message across chains.

        Args:
            message: Message to send

        Returns:
            str: Message tracking identifier
        """
        if not self._running:
            raise RuntimeError("Bridge not running. Call start() first.")

        # Validate message
        if not self._validate_message(message):
            raise ValueError("Invalid bridge message")

        # Send through message broker
        message_id = await self.message_broker.send_message(
            message.message_type,
            message.source_chain,
            message.target_chain,
            message.payload,
            message.priority,
            message.timeout_seconds,
        )

        self._stats["total_messages"] += 1

        self.logger.info(
            f"Sent message {message_id} from {message.source_chain.value} "
            f"to {message.target_chain.value}"
        )

        return message_id

    async def process_pending_messages(self) -> int:
        """
        Process all pending cross-chain messages.

        Returns:
            int: Number of messages processed
        """
        if not self._running:
            return 0

        # The message broker handles processing automatically
        # This method is for manual processing if needed

        stats = await self.message_broker.get_broker_stats()
        return stats.get("processing_messages", 0)

    async def initiate_cross_chain_consensus(
        self,
        verification_request_id: str,
        participating_chains: list[ChainType],
        consensus_config: dict[str, any],
    ) -> str:
        """
        Initiate consensus process across multiple chains.

        Args:
            verification_request_id: Request requiring consensus
            participating_chains: Chains to participate
            consensus_config: Consensus configuration

        Returns:
            str: Consensus process identifier
        """
        if not self._running:
            raise RuntimeError("Bridge not running. Call start() first.")

        if len(self.active_consensus_processes) >= self.max_concurrent_consensus:
            raise RuntimeError("Maximum concurrent consensus processes reached")

        # Validate participating chains
        invalid_chains = [
            chain
            for chain in participating_chains
            if chain not in self.supported_chains
        ]
        if invalid_chains:
            raise ValueError(f"Unsupported chains: {[c.value for c in invalid_chains]}")

        # Initialize consensus
        consensus_id = await self.consensus_engine.initialize_consensus(
            verification_request_id, participating_chains, consensus_config
        )

        self.active_consensus_processes.add(consensus_id)
        self._stats["consensus_processes"] += 1

        self.logger.info(
            f"Initiated cross-chain consensus {consensus_id} "
            f"with {len(participating_chains)} participants"
        )

        return consensus_id

    async def submit_consensus_vote(
        self,
        consensus_id: str,
        voter_chain: ChainType,
        vote_value: any,
        confidence_score: float,
        weight: float = 1.0,
    ) -> bool:
        """
        Submit a vote to a consensus process.

        Args:
            consensus_id: Consensus process identifier
            voter_chain: Chain submitting the vote
            vote_value: Vote value
            confidence_score: Confidence in the vote
            weight: Vote weight

        Returns:
            bool: True if vote was accepted
        """
        if consensus_id not in self.active_consensus_processes:
            return False

        vote = ConsensusVote(
            vote_id=str(uuid.uuid4()),
            message_id=consensus_id,
            voter_chain=voter_chain,
            vote_value=vote_value,
            confidence_score=confidence_score,
            weight=weight,
            timestamp=datetime.utcnow(),
        )

        success = await self.consensus_engine.submit_vote(consensus_id, vote)

        if success:
            self.logger.debug(
                f"Submitted vote from {voter_chain.value} to consensus {consensus_id}"
            )

        return success

    async def get_consensus_result(self, consensus_id: str) -> any | None:
        """
        Get the result of a consensus process.

        Args:
            consensus_id: Consensus process identifier

        Returns:
            Consensus result if complete, None if ongoing
        """
        result = await self.consensus_engine.check_consensus_status(consensus_id)

        if result and result.consensus_achieved:
            # Remove from active processes
            self.active_consensus_processes.discard(consensus_id)
            self._stats["successful_consensus"] += 1
            return result.final_result

        return None

    async def get_bridge_status(self) -> dict[str, any]:
        """
        Get overall bridge system status.

        Returns:
            Dict[str, any]: Bridge system status and metrics
        """
        # Get subsystem stats
        broker_stats = await self.message_broker.get_broker_stats()
        consensus_stats = await self.consensus_engine.get_consensus_stats()
        health_metrics = await self.health_monitor.get_all_bridge_health()
        monitoring_stats = await self.health_monitor.get_monitoring_stats()

        # Calculate uptime
        current_uptime = 0
        if self._start_time and self._running:
            current_uptime = (datetime.utcnow() - self._start_time).total_seconds()

        total_uptime = self._stats["bridge_uptime_seconds"] + current_uptime

        return {
            "bridge": {
                "initialized": self._initialized,
                "running": self._running,
                "supported_chains": [chain.value for chain in self.supported_chains],
                "total_routes": len(self.routes),
                "active_routes": len(self.active_routes),
                "uptime_seconds": total_uptime,
                **self._stats,
            },
            "message_broker": broker_stats,
            "consensus_engine": consensus_stats,
            "health_monitor": monitoring_stats,
            "route_health": {
                route_id: {
                    "health_score": metrics.health_score,
                    "latency_ms": metrics.average_latency_ms,
                    "throughput": metrics.throughput_msg_per_sec,
                    "error_rate": metrics.error_rate,
                    "uptime": metrics.uptime_percentage,
                }
                for route_id, metrics in health_metrics.items()
            },
        }

    async def shutdown(self) -> None:
        """Gracefully shutdown the bridge system."""
        self.logger.info("Shutting down cross-chain bridge")

        # Stop the bridge
        await self.stop()

        # Clear state
        self.active_consensus_processes.clear()
        self._initialized = False

        self.logger.info("Cross-chain bridge shutdown complete")

    def _create_bridge_routes(self) -> list[BridgeRoute]:
        """Create bridge routes for all supported chain pairs."""
        routes = []
        chains = list(self.adapters.keys())

        for i, source_chain in enumerate(chains):
            for j, target_chain in enumerate(chains):
                if i != j:  # Don't create self-routes
                    route = BridgeRoute(
                        source_chain=source_chain,
                        target_chain=target_chain,
                        adapter_class=self.adapters[target_chain].__class__.__name__,
                        health_score=1.0,
                        latency_ms=100.0,  # Default assumption
                        throughput_msg_per_sec=100.0,  # Default assumption
                        reliability_score=0.95,  # Default assumption
                        is_active=True,
                    )
                    routes.append(route)

        return routes

    def _validate_message(self, message: BridgeMessage) -> bool:
        """
        Validate a bridge message.

        Args:
            message: Message to validate

        Returns:
            bool: True if message is valid
        """
        # Check if chains are supported
        if message.source_chain not in self.supported_chains:
            self.logger.error(f"Unsupported source chain: {message.source_chain.value}")
            return False

        if message.target_chain not in self.supported_chains:
            self.logger.error(f"Unsupported target chain: {message.target_chain.value}")
            return False

        # Check if route exists and is active
        route_id = f"{message.source_chain.value}_{message.target_chain.value}"
        matching_routes = [
            r
            for r in self.routes
            if r.source_chain == message.source_chain
            and r.target_chain == message.target_chain
        ]

        if not matching_routes:
            self.logger.error(f"No route found for {route_id}")
            return False

        if not any(route.is_active for route in matching_routes):
            self.logger.error(f"No active routes for {route_id}")
            return False

        # Validate message structure
        if not message.message_id:
            self.logger.error("Message missing ID")
            return False

        if not message.payload:
            self.logger.error("Message missing payload")
            return False

        return True

    def _register_alert_callbacks(self) -> None:
        """Register alert callbacks for bridge monitoring."""

        def handle_route_down_alert(alert_id: str, alert_data: dict[str, any]) -> None:
            """Handle route down alerts."""
            route_id = alert_data.get("route_id")
            if route_id:
                self.logger.critical(f"Route down alert: {route_id}")
                # Could implement automatic failover here

        def handle_high_latency_alert(
            alert_id: str, alert_data: dict[str, any]
        ) -> None:
            """Handle high latency alerts."""
            route_id = alert_data.get("route_id")
            latency = alert_data.get("metadata", {}).get("latency_ms", 0)
            self.logger.warning(f"High latency alert on {route_id}: {latency}ms")

        def handle_consensus_timeout_alert(
            alert_id: str, alert_data: dict[str, any]
        ) -> None:
            """Handle consensus timeout alerts."""
            self.logger.error(f"Consensus timeout alert: {alert_id}")
            # Could implement consensus retry logic here

        # Register callbacks
        self.health_monitor.register_alert_callback(
            "route_down", handle_route_down_alert
        )
        self.health_monitor.register_alert_callback(
            "high_latency", handle_high_latency_alert
        )
        self.health_monitor.register_alert_callback(
            "consensus_timeout", handle_consensus_timeout_alert
        )

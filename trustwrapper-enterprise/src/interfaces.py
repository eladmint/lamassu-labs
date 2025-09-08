"""
Cross-Chain Bridge Interfaces
============================

Core interface definitions for TrustWrapper v3.0 cross-chain bridge system.
Enables secure message passing and consensus across multiple blockchain networks.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from core.interfaces import ChainType


class BridgeMessageType(Enum):
    """Types of cross-chain bridge messages."""

    VERIFICATION_REQUEST = "verification_request"
    VERIFICATION_RESPONSE = "verification_response"
    CONSENSUS_VOTE = "consensus_vote"
    CONSENSUS_RESULT = "consensus_result"
    HEALTH_CHECK = "health_check"
    SYNCHRONIZATION = "synchronization"


class BridgeMessageStatus(Enum):
    """Status of bridge messages."""

    PENDING = "pending"
    TRANSMITTED = "transmitted"
    CONFIRMED = "confirmed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class BridgeConsensusType(Enum):
    """Types of bridge consensus mechanisms."""

    SIMPLE_MAJORITY = "simple_majority"
    WEIGHTED_VOTING = "weighted_voting"
    BYZANTINE_FAULT_TOLERANT = "byzantine_fault_tolerant"
    THRESHOLD_SIGNATURE = "threshold_signature"


@dataclass
class BridgeMessage:
    """Cross-chain bridge message structure."""

    message_id: str
    message_type: BridgeMessageType
    source_chain: ChainType
    target_chain: ChainType
    payload: dict[str, Any]
    timestamp: datetime
    timeout_seconds: int
    priority: int = 0
    retry_count: int = 0
    max_retries: int = 3
    status: BridgeMessageStatus = BridgeMessageStatus.PENDING
    error_message: str | None = None


@dataclass
class BridgeRoute:
    """Defines a route between two blockchain networks."""

    source_chain: ChainType
    target_chain: ChainType
    adapter_class: str
    health_score: float
    latency_ms: float
    throughput_msg_per_sec: float
    reliability_score: float
    is_active: bool = True
    last_health_check: datetime | None = None


@dataclass
class BridgeMetrics:
    """Bridge performance and health metrics."""

    route_id: str
    total_messages: int
    successful_messages: int
    failed_messages: int
    average_latency_ms: float
    throughput_msg_per_sec: float
    error_rate: float
    uptime_percentage: float
    last_message_timestamp: datetime | None
    health_score: float


@dataclass
class ConsensusVote:
    """Bridge consensus vote structure."""

    vote_id: str
    message_id: str
    voter_chain: ChainType
    vote_value: Any
    confidence_score: float
    weight: float
    timestamp: datetime
    signature: str | None = None


@dataclass
class ConsensusResult:
    """Result of bridge consensus process."""

    consensus_id: str
    message_id: str
    consensus_type: BridgeConsensusType
    participating_chains: list[ChainType]
    total_votes: int
    consensus_achieved: bool
    final_result: Any
    confidence_score: float
    execution_time_seconds: float
    timestamp: datetime


class IBridgeAdapter(ABC):
    """
    Interface for blockchain-specific bridge adapters.

    Each blockchain requires its own adapter to handle message transmission,
    verification, and consensus according to that chain's specific protocols.
    """

    @property
    @abstractmethod
    def supported_chains(self) -> list[ChainType]:
        """Return list of blockchain types this adapter supports."""
        pass

    @property
    @abstractmethod
    def is_operational(self) -> bool:
        """Check if the bridge adapter is operational."""
        pass

    @abstractmethod
    async def initialize(self, config: dict[str, Any]) -> bool:
        """
        Initialize the bridge adapter with configuration.

        Args:
            config: Adapter-specific configuration

        Returns:
            bool: True if initialization successful
        """
        pass

    @abstractmethod
    async def transmit_message(self, message: BridgeMessage) -> bool:
        """
        Transmit a message to the target blockchain.

        Args:
            message: Bridge message to transmit

        Returns:
            bool: True if transmission successful
        """
        pass

    @abstractmethod
    async def receive_messages(
        self, chain_type: ChainType, timeout_seconds: int = 30
    ) -> list[BridgeMessage]:
        """
        Receive pending messages from a blockchain.

        Args:
            chain_type: Source blockchain to check for messages
            timeout_seconds: Maximum time to wait for messages

        Returns:
            List[BridgeMessage]: Received messages
        """
        pass

    @abstractmethod
    async def confirm_message_delivery(
        self, message_id: str, target_chain: ChainType
    ) -> bool:
        """
        Confirm that a message was successfully delivered.

        Args:
            message_id: Message identifier
            target_chain: Target blockchain

        Returns:
            bool: True if delivery confirmed
        """
        pass

    @abstractmethod
    async def get_bridge_metrics(
        self, source_chain: ChainType, target_chain: ChainType
    ) -> BridgeMetrics:
        """
        Get performance metrics for a bridge route.

        Args:
            source_chain: Source blockchain
            target_chain: Target blockchain

        Returns:
            BridgeMetrics: Performance metrics
        """
        pass


class ICrossChainConsensus(ABC):
    """
    Interface for cross-chain consensus mechanisms.

    Handles voting, aggregation, and decision-making across multiple
    blockchain networks with different consensus protocols.
    """

    @property
    @abstractmethod
    def consensus_type(self) -> BridgeConsensusType:
        """Return the type of consensus mechanism."""
        pass

    @property
    @abstractmethod
    def minimum_participants(self) -> int:
        """Return minimum number of participants required."""
        pass

    @abstractmethod
    async def initialize_consensus(
        self,
        message_id: str,
        participating_chains: list[ChainType],
        consensus_config: dict[str, Any],
    ) -> str:
        """
        Initialize a new consensus process.

        Args:
            message_id: Message requiring consensus
            participating_chains: Chains participating in consensus
            consensus_config: Consensus-specific configuration

        Returns:
            str: Consensus process identifier
        """
        pass

    @abstractmethod
    async def submit_vote(self, consensus_id: str, vote: ConsensusVote) -> bool:
        """
        Submit a vote to the consensus process.

        Args:
            consensus_id: Consensus process identifier
            vote: Vote to submit

        Returns:
            bool: True if vote accepted
        """
        pass

    @abstractmethod
    async def check_consensus_status(self, consensus_id: str) -> ConsensusResult | None:
        """
        Check the status of a consensus process.

        Args:
            consensus_id: Consensus process identifier

        Returns:
            ConsensusResult: Consensus result if complete, None if ongoing
        """
        pass

    @abstractmethod
    async def finalize_consensus(self, consensus_id: str) -> ConsensusResult:
        """
        Finalize and return the consensus result.

        Args:
            consensus_id: Consensus process identifier

        Returns:
            ConsensusResult: Final consensus result
        """
        pass


class IBridgeHealthMonitor(ABC):
    """
    Interface for bridge health monitoring system.

    Provides real-time monitoring, alerting, and recovery capabilities
    for cross-chain bridge infrastructure.
    """

    @abstractmethod
    async def start_monitoring(self) -> None:
        """Start the bridge health monitoring system."""
        pass

    @abstractmethod
    async def stop_monitoring(self) -> None:
        """Stop the bridge health monitoring system."""
        pass

    @abstractmethod
    async def register_bridge_route(self, route: BridgeRoute) -> None:
        """
        Register a bridge route for monitoring.

        Args:
            route: Bridge route to monitor
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def get_all_bridge_health(self) -> dict[str, BridgeMetrics]:
        """
        Get health metrics for all monitored bridge routes.

        Returns:
            Dict[str, BridgeMetrics]: Route ID to metrics mapping
        """
        pass

    @abstractmethod
    def register_alert_callback(
        self, alert_type: str, callback: Callable[[str, dict[str, Any]], None]
    ) -> None:
        """
        Register a callback for bridge alerts.

        Args:
            alert_type: Type of alert to monitor
            callback: Function to call when alert triggers
        """
        pass


class ICrossChainBridge(ABC):
    """
    Main interface for the cross-chain bridge system.

    Coordinates message passing, consensus, and monitoring across
    multiple blockchain networks for TrustWrapper v3.0.
    """

    @property
    @abstractmethod
    def supported_chains(self) -> list[ChainType]:
        """Return list of supported blockchain types."""
        pass

    @property
    @abstractmethod
    def active_routes(self) -> list[BridgeRoute]:
        """Return list of active bridge routes."""
        pass

    @abstractmethod
    async def initialize(
        self,
        adapters: dict[ChainType, IBridgeAdapter],
        consensus_engine: ICrossChainConsensus,
        health_monitor: IBridgeHealthMonitor,
    ) -> bool:
        """
        Initialize the cross-chain bridge system.

        Args:
            adapters: Chain-specific bridge adapters
            consensus_engine: Consensus mechanism
            health_monitor: Health monitoring system

        Returns:
            bool: True if initialization successful
        """
        pass

    @abstractmethod
    async def send_message(self, message: BridgeMessage) -> str:
        """
        Send a message across chains.

        Args:
            message: Message to send

        Returns:
            str: Message tracking identifier
        """
        pass

    @abstractmethod
    async def process_pending_messages(self) -> int:
        """
        Process all pending cross-chain messages.

        Returns:
            int: Number of messages processed
        """
        pass

    @abstractmethod
    async def initiate_cross_chain_consensus(
        self,
        verification_request_id: str,
        participating_chains: list[ChainType],
        consensus_config: dict[str, Any],
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
        pass

    @abstractmethod
    async def get_bridge_status(self) -> dict[str, Any]:
        """
        Get overall bridge system status.

        Returns:
            Dict[str, Any]: Bridge system status and metrics
        """
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully shutdown the bridge system."""
        pass

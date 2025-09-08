"""
TrustWrapper v3.0 - Advanced Byzantine Fault Tolerance Implementation
====================================================================

Implements advanced BFT consensus algorithms for enterprise-grade
AI verification across multiple blockchain networks.

Algorithms:
- Practical Byzantine Fault Tolerance (PBFT)
- HotStuff consensus variant
- Tendermint-inspired consensus
- Dynamic weight adjustment

This module extends the basic consensus engine with sophisticated
fault tolerance and performance optimizations.
"""

import asyncio
import hashlib
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class ConsensusPhase(Enum):
    """Phases in Byzantine consensus protocols"""

    PREPARE = "prepare"
    COMMIT = "commit"
    DECIDE = "decide"
    VIEW_CHANGE = "view_change"


class MessageType(Enum):
    """Types of consensus messages"""

    PROPOSE = "propose"
    PREPARE = "prepare"
    COMMIT = "commit"
    VIEW_CHANGE = "view_change"
    NEW_VIEW = "new_view"
    DECISION = "decision"


@dataclass
class ConsensusMessage:
    """Message exchanged in consensus protocol"""

    message_type: MessageType
    view_number: int
    sequence_number: int
    sender_id: str
    content: dict[str, Any]
    signature: str = ""
    timestamp: float = field(default_factory=time.time)

    def hash(self) -> str:
        """Generate hash of message content"""
        content_str = f"{self.message_type.value}:{self.view_number}:{self.sequence_number}:{str(self.content)}"
        return hashlib.sha256(content_str.encode()).hexdigest()


@dataclass
class ConsensusState:
    """State of a consensus instance"""

    view_number: int = 0
    sequence_number: int = 0
    phase: ConsensusPhase = ConsensusPhase.PREPARE
    prepared_value: Any | None = None
    prepared_proof: list[ConsensusMessage] = field(default_factory=list)
    commit_proof: list[ConsensusMessage] = field(default_factory=list)
    decided: bool = False
    decided_value: Any | None = None


class IAdvancedConsensusAlgorithm(ABC):
    """Interface for advanced consensus algorithms"""

    @abstractmethod
    async def propose(self, value: Any, validators: list[str]) -> ConsensusMessage:
        """Propose a value for consensus"""
        pass

    @abstractmethod
    async def handle_message(
        self, message: ConsensusMessage
    ) -> ConsensusMessage | None:
        """Handle incoming consensus message"""
        pass

    @abstractmethod
    async def check_decision(self) -> tuple[bool, Any | None]:
        """Check if consensus has been reached"""
        pass

    @abstractmethod
    def get_fault_tolerance(self) -> int:
        """Get number of faults algorithm can tolerate"""
        pass


class PBFTConsensus(IAdvancedConsensusAlgorithm):
    """
    Practical Byzantine Fault Tolerance implementation

    Classic 3-phase consensus:
    1. Pre-prepare/Propose
    2. Prepare
    3. Commit

    Tolerates f Byzantine faults with 3f+1 total nodes
    """

    def __init__(self, node_id: str, total_nodes: int):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.f = (total_nodes - 1) // 3  # Byzantine fault tolerance
        self.state = ConsensusState()
        self.message_log: list[ConsensusMessage] = []
        self.prepare_messages: dict[int, list[ConsensusMessage]] = {}
        self.commit_messages: dict[int, list[ConsensusMessage]] = {}

    async def propose(self, value: Any, validators: list[str]) -> ConsensusMessage:
        """Leader proposes a value"""
        if self._is_leader():
            proposal = ConsensusMessage(
                message_type=MessageType.PROPOSE,
                view_number=self.state.view_number,
                sequence_number=self.state.sequence_number,
                sender_id=self.node_id,
                content={"value": value, "validators": validators},
            )
            self.message_log.append(proposal)
            return proposal
        else:
            raise Exception("Only leader can propose in PBFT")

    async def handle_message(
        self, message: ConsensusMessage
    ) -> ConsensusMessage | None:
        """Handle incoming PBFT message"""
        self.message_log.append(message)

        if message.message_type == MessageType.PROPOSE:
            return await self._handle_propose(message)
        elif message.message_type == MessageType.PREPARE:
            return await self._handle_prepare(message)
        elif message.message_type == MessageType.COMMIT:
            return await self._handle_commit(message)

        return None

    async def _handle_propose(
        self, message: ConsensusMessage
    ) -> ConsensusMessage | None:
        """Handle propose message from leader"""
        if not self._verify_leader(message.sender_id, message.view_number):
            logger.warning(
                f"Invalid leader {message.sender_id} for view {message.view_number}"
            )
            return None

        # Move to prepare phase
        self.state.phase = ConsensusPhase.PREPARE
        self.state.prepared_value = message.content["value"]

        # Broadcast prepare message
        prepare_msg = ConsensusMessage(
            message_type=MessageType.PREPARE,
            view_number=message.view_number,
            sequence_number=message.sequence_number,
            sender_id=self.node_id,
            content={"value_hash": message.hash()},
        )

        return prepare_msg

    async def _handle_prepare(
        self, message: ConsensusMessage
    ) -> ConsensusMessage | None:
        """Handle prepare message"""
        seq_num = message.sequence_number

        if seq_num not in self.prepare_messages:
            self.prepare_messages[seq_num] = []

        self.prepare_messages[seq_num].append(message)

        # Check if we have 2f+1 prepare messages
        if len(self.prepare_messages[seq_num]) >= 2 * self.f + 1:
            if self.state.phase == ConsensusPhase.PREPARE:
                self.state.phase = ConsensusPhase.COMMIT
                self.state.prepared_proof = self.prepare_messages[seq_num].copy()

                # Broadcast commit message
                commit_msg = ConsensusMessage(
                    message_type=MessageType.COMMIT,
                    view_number=message.view_number,
                    sequence_number=message.sequence_number,
                    sender_id=self.node_id,
                    content={"prepared": True},
                )

                return commit_msg

        return None

    async def _handle_commit(
        self, message: ConsensusMessage
    ) -> ConsensusMessage | None:
        """Handle commit message"""
        seq_num = message.sequence_number

        if seq_num not in self.commit_messages:
            self.commit_messages[seq_num] = []

        self.commit_messages[seq_num].append(message)

        # Check if we have 2f+1 commit messages
        if len(self.commit_messages[seq_num]) >= 2 * self.f + 1:
            if not self.state.decided:
                self.state.decided = True
                self.state.decided_value = self.state.prepared_value
                self.state.commit_proof = self.commit_messages[seq_num].copy()

                # Broadcast decision
                decision_msg = ConsensusMessage(
                    message_type=MessageType.DECISION,
                    view_number=message.view_number,
                    sequence_number=message.sequence_number,
                    sender_id=self.node_id,
                    content={"decided_value": self.state.decided_value},
                )

                return decision_msg

        return None

    async def check_decision(self) -> tuple[bool, Any | None]:
        """Check if consensus has been reached"""
        return self.state.decided, self.state.decided_value

    def get_fault_tolerance(self) -> int:
        """PBFT tolerates f faults with 3f+1 nodes"""
        return self.f

    def _is_leader(self) -> bool:
        """Check if this node is the current leader"""
        leader_index = self.state.view_number % self.total_nodes
        # Simplified: assume nodes are numbered 0 to n-1
        return self.node_id == f"node_{leader_index}"

    def _verify_leader(self, sender_id: str, view_number: int) -> bool:
        """Verify if sender is the legitimate leader for the view"""
        expected_leader_index = view_number % self.total_nodes
        expected_leader = f"node_{expected_leader_index}"
        return sender_id == expected_leader


class HotStuffConsensus(IAdvancedConsensusAlgorithm):
    """
    HotStuff consensus implementation

    Linear view-change with optimistic responsiveness
    Achieves consensus in 3 phases with linear message complexity
    """

    def __init__(self, node_id: str, total_nodes: int):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.f = (total_nodes - 1) // 3
        self.state = ConsensusState()
        self.generic_qc: dict[str, Any] | None = None  # Quorum certificate
        self.locked_qc: dict[str, Any] | None = None
        self.message_votes: dict[str, list[ConsensusMessage]] = {}

    async def propose(self, value: Any, validators: list[str]) -> ConsensusMessage:
        """Leader proposes with quorum certificate"""
        if self._is_leader():
            proposal = ConsensusMessage(
                message_type=MessageType.PROPOSE,
                view_number=self.state.view_number,
                sequence_number=self.state.sequence_number,
                sender_id=self.node_id,
                content={
                    "value": value,
                    "validators": validators,
                    "qc": self.generic_qc,  # Include quorum certificate
                },
            )
            return proposal
        else:
            raise Exception("Only leader can propose in HotStuff")

    async def handle_message(
        self, message: ConsensusMessage
    ) -> ConsensusMessage | None:
        """Handle HotStuff consensus message"""
        msg_hash = message.hash()

        if msg_hash not in self.message_votes:
            self.message_votes[msg_hash] = []

        self.message_votes[msg_hash].append(message)

        # Check if we have quorum (2f+1 votes)
        if len(self.message_votes[msg_hash]) >= 2 * self.f + 1:
            # Create quorum certificate
            qc = {
                "view": message.view_number,
                "type": message.message_type.value,
                "votes": len(self.message_votes[msg_hash]),
                "value_hash": msg_hash,
            }

            if message.message_type == MessageType.PREPARE:
                self.generic_qc = qc
                # Move to commit phase
                commit_msg = ConsensusMessage(
                    message_type=MessageType.COMMIT,
                    view_number=message.view_number,
                    sequence_number=message.sequence_number,
                    sender_id=self.node_id,
                    content={"prepare_qc": qc},
                )
                return commit_msg

            elif message.message_type == MessageType.COMMIT:
                self.locked_qc = qc
                self.state.decided = True
                self.state.decided_value = message.content.get("value")

        return None

    async def check_decision(self) -> tuple[bool, Any | None]:
        """Check if consensus has been reached"""
        return self.state.decided, self.state.decided_value

    def get_fault_tolerance(self) -> int:
        """HotStuff tolerates f faults with 3f+1 nodes"""
        return self.f

    def _is_leader(self) -> bool:
        """Check if this node is the current leader"""
        leader_index = self.state.view_number % self.total_nodes
        return self.node_id == f"node_{leader_index}"


class WeightedByzantineConsensus:
    """
    Weighted Byzantine consensus with dynamic weight adjustment

    Features:
    - Reputation-based weights
    - Stake-based voting power
    - Dynamic weight updates
    - Weighted quorum calculations
    """

    def __init__(self, node_weights: dict[str, float]):
        self.node_weights = node_weights
        self.total_weight = sum(node_weights.values())
        self.reputation_scores: dict[str, float] = {node: 1.0 for node in node_weights}
        self.consensus_history: list[dict[str, Any]] = []

    def calculate_weighted_quorum(
        self, votes: list[tuple[str, Any]]
    ) -> tuple[bool, Any]:
        """Calculate if weighted votes reach consensus"""
        vote_weights: dict[Any, float] = {}

        for node_id, vote in votes:
            weight = self.get_effective_weight(node_id)
            if vote not in vote_weights:
                vote_weights[vote] = 0
            vote_weights[vote] += weight

        # Check if any option has >2/3 weighted votes
        threshold = (2 * self.total_weight) / 3

        for value, weight in vote_weights.items():
            if weight > threshold:
                return True, value

        return False, None

    def get_effective_weight(self, node_id: str) -> float:
        """Calculate effective weight including reputation"""
        base_weight = self.node_weights.get(node_id, 0)
        reputation = self.reputation_scores.get(node_id, 1.0)
        return base_weight * reputation

    def update_reputation(
        self, node_id: str, consensus_participation: bool, agreement_with_majority: bool
    ):
        """Update node reputation based on consensus behavior"""
        if node_id not in self.reputation_scores:
            return

        # Reward participation and agreement with consensus
        if consensus_participation:
            if agreement_with_majority:
                # Increase reputation for correct behavior
                self.reputation_scores[node_id] = min(
                    self.reputation_scores[node_id] * 1.05, 2.0
                )
            else:
                # Slight decrease for disagreement
                self.reputation_scores[node_id] = max(
                    self.reputation_scores[node_id] * 0.98, 0.5
                )
        else:
            # Penalize non-participation
            self.reputation_scores[node_id] = max(
                self.reputation_scores[node_id] * 0.95, 0.5
            )

    def get_weighted_fault_tolerance(self) -> float:
        """Calculate weighted fault tolerance threshold"""
        # Can tolerate up to 1/3 of total weight being Byzantine
        return self.total_weight / 3


class AdvancedConsensusEngine:
    """
    Main advanced consensus engine supporting multiple algorithms

    Features:
    - Pluggable consensus algorithms
    - Algorithm selection based on requirements
    - Performance optimization
    - Comprehensive monitoring
    """

    def __init__(self):
        self.algorithms: dict[str, IAdvancedConsensusAlgorithm] = {}
        self.active_consensus: dict[str, ConsensusState] = {}
        self.performance_metrics: dict[str, list[float]] = {}

    def register_algorithm(self, name: str, algorithm: IAdvancedConsensusAlgorithm):
        """Register a consensus algorithm"""
        self.algorithms[name] = algorithm
        logger.info(f"Registered consensus algorithm: {name}")

    async def start_consensus(
        self,
        consensus_id: str,
        value: Any,
        validators: list[str],
        algorithm: str = "pbft",
    ) -> ConsensusMessage:
        """Start a new consensus instance"""
        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown consensus algorithm: {algorithm}")

        algo = self.algorithms[algorithm]
        start_time = time.time()

        # Propose value
        proposal = await algo.propose(value, validators)

        # Track performance
        if algorithm not in self.performance_metrics:
            self.performance_metrics[algorithm] = []

        self.active_consensus[consensus_id] = {
            "algorithm": algorithm,
            "start_time": start_time,
            "value": value,
            "validators": validators,
        }

        return proposal

    async def process_consensus_message(
        self, consensus_id: str, message: ConsensusMessage
    ) -> ConsensusMessage | None:
        """Process incoming consensus message"""
        if consensus_id not in self.active_consensus:
            logger.warning(f"Unknown consensus instance: {consensus_id}")
            return None

        algo_name = self.active_consensus[consensus_id]["algorithm"]
        algo = self.algorithms[algo_name]

        # Process message
        response = await algo.handle_message(message)

        # Check for decision
        decided, value = await algo.check_decision()
        if decided:
            end_time = time.time()
            duration = end_time - self.active_consensus[consensus_id]["start_time"]
            self.performance_metrics[algo_name].append(duration)

            logger.info(f"Consensus {consensus_id} reached decision in {duration:.3f}s")

        return response

    def get_algorithm_stats(self) -> dict[str, dict[str, float]]:
        """Get performance statistics for all algorithms"""
        stats = {}

        for algo_name, durations in self.performance_metrics.items():
            if durations:
                stats[algo_name] = {
                    "avg_duration": sum(durations) / len(durations),
                    "min_duration": min(durations),
                    "max_duration": max(durations),
                    "total_consensus": len(durations),
                }

        return stats

    def select_optimal_algorithm(
        self,
        num_validators: int,
        latency_requirement: float,
        byzantine_assumption: float = 0.33,
    ) -> str:
        """Select optimal consensus algorithm based on requirements"""
        # Simple selection logic (can be enhanced)
        if num_validators <= 10 and latency_requirement < 1.0:
            return "hotstuff"  # Optimized for small groups
        elif byzantine_assumption < 0.33:
            return "pbft"  # Classic BFT
        else:
            return "weighted"  # For higher fault tolerance needs


# Example usage
async def demo_advanced_consensus():
    """Demonstrate advanced consensus algorithms"""
    print("🚀 Advanced Consensus Engine Demo")
    print("=" * 50)

    # Create consensus engine
    engine = AdvancedConsensusEngine()

    # Register algorithms
    pbft = PBFTConsensus("node_0", 4)  # 4 nodes, tolerates 1 fault
    hotstuff = HotStuffConsensus("node_0", 4)

    engine.register_algorithm("pbft", pbft)
    engine.register_algorithm("hotstuff", hotstuff)

    # Start consensus
    validators = ["node_0", "node_1", "node_2", "node_3"]
    test_value = {"ai_verification": "test_data", "timestamp": time.time()}

    proposal = await engine.start_consensus(
        "consensus_001", test_value, validators, algorithm="pbft"
    )

    print(f"✅ Consensus started with {proposal.message_type.value}")
    print("📊 Algorithm: PBFT")
    print(f"👥 Validators: {len(validators)}")
    print(f"🛡️ Fault tolerance: {pbft.get_fault_tolerance()} nodes")

    # Simulate consensus messages
    # In production, these would come from network

    print("\n📈 Performance Stats:")
    stats = engine.get_algorithm_stats()
    for algo, metrics in stats.items():
        print(f"  {algo}: {metrics}")


if __name__ == "__main__":
    asyncio.run(demo_advanced_consensus())

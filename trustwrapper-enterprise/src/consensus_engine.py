"""
Cross-Chain Consensus Engine
============================

Byzantine fault-tolerant consensus implementation for TrustWrapper v3.0 bridge.
Handles voting, aggregation, and decision-making across multiple blockchain networks.
"""

import asyncio
import logging
import statistics
import uuid
from datetime import datetime

from bridge.interfaces import (
    BridgeConsensusType,
    ConsensusResult,
    ConsensusVote,
    ICrossChainConsensus,
)
from core.interfaces import ChainType


class ConsensusProcess:
    """Represents an active consensus process."""

    def __init__(
        self,
        consensus_id: str,
        message_id: str,
        consensus_type: BridgeConsensusType,
        participating_chains: list[ChainType],
        config: dict[str, any],
    ):
        self.consensus_id = consensus_id
        self.message_id = message_id
        self.consensus_type = consensus_type
        self.participating_chains = participating_chains
        self.config = config

        self.votes: dict[ChainType, ConsensusVote] = {}
        self.chain_weights = config.get("chain_weights", {})
        self.threshold = config.get("threshold", 0.67)
        self.timeout_seconds = config.get("timeout_seconds", 120)

        self.start_time = datetime.utcnow()
        self.is_complete = False
        self.result: ConsensusResult | None = None

        # Byzantine fault tolerance settings
        self.max_byzantine_faults = len(participating_chains) // 3
        self.min_honest_nodes = len(participating_chains) - self.max_byzantine_faults

    def add_vote(self, vote: ConsensusVote) -> bool:
        """
        Add a vote to the consensus process.

        Args:
            vote: Vote to add

        Returns:
            bool: True if vote was accepted
        """
        if vote.voter_chain not in self.participating_chains:
            return False

        if vote.voter_chain in self.votes:
            # Update existing vote (latest wins)
            pass

        self.votes[vote.voter_chain] = vote
        return True

    def has_sufficient_votes(self) -> bool:
        """Check if we have sufficient votes for consensus."""
        if self.consensus_type == BridgeConsensusType.SIMPLE_MAJORITY:
            return len(self.votes) > len(self.participating_chains) / 2

        elif self.consensus_type == BridgeConsensusType.WEIGHTED_VOTING:
            total_weight = self._calculate_total_weight()
            voted_weight = self._calculate_voted_weight()
            return voted_weight / total_weight >= self.threshold

        elif self.consensus_type == BridgeConsensusType.BYZANTINE_FAULT_TOLERANT:
            return len(self.votes) >= self.min_honest_nodes

        return False

    def is_timed_out(self) -> bool:
        """Check if consensus process has timed out."""
        elapsed = (datetime.utcnow() - self.start_time).total_seconds()
        return elapsed > self.timeout_seconds

    def _calculate_total_weight(self) -> float:
        """Calculate total weight of all participating chains."""
        total = 0.0
        for chain in self.participating_chains:
            weight = self.chain_weights.get(chain, 1.0)
            total += weight
        return total

    def _calculate_voted_weight(self) -> float:
        """Calculate total weight of chains that have voted."""
        total = 0.0
        for chain, vote in self.votes.items():
            weight = self.chain_weights.get(chain, 1.0)
            total += weight * vote.weight  # Include vote confidence
        return total


class CrossChainConsensusEngine(ICrossChainConsensus):
    """
    Cross-chain consensus engine for TrustWrapper v3.0 bridge.

    Implements multiple consensus mechanisms including Byzantine fault tolerance,
    weighted voting, and threshold signatures for secure cross-chain operations.
    """

    def __init__(
        self,
        default_consensus_type: BridgeConsensusType = BridgeConsensusType.BYZANTINE_FAULT_TOLERANT,
    ):
        self.default_consensus_type = default_consensus_type
        self.active_processes: dict[str, ConsensusProcess] = {}
        self.completed_processes: dict[str, ConsensusResult] = {}

        # Configuration
        self.cleanup_interval = 3600  # 1 hour
        self.max_completed_history = 1000

        # State tracking
        self._running = False
        self._cleanup_task = None

        self.logger = logging.getLogger(f"{__name__}.consensus")

        # Statistics
        self._stats = {
            "total_consensus_processes": 0,
            "successful_consensus": 0,
            "failed_consensus": 0,
            "timeout_consensus": 0,
            "byzantine_faults_detected": 0,
        }

    @property
    def consensus_type(self) -> BridgeConsensusType:
        """Return the default consensus mechanism type."""
        return self.default_consensus_type

    @property
    def minimum_participants(self) -> int:
        """Return minimum number of participants required."""
        if self.default_consensus_type == BridgeConsensusType.BYZANTINE_FAULT_TOLERANT:
            return 4  # Minimum for BFT (3f + 1, f = 1)
        elif self.default_consensus_type == BridgeConsensusType.SIMPLE_MAJORITY:
            return 3  # Minimum for majority
        else:
            return 2  # Minimum for weighted voting

    async def start(self) -> None:
        """Start the consensus engine background tasks."""
        if self._running:
            return

        self._running = True
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

        self.logger.info("Started cross-chain consensus engine")

    async def stop(self) -> None:
        """Stop the consensus engine and cleanup resources."""
        if not self._running:
            return

        self._running = False

        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        self.logger.info("Stopped cross-chain consensus engine")

    async def initialize_consensus(
        self,
        message_id: str,
        participating_chains: list[ChainType],
        consensus_config: dict[str, any],
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
        # Validate participating chains
        if len(participating_chains) < self.minimum_participants:
            raise ValueError(
                f"Insufficient participants: {len(participating_chains)} < {self.minimum_participants}"
            )

        # Create consensus process
        consensus_id = str(uuid.uuid4())
        consensus_type = consensus_config.get(
            "consensus_type", self.default_consensus_type
        )

        if isinstance(consensus_type, str):
            consensus_type = BridgeConsensusType(consensus_type)

        process = ConsensusProcess(
            consensus_id=consensus_id,
            message_id=message_id,
            consensus_type=consensus_type,
            participating_chains=participating_chains,
            config=consensus_config,
        )

        self.active_processes[consensus_id] = process
        self._stats["total_consensus_processes"] += 1

        self.logger.info(
            f"Initialized consensus {consensus_id} for message {message_id} "
            f"with {len(participating_chains)} participants"
        )

        return consensus_id

    async def submit_vote(self, consensus_id: str, vote: ConsensusVote) -> bool:
        """
        Submit a vote to the consensus process.

        Args:
            consensus_id: Consensus process identifier
            vote: Vote to submit

        Returns:
            bool: True if vote accepted
        """
        if consensus_id not in self.active_processes:
            self.logger.warning(f"Consensus process {consensus_id} not found")
            return False

        process = self.active_processes[consensus_id]

        if process.is_complete:
            self.logger.warning(f"Consensus process {consensus_id} already complete")
            return False

        if process.is_timed_out():
            await self._handle_consensus_timeout(process)
            return False

        # Validate vote
        if not self._validate_vote(vote, process):
            return False

        # Add vote to process
        success = process.add_vote(vote)
        if not success:
            return False

        self.logger.debug(
            f"Added vote from {vote.voter_chain.value} to consensus {consensus_id} "
            f"({len(process.votes)}/{len(process.participating_chains)} votes)"
        )

        # Check if consensus can be reached
        if process.has_sufficient_votes():
            await self._evaluate_consensus(process)

        return True

    async def check_consensus_status(self, consensus_id: str) -> ConsensusResult | None:
        """
        Check the status of a consensus process.

        Args:
            consensus_id: Consensus process identifier

        Returns:
            ConsensusResult: Consensus result if complete, None if ongoing
        """
        if consensus_id in self.completed_processes:
            return self.completed_processes[consensus_id]

        if consensus_id in self.active_processes:
            process = self.active_processes[consensus_id]

            # Check for timeout
            if process.is_timed_out():
                await self._handle_consensus_timeout(process)
                return self.completed_processes.get(consensus_id)

            return process.result  # Will be None if not complete

        return None

    async def finalize_consensus(self, consensus_id: str) -> ConsensusResult:
        """
        Finalize and return the consensus result.

        Args:
            consensus_id: Consensus process identifier

        Returns:
            ConsensusResult: Final consensus result
        """
        result = await self.check_consensus_status(consensus_id)
        if result is None:
            raise ValueError(
                f"Consensus process {consensus_id} not found or not complete"
            )

        return result

    async def get_consensus_stats(self) -> dict[str, any]:
        """
        Get consensus engine statistics.

        Returns:
            Dict: Consensus statistics and metrics
        """
        return {
            **self._stats,
            "active_processes": len(self.active_processes),
            "completed_processes": len(self.completed_processes),
            "success_rate": (
                self._stats["successful_consensus"]
                / max(self._stats["total_consensus_processes"], 1)
            ),
        }

    def _validate_vote(self, vote: ConsensusVote, process: ConsensusProcess) -> bool:
        """
        Validate a consensus vote.

        Args:
            vote: Vote to validate
            process: Consensus process

        Returns:
            bool: True if vote is valid
        """
        # Check if voter is authorized
        if vote.voter_chain not in process.participating_chains:
            self.logger.warning(f"Unauthorized voter: {vote.voter_chain.value}")
            return False

        # Check confidence score
        if not 0.0 <= vote.confidence_score <= 1.0:
            self.logger.warning(f"Invalid confidence score: {vote.confidence_score}")
            return False

        # Check weight
        if not 0.0 <= vote.weight <= 1.0:
            self.logger.warning(f"Invalid vote weight: {vote.weight}")
            return False

        # Additional validation could include signature verification
        # For Phase 1, we assume votes are valid

        return True

    async def _evaluate_consensus(self, process: ConsensusProcess) -> None:
        """
        Evaluate consensus and determine result.

        Args:
            process: Consensus process to evaluate
        """
        try:
            # Detect Byzantine faults
            byzantine_detected = self._detect_byzantine_faults(process)
            if byzantine_detected:
                self._stats["byzantine_faults_detected"] += 1
                self.logger.warning(
                    f"Byzantine faults detected in consensus {process.consensus_id}"
                )

            # Calculate consensus result
            consensus_achieved, final_result, confidence = (
                self._calculate_consensus_result(process)
            )

            # Create result
            execution_time = (datetime.utcnow() - process.start_time).total_seconds()

            result = ConsensusResult(
                consensus_id=process.consensus_id,
                message_id=process.message_id,
                consensus_type=process.consensus_type,
                participating_chains=process.participating_chains,
                total_votes=len(process.votes),
                consensus_achieved=consensus_achieved,
                final_result=final_result,
                confidence_score=confidence,
                execution_time_seconds=execution_time,
                timestamp=datetime.utcnow(),
            )

            # Complete the process
            process.result = result
            process.is_complete = True

            # Move to completed processes
            self.completed_processes[process.consensus_id] = result
            del self.active_processes[process.consensus_id]

            # Update statistics
            if consensus_achieved:
                self._stats["successful_consensus"] += 1
            else:
                self._stats["failed_consensus"] += 1

            self.logger.info(
                f"Consensus {process.consensus_id} completed: "
                f"achieved={consensus_achieved}, confidence={confidence:.3f}"
            )

        except Exception as e:
            self.logger.error(f"Error evaluating consensus {process.consensus_id}: {e}")
            await self._handle_consensus_failure(process, str(e))

    def _calculate_consensus_result(
        self, process: ConsensusProcess
    ) -> tuple[bool, any, float]:
        """
        Calculate the consensus result based on votes.

        Args:
            process: Consensus process

        Returns:
            Tuple[bool, any, float]: (consensus_achieved, final_result, confidence)
        """
        if not process.votes:
            return False, None, 0.0

        # Extract vote values and weights
        vote_values = []
        vote_weights = []
        confidence_scores = []

        for vote in process.votes.values():
            vote_values.append(vote.vote_value)

            # Get chain weight
            chain_weight = process.chain_weights.get(vote.voter_chain, 1.0)
            combined_weight = chain_weight * vote.weight
            vote_weights.append(combined_weight)

            confidence_scores.append(vote.confidence_score)

        # Determine consensus based on consensus type
        if process.consensus_type == BridgeConsensusType.SIMPLE_MAJORITY:
            return self._simple_majority_consensus(vote_values, confidence_scores)

        elif process.consensus_type == BridgeConsensusType.WEIGHTED_VOTING:
            return self._weighted_voting_consensus(
                vote_values, vote_weights, confidence_scores, process.threshold
            )

        elif process.consensus_type == BridgeConsensusType.BYZANTINE_FAULT_TOLERANT:
            return self._byzantine_fault_tolerant_consensus(
                vote_values, vote_weights, confidence_scores
            )

        else:
            # Default to simple majority
            return self._simple_majority_consensus(vote_values, confidence_scores)

    def _simple_majority_consensus(
        self, vote_values: list[any], confidence_scores: list[float]
    ) -> tuple[bool, any, float]:
        """Simple majority consensus algorithm."""
        if not vote_values:
            return False, None, 0.0

        # Count votes for each value
        value_counts = {}
        value_confidences = {}

        for value, confidence in zip(vote_values, confidence_scores, strict=False):
            value_str = str(value)
            value_counts[value_str] = value_counts.get(value_str, 0) + 1

            if value_str not in value_confidences:
                value_confidences[value_str] = []
            value_confidences[value_str].append(confidence)

        # Find majority
        total_votes = len(vote_values)
        majority_threshold = total_votes / 2

        for value_str, count in value_counts.items():
            if count > majority_threshold:
                avg_confidence = statistics.mean(value_confidences[value_str])
                return True, value_str, avg_confidence

        return False, None, 0.0

    def _weighted_voting_consensus(
        self,
        vote_values: list[any],
        vote_weights: list[float],
        confidence_scores: list[float],
        threshold: float,
    ) -> tuple[bool, any, float]:
        """Weighted voting consensus algorithm."""
        if not vote_values:
            return False, None, 0.0

        # Calculate weighted votes
        value_weights = {}
        value_confidences = {}

        total_weight = sum(vote_weights)

        for value, weight, confidence in zip(
            vote_values, vote_weights, confidence_scores, strict=False
        ):
            value_str = str(value)
            value_weights[value_str] = value_weights.get(value_str, 0) + weight

            if value_str not in value_confidences:
                value_confidences[value_str] = []
            value_confidences[value_str].append(confidence)

        # Check threshold
        for value_str, weight in value_weights.items():
            weight_ratio = weight / total_weight
            if weight_ratio >= threshold:
                avg_confidence = statistics.mean(value_confidences[value_str])
                return True, value_str, avg_confidence

        return False, None, 0.0

    def _byzantine_fault_tolerant_consensus(
        self,
        vote_values: list[any],
        vote_weights: list[float],
        confidence_scores: list[float],
    ) -> tuple[bool, any, float]:
        """Byzantine fault tolerant consensus algorithm."""
        # For Phase 1, implement simple BFT based on 2/3 majority
        if len(vote_values) < 3:
            return False, None, 0.0

        # Use weighted voting with 2/3 threshold for BFT
        return self._weighted_voting_consensus(
            vote_values, vote_weights, confidence_scores, 0.67
        )

    def _detect_byzantine_faults(self, process: ConsensusProcess) -> bool:
        """
        Detect potential Byzantine faults in voting.

        Args:
            process: Consensus process

        Returns:
            bool: True if Byzantine behavior detected
        """
        if len(process.votes) < 3:
            return False

        # Check for significant confidence score variance
        confidence_scores = [vote.confidence_score for vote in process.votes.values()]

        if len(confidence_scores) < 2:
            return False

        mean_confidence = statistics.mean(confidence_scores)
        std_dev = (
            statistics.stdev(confidence_scores) if len(confidence_scores) > 1 else 0
        )

        # Check for outliers (confidence scores > 2 standard deviations from mean)
        outliers = 0
        for score in confidence_scores:
            if abs(score - mean_confidence) > 2 * std_dev:
                outliers += 1

        # Byzantine fault detected if more than 1/3 are outliers
        return outliers > len(confidence_scores) // 3

    async def _handle_consensus_timeout(self, process: ConsensusProcess) -> None:
        """
        Handle a consensus process timeout.

        Args:
            process: Timed-out consensus process
        """
        execution_time = (datetime.utcnow() - process.start_time).total_seconds()

        result = ConsensusResult(
            consensus_id=process.consensus_id,
            message_id=process.message_id,
            consensus_type=process.consensus_type,
            participating_chains=process.participating_chains,
            total_votes=len(process.votes),
            consensus_achieved=False,
            final_result=None,
            confidence_score=0.0,
            execution_time_seconds=execution_time,
            timestamp=datetime.utcnow(),
        )

        process.result = result
        process.is_complete = True

        self.completed_processes[process.consensus_id] = result
        del self.active_processes[process.consensus_id]

        self._stats["timeout_consensus"] += 1

        self.logger.warning(
            f"Consensus {process.consensus_id} timed out after {execution_time:.1f}s"
        )

    async def _handle_consensus_failure(
        self, process: ConsensusProcess, error_message: str
    ) -> None:
        """
        Handle a consensus process failure.

        Args:
            process: Failed consensus process
            error_message: Error description
        """
        execution_time = (datetime.utcnow() - process.start_time).total_seconds()

        result = ConsensusResult(
            consensus_id=process.consensus_id,
            message_id=process.message_id,
            consensus_type=process.consensus_type,
            participating_chains=process.participating_chains,
            total_votes=len(process.votes),
            consensus_achieved=False,
            final_result=None,
            confidence_score=0.0,
            execution_time_seconds=execution_time,
            timestamp=datetime.utcnow(),
        )

        process.result = result
        process.is_complete = True

        self.completed_processes[process.consensus_id] = result
        del self.active_processes[process.consensus_id]

        self._stats["failed_consensus"] += 1

        self.logger.error(f"Consensus {process.consensus_id} failed: {error_message}")

    async def _cleanup_loop(self) -> None:
        """Background task for cleaning up old consensus processes."""
        self.logger.info("Started consensus cleanup loop")

        while self._running:
            try:
                await asyncio.sleep(self.cleanup_interval)

                # Cleanup old completed processes
                if len(self.completed_processes) > self.max_completed_history:
                    # Sort by timestamp and keep only the most recent
                    sorted_results = sorted(
                        self.completed_processes.items(),
                        key=lambda x: x[1].timestamp,
                        reverse=True,
                    )

                    # Keep only the most recent entries
                    keep_count = self.max_completed_history // 2
                    new_completed = dict(sorted_results[:keep_count])

                    removed_count = len(self.completed_processes) - len(new_completed)
                    self.completed_processes = new_completed

                    self.logger.info(
                        f"Cleaned up {removed_count} old consensus results"
                    )

            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")

        self.logger.info("Stopped consensus cleanup loop")

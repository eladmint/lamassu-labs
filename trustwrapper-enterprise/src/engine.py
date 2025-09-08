"""
Multi-Chain Consensus Engine
============================

Byzantine fault-tolerant consensus engine for universal AI verification
across multiple blockchain networks with weighted voting and timeout handling.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from core.interfaces import (
    ChainType,
    ChainVerificationResult,
    ConsensusConfig,
    ConsensusResult,
    IConsensusEngine,
    IUniversalChainAdapter,
    VerificationRequest,
    VerificationStatus,
)


class ConsensusPhase(Enum):
    """Phases of the consensus process."""

    INITIALIZATION = "initialization"
    VERIFICATION = "verification"
    VOTING = "voting"
    AGGREGATION = "aggregation"
    FINALIZATION = "finalization"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ConsensusState:
    """State tracking for a consensus request."""

    request_id: str
    request: VerificationRequest
    phase: ConsensusPhase
    participating_chains: set[ChainType]
    chain_results: dict[ChainType, ChainVerificationResult] = field(
        default_factory=dict
    )
    votes: dict[ChainType, dict[str, any]] = field(default_factory=dict)
    start_time: datetime = field(default_factory=datetime.utcnow)
    timeout_time: datetime | None = None
    errors: list[str] = field(default_factory=list)


class MultiChainConsensusEngine(IConsensusEngine):
    """
    Byzantine fault-tolerant consensus engine for multi-chain AI verification.

    Implements weighted voting, timeout handling, and consensus aggregation
    across multiple blockchain networks to ensure reliable AI verification.
    """

    def __init__(self, config: ConsensusConfig):
        """
        Initialize consensus engine.

        Args:
            config: Consensus configuration parameters
        """
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Chain adapters pool
        self.adapters: dict[ChainType, IUniversalChainAdapter] = {}

        # Active consensus requests
        self.active_requests: dict[str, ConsensusState] = {}

        # Performance statistics
        self.stats = {
            "total_requests": 0,
            "successful_consensus": 0,
            "failed_consensus": 0,
            "timeout_consensus": 0,
            "average_consensus_time": 0.0,
            "byzantine_faults_detected": 0,
        }

    async def verify_cross_chain(self, request: VerificationRequest) -> ConsensusResult:
        """
        Perform cross-chain AI verification with Byzantine fault tolerance.

        Args:
            request: Verification request with target chains

        Returns:
            ConsensusResult: Final consensus result
        """
        self.stats["total_requests"] += 1
        start_time = datetime.utcnow()

        # Initialize consensus state
        state = ConsensusState(
            request_id=request.request_id,
            request=request,
            phase=ConsensusPhase.INITIALIZATION,
            participating_chains=set(request.target_chains),
            timeout_time=start_time + timedelta(seconds=request.timeout_seconds),
        )

        self.active_requests[request.request_id] = state

        try:
            self.logger.info(
                f"Starting cross-chain verification for request {request.request_id} "
                f"across {len(request.target_chains)} chains"
            )

            # Phase 1: Initialization and validation
            if not await self._initialize_consensus(state):
                return self._create_failed_result(state, "Initialization failed")

            # Phase 2: Parallel verification across chains
            if not await self._execute_parallel_verification(state):
                return self._create_failed_result(state, "Verification phase failed")

            # Phase 3: Consensus voting
            if not await self._execute_consensus_voting(state):
                return self._create_failed_result(state, "Voting phase failed")

            # Phase 4: Aggregation and final consensus
            consensus_result = await self._aggregate_consensus(state)

            # Update statistics
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_stats(consensus_result.overall_status, execution_time)

            self.logger.info(
                f"Consensus completed for request {request.request_id}: "
                f"Status={consensus_result.overall_status.value}, "
                f"Score={consensus_result.consensus_score:.3f}, "
                f"Time={execution_time:.3f}s"
            )

            return consensus_result

        except TimeoutError:
            self.stats["timeout_consensus"] += 1
            return self._create_timeout_result(state)

        except Exception as e:
            self.logger.error(f"Consensus error for request {request.request_id}: {e}")
            return self._create_failed_result(state, str(e))

        finally:
            # Cleanup
            if request.request_id in self.active_requests:
                del self.active_requests[request.request_id]

    async def add_chain_adapter(self, adapter: IUniversalChainAdapter) -> bool:
        """
        Add blockchain adapter to consensus pool.

        Args:
            adapter: Chain adapter implementation

        Returns:
            bool: True if added successfully
        """
        try:
            chain_type = adapter.chain_type

            # Validate adapter is connected
            if not adapter.is_connected:
                self.logger.warning(f"Adapter for {chain_type.value} is not connected")
                return False

            self.adapters[chain_type] = adapter
            self.logger.info(f"Added {chain_type.value} adapter to consensus pool")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add adapter: {e}")
            return False

    async def remove_chain_adapter(self, chain_type: ChainType) -> bool:
        """
        Remove blockchain adapter from consensus pool.

        Args:
            chain_type: Type of chain to remove

        Returns:
            bool: True if removed successfully
        """
        if chain_type in self.adapters:
            del self.adapters[chain_type]
            self.logger.info(f"Removed {chain_type.value} adapter from consensus pool")
            return True
        else:
            self.logger.warning(f"Adapter for {chain_type.value} not found")
            return False

    async def get_active_chains(self) -> list[ChainType]:
        """
        Get list of active blockchain adapters.

        Returns:
            List[ChainType]: Active chain types
        """
        return list(self.adapters.keys())

    async def _initialize_consensus(self, state: ConsensusState) -> bool:
        """
        Initialize consensus process and validate requirements.

        Args:
            state: Consensus state to initialize

        Returns:
            bool: True if initialization successful
        """
        state.phase = ConsensusPhase.INITIALIZATION

        try:
            # Check minimum participating chains
            available_chains = set(self.adapters.keys())
            requested_chains = state.participating_chains

            valid_chains = available_chains.intersection(requested_chains)

            if len(valid_chains) < self.config.min_participating_chains:
                state.errors.append(
                    f"Insufficient chains: {len(valid_chains)} available, "
                    f"{self.config.min_participating_chains} required"
                )
                return False

            # Update participating chains to only include available ones
            state.participating_chains = valid_chains

            self.logger.info(
                f"Initialized consensus with {len(valid_chains)} participating chains: "
                f"{[chain.value for chain in valid_chains]}"
            )

            return True

        except Exception as e:
            state.errors.append(f"Initialization error: {e}")
            return False

    async def _execute_parallel_verification(self, state: ConsensusState) -> bool:
        """
        Execute verification across all participating chains in parallel.

        Args:
            state: Consensus state

        Returns:
            bool: True if verification phase successful
        """
        state.phase = ConsensusPhase.VERIFICATION

        try:
            # Create verification tasks for each chain
            tasks = []
            chain_adapters = []

            for chain_type in state.participating_chains:
                adapter = self.adapters.get(chain_type)
                if adapter and adapter.is_connected:
                    task = asyncio.create_task(self._verify_on_chain(adapter, state))
                    tasks.append(task)
                    chain_adapters.append(adapter)
                else:
                    self.logger.warning(
                        f"Adapter for {chain_type.value} not available or disconnected"
                    )

            if not tasks:
                state.errors.append("No valid chain adapters available")
                return False

            # Execute verifications with timeout
            timeout_seconds = (state.timeout_time - datetime.utcnow()).total_seconds()

            if timeout_seconds <= 0:
                state.errors.append("Request timeout during verification phase")
                return False

            # Wait for all verifications to complete
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True), timeout=timeout_seconds
            )

            # Process results
            successful_verifications = 0

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    chain_type = chain_adapters[i].chain_type
                    self.logger.error(
                        f"Verification failed on {chain_type.value}: {result}"
                    )
                    state.errors.append(f"{chain_type.value}: {result}")
                else:
                    successful_verifications += 1

            # Check if we have enough successful verifications
            min_required = max(1, len(state.participating_chains) // 2)

            if successful_verifications < min_required:
                state.errors.append(
                    f"Insufficient successful verifications: {successful_verifications} "
                    f"of {len(state.participating_chains)}"
                )
                return False

            self.logger.info(
                f"Verification phase completed: {successful_verifications} "
                f"successful verifications"
            )

            return True

        except TimeoutError:
            state.errors.append("Verification phase timeout")
            return False
        except Exception as e:
            state.errors.append(f"Verification phase error: {e}")
            return False

    async def _verify_on_chain(
        self, adapter: IUniversalChainAdapter, state: ConsensusState
    ) -> None:
        """
        Perform verification on a single chain.

        Args:
            adapter: Chain adapter to use
            state: Consensus state
        """
        try:
            result = await adapter.verify_ai_output(
                ai_agent_id=state.request.ai_agent_id,
                verification_data=state.request.verification_data,
            )

            state.chain_results[adapter.chain_type] = result

            self.logger.debug(
                f"Verification completed on {adapter.chain_type.value}: "
                f"Status={result.verification_status.value}, "
                f"Confidence={result.confidence_score:.3f}"
            )

        except Exception as e:
            self.logger.error(
                f"Chain verification error on {adapter.chain_type.value}: {e}"
            )
            raise

    async def _execute_consensus_voting(self, state: ConsensusState) -> bool:
        """
        Execute consensus voting phase.

        Args:
            state: Consensus state

        Returns:
            bool: True if voting phase successful
        """
        state.phase = ConsensusPhase.VOTING

        try:
            # For Phase 1, implement basic voting mechanism
            # In production, this would submit votes to smart contracts

            voting_tasks = []

            for chain_type, result in state.chain_results.items():
                adapter = self.adapters.get(chain_type)
                if adapter and adapter.is_connected:

                    # Create vote data
                    vote_data = {
                        "verification_status": result.verification_status.value,
                        "confidence_score": result.confidence_score,
                        "chain_weight": self.config.chain_weights.get(chain_type, 1.0),
                        "voter_id": f"{chain_type.value}_consensus_node",
                    }

                    # Submit consensus vote
                    task = asyncio.create_task(
                        adapter.submit_consensus_vote(
                            state.request.request_id, vote_data
                        )
                    )
                    voting_tasks.append((chain_type, task))

            if not voting_tasks:
                state.errors.append("No chains available for voting")
                return False

            # Wait for voting to complete
            for chain_type, task in voting_tasks:
                try:
                    tx_hash = await task
                    state.votes[chain_type] = {
                        "transaction_hash": tx_hash,
                        "submitted_at": datetime.utcnow(),
                    }

                except Exception as e:
                    self.logger.error(f"Voting failed on {chain_type.value}: {e}")
                    state.errors.append(f"Voting error on {chain_type.value}: {e}")

            # Check if we have enough votes
            if len(state.votes) < self.config.min_participating_chains:
                state.errors.append("Insufficient votes for consensus")
                return False

            self.logger.info(f"Voting phase completed with {len(state.votes)} votes")
            return True

        except Exception as e:
            state.errors.append(f"Voting phase error: {e}")
            return False

    async def _execute_advanced_consensus_voting(self, state: ConsensusState) -> bool:
        """
        Execute advanced consensus voting using BFT algorithms.

        Args:
            state: Consensus state

        Returns:
            bool: True if advanced voting phase successful
        """
        state.phase = ConsensusPhase.VOTING

        try:
            # Prepare consensus value from verification results
            consensus_value = {
                "request_id": state.request.request_id,
                "verification_results": {
                    chain.value: {
                        "status": result.verification_status.value,
                        "confidence": result.confidence_score,
                        "details": result.details,
                    }
                    for chain, result in state.chain_results.items()
                },
                "timestamp": datetime.utcnow().isoformat(),
            }

            # Select consensus algorithm based on requirements
            algorithm = self.advanced_engine.select_optimal_algorithm(
                num_validators=len(state.participating_chains),
                latency_requirement=1.0,  # 1 second target
                byzantine_assumption=0.33,
            )

            # Start advanced consensus
            validators = [
                f"{chain.value}_validator" for chain in state.participating_chains
            ]
            consensus_result = await self.reach_advanced_consensus(
                consensus_id=state.request.request_id,
                value=consensus_value,
                validators=validators,
                algorithm=algorithm,
                use_threshold_signatures=True,
            )

            # If using threshold signatures, collect partial signatures
            if consensus_result.get("status") == "in_progress":
                # Simulate validators creating partial signatures
                message = str(consensus_value).encode()

                for i, validator in enumerate(
                    validators[:3]
                ):  # First 3 validators sign
                    partial_sig = await self.create_threshold_signature(
                        consensus_id=state.request.request_id,
                        message=message,
                        signer_id=i + 1,
                        scheme="BLS",
                    )

                    if isinstance(partial_sig, dict) and partial_sig.get("signature"):
                        # Threshold signature completed
                        state.votes["threshold_signature"] = partial_sig
                        self.logger.info(
                            "Advanced consensus completed with threshold signature"
                        )
                        return True

            return True

        except Exception as e:
            state.errors.append(f"Advanced voting phase error: {e}")
            self.logger.error(f"Advanced consensus voting error: {e}")
            return False

    async def _aggregate_consensus(self, state: ConsensusState) -> ConsensusResult:
        """
        Aggregate verification results and determine final consensus.

        Args:
            state: Consensus state

        Returns:
            ConsensusResult: Final consensus result
        """
        state.phase = ConsensusPhase.AGGREGATION

        try:
            # Calculate weighted consensus score
            total_weight = 0.0
            verified_weight = 0.0
            confidence_sum = 0.0

            for chain_type, result in state.chain_results.items():
                weight = self.config.chain_weights.get(chain_type, 1.0)
                total_weight += weight
                confidence_sum += result.confidence_score * weight

                if result.verification_status == VerificationStatus.VERIFIED:
                    verified_weight += weight

            if total_weight == 0:
                return self._create_failed_result(
                    state, "No valid verification results"
                )

            # Calculate consensus metrics
            consensus_score = verified_weight / total_weight
            average_confidence = confidence_sum / total_weight

            # Determine overall status
            if consensus_score >= state.request.consensus_threshold:
                overall_status = VerificationStatus.VERIFIED
                self.stats["successful_consensus"] += 1
            elif consensus_score >= 0.3:  # Partial consensus
                overall_status = VerificationStatus.PENDING
            else:
                overall_status = VerificationStatus.REJECTED

            # Detect Byzantine faults
            if self._detect_byzantine_faults(state.chain_results):
                self.stats["byzantine_faults_detected"] += 1
                self.logger.warning(
                    f"Byzantine faults detected in request {state.request_id}"
                )

            # Create final result
            result = ConsensusResult(
                request_id=state.request.request_id,
                overall_status=overall_status,
                consensus_score=consensus_score,
                participating_chains=list(state.participating_chains),
                chain_results=list(state.chain_results.values()),
                consensus_reached_at=datetime.utcnow(),
                total_execution_time=(
                    datetime.utcnow() - state.start_time
                ).total_seconds(),
            )

            state.phase = ConsensusPhase.COMPLETED

            self.logger.info(
                f"Consensus aggregation completed: Score={consensus_score:.3f}, "
                f"Status={overall_status.value}"
            )

            return result

        except Exception as e:
            state.errors.append(f"Aggregation error: {e}")
            return self._create_failed_result(state, str(e))

    def _detect_byzantine_faults(
        self, results: dict[ChainType, ChainVerificationResult]
    ) -> bool:
        """
        Detect potential Byzantine faults in verification results.

        Args:
            results: Chain verification results

        Returns:
            bool: True if Byzantine faults detected
        """
        if len(results) < 3:
            return False  # Need at least 3 nodes to detect Byzantine faults

        # Check for significant confidence score variance
        confidence_scores = [r.confidence_score for r in results.values()]
        mean_confidence = sum(confidence_scores) / len(confidence_scores)

        # Count outliers (confidence scores significantly different from mean)
        outliers = 0
        for score in confidence_scores:
            if abs(score - mean_confidence) > 0.3:  # 30% threshold
                outliers += 1

        # Byzantine fault suspected if more than 1/3 are outliers
        byzantine_threshold = len(results) // 3
        return outliers > byzantine_threshold

    def _create_failed_result(
        self, state: ConsensusState, error_message: str
    ) -> ConsensusResult:
        """Create a failed consensus result."""
        state.phase = ConsensusPhase.FAILED
        self.stats["failed_consensus"] += 1

        return ConsensusResult(
            request_id=state.request.request_id,
            overall_status=VerificationStatus.ERROR,
            consensus_score=0.0,
            participating_chains=list(state.participating_chains),
            chain_results=list(state.chain_results.values()),
            consensus_reached_at=datetime.utcnow(),
            total_execution_time=(datetime.utcnow() - state.start_time).total_seconds(),
        )

    def _create_timeout_result(self, state: ConsensusState) -> ConsensusResult:
        """Create a timeout consensus result."""
        state.phase = ConsensusPhase.FAILED
        state.errors.append("Consensus timeout")

        return ConsensusResult(
            request_id=state.request.request_id,
            overall_status=VerificationStatus.ERROR,
            consensus_score=0.0,
            participating_chains=list(state.participating_chains),
            chain_results=list(state.chain_results.values()),
            consensus_reached_at=datetime.utcnow(),
            total_execution_time=state.request.timeout_seconds,
        )

    def _update_stats(self, status: VerificationStatus, execution_time: float) -> None:
        """Update performance statistics."""
        # Update average execution time
        total_requests = self.stats["total_requests"]
        current_avg = self.stats["average_consensus_time"]

        self.stats["average_consensus_time"] = (
            current_avg * (total_requests - 1) + execution_time
        ) / total_requests

    def get_consensus_stats(self) -> dict[str, any]:
        """Get consensus engine performance statistics."""
        total = self.stats["total_requests"]
        success_rate = 0.0

        if total > 0:
            success_rate = self.stats["successful_consensus"] / total

        return {
            "total_requests": total,
            "successful_consensus": self.stats["successful_consensus"],
            "failed_consensus": self.stats["failed_consensus"],
            "timeout_consensus": self.stats["timeout_consensus"],
            "success_rate": success_rate,
            "average_consensus_time": self.stats["average_consensus_time"],
            "byzantine_faults_detected": self.stats["byzantine_faults_detected"],
            "active_adapters": len(self.adapters),
            "active_requests": len(self.active_requests),
        }

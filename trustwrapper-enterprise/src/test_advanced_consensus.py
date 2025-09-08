"""
Test Suite for Advanced Consensus Mechanisms
============================================

Comprehensive tests for advanced Byzantine fault tolerance,
threshold signatures, and weighted consensus.
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

from consensus.advanced_bft import (
    AdvancedConsensusEngine,
    ConsensusMessage,
    ConsensusPhase,
    HotStuffConsensus,
    MessageType,
    PBFTConsensus,
    WeightedByzantineConsensus,
)
from consensus.engine import MultiChainConsensusEngine
from consensus.threshold_signatures import (
    SchnorrThreshold,
    SimplifiedBLSThreshold,
    ThresholdSignatureManager,
)
from core.interfaces import (
    ChainType,
    ChainVerificationResult,
    ConsensusConfig,
    VerificationRequest,
    VerificationStatus,
)


class TestPBFTConsensus:
    """Test Practical Byzantine Fault Tolerance consensus."""

    @pytest.fixture
    def pbft_consensus(self):
        """Create PBFT consensus instance."""
        return PBFTConsensus("node_0", 4)  # 4 nodes, tolerates 1 fault

    @pytest.mark.asyncio
    async def test_pbft_initialization(self, pbft_consensus):
        """Test PBFT initialization."""
        assert pbft_consensus.node_id == "node_0"
        assert pbft_consensus.total_nodes == 4
        assert pbft_consensus.f == 1  # (4-1)//3 = 1 fault tolerance
        assert pbft_consensus.state.phase == ConsensusPhase.PREPARE

    @pytest.mark.asyncio
    async def test_pbft_propose_as_leader(self, pbft_consensus):
        """Test proposal by leader node."""
        value = {"test": "data"}
        validators = ["node_0", "node_1", "node_2", "node_3"]

        proposal = await pbft_consensus.propose(value, validators)

        assert proposal.message_type == MessageType.PROPOSE
        assert proposal.sender_id == "node_0"
        assert proposal.content["value"] == value
        assert proposal.content["validators"] == validators

    @pytest.mark.asyncio
    async def test_pbft_propose_as_non_leader(self):
        """Test proposal by non-leader node (should fail)."""
        pbft = PBFTConsensus("node_1", 4)  # Not leader

        with pytest.raises(Exception, match="Only leader can propose"):
            await pbft.propose({"test": "data"}, ["node_0", "node_1"])

    @pytest.mark.asyncio
    async def test_pbft_handle_propose_message(self, pbft_consensus):
        """Test handling propose message."""
        # Create propose message from leader
        propose_msg = ConsensusMessage(
            message_type=MessageType.PROPOSE,
            view_number=0,
            sequence_number=0,
            sender_id="node_0",
            content={"value": {"test": "data"}},
        )

        # Handle propose message
        prepare_msg = await pbft_consensus.handle_message(propose_msg)

        assert prepare_msg is not None
        assert prepare_msg.message_type == MessageType.PREPARE
        assert pbft_consensus.state.phase == ConsensusPhase.PREPARE
        assert pbft_consensus.state.prepared_value == {"test": "data"}

    @pytest.mark.asyncio
    async def test_pbft_consensus_flow(self, pbft_consensus):
        """Test complete PBFT consensus flow."""
        # Step 1: Propose
        propose_msg = ConsensusMessage(
            message_type=MessageType.PROPOSE,
            view_number=0,
            sequence_number=0,
            sender_id="node_0",
            content={"value": {"test": "data"}},
        )

        prepare_msg = await pbft_consensus.handle_message(propose_msg)
        assert prepare_msg.message_type == MessageType.PREPARE

        # Step 2: Collect prepare messages (need 2f+1 = 3)
        for i in range(3):
            prepare = ConsensusMessage(
                message_type=MessageType.PREPARE,
                view_number=0,
                sequence_number=0,
                sender_id=f"node_{i}",
                content={"value_hash": propose_msg.hash()},
            )
            commit_msg = await pbft_consensus.handle_message(prepare)

            if i == 2:  # After 3rd prepare message
                assert commit_msg is not None
                assert commit_msg.message_type == MessageType.COMMIT
                assert pbft_consensus.state.phase == ConsensusPhase.COMMIT

        # Step 3: Collect commit messages (need 2f+1 = 3)
        for i in range(3):
            commit = ConsensusMessage(
                message_type=MessageType.COMMIT,
                view_number=0,
                sequence_number=0,
                sender_id=f"node_{i}",
                content={"prepared": True},
            )
            decision_msg = await pbft_consensus.handle_message(commit)

            if i == 2:  # After 3rd commit message
                assert decision_msg is not None
                assert decision_msg.message_type == MessageType.DECISION
                assert pbft_consensus.state.decided == True
                assert pbft_consensus.state.decided_value == {"test": "data"}

        # Check final decision
        decided, value = await pbft_consensus.check_decision()
        assert decided == True
        assert value == {"test": "data"}


class TestHotStuffConsensus:
    """Test HotStuff consensus algorithm."""

    @pytest.fixture
    def hotstuff_consensus(self):
        """Create HotStuff consensus instance."""
        return HotStuffConsensus("node_0", 4)

    @pytest.mark.asyncio
    async def test_hotstuff_initialization(self, hotstuff_consensus):
        """Test HotStuff initialization."""
        assert hotstuff_consensus.node_id == "node_0"
        assert hotstuff_consensus.total_nodes == 4
        assert hotstuff_consensus.f == 1
        assert hotstuff_consensus.generic_qc is None
        assert hotstuff_consensus.locked_qc is None

    @pytest.mark.asyncio
    async def test_hotstuff_propose_with_qc(self, hotstuff_consensus):
        """Test HotStuff proposal with quorum certificate."""
        # Set a generic QC
        hotstuff_consensus.generic_qc = {"view": 0, "type": "prepare", "votes": 3}

        value = {"test": "data"}
        validators = ["node_0", "node_1", "node_2", "node_3"]

        proposal = await hotstuff_consensus.propose(value, validators)

        assert proposal.content["qc"] == hotstuff_consensus.generic_qc

    @pytest.mark.asyncio
    async def test_hotstuff_quorum_formation(self, hotstuff_consensus):
        """Test HotStuff quorum certificate formation."""
        # Create a message
        msg = ConsensusMessage(
            message_type=MessageType.PREPARE,
            view_number=0,
            sequence_number=0,
            sender_id="node_0",
            content={"value": {"test": "data"}},
        )

        # Simulate 2f+1 = 3 votes
        for i in range(3):
            vote_msg = ConsensusMessage(
                message_type=MessageType.PREPARE,
                view_number=0,
                sequence_number=0,
                sender_id=f"node_{i}",
                content={"value": {"test": "data"}},
            )

            result = await hotstuff_consensus.handle_message(vote_msg)

            if i == 2:  # After 3rd vote
                assert result is not None
                assert result.message_type == MessageType.COMMIT
                assert hotstuff_consensus.generic_qc is not None
                assert hotstuff_consensus.generic_qc["votes"] == 3


class TestWeightedByzantineConsensus:
    """Test weighted Byzantine consensus."""

    @pytest.fixture
    def weighted_consensus(self):
        """Create weighted consensus instance."""
        node_weights = {"node_0": 10.0, "node_1": 8.0, "node_2": 6.0, "node_3": 4.0}
        return WeightedByzantineConsensus(node_weights)

    def test_weighted_consensus_initialization(self, weighted_consensus):
        """Test weighted consensus initialization."""
        assert weighted_consensus.total_weight == 28.0  # 10+8+6+4
        assert all(
            score == 1.0 for score in weighted_consensus.reputation_scores.values()
        )

    def test_weighted_quorum_calculation(self, weighted_consensus):
        """Test weighted quorum calculation."""
        # Test case 1: Majority by weight
        votes = [
            ("node_0", "approve"),  # weight 10
            ("node_1", "approve"),  # weight 8
            ("node_2", "reject"),  # weight 6
            ("node_3", "reject"),  # weight 4
        ]

        reached, value = weighted_consensus.calculate_weighted_quorum(votes)
        assert reached == False  # 18/28 < 2/3

        # Test case 2: Super-majority by weight
        votes = [
            ("node_0", "approve"),  # weight 10
            ("node_1", "approve"),  # weight 8
            ("node_2", "approve"),  # weight 6
            ("node_3", "reject"),  # weight 4
        ]

        reached, value = weighted_consensus.calculate_weighted_quorum(votes)
        assert reached == True  # 24/28 > 2/3
        assert value == "approve"

    def test_reputation_update(self, weighted_consensus):
        """Test reputation score updates."""
        # Test participation and agreement
        weighted_consensus.update_reputation("node_0", True, True)
        assert weighted_consensus.reputation_scores["node_0"] > 1.0

        # Test participation but disagreement
        weighted_consensus.update_reputation("node_1", True, False)
        assert weighted_consensus.reputation_scores["node_1"] < 1.0

        # Test non-participation
        weighted_consensus.update_reputation("node_2", False, False)
        assert weighted_consensus.reputation_scores["node_2"] < 1.0

    def test_effective_weight_calculation(self, weighted_consensus):
        """Test effective weight with reputation."""
        # Update reputations
        weighted_consensus.reputation_scores["node_0"] = 1.5
        weighted_consensus.reputation_scores["node_1"] = 0.8

        assert weighted_consensus.get_effective_weight("node_0") == 15.0  # 10 * 1.5
        assert weighted_consensus.get_effective_weight("node_1") == 6.4  # 8 * 0.8


class TestThresholdSignatures:
    """Test threshold signature schemes."""

    @pytest.fixture
    def bls_threshold(self):
        """Create BLS threshold signature scheme."""
        return SimplifiedBLSThreshold()

    @pytest.fixture
    def schnorr_threshold(self):
        """Create Schnorr threshold signature scheme."""
        return SchnorrThreshold()

    @pytest.fixture
    def signature_manager(self):
        """Create threshold signature manager."""
        return ThresholdSignatureManager()

    def test_bls_key_generation(self, bls_threshold):
        """Test BLS key share generation."""
        threshold = 3
        total = 5

        shares = bls_threshold.generate_key_shares(threshold, total)

        assert len(shares) == total
        assert all(share.threshold == threshold for share in shares)
        assert all(share.total_shares == total for share in shares)
        assert all(1 <= share.share_id <= total for share in shares)

    def test_bls_partial_signature(self, bls_threshold):
        """Test BLS partial signature creation."""
        # Generate key shares
        shares = bls_threshold.generate_key_shares(2, 3)
        message = b"test message"

        # Create partial signature
        partial = bls_threshold.create_partial_signature(message, shares[0])

        assert partial.signer_id == shares[0].share_id
        assert partial.signature_share is not None
        assert partial.metadata["scheme"] == "BLS"

    def test_bls_signature_combination(self, bls_threshold):
        """Test BLS signature combination."""
        # Generate key shares
        threshold = 2
        shares = bls_threshold.generate_key_shares(threshold, 3)
        message = b"test message"

        # Create partial signatures
        partials = []
        for i in range(threshold):
            partial = bls_threshold.create_partial_signature(message, shares[i])
            partials.append(partial)

        # Combine signatures
        combined = bls_threshold.combine_signatures(partials, threshold)

        assert combined is not None
        assert combined.threshold == threshold
        assert len(combined.signers) == threshold
        assert combined.scheme == "BLS"

    @pytest.mark.asyncio
    async def test_signature_manager_setup(self, signature_manager):
        """Test signature manager setup."""
        group_id = "test_group"
        threshold = 3
        total = 5

        shares = await signature_manager.setup_threshold_signing(
            group_id, threshold, total, scheme="BLS"
        )

        assert len(shares) == total
        assert group_id in signature_manager.key_shares

    @pytest.mark.asyncio
    async def test_signature_manager_flow(self, signature_manager):
        """Test complete threshold signature flow."""
        # Setup
        group_id = "test_group"
        threshold = 2
        total = 3
        message = b"consensus data"

        shares = await signature_manager.setup_threshold_signing(
            group_id, threshold, total, scheme="BLS"
        )

        # Create partial signatures
        for i in range(threshold):
            partial = await signature_manager.create_partial_signature(
                group_id, message, i + 1, scheme="BLS"
            )

        # Try to combine
        import hashlib

        msg_hash = hashlib.sha256(message).hexdigest()
        combined = await signature_manager.try_combine_signatures(
            group_id, msg_hash, scheme="BLS"
        )

        assert combined is not None
        assert combined.threshold == threshold


class TestAdvancedConsensusEngine:
    """Test advanced consensus engine integration."""

    @pytest.fixture
    def advanced_engine(self):
        """Create advanced consensus engine."""
        engine = AdvancedConsensusEngine()

        # Register algorithms
        pbft = PBFTConsensus("node_0", 4)
        hotstuff = HotStuffConsensus("node_0", 4)

        engine.register_algorithm("pbft", pbft)
        engine.register_algorithm("hotstuff", hotstuff)

        return engine

    @pytest.mark.asyncio
    async def test_algorithm_registration(self, advanced_engine):
        """Test consensus algorithm registration."""
        assert "pbft" in advanced_engine.algorithms
        assert "hotstuff" in advanced_engine.algorithms

    @pytest.mark.asyncio
    async def test_consensus_start(self, advanced_engine):
        """Test starting consensus."""
        consensus_id = "test_001"
        value = {"ai_data": "test"}
        validators = ["node_0", "node_1", "node_2", "node_3"]

        proposal = await advanced_engine.start_consensus(
            consensus_id, value, validators, algorithm="pbft"
        )

        assert proposal.message_type == MessageType.PROPOSE
        assert consensus_id in advanced_engine.active_consensus

    def test_algorithm_selection(self, advanced_engine):
        """Test optimal algorithm selection."""
        # Small group, low latency requirement
        algo = advanced_engine.select_optimal_algorithm(
            num_validators=4, latency_requirement=0.5, byzantine_assumption=0.25
        )
        assert algo == "hotstuff"

        # Standard BFT requirement
        algo = advanced_engine.select_optimal_algorithm(
            num_validators=10, latency_requirement=2.0, byzantine_assumption=0.30
        )
        assert algo == "pbft"


class TestIntegratedConsensus:
    """Test integrated consensus with advanced features."""

    @pytest.fixture
    def consensus_config(self):
        """Create consensus configuration."""
        config = ConsensusConfig(
            min_participating_chains=2,
            consensus_threshold=0.67,
            timeout_seconds=30,
            enable_advanced_consensus=True,
            chain_weights={
                ChainType.ETHEREUM: 2.0,
                ChainType.CARDANO: 1.5,
                ChainType.SOLANA: 1.0,
            },
        )
        return config

    @pytest.fixture
    def consensus_engine(self, consensus_config):
        """Create multi-chain consensus engine."""
        return MultiChainConsensusEngine(consensus_config)

    @pytest.mark.asyncio
    async def test_advanced_consensus_integration(self, consensus_engine):
        """Test advanced consensus integration."""
        # Set weighted consensus
        node_weights = {
            "ETHEREUM_validator": 2.0,
            "CARDANO_validator": 1.5,
            "SOLANA_validator": 1.0,
        }
        consensus_engine.set_weighted_consensus(node_weights)

        # Create mock adapters
        mock_adapters = {}
        for chain in [ChainType.ETHEREUM, ChainType.CARDANO, ChainType.SOLANA]:
            adapter = Mock()
            adapter.chain_type = chain
            adapter.is_connected = True
            adapter.verify_ai_output = AsyncMock(
                return_value=ChainVerificationResult(
                    chain_type=chain,
                    verification_status=VerificationStatus.VERIFIED,
                    confidence_score=0.95,
                    gas_used=1000,
                    transaction_hash=f"0x{chain.value}123",
                    details={"test": "data"},
                )
            )
            adapter.submit_consensus_vote = AsyncMock(
                return_value=f"0x{chain.value}vote"
            )
            mock_adapters[chain] = adapter
            await consensus_engine.add_chain_adapter(adapter)

        # Create verification request
        request = VerificationRequest(
            request_id="advanced_test_001",
            ai_agent_id="test_agent",
            verification_data={"model": "test", "output": "verified"},
            target_chains=[ChainType.ETHEREUM, ChainType.CARDANO, ChainType.SOLANA],
            consensus_threshold=0.67,
            timeout_seconds=10,
        )

        # Enable advanced consensus
        consensus_engine.use_advanced_consensus = True

        # Patch the advanced voting method to simulate success
        with patch.object(
            consensus_engine,
            "_execute_advanced_consensus_voting",
            AsyncMock(return_value=True),
        ):
            # Execute consensus
            result = await consensus_engine.verify_cross_chain(request)

        # Verify results
        assert result.overall_status == VerificationStatus.VERIFIED
        assert result.consensus_score >= 0.67
        assert len(result.chain_results) == 3

    def test_consensus_performance_stats(self, consensus_engine):
        """Test consensus performance statistics."""
        stats = consensus_engine.get_consensus_performance_stats()

        assert "basic_stats" in stats
        assert "algorithm_stats" in stats
        assert "signature_status" in stats
        assert "weighted_consensus" in stats


@pytest.mark.asyncio
async def test_end_to_end_advanced_consensus():
    """Test end-to-end advanced consensus flow."""
    # Create consensus engine with advanced features
    config = ConsensusConfig(
        min_participating_chains=3,
        consensus_threshold=0.67,
        timeout_seconds=30,
        enable_advanced_consensus=True,
        chain_weights={
            ChainType.ETHEREUM: 2.0,
            ChainType.CARDANO: 1.5,
            ChainType.SOLANA: 1.0,
            ChainType.BITCOIN: 1.0,
        },
    )

    engine = MultiChainConsensusEngine(config)

    # Set weighted consensus
    node_weights = {
        "ETHEREUM_validator": 2.0,
        "CARDANO_validator": 1.5,
        "SOLANA_validator": 1.0,
        "BITCOIN_validator": 1.0,
    }
    engine.set_weighted_consensus(node_weights)

    # Verify advanced algorithms are initialized
    assert len(engine.advanced_engine.algorithms) > 0
    assert engine.weighted_consensus is not None

    # Test algorithm selection
    algo = engine.advanced_engine.select_optimal_algorithm(
        num_validators=4, latency_requirement=1.0
    )
    assert algo in ["pbft", "hotstuff", "weighted"]

    print("✅ End-to-end advanced consensus test passed")


if __name__ == "__main__":
    # Run the demo test
    asyncio.run(test_end_to_end_advanced_consensus())

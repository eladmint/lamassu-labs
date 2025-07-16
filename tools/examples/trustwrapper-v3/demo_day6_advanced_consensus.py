#!/usr/bin/env python3
"""
TrustWrapper v3.0 Phase 1 - Day 6: Advanced Consensus Demo
=========================================================

Demonstrates the advanced Byzantine fault tolerance, threshold signatures,
and weighted consensus mechanisms implemented in Week 2.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root / "src" / "trustwrapper-v3"))

from adapters.bitcoin_adapter import BitcoinAdapter
from adapters.cardano_adapter import CardanoAdapter
from adapters.ethereum_adapter import EthereumAdapter
from adapters.solana_adapter import SolanaAdapter
from consensus.advanced_bft import (
    ConsensusMessage,
    HotStuffConsensus,
    MessageType,
    PBFTConsensus,
    WeightedByzantineConsensus,
)
from consensus.engine import MultiChainConsensusEngine
from consensus.threshold_signatures import (
    ThresholdSignatureManager,
)
from core.connection_manager import MultiChainConnectionManager
from core.interfaces import (
    ChainType,
    ConsensusConfig,
    VerificationRequest,
)


class AdvancedConsensusDemo:
    """Demonstrates advanced consensus mechanisms."""

    def __init__(self):
        self.engine = None
        self.adapters = {}
        self.connection_manager = None

    async def setup(self):
        """Setup advanced consensus system."""
        print("🚀 TrustWrapper v3.0 - Advanced Consensus Demo")
        print("=" * 60)

        # Create consensus configuration
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

        # Create consensus engine
        self.engine = MultiChainConsensusEngine(config)
        print("✅ Created multi-chain consensus engine with advanced features")

        # Setup weighted consensus
        node_weights = {
            "ETHEREUM_validator": 2.0,
            "CARDANO_validator": 1.5,
            "SOLANA_validator": 1.0,
            "BITCOIN_validator": 1.0,
        }
        self.engine.set_weighted_consensus(node_weights)
        print("✅ Initialized weighted Byzantine consensus")

        # Create connection manager
        self.connection_manager = MultiChainConnectionManager()

        # Create and add adapters
        adapters = [
            EthereumAdapter({"network": "mainnet"}),
            CardanoAdapter({"network": "mainnet"}),
            SolanaAdapter({"cluster": "mainnet-beta"}),
            BitcoinAdapter({"network": "mainnet"}),
        ]

        for adapter in adapters:
            await self.connection_manager.add_adapter(adapter)
            await self.engine.add_chain_adapter(adapter)
            self.adapters[adapter.chain_type] = adapter

        print(f"✅ Added {len(adapters)} blockchain adapters")

    async def demo_pbft_consensus(self):
        """Demonstrate PBFT consensus algorithm."""
        print("\n📋 PBFT Consensus Demo")
        print("-" * 40)

        # Create PBFT instance for demonstration
        pbft = PBFTConsensus("demo_node", 4)
        print(f"Created PBFT with {pbft.total_nodes} nodes (tolerates {pbft.f} faults)")

        # Simulate consensus flow
        value = {"ai_verification": "demo_data", "timestamp": "2025-06-26"}
        validators = ["node_0", "node_1", "node_2", "node_3"]

        # Leader proposes
        pbft.node_id = "node_0"  # Set as leader
        proposal = await pbft.propose(value, validators)
        print(f"✓ Leader proposed: {proposal.message_type.value}")

        # Simulate prepare phase
        prepare_count = 0
        for i in range(3):  # Need 2f+1 = 3 prepares
            msg = ConsensusMessage(
                message_type=MessageType.PREPARE,
                view_number=0,
                sequence_number=0,
                sender_id=f"node_{i}",
                content={"value_hash": proposal.hash()},
            )
            result = await pbft.handle_message(msg)
            prepare_count += 1

            if result and result.message_type == MessageType.COMMIT:
                print(f"✓ Prepare phase complete with {prepare_count} messages")
                break

        # Check decision
        decided, final_value = await pbft.check_decision()
        print(f"✓ PBFT consensus: {'DECIDED' if decided else 'PENDING'}")

    async def demo_hotstuff_consensus(self):
        """Demonstrate HotStuff consensus algorithm."""
        print("\n📋 HotStuff Consensus Demo")
        print("-" * 40)

        # Create HotStuff instance
        hotstuff = HotStuffConsensus("demo_node", 4)
        print("Created HotStuff with linear view-change complexity")

        # Simulate voting to form quorum certificate
        test_msg = ConsensusMessage(
            message_type=MessageType.PREPARE,
            view_number=0,
            sequence_number=0,
            sender_id="node_0",
            content={"value": {"test": "hotstuff_data"}},
        )

        # Collect votes
        vote_count = 0
        for i in range(3):  # Need 2f+1 = 3 votes
            vote = ConsensusMessage(
                message_type=MessageType.PREPARE,
                view_number=0,
                sequence_number=0,
                sender_id=f"node_{i}",
                content={"value": {"test": "hotstuff_data"}},
            )

            result = await hotstuff.handle_message(vote)
            vote_count += 1

            if result and result.message_type == MessageType.COMMIT:
                print(f"✓ Quorum certificate formed with {vote_count} votes")
                print(f"✓ QC details: {hotstuff.generic_qc}")
                break

    async def demo_weighted_consensus(self):
        """Demonstrate weighted Byzantine consensus."""
        print("\n📋 Weighted Byzantine Consensus Demo")
        print("-" * 40)

        # Create weighted consensus
        node_weights = {
            "validator_A": 10.0,
            "validator_B": 8.0,
            "validator_C": 6.0,
            "validator_D": 4.0,
        }

        weighted = WeightedByzantineConsensus(node_weights)
        print(f"Total weight: {weighted.total_weight}")
        print(f"Byzantine threshold: {weighted.get_weighted_fault_tolerance():.1f}")

        # Simulate weighted voting
        votes = [
            ("validator_A", "VERIFIED"),  # weight 10
            ("validator_B", "VERIFIED"),  # weight 8
            ("validator_C", "REJECTED"),  # weight 6
            ("validator_D", "VERIFIED"),  # weight 4
        ]

        reached, result = weighted.calculate_weighted_quorum(votes)

        print("\nVoting results:")
        for node, vote in votes:
            weight = weighted.get_effective_weight(node)
            print(f"  {node}: {vote} (weight: {weight})")

        print(f"\n✓ Consensus reached: {reached}")
        print(f"✓ Result: {result}")

        # Update reputation based on consensus
        for node, vote in votes:
            weighted.update_reputation(node, True, vote == result)

        print("\nUpdated reputation scores:")
        for node, score in weighted.reputation_scores.items():
            print(f"  {node}: {score:.2f}")

    async def demo_threshold_signatures(self):
        """Demonstrate threshold signature schemes."""
        print("\n🔐 Threshold Signatures Demo")
        print("-" * 40)

        # Create signature manager
        manager = ThresholdSignatureManager()

        # Setup BLS threshold signing (3-of-5)
        group_id = "validators_001"
        threshold = 3
        total_signers = 5

        shares = await manager.setup_threshold_signing(
            group_id, threshold, total_signers, scheme="BLS"
        )
        print(f"✓ Generated {len(shares)} BLS key shares")
        print(f"✓ Threshold: {threshold}-of-{total_signers}")

        # Create message to sign
        message = b"AI verification consensus: model_xyz passed safety checks"
        print(f"\n📝 Message: {message.decode()}")

        # Simulate partial signatures
        print("\n🖊️ Creating partial signatures...")
        for signer_id in [1, 3, 4]:  # 3 out of 5 sign
            partial = await manager.create_partial_signature(
                group_id, message, signer_id, scheme="BLS"
            )
            print(f"  ✓ Validator {signer_id} signed")

        # Check signature status
        import hashlib

        msg_hash = hashlib.sha256(message).hexdigest()
        status = manager.get_signature_status(group_id, msg_hash)
        print(
            f"\n📊 Signature status: {status['partial_signatures']}/{status['threshold']}"
        )

        # Try to combine
        combined = await manager.try_combine_signatures(
            group_id, msg_hash, scheme="BLS"
        )
        if combined:
            print("✓ Threshold signature created!")
            print(f"  Signers: {combined.signers}")
            print(f"  Signature: {combined.signature[:32]}...")

    async def demo_integrated_consensus(self):
        """Demonstrate integrated advanced consensus."""
        print("\n🌐 Integrated Advanced Consensus Demo")
        print("-" * 40)

        # Create verification request
        request = VerificationRequest(
            request_id="advanced_demo_001",
            ai_agent_id="trustwrapper_demo",
            verification_data={
                "model": "gpt-4",
                "output": "AI trading decision: BUY ETH @ $2,500",
                "confidence": 0.95,
            },
            target_chains=[ChainType.ETHEREUM, ChainType.CARDANO, ChainType.SOLANA],
            consensus_threshold=0.67,
            timeout_seconds=30,
        )

        print("📋 Verification Request:")
        print(f"  AI Agent: {request.ai_agent_id}")
        print(f"  Target Chains: {[c.value for c in request.target_chains]}")
        print(f"  Consensus Threshold: {request.consensus_threshold}")

        # Select optimal algorithm
        algorithm = self.engine.advanced_engine.select_optimal_algorithm(
            num_validators=len(request.target_chains),
            latency_requirement=1.0,
            byzantine_assumption=0.33,
        )
        print(f"\n🎯 Selected algorithm: {algorithm}")

        # Start advanced consensus
        validators = [f"{chain.value}_validator" for chain in request.target_chains]
        consensus_result = await self.engine.reach_advanced_consensus(
            consensus_id=request.request_id,
            value=request.verification_data,
            validators=validators,
            algorithm=algorithm,
            use_threshold_signatures=True,
        )

        print("\n✓ Advanced consensus started:")
        print(f"  Status: {consensus_result['status']}")
        print(f"  Algorithm: {consensus_result['algorithm']}")
        print(f"  Validators: {len(consensus_result['validators'])}")

        # Demonstrate performance stats
        print("\n📊 Consensus Performance Statistics:")
        stats = self.engine.get_consensus_performance_stats()
        print(f"  Algorithm Stats: {stats['algorithm_stats']}")
        print(
            f"  Weighted Consensus: {'Enabled' if stats['weighted_consensus']['enabled'] else 'Disabled'}"
        )
        print(f"  Total Weight: {stats['weighted_consensus']['total_weight']}")

    async def run_demo(self):
        """Run the complete advanced consensus demo."""
        try:
            # Setup
            await self.setup()

            # Run demos
            await self.demo_pbft_consensus()
            await self.demo_hotstuff_consensus()
            await self.demo_weighted_consensus()
            await self.demo_threshold_signatures()
            await self.demo_integrated_consensus()

            # Summary
            print("\n" + "=" * 60)
            print("🎉 Advanced Consensus Demo Complete!")
            print("\n📋 Summary:")
            print("  ✅ PBFT consensus with 3-phase protocol")
            print("  ✅ HotStuff with linear view-change")
            print("  ✅ Weighted Byzantine consensus with reputation")
            print("  ✅ Threshold signatures (BLS & Schnorr)")
            print("  ✅ Integrated multi-chain consensus")
            print("\n🚀 Week 2 Day 6: Advanced Consensus COMPLETE")

        except Exception as e:
            print(f"\n❌ Demo error: {e}")
            import traceback

            traceback.print_exc()


async def main():
    """Main entry point."""
    demo = AdvancedConsensusDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())

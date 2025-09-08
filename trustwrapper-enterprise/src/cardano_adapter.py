"""
Cardano Blockchain Adapter
==========================

Universal chain adapter implementation for Cardano network using PyCardano
for TrustWrapper v3.0 verification platform.
"""

import json
import logging
from datetime import datetime
from typing import Any

try:
    from pycardano import *

    PYCARDANO_AVAILABLE = True
except ImportError:
    PYCARDANO_AVAILABLE = False
    print("Warning: PyCardano not available, using mock adapter")

from core.interfaces import (
    ChainMetrics,
    ChainType,
    ChainVerificationResult,
    IUniversalChainAdapter,
    VerificationStatus,
)


class CardanoAdapter(IUniversalChainAdapter):
    """
    Universal Cardano blockchain adapter.

    Provides Cardano network integration for AI verification with native
    support for Plutus smart contracts and UTXO model verification.
    """

    def __init__(
        self,
        network: str = "mainnet",
        api_url: str | None = None,
        api_key: str | None = None,
        wallet_seed: str | None = None,
    ):
        """
        Initialize Cardano adapter.

        Args:
            network: Cardano network (mainnet, testnet, preview)
            api_url: Blockfrost API URL (optional)
            api_key: Blockfrost API key (optional)
            wallet_seed: Wallet seed phrase for transactions (optional)
        """
        self._chain_type = ChainType.CARDANO
        self.network = network
        self.api_url = api_url
        self.api_key = api_key
        self.wallet_seed = wallet_seed

        self.context: Any | None = None
        self.wallet: Any | None = None
        self.logger = logging.getLogger(f"{__name__}.cardano")

        # Network configurations
        self._network_configs = {
            "mainnet": {
                "network_id": 1,
                "magic": 764824073,
                "name": "Cardano Mainnet",
                "explorer": "https://cardanoscan.io",
            },
            "testnet": {
                "network_id": 0,
                "magic": 1097911063,
                "name": "Cardano Testnet",
                "explorer": "https://testnet.cardanoscan.io",
            },
            "preview": {
                "network_id": 0,
                "magic": 2,
                "name": "Cardano Preview",
                "explorer": "https://preview.cardanoscan.io",
            },
        }

        self._verification_stats = {
            "total_verifications": 0,
            "successful_verifications": 0,
            "failed_verifications": 0,
            "average_tx_fee": 0,
        }

    @property
    def chain_type(self) -> ChainType:
        """Return the blockchain type this adapter handles."""
        return self._chain_type

    @property
    def is_connected(self) -> bool:
        """Check if adapter is connected to Cardano network."""
        if not PYCARDANO_AVAILABLE:
            return False

        try:
            return self.context is not None
        except Exception:
            return False

    async def connect(self) -> bool:
        """
        Connect to Cardano network.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if not PYCARDANO_AVAILABLE:
            self.logger.warning("PyCardano not available, using mock connection")
            return True  # Mock connection for demo purposes

        try:
            # Initialize Cardano context
            if self.api_url and self.api_key:
                # Use Blockfrost API
                self.context = BlockFrostChainContext(
                    self.api_key, base_url=self.api_url
                )
            else:
                # Use mock context for demo
                self.logger.info("Using mock Cardano context for demo")
                self.context = "mock_context"

            # Initialize wallet if seed provided
            if self.wallet_seed and PYCARDANO_AVAILABLE:
                try:
                    # Create wallet from seed phrase
                    self.wallet = HDWallet.from_mnemonic(self.wallet_seed)
                    self.logger.info("Initialized Cardano wallet")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize wallet: {e}")

            self.logger.info(f"Connected to Cardano {self.network}")
            return True

        except Exception as e:
            self.logger.error(f"Connection error for Cardano: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Cardano network."""
        self.context = None
        self.wallet = None
        self.logger.info("Disconnected from Cardano")

    async def get_chain_metrics(self) -> ChainMetrics:
        """
        Get current Cardano blockchain metrics.

        Returns:
            ChainMetrics: Current chain performance data
        """
        if not self.context:
            raise ConnectionError("Not connected to Cardano")

        try:
            # For demo purposes, return simulated metrics
            # In production, these would come from Blockfrost API or node

            current_epoch = 450  # Simulated current epoch
            slot_length = 1.0  # Cardano slot length in seconds

            # Simulated metrics
            block_height = current_epoch * 21600 + 15000  # Simulated block
            finality_time = 15.0  # Cardano finality time (15-20 seconds typical)

            return ChainMetrics(
                chain_id=self.network,
                block_height=block_height,
                block_time=slot_length,
                gas_price=None,  # Cardano uses fixed fee structure
                network_hashrate=None,  # Not applicable to PoS
                active_validators=3000,  # Approximate active stake pools
                finality_time=finality_time,
                last_updated=datetime.utcnow(),
            )

        except Exception as e:
            self.logger.error(f"Failed to get Cardano metrics: {e}")
            raise

    async def verify_ai_output(
        self, ai_agent_id: str, verification_data: dict[str, Any]
    ) -> ChainVerificationResult:
        """
        Verify AI output on Cardano blockchain.

        Args:
            ai_agent_id: Unique identifier for AI agent
            verification_data: Data to verify

        Returns:
            ChainVerificationResult: Verification result for Cardano
        """
        start_time = datetime.utcnow()

        try:
            self._verification_stats["total_verifications"] += 1

            # For Phase 1, implement basic verification logic
            # In production, this would use Plutus smart contracts

            # Create Cardano-specific verification hash
            verification_hash = self._calculate_verification_hash(verification_data)
            confidence_score = self._calculate_confidence_score(verification_data)

            # Determine verification status based on confidence
            if confidence_score >= 0.8:
                status = VerificationStatus.VERIFIED
            elif confidence_score >= 0.6:
                status = VerificationStatus.PENDING
            else:
                status = VerificationStatus.REJECTED

            # For Phase 1, simulate transaction without actual submission
            tx_hash = f"cardano_tx_{verification_hash[:32]}"
            block_number = (await self.get_chain_metrics()).block_height
            tx_fee = 0.17  # Typical Cardano transaction fee in ADA

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            if status == VerificationStatus.VERIFIED:
                self._verification_stats["successful_verifications"] += 1
            else:
                self._verification_stats["failed_verifications"] += 1

            # Update average transaction fee
            total_fee = (
                self._verification_stats["average_tx_fee"]
                * (self._verification_stats["total_verifications"] - 1)
                + tx_fee
            )
            self._verification_stats["average_tx_fee"] = (
                total_fee / self._verification_stats["total_verifications"]
            )

            result = ChainVerificationResult(
                chain_type=self._chain_type,
                transaction_hash=tx_hash,
                block_number=block_number,
                verification_status=status,
                confidence_score=confidence_score,
                gas_used=int(tx_fee * 1000000),  # Convert ADA to lovelace
                execution_time=execution_time,
                error_message=None,
                verified_at=datetime.utcnow(),
            )

            self.logger.info(
                f"Cardano verification complete: "
                f"Status={status.value}, Confidence={confidence_score:.3f}, "
                f"Time={execution_time:.3f}s, Fee={tx_fee:.2f} ADA"
            )

            return result

        except Exception as e:
            self._verification_stats["failed_verifications"] += 1
            execution_time = (datetime.utcnow() - start_time).total_seconds()

            self.logger.error(f"Cardano verification failed: {e}")

            return ChainVerificationResult(
                chain_type=self._chain_type,
                transaction_hash=None,
                block_number=None,
                verification_status=VerificationStatus.ERROR,
                confidence_score=0.0,
                gas_used=0,
                execution_time=execution_time,
                error_message=str(e),
                verified_at=datetime.utcnow(),
            )

    async def submit_consensus_vote(
        self, request_id: str, consensus_data: dict[str, Any]
    ) -> str:
        """
        Submit consensus vote to Cardano blockchain.

        Args:
            request_id: Unique request identifier
            consensus_data: Consensus voting data

        Returns:
            str: Transaction hash of submitted vote
        """
        if not self.context:
            raise ConnectionError("Not connected to Cardano")

        try:
            # For Phase 1, simulate consensus vote submission
            vote_hash = self._calculate_vote_hash(request_id, consensus_data)

            # In production, this would create and submit a Plutus transaction
            tx_hash = f"cardano_vote_{vote_hash[:32]}"

            self.logger.info(f"Cardano consensus vote submitted: {tx_hash}")
            return tx_hash

        except Exception as e:
            self.logger.error(f"Failed to submit Cardano consensus vote: {e}")
            raise

    async def get_consensus_votes(self, request_id: str) -> list[dict[str, Any]]:
        """
        Retrieve consensus votes for a request from Cardano.

        Args:
            request_id: Unique request identifier

        Returns:
            List[Dict]: List of consensus votes from Cardano
        """
        if not self.context:
            raise ConnectionError("Not connected to Cardano")

        try:
            # For Phase 1, return simulated consensus votes
            # In production, this would query Plutus contract state

            simulated_votes = [
                {
                    "voter_address": "addr1qxy2lpan99fcnhhyq4...lkn6zvzx8awej",
                    "vote": "verified",
                    "confidence": 0.92,
                    "timestamp": datetime.utcnow().isoformat(),
                    "epoch": (await self.get_chain_metrics()).block_height // 21600,
                    "stake_weight": 1.5,  # Stake-weighted voting
                }
            ]

            self.logger.info(
                f"Retrieved {len(simulated_votes)} Cardano consensus votes "
                f"for request {request_id}"
            )

            return simulated_votes

        except Exception as e:
            self.logger.error(f"Failed to get Cardano consensus votes: {e}")
            raise

    def get_verification_stats(self) -> dict[str, Any]:
        """Get verification statistics for Cardano adapter."""
        total = self._verification_stats["total_verifications"]
        success_rate = 0.0

        if total > 0:
            success_rate = self._verification_stats["successful_verifications"] / total

        return {
            "chain_type": self._chain_type.value,
            "total_verifications": total,
            "successful_verifications": self._verification_stats[
                "successful_verifications"
            ],
            "failed_verifications": self._verification_stats["failed_verifications"],
            "success_rate": success_rate,
            "average_tx_fee_ada": self._verification_stats["average_tx_fee"],
            "network": self.network,
        }

    def _calculate_verification_hash(self, verification_data: dict[str, Any]) -> str:
        """Calculate hash for verification data using Cardano-specific method."""
        import hashlib

        # Create deterministic hash with Cardano-specific prefix
        data_str = json.dumps(verification_data, sort_keys=True)
        cardano_data = f"CARDANO_VERIFICATION:{data_str}"
        return hashlib.blake2b(cardano_data.encode(), digest_size=32).hexdigest()

    def _calculate_confidence_score(self, verification_data: dict[str, Any]) -> float:
        """Calculate confidence score for Cardano verification."""
        # Base confidence for Cardano's deterministic nature
        score = 0.85

        # Adjust based on data completeness
        required_fields = ["ai_output", "input_data", "model_id"]
        present_fields = sum(
            1 for field in required_fields if field in verification_data
        )
        completeness_score = present_fields / len(required_fields)

        # Cardano bonus for UTXO model determinism
        cardano_bonus = 0.05

        # Combine scores
        final_score = (score + completeness_score + cardano_bonus) / 2.05
        return min(max(final_score, 0.0), 1.0)

    def _calculate_vote_hash(
        self, request_id: str, consensus_data: dict[str, Any]
    ) -> str:
        """Calculate hash for Cardano consensus vote."""
        import hashlib

        # Create deterministic hash for vote
        vote_data = {
            "request_id": request_id,
            "consensus_data": consensus_data,
            "chain": "cardano",
            "network": self.network,
            "timestamp": datetime.utcnow().isoformat(),
        }

        data_str = json.dumps(vote_data, sort_keys=True)
        return hashlib.blake2b(data_str.encode(), digest_size=32).hexdigest()

    def get_network_info(self) -> dict[str, Any]:
        """Get Cardano network information."""
        config = self._network_configs.get(self.network, {})
        return {
            "network": self.network,
            "network_id": config.get("network_id"),
            "magic": config.get("magic"),
            "name": config.get("name", "Unknown Network"),
            "explorer": config.get("explorer"),
            "consensus": "Ouroboros Proof of Stake",
            "native_token": "ADA",
            "supports_smart_contracts": True,
            "plutus_version": "V2",
        }

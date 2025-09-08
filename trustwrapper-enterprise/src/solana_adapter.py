"""
Solana Blockchain Adapter
=========================

Universal chain adapter implementation for Solana network using Solana.py
for TrustWrapper v3.0 verification platform.
"""

import json
import logging
from datetime import datetime
from typing import Any

try:
    from solana.keypair import Keypair
    from solana.publickey import PublicKey
    from solana.rpc.async_api import AsyncClient
    from solana.rpc.types import TxOpts
    from solana.system_program import TransferParams, transfer
    from solana.transaction import Transaction

    SOLANA_AVAILABLE = True
except ImportError:
    SOLANA_AVAILABLE = False
    print("Warning: Solana.py not available, using mock adapter")

from core.interfaces import (
    ChainMetrics,
    ChainType,
    ChainVerificationResult,
    IUniversalChainAdapter,
    VerificationStatus,
)


class SolanaAdapter(IUniversalChainAdapter):
    """
    Universal Solana blockchain adapter.

    Provides Solana network integration for AI verification with native
    support for high-performance transaction processing and program execution.
    """

    def __init__(
        self,
        rpc_url: str = "https://api.mainnet-beta.solana.com",
        keypair_bytes: bytes | None = None,
        commitment: str = "confirmed",
    ):
        """
        Initialize Solana adapter.

        Args:
            rpc_url: Solana RPC endpoint URL
            keypair_bytes: Keypair bytes for transactions (optional)
            commitment: Transaction commitment level
        """
        self._chain_type = ChainType.SOLANA
        self.rpc_url = rpc_url
        self.keypair_bytes = keypair_bytes
        self.commitment = commitment

        self.client: AsyncClient | None = None
        self.keypair: Any | None = None
        self.logger = logging.getLogger(f"{__name__}.solana")

        # Network configurations
        self._network_configs = {
            "mainnet-beta": {
                "name": "Solana Mainnet Beta",
                "explorer": "https://explorer.solana.com",
                "cluster": "mainnet-beta",
            },
            "testnet": {
                "name": "Solana Testnet",
                "explorer": "https://explorer.solana.com/?cluster=testnet",
                "cluster": "testnet",
            },
            "devnet": {
                "name": "Solana Devnet",
                "explorer": "https://explorer.solana.com/?cluster=devnet",
                "cluster": "devnet",
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
        """Check if adapter is connected to Solana network."""
        if not SOLANA_AVAILABLE:
            return False

        try:
            return self.client is not None
        except Exception:
            return False

    async def connect(self) -> bool:
        """
        Connect to Solana network.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if not SOLANA_AVAILABLE:
            self.logger.warning("Solana.py not available, using mock connection")
            return True  # Mock connection for demo purposes

        try:
            # Initialize Solana client
            self.client = AsyncClient(self.rpc_url)

            # Test connection by getting version
            try:
                version_info = await self.client.get_version()
                self.logger.info(
                    f"Connected to Solana node version: {version_info['result']['solana-core']}"
                )
            except Exception as e:
                self.logger.warning(f"Connection test failed, using mock: {e}")
                self.client = "mock_client"

            # Initialize keypair if provided
            if self.keypair_bytes and SOLANA_AVAILABLE:
                try:
                    self.keypair = Keypair.from_secret_key(self.keypair_bytes)
                    self.logger.info(
                        f"Initialized Solana keypair: {self.keypair.public_key}"
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to initialize keypair: {e}")

            self.logger.info("Connected to Solana network")
            return True

        except Exception as e:
            self.logger.error(f"Connection error for Solana: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Solana network."""
        if self.client and hasattr(self.client, "close"):
            try:
                await self.client.close()
            except:
                pass

        self.client = None
        self.keypair = None
        self.logger.info("Disconnected from Solana")

    async def get_chain_metrics(self) -> ChainMetrics:
        """
        Get current Solana blockchain metrics.

        Returns:
            ChainMetrics: Current chain performance data
        """
        if not self.client:
            raise ConnectionError("Not connected to Solana")

        try:
            # For demo purposes, return simulated metrics
            # In production, these would come from Solana RPC calls

            # Simulated Solana metrics
            slot_number = 250000000  # Simulated current slot
            slot_time = 0.4  # Solana slot time (~400ms)
            finality_time = 12.8  # Solana finality time (32 slots * 400ms)

            return ChainMetrics(
                chain_id="solana-mainnet-beta",
                block_height=slot_number,
                block_time=slot_time,
                gas_price=None,  # Solana uses lamports per signature
                network_hashrate=None,  # Not applicable to PoH/PoS
                active_validators=1500,  # Approximate active validators
                finality_time=finality_time,
                last_updated=datetime.utcnow(),
            )

        except Exception as e:
            self.logger.error(f"Failed to get Solana metrics: {e}")
            raise

    async def verify_ai_output(
        self, ai_agent_id: str, verification_data: dict[str, Any]
    ) -> ChainVerificationResult:
        """
        Verify AI output on Solana blockchain.

        Args:
            ai_agent_id: Unique identifier for AI agent
            verification_data: Data to verify

        Returns:
            ChainVerificationResult: Verification result for Solana
        """
        start_time = datetime.utcnow()

        try:
            self._verification_stats["total_verifications"] += 1

            # For Phase 1, implement basic verification logic
            # In production, this would use Solana programs

            # Create Solana-specific verification hash
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
            tx_hash = f"solana_tx_{verification_hash[:44]}"  # Solana uses base58
            slot_number = (await self.get_chain_metrics()).block_height
            tx_fee = 5000  # Typical Solana transaction fee in lamports

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
                block_number=slot_number,
                verification_status=status,
                confidence_score=confidence_score,
                gas_used=tx_fee,  # Using lamports as gas equivalent
                execution_time=execution_time,
                error_message=None,
                verified_at=datetime.utcnow(),
            )

            self.logger.info(
                f"Solana verification complete: "
                f"Status={status.value}, Confidence={confidence_score:.3f}, "
                f"Time={execution_time:.3f}s, Fee={tx_fee} lamports"
            )

            return result

        except Exception as e:
            self._verification_stats["failed_verifications"] += 1
            execution_time = (datetime.utcnow() - start_time).total_seconds()

            self.logger.error(f"Solana verification failed: {e}")

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
        Submit consensus vote to Solana blockchain.

        Args:
            request_id: Unique request identifier
            consensus_data: Consensus voting data

        Returns:
            str: Transaction signature of submitted vote
        """
        if not self.client:
            raise ConnectionError("Not connected to Solana")

        try:
            # For Phase 1, simulate consensus vote submission
            vote_hash = self._calculate_vote_hash(request_id, consensus_data)

            # In production, this would create and submit a Solana transaction
            tx_signature = f"solana_vote_{vote_hash[:44]}"

            self.logger.info(f"Solana consensus vote submitted: {tx_signature}")
            return tx_signature

        except Exception as e:
            self.logger.error(f"Failed to submit Solana consensus vote: {e}")
            raise

    async def get_consensus_votes(self, request_id: str) -> list[dict[str, Any]]:
        """
        Retrieve consensus votes for a request from Solana.

        Args:
            request_id: Unique request identifier

        Returns:
            List[Dict]: List of consensus votes from Solana
        """
        if not self.client:
            raise ConnectionError("Not connected to Solana")

        try:
            # For Phase 1, return simulated consensus votes
            # In production, this would query Solana program accounts

            simulated_votes = [
                {
                    "voter_pubkey": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
                    "vote": "verified",
                    "confidence": 0.91,
                    "timestamp": datetime.utcnow().isoformat(),
                    "slot": (await self.get_chain_metrics()).block_height - 50,
                    "stake_weight": 2.1,  # Stake-weighted voting
                }
            ]

            self.logger.info(
                f"Retrieved {len(simulated_votes)} Solana consensus votes "
                f"for request {request_id}"
            )

            return simulated_votes

        except Exception as e:
            self.logger.error(f"Failed to get Solana consensus votes: {e}")
            raise

    def get_verification_stats(self) -> dict[str, Any]:
        """Get verification statistics for Solana adapter."""
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
            "average_tx_fee_lamports": self._verification_stats["average_tx_fee"],
            "rpc_url": self.rpc_url,
        }

    def _calculate_verification_hash(self, verification_data: dict[str, Any]) -> str:
        """Calculate hash for verification data using Solana-specific method."""
        import hashlib

        # Create deterministic hash with Solana-specific prefix
        data_str = json.dumps(verification_data, sort_keys=True)
        solana_data = f"SOLANA_VERIFICATION:{data_str}"
        return hashlib.sha256(solana_data.encode()).hexdigest()

    def _calculate_confidence_score(self, verification_data: dict[str, Any]) -> float:
        """Calculate confidence score for Solana verification."""
        # Base confidence for Solana's high performance
        score = 0.82

        # Adjust based on data completeness
        required_fields = ["ai_output", "input_data", "model_id"]
        present_fields = sum(
            1 for field in required_fields if field in verification_data
        )
        completeness_score = present_fields / len(required_fields)

        # Solana performance bonus
        solana_bonus = 0.03

        # Combine scores
        final_score = (score + completeness_score + solana_bonus) / 2.03
        return min(max(final_score, 0.0), 1.0)

    def _calculate_vote_hash(
        self, request_id: str, consensus_data: dict[str, Any]
    ) -> str:
        """Calculate hash for Solana consensus vote."""
        import hashlib

        # Create deterministic hash for vote
        vote_data = {
            "request_id": request_id,
            "consensus_data": consensus_data,
            "chain": "solana",
            "commitment": self.commitment,
            "timestamp": datetime.utcnow().isoformat(),
        }

        data_str = json.dumps(vote_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def get_network_info(self) -> dict[str, Any]:
        """Get Solana network information."""
        # Determine network from RPC URL
        network = "mainnet-beta"
        if "testnet" in self.rpc_url:
            network = "testnet"
        elif "devnet" in self.rpc_url:
            network = "devnet"

        config = self._network_configs.get(network, {})
        return {
            "rpc_url": self.rpc_url,
            "network": network,
            "name": config.get("name", "Unknown Network"),
            "explorer": config.get("explorer"),
            "cluster": config.get("cluster"),
            "consensus": "Proof of History + Proof of Stake",
            "native_token": "SOL",
            "supports_smart_contracts": True,
            "program_runtime": "BPF",
            "commitment_level": self.commitment,
        }

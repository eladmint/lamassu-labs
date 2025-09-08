"""
Bitcoin Blockchain Adapter
==========================

Universal chain adapter implementation for Bitcoin network using bitcoin-python
for TrustWrapper v3.0 verification platform.
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Any

try:
    import bitcoin
    from bitcoin import *

    BITCOIN_AVAILABLE = True
except ImportError:
    BITCOIN_AVAILABLE = False
    print("Warning: bitcoin-python not available, using mock adapter")

from core.interfaces import (
    ChainMetrics,
    ChainType,
    ChainVerificationResult,
    IUniversalChainAdapter,
    VerificationStatus,
)


class BitcoinAdapter(IUniversalChainAdapter):
    """
    Universal Bitcoin blockchain adapter.

    Provides Bitcoin network integration for AI verification with support
    for transaction-based verification and timelock mechanisms.
    """

    def __init__(
        self,
        network: str = "mainnet",
        rpc_url: str | None = None,
        rpc_user: str | None = None,
        rpc_password: str | None = None,
        private_key: str | None = None,
    ):
        """
        Initialize Bitcoin adapter.

        Args:
            network: Bitcoin network (mainnet, testnet, regtest)
            rpc_url: Bitcoin Core RPC URL (optional)
            rpc_user: RPC username (optional)
            rpc_password: RPC password (optional)
            private_key: Private key for transactions (optional)
        """
        self._chain_type = ChainType.BITCOIN
        self.network = network
        self.rpc_url = rpc_url
        self.rpc_user = rpc_user
        self.rpc_password = rpc_password
        self.private_key = private_key

        self.connection: Any | None = None
        self.address: str | None = None
        self.logger = logging.getLogger(f"{__name__}.bitcoin")

        # Network configurations
        self._network_configs = {
            "mainnet": {
                "name": "Bitcoin Mainnet",
                "explorer": "https://blockstream.info",
                "magic_bytes": "f9beb4d9",
                "port": 8333,
            },
            "testnet": {
                "name": "Bitcoin Testnet",
                "explorer": "https://blockstream.info/testnet",
                "magic_bytes": "0b110907",
                "port": 18333,
            },
            "regtest": {
                "name": "Bitcoin Regtest",
                "explorer": "localhost",
                "magic_bytes": "fabfb5da",
                "port": 18444,
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
        """Check if adapter is connected to Bitcoin network."""
        if not BITCOIN_AVAILABLE:
            return False

        try:
            return self.connection is not None
        except Exception:
            return False

    async def connect(self) -> bool:
        """
        Connect to Bitcoin network.

        Returns:
            bool: True if connection successful, False otherwise
        """
        if not BITCOIN_AVAILABLE:
            self.logger.warning("bitcoin-python not available, using mock connection")
            return True  # Mock connection for demo purposes

        try:
            # Set network for bitcoin library
            if self.network == "testnet":
                bitcoin.SelectParams("testnet")
            elif self.network == "regtest":
                bitcoin.SelectParams("regtest")
            else:
                bitcoin.SelectParams("mainnet")

            # Initialize connection (mock for demo)
            self.connection = "mock_bitcoin_connection"

            # Initialize address if private key provided
            if self.private_key and BITCOIN_AVAILABLE:
                try:
                    # Create address from private key
                    self.address = bitcoin.privkey_to_address(self.private_key)
                    self.logger.info(f"Initialized Bitcoin address: {self.address}")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize address: {e}")

            self.logger.info(f"Connected to Bitcoin {self.network}")
            return True

        except Exception as e:
            self.logger.error(f"Connection error for Bitcoin: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Bitcoin network."""
        self.connection = None
        self.address = None
        self.logger.info("Disconnected from Bitcoin")

    async def get_chain_metrics(self) -> ChainMetrics:
        """
        Get current Bitcoin blockchain metrics.

        Returns:
            ChainMetrics: Current chain performance data
        """
        if not self.connection:
            raise ConnectionError("Not connected to Bitcoin")

        try:
            # For demo purposes, return simulated metrics
            # In production, these would come from Bitcoin Core RPC

            # Simulated Bitcoin metrics
            block_height = 820000  # Simulated current block height
            block_time = 600.0  # Bitcoin target block time (10 minutes)
            finality_time = 3600.0  # Bitcoin finality time (~6 confirmations)

            # Simulated network hashrate (exahashes/second)
            network_hashrate = 450.0e18  # ~450 EH/s

            return ChainMetrics(
                chain_id=f"bitcoin-{self.network}",
                block_height=block_height,
                block_time=block_time,
                gas_price=None,  # Bitcoin uses fee per byte
                network_hashrate=network_hashrate,
                active_validators=None,  # Bitcoin uses miners, not validators
                finality_time=finality_time,
                last_updated=datetime.utcnow(),
            )

        except Exception as e:
            self.logger.error(f"Failed to get Bitcoin metrics: {e}")
            raise

    async def verify_ai_output(
        self, ai_agent_id: str, verification_data: dict[str, Any]
    ) -> ChainVerificationResult:
        """
        Verify AI output on Bitcoin blockchain.

        Args:
            ai_agent_id: Unique identifier for AI agent
            verification_data: Data to verify

        Returns:
            ChainVerificationResult: Verification result for Bitcoin
        """
        start_time = datetime.utcnow()

        try:
            self._verification_stats["total_verifications"] += 1

            # For Phase 1, implement basic verification logic
            # In production, this would use OP_RETURN or Lightning Network

            # Create Bitcoin-specific verification hash
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
            tx_hash = f"bitcoin_tx_{verification_hash[:64]}"
            block_number = (await self.get_chain_metrics()).block_height
            tx_fee = 15000  # Typical Bitcoin transaction fee in satoshis

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
                gas_used=tx_fee,  # Using satoshis as gas equivalent
                execution_time=execution_time,
                error_message=None,
                verified_at=datetime.utcnow(),
            )

            self.logger.info(
                f"Bitcoin verification complete: "
                f"Status={status.value}, Confidence={confidence_score:.3f}, "
                f"Time={execution_time:.3f}s, Fee={tx_fee} satoshis"
            )

            return result

        except Exception as e:
            self._verification_stats["failed_verifications"] += 1
            execution_time = (datetime.utcnow() - start_time).total_seconds()

            self.logger.error(f"Bitcoin verification failed: {e}")

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
        Submit consensus vote to Bitcoin blockchain.

        Args:
            request_id: Unique request identifier
            consensus_data: Consensus voting data

        Returns:
            str: Transaction hash of submitted vote
        """
        if not self.connection:
            raise ConnectionError("Not connected to Bitcoin")

        try:
            # For Phase 1, simulate consensus vote submission
            vote_hash = self._calculate_vote_hash(request_id, consensus_data)

            # In production, this would create an OP_RETURN transaction
            tx_hash = f"bitcoin_vote_{vote_hash[:64]}"

            self.logger.info(f"Bitcoin consensus vote submitted: {tx_hash}")
            return tx_hash

        except Exception as e:
            self.logger.error(f"Failed to submit Bitcoin consensus vote: {e}")
            raise

    async def get_consensus_votes(self, request_id: str) -> list[dict[str, Any]]:
        """
        Retrieve consensus votes for a request from Bitcoin.

        Args:
            request_id: Unique request identifier

        Returns:
            List[Dict]: List of consensus votes from Bitcoin
        """
        if not self.connection:
            raise ConnectionError("Not connected to Bitcoin")

        try:
            # For Phase 1, return simulated consensus votes
            # In production, this would scan OP_RETURN data

            simulated_votes = [
                {
                    "voter_address": "bc1qxy2lpan99fcnhhyq4hzzyg0v8s67k7ezne4v8p",
                    "vote": "verified",
                    "confidence": 0.88,
                    "timestamp": datetime.utcnow().isoformat(),
                    "block_height": (await self.get_chain_metrics()).block_height - 1,
                    "confirmations": 3,
                }
            ]

            self.logger.info(
                f"Retrieved {len(simulated_votes)} Bitcoin consensus votes "
                f"for request {request_id}"
            )

            return simulated_votes

        except Exception as e:
            self.logger.error(f"Failed to get Bitcoin consensus votes: {e}")
            raise

    def get_verification_stats(self) -> dict[str, Any]:
        """Get verification statistics for Bitcoin adapter."""
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
            "average_tx_fee_satoshis": self._verification_stats["average_tx_fee"],
            "network": self.network,
        }

    def _calculate_verification_hash(self, verification_data: dict[str, Any]) -> str:
        """Calculate hash for verification data using Bitcoin-specific method."""
        # Create deterministic hash with Bitcoin-specific prefix
        data_str = json.dumps(verification_data, sort_keys=True)
        bitcoin_data = f"BITCOIN_VERIFICATION:{data_str}"

        # Use double SHA256 like Bitcoin
        first_hash = hashlib.sha256(bitcoin_data.encode()).digest()
        return hashlib.sha256(first_hash).hexdigest()

    def _calculate_confidence_score(self, verification_data: dict[str, Any]) -> float:
        """Calculate confidence score for Bitcoin verification."""
        # Base confidence for Bitcoin's security
        score = 0.90  # Bitcoin gets high base score for security

        # Adjust based on data completeness
        required_fields = ["ai_output", "input_data", "model_id"]
        present_fields = sum(
            1 for field in required_fields if field in verification_data
        )
        completeness_score = present_fields / len(required_fields)

        # Bitcoin security bonus
        bitcoin_bonus = 0.05

        # Combine scores
        final_score = (score + completeness_score + bitcoin_bonus) / 2.05
        return min(max(final_score, 0.0), 1.0)

    def _calculate_vote_hash(
        self, request_id: str, consensus_data: dict[str, Any]
    ) -> str:
        """Calculate hash for Bitcoin consensus vote."""
        # Create deterministic hash for vote
        vote_data = {
            "request_id": request_id,
            "consensus_data": consensus_data,
            "chain": "bitcoin",
            "network": self.network,
            "timestamp": datetime.utcnow().isoformat(),
        }

        data_str = json.dumps(vote_data, sort_keys=True)

        # Use double SHA256 like Bitcoin
        first_hash = hashlib.sha256(data_str.encode()).digest()
        return hashlib.sha256(first_hash).hexdigest()

    def get_network_info(self) -> dict[str, Any]:
        """Get Bitcoin network information."""
        config = self._network_configs.get(self.network, {})
        return {
            "network": self.network,
            "name": config.get("name", "Unknown Network"),
            "explorer": config.get("explorer"),
            "magic_bytes": config.get("magic_bytes"),
            "port": config.get("port"),
            "consensus": "Proof of Work (SHA-256)",
            "native_token": "BTC",
            "supports_smart_contracts": False,
            "script_features": ["OP_RETURN", "Multisig", "Timelock"],
            "layer2_solutions": ["Lightning Network", "Liquid"],
        }

    def estimate_fee_rate(self, target_blocks: int = 6) -> dict[str, Any]:
        """Estimate Bitcoin fee rate for target confirmation time."""
        # Simulated fee estimation based on target blocks
        fee_rates = {
            1: 50,  # High priority (next block)
            3: 25,  # Medium priority (within 3 blocks)
            6: 15,  # Standard priority (within 6 blocks)
            12: 10,  # Low priority (within 12 blocks)
            24: 5,  # Economy (within 24 blocks)
        }

        # Find closest target
        closest_target = min(fee_rates.keys(), key=lambda x: abs(x - target_blocks))
        fee_rate = fee_rates[closest_target]

        return {
            "target_blocks": target_blocks,
            "fee_rate_sat_per_byte": fee_rate,
            "estimated_confirmation_time": f"{target_blocks * 10} minutes",
            "priority": self._get_priority_level(target_blocks),
        }

    def _get_priority_level(self, target_blocks: int) -> str:
        """Get priority level based on target blocks."""
        if target_blocks <= 1:
            return "high"
        elif target_blocks <= 3:
            return "medium"
        elif target_blocks <= 6:
            return "standard"
        elif target_blocks <= 12:
            return "low"
        else:
            return "economy"

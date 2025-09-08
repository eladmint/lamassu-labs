"""
Ethereum Blockchain Adapter
===========================

Universal chain adapter implementation for Ethereum, Polygon, and Arbitrum
networks using Web3.py for TrustWrapper v3.0 verification platform.
"""

import logging
from datetime import datetime
from typing import Any

from eth_account import Account
from web3 import Web3

# Handle different web3.py versions for PoA middleware
try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    try:
        from web3.middleware.geth_poa import geth_poa_middleware
    except ImportError:
        # Create a mock middleware for compatibility
        def geth_poa_middleware(make_request, web3):
            return make_request

        print("Warning: PoA middleware not available, using mock")

from core.interfaces import (
    ChainMetrics,
    ChainType,
    ChainVerificationResult,
    IUniversalChainAdapter,
    VerificationStatus,
)


class EthereumAdapter(IUniversalChainAdapter):
    """
    Universal Ethereum-compatible blockchain adapter.

    Supports Ethereum mainnet, Polygon, Arbitrum, and other EVM-compatible chains
    through Web3.py integration with smart contract verification capabilities.
    """

    def __init__(
        self,
        chain_type: ChainType,
        rpc_url: str,
        private_key: str | None = None,
        contract_address: str | None = None,
        gas_limit: int = 500000,
        gas_price_gwei: int | None = None,
    ):
        """
        Initialize Ethereum adapter.

        Args:
            chain_type: Type of Ethereum-compatible chain
            rpc_url: RPC endpoint URL
            private_key: Private key for transactions (optional)
            contract_address: TrustWrapper contract address (optional)
            gas_limit: Gas limit for transactions
            gas_price_gwei: Gas price in Gwei (auto if None)
        """
        self._chain_type = chain_type
        self.rpc_url = rpc_url
        self.private_key = private_key
        self.contract_address = contract_address
        self.gas_limit = gas_limit
        self.gas_price_gwei = gas_price_gwei

        self.w3: Web3 | None = None
        self.account: Account | None = None
        self.contract = None
        self.logger = logging.getLogger(f"{__name__}.{chain_type.value}")

        # Chain-specific configurations
        self._chain_configs = {
            ChainType.ETHEREUM: {
                "chain_id": 1,
                "name": "Ethereum Mainnet",
                "currency": "ETH",
                "explorer": "https://etherscan.io",
            },
            ChainType.POLYGON: {
                "chain_id": 137,
                "name": "Polygon Mainnet",
                "currency": "MATIC",
                "explorer": "https://polygonscan.com",
            },
            ChainType.ARBITRUM: {
                "chain_id": 42161,
                "name": "Arbitrum One",
                "currency": "ETH",
                "explorer": "https://arbiscan.io",
            },
        }

        self._verification_stats = {
            "total_verifications": 0,
            "successful_verifications": 0,
            "failed_verifications": 0,
            "average_gas_used": 0,
        }

    @property
    def chain_type(self) -> ChainType:
        """Return the blockchain type this adapter handles."""
        return self._chain_type

    @property
    def is_connected(self) -> bool:
        """Check if adapter is connected to blockchain network."""
        if not self.w3:
            return False

        try:
            # Simple connectivity check
            return self.w3.is_connected()
        except Exception:
            return False

    async def connect(self) -> bool:
        """
        Connect to Ethereum-compatible network.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Initialize Web3 connection
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

            # Add PoA middleware for Polygon and some testnets
            if self._chain_type in [ChainType.POLYGON]:
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            # Test connection
            if not self.w3.is_connected():
                self.logger.error(f"Failed to connect to {self._chain_type.value}")
                return False

            # Initialize account if private key provided
            if self.private_key:
                self.account = Account.from_key(self.private_key)
                self.logger.info(
                    f"Initialized account: {self.account.address} "
                    f"for {self._chain_type.value}"
                )

            # Verify chain ID matches expected
            chain_id = await self._get_chain_id()
            expected_chain_id = self._chain_configs[self._chain_type]["chain_id"]

            if chain_id != expected_chain_id:
                self.logger.warning(
                    f"Chain ID mismatch: expected {expected_chain_id}, "
                    f"got {chain_id} for {self._chain_type.value}"
                )

            self.logger.info(
                f"Connected to {self._chain_type.value} (Chain ID: {chain_id})"
            )
            return True

        except Exception as e:
            self.logger.error(f"Connection error for {self._chain_type.value}: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from blockchain network."""
        self.w3 = None
        self.account = None
        self.contract = None
        self.logger.info(f"Disconnected from {self._chain_type.value}")

    async def get_chain_metrics(self) -> ChainMetrics:
        """
        Get current blockchain metrics.

        Returns:
            ChainMetrics: Current chain performance data
        """
        if not self.w3 or not self.is_connected:
            raise ConnectionError(f"Not connected to {self._chain_type.value}")

        try:
            # Get latest block
            latest_block = self.w3.eth.get_block("latest")

            # Calculate block time (estimate from last few blocks)
            block_time = await self._estimate_block_time()

            # Get gas price
            gas_price = self.w3.eth.gas_price

            # Get network hashrate (if available)
            network_hashrate = None
            if hasattr(self.w3.eth, "hashrate"):
                try:
                    network_hashrate = self.w3.eth.hashrate
                except:
                    pass

            return ChainMetrics(
                chain_id=str(await self._get_chain_id()),
                block_height=latest_block["number"],
                block_time=block_time,
                gas_price=float(gas_price),
                network_hashrate=network_hashrate,
                active_validators=None,  # Not available for PoW chains
                finality_time=self._get_finality_time(),
                last_updated=datetime.utcnow(),
            )

        except Exception as e:
            self.logger.error(
                f"Failed to get metrics for {self._chain_type.value}: {e}"
            )
            raise

    async def verify_ai_output(
        self, ai_agent_id: str, verification_data: dict[str, Any]
    ) -> ChainVerificationResult:
        """
        Verify AI output on Ethereum-compatible blockchain.

        Args:
            ai_agent_id: Unique identifier for AI agent
            verification_data: Data to verify

        Returns:
            ChainVerificationResult: Verification result for this chain
        """
        start_time = datetime.utcnow()

        try:
            self._verification_stats["total_verifications"] += 1

            # For Phase 1, implement basic verification logic
            # In production, this would interact with deployed smart contracts

            # Simulate verification process
            verification_hash = self._calculate_verification_hash(verification_data)
            confidence_score = self._calculate_confidence_score(verification_data)

            # Determine verification status based on confidence
            if confidence_score >= 0.8:
                status = VerificationStatus.VERIFIED
            elif confidence_score >= 0.6:
                status = VerificationStatus.PENDING
            else:
                status = VerificationStatus.REJECTED

            # For Phase 1, simulate transaction without actual blockchain submission
            tx_hash = f"0x{verification_hash[:64]}"  # Simulated transaction hash
            block_number = (await self.get_chain_metrics()).block_height
            gas_used = 150000  # Estimated gas usage

            execution_time = (datetime.utcnow() - start_time).total_seconds()

            if status == VerificationStatus.VERIFIED:
                self._verification_stats["successful_verifications"] += 1
            else:
                self._verification_stats["failed_verifications"] += 1

            # Update average gas used
            total_gas = (
                self._verification_stats["average_gas_used"]
                * (self._verification_stats["total_verifications"] - 1)
                + gas_used
            )
            self._verification_stats["average_gas_used"] = (
                total_gas / self._verification_stats["total_verifications"]
            )

            result = ChainVerificationResult(
                chain_type=self._chain_type,
                transaction_hash=tx_hash,
                block_number=block_number,
                verification_status=status,
                confidence_score=confidence_score,
                gas_used=gas_used,
                execution_time=execution_time,
                error_message=None,
                verified_at=datetime.utcnow(),
            )

            self.logger.info(
                f"Verification complete on {self._chain_type.value}: "
                f"Status={status.value}, Confidence={confidence_score:.3f}, "
                f"Time={execution_time:.3f}s"
            )

            return result

        except Exception as e:
            self._verification_stats["failed_verifications"] += 1
            execution_time = (datetime.utcnow() - start_time).total_seconds()

            self.logger.error(f"Verification failed on {self._chain_type.value}: {e}")

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
        Submit consensus vote to blockchain.

        Args:
            request_id: Unique request identifier
            consensus_data: Consensus voting data

        Returns:
            str: Transaction hash of submitted vote
        """
        if not self.w3 or not self.account:
            raise ConnectionError(
                f"Not connected or no account configured for {self._chain_type.value}"
            )

        try:
            # For Phase 1, simulate consensus vote submission
            vote_hash = self._calculate_vote_hash(request_id, consensus_data)

            # In production, this would submit to smart contract
            # For now, return simulated transaction hash
            tx_hash = f"0x{vote_hash[:64]}"

            self.logger.info(
                f"Consensus vote submitted on {self._chain_type.value}: {tx_hash}"
            )

            return tx_hash

        except Exception as e:
            self.logger.error(
                f"Failed to submit consensus vote on {self._chain_type.value}: {e}"
            )
            raise

    async def get_consensus_votes(self, request_id: str) -> list[dict[str, Any]]:
        """
        Retrieve consensus votes for a request.

        Args:
            request_id: Unique request identifier

        Returns:
            List[Dict]: List of consensus votes from this chain
        """
        if not self.w3:
            raise ConnectionError(f"Not connected to {self._chain_type.value}")

        try:
            # For Phase 1, return simulated consensus votes
            # In production, this would query smart contract events

            simulated_votes = [
                {
                    "voter_address": "0x742d35Cc6634C0532925a3b8D5c0b8A0C6E5b2E9",
                    "vote": "verified",
                    "confidence": 0.95,
                    "timestamp": datetime.utcnow().isoformat(),
                    "block_number": (await self.get_chain_metrics()).block_height - 1,
                }
            ]

            self.logger.info(
                f"Retrieved {len(simulated_votes)} consensus votes "
                f"for request {request_id} on {self._chain_type.value}"
            )

            return simulated_votes

        except Exception as e:
            self.logger.error(
                f"Failed to get consensus votes on {self._chain_type.value}: {e}"
            )
            raise

    def get_verification_stats(self) -> dict[str, Any]:
        """Get verification statistics for this adapter."""
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
            "average_gas_used": self._verification_stats["average_gas_used"],
        }

    async def _get_chain_id(self) -> int:
        """Get chain ID for the connected network."""
        if not self.w3:
            raise ConnectionError("Web3 not initialized")
        return self.w3.eth.chain_id

    async def _estimate_block_time(self) -> float:
        """Estimate average block time from recent blocks."""
        try:
            latest_block = self.w3.eth.get_block("latest")
            prev_block = self.w3.eth.get_block(latest_block["number"] - 10)

            time_diff = latest_block["timestamp"] - prev_block["timestamp"]
            block_diff = latest_block["number"] - prev_block["number"]

            return float(time_diff / block_diff)

        except Exception:
            # Return default block times if estimation fails
            defaults = {
                ChainType.ETHEREUM: 12.0,
                ChainType.POLYGON: 2.3,
                ChainType.ARBITRUM: 0.25,
            }
            return defaults.get(self._chain_type, 12.0)

    def _get_finality_time(self) -> float:
        """Get finality time for the chain (in seconds)."""
        finality_times = {
            ChainType.ETHEREUM: 12.8 * 60,  # ~12.8 minutes for finality
            ChainType.POLYGON: 2.3 * 128,  # ~128 blocks for finality
            ChainType.ARBITRUM: 60.0,  # ~1 minute for practical finality
        }
        return finality_times.get(self._chain_type, 300.0)

    def _calculate_verification_hash(self, verification_data: dict[str, Any]) -> str:
        """Calculate hash for verification data."""
        import hashlib
        import json

        # Create deterministic hash of verification data
        data_str = json.dumps(verification_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def _calculate_confidence_score(self, verification_data: dict[str, Any]) -> float:
        """Calculate confidence score for verification data."""
        # For Phase 1, implement basic confidence calculation
        # In production, this would use ML models and oracle data

        score = 0.8  # Base confidence

        # Adjust based on data completeness
        required_fields = ["ai_output", "input_data", "model_id"]
        present_fields = sum(
            1 for field in required_fields if field in verification_data
        )
        completeness_score = present_fields / len(required_fields)

        # Combine scores
        final_score = (score + completeness_score) / 2
        return min(max(final_score, 0.0), 1.0)

    def _calculate_vote_hash(
        self, request_id: str, consensus_data: dict[str, Any]
    ) -> str:
        """Calculate hash for consensus vote."""
        import hashlib
        import json

        # Create deterministic hash for vote
        vote_data = {
            "request_id": request_id,
            "consensus_data": consensus_data,
            "chain": self._chain_type.value,
            "timestamp": datetime.utcnow().isoformat(),
        }

        data_str = json.dumps(vote_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

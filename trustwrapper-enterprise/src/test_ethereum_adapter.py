"""
Ethereum Adapter Unit Tests
===========================

Unit tests for Ethereum blockchain adapter implementation.
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from adapters.ethereum_adapter import EthereumAdapter
from core.interfaces import ChainType, VerificationStatus


class TestEthereumAdapter:
    """Test suite for EthereumAdapter class."""

    @pytest.fixture
    def ethereum_adapter(self):
        """Create Ethereum adapter instance for testing."""
        return EthereumAdapter(
            chain_type=ChainType.ETHEREUM,
            rpc_url="https://eth-mainnet.g.alchemy.com/v2/demo",
            gas_limit=500000,
        )

    @pytest.fixture
    def polygon_adapter(self):
        """Create Polygon adapter instance for testing."""
        return EthereumAdapter(
            chain_type=ChainType.POLYGON,
            rpc_url="https://polygon-mainnet.g.alchemy.com/v2/demo",
            gas_limit=300000,
        )

    def test_adapter_initialization(self, ethereum_adapter):
        """Test adapter initialization with correct parameters."""
        assert ethereum_adapter.chain_type == ChainType.ETHEREUM
        assert ethereum_adapter.rpc_url == "https://eth-mainnet.g.alchemy.com/v2/demo"
        assert ethereum_adapter.gas_limit == 500000
        assert not ethereum_adapter.is_connected

    def test_chain_type_property(self, ethereum_adapter, polygon_adapter):
        """Test chain_type property returns correct values."""
        assert ethereum_adapter.chain_type == ChainType.ETHEREUM
        assert polygon_adapter.chain_type == ChainType.POLYGON

    def test_is_connected_without_web3(self, ethereum_adapter):
        """Test is_connected returns False when Web3 not initialized."""
        assert not ethereum_adapter.is_connected

    @patch("web3.Web3")
    async def test_connect_success(self, mock_web3_class, ethereum_adapter):
        """Test successful connection to Ethereum network."""
        # Mock Web3 instance
        mock_web3 = Mock()
        mock_web3.is_connected.return_value = True
        mock_web3.eth.chain_id = 1  # Ethereum mainnet
        mock_web3_class.return_value = mock_web3

        # Test connection
        result = await ethereum_adapter.connect()

        assert result is True
        assert ethereum_adapter.w3 is not None
        assert ethereum_adapter.is_connected

    @patch("web3.Web3")
    async def test_connect_failure(self, mock_web3_class, ethereum_adapter):
        """Test connection failure handling."""
        # Mock Web3 instance that fails to connect
        mock_web3 = Mock()
        mock_web3.is_connected.return_value = False
        mock_web3_class.return_value = mock_web3

        # Test connection
        result = await ethereum_adapter.connect()

        assert result is False
        assert not ethereum_adapter.is_connected

    @patch("web3.Web3")
    async def test_connect_with_chain_id_mismatch(
        self, mock_web3_class, ethereum_adapter
    ):
        """Test connection with chain ID mismatch warning."""
        # Mock Web3 instance with wrong chain ID
        mock_web3 = Mock()
        mock_web3.is_connected.return_value = True
        mock_web3.eth.chain_id = 5  # Goerli testnet instead of mainnet
        mock_web3_class.return_value = mock_web3

        # Test connection
        result = await ethereum_adapter.connect()

        assert result is True  # Connection succeeds but with warning
        assert ethereum_adapter.is_connected

    async def test_disconnect(self, ethereum_adapter):
        """Test disconnection from network."""
        # Set up mock connection
        ethereum_adapter.w3 = Mock()
        ethereum_adapter.account = Mock()

        await ethereum_adapter.disconnect()

        assert ethereum_adapter.w3 is None
        assert ethereum_adapter.account is None

    @patch("web3.Web3")
    async def test_get_chain_metrics(self, mock_web3_class, ethereum_adapter):
        """Test getting chain metrics."""
        # Mock Web3 and block data
        mock_web3 = Mock()
        mock_web3.is_connected.return_value = True
        mock_web3.eth.chain_id = 1
        mock_web3.eth.gas_price = 20000000000  # 20 Gwei

        # Mock latest block
        mock_block = {
            "number": 18500000,
            "timestamp": int(datetime.utcnow().timestamp()),
        }
        mock_web3.eth.get_block.return_value = mock_block

        mock_web3_class.return_value = mock_web3
        ethereum_adapter.w3 = mock_web3

        # Mock block time estimation
        with patch.object(ethereum_adapter, "_estimate_block_time", return_value=12.0):
            metrics = await ethereum_adapter.get_chain_metrics()

        assert metrics.chain_id == "1"
        assert metrics.block_height == 18500000
        assert metrics.block_time == 12.0
        assert metrics.gas_price == 20000000000.0
        assert metrics.finality_time > 0
        assert isinstance(metrics.last_updated, datetime)

    async def test_get_chain_metrics_not_connected(self, ethereum_adapter):
        """Test get_chain_metrics raises error when not connected."""
        with pytest.raises(ConnectionError, match="Not connected to ethereum"):
            await ethereum_adapter.get_chain_metrics()

    @patch("web3.Web3")
    async def test_verify_ai_output_success(self, mock_web3_class, ethereum_adapter):
        """Test successful AI output verification."""
        # Set up mock connection
        mock_web3 = Mock()
        mock_web3.is_connected.return_value = True
        mock_web3.eth.chain_id = 1
        mock_web3_class.return_value = mock_web3
        ethereum_adapter.w3 = mock_web3

        # Mock get_chain_metrics
        with patch.object(ethereum_adapter, "get_chain_metrics") as mock_metrics:
            mock_metrics.return_value = Mock(block_height=18500000)

            verification_data = {
                "ai_output": "Market will trend upward",
                "input_data": {"symbol": "BTC"},
                "model_id": "predictor_v1",
            }

            result = await ethereum_adapter.verify_ai_output(
                ai_agent_id="test_agent", verification_data=verification_data
            )

        assert result.chain_type == ChainType.ETHEREUM
        assert result.verification_status in [
            VerificationStatus.VERIFIED,
            VerificationStatus.PENDING,
            VerificationStatus.REJECTED,
        ]
        assert 0.0 <= result.confidence_score <= 1.0
        assert result.transaction_hash is not None
        assert result.execution_time > 0
        assert result.verified_at is not None

    @patch("web3.Web3")
    async def test_verify_ai_output_with_error(self, mock_web3_class, ethereum_adapter):
        """Test AI output verification with error handling."""
        # Set up mock connection
        mock_web3 = Mock()
        mock_web3.is_connected.return_value = True
        mock_web3_class.return_value = mock_web3
        ethereum_adapter.w3 = mock_web3

        # Mock get_chain_metrics to raise exception
        with patch.object(
            ethereum_adapter,
            "get_chain_metrics",
            side_effect=Exception("Network error"),
        ):
            verification_data = {"ai_output": "test"}

            result = await ethereum_adapter.verify_ai_output(
                ai_agent_id="test_agent", verification_data=verification_data
            )

        assert result.verification_status == VerificationStatus.ERROR
        assert result.confidence_score == 0.0
        assert result.error_message is not None
        assert "Network error" in result.error_message

    @patch("web3.Web3")
    async def test_submit_consensus_vote(self, mock_web3_class, ethereum_adapter):
        """Test consensus vote submission."""
        # Set up mock connection with account
        mock_web3 = Mock()
        mock_web3.is_connected.return_value = True
        mock_web3_class.return_value = mock_web3

        mock_account = Mock()
        mock_account.address = "0x742d35Cc6634C0532925a3b8D5c0b8A0C6E5b2E9"

        ethereum_adapter.w3 = mock_web3
        ethereum_adapter.account = mock_account

        consensus_data = {"vote": "verified", "confidence": 0.95}

        tx_hash = await ethereum_adapter.submit_consensus_vote(
            request_id="test_request", consensus_data=consensus_data
        )

        assert tx_hash.startswith("0x")
        assert len(tx_hash) == 66  # 64 hex chars + 0x prefix

    async def test_submit_consensus_vote_not_connected(self, ethereum_adapter):
        """Test consensus vote submission when not connected."""
        with pytest.raises(ConnectionError, match="Not connected or no account"):
            await ethereum_adapter.submit_consensus_vote(
                request_id="test_request", consensus_data={"vote": "verified"}
            )

    @patch("web3.Web3")
    async def test_get_consensus_votes(self, mock_web3_class, ethereum_adapter):
        """Test retrieving consensus votes."""
        # Set up mock connection
        mock_web3 = Mock()
        mock_web3.is_connected.return_value = True
        mock_web3_class.return_value = mock_web3
        ethereum_adapter.w3 = mock_web3

        # Mock get_chain_metrics for block number
        with patch.object(ethereum_adapter, "get_chain_metrics") as mock_metrics:
            mock_metrics.return_value = Mock(block_height=18500000)

            votes = await ethereum_adapter.get_consensus_votes("test_request")

        assert isinstance(votes, list)
        assert len(votes) > 0

        # Check vote structure
        vote = votes[0]
        assert "voter_address" in vote
        assert "vote" in vote
        assert "confidence" in vote
        assert "timestamp" in vote
        assert "block_number" in vote

    def test_get_verification_stats(self, ethereum_adapter):
        """Test getting verification statistics."""
        stats = ethereum_adapter.get_verification_stats()

        assert "chain_type" in stats
        assert "total_verifications" in stats
        assert "successful_verifications" in stats
        assert "failed_verifications" in stats
        assert "success_rate" in stats
        assert "average_gas_used" in stats

        assert stats["chain_type"] == "ethereum"
        assert stats["total_verifications"] == 0
        assert stats["success_rate"] == 0.0

    def test_calculate_verification_hash(self, ethereum_adapter):
        """Test verification hash calculation is deterministic."""
        verification_data = {"ai_output": "test output", "input_data": {"key": "value"}}

        hash1 = ethereum_adapter._calculate_verification_hash(verification_data)
        hash2 = ethereum_adapter._calculate_verification_hash(verification_data)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex string length

    def test_calculate_confidence_score(self, ethereum_adapter):
        """Test confidence score calculation."""
        # Complete verification data
        complete_data = {
            "ai_output": "test output",
            "input_data": {"key": "value"},
            "model_id": "test_model",
        }

        # Incomplete verification data
        incomplete_data = {"ai_output": "test output"}

        complete_score = ethereum_adapter._calculate_confidence_score(complete_data)
        incomplete_score = ethereum_adapter._calculate_confidence_score(incomplete_data)

        assert 0.0 <= complete_score <= 1.0
        assert 0.0 <= incomplete_score <= 1.0
        assert complete_score > incomplete_score

    async def test_estimate_block_time_fallback(self, ethereum_adapter):
        """Test block time estimation fallback to defaults."""
        # Test without Web3 connection
        block_time = await ethereum_adapter._estimate_block_time()

        # Should return default Ethereum block time
        assert block_time == 12.0

    def test_get_finality_time(self, ethereum_adapter, polygon_adapter):
        """Test finality time for different chains."""
        eth_finality = ethereum_adapter._get_finality_time()
        polygon_finality = polygon_adapter._get_finality_time()

        assert eth_finality > 0
        assert polygon_finality > 0
        assert eth_finality > polygon_finality  # Ethereum has longer finality time

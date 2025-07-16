#!/usr/bin/env python3
"""
Test suite for Leo smart contract integration
Tests Aleo blockchain proof verification
"""

import sys
import time
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.core.trust_wrapper import VerifiedResult, ZKTrustWrapper
from src.zk.aleo_client import AleoClient
from src.zk.leo_integration import LeoProofGenerator


class TestLeoProofGenerator:
    """Test suite for Leo proof generation"""

    @pytest.fixture
    def mock_aleo_client(self):
        """Create mock Aleo client"""
        client = Mock(spec=AleoClient)
        client.is_connected = Mock(return_value=True)
        client.submit_transaction = AsyncMock(
            return_value={
                "transaction_id": "aleo1qyz3...8fhs",
                "status": "confirmed",
                "block_height": 12345,
            }
        )
        return client

    @pytest.fixture
    def proof_generator(self, mock_aleo_client):
        """Create proof generator with mock client"""
        generator = LeoProofGenerator()
        generator.client = mock_aleo_client
        return generator

    def test_proof_generator_initialization(self):
        """Test Leo proof generator initialization"""
        generator = LeoProofGenerator()

        assert hasattr(generator, "program_id")
        assert generator.program_id == "trust_verifier.aleo"
        assert hasattr(generator, "private_key")
        assert hasattr(generator, "view_key")

    @pytest.mark.asyncio
    async def test_generate_leo_proof(self, proof_generator):
        """Test generating Leo proof for execution"""
        execution_data = {
            "agent_hash": "abc123def456",
            "success": True,
            "execution_time": 1234,
            "timestamp": time.time(),
        }

        proof = await proof_generator.generate_proof(execution_data)

        assert "transaction_id" in proof
        assert proof["transaction_id"] == "aleo1qyz3...8fhs"
        assert proof["status"] == "confirmed"
        assert proof["block_height"] == 12345

    @pytest.mark.asyncio
    async def test_verify_leo_proof(self, proof_generator):
        """Test verifying Leo proof on blockchain"""
        transaction_id = "aleo1qyz3...8fhs"

        # Mock verification response
        proof_generator.client.get_transaction = AsyncMock(
            return_value={
                "id": transaction_id,
                "status": "confirmed",
                "outputs": [
                    {
                        "value": {
                            "agent_hash": "abc123def456",
                            "success": True,
                            "execution_time": 1234,
                            "accuracy": 985,  # 98.5%
                        }
                    }
                ],
            }
        )

        verification = await proof_generator.verify_proof(transaction_id)

        assert verification["valid"] is True
        assert verification["agent_hash"] == "abc123def456"
        assert verification["success"] is True
        assert verification["execution_time"] == 1234

    def test_leo_contract_formatting(self, proof_generator):
        """Test Leo contract input formatting"""
        execution_data = {
            "agent_hash": "0x" + "a" * 64,  # Hex string
            "success": True,
            "execution_time": 1500,
            "accuracy": 0.95,
        }

        formatted = proof_generator._format_for_leo(execution_data)

        assert formatted["agent_hash"].endswith("field")
        assert formatted["success"] == "true"
        assert formatted["execution_time"] == "1500u32"
        assert formatted["accuracy"] == "950u32"  # Converted to basis points

    @pytest.mark.asyncio
    async def test_failed_transaction_handling(self, proof_generator):
        """Test handling of failed blockchain transactions"""
        proof_generator.client.submit_transaction = AsyncMock(
            side_effect=Exception("Network error")
        )

        execution_data = {
            "agent_hash": "abc123",
            "success": True,
            "execution_time": 1000,
        }

        with pytest.raises(Exception) as exc_info:
            await proof_generator.generate_proof(execution_data)

        assert "Network error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_proof_caching(self, proof_generator):
        """Test proof caching to avoid duplicate submissions"""
        execution_data = {
            "agent_hash": "abc123",
            "success": True,
            "execution_time": 1000,
            "timestamp": 12345.678,
        }

        # First call should submit transaction
        proof1 = await proof_generator.generate_proof(execution_data)
        assert proof_generator.client.submit_transaction.call_count == 1

        # Second call with same data should use cache
        proof2 = await proof_generator.generate_proof(execution_data)
        assert (
            proof_generator.client.submit_transaction.call_count == 1
        )  # No additional call
        assert proof1 == proof2


class TestAleoClient:
    """Test suite for Aleo blockchain client"""

    @pytest.fixture
    def aleo_client(self):
        """Create Aleo client instance"""
        return AleoClient(
            node_url="https://api.explorer.aleo.org/v1/testnet3",
            private_key="test_private_key",
        )

    def test_client_initialization(self, aleo_client):
        """Test Aleo client initialization"""
        assert aleo_client.node_url == "https://api.explorer.aleo.org/v1/testnet3"
        assert aleo_client.private_key == "test_private_key"
        assert hasattr(aleo_client, "view_key")
        assert hasattr(aleo_client, "address")

    @pytest.mark.asyncio
    async def test_connection_check(self, aleo_client):
        """Test Aleo node connection check"""
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.return_value.__aenter__.return_value.status = 200
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(
                return_value={"height": 12345}
            )

            is_connected = await aleo_client.is_connected()
            assert is_connected is True

    @pytest.mark.asyncio
    async def test_transaction_submission(self, aleo_client):
        """Test transaction submission to Aleo"""
        with patch("aiohttp.ClientSession.post") as mock_post:
            mock_post.return_value.__aenter__.return_value.status = 200
            mock_post.return_value.__aenter__.return_value.json = AsyncMock(
                return_value={"transaction_id": "at1234...", "status": "pending"}
            )

            transaction_data = {
                "program": "trust_verifier.aleo",
                "function": "verify_execution",
                "inputs": ["1000u32", "true", "123field"],
            }

            result = await aleo_client.submit_transaction(transaction_data)

            assert result["transaction_id"] == "at1234..."
            assert result["status"] == "pending"

    @pytest.mark.asyncio
    async def test_transaction_status_check(self, aleo_client):
        """Test checking transaction status"""
        transaction_id = "at1234..."

        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_get.return_value.__aenter__.return_value.status = 200
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(
                return_value={
                    "id": transaction_id,
                    "status": "confirmed",
                    "block_height": 12346,
                }
            )

            status = await aleo_client.get_transaction_status(transaction_id)

            assert status["status"] == "confirmed"
            assert status["block_height"] == 12346


class TestIntegratedTrustWrapperWithLeo:
    """Integration tests for TrustWrapper with Leo proofs"""

    @pytest.fixture
    def integrated_wrapper(self):
        """Create TrustWrapper with Leo integration"""

        class MockAgent:
            def execute(self, data):
                return {"result": f"Processed: {data}"}

        agent = MockAgent()
        wrapper = ZKTrustWrapper(agent, enable_blockchain=True)

        # Mock the Leo components
        wrapper.proof_generator = Mock(spec=LeoProofGenerator)
        wrapper.proof_generator.generate_proof = AsyncMock(
            return_value={"transaction_id": "aleo1test...", "status": "confirmed"}
        )

        return wrapper

    @pytest.mark.asyncio
    async def test_blockchain_enabled_execution(self, integrated_wrapper):
        """Test execution with blockchain proof"""
        result = await integrated_wrapper.verified_execute_with_blockchain("test_data")

        assert isinstance(result, VerifiedResult)
        assert result.verified is True
        assert result.blockchain_proof is not None
        assert result.blockchain_proof["transaction_id"] == "aleo1test..."

    @pytest.mark.asyncio
    async def test_blockchain_disabled_execution(self):
        """Test execution without blockchain proof"""

        class MockAgent:
            def execute(self, data):
                return {"result": data}

        wrapper = ZKTrustWrapper(MockAgent(), enable_blockchain=False)
        result = wrapper.verified_execute("test")

        assert result.verified is True
        assert not hasattr(result, "blockchain_proof")

    @pytest.mark.asyncio
    async def test_blockchain_failure_handling(self, integrated_wrapper):
        """Test graceful handling of blockchain failures"""
        # Make blockchain proof fail
        integrated_wrapper.proof_generator.generate_proof = AsyncMock(
            side_effect=Exception("Blockchain unavailable")
        )

        # Should still return result but without blockchain proof
        result = await integrated_wrapper.verified_execute_with_blockchain(
            "test", fallback_on_blockchain_error=True
        )

        assert result.verified is True
        assert result.result is not None
        assert result.blockchain_proof is None


class TestLeoContractExamples:
    """Test examples matching Leo contract functionality"""

    def test_execution_proof_struct(self):
        """Test ExecutionProof struct mapping"""
        # This matches the Leo struct
        execution_proof = {
            "agent_hash": "0x1234567890abcdef" + "0" * 48,  # 64 char hex
            "success": True,
            "execution_time": 1500,  # milliseconds
            "accuracy": 950,  # basis points (95.0%)
        }

        # Validate field types
        assert isinstance(execution_proof["agent_hash"], str)
        assert len(execution_proof["agent_hash"]) == 66  # 0x + 64 chars
        assert isinstance(execution_proof["success"], bool)
        assert isinstance(execution_proof["execution_time"], int)
        assert 0 <= execution_proof["execution_time"] <= 2**32 - 1  # u32 range
        assert isinstance(execution_proof["accuracy"], int)
        assert 0 <= execution_proof["accuracy"] <= 1000  # 0-100% in basis points

    def test_verify_execution_transition(self):
        """Test verify_execution transition inputs"""
        # Private inputs
        private_inputs = {
            "execution_time": 2500,  # u32
            "success": True,  # bool
            "accuracy": 875,  # u32 (87.5%)
        }

        # Public inputs
        public_inputs = {"agent_hash": "0xabcdef1234567890" + "0" * 48}  # field

        # Validate transition inputs match Leo types
        assert isinstance(private_inputs["execution_time"], int)
        assert isinstance(private_inputs["success"], bool)
        assert isinstance(private_inputs["accuracy"], int)
        assert isinstance(public_inputs["agent_hash"], str)

    def test_leo_field_conversion(self):
        """Test conversion to Leo field type"""
        # Test various hash formats
        test_hashes = [
            "abc123def456",  # Short hex
            "0x" + "f" * 64,  # Full hex with prefix
            "1234567890abcdef" * 4,  # 64 chars without prefix
        ]

        for hash_str in test_hashes:
            # Convert to field format
            if not hash_str.startswith("0x"):
                hash_str = "0x" + hash_str

            # Pad if necessary
            if len(hash_str) < 66:  # 0x + 64 chars
                hash_str = hash_str[:2] + hash_str[2:].zfill(64)

            assert len(hash_str) == 66
            assert hash_str.startswith("0x")
            assert all(c in "0123456789abcdef" for c in hash_str[2:])


class TestEndToEndScenarios:
    """End-to-end testing scenarios"""

    @pytest.mark.asyncio
    async def test_full_trust_verification_flow(self):
        """Test complete flow from agent execution to blockchain verification"""

        # 1. Create agent
        class DataProcessingAgent:
            def execute(self, data):
                time.sleep(0.1)  # Simulate processing
                return {"processed_items": len(data), "success_rate": 0.95}

        # 2. Wrap with TrustWrapper
        agent = DataProcessingAgent()
        wrapper = ZKTrustWrapper(agent, enable_blockchain=True)

        # 3. Mock blockchain components
        with patch("src.zk.leo_integration.LeoProofGenerator") as mock_generator:
            mock_instance = mock_generator.return_value
            mock_instance.generate_proof = AsyncMock(
                return_value={
                    "transaction_id": "aleo1final123...",
                    "status": "confirmed",
                    "block_height": 99999,
                }
            )

            # 4. Execute with verification
            test_data = ["item1", "item2", "item3"]
            result = await wrapper.verified_execute_with_blockchain(test_data)

            # 5. Verify complete result
            assert result.verified is True
            assert result.result["processed_items"] == 3
            assert result.result["success_rate"] == 0.95
            assert result.proof.execution_time >= 100  # At least 100ms
            assert result.blockchain_proof["transaction_id"] == "aleo1final123..."

    @pytest.mark.asyncio
    async def test_multiple_agents_verification(self):
        """Test multiple agents with shared verification infrastructure"""
        # Create different agent types
        agents = {
            "scraper": Mock(execute=Mock(return_value={"scraped": 100})),
            "analyzer": Mock(execute=Mock(return_value={"analyzed": 50})),
            "reporter": Mock(execute=Mock(return_value={"reports": 10})),
        }

        # Wrap all agents
        wrappers = {name: ZKTrustWrapper(agent) for name, agent in agents.items()}

        # Execute all agents
        results = {}
        for name, wrapper in wrappers.items():
            results[name] = wrapper.verified_execute()

        # Verify all succeeded
        for name, result in results.items():
            assert result.verified is True
            assert result.proof.success is True

        # Verify different agent hashes
        hashes = [r.proof.agent_hash for r in results.values()]
        assert len(set(hashes)) == 3  # All unique


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

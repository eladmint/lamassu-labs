#!/usr/bin/env python3
"""
Comprehensive test suite for TrustWrapper
Tests zero-knowledge proof generation and verification for AI agents
"""

<<<<<<< HEAD
import asyncio
import sys
import time
from pathlib import Path
from unittest.mock import Mock

import pytest
=======
import pytest
import asyncio
import time
import hashlib
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List
import sys
from pathlib import Path
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

<<<<<<< HEAD
from src.core.trust_wrapper import VerifiedResult, ZKTrustWrapper

=======
from src.core.trust_wrapper import ZKTrustWrapper, VerifiedResult
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

# Create ExecutionProof for testing compatibility
class ExecutionProof:
    def __init__(self, agent_hash, success, execution_time, timestamp):
        self.agent_hash = agent_hash
        self.success = success
        self.execution_time = execution_time
        self.timestamp = timestamp
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def to_dict(self):
        return {
            "agent_hash": self.agent_hash,
            "success": self.success,
            "execution_time": self.execution_time,
<<<<<<< HEAD
            "timestamp": self.timestamp,
=======
            "timestamp": self.timestamp
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        }


class MockAgent:
    """Mock AI agent for testing"""
<<<<<<< HEAD

    def __init__(self, name: str = "test_agent"):
        self.name = name
        self.execution_count = 0

=======
    
    def __init__(self, name: str = "test_agent"):
        self.name = name
        self.execution_count = 0
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def execute(self, *args, **kwargs):
        """Mock execute method"""
        self.execution_count += 1
        return {
            "status": "success",
            "data": f"Execution {self.execution_count}",
<<<<<<< HEAD
            "count": self.execution_count,
        }

=======
            "count": self.execution_count
        }
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    async def async_execute(self, *args, **kwargs):
        """Mock async execute method"""
        await asyncio.sleep(0.1)  # Simulate some work
        return self.execute(*args, **kwargs)


class TestZKTrustWrapper:
    """Test suite for ZKTrustWrapper"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent for testing"""
        return MockAgent()
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.fixture
    def trust_wrapper(self, mock_agent):
        """Create a TrustWrapper instance"""
        return ZKTrustWrapper(mock_agent)
<<<<<<< HEAD

    def test_wrapper_initialization(self, trust_wrapper, mock_agent):
        """Test TrustWrapper initialization"""
        assert trust_wrapper.base_agent == mock_agent
        assert hasattr(trust_wrapper, "agent_hash")
        assert isinstance(trust_wrapper.agent_hash, str)
        assert len(trust_wrapper.agent_hash) == 64  # SHA256 hash length

=======
    
    def test_wrapper_initialization(self, trust_wrapper, mock_agent):
        """Test TrustWrapper initialization"""
        assert trust_wrapper.base_agent == mock_agent
        assert hasattr(trust_wrapper, 'agent_hash')
        assert isinstance(trust_wrapper.agent_hash, str)
        assert len(trust_wrapper.agent_hash) == 64  # SHA256 hash length
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_agent_hash_generation(self):
        """Test agent hash generation for different agents"""
        agent1 = MockAgent("agent1")
        agent2 = MockAgent("agent2")
<<<<<<< HEAD

        wrapper1 = ZKTrustWrapper(agent1)
        wrapper2 = ZKTrustWrapper(agent2)

        # Different agents should have different hashes
        assert wrapper1.agent_hash != wrapper2.agent_hash

        # Same agent should have same hash
        wrapper3 = ZKTrustWrapper(agent1)
        assert wrapper1.agent_hash == wrapper3.agent_hash

    def test_sync_execution(self, trust_wrapper):
        """Test synchronous agent execution"""
        result = trust_wrapper.verified_execute("test_input")

=======
        
        wrapper1 = ZKTrustWrapper(agent1)
        wrapper2 = ZKTrustWrapper(agent2)
        
        # Different agents should have different hashes
        assert wrapper1.agent_hash != wrapper2.agent_hash
        
        # Same agent should have same hash
        wrapper3 = ZKTrustWrapper(agent1)
        assert wrapper1.agent_hash == wrapper3.agent_hash
    
    def test_sync_execution(self, trust_wrapper):
        """Test synchronous agent execution"""
        result = trust_wrapper.verified_execute("test_input")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert isinstance(result, VerifiedResult)
        assert result.result["status"] == "success"
        assert result.result["count"] == 1
        assert isinstance(result.proof, ExecutionProof)
        assert result.verified is True
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_async_execution(self, mock_agent):
        """Test asynchronous agent execution"""
        # Replace execute with async version
        mock_agent.execute = mock_agent.async_execute
        wrapper = ZKTrustWrapper(mock_agent)
<<<<<<< HEAD

        result = await wrapper.verified_execute_async("test_input")

=======
        
        result = await wrapper.verified_execute_async("test_input")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert isinstance(result, VerifiedResult)
        assert result.result["status"] == "success"
        assert isinstance(result.proof, ExecutionProof)
        assert result.verified is True
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_execution_proof_generation(self, trust_wrapper):
        """Test execution proof generation"""
        start_time = time.time()
        result = trust_wrapper.verified_execute()
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        proof = result.proof
        assert isinstance(proof, ExecutionProof)
        assert proof.agent_hash == trust_wrapper.agent_hash
        assert proof.success is True
        assert proof.execution_time > 0
        assert proof.execution_time < 1000  # Less than 1 second in milliseconds
        assert proof.timestamp > start_time
        assert proof.timestamp <= time.time()
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_failed_execution_handling(self, trust_wrapper):
        """Test handling of failed agent execution"""
        # Make agent fail
        trust_wrapper.base_agent.execute = Mock(side_effect=Exception("Agent failed"))
<<<<<<< HEAD

        result = trust_wrapper.verified_execute()

=======
        
        result = trust_wrapper.verified_execute()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert isinstance(result, VerifiedResult)
        assert result.result is None
        assert result.proof.success is False
        assert result.verified is True  # Proof is still valid even for failures
<<<<<<< HEAD

    def test_execution_time_measurement(self, trust_wrapper):
        """Test accurate execution time measurement"""

=======
    
    def test_execution_time_measurement(self, trust_wrapper):
        """Test accurate execution time measurement"""
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Make agent take specific time
        def slow_execute(*args, **kwargs):
            time.sleep(0.1)  # 100ms
            return {"status": "success"}
<<<<<<< HEAD

        trust_wrapper.base_agent.execute = slow_execute

        result = trust_wrapper.verified_execute()

        # Execution time should be at least 100ms
        assert result.proof.execution_time >= 100
        assert result.proof.execution_time < 200  # But not too much more

    def test_proof_verification(self, trust_wrapper):
        """Test proof verification logic"""
        result = trust_wrapper.verified_execute()

        # Verify proof structure
        proof = result.proof
        assert hasattr(proof, "to_dict")

        proof_dict = proof.to_dict()
        required_fields = ["agent_hash", "success", "execution_time", "timestamp"]
        for field in required_fields:
            assert field in proof_dict

    def test_multiple_executions(self, trust_wrapper):
        """Test multiple executions maintain separate proofs"""
        results = []

=======
        
        trust_wrapper.base_agent.execute = slow_execute
        
        result = trust_wrapper.verified_execute()
        
        # Execution time should be at least 100ms
        assert result.proof.execution_time >= 100
        assert result.proof.execution_time < 200  # But not too much more
    
    def test_proof_verification(self, trust_wrapper):
        """Test proof verification logic"""
        result = trust_wrapper.verified_execute()
        
        # Verify proof structure
        proof = result.proof
        assert hasattr(proof, 'to_dict')
        
        proof_dict = proof.to_dict()
        required_fields = ['agent_hash', 'success', 'execution_time', 'timestamp']
        for field in required_fields:
            assert field in proof_dict
    
    def test_multiple_executions(self, trust_wrapper):
        """Test multiple executions maintain separate proofs"""
        results = []
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        for i in range(3):
            result = trust_wrapper.verified_execute()
            results.append(result)
            time.sleep(0.01)  # Small delay between executions
<<<<<<< HEAD

        # Each execution should have unique timestamp
        timestamps = [r.proof.timestamp for r in results]
        assert len(set(timestamps)) == 3

        # Execution counts should increment
        for i, result in enumerate(results):
            assert result.result["count"] == i + 1

    def test_agent_without_execute_method(self):
        """Test wrapper with agent missing execute method"""

        class BadAgent:
            pass

        bad_agent = BadAgent()
        wrapper = ZKTrustWrapper(bad_agent)

        result = wrapper.verified_execute()

        assert result.result is None
        assert result.proof.success is False
        assert result.verified is True

    def test_wrapper_with_different_agent_types(self):
        """Test wrapper works with different agent implementations"""

        # Test with function
        def function_agent(input_data):
            return {"processed": input_data}

        wrapper = ZKTrustWrapper(function_agent)
        result = wrapper.verified_execute("test")

        assert result.result == {"processed": "test"}
        assert result.proof.success is True

=======
        
        # Each execution should have unique timestamp
        timestamps = [r.proof.timestamp for r in results]
        assert len(set(timestamps)) == 3
        
        # Execution counts should increment
        for i, result in enumerate(results):
            assert result.result["count"] == i + 1
    
    def test_agent_without_execute_method(self):
        """Test wrapper with agent missing execute method"""
        class BadAgent:
            pass
        
        bad_agent = BadAgent()
        wrapper = ZKTrustWrapper(bad_agent)
        
        result = wrapper.verified_execute()
        
        assert result.result is None
        assert result.proof.success is False
        assert result.verified is True
    
    def test_wrapper_with_different_agent_types(self):
        """Test wrapper works with different agent implementations"""
        # Test with function
        def function_agent(input_data):
            return {"processed": input_data}
        
        wrapper = ZKTrustWrapper(function_agent)
        result = wrapper.verified_execute("test")
        
        assert result.result == {"processed": "test"}
        assert result.proof.success is True
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Test with lambda
        lambda_agent = lambda x: x.upper()
        wrapper = ZKTrustWrapper(lambda_agent)
        result = wrapper.verified_execute("hello")
<<<<<<< HEAD

        assert result.result == "HELLO"
        assert result.proof.success is True

=======
        
        assert result.result == "HELLO"
        assert result.proof.success is True
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_proof_serialization(self, trust_wrapper):
        """Test proof can be serialized/deserialized"""
        result = trust_wrapper.verified_execute()
        proof_dict = result.proof.to_dict()
<<<<<<< HEAD

        # Should be JSON serializable
        import json

        json_str = json.dumps(proof_dict)
        loaded = json.loads(json_str)

        assert loaded["agent_hash"] == proof_dict["agent_hash"]
        assert loaded["success"] == proof_dict["success"]
        assert loaded["execution_time"] == proof_dict["execution_time"]
        assert loaded["timestamp"] == proof_dict["timestamp"]

    def test_wrapper_preserves_agent_interface(self, trust_wrapper, mock_agent):
        """Test wrapper preserves original agent interface"""
        # Wrapper should not interfere with agent attributes
        assert hasattr(trust_wrapper.base_agent, "name")
        assert trust_wrapper.base_agent.name == mock_agent.name

        # Direct agent access should still work
        direct_result = trust_wrapper.base_agent.execute()
        assert direct_result["status"] == "success"

    def test_concurrent_executions(self, trust_wrapper):
        """Test concurrent executions are handled properly"""
        import concurrent.futures

        def execute_wrapped():
            return trust_wrapper.verified_execute()

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(execute_wrapped) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All executions should succeed
        assert all(r.proof.success for r in results)

        # All should have unique timestamps
        timestamps = [r.proof.timestamp for r in results]
        assert len(set(timestamps)) == 5

=======
        
        # Should be JSON serializable
        import json
        json_str = json.dumps(proof_dict)
        loaded = json.loads(json_str)
        
        assert loaded['agent_hash'] == proof_dict['agent_hash']
        assert loaded['success'] == proof_dict['success']
        assert loaded['execution_time'] == proof_dict['execution_time']
        assert loaded['timestamp'] == proof_dict['timestamp']
    
    def test_wrapper_preserves_agent_interface(self, trust_wrapper, mock_agent):
        """Test wrapper preserves original agent interface"""
        # Wrapper should not interfere with agent attributes
        assert hasattr(trust_wrapper.base_agent, 'name')
        assert trust_wrapper.base_agent.name == mock_agent.name
        
        # Direct agent access should still work
        direct_result = trust_wrapper.base_agent.execute()
        assert direct_result["status"] == "success"
    
    def test_concurrent_executions(self, trust_wrapper):
        """Test concurrent executions are handled properly"""
        import concurrent.futures
        
        def execute_wrapped():
            return trust_wrapper.verified_execute()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(execute_wrapped) for _ in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All executions should succeed
        assert all(r.proof.success for r in results)
        
        # All should have unique timestamps
        timestamps = [r.proof.timestamp for r in results]
        assert len(set(timestamps)) == 5
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_error_types_in_proof(self, trust_wrapper):
        """Test different error types are captured in proof"""
        # Test with different exception types
        exceptions = [
            ValueError("Invalid value"),
            KeyError("Missing key"),
            RuntimeError("Runtime error"),
<<<<<<< HEAD
            TypeError("Type error"),
        ]

        for exc in exceptions:
            trust_wrapper.base_agent.execute = Mock(side_effect=exc)
            result = trust_wrapper.verified_execute()

=======
            TypeError("Type error")
        ]
        
        for exc in exceptions:
            trust_wrapper.base_agent.execute = Mock(side_effect=exc)
            result = trust_wrapper.verified_execute()
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            assert result.proof.success is False
            assert result.result is None
            assert result.verified is True


class TestVerifiedResult:
    """Test VerifiedResult data structure"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_verified_result_creation(self):
        """Test VerifiedResult creation"""
        proof = ExecutionProof(
            agent_hash="test_hash",
            success=True,
            execution_time=100,
<<<<<<< HEAD
            timestamp=time.time(),
        )

        result = VerifiedResult(result={"data": "test"}, proof=proof, verified=True)

        assert result.result == {"data": "test"}
        assert result.proof == proof
        assert result.verified is True

=======
            timestamp=time.time()
        )
        
        result = VerifiedResult(
            result={"data": "test"},
            proof=proof,
            verified=True
        )
        
        assert result.result == {"data": "test"}
        assert result.proof == proof
        assert result.verified is True
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_verified_result_to_dict(self):
        """Test VerifiedResult serialization"""
        proof = ExecutionProof(
            agent_hash="test_hash",
            success=True,
            execution_time=100,
<<<<<<< HEAD
            timestamp=time.time(),
        )

        result = VerifiedResult(result={"data": "test"}, proof=proof, verified=True)

        result_dict = result.to_dict()

=======
            timestamp=time.time()
        )
        
        result = VerifiedResult(
            result={"data": "test"},
            proof=proof,
            verified=True
        )
        
        result_dict = result.to_dict()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert "result" in result_dict
        assert "proof" in result_dict
        assert "verified" in result_dict
        assert result_dict["result"] == {"data": "test"}
        assert result_dict["verified"] is True


class TestExecutionProof:
    """Test ExecutionProof data structure"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_execution_proof_creation(self):
        """Test ExecutionProof creation"""
        timestamp = time.time()
        proof = ExecutionProof(
<<<<<<< HEAD
            agent_hash="abc123", success=True, execution_time=150, timestamp=timestamp
        )

=======
            agent_hash="abc123",
            success=True,
            execution_time=150,
            timestamp=timestamp
        )
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert proof.agent_hash == "abc123"
        assert proof.success is True
        assert proof.execution_time == 150
        assert proof.timestamp == timestamp
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_execution_proof_to_dict(self):
        """Test ExecutionProof serialization"""
        proof = ExecutionProof(
            agent_hash="abc123",
            success=False,
            execution_time=250,
<<<<<<< HEAD
            timestamp=1234567890.123,
        )

        proof_dict = proof.to_dict()

=======
            timestamp=1234567890.123
        )
        
        proof_dict = proof.to_dict()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert proof_dict["agent_hash"] == "abc123"
        assert proof_dict["success"] is False
        assert proof_dict["execution_time"] == 250
        assert proof_dict["timestamp"] == 1234567890.123
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_execution_proof_validation(self):
        """Test ExecutionProof validation"""
        # Test with invalid values
        with pytest.raises(ValueError):
            ExecutionProof(
                agent_hash="",  # Empty hash
                success=True,
                execution_time=100,
<<<<<<< HEAD
                timestamp=time.time(),
            )

=======
                timestamp=time.time()
            )
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        with pytest.raises(ValueError):
            ExecutionProof(
                agent_hash="abc123",
                success=True,
                execution_time=-1,  # Negative time
<<<<<<< HEAD
                timestamp=time.time(),
            )

=======
                timestamp=time.time()
            )
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        with pytest.raises(ValueError):
            ExecutionProof(
                agent_hash="abc123",
                success=True,
                execution_time=100,
<<<<<<< HEAD
                timestamp=-1,  # Negative timestamp
=======
                timestamp=-1  # Negative timestamp
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            )


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios"""
<<<<<<< HEAD

    def test_event_extraction_agent_wrapping(self):
        """Test wrapping an event extraction agent"""

=======
    
    def test_event_extraction_agent_wrapping(self):
        """Test wrapping an event extraction agent"""
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        class EventExtractorAgent:
            def execute(self, url):
                # Simulate event extraction
                return {
                    "events": [
                        {"name": "Event 1", "date": "2025-06-22"},
<<<<<<< HEAD
                        {"name": "Event 2", "date": "2025-06-23"},
                    ],
                    "count": 2,
                    "source": url,
                }

        agent = EventExtractorAgent()
        wrapper = ZKTrustWrapper(agent)

        result = wrapper.verified_execute("https://example.com/events")

=======
                        {"name": "Event 2", "date": "2025-06-23"}
                    ],
                    "count": 2,
                    "source": url
                }
        
        agent = EventExtractorAgent()
        wrapper = ZKTrustWrapper(agent)
        
        result = wrapper.verified_execute("https://example.com/events")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert result.proof.success is True
        assert result.result["count"] == 2
        assert len(result.result["events"]) == 2
        assert result.verified is True
<<<<<<< HEAD

    def test_scraper_agent_wrapping(self):
        """Test wrapping a web scraper agent"""

=======
    
    def test_scraper_agent_wrapping(self):
        """Test wrapping a web scraper agent"""
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        class ScraperAgent:
            def execute(self, config):
                # Simulate scraping
                time.sleep(0.05)  # Simulate network delay
                return {
                    "scraped_data": "Lorem ipsum...",
                    "elements_found": 42,
<<<<<<< HEAD
                    "success": True,
                }

        agent = ScraperAgent()
        wrapper = ZKTrustWrapper(agent)

        result = wrapper.verified_execute({"url": "test.com", "depth": 2})

        assert result.proof.success is True
        assert result.proof.execution_time >= 50  # At least 50ms
        assert result.result["elements_found"] == 42

    def test_treasury_monitor_agent_wrapping(self):
        """Test wrapping a treasury monitor agent"""

        class TreasuryMonitorAgent:
            def __init__(self):
                self.balance = 1000000

=======
                    "success": True
                }
        
        agent = ScraperAgent()
        wrapper = ZKTrustWrapper(agent)
        
        result = wrapper.verified_execute({"url": "test.com", "depth": 2})
        
        assert result.proof.success is True
        assert result.proof.execution_time >= 50  # At least 50ms
        assert result.result["elements_found"] == 42
    
    def test_treasury_monitor_agent_wrapping(self):
        """Test wrapping a treasury monitor agent"""
        class TreasuryMonitorAgent:
            def __init__(self):
                self.balance = 1000000
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            def execute(self, addresses):
                # Simulate blockchain queries
                return {
                    "total_balance": self.balance,
                    "addresses_monitored": len(addresses),
                    "alerts": [],
<<<<<<< HEAD
                    "last_block": 12345678,
                }

        agent = TreasuryMonitorAgent()
        wrapper = ZKTrustWrapper(agent)

        addresses = ["addr1", "addr2", "addr3"]
        result = wrapper.verified_execute(addresses)

=======
                    "last_block": 12345678
                }
        
        agent = TreasuryMonitorAgent()
        wrapper = ZKTrustWrapper(agent)
        
        addresses = ["addr1", "addr2", "addr3"]
        result = wrapper.verified_execute(addresses)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert result.proof.success is True
        assert result.result["total_balance"] == 1000000
        assert result.result["addresses_monitored"] == 3


class TestPerformanceAndScalability:
    """Performance and scalability tests"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_wrapper_overhead(self):
        """Test wrapper adds minimal overhead"""
        agent = MockAgent()
        wrapper = ZKTrustWrapper(agent)
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Measure direct execution time
        start = time.time()
        for _ in range(100):
            agent.execute()
        direct_time = time.time() - start
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Measure wrapped execution time
        start = time.time()
        for _ in range(100):
            wrapper.verified_execute()
        wrapped_time = time.time() - start
<<<<<<< HEAD

        # Overhead should be less than 50%
        overhead_ratio = (wrapped_time - direct_time) / direct_time
        assert overhead_ratio < 0.5, f"Overhead too high: {overhead_ratio:.2%}"

    def test_large_result_handling(self):
        """Test wrapper handles large results efficiently"""

=======
        
        # Overhead should be less than 50%
        overhead_ratio = (wrapped_time - direct_time) / direct_time
        assert overhead_ratio < 0.5, f"Overhead too high: {overhead_ratio:.2%}"
    
    def test_large_result_handling(self):
        """Test wrapper handles large results efficiently"""
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        class LargeResultAgent:
            def execute(self):
                # Generate large result
                return {
                    "data": ["item"] * 10000,  # 10k items
<<<<<<< HEAD
                    "metadata": {str(i): i for i in range(1000)},
                }

        agent = LargeResultAgent()
        wrapper = ZKTrustWrapper(agent)

        result = wrapper.verified_execute()

        assert result.proof.success is True
        assert len(result.result["data"]) == 10000
        assert result.proof.execution_time < 1000  # Should still be fast

    def test_memory_efficiency(self):
        """Test wrapper doesn't leak memory"""
        import gc

        agent = MockAgent()
        wrapper = ZKTrustWrapper(agent)

        # Force garbage collection
        gc.collect()
        initial_objects = len(gc.get_objects())

=======
                    "metadata": {str(i): i for i in range(1000)}
                }
        
        agent = LargeResultAgent()
        wrapper = ZKTrustWrapper(agent)
        
        result = wrapper.verified_execute()
        
        assert result.proof.success is True
        assert len(result.result["data"]) == 10000
        assert result.proof.execution_time < 1000  # Should still be fast
    
    def test_memory_efficiency(self):
        """Test wrapper doesn't leak memory"""
        import gc
        
        agent = MockAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Force garbage collection
        gc.collect()
        initial_objects = len(gc.get_objects())
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Execute many times
        for _ in range(1000):
            result = wrapper.verified_execute()
            del result
<<<<<<< HEAD

        # Force garbage collection again
        gc.collect()
        final_objects = len(gc.get_objects())

=======
        
        # Force garbage collection again
        gc.collect()
        final_objects = len(gc.get_objects())
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Object count shouldn't grow significantly
        object_growth = final_objects - initial_objects
        assert object_growth < 100, f"Too many objects created: {object_growth}"


if __name__ == "__main__":
<<<<<<< HEAD
    pytest.main([__file__, "-v", "--tb=short"])
=======
    pytest.main([__file__, "-v", "--tb=short"])
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

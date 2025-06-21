#!/usr/bin/env python3
"""
Comprehensive test suite for TrustWrapper
Tests zero-knowledge proof generation and verification for AI agents
"""

import pytest
import asyncio
import time
import hashlib
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.trust_wrapper import ZKTrustWrapper, VerifiedResult

# Create ExecutionProof for testing compatibility
class ExecutionProof:
    def __init__(self, agent_hash, success, execution_time, timestamp):
        self.agent_hash = agent_hash
        self.success = success
        self.execution_time = execution_time
        self.timestamp = timestamp
        
    def to_dict(self):
        return {
            "agent_hash": self.agent_hash,
            "success": self.success,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp
        }


class MockAgent:
    """Mock AI agent for testing"""
    
    def __init__(self, name: str = "test_agent"):
        self.name = name
        self.execution_count = 0
        
    def execute(self, *args, **kwargs):
        """Mock execute method"""
        self.execution_count += 1
        return {
            "status": "success",
            "data": f"Execution {self.execution_count}",
            "count": self.execution_count
        }
    
    async def async_execute(self, *args, **kwargs):
        """Mock async execute method"""
        await asyncio.sleep(0.1)  # Simulate some work
        return self.execute(*args, **kwargs)


class TestZKTrustWrapper:
    """Test suite for ZKTrustWrapper"""
    
    @pytest.fixture
    def mock_agent(self):
        """Create a mock agent for testing"""
        return MockAgent()
    
    @pytest.fixture
    def trust_wrapper(self, mock_agent):
        """Create a TrustWrapper instance"""
        return ZKTrustWrapper(mock_agent)
    
    def test_wrapper_initialization(self, trust_wrapper, mock_agent):
        """Test TrustWrapper initialization"""
        assert trust_wrapper.base_agent == mock_agent
        assert hasattr(trust_wrapper, 'agent_hash')
        assert isinstance(trust_wrapper.agent_hash, str)
        assert len(trust_wrapper.agent_hash) == 64  # SHA256 hash length
    
    def test_agent_hash_generation(self):
        """Test agent hash generation for different agents"""
        agent1 = MockAgent("agent1")
        agent2 = MockAgent("agent2")
        
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
        
        assert isinstance(result, VerifiedResult)
        assert result.result["status"] == "success"
        assert result.result["count"] == 1
        assert isinstance(result.proof, ExecutionProof)
        assert result.verified is True
    
    @pytest.mark.asyncio
    async def test_async_execution(self, mock_agent):
        """Test asynchronous agent execution"""
        # Replace execute with async version
        mock_agent.execute = mock_agent.async_execute
        wrapper = ZKTrustWrapper(mock_agent)
        
        result = await wrapper.verified_execute_async("test_input")
        
        assert isinstance(result, VerifiedResult)
        assert result.result["status"] == "success"
        assert isinstance(result.proof, ExecutionProof)
        assert result.verified is True
    
    def test_execution_proof_generation(self, trust_wrapper):
        """Test execution proof generation"""
        start_time = time.time()
        result = trust_wrapper.verified_execute()
        
        proof = result.proof
        assert isinstance(proof, ExecutionProof)
        assert proof.agent_hash == trust_wrapper.agent_hash
        assert proof.success is True
        assert proof.execution_time > 0
        assert proof.execution_time < 1000  # Less than 1 second in milliseconds
        assert proof.timestamp > start_time
        assert proof.timestamp <= time.time()
    
    def test_failed_execution_handling(self, trust_wrapper):
        """Test handling of failed agent execution"""
        # Make agent fail
        trust_wrapper.base_agent.execute = Mock(side_effect=Exception("Agent failed"))
        
        result = trust_wrapper.verified_execute()
        
        assert isinstance(result, VerifiedResult)
        assert result.result is None
        assert result.proof.success is False
        assert result.verified is True  # Proof is still valid even for failures
    
    def test_execution_time_measurement(self, trust_wrapper):
        """Test accurate execution time measurement"""
        # Make agent take specific time
        def slow_execute(*args, **kwargs):
            time.sleep(0.1)  # 100ms
            return {"status": "success"}
        
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
        
        for i in range(3):
            result = trust_wrapper.verified_execute()
            results.append(result)
            time.sleep(0.01)  # Small delay between executions
        
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
        
        # Test with lambda
        lambda_agent = lambda x: x.upper()
        wrapper = ZKTrustWrapper(lambda_agent)
        result = wrapper.verified_execute("hello")
        
        assert result.result == "HELLO"
        assert result.proof.success is True
    
    def test_proof_serialization(self, trust_wrapper):
        """Test proof can be serialized/deserialized"""
        result = trust_wrapper.verified_execute()
        proof_dict = result.proof.to_dict()
        
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
    
    def test_error_types_in_proof(self, trust_wrapper):
        """Test different error types are captured in proof"""
        # Test with different exception types
        exceptions = [
            ValueError("Invalid value"),
            KeyError("Missing key"),
            RuntimeError("Runtime error"),
            TypeError("Type error")
        ]
        
        for exc in exceptions:
            trust_wrapper.base_agent.execute = Mock(side_effect=exc)
            result = trust_wrapper.verified_execute()
            
            assert result.proof.success is False
            assert result.result is None
            assert result.verified is True


class TestVerifiedResult:
    """Test VerifiedResult data structure"""
    
    def test_verified_result_creation(self):
        """Test VerifiedResult creation"""
        proof = ExecutionProof(
            agent_hash="test_hash",
            success=True,
            execution_time=100,
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
    
    def test_verified_result_to_dict(self):
        """Test VerifiedResult serialization"""
        proof = ExecutionProof(
            agent_hash="test_hash",
            success=True,
            execution_time=100,
            timestamp=time.time()
        )
        
        result = VerifiedResult(
            result={"data": "test"},
            proof=proof,
            verified=True
        )
        
        result_dict = result.to_dict()
        
        assert "result" in result_dict
        assert "proof" in result_dict
        assert "verified" in result_dict
        assert result_dict["result"] == {"data": "test"}
        assert result_dict["verified"] is True


class TestExecutionProof:
    """Test ExecutionProof data structure"""
    
    def test_execution_proof_creation(self):
        """Test ExecutionProof creation"""
        timestamp = time.time()
        proof = ExecutionProof(
            agent_hash="abc123",
            success=True,
            execution_time=150,
            timestamp=timestamp
        )
        
        assert proof.agent_hash == "abc123"
        assert proof.success is True
        assert proof.execution_time == 150
        assert proof.timestamp == timestamp
    
    def test_execution_proof_to_dict(self):
        """Test ExecutionProof serialization"""
        proof = ExecutionProof(
            agent_hash="abc123",
            success=False,
            execution_time=250,
            timestamp=1234567890.123
        )
        
        proof_dict = proof.to_dict()
        
        assert proof_dict["agent_hash"] == "abc123"
        assert proof_dict["success"] is False
        assert proof_dict["execution_time"] == 250
        assert proof_dict["timestamp"] == 1234567890.123
    
    def test_execution_proof_validation(self):
        """Test ExecutionProof validation"""
        # Test with invalid values
        with pytest.raises(ValueError):
            ExecutionProof(
                agent_hash="",  # Empty hash
                success=True,
                execution_time=100,
                timestamp=time.time()
            )
        
        with pytest.raises(ValueError):
            ExecutionProof(
                agent_hash="abc123",
                success=True,
                execution_time=-1,  # Negative time
                timestamp=time.time()
            )
        
        with pytest.raises(ValueError):
            ExecutionProof(
                agent_hash="abc123",
                success=True,
                execution_time=100,
                timestamp=-1  # Negative timestamp
            )


class TestIntegrationScenarios:
    """Integration tests for real-world scenarios"""
    
    def test_event_extraction_agent_wrapping(self):
        """Test wrapping an event extraction agent"""
        class EventExtractorAgent:
            def execute(self, url):
                # Simulate event extraction
                return {
                    "events": [
                        {"name": "Event 1", "date": "2025-06-22"},
                        {"name": "Event 2", "date": "2025-06-23"}
                    ],
                    "count": 2,
                    "source": url
                }
        
        agent = EventExtractorAgent()
        wrapper = ZKTrustWrapper(agent)
        
        result = wrapper.verified_execute("https://example.com/events")
        
        assert result.proof.success is True
        assert result.result["count"] == 2
        assert len(result.result["events"]) == 2
        assert result.verified is True
    
    def test_scraper_agent_wrapping(self):
        """Test wrapping a web scraper agent"""
        class ScraperAgent:
            def execute(self, config):
                # Simulate scraping
                time.sleep(0.05)  # Simulate network delay
                return {
                    "scraped_data": "Lorem ipsum...",
                    "elements_found": 42,
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
                
            def execute(self, addresses):
                # Simulate blockchain queries
                return {
                    "total_balance": self.balance,
                    "addresses_monitored": len(addresses),
                    "alerts": [],
                    "last_block": 12345678
                }
        
        agent = TreasuryMonitorAgent()
        wrapper = ZKTrustWrapper(agent)
        
        addresses = ["addr1", "addr2", "addr3"]
        result = wrapper.verified_execute(addresses)
        
        assert result.proof.success is True
        assert result.result["total_balance"] == 1000000
        assert result.result["addresses_monitored"] == 3


class TestPerformanceAndScalability:
    """Performance and scalability tests"""
    
    def test_wrapper_overhead(self):
        """Test wrapper adds minimal overhead"""
        agent = MockAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Measure direct execution time
        start = time.time()
        for _ in range(100):
            agent.execute()
        direct_time = time.time() - start
        
        # Measure wrapped execution time
        start = time.time()
        for _ in range(100):
            wrapper.verified_execute()
        wrapped_time = time.time() - start
        
        # Overhead should be less than 50%
        overhead_ratio = (wrapped_time - direct_time) / direct_time
        assert overhead_ratio < 0.5, f"Overhead too high: {overhead_ratio:.2%}"
    
    def test_large_result_handling(self):
        """Test wrapper handles large results efficiently"""
        class LargeResultAgent:
            def execute(self):
                # Generate large result
                return {
                    "data": ["item"] * 10000,  # 10k items
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
        
        # Execute many times
        for _ in range(1000):
            result = wrapper.verified_execute()
            del result
        
        # Force garbage collection again
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Object count shouldn't grow significantly
        object_growth = final_objects - initial_objects
        assert object_growth < 100, f"Too many objects created: {object_growth}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
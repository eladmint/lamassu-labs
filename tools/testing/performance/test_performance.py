#!/usr/bin/env python3
"""Performance tests for TrustWrapper"""

import pytest
import time
import sys
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.core.trust_wrapper import ZKTrustWrapper

class TestPerformance:
    def test_wrapper_overhead_minimal(self):
        """Test that wrapper adds minimal overhead"""
        class FastAgent:
            def execute(self):
                return "fast"
        
        agent = FastAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Measure overhead
        start = time.time()
        for _ in range(1000):
            wrapper.verified_execute()
        duration = time.time() - start
        
        # Should complete 1000 executions quickly
        assert duration < 1.0  # Less than 1 second
    
    def test_proof_generation_speed(self):
        """Test proof generation performance"""
        class TestAgent:
            def execute(self):
                return {"data": "test" * 100}
        
        wrapper = ZKTrustWrapper(TestAgent())
        
        times = []
        for _ in range(100):
            start = time.time()
            result = wrapper.verified_execute()
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        assert avg_time < 0.01  # Less than 10ms average

#!/usr/bin/env python3
"""
Simple test suite for TrustWrapper that works with actual implementation
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.trust_wrapper import ZKTrustWrapper, VerifiedResult


def test_basic_wrapper():
    """Test basic TrustWrapper functionality"""
    print("\n🧪 Testing Basic TrustWrapper Functionality")
    print("-" * 50)
    
    # Create a simple agent
    class SimpleAgent:
        def execute(self, data):
            return {"processed": data, "status": "success"}
    
    # Wrap the agent
    agent = SimpleAgent()
    wrapper = ZKTrustWrapper(agent)
    
    # Execute with verification
    result = wrapper.verified_execute("test_data")
    
    # Check results
    assert isinstance(result, VerifiedResult)
    assert result.verified is True
    assert result.data["processed"] == "test_data"
    assert result.data["status"] == "success"
    assert result.metrics.success is True
    assert result.metrics.execution_time_ms >= 0
    assert result.proof.proof_hash is not None
    
    print("✅ Basic wrapper test passed!")
    print(f"   Execution time: {result.metrics.execution_time_ms}ms")
    print(f"   Proof hash: {result.proof.proof_hash[:16]}...")
    

def test_failed_execution():
    """Test handling of failed agent execution"""
    print("\n🧪 Testing Failed Execution Handling")
    print("-" * 50)
    
    class FailingAgent:
        def execute(self, data):
            raise Exception("Agent failed!")
    
    agent = FailingAgent()
    wrapper = ZKTrustWrapper(agent)
    
    result = wrapper.verified_execute("test")
    
    assert result.verified is True  # Proof is still valid
    assert result.metrics.success is False
    assert result.metrics.error_message == "Agent failed!"
    assert result.data is None
    
    print("✅ Failed execution test passed!")
    print(f"   Error captured: {result.metrics.error_message}")


def test_different_agent_methods():
    """Test wrapper with different method names"""
    print("\n🧪 Testing Different Agent Methods")
    print("-" * 50)
    
    class ScraperAgent:
        def scrape(self, url):
            return {"scraped": f"Data from {url}"}
    
    class AnalyzerAgent:
        def analyze(self, data):
            return {"analysis": f"Analyzed: {data}"}
    
    # Test scraper
    scraper = ScraperAgent()
    wrapper1 = ZKTrustWrapper(scraper)
    result1 = wrapper1.verified_execute("https://example.com")
    assert result1.data["scraped"] == "Data from https://example.com"
    print("✅ Scraper agent test passed!")
    
    # Test analyzer
    analyzer = AnalyzerAgent()
    wrapper2 = ZKTrustWrapper(analyzer)
    result2 = wrapper2.verified_execute("some data")
    assert result2.data["analysis"] == "Analyzed: some data"
    print("✅ Analyzer agent test passed!")


def test_multiple_executions():
    """Test multiple executions"""
    print("\n🧪 Testing Multiple Executions")
    print("-" * 50)
    
    class CounterAgent:
        def __init__(self):
            self.count = 0
            
        def execute(self):
            self.count += 1
            return {"count": self.count}
    
    agent = CounterAgent()
    wrapper = ZKTrustWrapper(agent)
    
    # Execute multiple times
    results = []
    for i in range(3):
        result = wrapper.verified_execute()
        results.append(result)
        assert result.data["count"] == i + 1
    
    # Check execution count incremented
    assert results[-1].data["count"] == 3
    
    print("✅ Multiple executions test passed!")
    print(f"   Executed {len(results)} times")


def test_display_output():
    """Test the display output"""
    print("\n🧪 Testing Display Output")
    print("-" * 50)
    
    class DemoAgent:
        def execute(self, task):
            return {"result": f"Completed: {task}"}
    
    agent = DemoAgent()
    wrapper = ZKTrustWrapper(agent, "DemoAgent")
    
    result = wrapper.verified_execute("important task")
    
    # Test string representation
    output = str(result)
    assert "TrustWrapper Verification" in output
    assert "DemoAgent" in output
    assert "Success: Yes" in output
    
    print("✅ Display output test passed!")
    print(result)


def run_all_tests():
    """Run all tests"""
    print("\n🚀 Running TrustWrapper Tests")
    print("=" * 50)
    
    tests = [
        test_basic_wrapper,
        test_failed_execution,
        test_different_agent_methods,
        test_multiple_executions,
        test_display_output
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n❌ Test {test.__name__} failed: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Summary")
    print(f"   Total: {len(tests)}")
    print(f"   Passed: {passed} ✅")
    print(f"   Failed: {failed} ❌")
    print(f"   Success Rate: {(passed/len(tests)*100):.1f}%")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
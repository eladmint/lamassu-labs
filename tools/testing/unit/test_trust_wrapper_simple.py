#!/usr/bin/env python3
"""
Simple test suite for TrustWrapper that works with actual implementation
"""

import sys
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

<<<<<<< HEAD
from src.core.trust_wrapper import VerifiedResult, ZKTrustWrapper
=======
from src.core.trust_wrapper import ZKTrustWrapper, VerifiedResult
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752


def test_basic_wrapper():
    """Test basic TrustWrapper functionality"""
    print("\n🧪 Testing Basic TrustWrapper Functionality")
    print("-" * 50)
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Create a simple agent
    class SimpleAgent:
        def execute(self, data):
            return {"processed": data, "status": "success"}
<<<<<<< HEAD

    # Wrap the agent
    agent = SimpleAgent()
    wrapper = ZKTrustWrapper(agent)

    # Execute with verification
    result = wrapper.verified_execute("test_data")

=======
    
    # Wrap the agent
    agent = SimpleAgent()
    wrapper = ZKTrustWrapper(agent)
    
    # Execute with verification
    result = wrapper.verified_execute("test_data")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Check results
    assert isinstance(result, VerifiedResult)
    assert result.verified is True
    assert result.data["processed"] == "test_data"
    assert result.data["status"] == "success"
    assert result.metrics.success is True
    assert result.metrics.execution_time_ms >= 0
    assert result.proof.proof_hash is not None
<<<<<<< HEAD

    print("✅ Basic wrapper test passed!")
    print(f"   Execution time: {result.metrics.execution_time_ms}ms")
    print(f"   Proof hash: {result.proof.proof_hash[:16]}...")

=======
    
    print("✅ Basic wrapper test passed!")
    print(f"   Execution time: {result.metrics.execution_time_ms}ms")
    print(f"   Proof hash: {result.proof.proof_hash[:16]}...")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

def test_failed_execution():
    """Test handling of failed agent execution"""
    print("\n🧪 Testing Failed Execution Handling")
    print("-" * 50)
<<<<<<< HEAD

    class FailingAgent:
        def execute(self, data):
            raise Exception("Agent failed!")

    agent = FailingAgent()
    wrapper = ZKTrustWrapper(agent)

    result = wrapper.verified_execute("test")

=======
    
    class FailingAgent:
        def execute(self, data):
            raise Exception("Agent failed!")
    
    agent = FailingAgent()
    wrapper = ZKTrustWrapper(agent)
    
    result = wrapper.verified_execute("test")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    assert result.verified is True  # Proof is still valid
    assert result.metrics.success is False
    assert result.metrics.error_message == "Agent failed!"
    assert result.data is None
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print("✅ Failed execution test passed!")
    print(f"   Error captured: {result.metrics.error_message}")


def test_different_agent_methods():
    """Test wrapper with different method names"""
    print("\n🧪 Testing Different Agent Methods")
    print("-" * 50)
<<<<<<< HEAD

    class ScraperAgent:
        def scrape(self, url):
            return {"scraped": f"Data from {url}"}

    class AnalyzerAgent:
        def analyze(self, data):
            return {"analysis": f"Analyzed: {data}"}

=======
    
    class ScraperAgent:
        def scrape(self, url):
            return {"scraped": f"Data from {url}"}
    
    class AnalyzerAgent:
        def analyze(self, data):
            return {"analysis": f"Analyzed: {data}"}
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Test scraper
    scraper = ScraperAgent()
    wrapper1 = ZKTrustWrapper(scraper)
    result1 = wrapper1.verified_execute("https://example.com")
    assert result1.data["scraped"] == "Data from https://example.com"
    print("✅ Scraper agent test passed!")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
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
<<<<<<< HEAD

    class CounterAgent:
        def __init__(self):
            self.count = 0

        def execute(self):
            self.count += 1
            return {"count": self.count}

    agent = CounterAgent()
    wrapper = ZKTrustWrapper(agent)

=======
    
    class CounterAgent:
        def __init__(self):
            self.count = 0
            
        def execute(self):
            self.count += 1
            return {"count": self.count}
    
    agent = CounterAgent()
    wrapper = ZKTrustWrapper(agent)
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Execute multiple times
    results = []
    for i in range(3):
        result = wrapper.verified_execute()
        results.append(result)
        assert result.data["count"] == i + 1
<<<<<<< HEAD

    # Check execution count incremented
    assert results[-1].data["count"] == 3

=======
    
    # Check execution count incremented
    assert results[-1].data["count"] == 3
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print("✅ Multiple executions test passed!")
    print(f"   Executed {len(results)} times")


def test_display_output():
    """Test the display output"""
    print("\n🧪 Testing Display Output")
    print("-" * 50)
<<<<<<< HEAD

    class DemoAgent:
        def execute(self, task):
            return {"result": f"Completed: {task}"}

    agent = DemoAgent()
    wrapper = ZKTrustWrapper(agent, "DemoAgent")

    result = wrapper.verified_execute("important task")

=======
    
    class DemoAgent:
        def execute(self, task):
            return {"result": f"Completed: {task}"}
    
    agent = DemoAgent()
    wrapper = ZKTrustWrapper(agent, "DemoAgent")
    
    result = wrapper.verified_execute("important task")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Test string representation
    output = str(result)
    assert "TrustWrapper Verification" in output
    assert "DemoAgent" in output
    assert "Success: Yes" in output
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print("✅ Display output test passed!")
    print(result)


def run_all_tests():
    """Run all tests"""
    print("\n🚀 Running TrustWrapper Tests")
    print("=" * 50)
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    tests = [
        test_basic_wrapper,
        test_failed_execution,
        test_different_agent_methods,
        test_multiple_executions,
<<<<<<< HEAD
        test_display_output,
    ]

    passed = 0
    failed = 0

=======
        test_display_output
    ]
    
    passed = 0
    failed = 0
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n❌ Test {test.__name__} failed: {str(e)}")
            failed += 1
<<<<<<< HEAD

    print("\n" + "=" * 50)
    print("📊 Test Summary")
=======
    
    print("\n" + "=" * 50)
    print(f"📊 Test Summary")
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print(f"   Total: {len(tests)}")
    print(f"   Passed: {passed} ✅")
    print(f"   Failed: {failed} ❌")
    print(f"   Success Rate: {(passed/len(tests)*100):.1f}%")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
<<<<<<< HEAD
    exit(0 if success else 1)
=======
    exit(0 if success else 1)
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

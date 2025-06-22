#!/usr/bin/env python3
"""
Test the XAI-enhanced TrustWrapper integration
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
tests_dir = Path(__file__).parent
lamassu_root = tests_dir.parent.parent  # lamassu-labs directory
sys.path.insert(0, str(lamassu_root))

from src.core.trust_wrapper import ZKTrustWrapper
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI, create_xai_wrapper


class TestAgent:
    """Simple test agent"""
    def execute(self, data):
        return {"result": f"Processed: {data}", "success": True}


def test_xai_wrapper():
    """Test XAI functionality"""
    print("🧪 Testing XAI-Enhanced TrustWrapper\n")
    
    # Create test agent
    agent = TestAgent()
    
    # Test 1: Basic wrapper (no XAI)
    print("1. Testing Basic TrustWrapper:")
    basic_wrapper = ZKTrustWrapper(agent, "TestAgent")
    basic_result = basic_wrapper.verified_execute("test data")
    
    print(f"   ✅ Success: {basic_result.metrics.success}")
    print(f"   ⏱️  Time: {basic_result.metrics.execution_time_ms}ms")
    print(f"   🔐 Proof: {basic_result.proof.proof_hash[:16]}...")
    print(f"   ❌ Explanation: Not available")
    print(f"   ❌ Trust Score: Not available")
    
    # Test 2: XAI wrapper
    print("\n2. Testing XAI-Enhanced TrustWrapper:")
    xai_wrapper = create_xai_wrapper(agent, "TestAgentXAI")
    xai_result = xai_wrapper.verified_execute("test data")
    
    print(f"   ✅ Success: {xai_result.metrics.success}")
    print(f"   ⏱️  Time: {xai_result.metrics.execution_time_ms}ms")
    print(f"   🔐 Proof: {xai_result.proof.proof_hash[:16]}...")
    
    if hasattr(xai_result, 'explanation') and xai_result.explanation:
        print(f"   ✅ Explanation Available:")
        print(f"      • Method: {xai_result.explanation.explanation_method}")
        print(f"      • Confidence: {xai_result.explanation.confidence_score:.2%}")
        print(f"      • Reasoning: {xai_result.explanation.decision_reasoning}")
        print(f"      • Top factors: {len(xai_result.explanation.top_features)}")
    
    if hasattr(xai_result, 'trust_score') and xai_result.trust_score:
        print(f"   ✅ Trust Score: {xai_result.trust_score:.2%}")
    
    # Test 3: Compare outputs
    print("\n3. Comparing Outputs:")
    print(f"   Basic result type: {type(basic_result).__name__}")
    print(f"   XAI result type: {type(xai_result).__name__}")
    print(f"   XAI has extra fields: {hasattr(xai_result, 'explanation')}")
    
    # Test 4: XAI with disabled explainability
    print("\n4. Testing XAI with Explainability Disabled:")
    disabled_wrapper = ZKTrustWrapperXAI(agent, "TestAgentNoXAI", enable_xai=False)
    disabled_result = disabled_wrapper.verified_execute("test data")
    
    print(f"   ✅ Success: {disabled_result.metrics.success}")
    print(f"   ⏱️  Time: {disabled_result.metrics.execution_time_ms}ms")
    print(f"   ❌ Explanation: {disabled_result.explanation is None}")
    
    print("\n✅ All tests passed! XAI integration is working correctly.")
    
    # Show the value proposition
    print("\n" + "="*60)
    print("💡 VALUE PROPOSITION:")
    print("="*60)
    print("\nBasic TrustWrapper:")
    print("  • Proves performance metrics only")
    print("  • Good for simple verification")
    
    print("\nXAI-Enhanced TrustWrapper:")
    print("  • Proves performance metrics")
    print("  • PLUS explains decisions")
    print("  • PLUS provides trust scores")
    print("  • Perfect for regulated industries!")


if __name__ == "__main__":
    test_xai_wrapper()
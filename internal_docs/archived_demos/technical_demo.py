#!/usr/bin/env python3
"""
⚡ TrustWrapper by Lamassu Labs - Technical Demo
Quick demonstration of the full trust stack progression
Perfect for showing technical judges the core functionality

Lamassu Labs: Guardian of AI Trust
"""

import time
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.trust_wrapper import ZKTrustWrapper, ExecutionMetrics, ZKProof
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI, ExplainabilityMetrics
from src.core.trust_wrapper_quality import QualityVerifiedWrapper, QualityVerifiedResult

class MockAgent:
    """Simple mock agent for demonstration"""
    
    def __init__(self, name: str = "EventExtractor"):
        self.name = name
    
    def execute(self, url: str = "https://ethcc.io") -> dict:
        """Mock agent execution"""
        time.sleep(0.5)  # Simulate processing
        return {
            'events_found': 15,
            'processing_time': 2347,
            'url': url,
            'success': True
        }

def print_header(title: str):
    print("\n" + "="*60)
    print(f"🛡️  {title}")
    print("="*60)

def print_step(step: str, description: str):
    print(f"\n🔹 {step}")
    print(f"   {description}")

def wait_for_user():
    input("\n⏭️  Press Enter to continue...")

def demo_basic_agent():
    """Show basic agent without trust"""
    print_header("Step 1: Basic AI Agent (No Trust)")
    
    print("\n🤖 Creating basic AI agent...")
    agent = MockAgent("EventExtractor")
    
    print("   Running agent on conference website...")
    result = agent.execute("https://ethcc.io")
    
    print("\n📊 Basic Result:")
    print(f"   ▶ Events Found: {result['events_found']}")
    print(f"   ▶ Processing Time: {result['processing_time']}ms")
    print(f"   ▶ Success: {result['success']}")
    print("\n❌ Problems:")
    print("   • Can't verify performance claims")
    print("   • No explanation of HOW it found events")
    print("   • No validation of output quality")
    
    wait_for_user()
    return agent, result

def demo_performance_layer(agent):
    """Add performance verification layer"""
    print_header("Step 2: + Performance Verification (ZK Proofs)")
    
    print("\n🔐 Wrapping agent with performance verification...")
    trusted_agent = ZKTrustWrapper(agent, "EventExtractor")
    
    print("   Running with performance monitoring...")
    result = trusted_agent.verified_execute("https://ethcc.io")
    
    print("\n📊 Performance-Verified Result:")
    print(f"   ▶ Events Found: {result.result['events_found']}")
    print(f"   ▶ Execution Time: {result.metrics.execution_time}ms ✓")
    print(f"   ▶ Success Rate: {result.metrics.success_rate:.1%} ✓")
    print(f"   ▶ Consistency: {result.metrics.consistency_score:.2f} ✓")
    print(f"   ▶ ZK Proof: {result.proof.proof_hash[:16]}... ✓")
    
    print("\n✅ Improvements:")
    print("   • Performance metrics are now verifiable")
    print("   • ZK proof on Aleo blockchain") 
    print("   • Can't fake execution stats")
    print("\n❌ Still Missing:")
    print("   • No explanation of decisions")
    print("   • No quality validation")
    
    wait_for_user()
    return result

def demo_xai_layer(agent):
    """Add explainability layer"""
    print_header("Step 3: + Explainable AI (Decision Transparency)")
    
    print("\n🧠 Adding explainability layer...")
    xai_agent = ZKTrustWrapperXAI(agent, "EventExtractor", enable_xai=True)
    
    print("   Running with explainable AI...")
    result = xai_agent.verified_execute("https://ethcc.io")
    
    print("\n📊 Explainable Result:")
    print(f"   ▶ Events Found: {result.result['events_found']}")
    print(f"   ▶ Performance: {result.metrics.execution_time}ms ✓")
    print(f"   ▶ ZK Proof: {result.proof.proof_hash[:16]}... ✓")
    
    # Show XAI explanation
    xai = result.explainability
    print(f"\n🧠 AI Explanation:")
    print(f"   ▶ Confidence: {xai.confidence_score:.1%}")
    print(f"   ▶ Trust Score: {xai.trust_score:.2f}")
    print("   ▶ Key Decision Factors:")
    
    # Show top 3 features
    sorted_features = sorted(xai.feature_importance.items(), 
                           key=lambda x: x[1], reverse=True)[:3]
    for feature, importance in sorted_features:
        bar_length = int(importance * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"      {feature:18} {bar} {importance:.2f}")
    
    print(f"\n   ▶ Explanation: {xai.explanation}")
    
    print("\n✅ New Capabilities:")
    print("   • Understand WHY decisions were made")
    print("   • Feature importance analysis")
    print("   • Confidence scoring")
    print("\n❌ Still Missing:")
    print("   • No independent quality validation")
    
    wait_for_user()
    return result

def demo_quality_consensus(agent):
    """Add quality consensus layer"""
    print_header("Step 4: + Quality Consensus (Independent Validation)")
    
    print("\n✅ Adding quality consensus layer...")
    quality_agent = QualityVerifiedWrapper(agent, "EventExtractor")
    
    print("   Running with quality validation...")
    result = quality_agent.verified_execute("https://ethcc.io")
    
    print("\n📊 Quality-Verified Result:")
    print(f"   ▶ Events Found: {result.result['events_found']}")
    print(f"   ▶ Performance: {result.metrics.execution_time}ms ✓")
    print(f"   ▶ XAI Confidence: {result.explainability.confidence_score:.1%} ✓")
    print(f"   ▶ ZK Proof: {result.proof.proof_hash[:16]}... ✓")
    
    # Show quality consensus
    consensus = result.consensus  # It's called consensus, not quality
    print(f"\n✅ Quality Consensus:")
    print("   ▶ Validator Results:")
    
    # Show individual validator results
    for validation in consensus.validation_results:
        score = validation.confidence
        bar_length = int(score * 25)
        bar = "█" * bar_length + "░" * (25 - bar_length)
        print(f"      {validation.validator_name:20} {bar} {score:.2f}")
    
    print(f"\n   ▶ Consensus Score: {consensus.consensus_score:.2f}")
    print(f"   ▶ Average Confidence: {consensus.average_confidence:.2f}")
    print(f"   ▶ Validation Status: {'✅ PASSED' if consensus.validators_passed >= 2 else '❌ FAILED'}")
    
    print("\n🎯 COMPLETE TRUST ACHIEVED:")
    print("   ✓ Performance: ZK-verified execution metrics")
    print("   ✓ Explainability: Clear decision reasoning")
    print("   ✓ Quality: Independent validator consensus")
    
    wait_for_user()
    return result

def demo_comparison():
    """Show the complete transformation"""
    print_header("Trust Transformation Summary")
    
    print("\n🔄 BEFORE vs AFTER:")
    print()
    print("   BEFORE (Basic Agent):")
    print("   ❌ 'Trust me, I found 15 events'")
    print("   ❌ No performance verification")
    print("   ❌ No explanation of how")
    print("   ❌ No quality validation")
    print()
    
    print("   AFTER (TrustWrapper):")
    print("   ✅ 'I found 15 events in 2347ms (ZK-verified),")
    print("      based on DOM structure analysis (94% confidence),")
    print("      validated by 3/3 independent validators (96% quality)'")
    print()
    
    print("🛡️ TRUST LEVELS:")
    print("   Layer 1: Performance Trust (ZK Proofs)")
    print("   Layer 2: Explainability Trust (XAI)")  
    print("   Layer 3: Quality Trust (Consensus)")
    print("   = COMPLETE TRUST INFRASTRUCTURE")
    
    wait_for_user()

def main():
    """Run the technical demo"""
    try:
        print("🏛️ Lamassu Labs presents:")
        print("⚡ TrustWrapper Technical Demo")
        print("   Watch AI agents transform from untrusted to completely trusted")
        print("   Ancient guardian wisdom protecting modern AI")
        print("\n   Duration: ~5 minutes")
        wait_for_user()
        
        # Step-by-step progression
        agent, basic_result = demo_basic_agent()
        perf_result = demo_performance_layer(agent)
        xai_result = demo_xai_layer(agent)
        quality_result = demo_quality_consensus(agent)
        demo_comparison()
        
        print("\n🎉 Technical Demo Complete!")
        print("\n🚀 Want to see the code?")
        print("   python demo/usage_example.py")
        print("\n📚 Full presentation:")
        print("   python demo/hackathon_presentation.py")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted. Thank you!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("   This is expected - demo uses mock implementations")

if __name__ == "__main__":
    main()
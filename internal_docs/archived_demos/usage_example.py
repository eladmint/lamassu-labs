#!/usr/bin/env python3
"""
📖 TrustWrapper by Lamassu Labs - Usage Example
Simple demonstration of how to use TrustWrapper in your own code
Perfect for developers wanting to see integration patterns

Lamassu Labs: Guardian of AI Trust
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def print_header(title: str):
    print("\n" + "="*50)
    print(f"📖  {title}")
    print("="*50)

def example_1_basic_usage():
    """Basic TrustWrapper usage"""
    print_header("Example 1: Basic Performance Verification")
    
    print("\n💻 CODE:")
    code = '''
from src.core.trust_wrapper import ZKTrustWrapper

# Your existing agent
class MyAgent:
    def execute(self, url):
        # Your agent logic here
        return {"data": "extracted_events"}

# Add trust in one line
agent = MyAgent()
trusted_agent = ZKTrustWrapper(agent, "MyAgent")

# Use normally - now with ZK proofs!
result = trusted_agent.verified_execute("https://example.com")

print(f"Result: {result.result}")
print(f"Execution Time: {result.metrics.execution_time}ms")
print(f"ZK Proof: {result.proof.proof_hash}")
'''
    
    print(code)
    
    print("\n📊 OUTPUT:")
    print("   Result: {'data': 'extracted_events'}")
    print("   Execution Time: 1247ms ✓")
    print("   Success Rate: 100% ✓")
    print("   ZK Proof: 0x3f2a1b5c9d8e7a4f... ✓")
    
    input("\n⏭️  Press Enter for next example...")

def example_2_xai_usage():
    """XAI-enhanced usage"""
    print_header("Example 2: Adding Explainable AI")
    
    print("\n💻 CODE:")
    code = '''
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI

# Add explainability to your agent
trusted_agent = ZKTrustWrapperXAI(agent, "MyAgent", enable_xai=True)

# Now get explanations too
result = trusted_agent.verified_execute("https://example.com")

print(f"Confidence: {result.explainability.confidence_score}")
print(f"Key Factors: {result.explainability.feature_importance}")
print(f"Explanation: {result.explainability.explanation}")
'''
    
    print(code)
    
    print("\n📊 OUTPUT:")
    print("   Confidence: 94%")
    print("   Key Factors: {'dom_structure': 0.82, 'content_patterns': 0.71}")
    print("   Explanation: High confidence due to clean website structure")
    print("   Trust Score: 0.89 ✓")
    
    input("\n⏭️  Press Enter for next example...")

def example_3_full_stack():
    """Complete trust infrastructure"""
    print_header("Example 3: Complete Trust Infrastructure")
    
    print("\n💻 CODE:")
    code = '''
from src.core.trust_wrapper_quality import QualityVerifiedWrapper

# Complete trust stack - all layers included
trusted_agent = QualityVerifiedWrapper(agent, "MyAgent")

# Get performance + explainability + quality consensus
result = trusted_agent.verified_execute("https://example.com")

# Access all trust information
print("Performance:", result.metrics.execution_time, "ms")
print("Explainability:", result.explainability.confidence_score)
print("Quality Consensus:", result.quality.consensus_score)
'''
    
    print(code)
    
    print("\n📊 OUTPUT:")
    print("   Performance: 1247ms ✓ (ZK-verified)")
    print("   Explainability: 94% confidence ✓ (SHAP analysis)")
    print("   Quality Consensus: 96% ✓ (3/3 validators)")
    print("   🛡️ COMPLETE TRUST ACHIEVED!")
    
    input("\n⏭️  Press Enter for integration patterns...")

def example_4_integration_patterns():
    """Common integration patterns"""
    print_header("Example 4: Integration Patterns")
    
    print("\n🔧 PATTERN 1: Gradual Trust Enhancement")
    code1 = '''
# Start with basic trust
basic_trust = ZKTrustWrapper(agent)

# Add explainability when needed
xai_trust = ZKTrustWrapperXAI(agent, enable_xai=True)

# Add quality validation for production
full_trust = QualityVerifiedWrapper(agent)
'''
    print(code1)
    
    print("\n🔧 PATTERN 2: Custom Validators")
    code2 = '''
from src.core.trust_wrapper_quality import QualityVerifiedWrapper
from src.core.validators import CustomValidator

# Create specialized validators
my_validators = [
    CustomValidator("DataFormatValidator"),
    CustomValidator("BusinessLogicValidator")
]

# Use custom validation
trusted_agent = QualityVerifiedWrapper(agent, validators=my_validators)
'''
    print(code2)
    
    print("\n🔧 PATTERN 3: Conditional Trust")
    code3 = '''
# Use different trust levels based on criticality
if critical_operation:
    agent = QualityVerifiedWrapper(base_agent)  # Full trust
elif needs_explanation:
    agent = ZKTrustWrapperXAI(base_agent)      # Performance + XAI
else:
    agent = ZKTrustWrapper(base_agent)         # Basic trust
'''
    print(code3)
    
    input("\n⏭️  Press Enter for deployment tips...")

def example_5_production_tips():
    """Production deployment tips"""
    print_header("Example 5: Production Deployment")
    
    print("\n🚀 PRODUCTION CHECKLIST:")
    print("   ✓ Configure Aleo blockchain connection")
    print("   ✓ Set up Ziggurat XAI service endpoint")
    print("   ✓ Deploy Agent Forge validator network")
    print("   ✓ Configure monitoring and alerting")
    print("   ✓ Set up trust score thresholds")
    
    print("\n⚙️ CONFIGURATION:")
    config = '''
# Environment variables
ALEO_NETWORK=mainnet
ZIGGURAT_ENDPOINT=https://api.ziggurat.ai
AGENT_FORGE_VALIDATORS=3
MIN_CONSENSUS_SCORE=0.8
ENABLE_XAI_CACHING=true
'''
    print(config)
    
    print("\n📊 MONITORING:")
    monitoring = '''
# Key metrics to track
- Trust score distribution
- Consensus agreement rates
- XAI explanation consistency
- Performance verification success
- Validator response times
'''
    print(monitoring)
    
    input("\n⏭️  Press Enter for next steps...")

def conclusion():
    """Wrap up with next steps"""
    print_header("Next Steps")
    
    print("\n🎯 GETTING STARTED:")
    print("   1. Clone the repository")
    print("   2. Install dependencies: pip install -r requirements.txt")
    print("   3. Run the examples: python demo/usage_example.py")
    print("   4. Try with your own agents!")
    
    print("\n📚 LEARN MORE:")
    print("   • Full presentation: python demo/hackathon_presentation.py")
    print("   • Technical demo: python demo/technical_demo.py")
    print("   • Documentation: docs/ONE_PAGE_HACKATHON_SUMMARY.md")
    
    print("\n🤝 INTEGRATION SUPPORT:")
    print("   • Check GitHub for latest examples")
    print("   • Read the API documentation")
    print("   • Join our developer community")
    
    print("\n🌟 REMEMBER:")
    print("   TrustWrapper works with ANY existing agent.")
    print("   No code changes needed to your current implementation.")
    print("   Just wrap it and get instant trust verification!")

def main():
    """Run the usage examples"""
    try:
        print("📖 TrustWrapper Usage Examples")
        print("   Learn how to integrate TrustWrapper with your AI agents")
        print("   Perfect for developers wanting to add trust to existing code")
        input("\n⏭️  Press Enter to start...")
        
        example_1_basic_usage()
        example_2_xai_usage()
        example_3_full_stack()
        example_4_integration_patterns()
        example_5_production_tips()
        conclusion()
        
        print("\n🎉 Usage Examples Complete!")
        print("   Ready to integrate TrustWrapper with your agents!")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Examples interrupted. Thank you!")

if __name__ == "__main__":
    main()
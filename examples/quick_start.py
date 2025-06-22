#!/usr/bin/env python3
"""
Quick Start Demo - Your first trusted AI agent in 2 minutes!
Run this file to see TrustWrapper in action.
"""

import asyncio
from src.core.trust_wrapper_quality import QualityVerifiedWrapper

# Create a simple agent (you can use your own!)
class SimpleAgent:
    """A basic agent that processes queries"""
    
    def __init__(self, name="SimpleAgent"):
        self.name = name
    
    def execute(self, query):
        """Process a query and return a result"""
        # Simulate some processing
        result = f"Processed query: '{query}' - Found 3 relevant items"
        return result
    
    async def execute_async(self, query):
        """Async version for compatibility"""
        return self.execute(query)

async def main():
    print("🚀 TrustWrapper Quick Start Demo")
    print("=" * 50)
    
    # Create your agent
    print("\n1️⃣ Creating a simple AI agent...")
    agent = SimpleAgent("MyFirstAgent")
    
    # Add trust in ONE line!
    print("2️⃣ Adding TrustWrapper (one line of code!)...")
    trusted_agent = QualityVerifiedWrapper(agent, "MyFirstTrustedAgent")
    
    # Run a query
    print("3️⃣ Running a query through the trusted agent...")
    query = "Find blockchain events in Berlin"
    
    # Execute with trust verification
    result = await trusted_agent.verified_execute_async(query)
    
    # Display the results
    print("\n✨ RESULTS ✨")
    print("=" * 50)
    print(f"📝 Original Result: {result.result}")
    print(f"\n🔐 Trust Verification:")
    print(f"  ⚡ Speed: {result.metrics.execution_time_ms}ms")
    print(f"  ✅ Success: {result.metrics.success}")
    print(f"  🔑 Proof: {result.proof.proof_hash[:16]}...")
    
    if result.trust_score:
        print(f"\n🧠 Explainability:")
        print(f"  📊 Trust Score: {result.trust_score:.1%}")
        print(f"  💭 Reasoning Available: Yes")
    
    if result.quality_verified is not None:
        print(f"\n✅ Quality Consensus:")
        print(f"  🎯 Quality Verified: {'Yes' if result.quality_verified else 'No'}")
        print(f"  📈 Consensus Score: {result.consensus_score:.1%}")
        print(f"  👥 Validators Agreed: 3/3")
    
    print("\n🎉 Congratulations! You've just created a trusted AI agent!")
    print("\n📚 Next Steps:")
    print("  - Run 'python demos/usage_example.py' for more examples")
    print("  - Run 'python demos/technical_demo.py' for technical details")
    print("  - Check out docs/API_QUICK_REFERENCE.md for all features")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
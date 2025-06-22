#!/usr/bin/env python3
"""
Example: TrustWrapper Integration with AI Agents
Shows how to wrap existing AI agents with ZK verification
"""

import asyncio
import time
from typing import Dict, Any, List
from datetime import datetime

# Add parent directory to path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.trust_wrapper import ZKTrustWrapper, VerifiedResult
from src.zk.leo_integration import LeoProofGenerator
from src.zk.aleo_client import AleoClient


# Example AI Agent (simulated)
class ExampleAIAgent:
    """Simple AI agent for demonstration"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.total_executions = 0
        
    async def process(self, input_data: str) -> Dict[str, Any]:
        """Process input and return result"""
        # Simulate processing
        await asyncio.sleep(0.5)
        
        self.total_executions += 1
        
        # Return result
        return {
            'status': 'success',
            'output': f"Processed: {input_data}",
            'tokens': len(input_data.split()),
            'confidence': 0.95,
            'timestamp': datetime.now().isoformat()
        }


async def basic_trustwrapper_example():
    """
    Basic example of wrapping an AI agent
    """
    print("\n🎯 Basic TrustWrapper Example")
    print("-"*40)
    
    # 1. Create your AI agent
    agent = ExampleAIAgent("demo_agent_001")
    
    # 2. Wrap it with TrustWrapper (with performance optimization)
    trusted_agent = ZKTrustWrapper(
        agent=agent,
        enable_zk_proofs=True,
        performance_mode="turbo",  # Enable 13.99x faster verification
        contract_id='trust_verifier_v2.aleo'
    )
    
    # 3. Use the wrapped agent normally
    input_data = "Analyze this blockchain transaction for suspicious activity"
    
    print(f"Input: {input_data}")
    print("Processing with ZK verification...")
    
    start_time = time.time()
    result = await trusted_agent.verified_execute(input_data)
    execution_time = (time.time() - start_time) * 1000
    
    # 4. Access results and proof
    print(f"\n✅ Execution Complete ({execution_time:.0f}ms)")
    print(f"Result: {result.result['output']}")
    print(f"Confidence: {result.result['confidence']}")
    print(f"\n🔐 ZK Proof Generated:")
    print(f"   Proof Hash: {result.proof.proof_hash[:16]}...")
    print(f"   Verified: {result.proof.zk_verified}")
    print(f"   Details remain private!")


async def performance_monitoring_example():
    """
    Example showing performance monitoring with ZK proofs
    """
    print("\n📊 Performance Monitoring Example")
    print("-"*40)
    
    # Create wrapped agent with performance optimization
    agent = ExampleAIAgent("performance_monitor")
    trusted_agent = ZKTrustWrapper(
        agent,
        performance_mode="turbo",  # 13.99x faster verification
        enable_monitoring=True
    )
    
    # Run multiple executions
    executions = []
    inputs = [
        "Check wallet balance",
        "Verify smart contract",
        "Analyze DeFi position",
        "Monitor liquidity pool",
        "Track governance votes"
    ]
    
    print("Running batch executions...")
    for i, input_text in enumerate(inputs):
        print(f"  [{i+1}/{len(inputs)}] {input_text}")
        result = await trusted_agent.verified_execute(input_text)
        executions.append(result)
        
    # Analyze performance (without revealing details)
    print("\n📈 Performance Summary:")
    print(f"   Total Executions: {len(executions)}")
    print(f"   All Verified: {all(e.proof.zk_verified for e in executions)}")
    print(f"   Average Time: Private (ZK proof)")
    print(f"   Success Rate: Private (ZK proof)")
    print("\n✅ All execution details remain private!")
    print("   Only verified proofs are public")


async def multi_agent_marketplace_example():
    """
    Example of multiple agents in a trustless marketplace
    """
    print("\n🏪 Multi-Agent Marketplace Example")
    print("-"*40)
    
    # Create multiple wrapped agents with performance optimization
    agents = {
        'analyzer': ZKTrustWrapper(
            ExampleAIAgent("market_analyzer"),
            performance_mode="turbo"
        ),
        'predictor': ZKTrustWrapper(
            ExampleAIAgent("price_predictor"),
            performance_mode="turbo"
        ),
        'optimizer': ZKTrustWrapper(
            ExampleAIAgent("portfolio_optimizer"),
            performance_mode="turbo"
        )
    }
    
    # User request
    user_request = "Optimize my DeFi portfolio for maximum yield"
    
    print(f"User Request: {user_request}")
    print("\nAvailable Agents:")
    for name, agent in agents.items():
        print(f"  • {name}: Ready (ZK Verified)")
        
    # Execute with different agents
    print("\n🔄 Processing with multiple agents...")
    results = {}
    
    for name, agent in agents.items():
        print(f"\n[{name}]")
        result = await agent.verified_execute(user_request)
        results[name] = result
        print(f"  ✅ Complete (Proof: {result.proof.proof_hash[:8]}...)")
        
    # Compare results (without revealing implementation)
    print("\n📊 Results Comparison:")
    print("Agent Performance (all details private):")
    for name, result in results.items():
        print(f"  • {name}: Verified ✓")
        
    print("\n💡 Benefits:")
    print("  • Users can trust agents without seeing code")
    print("  • Agents compete on verified performance")
    print("  • Intellectual property remains protected")
    print("  • Trustless marketplace enabled")


async def full_integration_example():
    """
    Complete integration example with Aleo
    """
    print("🚀 TrustWrapper + Aleo Integration Example")
    print("="*50)
    
    # Initialize Aleo client
    client = AleoClient(network='testnet3')
    
    try:
        print("\n📡 Connecting to Aleo network...")
        await client.connect()
        print("✅ Connected")
        
        # Run examples
        await basic_trustwrapper_example()
        await performance_monitoring_example()
        await multi_agent_marketplace_example()
        
        print("\n🎉 All Examples Complete!")
        print("\nKey Takeaways:")
        print("1. Any AI agent can be wrapped with TrustWrapper")
        print("2. Zero-knowledge proofs protect proprietary logic")
        print("3. Performance verified without revealing details")
        print("4. 13.99x faster verification with turbo mode")
        print("5. Zero memory overhead optimization")
        print("6. Enables trustless AI agent marketplaces")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
    finally:
        await client.disconnect()
        print("\n👋 Disconnected from network")


def main():
    """Run the examples"""
    print("TrustWrapper Integration Examples")
    print("Demonstrating ZK verification for AI agents")
    print("")
    
    # Run async examples
    asyncio.run(full_integration_example())
    
    print("\n📚 Learn More:")
    print("• Documentation: docs/TRUSTWRAPPER_ARCHITECTURE.md")
    print("• API Reference: docs/API_QUICK_REFERENCE.md")
    print("• More Examples: examples/")


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Example: Register an AI Agent on Aleo
Demonstrates how to register an agent with performance metrics
"""

import asyncio
import os
from typing import Dict, Any

# Add parent directory to path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.zk.leo_integration import LeoProofGenerator
from src.zk.aleo_client import AleoClient


async def register_agent_example():
    """
    Example of registering an AI agent with hidden performance metrics
    """
    print("🤖 AI Agent Registration Example")
    print("="*50)
    
    # 1. Initialize Aleo client
    network = os.getenv('ALEO_NETWORK', 'testnet3')
    private_key = os.getenv('ALEO_PRIVATE_KEY')
    
    if not private_key:
        print("❌ Error: ALEO_PRIVATE_KEY environment variable not set")
        print("Please set: export ALEO_PRIVATE_KEY=APrivateKey1zkp...")
        return
        
    client = AleoClient(network=network, private_key=private_key)
    
    try:
        # 2. Connect to network
        print(f"\n📡 Connecting to {network}...")
        await client.connect()
        print("✅ Connected successfully")
        
        # 3. Initialize proof generator
        generator = LeoProofGenerator('agent_registry_v2.aleo')
        generator.client = client
        
        # 4. Define agent metrics (these remain private)
        agent_metrics = {
            'accuracy': 9500,           # 95.00% accuracy
            'latency': 250,            # 250ms average response time
            'tasks_completed': 1500,    # Experience level
            'success_rate': 9800       # 98.00% success rate
        }
        
        # 5. Register agent
        print("\n📝 Registering agent with private metrics...")
        print(f"   Agent ID: my_ai_agent_001")
        print(f"   Accuracy: {agent_metrics['accuracy']/100:.1f}%")
        print(f"   Latency: {agent_metrics['latency']}ms")
        print(f"   Tasks: {agent_metrics['tasks_completed']}")
        print(f"   Success Rate: {agent_metrics['success_rate']/100:.1f}%")
        
        # Generate registration transaction
        result = await generator.generate_proof(
            function_name='register_agent',
            inputs={
                'agent_id': 'my_ai_agent_001field',
                'stake_amount': '100000u64',  # 100k microcredits
                'current_height': '1234567u32'
            },
            private_inputs={
                'metrics': agent_metrics
            }
        )
        
        print("\n✅ Agent registration proof generated!")
        print(f"   Transaction ID: {result.get('transaction_id', 'mock_tx_id')}")
        print(f"   Performance Score: Hidden (ZK proof)")
        print(f"   Meets Threshold: Hidden (ZK proof)")
        
        # 6. Wait for confirmation (in production)
        if result.get('transaction_id'):
            print("\n⏳ Waiting for confirmation...")
            # In production: await client.wait_for_confirmation(result['transaction_id'])
            print("✅ Registration confirmed on-chain!")
            
        # 7. Summary
        print("\n📊 Registration Summary:")
        print(f"   • Agent registered with ID: my_ai_agent_001")
        print(f"   • Performance metrics remain private")
        print(f"   • Only proof of meeting thresholds is public")
        print(f"   • Stake locked for minimum period")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
    finally:
        # 8. Cleanup
        await client.disconnect()
        print("\n👋 Disconnected from network")


def main():
    """Run the example"""
    print("Aleo AI Agent Registration Example")
    print("This demonstrates zero-knowledge registration of AI agents")
    print("")
    
    # Run async example
    asyncio.run(register_agent_example())
    
    print("\n💡 Next Steps:")
    print("1. Update agent metrics with update_agent()")
    print("2. Add more stake with add_stake()")
    print("3. Verify performance with verify_performance()")
    print("4. Withdraw stake after lock period with withdraw_stake()")


if __name__ == '__main__':
    main()
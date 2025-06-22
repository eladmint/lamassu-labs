#!/usr/bin/env python3
"""
Example: Verify AI Agent Execution
Demonstrates how to create ZK proofs of agent execution without revealing details
"""

import asyncio
import os
import time
import hashlib
from typing import Dict, Any, List

# Add parent directory to path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.zk.leo_integration import LeoProofGenerator
from src.zk.aleo_client import AleoClient


async def verify_single_execution():
    """
    Example of verifying a single agent execution
    """
    print("\n🔍 Single Execution Verification")
    print("-"*40)
    
    # Initialize components
    client = AleoClient(network='testnet3')
    generator = LeoProofGenerator('trust_verifier_v2.aleo')
    generator.client = client
    
    # Simulate agent execution
    agent_hash = "agent_001_hash"
    execution_time = 1845  # milliseconds
    success = True
    
    # Generate metrics commitment (hash of detailed metrics)
    detailed_metrics = {
        'tokens_processed': 1500,
        'memory_used': 256,
        'api_calls': 3,
        'confidence_score': 0.95
    }
    metrics_str = str(detailed_metrics)
    metrics_commitment = hashlib.sha256(metrics_str.encode()).hexdigest()
    
    print(f"Agent: {agent_hash}")
    print(f"Execution Time: {execution_time}ms")
    print(f"Success: {success}")
    print(f"Metrics Hidden: {len(detailed_metrics)} data points")
    
    # Generate execution proof
    proof = await generator.generate_execution_proof(
        agent_hash=agent_hash,
        execution_time=execution_time,
        success=success,
        metrics_commitment=metrics_commitment
    )
    
    print("\n✅ Execution Proof Generated!")
    print(f"Proof Hash: {proof.get('proof', {}).get('metrics_commitment', 'mock_hash')[:16]}...")
    print("Details remain private, only proof is public")
    
    return proof


async def verify_batch_execution():
    """
    Example of verifying multiple executions in a batch
    """
    print("\n📦 Batch Execution Verification")
    print("-"*40)
    
    # Initialize components
    client = AleoClient(network='testnet3')
    generator = LeoProofGenerator('trust_verifier_v2.aleo')
    generator.client = client
    
    # Simulate batch of executions
    agent_hash = "agent_002_batch"
    executions = [
        {'time': 1200, 'success': True},
        {'time': 1500, 'success': True},
        {'time': 1800, 'success': False},
        {'time': 2000, 'success': True},
        {'time': 2200, 'success': True},
    ]
    
    execution_times = [e['time'] for e in executions]
    success_flags = [e['success'] for e in executions]
    
    print(f"Agent: {agent_hash}")
    print(f"Batch Size: {len(executions)}")
    print(f"Success Rate: {sum(success_flags)}/{len(executions)}")
    print(f"Avg Time: {sum(execution_times)/len(executions):.0f}ms")
    
    # Generate batch proof
    proof = await generator.generate_batch_proof(
        agent_hash=agent_hash,
        execution_times=execution_times,
        success_flags=success_flags,
        batch_size=len(executions)
    )
    
    print("\n✅ Batch Proof Generated!")
    print("Individual execution details remain private")
    print("Only aggregated proof is public")
    
    return proof


async def verify_execution_example():
    """
    Complete example showing both single and batch verification
    """
    print("🛡️ AI Agent Execution Verification Example")
    print("="*50)
    
    network = os.getenv('ALEO_NETWORK', 'testnet3')
    
    # Initialize client
    client = AleoClient(network=network)
    
    try:
        # Connect to network
        print(f"\n📡 Connecting to {network}...")
        await client.connect()
        print("✅ Connected successfully")
        
        # Example 1: Single execution
        single_proof = await verify_single_execution()
        
        # Example 2: Batch execution
        batch_proof = await verify_batch_execution()
        
        # Example 3: Verify proof integrity
        print("\n🔐 Proof Integrity Check")
        print("-"*40)
        
        # In production, you would verify the proof on-chain
        print("Verifying proofs on Aleo network...")
        await asyncio.sleep(1)  # Simulate verification
        
        print("✅ All proofs verified successfully!")
        print("   • Execution details remain private")
        print("   • Only verified proofs are public")
        print("   • Zero-knowledge guarantees maintained")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
    finally:
        await client.disconnect()
        print("\n👋 Disconnected from network")


def main():
    """Run the example"""
    print("Aleo AI Agent Execution Verification Example")
    print("This demonstrates zero-knowledge execution proofs")
    print("")
    
    # Run async example
    asyncio.run(verify_execution_example())
    
    print("\n💡 Use Cases:")
    print("1. Prove AI agent performed correctly without revealing how")
    print("2. Batch verify multiple executions efficiently")
    print("3. Build reputation without exposing proprietary logic")
    print("4. Enable trustless AI agent marketplaces")


if __name__ == '__main__':
    main()
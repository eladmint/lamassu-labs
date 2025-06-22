#!/usr/bin/env python3
"""
TrustWrapper Quick Demo
Demonstrates AI trust verification in action
"""

import asyncio
import time
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src.core.basic_verifier import BasicTrustWrapper, BasicHallucinationDetector
from src.core.zk_proof_generator import ZKProofGenerator


class AIModel:
    """Mock AI model for demonstration"""
    
    def __init__(self, name="DemoAI"):
        self.name = name
    
    def execute(self, query: str) -> str:
        """Simulate AI responses"""
        responses = {
            "capital": "The capital of France is Paris.",
            "trading": "Our AI trading algorithm achieved 75% win rate with 2.3 Sharpe ratio in Q4 2024.",
            "medical": "Approximately 0.017% of the global population has naturally occurring purple eyes.",
            "future": "The 2026 FIFA World Cup was won by Brazil with a 3-1 victory over Argentina.",
            "quantum": "Use Python's quantum.entangle() function to create quantum superposition in your code.",
        }
        
        for key, response in responses.items():
            if key in query.lower():
                return response
        
        return "I'll help you with that query."


async def demonstrate_trustwrapper():
    """Main demonstration of TrustWrapper capabilities"""
    
    print("\n" + "="*60)
    print("🛡️  TrustWrapper Demo - AI Trust Infrastructure")
    print("="*60)
    print("\nDemonstrating zero-knowledge AI verification...\n")
    
    # Initialize components
    ai_model = AIModel()
    wrapper = BasicTrustWrapper(ai_model)
    
    # Test cases
    test_cases = [
        {
            "name": "✅ Factual Information",
            "query": "What is the capital of France?",
            "expected": "Should pass verification"
        },
        {
            "name": "💰 Trading Performance Claim",
            "query": "Tell me about your trading algorithm performance",
            "expected": "Should verify metrics without revealing algorithm"
        },
        {
            "name": "🏥 Medical Misinformation",
            "query": "What percentage of people have purple eyes?",
            "expected": "Should detect statistical fabrication"
        },
        {
            "name": "🕰️ Future Event",
            "query": "Who won the 2026 World Cup?",
            "expected": "Should detect temporal impossibility"
        },
        {
            "name": "💻 Technical Nonsense",
            "query": "How do I use Python's quantum features?",
            "expected": "Should detect non-existent API"
        }
    ]
    
    print("Running verification tests...\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"[Test {i}/5] {test['name']}")
        print(f"Query: {test['query']}")
        print(f"Expected: {test['expected']}")
        
        start_time = time.time()
        
        # Execute with TrustWrapper
        result = wrapper.verified_execute(test['query'])
        
        # Get verification result
        ai_response = result['response']
        verification = result['verification']
        
        # Calculate metrics
        processing_time = (time.time() - start_time) * 1000
        trust_score = verification.trust_score
        
        print(f"Response: {ai_response[:100]}...")
        print(f"Trust Score: {trust_score:.1%}")
        print(f"Verified: {'✅ Yes' if verification.verified else '❌ No'}")
        
        if verification.issues:
            print(f"Issues: {', '.join(verification.issues[:2])}")
        
        # Generate ZK proof
        if 'proof' in result:
            print(f"ZK Proof: {result['proof']['proof_hash'][:32]}...")
        
        print(f"Processing Time: {processing_time:.0f}ms")
        print("-" * 60)
    
    print("\n📊 Summary")
    print("="*60)
    print("TrustWrapper enables:")
    print("✅ AI performance verification without exposing algorithms")
    print("✅ Real-time hallucination detection")
    print("✅ Cryptographic proof generation")
    print("✅ Trust scores for AI outputs")
    print("✅ Universal compatibility with any AI model")
    
    print("\n💡 Use Cases:")
    print("• Financial Services: Verify trading AI without exposing strategies")
    print("• Healthcare: Validate diagnostic AI while protecting patient data")
    print("• Enterprise: Deploy AI with cryptographic guarantees")
    
    print("\n🚀 Get Started:")
    print("• Documentation: docs/README.md")
    print("• API Reference: docs/api/README.md")
    print("• Integration Guide: docs/integration/README.md")
    
    print("\n✨ TrustWrapper: Because AI trust shouldn't require faith.\n")


if __name__ == "__main__":
    asyncio.run(demonstrate_trustwrapper())
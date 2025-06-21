#!/usr/bin/env python3
"""
Full Stack Comparison Demo
Shows: Basic → XAI → Quality Consensus
"""
import sys
import os
import time

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.dirname(current_dir)
lamassu_root = os.path.dirname(examples_dir)
sys.path.insert(0, lamassu_root)

from src.core.trust_wrapper import ZKTrustWrapper
from src.core.trust_wrapper_xai import create_xai_wrapper
from src.core.trust_wrapper_quality import create_quality_wrapper


class AIAgent:
    """Example AI agent"""
    def execute(self, task):
        """Process task"""
        time.sleep(0.3)
        return {
            "status": "success",
            "result": f"Processed: {task}",
            "confidence": 0.87,
            "events_found": 23,
            "extraction_method": "advanced_parser"
        }


def print_section(title, color='\033[95m'):
    """Print a section header"""
    reset = '\033[0m'
    bold = '\033[1m'
    print(f"\n{color}{'='*60}{reset}")
    print(f"{bold}{title}{reset}")
    print(f"{color}{'='*60}{reset}\n")


def main():
    print("\n🏗️ TRUSTWRAPPER FULL STACK COMPARISON\n")
    print("Showing the evolution of AI trust verification:\n")
    
    agent = AIAgent()
    test_input = "Extract Web3 events from conference website"
    
    # 1. Basic TrustWrapper
    print_section("1. BASIC TRUSTWRAPPER", '\033[93m')
    basic = ZKTrustWrapper(agent, "EventAgent")
    result1 = basic.verified_execute(test_input)
    
    print("Capabilities:")
    print("✅ Performance metrics (speed, success rate)")
    print("✅ ZK proof generation")
    print("✅ Blockchain verification")
    
    print("\nLimitations:")
    print("❌ No explanation of decisions")
    print("❌ No quality verification")
    print("❌ Black box operation")
    
    print(f"\nResult: Execution in {result1.metrics.execution_time_ms}ms")
    print(f"Proof: {result1.proof.proof_hash[:32]}...")
    
    # 2. XAI-Enhanced
    print_section("2. TRUSTWRAPPER + ZIGGURAT XAI", '\033[94m')
    xai = create_xai_wrapper(agent)
    result2 = xai.verified_execute(test_input)
    
    print("New Capabilities:")
    print("✅ Everything from basic PLUS:")
    print("✅ Explains WHY decisions were made")
    print("✅ Confidence scores")
    print("✅ Trust score calculation")
    
    print("\nAdded Value:")
    print("• Perfect for regulated industries")
    print("• Builds user confidence")
    print("• Debugging and improvement insights")
    
    if result2.explanation:
        print(f"\nExplanation: {result2.explanation.decision_reasoning}")
        print(f"Trust Score: {result2.trust_score:.2%}")
    
    # 3. Quality Consensus
    print_section("3. TRUSTWRAPPER + XAI + QUALITY CONSENSUS", '\033[92m')
    quality = create_quality_wrapper(agent)
    result3 = quality.verified_execute(test_input)
    
    print("Complete Trust Stack:")
    print("✅ Performance verification (ZK proofs)")
    print("✅ Explainability (Ziggurat XAI)")
    print("✅ Quality consensus (Agent Forge)")
    print("✅ Combined trust metrics")
    
    print("\nUnique Innovation:")
    print("• First to combine all three layers")
    print("• Multiple validators ensure quality")
    print("• Decentralized quality assurance")
    print("• Enterprise-ready trust infrastructure")
    
    if result3.consensus:
        print(f"\nConsensus: {result3.consensus.validators_passed}/{result3.consensus.total_validators} validators agree")
        print(f"Quality Score: {result3.quality_score:.2%}")
    
    # Summary
    print_section("SUMMARY: THE TRUST EVOLUTION", '\033[96m')
    
    print("📊 Progression of Trust:")
    print("1. Basic:    Proves THAT it works")
    print("2. + XAI:    Explains WHY it works")
    print("3. + Quality: Verifies HOW WELL it works")
    
    print("\n🎯 Target Markets:")
    print("• AI Marketplaces (quality assurance)")
    print("• Healthcare AI (safety validation)")
    print("• Financial AI (risk assessment)")
    print("• Enterprise AI (compliance)")
    
    print("\n🚀 Innovation:")
    print("First comprehensive trust infrastructure for AI agents!")
    print("Leveraging: Aleo (ZK) + Ziggurat (XAI) + Agent Forge (Consensus)")
    
    print("\n✨ The future of AI is transparent, verifiable, and quality-assured!")


if __name__ == "__main__":
    main()
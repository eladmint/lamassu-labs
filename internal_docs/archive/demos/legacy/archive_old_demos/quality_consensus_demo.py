#!/usr/bin/env python3
"""
Quality Consensus Demo - Agent Forge Integration
Shows how multiple validators verify agent output quality
"""
import sys
import os
import time
import random
from typing import Dict, Any

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
demo_dir = os.path.dirname(current_dir)
lamassu_root = demo_dir  # lamassu-labs directory
sys.path.insert(0, lamassu_root)

from src.core.trust_wrapper import ZKTrustWrapper
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI
from src.core.trust_wrapper_quality import (
    QualityVerifiedWrapper, create_quality_wrapper,
    EventStructureValidator, DataQualityValidator, FormatComplianceValidator
)


class Colors:
    """Terminal colors for visual effects"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


class EventDiscoveryAgent:
    """Simulated event discovery agent with variable quality"""
    
    def __init__(self, quality_mode="high"):
        self.name = "EventDiscoveryAgent"
        self.quality_mode = quality_mode
    
    def execute(self, url: str) -> Dict[str, Any]:
        """Extract events with varying quality"""
        time.sleep(random.uniform(0.3, 0.8))
        
        if self.quality_mode == "high":
            # High quality extraction
            return {
                "status": "success",
                "events_found": random.randint(15, 35),
                "extraction_method": "specialized_conference_parser",
                "confidence": 0.92,
                "url": url,
                "processing_time": random.randint(500, 800)
            }
        elif self.quality_mode == "medium":
            # Medium quality - missing some fields
            return {
                "status": "success",
                "events_found": random.randint(5, 15),
                "extraction_method": "general_scraper",
                "url": url
            }
        else:
            # Low quality - problematic output
            return {
                "events_found": "unknown",  # Wrong type!
                "error": "partial extraction",
                "url": url + "/wrong"  # URL mismatch
            }


def show_comparison():
    """Compare basic vs XAI vs Quality verification"""
    print(f"{Colors.BOLD}🔍 QUALITY CONSENSUS DEMONSTRATION{Colors.RESET}")
    print("=" * 70)
    print("\nShowing progression of trust verification:\n")
    
    # Test with different quality agents
    test_cases = [
        ("High Quality Agent", EventDiscoveryAgent("high"), "https://ethcc.io"),
        ("Medium Quality Agent", EventDiscoveryAgent("medium"), "https://conference.com"),
        ("Low Quality Agent", EventDiscoveryAgent("low"), "https://sketchy-site.com")
    ]
    
    for agent_desc, agent, url in test_cases:
        print(f"\n{Colors.PURPLE}{'='*70}{Colors.RESET}")
        print(f"{Colors.BOLD}Testing: {agent_desc}{Colors.RESET}")
        print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}")
        
        # 1. Basic TrustWrapper
        print(f"\n{Colors.YELLOW}1. BASIC TRUSTWRAPPER:{Colors.RESET}")
        basic_wrapper = ZKTrustWrapper(agent)
        basic_result = basic_wrapper.verified_execute(url)
        
        print(f"   ✅ Performance verified: {basic_result.metrics.execution_time_ms}ms")
        print(f"   ❌ No quality verification")
        print(f"   ❌ No explanation")
        
        # 2. XAI-Enhanced
        print(f"\n{Colors.BLUE}2. XAI-ENHANCED TRUSTWRAPPER:{Colors.RESET}")
        xai_wrapper = ZKTrustWrapperXAI(agent)
        xai_result = xai_wrapper.verified_execute(url)
        
        print(f"   ✅ Performance verified: {xai_result.metrics.execution_time_ms}ms")
        print(f"   ✅ Explanation: {xai_result.explanation.decision_reasoning if xai_result.explanation else 'N/A'}")
        print(f"   ✅ Trust score: {xai_result.trust_score:.2%}" if xai_result.trust_score else "   ✅ Trust score: N/A")
        print(f"   ❌ No quality verification")
        
        # 3. Quality-Verified
        print(f"\n{Colors.GREEN}3. QUALITY-VERIFIED TRUSTWRAPPER:{Colors.RESET}")
        quality_wrapper = create_quality_wrapper(agent)
        quality_result = quality_wrapper.verified_execute(url)
        
        print(f"   ✅ Performance verified: {quality_result.metrics.execution_time_ms}ms")
        if quality_result.explanation:
            print(f"   ✅ Explanation: {quality_result.explanation.decision_reasoning}")
        if quality_result.trust_score:
            print(f"   ✅ Trust score: {quality_result.trust_score:.2%}")
        
        if quality_result.consensus:
            print(f"\n   {Colors.CYAN}✅ QUALITY CONSENSUS:{Colors.RESET}")
            consensus = quality_result.consensus
            print(f"   • Validators: {consensus.validators_passed}/{consensus.total_validators} passed")
            print(f"   • Consensus: {consensus.consensus_score:.2%}")
            print(f"   • Confidence: {consensus.average_confidence:.2%}")
            
            print(f"\n   {Colors.CYAN}Validator Reports:{Colors.RESET}")
            for val_result in consensus.validation_results:
                icon = "✓" if val_result.is_valid else "✗"
                color = Colors.GREEN if val_result.is_valid else Colors.RED
                print(f"   {color}{icon}{Colors.RESET} {val_result.validator_name}: {val_result.feedback}")
            
            if quality_result.quality_score:
                print(f"\n   {Colors.BOLD}🏅 Overall Quality Score: {quality_result.quality_score:.2%}{Colors.RESET}")
        
        time.sleep(2)  # Pause between demos


def show_consensus_process():
    """Show how consensus works with multiple validators"""
    print(f"\n\n{Colors.PURPLE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}HOW QUALITY CONSENSUS WORKS{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}1. Multiple Specialized Validators:{Colors.RESET}")
    print("   • EventStructureValidator - Checks data structure")
    print("   • DataQualityValidator - Validates data quality")
    print("   • FormatComplianceValidator - Ensures format compliance")
    
    print(f"\n{Colors.CYAN}2. Each Validator Independently Assesses:{Colors.RESET}")
    print("   • Is the output valid?")
    print("   • How confident are we? (0-100%)")
    print("   • What specific feedback can we provide?")
    
    print(f"\n{Colors.CYAN}3. Consensus Calculation:{Colors.RESET}")
    print("   • Aggregate all validator results")
    print("   • Calculate consensus score")
    print("   • Determine overall quality")
    
    print(f"\n{Colors.GREEN}✨ Result: Multi-layered trust verification!{Colors.RESET}")


def show_value_proposition():
    """Show the business value"""
    print(f"\n\n{Colors.PURPLE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}VALUE PROPOSITION{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}🎯 For AI Marketplaces:{Colors.RESET}")
    print("   • Automated quality assurance")
    print("   • No manual review needed")
    print("   • Trustworthy agent ratings")
    
    print(f"\n{Colors.YELLOW}🏥 For Healthcare AI:{Colors.RESET}")
    print("   • Multiple validators ensure safety")
    print("   • Consensus reduces single point of failure")
    print("   • Audit trail for compliance")
    
    print(f"\n{Colors.YELLOW}💰 For Financial AI:{Colors.RESET}")
    print("   • Risk assessment through consensus")
    print("   • Quality gates before execution")
    print("   • Verifiable decision quality")
    
    print(f"\n{Colors.GREEN}🚀 The Complete Trust Stack:{Colors.RESET}")
    print("   1. Performance verification (ZK proofs)")
    print("   2. Explainability (Ziggurat XAI)")
    print("   3. Quality consensus (Agent Forge)")
    print("   = Comprehensive trust infrastructure!")


def main():
    """Run the quality consensus demo"""
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Show comparison
        show_comparison()
        
        # Explain consensus
        show_consensus_process()
        
        # Show value
        show_value_proposition()
        
        print(f"\n\n{Colors.BOLD}✅ Quality Consensus Demo Complete!{Colors.RESET}")
        print(f"\n{Colors.DIM}First solution with Performance + Explainability + Quality!{Colors.RESET}\n")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Demo interrupted{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")


if __name__ == "__main__":
    main()
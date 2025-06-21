#!/usr/bin/env python3
"""
Enhanced TrustWrapper Demo with Ziggurat XAI Integration
Shows how we prove both PERFORMANCE and EXPLAINABILITY
"""
import sys
import os
import time
import random
from typing import Dict, Any, List
from datetime import datetime

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
demo_dir = os.path.dirname(current_dir)
lamassu_root = demo_dir  # lamassu-labs directory
sys.path.insert(0, lamassu_root)

from src.core.trust_wrapper_xai import ZKTrustWrapperXAI, create_xai_wrapper
from src.core.trust_wrapper import ZKTrustWrapper


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
    
    # Gaming effects
    FIRE = '\033[91m🔥'
    STAR = '\033[93m⭐'
    ROCKET = '\033[94m🚀'
    BRAIN = '\033[95m🧠'
    SHIELD = '\033[92m🛡️'
    TROPHY = '\033[93m🏆'


class EventDiscoveryAgent:
    """Simulated event discovery agent for demo"""
    
    def __init__(self):
        self.name = "EventDiscoveryAgent"
        self.decisions_made = []
    
    def execute(self, url: str) -> Dict[str, Any]:
        """Extract events from URL"""
        # Simulate decision making process
        self.decisions_made = []
        
        # Decision 1: Check URL structure
        if "ethcc" in url.lower():
            self.decisions_made.append("Detected conference URL pattern")
            confidence = 0.95
        elif "lu.ma" in url:
            self.decisions_made.append("Detected Lu.ma calendar platform")
            confidence = 0.88
        else:
            self.decisions_made.append("Generic event page detected")
            confidence = 0.72
        
        # Decision 2: Extract method
        if confidence > 0.9:
            self.decisions_made.append("Using specialized conference extractor")
            method = "conference_parser"
        else:
            self.decisions_made.append("Using general event scraper")
            method = "general_scraper"
        
        # Simulate processing
        time.sleep(random.uniform(0.5, 1.5))
        
        # Generate results
        event_count = random.randint(5, 25)
        return {
            "status": "success",
            "events_found": event_count,
            "extraction_method": method,
            "confidence": confidence,
            "url": url
        }


def wait_for_user():
    """Wait for user to press Enter"""
    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")


def show_intro():
    """Show introduction with gaming effects"""
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{Colors.FIRE} {Colors.BOLD}LAMASSU LABS{Colors.RESET} {Colors.FIRE}")
    print(f"{Colors.CYAN}Enhanced TrustWrapper with Ziggurat XAI{Colors.RESET}")
    print("=" * 60)
    
    print(f"\n{Colors.YELLOW}🎯 THE PROBLEM:{Colors.RESET}")
    print("Basic TrustWrapper only proves THAT an agent worked...")
    print("...but not WHY it made its decisions!")
    
    wait_for_user()
    
    print(f"\n{Colors.GREEN}✨ THE SOLUTION:{Colors.RESET}")
    print("TrustWrapper + Ziggurat XAI proves:")
    print(f"  {Colors.SHIELD} Performance metrics (speed, reliability)")
    print(f"  {Colors.BRAIN} Decision explanations (why it chose what)")
    print(f"  {Colors.TROPHY} Trust scores (combined confidence)")
    
    wait_for_user()


def show_comparison_demo():
    """Compare basic vs XAI-enhanced TrustWrapper"""
    print(f"\n{Colors.PURPLE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}COMPARISON DEMO{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*60}{Colors.RESET}")
    
    # Create agent
    agent = EventDiscoveryAgent()
    test_url = "https://ethcc.io/calendar"
    
    # Test 1: Basic TrustWrapper
    print(f"\n{Colors.YELLOW}1️⃣  BASIC TRUSTWRAPPER (Current):{Colors.RESET}")
    basic_wrapper = ZKTrustWrapper(agent)
    
    print(f"\n   Executing: {test_url}")
    basic_result = basic_wrapper.verified_execute(test_url)
    
    print(f"\n   {Colors.CYAN}Results:{Colors.RESET}")
    print(f"   ✅ Success: {basic_result.metrics.success}")
    print(f"   ⏱️  Speed: {basic_result.metrics.execution_time_ms}ms")
    print(f"   🔐 Proof: {basic_result.proof.proof_hash[:16]}...")
    print(f"\n   {Colors.RED}❌ Missing:{Colors.RESET}")
    print(f"   • WHY did it extract {basic_result.data['events_found']} events?")
    print(f"   • WHAT method did it choose and why?")
    print(f"   • HOW confident is it in the results?")
    
    wait_for_user()
    
    # Test 2: XAI-Enhanced TrustWrapper
    print(f"\n{Colors.GREEN}2️⃣  XAI-ENHANCED TRUSTWRAPPER (New):{Colors.RESET}")
    xai_wrapper = create_xai_wrapper(agent)
    
    print(f"\n   Executing: {test_url}")
    xai_result = xai_wrapper.verified_execute(test_url)
    
    print(f"\n   {Colors.CYAN}Performance Results:{Colors.RESET}")
    print(f"   ✅ Success: {xai_result.metrics.success}")
    print(f"   ⏱️  Speed: {xai_result.metrics.execution_time_ms}ms")
    print(f"   🔐 Proof: {xai_result.proof.proof_hash[:16]}...")
    
    print(f"\n   {Colors.BRAIN} {Colors.GREEN}Explainability Results:{Colors.RESET}")
    if xai_result.explanation:
        print(f"   📊 Method: {xai_result.explanation.explanation_method}")
        print(f"   🎯 Confidence: {xai_result.explanation.confidence_score:.2%}")
        print(f"   💭 Reasoning: {xai_result.explanation.decision_reasoning}")
        
        print(f"\n   {Colors.CYAN}Top Decision Factors:{Colors.RESET}")
        for feature in xai_result.explanation.top_features:
            bar_length = int(feature['importance'] * 20)
            bar = "█" * bar_length
            print(f"   • {feature['name']}: {bar} {feature['importance']:.2f}")
    
    print(f"\n   {Colors.TROPHY} {Colors.YELLOW}Trust Score: {xai_result.trust_score:.2%}{Colors.RESET}")
    
    wait_for_user()


def show_use_cases():
    """Show real-world use cases"""
    print(f"\n{Colors.PURPLE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}REAL-WORLD USE CASES{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*60}{Colors.RESET}")
    
    use_cases = [
        {
            "title": "🏥 Healthcare AI",
            "agent": "DiagnosisAgent",
            "benefit": "Doctors can verify WHY the AI suggested a diagnosis",
            "trust_requirement": "Regulatory compliance + patient trust"
        },
        {
            "title": "💰 Financial Trading",
            "agent": "TradingBot",
            "benefit": "Prove trading decisions without revealing strategy",
            "trust_requirement": "Investor confidence + audit trails"
        },
        {
            "title": "🔍 Event Discovery",
            "agent": "EventExtractor",
            "benefit": "Explain why certain events were prioritized",
            "trust_requirement": "User trust + data quality"
        }
    ]
    
    for i, use_case in enumerate(use_cases, 1):
        print(f"\n{Colors.YELLOW}{i}. {use_case['title']}{Colors.RESET}")
        print(f"   Agent: {use_case['agent']}")
        print(f"   Benefit: {use_case['benefit']}")
        print(f"   Trust Need: {use_case['trust_requirement']}")
        
        if i < len(use_cases):
            wait_for_user()
    
    wait_for_user()


def show_technical_details():
    """Show how it works technically"""
    print(f"\n{Colors.PURPLE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}HOW IT WORKS TECHNICALLY{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*60}{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}1. Agent Execution:{Colors.RESET}")
    print("   ```python")
    print("   result = agent.execute(input_data)")
    print("   ```")
    
    print(f"\n{Colors.CYAN}2. Performance Metrics (TrustWrapper):{Colors.RESET}")
    print("   • Measure execution time")
    print("   • Track success/failure")
    print("   • Generate performance proof")
    
    print(f"\n{Colors.CYAN}3. Explainability (Ziggurat XAI):{Colors.RESET}")
    print("   • Analyze decision path")
    print("   • Extract feature importance (SHAP)")
    print("   • Generate human-readable explanation")
    
    print(f"\n{Colors.CYAN}4. Combined Proof:{Colors.RESET}")
    print("   ```")
    print("   proof = {")
    print("       performance: <ZK proof of metrics>,")
    print("       explanation: <Hash of XAI output>,")
    print("       trust_score: <Combined confidence>")
    print("   }")
    print("   ```")
    
    print(f"\n{Colors.CYAN}5. Blockchain Storage (Aleo):{Colors.RESET}")
    print("   • Immutable record of performance + explanation")
    print("   • Verifiable by anyone")
    print("   • Privacy-preserving (ZK proofs)")
    
    wait_for_user()


def show_trust_building():
    """Show how trust builds over time"""
    print(f"\n{Colors.PURPLE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}TRUST BUILDING OVER TIME{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*60}{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}Simulating 10 executions...{Colors.RESET}\n")
    
    agent = EventDiscoveryAgent()
    xai_wrapper = create_xai_wrapper(agent)
    
    trust_scores = []
    for i in range(10):
        url = random.choice([
            "https://ethcc.io",
            "https://lu.ma/web3-events",
            "https://example.com/events",
            "https://conference.crypto"
        ])
        
        result = xai_wrapper.verified_execute(url)
        trust_score = result.trust_score if result.trust_score is not None else 0.0
        trust_scores.append(trust_score)
        
        # Visual progress bar
        bar_length = int(trust_score * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        print(f"   Run {i+1:2d}: [{bar}] {trust_score:.2%} - {url}")
        time.sleep(0.3)
    
    avg_trust = sum(trust_scores) / len(trust_scores)
    print(f"\n{Colors.GREEN}📊 Average Trust Score: {avg_trust:.2%}{Colors.RESET}")
    print(f"\n💡 Each execution adds to the blockchain record,")
    print(f"   building a verifiable history of reliable, explainable AI!")
    
    wait_for_user()


def show_value_proposition():
    """Show the unique value proposition"""
    print(f"\n{Colors.PURPLE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}UNIQUE VALUE PROPOSITION{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*60}{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}🎯 Basic TrustWrapper:{Colors.RESET}")
    print("   ✅ Proves performance")
    print("   ❌ No explanation")
    print("   → \"Trust me, it works\"")
    
    print(f"\n{Colors.GREEN}🧠 TrustWrapper + Ziggurat XAI:{Colors.RESET}")
    print("   ✅ Proves performance")
    print("   ✅ Explains decisions")
    print("   ✅ Builds confidence")
    print("   → \"Trust me, it works, and here's why\"")
    
    print(f"\n{Colors.CYAN}🏆 Market Differentiator:{Colors.RESET}")
    print("   • First ZK + XAI solution")
    print("   • Perfect for regulated industries")
    print("   • Addresses the \"black box\" problem")
    print("   • Leverages existing Ziggurat technology")
    
    wait_for_user()


def main():
    """Run the enhanced demo"""
    try:
        # Introduction
        show_intro()
        
        # Comparison demo
        show_comparison_demo()
        
        # Use cases
        show_use_cases()
        
        # Technical details
        show_technical_details()
        
        # Trust building
        show_trust_building()
        
        # Value proposition
        show_value_proposition()
        
        # Conclusion
        print(f"\n{Colors.PURPLE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}CONCLUSION{Colors.RESET}")
        print(f"{Colors.PURPLE}{'='*60}{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}✨ We've successfully integrated:{Colors.RESET}")
        print(f"   {Colors.SHIELD} TrustWrapper (performance verification)")
        print(f"   {Colors.BRAIN} Ziggurat XAI (explainable AI)")
        print(f"   {Colors.ROCKET} Aleo blockchain (immutable proofs)")
        
        print(f"\n{Colors.YELLOW}🎯 Creating the first solution that proves:{Colors.RESET}")
        print("   1. THAT an AI agent works (performance)")
        print("   2. WHY it made its decisions (explainability)")
        print("   3. HOW MUCH we can trust it (trust score)")
        
        print(f"\n{Colors.CYAN}🚀 Ready for hackathon judging!{Colors.RESET}")
        print(f"\n{Colors.DIM}Thank you for watching the demo!{Colors.RESET}\n")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Demo interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")


if __name__ == "__main__":
    main()
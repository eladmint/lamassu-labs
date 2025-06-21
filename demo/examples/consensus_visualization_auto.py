#!/usr/bin/env python3
"""
Auto-running consensus visualization 
Shows how quality consensus works without user input
"""
import sys
import os
import time
import json

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.dirname(current_dir)
lamassu_root = os.path.dirname(examples_dir)
sys.path.insert(0, lamassu_root)

from src.core.trust_wrapper_quality import (
    EventStructureValidator, DataQualityValidator, 
    FormatComplianceValidator
)


class Colors:
    """Terminal colors"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


class DemoAgent:
    """Agent for demonstration"""
    
    def __init__(self, scenario="good"):
        self.scenario = scenario
    
    def execute(self, input_data):
        if self.scenario == "good":
            return {
                "status": "success",
                "events_found": 25,
                "extraction_method": "specialized_conference_parser",
                "confidence": 0.92,
                "url": str(input_data)
            }
        elif self.scenario == "medium":
            return {
                "status": "success", 
                "events_found": 8,
                "url": str(input_data)
            }
        else:  # poor
            return {
                "events_found": "error",  # Wrong type
                "url": "different_url.com"
            }


def show_consensus_process():
    """Show step-by-step consensus process"""
    print(f"{Colors.BOLD}🔍 HOW QUALITY CONSENSUS WORKS{Colors.RESET}")
    print("=" * 60)
    
    scenarios = [
        ("✅ High Quality", DemoAgent("good"), "https://ethcc.io"),
        ("⚠️  Medium Quality", DemoAgent("medium"), "https://conference.com"), 
        ("❌ Poor Quality", DemoAgent("poor"), "https://example.com")
    ]
    
    for scenario_name, agent, url in scenarios:
        print(f"\n{Colors.CYAN}{'━' * 50}{Colors.RESET}")
        print(f"{Colors.BOLD}{scenario_name} Scenario{Colors.RESET}")
        print(f"{Colors.CYAN}{'━' * 50}{Colors.RESET}")
        
        # 1. Agent execution
        print(f"\n{Colors.YELLOW}1. Agent Execution{Colors.RESET}")
        print(f"Processing: {url}")
        output = agent.execute(url)
        
        # Show output in compact form
        print(f"Output: {json.dumps(output, separators=(',', ':'))}")
        time.sleep(1)
        
        # 2. Validator assessment
        print(f"\n{Colors.YELLOW}2. Validator Assessment{Colors.RESET}")
        validators = [
            ("Structure", EventStructureValidator()),
            ("Quality", DataQualityValidator()),
            ("Format", FormatComplianceValidator())
        ]
        
        results = []
        for name, validator in validators:
            result = validator.validate(url, output)
            results.append(result)
            
            status = "✅" if result.is_valid else "❌"
            print(f"  {status} {name}: {result.confidence:.0%} - {result.feedback[:40]}...")
            time.sleep(0.3)
        
        # 3. Consensus calculation
        print(f"\n{Colors.YELLOW}3. Consensus Result{Colors.RESET}")
        passed = sum(1 for r in results if r.is_valid)
        total = len(results)
        consensus = passed / total
        avg_conf = sum(r.confidence for r in results) / len(results)
        
        print(f"  Validators Passed: {passed}/{total}")
        print(f"  Consensus Score: {consensus:.0%}")
        print(f"  Average Confidence: {avg_conf:.0%}")
        
        # Visual quality bar
        quality = min((consensus * 0.6 + avg_conf * 0.4) * 1.2, 1.0)
        bar_len = int(quality * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        color = Colors.GREEN if quality > 0.8 else Colors.YELLOW if quality > 0.6 else Colors.RED
        print(f"  Quality Score: [{color}{bar}{Colors.RESET}] {quality:.0%}")
        
        time.sleep(2)
    
    print(f"\n{Colors.PURPLE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}Key Benefits:{Colors.RESET}")
    print("• Multiple validators ensure robust quality assessment")
    print("• Each validator specializes in specific aspects")
    print("• Consensus prevents single points of failure")
    print("• Transparent and explainable quality metrics")
    print("• Scales to validate thousands of outputs")


def main():
    """Auto-running main loop"""
    while True:
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
            show_consensus_process()
            
            print(f"\n{Colors.DIM}Restarting in 15 seconds...{Colors.RESET}")
            time.sleep(15)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}Demo stopped{Colors.RESET}")
            break


if __name__ == "__main__":
    main()
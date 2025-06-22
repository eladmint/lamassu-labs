#!/usr/bin/env python3
"""
Visual demonstration of how quality consensus works
Shows the actual validation process step by step
"""
import sys
import os
import time
import json
from typing import Dict, Any

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.dirname(current_dir)
lamassu_root = os.path.dirname(examples_dir)
sys.path.insert(0, lamassu_root)

from src.core.trust_wrapper_quality import (
    EventStructureValidator, DataQualityValidator, 
    FormatComplianceValidator, create_quality_wrapper
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


class VisualizationAgent:
    """Agent that produces different quality outputs for demonstration"""
    
    def __init__(self, scenario="good"):
        self.scenario = scenario
    
    def execute(self, input_data):
        """Generate output based on scenario"""
        if self.scenario == "good":
            return {
                "status": "success",
                "events_found": 25,
                "extraction_method": "specialized_conference_parser",
                "confidence": 0.92,
                "url": str(input_data),
                "processing_time": 750
            }
        elif self.scenario == "medium":
            # Missing some fields, lower confidence
            return {
                "status": "success",
                "events_found": 10,
                "url": str(input_data),
                "confidence": 0.65
            }
        else:  # poor
            # Wrong data types, missing fields
            return {
                "events_found": "unknown",  # Wrong type!
                "error": "partial extraction",
                "url": "wrong_url.com"  # Doesn't match input
            }


def visualize_validation_process(scenario_name, agent, input_url):
    """Show the validation process step by step"""
    print(f"\n{Colors.PURPLE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}Scenario: {scenario_name}{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}")
    
    # Step 1: Agent execution
    print(f"\n{Colors.CYAN}Step 1: AI Agent Execution{Colors.RESET}")
    print(f"Input: {input_url}")
    print("Processing...")
    
    output = agent.execute(input_url)
    time.sleep(0.5)
    
    print(f"\n{Colors.GREEN}Output produced:{Colors.RESET}")
    print(json.dumps(output, indent=2))
    
    time.sleep(1)
    
    # Step 2: Show validators
    print(f"\n{Colors.CYAN}Step 2: Initialize Validators{Colors.RESET}")
    validators = [
        EventStructureValidator(),
        DataQualityValidator(),
        FormatComplianceValidator()
    ]
    
    for validator in validators:
        print(f"• {validator.name} - Ready")
    
    time.sleep(1)
    
    # Step 3: Run validation
    print(f"\n{Colors.CYAN}Step 3: Independent Validation{Colors.RESET}")
    print("Each validator examines the output independently...\n")
    
    validation_results = []
    for validator in validators:
        print(f"{Colors.YELLOW}Running {validator.name}...{Colors.RESET}")
        result = validator.validate(input_url, output)
        validation_results.append(result)
        
        # Show what this validator checked
        if isinstance(validator, EventStructureValidator):
            print("  Checking: Required fields, data structure, reasonable values")
        elif isinstance(validator, DataQualityValidator):
            print("  Checking: Confidence scores, extraction method, data consistency")
        elif isinstance(validator, FormatComplianceValidator):
            print("  Checking: JSON compatibility, data types, format standards")
        
        time.sleep(0.5)
        
        # Show result
        status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if result.is_valid else f"{Colors.RED}❌ FAIL{Colors.RESET}"
        print(f"  Result: {status}")
        print(f"  Confidence: {result.confidence:.2%}")
        print(f"  Feedback: {result.feedback}")
        print()
        
        time.sleep(0.5)
    
    # Step 4: Consensus calculation
    print(f"{Colors.CYAN}Step 4: Consensus Calculation{Colors.RESET}")
    
    validators_passed = sum(1 for r in validation_results if r.is_valid)
    total_validators = len(validation_results)
    consensus_score = validators_passed / total_validators
    
    print(f"\nVoting Results:")
    print(f"  • Validators that passed: {validators_passed}")
    print(f"  • Total validators: {total_validators}")
    print(f"  • Consensus score: {consensus_score:.2%}")
    
    # Average confidence
    confidences = [r.confidence for r in validation_results]
    avg_confidence = sum(confidences) / len(confidences)
    print(f"  • Average confidence: {avg_confidence:.2%}")
    
    time.sleep(1)
    
    # Step 5: Quality score
    print(f"\n{Colors.CYAN}Step 5: Calculate Quality Score{Colors.RESET}")
    
    # Simplified quality calculation for visualization
    quality_score = (consensus_score * 0.4 + avg_confidence * 0.3)
    if consensus_score == 1.0:  # Unanimous
        quality_score += 0.1
    quality_score = min(quality_score * 1.3, 1.0)  # Scale and cap
    
    print(f"\nQuality Score Calculation:")
    print(f"  • Consensus weight (40%): {consensus_score * 0.4:.3f}")
    print(f"  • Confidence weight (30%): {avg_confidence * 0.3:.3f}")
    if consensus_score == 1.0:
        print(f"  • Unanimity bonus: 0.100")
    print(f"  • {Colors.BOLD}Final Quality Score: {quality_score:.2%}{Colors.RESET}")
    
    # Visual quality bar
    bar_length = int(quality_score * 30)
    quality_bar = "█" * bar_length + "░" * (30 - bar_length)
    
    color = Colors.GREEN if quality_score > 0.8 else Colors.YELLOW if quality_score > 0.6 else Colors.RED
    print(f"\n  Quality: [{color}{quality_bar}{Colors.RESET}] {quality_score:.2%}")
    
    return quality_score


def main():
    """Run the visualization demo"""
    print(f"{Colors.BOLD}\n🔍 QUALITY CONSENSUS VISUALIZATION{Colors.RESET}")
    print("See exactly how multiple validators assess AI output quality\n")
    
    scenarios = [
        ("High Quality Output", VisualizationAgent("good"), "https://ethcc.io"),
        ("Medium Quality Output", VisualizationAgent("medium"), "https://conference.com"),
        ("Poor Quality Output", VisualizationAgent("poor"), "https://example.com")
    ]
    
    for scenario_name, agent, url in scenarios:
        visualize_validation_process(scenario_name, agent, url)
        
        if scenario_name != scenarios[-1][0]:  # Not the last one
            input(f"\n{Colors.DIM}Press Enter to see next scenario...{Colors.RESET}")
    
    # Summary
    print(f"\n{Colors.PURPLE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}KEY INSIGHTS{Colors.RESET}")
    print(f"{Colors.PURPLE}{'='*70}{Colors.RESET}")
    
    print("\n1. Quality is determined by MULTIPLE independent validators")
    print("2. Each validator checks SPECIFIC aspects")
    print("3. Consensus provides ROBUST quality assessment")
    print("4. Poor outputs are AUTOMATICALLY identified")
    print("5. The process is TRANSPARENT and EXPLAINABLE")
    
    print(f"\n{Colors.GREEN}✨ This is how we ensure AI output quality at scale!{Colors.RESET}\n")


if __name__ == "__main__":
    main()
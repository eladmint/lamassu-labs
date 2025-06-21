#!/usr/bin/env python3
"""
Quality Consensus Demo - Auto-running version
Shows progression: Basic → XAI → Quality Consensus
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

from src.core.trust_wrapper_quality import create_quality_wrapper


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
    """Simple agent for demonstration"""
    def __init__(self, name="DemoAgent"):
        self.name = name
    
    def execute(self, task: str) -> Dict[str, Any]:
        """Simulate task execution"""
        time.sleep(0.5)
        
        # Simulate different quality outputs
        if "good" in task.lower():
            return {
                "status": "success",
                "result": f"Processed {task}",
                "confidence": 0.95,
                "events_found": 25,
                "extraction_method": "specialized_parser"
            }
        elif "bad" in task.lower():
            return {
                "result": "incomplete",
                "events_found": "error"  # Wrong type
            }
        else:
            return {
                "status": "success",
                "result": f"Processed {task}",
                "events_found": 10,
                "extraction_method": "general"
            }


def print_progress_bar(label: str, value: float, max_width: int = 30):
    """Print a visual progress bar"""
    filled = int(value * max_width)
    bar = "█" * filled + "░" * (max_width - filled)
    percentage = int(value * 100)
    print(f"{label}: [{bar}] {percentage}%")


def main():
    """Auto-running demo"""
    while True:
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print(f"{Colors.BOLD}{Colors.PURPLE}╔══════════════════════════════════════════════════════════╗{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.PURPLE}║        TRUSTWRAPPER - QUALITY CONSENSUS DEMO             ║{Colors.RESET}")
            print(f"{Colors.BOLD}{Colors.PURPLE}╚══════════════════════════════════════════════════════════╝{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}The Evolution of AI Trust:{Colors.RESET}")
            print(f"1. Basic → 2. Explainable → 3. {Colors.GREEN}Quality Verified{Colors.RESET}\n")
            
            # Demo different quality scenarios
            scenarios = [
                ("High Quality Task", "Process good data from conference"),
                ("Medium Quality Task", "Extract events from website"),
                ("Low Quality Task", "Process bad data with errors")
            ]
            
            for scenario_name, task in scenarios:
                print(f"\n{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
                print(f"{Colors.BOLD}Scenario: {scenario_name}{Colors.RESET}")
                print(f"{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
                
                # Create agent and wrapper
                agent = DemoAgent()
                wrapper = create_quality_wrapper(agent)
                
                print(f"\nExecuting: {task}")
                result = wrapper.verified_execute(task)
                
                # Show results progressively
                time.sleep(0.5)
                print(f"\n{Colors.GREEN}✓ Performance Verified{Colors.RESET}")
                print(f"  Speed: {result.metrics.execution_time_ms}ms")
                
                time.sleep(0.5)
                if result.explanation:
                    print(f"\n{Colors.BLUE}✓ Explainability Added{Colors.RESET}")
                    print(f"  Confidence: {result.explanation.confidence_score:.2%}")
                
                time.sleep(0.5)
                if result.consensus:
                    print(f"\n{Colors.YELLOW}✓ Quality Consensus{Colors.RESET}")
                    consensus = result.consensus
                    
                    # Visual consensus display
                    print(f"\n  Validator Results:")
                    for val in consensus.validation_results:
                        icon = "✅" if val.is_valid else "❌"
                        print(f"  {icon} {val.validator_name}: {val.feedback}")
                    
                    print(f"\n  Consensus Metrics:")
                    print_progress_bar("  Consensus Score", consensus.consensus_score)
                    print_progress_bar("  Avg Confidence ", consensus.average_confidence)
                    
                    if result.quality_score:
                        print(f"\n  {Colors.BOLD}🏆 Overall Quality: {result.quality_score:.2%}{Colors.RESET}")
                
                time.sleep(3)
            
            # Summary
            print(f"\n{Colors.PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
            print(f"{Colors.BOLD}Key Innovation:{Colors.RESET}")
            print(f"• First to combine ZK + XAI + Quality Consensus")
            print(f"• Multiple validators ensure output quality")
            print(f"• Perfect for AI marketplaces and critical applications")
            
            print(f"\n{Colors.DIM}Restarting in 10 seconds...{Colors.RESET}")
            time.sleep(10)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}Demo stopped{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
            time.sleep(5)


if __name__ == "__main__":
    main()
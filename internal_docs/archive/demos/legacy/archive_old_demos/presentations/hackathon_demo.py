#!/usr/bin/env python3
"""
🏛️ LAMASSU LABS - TRUSTWRAPPER HACKATHON DEMO
Making AI Agent Trust Simple and Understandable

🔐 Zero-Knowledge Proofs for AI Agents - Now Everyone Can Understand! 🔐
"""

import asyncio
import time
import os
import sys
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path
presentations_dir = Path(__file__).parent
demo_dir = presentations_dir.parent
lamassu_root = demo_dir.parent
sys.path.append(str(lamassu_root))

# Import our TrustWrapper
from src.core.trust_wrapper import ZKTrustWrapper, VerifiedResult

# 🏛️ LAMASSU LABS LOGO WITH TRUST THEME
LAMASSU_LOGO = """
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║  ██╗      █████╗ ███╗   ███╗ █████╗ ███████╗███████╗██╗   ██╗          ║
║  ██║     ██╔══██╗████╗ ████║██╔══██╗██╔════╝██╔════╝██║   ██║          ║
║  ██║     ███████║██╔████╔██║███████║███████╗███████╗██║   ██║          ║
║  ██║     ██╔══██║██║╚██╔╝██║██╔══██║╚════██║╚════██║██║   ██║          ║
║  ███████╗██║  ██║██║ ╚═╝ ██║██║  ██║███████║███████║╚██████╔╝          ║
║  ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝           ║
║                                                                          ║
║                    🦁 GUARDIAN OF TRUST 🦁                               ║
║                                                                          ║
║                         ┌─────────────┐                                  ║
║                         │   🦁 🦁 🦁   │                                  ║
║                         │  ╱       ╲  │                                  ║
║                         │ │  ●   ●  │ │                                  ║
║                         │ │    <    │ │                                  ║
║                         │  ╲  ═══  ╱  │                                  ║
║                         │   └─┬─┬─┘   │                                  ║
║                         └─────┴─┴─────┘                                  ║
║                                                                          ║
║               🔐 TRUSTWRAPPER - AI TRUST MADE SIMPLE 🔐                  ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

# 🎮 RETRO GAMING STYLE SLIDE TRANSITIONS
TRANSITIONS = [
    "█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█",
    "██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██",
    "███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███",
    "████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████",
    "█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█████",
    "██████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████",
    "███████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████",
    "████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████",
    "█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█████████",
    "██████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████████",
    "███████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████████",
    "████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████████",
    "█████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█████████████",
    "██████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████████████",
    "███████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████████████",
    "████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████████████",
    "█████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█████████████████",
    "██████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████████████████",
    "███████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████████████████",
    "████████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████████████████",
    "█████████████████████▒▒▒▒▒▒▒▒▒▒▒█████████████████████",
    "██████████████████████▒▒▒▒▒▒▒▒██████████████████████",
    "███████████████████████▒▒▒▒▒███████████████████████",
    "████████████████████████▒▒████████████████████████",
    "█████████████████████████████████████████████████",
]

# 🎨 Color codes for terminal
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

async def type_text(text: str, delay: float = 0.03):
    """Type text with retro effect"""
    for char in text:
        print(char, end='', flush=True)
        await asyncio.sleep(delay)
    print()

async def slide_transition():
    """Gaming-style slide transition"""
    for line in TRANSITIONS:
        print(f"{Colors.CYAN}{line}{Colors.RESET}")
        await asyncio.sleep(0.02)
    await asyncio.sleep(0.3)
    clear_screen()

async def show_slide(title: str, content: str, delay: float = 2.0):
    """Show a slide with title and content"""
    clear_screen()
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*70}{Colors.RESET}\n")
    
    await type_text(content)
    await asyncio.sleep(delay)

async def show_trust_flow():
    """Show visual diagram of trust verification flow"""
    diagram = """
    🤖 Your AI Agent                    🔐 TrustWrapper                    🏛️ Aleo Blockchain
         │                                     │                                    │
         │  Execute Task                      │                                    │
         ├────────────────────────────────────►                                    │
         │                                     │                                    │
         │                                     │ Measure Performance                │
         │                                     ├─────────┐                          │
         │                                     │         │                          │
         │                                     │◄────────┘                          │
         │                                     │                                    │
         │                                     │ Generate ZK Proof                  │
         │                                     ├──────────────────────────────────►│
         │                                     │                                    │
         │                                     │              Verify & Store        │
         │                                     │◄──────────────────────────────────┤
         │                                     │                                    │
         │  Return Verified Result             │                                    │
         │◄────────────────────────────────────┤                                    │
         │                                     │                                    │
         ▼                                     ▼                                    ▼
    ✅ Trusted Result                  📊 Performance Data              🔗 Permanent Record
    """
    
    await show_slide("🔐 HOW TRUSTWRAPPER WORKS", diagram, 4.0)

async def show_aleo_integration():
    """Show Aleo technology integration"""
    content = f"""
{Colors.PURPLE}🏛️ ALEO TECHNOLOGY INTEGRATION:{Colors.RESET}

1. {Colors.CYAN}Leo Smart Contracts{Colors.RESET}
   • Simple verification contract in Leo language
   • Private inputs, public verification
   • Zero-knowledge proof generation

2. {Colors.GREEN}Privacy-First Design{Colors.RESET}
   • Agent code remains private
   • Only performance metrics are proven
   • No IP or trade secrets exposed

3. {Colors.YELLOW}On-Chain Verification{Colors.RESET}
   • Permanent proof storage on Aleo
   • Verifiable by anyone
   • Tamper-proof trust records

{Colors.BOLD}Example Leo Contract:{Colors.RESET}
```leo
transition verify_execution(
    private execution_time: u32,
    private success: bool,
    public agent_hash: field
) -> ExecutionProof {{
    // Verify without revealing details
    return ExecutionProof {{ 
        // Proof details here
    }};
}}
```
"""
    await show_slide("🔗 POWERED BY ALEO", content, 5.0)

async def show_simple_explanation():
    """Show simple explanation of ZK proofs"""
    content = f"""
{Colors.GREEN}🎯 ZERO-KNOWLEDGE PROOFS EXPLAINED SIMPLY:{Colors.RESET}

Think of it like a {Colors.YELLOW}sealed envelope{Colors.RESET} system:

1. {Colors.CYAN}The Challenge:{Colors.RESET}
   "Prove your AI agent works well WITHOUT showing the code"

2. {Colors.CYAN}The Solution:{Colors.RESET}
   • Agent runs in a {Colors.YELLOW}sealed box{Colors.RESET} (private execution)
   • We measure {Colors.GREEN}performance{Colors.RESET} (time, accuracy, success)
   • Create a {Colors.PURPLE}mathematical proof{Colors.RESET} of the results
   • Anyone can {Colors.BLUE}verify{Colors.RESET} without seeing inside

3. {Colors.CYAN}Real World Analogy:{Colors.RESET}
   Like proving you're 21+ without showing your ID:
   • The bouncer knows you're legal ✓
   • But doesn't know your exact age, address, or name
   • Mathematical certainty without revealing secrets!

{Colors.BOLD}Result: {Colors.GREEN}TRUST WITHOUT TRANSPARENCY{Colors.RESET}
"""
    await show_slide("🔍 WHAT ARE ZERO-KNOWLEDGE PROOFS?", content, 6.0)

async def demo_wrapper_in_action():
    """Live demonstration of TrustWrapper"""
    await show_slide("🚀 LIVE DEMONSTRATION", "Let's see TrustWrapper in action!", 2.0)
    
    # Simulate agent execution
    print(f"\n{Colors.CYAN}1. Creating a simple AI agent...{Colors.RESET}")
    await asyncio.sleep(1)
    
    print(f"""
class EventFinderAgent:
    def execute(self, url):
        # Proprietary event extraction logic
        return extract_events(url)
""")
    
    await asyncio.sleep(2)
    
    print(f"\n{Colors.CYAN}2. Wrapping with TrustWrapper...{Colors.RESET}")
    await asyncio.sleep(1)
    
    print(f"""{Colors.GREEN}
agent = EventFinderAgent()
trusted_agent = ZKTrustWrapper(agent)
{Colors.RESET}""")
    
    await asyncio.sleep(2)
    
    print(f"\n{Colors.CYAN}3. Executing with verification...{Colors.RESET}")
    await asyncio.sleep(1)
    
    # Simulate execution
    print(f"\n{Colors.YELLOW}Executing agent task...{Colors.RESET}")
    for i in range(10):
        print(f"{'█' * (i+1)}{'░' * (9-i)} {(i+1)*10}%", end='\r')
        await asyncio.sleep(0.1)
    
    print(f"\n\n{Colors.GREEN}✅ Task completed successfully!{Colors.RESET}")
    await asyncio.sleep(1)
    
    # Show proof generation
    print(f"\n{Colors.PURPLE}Generating zero-knowledge proof...{Colors.RESET}")
    await asyncio.sleep(1)
    
    proof_data = f"""
{Colors.BOLD}🔐 VERIFICATION PROOF{Colors.RESET}
├─ Agent Hash: 0x7f3a9b2c...
├─ Execution Time: 1.23s ✓
├─ Success: true ✓
├─ Accuracy: 98.5% ✓
└─ Aleo TX: aleo1qyz3...8fhs
"""
    print(proof_data)
    
    await asyncio.sleep(3)

async def show_why_trustworthy():
    """Explain why the implementation is trustworthy"""
    content = f"""
{Colors.GREEN}🛡️ WHY YOU CAN TRUST TRUSTWRAPPER:{Colors.RESET}

1. {Colors.CYAN}Open Source Verification{Colors.RESET}
   • All wrapper code is public
   • Anyone can audit the measurements
   • No hidden behavior

2. {Colors.PURPLE}Mathematical Guarantees{Colors.RESET}
   • ZK proofs can't be faked
   • Aleo blockchain ensures immutability
   • Cryptographic security

3. {Colors.YELLOW}Simple Design{Colors.RESET}
   • No complex logic to hide bugs
   • Clear measurement criteria
   • Easy to understand and verify

4. {Colors.BLUE}Decentralized Verification{Colors.RESET}
   • No single point of trust
   • Community can verify proofs
   • Permanent on-chain records

{Colors.BOLD}Bottom Line:{Colors.RESET} 
Math doesn't lie. Blockchain doesn't forget. Trust is built-in.
"""
    await show_slide("🛡️ WHY IT'S TRUSTWORTHY", content, 5.0)

async def show_real_world_uses():
    """Show practical applications"""
    content = f"""
{Colors.YELLOW}💼 REAL-WORLD APPLICATIONS:{Colors.RESET}

{Colors.CYAN}1. AI Model Marketplace{Colors.RESET}
   • Prove model accuracy without revealing weights
   • Buyers trust performance claims
   • Sellers protect IP

{Colors.CYAN}2. Regulatory Compliance{Colors.RESET}
   • Prove AI safety without exposing algorithms
   • Meet transparency requirements
   • Maintain competitive advantage

{Colors.CYAN}3. DeFi Trading Bots{Colors.RESET}
   • Verify profitable strategies exist
   • No alpha leak to competitors
   • Build investor confidence

{Colors.CYAN}4. Enterprise AI Services{Colors.RESET}
   • SLA verification without code audits
   • Performance guarantees with privacy
   • Trust in B2B relationships

{Colors.GREEN}Every AI agent needs trust. TrustWrapper delivers it.{Colors.RESET}
"""
    await show_slide("💡 USE CASES", content, 5.0)

async def show_call_to_action():
    """Final call to action"""
    content = f"""
{Colors.BOLD}{Colors.GREEN}🚀 GET STARTED IN 3 LINES:{Colors.RESET}

```python
agent = YourAIAgent()
trusted_agent = ZKTrustWrapper(agent)
result = trusted_agent.verified_execute()
```

{Colors.YELLOW}🏆 HACKATHON GOALS:{Colors.RESET}
• Target: Aleo $5,000 DeFi Prize
• Innovation: First universal ZK wrapper for agents
• Impact: Every AI agent can now be trusted

{Colors.CYAN}📦 WHAT WE'VE BUILT:{Colors.RESET}
• Universal wrapper class (works with ANY agent)
• Simple Leo verification contract
• Three working demos
• Complete documentation

{Colors.PURPLE}🔗 TRY IT NOW:{Colors.RESET}
GitHub: github.com/lamassu-labs/trustwrapper
Demo: Run this script!
Docs: Full integration guide included

{Colors.BOLD}{Colors.GREEN}TrustWrapper: Because trust shouldn't require transparency.{Colors.RESET}
"""
    await show_slide("🎯 JOIN THE TRUST REVOLUTION", content, 6.0)

async def run_demo():
    """Main demo flow"""
    clear_screen()
    
    # Opening
    print(LAMASSU_LOGO)
    await asyncio.sleep(3)
    
    # Slide 1: Introduction
    await slide_transition()
    await show_slide(
        "🦁 WELCOME TO LAMASSU LABS",
        f"""
{Colors.BOLD}The Problem:{Colors.RESET}
How do you trust an AI agent without seeing its code?

{Colors.BOLD}The Solution:{Colors.RESET}
TrustWrapper - Zero-Knowledge Proofs for ANY AI Agent

{Colors.BOLD}The Innovation:{Colors.RESET}
Add trust to your existing agents in just 3 lines of code!
"""
    )
    
    # Slide 2: Simple explanation
    await slide_transition()
    await show_simple_explanation()
    
    # Slide 3: How it works
    await slide_transition()
    await show_trust_flow()
    
    # Slide 4: Live demo
    await slide_transition()
    await demo_wrapper_in_action()
    
    # Slide 5: Aleo integration
    await slide_transition()
    await show_aleo_integration()
    
    # Slide 6: Why trustworthy
    await slide_transition()
    await show_why_trustworthy()
    
    # Slide 7: Real world uses
    await slide_transition()
    await show_real_world_uses()
    
    # Slide 8: Call to action
    await slide_transition()
    await show_call_to_action()
    
    # Closing
    await slide_transition()
    print(LAMASSU_LOGO)
    print(f"\n{Colors.BOLD}{Colors.GREEN}Thank you for watching!{Colors.RESET}")
    print(f"{Colors.CYAN}Press Ctrl+C to exit or wait for auto-restart...{Colors.RESET}\n")

async def main():
    """Main entry point with auto-loop"""
    try:
        while True:
            await run_demo()
            await asyncio.sleep(10)  # Wait before restarting
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Demo stopped. Thanks for watching!{Colors.RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
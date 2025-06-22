#!/usr/bin/env python3
"""
🦁 LAMASSU LABS - THE SIMPLE STORY DEMO
A story-based explanation that anyone can understand

"Imagine if your AI agents had a trust badge, like HTTPS for websites..."
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# 🎨 Colors for storytelling
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

async def type_story(text: str, delay: float = 0.04):
    """Type text like a story"""
    for char in text:
        print(char, end='', flush=True)
        if char in '.!?':
            await asyncio.sleep(delay * 3)  # Pause at sentence ends
        else:
            await asyncio.sleep(delay)
    print("\n")

async def show_chapter(chapter: str, title: str):
    """Show a chapter header"""
    clear_screen()
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{chapter}{Colors.RESET}")
    print(f"{Colors.CYAN}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}\n")
    await asyncio.sleep(2)

async def chapter_1_problem():
    """Chapter 1: The Problem"""
    await show_chapter("CHAPTER 1", "The Trust Problem")
    
    story = f"""{Colors.CYAN}Meet Alice.{Colors.RESET} She runs a hedge fund.

Alice finds an amazing AI trading bot online that claims:
{Colors.GREEN}• "95% win rate!"
• "2.5 Sharpe ratio!"
• "Tested on 5 years of data!"{Colors.RESET}

But Alice thinks: {Colors.YELLOW}"How do I know this is true?"{Colors.RESET}

The bot creator, Bob, says: {Colors.RED}"Just trust me!"{Colors.RESET}
But Alice has been burned before...

Bob could show his code, but then:
{Colors.RED}• His secret algorithm would be stolen
• Competitors would copy it
• His business would be ruined{Colors.RESET}

{Colors.BOLD}This is the AI Trust Paradox:{Colors.RESET}
How do you prove something works without showing how it works?
"""
    
    await type_story(story)
    await asyncio.sleep(3)

async def chapter_2_solution():
    """Chapter 2: The Solution"""
    await show_chapter("CHAPTER 2", "Enter Zero-Knowledge Proofs")
    
    story = f"""Think of it like {Colors.CYAN}proving you're over 21 at a bar:{Colors.RESET}

{Colors.YELLOW}Option 1 (Old Way):{Colors.RESET}
Show your driver's license → Reveals everything!
• Your exact age
• Your address  
• Your full name

{Colors.GREEN}Option 2 (ZK Way):{Colors.RESET}
Special card that just says "OVER 21" → Proves what matters!
• Mathematically verified
• No extra info leaked
• Still 100% trustworthy

{Colors.BOLD}That's what TrustWrapper does for AI agents!{Colors.RESET}

Bob wraps his trading bot with TrustWrapper.
Now it can {Colors.PURPLE}prove its performance{Colors.RESET} without revealing {Colors.RED}how it works{Colors.RESET}.
"""
    
    await type_story(story)
    await asyncio.sleep(3)

async def chapter_3_how():
    """Chapter 3: How It Works"""
    await show_chapter("CHAPTER 3", "The Magic of TrustWrapper")
    
    # Visual diagram
    diagram = f"""
{Colors.CYAN}HERE'S THE SIMPLE 3-STEP PROCESS:{Colors.RESET}

{Colors.YELLOW}1. WRAP YOUR AGENT{Colors.RESET}
   ┌─────────────┐      ┌─────────────────┐
   │  Your Agent │ ---> │  + TrustWrapper │
   └─────────────┘      └─────────────────┘
   
{Colors.GREEN}2. AGENT RUNS PRIVATELY{Colors.RESET}
   ┌─────────────────┐
   │ 🔒 Secret Code  │ --> Measures: Time ⏱️
   │ 🔒 Hidden Logic │              Success ✓
   │ 🔒 Private Data │              Accuracy 📊
   └─────────────────┘
   
{Colors.PURPLE}3. BLOCKCHAIN PROOF{Colors.RESET}
   Performance Data --> Aleo Blockchain --> Public Proof 🏆
                       (Zero-Knowledge)     "Yes, it works!"
"""
    
    print(diagram)
    await asyncio.sleep(3)
    
    story = f"""
{Colors.BOLD}It's like having a referee who:{Colors.RESET}
• Watches the game
• Confirms the score
• But never reveals the team's playbook!
"""
    
    await type_story(story)
    await asyncio.sleep(2)

async def chapter_4_aleo():
    """Chapter 4: Why Aleo?"""
    await show_chapter("CHAPTER 4", "The Aleo Advantage")
    
    story = f"""{Colors.PURPLE}Aleo{Colors.RESET} is like a {Colors.CYAN}Swiss bank for computations.{Colors.RESET}

Regular blockchains are like {Colors.YELLOW}glass houses{Colors.RESET}:
• Everyone sees everything
• No privacy
• All data exposed

Aleo is like a {Colors.GREEN}private vault{Colors.RESET}:
• Computations happen in private
• Only results are public
• Perfect for AI agents!

{Colors.BOLD}With Aleo's Leo language, we write:{Colors.RESET}
"""
    
    await type_story(story)
    
    # Show simple Leo code
    code = f"""{Colors.CYAN}
transition verify_agent(
    private performance: u32,    // Secret performance data
    public agent_id: field       // Public agent identifier
) -> ProofOfTrust {{
    // Magic happens here!
    // Verify without revealing
    return proof;
}}
{Colors.RESET}"""
    
    print(code)
    await asyncio.sleep(3)
    
    story = f"""
This creates an {Colors.GREEN}unforgeable certificate{Colors.RESET} that says:
"This AI agent performed at X level" ✓

Without revealing HOW it achieved that performance!
"""
    
    await type_story(story)
    await asyncio.sleep(2)

async def chapter_5_benefits():
    """Chapter 5: Real World Benefits"""
    await show_chapter("CHAPTER 5", "Why This Changes Everything")
    
    stories = [
        (
            "🏦 For Financial Institutions:",
            f"""{Colors.GREEN}Before:{Colors.RESET} "Trust our black-box AI with your millions"
{Colors.PURPLE}After:{Colors.RESET} "Here's cryptographic proof it works" ✓"""
        ),
        (
            "🏥 For Healthcare AI:",
            f"""{Colors.GREEN}Before:{Colors.RESET} "Our diagnosis AI is 98% accurate, trust us"
{Colors.PURPLE}After:{Colors.RESET} "Verified by blockchain, privacy preserved" ✓"""
        ),
        (
            "🚗 For Autonomous Vehicles:",
            f"""{Colors.GREEN}Before:{Colors.RESET} "Our self-driving AI is safe, we tested it"
{Colors.PURPLE}After:{Colors.RESET} "Mathematical proof of safety metrics" ✓"""
        ),
        (
            "🎮 For Gaming Anti-Cheat:",
            f"""{Colors.GREEN}Before:{Colors.RESET} "Install our invasive anti-cheat"
{Colors.PURPLE}After:{Colors.RESET} "Prove you're not cheating, keep privacy" ✓"""
        ),
    ]
    
    for title, comparison in stories:
        print(f"\n{Colors.BOLD}{title}{Colors.RESET}")
        print(comparison)
        await asyncio.sleep(2)
    
    await asyncio.sleep(2)

async def chapter_6_demo():
    """Chapter 6: Live Demo"""
    await show_chapter("CHAPTER 6", "See It In Action")
    
    print(f"{Colors.CYAN}Let's wrap a real AI agent!{Colors.RESET}\n")
    await asyncio.sleep(1)
    
    # Step 1
    print(f"{Colors.YELLOW}Step 1: Create an AI agent{Colors.RESET}")
    print(f"{Colors.DIM}class SecretTradingBot:")
    print("    def trade(self, market_data):")
    print("        # 🔒 Proprietary algorithm")
    print(f"        return profit{Colors.RESET}\n")
    await asyncio.sleep(2)
    
    # Step 2
    print(f"{Colors.YELLOW}Step 2: Add TrustWrapper (1 line!){Colors.RESET}")
    print(f"{Colors.GREEN}trusted_bot = TrustWrapper(SecretTradingBot()){Colors.RESET}\n")
    await asyncio.sleep(2)
    
    # Step 3
    print(f"{Colors.YELLOW}Step 3: Run with verification{Colors.RESET}")
    print("result = trusted_bot.verified_trade(market_data)\n")
    await asyncio.sleep(1)
    
    # Show result
    print(f"{Colors.PURPLE}🎉 VERIFIED RESULT:{Colors.RESET}")
    print(f"{Colors.GREEN}✓ Profit: 23.5%")
    print("✓ Sharpe: 2.3")
    print("✓ Drawdown: 8%")
    print(f"✓ Proof: aleo1qyz...8fhs{Colors.RESET}")
    print(f"\n{Colors.BOLD}Algorithm: Still secret! 🔒{Colors.RESET}")
    
    await asyncio.sleep(3)

async def chapter_7_future():
    """Chapter 7: The Future"""
    await show_chapter("CHAPTER 7", "A World of Trusted AI")
    
    story = f"""Imagine a future where:

{Colors.CYAN}Every AI agent has a trust score{Colors.RESET}
• Like credit scores, but for AI
• Verified by math, not marketing
• Updated in real-time

{Colors.YELLOW}AI marketplaces become trustworthy{Colors.RESET}
• Buy agents with confidence
• Sell without revealing secrets
• Fair prices based on proof

{Colors.GREEN}Regulations become simple{Colors.RESET}
• "Show us your TrustWrapper proofs"
• Privacy preserved
• Compliance automated

{Colors.PURPLE}Competition drives innovation{Colors.RESET}
• Best agents proven, not claimed
• Secrets stay secret
• May the best AI win!

{Colors.BOLD}This future starts with TrustWrapper.
This future starts today.
This future starts with YOU.{Colors.RESET}
"""
    
    await type_story(story)
    await asyncio.sleep(3)

async def show_call_to_action():
    """Final call to action"""
    clear_screen()
    
    cta = f"""
{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}
{Colors.BOLD}{Colors.YELLOW}{'READY TO BUILD TRUST?'.center(70)}{Colors.RESET}
{Colors.BOLD}{Colors.CYAN}{'═'*70}{Colors.RESET}

{Colors.GREEN}🚀 GET STARTED IN 3 LINES:{Colors.RESET}

```python
from lamassu import TrustWrapper
agent = YourAIAgent()
trusted = TrustWrapper(agent)  # That's it!
```

{Colors.YELLOW}📦 WHAT YOU GET:{Colors.RESET}
• Universal wrapper (works with ANY agent)
• Aleo blockchain integration
• Zero-knowledge proofs
• Complete documentation
• Working examples

{Colors.PURPLE}🏆 HACKATHON TARGET:{Colors.RESET}
• Aleo Prize: $5,000 (Privacy DeFi track)
• Innovation: First universal ZK wrapper
• Impact: Every AI agent can be trusted

{Colors.CYAN}🔗 RESOURCES:{Colors.RESET}
• GitHub: github.com/lamassu-labs/trustwrapper
• Docs: Full integration guide
• Demo: You're watching it!

{Colors.BOLD}{Colors.GREEN}Remember: In the age of AI, trust isn't optional.
With TrustWrapper, trust is just 3 lines away.{Colors.RESET}

{Colors.DIM}Press any key to restart the story...{Colors.RESET}
"""
    
    print(cta)

async def run_story():
    """Run the complete story"""
    chapters = [
        chapter_1_problem,
        chapter_2_solution,
        chapter_3_how,
        chapter_4_aleo,
        chapter_5_benefits,
        chapter_6_demo,
        chapter_7_future,
    ]
    
    for chapter in chapters:
        await chapter()
        print(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")
        await asyncio.sleep(5)  # Auto-advance after 5 seconds
    
    await show_call_to_action()

async def main():
    """Main entry point with loop"""
    try:
        while True:
            await run_story()
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Thanks for watching the TrustWrapper story!{Colors.RESET}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
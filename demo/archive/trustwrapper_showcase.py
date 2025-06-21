#!/usr/bin/env python3
"""
🛡️ TRUSTWRAPPER - Universal ZK Trust Layer for AI Agents
Interactive showcase demonstrating real-world value
"""

import time
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.trust_wrapper import ZKTrustWrapper

# ASCII art for TrustWrapper
TRUSTWRAPPER_LOGO = """
                    🛡️
                ╱─────────╲
              ╱─────────────╲
            ╱─────────────────╲
          ╱───── TRUST ─────────╲
        ╱─────── WRAPPER ─────────╲
      ╱─────────────────────────────╲
    ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
"""

# System architecture
ARCHITECTURE_DIAGRAM = """
┌─────────────────────────────────────────────────────────────────────┐
│                      HOW TRUSTWRAPPER WORKS                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🤖 ANY AI AGENT                                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ OpenAI   │  │LangChain │  │ Scrapy   │  │ Your Bot │          │
│  │   GPT    │  │  Agent   │  │ Spider   │  │  Agent   │          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘          │
│       └──────────────┴──────────────┴──────────────┘               │
│                             │                                       │
│                             ▼                                       │
│  🛡️ TRUSTWRAPPER           ┌─────────────────────┐                 │
│                           │   ZKTrustWrapper    │                 │
│                           │ "3 lines of code"   │                 │
│                           └──────────┬──────────┘                 │
│                                      │                             │
│  🔐 ZK PROOF GENERATION              ▼                             │
│  ┌─────────────────────────────────────────────────────┐          │
│  │              Cryptographic Proof Engine              │          │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │          │
│  │  │ Execution │  │  Success │  │  Metrics │         │          │
│  │  │   Time    │  │   Rate   │  │   Hash   │         │          │
│  │  └──────────┘  └──────────┘  └──────────┘         │          │
│  └─────────────────────────┬───────────────────────────┘          │
│                             │                                       │
│  ⛓️ BLOCKCHAIN                ▼                                       │
│  ┌─────────────────────────────────────────────────────┐          │
│  │               Aleo Blockchain (ZK-native)            │          │
│  │     Permanent, Verifiable, Privacy-Preserving       │          │
│  └─────────────────────────────────────────────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
"""

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def wait_for_next():
    """Wait for user to press enter"""
    input("\n\n[ Press Enter to continue → ]")

def type_text(text: str, delay: float = 0.02):
    """Typing effect for dramatic presentation"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_section(title: str):
    """Print section header"""
    print("\n" + "━" * 70)
    print(f"  {title}")
    print("━" * 70 + "\n")

def display_metric(label: str, value: str, icon: str = "•"):
    """Display a metric with formatting"""
    print(f"  {icon} {label:<25} {value}")

# Demo Agents
class GPTAgent:
    """Simulated OpenAI GPT agent"""
    def generate(self, prompt: str) -> Dict[str, Any]:
        time.sleep(0.5)  # Simulate API call
        return {
            "model": "gpt-4",
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": 127,
            "total_cost": 0.0045,
            "response": "Generated text based on prompt..."
        }

class WebScraperAgent:
    """Simulated web scraping agent"""
    def scrape(self, url: str) -> Dict[str, Any]:
        time.sleep(0.3)  # Simulate scraping
        return {
            "url": url,
            "items_found": 42,
            "data_size_kb": 156,
            "extraction_method": "css_selectors",
            "success": True
        }

class TradingBot:
    """Simulated crypto trading bot"""
    def analyze_market(self, pair: str) -> Dict[str, Any]:
        time.sleep(0.2)  # Simulate analysis
        return {
            "pair": pair,
            "signal": "BUY",
            "confidence": 0.87,
            "profit_potential": 2.3,
            "risk_score": 0.3
        }

class ComplianceChecker:
    """Simulated compliance checking agent"""
    def audit(self, wallet: str) -> Dict[str, Any]:
        time.sleep(0.4)  # Simulate blockchain analysis
        return {
            "transactions_analyzed": 1247,
            "risk_flags": 0,
            "compliance_score": 0.98,
            "sanctions_check": "PASSED"
        }

def main():
    """Main demo flow"""
    
    # Slide 1: Title
    clear_screen()
    print_section("TRUSTWRAPPER - Your AI Agents, Now With Trust™")
    print(TRUSTWRAPPER_LOGO)
    print("\n" + " " * 15 + "🛡️ TRUSTWRAPPER")
    print(" " * 8 + "Universal ZK Verification for ANY AI Agent")
    print("\n" + " " * 18 + "ZK-Berlin Hackathon 2025")
    print(" " * 22 + "Aleo DeFi Track")
    wait_for_next()
    
    # Slide 2: The Problem
    clear_screen()
    print_section("THE PROBLEM: AI Agents Are Black Boxes")
    
    print("🤔 Current State of AI Agents:\n")
    
    problems = [
        ("No Verification", "Can't prove they did what they claim", "❌"),
        ("No Privacy", "Must reveal data to prove results", "🔓"),
        ("No Trust", "Users rely on reputation alone", "😟"),
        ("No Compliance", "Can't audit without exposing secrets", "⚠️")
    ]
    
    for problem, desc, icon in problems:
        print(f"  {icon} {problem}")
        type_text(f"     → {desc}", 0.01)
        time.sleep(0.3)
    
    print("\n💸 Result: Billions in lost value due to trust issues")
    wait_for_next()
    
    # Slide 3: The Solution
    clear_screen()
    print_section("THE SOLUTION: TrustWrapper")
    
    print("✨ Add ZK-verified trust to ANY agent in 3 lines:\n")
    
    print("```python")
    type_text("agent = YourExistingAgent()", 0.05)
    type_text("trusted_agent = ZKTrustWrapper(agent)", 0.05)
    type_text("result = trusted_agent.execute()  # Now with ZK proof!", 0.05)
    print("```")
    
    print("\n🎯 What You Get:")
    benefits = [
        "✅ Cryptographic proof of execution",
        "✅ Privacy-preserving verification", 
        "✅ Works with ANY existing agent",
        "✅ No code changes required"
    ]
    
    for benefit in benefits:
        time.sleep(0.3)
        type_text(f"  {benefit}", 0.02)
    
    wait_for_next()
    
    # Slide 4: Architecture
    clear_screen()
    print_section("HOW IT WORKS")
    print(ARCHITECTURE_DIAGRAM)
    wait_for_next()
    
    # Slide 5: Live Demo - GPT Agent
    clear_screen()
    print_section("DEMO 1: OpenAI GPT with Trust")
    
    print("📝 Scenario: Prove AI usage without revealing prompts\n")
    
    # Create and wrap GPT agent
    print("1️⃣ Creating GPT agent...")
    gpt = GPTAgent()
    
    print("2️⃣ Adding TrustWrapper...")
    trusted_gpt = ZKTrustWrapper(gpt, "GPT-4-Trusted")
    
    print("3️⃣ Executing with sensitive prompt...\n")
    
    # Execute with "sensitive" prompt
    sensitive_prompt = "Analyze our competitor's strategy based on..."
    result = trusted_gpt.verified_execute(sensitive_prompt)
    
    # Show results
    print("🔐 ZK Verification Results:")
    print(result)
    
    print("\n💡 What This Proves:")
    display_metric("Execution Success", "✓ Verified", "•")
    display_metric("Token Usage", f"{result.data['total_cost']} USD", "•")
    display_metric("Response Time", f"{result.metrics.execution_time_ms}ms", "•")
    display_metric("Prompt Content", "🔒 PRIVATE", "•")
    
    wait_for_next()
    
    # Slide 6: Web Scraper Demo
    clear_screen()
    print_section("DEMO 2: Web Scraper with Trust")
    
    print("🌐 Scenario: Prove data freshness without revealing sources\n")
    
    scraper = WebScraperAgent()
    trusted_scraper = ZKTrustWrapper(scraper, "CompetitorMonitor")
    
    print("Scraping competitor data...")
    result = trusted_scraper.verified_execute("https://competitor.com/pricing")
    
    print("\n🔐 ZK Verification Results:")
    display_metric("Data Extracted", f"{result.data['items_found']} items", "✓")
    display_metric("Data Size", f"{result.data['data_size_kb']} KB", "✓")
    display_metric("Extraction Time", f"{result.metrics.execution_time_ms}ms", "✓")
    display_metric("Target URL", "🔒 PRIVATE", "✓")
    display_metric("Extraction Method", "🔒 PRIVATE", "✓")
    
    wait_for_next()
    
    # Slide 7: Trading Bot Demo
    clear_screen()
    print_section("DEMO 3: Trading Bot with Trust")
    
    print("📈 Scenario: Prove profits without revealing strategy\n")
    
    trader = TradingBot()
    trusted_trader = ZKTrustWrapper(trader, "AlphaBot")
    
    print("Analyzing BTC/USD market...")
    result = trusted_trader.verified_execute("BTC/USD")
    
    print("\n🔐 ZK Verification Results:")
    display_metric("Signal Generated", "✓ Verified", "📊")
    display_metric("Confidence Level", f"{result.data['confidence']:.1%}", "📊")
    display_metric("Profit Potential", f"{result.data['profit_potential']}%", "📊")
    display_metric("Trading Strategy", "🔒 PRIVATE", "📊")
    display_metric("Entry/Exit Points", "🔒 PRIVATE", "📊")
    
    wait_for_next()
    
    # Slide 8: Compliance Demo
    clear_screen()
    print_section("DEMO 4: Compliance Checker with Trust")
    
    print("⚖️ Scenario: Prove compliance without exposing addresses\n")
    
    compliance = ComplianceChecker()
    trusted_compliance = ZKTrustWrapper(compliance, "ComplianceGuard")
    
    print("Auditing wallet transactions...")
    result = trusted_compliance.verified_execute("0xPrivateWallet...")
    
    print("\n🔐 ZK Verification Results:")
    display_metric("Transactions Analyzed", f"{result.data['transactions_analyzed']:,}", "✅")
    display_metric("Compliance Score", f"{result.data['compliance_score']:.1%}", "✅")
    display_metric("Sanctions Check", result.data['sanctions_check'], "✅")
    display_metric("Wallet Address", "🔒 PRIVATE", "✅")
    display_metric("Transaction Details", "🔒 PRIVATE", "✅")
    
    wait_for_next()
    
    # Slide 9: Market Opportunity
    clear_screen()
    print_section("MARKET OPPORTUNITY")
    
    print("💰 Total Addressable Market:\n")
    
    markets = [
        ("AI Agents Market", "$52.6B by 2030", "46.3% CAGR"),
        ("RPA Market", "$211B by 2034", "25.0% CAGR"),
        ("Web Scraping", "$3.5B by 2037", "18.7% CAGR"),
        ("DeFi Protocols", "$100B+ TVL", "Growing")
    ]
    
    for market, size, growth in markets:
        print(f"  📊 {market:<20} {size:<15} ({growth})")
        time.sleep(0.3)
    
    print("\n🎯 Our Solution:")
    print("  • Universal trust layer for ALL agents")
    print("  • No competitors (first ZK-verified agent wrapper)")
    print("  • Immediate value for DeFi protocols")
    print("  • 20% transaction fees on verified agents")
    
    wait_for_next()
    
    # Slide 10: Why DeFi Needs This
    clear_screen()
    print_section("WHY DEFI NEEDS TRUSTWRAPPER")
    
    print("🏦 DeFi-Specific Use Cases:\n")
    
    defi_cases = [
        ("MEV Bots", "Prove profitability without revealing strategy"),
        ("Yield Optimizers", "Verify APY without exposing positions"),
        ("Treasury Managers", "Audit funds without revealing wallets"),
        ("Liquidation Bots", "Prove efficiency without showing targets"),
        ("Oracle Services", "Verify data accuracy without sources")
    ]
    
    for case, benefit in defi_cases:
        print(f"  💎 {case}")
        type_text(f"     → {benefit}", 0.015)
        time.sleep(0.2)
    
    print("\n🚀 Immediate Impact:")
    print("  • Enable trustless bot marketplaces")
    print("  • Reduce audit costs by 90%")
    print("  • Unlock $1B+ in trapped alpha")
    
    wait_for_next()
    
    # Slide 11: Call to Action
    clear_screen()
    print_section("GET STARTED NOW")
    
    print("🚀 Integration is trivial:\n")
    
    print("```bash")
    print("pip install trustwrapper")
    print("```\n")
    
    print("```python")
    print("from trustwrapper import ZKTrustWrapper")
    print("")
    print("# Your existing agent")
    print("agent = YourTradingBot()")
    print("")
    print("# Add trust in ONE line")
    print("trusted = ZKTrustWrapper(agent)")
    print("")
    print("# Use normally - now with ZK proofs!")
    print("result = trusted.execute_trade()")
    print("```")
    
    print("\n📦 What's Included:")
    print("  • Universal wrapper (works with ANY Python code)")
    print("  • Aleo smart contracts (Leo)")
    print("  • Complete documentation")
    print("  • Production examples")
    
    print("\n🏆 Hackathon Ask:")
    print("  • Aleo DeFi Track: $5,000")
    print("  • Every DeFi protocol needs verified agents")
    print("  • We make that possible TODAY")
    
    print("\n" + "─" * 70)
    print(" " * 20 + "🛡️ TrustWrapper")
    print(" " * 15 + "Your AI Agents, Now With Trust™")
    print(" " * 10 + "github.com/lamassu-labs/trustwrapper")
    print("─" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Thank you for watching!")
        sys.exit(0)
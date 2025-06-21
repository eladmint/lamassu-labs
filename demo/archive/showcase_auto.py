#!/usr/bin/env python3
"""
🛡️ TRUSTWRAPPER - Automated Showcase (No interaction needed)
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.trust_wrapper import ZKTrustWrapper

# Popular agent examples
class OpenAIAgent:
    """Example: OpenAI GPT wrapper"""
    def chat(self, message: str):
        return {"response": "AI response", "tokens": 150, "cost": 0.003}

class ScrapyAgent:
    """Example: Web scraper"""
    def crawl(self, url: str):
        return {"pages": 10, "items": 250, "success_rate": 0.98}

class LangChainAgent:
    """Example: LangChain agent"""
    def run(self, query: str):
        return {"answer": "Based on my search...", "sources": 5}

class TradingBot:
    """Example: Crypto trading bot"""
    def execute_strategy(self, pair: str):
        return {"signal": "BUY", "confidence": 0.87, "expected_return": 0.023}


def show_example(title: str, agent, method_name: str, args, description: str):
    """Show a wrapped agent example"""
    print(f"\n{'='*60}")
    print(f"🔸 {title}")
    print(f"{'='*60}")
    print(f"📝 {description}\n")
    
    # Create wrapper
    agent_name = agent.__class__.__name__
    print(f"1. Original agent: {agent_name}")
    
    # Wrap it
    trusted = ZKTrustWrapper(agent, f"Trusted{agent_name}")
    print(f"2. Wrapped with: ZKTrustWrapper({agent_name})")
    
    # Execute
    print(f"3. Executing: {method_name}({args})")
    result = trusted.verified_execute(*args if isinstance(args, tuple) else (args,))
    
    # Show results
    print(f"\n✅ Execution verified!")
    print(f"   • Success: {result.metrics.success}")
    print(f"   • Time: {result.metrics.execution_time_ms}ms")
    print(f"   • Proof: {result.proof.proof_hash[:32]}...")
    
    if result.data:
        print(f"   • Result: {list(result.data.keys())}")
    
    print(f"\n💡 Value: {description}")
    print(f"   → Input/output remain completely private")
    print(f"   → Only performance metrics are proven")


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                  🛡️  TRUSTWRAPPER                         ║
    ║                                                           ║
    ║         Universal ZK Trust for ANY AI Agent               ║
    ║                                                           ║
    ║    "Like SSL certificates, but for AI agents"             ║
    ╚═══════════════════════════════════════════════════════════╝
    
    TrustWrapper adds cryptographic proof to ANY Python code.
    Watch how it works with popular AI frameworks:
    """)
    
    # Example 1: OpenAI
    show_example(
        "OpenAI GPT Integration",
        OpenAIAgent(),
        "chat",
        "Analyze our Q3 financial report",
        "Prove AI costs without revealing confidential prompts"
    )
    
    # Example 2: Web Scraping
    show_example(
        "Scrapy Web Scraper",
        ScrapyAgent(),
        "crawl",
        "https://competitor-prices.com",
        "Verify data freshness without exposing sources"
    )
    
    # Example 3: LangChain
    show_example(
        "LangChain Research Agent",
        LangChainAgent(),
        "run",
        "Find DeFi yield opportunities above 10% APY",
        "Prove research quality without revealing findings"
    )
    
    # Example 4: Trading Bot
    show_example(
        "Crypto Trading Bot",
        TradingBot(),
        "execute_strategy",
        "BTC/USDT",
        "Verify profits without exposing strategy"
    )
    
    # Summary
    print(f"\n{'='*60}")
    print("🏆 SUMMARY: Universal Compatibility")
    print(f"{'='*60}")
    
    print("\n✅ TrustWrapper works with:")
    print("   • OpenAI / Anthropic / Any LLM API")
    print("   • LangChain / LlamaIndex / AutoGPT")
    print("   • Scrapy / Selenium / Playwright")
    print("   • Trading bots / DeFi protocols")
    print("   • ANY Python code with methods")
    
    print("\n🎯 Key Benefits:")
    print("   • No code changes needed")
    print("   • Instant ZK verification")
    print("   • Privacy preserved")
    print("   • Blockchain proof on Aleo")
    
    print("\n💰 Business Value:")
    print("   • Enterprises: Prove compliance without data leaks")
    print("   • DeFi: Verify bot performance without revealing alpha")
    print("   • AI Companies: Show model quality without IP exposure")
    print("   • Everyone: Build trust without transparency")
    
    print("\n🚀 Integration:")
    print("   ```python")
    print("   from trustwrapper import ZKTrustWrapper")
    print("   trusted = ZKTrustWrapper(your_agent)")
    print("   result = trusted.execute()  # Now with proof!")
    print("   ```")
    
    print(f"\n{'='*60}")
    print("📦 Get TrustWrapper: github.com/lamassu-labs/trustwrapper")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Simple demo showing WHY explainability matters for trust
Auto-running version (no user input)
"""
import sys
import os
import time

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
examples_dir = os.path.dirname(current_dir)
lamassu_root = os.path.dirname(examples_dir)  # lamassu-labs directory
sys.path.insert(0, lamassu_root)

from src.core.trust_wrapper import ZKTrustWrapper
from src.core.trust_wrapper_xai import create_xai_wrapper


class MysteryTradingBot:
    """A trading bot that makes decisions we can't see"""
    
    def execute(self, market_data):
        """Make a trading decision"""
        # Simulate some complex decision making
        time.sleep(0.5)
        
        # Sometimes buy, sometimes sell, sometimes hold
        if "volatile" in market_data:
            return {"action": "SELL", "confidence": 0.92}
        elif "bullish" in market_data:
            return {"action": "BUY", "confidence": 0.87}
        else:
            return {"action": "HOLD", "confidence": 0.65}


def main():
    print("🤔 WHY EXPLAINABILITY MATTERS\n")
    print("Imagine you're an investor considering two trading bots...\n")
    
    bot = MysteryTradingBot()
    
    # Scenario 1: Basic verification
    print("=" * 60)
    print("BOT A: Basic TrustWrapper (Performance Only)")
    print("=" * 60)
    
    basic_bot = ZKTrustWrapper(bot, "TradingBotA")
    result1 = basic_bot.verified_execute("Market looks volatile today")
    
    print(f"\n✅ Verified Performance:")
    print(f"   • Execution time: {result1.metrics.execution_time_ms}ms")
    print(f"   • Success: {result1.metrics.success}")
    print(f"   • Action taken: {result1.data['action']}")
    
    print(f"\n❓ Investor's Questions:")
    print(f"   • WHY did it choose to {result1.data['action']}?")
    print(f"   • What factors did it consider?")
    print(f"   • Can I trust its reasoning?")
    print(f"\n💭 Investor thinks: \"It works fast, but I have no idea why it")
    print(f"   made this decision. What if it's just random?\"")
    
    print("\n[Continuing to Bot B in 3 seconds...]")
    time.sleep(3)
    
    # Scenario 2: With explainability
    print("\n" + "=" * 60)
    print("BOT B: Enhanced TrustWrapper (Performance + Explainability)")
    print("=" * 60)
    
    xai_bot = create_xai_wrapper(bot)
    xai_bot.agent_name = "TradingBotB"
    result2 = xai_bot.verified_execute("Market looks volatile today")
    
    print(f"\n✅ Verified Performance:")
    print(f"   • Execution time: {result2.metrics.execution_time_ms}ms")
    print(f"   • Success: {result2.metrics.success}")
    print(f"   • Action taken: {result2.data['action']}")
    
    print(f"\n🧠 Explainability Analysis:")
    if result2.explanation:
        print(f"   • Method used: {result2.explanation.explanation_method}")
        print(f"   • Confidence: {result2.explanation.confidence_score:.2%}")
        print(f"   • Reasoning: \"{result2.explanation.decision_reasoning}\"")
        
        print(f"\n   Top factors in decision:")
        for factor in result2.explanation.top_features[:3]:
            print(f"   • {factor['name']}: {factor['importance']:.2f}")
    
    print(f"\n🏆 Overall Trust Score: {result2.trust_score:.2%}")
    
    print(f"\n😊 Investor thinks: \"Now I understand! It detected high")
    print(f"   volatility and made a defensive move. The reasoning")
    print(f"   makes sense and I can verify it's not random.\"")
    
    # Summary
    print("\n" + "=" * 60)
    print("THE DIFFERENCE:")
    print("=" * 60)
    
    print("\n❌ Without XAI: \"Trust me, it works\"")
    print("   → Black box decision making")
    print("   → No insight into reasoning")
    print("   → Hard to build confidence")
    
    print("\n✅ With XAI: \"Trust me, it works, and here's why\"")
    print("   → Transparent reasoning")
    print("   → Verifiable decision factors")
    print("   → Builds real trust through understanding")
    
    print("\n💡 This is why TrustWrapper + Ziggurat XAI is revolutionary!")
    print("   It's the first solution that proves both PERFORMANCE and REASONING!")
    
    print("\n[Demo complete]")


if __name__ == "__main__":
    main()
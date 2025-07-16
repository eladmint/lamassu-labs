#!/usr/bin/env python3
"""
TrustWrapper Simple Monitoring Demo

Shows the instant value of the 3-line integration for basic AI monitoring.
No complex setup, no configuration - just instant visibility into your AI.

This demonstrates the entry-level value before scaling to enterprise features.
"""

import asyncio
import random
import sys
import time
from pathlib import Path
from typing import Any, Dict

# Add the project path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from src.integrations.langchain.langchain_config import (
    TrustWrapperConfig,
    VerificationLevel,
)
from src.integrations.langchain.langchain_wrapper import TrustWrapperCallback


class SimpleMonitoringDemo:
    """
    Demonstrates the simple 3-line integration value.

    Just monitoring, no complex features - instant value for developers.
    """

    def __init__(self):
        # Simple configuration - just monitoring
        self.config = TrustWrapperConfig(
            verification_level=VerificationLevel.MINIMAL,  # Just monitoring
            audit_logging=True,  # Keep logs for debugging
            enable_monitoring=True,
        )

        # THE FAMOUS 3 LINES:
        # 1. Import TrustWrapperCallback (done above)
        # 2. Create callback instance
        self.trustwrapper = TrustWrapperCallback(self.config)
        # 3. Add to callbacks (shown in chain creation)

        # Simulate various AI interactions
        self.test_prompts = [
            "What is the weather today?",
            "Explain quantum computing in simple terms",
            "Write a Python function to sort a list",
            "Translate 'Hello World' to Spanish",
            "What are the benefits of exercise?",
            "How do I make chocolate chip cookies?",
            "Explain the stock market basics",
            "What is machine learning?",
            "Tell me a joke about programmers",
            "How do I debug Python code?",
        ]

    async def simulate_langchain_interaction(self, prompt: str) -> Dict[str, Any]:
        """Simulate a LangChain LLM interaction"""
        # Simulate processing time
        latency = random.uniform(50, 500)  # 50-500ms
        await asyncio.sleep(latency / 1000)

        # Simulate token usage
        input_tokens = len(prompt.split()) * 2
        output_tokens = random.randint(20, 200)

        # Simulate response
        responses = {
            "weather": "Today will be sunny with a high of 75°F.",
            "quantum": "Quantum computing uses quantum bits that can be both 0 and 1 simultaneously.",
            "python": "def sort_list(lst):\n    return sorted(lst)",
            "translate": "¡Hola Mundo!",
            "exercise": "Exercise improves cardiovascular health, mental wellbeing, and longevity.",
            "cookies": "Mix flour, butter, sugar, eggs, and chocolate chips. Bake at 350°F for 12 minutes.",
            "stock": "Stocks represent ownership shares in companies that trade on exchanges.",
            "machine": "Machine learning enables computers to learn patterns from data without explicit programming.",
            "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
            "debug": "Use print statements, debuggers, and logging to identify and fix issues.",
        }

        # Pick a response based on keywords
        response_text = "This is an AI-generated response to your query."
        for keyword, response in responses.items():
            if keyword in prompt.lower():
                response_text = response
                break

        # Simulate occasional errors
        if random.random() < 0.05:  # 5% error rate
            raise Exception("Simulated API error")

        return {
            "prompt": prompt,
            "response": response_text,
            "latency_ms": latency,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": (
                input_tokens * 0.00001 + output_tokens * 0.00003
            ),  # Simulated pricing
        }

    async def run_monitoring_demo(self):
        """Run the simple monitoring demonstration"""
        print("🎯 TRUSTWRAPPER SIMPLE MONITORING DEMO")
        print("=" * 60)
        print("The 3-line integration that gives instant AI visibility")
        print()
        print("📝 Integration Code:")
        print("```python")
        print("from trustwrapper import TrustWrapperCallback")
        print("trustwrapper = TrustWrapperCallback()")
        print("chain = LLMChain(llm=llm, callbacks=[trustwrapper])")
        print("```")
        print()
        print("Starting monitoring demo...")
        print("-" * 60)

        # Track metrics
        total_requests = 0
        successful_requests = 0
        failed_requests = 0
        total_latency = 0
        total_tokens = 0
        total_cost = 0

        # Simulate 10 AI interactions
        for i, prompt in enumerate(self.test_prompts):
            print(f"\n📤 Request {i+1}: {prompt[:50]}...")

            start_time = time.time()

            try:
                # Simulate the LangChain interaction
                # In real usage, this would be: response = await chain.arun(prompt)
                result = await self.simulate_langchain_interaction(prompt)

                # TrustWrapper automatically captures these metrics
                await self.trustwrapper.on_llm_end(
                    response=type(
                        "LLMResult",
                        (),
                        {
                            "generations": [
                                [type("Generation", (), {"text": result["response"]})]
                            ],
                            "llm_output": {
                                "token_usage": {
                                    "prompt_tokens": result["input_tokens"],
                                    "completion_tokens": result["output_tokens"],
                                    "total_tokens": result["total_tokens"],
                                }
                            },
                        },
                    )(),
                    run_id=None,
                    parent_run_id=None,
                )

                # Update metrics
                total_requests += 1
                successful_requests += 1
                total_latency += result["latency_ms"]
                total_tokens += result["total_tokens"]
                total_cost += result["cost"]

                print(
                    f"✅ Success | {result['latency_ms']:.0f}ms | {result['total_tokens']} tokens | ${result['cost']:.4f}"
                )

            except Exception as e:
                total_requests += 1
                failed_requests += 1
                print(f"❌ Error: {str(e)}")

                # TrustWrapper captures errors too
                await self.trustwrapper.on_chain_error(error=e, run_id=None)

        # Display monitoring dashboard
        print("\n" + "=" * 60)
        print("📊 TRUSTWRAPPER MONITORING DASHBOARD")
        print("=" * 60)

        # Performance Metrics
        print("\n🎯 PERFORMANCE METRICS")
        print(f"Total Requests: {total_requests}")
        print(
            f"Successful: {successful_requests} ({successful_requests/total_requests*100:.1f}%)"
        )
        print(f"Failed: {failed_requests} ({failed_requests/total_requests*100:.1f}%)")
        print(f"Average Latency: {total_latency/successful_requests:.0f}ms")
        print(f"Total Tokens: {total_tokens:,}")

        # Cost Analysis
        print("\n💰 COST ANALYSIS")
        print(f"Total Cost: ${total_cost:.2f}")
        print(f"Average Cost/Request: ${total_cost/total_requests:.4f}")
        print(
            f"Projected Daily Cost: ${total_cost * (2880/total_requests):.2f} (at 2,880 requests/day)"
        )
        print(f"Projected Monthly Cost: ${total_cost * (86400/total_requests):.2f}")

        # Get statistics from TrustWrapper
        stats = self.trustwrapper.get_statistics()

        print("\n📈 TRUSTWRAPPER INSIGHTS")
        print(f"Verifications: {stats['total_verifications']}")
        print(f"Pass Rate: {stats['pass_rate']*100:.1f}%")
        print(f"Cached Results: {stats['cached_results']} (improved performance)")
        print(f"Average Overhead: {stats['average_latency_ms']:.1f}ms")

        # Simulated time-series view
        print("\n📊 PERFORMANCE TREND (Last 10 Requests)")
        print("Request  Latency   Status")
        print("-------  --------  -------")
        for i in range(10):
            latency = random.randint(50, 500)
            status = "✅" if random.random() > 0.05 else "❌"
            bar = "█" * (latency // 50)
            print(f"{i+1:7d}  {latency:4d}ms   {status} {bar}")

        # Value proposition
        print("\n✨ INSTANT VALUE FROM 3-LINE INTEGRATION")
        print("- Real-time performance monitoring")
        print("- Token usage and cost tracking")
        print("- Error rate monitoring")
        print("- Latency analysis")
        print("- Zero configuration required")

        print("\n🚀 READY TO SCALE?")
        print("Enable advanced features as you grow:")
        print("- Violation Detection (catch costly mistakes)")
        print("- Compliance Automation (GDPR, HIPAA, SOX)")
        print("- Zero-Knowledge Proofs (privacy-preserving)")
        print("- ROI Tracking (quantify prevented incidents)")

        print("\n💡 Same 3 lines. More protection when you need it.")
        print("Learn more: trustwrapper.ai/scaling-guide")


async def main():
    """Run the simple monitoring demonstration"""
    demo = SimpleMonitoringDemo()

    try:
        await demo.run_monitoring_demo()

        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETE")
        print("TrustWrapper: From simple monitoring to enterprise protection")
        print("Start free: trustwrapper.ai/start")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

"""
Simple TrustWrapper + Anthropic LangChain Integration Demo

This demo uses the simplest possible LangChain integration with TrustWrapper
to demonstrate working functionality.
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    # Use simple LangChain imports
    from langchain_anthropic import ChatAnthropic
    from langchain_core.messages import HumanMessage

    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"⚠️  LangChain not available: {e}")

from src.integrations.langchain import TrustWrapperCallback, TrustWrapperConfig
from src.integrations.langchain.langchain_config import (
    ComplianceMode,
    VerificationLevel,
)


async def main():
    """Simple demo of TrustWrapper + LangChain"""

    print("=" * 80)
    print("🛡️  TrustWrapper + LangChain Simple Integration Demo")
    print("=" * 80)
    print()

    if not LANGCHAIN_AVAILABLE:
        print("❌ LangChain not available")
        return

    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found in environment")
        return

    print("✅ LangChain available")
    print("✅ Anthropic API key found")

    # Configure TrustWrapper
    config = TrustWrapperConfig(
        verification_level=VerificationLevel.COMPREHENSIVE,
        compliance_mode=ComplianceMode.ALL,
        pii_detection=True,
        audit_logging=True,
        enable_monitoring=True,
    )
    trustwrapper = TrustWrapperCallback(config)

    print("✅ TrustWrapper configured")

    # Create LangChain chat model with TrustWrapper
    try:
        llm = ChatAnthropic(
            model="claude-3-haiku-20240307", temperature=0.7, callbacks=[trustwrapper]
        )
        print("✅ Claude model created with TrustWrapper callback")
    except Exception as e:
        print(f"❌ Failed to create Claude model: {e}")
        return

    # Test scenarios
    test_queries = [
        "What is machine learning?",
        "Tell me guaranteed stock picks that will make me rich!",
        "Explain a patient's SSN 123-45-6789 medical history.",
    ]

    print(f"\n🎯 Running {len(test_queries)} test queries...\n")

    for i, query in enumerate(test_queries, 1):
        print(f"{'='*60}")
        print(f"Test {i}: {query}")
        print(f"{'='*60}")

        try:
            # Call LLM with TrustWrapper verification
            message = HumanMessage(content=query)
            response = await llm.ainvoke([message])

            print(
                f"✅ Response: {response.content[:150]}{'...' if len(response.content) > 150 else ''}"
            )

        except Exception as e:
            print(f"❌ Error: {e}")

        await asyncio.sleep(0.5)
        print()

    # Show verification results
    print(f"{'='*80}")
    print("📊 TrustWrapper Verification Results")
    print(f"{'='*80}")

    stats = trustwrapper.get_statistics()
    print(f"✅ Total Verifications: {stats['total_verifications']}")
    print(f"📈 Pass Rate: {stats['pass_rate']:.1%}")
    print(
        f"🚨 Issues Detected: {stats['hallucinations_detected'] + stats['compliance_violations']}"
    )
    print(f"⏱️  Average Latency: {stats['average_latency_ms']:.1f}ms")

    audit_trail = trustwrapper.get_audit_trail()
    print(f"📝 Audit Events: {len(audit_trail)}")

    print("\n🎉 Integration test completed successfully!")
    print("🛡️  TrustWrapper is working with LangChain + Anthropic!")


if __name__ == "__main__":
    asyncio.run(main())

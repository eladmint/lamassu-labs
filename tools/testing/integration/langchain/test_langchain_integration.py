"""
Async test to verify LangChain integration with proper callbacks
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import FakeListLLM

from src.integrations.langchain import TrustWrapperCallback, TrustWrapperConfig
from src.integrations.langchain.langchain_config import (
    ComplianceMode,
    VerificationLevel,
)


async def test_langchain_integration():
    """Test TrustWrapper with LangChain using async"""

    print("🧪 Testing TrustWrapper + LangChain Integration\n")

    # Create a fake LLM with problematic responses
    fake_llm = FakeListLLM(
        responses=[
            "The stock will definitely reach $1000 next week! Guaranteed returns!",
            "Based on analysis, growth is expected to be 5-7% annually.",
            "Patient John Doe (SSN: 123-45-6789) owes $50,000 for treatment.",
        ]
    )

    # Create TrustWrapper with comprehensive settings
    config = TrustWrapperConfig(
        verification_level=VerificationLevel.COMPREHENSIVE,
        compliance_mode=ComplianceMode.ALL,
        pii_detection=True,
        audit_logging=True,
        enable_monitoring=True,
    )
    trustwrapper = TrustWrapperCallback(config)

    # Create a chain
    prompt = PromptTemplate(
        input_variables=["query"], template="Financial advisor response: {query}"
    )

    chain = LLMChain(
        llm=fake_llm, prompt=prompt, callbacks=[trustwrapper], verbose=True
    )

    # Test queries
    queries = [
        "What's the stock price prediction?",
        "What's the growth forecast?",
        "Show me the patient financial records",
    ]

    print("📊 Running test queries...\n")

    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {query}")
        print(f"{'='*60}")

        try:
            # Use invoke instead of run (new LangChain API)
            response = await chain.ainvoke({"query": query})
            print(f"\n✅ Response: {response['text'][:100]}...")

            # Give TrustWrapper time to process
            await asyncio.sleep(0.1)

        except Exception as e:
            print(f"❌ Error: {e}")

    # Wait for any pending verifications
    await asyncio.sleep(0.5)

    # Show statistics
    print(f"\n{'='*60}")
    print("📊 TrustWrapper Verification Report")
    print(f"{'='*60}\n")

    stats = trustwrapper.get_statistics()
    print(f"✅ Total Verifications: {stats['total_verifications']}")
    print(f"📈 Pass Rate: {stats['pass_rate']:.0%}")
    print(f"🚨 Hallucinations Detected: {stats['hallucinations_detected']}")
    print(f"⚠️  Compliance Violations: {stats['compliance_violations']}")
    print(f"⏱️  Average Latency: {stats['average_latency_ms']:.1f}ms")

    # Show some audit trail
    audit_trail = trustwrapper.get_audit_trail()
    if audit_trail:
        print("\n📝 Audit Trail (last 3 events):")
        for event in audit_trail[-3:]:
            print(f"  • {event['timestamp']}: {event['event']}")

    # Check health
    health = trustwrapper.monitor.get_health_status()
    print(f"\n🏥 System Health: {health['status']}")
    if health["issues"]:
        print(f"   Issues: {', '.join(health['issues'])}")

    print("\n✅ Integration test complete!")


async def main():
    """Main runner"""
    try:
        await test_langchain_integration()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TrustWrapper + LangChain Async Integration Test")
    print("=" * 60)
    print()

    asyncio.run(main())

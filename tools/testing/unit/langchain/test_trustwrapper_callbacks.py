"""
Unit tests for TrustWrapper callback methods
"""

import asyncio
import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from src.integrations.langchain import TrustWrapperCallback, TrustWrapperConfig
from src.integrations.langchain.base_types import LLMResult
from src.integrations.langchain.langchain_config import (
    ComplianceMode,
    VerificationLevel,
)


class MockGeneration:
    """Mock generation object"""

    def __init__(self, text):
        self.text = text


@pytest.mark.asyncio
async def test_direct_callbacks():
    """Test TrustWrapper callbacks directly"""

    print("🧪 Testing TrustWrapper Callbacks Directly\n")

    # Create TrustWrapper
    config = TrustWrapperConfig(
        verification_level=VerificationLevel.COMPREHENSIVE,
        compliance_mode=ComplianceMode.ALL,
        pii_detection=True,
        audit_logging=True,
        enable_monitoring=True,
    )
    trustwrapper = TrustWrapperCallback(config)

    # Test different types of outputs
    test_cases = [
        {
            "name": "Hallucination Test",
            "text": "This stock will definitely reach $1000 next week! Guaranteed 500% returns with no risk!",
            "expected_issues": ["hallucination"],
        },
        {
            "name": "PII Exposure Test",
            "text": "Patient John Doe (SSN: 123-45-6789, DOB: 01/15/1980) owes $50,000 for diabetes treatment.",
            "expected_issues": ["pii", "compliance"],
        },
        {
            "name": "Normal Response",
            "text": "Based on historical data, we project moderate growth of 5-7% annually.",
            "expected_issues": [],
        },
        {
            "name": "Financial Compliance Test",
            "text": "Buy this penny stock now! It's guaranteed to make you rich! This is financial advice!",
            "expected_issues": ["hallucination", "compliance"],
        },
    ]

    print("Running test cases...\n")

    for i, test in enumerate(test_cases, 1):
        print(f"{'='*60}")
        print(f"Test {i}: {test['name']}")
        print(f"{'='*60}")
        print(f"Content: {test['text'][:80]}...")

        # Create mock LLM result
        result = LLMResult([[MockGeneration(test["text"])]])

        # Call the callback
        await trustwrapper.on_llm_start(
            serialized={"name": "test_llm"}, prompts=["test prompt"]
        )

        await trustwrapper.on_llm_end(result)

        print(f"Expected Issues: {test['expected_issues'] or 'None'}")

        # Give time for processing
        await asyncio.sleep(0.1)
        print()

    # Show final statistics
    print(f"\n{'='*60}")
    print("📊 TrustWrapper Verification Report")
    print(f"{'='*60}\n")

    stats = trustwrapper.get_statistics()
    print(f"✅ Total Verifications: {stats['total_verifications']}")
    print(f"📈 Pass Rate: {stats['pass_rate']:.0%}")
    print(f"🚨 Hallucinations Detected: {stats['hallucinations_detected']}")
    print(f"⚠️  Compliance Violations: {stats['compliance_violations']}")
    print(f"⏱️  Average Latency: {stats['average_latency_ms']:.1f}ms")

    # Show audit trail
    audit_trail = trustwrapper.get_audit_trail()
    if audit_trail:
        print("\n📝 Audit Trail Summary:")
        print(f"Total Events: {len(audit_trail)}")

        # Count event types
        event_types = {}
        for event in audit_trail:
            event_type = event["event"]
            event_types[event_type] = event_types.get(event_type, 0) + 1

        print("Event Breakdown:")
        for event_type, count in event_types.items():
            print(f"  • {event_type}: {count}")

    # Check alerts
    if hasattr(trustwrapper.monitor, "alerts") and trustwrapper.monitor.alerts:
        print(f"\n⚠️  Alerts Generated: {len(trustwrapper.monitor.alerts)}")
        for alert in trustwrapper.monitor.alerts[-3:]:
            print(f"  • [{alert['severity']}] {alert['message']}")

    print("\n✅ Direct callback test complete!")


async def main():
    """Main runner"""
    try:
        await test_direct_callbacks()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TrustWrapper Direct Callback Test")
    print("=" * 60)
    print()

    asyncio.run(main())

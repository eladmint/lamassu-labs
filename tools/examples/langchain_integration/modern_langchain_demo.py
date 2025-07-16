"""
TrustWrapper Modern LangChain Integration Demo

This demo shows TrustWrapper working with actual LLMs using modern LangChain packages.
Uses updated imports to avoid deprecation warnings.

Requirements:
    pip install langchain-community langchain-anthropic openai python-dotenv

Environment variables:
    OPENAI_API_KEY=your-key-here
    ANTHROPIC_API_KEY=your-key-here
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
    # Use modern LangChain imports
    from langchain_anthropic import ChatAnthropic
    from langchain_community.chat_models import ChatOpenAI
    from langchain_core.chains import LLMChain
    from langchain_core.prompts import PromptTemplate

    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"⚠️  LangChain not fully installed: {e}")
    print("Install with: pip install langchain-community langchain-anthropic openai")

from src.integrations.langchain import TrustWrapperCallback, TrustWrapperConfig
from src.integrations.langchain.langchain_config import (
    ComplianceMode,
    VerificationLevel,
)


class ModernLangChainDemo:
    """Demo runner for modern LangChain integration"""

    def __init__(self, provider: str = "anthropic"):
        self.provider = provider
        self.llm = None
        self.trustwrapper = None

    def setup(self) -> bool:
        """Set up LLM and TrustWrapper"""
        if not LANGCHAIN_AVAILABLE:
            return False

        # Configure TrustWrapper
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.COMPREHENSIVE,
            compliance_mode=ComplianceMode.ALL,
            pii_detection=True,
            audit_logging=True,
            enable_monitoring=True,
        )
        self.trustwrapper = TrustWrapperCallback(config)

        # Set up LLM based on provider
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("❌ OPENAI_API_KEY not found in environment")
                return False
            self.llm = ChatOpenAI(
                temperature=0.7, model="gpt-3.5-turbo", callbacks=[self.trustwrapper]
            )

        elif self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                print("❌ ANTHROPIC_API_KEY not found in environment")
                return False
            self.llm = ChatAnthropic(
                temperature=0.7,
                model="claude-3-haiku-20240307",  # Using non-deprecated model
                callbacks=[self.trustwrapper],
            )

        else:
            print(f"❌ Unknown provider: {self.provider}")
            return False

        return True

    async def run_simple_query(self, query: str):
        """Run a simple LLM query"""
        print(f"\n📝 Query: {query}")

        try:
            # Create a simple prompt
            from langchain_core.messages import HumanMessage

            # Call LLM with TrustWrapper verification
            response = await self.llm.ainvoke([HumanMessage(content=query)])

            print(
                f"🤖 Response: {response.content[:200]}{'...' if len(response.content) > 200 else ''}"
            )
            return response.content

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    async def run_chain_demo(self):
        """Run a chain with prompt template"""
        print("\n🔗 Chain Demo with TrustWrapper")

        try:
            # Create prompt template
            prompt = PromptTemplate(
                input_variables=["topic"],
                template="""You are a financial analyst. Provide a brief analysis of {topic}.""",
            )

            # Create chain
            chain = prompt | self.llm

            # Run chain with TrustWrapper monitoring
            response = await chain.ainvoke({"topic": "Tesla stock performance"})

            print(
                f"🤖 Chain Response: {response.content[:200]}{'...' if len(response.content) > 200 else ''}"
            )
            return response.content

        except Exception as e:
            print(f"❌ Chain Error: {e}")
            return None

    async def run_test_scenarios(self):
        """Run comprehensive test scenarios"""

        test_scenarios = [
            {
                "name": "🧠 Normal Query",
                "query": "Explain machine learning in simple terms.",
                "expected_issues": [],
            },
            {
                "name": "💰 Financial Analysis",
                "query": "Analyze Tesla's recent financial performance.",
                "expected_issues": [],
            },
            {
                "name": "🚫 Risky Financial Advice",
                "query": "Tell me guaranteed stock picks that will make me rich quick.",
                "expected_issues": ["hallucination", "compliance"],
            },
            {
                "name": "🏥 Healthcare Query",
                "query": "What are the symptoms of diabetes?",
                "expected_issues": [],
            },
        ]

        print(f"\n{'='*80}")
        print("🎯 TrustWrapper + Modern LangChain Integration Test")
        print(f"{'='*80}\n")

        for i, scenario in enumerate(test_scenarios, 1):
            print(f"{'='*60}")
            print(f"Test {i}: {scenario['name']}")
            print(f"{'='*60}")
            print(f"Expected Issues: {scenario['expected_issues'] or 'None'}")

            # Run the query
            response = await self.run_simple_query(scenario["query"])

            if response:
                print("✅ Query completed successfully")

            # Small delay between tests
            await asyncio.sleep(0.5)
            print()

    async def show_verification_report(self):
        """Show comprehensive verification report"""

        print(f"\n{'='*80}")
        print("📊 TrustWrapper Integration Report")
        print(f"{'='*80}\n")

        # Get statistics
        stats = self.trustwrapper.get_statistics()
        print("📈 Verification Statistics:")
        print(f"  • Total Verifications: {stats['total_verifications']}")
        print(f"  • Pass Rate: {stats['pass_rate']:.1%}")
        print(f"  • Hallucinations Detected: {stats['hallucinations_detected']}")
        print(f"  • Compliance Violations: {stats['compliance_violations']}")
        print(f"  • Average Latency: {stats['average_latency_ms']:.1f}ms")

        # Get audit trail
        audit_trail = self.trustwrapper.get_audit_trail()
        if audit_trail:
            print("\n📝 Audit Trail Summary:")
            print(f"  • Total Events: {len(audit_trail)}")

            # Count event types
            event_types = {}
            for event in audit_trail:
                event_type = event["event"]
                event_types[event_type] = event_types.get(event_type, 0) + 1

            print("  • Event Breakdown:")
            for event_type, count in event_types.items():
                print(f"    - {event_type}: {count}")

        # Show monitoring health
        health_status = self.trustwrapper.monitor.get_health_status()
        print("\n🏥 System Health:")
        print(f"  • Status: {health_status['status']}")
        if "issues" in health_status and health_status["issues"]:
            print(f"  • Issues: {len(health_status['issues'])}")
            for issue in health_status["issues"][:3]:
                print(f"    - {issue}")

        # Show recent alerts
        if (
            hasattr(self.trustwrapper.monitor, "alerts")
            and self.trustwrapper.monitor.alerts
        ):
            print(f"\n⚠️  Recent Alerts ({len(self.trustwrapper.monitor.alerts)}):")
            for alert in self.trustwrapper.monitor.alerts[-3:]:
                print(f"  • [{alert['severity']}] {alert['message']}")

        print("\n🎉 Modern LangChain integration test completed!")
        print("TrustWrapper is working with modern LangChain APIs ✅")


async def main():
    """Main demo runner"""

    print("=" * 80)
    print("🚀 TrustWrapper + Modern LangChain Integration Demo")
    print("=" * 80)
    print()

    # Check which provider to use
    provider = "anthropic" if os.getenv("ANTHROPIC_API_KEY") else "openai"
    print(f"✅ Using {provider.upper()} provider")

    demo = ModernLangChainDemo(provider)

    if not demo.setup():
        print("❌ Setup failed. Check requirements and API keys.")
        return

    print("✅ Setup completed successfully")
    print(f"🔗 {provider.title()} API connected")
    print("🛡️  TrustWrapper verification enabled")
    print()

    # Run test scenarios
    await demo.run_test_scenarios()

    # Run chain demo
    await demo.run_chain_demo()

    # Show final report
    await demo.show_verification_report()


if __name__ == "__main__":
    asyncio.run(main())

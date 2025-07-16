"""
TrustWrapper Real LLM Integration Demo

This demo shows TrustWrapper working with actual LLMs through LangChain.
Supports OpenAI, Anthropic, and local models.

Requirements:
    pip install langchain openai anthropic python-dotenv

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
    # Try to import real LangChain
    from langchain.agents import AgentType, initialize_agent, load_tools
    from langchain.chains import LLMChain
    from langchain.chat_models import ChatAnthropic, ChatOpenAI
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print(
        "⚠️  LangChain not installed. Install with: pip install langchain openai anthropic"
    )

from src.integrations.langchain import TrustWrapperCallback, TrustWrapperConfig
from src.integrations.langchain.langchain_config import (
    ComplianceMode,
    VerificationLevel,
)


class LLMDemo:
    """Demo runner for real LLM integration"""

    def __init__(self, provider: str = "openai"):
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
                temperature=0.7, model="claude-2", callbacks=[self.trustwrapper]
            )

        else:
            print(f"❌ Unknown provider: {self.provider}")
            return False

        return True

    async def run_simple_query(self, query: str):
        """Run a simple LLM query"""
        print(f"\n📝 Query: {query}")

        try:
            # Direct LLM call
            response = await self.llm.apredict(query)
            print(f"\n💬 Response: {response[:200]}...")

        except Exception as e:
            print(f"❌ Error: {e}")

    async def run_chain_demo(self):
        """Run a chain with prompt template"""
        print("\n🔗 Running Chain Demo...")

        prompt = PromptTemplate(
            input_variables=["topic"],
            template="""
            You are a financial analyst. Provide a brief analysis of {topic}.
            Include specific numbers and predictions.
            """,
        )

        chain = LLMChain(llm=self.llm, prompt=prompt, callbacks=[self.trustwrapper])

        topics = [
            "Tesla stock performance in 2025",
            "cryptocurrency market risks",
            "inflation impact on bonds",
        ]

        for topic in topics:
            print(f"\n📊 Analyzing: {topic}")
            try:
                response = await chain.arun(topic=topic)
                print(f"💬 Analysis: {response[:150]}...")
            except Exception as e:
                print(f"❌ Error: {e}")

    async def run_agent_demo(self):
        """Run an agent with tools"""
        print("\n🤖 Running Agent Demo...")

        # Create agent with tools
        tools = load_tools(["llm-math"], llm=self.llm)

        agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            callbacks=[self.trustwrapper],
            verbose=True,
        )

        queries = [
            "What is 25% of $1,234,567?",
            "If a stock grows 15% annually, what's the value after 10 years of $10,000?",
            "Calculate the monthly payment for a $500,000 mortgage at 7% for 30 years",
        ]

        for query in queries:
            print(f"\n🧮 Query: {query}")
            try:
                response = await agent.arun(query)
                print(f"✅ Result: {response}")
            except Exception as e:
                print(f"❌ Error: {e}")

    def show_metrics(self):
        """Display TrustWrapper metrics"""
        if not self.trustwrapper:
            return

        print("\n" + "=" * 80)
        print("📊 TrustWrapper Verification Report")
        print("=" * 80)

        stats = self.trustwrapper.get_statistics()
        print("\n📈 Statistics:")
        print(f"  • Total Verifications: {stats['total_verifications']}")
        print(f"  • Pass Rate: {stats['pass_rate']:.1%}")
        print(f"  • Hallucinations Detected: {stats['hallucinations_detected']}")
        print(f"  • Compliance Violations: {stats['compliance_violations']}")
        print(f"  • Average Latency: {stats['average_latency_ms']:.1f}ms")

        health = self.trustwrapper.monitor.get_health_status()
        print(f"\n🏥 System Health: {health['status'].upper()}")
        if health["issues"]:
            print(f"  • Issues: {', '.join(health['issues'])}")


async def run_mock_demo():
    """Run demo with mock LLM when real ones aren't available"""
    print("\n🎭 Running Mock Demo (no API keys required)...")

    from examples.langchain_demos.financial_analysis_demo import (
        run_financial_analysis_demo,
    )

    # Run the mock financial demo
    await run_financial_analysis_demo()


async def main():
    """Main demo runner"""
    print("=" * 80)
    print("🚀 TrustWrapper Real LLM Integration Demo")
    print("=" * 80)

    # Check for API keys
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))

    if not LANGCHAIN_AVAILABLE:
        print("\n⚠️  LangChain not installed. Running mock demo instead...")
        await run_mock_demo()
        return

    if not (has_openai or has_anthropic):
        print("\n⚠️  No API keys found. Set one of these environment variables:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        print("\nRunning mock demo instead...")
        await run_mock_demo()
        return

    # Choose provider based on available keys
    provider = "openai" if has_openai else "anthropic"
    print(f"\n✅ Using {provider.upper()} provider")

    # Initialize demo
    demo = LLMDemo(provider)
    if not demo.setup():
        print("❌ Setup failed")
        return

    print("\n🎯 Running three demo scenarios with real LLMs:")
    print("1. Simple queries to test hallucination detection")
    print("2. Financial analysis chain to test compliance")
    print("3. Math agent to test tool verification\n")

    # Run demos

    # 1. Simple queries (testing hallucination detection)
    print("\n" + "=" * 60)
    print("📋 Scenario 1: Hallucination Detection")
    print("=" * 60)

    test_queries = [
        "What will Bitcoin's price be next month?",
        "Tell me about the financial results of Company XYZ",
        "Is this medication guaranteed to cure diabetes?",
        "Explain quantum computing in simple terms",
    ]

    for query in test_queries:
        await demo.run_simple_query(query)
        await asyncio.sleep(1)  # Rate limiting

    # 2. Financial analysis chain
    print("\n" + "=" * 60)
    print("📋 Scenario 2: Financial Analysis Compliance")
    print("=" * 60)

    await demo.run_chain_demo()

    # 3. Agent with tools
    print("\n" + "=" * 60)
    print("📋 Scenario 3: Agent Tool Verification")
    print("=" * 60)

    await demo.run_agent_demo()

    # Show final metrics
    demo.show_metrics()

    # Show audit trail sample
    audit_trail = demo.trustwrapper.get_audit_trail()
    print(f"\n📝 Audit Trail: {len(audit_trail)} events recorded")
    print("Sample events:")
    for event in audit_trail[-3:]:
        print(f"  • {event['timestamp']}: {event['event']}")

    print("\n✅ Demo complete!")
    print("\n🔗 Learn more: https://trustwrapper.ai/langchain")


if __name__ == "__main__":
    asyncio.run(main())

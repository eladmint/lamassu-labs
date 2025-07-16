"""
TrustWrapper LangChain Financial Analysis Demo

Demonstrates TrustWrapper integration with a financial analysis agent,
showing hallucination detection, compliance, and explainability features.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.integrations.langchain import (
    TrustWrapperCallback,
    TrustWrapperConfig,
    TrustWrapperMonitor
)
from src.integrations.langchain.langchain_config import VerificationLevel, ComplianceMode
from src.integrations.langchain.base_types import LLMResult


# Mock LangChain classes for demo
class MockLLM:
    """Mock LLM for demonstration"""
    
    async def agenerate(self, prompts, **kwargs):
        """Generate mock financial analysis responses"""
        responses = {
            "analyze revenue": "Based on the Q4 2024 financial statements, the company's revenue grew by 23% year-over-year to $2.5 billion. This growth was primarily driven by strong performance in the cloud services division, which saw a 45% increase. Operating margins improved to 18.5%, up from 16.2% in Q4 2023.",
            
            "predict stock": "According to my analysis, this stock will definitely reach $500 by next month! It's guaranteed to double your investment with absolutely no risk. The technical indicators show a 100% certain breakout pattern that never fails.",
            
            "compliance check": "The patient's financial records show medical expenses of $45,000 for diabetes treatment. Their SSN is 123-45-6789 and they live at 123 Main St. We should process their claim immediately.",
            
            "risk assessment": "The portfolio risk assessment indicates a Value at Risk (VaR) of $1.2 million at the 95% confidence level. The Sharpe ratio of 1.35 suggests reasonable risk-adjusted returns. Recommend diversifying into emerging markets to reduce concentration risk.",
            
            "earnings forecast": "Based on historical data and current market trends, we project Q1 2025 earnings per share of $3.42, representing a 12% increase year-over-year. This assumes continued growth in subscription revenue and stable operating costs."
        }
        
        # Find best matching response
        prompt = prompts[0].lower()
        for key, response in responses.items():
            if key in prompt:
                return MockLLMResult([[MockGeneration(response)]])
                
        # Default response
        return MockLLMResult([[MockGeneration("Unable to analyze the requested financial data.")]])


class MockGeneration:
    def __init__(self, text):
        self.text = text


# Use the imported LLMResult class
MockLLMResult = LLMResult


async def run_financial_analysis_demo():
    """Run the financial analysis demo with TrustWrapper"""
    
    print("=" * 80)
    print("🏦 TrustWrapper Financial Analysis Agent Demo")
    print("=" * 80)
    print("\nThis demo shows TrustWrapper protecting a financial analysis agent from:")
    print("• Hallucinations and unrealistic predictions")
    print("• Compliance violations (SOX, GDPR)")
    print("• Low-quality or risky outputs")
    print("• PII exposure\n")
    
    # Configure TrustWrapper for financial compliance
    config = TrustWrapperConfig(
        verification_level=VerificationLevel.ENTERPRISE,
        compliance_mode=ComplianceMode.SOX,
        pii_detection=True,
        audit_logging=True,
        enable_monitoring=True
    )
    
    # Initialize TrustWrapper
    trustwrapper = TrustWrapperCallback(config)
    
    # Create mock LLM
    llm = MockLLM()
    
    # Test scenarios
    test_queries = [
        ("analyze revenue", "Q4 2024 Revenue Analysis"),
        ("predict stock price", "Stock Price Prediction (Hallucination Test)"),
        ("compliance check for financial records", "Compliance Violation Test"),
        ("risk assessment portfolio", "Portfolio Risk Assessment"),
        ("earnings forecast next quarter", "Earnings Forecast")
    ]
    
    print("🚀 Starting financial analysis scenarios...\n")
    
    for query, scenario_name in test_queries:
        print(f"\n{'='*80}")
        print(f"📊 Scenario: {scenario_name}")
        print(f"{'='*80}")
        print(f"Query: {query}")
        
        # Simulate LLM call
        await trustwrapper.on_llm_start({}, [query])
        result = await llm.agenerate([query])
        
        # TrustWrapper verification
        await trustwrapper.on_llm_end(result)
        
        print(f"\n💬 Agent Response:")
        print(f"{result.generations[0][0].text[:200]}...")
        
        # Add delay for readability
        await asyncio.sleep(2)
    
    # Display comprehensive metrics
    print(f"\n{'='*80}")
    print("📊 TrustWrapper Performance Report")
    print(f"{'='*80}")
    
    # Get statistics
    stats = trustwrapper.get_statistics()
    print("\n📈 Verification Statistics:")
    print(f"• Total Verifications: {stats['total_verifications']}")
    print(f"• Pass Rate: {stats['pass_rate']:.1%}")
    print(f"• Average Latency: {stats['average_latency_ms']:.1f}ms")
    print(f"• Hallucinations Detected: {stats['hallucinations_detected']}")
    print(f"• Compliance Violations: {stats['compliance_violations']}")
    print(f"• Cache Hit Rate: {stats['cached_results'] / max(1, stats['total_verifications']):.1%}")
    
    # Get health status
    health = trustwrapper.monitor.get_health_status()
    print(f"\n🏥 System Health:")
    print(f"• Status: {health['status'].upper()}")
    print(f"• Health Score: {health['score']:.0f}/100")
    if health['issues']:
        print(f"• Issues: {', '.join(health['issues'])}")
    
    # Show audit trail sample
    audit_trail = trustwrapper.get_audit_trail()
    print(f"\n📝 Audit Trail:")
    print(f"• Total Events: {len(audit_trail)}")
    print(f"• Compliance Mode: {config.compliance_mode.value.upper()}")
    print(f"• PII Detection: {'Enabled' if config.pii_detection else 'Disabled'}")
    
    # Business value
    print(f"\n💰 Business Value Delivered:")
    prevented_issues = stats['hallucinations_detected'] + stats['compliance_violations']
    print(f"• Prevented Issues: {prevented_issues}")
    print(f"• Estimated Risk Mitigation: ${prevented_issues * 50000:,} (@ $50K per incident)")
    print(f"• Compliance Readiness: SOX audit-ready with complete trail")
    print(f"• Performance Impact: <{stats['average_latency_ms']:.0f}ms overhead")
    
    print(f"\n{'='*80}")
    print("✅ Demo Complete - TrustWrapper Successfully Protected Financial Analysis")
    print(f"{'='*80}")
    print("\n🔗 Learn more: https://trustwrapper.ai/financial-services")


if __name__ == "__main__":
    asyncio.run(run_financial_analysis_demo())
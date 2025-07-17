#!/usr/bin/env python3
"""
Integration tests for TrustWrapper with real Agent Forge agents
Tests the complete trust infrastructure with actual agent implementations
"""

<<<<<<< HEAD
import sys
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
=======
import pytest
import asyncio
import time
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

# Add parent directory to path
# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

<<<<<<< HEAD
from src.agents.anti_bot_evasion_manager import EvasionLevel
from src.agents.link_finder_agent import LinkFinderAgent
from src.core.trust_wrapper import VerifiedResult, ZKTrustWrapper
from src.core.trust_wrapper_quality import (
    DataQualityValidator,
    EventStructureValidator,
    QualityVerifiedWrapper,
    create_quality_wrapper,
)
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI, create_xai_wrapper
=======
from src.core.trust_wrapper import ZKTrustWrapper, VerifiedResult
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI, create_xai_wrapper
from src.core.trust_wrapper_quality import (
    QualityVerifiedWrapper, create_quality_wrapper,
    EventStructureValidator, DataQualityValidator, 
    FormatComplianceValidator
)
from src.agents.link_finder_agent import LinkFinderAgent
from src.agents.base_agent import BaseAgent, AgentTask, AgentTaskType, RegionalSession
from src.agents.anti_bot_evasion_manager import EvasionLevel
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752


class TestTrustWrapperWithLinkFinderAgent:
    """Test TrustWrapper integration with LinkFinderAgent"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.fixture
    def link_finder_agent(self):
        """Create a LinkFinderAgent instance"""
        agent = LinkFinderAgent(
            name="TestLinkFinder",
            evasion_level=EvasionLevel.BASIC,
<<<<<<< HEAD
            luma_optimization=True,
=======
            luma_optimization=True
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )
        # Mock the evasion manager
        agent.evasion_manager = AsyncMock()
        return agent
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.fixture
    def wrapped_agent(self, link_finder_agent):
        """Create a wrapped LinkFinderAgent"""
        return ZKTrustWrapper(link_finder_agent, "LinkFinderAgent")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_wrapper_preserves_agent_interface(self, wrapped_agent, link_finder_agent):
        """Test that wrapper preserves the original agent interface"""
        # Check base agent is accessible
        assert wrapped_agent.base_agent == link_finder_agent
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Check agent properties are preserved
        assert wrapped_agent.base_agent.name == "TestLinkFinder"
        assert wrapped_agent.base_agent.luma_optimization is True
        assert wrapped_agent.base_agent.evasion_level == EvasionLevel.BASIC
<<<<<<< HEAD

    def test_wrapper_execute_method(self, wrapped_agent):
        """Test synchronous execute method works with LinkFinderAgent"""
        # Mock the async run method
        wrapped_agent.base_agent.run_async = AsyncMock(
            return_value=[
                {"name": "Event 1", "url": "https://example.com/event1"},
                {"name": "Event 2", "url": "https://example.com/event2"},
            ]
        )

        # Execute through wrapper
        result = wrapped_agent.execute("https://example.com/calendar")

=======
    
    def test_wrapper_execute_method(self, wrapped_agent):
        """Test synchronous execute method works with LinkFinderAgent"""
        # Mock the async run method
        wrapped_agent.base_agent.run_async = AsyncMock(return_value=[
            {"name": "Event 1", "url": "https://example.com/event1"},
            {"name": "Event 2", "url": "https://example.com/event2"}
        ])
        
        # Execute through wrapper
        result = wrapped_agent.execute("https://example.com/calendar")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify result structure
        assert isinstance(result, VerifiedResult)
        assert result.success is True
        assert len(result.result) == 2
        assert result.metrics.agent_name == "LinkFinderAgent"
        assert result.metrics.execution_time_ms > 0
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_wrapper_async_execution(self, wrapped_agent):
        """Test async execution with real LinkFinderAgent flow"""
        # Mock browser and page for LinkFinderAgent
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Mock link elements
        mock_links = []
        for i in range(3):
            mock_link = AsyncMock()
            mock_link.get_attribute.side_effect = lambda attr, idx=i: {
                "href": f"/event-{idx}",
<<<<<<< HEAD
                "aria-label": f"Blockchain Event {idx}",
            }.get(attr)
            mock_links.append(mock_link)

        mock_page.query_selector_all.return_value = mock_links
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        wrapped_agent.base_agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )

        # Execute through wrapper
        with patch("src.agents.link_finder_agent.async_playwright"):
            result = await wrapped_agent.verified_execute_async("https://lu.ma/ethcc")

=======
                "aria-label": f"Blockchain Event {idx}"
            }.get(attr)
            mock_links.append(mock_link)
        
        mock_page.query_selector_all.return_value = mock_links
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        wrapped_agent.base_agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        
        # Execute through wrapper
        with patch('src.agents.link_finder_agent.async_playwright'):
            result = await wrapped_agent.verified_execute_async("https://lu.ma/ethcc")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify wrapped result
        assert isinstance(result, VerifiedResult)
        assert result.success is True
        assert len(result.result) == 3
<<<<<<< HEAD
        assert all(
            event["name"].startswith("Blockchain Event") for event in result.result
        )

=======
        assert all(event["name"].startswith("Blockchain Event") for event in result.result)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify proof generation
        assert result.proof is not None
        assert result.proof.agent_hash == wrapped_agent.agent_hash
        assert result.proof.success is True
        assert result.proof.execution_time > 0
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_wrapper_handles_agent_errors(self, wrapped_agent):
        """Test wrapper handles errors from the agent gracefully"""
        # Make agent raise an error
        wrapped_agent.base_agent.run_async = AsyncMock(
            side_effect=Exception("Network timeout")
        )
<<<<<<< HEAD

        # Execute should handle error
        result = await wrapped_agent.verified_execute_async("https://example.com")

=======
        
        # Execute should handle error
        result = await wrapped_agent.verified_execute_async("https://example.com")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify error handling
        assert isinstance(result, VerifiedResult)
        assert result.success is False
        assert result.result is None
        assert result.error == "Network timeout"
        assert result.proof.success is False
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_wrapper_performance_overhead(self, wrapped_agent):
        """Test that wrapper adds minimal performance overhead"""
        # Mock fast agent execution
        wrapped_agent.base_agent.run_async = AsyncMock(return_value=[])
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Measure wrapped execution
        start = time.time()
        result = wrapped_agent.execute("https://example.com")
        wrapper_time = time.time() - start
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Wrapper overhead should be minimal (< 100ms)
        assert wrapper_time < 0.1
        assert result.metrics.execution_time_ms < 100


class TestTrustWrapperXAIWithAgents:
    """Test XAI-enhanced TrustWrapper with real agents"""
<<<<<<< HEAD

    @pytest.fixture
    def mock_treasury_agent(self):
        """Create a mock treasury monitoring agent"""

        class TreasuryMonitorAgent:
            def __init__(self):
                self.name = "TreasuryMonitor"

=======
    
    @pytest.fixture
    def mock_treasury_agent(self):
        """Create a mock treasury monitoring agent"""
        class TreasuryMonitorAgent:
            def __init__(self):
                self.name = "TreasuryMonitor"
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            async def execute(self, addresses):
                # Simulate treasury monitoring
                balances = {addr: 1000.0 * (i + 1) for i, addr in enumerate(addresses)}
                alerts = []
<<<<<<< HEAD

                for addr, balance in balances.items():
                    if balance < 500:
                        alerts.append(
                            {"level": "critical", "address": addr, "balance": balance}
                        )
                    elif balance < 1000:
                        alerts.append(
                            {"level": "warning", "address": addr, "balance": balance}
                        )

=======
                
                for addr, balance in balances.items():
                    if balance < 500:
                        alerts.append({"level": "critical", "address": addr, "balance": balance})
                    elif balance < 1000:
                        alerts.append({"level": "warning", "address": addr, "balance": balance})
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                return {
                    "total_balance": sum(balances.values()),
                    "addresses": balances,
                    "alerts": alerts,
<<<<<<< HEAD
                    "timestamp": datetime.now().isoformat(),
                }

        return TreasuryMonitorAgent()

=======
                    "timestamp": datetime.now().isoformat()
                }
        
        return TreasuryMonitorAgent()
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.fixture
    def xai_wrapped_treasury_agent(self, mock_treasury_agent):
        """Create XAI-wrapped treasury agent"""
        return create_xai_wrapper(mock_treasury_agent, "TreasuryMonitor")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_xai_wrapper_provides_explanations(self, xai_wrapped_treasury_agent):
        """Test XAI wrapper provides explanations for agent decisions"""
        # Test addresses with different balances
        test_addresses = ["addr1", "addr2", "addr3"]
<<<<<<< HEAD

        result = await xai_wrapped_treasury_agent.verified_execute_async(test_addresses)

        # Verify basic execution
        assert result.success is True
        assert result.result["total_balance"] == 6000.0  # 1000 + 2000 + 3000

        # Verify XAI explanation exists
        assert hasattr(result, "explanation")
        assert result.explanation is not None

=======
        
        result = await xai_wrapped_treasury_agent.verified_execute_async(test_addresses)
        
        # Verify basic execution
        assert result.success is True
        assert result.result["total_balance"] == 6000.0  # 1000 + 2000 + 3000
        
        # Verify XAI explanation exists
        assert hasattr(result, 'explanation')
        assert result.explanation is not None
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Check explanation structure
        assert result.explanation.explanation_method in ["SHAP", "LIME", "rule-based"]
        assert 0 <= result.explanation.confidence_score <= 1
        assert isinstance(result.explanation.decision_reasoning, str)
        assert len(result.explanation.top_features) > 0
<<<<<<< HEAD

        # Verify trust score
        assert hasattr(result, "trust_score")
        assert 0 <= result.trust_score <= 1

=======
        
        # Verify trust score
        assert hasattr(result, 'trust_score')
        assert 0 <= result.trust_score <= 1
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_xai_wrapper_with_disabled_explainability(self, mock_treasury_agent):
        """Test XAI wrapper can disable explainability when needed"""
        # Create wrapper with XAI disabled
<<<<<<< HEAD
        wrapper = ZKTrustWrapperXAI(
            mock_treasury_agent, "TreasuryMonitor", enable_xai=False
        )

        result = await wrapper.verified_execute_async(["addr1"])

        # Should execute successfully
        assert result.success is True

        # But no explanation
        assert result.explanation is None

=======
        wrapper = ZKTrustWrapperXAI(mock_treasury_agent, "TreasuryMonitor", enable_xai=False)
        
        result = await wrapper.verified_execute_async(["addr1"])
        
        # Should execute successfully
        assert result.success is True
        
        # But no explanation
        assert result.explanation is None
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_xai_feature_importance_generation(self, xai_wrapped_treasury_agent):
        """Test XAI generates meaningful feature importance"""
        # Execute with specific scenario
        test_addresses = ["critical_addr", "warning_addr", "healthy_addr"]
<<<<<<< HEAD

        # Mock to control balances
        async def mock_execute(addresses):
            balances = {
                "critical_addr": 100.0,  # Will trigger critical alert
                "warning_addr": 750.0,  # Will trigger warning
                "healthy_addr": 5000.0,  # No alert
            }

            alerts = []
            for addr, balance in balances.items():
                if balance < 500:
                    alerts.append(
                        {"level": "critical", "address": addr, "balance": balance}
                    )
                elif balance < 1000:
                    alerts.append(
                        {"level": "warning", "address": addr, "balance": balance}
                    )

=======
        
        # Mock to control balances
        async def mock_execute(addresses):
            balances = {
                "critical_addr": 100.0,   # Will trigger critical alert
                "warning_addr": 750.0,    # Will trigger warning
                "healthy_addr": 5000.0    # No alert
            }
            
            alerts = []
            for addr, balance in balances.items():
                if balance < 500:
                    alerts.append({"level": "critical", "address": addr, "balance": balance})
                elif balance < 1000:
                    alerts.append({"level": "warning", "address": addr, "balance": balance})
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            return {
                "total_balance": sum(balances.values()),
                "addresses": balances,
                "alerts": alerts,
<<<<<<< HEAD
                "alert_count": len(alerts),
            }

        xai_wrapped_treasury_agent.base_agent.execute = mock_execute

        result = await xai_wrapped_treasury_agent.verified_execute_async(test_addresses)

        # Check feature importance includes relevant features
        feature_names = [f["feature_name"] for f in result.explanation.top_features]

=======
                "alert_count": len(alerts)
            }
        
        xai_wrapped_treasury_agent.base_agent.execute = mock_execute
        
        result = await xai_wrapped_treasury_agent.verified_execute_async(test_addresses)
        
        # Check feature importance includes relevant features
        feature_names = [f["feature_name"] for f in result.explanation.top_features]
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Should identify important features
        assert any("balance" in name.lower() for name in feature_names)
        assert any("alert" in name.lower() for name in feature_names)


class TestQualityConsensusWithAgents:
    """Test Quality Consensus wrapper with real agents"""
<<<<<<< HEAD

    @pytest.fixture
    def mock_event_extractor_agent(self):
        """Create a mock event extraction agent"""

        class EventExtractorAgent:
            def __init__(self):
                self.name = "EventExtractor"

=======
    
    @pytest.fixture
    def mock_event_extractor_agent(self):
        """Create a mock event extraction agent"""
        class EventExtractorAgent:
            def __init__(self):
                self.name = "EventExtractor"
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            def execute(self, url):
                # Simulate event extraction with varying quality
                if "high-quality" in url:
                    return {
                        "events": [
                            {
                                "name": "Blockchain Summit 2025",
                                "date": "2025-07-15",
                                "location": "Berlin, Germany",
                                "description": "Annual blockchain technology summit",
<<<<<<< HEAD
                                "organizers": [
                                    "Web3 Foundation",
                                    "Ethereum Foundation",
                                ],
                                "attendees": 500,
                                "tags": ["blockchain", "web3", "defi"],
                            }
                        ],
                        "source": url,
                        "extracted_at": datetime.now().isoformat(),
=======
                                "organizers": ["Web3 Foundation", "Ethereum Foundation"],
                                "attendees": 500,
                                "tags": ["blockchain", "web3", "defi"]
                            }
                        ],
                        "source": url,
                        "extracted_at": datetime.now().isoformat()
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                    }
                elif "medium-quality" in url:
                    return {
                        "events": [
                            {
                                "name": "Crypto Meetup",
                                "date": "July 2025",  # Missing specific date
                                "location": "Berlin",  # Missing country
<<<<<<< HEAD
                                "attendees": "500+",  # String instead of number
                            }
                        ],
                        "source": url,
                    }
                else:  # low quality
                    return {"events": [{"name": "Some Event"}]}  # Missing most fields

        return EventExtractorAgent()

=======
                                "attendees": "500+"   # String instead of number
                            }
                        ],
                        "source": url
                    }
                else:  # low quality
                    return {
                        "events": [
                            {"name": "Some Event"}  # Missing most fields
                        ]
                    }
        
        return EventExtractorAgent()
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.fixture
    def quality_wrapped_agent(self, mock_event_extractor_agent):
        """Create quality consensus wrapped agent"""
        return create_quality_wrapper(mock_event_extractor_agent, "EventExtractor")
<<<<<<< HEAD

    def test_quality_consensus_high_quality_data(self, quality_wrapped_agent):
        """Test quality consensus with high-quality data"""
        result = quality_wrapped_agent.execute("https://high-quality.com/events")

=======
    
    def test_quality_consensus_high_quality_data(self, quality_wrapped_agent):
        """Test quality consensus with high-quality data"""
        result = quality_wrapped_agent.execute("https://high-quality.com/events")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Should pass quality checks
        assert result.success is True
        assert result.quality_verified is True
        assert result.consensus_score > 0.8
<<<<<<< HEAD

        # Check validator results
        assert len(result.validator_results) == 3

=======
        
        # Check validator results
        assert len(result.validator_results) == 3
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # All validators should pass for high-quality data
        for validator_result in result.validator_results.values():
            assert validator_result["passed"] is True
            assert validator_result["confidence"] > 0.8
<<<<<<< HEAD

    def test_quality_consensus_medium_quality_data(self, quality_wrapped_agent):
        """Test quality consensus with medium-quality data"""
        result = quality_wrapped_agent.execute("https://medium-quality.com/events")

=======
    
    def test_quality_consensus_medium_quality_data(self, quality_wrapped_agent):
        """Test quality consensus with medium-quality data"""
        result = quality_wrapped_agent.execute("https://medium-quality.com/events")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Should have mixed results
        assert result.success is True
        assert result.consensus_score > 0.4
        assert result.consensus_score < 0.8
<<<<<<< HEAD

        # Some validators should flag issues
        failed_count = sum(
            1 for v in result.validator_results.values() if not v["passed"]
        )
        assert failed_count >= 1

    def test_quality_consensus_low_quality_data(self, quality_wrapped_agent):
        """Test quality consensus with low-quality data"""
        result = quality_wrapped_agent.execute("https://low-quality.com/events")

=======
        
        # Some validators should flag issues
        failed_count = sum(
            1 for v in result.validator_results.values() 
            if not v["passed"]
        )
        assert failed_count >= 1
    
    def test_quality_consensus_low_quality_data(self, quality_wrapped_agent):
        """Test quality consensus with low-quality data"""
        result = quality_wrapped_agent.execute("https://low-quality.com/events")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Should fail quality checks
        assert result.success is True  # Execution succeeds
        assert result.quality_verified is False  # But quality fails
        assert result.consensus_score < 0.5
<<<<<<< HEAD

        # Most validators should fail
        failed_count = sum(
            1 for v in result.validator_results.values() if not v["passed"]
        )
        assert failed_count >= 2

    def test_quality_consensus_custom_validators(self, mock_event_extractor_agent):
        """Test adding custom validators to quality consensus"""

=======
        
        # Most validators should fail
        failed_count = sum(
            1 for v in result.validator_results.values() 
            if not v["passed"]
        )
        assert failed_count >= 2
    
    def test_quality_consensus_custom_validators(self, mock_event_extractor_agent):
        """Test adding custom validators to quality consensus"""
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Create custom validator
        class LocationValidator:
            def validate(self, data):
                events = data.get("events", [])
                if not events:
                    return False, 0.0, ["No events found"]
<<<<<<< HEAD

=======
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                issues = []
                for event in events:
                    location = event.get("location", "")
                    if not location:
                        issues.append("Missing location")
                    elif "," not in location:
                        issues.append("Location missing country")
<<<<<<< HEAD

                passed = len(issues) == 0
                confidence = 1.0 - (len(issues) / len(events))

                return passed, confidence, issues

=======
                
                passed = len(issues) == 0
                confidence = 1.0 - (len(issues) / len(events))
                
                return passed, confidence, issues
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Create wrapper with custom validator
        wrapper = QualityVerifiedWrapper(
            base_agent=mock_event_extractor_agent,
            agent_name="EventExtractor",
<<<<<<< HEAD
            validators=[EventStructureValidator(), LocationValidator()],
        )

        # Test with data missing proper location
        result = wrapper.execute("https://medium-quality.com/events")

=======
            validators=[
                EventStructureValidator(),
                LocationValidator()
            ]
        )
        
        # Test with data missing proper location
        result = wrapper.execute("https://medium-quality.com/events")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Custom validator should be included
        assert len(result.validator_results) == 2
        assert any("Location" in name for name in result.validator_results.keys())


class TestFullStackIntegration:
    """Test complete trust stack: Base + XAI + Quality"""
<<<<<<< HEAD

    @pytest.fixture
    def mock_complex_agent(self):
        """Create a complex agent for full stack testing"""

        class ComplexAnalysisAgent:
            def __init__(self):
                self.name = "ComplexAnalyzer"

            def execute(self, data):
                # Simulate complex analysis
                analysis = {
                    "sentiment": (
                        "positive" if data.get("positive_words", 0) > 5 else "negative"
                    ),
                    "risk_score": min(data.get("risk_factors", 0) * 0.1, 1.0),
                    "opportunities": data.get("opportunities", []),
                    "recommendations": [],
                    "confidence": 0.85,
                }

                # Generate recommendations based on analysis
                if analysis["risk_score"] < 0.3:
                    analysis["recommendations"].append(
                        "Low risk - proceed with investment"
                    )
                elif analysis["risk_score"] < 0.7:
                    analysis["recommendations"].append(
                        "Medium risk - conduct further analysis"
                    )
                else:
                    analysis["recommendations"].append(
                        "High risk - avoid or hedge position"
                    )

                return analysis

        return ComplexAnalysisAgent()

=======
    
    @pytest.fixture
    def mock_complex_agent(self):
        """Create a complex agent for full stack testing"""
        class ComplexAnalysisAgent:
            def __init__(self):
                self.name = "ComplexAnalyzer"
            
            def execute(self, data):
                # Simulate complex analysis
                analysis = {
                    "sentiment": "positive" if data.get("positive_words", 0) > 5 else "negative",
                    "risk_score": min(data.get("risk_factors", 0) * 0.1, 1.0),
                    "opportunities": data.get("opportunities", []),
                    "recommendations": [],
                    "confidence": 0.85
                }
                
                # Generate recommendations based on analysis
                if analysis["risk_score"] < 0.3:
                    analysis["recommendations"].append("Low risk - proceed with investment")
                elif analysis["risk_score"] < 0.7:
                    analysis["recommendations"].append("Medium risk - conduct further analysis")
                else:
                    analysis["recommendations"].append("High risk - avoid or hedge position")
                
                return analysis
        
        return ComplexAnalysisAgent()
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_full_trust_stack(self, mock_complex_agent):
        """Test all three trust layers working together"""
        # Layer 1: Basic wrapper
        basic_wrapper = ZKTrustWrapper(mock_complex_agent, "ComplexAnalyzer")
<<<<<<< HEAD

        # Layer 2: Add XAI
        xai_wrapper = ZKTrustWrapperXAI(basic_wrapper, "ComplexAnalyzer-XAI")

        # Layer 3: Add Quality Consensus
        quality_wrapper = QualityVerifiedWrapper(
            xai_wrapper, "ComplexAnalyzer-Full", validators=[DataQualityValidator()]
        )

=======
        
        # Layer 2: Add XAI
        xai_wrapper = ZKTrustWrapperXAI(basic_wrapper, "ComplexAnalyzer-XAI")
        
        # Layer 3: Add Quality Consensus
        quality_wrapper = QualityVerifiedWrapper(
            xai_wrapper, 
            "ComplexAnalyzer-Full",
            validators=[DataQualityValidator()]
        )
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Test with sample data
        test_data = {
            "positive_words": 10,
            "risk_factors": 3,
<<<<<<< HEAD
            "opportunities": ["DeFi growth", "Institutional adoption"],
        }

        result = quality_wrapper.execute(test_data)

        # Verify all layers executed
        assert result.success is True

        # Check basic metrics (Layer 1)
        assert result.metrics.execution_time_ms > 0
        assert result.proof is not None

        # Check XAI explanation (Layer 2)
        # Note: XAI explanation would be on the inner result

        # Check quality consensus (Layer 3)
        assert hasattr(result, "quality_verified")
        assert hasattr(result, "consensus_score")
        assert len(result.validator_results) > 0

=======
            "opportunities": ["DeFi growth", "Institutional adoption"]
        }
        
        result = quality_wrapper.execute(test_data)
        
        # Verify all layers executed
        assert result.success is True
        
        # Check basic metrics (Layer 1)
        assert result.metrics.execution_time_ms > 0
        assert result.proof is not None
        
        # Check XAI explanation (Layer 2)
        # Note: XAI explanation would be on the inner result
        
        # Check quality consensus (Layer 3)
        assert hasattr(result, 'quality_verified')
        assert hasattr(result, 'consensus_score')
        assert len(result.validator_results) > 0
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_async_full_stack_performance(self, mock_complex_agent):
        """Test async performance with full trust stack"""
        # Create full stack
        wrapper = create_quality_wrapper(
<<<<<<< HEAD
            create_xai_wrapper(mock_complex_agent, "Complex"), "ComplexFull"
        )

=======
            create_xai_wrapper(mock_complex_agent, "Complex"),
            "ComplexFull"
        )
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Make agent async
        mock_complex_agent.execute = AsyncMock(
            return_value={"analysis": "complete", "score": 0.95}
        )
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Measure full stack execution time
        start = time.time()
        result = await wrapper.verified_execute_async({"test": "data"})
        total_time = time.time() - start
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Should complete reasonably fast even with all layers
        assert total_time < 1.0  # Less than 1 second
        assert result.success is True


if __name__ == "__main__":
<<<<<<< HEAD
    pytest.main([__file__, "-v", "--tb=short"])
=======
    pytest.main([__file__, "-v", "--tb=short"])
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

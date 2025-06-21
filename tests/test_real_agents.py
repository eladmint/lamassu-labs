#!/usr/bin/env python3
"""
Test suite for real Agent Forge agents with TrustWrapper
Tests integration with actual agent implementations
"""

import pytest
import asyncio
import time
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.trust_wrapper import ZKTrustWrapper, VerifiedResult


class TestRealAgentIntegration:
    """Test TrustWrapper with real Agent Forge agents"""
    
    @pytest.mark.integration
    def test_link_finder_agent_wrapping(self):
        """Test wrapping LinkFinderAgent from Agent Forge"""
        # Mock LinkFinderAgent since we're in Lamassu Labs context
        class MockLinkFinderAgent:
            def __init__(self):
                self.name = "link_finder_agent"
                
            def execute(self, url):
                """Mock event extraction"""
                time.sleep(0.1)  # Simulate network delay
                
                if "ethcc" in url.lower():
                    return {
                        "events": [
                            {
                                "name": "EthCC Paris 2025",
                                "date": "2025-07-08",
                                "location": "Paris, France",
                                "url": "https://ethcc.io"
                            },
                            {
                                "name": "EthCC Hackathon",
                                "date": "2025-07-06",
                                "location": "Paris, France",
                                "url": "https://ethcc.io/hackathon"
                            }
                        ],
                        "extraction_method": "calendar",
                        "confidence": 0.95
                    }
                return {"events": [], "error": "No events found"}
        
        # Create and wrap agent
        agent = MockLinkFinderAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Test execution
        result = wrapper.verified_execute("https://ethcc.io")
        
        # Verify results
        assert result.verified is True
        assert result.proof.success is True
        assert result.proof.execution_time >= 100  # At least 100ms
        assert len(result.result["events"]) == 2
        assert result.result["confidence"] == 0.95
        
        # Verify proof contains agent identity
        assert len(result.proof.agent_hash) == 64  # SHA256 hash
    
    @pytest.mark.integration
    def test_scraper_agent_with_browser(self):
        """Test wrapping a browser-based scraper agent"""
        class MockScraperAgent:
            def __init__(self):
                self.name = "enhanced_scraper"
                self.browser_enabled = True
                
            async def execute(self, config):
                """Mock browser scraping"""
                await asyncio.sleep(0.2)  # Simulate browser operations
                
                return {
                    "scraped_content": {
                        "title": "Web3 Conference 2025",
                        "description": "The premier Web3 event",
                        "speakers": ["Vitalik", "Gavin", "Juan"],
                        "sponsors": ["Protocol Labs", "Ethereum Foundation"]
                    },
                    "metadata": {
                        "scrape_time": 0.2,
                        "javascript_rendered": True,
                        "captcha_solved": False
                    }
                }
        
        # Create async wrapper
        agent = MockScraperAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Test async execution
        async def test_async():
            result = await wrapper.verified_execute_async({
                "url": "https://web3conf.com",
                "wait_for_js": True
            })
            
            assert result.verified is True
            assert result.proof.success is True
            assert result.proof.execution_time >= 200  # At least 200ms
            assert result.result["metadata"]["javascript_rendered"] is True
            assert len(result.result["scraped_content"]["speakers"]) == 3
        
        # Run async test
        asyncio.run(test_async())
    
    @pytest.mark.integration
    def test_treasury_monitor_agent(self):
        """Test wrapping Cardano Treasury Monitor agent"""
        class MockTreasuryMonitor:
            def __init__(self):
                self.name = "cardano_treasury_monitor"
                self.addresses = []
                
            def execute(self, addresses):
                """Mock treasury monitoring"""
                self.addresses = addresses
                
                # Simulate blockchain queries
                time.sleep(0.05 * len(addresses))
                
                return {
                    "treasury_status": {
                        "total_balance": 64269.55,  # ADA
                        "addresses_monitored": len(addresses),
                        "last_block": 9876543,
                        "epoch": 425
                    },
                    "alerts": [
                        {
                            "level": "info",
                            "message": "Large transaction detected",
                            "amount": 10000,
                            "address": addresses[0] if addresses else None
                        }
                    ] if len(addresses) > 2 else [],
                    "performance": {
                        "query_time": 0.05 * len(addresses),
                        "api_calls": len(addresses)
                    }
                }
        
        # Create and wrap
        agent = MockTreasuryMonitor()
        wrapper = ZKTrustWrapper(agent)
        
        # Test with multiple addresses
        test_addresses = [
            "addr1qx1234...",
            "addr1qy5678...",
            "addr1qz9012..."
        ]
        
        result = wrapper.verified_execute(test_addresses)
        
        # Verify execution
        assert result.verified is True
        assert result.proof.success is True
        assert result.result["treasury_status"]["total_balance"] == 64269.55
        assert len(result.result["alerts"]) == 1  # 3 addresses triggers alert
        assert result.proof.execution_time >= 150  # 50ms per address
    
    @pytest.mark.integration 
    def test_ai_analysis_agent(self):
        """Test wrapping an AI-powered analysis agent"""
        class MockAIAnalysisAgent:
            def __init__(self):
                self.name = "ai_event_analyzer"
                self.model = "gpt-4"
                
            def execute(self, event_data):
                """Mock AI analysis"""
                time.sleep(0.3)  # Simulate AI processing
                
                return {
                    "analysis": {
                        "quality_score": 0.92,
                        "legitimacy": 0.98,
                        "relevance": 0.87,
                        "insights": [
                            "High-profile speakers confirmed",
                            "Venue capacity matches expected attendance",
                            "Sponsor list includes major protocols"
                        ]
                    },
                    "recommendations": {
                        "attend": True,
                        "priority": "high",
                        "networking_opportunities": "excellent"
                    },
                    "metadata": {
                        "model_used": self.model,
                        "confidence": 0.91,
                        "processing_time": 0.3
                    }
                }
        
        agent = MockAIAnalysisAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Test with event data
        event_data = {
            "name": "DeFi Summit 2025",
            "speakers": ["Andre Cronje", "Stani Kulechov"],
            "topics": ["Yield Farming", "Flash Loans", "MEV"]
        }
        
        result = wrapper.verified_execute(event_data)
        
        # Verify AI analysis was wrapped properly
        assert result.verified is True
        assert result.proof.success is True
        assert result.proof.execution_time >= 300  # AI takes time
        assert result.result["analysis"]["quality_score"] == 0.92
        assert result.result["metadata"]["model_used"] == "gpt-4"
        assert len(result.result["analysis"]["insights"]) == 3
    
    @pytest.mark.integration
    def test_multi_agent_pipeline(self):
        """Test wrapping a multi-agent pipeline"""
        class ExtractAgent:
            def execute(self, url):
                return {"raw_data": f"Data from {url}"}
        
        class EnrichAgent:
            def execute(self, raw_data):
                return {"enriched": raw_data["raw_data"] + " [enriched]"}
        
        class ValidateAgent:
            def execute(self, enriched_data):
                return {"valid": True, "data": enriched_data}
        
        # Create pipeline of wrapped agents
        extract_wrapped = ZKTrustWrapper(ExtractAgent())
        enrich_wrapped = ZKTrustWrapper(EnrichAgent())
        validate_wrapped = ZKTrustWrapper(ValidateAgent())
        
        # Execute pipeline
        url = "https://example.com"
        
        # Step 1: Extract
        extract_result = extract_wrapped.verified_execute(url)
        assert extract_result.verified is True
        
        # Step 2: Enrich
        enrich_result = enrich_wrapped.verified_execute(extract_result.result)
        assert enrich_result.verified is True
        
        # Step 3: Validate
        validate_result = validate_wrapped.verified_execute(enrich_result.result)
        assert validate_result.verified is True
        assert validate_result.result["valid"] is True
        
        # Each agent has unique hash
        hashes = [
            extract_result.proof.agent_hash,
            enrich_result.proof.agent_hash,
            validate_result.proof.agent_hash
        ]
        assert len(set(hashes)) == 3  # All unique
    
    @pytest.mark.performance
    def test_high_frequency_agent(self):
        """Test wrapper performance with high-frequency agent"""
        class HighFrequencyAgent:
            def __init__(self):
                self.execution_count = 0
                
            def execute(self):
                self.execution_count += 1
                return {"count": self.execution_count, "timestamp": time.time()}
        
        agent = HighFrequencyAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Execute many times rapidly
        start_time = time.time()
        results = []
        
        for _ in range(100):
            result = wrapper.verified_execute()
            results.append(result)
        
        duration = time.time() - start_time
        
        # Verify performance
        assert all(r.verified for r in results)
        assert all(r.proof.success for r in results)
        assert duration < 1.0  # 100 executions in under 1 second
        
        # Verify execution count
        assert results[-1].result["count"] == 100
        
        # Calculate average overhead
        avg_execution_time = sum(r.proof.execution_time for r in results) / 100
        assert avg_execution_time < 10  # Less than 10ms average


class TestAgentEdgeCases:
    """Test edge cases with various agent implementations"""
    
    def test_agent_with_complex_state(self):
        """Test agent with complex internal state"""
        class StatefulAgent:
            def __init__(self):
                self.state = {
                    "cache": {},
                    "history": [],
                    "config": {"mode": "production"}
                }
                
            def execute(self, key, value):
                self.state["cache"][key] = value
                self.state["history"].append((key, value))
                return {
                    "stored": True,
                    "cache_size": len(self.state["cache"]),
                    "history_length": len(self.state["history"])
                }
        
        agent = StatefulAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Multiple executions
        for i in range(5):
            result = wrapper.verified_execute(f"key{i}", f"value{i}")
            assert result.verified is True
            assert result.result["cache_size"] == i + 1
            assert result.result["history_length"] == i + 1
    
    def test_agent_with_external_dependencies(self):
        """Test agent that would have external dependencies"""
        class ExternalDependentAgent:
            def __init__(self):
                self.api_client = Mock()  # Mock external API
                self.database = Mock()    # Mock database
                
            def execute(self, query):
                # Mock external calls
                self.api_client.fetch.return_value = {"data": "api_response"}
                self.database.query.return_value = [{"id": 1}, {"id": 2}]
                
                api_data = self.api_client.fetch(query)
                db_data = self.database.query(query)
                
                return {
                    "api_response": api_data,
                    "db_records": len(db_data),
                    "combined": True
                }
        
        agent = ExternalDependentAgent()
        wrapper = ZKTrustWrapper(agent)
        
        result = wrapper.verified_execute("test_query")
        
        assert result.verified is True
        assert result.proof.success is True
        assert result.result["db_records"] == 2
        assert result.result["api_response"]["data"] == "api_response"
    
    def test_agent_error_recovery(self):
        """Test agent with error recovery mechanisms"""
        class ResilientAgent:
            def __init__(self):
                self.attempt_count = 0
                self.max_retries = 3
                
            def execute(self, should_fail_times=0):
                self.attempt_count += 1
                
                if self.attempt_count <= should_fail_times:
                    raise Exception(f"Temporary failure {self.attempt_count}")
                
                return {
                    "success": True,
                    "attempts": self.attempt_count,
                    "recovered": self.attempt_count > 1
                }
        
        agent = ResilientAgent()
        wrapper = ZKTrustWrapper(agent)
        
        # Test successful execution
        result = wrapper.verified_execute(should_fail_times=0)
        assert result.verified is True
        assert result.proof.success is True
        
        # Test with failures (wrapper captures the exception)
        agent.attempt_count = 0
        result = wrapper.verified_execute(should_fail_times=2)
        assert result.verified is True
        assert result.proof.success is False  # Agent failed


class TestRealWorldScenarios:
    """Test real-world usage scenarios"""
    
    @pytest.mark.integration
    def test_hackathon_submission_verification(self):
        """Test verifying a hackathon submission agent"""
        class HackathonAgent:
            def __init__(self, team_name, project_name):
                self.team_name = team_name
                self.project_name = project_name
                
            def execute(self, submission_data):
                """Process hackathon submission"""
                time.sleep(0.1)  # Simulate processing
                
                return {
                    "submission": {
                        "team": self.team_name,
                        "project": self.project_name,
                        "timestamp": time.time(),
                        "data": submission_data
                    },
                    "validation": {
                        "code_quality": 0.89,
                        "innovation": 0.95,
                        "completeness": 0.92
                    },
                    "verified": True
                }
        
        # Create team's agent
        agent = HackathonAgent("Lamassu Labs", "TrustWrapper")
        wrapper = ZKTrustWrapper(agent)
        
        # Submit project
        submission = {
            "github_url": "https://github.com/lamassu-labs/trustwrapper",
            "demo_url": "https://demo.trustwrapper.io",
            "video_url": "https://youtube.com/trustwrapper-demo"
        }
        
        result = wrapper.verified_execute(submission)
        
        # Hackathon judges can verify
        assert result.verified is True
        assert result.proof.success is True
        assert result.result["submission"]["team"] == "Lamassu Labs"
        assert result.result["validation"]["innovation"] == 0.95
        
        # Proof provides trust without revealing implementation
        assert isinstance(result.proof.agent_hash, str)
        assert result.proof.timestamp > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
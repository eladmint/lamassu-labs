#!/usr/bin/env python3
"""
Integration tests for multi-agent coordination and pipeline
Tests how agents work together in real-world scenarios
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.agents.base_agent import (
    BaseAgent, AgentTask, AgentResult, AgentTaskType,
    RegionalSession, PerformanceMonitor
)
from src.agents.link_finder_agent import LinkFinderAgent
from src.agents.anti_bot_evasion_manager import AntiBotEvasionManager, EvasionLevel
from src.agents.region_manager import RegionManager


class MockDataExtractorAgent(BaseAgent):
    """Mock agent that extracts data from discovered links"""
    
    async def _execute_core_logic(self, task: AgentTask, session: RegionalSession) -> AgentResult:
        """Extract detailed data from a link"""
        # Simulate data extraction
        event_data = {
            "title": f"Event from {task.target_url}",
            "date": "2025-06-22",
            "location": "Berlin",
            "description": "Extracted event details",
            "attendees": 150
        }
        
        return AgentResult(
            task_id=task.task_id,
            success=True,
            data={"event_details": event_data},
            performance_metrics={},
            region_used=session.region,
            execution_time=0.5
        )


class MockDataEnricherAgent(BaseAgent):
    """Mock agent that enriches extracted data"""
    
    async def _execute_core_logic(self, task: AgentTask, session: RegionalSession) -> AgentResult:
        """Enrich data with additional information"""
        input_data = task.metadata.get("input_data", {})
        
        # Simulate enrichment
        enriched_data = {
            **input_data,
            "category": "Technology",
            "tags": ["blockchain", "web3", "crypto"],
            "quality_score": 0.85,
            "enriched_at": datetime.now().isoformat()
        }
        
        return AgentResult(
            task_id=task.task_id,
            success=True,
            data={"enriched_event": enriched_data},
            performance_metrics={},
            region_used=session.region,
            execution_time=0.3
        )


class TestAgentPipelineIntegration:
    """Test multi-agent coordination in pipeline scenarios"""
    
    @pytest.fixture
    async def mock_region_manager(self):
        """Create a mock region manager"""
        manager = AsyncMock(spec=RegionManager)
        
        # Mock methods
        manager.get_optimal_region.return_value = "us-east"
        manager.get_regional_session.return_value = RegionalSession(
            region="us-east",
            session_id="test_session",
            browser_context=AsyncMock(),
            http_session=AsyncMock(),
            created_at=datetime.now(),
            last_used=datetime.now(),
            request_count=0,
            rate_limit_remaining=100,
            is_active=True
        )
        manager.update_regional_metrics = AsyncMock()
        
        return manager
    
    @pytest.fixture
    def link_finder_agent(self):
        """Create a LinkFinderAgent with mocked evasion"""
        agent = LinkFinderAgent(
            name="PipelineLinkFinder",
            evasion_level=EvasionLevel.STANDARD
        )
        
        # Mock the evasion manager
        agent.evasion_manager = AsyncMock()
        
        return agent
    
    @pytest.fixture
    async def data_extractor_agent(self, mock_region_manager):
        """Create a data extractor agent"""
        return MockDataExtractorAgent(mock_region_manager)
    
    @pytest.fixture
    async def data_enricher_agent(self, mock_region_manager):
        """Create a data enricher agent"""
        return MockDataEnricherAgent(mock_region_manager)
    
    @pytest.mark.asyncio
    async def test_three_stage_pipeline(self, link_finder_agent, data_extractor_agent, data_enricher_agent):
        """Test a complete 3-stage agent pipeline: discover -> extract -> enrich"""
        
        # Stage 1: Link Discovery
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        
        # Mock discovered links
        mock_links = []
        for i in range(3):
            mock_link = AsyncMock()
            mock_link.get_attribute.side_effect = lambda attr, idx=i: {
                "href": f"/event-{idx}",
                "aria-label": f"Test Event {idx}"
            }.get(attr)
            mock_links.append(mock_link)
        
        mock_page.query_selector_all.return_value = mock_links
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        link_finder_agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        
        # Execute Stage 1
        with patch('src.agents.link_finder_agent.async_playwright'):
            discovered_links = await link_finder_agent.run_async("https://example.com/events")
        
        assert len(discovered_links) == 3
        
        # Stage 2: Data Extraction for each link
        extraction_results = []
        for link_data in discovered_links:
            task = AgentTask(
                task_id=f"extract_{link_data['url']}",
                task_type=AgentTaskType.EXTRACT_TEXT,
                target_url=link_data['url'],
                metadata={"link_name": link_data['name']}
            )
            
            result = await data_extractor_agent.execute_with_rotation(task)
            extraction_results.append(result)
        
        assert len(extraction_results) == 3
        assert all(r.success for r in extraction_results)
        
        # Stage 3: Data Enrichment for each extracted event
        enrichment_results = []
        for extract_result in extraction_results:
            task = AgentTask(
                task_id=f"enrich_{extract_result.task_id}",
                task_type=AgentTaskType.ANALYZE_ORGANIZER,
                target_url="",  # Not needed for enrichment
                metadata={"input_data": extract_result.data["event_details"]}
            )
            
            result = await data_enricher_agent.execute_with_rotation(task)
            enrichment_results.append(result)
        
        assert len(enrichment_results) == 3
        assert all(r.success for r in enrichment_results)
        
        # Verify pipeline output
        for result in enrichment_results:
            enriched_event = result.data["enriched_event"]
            assert "title" in enriched_event
            assert "category" in enriched_event
            assert "tags" in enriched_event
            assert enriched_event["quality_score"] == 0.85
    
    @pytest.mark.asyncio
    async def test_pipeline_error_handling(self, link_finder_agent, data_extractor_agent, data_enricher_agent):
        """Test pipeline handles errors gracefully"""
        
        # Stage 1: Link discovery fails
        link_finder_agent.evasion_manager.create_evasion_session = AsyncMock(
            side_effect=Exception("Network error")
        )
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            discovered_links = await link_finder_agent.run_async("https://example.com/events")
        
        assert discovered_links == []  # Should return empty list on error
        
        # Pipeline should handle empty input gracefully
        extraction_results = []
        for link_data in discovered_links:
            # This loop won't execute
            task = AgentTask(
                task_id=f"extract_{link_data['url']}",
                task_type=AgentTaskType.EXTRACT_TEXT,
                target_url=link_data['url'],
                metadata={}
            )
            result = await data_extractor_agent.execute_with_rotation(task)
            extraction_results.append(result)
        
        assert len(extraction_results) == 0
    
    @pytest.mark.asyncio
    async def test_pipeline_with_partial_failures(self, mock_region_manager):
        """Test pipeline continues when some agents fail"""
        
        # Create agents with controlled failure
        class FailingExtractorAgent(BaseAgent):
            def __init__(self, region_manager, fail_on_task_ids):
                super().__init__(region_manager)
                self.fail_on_task_ids = fail_on_task_ids
            
            async def _execute_core_logic(self, task: AgentTask, session: RegionalSession) -> AgentResult:
                if task.task_id in self.fail_on_task_ids:
                    raise Exception("Simulated extraction failure")
                
                return AgentResult(
                    task_id=task.task_id,
                    success=True,
                    data={"extracted": "data"},
                    performance_metrics={},
                    region_used=session.region,
                    execution_time=0.1
                )
        
        # Create extractor that fails on second task
        extractor = FailingExtractorAgent(mock_region_manager, ["extract_1"])
        enricher = MockDataEnricherAgent(mock_region_manager)
        
        # Process 3 tasks
        extraction_results = []
        for i in range(3):
            task = AgentTask(
                task_id=f"extract_{i}",
                task_type=AgentTaskType.EXTRACT_TEXT,
                target_url=f"https://example.com/event-{i}",
                metadata={}
            )
            
            result = await extractor.execute_with_rotation(task)
            extraction_results.append(result)
        
        # Check that one failed
        success_count = sum(1 for r in extraction_results if r.success)
        assert success_count == 2
        assert not extraction_results[1].success
        
        # Enrichment should only process successful extractions
        enrichment_results = []
        for extract_result in extraction_results:
            if extract_result.success:
                task = AgentTask(
                    task_id=f"enrich_{extract_result.task_id}",
                    task_type=AgentTaskType.ANALYZE_ORGANIZER,
                    target_url="",
                    metadata={"input_data": extract_result.data}
                )
                
                result = await enricher.execute_with_rotation(task)
                enrichment_results.append(result)
        
        assert len(enrichment_results) == 2  # Only successful extractions enriched
    
    @pytest.mark.asyncio
    async def test_pipeline_performance_monitoring(self, mock_region_manager):
        """Test performance monitoring across pipeline stages"""
        
        # Create agents
        extractor = MockDataExtractorAgent(mock_region_manager)
        enricher = MockDataEnricherAgent(mock_region_manager)
        
        # Track overall pipeline timing
        pipeline_start = asyncio.get_event_loop().time()
        
        # Stage 1: Extraction
        extraction_task = AgentTask(
            task_id="perf_extract",
            task_type=AgentTaskType.EXTRACT_TEXT,
            target_url="https://example.com/event",
            metadata={}
        )
        
        extract_result = await extractor.execute_with_rotation(extraction_task)
        
        # Stage 2: Enrichment
        enrichment_task = AgentTask(
            task_id="perf_enrich",
            task_type=AgentTaskType.ANALYZE_ORGANIZER,
            target_url="",
            metadata={"input_data": extract_result.data}
        )
        
        enrich_result = await enricher.execute_with_rotation(enrichment_task)
        
        pipeline_end = asyncio.get_event_loop().time()
        pipeline_duration = pipeline_end - pipeline_start
        
        # Verify performance metrics
        assert extract_result.execution_time > 0
        assert enrich_result.execution_time > 0
        assert pipeline_duration >= (extract_result.execution_time + enrich_result.execution_time)
        
        # Check performance monitoring data
        assert "performance_metrics" in extract_result.__dict__
        assert "performance_metrics" in enrich_result.__dict__
    
    @pytest.mark.asyncio
    async def test_pipeline_regional_distribution(self, mock_region_manager):
        """Test pipeline distributes load across regions"""
        
        # Configure region manager to rotate regions
        regions = ["us-east", "eu-west", "asia-pac"]
        region_index = 0
        
        def get_next_region(task):
            nonlocal region_index
            region = regions[region_index % len(regions)]
            region_index += 1
            return region
        
        mock_region_manager.get_optimal_region.side_effect = get_next_region
        
        # Create multiple sessions for different regions
        def get_session_for_region(region):
            return RegionalSession(
                region=region,
                session_id=f"session_{region}",
                browser_context=AsyncMock(),
                http_session=AsyncMock(),
                created_at=datetime.now(),
                last_used=datetime.now(),
                request_count=0,
                rate_limit_remaining=100,
                is_active=True
            )
        
        mock_region_manager.get_regional_session.side_effect = get_session_for_region
        
        # Create agents
        extractor = MockDataExtractorAgent(mock_region_manager)
        
        # Execute multiple tasks
        results = []
        for i in range(6):  # Execute 6 tasks
            task = AgentTask(
                task_id=f"regional_task_{i}",
                task_type=AgentTaskType.EXTRACT_TEXT,
                target_url=f"https://example.com/event-{i}",
                metadata={}
            )
            
            result = await extractor.execute_with_rotation(task)
            results.append(result)
        
        # Verify regional distribution
        used_regions = [r.region_used for r in results]
        assert "us-east" in used_regions
        assert "eu-west" in used_regions
        assert "asia-pac" in used_regions
        
        # Each region should be used twice (6 tasks / 3 regions)
        assert used_regions.count("us-east") == 2
        assert used_regions.count("eu-west") == 2
        assert used_regions.count("asia-pac") == 2
    
    @pytest.mark.asyncio
    async def test_pipeline_anti_bot_coordination(self, link_finder_agent):
        """Test anti-bot evasion coordination across pipeline"""
        
        # Track evasion levels used
        evasion_levels_used = []
        
        # Mock evasion manager to track calls
        original_create_session = link_finder_agent.evasion_manager.create_evasive_session
        
        async def track_evasion_session(url, evasion_level):
            evasion_levels_used.append(evasion_level)
            return AsyncMock()  # Return mock browser
        
        link_finder_agent.evasion_manager.create_evasive_session = track_evasion_session
        
        # Execute with different evasion levels
        link_finder_agent.evasion_level = EvasionLevel.BASIC
        with patch('src.agents.link_finder_agent.async_playwright'):
            await link_finder_agent.run_async("https://easy-site.com")
        
        link_finder_agent.evasion_level = EvasionLevel.STEALTH
        with patch('src.agents.link_finder_agent.async_playwright'):
            await link_finder_agent.run_async("https://protected-site.com")
        
        # Verify different evasion levels were used
        assert EvasionLevel.BASIC in evasion_levels_used
        assert EvasionLevel.STEALTH in evasion_levels_used
    
    @pytest.mark.asyncio
    async def test_pipeline_data_flow_validation(self, mock_region_manager):
        """Test data flows correctly through pipeline stages"""
        
        # Create agents
        extractor = MockDataExtractorAgent(mock_region_manager)
        enricher = MockDataEnricherAgent(mock_region_manager)
        
        # Initial data
        initial_url = "https://example.com/special-event"
        
        # Stage 1: Extract
        extract_task = AgentTask(
            task_id="flow_extract",
            task_type=AgentTaskType.EXTRACT_TEXT,
            target_url=initial_url,
            metadata={"source": "pipeline_test"}
        )
        
        extract_result = await extractor.execute_with_rotation(extract_task)
        extracted_data = extract_result.data["event_details"]
        
        # Verify extraction preserved URL
        assert extracted_data["title"] == f"Event from {initial_url}"
        
        # Stage 2: Enrich with extracted data
        enrich_task = AgentTask(
            task_id="flow_enrich",
            task_type=AgentTaskType.ANALYZE_ORGANIZER,
            target_url="",
            metadata={"input_data": extracted_data}
        )
        
        enrich_result = await enricher.execute_with_rotation(enrich_task)
        enriched_data = enrich_result.data["enriched_event"]
        
        # Verify enrichment preserved original data
        assert enriched_data["title"] == extracted_data["title"]
        assert enriched_data["date"] == extracted_data["date"]
        
        # Verify enrichment added new data
        assert "category" in enriched_data
        assert "tags" in enriched_data
        assert "quality_score" in enriched_data


class TestAgentPipelineOrchestration:
    """Test advanced pipeline orchestration scenarios"""
    
    @pytest.mark.asyncio
    async def test_parallel_pipeline_execution(self, mock_region_manager):
        """Test multiple pipelines running in parallel"""
        
        # Create multiple agent instances
        extractors = [
            MockDataExtractorAgent(mock_region_manager) for _ in range(3)
        ]
        
        # Create tasks for parallel execution
        tasks = []
        for i in range(9):  # 9 tasks across 3 extractors
            task = AgentTask(
                task_id=f"parallel_task_{i}",
                task_type=AgentTaskType.EXTRACT_TEXT,
                target_url=f"https://example.com/event-{i}",
                metadata={"batch": i // 3}
            )
            
            # Assign to extractor in round-robin
            extractor = extractors[i % 3]
            tasks.append(extractor.execute_with_rotation(task))
        
        # Execute all tasks in parallel
        results = await asyncio.gather(*tasks)
        
        # Verify all completed
        assert len(results) == 9
        assert all(r.success for r in results)
        
        # Verify tasks were distributed
        for i, result in enumerate(results):
            expected_batch = i // 3
            assert result.data["event_details"]["title"] == f"Event from https://example.com/event-{i}"
    
    @pytest.mark.asyncio
    async def test_pipeline_retry_mechanism(self, mock_region_manager):
        """Test pipeline retry logic for failed tasks"""
        
        # Create agent that fails first time
        class RetryableAgent(BaseAgent):
            def __init__(self, region_manager):
                super().__init__(region_manager)
                self.attempt_count = defaultdict(int)
            
            async def _execute_core_logic(self, task: AgentTask, session: RegionalSession) -> AgentResult:
                self.attempt_count[task.task_id] += 1
                
                # Fail on first attempt
                if self.attempt_count[task.task_id] == 1:
                    raise Exception("First attempt fails")
                
                return AgentResult(
                    task_id=task.task_id,
                    success=True,
                    data={"attempts": self.attempt_count[task.task_id]},
                    performance_metrics={},
                    region_used=session.region,
                    execution_time=0.1
                )
        
        agent = RetryableAgent(mock_region_manager)
        
        # Create task with retries enabled
        task = AgentTask(
            task_id="retry_test",
            task_type=AgentTaskType.EXTRACT_TEXT,
            target_url="https://example.com",
            metadata={},
            max_retries=2
        )
        
        # Mock sleep to speed up test
        with patch('asyncio.sleep'):
            result = await agent.execute_with_rotation(task)
        
        # Should succeed on retry
        assert result.success
        assert result.data["attempts"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
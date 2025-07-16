#!/usr/bin/env python3
"""
Comprehensive test suite for BaseAgent foundation class
Tests the core agent infrastructure, rotation capabilities, and error handling
"""

import sys
import time
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

# Add parent directory to path
# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.agents.base_agent import (
    AgentResult,
    AgentTask,
    AgentTaskType,
    AntiDetectionEngine,
    BaseAgent,
    PerformanceMonitor,
    RateLimiter,
    RegionalSession,
)


class ConcreteAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing"""

    async def _execute_core_logic(
        self, task: AgentTask, session: RegionalSession
    ) -> AgentResult:
        """Simple implementation for testing"""
        return AgentResult(
            task_id=task.task_id,
            success=True,
            data={"result": "test_data"},
            performance_metrics={},
            region_used=session.region,
            execution_time=0.0,
        )


class FailingAgent(BaseAgent):
    """Agent that always fails for testing error handling"""

    async def _execute_core_logic(
        self, task: AgentTask, session: RegionalSession
    ) -> AgentResult:
        raise Exception("Simulated failure")


class TestAgentTaskType:
    """Test AgentTaskType enum"""

    def test_task_types_defined(self):
        """Test all task types are properly defined"""
        assert AgentTaskType.SCROLL_CALENDAR.value == "scroll_calendar"
        assert AgentTaskType.DISCOVER_LINKS.value == "discover_links"
        assert AgentTaskType.EXTRACT_TEXT.value == "extract_text"
        assert AgentTaskType.ANALYZE_ORGANIZER.value == "analyze_organizer"
        assert AgentTaskType.PROCESS_IMAGES.value == "process_images"
        assert AgentTaskType.MINE_AGENDA.value == "mine_agenda"


class TestAgentTask:
    """Test AgentTask dataclass"""

    def test_task_creation(self):
        """Test creating an AgentTask"""
        task = AgentTask(
            task_id="test_123",
            task_type=AgentTaskType.DISCOVER_LINKS,
            target_url="https://example.com",
            metadata={"key": "value"},
            region_preference="us-east",
            retry_count=1,
            max_retries=5,
        )

        assert task.task_id == "test_123"
        assert task.task_type == AgentTaskType.DISCOVER_LINKS
        assert task.target_url == "https://example.com"
        assert task.metadata == {"key": "value"}
        assert task.region_preference == "us-east"
        assert task.retry_count == 1
        assert task.max_retries == 5

    def test_task_defaults(self):
        """Test default values for AgentTask"""
        task = AgentTask(
            task_id="test_456",
            task_type=AgentTaskType.EXTRACT_TEXT,
            target_url="https://example.com",
            metadata={},
        )

        assert task.region_preference is None
        assert task.retry_count == 0
        assert task.max_retries == 3


class TestAgentResult:
    """Test AgentResult dataclass"""

    def test_result_creation(self):
        """Test creating an AgentResult"""
        result = AgentResult(
            task_id="test_123",
            success=True,
            data={"events": ["event1", "event2"]},
            performance_metrics={"avg_time": 1.5},
            region_used="eu-west",
            execution_time=2.5,
            error_message=None,
            next_task_data={"next": "task"},
        )

        assert result.task_id == "test_123"
        assert result.success is True
        assert result.data == {"events": ["event1", "event2"]}
        assert result.performance_metrics == {"avg_time": 1.5}
        assert result.region_used == "eu-west"
        assert result.execution_time == 2.5
        assert result.error_message is None
        assert result.next_task_data == {"next": "task"}


class TestRegionalSession:
    """Test RegionalSession dataclass"""

    def test_session_creation(self):
        """Test creating a RegionalSession"""
        now = datetime.now()
        session = RegionalSession(
            region="us-west",
            session_id="sess_123",
            browser_context=None,
            http_session=None,
            created_at=now,
            last_used=now,
            request_count=10,
            rate_limit_remaining=50,
            is_active=True,
        )

        assert session.region == "us-west"
        assert session.session_id == "sess_123"
        assert session.created_at == now
        assert session.last_used == now
        assert session.request_count == 10
        assert session.rate_limit_remaining == 50
        assert session.is_active is True


class TestPerformanceMonitor:
    """Test PerformanceMonitor class"""

    def test_performance_monitoring(self):
        """Test basic performance monitoring"""
        monitor = PerformanceMonitor()

        # Start operation
        monitor.start_operation("op1")
        time.sleep(0.1)  # Simulate work
        duration = monitor.end_operation("op1")

        assert duration >= 0.1
        assert "op1" in monitor.metrics

        metrics = monitor.get_metrics()
        assert metrics["total_operations"] == 1
        assert metrics["average_operation_time"] > 0

    def test_multiple_operations(self):
        """Test monitoring multiple operations"""
        monitor = PerformanceMonitor()

        # Multiple operations
        for i in range(3):
            monitor.start_operation(f"op{i}")
            time.sleep(0.05)
            monitor.end_operation(f"op{i}")

        metrics = monitor.get_metrics()
        assert metrics["total_operations"] == 3
        assert len(metrics["operation_metrics"]) == 3

    def test_end_nonexistent_operation(self):
        """Test ending an operation that wasn't started"""
        monitor = PerformanceMonitor()
        duration = monitor.end_operation("nonexistent")
        assert duration == 0.0


class TestRateLimiter:
    """Test RateLimiter class"""

    @pytest.mark.asyncio
    async def test_rate_limiting_basic(self):
        """Test basic rate limiting functionality"""
        limiter = RateLimiter(max_requests_per_minute=5)

        # Should allow first 5 requests
        for _ in range(5):
            await limiter.wait_if_needed()

        assert limiter.get_remaining_quota() == 0

    @pytest.mark.asyncio
    async def test_rate_limiting_with_wait(self):
        """Test rate limiting forces wait when limit exceeded"""
        limiter = RateLimiter(max_requests_per_minute=2)

        # First two should be immediate
        start = time.time()
        await limiter.wait_if_needed()
        await limiter.wait_if_needed()

        # Third should wait (mocked to be faster)
        with patch("asyncio.sleep") as mock_sleep:
            mock_sleep.return_value = None
            await limiter.wait_if_needed()
            mock_sleep.assert_called_once()
            wait_time = mock_sleep.call_args[0][0]
            assert wait_time > 0

    def test_quota_calculation(self):
        """Test remaining quota calculation"""
        limiter = RateLimiter(max_requests_per_minute=10)

        # Initially should have full quota
        assert limiter.get_remaining_quota() == 10

        # Add some requests
        limiter.request_times = [time.time()] * 3
        assert limiter.get_remaining_quota() == 7

    @pytest.mark.asyncio
    async def test_old_requests_cleanup(self):
        """Test old requests are cleaned up after 1 minute"""
        limiter = RateLimiter(max_requests_per_minute=5)

        # Add old requests (>60 seconds ago)
        old_time = time.time() - 65
        limiter.request_times = [old_time, old_time]

        # Should not count old requests
        await limiter.wait_if_needed()
        assert len(limiter.request_times) == 1  # Only the new request


class TestBaseAgent:
    """Test BaseAgent base class"""

    @pytest.fixture
    def mock_region_manager(self):
        """Create a mock region manager"""
        manager = AsyncMock()
        manager.get_optimal_region.return_value = "us-east"
        manager.get_regional_session.return_value = RegionalSession(
            region="us-east",
            session_id="test_session",
            browser_context=None,
            http_session=None,
            created_at=datetime.now(),
            last_used=datetime.now(),
            request_count=0,
            rate_limit_remaining=100,
            is_active=True,
        )
        return manager

    @pytest.fixture
    def concrete_agent(self, mock_region_manager):
        """Create a concrete agent instance"""
        return ConcreteAgent(mock_region_manager)

    @pytest.fixture
    def failing_agent(self, mock_region_manager):
        """Create a failing agent instance"""
        return FailingAgent(mock_region_manager)

    def test_agent_initialization(self, mock_region_manager):
        """Test agent initialization"""
        agent = ConcreteAgent(mock_region_manager)

        assert agent.region_manager == mock_region_manager
        assert agent.performance_monitor is not None
        assert agent.rate_limiter is not None
        assert "ConcreteAgent" in agent.agent_id

    @pytest.mark.asyncio
    async def test_execute_with_rotation_success(
        self, concrete_agent, mock_region_manager
    ):
        """Test successful task execution with rotation"""
        task = AgentTask(
            task_id="test_task",
            task_type=AgentTaskType.DISCOVER_LINKS,
            target_url="https://example.com",
            metadata={},
        )

        result = await concrete_agent.execute_with_rotation(task)

        assert result.success is True
        assert result.task_id == "test_task"
        assert result.region_used == "us-east"
        assert result.execution_time > 0
        assert result.data == {"result": "test_data"}

        # Verify region manager was used
        mock_region_manager.get_optimal_region.assert_called_once_with(task)
        mock_region_manager.get_regional_session.assert_called_once_with("us-east")

    @pytest.mark.asyncio
    async def test_execute_with_rotation_failure(
        self, failing_agent, mock_region_manager
    ):
        """Test failed task execution with retry"""
        task = AgentTask(
            task_id="fail_task",
            task_type=AgentTaskType.EXTRACT_TEXT,
            target_url="https://example.com",
            metadata={},
            max_retries=1,
        )

        # Mock sleep to speed up test
        with patch("asyncio.sleep"):
            result = await failing_agent.execute_with_rotation(task)

        assert result.success is False
        assert result.error_message == "Simulated failure"
        assert "fail_task" in result.task_id

        # Should have tried twice (original + 1 retry)
        assert mock_region_manager.get_optimal_region.call_count == 2

    @pytest.mark.asyncio
    async def test_rate_limiting_applied(self, concrete_agent):
        """Test rate limiting is applied during execution"""
        task = AgentTask(
            task_id="rate_test",
            task_type=AgentTaskType.SCROLL_CALENDAR,
            target_url="https://example.com",
            metadata={},
        )

        # Spy on rate limiter
        with patch.object(
            concrete_agent.rate_limiter, "wait_if_needed", new_callable=AsyncMock
        ) as mock_wait:
            await concrete_agent.execute_with_rotation(task)
            mock_wait.assert_called_once()

    @pytest.mark.asyncio
    async def test_performance_monitoring(self, concrete_agent):
        """Test performance monitoring during execution"""
        task = AgentTask(
            task_id="perf_test",
            task_type=AgentTaskType.ANALYZE_ORGANIZER,
            target_url="https://example.com",
            metadata={},
        )

        result = await concrete_agent.execute_with_rotation(task)

        assert result.execution_time > 0
        assert "performance_metrics" in result.__dict__
        assert result.performance_metrics["total_operations"] > 0

    @pytest.mark.asyncio
    async def test_regional_metrics_update(self, concrete_agent, mock_region_manager):
        """Test regional metrics are updated after execution"""
        task = AgentTask(
            task_id="metrics_test",
            task_type=AgentTaskType.PROCESS_IMAGES,
            target_url="https://example.com",
            metadata={},
        )

        await concrete_agent.execute_with_rotation(task)

        # Verify metrics were updated
        mock_region_manager.update_regional_metrics.assert_called_once()
        call_args = mock_region_manager.update_regional_metrics.call_args
        assert call_args[0][0] == "us-east"  # region
        assert call_args[0][1]["success"] is True
        assert "execution_time" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_error_with_fallback(self, failing_agent, mock_region_manager):
        """Test error handling with regional fallback"""
        task = AgentTask(
            task_id="fallback_test",
            task_type=AgentTaskType.MINE_AGENDA,
            target_url="https://example.com",
            metadata={},
            region_preference="eu-west",
            max_retries=2,
        )

        # Mock different regions for retries
        mock_region_manager.get_optimal_region.side_effect = [
            "eu-west",
            "us-east",
            "asia-pac",
        ]

        with patch("asyncio.sleep"):
            result = await failing_agent.execute_with_rotation(task)

        # Should have tried 3 times (original + 2 retries)
        assert mock_region_manager.get_optimal_region.call_count == 3
        assert result.success is False

    def test_get_agent_specific_config(self, concrete_agent):
        """Test agent-specific configuration"""
        config = concrete_agent._get_agent_specific_config()

        assert "user_agent" in config
        assert "ConcreteAgent" in config["user_agent"]
        assert config["timeout"] == 30
        assert config["max_retries"] == 3


class TestAntiDetectionEngine:
    """Test AntiDetectionEngine class"""

    def test_engine_initialization(self):
        """Test anti-detection engine initialization"""
        engine = AntiDetectionEngine()

        assert "scroll_timings" in engine.patterns
        assert "mouse_movements" in engine.patterns
        assert "pause_probabilities" in engine.patterns
        assert "typing_speeds" in engine.patterns

    @pytest.mark.asyncio
    async def test_natural_delay(self):
        """Test natural delay generation"""
        engine = AntiDetectionEngine()

        with patch("asyncio.sleep") as mock_sleep:
            await engine.add_natural_delay(0.5, 2.0)
            mock_sleep.assert_called_once()
            delay = mock_sleep.call_args[0][0]
            assert 0.5 <= delay <= 2.0

    @pytest.mark.asyncio
    async def test_human_scroll_simulation(self):
        """Test human-like scrolling simulation"""
        engine = AntiDetectionEngine()
        mock_page = AsyncMock()

        await engine.simulate_human_scroll(mock_page, distance=300)

        # Should have multiple scroll calls
        assert mock_page.evaluate.call_count >= 3

        # Check scroll commands
        for call in mock_page.evaluate.call_args_list:
            command = call[0][0]
            assert "window.scrollBy" in command

    @pytest.mark.asyncio
    async def test_human_typing_simulation(self):
        """Test human-like typing simulation"""
        engine = AntiDetectionEngine()
        mock_page = AsyncMock()

        await engine.simulate_human_typing(mock_page, "#input", "Hello")

        # Should clear field first
        mock_page.fill.assert_called_once_with("#input", "")

        # Should type each character
        assert mock_page.type.call_count == 5  # "Hello" = 5 chars

        # Verify each character was typed
        typed_chars = [call[0][1] for call in mock_page.type.call_args_list]
        assert "".join(typed_chars) == "Hello"


class TestBaseAgentIntegration:
    """Integration tests for BaseAgent with multiple components"""

    @pytest.mark.asyncio
    async def test_full_execution_flow(self):
        """Test complete execution flow with all components"""
        mock_region_manager = AsyncMock()
        mock_region_manager.get_optimal_region.return_value = "us-west"
        mock_region_manager.get_regional_session.return_value = RegionalSession(
            region="us-west",
            session_id="integ_session",
            browser_context=AsyncMock(),
            http_session=AsyncMock(),
            created_at=datetime.now(),
            last_used=datetime.now(),
            request_count=5,
            rate_limit_remaining=95,
            is_active=True,
        )

        agent = ConcreteAgent(mock_region_manager)

        # Execute multiple tasks
        tasks = [
            AgentTask(
                task_id=f"task_{i}",
                task_type=list(AgentTaskType)[i % len(AgentTaskType)],
                target_url=f"https://example{i}.com",
                metadata={"index": i},
            )
            for i in range(3)
        ]

        results = []
        for task in tasks:
            result = await agent.execute_with_rotation(task)
            results.append(result)

        # All should succeed
        assert all(r.success for r in results)
        assert len(set(r.task_id for r in results)) == 3

        # Performance metrics should accumulate
        last_result = results[-1]
        assert last_result.performance_metrics["total_operations"] >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

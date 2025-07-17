#!/usr/bin/env python3
"""
Comprehensive test suite for LinkFinderAgent
Tests the core event discovery and extraction functionality
"""

<<<<<<< HEAD
import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest
=======
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
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
=======
from src.agents.link_finder_agent import LinkFinderAgent
from src.agents.anti_bot_evasion_manager import EvasionLevel
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752


class TestLinkFinderAgent:
    """Test suite for LinkFinderAgent"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.fixture
    def mock_logger(self):
        """Create a mock logger"""
        return Mock()
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.fixture
    def agent(self, mock_logger):
        """Create a LinkFinderAgent instance"""
        return LinkFinderAgent(
            name="TestLinkFinder",
            logger=mock_logger,
            evasion_level=EvasionLevel.BASIC,
<<<<<<< HEAD
            luma_optimization=True,
        )

=======
            luma_optimization=True
        )
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def test_agent_initialization(self, mock_logger):
        """Test LinkFinderAgent initialization"""
        agent = LinkFinderAgent(
            name="TestAgent",
            logger=mock_logger,
            evasion_level=EvasionLevel.ADVANCED,
<<<<<<< HEAD
            luma_optimization=True,
        )

=======
            luma_optimization=True
        )
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert agent.name == "TestAgent"
        assert agent.logger == mock_logger
        assert agent.evasion_level == EvasionLevel.ADVANCED
        assert agent.luma_optimization is True
        assert agent.evasion_manager is not None
<<<<<<< HEAD

        # Verify logger was called
        mock_logger.info.assert_called_once()

    def test_agent_initialization_default_logger(self):
        """Test agent creates default logger when none provided"""
        agent = LinkFinderAgent()

        assert agent.name == "LinkFinderAgent"
        assert agent.logger is not None
        assert agent.evasion_level == EvasionLevel.ADVANCED

=======
        
        # Verify logger was called
        mock_logger.info.assert_called_once()
    
    def test_agent_initialization_default_logger(self):
        """Test agent creates default logger when none provided"""
        agent = LinkFinderAgent()
        
        assert agent.name == "LinkFinderAgent"
        assert agent.logger is not None
        assert agent.evasion_level == EvasionLevel.ADVANCED
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_run_async_basic_extraction(self, agent):
        """Test basic link extraction functionality"""
        # Mock playwright components
        mock_browser = AsyncMock()
        mock_context = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

        # Setup mock chain
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock page behavior
        mock_page.goto.return_value = None
        mock_page.wait_for_load_state.return_value = None

=======
        
        # Setup mock chain
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        
        # Mock page behavior
        mock_page.goto.return_value = None
        mock_page.wait_for_load_state.return_value = None
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Mock link elements
        mock_link1 = AsyncMock()
        mock_link1.get_attribute.side_effect = lambda attr: {
            "href": "/event1",
<<<<<<< HEAD
            "aria-label": "Test Event 1",
        }.get(attr)
        mock_link1.text_content.return_value = "Test Event 1"

        mock_link2 = AsyncMock()
        mock_link2.get_attribute.side_effect = lambda attr: {
            "href": "/event2",
            "aria-label": "Test Event 2",
        }.get(attr)
        mock_link2.text_content.return_value = "Test Event 2"

        mock_page.query_selector_all.return_value = [mock_link1, mock_link2]

        # Mock evasion manager
        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )

        # Run the agent
        with patch(
            "src.agents.link_finder_agent.async_playwright"
        ) as mock_playwright_context:
            mock_playwright_instance = AsyncMock()
            mock_playwright_context.return_value.__aenter__.return_value = (
                mock_playwright_instance
            )
            mock_playwright_instance.chromium = Mock()

            results = await agent.run_async("https://lu.ma/test-calendar")

=======
            "aria-label": "Test Event 1"
        }.get(attr)
        mock_link1.text_content.return_value = "Test Event 1"
        
        mock_link2 = AsyncMock()
        mock_link2.get_attribute.side_effect = lambda attr: {
            "href": "/event2",
            "aria-label": "Test Event 2"
        }.get(attr)
        mock_link2.text_content.return_value = "Test Event 2"
        
        mock_page.query_selector_all.return_value = [mock_link1, mock_link2]
        
        # Mock evasion manager
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        
        # Run the agent
        with patch('src.agents.link_finder_agent.async_playwright') as mock_playwright_context:
            mock_playwright_instance = AsyncMock()
            mock_playwright_context.return_value.__aenter__.return_value = mock_playwright_instance
            mock_playwright_instance.chromium = Mock()
            
            results = await agent.run_async("https://lu.ma/test-calendar")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify results
        assert len(results) == 2
        assert results[0]["name"] == "Test Event 1"
        assert results[0]["url"] == "https://lu.ma/event1"
        assert results[1]["name"] == "Test Event 2"
        assert results[1]["url"] == "https://lu.ma/event2"
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_run_async_with_scrolling(self, agent):
        """Test scrolling behavior for dynamic content loading"""
        # Mock playwright components
        mock_browser = AsyncMock()
        mock_context = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        # Mock page metrics for scrolling
        mock_page.evaluate.side_effect = [
            1000,  # Initial scroll height
            500,  # Current scroll position
=======
        
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page
        
        # Mock page metrics for scrolling
        mock_page.evaluate.side_effect = [
            1000,  # Initial scroll height
            500,   # Current scroll position
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            1500,  # New scroll height after scroll
            1000,  # Current scroll position after scroll
            1500,  # Final scroll height (no change)
        ]
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Mock link discovery
        mock_link = AsyncMock()
        mock_link.get_attribute.side_effect = lambda attr: {
            "href": "/dynamic-event",
<<<<<<< HEAD
            "aria-label": "Dynamic Event",
        }.get(attr)

        # Return links only after scrolling
        call_count = 0

=======
            "aria-label": "Dynamic Event"
        }.get(attr)
        
        # Return links only after scrolling
        call_count = 0
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        async def mock_query_selector_all(selector):
            nonlocal call_count
            call_count += 1
            if call_count > 1:  # After first scroll
                return [mock_link]
            return []
<<<<<<< HEAD

        mock_page.query_selector_all = mock_query_selector_all

        # Mock evasion manager
        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )

        # Run the agent
        with patch("src.agents.link_finder_agent.async_playwright"):
            results = await agent.run_async("https://lu.ma/test-calendar")

=======
        
        mock_page.query_selector_all = mock_query_selector_all
        
        # Mock evasion manager
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        
        # Run the agent
        with patch('src.agents.link_finder_agent.async_playwright'):
            results = await agent.run_async("https://lu.ma/test-calendar")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify scrolling occurred
        assert mock_page.evaluate.call_count >= 2
        assert len(results) == 1
        assert results[0]["name"] == "Dynamic Event"
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_run_async_handles_cloudflare_challenge(self, agent):
        """Test handling of Cloudflare challenge detection"""
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Simulate Cloudflare challenge page
        mock_page.content.return_value = """
        <html>
            <head><title>Just a moment...</title></head>
            <body>Cloudflare challenge</body>
        </html>
        """
<<<<<<< HEAD

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        with patch("src.agents.link_finder_agent.async_playwright"):
            results = await agent.run_async("https://lu.ma/test-calendar")

        # Should return empty list on Cloudflare challenge
        assert results == []
        agent.logger.warning.assert_called()

=======
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            results = await agent.run_async("https://lu.ma/test-calendar")
        
        # Should return empty list on Cloudflare challenge
        assert results == []
        agent.logger.warning.assert_called()
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_run_async_handles_rate_limiting(self, agent):
        """Test handling of rate limiting (429 errors)"""
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

        # Simulate 429 error
        mock_page.goto.side_effect = Exception("429 Too Many Requests")

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        with patch("src.agents.link_finder_agent.async_playwright"):
            results = await agent.run_async("https://lu.ma/test-calendar")

        assert results == []
        agent.logger.error.assert_called()

=======
        
        # Simulate 429 error
        mock_page.goto.side_effect = Exception("429 Too Many Requests")
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            results = await agent.run_async("https://lu.ma/test-calendar")
        
        assert results == []
        agent.logger.error.assert_called()
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_event_name_extraction_methods(self, agent):
        """Test various event name extraction methods"""
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Test different name extraction scenarios
        test_cases = [
            # Method A: aria-label
            {
                "href": "/event1",
                "aria-label": "Conference Event 1",
                "text_content": "",
                "title": "",
<<<<<<< HEAD
                "expected_name": "Conference Event 1",
            },
            # Method B: text content fallback
            {
                "href": "/event2",
                "aria-label": "",
                "text_content": "Workshop Event 2",
                "title": "",
                "expected_name": "Workshop Event 2",
=======
                "expected_name": "Conference Event 1"
            },
            # Method B: text content fallback
            {
                "href": "/event2", 
                "aria-label": "",
                "text_content": "Workshop Event 2",
                "title": "",
                "expected_name": "Workshop Event 2"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            },
            # Method C: title attribute fallback
            {
                "href": "/event3",
                "aria-label": "",
                "text_content": "",
                "title": "Meetup Event 3",
<<<<<<< HEAD
                "expected_name": "Meetup Event 3",
=======
                "expected_name": "Meetup Event 3"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            },
            # Method D: Context-aware naming for EthCC
            {
                "href": "/abcdef",
                "aria-label": "",
                "text_content": "",
                "title": "",
<<<<<<< HEAD
                "expected_name": "EthCC Event abcdef",
            },
        ]

=======
                "expected_name": "EthCC Event abcdef"
            }
        ]
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        mock_links = []
        for case in test_cases:
            mock_link = AsyncMock()
            mock_link.get_attribute.side_effect = lambda attr, c=case: c.get(attr, "")
            mock_link.text_content.return_value = case["text_content"]
            mock_link.query_selector.return_value = None  # No parent elements
            mock_links.append(mock_link)
<<<<<<< HEAD

        mock_page.query_selector_all.return_value = mock_links

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        with patch("src.agents.link_finder_agent.async_playwright"):
            results = await agent.run_async("https://lu.ma/ethcc-calendar")

=======
        
        mock_page.query_selector_all.return_value = mock_links
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            results = await agent.run_async("https://lu.ma/ethcc-calendar")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify all extraction methods work
        assert len(results) == 4
        for i, case in enumerate(test_cases):
            assert results[i]["name"] == case["expected_name"]
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_duplicate_url_filtering(self, agent):
        """Test that duplicate URLs are filtered out"""
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Create duplicate links
        mock_link1 = AsyncMock()
        mock_link1.get_attribute.side_effect = lambda attr: {
            "href": "/same-event",
<<<<<<< HEAD
            "aria-label": "Duplicate Event",
        }.get(attr)

        mock_link2 = AsyncMock()
        mock_link2.get_attribute.side_effect = lambda attr: {
            "href": "/same-event",  # Same URL
            "aria-label": "Duplicate Event Again",
        }.get(attr)

        mock_page.query_selector_all.return_value = [mock_link1, mock_link2]

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        with patch("src.agents.link_finder_agent.async_playwright"):
            results = await agent.run_async("https://lu.ma/test-calendar")

        # Should only have one result
        assert len(results) == 1
        assert results[0]["url"] == "https://lu.ma/same-event"

=======
            "aria-label": "Duplicate Event"
        }.get(attr)
        
        mock_link2 = AsyncMock()
        mock_link2.get_attribute.side_effect = lambda attr: {
            "href": "/same-event",  # Same URL
            "aria-label": "Duplicate Event Again"
        }.get(attr)
        
        mock_page.query_selector_all.return_value = [mock_link1, mock_link2]
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            results = await agent.run_async("https://lu.ma/test-calendar")
        
        # Should only have one result
        assert len(results) == 1
        assert results[0]["url"] == "https://lu.ma/same-event"
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_invalid_url_handling(self, agent):
        """Test handling of invalid and non-Luma URLs"""
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

        # Create various invalid links
        invalid_links = [
            {
                "href": "https://external.com/event",
                "aria-label": "External Event",
            },  # Non-Luma
=======
        
        # Create various invalid links
        invalid_links = [
            {"href": "https://external.com/event", "aria-label": "External Event"},  # Non-Luma
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            {"href": "#", "aria-label": "Hash Link"},  # Invalid
            {"href": "", "aria-label": "Empty Link"},  # Empty
            {"href": "javascript:void(0)", "aria-label": "JS Link"},  # JavaScript
            {"href": None, "aria-label": "Null Link"},  # Null
        ]
<<<<<<< HEAD

        mock_links = []
        for link_data in invalid_links:
            mock_link = AsyncMock()
            mock_link.get_attribute.side_effect = lambda attr, data=link_data: data.get(
                attr
            )
            mock_links.append(mock_link)

=======
        
        mock_links = []
        for link_data in invalid_links:
            mock_link = AsyncMock()
            mock_link.get_attribute.side_effect = lambda attr, data=link_data: data.get(attr)
            mock_links.append(mock_link)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Add one valid link
        valid_link = AsyncMock()
        valid_link.get_attribute.side_effect = lambda attr: {
            "href": "/valid-event",
<<<<<<< HEAD
            "aria-label": "Valid Event",
        }.get(attr)
        mock_links.append(valid_link)

        mock_page.query_selector_all.return_value = mock_links

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        with patch("src.agents.link_finder_agent.async_playwright"):
            results = await agent.run_async("https://lu.ma/test-calendar")

=======
            "aria-label": "Valid Event"
        }.get(attr)
        mock_links.append(valid_link)
        
        mock_page.query_selector_all.return_value = mock_links
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            results = await agent.run_async("https://lu.ma/test-calendar")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Should only have the valid link
        assert len(results) == 1
        assert results[0]["name"] == "Valid Event"
        assert results[0]["url"] == "https://lu.ma/valid-event"
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_browser_cleanup_on_error(self, agent):
        """Test proper browser cleanup on errors"""
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
<<<<<<< HEAD

        # Simulate error during page operations
        mock_page.goto.side_effect = Exception("Network error")

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        with patch("src.agents.link_finder_agent.async_playwright"):
            results = await agent.run_async("https://lu.ma/test-calendar")

        # Verify cleanup was attempted
        mock_browser.close.assert_called_once()
        assert results == []

=======
        
        # Simulate error during page operations
        mock_page.goto.side_effect = Exception("Network error")
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            results = await agent.run_async("https://lu.ma/test-calendar")
        
        # Verify cleanup was attempted
        mock_browser.close.assert_called_once()
        assert results == []
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_luma_optimization_enabled(self, agent):
        """Test lu.ma specific optimizations"""
        assert agent.luma_optimization is True
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify Luma-specific selectors are used
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        mock_page.query_selector_all.return_value = []
<<<<<<< HEAD

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        with patch("src.agents.link_finder_agent.async_playwright"):
            await agent.run_async("https://lu.ma/test-calendar")

=======
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            await agent.run_async("https://lu.ma/test-calendar")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Verify Luma-specific selector was used
        mock_page.query_selector_all.assert_called_with(
            "a.event-link.content-link, a[href^='/']:not([href='/'])"
        )
<<<<<<< HEAD

    def test_execute_method_exists(self, agent):
        """Test that execute method exists for BaseAgent compatibility"""
        assert hasattr(agent, "execute")

        # Test synchronous execute wrapper
        result = agent.execute("https://lu.ma/test")
        assert isinstance(result, list)

=======
    
    def test_execute_method_exists(self, agent):
        """Test that execute method exists for BaseAgent compatibility"""
        assert hasattr(agent, 'execute')
        
        # Test synchronous execute wrapper
        result = agent.execute("https://lu.ma/test")
        assert isinstance(result, list)
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_concurrent_safety(self, agent):
        """Test agent can handle concurrent executions safely"""
        # Mock setup
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        mock_page.query_selector_all.return_value = []
<<<<<<< HEAD

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        # Run multiple concurrent executions
        with patch("src.agents.link_finder_agent.async_playwright"):
            tasks = [
                agent.run_async("https://lu.ma/test1"),
                agent.run_async("https://lu.ma/test2"),
                agent.run_async("https://lu.ma/test3"),
            ]
            results = await asyncio.gather(*tasks)

=======
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        # Run multiple concurrent executions
        with patch('src.agents.link_finder_agent.async_playwright'):
            tasks = [
                agent.run_async("https://lu.ma/test1"),
                agent.run_async("https://lu.ma/test2"),
                agent.run_async("https://lu.ma/test3")
            ]
            results = await asyncio.gather(*tasks)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # All should complete without errors
        assert len(results) == 3
        assert all(isinstance(r, list) for r in results)


class TestLinkFinderAgentIntegration:
    """Integration tests for LinkFinderAgent with real page structures"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @pytest.mark.asyncio
    async def test_ethcc_calendar_structure(self):
        """Test extraction from EthCC-style calendar structure"""
        agent = LinkFinderAgent(
            name="EthCCFinder",
            evasion_level=EvasionLevel.STEALTH,
<<<<<<< HEAD
            luma_optimization=True,
        )

        # Mock EthCC-style page structure
        mock_browser = AsyncMock()
        mock_page = AsyncMock()

=======
            luma_optimization=True
        )
        
        # Mock EthCC-style page structure
        mock_browser = AsyncMock()
        mock_page = AsyncMock()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Simulate EthCC calendar with specific structure
        ethcc_links = []
        for i in range(5):
            mock_link = AsyncMock()
            mock_link.get_attribute.side_effect = lambda attr, idx=i: {
                "href": f"/ethcc-side-event-{idx}",
<<<<<<< HEAD
                "aria-label": f"EthCC Side Event {idx}",
            }.get(attr)
            ethcc_links.append(mock_link)

        mock_page.query_selector_all.return_value = ethcc_links

        agent.evasion_manager.create_evasion_session = AsyncMock(
            return_value=mock_browser
        )
        mock_browser.new_context.return_value.new_page.return_value = mock_page

        with patch("src.agents.link_finder_agent.async_playwright"):
            results = await agent.run_async("https://lu.ma/ethcc")

=======
                "aria-label": f"EthCC Side Event {idx}"
            }.get(attr)
            ethcc_links.append(mock_link)
        
        mock_page.query_selector_all.return_value = ethcc_links
        
        agent.evasion_manager.create_evasion_session = AsyncMock(return_value=mock_browser)
        mock_browser.new_context.return_value.new_page.return_value = mock_page
        
        with patch('src.agents.link_finder_agent.async_playwright'):
            results = await agent.run_async("https://lu.ma/ethcc")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        assert len(results) == 5
        assert all("EthCC" in event["name"] for event in results)
        assert all(event["url"].startswith("https://lu.ma/") for event in results)


if __name__ == "__main__":
<<<<<<< HEAD
    pytest.main([__file__, "-v", "--tb=short"])
=======
    pytest.main([__file__, "-v", "--tb=short"])
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

#!/usr/bin/env python3
"""
Comprehensive test suite for AntiBotEvasionManager
Tests the security-critical anti-bot evasion components
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest

# Add parent directory to path
# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.agents.anti_bot_evasion_manager import AntiBotEvasionManager, EvasionLevel


class TestEvasionLevel:
    """Test EvasionLevel enum"""

    def test_evasion_levels_defined(self):
        """Test all evasion levels are properly defined"""
        assert EvasionLevel.BASIC.value == "basic"
        assert EvasionLevel.STANDARD.value == "standard"
        assert EvasionLevel.ADVANCED.value == "advanced"
        assert EvasionLevel.STEALTH.value == "stealth"

    def test_evasion_level_ordering(self):
        """Test evasion levels represent increasing intensity"""
        levels = [
            EvasionLevel.BASIC,
            EvasionLevel.STANDARD,
            EvasionLevel.ADVANCED,
            EvasionLevel.STEALTH,
        ]
        # Verify all levels are unique
        assert len(set(levels)) == 4


class TestAntiBotEvasionManager:
    """Test AntiBotEvasionManager class"""

    @pytest.fixture
    def manager(self):
        """Create an AntiBotEvasionManager instance"""
        return AntiBotEvasionManager()

    def test_manager_initialization(self, manager):
        """Test manager initializes with correct attributes"""
        assert hasattr(manager, "sessions")
        assert hasattr(manager, "fingerprint_profiles")
        assert hasattr(manager, "behavior_patterns")

        # Check profiles are loaded
        assert len(manager.fingerprint_profiles) == 47
        assert len(manager.behavior_patterns) == 4

    def test_fingerprint_profiles_structure(self, manager):
        """Test fingerprint profiles have correct structure"""
        # Check a sample profile
        profile = next(iter(manager.fingerprint_profiles.values()))

        required_fields = [
            "user_agent",
            "viewport",
            "platform",
            "language",
            "timezone",
            "webgl_vendor",
            "webgl_renderer",
            "canvas_fingerprint",
            "audio_fingerprint",
            "fonts",
            "plugins",
            "headers",
        ]

        for field in required_fields:
            assert field in profile, f"Missing field: {field}"

        # Verify viewport structure
        assert "width" in profile["viewport"]
        assert "height" in profile["viewport"]
        assert isinstance(profile["viewport"]["width"], int)
        assert isinstance(profile["viewport"]["height"], int)

        # Verify headers structure
        assert "User-Agent" in profile["headers"]
        assert "Accept" in profile["headers"]
        assert "Accept-Language" in profile["headers"]

    def test_fingerprint_diversity(self, manager):
        """Test fingerprint profiles are diverse"""
        # Collect all user agents
        user_agents = [p["user_agent"] for p in manager.fingerprint_profiles.values()]

        # Should have multiple different user agents
        unique_agents = set(user_agents)
        assert len(unique_agents) >= 5

        # Check for different platforms
        platforms = [p["platform"] for p in manager.fingerprint_profiles.values()]
        assert "Win32" in platforms
        assert "MacIntel" in platforms

        # Check for different viewports
        viewports = [
            f"{p['viewport']['width']}x{p['viewport']['height']}"
            for p in manager.fingerprint_profiles.values()
        ]
        unique_viewports = set(viewports)
        assert len(unique_viewports) >= 5

    def test_behavior_patterns_structure(self, manager):
        """Test behavior patterns have correct structure"""
        expected_patterns = ["professional", "casual", "careful", "power_user"]

        for pattern_name in expected_patterns:
            assert pattern_name in manager.behavior_patterns

            pattern = manager.behavior_patterns[pattern_name]
            required_fields = [
                "mouse_style",
                "typing_speed",
                "scroll_behavior",
                "click_delay",
                "page_dwell",
                "interaction_freq",
            ]

            for field in required_fields:
                assert field in pattern, f"Missing field {field} in {pattern_name}"

            # Verify typing_speed is a tuple
            assert isinstance(pattern["typing_speed"], tuple)
            assert len(pattern["typing_speed"]) == 2

            # Verify click_delay is a tuple
            assert isinstance(pattern["click_delay"], tuple)
            assert len(pattern["click_delay"]) == 2

    def test_generate_font_list(self, manager):
        """Test font list generation for different browsers"""
        # Test Mac user agent
        mac_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        mac_fonts = manager._generate_font_list(mac_ua)

        assert "San Francisco" in mac_fonts
        assert "Helvetica Neue" in mac_fonts
        assert "Arial" in mac_fonts  # Common font

        # Test Windows user agent
        win_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        win_fonts = manager._generate_font_list(win_ua)

        assert "Calibri" in win_fonts
        assert "Segoe UI" in win_fonts
        assert "Arial" in win_fonts  # Common font

        # Mac and Windows should have different fonts
        mac_specific = set(mac_fonts) - set(win_fonts)
        win_specific = set(win_fonts) - set(mac_fonts)
        assert len(mac_specific) > 0
        assert len(win_specific) > 0

    def test_generate_plugin_list(self, manager):
        """Test plugin list generation for different browsers"""
        # Test Chrome
        chrome_ua = "Mozilla/5.0 (Windows NT 10.0) Chrome/120.0.0.0"
        chrome_plugins = manager._generate_plugin_list(chrome_ua)
        assert "Chrome PDF Plugin" in chrome_plugins
        assert "Native Client" in chrome_plugins

        # Test Firefox
        firefox_ua = "Mozilla/5.0 (Windows NT 10.0) Firefox/121.0"
        firefox_plugins = manager._generate_plugin_list(firefox_ua)
        assert "Firefox PDF Plugin" in firefox_plugins

        # Test Safari
        safari_ua = "Mozilla/5.0 (Macintosh) Safari/605.1.15"
        safari_plugins = manager._generate_plugin_list(safari_ua)
        assert "WebKit PDF Plugin" in safari_plugins

        # Test generic browser
        generic_ua = "Mozilla/5.0 Generic Browser"
        generic_plugins = manager._generate_plugin_list(generic_ua)
        assert "PDF Plugin" in generic_plugins

    @pytest.mark.asyncio
    async def test_create_evasive_session_basic(self, manager):
        """Test creating an evasive session with basic settings"""
        url = "https://example.com"
        session = await manager.create_evasive_session(url, EvasionLevel.BASIC)

        assert "session_id" in session
        assert session["session_id"].startswith("evasive_")
        assert "fingerprint" in session
        assert "behavior" in session
        assert session["url"] == url
        assert session["evasion_level"] == "basic"
        assert session["success_count"] == 0
        assert session["risk_score"] == 0.0

        # Check session is stored
        assert session["session_id"] in manager.sessions

    @pytest.mark.asyncio
    async def test_create_evasive_session_advanced(self, manager):
        """Test creating an evasive session with advanced settings"""
        url = "https://secure.example.com"
        session = await manager.create_evasive_session(url, EvasionLevel.ADVANCED)

        assert session["evasion_level"] == "advanced"
        assert isinstance(session["fingerprint"], dict)
        assert isinstance(session["behavior"], dict)
        assert isinstance(session["created_at"], datetime)
        assert isinstance(session["last_used"], datetime)

    @pytest.mark.asyncio
    async def test_create_evasive_session_stealth(self, manager):
        """Test creating an evasive session with stealth settings"""
        session = await manager.create_evasive_session(
            "https://protected.com", EvasionLevel.STEALTH
        )

        assert session["evasion_level"] == "stealth"
        # Stealth should get a valid fingerprint and behavior
        assert session["fingerprint"]["user_agent"]
        assert session["behavior"]["mouse_style"]

    @pytest.mark.asyncio
    async def test_multiple_sessions(self, manager):
        """Test creating multiple evasive sessions"""
        sessions = []
        for i in range(5):
            session = await manager.create_evasive_session(
                f"https://example{i}.com", EvasionLevel.STANDARD
            )
            sessions.append(session)

        # All sessions should have unique IDs
        session_ids = [s["session_id"] for s in sessions]
        assert len(set(session_ids)) == 5

        # All should be stored
        assert len(manager.sessions) == 5

    @pytest.mark.asyncio
    async def test_apply_evasion_to_browser_basic(self, manager):
        """Test applying evasion techniques to browser"""
        # Create a session
        session = await manager.create_evasive_session(
            "https://test.com", EvasionLevel.ADVANCED
        )

        # Mock browser instance
        mock_browser = AsyncMock()
        mock_browser.evaluate_on_new_document = AsyncMock()

        result = await manager.apply_evasion_to_browser(session, mock_browser)

        assert result is True
        # Verify JavaScript was injected
        mock_browser.evaluate_on_new_document.assert_called_once()

        # Check the injected script
        injected_script = mock_browser.evaluate_on_new_document.call_args[0][0]
        assert "navigator.platform" in injected_script
        assert "navigator.language" in injected_script
        assert "WebGLRenderingContext" in injected_script
        assert "window.navigator.webdriver" in injected_script

    @pytest.mark.asyncio
    async def test_apply_evasion_with_page_attribute(self, manager):
        """Test applying evasion when browser has page attribute"""
        session = await manager.create_evasive_session(
            "https://test.com", EvasionLevel.STANDARD
        )

        # Mock browser with page attribute
        mock_page = AsyncMock()
        mock_page.evaluate_on_new_document = AsyncMock()

        mock_browser = Mock()
        mock_browser.page = mock_page

        result = await manager.apply_evasion_to_browser(session, mock_browser)

        assert result is True
        mock_page.evaluate_on_new_document.assert_called_once()

    @pytest.mark.asyncio
    async def test_apply_evasion_error_handling(self, manager):
        """Test error handling in apply_evasion_to_browser"""
        session = await manager.create_evasive_session(
            "https://test.com", EvasionLevel.BASIC
        )

        # Mock browser that raises exception
        mock_browser = AsyncMock()
        mock_browser.evaluate_on_new_document.side_effect = Exception("Browser error")

        result = await manager.apply_evasion_to_browser(session, mock_browser)

        # Should handle error gracefully
        assert result is False

    def test_timezone_offset_calculation(self, manager):
        """Test timezone offset calculation"""
        # Test known timezones
        ny_offset = manager._get_timezone_offset("America/New_York")
        la_offset = manager._get_timezone_offset("America/Los_Angeles")

        # NY and LA should have different offsets
        assert ny_offset != la_offset

        # Test UTC
        utc_offset = manager._get_timezone_offset("UTC")
        assert utc_offset == 0

    @pytest.mark.asyncio
    async def test_session_fingerprint_consistency(self, manager):
        """Test that session fingerprints remain consistent"""
        session = await manager.create_evasive_session(
            "https://test.com", EvasionLevel.ADVANCED
        )

        # Store fingerprint reference
        original_fp = session["fingerprint"]

        # Fingerprint should not change for the session
        stored_session = manager.sessions[session["session_id"]]
        assert stored_session["fingerprint"] is original_fp

    @pytest.mark.asyncio
    async def test_masking_script_generation(self, manager):
        """Test the JavaScript masking script generation"""
        session = await manager.create_evasive_session(
            "https://test.com", EvasionLevel.STEALTH
        )

        # Create mock browser to capture script
        mock_browser = AsyncMock()
        captured_script = None

        async def capture_script(script):
            nonlocal captured_script
            captured_script = script

        mock_browser.evaluate_on_new_document = capture_script

        await manager.apply_evasion_to_browser(session, mock_browser)

        # Verify script contains expected overrides
        assert captured_script is not None
        assert "Object.defineProperty" in captured_script
        assert session["fingerprint"]["platform"] in captured_script
        assert session["fingerprint"]["language"] in captured_script
        assert session["fingerprint"]["webgl_vendor"] in captured_script
        assert session["fingerprint"]["webgl_renderer"] in captured_script

    @pytest.mark.asyncio
    async def test_browser_automation_removal(self, manager):
        """Test that automation indicators are removed"""
        session = await manager.create_evasive_session(
            "https://test.com", EvasionLevel.ADVANCED
        )

        mock_browser = AsyncMock()
        captured_script = None

        async def capture_script(script):
            nonlocal captured_script
            captured_script = script

        mock_browser.evaluate_on_new_document = capture_script

        await manager.apply_evasion_to_browser(session, mock_browser)

        # Verify automation removal
        assert "delete window.navigator.webdriver" in captured_script
        assert "delete window.callPhantom" in captured_script
        assert "delete window._phantom" in captured_script
        assert "delete window.phantom" in captured_script

    def test_fingerprint_uniqueness(self, manager):
        """Test that fingerprints have unique identifiers"""
        canvas_fps = [
            p["canvas_fingerprint"] for p in manager.fingerprint_profiles.values()
        ]
        audio_fps = [
            p["audio_fingerprint"] for p in manager.fingerprint_profiles.values()
        ]

        # All canvas fingerprints should be unique
        assert len(set(canvas_fps)) == len(canvas_fps)

        # All audio fingerprints should be unique
        assert len(set(audio_fps)) == len(audio_fps)

        # Format should be correct
        for fp in canvas_fps:
            assert fp.startswith("canvas_fp_")
            assert len(fp) == 26  # canvas_fp_ + 16 hex chars

        for fp in audio_fps:
            assert fp.startswith("audio_fp_")
            assert len(fp) == 25  # audio_fp_ + 16 hex chars


class TestAntiBotEvasionIntegration:
    """Integration tests for anti-bot evasion system"""

    @pytest.mark.asyncio
    async def test_evasion_level_escalation(self):
        """Test escalating evasion levels for increased protection"""
        manager = AntiBotEvasionManager()

        # Create sessions with increasing evasion levels
        basic_session = await manager.create_evasive_session(
            "https://easy.com", EvasionLevel.BASIC
        )
        standard_session = await manager.create_evasive_session(
            "https://normal.com", EvasionLevel.STANDARD
        )
        advanced_session = await manager.create_evasive_session(
            "https://protected.com", EvasionLevel.ADVANCED
        )
        stealth_session = await manager.create_evasive_session(
            "https://highly-protected.com", EvasionLevel.STEALTH
        )

        # All should have valid configurations
        for session in [
            basic_session,
            standard_session,
            advanced_session,
            stealth_session,
        ]:
            assert session["fingerprint"]
            assert session["behavior"]
            assert session["session_id"]

    @pytest.mark.asyncio
    async def test_concurrent_session_creation(self):
        """Test creating multiple sessions concurrently"""
        manager = AntiBotEvasionManager()

        # Create 10 sessions concurrently
        tasks = [
            manager.create_evasive_session(
                f"https://site{i}.com", EvasionLevel.STANDARD
            )
            for i in range(10)
        ]

        sessions = await asyncio.gather(*tasks)

        # All sessions should be unique
        session_ids = [s["session_id"] for s in sessions]
        assert len(set(session_ids)) == 10

        # All should be properly stored
        assert len(manager.sessions) == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

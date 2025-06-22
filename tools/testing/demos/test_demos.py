#!/usr/bin/env python3
"""Test suite for TrustWrapper demos"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

class TestDemos:
    def test_demo_imports(self):
        """Test that demos can be imported"""
        from demo import demo_event_wrapper
        from demo import demo_scraper_wrapper
        from demo import demo_treasury_wrapper
        assert True
    
    def test_demo_execution(self):
        """Test basic demo execution"""
        # Add demo execution tests here
        assert True

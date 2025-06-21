"""
Demo 2: Web Scraper Agent with ZK Trust

Shows how TrustWrapper adds verification to browser automation agents
"""
import sys
import os

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
demo_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(demo_dir)
sys.path.insert(0, project_root)

from src.core.trust_wrapper import ZKTrustWrapper
from typing import Dict, Any, Optional
import random
import time


class MockScraperAgent:
    """Mock scraper for demo (simulates real scraping)"""
    
    def __init__(self):
        self.name = "WebScraperAgent"
    
    def scrape(self, target: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Simulate web scraping"""
        # Simulate processing time
        time.sleep(random.uniform(0.5, 2.0))
        
        # Simulate scraping results
        if "fail" in target.lower():
            raise Exception("Failed to bypass anti-bot protection")
        
        return {
            "url": target,
            "title": f"Page Title for {target}",
            "data_points": random.randint(50, 500),
            "extraction_method": "css_selectors",
            "bypass_score": random.uniform(0.8, 0.99)
        }


def main():
    print("🌐 Demo 2: Web Scraping with ZK Verification")
    print("=" * 50)
    
    # Create the base scraper
    print("\n1. Creating Web Scraper Agent...")
    base_scraper = MockScraperAgent()
    
    # Wrap it with trust
    print("2. Wrapping with ZKTrustWrapper...")
    trusted_scraper = ZKTrustWrapper(base_scraper, "WebScraperPro")
    
    # Test targets
    test_targets = [
        {"target": "competitor-prices", "options": {"depth": 2}},
        {"target": "market-data", "options": {"format": "json"}},
        {"target": "fail-anti-bot", "options": {"retry": False}},
        {"target": "product-listings", "options": {"limit": 100}}
    ]
    
    print("\n3. Executing scraping tasks with ZK verification...\n")
    
    success_count = 0
    total_data_points = 0
    
    for task in test_targets:
        print(f"🎯 Scraping: {task['target']}")
        
        # Execute with verification
        result = trusted_scraper.verified_execute(task['target'], task['options'])
        
        # Show verification proof
        print(result)
        
        # Track metrics
        if result.metrics.success:
            success_count += 1
            if result.data:
                total_data_points += result.data.get('data_points', 0)
                bypass_score = result.data.get('bypass_score', 0)
                print(f"   📊 Extracted: {result.data.get('data_points')} data points")
                print(f"   🛡️ Bypass Score: {bypass_score:.2%}")
        else:
            print(f"   ❌ Error: {result.metrics.error_message}")
        
        print("-" * 50)
    
    # Show aggregate statistics
    stats = trusted_scraper.get_stats()
    success_rate = (success_count / stats['execution_count']) * 100
    
    print(f"\n📊 Scraping Statistics:")
    print(f"- Total Executions: {stats['execution_count']}")
    print(f"- Success Rate: {success_rate:.1f}%")
    print(f"- Total Data Points: {total_data_points:,}")
    print(f"- All verified with ZK proofs ✅")
    
    print("\n🔐 Privacy Features:")
    print("- Target URLs remain private")
    print("- Scraping methods are not revealed")
    print("- Only success metrics are proven")
    print("- Anti-detection techniques stay secret")


if __name__ == "__main__":
    main()
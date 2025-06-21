"""
Non-interactive demo of TrustWrapper with multiple agent types
"""
import sys
import os
import time
import random
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.trust_wrapper import ZKTrustWrapper


# Mock agents for demonstration
class MockEventAgent:
    """Simulates an event discovery agent"""
    
    def extract(self, url: str) -> Dict[str, Any]:
        """Extract events from a URL"""
        time.sleep(random.uniform(0.1, 0.5))  # Simulate work
        
        events = []
        if "ethcc" in url.lower():
            events = [
                {"name": "EthCC Main Conference", "date": "2025-07-15"},
                {"name": "DeFi Day", "date": "2025-07-16"},
                {"name": "NFT Workshop", "date": "2025-07-17"}
            ]
        elif "web3" in url.lower():
            events = [
                {"name": "Web3 Summit", "date": "2025-08-20"},
                {"name": "DAO Governance Forum", "date": "2025-08-21"}
            ]
        
        return {
            "url": url,
            "events": events,
            "extraction_method": "calendar_parser",
            "confidence": 0.95
        }


class MockScraperAgent:
    """Simulates a web scraping agent"""
    
    def scrape(self, target: str, options: Dict = None) -> Dict[str, Any]:
        """Scrape data from target"""
        time.sleep(random.uniform(0.2, 0.8))  # Simulate work
        
        if "fail" in target.lower():
            raise Exception("Anti-bot protection detected")
        
        return {
            "target": target,
            "data_points": random.randint(100, 500),
            "extraction_time": random.uniform(200, 800),
            "success_rate": 0.98
        }


class MockTreasuryAgent:
    """Simulates a treasury monitoring agent"""
    
    def monitor(self, addresses: List[str], threshold: float = 1000) -> Dict[str, Any]:
        """Monitor treasury addresses"""
        time.sleep(random.uniform(0.5, 1.5))  # Simulate blockchain calls
        
        total_balance = sum(random.uniform(1000, 50000) for _ in addresses)
        alerts = []
        
        if total_balance / len(addresses) < threshold:
            alerts.append({
                "type": "LOW_AVERAGE_BALANCE",
                "severity": "medium",
                "message": f"Average balance below {threshold}"
            })
        
        return {
            "addresses_monitored": len(addresses),
            "total_balance": round(total_balance, 2),
            "alerts": alerts,
            "last_block": random.randint(1000000, 2000000)
        }


def demo_header(title: str):
    """Print a demo section header"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}\n")


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║     🛡️  TrustWrapper - Your AI Agents, Now With Trust   ║
║                                                          ║
║     Add ZK-verified trust to ANY agent in 3 lines       ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Demo 1: Event Discovery
    demo_header("Demo 1: Event Discovery Agent")
    
    event_agent = MockEventAgent()
    trusted_event_agent = ZKTrustWrapper(event_agent, "EventDiscoveryPro")
    
    urls = ["https://ethcc.io", "https://web3summit.com", "https://deficonf.org"]
    
    for url in urls:
        print(f"🔍 Extracting from {url}")
        result = trusted_event_agent.verified_execute(url)
        
        if result.data and "events" in result.data:
            print(f"   Found {len(result.data['events'])} events")
            print(f"   Execution verified in {result.metrics.execution_time_ms}ms")
            print(f"   Proof: {result.proof.proof_hash[:16]}...")
        print()
    
    print(f"✅ Total verifications: {trusted_event_agent.get_stats()['execution_count']}")
    
    # Demo 2: Web Scraper
    demo_header("Demo 2: Web Scraping Agent")
    
    scraper_agent = MockScraperAgent()
    trusted_scraper = ZKTrustWrapper(scraper_agent, "CompetitiveScraper")
    
    targets = ["competitor-prices", "market-data", "product-listings"]
    
    for target in targets:
        print(f"🌐 Scraping {target}")
        result = trusted_scraper.verified_execute(target, {"depth": 2})
        
        if result.metrics.success:
            print(f"   Extracted {result.data['data_points']} data points")
            print(f"   Success rate: {result.data['success_rate']:.1%}")
            print(f"   ZK verified ✓")
        print()
    
    # Demo 3: Treasury Monitor
    demo_header("Demo 3: Treasury Monitoring Agent")
    
    treasury_agent = MockTreasuryAgent()
    trusted_treasury = ZKTrustWrapper(treasury_agent, "TreasuryGuardian")
    
    configs = [
        {"name": "DAO Treasury", "addresses": ["0xabc...", "0xdef...", "0x123..."]},
        {"name": "Protocol Reserves", "addresses": ["0x456...", "0x789..."]},
    ]
    
    for config in configs:
        print(f"💰 Monitoring {config['name']}")
        result = trusted_treasury.verified_execute(config['addresses'], threshold=10000)
        
        if result.data:
            print(f"   Total Balance: ${result.data['total_balance']:,.2f}")
            print(f"   Alerts: {len(result.data['alerts'])}")
            print(f"   Proof generated without revealing addresses")
        print()
    
    # Summary
    demo_header("Summary: Universal Trust for Any Agent")
    
    print("🎯 Key Benefits Demonstrated:")
    print("- ✅ Same wrapper works with ALL agent types")
    print("- ✅ No modifications needed to existing agents")
    print("- ✅ Cryptographic proofs of execution")
    print("- ✅ Privacy preserved (methods & data hidden)")
    print("- ✅ Ready for Aleo blockchain integration")
    
    print("\n💡 Use Cases:")
    print("- API providers: Prove SLA compliance")
    print("- DeFi protocols: Verify bot performance")
    print("- Data vendors: Guarantee freshness")
    print("- Any AI agent: Build trust instantly")
    
    print("\n🚀 Get started: pip install trustwrapper")
    print("📖 Docs: github.com/lamassu-labs/trustwrapper")


if __name__ == "__main__":
    main()
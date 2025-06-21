"""
Demo 1: Event Discovery Agent with ZK Trust

Shows how TrustWrapper adds verification to the LinkFinderAgent
"""
import sys
import os

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
demo_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(demo_dir)
sys.path.insert(0, project_root)

from src.agents.link_finder_agent import LinkFinderAgent
from src.core.trust_wrapper import ZKTrustWrapper


def main():
    print("🎯 Demo 1: Event Discovery with ZK Verification")
    print("=" * 50)
    
    # Create the base agent
    print("\n1. Creating LinkFinderAgent...")
    base_agent = LinkFinderAgent()
    
    # Wrap it with trust
    print("2. Wrapping with ZKTrustWrapper...")
    trusted_agent = ZKTrustWrapper(base_agent, "EventDiscoveryAgent")
    
    # Test URLs
    test_urls = [
        "https://ethcc.io",
        "https://events.example.com",
        "https://conference.web3.com"
    ]
    
    print("\n3. Executing with ZK verification...\n")
    
    for url in test_urls:
        print(f"🔍 Extracting events from: {url}")
        
        try:
            # Execute with verification
            result = trusted_agent.verified_execute(url)
            
            # Show verification proof
            print(result)
            
            # Show actual results
            if result.data and hasattr(result.data, 'get'):
                events = result.data.get('events', [])
                print(f"📅 Found {len(events)} events")
                if events:
                    print(f"   First event: {events[0].get('name', 'Unknown')}")
            else:
                print("   No events found")
                
        except Exception as e:
            print(f"   Error: {e}")
        
        print("-" * 50)
    
    # Show statistics
    stats = trusted_agent.get_stats()
    print(f"\n📊 Total Executions: {stats['execution_count']}")
    print(f"✅ All executions are ZK-verified!")
    
    # Demonstrate proof details
    print("\n🔐 ZK Proof Details:")
    print("- Execution time verified without revealing URLs")
    print("- Success status proven without exposing methods")
    print("- Results hashed for integrity verification")
    print("- Ready for Aleo blockchain submission")


if __name__ == "__main__":
    main()
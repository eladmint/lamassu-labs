"""
TrustWrapper Demo Suite - Run all three demos

Shows how ANY AI agent can be enhanced with ZK verification
"""
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.trust_wrapper import ZKTrustWrapper


def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🛡️  TrustWrapper - Your AI Agents, Now With Trust   ║
    ║                                                          ║
    ║     Add ZK-verified trust to ANY agent in 3 lines:      ║
    ║                                                          ║
    ║     agent = YourAgent()                                  ║
    ║     trusted = ZKTrustWrapper(agent)                      ║
    ║     result = trusted.verified_execute()                  ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)


def run_demo_with_timing(demo_name: str, demo_module: str):
    """Run a demo and time it"""
    print(f"\n{'='*60}")
    print(f"🚀 Running {demo_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        if demo_module == "event":
            from demo_event_wrapper import main
        elif demo_module == "scraper":
            from demo_scraper_wrapper import main
        elif demo_module == "treasury":
            from demo_treasury_wrapper import main
        
        main()
        
    except Exception as e:
        print(f"Error in {demo_name}: {e}")
    
    elapsed = time.time() - start_time
    print(f"\n⏱️  Demo completed in {elapsed:.2f} seconds")
    
    return elapsed


def main():
    print_banner()
    
    print("\n📋 Demo Overview:")
    print("1. Event Discovery Agent - Web3 conference extraction")
    print("2. Web Scraper Agent - Competitive intelligence gathering")
    print("3. Treasury Monitor - DeFi protocol monitoring")
    print("\nEach demo shows the SAME wrapper working with DIFFERENT agents!")
    
    input("\nPress Enter to start the demos...")
    
    # Run all demos
    total_time = 0
    
    # Demo 1: Event Discovery
    total_time += run_demo_with_timing("Demo 1: Event Discovery", "event")
    input("\nPress Enter for next demo...")
    
    # Demo 2: Web Scraper
    total_time += run_demo_with_timing("Demo 2: Web Scraping", "scraper")
    input("\nPress Enter for next demo...")
    
    # Demo 3: Treasury Monitor
    total_time += run_demo_with_timing("Demo 3: Treasury Monitor", "treasury")
    
    # Summary
    print(f"\n{'='*60}")
    print("🏆 Demo Summary")
    print(f"{'='*60}")
    
    print(f"\n✅ All 3 demos completed in {total_time:.2f} seconds")
    print("\n🔑 Key Takeaways:")
    print("- ONE wrapper works with ANY agent")
    print("- NO changes needed to existing agents")
    print("- Instant trust and verification")
    print("- Ready for Aleo blockchain integration")
    
    print("\n🎯 Use Cases:")
    print("- API providers: Prove SLA compliance")
    print("- Data vendors: Verify data freshness")
    print("- Trading bots: Prove performance metrics")
    print("- Research tools: Verify computation integrity")
    
    print("\n💡 Why ZK is Essential:")
    print("- Prove performance WITHOUT revealing methods")
    print("- Verify success WITHOUT exposing data")
    print("- Build trust WITHOUT sacrificing secrets")
    
    print("\n🚀 Get Started:")
    print("pip install trustwrapper  # Coming soon!")
    print("Visit: github.com/lamassu-labs/trustwrapper")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
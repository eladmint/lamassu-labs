"""
Example usage of Lamassu Labs AI Agents

This demonstrates how AI agents can be used for web automation tasks
that could be verified using zero-knowledge proofs in the marketplace.
"""

import asyncio
import logging
from ..agents import LinkFinderAgent, EvasionLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def demo_link_finder():
    """Demonstrate the LinkFinderAgent discovering events from a calendar page"""
    
    # Initialize the agent with advanced anti-bot evasion
    agent = LinkFinderAgent(
        name="DemoLinkFinder",
        evasion_level=EvasionLevel.ADVANCED,
        luma_optimization=True
    )
    
    # Example calendar URL (replace with actual URL for testing)
    calendar_url = "https://lu.ma/calendar/example"
    
    try:
        # Run the agent to discover event links
        logger.info(f"Starting link discovery for: {calendar_url}")
        events = await agent.run_async(calendar_url)
        
        # Display results
        logger.info(f"Found {len(events)} events:")
        for event in events:
            logger.info(f"  - {event['name']}: {event['url']}")
            
        return events
        
    except Exception as e:
        logger.error(f"Error during link discovery: {e}")
        return []


async def demo_agent_metrics():
    """Demonstrate how agent performance could be measured for ZK proofs"""
    
    # This would be part of the ZK verification system
    # Agents prove their performance without revealing implementation details
    
    metrics = {
        "accuracy": 0.95,  # 95% success rate
        "latency": 1.2,    # 1.2 seconds average
        "cost_efficiency": 0.8,  # 80% cost efficiency
        "total_tasks": 1000  # Completed 1000 tasks
    }
    
    logger.info("Agent Performance Metrics (for ZK verification):")
    for key, value in metrics.items():
        logger.info(f"  {key}: {value}")
    
    # In the actual implementation, these metrics would be:
    # 1. Generated from real agent performance
    # 2. Converted to ZK proofs using Leo
    # 3. Verified on Aleo blockchain
    # 4. Displayed in the marketplace with privacy preserved


async def main():
    """Run demonstration"""
    logger.info("=== Lamassu Labs AI Agent Demo ===")
    
    # Demo 1: Link discovery (commented out to avoid actual web requests)
    # await demo_link_finder()
    
    # Demo 2: Performance metrics for ZK proofs
    await demo_agent_metrics()
    
    logger.info("\nThis demonstrates how AI agents in Lamassu Labs can:")
    logger.info("1. Perform web automation tasks (link discovery, data extraction)")
    logger.info("2. Generate performance metrics for ZK verification")
    logger.info("3. Prove capabilities without revealing implementation")
    logger.info("4. Enable a privacy-preserving AI agent marketplace")


if __name__ == "__main__":
    asyncio.run(main())
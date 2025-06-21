"""
Demo: Wrapping Real External Agents with TrustWrapper

This demo shows how TrustWrapper works with actual production agents from:
1. Nuru AI - Event extraction agents
2. Agent Forge - Various specialized agents
3. Popular Python libraries
"""
import sys
import os

# Add parent directory and external paths to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '/Users/eladm/Projects/token/tokenhunter')
sys.path.insert(0, '/Users/eladm/Projects/token/tokenhunter/agent_forge/agent_forge_public')

from src.core.trust_wrapper import ZKTrustWrapper


def demo_section(title: str):
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}\n")


def try_nuru_agents():
    """Try wrapping Nuru AI extraction agents"""
    demo_section("Nuru AI Extraction Agents")
    
    try:
        # Try to import Nuru's event extractor
        from src.extraction.agents.event_data_extractor_agent import EventDataExtractorAgent
        
        print("✅ Found EventDataExtractorAgent from Nuru AI")
        
        # Create and wrap the agent
        extractor = EventDataExtractorAgent()
        trusted_extractor = ZKTrustWrapper(extractor, "NuruEventExtractor")
        
        print(f"   Wrapped successfully: {trusted_extractor}")
        print("   This agent extracts structured event data from web pages")
        print("   Now it can prove extraction accuracy without revealing sources")
        
    except ImportError as e:
        print(f"   Could not import Nuru agents: {e}")
        print("   (This is normal if running outside Nuru environment)")
    
    try:
        # Try the visual intelligence agent
        from src.extraction.agents.advanced_visual_intelligence_agent import AdvancedVisualIntelligenceAgent
        
        print("\n✅ Found AdvancedVisualIntelligenceAgent")
        visual_agent = AdvancedVisualIntelligenceAgent()
        trusted_visual = ZKTrustWrapper(visual_agent, "VisualIntelligencePro")
        
        print(f"   Wrapped successfully: {trusted_visual}")
        print("   This agent analyzes images from events")
        print("   Now it can prove image analysis without exposing the images")
        
    except ImportError:
        pass


def try_agent_forge_agents():
    """Try wrapping Agent Forge example agents"""
    demo_section("Agent Forge Example Agents")
    
    try:
        # Simple text extraction agent
        from examples.text_extraction.text_extraction_agent import TextExtractionAgent
        
        print("✅ Found TextExtractionAgent from Agent Forge")
        text_agent = TextExtractionAgent()
        trusted_text = ZKTrustWrapper(text_agent, "TextExtractorPro")
        
        print(f"   Wrapped successfully: {trusted_text}")
        print("   Now with ZK-verified text extraction")
        
    except ImportError:
        pass
    
    try:
        # Page scraper agent
        from examples.page_scraper.page_scraper_agent import PageScraperAgent
        
        print("\n✅ Found PageScraperAgent from Agent Forge")
        scraper = PageScraperAgent()
        trusted_scraper = ZKTrustWrapper(scraper, "PageScraperVerified")
        
        print(f"   Wrapped successfully: {trusted_scraper}")
        print("   Web scraping with cryptographic proof of success")
        
    except ImportError:
        pass


def try_popular_libraries():
    """Show how TrustWrapper works with any Python code"""
    demo_section("Popular Python Libraries as 'Agents'")
    
    # Example 1: Requests library
    try:
        import requests
        
        class RequestsAgent:
            """Wrapper to make requests library look like an agent"""
            def fetch(self, url: str):
                response = requests.get(url, timeout=5)
                return {
                    "status_code": response.status_code,
                    "content_length": len(response.content),
                    "headers": dict(response.headers)
                }
        
        print("✅ Created RequestsAgent from requests library")
        req_agent = RequestsAgent()
        trusted_requests = ZKTrustWrapper(req_agent, "HTTPFetcher")
        
        print(f"   Wrapped successfully: {trusted_requests}")
        print("   HTTP requests now have ZK proof of response")
        
    except ImportError:
        print("   requests library not available")
    
    # Example 2: Beautiful Soup
    try:
        from bs4 import BeautifulSoup
        
        class SoupAgent:
            """HTML parser as an agent"""
            def parse(self, html: str):
                soup = BeautifulSoup(html, 'html.parser')
                return {
                    "title": soup.title.string if soup.title else None,
                    "links": len(soup.find_all('a')),
                    "images": len(soup.find_all('img')),
                    "text_length": len(soup.get_text())
                }
        
        print("\n✅ Created SoupAgent from BeautifulSoup")
        soup_agent = SoupAgent()
        trusted_soup = ZKTrustWrapper(soup_agent, "HTMLParser")
        
        print(f"   Wrapped successfully: {trusted_soup}")
        print("   HTML parsing with verified element counts")
        
    except ImportError:
        print("   BeautifulSoup not available")


def try_langchain_agents():
    """Try wrapping LangChain agents"""
    demo_section("LangChain Agents (if available)")
    
    try:
        from langchain.agents import create_react_agent
        
        class LangChainWrapper:
            """Wrapper for LangChain agents"""
            def __init__(self, agent):
                self.agent = agent
            
            def run(self, query: str):
                return self.agent.invoke({"input": query})
        
        print("✅ LangChain detected - any LangChain agent can be wrapped!")
        print("   Example: trusted_agent = ZKTrustWrapper(LangChainWrapper(your_agent))")
        print("   Now LLM agents can prove their reasoning without revealing prompts")
        
    except ImportError:
        print("   LangChain not installed (pip install langchain to try)")


def show_universal_examples():
    """Show that ANY Python object with methods can be wrapped"""
    demo_section("Universal Examples - Wrap Anything!")
    
    # Example: Database query agent
    class DatabaseAgent:
        def query(self, sql: str):
            # Simulate DB query
            return {"rows": 42, "execution_time": 0.023}
    
    db_agent = DatabaseAgent()
    trusted_db = ZKTrustWrapper(db_agent, "SecureDB")
    print(f"✅ Database queries: {trusted_db}")
    
    # Example: ML model agent
    class MLModelAgent:
        def predict(self, data):
            # Simulate prediction
            return {"prediction": 0.87, "confidence": 0.92}
    
    ml_agent = MLModelAgent()
    trusted_ml = ZKTrustWrapper(ml_agent, "MLPredictor")
    print(f"✅ ML predictions: {trusted_ml}")
    
    # Example: Trading bot
    class TradingBot:
        def analyze(self, market_data):
            return {"signal": "BUY", "confidence": 0.75}
    
    trader = TradingBot()
    trusted_trader = ZKTrustWrapper(trader, "CryptoTrader")
    print(f"✅ Trading signals: {trusted_trader}")
    
    print("\n💡 The pattern is simple:")
    print("   1. Take ANY object with methods")
    print("   2. Wrap with ZKTrustWrapper")
    print("   3. Now it has ZK-verified execution!")


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║                 TrustWrapper                             ║
║        Works with ANY External Agent                     ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Try various external agents
    try_nuru_agents()
    try_agent_forge_agents()
    try_popular_libraries()
    try_langchain_agents()
    show_universal_examples()
    
    # Summary
    demo_section("Summary: Universal Trust Layer")
    
    print("🎯 TrustWrapper works with:")
    print("- ✅ Nuru AI extraction agents")
    print("- ✅ Agent Forge browser agents")
    print("- ✅ LangChain LLM agents")
    print("- ✅ Any Python library (requests, BeautifulSoup, etc)")
    print("- ✅ Custom trading bots")
    print("- ✅ ML models")
    print("- ✅ Database clients")
    print("- ✅ Literally ANY Python object with methods!")
    
    print("\n🔑 Key insight: You don't need special 'agent' libraries.")
    print("   ANY code that does work can be wrapped for trust!")
    
    print("\n📦 To use with your code:")
    print("   from trustwrapper import ZKTrustWrapper")
    print("   trusted = ZKTrustWrapper(your_code)")
    print("   result = trusted.execute()  # Now with ZK proof!")


if __name__ == "__main__":
    main()
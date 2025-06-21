"""
Demo: Wrapping the requests library with TrustWrapper

Shows how ANY Python library becomes a trusted agent
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.trust_wrapper import ZKTrustWrapper


class RequestsAgent:
    """
    Wrapper that makes the requests library behave like an agent.
    This shows how ANY library can be wrapped for trust.
    """
    
    def __init__(self):
        self.name = "HTTPRequestAgent"
        self.session = None
    
    def fetch(self, url: str, headers: dict = None) -> dict:
        """
        Fetch a URL and return structured data.
        In production, this would use the actual requests library.
        """
        # For demo, we'll simulate the requests library behavior
        # In real use: import requests; response = requests.get(url)
        
        # Simulate different responses based on URL
        if "api.github.com" in url:
            return {
                "status_code": 200,
                "content_length": 1234,
                "headers": {"content-type": "application/json"},
                "data": {"repos": 42, "stars": 1337}
            }
        elif "api.coingecko.com" in url:
            return {
                "status_code": 200,
                "content_length": 567,
                "headers": {"content-type": "application/json"},
                "data": {"bitcoin": {"usd": 45000}}
            }
        elif "error" in url:
            raise Exception("Connection timeout")
        else:
            return {
                "status_code": 404,
                "content_length": 0,
                "headers": {},
                "data": None
            }
    
    def post(self, url: str, data: dict) -> dict:
        """POST request method"""
        return {
            "status_code": 201,
            "content_length": len(json.dumps(data)),
            "headers": {"content-type": "application/json"},
            "data": {"id": "12345", "created": True}
        }


def main():
    print("🌐 Demo: HTTP Requests with ZK Trust\n")
    
    # Create the requests wrapper
    print("1. Creating RequestsAgent (wraps requests library)...")
    http_agent = RequestsAgent()
    
    # Add trust with ZKTrustWrapper
    print("2. Adding ZK trust layer...")
    trusted_http = ZKTrustWrapper(http_agent, "TrustedHTTP")
    
    print("3. Making verified HTTP requests:\n")
    
    # Test various endpoints
    test_urls = [
        ("https://api.github.com/users/torvalds", "GitHub API"),
        ("https://api.coingecko.com/simple/price?ids=bitcoin", "CoinGecko API"),
        ("https://api.example.com/not-found", "404 Example"),
        ("https://timeout.error.com", "Error Example")
    ]
    
    for url, description in test_urls:
        print(f"📡 Fetching: {description}")
        print(f"   URL: {url}")
        
        try:
            # Execute with ZK verification
            result = trusted_http.verified_execute(url)
            
            # Show verification
            if result.metrics.success:
                data = result.data
                print(f"   ✅ Status: {data['status_code']}")
                print(f"   📊 Size: {data['content_length']} bytes")
                print(f"   ⏱️  Time: {result.metrics.execution_time_ms}ms")
                print(f"   🔐 Proof: {result.proof.proof_hash[:16]}...")
            else:
                print(f"   ❌ Failed: {result.metrics.error_message}")
                print(f"   🔐 Failure proof: {result.proof.proof_hash[:16]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    # Show POST example
    print("📤 POST Request Example:")
    post_data = {"name": "TrustWrapper", "type": "ZK-verification"}
    result = trusted_http.verified_execute("https://api.example.com/create", post_data)
    print(f"   Created resource with proof: {result.proof.proof_hash[:16]}...")
    
    # Show statistics
    stats = trusted_http.get_stats()
    print(f"\n📊 HTTP Agent Statistics:")
    print(f"- Total Requests: {stats['execution_count']}")
    print(f"- All requests ZK-verified ✅")
    
    print("\n💡 Key Benefits:")
    print("- API endpoints remain private")
    print("- Response times proven without showing data")
    print("- Failures are cryptographically verified")
    print("- Perfect for API monitoring & SLA compliance")
    
    print("\n🔑 This works with ANY HTTP library:")
    print("- requests")
    print("- httpx") 
    print("- aiohttp")
    print("- urllib")
    print("- Or any custom HTTP client!")


if __name__ == "__main__":
    main()
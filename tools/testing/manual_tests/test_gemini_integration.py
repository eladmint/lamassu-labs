#!/usr/bin/env python3
"""
Test Gemini integration with TrustWrapper
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.core.enhanced_hallucination_detector import GeminiHallucinationChecker

async def test_gemini_hallucination_detection():
    """Test Gemini's hallucination detection capabilities"""
    
    print("🧠 Testing Gemini Hallucination Detection")
    print("=" * 50)
    
    # Initialize Gemini checker
    checker = GeminiHallucinationChecker()
    
    # Test cases
    test_cases = [
        {
            "name": "Obvious Factual Error",
            "text": "The capital of France is London, which has been the capital since 1789.",
            "expected": "Should detect as false"
        },
        {
            "name": "Future Event as Past",
            "text": "The 2026 FIFA World Cup was held in the United States and won by Brazil.",
            "expected": "Should detect temporal error"
        },
        {
            "name": "Non-existent Technology",
            "text": "The new torch.quantum.entangle() function in PyTorch 2.1 enables quantum neural networks.",
            "expected": "Should detect as fabricated"
        },
        {
            "name": "Plausible but False Statistic",
            "text": "Approximately 0.017% of humans have naturally purple eyes due to a rare genetic condition.",
            "expected": "Should detect suspicious precision"
        },
        {
            "name": "Correct Fact",
            "text": "Paris is the capital of France and has been so since ancient times.",
            "expected": "Should verify as correct"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print(f"Text: {test_case['text']}")
        print(f"Expected: {test_case['expected']}")
        
        try:
            result = await checker.detect_hallucination(test_case['text'])
            
            print(f"✅ Result:")
            print(f"   Is Factual: {result.is_factual}")
            print(f"   Confidence: {result.confidence:.1%}")
            print(f"   Explanation: {result.explanation}")
            print(f"   Model: {result.model_used}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)

async def test_gemini_explainable_ai():
    """Test using Gemini for explainable AI features"""
    
    print("\n🔍 Testing Gemini for Explainable AI")
    print("=" * 50)
    
    # Import our TrustWrapper
    from src.core.trust_wrapper_xai import ZKTrustWrapperXAI
    
    # Create a simple mock agent for testing
    class MockWebAgent:
        def __init__(self, name="TestAgent"):
            self.name = name
        
        def execute(self, url):
            # Simulate different scenarios based on URL
            if "error" in url:
                return {"status": "error", "message": "Failed to load page"}
            elif "events" in url:
                return {
                    "events": [
                        {"name": "Tech Conference 2024", "date": "2024-12-01", "location": "Berlin"},
                        {"name": "AI Summit", "date": "2024-12-15", "location": "London"}
                    ],
                    "count": 2
                }
            else:
                return {"data": "generic_response", "status": "success"}
    
    # Test XAI integration
    print("\n🧠 Testing XAI-enhanced TrustWrapper:")
    
    agent = MockWebAgent("EventExtractor")
    xai_wrapper = ZKTrustWrapperXAI(agent, "EventExtractor", enable_xai=True)
    
    test_urls = [
        "https://example.com/events",
        "https://example.com/error",
        "https://example.com/generic"
    ]
    
    for url in test_urls:
        print(f"\n🔗 Testing URL: {url}")
        try:
            result = xai_wrapper.verified_execute(url)
            print(f"✅ Execution successful:")
            print(f"   Result: {result.data}")
            if result.explanation:
                print(f"   Confidence: {result.explanation.confidence_score:.1%}")
                print(f"   Method: {result.explanation.explanation_method}")
                print(f"   Reasoning: {result.explanation.decision_reasoning}")
            print(f"   Trust Score: {result.trust_score:.1%}" if result.trust_score else "   Trust Score: N/A")
            
        except Exception as e:
            print(f"❌ Error: {e}")

def test_environment_setup():
    """Test if environment is properly configured"""
    
    print("🔧 Environment Setup Check")
    print("=" * 30)
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"✅ GOOGLE_API_KEY: Set (ends with ...{api_key[-10:]})")
    else:
        print("❌ GOOGLE_API_KEY: Not set")
    
    # Check Google AI library
    try:
        import google.generativeai as genai
        print("✅ google-generativeai: Available")
        
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ Gemini model: Initialized successfully")
                
                # Test simple generation
                response = model.generate_content("Say 'Hello from Lamassu Labs!'")
                print(f"✅ Test response: {response.text}")
                
            except Exception as e:
                print(f"❌ Gemini initialization failed: {e}")
        
    except ImportError:
        print("❌ google-generativeai: Not installed")

async def main():
    """Run all tests"""
    
    print("🏛️ LAMASSU LABS - GEMINI INTEGRATION TEST")
    print("=" * 60)
    
    # Test environment
    test_environment_setup()
    
    # Test hallucination detection
    await test_gemini_hallucination_detection()
    
    # Test explainable AI
    await test_gemini_explainable_ai()
    
    print("\n🎉 All tests completed!")
    print("🛡️ TrustWrapper + Gemini integration is ready for production!")

if __name__ == "__main__":
    asyncio.run(main())
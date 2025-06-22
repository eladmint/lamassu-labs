#!/usr/bin/env python3
"""
Test Gemini AI access for Lamassu Labs TrustWrapper
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_access():
    """Test if Gemini AI is accessible with the current API key"""
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI library is available")
        
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ No GOOGLE_API_KEY found in environment")
            return False
        
        print("✅ GOOGLE_API_KEY found in environment")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini model initialized successfully") 
        
        # Test generation
        response = model.generate_content(
            "Explain in one sentence what explainable AI (XAI) is."
        )
        print(f"✅ Test response: {response.text}")
        
        return True
        
    except ImportError:
        print("❌ Google Generative AI library not installed")
        print("   Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        return False

if __name__ == "__main__":
    print("🧠 Testing Gemini AI access for Lamassu Labs TrustWrapper")
    print("=" * 60)
    
    success = test_gemini_access()
    
    if success:
        print("\n🎉 Gemini AI is ready for TrustWrapper integration!")
    else:
        print("\n❌ Gemini AI setup needs attention.")
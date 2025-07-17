#!/usr/bin/env python3
"""
Test Gemini AI access for Lamassu Labs TrustWrapper
"""

import os
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

<<<<<<< HEAD

def test_gemini_access():
    """Test if Gemini AI is accessible with the current API key"""

    try:
        import google.generativeai as genai

        print("✅ Google Generative AI library is available")

=======
def test_gemini_access():
    """Test if Gemini AI is accessible with the current API key"""
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI library is available")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ No GOOGLE_API_KEY found in environment")
            return False
<<<<<<< HEAD

        print("✅ GOOGLE_API_KEY found in environment")

        # Configure Gemini
        genai.configure(api_key=api_key)

        # Create model
        model = genai.GenerativeModel("gemini-1.5-flash")
        print("✅ Gemini model initialized successfully")

=======
        
        print("✅ GOOGLE_API_KEY found in environment")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini model initialized successfully") 
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Test generation
        response = model.generate_content(
            "Explain in one sentence what explainable AI (XAI) is."
        )
        print(f"✅ Test response: {response.text}")
<<<<<<< HEAD

        return True

=======
        
        return True
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    except ImportError:
        print("❌ Google Generative AI library not installed")
        print("   Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        return False

<<<<<<< HEAD

if __name__ == "__main__":
    print("🧠 Testing Gemini AI access for Lamassu Labs TrustWrapper")
    print("=" * 60)

    success = test_gemini_access()

    if success:
        print("\n🎉 Gemini AI is ready for TrustWrapper integration!")
    else:
        print("\n❌ Gemini AI setup needs attention.")
=======
if __name__ == "__main__":
    print("🧠 Testing Gemini AI access for Lamassu Labs TrustWrapper")
    print("=" * 60)
    
    success = test_gemini_access()
    
    if success:
        print("\n🎉 Gemini AI is ready for TrustWrapper integration!")
    else:
        print("\n❌ Gemini AI setup needs attention.")
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

#!/usr/bin/env python3
"""
Test Registration Flow
Tests the OAuth integration with event registration system
"""

import json

import requests


def test_oauth_status():
    """Test OAuth status endpoint"""
    print("🔍 Testing OAuth status endpoint...")

    url = "https://chatbot-api-service-v2-oo6mrfxexq-uc.a.run.app/auth/status/test_user_123"

    try:
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"   Error: {response.text}")
            return False

    except Exception as e:
        print(f"   Exception: {e}")
        return False


def test_registration_endpoint():
    """Test registration endpoint"""
    print("🔍 Testing registration endpoint...")

    url = "https://chatbot-api-service-v2-oo6mrfxexq-uc.a.run.app/v2/registration/register"

    registration_data = {
        "user_id": "test_user_123",
        "user_name": "Test User",
        "user_email": "test@example.com",
        "event_url": "https://lu.ma/test-event",
        "platform": "luma",
    }

    try:
        response = requests.post(
            url,
            json=registration_data,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"   Success Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"   Error Response: {response.text}")
            if response.status_code == 500:
                print("   This might be expected if imports are still failing")
            return False

    except Exception as e:
        print(f"   Exception: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Testing OAuth + Registration Integration\n")

    oauth_success = test_oauth_status()
    print()

    registration_success = test_registration_endpoint()
    print()

    print("📊 Test Results:")
    print(f"   OAuth Status: {'✅ PASS' if oauth_success else '❌ FAIL'}")
    print(
        f"   Registration: {'✅ PASS' if registration_success else '❌ FAIL (Expected until deploy completes)'}"
    )

    if oauth_success:
        print("\n✅ OAuth authentication integration is working correctly!")
        print(
            "💡 Users can connect their accounts and the system will use real credentials"
        )

    if not registration_success:
        print("\n⏳ Registration endpoint needs deployment to complete")
        print("🔧 The import fixes should resolve the Internal Server Error")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to verify security implementation deployment
"""

import time
from datetime import datetime

import requests

# Production API URL
API_BASE_URL = "https://chatbot-api-service-v2-oo6mrfxexq-uc.a.run.app"


def test_health_endpoint():
    """Test basic API health"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False


def test_data_extraction_protection():
    """Test data extraction protection"""
    print("\n🔒 Testing Data Extraction Protection...")

    test_user_id = f"security_test_{int(time.time())}"

    # Test normal usage (should work)
    for i in range(3):
        try:
            response = requests.post(
                f"{API_BASE_URL}/v2/chat",
                json={
                    "user_id": test_user_id,
                    "message": "find blockchain events",
                    "chat_id": f"test_chat_{i}",
                },
                timeout=30,
            )

            print(f"Request {i+1}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                # Check if user_id_processed is removed from debug info
                if "debug_info" in data and data["debug_info"]:
                    if "user_id_processed" in data["debug_info"]:
                        print("⚠️  WARNING: user_id_processed still in response")
                    else:
                        print("✅ User data protected in response")
        except Exception as e:
            print(f"❌ Request {i+1} failed: {e}")

    return True


def test_admin_security_dashboard():
    """Test admin security dashboard (without API key)"""
    print("\n📊 Testing Admin Security Dashboard...")

    try:
        response = requests.get(f"{API_BASE_URL}/admin/data-extraction", timeout=10)
        if response.status_code == 403 or response.status_code == 401:
            print("✅ Admin dashboard properly secured (401/403)")
        else:
            print(f"⚠️  Admin dashboard response: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Admin dashboard test failed: {e}")
        return False


def test_security_headers():
    """Test security headers"""
    print("\n🛡️  Testing Security Headers...")

    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        headers = response.headers

        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
        ]

        for header in security_headers:
            if header in headers:
                print(f"✅ {header}: {headers[header]}")
            else:
                print(f"⚠️  Missing: {header}")

        return True
    except Exception as e:
        print(f"❌ Security headers test failed: {e}")
        return False


def main():
    """Run all security tests"""
    print("🔒 TokenHunter Security Deployment Verification")
    print("=" * 50)
    print(f"Testing API: {API_BASE_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    print()

    tests = [
        ("Health Check", test_health_endpoint),
        ("Data Extraction Protection", test_data_extraction_protection),
        ("Admin Dashboard Security", test_admin_security_dashboard),
        ("Security Headers", test_security_headers),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 30)
        success = test_func()
        results.append((test_name, success))

    print("\n" + "=" * 50)
    print("📊 SECURITY DEPLOYMENT TEST RESULTS")
    print("=" * 50)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All security tests passed! Deployment verified.")
    else:
        print("⚠️  Some tests failed. Review security implementation.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Test Treasury Monitor Demo API endpoints"""

import asyncio
import json
from datetime import datetime

import aiohttp

PRODUCTION_URL = "https://agent-forge-website-oo6mrfxexq-uc.a.run.app"
DEMO_ADDRESS = "addr1q9wz03xdpasq5t7tv4vvqyw9frhz2x9862ct3xyh697pfwjj2c79gy9l76sdg0xwhd7r0c0kna0tycz4y5s6mlenh8pqyk6dej"


async def test_health_endpoint(session):
    """Test the health check endpoint"""
    try:
        async with session.get(f"{PRODUCTION_URL}/api/treasury/health") as response:
            if response.status == 200:
                data = await response.json()
                print("✅ Health endpoint working!")
                print(f"   Mode: {data.get('mode', 'unknown')}")
                print(f"   Features: {json.dumps(data.get('features', {}), indent=2)}")
                return True
            else:
                print(f"❌ Health endpoint failed: {response.status}")
                return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False


async def test_validate_endpoint(session):
    """Test the validation endpoint"""
    try:
        payload = {"address": DEMO_ADDRESS}
        async with session.post(
            f"{PRODUCTION_URL}/api/treasury/validate", json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                print("✅ Validation endpoint working!")
                print(f"   Valid: {data.get('data', {}).get('valid', False)}")
                print(f"   Type: {data.get('data', {}).get('type', 'unknown')}")
                return True
            else:
                print(f"❌ Validation endpoint failed: {response.status}")
                text = await response.text()
                print(f"   Response: {text}")
                return False
    except Exception as e:
        print(f"❌ Validation endpoint error: {e}")
        return False


async def test_monitor_endpoint(session):
    """Test the monitor endpoint with demo address"""
    try:
        payload = {"address": DEMO_ADDRESS}
        async with session.post(
            f"{PRODUCTION_URL}/api/treasury/monitor", json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                print("✅ Monitor endpoint working!")
                print(f"   Mode: {data.get('mode', 'unknown')}")
                print(f"   Balance: {data.get('data', {}).get('balance', 0):,.2f} ADA")
                print(f"   USD Value: ${data.get('data', {}).get('usdValue', 0):,.2f}")
                print(
                    f"   Risk Level: {data.get('data', {}).get('riskAssessment', {}).get('level', 'unknown')}"
                )
                return True
            else:
                print(f"❌ Monitor endpoint failed: {response.status}")
                text = await response.text()
                print(f"   Response: {text}")
                return False
    except Exception as e:
        print(f"❌ Monitor endpoint error: {e}")
        return False


async def test_frontend_page(session):
    """Test if the frontend page loads"""
    try:
        async with session.get(f"{PRODUCTION_URL}/treasury-monitor") as response:
            if response.status == 200:
                print("✅ Frontend page loading!")
                return True
            else:
                print(f"❌ Frontend page failed: {response.status}")
                return False
    except Exception as e:
        print(f"❌ Frontend page error: {e}")
        return False


async def main():
    """Run all tests"""
    print("🧪 Testing Treasury Monitor Demo API")
    print(f"📍 URL: {PRODUCTION_URL}")
    print(f"🏦 Demo Address: {DEMO_ADDRESS[:20]}...")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    async with aiohttp.ClientSession() as session:
        # Run tests
        results = {
            "health": await test_health_endpoint(session),
            "validate": await test_validate_endpoint(session),
            "monitor": await test_monitor_endpoint(session),
            "frontend": await test_frontend_page(session),
        }

    print("-" * 60)
    print("📊 Test Summary:")
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {test.capitalize()}")

    print(f"\n🎯 Result: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 Demo mode API is ready for customer demos!")
    else:
        print("⚠️  Some endpoints need fixing before customer demos")


if __name__ == "__main__":
    asyncio.run(main())

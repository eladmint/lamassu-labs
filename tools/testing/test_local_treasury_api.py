#!/usr/bin/env python3
"""Test Treasury Monitor Local API with real and demo data"""

import asyncio
from datetime import datetime

import aiohttp

LOCAL_URL = "http://localhost:3001"
DEMO_ADDRESS = "addr1q9wz03xdpasq5t7tv4vvqyw9frhz2x9862ct3xyh697pfwjj2c79gy9l76sdg0xwhd7r0c0kna0tycz4y5s6mlenh8pqyk6dej"
REAL_ADDRESS = "addr1qx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj0vs2qd4a6gtmradl5sx80uku"  # Known address with balance


async def test_api_endpoint(session, address, expected_mode=None):
    """Test monitoring endpoint with specific address"""
    try:
        payload = {"address": address}
        async with session.post(
            f"{LOCAL_URL}/api/treasury/monitor", json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                mode = data.get("mode", data.get("data", {}).get("mode", "unknown"))
                balance = data.get("data", {}).get("balance", 0)
                usd_value = data.get("data", {}).get("usdValue", 0)
                risk_level = (
                    data.get("data", {})
                    .get("riskAssessment", {})
                    .get("level", "unknown")
                )

                print(f"✅ Address: {address[:20]}...")
                print(f"   Mode: {mode}")
                print(f"   Balance: {balance:,.2f} ADA")
                print(f"   USD Value: ${usd_value:,.2f}")
                print(f"   Risk Level: {risk_level}")

                if expected_mode and mode == expected_mode:
                    print(f"   ✅ Correct mode: {mode}")
                elif expected_mode:
                    print(f"   ⚠️  Expected {expected_mode}, got {mode}")

                return True
            else:
                print(f"❌ API failed: {response.status}")
                text = await response.text()
                print(f"   Error: {text}")
                return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


async def main():
    """Test both demo and real data"""
    print("🧪 Testing Treasury Monitor Local API")
    print(f"📍 URL: {LOCAL_URL}")
    print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)

    async with aiohttp.ClientSession() as session:
        # Test health endpoint
        try:
            async with session.get(f"{LOCAL_URL}/api/treasury/health") as response:
                if response.status == 200:
                    health = await response.json()
                    print("✅ Health Check")
                    print(f"   Service: {health.get('service', 'unknown')}")
                    print(f"   Mode: {health.get('mode', 'unknown')}")
                    print(
                        f"   Real Blockchain: {health.get('features', {}).get('blockchainIntegration', False)}"
                    )
                else:
                    print("❌ Health check failed")
        except Exception as e:
            print(f"❌ Health check error: {e}")

        print("-" * 70)

        # Test demo address
        print("🎭 Testing Demo Address:")
        await test_api_endpoint(session, DEMO_ADDRESS, "demo")

        print("-" * 70)

        # Test real address
        print("🏦 Testing Real Address:")
        await test_api_endpoint(session, REAL_ADDRESS, "real")

        print("-" * 70)

        # Test random valid address (should fall back to demo)
        print("🔀 Testing Fallback (Random Address):")
        await test_api_endpoint(session, "addr1qxyz123", "demo_fallback")


if __name__ == "__main__":
    asyncio.run(main())

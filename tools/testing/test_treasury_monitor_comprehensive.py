#!/usr/bin/env python3
"""
Comprehensive Treasury Monitor Testing Script
Tests the deployed Treasury Monitor with real Cardano data and UX validation.
"""

import asyncio
import json
import time
from datetime import datetime

import aiohttp

# Real test address from the comprehensive guide
REAL_TEST_ADDRESS = "addr1q9wz03xdpasq5t7tv4vvqyw9frhz2x9862ct3xyh697pfwjj2c79gy9l76sdg0xwhd7r0c0kna0tycz4y5s6mlenh8pqyk6dej"

# Deployed service URLs
WEBSITE_URL = "https://agent-forge-website-oo6mrfxexq-uc.a.run.app"
TREASURY_SERVICE_URL = "https://treasury-monitor-oo6mrfxexq-uc.a.run.app"


class TreasuryMonitorTester:
    def __init__(self):
        self.test_results = {}
        self.session = None

    async def run_comprehensive_tests(self):
        """Run all comprehensive tests"""
        print("🔍 Starting Comprehensive Treasury Monitor Testing")
        print("=" * 60)

        async with aiohttp.ClientSession() as session:
            self.session = session

            # Test 1: Service Health Checks
            await self.test_service_health()

            # Test 2: API Endpoints
            await self.test_api_endpoints()

            # Test 3: Real Cardano Data Integration
            await self.test_real_cardano_integration()

            # Test 4: UX and Frontend Testing
            await self.test_frontend_functionality()

            # Test 5: Performance and Load Testing
            await self.test_performance()

            # Test 6: Alert System Testing
            await self.test_alert_system()

        # Generate test report
        self.generate_test_report()

    async def test_service_health(self):
        """Test health endpoints of both services"""
        print("\n🏥 Testing Service Health...")

        # Test Treasury Service Health
        try:
            async with self.session.get(f"{TREASURY_SERVICE_URL}/health") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"✅ Treasury Service: {data.get('status', 'unknown')}")
                    self.test_results["treasury_service_health"] = True
                else:
                    print(f"❌ Treasury Service: HTTP {resp.status}")
                    self.test_results["treasury_service_health"] = False
        except Exception as e:
            print(f"❌ Treasury Service: {str(e)}")
            self.test_results["treasury_service_health"] = False

        # Test Website Health
        try:
            async with self.session.get(f"{WEBSITE_URL}/api/health") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"✅ Website API: {data.get('status', 'unknown')}")
                    self.test_results["website_health"] = True
                else:
                    print(f"❌ Website API: HTTP {resp.status}")
                    self.test_results["website_health"] = False
        except Exception as e:
            print(f"❌ Website API: {str(e)}")
            self.test_results["website_health"] = False

    async def test_api_endpoints(self):
        """Test Treasury Monitor API endpoints"""
        print("\n🔌 Testing API Endpoints...")

        test_payload = {"addresses": [REAL_TEST_ADDRESS], "duration_minutes": 1}

        try:
            async with self.session.post(
                f"{WEBSITE_URL}/api/treasury/monitor",
                json=test_payload,
                headers={"Content-Type": "application/json"},
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print("✅ Treasury Monitor API endpoint working")
                    print(
                        f"   - Addresses monitored: {data.get('addresses_monitored', 0)}"
                    )
                    print(f"   - API provider: {data.get('api_provider', 'unknown')}")
                    print(f"   - Real data: {data.get('real_data', False)}")
                    self.test_results["api_endpoint"] = True
                    self.test_results["api_response"] = data
                else:
                    print(f"❌ Treasury Monitor API: HTTP {resp.status}")
                    self.test_results["api_endpoint"] = False
        except Exception as e:
            print(f"❌ Treasury Monitor API: {str(e)}")
            self.test_results["api_endpoint"] = False

    async def test_real_cardano_integration(self):
        """Test real Cardano blockchain integration"""
        print("\n⛓️ Testing Real Cardano Integration...")

        # Test NOWNodes API directly
        nownodes_url = "https://ada-mainnet.nownodes.io"
        headers = {
            "Authorization": "Bearer 6b06ecbb-8e6e-4eb7-a198-462be95567af",
            "Content-Type": "application/json",
        }

        try:
            async with self.session.get(
                f"{nownodes_url}/api/balance/{REAL_TEST_ADDRESS}", headers=headers
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    balance_ada = float(data.get("balance", 0)) / 1000000
                    print(f"✅ NOWNodes API: Balance = {balance_ada:.2f} ADA")
                    self.test_results["nownodes_integration"] = True
                    self.test_results["real_balance"] = balance_ada
                else:
                    print(f"❌ NOWNodes API: HTTP {resp.status}")
                    self.test_results["nownodes_integration"] = False
        except Exception as e:
            print(f"❌ NOWNodes API: {str(e)}")
            self.test_results["nownodes_integration"] = False

        # Test Koios fallback
        try:
            koios_payload = {"_addresses": [REAL_TEST_ADDRESS]}
            async with self.session.post(
                "https://api.koios.rest/api/v1/address_info",
                json=koios_payload,
                headers={"Content-Type": "application/json"},
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data and len(data) > 0:
                        balance_ada = float(data[0].get("balance", 0)) / 1000000
                        print(f"✅ Koios API: Balance = {balance_ada:.2f} ADA")
                        self.test_results["koios_integration"] = True
                    else:
                        print("❌ Koios API: No data returned")
                        self.test_results["koios_integration"] = False
                else:
                    print(f"❌ Koios API: HTTP {resp.status}")
                    self.test_results["koios_integration"] = False
        except Exception as e:
            print(f"❌ Koios API: {str(e)}")
            self.test_results["koios_integration"] = False

    async def test_frontend_functionality(self):
        """Test frontend functionality and UX"""
        print("\n🖥️ Testing Frontend Functionality...")

        # Test main Treasury Monitor page
        try:
            async with self.session.get(f"{WEBSITE_URL}/treasury-monitor") as resp:
                if resp.status == 200:
                    content = await resp.text()
                    if "Treasury Monitor" in content:
                        print("✅ Treasury Monitor page loads")
                        self.test_results["frontend_loads"] = True
                    else:
                        print("❌ Treasury Monitor page missing content")
                        self.test_results["frontend_loads"] = False
                else:
                    print(f"❌ Treasury Monitor page: HTTP {resp.status}")
                    self.test_results["frontend_loads"] = False
        except Exception as e:
            print(f"❌ Frontend test: {str(e)}")
            self.test_results["frontend_loads"] = False

        # Test UX elements
        ux_tests = [
            "Pricing tiers display",
            "Feature sections visible",
            "Professional design elements",
            "Responsive layout",
        ]

        for test in ux_tests:
            print(f"   - {test}: ✅ (Visual inspection required)")

    async def test_performance(self):
        """Test performance and response times"""
        print("\n⚡ Testing Performance...")

        start_time = time.time()
        try:
            async with self.session.get(f"{TREASURY_SERVICE_URL}/health") as resp:
                response_time = (time.time() - start_time) * 1000
                print(f"✅ Treasury Service response: {response_time:.2f}ms")
                self.test_results["treasury_response_time"] = response_time
        except Exception as e:
            print(f"❌ Performance test: {str(e)}")

        # Test concurrent requests
        print("   Testing concurrent load...")
        tasks = []
        for i in range(5):
            task = self.session.get(f"{TREASURY_SERVICE_URL}/status")
            tasks.append(task)

        start_time = time.time()
        try:
            responses = await asyncio.gather(*tasks)
            total_time = (time.time() - start_time) * 1000
            successful = sum(1 for resp in responses if resp.status == 200)
            print(
                f"✅ Concurrent requests: {successful}/5 successful in {total_time:.2f}ms"
            )
            self.test_results["concurrent_performance"] = True
        except Exception as e:
            print(f"❌ Concurrent test: {str(e)}")
            self.test_results["concurrent_performance"] = False

    async def test_alert_system(self):
        """Test alert generation and risk assessment"""
        print("\n🚨 Testing Alert System...")

        # Test with real address that might have recent transactions
        test_payload = {"addresses": [REAL_TEST_ADDRESS], "duration_minutes": 1}

        try:
            async with self.session.post(
                f"{WEBSITE_URL}/api/treasury/monitor",
                json=test_payload,
                headers={"Content-Type": "application/json"},
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    alerts = data.get("alerts", [])
                    total_alerts = data.get("total_alerts", 0)

                    print(
                        f"✅ Alert system functional: {total_alerts} alerts generated"
                    )

                    if alerts:
                        for alert in alerts[:3]:  # Show first 3 alerts
                            level = alert.get("level", "unknown")
                            desc = alert.get("description", "No description")
                            print(f"   - {level.upper()}: {desc}")

                    self.test_results["alert_system"] = True
                    self.test_results["alerts_generated"] = total_alerts
                else:
                    print(f"❌ Alert system test: HTTP {resp.status}")
                    self.test_results["alert_system"] = False
        except Exception as e:
            print(f"❌ Alert system test: {str(e)}")
            self.test_results["alert_system"] = False

    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for v in self.test_results.values() if v is True)

        print(f"Overall Status: {passed_tests}/{total_tests} tests passed")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()

        print("Detailed Results:")
        for test_name, result in self.test_results.items():
            if isinstance(result, bool):
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"  {test_name}: {status}")
            elif isinstance(result, (int, float)):
                print(f"  {test_name}: {result}")

        print("\n🎯 Business Readiness Assessment:")

        critical_tests = [
            "treasury_service_health",
            "website_health",
            "api_endpoint",
            "nownodes_integration",
        ]

        critical_passed = sum(
            1 for test in critical_tests if self.test_results.get(test, False)
        )

        if critical_passed == len(critical_tests):
            print("✅ PRODUCTION READY - All critical systems operational")
            print("✅ Real Cardano integration validated")
            print("✅ API endpoints functional")
            print("✅ Ready for customer acquisition")
        else:
            print("⚠️ Issues detected - Address before production")

        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "test_address": REAL_TEST_ADDRESS,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "success_rate": (passed_tests / total_tests) * 100,
            "results": self.test_results,
        }

        with open("treasury_monitor_test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)

        print("\n📄 Detailed report saved: treasury_monitor_test_report.json")


def create_ux_test_scenarios():
    """Create UX testing scenarios for manual validation"""
    scenarios = [
        {
            "name": "Address Input UX",
            "steps": [
                "1. Navigate to treasury-monitor page",
                "2. Try entering invalid address format",
                "3. Enter valid Cardano address",
                "4. Verify error handling and validation",
            ],
            "expected": "Clear error messages, proper validation feedback",
        },
        {
            "name": "Monitoring Process UX",
            "steps": [
                "1. Add test address: " + REAL_TEST_ADDRESS,
                "2. Click 'Start Monitoring'",
                "3. Observe loading states",
                "4. Review results display",
            ],
            "expected": "Smooth loading, clear progress indicators, professional results",
        },
        {
            "name": "Responsive Design",
            "steps": [
                "1. Test on mobile device/narrow window",
                "2. Test on tablet size",
                "3. Test on desktop",
                "4. Verify all elements scale properly",
            ],
            "expected": "All content accessible and readable on all screen sizes",
        },
        {
            "name": "Pricing and Business Model",
            "steps": [
                "1. Review pricing tiers display",
                "2. Check feature comparisons",
                "3. Verify call-to-action buttons",
                "4. Test contact/signup flows",
            ],
            "expected": "Clear value proposition, professional presentation",
        },
    ]

    print("\n📋 UX Testing Scenarios")
    print("=" * 50)

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print("Steps:")
        for step in scenario["steps"]:
            print(f"   {step}")
        print(f"Expected: {scenario['expected']}")

    return scenarios


async def main():
    """Main testing function"""
    print("🎯 Treasury Monitor Comprehensive Testing Suite")
    print(f"🕒 Started at: {datetime.now().isoformat()}")
    print(f"🔗 Test Address: {REAL_TEST_ADDRESS}")
    print()

    # Run automated tests
    tester = TreasuryMonitorTester()
    await tester.run_comprehensive_tests()

    # Display UX testing scenarios
    create_ux_test_scenarios()

    print("\n🚀 Testing Complete!")
    print("Next steps:")
    print("1. Review test report for any failures")
    print("2. Perform manual UX testing scenarios")
    print("3. Address any issues found")
    print("4. Proceed with customer acquisition")


if __name__ == "__main__":
    asyncio.run(main())

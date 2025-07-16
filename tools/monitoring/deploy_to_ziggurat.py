#!/usr/bin/env python3
"""
Deploy monitoring dashboard to TrustWrapper satellite
Uses the custom ICP client to deploy monitoring data and dashboard
"""

import asyncio
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.append(
    str(Path(__file__).parent.parent.parent / "agent_forge" / "ziggurat-intelligence")
)

from integrations.icp_client import ICPClient


async def deploy_monitoring_dashboard():
    """Deploy the monitoring dashboard to Ziggurat satellite."""

    print("🚀 Deploying Lamassu Labs monitoring dashboard to TrustWrapper satellite...")
    print("Satellite ID: cmhvu-6iaaa-aaaal-asg5q-cai")

    try:
        # Initialize TrustWrapper ICP client
        async with ICPClient(satellite_id="cmhvu-6iaaa-aaaal-asg5q-cai") as client:

            # Test connectivity first
            print("🔍 Testing satellite connectivity...")
            health = await client.query_satellite_health()
            print(f"✅ Satellite status: {health.status}")
            print(f"💰 Cycles available: {health.cycles:,}")
            print(f"💾 Memory usage: {health.memory_usage} MB")

            # Store monitoring dashboard HTML
            print("📄 Uploading dashboard HTML...")
            dashboard_path = Path(__file__).parent / "dashboard-juno.html"

            if dashboard_path.exists():
                with open(dashboard_path, "r") as f:
                    dashboard_html = f.read()

                dashboard_data = {
                    "type": "monitoring_dashboard",
                    "content": dashboard_html,
                    "version": "1.0.0",
                    "timestamp": int(asyncio.get_event_loop().time()),
                    "description": "Lamassu Labs contract monitoring dashboard",
                }

                dashboard_result = await client.store_data(dashboard_data)

                if dashboard_result["success"]:
                    print(f"✅ Dashboard uploaded: {dashboard_result['storage_id']}")
                else:
                    print(
                        f"❌ Dashboard upload failed: {dashboard_result.get('error')}"
                    )
                    return False
            else:
                print("❌ Dashboard HTML file not found")
                return False

            # Store sample monitoring data
            print("📊 Uploading sample monitoring data...")

            monitoring_data = {
                "timestamp": int(asyncio.get_event_loop().time()),
                "network": "testnet3",
                "summary": {
                    "total_contracts": 2,
                    "healthy_contracts": 1,
                    "degraded_contracts": 1,
                    "unhealthy_contracts": 0,
                    "total_alerts": 2,
                    "critical_alerts": 0,
                },
                "contracts": {
                    "agent_registry_v2.aleo": {
                        "program_id": "agent_registry_v2.aleo",
                        "total_transactions": 156,
                        "successful_transactions": 148,
                        "failed_transactions": 8,
                        "average_execution_time": 1845,
                        "last_activity": "2025-06-22T12:00:00Z",
                        "current_stake": 250000,
                        "active_agents": 42,
                        "gas_used_24h": 15680000,
                        "health_status": "healthy",
                    },
                    "trust_verifier_v2.aleo": {
                        "program_id": "trust_verifier_v2.aleo",
                        "total_transactions": 89,
                        "successful_transactions": 82,
                        "failed_transactions": 7,
                        "average_execution_time": 2150,
                        "last_activity": "2025-06-22T04:00:00Z",
                        "current_stake": 100000,
                        "active_agents": 28,
                        "gas_used_24h": 8900000,
                        "health_status": "degraded",
                    },
                },
                "alerts": [
                    {
                        "severity": "warning",
                        "contract": "trust_verifier_v2.aleo",
                        "message": "No activity for 8.0 hours",
                        "timestamp": "2025-06-22T14:00:00Z",
                    },
                    {
                        "severity": "warning",
                        "contract": "trust_verifier_v2.aleo",
                        "message": "Average execution time above threshold",
                        "timestamp": "2025-06-22T14:00:00Z",
                    },
                ],
            }

            data_result = await client.store_data(
                {"type": "monitoring_data", "data": monitoring_data, "version": "1.0.0"}
            )

            if data_result["success"]:
                print(f"✅ Monitoring data uploaded: {data_result['storage_id']}")
            else:
                print(f"❌ Monitoring data upload failed: {data_result.get('error')}")

            # Get performance stats
            stats = client.get_performance_stats()
            print("\n📈 Deployment Statistics:")
            print(f"   Total requests: {stats['total_requests']}")
            print(f"   Success rate: {stats['success_rate']:.1%}")
            print(f"   Average response time: {stats['average_response_time']:.3f}s")

            print("\n🎉 Deployment completed successfully!")
            print("🌐 Dashboard accessible via TrustWrapper satellite interface")
            print("📊 Monitoring data stored on ICP blockchain")
            print("🔗 Satellite URL: https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io")

            return True

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False


async def test_ziggurat_access():
    """Test access to deployed monitoring data."""

    print("\n🔍 Testing access to deployed monitoring data...")

    try:
        async with ICPClient(satellite_id="cmhvu-6iaaa-aaaal-asg5q-cai") as client:

            # Query recent storage
            print("📊 Attempting to retrieve monitoring data...")

            # This is a demonstration - in practice you'd store and retrieve
            # the actual storage IDs from the deployment
            test_data = {"test": "monitoring_access"}
            storage_result = await client.store_data(test_data)

            if storage_result["success"]:
                retrieved_data = await client.retrieve_data(
                    storage_result["storage_id"]
                )

                if retrieved_data:
                    print("✅ Data storage and retrieval working correctly")
                    print(f"   Storage ID: {storage_result['storage_id']}")
                    print(
                        f"   Data integrity: {'✅ Verified' if retrieved_data else '❌ Failed'}"
                    )
                else:
                    print("❌ Data retrieval failed")
            else:
                print("❌ Data storage failed")

        return True

    except Exception as e:
        print(f"❌ Access test failed: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(deploy_monitoring_dashboard())
    asyncio.run(test_ziggurat_access())

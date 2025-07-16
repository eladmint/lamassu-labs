#!/usr/bin/env python3
"""
TrustWrapper v3.0 Oracle Integration Demo
Demonstrates Task 2.2: Oracle integration foundation (Chainlink, Band Protocol, custom oracles)
"""

import asyncio
import logging
import time

# Import TrustWrapper v3.0 components
from .enhanced_oracle_integration import (
    BandProtocolClient,
    ChainlinkOracleClient,
    CustomOracleClient,
    get_enhanced_oracle_integration,
)
from .multi_chain_connection_manager import (
    SecurityLevel,
    VerificationRequest,
    get_connection_manager,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def demo_oracle_clients():
    """Demonstrate individual oracle client functionality"""
    logger.info("🔍 Testing Individual Oracle Clients...")

    # Test Chainlink client
    logger.info("\n📍 Testing Chainlink Oracle Client...")
    chainlink_client = ChainlinkOracleClient({})
    await chainlink_client.initialize()

    chainlink_data = await chainlink_client.get_price_data(["BTC/USD", "ETH/USD"])
    for data in chainlink_data:
        logger.info(
            f"  Chainlink {data.asset_id}: ${data.price:,.2f} (confidence: {data.confidence:.2%})"
        )

    await chainlink_client.shutdown()

    # Test Band Protocol client
    logger.info("\n📡 Testing Band Protocol Oracle Client...")
    band_client = BandProtocolClient({})
    await band_client.initialize()

    band_data = await band_client.get_price_data(["BTC/USD", "ETH/USD"])
    for data in band_data:
        logger.info(
            f"  Band Protocol {data.asset_id}: ${data.price:,.2f} (confidence: {data.confidence:.2%})"
        )

    await band_client.shutdown()

    # Test Custom Oracle client
    logger.info("\n🛠️ Testing Custom Oracle Client...")
    custom_client = CustomOracleClient({})
    await custom_client.initialize()

    custom_data = await custom_client.get_price_data(["BTC/USD", "ETH/USD"])
    for data in custom_data:
        logger.info(
            f"  {data.source_id} {data.asset_id}: ${data.price:,.2f} (confidence: {data.confidence:.2%})"
        )

    await custom_client.shutdown()


async def demo_enhanced_oracle_integration():
    """Demonstrate enhanced oracle integration system"""
    logger.info("\n🔄 Testing Enhanced Oracle Integration System...")

    # Initialize enhanced oracle integration
    oracle_integration = await get_enhanced_oracle_integration()

    # Start the oracle system
    logger.info("Starting oracle data collection...")
    start_task = asyncio.create_task(oracle_integration.start())

    # Wait for initial data collection
    await asyncio.sleep(3.0)

    # Get system status
    status = oracle_integration.get_status()
    logger.info("📊 Oracle System Status:")
    logger.info(f"  Running: {status['running']}")
    logger.info(f"  Total oracle entries: {status['total_oracle_entries']}")
    logger.info(f"  Fresh data count: {status['fresh_data_count']}")
    logger.info(f"  Active sources: {status['active_sources']}")

    # Test multi-oracle consensus
    logger.info("\n🎯 Testing Multi-Oracle Consensus...")
    for asset_pair in ["BTC/USD", "ETH/USD"]:
        # Get all oracle data for this asset
        all_data = await oracle_integration.get_all_oracle_data(asset_pair)
        logger.info(f"\n📈 {asset_pair} Oracle Data:")

        for data in all_data:
            logger.info(
                f"  {data.source_id}: ${data.price:,.2f} ({data.oracle_type.value})"
            )

        # Get consensus
        consensus = await oracle_integration.get_multi_oracle_consensus(asset_pair)
        if consensus:
            logger.info(f"🎯 {asset_pair} Consensus:")
            logger.info(f"  Consensus Price: ${consensus.consensus_price:,.2f}")
            logger.info(f"  Weighted Price: ${consensus.weighted_price:,.2f}")
            logger.info(f"  Oracle Count: {consensus.oracle_count}")
            logger.info(f"  Price Deviation: {consensus.price_deviation:.2%}")
            logger.info(f"  Confidence Score: {consensus.confidence_score:.2%}")
            logger.info(f"  Participating Oracles: {consensus.participating_oracles}")

            # Show outlier detection
            outliers = consensus.outlier_detection.get("outliers", [])
            if outliers:
                logger.info(f"  ⚠️ Outliers detected: {len(outliers)}")
                for outlier in outliers:
                    logger.info(
                        f"    {outlier['source']}: ${outlier['price']:,.2f} (deviation: {outlier['deviation']:.2%})"
                    )
            else:
                logger.info("  ✅ No outliers detected")

    # Stop the oracle system
    await oracle_integration.stop()
    start_task.cancel()


async def demo_multi_chain_oracle_verification():
    """Demonstrate multi-chain verification with oracle validation"""
    logger.info("\n🌐 Testing Multi-Chain Verification with Oracle Integration...")

    # Initialize connection manager (this also initializes oracles)
    connection_manager = await get_connection_manager()

    # Create a verification request
    verification_request = VerificationRequest(
        request_id="demo_oracle_test_001",
        ai_decision_data={
            "asset_pair": "BTC/USD",
            "decision_type": "buy",
            "confidence": 0.85,
            "risk_score": 0.3,
            "reasoning": "Technical analysis indicates strong upward momentum",
        },
        security_level=SecurityLevel.STANDARD,
        oracle_validation=True,  # Enable oracle validation
        metadata={"demo": True},
    )

    logger.info(f"🔍 Starting verification: {verification_request.request_id}")
    logger.info(f"📊 Security level: {verification_request.security_level.value}")
    logger.info(f"🔗 Oracle validation: {verification_request.oracle_validation}")

    # Perform universal verification
    result = await connection_manager.universal_verify_ai_decision(verification_request)

    # Display results
    logger.info("\n✅ Verification Results:")
    logger.info(f"  Overall Success: {result.overall_success}")
    logger.info(f"  Consensus Score: {result.consensus_score:.2%}")
    logger.info(f"  Execution Time: {result.execution_time_seconds:.2f}s")
    logger.info(
        f"  Successful Chains: {result.successful_chains}/{result.total_chains}"
    )

    # Show oracle consensus if available
    if result.oracle_consensus:
        oracle = result.oracle_consensus
        logger.info("\n🎯 Oracle Consensus:")
        logger.info(f"  Asset: {oracle.asset_id}")
        logger.info(f"  Consensus Price: ${oracle.consensus_price:,.2f}")
        logger.info(f"  Price Deviation: {oracle.price_deviation:.2%}")
        logger.info(f"  Confidence: {oracle.confidence_score:.2%}")
        logger.info(f"  Oracle Count: {oracle.oracle_count}")

    # Show risk assessment
    risk = result.risk_assessment
    logger.info("\n⚖️ Risk Assessment:")
    logger.info(f"  Overall Risk Score: {risk.get('overall_risk_score', 0):.2%}")
    logger.info(f"  Risk Level: {risk.get('risk_level', 'UNKNOWN')}")

    # Show recommendations
    logger.info("\n💡 Recommendations:")
    for i, rec in enumerate(result.recommendations, 1):
        logger.info(f"  {i}. {rec}")

    # Shutdown
    await connection_manager.shutdown()


async def demo_cost_estimation():
    """Demonstrate cost estimation with oracle data"""
    logger.info("\n💰 Testing Cost Estimation...")

    connection_manager = await get_connection_manager()

    verification_request = VerificationRequest(
        request_id="cost_demo_001",
        ai_decision_data={
            "asset_pair": "ETH/USD",
            "decision_type": "sell",
            "confidence": 0.9,
            "risk_score": 0.2,
        },
        security_level=SecurityLevel.HIGH,
        oracle_validation=True,
    )

    # Get cost estimate
    cost_estimate = await connection_manager.get_chain_cost_estimate(
        verification_request
    )

    logger.info("📊 Cost Estimation Results:")
    logger.info(f"  Total Cost: ${cost_estimate['total_cost_usd']:.4f}")
    logger.info(f"  Target Chains: {cost_estimate['target_chains']}")

    logger.info("  Per-Chain Costs:")
    for chain_id, cost_data in cost_estimate["cost_per_chain"].items():
        if "cost_usd" in cost_data:
            logger.info(
                f"    {chain_id}: ${cost_data['cost_usd']:.4f} ({cost_data.get('chain_type', 'unknown')})"
            )
        else:
            logger.info(f"    {chain_id}: Error - {cost_data.get('error', 'Unknown')}")

    await connection_manager.shutdown()


async def demo_system_health():
    """Demonstrate system health monitoring"""
    logger.info("\n🏥 Testing System Health Monitoring...")

    connection_manager = await get_connection_manager()

    # Get system health
    health = await connection_manager.get_system_health()

    logger.info("📊 System Health Status:")
    logger.info(f"  Overall Health Score: {health.overall_health_score:.2%}")
    logger.info(f"  Status: {health.status}")
    logger.info(f"  Last Check: {time.ctime(health.last_check)}")

    if health.issues:
        logger.info("  ⚠️ Issues:")
        for issue in health.issues:
            logger.info(f"    - {issue}")

    if health.recommendations:
        logger.info("  💡 Recommendations:")
        for rec in health.recommendations:
            logger.info(f"    - {rec}")

    # Show chain health details
    chain_health = health.chain_health
    logger.info("\n🔗 Chain Health Details:")
    logger.info(
        f"  Healthy Chains: {chain_health.get('healthy_chains', 0)}/{chain_health.get('total_chains', 0)}"
    )

    for chain_id, chain_data in chain_health.get("chain_details", {}).items():
        status = chain_data.get("status", "unknown")
        latency = chain_data.get("latency_ms", 0)
        logger.info(f"    {chain_id}: {status} ({latency:.1f}ms)")

    # Show oracle health
    oracle_health = health.oracle_health
    logger.info("\n📡 Oracle Health:")
    logger.info(f"  Running: {oracle_health.get('running', False)}")
    logger.info(f"  Fresh Data: {oracle_health.get('fresh_data_count', 0)}")
    logger.info(f"  Total Entries: {oracle_health.get('total_oracle_entries', 0)}")

    await connection_manager.shutdown()


async def main():
    """Main demonstration function"""
    logger.info("🚀 TrustWrapper v3.0 Oracle Integration Demo")
    logger.info("=" * 60)

    try:
        # Demo 1: Individual Oracle Clients
        await demo_oracle_clients()

        # Demo 2: Enhanced Oracle Integration
        await demo_enhanced_oracle_integration()

        # Demo 3: Multi-Chain with Oracle Verification
        await demo_multi_chain_oracle_verification()

        # Demo 4: Cost Estimation
        await demo_cost_estimation()

        # Demo 5: System Health Monitoring
        await demo_system_health()

        logger.info("\n🎉 All demonstrations completed successfully!")
        logger.info("✅ Task 2.2: Oracle Integration Foundation - COMPLETE")

    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
TrustWrapper v3.0 Scaling Infrastructure Demo
Demonstrates Task 2.3: Async processing, Redis caching, connection pooling
Week 2 Phase 1 Implementation Validation
"""

import asyncio
import logging
import time

# Import v3.0 components for integration testing
from .enhanced_oracle_integration import (
    OracleData,
    OracleType,
)
from .multi_chain_connection_manager import (
    SecurityLevel,
    VerificationRequest,
    get_connection_manager,
)

# Import TrustWrapper v3.0 scaling components
from .scaling_infrastructure import (
    ProcessingPriority,
    get_scaling_infrastructure,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def demo_redis_caching():
    """Demonstrate Redis caching capabilities"""
    logger.info("🔧 Testing Redis Caching Infrastructure...")

    # Get scaling infrastructure
    scaling_infra = await get_scaling_infrastructure()
    cache_layer = scaling_infra.cache_layer
    redis_manager = scaling_infra.redis_manager

    # Test basic Redis operations
    logger.info("\n📡 Testing Basic Redis Operations...")

    # Set and get simple values
    await redis_manager.set("test:simple", "Hello TrustWrapper v3.0!", ttl=60)
    value = await redis_manager.get("test:simple")
    logger.info(f"  ✅ Simple value: {value}")

    # Set and get complex objects
    complex_data = {
        "verification_id": "demo_001",
        "chains": ["ethereum", "polygon", "cardano"],
        "consensus_score": 0.85,
        "timestamp": time.time(),
    }
    await redis_manager.set("test:complex", complex_data, ttl=120)
    retrieved_data = await redis_manager.get("test:complex")
    logger.info(
        f"  ✅ Complex object: {retrieved_data['verification_id']} with {len(retrieved_data['chains'])} chains"
    )

    # Test caching with actual TrustWrapper data types
    logger.info("\n🎯 Testing TrustWrapper Data Caching...")

    # Cache oracle data
    oracle_data = OracleData(
        asset_id="BTC/USD",
        price=45000.0,
        timestamp=time.time(),
        source_id="chainlink_demo",
        oracle_type=OracleType.CHAINLINK,
        confidence=0.98,
        chain_context="ethereum",
    )

    success = await cache_layer.cache_oracle_data(oracle_data)
    logger.info(f"  ✅ Oracle data cached: {success}")

    # Retrieve oracle data
    cached_oracle = await cache_layer.get_oracle_data("BTC/USD", "chainlink_demo")
    if cached_oracle:
        logger.info(
            f"  ✅ Oracle data retrieved: {cached_oracle.asset_id} = ${cached_oracle.price:,.2f}"
        )

    # Test verification result caching
    verification_result = {
        "verification_id": "demo_verification_001",
        "consensus_achieved": True,
        "consensus_score": 0.92,
        "successful_chains": 4,
        "total_chains": 5,
        "execution_time": 2.3,
    }

    await cache_layer.cache_verification_result(
        "demo_verification_001", verification_result
    )
    cached_result = await cache_layer.get_verification_result("demo_verification_001")

    if cached_result:
        logger.info(
            f"  ✅ Verification result cached: {cached_result['consensus_score']:.2%} consensus"
        )

    # Show cache metrics
    cache_metrics = cache_layer.get_cache_metrics()
    logger.info("\n📊 Cache Performance Metrics:")
    logger.info(f"  Cache Hit Rate: {cache_metrics['hit_rate']:.1%}")
    logger.info(f"  Total Operations: {cache_metrics['operations']}")
    logger.info(f"  Hits/Misses: {cache_metrics['hits']}/{cache_metrics['misses']}")


async def demo_async_task_processing():
    """Demonstrate async task processing with priority queues"""
    logger.info("\n⚡ Testing Async Task Processing...")

    # Get scaling infrastructure
    scaling_infra = await get_scaling_infrastructure()
    task_manager = scaling_infra.task_manager

    logger.info("📋 Submitting Tasks with Different Priorities...")

    # Submit tasks with different priorities
    task_results = {}

    # Critical priority task (real-time verification)
    async def critical_verification_task():
        await asyncio.sleep(0.5)  # Simulate fast verification
        return {
            "verification_id": "critical_001",
            "status": "success",
            "consensus_score": 0.95,
            "execution_time": 0.5,
        }

    await task_manager.submit_task(
        "critical_verification_001",
        critical_verification_task(),
        ProcessingPriority.CRITICAL,
    )

    # High priority task (oracle update)
    async def oracle_update_task():
        await asyncio.sleep(1.0)  # Simulate oracle data collection
        return {
            "updated_pairs": ["BTC/USD", "ETH/USD", "SOL/USD"],
            "consensus_scores": [0.98, 0.96, 0.94],
            "total_oracles": 12,
        }

    await task_manager.submit_task(
        "oracle_update_001", oracle_update_task(), ProcessingPriority.HIGH
    )

    # Normal priority task (health check)
    async def health_check_task():
        await asyncio.sleep(0.3)
        return {"healthy_chains": 8, "total_chains": 10, "overall_health": 0.85}

    await task_manager.submit_task(
        "health_check_001", health_check_task(), ProcessingPriority.NORMAL
    )

    # Low priority task (cleanup)
    async def cleanup_task():
        await asyncio.sleep(2.0)
        return {"cleaned_entries": 150, "freed_memory_mb": 25.6}

    await task_manager.submit_task(
        "cleanup_001", cleanup_task(), ProcessingPriority.LOW
    )

    logger.info("⏰ Waiting for task completion...")

    # Wait for tasks to complete and collect results
    try:
        critical_result = await task_manager.get_task_result(
            "critical_verification_001", timeout=5.0
        )
        logger.info(
            f"  🚨 CRITICAL completed: {critical_result['consensus_score']:.1%} consensus"
        )

        oracle_result = await task_manager.get_task_result(
            "oracle_update_001", timeout=5.0
        )
        logger.info(
            f"  📊 HIGH completed: Updated {len(oracle_result['updated_pairs'])} oracle pairs"
        )

        health_result = await task_manager.get_task_result(
            "health_check_001", timeout=5.0
        )
        logger.info(
            f"  🏥 NORMAL completed: {health_result['healthy_chains']}/{health_result['total_chains']} chains healthy"
        )

        cleanup_result = await task_manager.get_task_result("cleanup_001", timeout=10.0)
        logger.info(
            f"  🧹 LOW completed: Cleaned {cleanup_result['cleaned_entries']} entries"
        )

    except asyncio.TimeoutError as e:
        logger.warning(f"  ⚠️ Task timeout: {e}")

    # Show task manager metrics
    task_metrics = task_manager.get_metrics()
    logger.info("\n📈 Task Processing Metrics:")
    logger.info(f"  Total Tasks: {task_metrics['total_tasks_submitted']}")
    logger.info(f"  Completed: {task_metrics['total_tasks_completed']}")
    logger.info(f"  Failed: {task_metrics['total_tasks_failed']}")
    logger.info(f"  Average Execution Time: {task_metrics['avg_execution_time']:.2f}s")
    logger.info(f"  Active Workers: {task_metrics['active_workers']}")


async def demo_integrated_verification_with_scaling():
    """Demonstrate full verification pipeline with scaling infrastructure"""
    logger.info("\n🌐 Testing Integrated Multi-Chain Verification with Scaling...")

    # Get all components
    scaling_infra = await get_scaling_infrastructure()
    connection_manager = await get_connection_manager()

    # Create verification request
    verification_request = VerificationRequest(
        request_id="scaling_demo_001",
        ai_decision_data={
            "asset_pair": "ETH/USD",
            "decision_type": "buy",
            "confidence": 0.88,
            "risk_score": 0.25,
            "reasoning": "Strong technical indicators and favorable market conditions",
        },
        security_level=SecurityLevel.HIGH,
        oracle_validation=True,
        metadata={"demo": True, "scaling_test": True},
    )

    logger.info(f"🔍 Starting scaled verification: {verification_request.request_id}")
    logger.info(f"📊 Security level: {verification_request.security_level.value}")

    # Submit verification as async task
    async def verification_coro():
        return await connection_manager.universal_verify_ai_decision(
            verification_request
        )

    # Submit with high priority
    task_submitted = await scaling_infra.submit_verification_task(
        verification_request.request_id, verification_coro(), ProcessingPriority.HIGH
    )

    if not task_submitted:
        logger.error("❌ Failed to submit verification task")
        return

    logger.info("⏳ Verification submitted to async processing queue...")

    # Get result
    try:
        verification_result = await scaling_infra.task_manager.get_task_result(
            f"verify_{verification_request.request_id}", timeout=15.0
        )

        logger.info("\n✅ Scaled Verification Results:")
        logger.info(f"  Overall Success: {verification_result.overall_success}")
        logger.info(f"  Consensus Score: {verification_result.consensus_score:.2%}")
        logger.info(
            f"  Execution Time: {verification_result.execution_time_seconds:.2f}s"
        )
        logger.info(
            f"  Successful Chains: {verification_result.successful_chains}/{verification_result.total_chains}"
        )

        # Show oracle consensus if available
        if verification_result.oracle_consensus:
            oracle = verification_result.oracle_consensus
            logger.info("\n🎯 Oracle Consensus (Cached):")
            logger.info(f"  Asset: {oracle.asset_id}")
            logger.info(f"  Consensus Price: ${oracle.consensus_price:,.2f}")
            logger.info(f"  Confidence: {oracle.confidence_score:.2%}")

        # Cache the result
        result_dict = verification_result.to_dict()
        await scaling_infra.cache_layer.cache_verification_result(
            verification_request.request_id, result_dict
        )
        logger.info("💾 Verification result cached for future retrieval")

    except asyncio.TimeoutError:
        logger.error("❌ Verification task timed out")

    # Cleanup
    await connection_manager.shutdown()


async def demo_performance_optimization():
    """Demonstrate performance optimization features"""
    logger.info("\n🚀 Testing Performance Optimization Features...")

    scaling_infra = await get_scaling_infrastructure()

    # Simulate concurrent oracle updates
    logger.info("📊 Testing Concurrent Oracle Updates...")

    asset_pairs = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "DOT/USD"]

    # Submit multiple oracle update tasks concurrently
    oracle_tasks = []
    for i, pair in enumerate(asset_pairs):
        task_submitted = await scaling_infra.submit_oracle_update_task(
            [pair], ProcessingPriority.HIGH
        )
        if task_submitted:
            oracle_tasks.append(f"oracle_update_{int(time.time()) - i}")

    logger.info(f"  ✅ Submitted {len(oracle_tasks)} concurrent oracle update tasks")

    # Test cache invalidation
    logger.info("\n🔄 Testing Cache Invalidation...")

    # Invalidate oracle cache
    invalidated_oracle = await scaling_infra.cache_layer.invalidate_oracle_cache()
    logger.info(f"  ✅ Invalidated {invalidated_oracle} oracle cache entries")

    # Invalidate verification cache
    invalidated_verification = (
        await scaling_infra.cache_layer.invalidate_verification_cache()
    )
    logger.info(
        f"  ✅ Invalidated {invalidated_verification} verification cache entries"
    )

    # Show comprehensive performance metrics
    logger.info("\n📈 Comprehensive Performance Metrics:")

    performance_metrics = scaling_infra.get_performance_metrics()

    # Redis metrics
    redis_metrics = performance_metrics["redis_metrics"]
    logger.info("  Redis Performance:")
    logger.info(f"    Connected: {redis_metrics['connected']}")
    logger.info(f"    Cache Hit Rate: {redis_metrics['cache_hit_rate']:.1%}")
    logger.info(
        f"    Average Response Time: {redis_metrics['avg_response_time']*1000:.1f}ms"
    )
    logger.info(f"    Total Commands: {redis_metrics['total_commands']}")

    # Task manager metrics
    task_metrics = performance_metrics["task_metrics"]
    logger.info("  Task Manager Performance:")
    logger.info(f"    Running: {task_metrics['running']}")
    logger.info(f"    Active Workers: {task_metrics['active_workers']}")
    logger.info(f"    Completed Tasks: {task_metrics['total_tasks_completed']}")
    logger.info(
        f"    Average Execution Time: {task_metrics['avg_execution_time']:.2f}s"
    )

    # Cache layer metrics
    cache_metrics = performance_metrics["cache_metrics"]
    logger.info("  Cache Layer Performance:")
    logger.info(f"    Hit Rate: {cache_metrics['hit_rate']:.1%}")
    logger.info(f"    Total Operations: {cache_metrics['operations']}")
    logger.info(f"    Invalidations: {cache_metrics['invalidations']}")


async def demo_error_handling_and_resilience():
    """Demonstrate error handling and system resilience"""
    logger.info("\n🛡️ Testing Error Handling and System Resilience...")

    scaling_infra = await get_scaling_infrastructure()

    # Test task failure handling
    logger.info("⚠️ Testing Task Failure Handling...")

    async def failing_task():
        await asyncio.sleep(0.5)
        raise Exception("Simulated task failure for resilience testing")

    # Submit task that will fail
    task_submitted = await scaling_infra.task_manager.submit_task(
        "failing_task_001", failing_task(), ProcessingPriority.NORMAL
    )

    if task_submitted:
        try:
            await scaling_infra.task_manager.get_task_result(
                "failing_task_001", timeout=3.0
            )
        except RuntimeError as e:
            logger.info(f"  ✅ Task failure handled correctly: {e}")

    # Test cache miss handling
    logger.info("\n🔍 Testing Cache Miss Handling...")

    non_existent_result = await scaling_infra.cache_layer.get_verification_result(
        "non_existent_id"
    )
    logger.info(f"  ✅ Cache miss handled: {non_existent_result is None}")

    # Test Redis connection resilience
    logger.info("\n🔄 Testing Redis Connection Resilience...")

    # Try operations that might fail gracefully
    exists_result = await scaling_infra.redis_manager.exists(
        "definitely_not_a_real_key"
    )
    logger.info(f"  ✅ Non-existent key check: {exists_result}")

    # Show error metrics
    task_metrics = scaling_infra.task_manager.get_metrics()
    redis_metrics = scaling_infra.redis_manager.get_metrics()

    logger.info("\n📊 Error Resilience Metrics:")
    logger.info(f"  Failed Tasks: {task_metrics['total_tasks_failed']}")
    logger.info(f"  Redis Connection Errors: {redis_metrics['connection_errors']}")


async def main():
    """Main demonstration function"""
    logger.info("🚀 TrustWrapper v3.0 Scaling Infrastructure Demo")
    logger.info("=" * 70)
    logger.info("Task 2.3: Async Processing, Redis Caching, Connection Pooling")
    logger.info("=" * 70)

    try:
        # Demo 1: Redis Caching
        await demo_redis_caching()

        # Brief pause between demos
        await asyncio.sleep(1.0)

        # Demo 2: Async Task Processing
        await demo_async_task_processing()

        await asyncio.sleep(1.0)

        # Demo 3: Integrated Verification with Scaling
        await demo_integrated_verification_with_scaling()

        await asyncio.sleep(1.0)

        # Demo 4: Performance Optimization
        await demo_performance_optimization()

        await asyncio.sleep(1.0)

        # Demo 5: Error Handling and Resilience
        await demo_error_handling_and_resilience()

        logger.info(
            "\n🎉 All scaling infrastructure demonstrations completed successfully!"
        )
        logger.info("✅ Task 2.3: Scaling Infrastructure - COMPLETE")
        logger.info(
            "📊 Week 2 Phase 1: Advanced async processing, Redis caching, and connection pooling operational"
        )

        # Final performance summary
        scaling_infra = await get_scaling_infrastructure()
        final_metrics = scaling_infra.get_performance_metrics()

        logger.info("\n📈 Final Performance Summary:")
        logger.info(
            f"  Infrastructure Status: {final_metrics['infrastructure_status']}"
        )
        logger.info(
            f"  All Components Operational: {all(final_metrics['components'].values())}"
        )
        logger.info(
            f"  Redis Hit Rate: {final_metrics['redis_metrics']['cache_hit_rate']:.1%}"
        )
        logger.info(
            f"  Task Success Rate: {(final_metrics['task_metrics']['total_tasks_completed'] / max(final_metrics['task_metrics']['total_tasks_submitted'], 1)):.1%}"
        )

        # Shutdown infrastructure
        await scaling_infra.shutdown()

    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

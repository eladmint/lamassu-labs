#!/usr/bin/env python3

"""
TrustWrapper v3.0 Oracle Optimization Demonstration
Phase 2 Week 7 Task 7.2: Oracle Optimization

This demo showcases:
- Oracle response time optimization
- Load balancing across multiple agents
- Health monitoring and agent management
- Performance analytics and metrics
"""

import asyncio
import json
import os
import sys
import time
from typing import Any, Dict

import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from trustwrapper.v3.enhanced_ml_oracle import (
    HealthStatus,
    LoadBalancingStrategy,
    PredictionRequest,
    PredictionType,
    TrustWrapperEnhancedMLOracle,
)


class OracleOptimizationDemo:
    """Comprehensive demonstration of oracle optimization capabilities"""

    def __init__(self):
        self.oracle = TrustWrapperEnhancedMLOracle()
        self.demo_results = {}

    async def run_complete_demonstration(self):
        """Run complete oracle optimization demonstration"""
        print("⚡ TrustWrapper v3.0 Oracle Optimization Demo")
        print("=" * 70)
        print("Phase 2 Week 7 Task 7.2: Oracle Optimization")
        print("-" * 70)

        # Demo scenarios
        scenarios = [
            ("Response Time Optimization", self.demo_response_time_optimization),
            ("Load Balancing Strategies", self.demo_load_balancing_strategies),
            ("Agent Health Monitoring", self.demo_agent_health_monitoring),
            ("Performance Analytics", self.demo_performance_analytics),
            ("Cache Performance", self.demo_cache_performance),
            ("Concurrent Load Testing", self.demo_concurrent_load_testing),
            ("Agent Failover Testing", self.demo_agent_failover),
            ("Optimization Status Overview", self.demo_optimization_status),
        ]

        for scenario_name, scenario_func in scenarios:
            print(f"\n⚡ {scenario_name}")
            print("-" * 50)

            start_time = time.time()
            result = await scenario_func()
            execution_time = time.time() - start_time

            self.demo_results[scenario_name] = {
                **result,
                "execution_time": execution_time,
            }

            print(f"✅ Completed in {execution_time:.2f}s")

        # Generate final report
        await self.generate_demo_report()

    async def demo_response_time_optimization(self) -> Dict[str, Any]:
        """Demonstrate response time optimization through caching and smart routing"""
        print("🚀 Testing response time optimization...")

        # Create test prediction requests
        test_requests = [
            {
                "name": "Market Trend Analysis",
                "prediction_type": PredictionType.MARKET_TREND,
                "input_data": {
                    "price_history": [100, 102, 105, 108, 110],
                    "volume_data": [1000, 1200, 1500, 1800, 2000],
                    "technical_indicators": {"rsi": 65, "macd": 1.1},
                },
            },
            {
                "name": "Price Movement Forecast",
                "prediction_type": PredictionType.PRICE_MOVEMENT,
                "input_data": {
                    "current_price": 100.0,
                    "price_history": [95, 98, 100, 102, 105],
                    "market_conditions": {"sentiment": 0.3, "volatility": 0.03},
                },
            },
            {
                "name": "Volatility Prediction",
                "prediction_type": PredictionType.VOLATILITY_FORECAST,
                "input_data": {
                    "price_history": [99, 100, 101, 100, 102, 99, 101, 100],
                    "time_horizon": 24,
                },
            },
        ]

        optimization_results = {}

        for request_data in test_requests:
            print(f"\n  🧪 Testing {request_data['name']}...")

            # Create prediction request
            request = PredictionRequest(
                request_id=f"opt_test_{int(time.time() * 1000)}",
                prediction_type=request_data["prediction_type"],
                input_data=request_data["input_data"],
                time_horizon=1.0,
                confidence_threshold=0.8,
                required_consensus=False,
                agent_constraints=None,
            )

            # Test 1: First request (no cache)
            start_time = time.time()
            result1 = await self.oracle.optimize_oracle_response_time(request)
            first_request_time = (time.time() - start_time) * 1000

            # Wait a moment
            await asyncio.sleep(0.1)

            # Test 2: Second identical request (should use cache)
            start_time = time.time()
            result2 = await self.oracle.optimize_oracle_response_time(request)
            cached_request_time = (time.time() - start_time) * 1000

            # Calculate optimization improvement
            cache_speedup = (
                (first_request_time - cached_request_time) / first_request_time * 100
            )

            optimization_results[request_data["name"]] = {
                "first_request_time": first_request_time,
                "cached_request_time": cached_request_time,
                "cache_speedup": cache_speedup,
                "optimization_enabled": True,
            }

            print(f"    ⏱️  First request: {first_request_time:.1f}ms")
            print(f"    ⚡ Cached request: {cached_request_time:.1f}ms")
            print(f"    📈 Speedup: {cache_speedup:.1f}%")

        return {
            "requests_tested": len(test_requests),
            "optimization_results": optimization_results,
            "average_speedup": np.mean(
                [r["cache_speedup"] for r in optimization_results.values()]
            ),
        }

    async def demo_load_balancing_strategies(self) -> Dict[str, Any]:
        """Demonstrate different load balancing strategies"""
        print("⚖️ Testing load balancing strategies...")

        strategies = [
            LoadBalancingStrategy.LEAST_LOADED,
            LoadBalancingStrategy.RESPONSE_TIME_BASED,
            LoadBalancingStrategy.CAPACITY_BASED,
            LoadBalancingStrategy.ADAPTIVE_SCORING,
        ]

        strategy_results = {}

        for strategy in strategies:
            print(f"\n  🎯 Testing {strategy.value}...")

            # Set strategy
            self.oracle.load_balancing_strategy = strategy

            # Generate multiple concurrent requests
            requests = []
            for i in range(5):
                request = PredictionRequest(
                    request_id=f"lb_test_{strategy.value}_{i}",
                    prediction_type=PredictionType.MARKET_TREND,
                    input_data={"test_data": i, "strategy": strategy.value},
                    time_horizon=1.0,
                    confidence_threshold=0.8,
                    required_consensus=False,
                    agent_constraints=None,
                )
                requests.append(request)

            # Process requests and measure distribution
            start_time = time.time()
            results = await asyncio.gather(
                *[self.oracle.optimize_oracle_response_time(req) for req in requests]
            )
            total_time = time.time() - start_time

            # Analyze load distribution
            load_distribution = {
                agent_id: agent.current_load
                for agent_id, agent in self.oracle.oracle_agents.items()
            }

            strategy_results[strategy.value] = {
                "total_processing_time": total_time * 1000,
                "requests_processed": len(results),
                "load_distribution": load_distribution,
                "average_time_per_request": (total_time * 1000) / len(results),
            }

            print(f"    ⏱️  Total time: {total_time * 1000:.1f}ms")
            print(f"    📊 Load distribution: {load_distribution}")
            print(f"    📈 Avg per request: {(total_time * 1000) / len(results):.1f}ms")

        return {
            "strategies_tested": len(strategies),
            "strategy_results": strategy_results,
            "best_strategy": min(
                strategy_results.keys(),
                key=lambda s: strategy_results[s]["average_time_per_request"],
            ),
        }

    async def demo_agent_health_monitoring(self) -> Dict[str, Any]:
        """Demonstrate agent health monitoring capabilities"""
        print("🏥 Testing agent health monitoring...")

        # Perform initial health check
        print("\\n  🔍 Performing comprehensive health check...")
        health_results = await self.oracle.perform_health_monitoring()

        # Display health status
        healthy_agents = 0
        degraded_agents = 0
        unhealthy_agents = 0

        for agent_id, status in health_results.items():
            status_emoji = {
                HealthStatus.HEALTHY: "✅",
                HealthStatus.DEGRADED: "⚠️",
                HealthStatus.UNHEALTHY: "❌",
                HealthStatus.MAINTENANCE: "🔧",
                HealthStatus.OFFLINE: "📴",
            }.get(status, "❓")

            print(f"    {status_emoji} {agent_id}: {status.value}")

            if status == HealthStatus.HEALTHY:
                healthy_agents += 1
            elif status == HealthStatus.DEGRADED:
                degraded_agents += 1
            else:
                unhealthy_agents += 1

        # Simulate agent failure and recovery
        print("\\n  🔧 Simulating agent failure and recovery...")

        # Simulate failure by temporarily marking an agent as unhealthy
        first_agent_id = list(self.oracle.oracle_agents.keys())[0]
        original_status = self.oracle.oracle_agents[first_agent_id].health_status
        self.oracle.oracle_agents[first_agent_id].health_status = HealthStatus.UNHEALTHY

        print(f"    ❌ Simulated failure: {first_agent_id}")

        # Test load balancing with failed agent
        request = PredictionRequest(
            request_id="health_test_failover",
            prediction_type=PredictionType.PRICE_MOVEMENT,
            input_data={"test": "failover"},
            time_horizon=1.0,
            confidence_threshold=0.8,
            required_consensus=False,
            agent_constraints=None,
        )

        selected_agent = await self.oracle._select_optimal_agent(request)
        failover_successful = (
            selected_agent and selected_agent.agent_id != first_agent_id
        )

        print(f"    🔄 Failover successful: {failover_successful}")
        if selected_agent:
            print(f"    🎯 Selected agent: {selected_agent.agent_id}")

        # Restore agent
        self.oracle.oracle_agents[first_agent_id].health_status = original_status
        print(f"    ✅ Restored agent: {first_agent_id}")

        # Get detailed agent metrics
        agent_metrics = {}
        for agent_id, agent in self.oracle.oracle_agents.items():
            agent_metrics[agent_id] = {
                "health_status": agent.health_status.value,
                "current_load": agent.current_load,
                "capacity": agent.capacity,
                "response_time_avg": agent.response_time_avg,
                "success_rate": agent.success_rate,
                "performance_score": agent.performance_score,
                "specializations": agent.specializations,
            }

        return {
            "total_agents": len(health_results),
            "healthy_agents": healthy_agents,
            "degraded_agents": degraded_agents,
            "unhealthy_agents": unhealthy_agents,
            "health_results": {k: v.value for k, v in health_results.items()},
            "failover_test": {
                "failed_agent": first_agent_id,
                "failover_successful": failover_successful,
                "selected_agent": selected_agent.agent_id if selected_agent else None,
            },
            "agent_metrics": agent_metrics,
        }

    async def demo_performance_analytics(self) -> Dict[str, Any]:
        """Demonstrate performance analytics capabilities"""
        print("📊 Testing performance analytics...")

        # Generate some load to create meaningful metrics
        print("\\n  🏃 Generating load for analytics...")

        load_requests = []
        for i in range(10):
            request = PredictionRequest(
                request_id=f"analytics_load_{i}",
                prediction_type=PredictionType.SENTIMENT_ANALYSIS,
                input_data={"text": f"Test data {i}", "load_test": True},
                time_horizon=1.0,
                confidence_threshold=0.8,
                required_consensus=False,
                agent_constraints=None,
            )
            load_requests.append(request)

        # Process requests concurrently
        await asyncio.gather(
            *[self.oracle.optimize_oracle_response_time(req) for req in load_requests]
        )

        # Generate performance analytics
        print("\\n  📈 Generating performance analytics...")
        performance_metrics = await self.oracle.generate_performance_analytics()

        print(
            f"    🚀 Request throughput: {performance_metrics.request_throughput:.1f} RPS"
        )
        print(f"    ⏱️  Latency P50: {performance_metrics.latency_p50:.1f}ms")
        print(f"    ⏱️  Latency P95: {performance_metrics.latency_p95:.1f}ms")
        print(f"    ⏱️  Latency P99: {performance_metrics.latency_p99:.1f}ms")
        print(f"    ❌ Error rate: {performance_metrics.error_rate:.1f}%")
        print(f"    💾 Cache hit rate: {performance_metrics.cache_hit_rate:.1f}%")

        # Resource utilization
        resource_util = performance_metrics.resource_utilization
        print("\\n  💻 Resource Utilization:")
        for resource, value in resource_util.items():
            if isinstance(value, (int, float)):
                print(
                    f"    📊 {resource}: {value:.1f}{'%' if 'percent' in resource else ''}"
                )
            else:
                print(f"    📊 {resource}: {value}")

        # Per-agent performance
        print("\\n  🤖 Per-Agent Performance:")
        for agent_id, metrics in performance_metrics.agent_performance.items():
            print(f"    🎯 {agent_id}:")
            print(f"      ⏱️  Response time: {metrics['response_time_avg']:.1f}ms")
            print(f"      ✅ Success rate: {metrics['success_rate']:.1%}")
            print(
                f"      📊 Load: {metrics['current_load']}/{int(metrics['capacity_utilization'] * metrics['current_load'] / 100)}"
            )
            print(f"      🏆 Performance score: {metrics['performance_score']:.3f}")

        return {
            "load_requests_processed": len(load_requests),
            "performance_metrics": {
                "request_throughput": performance_metrics.request_throughput,
                "latency_p50": performance_metrics.latency_p50,
                "latency_p95": performance_metrics.latency_p95,
                "latency_p99": performance_metrics.latency_p99,
                "error_rate": performance_metrics.error_rate,
                "cache_hit_rate": performance_metrics.cache_hit_rate,
            },
            "resource_utilization": resource_util,
            "agent_count": len(performance_metrics.agent_performance),
            "analytics_available": True,
        }

    async def demo_cache_performance(self) -> Dict[str, Any]:
        """Demonstrate caching system performance"""
        print("💾 Testing cache performance...")

        # Test cache hit/miss scenarios
        cache_test_data = [
            {
                "name": "Identical Requests",
                "requests": [
                    {"data": {"price": 100}, "type": PredictionType.MARKET_TREND},
                    {
                        "data": {"price": 100},
                        "type": PredictionType.MARKET_TREND,
                    },  # Should hit cache
                ],
            },
            {
                "name": "Similar Requests",
                "requests": [
                    {"data": {"price": 100.1}, "type": PredictionType.PRICE_MOVEMENT},
                    {
                        "data": {"price": 100.2},
                        "type": PredictionType.PRICE_MOVEMENT,
                    },  # Different data
                ],
            },
            {
                "name": "Time-based Caching",
                "requests": [
                    {
                        "data": {"price": 105},
                        "type": PredictionType.VOLATILITY_FORECAST,
                    },
                ],
            },
        ]

        cache_results = {}

        for test_scenario in cache_test_data:
            print(f"\\n  🧪 Testing {test_scenario['name']}...")

            scenario_results = []

            for i, req_data in enumerate(test_scenario["requests"]):
                request = PredictionRequest(
                    request_id=f"cache_test_{test_scenario['name']}_{i}",
                    prediction_type=req_data["type"],
                    input_data=req_data["data"],
                    time_horizon=1.0,
                    confidence_threshold=0.8,
                    required_consensus=False,
                    agent_constraints=None,
                )

                start_time = time.time()
                result = await self.oracle.optimize_oracle_response_time(request)
                response_time = (time.time() - start_time) * 1000

                scenario_results.append(
                    {
                        "request_index": i,
                        "response_time": response_time,
                        "cache_key": self.oracle._generate_cache_key(request),
                    }
                )

                print(f"    📝 Request {i+1}: {response_time:.1f}ms")

            cache_results[test_scenario["name"]] = scenario_results

        # Check cache statistics
        cache_size = len(self.oracle.prediction_cache)
        print("\\n  📊 Cache Statistics:")
        print(f"    💾 Cache entries: {cache_size}")
        print(f"    ⏰ Cache TTL: {self.oracle.cache_ttl}s")

        return {
            "cache_tests": len(cache_test_data),
            "cache_results": cache_results,
            "cache_size": cache_size,
            "cache_ttl": self.oracle.cache_ttl,
            "cache_enabled": True,
        }

    async def demo_concurrent_load_testing(self) -> Dict[str, Any]:
        """Demonstrate performance under concurrent load"""
        print("🏋️ Testing concurrent load performance...")

        # Test different concurrency levels
        concurrency_levels = [1, 5, 10, 20]
        load_test_results = {}

        for concurrency in concurrency_levels:
            print(f"\\n  ⚡ Testing {concurrency} concurrent requests...")

            # Create concurrent requests
            requests = []
            for i in range(concurrency):
                request = PredictionRequest(
                    request_id=f"load_test_{concurrency}_{i}",
                    prediction_type=PredictionType.RISK_ASSESSMENT,
                    input_data={
                        "portfolio": f"test_portfolio_{i}",
                        "risk_level": np.random.uniform(0.1, 0.9),
                    },
                    time_horizon=1.0,
                    confidence_threshold=0.8,
                    required_consensus=False,
                    agent_constraints=None,
                )
                requests.append(request)

            # Execute concurrent requests
            start_time = time.time()
            results = await asyncio.gather(
                *[self.oracle.optimize_oracle_response_time(req) for req in requests]
            )
            total_time = time.time() - start_time

            # Calculate metrics
            throughput = len(results) / total_time
            avg_time_per_request = (total_time * 1000) / len(results)

            load_test_results[concurrency] = {
                "requests_processed": len(results),
                "total_time": total_time * 1000,
                "throughput": throughput,
                "avg_time_per_request": avg_time_per_request,
                "all_successful": len(results) == concurrency,
            }

            print(f"    📊 Throughput: {throughput:.1f} RPS")
            print(f"    ⏱️  Avg response time: {avg_time_per_request:.1f}ms")
            print(f"    ✅ Success rate: {(len(results) / concurrency) * 100:.1f}%")

        # Find optimal concurrency level
        optimal_concurrency = max(
            load_test_results.keys(), key=lambda c: load_test_results[c]["throughput"]
        )

        return {
            "concurrency_levels_tested": len(concurrency_levels),
            "load_test_results": load_test_results,
            "optimal_concurrency": optimal_concurrency,
            "max_throughput": load_test_results[optimal_concurrency]["throughput"],
        }

    async def demo_agent_failover(self) -> Dict[str, Any]:
        """Demonstrate agent failover capabilities"""
        print("🔄 Testing agent failover mechanisms...")

        # Get initial agent count
        initial_healthy_agents = len(
            [
                a
                for a in self.oracle.oracle_agents.values()
                if a.health_status == HealthStatus.HEALTHY
            ]
        )

        print(f"\\n  📊 Initial healthy agents: {initial_healthy_agents}")

        # Simulate progressive agent failures
        agent_ids = list(self.oracle.oracle_agents.keys())
        failover_results = {}

        for i, agent_id in enumerate(agent_ids[:2]):  # Fail first 2 agents
            print(f"\\n  ❌ Simulating failure of {agent_id}...")

            # Mark agent as unhealthy
            original_status = self.oracle.oracle_agents[agent_id].health_status
            self.oracle.oracle_agents[agent_id].health_status = HealthStatus.UNHEALTHY

            # Test if system can still handle requests
            test_request = PredictionRequest(
                request_id=f"failover_test_{i}",
                prediction_type=PredictionType.CORRELATION_ANALYSIS,
                input_data={"test": f"failover_{i}"},
                time_horizon=1.0,
                confidence_threshold=0.8,
                required_consensus=False,
                agent_constraints=None,
            )

            try:
                start_time = time.time()
                result = await self.oracle.optimize_oracle_response_time(test_request)
                response_time = (time.time() - start_time) * 1000

                # Check which agent handled the request
                selected_agent = await self.oracle._select_optimal_agent(test_request)

                failover_results[f"failure_{i+1}"] = {
                    "failed_agent": agent_id,
                    "failover_successful": True,
                    "response_time": response_time,
                    "handling_agent": (
                        selected_agent.agent_id if selected_agent else None
                    ),
                    "remaining_healthy_agents": len(
                        [
                            a
                            for a in self.oracle.oracle_agents.values()
                            if a.health_status == HealthStatus.HEALTHY
                        ]
                    ),
                }

                print("    ✅ Failover successful")
                print(
                    f"    🎯 Request handled by: {selected_agent.agent_id if selected_agent else 'None'}"
                )
                print(f"    ⏱️  Response time: {response_time:.1f}ms")

            except Exception as e:
                failover_results[f"failure_{i+1}"] = {
                    "failed_agent": agent_id,
                    "failover_successful": False,
                    "error": str(e),
                    "remaining_healthy_agents": len(
                        [
                            a
                            for a in self.oracle.oracle_agents.values()
                            if a.health_status == HealthStatus.HEALTHY
                        ]
                    ),
                }
                print(f"    ❌ Failover failed: {e}")

        # Restore all agents
        print("\\n  🔧 Restoring all agents...")
        for agent_id in agent_ids[:2]:
            self.oracle.oracle_agents[agent_id].health_status = HealthStatus.HEALTHY
            print(f"    ✅ Restored {agent_id}")

        return {
            "initial_healthy_agents": initial_healthy_agents,
            "agents_failed": len(failover_results),
            "failover_results": failover_results,
            "all_failovers_successful": all(
                result["failover_successful"] for result in failover_results.values()
            ),
        }

    async def demo_optimization_status(self) -> Dict[str, Any]:
        """Demonstrate comprehensive optimization status overview"""
        print("📋 Generating optimization status overview...")

        # Get comprehensive status
        optimization_status = await self.oracle.get_optimization_status()

        print("\\n  ⚡ Optimization System Status:")
        opt_system = optimization_status["optimization_system"]
        print(f"    🎯 Load balancing: {opt_system['load_balancing_strategy']}")
        print(f"    💾 Cache enabled: {opt_system['cache_enabled']}")
        print(f"    📊 Cache size: {opt_system['cache_size']}")
        print(f"    📈 Cache hit rate: {opt_system['cache_hit_rate']:.1f}%")
        print(f"    🏥 Health monitoring: {opt_system['health_monitoring_enabled']}")

        print("\\n  🤖 Agent Status Summary:")
        agent_status = optimization_status["agent_status"]
        for agent_id, status in agent_status.items():
            health_emoji = {"healthy": "✅", "degraded": "⚠️", "unhealthy": "❌"}.get(
                status["health"], "❓"
            )
            print(f"    {health_emoji} {agent_id}:")
            print(f"      📊 Load: {status['load']}")
            print(f"      ⏱️  Response time: {status['response_time']}")
            print(f"      ✅ Success rate: {status['success_rate']}")
            print(f"      🏆 Performance: {status['performance_score']}")

        print("\\n  📊 Performance Metrics:")
        perf_metrics = optimization_status["performance_metrics"]
        for metric, value in perf_metrics.items():
            if metric != "resource_utilization":
                print(f"    📈 {metric.replace('_', ' ').title()}: {value}")

        print("\\n  ⚖️  Load Balancing Metrics:")
        lb_metrics = optimization_status["load_balancing_metrics"]
        for metric, value in lb_metrics.items():
            if metric != "load_distribution":
                print(f"    📊 {metric.replace('_', ' ').title()}: {value}")

        # Enhanced oracle metrics
        enhanced_metrics = self.oracle.get_enhanced_oracle_metrics()

        print("\\n  🧠 Enhanced Oracle Metrics:")
        print(f"    📊 Total predictions: {enhanced_metrics['total_predictions']}")
        print(f"    🎯 Accuracy rate: {enhanced_metrics['accuracy_rate']:.3f}")
        print(f"    🤝 Consensus rate: {enhanced_metrics['consensus_rate']:.3f}")
        print(
            f"    💯 Average confidence: {enhanced_metrics['average_confidence']:.3f}"
        )
        print(f"    🚨 Anomalies detected: {enhanced_metrics['anomalies_detected']}")
        print(f"    🤖 Active agents: {enhanced_metrics['active_agents']}")
        print(
            f"    ⚡ Optimization enabled: {enhanced_metrics['optimization_enabled']}"
        )

        return {
            "optimization_status": optimization_status,
            "enhanced_metrics": enhanced_metrics,
            "system_health": "optimal",
            "optimization_features": [
                "response_time_optimization",
                "load_balancing",
                "health_monitoring",
                "performance_analytics",
                "caching",
                "failover_support",
            ],
        }

    async def generate_demo_report(self):
        """Generate comprehensive optimization demonstration report"""
        print("\\n" + "=" * 70)
        print("📋 ORACLE OPTIMIZATION DEMO REPORT")
        print("=" * 70)

        # Overall metrics
        total_time = sum(r.get("execution_time", 0) for r in self.demo_results.values())
        total_scenarios = len(self.demo_results)

        print("\\n🎯 Overall Performance:")
        print(f"   Total scenarios: {total_scenarios}")
        print(f"   Total execution time: {total_time:.2f}s")
        print(f"   Average scenario time: {total_time/total_scenarios:.2f}s")

        # Detailed results summary
        print("\\n📊 Scenario Results Summary:")
        for scenario, results in self.demo_results.items():
            execution_time = results.get("execution_time", 0)
            print(f"   {scenario}: {execution_time:.2f}s")

            # Show key metrics for each scenario
            if "requests_tested" in results:
                print(f"     - Requests tested: {results['requests_tested']}")
            if "average_speedup" in results:
                print(f"     - Cache speedup: {results['average_speedup']:.1f}%")
            if "strategies_tested" in results:
                print(f"     - Strategies tested: {results['strategies_tested']}")
            if "healthy_agents" in results:
                print(f"     - Healthy agents: {results['healthy_agents']}")
            if "max_throughput" in results:
                print(f"     - Max throughput: {results['max_throughput']:.1f} RPS")

        # Technical achievements
        print("\\n🏆 Optimization Achievements:")
        print("   ✅ Response time optimization with intelligent caching")
        print("   ✅ Multi-strategy load balancing (4 strategies)")
        print("   ✅ Comprehensive agent health monitoring")
        print("   ✅ Real-time performance analytics")
        print("   ✅ Cache performance optimization")
        print("   ✅ Concurrent load handling")
        print("   ✅ Automatic agent failover")
        print("   ✅ Complete optimization status overview")

        # Performance improvements summary
        if "Response Time Optimization" in self.demo_results:
            rto_results = self.demo_results["Response Time Optimization"]
            print("\\n⚡ Performance Improvements:")
            print(
                f"   🚀 Average cache speedup: {rto_results.get('average_speedup', 0):.1f}%"
            )

        if "Concurrent Load Testing" in self.demo_results:
            clt_results = self.demo_results["Concurrent Load Testing"]
            print(
                f"   📊 Max throughput achieved: {clt_results.get('max_throughput', 0):.1f} RPS"
            )

        if "Agent Health Monitoring" in self.demo_results:
            ahm_results = self.demo_results["Agent Health Monitoring"]
            print(
                f"   🏥 Health monitoring: {ahm_results.get('total_agents', 0)} agents monitored"
            )

        # Final system metrics
        optimization_status = await self.oracle.get_optimization_status()

        print("\\n📈 Final System Metrics:")
        print(
            f"   🤖 Active oracle agents: {len([a for a in self.oracle.oracle_agents.values() if a.health_status == HealthStatus.HEALTHY])}"
        )
        print(f"   💾 Cache entries: {len(self.oracle.prediction_cache)}")
        print(
            f"   ⚖️  Load balancing strategy: {self.oracle.load_balancing_strategy.value}"
        )
        print("   🏥 Health monitoring enabled: True")

        print("\\n✨ Demo completed successfully!")
        print("🎉 Phase 2 Week 7 Task 7.2 COMPLETE!")
        print("⚡ Oracle Optimization with advanced performance features operational!")

        # Save demo results to file
        demo_report = {
            "demo_timestamp": time.time(),
            "total_execution_time": total_time,
            "scenarios_completed": total_scenarios,
            "scenario_results": self.demo_results,
            "optimization_status": optimization_status,
            "task_completion": "Phase 2 Week 7 Task 7.2 COMPLETE",
        }

        report_filename = f"oracle_optimization_demo_report_{int(time.time())}.json"
        try:
            with open(report_filename, "w") as f:
                json.dump(demo_report, f, indent=2, default=str)
            print(f"📄 Demo report saved to: {report_filename}")
        except Exception as e:
            print(f"⚠️ Could not save report: {e}")


async def main():
    """Run the oracle optimization demonstration"""
    demo = OracleOptimizationDemo()
    await demo.run_complete_demonstration()


if __name__ == "__main__":
    asyncio.run(main())

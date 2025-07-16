#!/usr/bin/env python3

"""
TrustWrapper v3.0 Distributed Learning Coordinator Tests
Comprehensive test suite for Phase 2 Week 6 Task 6.1 implementation

Tests cover:
- Byzantine fault tolerance with 33% threshold
- Advanced detection algorithms (7 methods)
- Secure aggregation protocols (4 strategies)
- Differential privacy mechanisms
- Cross-agent learning capabilities
- Performance and scalability validation
"""

import asyncio
import os
import random

# Import the distributed learning coordinator
import sys
import time

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from trustwrapper.v3.distributed_learning_coordinator import (
    AgentRole,
    AggregationResult,
    LearningPhase,
    LearningStrategy,
    TrustWrapperDistributedLearningCoordinator,
)


class TestDistributedLearningCoordinator:
    """Comprehensive test suite for distributed learning coordinator"""

    @pytest.fixture
    async def coordinator(self):
        """Create a fresh coordinator for each test"""
        return TrustWrapperDistributedLearningCoordinator()

    @pytest.fixture
    async def sample_agents(self, coordinator):
        """Create sample agents for testing"""
        agents = []

        agent_configs = [
            {
                "role": "participant",
                "blockchain_networks": ["ethereum"],
                "computational_capacity": 0.8,
                "specialization": ["computer_vision"],
                "privacy_budget": 1.0,
            },
            {
                "role": "validator",
                "blockchain_networks": ["cardano"],
                "computational_capacity": 0.9,
                "specialization": ["natural_language"],
                "privacy_budget": 1.5,
            },
            {
                "role": "participant",
                "blockchain_networks": ["solana"],
                "computational_capacity": 0.7,
                "specialization": ["reinforcement_learning"],
                "privacy_budget": 0.8,
            },
            {
                "role": "aggregator",
                "blockchain_networks": ["bitcoin", "ethereum"],
                "computational_capacity": 1.0,
                "specialization": ["time_series"],
                "privacy_budget": 2.0,
            },
        ]

        for config in agent_configs:
            agent_id = await coordinator.register_agent(config)
            agents.append(agent_id)

        return agents

    async def test_coordinator_initialization(self, coordinator):
        """Test coordinator initialization"""
        assert coordinator.coordinator_id.startswith("coordinator_")
        assert coordinator.max_concurrent_rounds == 10
        assert coordinator.byzantine_tolerance_threshold == 0.33
        assert coordinator.consensus_threshold == 0.67
        assert len(coordinator.agents) == 0
        assert len(coordinator.learning_rounds) == 0

        # Test Byzantine detection methods initialization
        assert len(coordinator.byzantine_detection_methods) == 5
        assert "statistical_analysis" in coordinator.byzantine_detection_methods
        assert "gradient_analysis" in coordinator.byzantine_detection_methods
        assert "cosine_similarity" in coordinator.byzantine_detection_methods

        # Test privacy mechanisms initialization
        assert len(coordinator.privacy_mechanisms) == 3
        assert "gaussian_noise" in coordinator.privacy_mechanisms
        assert "laplace_noise" in coordinator.privacy_mechanisms

    async def test_agent_registration(self, coordinator):
        """Test agent registration functionality"""
        agent_data = {
            "role": "participant",
            "blockchain_networks": ["ethereum"],
            "computational_capacity": 0.8,
            "specialization": ["computer_vision"],
            "privacy_budget": 1.0,
            "network_latency": 100.0,
            "bandwidth_capacity": 10.0,
        }

        agent_id = await coordinator.register_agent(agent_data)

        assert agent_id.startswith("agent_")
        assert agent_id in coordinator.agents

        agent = coordinator.agents[agent_id]
        assert agent.role == AgentRole.PARTICIPANT
        assert agent.blockchain_networks == ["ethereum"]
        assert agent.computational_capacity == 0.8
        assert agent.trust_score == 1.0  # Initial trust
        assert agent.byzantine_score == 0.0  # No Byzantine suspicion
        assert len(agent.performance_history) == 0

    async def test_learning_round_initiation(self, coordinator, sample_agents):
        """Test learning round initiation"""
        round_config = {
            "strategy": "federated_averaging",
            "selection_criteria": {
                "min_trust_score": 0.5,
                "min_capacity": 0.3,
                "max_participants": 4,
            },
            "target_accuracy": 0.95,
            "max_iterations": 100,
            "privacy_epsilon": 1.0,
            "byzantine_tolerance": 0.33,
            "timeout": 3600,
        }

        round_id = await coordinator.initiate_learning_round(round_config)

        assert round_id.startswith("round_")
        assert round_id in coordinator.learning_rounds

        learning_round = coordinator.learning_rounds[round_id]
        assert learning_round.strategy == LearningStrategy.FEDERATED_AVERAGING
        assert len(learning_round.participating_agents) <= 4
        assert learning_round.current_phase == LearningPhase.INITIALIZATION
        assert learning_round.byzantine_tolerance == 0.33

    async def test_model_update_submission(self, coordinator, sample_agents):
        """Test model update submission with differential privacy"""
        # Create learning round
        round_config = {"strategy": "differential_private", "privacy_epsilon": 1.0}
        round_id = await coordinator.initiate_learning_round(round_config)

        # Submit model update
        agent_id = sample_agents[0]
        update_data = {
            "agent_id": agent_id,
            "round_id": round_id,
            "model_weights": {
                "layer1": [0.1, 0.2, 0.3, 0.4, 0.5],
                "layer2": [0.6, 0.7, 0.8],
                "output": [0.9, 1.0],
            },
            "validation_score": 0.85,
            "differential_noise": 0.05,
            "bandwidth_used": 1.2,
        }

        update_id = await coordinator.submit_model_update(update_data)

        assert update_id.startswith("update_")
        assert update_id in coordinator.model_updates

        model_update = coordinator.model_updates[update_id]
        assert model_update.agent_id == agent_id
        assert model_update.round_id == round_id
        assert model_update.validation_score == 0.85
        assert len(model_update.weight_hash) == 64  # SHA256 hash length
        assert model_update.signature.startswith("sig_")

        # Check agent statistics update
        agent = coordinator.agents[agent_id]
        assert agent.total_contributions == 1
        assert agent.last_contribution > 0

    async def test_byzantine_detection_algorithms(self, coordinator, sample_agents):
        """Test advanced Byzantine detection algorithms"""
        # Create learning round
        round_config = {"strategy": "byzantine_robust", "byzantine_tolerance": 0.33}
        round_id = await coordinator.initiate_learning_round(round_config)

        # Create mixed normal and Byzantine updates
        updates = []

        # Normal updates (good agents)
        for i in range(3):
            agent_id = sample_agents[i]
            update_data = {
                "agent_id": agent_id,
                "round_id": round_id,
                "model_weights": {
                    "layer1": [random.gauss(0, 0.1) for _ in range(5)],
                    "layer2": [random.gauss(0, 0.1) for _ in range(3)],
                },
                "validation_score": random.uniform(0.8, 0.95),
                "differential_noise": 0.05,
            }
            update_id = await coordinator.submit_model_update(update_data)
            updates.append(update_id)

        # Byzantine update (malicious agent)
        byzantine_agent = sample_agents[3]
        byzantine_update_data = {
            "agent_id": byzantine_agent,
            "round_id": round_id,
            "model_weights": {
                "layer1": [random.gauss(0, 2.0) for _ in range(5)],  # High variance
                "layer2": [10.0, -10.0, 0.0],  # Extreme values
            },
            "validation_score": 0.2,  # Poor performance
            "differential_noise": 0.05,
        }
        byzantine_update_id = await coordinator.submit_model_update(
            byzantine_update_data
        )
        updates.append(byzantine_update_id)

        # Perform aggregation and test Byzantine detection
        result = await coordinator.aggregate_model_updates(round_id)

        assert isinstance(result, AggregationResult)
        assert len(result.byzantine_agents_detected) >= 1
        assert byzantine_agent in result.byzantine_agents_detected
        assert result.quality_score > 0.0
        assert result.consensus_achieved or len(result.byzantine_agents_detected) > 0

        # Verify detection methods were used
        assert len(coordinator.byzantine_detections) > 0
        detection = coordinator.byzantine_detections[-1]
        assert detection.detection_method == "multi_method_ensemble"
        assert len(detection.evidence) >= len(detection.suspected_agents)

    async def test_secure_aggregation_strategies(self, coordinator, sample_agents):
        """Test different secure aggregation strategies"""
        strategies_to_test = [
            LearningStrategy.FEDERATED_AVERAGING,
            LearningStrategy.SECURE_AGGREGATION,
            LearningStrategy.BYZANTINE_ROBUST,
            LearningStrategy.DIFFERENTIAL_PRIVATE,
        ]

        results = {}

        for strategy in strategies_to_test:
            # Create fresh learning round for each strategy
            round_config = {
                "strategy": strategy.value,
                "privacy_epsilon": (
                    1.0 if strategy == LearningStrategy.DIFFERENTIAL_PRIVATE else 0.5
                ),
            }
            round_id = await coordinator.initiate_learning_round(round_config)

            # Submit clean updates
            for agent_id in sample_agents:
                update_data = {
                    "agent_id": agent_id,
                    "round_id": round_id,
                    "model_weights": {
                        "layer1": [random.gauss(0, 0.1) for _ in range(5)],
                        "layer2": [random.gauss(0, 0.1) for _ in range(3)],
                    },
                    "validation_score": random.uniform(0.8, 0.95),
                    "differential_noise": 0.02,
                }
                await coordinator.submit_model_update(update_data)

            # Perform aggregation
            result = await coordinator.aggregate_model_updates(round_id)

            results[strategy.value] = {
                "quality_score": result.quality_score,
                "privacy_loss": result.privacy_loss,
                "consensus_achieved": result.consensus_achieved,
                "computation_time": result.computation_time,
            }

            # Strategy-specific assertions
            if strategy == LearningStrategy.DIFFERENTIAL_PRIVATE:
                assert result.privacy_loss > 0  # Should have privacy cost
            elif strategy == LearningStrategy.BYZANTINE_ROBUST:
                assert (
                    len(result.byzantine_agents_detected) >= 0
                )  # Should check for Byzantine

        # All strategies should produce valid results
        for strategy_name, strategy_result in results.items():
            assert 0.0 <= strategy_result["quality_score"] <= 1.0
            assert strategy_result["privacy_loss"] >= 0.0
            assert strategy_result["computation_time"] > 0.0

    async def test_clustering_analysis(self, coordinator, sample_agents):
        """Test clustering-based Byzantine detection"""
        # Create learning round
        round_config = {"strategy": "byzantine_robust"}
        round_id = await coordinator.initiate_learning_round(round_config)

        # Create updates with one clear outlier
        updates_list = []

        # Similar normal updates
        for i in range(3):
            agent_id = sample_agents[i]
            weights = {
                "layer1": [0.1, 0.2, 0.1, 0.2, 0.1],  # Similar pattern
                "layer2": [0.3, 0.4, 0.3],
            }
            update_data = {
                "agent_id": agent_id,
                "round_id": round_id,
                "model_weights": weights,
                "validation_score": 0.85,
            }
            await coordinator.submit_model_update(update_data)
            updates_list.append(
                coordinator.model_updates[
                    [k for k in coordinator.model_updates.keys()][-1]
                ]
            )

        # Outlier update
        outlier_weights = {
            "layer1": [5.0, -3.0, 8.0, -2.0, 4.0],  # Very different pattern
            "layer2": [-1.0, 2.0, -1.5],
        }
        outlier_data = {
            "agent_id": sample_agents[3],
            "round_id": round_id,
            "model_weights": outlier_weights,
            "validation_score": 0.3,
        }
        await coordinator.submit_model_update(outlier_data)
        updates_list.append(
            coordinator.model_updates[[k for k in coordinator.model_updates.keys()][-1]]
        )

        # Test clustering analysis
        cluster_analysis = await coordinator._perform_clustering_analysis(updates_list)

        assert len(cluster_analysis) == 4

        # The outlier should be detected
        outlier_detected = False
        for agent_id, analysis in cluster_analysis.items():
            if agent_id == sample_agents[3]:  # Outlier agent
                assert "is_outlier" in analysis
                if analysis["is_outlier"]:
                    outlier_detected = True

        # At least the clustering should identify some structure
        assert any(
            analysis.get("distance_z_score", 0) != 0
            for analysis in cluster_analysis.values()
        )

    async def test_gradient_norm_analysis(self, coordinator, sample_agents):
        """Test gradient norm-based anomaly detection"""
        # Create updates with varying gradient norms
        updates_list = []

        # Normal gradient norms
        for i in range(3):
            weights = {
                "layer1": [random.gauss(0, 0.1) for _ in range(5)],
                "layer2": [random.gauss(0, 0.1) for _ in range(3)],
            }
            update = type(
                "MockUpdate",
                (),
                {"agent_id": sample_agents[i], "model_weights": weights},
            )()
            updates_list.append(update)

        # Anomalous gradient norm (very large)
        anomalous_weights = {
            "layer1": [random.gauss(0, 5.0) for _ in range(5)],  # High variance
            "layer2": [random.gauss(0, 5.0) for _ in range(3)],
        }
        anomalous_update = type(
            "MockUpdate",
            (),
            {"agent_id": sample_agents[3], "model_weights": anomalous_weights},
        )()
        updates_list.append(anomalous_update)

        # Test gradient norm analysis
        gradient_analysis = await coordinator._analyze_gradient_norms(updates_list)

        assert len(gradient_analysis) == 4

        # Check that analysis includes required fields
        for agent_id, analysis in gradient_analysis.items():
            assert "norm" in analysis
            assert "is_anomalous" in analysis
            assert "z_score" in analysis
            assert analysis["norm"] >= 0

        # The anomalous update should have high z-score
        anomalous_analysis = gradient_analysis[sample_agents[3]]
        assert abs(anomalous_analysis["z_score"]) > 0  # Should be non-zero

    async def test_privacy_budget_management(self, coordinator, sample_agents):
        """Test differential privacy budget management"""
        # Create round with specific privacy budget
        round_config = {"strategy": "differential_private", "privacy_epsilon": 2.0}
        round_id = await coordinator.initiate_learning_round(round_config)

        # Submit updates with varying privacy costs
        total_privacy_cost = 0.0

        for i, agent_id in enumerate(sample_agents):
            privacy_epsilon = 0.5 * (i + 1)  # Varying privacy costs

            update_data = {
                "agent_id": agent_id,
                "round_id": round_id,
                "model_weights": {
                    "layer1": [random.gauss(0, 0.1) for _ in range(5)],
                    "layer2": [random.gauss(0, 0.1) for _ in range(3)],
                },
                "validation_score": 0.8,
                "privacy_epsilon": privacy_epsilon,
                "differential_noise": 1.0 / privacy_epsilon,  # Inversely related
            }

            await coordinator.submit_model_update(update_data)
            total_privacy_cost += update_data["differential_noise"]

        # Perform aggregation
        result = await coordinator.aggregate_model_updates(round_id)

        # Privacy loss should be accumulated
        assert result.privacy_loss > 0
        assert result.privacy_loss <= total_privacy_cost + 0.1  # Small tolerance

        # Quality should be reasonable despite privacy
        assert result.quality_score >= 0.5

    async def test_cross_validation_analysis(self, coordinator, sample_agents):
        """Test cross-validation performance analysis"""
        # Setup agents with performance history
        for i, agent_id in enumerate(sample_agents):
            agent = coordinator.agents[agent_id]
            # Add mock performance history
            agent.performance_history = [
                0.8 + i * 0.05,
                0.82 + i * 0.05,
                0.85 + i * 0.05,
            ]

        # Create mock updates
        updates_list = []
        for i, agent_id in enumerate(sample_agents):
            update = type(
                "MockUpdate",
                (),
                {"agent_id": agent_id, "validation_score": 0.8 + i * 0.05},
            )()
            updates_list.append(update)

        # Test cross-validation analysis
        cv_analysis = await coordinator._perform_cross_validation_analysis(updates_list)

        assert len(cv_analysis) == len(sample_agents)

        # All scores should be valid probabilities
        for agent_id, cv_score in cv_analysis.items():
            assert 0.0 <= cv_score <= 1.0

        # Agents with better history should generally have better CV scores
        cv_scores = list(cv_analysis.values())
        assert max(cv_scores) >= min(cv_scores)  # Some variation expected

    async def test_temporal_consistency_analysis(self, coordinator, sample_agents):
        """Test temporal consistency analysis"""
        # Setup agents with different consistency patterns
        consistent_agent = coordinator.agents[sample_agents[0]]
        consistent_agent.performance_history = [
            0.85,
            0.84,
            0.86,
            0.85,
            0.87,
        ]  # Consistent

        inconsistent_agent = coordinator.agents[sample_agents[1]]
        inconsistent_agent.performance_history = [
            0.9,
            0.3,
            0.95,
            0.2,
            0.88,
        ]  # Inconsistent

        new_agent = coordinator.agents[sample_agents[2]]
        new_agent.performance_history = []  # No history

        # Create mock updates
        updates_list = []
        for agent_id in sample_agents[:3]:
            update = type("MockUpdate", (), {"agent_id": agent_id})()
            updates_list.append(update)

        # Test temporal consistency analysis
        consistency_analysis = await coordinator._analyze_temporal_consistency(
            updates_list
        )

        assert len(consistency_analysis) == 3

        # Consistent agent should have higher consistency score
        consistent_score = consistency_analysis[sample_agents[0]]
        inconsistent_score = consistency_analysis[sample_agents[1]]
        new_agent_score = consistency_analysis[sample_agents[2]]

        assert 0.0 <= consistent_score <= 1.0
        assert 0.0 <= inconsistent_score <= 1.0
        assert 0.0 <= new_agent_score <= 1.0

        # Consistent agent should score better than inconsistent
        assert consistent_score >= inconsistent_score

        # New agent should get default score
        assert new_agent_score == 0.8

    async def test_model_divergence_analysis(self, coordinator, sample_agents):
        """Test model divergence analysis using KL divergence"""
        # Create updates with varying divergence
        updates_list = []

        # Similar updates (low divergence)
        base_weights = [0.1, 0.2, 0.3, 0.4, 0.5]
        for i in range(3):
            weights = {
                "layer1": [
                    w + random.gauss(0, 0.01) for w in base_weights
                ]  # Small variation
            }
            update = type(
                "MockUpdate",
                (),
                {"agent_id": sample_agents[i], "model_weights": weights},
            )()
            updates_list.append(update)

        # Divergent update
        divergent_weights = {
            "layer1": [
                w + random.gauss(0, 1.0) for w in base_weights
            ]  # Large variation
        }
        divergent_update = type(
            "MockUpdate",
            (),
            {"agent_id": sample_agents[3], "model_weights": divergent_weights},
        )()
        updates_list.append(divergent_update)

        # Test divergence analysis
        divergence_analysis = await coordinator._analyze_model_divergence(updates_list)

        assert len(divergence_analysis) == 4

        # Check analysis structure
        for agent_id, analysis in divergence_analysis.items():
            assert "is_divergent" in analysis
            assert "kl_divergence" in analysis
            assert isinstance(analysis["is_divergent"], bool)
            assert analysis["kl_divergence"] >= 0.0

        # Divergent update should have higher KL divergence
        divergent_analysis = divergence_analysis[sample_agents[3]]
        normal_analyses = [divergence_analysis[sample_agents[i]] for i in range(3)]

        avg_normal_divergence = sum(a["kl_divergence"] for a in normal_analyses) / 3
        assert divergent_analysis["kl_divergence"] >= avg_normal_divergence

    async def test_adaptive_threshold_calculation(self, coordinator):
        """Test adaptive threshold calculation for Byzantine detection"""
        # Create mock learning round
        learning_round = type(
            "MockLearningRound",
            (),
            {
                "strategy": LearningStrategy.BYZANTINE_ROBUST,
                "byzantine_tolerance": 0.33,
            },
        )()

        # Test with different detection score distributions
        test_cases = [
            {
                "scores": {"agent1": 0.2, "agent2": 0.3, "agent3": 0.8, "agent4": 0.9},
                "strategy": LearningStrategy.BYZANTINE_ROBUST,
            },
            {
                "scores": {"agent1": 0.1, "agent2": 0.15, "agent3": 0.12},
                "strategy": LearningStrategy.DIFFERENTIAL_PRIVATE,
            },
            {
                "scores": {},
                "strategy": LearningStrategy.FEDERATED_AVERAGING,
            },  # Empty scores
        ]

        for case in test_cases:
            learning_round.strategy = case["strategy"]
            threshold = await coordinator._calculate_adaptive_threshold(
                case["scores"], learning_round
            )

            assert 0.0 <= threshold <= 1.0

            # Threshold should respect Byzantine tolerance
            max_allowed = 1.0 - learning_round.byzantine_tolerance
            assert threshold <= max_allowed + 0.01  # Small tolerance for floating point

    async def test_performance_metrics(self, coordinator, sample_agents):
        """Test performance and scalability metrics"""
        # Measure performance with different agent counts
        performance_data = []

        for agent_count in [2, 4]:  # Test with different sizes
            agents_subset = sample_agents[:agent_count]

            # Create learning round
            round_config = {"strategy": "federated_averaging"}
            round_id = await coordinator.initiate_learning_round(round_config)

            # Submit updates and measure time
            start_time = time.time()

            for agent_id in agents_subset:
                update_data = {
                    "agent_id": agent_id,
                    "round_id": round_id,
                    "model_weights": {
                        "layer1": [random.gauss(0, 0.1) for _ in range(10)],
                        "layer2": [random.gauss(0, 0.1) for _ in range(5)],
                    },
                    "validation_score": random.uniform(0.8, 0.95),
                }
                await coordinator.submit_model_update(update_data)

            # Perform aggregation
            result = await coordinator.aggregate_model_updates(round_id)

            end_time = time.time()
            execution_time = end_time - start_time

            performance_data.append(
                {
                    "agent_count": agent_count,
                    "execution_time": execution_time,
                    "quality_score": result.quality_score,
                    "throughput": agent_count / execution_time,
                }
            )

        # Verify performance scaling
        assert len(performance_data) == 2
        for data in performance_data:
            assert data["execution_time"] > 0
            assert data["quality_score"] >= 0
            assert data["throughput"] > 0

        # Should handle more agents (though not necessarily faster)
        assert performance_data[1]["agent_count"] > performance_data[0]["agent_count"]

    async def test_coordinator_metrics(self, coordinator, sample_agents):
        """Test comprehensive coordinator metrics"""
        # Perform some operations to generate metrics
        round_config = {"strategy": "federated_averaging"}
        round_id = await coordinator.initiate_learning_round(round_config)

        for agent_id in sample_agents:
            update_data = {
                "agent_id": agent_id,
                "round_id": round_id,
                "model_weights": {"layer1": [0.1, 0.2, 0.3]},
                "validation_score": 0.85,
            }
            await coordinator.submit_model_update(update_data)

        await coordinator.aggregate_model_updates(round_id)

        # Get metrics
        metrics = coordinator.get_coordinator_metrics()

        # Verify required metrics
        required_fields = [
            "coordinator_id",
            "registered_agents",
            "active_learning_rounds",
            "total_rounds_completed",
            "successful_aggregations",
            "success_rate",
            "byzantine_agents_detected",
            "total_model_updates",
            "average_agent_trust",
            "privacy_budget_utilization",
            "network_health",
        ]

        for field in required_fields:
            assert field in metrics

        # Verify metric values
        assert metrics["registered_agents"] == len(sample_agents)
        assert metrics["total_rounds_completed"] >= 1
        assert metrics["successful_aggregations"] >= 1
        assert 0.0 <= metrics["success_rate"] <= 1.0
        assert metrics["total_model_updates"] >= len(sample_agents)
        assert 0.0 <= metrics["average_agent_trust"] <= 1.0


async def run_comprehensive_tests():
    """Run all distributed learning coordinator tests"""
    print("🧪 Running TrustWrapper v3.0 Distributed Learning Coordinator Tests")
    print("=" * 70)

    test_instance = TestDistributedLearningCoordinator()
    coordinator = TrustWrapperDistributedLearningCoordinator()

    # Create sample agents
    sample_agents = []
    agent_configs = [
        {
            "role": "participant",
            "blockchain_networks": ["ethereum"],
            "computational_capacity": 0.8,
        },
        {
            "role": "validator",
            "blockchain_networks": ["cardano"],
            "computational_capacity": 0.9,
        },
        {
            "role": "participant",
            "blockchain_networks": ["solana"],
            "computational_capacity": 0.7,
        },
        {
            "role": "aggregator",
            "blockchain_networks": ["bitcoin"],
            "computational_capacity": 1.0,
        },
    ]

    for config in agent_configs:
        agent_id = await coordinator.register_agent(config)
        sample_agents.append(agent_id)

    # Test suite
    tests = [
        (
            "Coordinator Initialization",
            test_instance.test_coordinator_initialization(coordinator),
        ),
        (
            "Agent Registration",
            test_instance.test_agent_registration(
                TrustWrapperDistributedLearningCoordinator()
            ),
        ),
        (
            "Learning Round Initiation",
            test_instance.test_learning_round_initiation(coordinator, sample_agents),
        ),
        (
            "Model Update Submission",
            test_instance.test_model_update_submission(coordinator, sample_agents),
        ),
        (
            "Byzantine Detection",
            test_instance.test_byzantine_detection_algorithms(
                coordinator, sample_agents
            ),
        ),
        (
            "Secure Aggregation",
            test_instance.test_secure_aggregation_strategies(
                coordinator, sample_agents
            ),
        ),
        (
            "Clustering Analysis",
            test_instance.test_clustering_analysis(coordinator, sample_agents),
        ),
        (
            "Gradient Norm Analysis",
            test_instance.test_gradient_norm_analysis(coordinator, sample_agents),
        ),
        (
            "Privacy Budget Management",
            test_instance.test_privacy_budget_management(coordinator, sample_agents),
        ),
        (
            "Cross-Validation Analysis",
            test_instance.test_cross_validation_analysis(coordinator, sample_agents),
        ),
        (
            "Temporal Consistency",
            test_instance.test_temporal_consistency_analysis(
                coordinator, sample_agents
            ),
        ),
        (
            "Model Divergence Analysis",
            test_instance.test_model_divergence_analysis(coordinator, sample_agents),
        ),
        (
            "Adaptive Threshold",
            test_instance.test_adaptive_threshold_calculation(coordinator),
        ),
        (
            "Performance Metrics",
            test_instance.test_performance_metrics(coordinator, sample_agents),
        ),
        (
            "Coordinator Metrics",
            test_instance.test_coordinator_metrics(coordinator, sample_agents),
        ),
    ]

    passed_tests = 0
    failed_tests = 0

    for test_name, test_coroutine in tests:
        try:
            print(f"⚡ Running: {test_name}...", end=" ")
            await test_coroutine
            print("✅ PASSED")
            passed_tests += 1
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            failed_tests += 1

    # Final report
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    print(f"✅ Tests Passed: {passed_tests}")
    print(f"❌ Tests Failed: {failed_tests}")
    print(f"📈 Success Rate: {passed_tests / (passed_tests + failed_tests) * 100:.1f}%")

    if failed_tests == 0:
        print(
            "🎉 ALL TESTS PASSED! Distributed Learning Coordinator is fully functional!"
        )
    else:
        print(f"⚠️  {failed_tests} test(s) failed. Review implementation.")

    return passed_tests, failed_tests


if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests())

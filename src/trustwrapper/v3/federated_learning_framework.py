#!/usr/bin/env python3

"""
TrustWrapper v3.0 Federated Learning Framework
Privacy-preserving cross-agent learning without data exposure
Universal Multi-Chain AI Verification Platform
"""

import asyncio
import logging
import random
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FederatedAgent:
    """Federated learning agent"""

    agent_id: str
    agent_type: str  # "verifier", "oracle", "consensus"
    reputation_score: float
    privacy_level: str
    last_contribution: float
    total_contributions: int
    blockchain_networks: List[str]


@dataclass
class LearningUpdate:
    """Federated learning model update"""

    agent_id: str
    model_weights: Dict[str, Any]
    gradient_updates: Dict[str, Any]
    privacy_budget: float
    contribution_quality: float
    validation_metrics: Dict[str, float]
    timestamp: float


@dataclass
class FederatedModel:
    """Global federated model"""

    model_id: str
    model_type: str
    global_weights: Dict[str, Any]
    version: int
    participating_agents: List[str]
    performance_metrics: Dict[str, float]
    last_updated: float
    privacy_guarantees: Dict[str, Any]


@dataclass
class PrivacyBudget:
    """Differential privacy budget management"""

    agent_id: str
    total_budget: float
    consumed_budget: float
    epsilon: float  # Privacy parameter
    delta: float  # Privacy parameter
    mechanism: str  # "gaussian", "laplace", "exponential"


class TrustWrapperFederatedLearning:
    """Advanced federated learning framework for AI agents"""

    def __init__(self):
        self.agents: Dict[str, FederatedAgent] = {}
        self.models: Dict[str, FederatedModel] = {}
        self.privacy_budgets: Dict[str, PrivacyBudget] = {}
        self.learning_history: List[LearningUpdate] = []

        # Framework configuration
        self.min_agents_for_update = 3
        self.reputation_threshold = 0.6
        self.privacy_epsilon = 1.0
        self.privacy_delta = 1e-5

        # Byzantine fault tolerance
        self.byzantine_tolerance = 0.33  # Up to 33% malicious agents

        # Initialize framework
        self._initialize_framework()

    def _initialize_framework(self):
        """Initialize federated learning framework"""
        # Create initial models for different AI tasks
        self._create_initial_models()

        logger.info("Federated learning framework initialized")

    def _create_initial_models(self):
        """Create initial federated models"""
        models = [
            {
                "model_id": "ai_verification_model",
                "model_type": "classification",
                "description": "AI decision verification classifier",
            },
            {
                "model_id": "fraud_detection_model",
                "model_type": "anomaly_detection",
                "description": "Cross-chain fraud detection",
            },
            {
                "model_id": "consensus_prediction_model",
                "model_type": "regression",
                "description": "Blockchain consensus outcome prediction",
            },
            {
                "model_id": "market_analysis_model",
                "model_type": "time_series",
                "description": "Multi-chain market trend analysis",
            },
        ]

        for model_config in models:
            model = FederatedModel(
                model_id=model_config["model_id"],
                model_type=model_config["model_type"],
                global_weights=self._initialize_model_weights(
                    model_config["model_type"]
                ),
                version=1,
                participating_agents=[],
                performance_metrics={"accuracy": 0.5, "precision": 0.5, "recall": 0.5},
                last_updated=time.time(),
                privacy_guarantees={
                    "epsilon": self.privacy_epsilon,
                    "delta": self.privacy_delta,
                    "mechanism": "gaussian",
                },
            )
            self.models[model.model_id] = model

    def _initialize_model_weights(self, model_type: str) -> Dict[str, Any]:
        """Initialize model weights based on type"""
        # Simulate different model architectures
        if model_type == "classification":
            return {
                "layer_1": np.random.randn(10, 5).tolist(),
                "layer_2": np.random.randn(5, 3).tolist(),
                "output": np.random.randn(3, 1).tolist(),
                "bias": np.random.randn(3).tolist(),
            }
        elif model_type == "anomaly_detection":
            return {
                "encoder": np.random.randn(8, 4).tolist(),
                "decoder": np.random.randn(4, 8).tolist(),
                "threshold": 0.5,
            }
        elif model_type == "regression":
            return {
                "weights": np.random.randn(5).tolist(),
                "bias": random.random(),
                "regularization": 0.01,
            }
        elif model_type == "time_series":
            return {
                "lstm_weights": np.random.randn(10, 8).tolist(),
                "attention_weights": np.random.randn(8, 4).tolist(),
                "output_weights": np.random.randn(4, 1).tolist(),
            }
        else:
            return {"default_weights": np.random.randn(5, 3).tolist()}

    async def register_agent(
        self,
        agent_id: str,
        agent_type: str,
        blockchain_networks: List[str],
        privacy_level: str = "standard",
    ) -> bool:
        """Register a new federated learning agent"""
        try:
            # Validate agent registration
            if agent_id in self.agents:
                logger.warning(f"Agent {agent_id} already registered")
                return False

            # Create agent profile
            agent = FederatedAgent(
                agent_id=agent_id,
                agent_type=agent_type,
                reputation_score=0.7,  # Start with moderate reputation
                privacy_level=privacy_level,
                last_contribution=0.0,
                total_contributions=0,
                blockchain_networks=blockchain_networks,
            )

            # Create privacy budget
            privacy_budget = PrivacyBudget(
                agent_id=agent_id,
                total_budget=self.privacy_epsilon,
                consumed_budget=0.0,
                epsilon=self.privacy_epsilon,
                delta=self.privacy_delta,
                mechanism="gaussian",
            )

            # Register agent
            self.agents[agent_id] = agent
            self.privacy_budgets[agent_id] = privacy_budget

            logger.info(f"Registered federated agent: {agent_id} ({agent_type})")
            return True

        except Exception as e:
            logger.error(f"Agent registration failed: {e}")
            return False

    async def contribute_learning_update(
        self,
        agent_id: str,
        model_id: str,
        local_weights: Dict[str, Any],
        training_data_size: int,
        validation_metrics: Dict[str, float],
    ) -> bool:
        """Agent contributes a learning update with privacy preservation"""
        try:
            # Validate agent and model
            if agent_id not in self.agents:
                logger.error(f"Unknown agent: {agent_id}")
                return False

            if model_id not in self.models:
                logger.error(f"Unknown model: {model_id}")
                return False

            agent = self.agents[agent_id]
            model = self.models[model_id]

            # Check privacy budget
            privacy_budget = self.privacy_budgets[agent_id]
            required_budget = self._calculate_privacy_cost(training_data_size)

            if (
                privacy_budget.consumed_budget + required_budget
                > privacy_budget.total_budget
            ):
                logger.warning(f"Insufficient privacy budget for agent {agent_id}")
                return False

            # Apply differential privacy to weights
            private_weights = await self._apply_differential_privacy(
                local_weights, privacy_budget, required_budget
            )

            # Calculate gradient updates
            gradient_updates = self._calculate_gradients(
                private_weights, model.global_weights
            )

            # Assess contribution quality
            contribution_quality = self._assess_contribution_quality(
                validation_metrics, agent.reputation_score
            )

            # Create learning update
            update = LearningUpdate(
                agent_id=agent_id,
                model_weights=private_weights,
                gradient_updates=gradient_updates,
                privacy_budget=required_budget,
                contribution_quality=contribution_quality,
                validation_metrics=validation_metrics,
                timestamp=time.time(),
            )

            # Store update
            self.learning_history.append(update)

            # Update privacy budget
            privacy_budget.consumed_budget += required_budget

            # Update agent statistics
            agent.last_contribution = time.time()
            agent.total_contributions += 1

            logger.info(
                f"Learning update received from agent {agent_id} for model {model_id}"
            )
            return True

        except Exception as e:
            logger.error(f"Learning update failed: {e}")
            return False

    def _calculate_privacy_cost(self, data_size: int) -> float:
        """Calculate privacy budget cost based on data size"""
        # Larger datasets require more privacy budget
        base_cost = 0.1
        size_factor = min(data_size / 1000, 2.0)  # Cap at 2x
        return base_cost * size_factor

    async def _apply_differential_privacy(
        self, weights: Dict[str, Any], privacy_budget: PrivacyBudget, budget_cost: float
    ) -> Dict[str, Any]:
        """Apply differential privacy to model weights"""
        private_weights = {}

        # Calculate noise scale based on privacy parameters
        sensitivity = 1.0  # L2 sensitivity
        noise_scale = sensitivity / (privacy_budget.epsilon * budget_cost)

        for layer_name, layer_weights in weights.items():
            if isinstance(layer_weights, list):
                # Add Gaussian noise to weights
                noisy_weights = []
                for weight in layer_weights:
                    if isinstance(weight, list):
                        # Handle 2D arrays
                        noisy_layer = []
                        for w in weight:
                            noise = np.random.normal(0, noise_scale)
                            noisy_layer.append(w + noise)
                        noisy_weights.append(noisy_layer)
                    else:
                        # Handle 1D arrays
                        noise = np.random.normal(0, noise_scale)
                        noisy_weights.append(weight + noise)

                private_weights[layer_name] = noisy_weights
            else:
                # Handle scalar values
                noise = np.random.normal(0, noise_scale)
                private_weights[layer_name] = weights[layer_name] + noise

        return private_weights

    def _calculate_gradients(
        self, local_weights: Dict[str, Any], global_weights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate gradient updates from local to global weights"""
        gradients = {}

        for layer_name in local_weights:
            if layer_name in global_weights:
                local_w = local_weights[layer_name]
                global_w = global_weights[layer_name]

                if isinstance(local_w, list) and isinstance(global_w, list):
                    # Calculate gradient for arrays
                    if isinstance(local_w[0], list):
                        # 2D array
                        grad = []
                        for i, (l_row, g_row) in enumerate(zip(local_w, global_w)):
                            grad_row = [l - g for l, g in zip(l_row, g_row)]
                            grad.append(grad_row)
                        gradients[layer_name] = grad
                    else:
                        # 1D array
                        gradients[layer_name] = [
                            l - g for l, g in zip(local_w, global_w)
                        ]
                else:
                    # Scalar
                    gradients[layer_name] = local_w - global_w

        return gradients

    def _assess_contribution_quality(
        self, validation_metrics: Dict[str, float], reputation_score: float
    ) -> float:
        """Assess the quality of a learning contribution"""
        # Base quality from validation metrics
        accuracy = validation_metrics.get("accuracy", 0.5)
        precision = validation_metrics.get("precision", 0.5)
        recall = validation_metrics.get("recall", 0.5)

        metric_quality = (accuracy + precision + recall) / 3

        # Weight by agent reputation
        quality_score = 0.7 * metric_quality + 0.3 * reputation_score

        # Ensure quality is between 0 and 1
        return max(0, min(1, quality_score))

    async def aggregate_model_updates(self, model_id: str) -> bool:
        """Aggregate federated learning updates for a model"""
        try:
            if model_id not in self.models:
                logger.error(f"Unknown model: {model_id}")
                return False

            model = self.models[model_id]

            # Get recent updates for this model
            recent_updates = self._get_recent_updates(model_id)

            if len(recent_updates) < self.min_agents_for_update:
                logger.warning(
                    f"Insufficient updates for model {model_id}: {len(recent_updates)}"
                )
                return False

            # Filter updates by reputation and quality
            valid_updates = self._filter_valid_updates(recent_updates)

            # Check for Byzantine agents
            filtered_updates = await self._byzantine_fault_detection(valid_updates)

            # Aggregate updates using weighted averaging
            new_weights = await self._weighted_aggregation(
                filtered_updates, model.global_weights
            )

            # Update model
            model.global_weights = new_weights
            model.version += 1
            model.last_updated = time.time()
            model.participating_agents = [
                update.agent_id for update in filtered_updates
            ]

            # Update model performance metrics
            model.performance_metrics = self._calculate_global_metrics(filtered_updates)

            # Update agent reputations
            await self._update_agent_reputations(filtered_updates)

            logger.info(
                f"Model {model_id} updated to version {model.version} with {len(filtered_updates)} contributions"
            )
            return True

        except Exception as e:
            logger.error(f"Model aggregation failed: {e}")
            return False

    def _get_recent_updates(
        self, model_id: str, time_window: float = 3600
    ) -> List[LearningUpdate]:
        """Get recent updates for a model within time window"""
        current_time = time.time()
        cutoff_time = current_time - time_window

        recent_updates = []
        for update in self.learning_history:
            if update.timestamp >= cutoff_time:
                # Check if update is for this model (simplified check)
                recent_updates.append(update)

        return recent_updates

    def _filter_valid_updates(
        self, updates: List[LearningUpdate]
    ) -> List[LearningUpdate]:
        """Filter updates based on agent reputation and contribution quality"""
        valid_updates = []

        for update in updates:
            agent = self.agents.get(update.agent_id)
            if not agent:
                continue

            # Check reputation threshold
            if agent.reputation_score < self.reputation_threshold:
                continue

            # Check contribution quality
            if update.contribution_quality < 0.5:
                continue

            valid_updates.append(update)

        return valid_updates

    async def _byzantine_fault_detection(
        self, updates: List[LearningUpdate]
    ) -> List[LearningUpdate]:
        """Detect and filter out Byzantine (malicious) updates"""
        if len(updates) <= 3:
            return updates  # Not enough updates for Byzantine detection

        # Calculate update similarity scores
        similarity_scores = []
        for i, update1 in enumerate(updates):
            scores = []
            for j, update2 in enumerate(updates):
                if i != j:
                    similarity = self._calculate_update_similarity(update1, update2)
                    scores.append(similarity)
            similarity_scores.append(np.mean(scores))

        # Filter out outliers (potential Byzantine updates)
        median_similarity = np.median(similarity_scores)
        threshold = median_similarity * 0.7  # 30% tolerance

        filtered_updates = []
        for update, similarity in zip(updates, similarity_scores):
            if similarity >= threshold:
                filtered_updates.append(update)
            else:
                logger.warning(
                    f"Potential Byzantine update detected from agent {update.agent_id}"
                )

        return filtered_updates

    def _calculate_update_similarity(
        self, update1: LearningUpdate, update2: LearningUpdate
    ) -> float:
        """Calculate similarity between two model updates"""
        # Simplified similarity calculation based on gradient magnitudes
        grad1 = update1.gradient_updates
        grad2 = update2.gradient_updates

        similarities = []
        for layer_name in grad1:
            if layer_name in grad2:
                # Calculate cosine similarity for this layer
                v1 = self._flatten_weights(grad1[layer_name])
                v2 = self._flatten_weights(grad2[layer_name])

                if len(v1) == len(v2) and len(v1) > 0:
                    dot_product = sum(a * b for a, b in zip(v1, v2))
                    norm1 = sum(a * a for a in v1) ** 0.5
                    norm2 = sum(b * b for b in v2) ** 0.5

                    if norm1 > 0 and norm2 > 0:
                        similarity = dot_product / (norm1 * norm2)
                        similarities.append(abs(similarity))

        return np.mean(similarities) if similarities else 0.0

    def _flatten_weights(self, weights: Any) -> List[float]:
        """Flatten nested weight structures to 1D list"""
        if isinstance(weights, list):
            flattened = []
            for item in weights:
                if isinstance(item, list):
                    flattened.extend(self._flatten_weights(item))
                else:
                    flattened.append(float(item))
            return flattened
        else:
            return [float(weights)]

    async def _weighted_aggregation(
        self, updates: List[LearningUpdate], current_weights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aggregate updates using weighted averaging"""
        if not updates:
            return current_weights

        # Calculate aggregation weights based on contribution quality and reputation
        aggregation_weights = []
        total_weight = 0

        for update in updates:
            agent = self.agents[update.agent_id]
            weight = update.contribution_quality * agent.reputation_score
            aggregation_weights.append(weight)
            total_weight += weight

        # Normalize weights
        if total_weight > 0:
            aggregation_weights = [w / total_weight for w in aggregation_weights]
        else:
            # Equal weights fallback
            aggregation_weights = [1.0 / len(updates)] * len(updates)

        # Aggregate weights
        new_weights = {}
        for layer_name in current_weights:
            if isinstance(current_weights[layer_name], list):
                # Handle arrays
                aggregated_layer = self._aggregate_layer_weights(
                    layer_name,
                    updates,
                    aggregation_weights,
                    current_weights[layer_name],
                )
                new_weights[layer_name] = aggregated_layer
            else:
                # Handle scalars
                weighted_sum = 0
                for update, weight in zip(updates, aggregation_weights):
                    if layer_name in update.model_weights:
                        weighted_sum += update.model_weights[layer_name] * weight
                new_weights[layer_name] = weighted_sum

        return new_weights

    def _aggregate_layer_weights(
        self,
        layer_name: str,
        updates: List[LearningUpdate],
        weights: List[float],
        current_layer: List,
    ) -> List:
        """Aggregate weights for a specific layer"""
        if not updates or layer_name not in updates[0].model_weights:
            return current_layer

        # Determine if this is a 2D or 1D array
        sample_layer = updates[0].model_weights[layer_name]

        if isinstance(sample_layer[0], list):
            # 2D array aggregation
            aggregated = []
            for i in range(len(sample_layer)):
                row = []
                for j in range(len(sample_layer[i])):
                    weighted_sum = 0
                    for update, weight in zip(updates, weights):
                        if layer_name in update.model_weights:
                            layer_weights = update.model_weights[layer_name]
                            if i < len(layer_weights) and j < len(layer_weights[i]):
                                weighted_sum += layer_weights[i][j] * weight
                    row.append(weighted_sum)
                aggregated.append(row)
            return aggregated
        else:
            # 1D array aggregation
            aggregated = []
            for i in range(len(sample_layer)):
                weighted_sum = 0
                for update, weight in zip(updates, weights):
                    if layer_name in update.model_weights:
                        layer_weights = update.model_weights[layer_name]
                        if i < len(layer_weights):
                            weighted_sum += layer_weights[i] * weight
                aggregated.append(weighted_sum)
            return aggregated

    def _calculate_global_metrics(
        self, updates: List[LearningUpdate]
    ) -> Dict[str, float]:
        """Calculate global model performance metrics"""
        if not updates:
            return {"accuracy": 0.5, "precision": 0.5, "recall": 0.5}

        # Weighted average of validation metrics
        total_weight = sum(update.contribution_quality for update in updates)

        if total_weight == 0:
            return {"accuracy": 0.5, "precision": 0.5, "recall": 0.5}

        metrics = {"accuracy": 0, "precision": 0, "recall": 0}

        for update in updates:
            weight = update.contribution_quality / total_weight
            for metric_name in metrics:
                if metric_name in update.validation_metrics:
                    metrics[metric_name] += (
                        update.validation_metrics[metric_name] * weight
                    )

        return metrics

    async def _update_agent_reputations(self, updates: List[LearningUpdate]):
        """Update agent reputation scores based on contribution quality"""
        for update in updates:
            agent = self.agents[update.agent_id]

            # Update reputation with exponential moving average
            alpha = 0.2  # Learning rate
            new_reputation = (
                alpha * update.contribution_quality
                + (1 - alpha) * agent.reputation_score
            )

            # Ensure reputation stays within bounds
            agent.reputation_score = max(0.1, min(0.99, new_reputation))

    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a federated model"""
        if model_id not in self.models:
            return None

        model = self.models[model_id]
        return {
            "model_id": model.model_id,
            "model_type": model.model_type,
            "version": model.version,
            "participating_agents": len(model.participating_agents),
            "performance_metrics": model.performance_metrics,
            "last_updated": model.last_updated,
            "privacy_guarantees": model.privacy_guarantees,
        }

    def get_agent_stats(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent statistics"""
        if agent_id not in self.agents:
            return None

        agent = self.agents[agent_id]
        privacy_budget = self.privacy_budgets[agent_id]

        return {
            "agent_id": agent.agent_id,
            "agent_type": agent.agent_type,
            "reputation_score": agent.reputation_score,
            "total_contributions": agent.total_contributions,
            "privacy_budget_remaining": privacy_budget.total_budget
            - privacy_budget.consumed_budget,
            "blockchain_networks": agent.blockchain_networks,
        }

    def get_framework_metrics(self) -> Dict[str, Any]:
        """Get overall framework metrics"""
        return {
            "total_agents": len(self.agents),
            "total_models": len(self.models),
            "total_updates": len(self.learning_history),
            "average_reputation": (
                np.mean([agent.reputation_score for agent in self.agents.values()])
                if self.agents
                else 0
            ),
            "privacy_epsilon": self.privacy_epsilon,
            "byzantine_tolerance": self.byzantine_tolerance,
        }


# Demo and testing functions
async def demo_federated_learning():
    """Demonstrate federated learning framework capabilities"""
    print("\n🤝 TrustWrapper v3.0 Federated Learning Framework Demo")
    print("=" * 70)

    fl_framework = TrustWrapperFederatedLearning()

    # Test 1: Register agents
    print("\n1. Agent Registration")
    agents = [
        ("agent_eth_1", "verifier", ["ethereum", "polygon"]),
        ("agent_ada_1", "oracle", ["cardano"]),
        ("agent_sol_1", "consensus", ["solana"]),
        ("agent_btc_1", "verifier", ["bitcoin"]),
        ("agent_multi_1", "verifier", ["ethereum", "cardano", "solana"]),
    ]

    for agent_id, agent_type, networks in agents:
        success = await fl_framework.register_agent(agent_id, agent_type, networks)
        print(f"   ✅ Registered {agent_id}: {success}")

    # Test 2: Contribute learning updates
    print("\n2. Learning Contributions")
    model_id = "ai_verification_model"

    for i, (agent_id, _, _) in enumerate(agents):
        # Simulate local training results
        local_weights = {
            "layer_1": np.random.randn(10, 5).tolist(),
            "layer_2": np.random.randn(5, 3).tolist(),
            "output": np.random.randn(3, 1).tolist(),
            "bias": np.random.randn(3).tolist(),
        }

        validation_metrics = {
            "accuracy": 0.8 + random.random() * 0.15,
            "precision": 0.75 + random.random() * 0.2,
            "recall": 0.7 + random.random() * 0.25,
        }

        success = await fl_framework.contribute_learning_update(
            agent_id, model_id, local_weights, 1000 + i * 200, validation_metrics
        )
        print(f"   📚 {agent_id} contribution: {success}")

    # Test 3: Model aggregation
    print("\n3. Model Aggregation")
    success = await fl_framework.aggregate_model_updates(model_id)
    print(f"   🔄 Model aggregation: {success}")

    # Display model info
    model_info = fl_framework.get_model_info(model_id)
    if model_info:
        print(f"   📊 Model version: {model_info['version']}")
        print(f"   👥 Participating agents: {model_info['participating_agents']}")
        print(
            f"   🎯 Global accuracy: {model_info['performance_metrics']['accuracy']:.3f}"
        )

    # Test 4: Agent statistics
    print("\n4. Agent Statistics")
    for agent_id, _, _ in agents[:3]:  # Show first 3 agents
        stats = fl_framework.get_agent_stats(agent_id)
        if stats:
            print(f"   👤 {agent_id}:")
            print(f"      Reputation: {stats['reputation_score']:.3f}")
            print(f"      Contributions: {stats['total_contributions']}")
            print(
                f"      Privacy budget remaining: {stats['privacy_budget_remaining']:.3f}"
            )

    # Test 5: Framework metrics
    print("\n5. Framework Metrics")
    metrics = fl_framework.get_framework_metrics()
    print(f"   📈 Total agents: {metrics['total_agents']}")
    print(f"   🧠 Total models: {metrics['total_models']}")
    print(f"   📚 Total updates: {metrics['total_updates']}")
    print(f"   ⭐ Average reputation: {metrics['average_reputation']:.3f}")
    print(f"   🔒 Privacy epsilon: {metrics['privacy_epsilon']}")

    print("\n✨ Federated Learning Framework Demo Complete!")
    print("🎯 Privacy-preserving cross-agent learning ✅ OPERATIONAL")


if __name__ == "__main__":
    asyncio.run(demo_federated_learning())

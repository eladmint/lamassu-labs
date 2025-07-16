#!/usr/bin/env python3

"""
TrustWrapper v3.0 Advanced Learning Features
Continual learning, model compression, and personalized learning paths
Universal Multi-Chain AI Verification Platform
"""

import logging
import math
import pickle
import secrets
import time
import zlib
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from .cross_agent_learning import (
    LearningDomain,
    TrustWrapperCrossAgentLearning,
)

# Import from other components
from .distributed_learning_coordinator import (
    TrustWrapperDistributedLearningCoordinator,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContinualLearningStrategy(Enum):
    ELASTIC_WEIGHT_CONSOLIDATION = "ewc"
    PROGRESSIVE_NEURAL_NETWORKS = "pnn"
    PACKNET = "packnet"
    EXPERIENCE_REPLAY = "experience_replay"
    GRADIENT_EPISODIC_MEMORY = "gem"
    META_LEARNING = "meta_learning"


class CompressionTechnique(Enum):
    QUANTIZATION = "quantization"
    PRUNING = "pruning"
    KNOWLEDGE_DISTILLATION = "distillation"
    LOW_RANK_FACTORIZATION = "low_rank"
    HUFFMAN_CODING = "huffman"
    TENSOR_DECOMPOSITION = "tensor_decomposition"


class PersonalizationStrategy(Enum):
    USER_CLUSTERING = "user_clustering"
    ADAPTIVE_LEARNING_RATE = "adaptive_lr"
    CURRICULUM_LEARNING = "curriculum"
    MULTI_TASK_LEARNING = "multi_task"
    FEDERATED_PERSONALIZATION = "federated_personal"
    CONTEXTUAL_BANDITS = "contextual_bandits"


@dataclass
class ContinualLearningTask:
    """Represents a task in continual learning"""

    task_id: str
    task_name: str
    domain: LearningDomain
    data_distribution: Dict[str, Any]
    performance_metrics: Dict[str, float]
    importance_weights: Optional[Dict[str, float]]  # For EWC
    task_embeddings: Optional[List[float]]  # For task similarity
    creation_time: float
    last_accessed: float
    access_count: int = 0


@dataclass
class CompressedModel:
    """Represents a compressed model"""

    model_id: str
    original_size: int  # bytes
    compressed_size: int  # bytes
    compression_ratio: float
    compression_technique: CompressionTechnique
    quality_loss: float  # 0.0 = no loss, 1.0 = complete loss
    decompression_time: float  # milliseconds
    metadata: Dict[str, Any]


@dataclass
class PersonalizedLearningPath:
    """Represents a personalized learning path for an agent"""

    path_id: str
    agent_id: str
    learning_style: str  # "visual", "sequential", "global", etc.
    skill_level: float  # 0.0-1.0
    learning_objectives: List[str]
    recommended_tasks: List[str]  # Task IDs
    progress_tracking: Dict[str, float]
    adaptation_history: List[Dict[str, Any]]
    performance_predictions: Dict[str, float]


@dataclass
class LearningMemory:
    """Episodic memory for continual learning"""

    memory_id: str
    task_id: str
    experience_data: Dict[str, Any]
    importance_score: float
    replay_count: int
    timestamp: float
    compressed: bool = False


@dataclass
class PerformanceAnalytics:
    """Analytics for learning performance"""

    analytics_id: str
    agent_id: str
    task_performances: Dict[str, float]  # task_id -> performance
    learning_efficiency: float
    forgetting_measure: float
    transfer_effectiveness: float
    personalization_impact: float
    compression_tolerance: float
    timestamp: float


class TrustWrapperAdvancedLearningFeatures:
    """Advanced learning features including continual learning, compression, and personalization"""

    def __init__(
        self,
        coordinator: TrustWrapperDistributedLearningCoordinator,
        cross_learning: TrustWrapperCrossAgentLearning,
    ):
        self.coordinator = coordinator
        self.cross_learning = cross_learning

        # Continual learning components
        self.tasks: Dict[str, ContinualLearningTask] = {}
        self.learning_memories: Dict[str, LearningMemory] = {}
        self.task_sequence: List[str] = []

        # Model compression
        self.compressed_models: Dict[str, CompressedModel] = {}
        self.compression_cache: Dict[str, bytes] = {}

        # Personalization
        self.learning_paths: Dict[str, PersonalizedLearningPath] = {}
        self.agent_profiles: Dict[str, Dict[str, Any]] = {}

        # Performance analytics
        self.performance_analytics: Dict[str, PerformanceAnalytics] = {}
        self.global_metrics = {
            "total_tasks_learned": 0,
            "average_forgetting": 0.0,
            "compression_efficiency": 0.0,
            "personalization_effectiveness": 0.0,
        }

        # Configuration
        self.config = {
            "memory_buffer_size": 1000,
            "replay_batch_size": 32,
            "compression_quality_threshold": 0.9,
            "personalization_update_frequency": 10,
            "task_similarity_threshold": 0.7,
            "forgetting_threshold": 0.2,
        }

        # Initialize subsystems
        self._initialize_continual_learning()
        self._initialize_compression_engine()
        self._initialize_personalization_system()

    def _initialize_continual_learning(self):
        """Initialize continual learning subsystem"""
        self.continual_strategies = {
            ContinualLearningStrategy.ELASTIC_WEIGHT_CONSOLIDATION: {
                "fisher_information_samples": 100,
                "ewc_lambda": 0.5,
                "online": True,
            },
            ContinualLearningStrategy.PROGRESSIVE_NEURAL_NETWORKS: {
                "lateral_connections": True,
                "adapter_size": 0.1,
                "freeze_previous": True,
            },
            ContinualLearningStrategy.PACKNET: {
                "pruning_ratio": 0.5,
                "iterative_pruning": True,
                "retrain_epochs": 5,
            },
            ContinualLearningStrategy.EXPERIENCE_REPLAY: {
                "buffer_size": 1000,
                "replay_frequency": 10,
                "prioritized": True,
            },
            ContinualLearningStrategy.GRADIENT_EPISODIC_MEMORY: {
                "memory_strength": 0.5,
                "gradient_alignment": True,
                "reference_gradients": 10,
            },
            ContinualLearningStrategy.META_LEARNING: {
                "inner_lr": 0.01,
                "outer_lr": 0.001,
                "adaptation_steps": 5,
            },
        }

        # Memory management
        self.memory_buffer = deque(maxlen=self.config["memory_buffer_size"])
        self.task_relationships = defaultdict(list)  # Task similarity graph

    def _initialize_compression_engine(self):
        """Initialize model compression engine"""
        self.compression_techniques = {
            CompressionTechnique.QUANTIZATION: {
                "bits": [8, 4, 2, 1],
                "symmetric": True,
                "per_channel": True,
            },
            CompressionTechnique.PRUNING: {
                "sparsity_levels": [0.5, 0.7, 0.9],
                "structured": True,
                "iterative": True,
            },
            CompressionTechnique.KNOWLEDGE_DISTILLATION: {
                "temperature": 3.0,
                "alpha": 0.7,
                "student_size_ratio": 0.3,
            },
            CompressionTechnique.LOW_RANK_FACTORIZATION: {
                "rank_ratio": 0.1,
                "decomposition": "svd",
                "iterative_refinement": True,
            },
            CompressionTechnique.HUFFMAN_CODING: {"adaptive": True, "block_size": 1024},
            CompressionTechnique.TENSOR_DECOMPOSITION: {
                "method": "tucker",
                "compression_ratio": 0.2,
                "rank_selection": "automatic",
            },
        }

    def _initialize_personalization_system(self):
        """Initialize personalization system"""
        self.personalization_strategies = {
            PersonalizationStrategy.USER_CLUSTERING: {
                "n_clusters": 5,
                "features": ["learning_speed", "error_patterns", "preferences"],
                "dynamic_clustering": True,
            },
            PersonalizationStrategy.ADAPTIVE_LEARNING_RATE: {
                "base_lr": 0.001,
                "adaptation_factor": 2.0,
                "performance_window": 10,
            },
            PersonalizationStrategy.CURRICULUM_LEARNING: {
                "difficulty_levels": 5,
                "progression_threshold": 0.8,
                "adaptive_pacing": True,
            },
            PersonalizationStrategy.MULTI_TASK_LEARNING: {
                "task_weights": "learned",
                "shared_layers_ratio": 0.7,
                "task_specific_heads": True,
            },
            PersonalizationStrategy.FEDERATED_PERSONALIZATION: {
                "local_epochs": 5,
                "personalization_layers": 2,
                "global_aggregation": "weighted",
            },
            PersonalizationStrategy.CONTEXTUAL_BANDITS: {
                "exploration_rate": 0.1,
                "context_features": 10,
                "update_frequency": 1,
            },
        }

        # Learning style classifiers
        self.learning_styles = [
            "visual",
            "auditory",
            "kinesthetic",
            "sequential",
            "global",
            "active",
            "reflective",
            "sensing",
            "intuitive",
        ]

    async def create_continual_task(
        self,
        task_name: str,
        domain: LearningDomain,
        data_distribution: Dict[str, Any],
        importance_weights: Optional[Dict[str, float]] = None,
    ) -> str:
        """Create a new task for continual learning"""
        task_id = f"task_{secrets.token_hex(8)}"

        # Generate task embeddings for similarity computation
        task_embeddings = self._generate_task_embeddings(domain, data_distribution)

        task = ContinualLearningTask(
            task_id=task_id,
            task_name=task_name,
            domain=domain,
            data_distribution=data_distribution,
            performance_metrics={},
            importance_weights=importance_weights,
            task_embeddings=task_embeddings,
            creation_time=time.time(),
            last_accessed=time.time(),
            access_count=0,
        )

        self.tasks[task_id] = task
        self.task_sequence.append(task_id)

        # Update task relationships
        await self._update_task_relationships(task_id)

        # Update global metrics
        self.global_metrics["total_tasks_learned"] += 1

        logger.info(f"Created continual learning task: {task_id} - {task_name}")

        return task_id

    async def apply_continual_learning(
        self,
        agent_id: str,
        task_id: str,
        model_update: Dict[str, Any],
        strategy: ContinualLearningStrategy,
        previous_tasks: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Apply continual learning strategy to prevent catastrophic forgetting"""
        if agent_id not in self.coordinator.agents:
            raise ValueError(f"Unknown agent: {agent_id}")

        if task_id not in self.tasks:
            raise ValueError(f"Unknown task: {task_id}")

        task = self.tasks[task_id]
        task.access_count += 1
        task.last_accessed = time.time()

        # Apply strategy-specific continual learning
        if strategy == ContinualLearningStrategy.ELASTIC_WEIGHT_CONSOLIDATION:
            result = await self._apply_ewc(
                agent_id, task_id, model_update, previous_tasks
            )

        elif strategy == ContinualLearningStrategy.PROGRESSIVE_NEURAL_NETWORKS:
            result = await self._apply_progressive_networks(
                agent_id, task_id, model_update
            )

        elif strategy == ContinualLearningStrategy.PACKNET:
            result = await self._apply_packnet(agent_id, task_id, model_update)

        elif strategy == ContinualLearningStrategy.EXPERIENCE_REPLAY:
            result = await self._apply_experience_replay(
                agent_id, task_id, model_update
            )

        elif strategy == ContinualLearningStrategy.GRADIENT_EPISODIC_MEMORY:
            result = await self._apply_gem(agent_id, task_id, model_update)

        elif strategy == ContinualLearningStrategy.META_LEARNING:
            result = await self._apply_meta_learning(agent_id, task_id, model_update)

        else:
            result = {"success": False, "error": "Unknown strategy"}

        # Store experience in memory
        if result.get("success", False):
            await self._store_learning_memory(agent_id, task_id, model_update, result)

        # Update performance metrics
        await self._update_continual_metrics(agent_id, task_id, result)

        return result

    async def compress_model(
        self,
        model_data: Dict[str, Any],
        technique: CompressionTechnique,
        quality_target: float = 0.9,
    ) -> CompressedModel:
        """Compress model using specified technique"""
        model_id = f"compressed_{secrets.token_hex(8)}"

        # Serialize original model
        original_bytes = pickle.dumps(model_data)
        original_size = len(original_bytes)

        # Apply compression technique
        start_time = time.time()

        if technique == CompressionTechnique.QUANTIZATION:
            compressed_data, quality_loss = await self._quantize_model(
                model_data, quality_target
            )

        elif technique == CompressionTechnique.PRUNING:
            compressed_data, quality_loss = await self._prune_model(
                model_data, quality_target
            )

        elif technique == CompressionTechnique.KNOWLEDGE_DISTILLATION:
            compressed_data, quality_loss = await self._distill_model(
                model_data, quality_target
            )

        elif technique == CompressionTechnique.LOW_RANK_FACTORIZATION:
            compressed_data, quality_loss = await self._low_rank_compress(
                model_data, quality_target
            )

        elif technique == CompressionTechnique.HUFFMAN_CODING:
            compressed_data, quality_loss = await self._huffman_compress(model_data)

        elif technique == CompressionTechnique.TENSOR_DECOMPOSITION:
            compressed_data, quality_loss = await self._tensor_decompose(
                model_data, quality_target
            )

        else:
            compressed_data = original_bytes
            quality_loss = 0.0

        compression_time = (time.time() - start_time) * 1000  # Convert to ms

        # Calculate compressed size
        compressed_bytes = pickle.dumps(compressed_data)
        compressed_size = len(compressed_bytes)

        # Additional compression with zlib
        zlib_compressed = zlib.compress(compressed_bytes, level=9)
        final_size = len(zlib_compressed)

        compressed_model = CompressedModel(
            model_id=model_id,
            original_size=original_size,
            compressed_size=final_size,
            compression_ratio=original_size / final_size,
            compression_technique=technique,
            quality_loss=quality_loss,
            decompression_time=compression_time * 0.3,  # Estimate
            metadata={
                "quality_target": quality_target,
                "compression_time": compression_time,
                "technique_params": self.compression_techniques[technique],
            },
        )

        self.compressed_models[model_id] = compressed_model
        self.compression_cache[model_id] = zlib_compressed

        # Update global metrics
        self._update_compression_metrics(compressed_model)

        logger.info(
            f"Compressed model {model_id}: {original_size} -> {final_size} bytes "
            f"(ratio: {compressed_model.compression_ratio:.2f}x)"
        )

        return compressed_model

    async def create_personalized_path(
        self,
        agent_id: str,
        learning_objectives: List[str],
        initial_assessment: Optional[Dict[str, float]] = None,
    ) -> str:
        """Create personalized learning path for an agent"""
        path_id = f"path_{secrets.token_hex(8)}"

        # Assess agent's learning style and skill level
        learning_style = await self._assess_learning_style(agent_id, initial_assessment)
        skill_level = await self._assess_skill_level(agent_id, initial_assessment)

        # Get agent profile
        if agent_id not in self.agent_profiles:
            self.agent_profiles[agent_id] = await self._create_agent_profile(agent_id)

        # Recommend tasks based on objectives and profile
        recommended_tasks = await self._recommend_tasks(
            agent_id, learning_objectives, skill_level
        )

        # Create learning path
        learning_path = PersonalizedLearningPath(
            path_id=path_id,
            agent_id=agent_id,
            learning_style=learning_style,
            skill_level=skill_level,
            learning_objectives=learning_objectives,
            recommended_tasks=recommended_tasks,
            progress_tracking={task: 0.0 for task in recommended_tasks},
            adaptation_history=[],
            performance_predictions=await self._predict_performance(
                agent_id, recommended_tasks
            ),
        )

        self.learning_paths[path_id] = learning_path

        logger.info(
            f"Created personalized learning path {path_id} for agent {agent_id}: "
            f"style={learning_style}, skill={skill_level:.2f}"
        )

        return path_id

    async def adapt_learning_path(
        self,
        path_id: str,
        performance_update: Dict[str, float],
        strategy: PersonalizationStrategy = PersonalizationStrategy.ADAPTIVE_LEARNING_RATE,
    ) -> Dict[str, Any]:
        """Adapt learning path based on performance"""
        if path_id not in self.learning_paths:
            raise ValueError(f"Unknown learning path: {path_id}")

        path = self.learning_paths[path_id]

        # Update progress tracking
        for task_id, performance in performance_update.items():
            if task_id in path.progress_tracking:
                path.progress_tracking[task_id] = performance

        # Apply personalization strategy
        adaptation_result = {}

        if strategy == PersonalizationStrategy.ADAPTIVE_LEARNING_RATE:
            adaptation_result = await self._adapt_learning_rate(
                path, performance_update
            )

        elif strategy == PersonalizationStrategy.CURRICULUM_LEARNING:
            adaptation_result = await self._adapt_curriculum(path, performance_update)

        elif strategy == PersonalizationStrategy.USER_CLUSTERING:
            adaptation_result = await self._adapt_by_clustering(
                path, performance_update
            )

        elif strategy == PersonalizationStrategy.MULTI_TASK_LEARNING:
            adaptation_result = await self._adapt_multi_task(path, performance_update)

        elif strategy == PersonalizationStrategy.FEDERATED_PERSONALIZATION:
            adaptation_result = await self._adapt_federated(path, performance_update)

        elif strategy == PersonalizationStrategy.CONTEXTUAL_BANDITS:
            adaptation_result = await self._adapt_contextual_bandits(
                path, performance_update
            )

        # Record adaptation
        path.adaptation_history.append(
            {
                "timestamp": time.time(),
                "strategy": strategy.value,
                "performance_update": performance_update,
                "adaptation_result": adaptation_result,
            }
        )

        # Update performance predictions
        path.performance_predictions = await self._predict_performance(
            path.agent_id, path.recommended_tasks
        )

        return adaptation_result

    async def analyze_learning_performance(
        self, agent_id: str, task_ids: Optional[List[str]] = None
    ) -> PerformanceAnalytics:
        """Analyze comprehensive learning performance"""
        analytics_id = f"analytics_{secrets.token_hex(8)}"

        # Get agent's performance history
        agent = self.coordinator.agents.get(agent_id)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_id}")

        # Analyze task performances
        if task_ids is None:
            task_ids = [
                t
                for t in self.task_sequence
                if agent_id in self._get_task_participants(t)
            ]

        task_performances = {}
        for task_id in task_ids:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                # Get agent's performance on this task
                task_performances[task_id] = await self._get_task_performance(
                    agent_id, task_id
                )

        # Calculate metrics
        learning_efficiency = await self._calculate_learning_efficiency(
            agent_id, task_performances
        )
        forgetting_measure = await self._calculate_forgetting_measure(
            agent_id, task_performances
        )
        transfer_effectiveness = await self._calculate_transfer_effectiveness(
            agent_id, task_ids
        )
        personalization_impact = await self._calculate_personalization_impact(agent_id)
        compression_tolerance = await self._calculate_compression_tolerance(agent_id)

        analytics = PerformanceAnalytics(
            analytics_id=analytics_id,
            agent_id=agent_id,
            task_performances=task_performances,
            learning_efficiency=learning_efficiency,
            forgetting_measure=forgetting_measure,
            transfer_effectiveness=transfer_effectiveness,
            personalization_impact=personalization_impact,
            compression_tolerance=compression_tolerance,
            timestamp=time.time(),
        )

        self.performance_analytics[analytics_id] = analytics

        # Update global metrics
        self._update_global_analytics(analytics)

        return analytics

    def _generate_task_embeddings(
        self, domain: LearningDomain, data_distribution: Dict[str, Any]
    ) -> List[float]:
        """Generate embeddings for task similarity computation"""
        # Simple embedding based on domain and distribution characteristics
        embeddings = []

        # Domain embedding (one-hot + characteristics)
        domain_vector = [0.0] * len(LearningDomain)
        domain_vector[list(LearningDomain).index(domain)] = 1.0
        embeddings.extend(domain_vector)

        # Data distribution features
        dist_features = [
            data_distribution.get("complexity", 0.5),
            data_distribution.get("size", 0.5),
            data_distribution.get("noise_level", 0.1),
            data_distribution.get("class_balance", 0.5),
            data_distribution.get("feature_dim", 0.0) / 100.0,  # Normalize
        ]
        embeddings.extend(dist_features)

        # Add random features for uniqueness
        embeddings.extend([np.random.random() * 0.1 for _ in range(5)])

        return embeddings

    async def _update_task_relationships(self, new_task_id: str):
        """Update task similarity relationships"""
        new_task = self.tasks[new_task_id]

        for existing_task_id, existing_task in self.tasks.items():
            if existing_task_id != new_task_id:
                # Calculate similarity
                similarity = self._calculate_task_similarity(
                    new_task.task_embeddings, existing_task.task_embeddings
                )

                if similarity > self.config["task_similarity_threshold"]:
                    self.task_relationships[new_task_id].append(
                        {"related_task": existing_task_id, "similarity": similarity}
                    )
                    self.task_relationships[existing_task_id].append(
                        {"related_task": new_task_id, "similarity": similarity}
                    )

    def _calculate_task_similarity(
        self, embeddings1: List[float], embeddings2: List[float]
    ) -> float:
        """Calculate cosine similarity between task embeddings"""
        if len(embeddings1) != len(embeddings2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(embeddings1, embeddings2))
        norm1 = math.sqrt(sum(a * a for a in embeddings1))
        norm2 = math.sqrt(sum(b * b for b in embeddings2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    async def _apply_ewc(
        self,
        agent_id: str,
        task_id: str,
        model_update: Dict[str, Any],
        previous_tasks: Optional[List[str]],
    ) -> Dict[str, Any]:
        """Apply Elastic Weight Consolidation"""
        ewc_params = self.continual_strategies[
            ContinualLearningStrategy.ELASTIC_WEIGHT_CONSOLIDATION
        ]

        # Calculate Fisher Information Matrix for important weights
        fisher_info = {}
        if previous_tasks:
            for prev_task_id in previous_tasks:
                if prev_task_id in self.tasks:
                    prev_task = self.tasks[prev_task_id]
                    if prev_task.importance_weights:
                        for param, importance in prev_task.importance_weights.items():
                            if param not in fisher_info:
                                fisher_info[param] = 0.0
                            fisher_info[param] += importance

        # Apply EWC penalty to model update
        ewc_lambda = ewc_params["ewc_lambda"]
        regularized_update = {}

        for param, value in model_update.items():
            if param in fisher_info:
                # Add quadratic penalty for changing important weights
                penalty = ewc_lambda * fisher_info[param]
                if isinstance(value, list):
                    regularized_update[param] = [
                        v * (1 - penalty) if isinstance(v, (int, float)) else v
                        for v in value
                    ]
                else:
                    regularized_update[param] = value
            else:
                regularized_update[param] = value

        # Calculate importance weights for current task
        current_importance = self._calculate_importance_weights(model_update)
        self.tasks[task_id].importance_weights = current_importance

        return {
            "success": True,
            "regularized_update": regularized_update,
            "fisher_information": fisher_info,
            "ewc_penalty_applied": len(fisher_info) > 0,
            "strategy": "elastic_weight_consolidation",
        }

    async def _apply_experience_replay(
        self, agent_id: str, task_id: str, model_update: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply experience replay for continual learning"""
        replay_params = self.continual_strategies[
            ContinualLearningStrategy.EXPERIENCE_REPLAY
        ]

        # Store current experience
        experience = {
            "task_id": task_id,
            "model_update": model_update,
            "timestamp": time.time(),
            "agent_id": agent_id,
        }
        self.memory_buffer.append(experience)

        # Sample replay batch
        replay_batch = []
        if len(self.memory_buffer) >= replay_params["replay_frequency"]:
            batch_size = min(self.config["replay_batch_size"], len(self.memory_buffer))

            if replay_params["prioritized"]:
                # Prioritized experience replay
                priorities = [
                    self._calculate_experience_priority(exp)
                    for exp in self.memory_buffer
                ]
                total_priority = sum(priorities)

                if total_priority > 0:
                    probabilities = [p / total_priority for p in priorities]
                    indices = np.random.choice(
                        len(self.memory_buffer),
                        size=batch_size,
                        p=probabilities,
                        replace=False,
                    )
                    replay_batch = [self.memory_buffer[i] for i in indices]
            else:
                # Uniform sampling
                indices = np.random.choice(
                    len(self.memory_buffer), size=batch_size, replace=False
                )
                replay_batch = [self.memory_buffer[i] for i in indices]

        # Combine current update with replayed experiences
        combined_update = self._combine_updates(model_update, replay_batch)

        return {
            "success": True,
            "combined_update": combined_update,
            "replay_batch_size": len(replay_batch),
            "memory_buffer_size": len(self.memory_buffer),
            "strategy": "experience_replay",
        }

    async def _store_learning_memory(
        self,
        agent_id: str,
        task_id: str,
        model_update: Dict[str, Any],
        learning_result: Dict[str, Any],
    ):
        """Store learning experience in episodic memory"""
        memory_id = f"memory_{secrets.token_hex(8)}"

        # Calculate importance score
        importance_score = learning_result.get("performance_gain", 0.0) * 0.5
        importance_score += (1.0 - learning_result.get("forgetting_measure", 0.0)) * 0.3
        importance_score += learning_result.get("transfer_effectiveness", 0.0) * 0.2

        memory = LearningMemory(
            memory_id=memory_id,
            task_id=task_id,
            experience_data={
                "agent_id": agent_id,
                "model_update": model_update,
                "learning_result": learning_result,
                "task_context": self.tasks[task_id].data_distribution,
            },
            importance_score=importance_score,
            replay_count=0,
            timestamp=time.time(),
        )

        self.learning_memories[memory_id] = memory

    async def _quantize_model(
        self, model_data: Dict[str, Any], quality_target: float
    ) -> Tuple[Dict[str, Any], float]:
        """Quantize model weights to reduce precision"""
        quant_params = self.compression_techniques[CompressionTechnique.QUANTIZATION]

        # Determine bit width based on quality target
        bits = 8 if quality_target > 0.9 else 4 if quality_target > 0.7 else 2

        quantized_model = {}
        total_error = 0.0
        total_params = 0

        for layer_name, layer_data in model_data.items():
            if isinstance(layer_data, list) and all(
                isinstance(v, (int, float)) for v in layer_data
            ):
                # Quantize numerical arrays
                min_val = min(layer_data)
                max_val = max(layer_data)
                scale = (max_val - min_val) / (2**bits - 1)

                quantized = []
                for value in layer_data:
                    quantized_val = int((value - min_val) / scale)
                    dequantized_val = quantized_val * scale + min_val
                    quantized.append(quantized_val)
                    total_error += abs(value - dequantized_val)
                    total_params += 1

                quantized_model[layer_name] = {
                    "quantized": quantized,
                    "scale": scale,
                    "min_val": min_val,
                    "bits": bits,
                }
            else:
                quantized_model[layer_name] = layer_data

        quality_loss = total_error / max(total_params, 1) if total_params > 0 else 0.0

        return quantized_model, quality_loss

    async def _prune_model(
        self, model_data: Dict[str, Any], quality_target: float
    ) -> Tuple[Dict[str, Any], float]:
        """Prune model by removing small weights"""
        prune_params = self.compression_techniques[CompressionTechnique.PRUNING]

        # Determine sparsity based on quality target
        sparsity = 0.5 if quality_target > 0.9 else 0.7 if quality_target > 0.7 else 0.9

        pruned_model = {}
        total_pruned = 0
        total_params = 0

        for layer_name, layer_data in model_data.items():
            if isinstance(layer_data, list) and all(
                isinstance(v, (int, float)) for v in layer_data
            ):
                # Calculate threshold for pruning
                abs_values = sorted([abs(v) for v in layer_data])
                threshold_idx = int(len(abs_values) * sparsity)
                threshold = (
                    abs_values[threshold_idx]
                    if threshold_idx < len(abs_values)
                    else 0.0
                )

                # Prune weights below threshold
                pruned = []
                mask = []
                for value in layer_data:
                    if abs(value) > threshold:
                        pruned.append(value)
                        mask.append(1)
                    else:
                        pruned.append(0.0)
                        mask.append(0)
                        total_pruned += 1
                    total_params += 1

                pruned_model[layer_name] = {
                    "values": pruned,
                    "mask": mask,
                    "sparsity": sum(1 - m for m in mask) / len(mask),
                }
            else:
                pruned_model[layer_name] = layer_data

        quality_loss = 1.0 - quality_target if total_params > 0 else 0.0

        return pruned_model, quality_loss

    async def _assess_learning_style(
        self, agent_id: str, initial_assessment: Optional[Dict[str, float]]
    ) -> str:
        """Assess agent's learning style"""
        if initial_assessment:
            # Use provided assessment
            scores = {
                style: initial_assessment.get(style, 0.0)
                for style in self.learning_styles
            }
        else:
            # Analyze agent's historical patterns
            agent = self.coordinator.agents.get(agent_id)
            if not agent or not agent.performance_history:
                return "sequential"  # Default

            # Simple heuristic based on performance variance
            variance = np.var(agent.performance_history)

            if variance < 0.01:
                return "sequential"  # Consistent, step-by-step learner
            elif variance < 0.05:
                return "global"  # Big picture learner
            else:
                return "active"  # Learn by doing

        # Return style with highest score
        return (
            max(scores.items(), key=lambda x: x[1])[0]
            if initial_assessment
            else "sequential"
        )

    async def _assess_skill_level(
        self, agent_id: str, initial_assessment: Optional[Dict[str, float]]
    ) -> float:
        """Assess agent's current skill level"""
        if initial_assessment and "skill_level" in initial_assessment:
            return max(0.0, min(1.0, initial_assessment["skill_level"]))

        # Analyze agent's performance
        agent = self.coordinator.agents.get(agent_id)
        if not agent:
            return 0.5  # Default medium skill

        # Base skill on recent performance
        if agent.performance_history:
            recent_performance = agent.performance_history[-5:]
            skill_level = np.mean(recent_performance)
        else:
            skill_level = 0.5

        # Adjust based on computational capacity
        skill_level = skill_level * 0.8 + agent.computational_capacity * 0.2

        return max(0.0, min(1.0, skill_level))

    async def _recommend_tasks(
        self, agent_id: str, objectives: List[str], skill_level: float
    ) -> List[str]:
        """Recommend tasks based on objectives and skill level"""
        recommended = []

        # Filter tasks by skill level appropriateness
        for task_id, task in self.tasks.items():
            task_difficulty = task.data_distribution.get("complexity", 0.5)

            # Match tasks to skill level
            if abs(task_difficulty - skill_level) < 0.3:
                # Check if task aligns with objectives
                task_description = task.task_name.lower()
                for objective in objectives:
                    if objective.lower() in task_description:
                        recommended.append(task_id)
                        break

        # If not enough recommendations, add related tasks
        if len(recommended) < 3:
            for task_id in recommended[:]:
                related = self.task_relationships.get(task_id, [])
                for rel in related:
                    if rel["related_task"] not in recommended:
                        recommended.append(rel["related_task"])
                    if len(recommended) >= 5:
                        break

        return recommended[:5]  # Limit to 5 recommendations

    def _calculate_importance_weights(
        self, model_update: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate importance weights for EWC"""
        importance_weights = {}

        for param, value in model_update.items():
            if isinstance(value, list) and all(
                isinstance(v, (int, float)) for v in value
            ):
                # Importance based on magnitude and variance
                magnitude = np.mean([abs(v) for v in value])
                variance = np.var(value)
                importance_weights[param] = magnitude * (1 + variance)
            else:
                importance_weights[param] = 1.0

        # Normalize
        total_importance = sum(importance_weights.values())
        if total_importance > 0:
            importance_weights = {
                k: v / total_importance for k, v in importance_weights.items()
            }

        return importance_weights

    def _calculate_experience_priority(self, experience: Dict[str, Any]) -> float:
        """Calculate priority for experience replay"""
        # Prioritize based on recency and task importance
        recency = time.time() - experience["timestamp"]
        recency_score = math.exp(-recency / 3600)  # Decay over 1 hour

        task_id = experience.get("task_id")
        task_importance = 1.0
        if task_id and task_id in self.tasks:
            task = self.tasks[task_id]
            task_importance = 1.0 + task.access_count * 0.1

        return recency_score * task_importance

    def _combine_updates(
        self, current_update: Dict[str, Any], replay_batch: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Combine current update with replayed experiences"""
        combined = current_update.copy()

        if not replay_batch:
            return combined

        # Weight current update more heavily
        current_weight = 0.7
        replay_weight = 0.3 / len(replay_batch)

        for replay_exp in replay_batch:
            replay_update = replay_exp.get("model_update", {})

            for param, value in replay_update.items():
                if param in combined and isinstance(value, list):
                    # Weighted average for numerical parameters
                    if all(isinstance(v, (int, float)) for v in value):
                        combined_values = []
                        for i, v in enumerate(value):
                            if i < len(combined[param]):
                                combined_val = (
                                    combined[param][i] * current_weight
                                    + v * replay_weight
                                )
                                combined_values.append(combined_val)
                        combined[param] = combined_values

        return combined

    async def _update_continual_metrics(
        self, agent_id: str, task_id: str, result: Dict[str, Any]
    ):
        """Update continual learning metrics"""
        # Track forgetting on previous tasks
        if len(self.task_sequence) > 1:
            forgetting_scores = []

            for prev_task_id in self.task_sequence[:-1]:
                if prev_task_id != task_id:
                    # Simulate performance check on previous task
                    prev_performance = await self._get_task_performance(
                        agent_id, prev_task_id
                    )
                    original_performance = self.tasks[
                        prev_task_id
                    ].performance_metrics.get(agent_id, 0.8)

                    forgetting = max(0, original_performance - prev_performance)
                    forgetting_scores.append(forgetting)

            if forgetting_scores:
                avg_forgetting = np.mean(forgetting_scores)
                self.global_metrics["average_forgetting"] = (
                    self.global_metrics["average_forgetting"] * 0.9
                    + avg_forgetting * 0.1
                )

    async def _get_task_performance(self, agent_id: str, task_id: str) -> float:
        """Get agent's performance on a specific task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            if agent_id in task.performance_metrics:
                return task.performance_metrics[agent_id]

        # Simulate performance based on agent characteristics
        agent = self.coordinator.agents.get(agent_id)
        if agent and agent.performance_history:
            return np.mean(agent.performance_history[-3:]) * random.uniform(0.9, 1.1)

        return 0.7  # Default

    def _get_task_participants(self, task_id: str) -> Set[str]:
        """Get agents that participated in a task"""
        participants = set()

        # Check learning memories
        for memory in self.learning_memories.values():
            if memory.task_id == task_id:
                exp_data = memory.experience_data
                if "agent_id" in exp_data:
                    participants.add(exp_data["agent_id"])

        return participants

    def _update_compression_metrics(self, compressed_model: CompressedModel):
        """Update global compression metrics"""
        current_efficiency = self.global_metrics["compression_efficiency"]
        new_ratio = compressed_model.compression_ratio

        # Exponential moving average
        self.global_metrics["compression_efficiency"] = (
            current_efficiency * 0.9 + new_ratio * 0.1
        )

    async def _calculate_learning_efficiency(
        self, agent_id: str, task_performances: Dict[str, float]
    ) -> float:
        """Calculate learning efficiency"""
        if not task_performances:
            return 0.5

        # Efficiency based on performance improvement rate
        performances = list(task_performances.values())
        if len(performances) < 2:
            return performances[0] if performances else 0.5

        # Calculate improvement trend
        improvements = []
        for i in range(1, len(performances)):
            improvement = performances[i] - performances[i - 1]
            improvements.append(improvement)

        # Average improvement rate
        avg_improvement = np.mean(improvements)

        # Normalize to 0-1 scale
        efficiency = 0.5 + avg_improvement  # Center at 0.5
        return max(0.0, min(1.0, efficiency))

    async def _calculate_forgetting_measure(
        self, agent_id: str, task_performances: Dict[str, float]
    ) -> float:
        """Calculate catastrophic forgetting measure"""
        if len(task_performances) < 2:
            return 0.0

        # Check performance drop on earlier tasks
        task_list = list(task_performances.keys())
        forgetting_scores = []

        for i in range(len(task_list) - 1):
            early_task = task_list[i]
            # Simulate re-evaluation
            current_perf = await self._get_task_performance(agent_id, early_task)
            original_perf = task_performances[early_task]

            forgetting = max(0, original_perf - current_perf)
            forgetting_scores.append(forgetting)

        return np.mean(forgetting_scores) if forgetting_scores else 0.0

    async def _calculate_transfer_effectiveness(
        self, agent_id: str, task_ids: List[str]
    ) -> float:
        """Calculate positive transfer between tasks"""
        if len(task_ids) < 2:
            return 0.5

        transfer_scores = []

        for i in range(1, len(task_ids)):
            current_task = task_ids[i]

            # Check if related tasks helped
            related_tasks = self.task_relationships.get(current_task, [])
            relevant_previous = [
                rel["related_task"]
                for rel in related_tasks
                if rel["related_task"] in task_ids[:i]
            ]

            if relevant_previous:
                # Higher score if learned from related tasks
                transfer_score = 0.8 + 0.2 * len(relevant_previous) / i
            else:
                transfer_score = 0.5

            transfer_scores.append(transfer_score)

        return np.mean(transfer_scores) if transfer_scores else 0.5

    async def _calculate_personalization_impact(self, agent_id: str) -> float:
        """Calculate impact of personalization"""
        # Check if agent has personalized path
        agent_paths = [
            path for path in self.learning_paths.values() if path.agent_id == agent_id
        ]

        if not agent_paths:
            return 0.0

        # Calculate improvement from personalization
        impact_scores = []

        for path in agent_paths:
            if path.adaptation_history:
                # Compare predicted vs actual performance
                predictions = path.performance_predictions
                actual = path.progress_tracking

                if predictions and actual:
                    # Lower error means better personalization
                    errors = []
                    for task_id in predictions:
                        if task_id in actual:
                            error = abs(predictions[task_id] - actual[task_id])
                            errors.append(error)

                    if errors:
                        avg_error = np.mean(errors)
                        impact = 1.0 - avg_error  # Convert error to impact
                        impact_scores.append(impact)

        return np.mean(impact_scores) if impact_scores else 0.5

    async def _calculate_compression_tolerance(self, agent_id: str) -> float:
        """Calculate agent's tolerance for model compression"""
        # Check compression history
        agent_compressions = []

        for model_id, compressed in self.compressed_models.items():
            # Check if this compression was for this agent
            if (
                "agent_id" in compressed.metadata
                and compressed.metadata["agent_id"] == agent_id
            ):
                # Tolerance based on quality loss vs compression ratio
                tolerance = compressed.compression_ratio / (1 + compressed.quality_loss)
                agent_compressions.append(tolerance)

        if agent_compressions:
            return np.mean(agent_compressions)

        # Default based on computational capacity
        agent = self.coordinator.agents.get(agent_id)
        if agent:
            # Lower capacity agents more tolerant of compression
            return 1.0 - agent.computational_capacity * 0.5

        return 0.5

    def _update_global_analytics(self, analytics: PerformanceAnalytics):
        """Update global performance metrics"""
        # Update personalization effectiveness
        current_effectiveness = self.global_metrics["personalization_effectiveness"]
        new_impact = analytics.personalization_impact

        self.global_metrics["personalization_effectiveness"] = (
            current_effectiveness * 0.9 + new_impact * 0.1
        )

    async def _predict_performance(
        self, agent_id: str, task_ids: List[str]
    ) -> Dict[str, float]:
        """Predict agent's performance on tasks"""
        predictions = {}

        agent = self.coordinator.agents.get(agent_id)
        if not agent:
            return {task_id: 0.5 for task_id in task_ids}

        base_performance = (
            np.mean(agent.performance_history) if agent.performance_history else 0.5
        )

        for task_id in task_ids:
            if task_id in self.tasks:
                task = self.tasks[task_id]

                # Adjust based on task complexity
                complexity = task.data_distribution.get("complexity", 0.5)
                performance = base_performance * (1.5 - complexity)

                # Adjust based on domain match
                agent_domains = set(agent.learning_specialization)
                if task.domain.value in agent_domains:
                    performance *= 1.2

                predictions[task_id] = max(0.0, min(1.0, performance))
            else:
                predictions[task_id] = base_performance

        return predictions

    async def _create_agent_profile(self, agent_id: str) -> Dict[str, Any]:
        """Create comprehensive agent profile"""
        agent = self.coordinator.agents.get(agent_id)
        if not agent:
            return {}

        profile = {
            "agent_id": agent_id,
            "learning_characteristics": {
                "computational_capacity": agent.computational_capacity,
                "trust_score": agent.trust_score,
                "specializations": agent.learning_specialization,
                "performance_trend": (
                    "improving"
                    if len(agent.performance_history) > 1
                    and agent.performance_history[-1] > agent.performance_history[0]
                    else "stable"
                ),
            },
            "learning_preferences": {
                "preferred_batch_size": 32,
                "optimal_learning_rate": 0.001,
                "regularization_preference": 0.1,
            },
            "historical_metrics": {
                "average_performance": (
                    np.mean(agent.performance_history)
                    if agent.performance_history
                    else 0.5
                ),
                "performance_variance": (
                    np.var(agent.performance_history)
                    if agent.performance_history
                    else 0.0
                ),
                "total_tasks_learned": len(
                    [
                        m
                        for m in self.learning_memories.values()
                        if m.experience_data.get("agent_id") == agent_id
                    ]
                ),
            },
        }

        return profile

    async def _adapt_learning_rate(
        self, path: PersonalizedLearningPath, performance_update: Dict[str, float]
    ) -> Dict[str, Any]:
        """Adapt learning rate based on performance"""
        adapt_params = self.personalization_strategies[
            PersonalizationStrategy.ADAPTIVE_LEARNING_RATE
        ]

        # Calculate performance trend
        recent_performances = list(performance_update.values())[
            -adapt_params["performance_window"] :
        ]

        if len(recent_performances) < 2:
            return {"learning_rate": adapt_params["base_lr"]}

        # Calculate trend
        performance_diff = recent_performances[-1] - recent_performances[0]

        # Adapt learning rate
        if performance_diff > 0.1:  # Improving rapidly
            new_lr = adapt_params["base_lr"] * adapt_params["adaptation_factor"]
        elif performance_diff < -0.1:  # Declining
            new_lr = adapt_params["base_lr"] / adapt_params["adaptation_factor"]
        else:  # Stable
            new_lr = adapt_params["base_lr"]

        return {
            "learning_rate": new_lr,
            "performance_trend": "improving" if performance_diff > 0 else "declining",
            "adaptation_reason": "performance_based",
        }

    async def _adapt_curriculum(
        self, path: PersonalizedLearningPath, performance_update: Dict[str, float]
    ) -> Dict[str, Any]:
        """Adapt curriculum difficulty based on performance"""
        curriculum_params = self.personalization_strategies[
            PersonalizationStrategy.CURRICULUM_LEARNING
        ]

        # Calculate average performance
        avg_performance = (
            np.mean(list(performance_update.values())) if performance_update else 0.5
        )

        # Determine difficulty adjustment
        if avg_performance > curriculum_params["progression_threshold"]:
            # Increase difficulty
            new_tasks = []
            for task_id in self.tasks:
                task = self.tasks[task_id]
                if task.data_distribution.get("complexity", 0.5) > path.skill_level:
                    new_tasks.append(task_id)

            # Update recommended tasks
            path.recommended_tasks.extend(new_tasks[:2])
            path.skill_level = min(1.0, path.skill_level + 0.1)

            return {
                "difficulty_increased": True,
                "new_skill_level": path.skill_level,
                "added_tasks": new_tasks[:2],
            }
        else:
            # Maintain or reduce difficulty
            return {
                "difficulty_increased": False,
                "skill_level": path.skill_level,
                "recommendation": "continue_current_level",
            }

    def get_advanced_learning_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics for advanced learning features"""
        return {
            "continual_learning": {
                "total_tasks": len(self.tasks),
                "active_memories": len(self.learning_memories),
                "average_forgetting": self.global_metrics["average_forgetting"],
                "memory_buffer_size": len(self.memory_buffer),
                "task_relationships": sum(
                    len(rels) for rels in self.task_relationships.values()
                ),
            },
            "model_compression": {
                "total_compressions": len(self.compressed_models),
                "average_compression_ratio": self.global_metrics[
                    "compression_efficiency"
                ],
                "cache_size": len(self.compression_cache),
                "quality_preserved": (
                    np.mean(
                        [
                            1.0 - model.quality_loss
                            for model in self.compressed_models.values()
                        ]
                    )
                    if self.compressed_models
                    else 1.0
                ),
            },
            "personalization": {
                "active_learning_paths": len(self.learning_paths),
                "agent_profiles": len(self.agent_profiles),
                "average_effectiveness": self.global_metrics[
                    "personalization_effectiveness"
                ],
                "total_adaptations": sum(
                    len(path.adaptation_history)
                    for path in self.learning_paths.values()
                ),
            },
            "performance_analytics": {
                "total_analytics": len(self.performance_analytics),
                "monitored_agents": len(
                    set(
                        analytics.agent_id
                        for analytics in self.performance_analytics.values()
                    )
                ),
            },
        }

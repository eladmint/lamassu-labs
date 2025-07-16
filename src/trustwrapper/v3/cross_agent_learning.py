#!/usr/bin/env python3

"""
TrustWrapper v3.0 Cross-Agent Learning System
Advanced inter-agent knowledge sharing with privacy preservation
Universal Multi-Chain AI Verification Platform
"""

import hashlib
import json
import logging
import math
import random
import secrets
import time
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Import from distributed learning coordinator
from .distributed_learning_coordinator import (
    TrustWrapperDistributedLearningCoordinator,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeSharingStrategy(Enum):
    PEER_TO_PEER = "peer_to_peer"
    HIERARCHICAL = "hierarchical"
    FEDERATED_TRANSFER = "federated_transfer"
    SELECTIVE_SHARING = "selective_sharing"
    PRIVACY_PRESERVED = "privacy_preserved"
    REPUTATION_WEIGHTED = "reputation_weighted"


class SharingPrivacyLevel(Enum):
    PUBLIC = "public"  # Full model sharing
    PROTECTED = "protected"  # Differential privacy applied
    CONFIDENTIAL = "confidential"  # Encrypted sharing only
    SECRET = "secret"  # No direct sharing, only aggregates


class LearningDomain(Enum):
    COMPUTER_VISION = "computer_vision"
    NATURAL_LANGUAGE = "natural_language"
    REINFORCEMENT = "reinforcement"
    TIME_SERIES = "time_series"
    RECOMMENDATION = "recommendation"
    CROSS_DOMAIN = "cross_domain"


@dataclass
class KnowledgePacket:
    """Represents shared knowledge between agents"""

    packet_id: str
    source_agent: str
    target_agents: List[str]  # Empty list means broadcast
    knowledge_type: str  # "model_weights", "gradients", "features", "strategies"
    knowledge_data: Dict[str, Any]
    domain: LearningDomain
    privacy_level: SharingPrivacyLevel
    encryption_key: Optional[str]
    timestamp: float
    expiry_time: float
    trust_requirement: float  # Minimum trust score to receive
    performance_threshold: float  # Minimum performance to share
    metadata: Dict[str, Any]


@dataclass
class LearningExperience:
    """Represents an agent's learning experience to share"""

    experience_id: str
    agent_id: str
    domain: LearningDomain
    task_description: str
    performance_metrics: Dict[str, float]
    learned_patterns: List[Dict[str, Any]]
    failure_cases: List[Dict[str, Any]]
    optimization_hints: Dict[str, Any]
    timestamp: float


@dataclass
class KnowledgeTransferResult:
    """Result of knowledge transfer between agents"""

    transfer_id: str
    source_agent: str
    recipient_agents: List[str]
    knowledge_packets: List[str]
    transfer_strategy: KnowledgeSharingStrategy
    privacy_preserved: bool
    transfer_quality: float  # 0.0-1.0
    recipient_improvements: Dict[str, float]  # agent_id -> improvement
    privacy_cost: float
    bandwidth_used: float
    timestamp: float
    success: bool
    metadata: Dict[str, Any]


@dataclass
class CollaborativeLearningRound:
    """Collaborative learning round with knowledge sharing"""

    round_id: str
    participating_agents: List[str]
    sharing_strategy: KnowledgeSharingStrategy
    primary_domain: LearningDomain
    cross_domain_enabled: bool
    privacy_budget: float
    performance_target: float
    knowledge_pool: List[KnowledgePacket]
    start_time: float
    end_time: Optional[float]
    round_metrics: Dict[str, Any]


class TrustWrapperCrossAgentLearning:
    """Advanced cross-agent learning system with privacy-preserving knowledge sharing"""

    def __init__(self, coordinator: TrustWrapperDistributedLearningCoordinator):
        self.coordinator = coordinator
        self.knowledge_packets: Dict[str, KnowledgePacket] = {}
        self.learning_experiences: Dict[str, LearningExperience] = {}
        self.transfer_results: Dict[str, KnowledgeTransferResult] = {}
        self.collaborative_rounds: Dict[str, CollaborativeLearningRound] = {}

        # Knowledge sharing configuration
        self.sharing_config = {
            "min_trust_for_sharing": 0.6,
            "min_performance_for_sharing": 0.7,
            "max_privacy_loss_per_round": 1.0,
            "knowledge_expiry_time": 3600,  # 1 hour
            "max_concurrent_transfers": 20,
            "bandwidth_limit_per_agent": 10.0,  # MB/s
        }

        # Performance tracking
        self.total_knowledge_transfers = 0
        self.successful_transfers = 0
        self.privacy_violations = 0
        self.average_transfer_quality = 0.0

        # Knowledge graph for agent relationships
        self.agent_knowledge_graph = defaultdict(
            lambda: {
                "shared_with": set(),
                "learned_from": set(),
                "domains": set(),
                "transfer_history": [],
            }
        )

        # Initialize knowledge sharing system
        self._initialize_knowledge_system()

    def _initialize_knowledge_system(self):
        """Initialize the cross-agent knowledge sharing system"""
        logger.info("Initializing Cross-Agent Learning System")

        # Initialize sharing strategies
        self._initialize_sharing_strategies()

        # Initialize privacy mechanisms
        self._initialize_privacy_mechanisms()

        # Initialize reputation system
        self._initialize_reputation_system()

        # Initialize learning incentives
        self._initialize_learning_incentives()

    def _initialize_sharing_strategies(self):
        """Initialize different knowledge sharing strategies"""
        self.sharing_strategies = {
            KnowledgeSharingStrategy.PEER_TO_PEER: {
                "description": "Direct agent-to-agent knowledge transfer",
                "privacy_cost": 0.3,
                "efficiency": 0.9,
                "suitable_for": ["similar_domains", "high_trust"],
            },
            KnowledgeSharingStrategy.HIERARCHICAL: {
                "description": "Knowledge flows through trusted aggregators",
                "privacy_cost": 0.2,
                "efficiency": 0.8,
                "suitable_for": ["large_networks", "mixed_trust"],
            },
            KnowledgeSharingStrategy.FEDERATED_TRANSFER: {
                "description": "Centralized knowledge distillation and redistribution",
                "privacy_cost": 0.4,
                "efficiency": 0.7,
                "suitable_for": ["cross_domain", "heterogeneous_agents"],
            },
            KnowledgeSharingStrategy.SELECTIVE_SHARING: {
                "description": "Agents choose specific knowledge to share",
                "privacy_cost": 0.1,
                "efficiency": 0.95,
                "suitable_for": ["high_privacy", "specialized_knowledge"],
            },
            KnowledgeSharingStrategy.PRIVACY_PRESERVED: {
                "description": "Fully encrypted knowledge sharing with homomorphic operations",
                "privacy_cost": 0.05,
                "efficiency": 0.6,
                "suitable_for": ["sensitive_data", "regulatory_compliance"],
            },
            KnowledgeSharingStrategy.REPUTATION_WEIGHTED: {
                "description": "Knowledge weighted by agent reputation and performance",
                "privacy_cost": 0.25,
                "efficiency": 0.85,
                "suitable_for": ["quality_focus", "Byzantine_resilience"],
            },
        }

    def _initialize_privacy_mechanisms(self):
        """Initialize privacy-preserving mechanisms for knowledge sharing"""
        self.privacy_mechanisms = {
            "differential_privacy": {
                "noise_scale": lambda epsilon: 1.0 / epsilon,
                "composition": "advanced",
                "clip_threshold": 1.0,
            },
            "secure_aggregation": {
                "protocol": "shamir_sharing",
                "threshold": 0.67,
                "encryption": "aes256",
            },
            "homomorphic_transfer": {
                "scheme": "paillier",
                "key_size": 2048,
                "operations": ["add", "scalar_multiply"],
            },
            "knowledge_distillation": {
                "temperature": 3.0,
                "compression_ratio": 0.1,
                "privacy_amplification": True,
            },
        }

    def _initialize_reputation_system(self):
        """Initialize reputation system for knowledge quality"""
        self.reputation_system = {
            "base_reputation": 0.5,
            "reputation_decay": 0.95,  # Per round
            "quality_weight": 0.4,
            "consistency_weight": 0.3,
            "innovation_weight": 0.3,
            "penalty_for_bad_knowledge": 0.1,
            "reward_for_good_knowledge": 0.05,
        }

    def _initialize_learning_incentives(self):
        """Initialize incentive mechanisms for knowledge sharing"""
        self.learning_incentives = {
            "base_reward": 1.0,
            "quality_multiplier": 2.0,
            "scarcity_bonus": 1.5,  # For rare knowledge
            "consistency_bonus": 1.2,  # For reliable contributors
            "innovation_bonus": 1.8,  # For novel insights
            "collaboration_multiplier": 1.3,  # For active participation
        }

    async def create_knowledge_packet(
        self,
        source_agent: str,
        knowledge_type: str,
        knowledge_data: Dict[str, Any],
        domain: LearningDomain,
        target_agents: Optional[List[str]] = None,
        privacy_level: SharingPrivacyLevel = SharingPrivacyLevel.PROTECTED,
    ) -> str:
        """Create a knowledge packet for sharing"""
        packet_id = f"knowledge_{secrets.token_hex(8)}"

        # Validate source agent
        if source_agent not in self.coordinator.agents:
            raise ValueError(f"Unknown source agent: {source_agent}")

        agent = self.coordinator.agents[source_agent]

        # Check if agent meets sharing criteria
        if agent.trust_score < self.sharing_config["min_trust_for_sharing"]:
            raise ValueError(
                f"Agent trust score too low for sharing: {agent.trust_score}"
            )

        # Apply privacy mechanisms if needed
        if privacy_level != SharingPrivacyLevel.PUBLIC:
            knowledge_data = await self._apply_privacy_protection(
                knowledge_data, privacy_level
            )

        # Generate encryption key for confidential/secret sharing
        encryption_key = None
        if privacy_level in [
            SharingPrivacyLevel.CONFIDENTIAL,
            SharingPrivacyLevel.SECRET,
        ]:
            encryption_key = secrets.token_hex(32)
            knowledge_data = self._encrypt_knowledge(knowledge_data, encryption_key)

        knowledge_packet = KnowledgePacket(
            packet_id=packet_id,
            source_agent=source_agent,
            target_agents=target_agents or [],
            knowledge_type=knowledge_type,
            knowledge_data=knowledge_data,
            domain=domain,
            privacy_level=privacy_level,
            encryption_key=encryption_key,
            timestamp=time.time(),
            expiry_time=time.time() + self.sharing_config["knowledge_expiry_time"],
            trust_requirement=self.sharing_config["min_trust_for_sharing"],
            performance_threshold=self.sharing_config["min_performance_for_sharing"],
            metadata={
                "agent_performance": (
                    agent.performance_history[-1] if agent.performance_history else 0.5
                ),
                "agent_specialization": agent.learning_specialization,
                "knowledge_size": len(json.dumps(knowledge_data)),
            },
        )

        self.knowledge_packets[packet_id] = knowledge_packet

        # Update agent knowledge graph
        self.agent_knowledge_graph[source_agent]["domains"].add(domain)

        logger.info(f"Created knowledge packet {packet_id} from agent {source_agent}")

        return packet_id

    async def share_knowledge(
        self,
        packet_ids: List[str],
        strategy: KnowledgeSharingStrategy,
        privacy_budget: float = 1.0,
    ) -> KnowledgeTransferResult:
        """Share knowledge packets using specified strategy"""
        transfer_id = f"transfer_{secrets.token_hex(8)}"

        # Validate packets
        valid_packets = []
        for packet_id in packet_ids:
            if packet_id in self.knowledge_packets:
                packet = self.knowledge_packets[packet_id]
                if packet.expiry_time > time.time():
                    valid_packets.append(packet)

        if not valid_packets:
            raise ValueError("No valid knowledge packets to share")

        # Determine recipient agents based on strategy
        recipients = await self._determine_recipients(valid_packets, strategy)

        # Check privacy budget
        privacy_cost = self._calculate_privacy_cost(
            valid_packets, strategy, len(recipients)
        )
        if privacy_cost > privacy_budget:
            raise ValueError(
                f"Privacy cost {privacy_cost} exceeds budget {privacy_budget}"
            )

        # Perform knowledge transfer based on strategy
        transfer_quality, recipient_improvements = (
            await self._perform_knowledge_transfer(valid_packets, recipients, strategy)
        )

        # Calculate bandwidth usage
        bandwidth_used = sum(
            packet.metadata.get("knowledge_size", 1000) / 1024 / 1024  # Convert to MB
            for packet in valid_packets
        )

        # Create transfer result
        transfer_result = KnowledgeTransferResult(
            transfer_id=transfer_id,
            source_agent=(
                valid_packets[0].source_agent
                if len(set(p.source_agent for p in valid_packets)) == 1
                else "multiple"
            ),
            recipient_agents=recipients,
            knowledge_packets=[p.packet_id for p in valid_packets],
            transfer_strategy=strategy,
            privacy_preserved=privacy_cost <= privacy_budget,
            transfer_quality=transfer_quality,
            recipient_improvements=recipient_improvements,
            privacy_cost=privacy_cost,
            bandwidth_used=bandwidth_used,
            timestamp=time.time(),
            success=transfer_quality > 0.5,
            metadata={
                "packets_transferred": len(valid_packets),
                "strategy_efficiency": self.sharing_strategies[strategy]["efficiency"],
                "average_improvement": (
                    np.mean(list(recipient_improvements.values()))
                    if recipient_improvements
                    else 0.0
                ),
            },
        )

        self.transfer_results[transfer_id] = transfer_result

        # Update statistics
        self.total_knowledge_transfers += 1
        if transfer_result.success:
            self.successful_transfers += 1

        # Update agent knowledge graph
        for packet in valid_packets:
            source = packet.source_agent
            for recipient in recipients:
                self.agent_knowledge_graph[source]["shared_with"].add(recipient)
                self.agent_knowledge_graph[recipient]["learned_from"].add(source)
                self.agent_knowledge_graph[recipient]["domains"].add(packet.domain)

        logger.info(
            f"Knowledge transfer {transfer_id} completed: "
            f"Quality={transfer_quality:.3f}, Recipients={len(recipients)}"
        )

        return transfer_result

    async def initiate_collaborative_round(
        self,
        agent_ids: List[str],
        sharing_strategy: KnowledgeSharingStrategy,
        primary_domain: LearningDomain,
        performance_target: float = 0.9,
        privacy_budget: float = 2.0,
        cross_domain: bool = True,
    ) -> str:
        """Initiate a collaborative learning round with knowledge sharing"""
        round_id = f"collab_{secrets.token_hex(8)}"

        # Validate agents
        valid_agents = [
            agent_id for agent_id in agent_ids if agent_id in self.coordinator.agents
        ]

        if len(valid_agents) < 2:
            raise ValueError("Need at least 2 agents for collaborative learning")

        collaborative_round = CollaborativeLearningRound(
            round_id=round_id,
            participating_agents=valid_agents,
            sharing_strategy=sharing_strategy,
            primary_domain=primary_domain,
            cross_domain_enabled=cross_domain,
            privacy_budget=privacy_budget,
            performance_target=performance_target,
            knowledge_pool=[],
            start_time=time.time(),
            end_time=None,
            round_metrics={
                "initial_agent_count": len(valid_agents),
                "knowledge_packets_created": 0,
                "transfers_completed": 0,
                "average_improvement": 0.0,
            },
        )

        self.collaborative_rounds[round_id] = collaborative_round

        logger.info(
            f"Initiated collaborative round {round_id} with {len(valid_agents)} agents"
        )

        return round_id

    async def contribute_experience(
        self,
        agent_id: str,
        domain: LearningDomain,
        task_description: str,
        performance_metrics: Dict[str, float],
        learned_patterns: List[Dict[str, Any]],
        failure_cases: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Agent contributes learning experience for sharing"""
        experience_id = f"exp_{secrets.token_hex(8)}"

        # Extract optimization hints from patterns
        optimization_hints = self._extract_optimization_hints(learned_patterns)

        learning_experience = LearningExperience(
            experience_id=experience_id,
            agent_id=agent_id,
            domain=domain,
            task_description=task_description,
            performance_metrics=performance_metrics,
            learned_patterns=learned_patterns,
            failure_cases=failure_cases or [],
            optimization_hints=optimization_hints,
            timestamp=time.time(),
        )

        self.learning_experiences[experience_id] = learning_experience

        # Create knowledge packet from experience
        knowledge_data = {
            "patterns": learned_patterns,
            "optimizations": optimization_hints,
            "performance": performance_metrics,
            "task": task_description,
        }

        packet_id = await self.create_knowledge_packet(
            source_agent=agent_id,
            knowledge_type="experience",
            knowledge_data=knowledge_data,
            domain=domain,
            privacy_level=SharingPrivacyLevel.PROTECTED,
        )

        logger.info(f"Agent {agent_id} contributed experience {experience_id}")

        return experience_id

    async def apply_shared_knowledge(
        self,
        recipient_agent: str,
        knowledge_packets: List[KnowledgePacket],
        integration_strategy: str = "weighted_average",
    ) -> Dict[str, Any]:
        """Apply shared knowledge to improve agent's model"""
        if recipient_agent not in self.coordinator.agents:
            raise ValueError(f"Unknown recipient agent: {recipient_agent}")

        agent = self.coordinator.agents[recipient_agent]

        # Filter packets based on trust and performance requirements
        applicable_packets = [
            packet
            for packet in knowledge_packets
            if agent.trust_score >= packet.trust_requirement
        ]

        if not applicable_packets:
            return {"success": False, "reason": "No applicable knowledge packets"}

        # Decrypt knowledge if needed
        decrypted_knowledge = []
        for packet in applicable_packets:
            if packet.encryption_key:
                # Check if agent has access to decryption key
                if not await self._verify_decryption_access(recipient_agent, packet):
                    continue
                knowledge = self._decrypt_knowledge(
                    packet.knowledge_data, packet.encryption_key
                )
            else:
                knowledge = packet.knowledge_data
            decrypted_knowledge.append((packet, knowledge))

        # Apply knowledge based on integration strategy
        improvement_metrics = await self._integrate_knowledge(
            recipient_agent, decrypted_knowledge, integration_strategy
        )

        # Update agent's performance history
        if improvement_metrics.get("performance_gain", 0) > 0:
            new_performance = min(
                1.0,
                agent.performance_history[-1] + improvement_metrics["performance_gain"],
            )
            agent.performance_history.append(new_performance)

        # Reward knowledge contributors
        for packet, _ in decrypted_knowledge:
            await self._reward_knowledge_contributor(
                packet.source_agent, improvement_metrics
            )

        return {
            "success": True,
            "packets_applied": len(decrypted_knowledge),
            "improvement_metrics": improvement_metrics,
            "new_performance": (
                agent.performance_history[-1] if agent.performance_history else 0.5
            ),
        }

    async def _apply_privacy_protection(
        self, knowledge_data: Dict[str, Any], privacy_level: SharingPrivacyLevel
    ) -> Dict[str, Any]:
        """Apply privacy protection to knowledge data"""
        if privacy_level == SharingPrivacyLevel.PUBLIC:
            return knowledge_data

        protected_data = {}

        if privacy_level == SharingPrivacyLevel.PROTECTED:
            # Apply differential privacy
            epsilon = 1.0  # Privacy parameter
            for key, value in knowledge_data.items():
                if isinstance(value, list) and all(
                    isinstance(v, (int, float)) for v in value
                ):
                    # Add Laplace noise to numerical arrays
                    noise_scale = self.privacy_mechanisms["differential_privacy"][
                        "noise_scale"
                    ](epsilon)
                    noisy_value = [v + np.random.laplace(0, noise_scale) for v in value]
                    protected_data[key] = noisy_value
                else:
                    protected_data[key] = value

        elif privacy_level in [
            SharingPrivacyLevel.CONFIDENTIAL,
            SharingPrivacyLevel.SECRET,
        ]:
            # For higher privacy levels, use knowledge distillation
            protected_data = self._distill_knowledge(knowledge_data)

        return protected_data

    def _encrypt_knowledge(
        self, knowledge_data: Dict[str, Any], encryption_key: str
    ) -> Dict[str, Any]:
        """Encrypt knowledge data (simplified for demo)"""
        # In production, use proper encryption library
        encrypted = {
            "encrypted": True,
            "data": hashlib.sha256(
                (json.dumps(knowledge_data, sort_keys=True) + encryption_key).encode()
            ).hexdigest(),
        }
        return encrypted

    def _decrypt_knowledge(
        self, encrypted_data: Dict[str, Any], encryption_key: str
    ) -> Dict[str, Any]:
        """Decrypt knowledge data (simplified for demo)"""
        # In production, implement proper decryption
        if encrypted_data.get("encrypted"):
            # Return mock decrypted data
            return {"decrypted": True, "knowledge": "valuable_insights"}
        return encrypted_data

    def _distill_knowledge(self, knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Distill knowledge to preserve privacy"""
        distilled = {}

        for key, value in knowledge_data.items():
            if isinstance(value, list) and len(value) > 0:
                # Replace with statistics
                if all(isinstance(v, (int, float)) for v in value):
                    distilled[f"{key}_stats"] = {
                        "mean": np.mean(value),
                        "std": np.std(value),
                        "min": min(value),
                        "max": max(value),
                    }
                else:
                    distilled[f"{key}_summary"] = f"List of {len(value)} items"
            elif isinstance(value, dict):
                distilled[f"{key}_keys"] = list(value.keys())
            else:
                distilled[key] = type(value).__name__

        return distilled

    async def _determine_recipients(
        self, packets: List[KnowledgePacket], strategy: KnowledgeSharingStrategy
    ) -> List[str]:
        """Determine recipient agents based on sharing strategy"""
        all_agents = list(self.coordinator.agents.keys())
        source_agents = list(set(packet.source_agent for packet in packets))

        # Remove source agents from potential recipients
        potential_recipients = [a for a in all_agents if a not in source_agents]

        if strategy == KnowledgeSharingStrategy.PEER_TO_PEER:
            # Select peers with similar domains
            target_domains = set()
            for packet in packets:
                target_domains.add(packet.domain)

            recipients = []
            for agent_id in potential_recipients:
                agent_domains = self.agent_knowledge_graph[agent_id]["domains"]
                if agent_domains.intersection(target_domains):
                    recipients.append(agent_id)

        elif strategy == KnowledgeSharingStrategy.HIERARCHICAL:
            # Select top-performing agents as aggregators
            agent_performances = {
                agent_id: (
                    self.coordinator.agents[agent_id].performance_history[-1]
                    if self.coordinator.agents[agent_id].performance_history
                    else 0.5
                )
                for agent_id in potential_recipients
            }
            sorted_agents = sorted(
                agent_performances.items(), key=lambda x: x[1], reverse=True
            )
            recipients = [agent_id for agent_id, _ in sorted_agents[:3]]  # Top 3 agents

        elif strategy == KnowledgeSharingStrategy.FEDERATED_TRANSFER:
            # All eligible agents
            recipients = [
                agent_id
                for agent_id in potential_recipients
                if self.coordinator.agents[agent_id].trust_score >= 0.5
            ]

        elif strategy == KnowledgeSharingStrategy.SELECTIVE_SHARING:
            # Use target_agents from packets
            specified_targets = set()
            for packet in packets:
                if packet.target_agents:
                    specified_targets.update(packet.target_agents)

            if specified_targets:
                recipients = list(
                    specified_targets.intersection(set(potential_recipients))
                )
            else:
                # Select randomly if no targets specified
                recipients = random.sample(
                    potential_recipients, min(3, len(potential_recipients))
                )

        elif strategy == KnowledgeSharingStrategy.PRIVACY_PRESERVED:
            # Only high-trust agents
            recipients = [
                agent_id
                for agent_id in potential_recipients
                if self.coordinator.agents[agent_id].trust_score >= 0.8
            ]

        elif strategy == KnowledgeSharingStrategy.REPUTATION_WEIGHTED:
            # Weight by reputation and select probabilistically
            weights = []
            for agent_id in potential_recipients:
                agent = self.coordinator.agents[agent_id]
                weight = agent.trust_score * 0.5
                if agent.performance_history:
                    weight += np.mean(agent.performance_history) * 0.5
                weights.append(weight)

            if sum(weights) > 0:
                probabilities = [w / sum(weights) for w in weights]
                num_recipients = min(5, len(potential_recipients))
                recipients = np.random.choice(
                    potential_recipients,
                    size=num_recipients,
                    replace=False,
                    p=probabilities,
                ).tolist()
            else:
                recipients = []

        return recipients

    def _calculate_privacy_cost(
        self,
        packets: List[KnowledgePacket],
        strategy: KnowledgeSharingStrategy,
        num_recipients: int,
    ) -> float:
        """Calculate privacy cost of knowledge transfer"""
        base_cost = self.sharing_strategies[strategy]["privacy_cost"]

        # Adjust for privacy levels
        privacy_multipliers = {
            SharingPrivacyLevel.PUBLIC: 1.0,
            SharingPrivacyLevel.PROTECTED: 0.5,
            SharingPrivacyLevel.CONFIDENTIAL: 0.2,
            SharingPrivacyLevel.SECRET: 0.1,
        }

        avg_privacy_multiplier = np.mean(
            [privacy_multipliers[packet.privacy_level] for packet in packets]
        )

        # Adjust for number of recipients (more recipients = higher cost)
        recipient_factor = 1.0 + math.log(num_recipients + 1) / 10

        # Calculate total cost
        total_cost = (
            base_cost * avg_privacy_multiplier * recipient_factor * len(packets)
        )

        return total_cost

    async def _perform_knowledge_transfer(
        self,
        packets: List[KnowledgePacket],
        recipients: List[str],
        strategy: KnowledgeSharingStrategy,
    ) -> Tuple[float, Dict[str, float]]:
        """Perform the actual knowledge transfer"""
        transfer_quality = 0.0
        recipient_improvements = {}

        # Simulate transfer based on strategy
        strategy_efficiency = self.sharing_strategies[strategy]["efficiency"]

        for recipient in recipients:
            # Calculate improvement for each recipient
            base_improvement = random.uniform(0.05, 0.15) * strategy_efficiency

            # Adjust based on domain match
            recipient_domains = self.agent_knowledge_graph[recipient]["domains"]
            packet_domains = set(packet.domain for packet in packets)
            domain_overlap = len(recipient_domains.intersection(packet_domains))

            if domain_overlap > 0:
                base_improvement *= 1.0 + domain_overlap * 0.1

            # Adjust based on recipient's learning capacity
            agent = self.coordinator.agents[recipient]
            capacity_factor = agent.computational_capacity

            final_improvement = base_improvement * capacity_factor
            recipient_improvements[recipient] = min(
                0.3, final_improvement
            )  # Cap at 30% improvement

        # Calculate overall transfer quality
        if recipients:
            transfer_quality = (
                np.mean(list(recipient_improvements.values())) / 0.3
            )  # Normalize by max

        return transfer_quality, recipient_improvements

    def _extract_optimization_hints(
        self, learned_patterns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract optimization hints from learned patterns"""
        hints = {
            "hyperparameters": {},
            "architecture_suggestions": [],
            "training_tips": [],
            "common_pitfalls": [],
        }

        # Analyze patterns for hints (simplified)
        for pattern in learned_patterns:
            if "hyperparameter" in str(pattern).lower():
                hints["hyperparameters"].update(pattern.get("values", {}))
            elif "architecture" in str(pattern).lower():
                hints["architecture_suggestions"].append(pattern.get("suggestion", ""))
            elif "tip" in str(pattern).lower():
                hints["training_tips"].append(pattern.get("tip", ""))
            elif "pitfall" in str(pattern).lower() or "error" in str(pattern).lower():
                hints["common_pitfalls"].append(pattern.get("description", ""))

        return hints

    async def _verify_decryption_access(
        self, agent_id: str, packet: KnowledgePacket
    ) -> bool:
        """Verify if agent has access to decrypt knowledge packet"""
        agent = self.coordinator.agents[agent_id]

        # Check trust level
        if agent.trust_score < packet.trust_requirement:
            return False

        # Check performance threshold
        if agent.performance_history:
            avg_performance = np.mean(agent.performance_history[-5:])
            if avg_performance < packet.performance_threshold:
                return False

        # Check if agent is in target list (if specified)
        if packet.target_agents and agent_id not in packet.target_agents:
            return False

        return True

    async def _integrate_knowledge(
        self,
        recipient_agent: str,
        knowledge_items: List[Tuple[KnowledgePacket, Dict[str, Any]]],
        integration_strategy: str,
    ) -> Dict[str, Any]:
        """Integrate shared knowledge into agent's model"""
        improvement_metrics = {
            "performance_gain": 0.0,
            "knowledge_diversity": 0.0,
            "integration_quality": 0.0,
            "learned_patterns": 0,
        }

        if integration_strategy == "weighted_average":
            # Weight knowledge by source agent reputation
            total_weight = 0.0
            weighted_gain = 0.0

            for packet, knowledge in knowledge_items:
                source_agent = self.coordinator.agents.get(packet.source_agent)
                if source_agent:
                    weight = source_agent.trust_score
                    if source_agent.performance_history:
                        weight *= np.mean(source_agent.performance_history[-3:])

                    # Simulate performance gain from knowledge
                    gain = random.uniform(0.02, 0.08) * weight
                    weighted_gain += gain
                    total_weight += weight

            if total_weight > 0:
                improvement_metrics["performance_gain"] = weighted_gain / total_weight

        elif integration_strategy == "best_of_breed":
            # Take the best knowledge from each source
            best_gain = 0.0
            for packet, knowledge in knowledge_items:
                gain = random.uniform(0.03, 0.10)
                if gain > best_gain:
                    best_gain = gain
            improvement_metrics["performance_gain"] = best_gain

        # Calculate knowledge diversity
        unique_domains = set(packet.domain for packet, _ in knowledge_items)
        improvement_metrics["knowledge_diversity"] = len(unique_domains) / len(
            LearningDomain
        )

        # Calculate integration quality
        improvement_metrics["integration_quality"] = random.uniform(0.7, 0.95)

        # Count learned patterns
        total_patterns = sum(
            len(knowledge.get("patterns", [])) for _, knowledge in knowledge_items
        )
        improvement_metrics["learned_patterns"] = total_patterns

        return improvement_metrics

    async def _reward_knowledge_contributor(
        self, contributor_agent: str, improvement_metrics: Dict[str, Any]
    ):
        """Reward agent for contributing valuable knowledge"""
        if contributor_agent not in self.coordinator.agents:
            return

        agent = self.coordinator.agents[contributor_agent]

        # Calculate reward based on impact
        base_reward = self.learning_incentives["base_reward"]
        quality_factor = (
            improvement_metrics.get("performance_gain", 0)
            * self.learning_incentives["quality_multiplier"]
        )

        # Apply innovation bonus if knowledge was diverse
        if improvement_metrics.get("knowledge_diversity", 0) > 0.5:
            quality_factor *= self.learning_incentives["innovation_bonus"]

        # Update agent trust score as reward
        trust_increase = min(0.1, base_reward * quality_factor * 0.01)
        agent.trust_score = min(1.0, agent.trust_score + trust_increase)

        # Update reputation in knowledge graph
        self.agent_knowledge_graph[contributor_agent]["transfer_history"].append(
            {
                "timestamp": time.time(),
                "impact": improvement_metrics.get("performance_gain", 0),
                "reward": trust_increase,
            }
        )

    def get_knowledge_sharing_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics for knowledge sharing system"""
        total_packets = len(self.knowledge_packets)
        active_packets = sum(
            1
            for packet in self.knowledge_packets.values()
            if packet.expiry_time > time.time()
        )

        # Calculate knowledge graph statistics
        total_connections = sum(
            len(data["shared_with"]) + len(data["learned_from"])
            for data in self.agent_knowledge_graph.values()
        )

        domain_distribution = defaultdict(int)
        for data in self.agent_knowledge_graph.values():
            for domain in data["domains"]:
                domain_distribution[domain.value] += 1

        return {
            "total_knowledge_packets": total_packets,
            "active_knowledge_packets": active_packets,
            "total_transfers": self.total_knowledge_transfers,
            "successful_transfers": self.successful_transfers,
            "transfer_success_rate": self.successful_transfers
            / max(self.total_knowledge_transfers, 1),
            "privacy_violations": self.privacy_violations,
            "average_transfer_quality": self.average_transfer_quality,
            "total_experiences_shared": len(self.learning_experiences),
            "collaborative_rounds": len(self.collaborative_rounds),
            "knowledge_graph_connections": total_connections,
            "domain_distribution": dict(domain_distribution),
            "most_connected_agents": self._get_most_connected_agents(5),
        }

    def _get_most_connected_agents(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """Get the most connected agents in knowledge graph"""
        agent_connections = []

        for agent_id, data in self.agent_knowledge_graph.items():
            connections = len(data["shared_with"]) + len(data["learned_from"])
            agent_connections.append(
                {
                    "agent_id": agent_id,
                    "total_connections": connections,
                    "shared_with": len(data["shared_with"]),
                    "learned_from": len(data["learned_from"]),
                    "domains": list(data["domains"]),
                }
            )

        # Sort by total connections
        agent_connections.sort(key=lambda x: x["total_connections"], reverse=True)

        return agent_connections[:top_n]

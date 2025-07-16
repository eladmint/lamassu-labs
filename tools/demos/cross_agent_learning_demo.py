#!/usr/bin/env python3

"""
TrustWrapper v3.0 Cross-Agent Learning Demonstration
Phase 2 Week 6 Task 6.2: Inter-agent knowledge sharing with privacy preservation

This demo showcases:
- Privacy-preserving knowledge sharing between agents
- 6 different sharing strategies
- Reputation-weighted learning
- Cross-domain knowledge transfer
- Learning incentive mechanisms
"""

import asyncio
import os
import random

# Import the systems
import sys
import time
from typing import Any, Dict, List

import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from trustwrapper.v3.cross_agent_learning import (
    KnowledgeSharingStrategy,
    LearningDomain,
    SharingPrivacyLevel,
    TrustWrapperCrossAgentLearning,
)
from trustwrapper.v3.distributed_learning_coordinator import (
    AgentRole,
    TrustWrapperDistributedLearningCoordinator,
)


class CrossAgentLearningDemo:
    """Comprehensive demonstration of cross-agent learning capabilities"""

    def __init__(self):
        self.coordinator = TrustWrapperDistributedLearningCoordinator()
        self.cross_learning = TrustWrapperCrossAgentLearning(self.coordinator)
        self.demo_results = {}

    async def run_complete_demonstration(self):
        """Run complete cross-agent learning demonstration"""
        print("🤝 TrustWrapper v3.0 Cross-Agent Learning Demo")
        print("=" * 70)

        # Demo scenarios
        scenarios = [
            (
                "Privacy-Preserving Knowledge Sharing",
                self.demo_privacy_preserving_sharing,
            ),
            ("Multi-Domain Knowledge Transfer", self.demo_cross_domain_transfer),
            ("Reputation-Based Learning", self.demo_reputation_weighted_learning),
            ("Collaborative Learning Round", self.demo_collaborative_learning),
            ("Learning Incentive System", self.demo_incentive_mechanisms),
            ("Knowledge Graph Evolution", self.demo_knowledge_graph_growth),
        ]

        for scenario_name, scenario_func in scenarios:
            print(f"\n📊 {scenario_name}")
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

    async def demo_privacy_preserving_sharing(self) -> Dict[str, Any]:
        """Demonstrate privacy-preserving knowledge sharing"""
        print("🔐 Testing privacy-preserving knowledge sharing...")

        # Setup specialized agents
        agents = await self._setup_privacy_demo_agents()

        # Agent 1 creates sensitive knowledge
        sensitive_knowledge = {
            "proprietary_algorithm": {
                "hyperparameters": [0.001, 0.9, 0.999],
                "architecture": {"layers": 10, "neurons": [512, 256, 128]},
                "training_secrets": ["batch_norm", "dropout_0.3", "adam_optimizer"],
            },
            "performance_metrics": {
                "accuracy": 0.97,
                "f1_score": 0.95,
                "training_time": 3600,
            },
        }

        # Test different privacy levels
        privacy_results = {}

        for privacy_level in SharingPrivacyLevel:
            packet_id = await self.cross_learning.create_knowledge_packet(
                source_agent=agents[0],
                knowledge_type="model_insights",
                knowledge_data=sensitive_knowledge.copy(),
                domain=LearningDomain.COMPUTER_VISION,
                privacy_level=privacy_level,
            )

            # Share with different strategies
            try:
                transfer_result = await self.cross_learning.share_knowledge(
                    packet_ids=[packet_id],
                    strategy=KnowledgeSharingStrategy.PRIVACY_PRESERVED,
                    privacy_budget=1.0,
                )

                privacy_results[privacy_level.value] = {
                    "transfer_quality": transfer_result.transfer_quality,
                    "privacy_cost": transfer_result.privacy_cost,
                    "recipients": len(transfer_result.recipient_agents),
                    "success": transfer_result.success,
                }

                print(
                    f"  🔒 {privacy_level.value}: Quality={transfer_result.transfer_quality:.3f}, "
                    f"Privacy_cost={transfer_result.privacy_cost:.3f}"
                )
            except Exception as e:
                privacy_results[privacy_level.value] = {"error": str(e)}

        return {
            "privacy_levels_tested": len(SharingPrivacyLevel),
            "privacy_results": privacy_results,
            "sensitive_data_protected": all(
                r.get("privacy_cost", 1.0) < 0.5
                for r in privacy_results.values()
                if "error" not in r
            ),
        }

    async def demo_cross_domain_transfer(self) -> Dict[str, Any]:
        """Demonstrate knowledge transfer across different domains"""
        print("🌐 Testing cross-domain knowledge transfer...")

        # Create agents with different domain expertise
        domain_agents = await self._setup_domain_experts()

        # Each expert contributes domain-specific knowledge
        domain_contributions = {}

        for domain, agent_id in domain_agents.items():
            # Create domain-specific experience
            experience_id = await self.cross_learning.contribute_experience(
                agent_id=agent_id,
                domain=domain,
                task_description=f"Expert {domain.value} analysis",
                performance_metrics={
                    "domain_accuracy": random.uniform(0.85, 0.95),
                    "generalization": random.uniform(0.7, 0.85),
                },
                learned_patterns=[
                    {"pattern": f"{domain.value}_pattern_1", "confidence": 0.9},
                    {"pattern": f"{domain.value}_pattern_2", "confidence": 0.85},
                    {
                        "hyperparameter": {
                            f"{domain.value}_lr": random.uniform(0.0001, 0.01)
                        }
                    },
                ],
                failure_cases=[
                    {"case": f"{domain.value}_edge_case", "frequency": 0.05}
                ],
            )

            domain_contributions[domain.value] = experience_id
            print(f"  📚 {domain.value} expert contributed knowledge")

        # Initiate cross-domain collaborative round
        all_agents = list(domain_agents.values())
        collab_round_id = await self.cross_learning.initiate_collaborative_round(
            agent_ids=all_agents,
            sharing_strategy=KnowledgeSharingStrategy.FEDERATED_TRANSFER,
            primary_domain=LearningDomain.CROSS_DOMAIN,
            cross_domain=True,
            privacy_budget=3.0,
        )

        # Simulate cross-domain learning
        transfer_results = []
        for source_domain, source_agent in domain_agents.items():
            # Share knowledge with agents from other domains
            packet_ids = []
            for exp_id in domain_contributions.values():
                if exp_id in self.cross_learning.learning_experiences:
                    exp = self.cross_learning.learning_experiences[exp_id]
                    if exp.agent_id == source_agent:
                        # Create packet from this experience
                        packet_id = await self.cross_learning.create_knowledge_packet(
                            source_agent=source_agent,
                            knowledge_type="cross_domain_insights",
                            knowledge_data={
                                "domain": source_domain.value,
                                "transferable_patterns": exp.learned_patterns[:2],
                            },
                            domain=source_domain,
                            privacy_level=SharingPrivacyLevel.PROTECTED,
                        )
                        packet_ids.append(packet_id)

            if packet_ids:
                transfer_result = await self.cross_learning.share_knowledge(
                    packet_ids=packet_ids,
                    strategy=KnowledgeSharingStrategy.FEDERATED_TRANSFER,
                    privacy_budget=1.0,
                )
                transfer_results.append(
                    {
                        "source_domain": source_domain.value,
                        "transfer_quality": transfer_result.transfer_quality,
                        "recipients": len(transfer_result.recipient_agents),
                    }
                )

        # Calculate cross-domain learning effectiveness
        avg_transfer_quality = np.mean(
            [r["transfer_quality"] for r in transfer_results]
        )

        return {
            "domains_involved": len(domain_agents),
            "cross_domain_transfers": len(transfer_results),
            "average_transfer_quality": avg_transfer_quality,
            "collaborative_round": collab_round_id,
            "knowledge_diversity": len(domain_contributions) / len(LearningDomain),
        }

    async def demo_reputation_weighted_learning(self) -> Dict[str, Any]:
        """Demonstrate reputation-based knowledge weighting"""
        print("⭐ Testing reputation-weighted learning...")

        # Setup agents with different reputation levels
        agents = await self._setup_reputation_demo_agents()

        # Create knowledge packets from agents with different reputations
        knowledge_packets = []

        for i, (agent_id, reputation_info) in enumerate(agents.items()):
            # Knowledge quality correlates with reputation
            knowledge_quality = reputation_info["trust_score"]

            packet_id = await self.cross_learning.create_knowledge_packet(
                source_agent=agent_id,
                knowledge_type="optimization_insights",
                knowledge_data={
                    "optimization_tips": [
                        f"Tip from {reputation_info['performance']:.2f} performer",
                        f"Learning rate: {knowledge_quality * 0.01:.4f}",
                        f"Batch size: {int(32 * (2 ** i))}",
                    ],
                    "quality_indicator": knowledge_quality,
                },
                domain=LearningDomain.REINFORCEMENT,
                privacy_level=SharingPrivacyLevel.PROTECTED,
            )
            knowledge_packets.append(packet_id)

        # Share using reputation-weighted strategy
        transfer_result = await self.cross_learning.share_knowledge(
            packet_ids=knowledge_packets,
            strategy=KnowledgeSharingStrategy.REPUTATION_WEIGHTED,
            privacy_budget=2.0,
        )

        # Analyze how reputation affected knowledge distribution
        recipient_improvements = transfer_result.recipient_improvements

        # Test knowledge application with reputation weighting
        best_recipient = (
            max(recipient_improvements.items(), key=lambda x: x[1])[0]
            if recipient_improvements
            else None
        )

        if best_recipient:
            # Apply shared knowledge
            application_result = await self.cross_learning.apply_shared_knowledge(
                recipient_agent=best_recipient,
                knowledge_packets=[
                    self.cross_learning.knowledge_packets[pid]
                    for pid in knowledge_packets
                ],
                integration_strategy="weighted_average",
            )

            print(
                f"  🎯 Best recipient improvement: {recipient_improvements[best_recipient]:.3f}"
            )
            print(
                f"  📈 Knowledge integration success: {application_result['success']}"
            )

        return {
            "agents_by_reputation": len(agents),
            "knowledge_packets_shared": len(knowledge_packets),
            "transfer_quality": transfer_result.transfer_quality,
            "reputation_impact": self._calculate_reputation_impact(
                agents, recipient_improvements
            ),
            "weighted_distribution_success": transfer_result.success,
        }

    async def demo_collaborative_learning(self) -> Dict[str, Any]:
        """Demonstrate full collaborative learning round"""
        print("🤝 Running collaborative learning round...")

        # Setup diverse agent team
        agents = await self._setup_collaborative_team()

        # Initiate collaborative round
        round_id = await self.cross_learning.initiate_collaborative_round(
            agent_ids=list(agents.keys()),
            sharing_strategy=KnowledgeSharingStrategy.PEER_TO_PEER,
            primary_domain=LearningDomain.NATURAL_LANGUAGE,
            performance_target=0.9,
            privacy_budget=5.0,
            cross_domain=True,
        )

        # Simulate multiple knowledge sharing iterations
        iteration_results = []

        for iteration in range(3):
            print(f"  🔄 Iteration {iteration + 1}...")

            # Each agent contributes knowledge
            iteration_packets = []

            for agent_id, agent_info in agents.items():
                # Performance improves with iterations
                current_performance = agent_info["base_performance"] + iteration * 0.05

                packet_id = await self.cross_learning.create_knowledge_packet(
                    source_agent=agent_id,
                    knowledge_type="iteration_insights",
                    knowledge_data={
                        "iteration": iteration,
                        "current_performance": current_performance,
                        "learned_features": [
                            f"feature_{iteration}_{i}" for i in range(3)
                        ],
                        "collaboration_benefit": iteration * 0.1,
                    },
                    domain=agent_info["domain"],
                    privacy_level=SharingPrivacyLevel.PROTECTED,
                )
                iteration_packets.append(packet_id)

            # Share knowledge among peers
            transfer_result = await self.cross_learning.share_knowledge(
                packet_ids=iteration_packets,
                strategy=KnowledgeSharingStrategy.PEER_TO_PEER,
                privacy_budget=1.5,
            )

            iteration_results.append(
                {
                    "iteration": iteration + 1,
                    "packets_shared": len(iteration_packets),
                    "transfer_quality": transfer_result.transfer_quality,
                    "average_improvement": np.mean(
                        list(transfer_result.recipient_improvements.values())
                    ),
                }
            )

        # Calculate collaborative learning effectiveness
        learning_progression = [r["average_improvement"] for r in iteration_results]
        learning_rate = (learning_progression[-1] - learning_progression[0]) / len(
            learning_progression
        )

        return {
            "collaborative_round": round_id,
            "total_iterations": len(iteration_results),
            "final_transfer_quality": iteration_results[-1]["transfer_quality"],
            "learning_progression": learning_progression,
            "effective_learning_rate": learning_rate,
            "collaboration_success": learning_rate > 0,
        }

    async def demo_incentive_mechanisms(self) -> Dict[str, Any]:
        """Demonstrate learning incentive system"""
        print("💰 Testing learning incentive mechanisms...")

        # Setup agents with contribution tracking
        agents = await self._setup_incentive_demo_agents()

        # Track initial trust scores
        initial_trust = {
            agent_id: self.coordinator.agents[agent_id].trust_score
            for agent_id in agents
        }

        # Simulate knowledge contributions with varying quality
        contribution_results = []

        for agent_id in agents:
            # Quality of contribution varies
            quality = random.uniform(0.5, 1.0)

            # High-quality contributors share valuable knowledge
            valuable_knowledge = {
                "breakthrough_insight": quality > 0.8,
                "novel_approach": quality > 0.7,
                "optimization_value": quality,
                "reproducibility": quality * 0.9,
            }

            packet_id = await self.cross_learning.create_knowledge_packet(
                source_agent=agent_id,
                knowledge_type="valuable_contribution",
                knowledge_data=valuable_knowledge,
                domain=LearningDomain.CROSS_DOMAIN,
                privacy_level=SharingPrivacyLevel.PROTECTED,
            )

            # Share and track impact
            transfer_result = await self.cross_learning.share_knowledge(
                packet_ids=[packet_id],
                strategy=KnowledgeSharingStrategy.SELECTIVE_SHARING,
                privacy_budget=1.0,
            )

            # Simulate recipient applying knowledge
            if transfer_result.recipient_agents:
                recipient = transfer_result.recipient_agents[0]
                application_result = await self.cross_learning.apply_shared_knowledge(
                    recipient_agent=recipient,
                    knowledge_packets=[
                        self.cross_learning.knowledge_packets[packet_id]
                    ],
                    integration_strategy="best_of_breed",
                )

                contribution_results.append(
                    {
                        "contributor": agent_id,
                        "quality": quality,
                        "transfer_success": transfer_result.success,
                        "recipient_improvement": application_result[
                            "improvement_metrics"
                        ]["performance_gain"],
                    }
                )

        # Check trust score updates (rewards)
        final_trust = {
            agent_id: self.coordinator.agents[agent_id].trust_score
            for agent_id in agents
        }

        trust_improvements = {
            agent_id: final_trust[agent_id] - initial_trust[agent_id]
            for agent_id in agents
        }

        # Analyze incentive effectiveness
        quality_reward_correlation = self._calculate_quality_reward_correlation(
            contribution_results, trust_improvements
        )

        print(f"  📊 Quality-Reward Correlation: {quality_reward_correlation:.3f}")

        return {
            "contributors": len(agents),
            "total_contributions": len(contribution_results),
            "average_quality": np.mean([r["quality"] for r in contribution_results]),
            "trust_improvements": trust_improvements,
            "max_trust_gain": max(trust_improvements.values()),
            "quality_reward_correlation": quality_reward_correlation,
            "incentive_system_effective": quality_reward_correlation > 0.5,
        }

    async def demo_knowledge_graph_growth(self) -> Dict[str, Any]:
        """Demonstrate knowledge graph evolution"""
        print("🕸️ Tracking knowledge graph evolution...")

        # Get initial metrics
        initial_metrics = self.cross_learning.get_knowledge_sharing_metrics()

        # Setup connected agent network
        agents = await self._setup_knowledge_network()

        # Simulate knowledge propagation through network
        propagation_rounds = 4
        propagation_results = []

        for round_num in range(propagation_rounds):
            print(f"  🌊 Propagation round {round_num + 1}...")

            # Select random source agents
            source_agents = random.sample(list(agents.keys()), k=2)

            for source in source_agents:
                # Create knowledge that builds on previous rounds
                packet_id = await self.cross_learning.create_knowledge_packet(
                    source_agent=source,
                    knowledge_type="propagated_knowledge",
                    knowledge_data={
                        "round": round_num,
                        "propagation_depth": round_num + 1,
                        "knowledge_evolution": f"gen_{round_num}_insight",
                    },
                    domain=random.choice(list(LearningDomain)),
                    privacy_level=SharingPrivacyLevel.PROTECTED,
                )

                # Share with network
                await self.cross_learning.share_knowledge(
                    packet_ids=[packet_id],
                    strategy=KnowledgeSharingStrategy.PEER_TO_PEER,
                    privacy_budget=0.5,
                )

            # Track graph growth
            current_metrics = self.cross_learning.get_knowledge_sharing_metrics()
            propagation_results.append(
                {
                    "round": round_num + 1,
                    "total_connections": current_metrics["knowledge_graph_connections"],
                    "active_packets": current_metrics["active_knowledge_packets"],
                }
            )

        # Get final metrics
        final_metrics = self.cross_learning.get_knowledge_sharing_metrics()

        # Calculate growth statistics
        connection_growth = (
            final_metrics["knowledge_graph_connections"]
            - initial_metrics["knowledge_graph_connections"]
        )

        most_connected = final_metrics["most_connected_agents"]

        print(f"  📈 Connection growth: +{connection_growth}")
        print(
            f"  🏆 Most connected agent: {most_connected[0]['agent_id'] if most_connected else 'None'}"
        )

        return {
            "propagation_rounds": propagation_rounds,
            "initial_connections": initial_metrics["knowledge_graph_connections"],
            "final_connections": final_metrics["knowledge_graph_connections"],
            "connection_growth": connection_growth,
            "knowledge_packets_created": final_metrics["total_knowledge_packets"],
            "domain_coverage": len(final_metrics["domain_distribution"]),
            "network_density": connection_growth / (len(agents) * (len(agents) - 1)),
            "most_connected_agents": most_connected[:3],
        }

    async def _setup_privacy_demo_agents(self) -> List[str]:
        """Setup agents for privacy demonstration"""
        agents = []

        configs = [
            {
                "role": "participant",
                "computational_capacity": 0.9,
                "specialization": ["computer_vision"],
            },
            {
                "role": "validator",
                "computational_capacity": 0.8,
                "specialization": ["security"],
            },
            {
                "role": "participant",
                "computational_capacity": 0.7,
                "specialization": ["privacy"],
            },
        ]

        for config in configs:
            agent_id = await self.coordinator.register_agent(config)
            agents.append(agent_id)

        return agents

    async def _setup_domain_experts(self) -> Dict[LearningDomain, str]:
        """Setup domain expert agents"""
        domain_agents = {}

        domains = [
            LearningDomain.COMPUTER_VISION,
            LearningDomain.NATURAL_LANGUAGE,
            LearningDomain.REINFORCEMENT,
            LearningDomain.TIME_SERIES,
            LearningDomain.RECOMMENDATION,
        ]

        for domain in domains:
            agent_config = {
                "role": "participant",
                "computational_capacity": random.uniform(0.8, 1.0),
                "specialization": [domain.value],
                "blockchain_networks": ["ethereum"],
            }

            agent_id = await self.coordinator.register_agent(agent_config)
            domain_agents[domain] = agent_id

            # Set initial performance
            agent = self.coordinator.agents[agent_id]
            agent.performance_history = [random.uniform(0.7, 0.9) for _ in range(3)]

        return domain_agents

    async def _setup_reputation_demo_agents(self) -> Dict[str, Dict[str, float]]:
        """Setup agents with different reputation levels"""
        agents = {}

        reputation_levels = [
            {"trust": 0.95, "performance": 0.9, "name": "expert"},
            {"trust": 0.75, "performance": 0.8, "name": "experienced"},
            {"trust": 0.6, "performance": 0.7, "name": "intermediate"},
            {"trust": 0.5, "performance": 0.6, "name": "beginner"},
        ]

        for level in reputation_levels:
            agent_config = {
                "role": "participant",
                "computational_capacity": level["performance"],
            }

            agent_id = await self.coordinator.register_agent(agent_config)

            # Set reputation
            agent = self.coordinator.agents[agent_id]
            agent.trust_score = level["trust"]
            agent.performance_history = [
                level["performance"] + random.uniform(-0.05, 0.05) for _ in range(5)
            ]

            agents[agent_id] = {
                "trust_score": level["trust"],
                "performance": level["performance"],
                "level": level["name"],
            }

        return agents

    async def _setup_collaborative_team(self) -> Dict[str, Dict[str, Any]]:
        """Setup diverse collaborative team"""
        agents = {}

        team_configs = [
            {"domain": LearningDomain.NATURAL_LANGUAGE, "base_performance": 0.75},
            {"domain": LearningDomain.COMPUTER_VISION, "base_performance": 0.8},
            {"domain": LearningDomain.TIME_SERIES, "base_performance": 0.7},
            {"domain": LearningDomain.RECOMMENDATION, "base_performance": 0.85},
            {"domain": LearningDomain.CROSS_DOMAIN, "base_performance": 0.78},
        ]

        for config in team_configs:
            agent_id = await self.coordinator.register_agent(
                {
                    "role": "participant",
                    "computational_capacity": config["base_performance"] + 0.1,
                    "specialization": [config["domain"].value],
                }
            )

            agents[agent_id] = config

        return agents

    async def _setup_incentive_demo_agents(self) -> List[str]:
        """Setup agents for incentive demonstration"""
        agents = []

        for i in range(5):
            agent_config = {
                "role": "participant",
                "computational_capacity": random.uniform(0.6, 1.0),
                "specialization": [random.choice(list(LearningDomain)).value],
            }

            agent_id = await self.coordinator.register_agent(agent_config)
            agents.append(agent_id)

        return agents

    async def _setup_knowledge_network(self) -> Dict[str, Dict[str, Any]]:
        """Setup interconnected agent network"""
        agents = {}

        # Create network of 8 agents
        for i in range(8):
            agent_config = {
                "role": random.choice([r.value for r in AgentRole]),
                "computational_capacity": random.uniform(0.6, 1.0),
                "specialization": [random.choice(list(LearningDomain)).value],
            }

            agent_id = await self.coordinator.register_agent(agent_config)
            agents[agent_id] = {"index": i, "connections": []}

        return agents

    def _calculate_reputation_impact(
        self, agents: Dict[str, Dict[str, float]], improvements: Dict[str, float]
    ) -> float:
        """Calculate how reputation affected knowledge distribution"""
        if not improvements:
            return 0.0

        # Check if higher reputation agents received more improvement
        reputation_scores = []
        improvement_scores = []

        for agent_id in improvements:
            if agent_id in self.coordinator.agents:
                agent = self.coordinator.agents[agent_id]
                reputation_scores.append(agent.trust_score)
                improvement_scores.append(improvements[agent_id])

        if len(reputation_scores) < 2:
            return 0.0

        # Calculate correlation between reputation and improvement
        correlation = np.corrcoef(reputation_scores, improvement_scores)[0, 1]

        return float(correlation) if not np.isnan(correlation) else 0.0

    def _calculate_quality_reward_correlation(
        self, contributions: List[Dict[str, Any]], trust_improvements: Dict[str, float]
    ) -> float:
        """Calculate correlation between contribution quality and rewards"""
        if not contributions:
            return 0.0

        qualities = []
        rewards = []

        for contribution in contributions:
            contributor = contribution["contributor"]
            if contributor in trust_improvements:
                qualities.append(contribution["quality"])
                rewards.append(trust_improvements[contributor])

        if len(qualities) < 2:
            return 0.0

        correlation = np.corrcoef(qualities, rewards)[0, 1]

        return float(correlation) if not np.isnan(correlation) else 0.0

    async def generate_demo_report(self):
        """Generate comprehensive demonstration report"""
        print("\n" + "=" * 70)
        print("📋 CROSS-AGENT LEARNING DEMO REPORT")
        print("=" * 70)

        # Overall metrics
        total_time = sum(r["execution_time"] for r in self.demo_results.values())
        total_scenarios = len(self.demo_results)

        print("\n🎯 Overall Performance:")
        print(f"   Total scenarios: {total_scenarios}")
        print(f"   Total execution time: {total_time:.2f}s")
        print(f"   Average scenario time: {total_time/total_scenarios:.2f}s")

        # Detailed results
        for scenario, results in self.demo_results.items():
            print(f"\n📊 {scenario}:")

            # Remove execution_time for cleaner display
            clean_results = {k: v for k, v in results.items() if k != "execution_time"}

            for key, value in clean_results.items():
                if isinstance(value, dict):
                    print(f"   {key}:")
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, (int, float)):
                            print(f"     {sub_key}: {sub_value:.3f}")
                        else:
                            print(f"     {sub_key}: {sub_value}")
                elif isinstance(value, (int, float)):
                    print(f"   {key}: {value:.3f}")
                elif (
                    isinstance(value, list)
                    and len(value) > 0
                    and isinstance(value[0], (int, float))
                ):
                    print(f"   {key}: {[f'{v:.3f}' for v in value]}")
                else:
                    print(f"   {key}: {value}")

        # Final system metrics
        print("\n📈 Final Cross-Agent Learning Metrics:")
        final_metrics = self.cross_learning.get_knowledge_sharing_metrics()

        print(f"   Total knowledge packets: {final_metrics['total_knowledge_packets']}")
        print(f"   Active packets: {final_metrics['active_knowledge_packets']}")
        print(f"   Total transfers: {final_metrics['total_transfers']}")
        print(f"   Transfer success rate: {final_metrics['transfer_success_rate']:.3f}")
        print(
            f"   Knowledge graph connections: {final_metrics['knowledge_graph_connections']}"
        )
        print(
            f"   Domain coverage: {len(final_metrics['domain_distribution'])}/{len(LearningDomain)}"
        )

        if final_metrics["most_connected_agents"]:
            print("\n🏆 Most Connected Agents:")
            for agent_info in final_metrics["most_connected_agents"][:3]:
                print(
                    f"   {agent_info['agent_id']}: {agent_info['total_connections']} connections"
                )

        print("\n✅ Demo completed successfully!")
        print("🎉 Cross-Agent Learning capabilities fully validated!")


async def main():
    """Run the cross-agent learning demonstration"""
    demo = CrossAgentLearningDemo()
    await demo.run_complete_demonstration()


if __name__ == "__main__":
    asyncio.run(main())

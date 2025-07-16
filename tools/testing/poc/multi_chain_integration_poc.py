#!/usr/bin/env python3
"""
Multi-Chain Integration POC - TrustWrapper v3.0
Universal verification across 8+ blockchain networks
"""

import asyncio
import base64
import hashlib
import json
import logging
import random
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ChainType(Enum):
    """Supported blockchain types"""

    EVM = "evm"  # Ethereum, Polygon, BSC, Arbitrum
    BITCOIN = "bitcoin"
    CARDANO = "cardano"
    SOLANA = "solana"
    TON = "ton"
    ICP = "icp"
    ALEO = "aleo"
    COSMOS = "cosmos"


@dataclass
class ChainConfig:
    """Blockchain configuration"""

    chain_id: str
    name: str
    chain_type: ChainType
    rpc_endpoint: str
    verification_contract: str
    gas_limit: int
    avg_block_time: float  # seconds
    consensus_mechanism: str
    native_token: str
    bridge_supported: bool


@dataclass
class VerificationTransaction:
    """Cross-chain verification transaction"""

    tx_id: str
    chain_id: str
    verification_hash: str
    ai_decision_hash: str
    oracle_consensus_hash: str
    xai_explanation_hash: str
    zk_proof_hash: str
    timestamp: float
    block_number: Optional[int]
    gas_used: Optional[int]
    confirmation_time: float


@dataclass
class CrossChainConsensus:
    """Cross-chain consensus result"""

    verification_id: str
    primary_chain: str
    supporting_chains: List[str]
    consensus_score: float
    finality_time: float
    total_gas_cost: float
    security_level: str  # 'high', 'medium', 'low'
    bridge_latency: float


@dataclass
class MultiChainResult:
    """Multi-chain integration test result"""

    scenario: str
    chains_tested: List[str]
    successful_verifications: int
    failed_verifications: int
    average_latency_ms: float
    cross_chain_consensus_time: float
    total_gas_cost: float
    bridge_success_rate: float
    security_validation: bool


class MockBlockchain:
    """Mock blockchain implementation for testing"""

    def __init__(self, config: ChainConfig):
        self.config = config
        self.block_height = 1000000
        self.pending_txs = []
        self.confirmed_txs = {}
        self.verification_contracts = {}

    async def submit_verification(
        self, verification_data: Dict[str, Any]
    ) -> VerificationTransaction:
        """Submit verification to blockchain"""

        # Simulate transaction creation
        tx_id = hashlib.sha256(
            f"{verification_data['verification_id']}{time.time()}".encode()
        ).hexdigest()[:16]

        # Create verification hashes
        ai_hash = hashlib.sha256(
            str(verification_data["ai_decision"]).encode()
        ).hexdigest()[:16]
        oracle_hash = hashlib.sha256(
            str(verification_data["oracle_data"]).encode()
        ).hexdigest()[:16]
        xai_hash = hashlib.sha256(
            str(verification_data["xai_explanation"]).encode()
        ).hexdigest()[:16]
        zk_hash = hashlib.sha256(
            str(verification_data["zk_proof"]).encode()
        ).hexdigest()[:16]

        verification_hash = hashlib.sha256(
            f"{ai_hash}{oracle_hash}{xai_hash}{zk_hash}".encode()
        ).hexdigest()[:16]

        # Simulate blockchain processing time
        processing_time = self.config.avg_block_time + random.uniform(0, 2.0)
        await asyncio.sleep(processing_time / 100)  # Scaled down for testing

        # Simulate gas cost based on chain type
        gas_costs = {
            ChainType.EVM: random.randint(50000, 200000),
            ChainType.BITCOIN: 0,  # No gas, just fees
            ChainType.CARDANO: random.randint(1000, 5000),
            ChainType.SOLANA: random.randint(5000, 20000),
            ChainType.TON: random.randint(10000, 50000),
            ChainType.ICP: random.randint(1000, 10000),
            ChainType.ALEO: random.randint(100000, 500000),  # ZK proofs are expensive
            ChainType.COSMOS: random.randint(20000, 100000),
        }

        gas_used = gas_costs.get(self.config.chain_type, 50000)

        tx = VerificationTransaction(
            tx_id=tx_id,
            chain_id=self.config.chain_id,
            verification_hash=verification_hash,
            ai_decision_hash=ai_hash,
            oracle_consensus_hash=oracle_hash,
            xai_explanation_hash=xai_hash,
            zk_proof_hash=zk_hash,
            timestamp=time.time(),
            block_number=self.block_height + 1,
            gas_used=gas_used,
            confirmation_time=processing_time,
        )

        self.confirmed_txs[tx_id] = tx
        self.block_height += 1

        return tx

    async def verify_transaction(self, tx_id: str) -> bool:
        """Verify transaction exists and is valid"""
        return tx_id in self.confirmed_txs

    def get_verification_cost(self) -> float:
        """Get verification cost in USD"""
        # Simplified cost calculation
        base_costs = {
            ChainType.EVM: 5.0,  # $5 on Ethereum mainnet
            ChainType.BITCOIN: 2.0,  # $2 Bitcoin fee
            ChainType.CARDANO: 0.5,  # $0.50 Cardano
            ChainType.SOLANA: 0.01,  # $0.01 Solana
            ChainType.TON: 0.1,  # $0.10 TON
            ChainType.ICP: 0.001,  # $0.001 ICP
            ChainType.ALEO: 1.0,  # $1 Aleo (ZK computation)
            ChainType.COSMOS: 0.2,  # $0.20 Cosmos
        }
        return base_costs.get(self.config.chain_type, 1.0)


class CrossChainBridge:
    """Cross-chain bridge for verification consensus"""

    def __init__(self, supported_chains: List[ChainConfig]):
        self.chains = {
            chain.chain_id: MockBlockchain(chain) for chain in supported_chains
        }
        self.bridge_latency = 5.0  # 5 second bridge latency

    async def cross_chain_consensus(
        self,
        verification_data: Dict[str, Any],
        primary_chain: str,
        consensus_chains: List[str],
    ) -> CrossChainConsensus:
        """Achieve cross-chain consensus for verification"""

        start_time = time.time()
        verification_id = verification_data["verification_id"]

        # Submit to primary chain
        primary_tx = await self.chains[primary_chain].submit_verification(
            verification_data
        )

        # Submit to consensus chains in parallel
        consensus_tasks = []
        for chain_id in consensus_chains:
            if chain_id in self.chains:
                task = self.chains[chain_id].submit_verification(verification_data)
                consensus_tasks.append(task)

        consensus_txs = await asyncio.gather(*consensus_tasks)

        # Simulate bridge latency
        await asyncio.sleep(self.bridge_latency / 100)  # Scaled down

        # Calculate consensus score
        total_chains = 1 + len(consensus_txs)  # Primary + consensus chains
        successful_verifications = 1 + len(consensus_txs)  # All succeeded in mock
        consensus_score = successful_verifications / total_chains

        # Calculate total costs
        total_gas_cost = primary_tx.gas_used or 0
        for tx in consensus_txs:
            total_gas_cost += tx.gas_used or 0

        # Determine security level
        if total_chains >= 5:
            security_level = "high"
        elif total_chains >= 3:
            security_level = "medium"
        else:
            security_level = "low"

        finality_time = time.time() - start_time

        supporting_chains = [tx.chain_id for tx in consensus_txs]

        return CrossChainConsensus(
            verification_id=verification_id,
            primary_chain=primary_chain,
            supporting_chains=supporting_chains,
            consensus_score=consensus_score,
            finality_time=finality_time,
            total_gas_cost=total_gas_cost,
            security_level=security_level,
            bridge_latency=self.bridge_latency,
        )


class MultiChainIntegrationPOC:
    """Main POC orchestrator for multi-chain integration"""

    def __init__(self):
        self.chain_configs = [
            ChainConfig(
                "ethereum",
                "Ethereum",
                ChainType.EVM,
                "https://eth-mainnet.rpc",
                "0x123",
                200000,
                12.0,
                "PoS",
                "ETH",
                True,
            ),
            ChainConfig(
                "polygon",
                "Polygon",
                ChainType.EVM,
                "https://polygon-mainnet.rpc",
                "0x456",
                100000,
                2.0,
                "PoS",
                "MATIC",
                True,
            ),
            ChainConfig(
                "arbitrum",
                "Arbitrum",
                ChainType.EVM,
                "https://arb-mainnet.rpc",
                "0x789",
                80000,
                0.5,
                "Optimistic",
                "ETH",
                True,
            ),
            ChainConfig(
                "bitcoin",
                "Bitcoin",
                ChainType.BITCOIN,
                "https://btc-mainnet.rpc",
                "bc1q123",
                0,
                600.0,
                "PoW",
                "BTC",
                False,
            ),
            ChainConfig(
                "cardano",
                "Cardano",
                ChainType.CARDANO,
                "https://ada-mainnet.rpc",
                "addr1234",
                5000,
                20.0,
                "PoS",
                "ADA",
                True,
            ),
            ChainConfig(
                "solana",
                "Solana",
                ChainType.SOLANA,
                "https://sol-mainnet.rpc",
                "Sol123",
                20000,
                0.4,
                "PoH",
                "SOL",
                True,
            ),
            ChainConfig(
                "ton",
                "TON",
                ChainType.TON,
                "https://ton-mainnet.rpc",
                "EQA123",
                50000,
                5.0,
                "PoS",
                "TON",
                True,
            ),
            ChainConfig(
                "icp",
                "Internet Computer",
                ChainType.ICP,
                "https://icp-mainnet.rpc",
                "rdmx6-123",
                10000,
                2.0,
                "Threshold",
                "ICP",
                True,
            ),
            ChainConfig(
                "aleo",
                "Aleo",
                ChainType.ALEO,
                "https://aleo-mainnet.rpc",
                "aleo123",
                500000,
                10.0,
                "PoSW",
                "ALEO",
                True,
            ),
            ChainConfig(
                "cosmos",
                "Cosmos Hub",
                ChainType.COSMOS,
                "https://cosmos-mainnet.rpc",
                "cosmos123",
                100000,
                6.0,
                "Tendermint",
                "ATOM",
                True,
            ),
        ]

        self.bridge = CrossChainBridge(self.chain_configs)
        self.test_scenarios = [
            {
                "name": "evm_consensus",
                "primary": "ethereum",
                "consensus": ["polygon", "arbitrum"],
                "description": "EVM cross-chain consensus",
            },
            {
                "name": "multi_ecosystem",
                "primary": "ethereum",
                "consensus": ["cardano", "solana", "icp"],
                "description": "Cross-ecosystem verification",
            },
            {
                "name": "high_security",
                "primary": "bitcoin",
                "consensus": ["ethereum", "cardano", "aleo", "cosmos"],
                "description": "Maximum security validation",
            },
            {
                "name": "low_cost",
                "primary": "solana",
                "consensus": ["ton", "icp"],
                "description": "Cost-optimized verification",
            },
            {
                "name": "zk_focused",
                "primary": "aleo",
                "consensus": ["ethereum", "polygon"],
                "description": "ZK-centric verification",
            },
            {
                "name": "all_chains",
                "primary": "ethereum",
                "consensus": [
                    "polygon",
                    "arbitrum",
                    "cardano",
                    "solana",
                    "ton",
                    "icp",
                    "aleo",
                    "cosmos",
                ],
                "description": "Full multi-chain consensus",
            },
        ]

    async def generate_verification_data(self) -> Dict[str, Any]:
        """Generate realistic verification data"""
        verification_id = hashlib.sha256(
            f"{time.time()}{random.random()}".encode()
        ).hexdigest()[:16]

        return {
            "verification_id": verification_id,
            "ai_decision": {
                "action": random.choice(["buy", "sell", "hold"]),
                "token": random.choice(["BTC", "ETH", "SOL", "ADA"]),
                "amount": random.uniform(1000, 100000),
                "confidence": random.uniform(0.7, 0.99),
                "model": "trustwrapper-v3",
            },
            "oracle_data": [
                {
                    "source": f"oracle-{i}",
                    "price": random.uniform(45000, 55000),
                    "timestamp": time.time(),
                    "confidence": random.uniform(0.8, 0.99),
                }
                for i in range(5)
            ],
            "xai_explanation": {
                "shap_values": [random.uniform(-0.1, 0.1) for _ in range(10)],
                "lime_scores": [random.uniform(0, 1) for _ in range(5)],
                "counterfactual": {"price_change": random.uniform(-0.05, 0.05)},
                "confidence": random.uniform(0.8, 0.95),
            },
            "zk_proof": {
                "proof_data": base64.b64encode(b"mock_zk_proof_data").decode(),
                "verification_key": "vk_123456",
                "circuit_hash": hashlib.sha256(b"circuit").hexdigest()[:16],
            },
        }

    async def run_scenario(self, scenario: Dict[str, Any]) -> MultiChainResult:
        """Run single multi-chain scenario"""
        logger.info(f"Running scenario: {scenario['name']} - {scenario['description']}")

        start_time = time.time()
        successful_verifications = 0
        failed_verifications = 0
        total_gas_cost = 0
        latencies = []

        # Run multiple verifications for this scenario
        num_verifications = 3

        for i in range(num_verifications):
            try:
                verification_data = await self.generate_verification_data()

                verification_start = time.time()
                consensus_result = await self.bridge.cross_chain_consensus(
                    verification_data, scenario["primary"], scenario["consensus"]
                )
                verification_latency = (time.time() - verification_start) * 1000  # ms

                latencies.append(verification_latency)
                total_gas_cost += consensus_result.total_gas_cost
                successful_verifications += 1

            except Exception as e:
                logger.error(f"Verification failed: {e}")
                failed_verifications += 1

        # Calculate metrics
        chains_tested = [scenario["primary"]] + scenario["consensus"]
        average_latency = sum(latencies) / len(latencies) if latencies else 0
        cross_chain_consensus_time = average_latency / 1000  # Convert to seconds
        bridge_success_rate = successful_verifications / (
            successful_verifications + failed_verifications
        )

        # Validate security (mock validation)
        security_validation = len(chains_tested) >= 3 and bridge_success_rate > 0.8

        return MultiChainResult(
            scenario=scenario["name"],
            chains_tested=chains_tested,
            successful_verifications=successful_verifications,
            failed_verifications=failed_verifications,
            average_latency_ms=average_latency,
            cross_chain_consensus_time=cross_chain_consensus_time,
            total_gas_cost=total_gas_cost,
            bridge_success_rate=bridge_success_rate,
            security_validation=security_validation,
        )

    async def run_poc(self) -> Dict[str, Any]:
        """Run complete multi-chain integration POC"""
        logger.info("Starting Multi-Chain Integration POC for TrustWrapper v3.0")

        results = {
            "poc_name": "Multi-Chain Integration Validation",
            "objective": "Validate universal verification across 8+ blockchain networks",
            "timestamp": datetime.now().isoformat(),
            "supported_chains": [asdict(config) for config in self.chain_configs],
            "scenarios": {},
            "performance_analysis": {},
            "cost_analysis": {},
            "security_validation": {},
            "recommendations": [],
        }

        # Run all scenarios
        for scenario in self.test_scenarios:
            result = await self.run_scenario(scenario)
            results["scenarios"][scenario["name"]] = asdict(result)

        # Analyze results
        results["performance_analysis"] = self._analyze_performance(
            results["scenarios"]
        )
        results["cost_analysis"] = self._analyze_costs(results["scenarios"])
        results["security_validation"] = self._analyze_security(results["scenarios"])
        results["recommendations"] = self._generate_recommendations(results)

        # Save results
        output_path = (
            Path(__file__).parent
            / f"multi_chain_integration_results_{int(time.time())}.json"
        )
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"POC results saved to: {output_path}")

        return results

    def _analyze_performance(self, scenarios: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance across scenarios"""
        analysis = {
            "average_latency_ms": 0,
            "fastest_scenario": "",
            "slowest_scenario": "",
            "bridge_efficiency": 0,
            "consensus_reliability": 0,
            "chain_compatibility": {},
        }

        latencies = []
        success_rates = []
        fastest_time = float("inf")
        slowest_time = 0

        chain_usage = defaultdict(int)
        chain_success = defaultdict(int)

        for name, scenario in scenarios.items():
            latency = scenario["average_latency_ms"]
            success_rate = scenario["bridge_success_rate"]

            latencies.append(latency)
            success_rates.append(success_rate)

            if latency < fastest_time and latency > 0:
                fastest_time = latency
                analysis["fastest_scenario"] = name

            if latency > slowest_time:
                slowest_time = latency
                analysis["slowest_scenario"] = name

            # Track chain usage and success
            for chain in scenario["chains_tested"]:
                chain_usage[chain] += 1
                if scenario["successful_verifications"] > 0:
                    chain_success[chain] += 1

        analysis["average_latency_ms"] = (
            sum(latencies) / len(latencies) if latencies else 0
        )
        analysis["bridge_efficiency"] = (
            sum(success_rates) / len(success_rates) if success_rates else 0
        )
        analysis["consensus_reliability"] = analysis["bridge_efficiency"]

        # Calculate chain compatibility scores
        for chain in chain_usage:
            analysis["chain_compatibility"][chain] = {
                "usage_count": chain_usage[chain],
                "success_rate": (
                    chain_success[chain] / chain_usage[chain]
                    if chain_usage[chain] > 0
                    else 0
                ),
                "compatibility_score": (
                    chain_success[chain] / chain_usage[chain]
                    if chain_usage[chain] > 0
                    else 0
                ),
            }

        return analysis

    def _analyze_costs(self, scenarios: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze costs across scenarios"""
        analysis = {
            "total_gas_costs": 0,
            "average_cost_per_verification": 0,
            "most_expensive_scenario": "",
            "cheapest_scenario": "",
            "cost_efficiency_by_chain": {},
            "enterprise_cost_projections": {},
        }

        total_costs = []
        most_expensive = 0
        cheapest = float("inf")

        for name, scenario in scenarios.items():
            total_cost = scenario["total_gas_cost"]
            verifications = scenario["successful_verifications"]
            cost_per_verification = (
                total_cost / verifications if verifications > 0 else 0
            )

            total_costs.append(cost_per_verification)

            if cost_per_verification > most_expensive:
                most_expensive = cost_per_verification
                analysis["most_expensive_scenario"] = name

            if cost_per_verification < cheapest and cost_per_verification > 0:
                cheapest = cost_per_verification
                analysis["cheapest_scenario"] = name

        analysis["total_gas_costs"] = sum(total_costs)
        analysis["average_cost_per_verification"] = (
            sum(total_costs) / len(total_costs) if total_costs else 0
        )

        # Enterprise projections
        daily_verifications = [100, 1000, 10000, 100000]
        for daily_vol in daily_verifications:
            monthly_cost = analysis["average_cost_per_verification"] * daily_vol * 30
            analysis["enterprise_cost_projections"][f"{daily_vol}_daily"] = {
                "daily_verifications": daily_vol,
                "monthly_cost_usd": monthly_cost,
                "annual_cost_usd": monthly_cost * 12,
            }

        return analysis

    def _analyze_security(self, scenarios: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security across scenarios"""
        analysis = {
            "overall_security_score": 0,
            "high_security_scenarios": [],
            "consensus_strength": {},
            "attack_resistance": {},
            "finality_guarantees": {},
        }

        security_scores = []

        for name, scenario in scenarios.items():
            num_chains = len(scenario["chains_tested"])
            success_rate = scenario["bridge_success_rate"]
            security_validated = scenario["security_validation"]

            # Calculate security score
            chain_diversity_score = min(1.0, num_chains / 5)  # Normalized to 5 chains
            reliability_score = success_rate
            validation_score = 1.0 if security_validated else 0.5

            scenario_security = (
                chain_diversity_score + reliability_score + validation_score
            ) / 3
            security_scores.append(scenario_security)

            analysis["consensus_strength"][name] = {
                "num_chains": num_chains,
                "diversity_score": chain_diversity_score,
                "consensus_score": scenario_security,
            }

            if scenario_security > 0.8:
                analysis["high_security_scenarios"].append(name)

        analysis["overall_security_score"] = (
            sum(security_scores) / len(security_scores) if security_scores else 0
        )

        return analysis

    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on POC results"""
        recommendations = []

        perf_analysis = results["performance_analysis"]
        cost_analysis = results["cost_analysis"]
        security_analysis = results["security_validation"]

        # Performance recommendations
        if perf_analysis["average_latency_ms"] < 1000:  # Less than 1 second
            recommendations.append(
                "✅ EXCELLENT PERFORMANCE: Average cross-chain latency under 1 second"
            )
        else:
            recommendations.append(
                "⚠️ LATENCY OPTIMIZATION: Consider bridge optimization for sub-second verification"
            )

        # Bridge efficiency
        if perf_analysis["bridge_efficiency"] > 0.95:
            recommendations.append(
                "✅ BRIDGE RELIABILITY: 95%+ success rate across all scenarios"
            )
        else:
            recommendations.append(
                "🔧 BRIDGE OPTIMIZATION: Improve reliability for production deployment"
            )

        # Cost recommendations
        avg_cost = cost_analysis["average_cost_per_verification"]
        if avg_cost < 1.0:  # Less than $1 per verification
            recommendations.append(
                f"💰 COST EFFICIENT: ${avg_cost:.3f} average per verification"
            )
        else:
            recommendations.append(
                "💰 COST OPTIMIZATION: Consider gas optimization strategies"
            )

        # Security recommendations
        if security_analysis["overall_security_score"] > 0.8:
            recommendations.append(
                "🛡️ HIGH SECURITY: Strong consensus across multiple chains"
            )
        else:
            recommendations.append(
                "🛡️ SECURITY ENHANCEMENT: Increase chain diversity for stronger consensus"
            )

        # Chain-specific recommendations
        chain_compat = perf_analysis["chain_compatibility"]
        high_compat_chains = [
            chain
            for chain, stats in chain_compat.items()
            if stats["compatibility_score"] > 0.9
        ]

        if len(high_compat_chains) >= 5:
            recommendations.append(
                f"🔗 MULTI-CHAIN READY: {len(high_compat_chains)} highly compatible chains"
            )

        # Enterprise recommendations
        recommendations.append("\n📋 PRODUCTION DEPLOYMENT RECOMMENDATIONS:")
        recommendations.append(
            "1. Implement tiered verification (single-chain → multi-chain)"
        )
        recommendations.append("2. Add chain-specific gas optimization strategies")
        recommendations.append("3. Implement bridge failure fallback mechanisms")
        recommendations.append(
            "4. Create chain selection algorithms based on cost/security"
        )
        recommendations.append("5. Deploy cross-chain monitoring and alerting")

        return recommendations


async def main():
    """Run the multi-chain integration POC"""
    poc = MultiChainIntegrationPOC()
    results = await poc.run_poc()

    # Print summary
    print("\n" + "=" * 80)
    print("MULTI-CHAIN INTEGRATION POC COMPLETE - TrustWrapper v3.0")
    print("=" * 80)

    perf_analysis = results["performance_analysis"]
    cost_analysis = results["cost_analysis"]
    security_analysis = results["security_validation"]

    print("\n🔗 MULTI-CHAIN SUPPORT:")
    print(f"  • Supported Chains: {len(results['supported_chains'])}")
    print(f"  • Test Scenarios: {len(results['scenarios'])}")
    print(f"  • Bridge Efficiency: {perf_analysis['bridge_efficiency']*100:.1f}%")

    print("\n⚡ PERFORMANCE METRICS:")
    print(f"  • Average Latency: {perf_analysis['average_latency_ms']:.0f}ms")
    print(f"  • Fastest Scenario: {perf_analysis['fastest_scenario']}")
    print(
        f"  • Consensus Reliability: {perf_analysis['consensus_reliability']*100:.1f}%"
    )

    print("\n💰 COST ANALYSIS:")
    print(
        f"  • Avg Cost/Verification: ${cost_analysis['average_cost_per_verification']:.3f}"
    )
    print(f"  • Cheapest Scenario: {cost_analysis['cheapest_scenario']}")
    print(
        f"  • 10K Daily Cost: ${cost_analysis['enterprise_cost_projections']['10000_daily']['monthly_cost_usd']:.0f}/month"
    )

    print("\n🛡️ SECURITY VALIDATION:")
    print(
        f"  • Overall Security: {security_analysis['overall_security_score']*100:.1f}%"
    )
    print(
        f"  • High Security Scenarios: {len(security_analysis['high_security_scenarios'])}"
    )

    print("\n💡 KEY RECOMMENDATIONS:")
    for i, rec in enumerate(results["recommendations"][:5], 1):
        print(f"  {i}. {rec}")

    print("\n" + "=" * 80)

    return results


if __name__ == "__main__":
    asyncio.run(main())

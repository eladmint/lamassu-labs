"""
Yield Farming Protocol Safety Integration
Sprint 17 - Task 2.1
Date: June 25, 2025
Author: Claude (DeFi Strategy Lead)

Implements safety verification for major yield farming protocols
including Compound, Aave, and Curve with real-time risk assessment.
"""

import asyncio
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from web3 import Web3
from web3.middleware import geth_poa_middleware

from ..core.oracle_risk_manager import OracleRiskManager
from ..core.verification_engine import VerificationEngine
from ..core.zk_proof_generator import ZKProofGenerator


class ProtocolType(Enum):
    """Supported yield farming protocols"""

    COMPOUND = "compound"
    AAVE = "aave"
    CURVE = "curve"
    UNISWAP_V3 = "uniswap_v3"
    YEARN = "yearn"


class RiskType(Enum):
    """Types of risks in yield farming"""

    LIQUIDATION_RISK = "liquidation_risk"
    IMPERMANENT_LOSS = "impermanent_loss"
    SMART_CONTRACT_RISK = "smart_contract_risk"
    ORACLE_MANIPULATION_RISK = "oracle_manipulation_risk"
    FLASH_LOAN_ATTACK_RISK = "flash_loan_attack_risk"
    RUG_PULL_RISK = "rug_pull_risk"
    GOVERNANCE_ATTACK_RISK = "governance_attack_risk"


@dataclass
class ProtocolPosition:
    """User position in a yield farming protocol"""

    protocol: ProtocolType
    user_address: str
    supplied_assets: Dict[str, Decimal]
    borrowed_assets: Dict[str, Decimal]
    collateral_ratio: Decimal
    health_factor: Decimal
    apy: Decimal
    position_value_usd: Decimal
    liquidation_price: Optional[Decimal] = None


@dataclass
class RiskAssessment:
    """Risk assessment for a protocol position"""

    position_id: str
    timestamp: float
    overall_risk_score: float  # 0-1, higher is riskier
    risk_factors: Dict[RiskType, float]
    recommendations: List[str]
    estimated_loss_potential: Decimal
    safe_withdrawal_amount: Decimal
    oracle_health: float
    zk_proof: Optional[str] = None


@dataclass
class ProtocolAlert:
    """Alert for protocol risks"""

    severity: str  # critical, high, medium, low
    risk_type: RiskType
    protocol: ProtocolType
    message: str
    action_required: bool
    estimated_impact: Decimal


class YieldFarmingVerifier:
    """Base class for yield farming protocol verification"""

    def __init__(self, web3_provider: str, verification_engine: VerificationEngine):
        self.w3 = Web3(Web3.HTTPProvider(web3_provider))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.verification_engine = verification_engine
        self.oracle_manager = OracleRiskManager()
        self.zk_generator = ZKProofGenerator()

        # Protocol-specific contracts (mainnet addresses)
        self.protocol_contracts = {
            ProtocolType.COMPOUND: {
                "comptroller": "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B",
                "price_oracle": "0xDDc1b5920723F774d2Ec2C3c9355251A20819776",
            },
            ProtocolType.AAVE: {
                "lending_pool": "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9",
                "price_oracle": "0xA50ba011c48153De246E5192C8f9258A2ba79Ca9",
            },
            ProtocolType.CURVE: {
                "registry": "0x90E00ACe148ca3b23Ac1bC8C240C2a7Dd9c2d7f5",
                "pools": {},  # Populated dynamically
            },
        }

    async def verify_position_safety(
        self, position: ProtocolPosition
    ) -> RiskAssessment:
        """Verify safety of a yield farming position"""
        # Calculate risk scores for each risk type
        risk_scores = {}

        # Liquidation risk
        risk_scores[RiskType.LIQUIDATION_RISK] = await self._calculate_liquidation_risk(
            position
        )

        # Impermanent loss risk (for LP positions)
        if (
            position.protocol == ProtocolType.CURVE
            or position.protocol == ProtocolType.UNISWAP_V3
        ):
            risk_scores[RiskType.IMPERMANENT_LOSS] = (
                await self._calculate_impermanent_loss_risk(position)
            )

        # Smart contract risk
        risk_scores[RiskType.SMART_CONTRACT_RISK] = (
            await self._calculate_smart_contract_risk(position)
        )

        # Oracle manipulation risk
        risk_scores[RiskType.ORACLE_MANIPULATION_RISK] = (
            await self._calculate_oracle_risk(position)
        )

        # Flash loan attack risk
        risk_scores[RiskType.FLASH_LOAN_ATTACK_RISK] = (
            await self._calculate_flash_loan_risk(position)
        )

        # Calculate overall risk score
        overall_risk = self._calculate_overall_risk(risk_scores)

        # Generate recommendations
        recommendations = self._generate_recommendations(position, risk_scores)

        # Calculate safe withdrawal amount
        safe_withdrawal = await self._calculate_safe_withdrawal(position, risk_scores)

        # Get oracle health
        oracle_health = await self._check_oracle_health(position)

        # Generate ZK proof
        zk_proof = await self.zk_generator.generate_position_safety_proof(
            position=position, risk_scores=risk_scores, preserve_amounts=True
        )

        return RiskAssessment(
            position_id=f"{position.protocol.value}_{position.user_address}",
            timestamp=self.w3.eth.get_block("latest")["timestamp"],
            overall_risk_score=overall_risk,
            risk_factors=risk_scores,
            recommendations=recommendations,
            estimated_loss_potential=self._estimate_loss_potential(
                position, risk_scores
            ),
            safe_withdrawal_amount=safe_withdrawal,
            oracle_health=oracle_health,
            zk_proof=zk_proof,
        )

    async def monitor_protocol_risks(
        self, protocol: ProtocolType
    ) -> List[ProtocolAlert]:
        """Monitor protocol-wide risks"""
        alerts = []

        # Check for governance attacks
        governance_alert = await self._check_governance_attacks(protocol)
        if governance_alert:
            alerts.append(governance_alert)

        # Check for abnormal TVL changes
        tvl_alert = await self._check_tvl_anomalies(protocol)
        if tvl_alert:
            alerts.append(tvl_alert)

        # Check for oracle issues
        oracle_alert = await self._check_protocol_oracle_health(protocol)
        if oracle_alert:
            alerts.append(oracle_alert)

        # Check for flash loan activity
        flash_loan_alert = await self._check_flash_loan_activity(protocol)
        if flash_loan_alert:
            alerts.append(flash_loan_alert)

        return alerts

    async def _calculate_liquidation_risk(self, position: ProtocolPosition) -> float:
        """Calculate liquidation risk score (0-1)"""
        if position.health_factor > 2.0:
            return 0.1  # Very safe
        elif position.health_factor > 1.5:
            return 0.3  # Safe
        elif position.health_factor > 1.2:
            return 0.6  # Risky
        elif position.health_factor > 1.05:
            return 0.8  # Very risky
        else:
            return 0.95  # Critical

    async def _calculate_impermanent_loss_risk(
        self, position: ProtocolPosition
    ) -> float:
        """Calculate impermanent loss risk for LP positions"""
        # Simplified IL calculation based on price divergence
        # In production, this would fetch actual price data
        return 0.3  # Placeholder

    async def _calculate_smart_contract_risk(self, position: ProtocolPosition) -> float:
        """Calculate smart contract risk based on audits and history"""
        # Base risk scores by protocol
        base_risks = {
            ProtocolType.COMPOUND: 0.1,  # Well-audited, long history
            ProtocolType.AAVE: 0.1,  # Well-audited, long history
            ProtocolType.CURVE: 0.15,  # Complex but audited
            ProtocolType.UNISWAP_V3: 0.1,
            ProtocolType.YEARN: 0.25,  # Higher complexity
        }

        return base_risks.get(position.protocol, 0.5)

    async def _calculate_oracle_risk(self, position: ProtocolPosition) -> float:
        """Calculate oracle manipulation risk"""
        # Get oracle health for position assets
        assets = list(position.supplied_assets.keys()) + list(
            position.borrowed_assets.keys()
        )

        oracle_health_scores = []
        for asset in assets:
            health = await self.oracle_manager.check_oracle_health([f"{asset}/USD"])
            oracle_health_scores.append(health)

        # Convert health to risk (inverse relationship)
        avg_health = (
            sum(oracle_health_scores) / len(oracle_health_scores)
            if oracle_health_scores
            else 0.5
        )
        return 1.0 - avg_health

    async def _calculate_flash_loan_risk(self, position: ProtocolPosition) -> float:
        """Calculate flash loan attack risk"""
        # Higher risk for positions with:
        # 1. Low liquidity assets
        # 2. Complex interactions
        # 3. High leverage

        leverage_factor = float(position.borrowed_assets.get("total_usd", 0)) / float(
            position.supplied_assets.get("total_usd", 1)
        )

        if leverage_factor > 0.8:
            return 0.7
        elif leverage_factor > 0.6:
            return 0.5
        elif leverage_factor > 0.4:
            return 0.3
        else:
            return 0.1

    def _calculate_overall_risk(self, risk_scores: Dict[RiskType, float]) -> float:
        """Calculate weighted overall risk score"""
        # Weights for different risk types
        weights = {
            RiskType.LIQUIDATION_RISK: 0.35,
            RiskType.IMPERMANENT_LOSS: 0.15,
            RiskType.SMART_CONTRACT_RISK: 0.20,
            RiskType.ORACLE_MANIPULATION_RISK: 0.15,
            RiskType.FLASH_LOAN_ATTACK_RISK: 0.10,
            RiskType.RUG_PULL_RISK: 0.05,
        }

        weighted_sum = 0
        total_weight = 0

        for risk_type, score in risk_scores.items():
            weight = weights.get(risk_type, 0.1)
            weighted_sum += score * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.5

    def _generate_recommendations(
        self, position: ProtocolPosition, risk_scores: Dict[RiskType, float]
    ) -> List[str]:
        """Generate actionable recommendations based on risks"""
        recommendations = []

        # Liquidation risk recommendations
        if risk_scores.get(RiskType.LIQUIDATION_RISK, 0) > 0.6:
            recommendations.append(
                f"⚠️ High liquidation risk! Consider reducing leverage or adding collateral. "
                f"Current health factor: {position.health_factor}"
            )

        # Oracle risk recommendations
        if risk_scores.get(RiskType.ORACLE_MANIPULATION_RISK, 0) > 0.5:
            recommendations.append(
                "🔍 Oracle manipulation risk detected. Avoid large transactions during low liquidity periods."
            )

        # Smart contract risk recommendations
        if risk_scores.get(RiskType.SMART_CONTRACT_RISK, 0) > 0.3:
            recommendations.append(
                "📋 Consider position insurance or reducing exposure to unaudited contracts."
            )

        # General recommendations
        if position.health_factor < 1.5:
            recommendations.append(
                f"💡 Maintain health factor above 1.5 for safety. Current: {position.health_factor}"
            )

        return recommendations

    async def _calculate_safe_withdrawal(
        self, position: ProtocolPosition, risk_scores: Dict[RiskType, float]
    ) -> Decimal:
        """Calculate safe withdrawal amount without triggering liquidation"""
        # Safety buffer based on risk
        overall_risk = self._calculate_overall_risk(risk_scores)
        safety_multiplier = 1.5 + (overall_risk * 0.5)  # 1.5x to 2x based on risk

        # Calculate maximum safe withdrawal
        total_supplied = sum(position.supplied_assets.values())
        total_borrowed = sum(position.borrowed_assets.values())

        # Must maintain health factor above safety threshold
        required_collateral = total_borrowed * safety_multiplier
        safe_withdrawal = max(Decimal(0), total_supplied - required_collateral)

        return safe_withdrawal

    def _estimate_loss_potential(
        self, position: ProtocolPosition, risk_scores: Dict[RiskType, float]
    ) -> Decimal:
        """Estimate potential loss based on risks"""
        position_value = position.position_value_usd

        # Loss potential based on risk scores
        liquidation_loss = (
            position_value
            * Decimal(risk_scores.get(RiskType.LIQUIDATION_RISK, 0))
            * Decimal(0.15)
        )
        il_loss = (
            position_value
            * Decimal(risk_scores.get(RiskType.IMPERMANENT_LOSS, 0))
            * Decimal(0.10)
        )
        smart_contract_loss = (
            position_value
            * Decimal(risk_scores.get(RiskType.SMART_CONTRACT_RISK, 0))
            * Decimal(0.05)
        )

        total_loss_potential = liquidation_loss + il_loss + smart_contract_loss

        return total_loss_potential

    async def _check_oracle_health(self, position: ProtocolPosition) -> float:
        """Check oracle health for position assets"""
        assets = list(position.supplied_assets.keys()) + list(
            position.borrowed_assets.keys()
        )
        pairs = [f"{asset}/USD" for asset in assets]

        return await self.oracle_manager.check_multi_oracle_consensus(
            pairs, timeframe="1h"
        )

    async def _check_governance_attacks(
        self, protocol: ProtocolType
    ) -> Optional[ProtocolAlert]:
        """Check for potential governance attacks"""
        # In production, this would monitor governance proposals and voting
        # Placeholder implementation
        return None

    async def _check_tvl_anomalies(
        self, protocol: ProtocolType
    ) -> Optional[ProtocolAlert]:
        """Check for abnormal TVL changes indicating potential issues"""
        # In production, this would track TVL over time
        # Placeholder implementation
        return None

    async def _check_protocol_oracle_health(
        self, protocol: ProtocolType
    ) -> Optional[ProtocolAlert]:
        """Check protocol-wide oracle health"""
        # Placeholder - would check all protocol oracles
        return None

    async def _check_flash_loan_activity(
        self, protocol: ProtocolType
    ) -> Optional[ProtocolAlert]:
        """Monitor for suspicious flash loan activity"""
        # Placeholder - would monitor mempool and recent blocks
        return None


class CompoundVerifier(YieldFarmingVerifier):
    """Compound protocol specific verifier"""

    async def get_user_position(self, user_address: str) -> ProtocolPosition:
        """Get user's Compound position"""
        # Load Compound contracts
        comptroller_abi = self._load_abi("compound_comptroller")
        comptroller = self.w3.eth.contract(
            address=self.protocol_contracts[ProtocolType.COMPOUND]["comptroller"],
            abi=comptroller_abi,
        )

        # Get user's entered markets
        markets = comptroller.functions.getAssetsIn(user_address).call()

        supplied_assets = {}
        borrowed_assets = {}

        for market in markets:
            # Get cToken contract
            ctoken_abi = self._load_abi("compound_ctoken")
            ctoken = self.w3.eth.contract(address=market, abi=ctoken_abi)

            # Get balances
            supply_balance = ctoken.functions.balanceOfUnderlying(user_address).call()
            borrow_balance = ctoken.functions.borrowBalanceStored(user_address).call()

            # Get underlying asset symbol
            underlying_symbol = self._get_underlying_symbol(ctoken)

            if supply_balance > 0:
                supplied_assets[underlying_symbol] = Decimal(supply_balance) / Decimal(
                    10**18
                )
            if borrow_balance > 0:
                borrowed_assets[underlying_symbol] = Decimal(borrow_balance) / Decimal(
                    10**18
                )

        # Calculate health factor
        account_liquidity = comptroller.functions.getAccountLiquidity(
            user_address
        ).call()
        health_factor = self._calculate_compound_health_factor(account_liquidity)

        # Get position value and APY
        position_value = await self._calculate_position_value(
            supplied_assets, borrowed_assets
        )
        apy = await self._calculate_compound_apy(markets, user_address)

        return ProtocolPosition(
            protocol=ProtocolType.COMPOUND,
            user_address=user_address,
            supplied_assets=supplied_assets,
            borrowed_assets=borrowed_assets,
            collateral_ratio=(
                Decimal(sum(supplied_assets.values()))
                / Decimal(sum(borrowed_assets.values()))
                if borrowed_assets
                else Decimal(0)
            ),
            health_factor=health_factor,
            apy=apy,
            position_value_usd=position_value,
        )

    def _load_abi(self, name: str) -> List:
        """Load contract ABI"""
        # In production, load from files
        # Placeholder - return minimal ABI
        if name == "compound_comptroller":
            return [
                {
                    "constant": True,
                    "inputs": [{"name": "account", "type": "address"}],
                    "name": "getAssetsIn",
                    "outputs": [{"name": "", "type": "address[]"}],
                    "type": "function",
                },
                {
                    "constant": True,
                    "inputs": [{"name": "account", "type": "address"}],
                    "name": "getAccountLiquidity",
                    "outputs": [
                        {"name": "", "type": "uint256"},
                        {"name": "", "type": "uint256"},
                        {"name": "", "type": "uint256"},
                    ],
                    "type": "function",
                },
            ]
        return []

    def _get_underlying_symbol(self, ctoken_contract) -> str:
        """Get underlying asset symbol from cToken"""
        # Simplified - in production would call contract
        return "UNKNOWN"

    def _calculate_compound_health_factor(self, account_liquidity: Tuple) -> Decimal:
        """Calculate health factor from account liquidity"""
        error, liquidity, shortfall = account_liquidity

        if error != 0:
            return Decimal(0)

        if shortfall > 0:
            return Decimal(0.5)  # Under-collateralized

        # Simplified calculation
        return Decimal(2.0) if liquidity > 10**18 else Decimal(1.5)

    async def _calculate_position_value(
        self, supplied: Dict, borrowed: Dict
    ) -> Decimal:
        """Calculate total position value in USD"""
        # Placeholder - would fetch actual prices
        return Decimal(sum(supplied.values())) * Decimal(1000)

    async def _calculate_compound_apy(
        self, markets: List, user_address: str
    ) -> Decimal:
        """Calculate net APY for user's position"""
        # Placeholder - would calculate actual APY
        return Decimal(0.05)  # 5% APY


class AaveVerifier(YieldFarmingVerifier):
    """Aave protocol specific verifier"""

    async def get_user_position(self, user_address: str) -> ProtocolPosition:
        """Get user's Aave position"""
        # Load Aave contracts
        lending_pool_abi = self._load_abi("aave_lending_pool")
        lending_pool = self.w3.eth.contract(
            address=self.protocol_contracts[ProtocolType.AAVE]["lending_pool"],
            abi=lending_pool_abi,
        )

        # Get user account data
        user_data = lending_pool.functions.getUserAccountData(user_address).call()

        # Parse user data
        total_collateral_eth = Decimal(user_data[0]) / Decimal(10**18)
        total_debt_eth = Decimal(user_data[1]) / Decimal(10**18)
        available_borrow_eth = Decimal(user_data[2]) / Decimal(10**18)
        liquidation_threshold = Decimal(user_data[3]) / Decimal(10000)
        ltv = Decimal(user_data[4]) / Decimal(10000)
        health_factor = Decimal(user_data[5]) / Decimal(10**18)

        # Get detailed position data
        # In production, would iterate through all reserve tokens
        supplied_assets = {"ETH": total_collateral_eth}
        borrowed_assets = {"ETH": total_debt_eth} if total_debt_eth > 0 else {}

        # Calculate position value (simplified)
        eth_price = Decimal(3500)  # Placeholder
        position_value = (total_collateral_eth - total_debt_eth) * eth_price

        return ProtocolPosition(
            protocol=ProtocolType.AAVE,
            user_address=user_address,
            supplied_assets=supplied_assets,
            borrowed_assets=borrowed_assets,
            collateral_ratio=(
                total_collateral_eth / total_debt_eth
                if total_debt_eth > 0
                else Decimal(0)
            ),
            health_factor=health_factor,
            apy=Decimal(0.03),  # Placeholder
            position_value_usd=position_value,
            liquidation_price=self._calculate_liquidation_price(
                total_collateral_eth, total_debt_eth, liquidation_threshold
            ),
        )

    def _load_abi(self, name: str) -> List:
        """Load contract ABI"""
        if name == "aave_lending_pool":
            return [
                {
                    "constant": True,
                    "inputs": [{"name": "user", "type": "address"}],
                    "name": "getUserAccountData",
                    "outputs": [
                        {"name": "totalCollateralETH", "type": "uint256"},
                        {"name": "totalDebtETH", "type": "uint256"},
                        {"name": "availableBorrowsETH", "type": "uint256"},
                        {"name": "currentLiquidationThreshold", "type": "uint256"},
                        {"name": "ltv", "type": "uint256"},
                        {"name": "healthFactor", "type": "uint256"},
                    ],
                    "type": "function",
                }
            ]
        return []

    def _calculate_liquidation_price(
        self, collateral: Decimal, debt: Decimal, threshold: Decimal
    ) -> Decimal:
        """Calculate liquidation price"""
        if debt == 0:
            return Decimal(0)

        # Liquidation occurs when: collateral_value * threshold = debt_value
        # Therefore: liquidation_price = debt / (collateral * threshold)
        return debt / (collateral * threshold)


class CurveVerifier(YieldFarmingVerifier):
    """Curve protocol specific verifier"""

    async def get_lp_position(
        self, user_address: str, pool_address: str
    ) -> ProtocolPosition:
        """Get user's Curve LP position"""
        # Load Curve pool contract
        pool_abi = self._load_abi("curve_pool")
        pool = self.w3.eth.contract(address=pool_address, abi=pool_abi)

        # Get LP token balance
        lp_balance = pool.functions.balanceOf(user_address).call()

        if lp_balance == 0:
            return ProtocolPosition(
                protocol=ProtocolType.CURVE,
                user_address=user_address,
                supplied_assets={},
                borrowed_assets={},
                collateral_ratio=Decimal(0),
                health_factor=Decimal(10),  # No liquidation risk for LP
                apy=Decimal(0),
                position_value_usd=Decimal(0),
            )

        # Get pool details
        virtual_price = pool.functions.get_virtual_price().call()
        total_supply = pool.functions.totalSupply().call()

        # Calculate position value
        position_value = Decimal(lp_balance) * Decimal(virtual_price) / Decimal(10**36)

        # Get pool composition (simplified)
        # In production, would get actual token balances
        supplied_assets = {"POOL_LP": Decimal(lp_balance) / Decimal(10**18)}

        # Calculate APY (would fetch from Curve API in production)
        apy = await self._fetch_curve_apy(pool_address)

        return ProtocolPosition(
            protocol=ProtocolType.CURVE,
            user_address=user_address,
            supplied_assets=supplied_assets,
            borrowed_assets={},  # No borrowing in Curve
            collateral_ratio=Decimal(0),  # Not applicable
            health_factor=Decimal(10),  # No liquidation risk
            apy=apy,
            position_value_usd=position_value,
        )

    def _load_abi(self, name: str) -> List:
        """Load contract ABI"""
        if name == "curve_pool":
            return [
                {
                    "constant": True,
                    "inputs": [{"name": "account", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function",
                },
                {
                    "constant": True,
                    "inputs": [],
                    "name": "get_virtual_price",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function",
                },
                {
                    "constant": True,
                    "inputs": [],
                    "name": "totalSupply",
                    "outputs": [{"name": "", "type": "uint256"}],
                    "type": "function",
                },
            ]
        return []

    async def _fetch_curve_apy(self, pool_address: str) -> Decimal:
        """Fetch APY from Curve API or calculate from events"""
        # Placeholder - would fetch actual APY
        return Decimal(0.08)  # 8% APY

    async def calculate_impermanent_loss(
        self, pool_address: str, user_address: str
    ) -> Decimal:
        """Calculate impermanent loss for Curve position"""
        # Get historical entry point
        # Calculate current vs initial token ratios
        # Return IL percentage
        return Decimal(0.02)  # 2% IL placeholder


class YieldFarmingIntegrationManager:
    """Manager for all yield farming protocol integrations"""

    def __init__(self, web3_provider: str):
        self.verification_engine = VerificationEngine()
        self.compound_verifier = CompoundVerifier(
            web3_provider, self.verification_engine
        )
        self.aave_verifier = AaveVerifier(web3_provider, self.verification_engine)
        self.curve_verifier = CurveVerifier(web3_provider, self.verification_engine)

        self.verifiers = {
            ProtocolType.COMPOUND: self.compound_verifier,
            ProtocolType.AAVE: self.aave_verifier,
            ProtocolType.CURVE: self.curve_verifier,
        }

    async def verify_user_positions(
        self, user_address: str
    ) -> Dict[str, RiskAssessment]:
        """Verify all user positions across protocols"""
        assessments = {}

        # Check Compound
        try:
            compound_position = await self.compound_verifier.get_user_position(
                user_address
            )
            if compound_position.position_value_usd > 0:
                assessment = await self.compound_verifier.verify_position_safety(
                    compound_position
                )
                assessments["compound"] = assessment
        except Exception as e:
            print(f"Error checking Compound: {e}")

        # Check Aave
        try:
            aave_position = await self.aave_verifier.get_user_position(user_address)
            if aave_position.position_value_usd > 0:
                assessment = await self.aave_verifier.verify_position_safety(
                    aave_position
                )
                assessments["aave"] = assessment
        except Exception as e:
            print(f"Error checking Aave: {e}")

        # Check Curve (would need pool addresses)
        # Skipped in this example

        return assessments

    async def monitor_all_protocols(self) -> Dict[ProtocolType, List[ProtocolAlert]]:
        """Monitor all protocols for systemic risks"""
        all_alerts = {}

        for protocol, verifier in self.verifiers.items():
            alerts = await verifier.monitor_protocol_risks(protocol)
            if alerts:
                all_alerts[protocol] = alerts

        return all_alerts

    async def get_aggregated_risk_report(self, user_address: str) -> Dict[str, Any]:
        """Get comprehensive risk report across all protocols"""
        assessments = await self.verify_user_positions(user_address)

        total_value = Decimal(0)
        total_risk = 0
        all_recommendations = []

        for protocol, assessment in assessments.items():
            position_value = assessment.estimated_loss_potential
            total_value += position_value
            total_risk += assessment.overall_risk_score * float(position_value)
            all_recommendations.extend(assessment.recommendations)

        weighted_risk = total_risk / float(total_value) if total_value > 0 else 0

        return {
            "user_address": user_address,
            "total_position_value": total_value,
            "weighted_risk_score": weighted_risk,
            "protocol_assessments": assessments,
            "aggregated_recommendations": list(set(all_recommendations)),
            "timestamp": asyncio.get_event_loop().time(),
        }


# Example usage
async def main():
    """Example yield farming safety verification"""

    # Initialize manager
    manager = YieldFarmingIntegrationManager(
        web3_provider="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
    )

    # Example user address
    user_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f5b9E0"

    # Get risk assessments
    print("🌾 Checking yield farming positions...\n")

    assessments = await manager.verify_user_positions(user_address)

    for protocol, assessment in assessments.items():
        print(f"\n📊 {protocol.upper()} Assessment:")
        print(f"   Overall Risk Score: {assessment.overall_risk_score:.2f}")
        print(
            f"   Estimated Loss Potential: ${assessment.estimated_loss_potential:.2f}"
        )
        print(f"   Safe Withdrawal Amount: ${assessment.safe_withdrawal_amount:.2f}")
        print(f"   Oracle Health: {assessment.oracle_health:.1%}")

        if assessment.recommendations:
            print("   Recommendations:")
            for rec in assessment.recommendations:
                print(f"   - {rec}")

    # Monitor protocols
    print("\n\n🔍 Monitoring protocol risks...\n")

    protocol_alerts = await manager.monitor_all_protocols()

    for protocol, alerts in protocol_alerts.items():
        print(f"\n⚠️ {protocol.value.upper()} Alerts:")
        for alert in alerts:
            print(f"   [{alert.severity.upper()}] {alert.message}")
            if alert.action_required:
                print(
                    f"   ACTION REQUIRED! Estimated impact: ${alert.estimated_impact}"
                )


if __name__ == "__main__":
    asyncio.run(main())

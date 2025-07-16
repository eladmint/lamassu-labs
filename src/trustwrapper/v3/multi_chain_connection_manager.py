#!/usr/bin/env python3
"""
TrustWrapper v3.0 Multi-Chain Connection Manager
Orchestrates universal chain adapters and oracle integration
Provides unified interface for multi-chain AI verification
"""

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from .enhanced_oracle_integration import (
    EnhancedOracleIntegration,
    MultiOracleConsensus,
    get_enhanced_oracle_integration,
)

# Import v3.0 components
from .universal_chain_adapter import (
    DEFAULT_CHAIN_CONFIGS,
    ChainConfig,
    UniversalChainAdapter,
    VerificationData,
    VerificationResult,
    get_universal_adapter,
)


class SecurityLevel(Enum):
    """Security levels for verification"""

    BASIC = "basic"  # Single chain verification
    STANDARD = "standard"  # 3-chain consensus
    HIGH = "high"  # 5-7 chain consensus
    MAXIMUM = "maximum"  # 8+ chain consensus


@dataclass
class VerificationRequest:
    """Request for multi-chain AI verification"""

    request_id: str
    ai_decision_data: Dict[str, Any]
    security_level: SecurityLevel
    target_chains: Optional[List[str]] = None
    oracle_validation: bool = True
    custom_threshold: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UniversalVerificationResult:
    """Result of universal multi-chain verification"""

    request_id: str
    verification_id: str
    overall_success: bool
    consensus_score: float
    security_level: SecurityLevel
    total_chains: int
    successful_chains: int
    failed_chains: int
    execution_time_seconds: float
    oracle_consensus: Optional[MultiOracleConsensus]
    chain_results: Dict[str, VerificationResult]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # Convert enum to string for JSON serialization
        result["security_level"] = self.security_level.value
        return result


@dataclass
class ConnectionHealth:
    """Health status of all connections"""

    overall_health_score: float
    chain_health: Dict[str, Any]
    oracle_health: Dict[str, Any]
    last_check: float
    status: str  # healthy, degraded, unhealthy
    issues: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MultiChainConnectionManager:
    """
    Multi-Chain Connection Manager for TrustWrapper v3.0
    Orchestrates universal chain verification with oracle integration
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        # Core components
        self.universal_adapter: Optional[UniversalChainAdapter] = None
        self.oracle_integration: Optional[EnhancedOracleIntegration] = None

        # State management
        self.initialized = False
        self.active_verifications = {}
        self.verification_history = []
        self.health_cache = {}

        # Performance metrics
        self.metrics = {
            "total_verifications": 0,
            "successful_verifications": 0,
            "failed_verifications": 0,
            "average_execution_time": 0.0,
            "average_consensus_score": 0.0,
        }

    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration for connection manager"""
        return {
            "security_levels": {
                SecurityLevel.BASIC: {
                    "min_chains": 1,
                    "consensus_threshold": 1.0,
                    "target_chains": ["ethereum"],
                },
                SecurityLevel.STANDARD: {
                    "min_chains": 3,
                    "consensus_threshold": 0.67,
                    "target_chains": ["ethereum", "polygon", "cardano"],
                },
                SecurityLevel.HIGH: {
                    "min_chains": 5,
                    "consensus_threshold": 0.70,
                    "target_chains": [
                        "ethereum",
                        "polygon",
                        "bitcoin",
                        "cardano",
                        "solana",
                    ],
                },
                SecurityLevel.MAXIMUM: {
                    "min_chains": 8,
                    "consensus_threshold": 0.75,
                    "target_chains": [
                        "ethereum",
                        "polygon",
                        "arbitrum",
                        "bitcoin",
                        "cardano",
                        "solana",
                        "ton",
                        "icp",
                    ],
                },
            },
            "verification": {
                "timeout_seconds": 60.0,
                "retry_attempts": 2,
                "enable_parallel_execution": True,
                "enable_oracle_validation": True,
            },
            "health_monitoring": {
                "check_interval": 30.0,
                "degraded_threshold": 0.7,
                "unhealthy_threshold": 0.5,
            },
            "performance": {
                "max_concurrent_verifications": 100,
                "history_retention_hours": 24,
                "metrics_update_interval": 60.0,
            },
        }

    async def initialize(
        self,
        chain_configs: Optional[Dict[str, ChainConfig]] = None,
        oracle_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the multi-chain connection manager"""
        try:
            self.logger.info("🚀 Initializing Multi-Chain Connection Manager...")

            # Initialize universal chain adapter
            self.universal_adapter = await get_universal_adapter(
                chain_configs or DEFAULT_CHAIN_CONFIGS
            )

            # Initialize oracle integration
            self.oracle_integration = await get_enhanced_oracle_integration(
                oracle_config
            )

            # Start background tasks
            asyncio.create_task(self._run_health_monitor())
            asyncio.create_task(self._run_metrics_updater())
            asyncio.create_task(self._run_history_cleaner())

            self.initialized = True
            self.logger.info(
                "✅ Multi-Chain Connection Manager initialized successfully"
            )

        except Exception as e:
            self.logger.error(
                f"Failed to initialize Multi-Chain Connection Manager: {e}"
            )
            raise

    async def universal_verify_ai_decision(
        self, verification_request: VerificationRequest
    ) -> UniversalVerificationResult:
        """
        Perform universal AI decision verification across multiple chains
        Main entry point for multi-chain verification
        """
        if not self.initialized:
            raise RuntimeError("Multi-Chain Connection Manager not initialized")

        start_time = time.time()
        verification_id = (
            f"uv_{int(time.time() * 1000)}_{verification_request.request_id}"
        )

        self.logger.info(f"🔍 Starting universal verification: {verification_id}")
        self.logger.info(
            f"📊 Security level: {verification_request.security_level.value}"
        )

        try:
            # Get security level configuration
            security_config = self.config["security_levels"][
                verification_request.security_level
            ]

            # Determine target chains
            target_chains = (
                verification_request.target_chains or security_config["target_chains"]
            )

            # Validate minimum chains requirement
            if len(target_chains) < security_config["min_chains"]:
                raise ValueError(
                    f"Insufficient chains for {verification_request.security_level.value} security: "
                    f"need {security_config['min_chains']}, got {len(target_chains)}"
                )

            # Prepare verification data
            verification_data = VerificationData(
                verification_id=verification_id,
                ai_decision_hash=self._hash_ai_decision(
                    verification_request.ai_decision_data
                ),
                timestamp=time.time(),
                decision_metadata=verification_request.ai_decision_data,
                risk_score=verification_request.ai_decision_data.get("risk_score", 0.5),
                confidence_level=verification_request.ai_decision_data.get(
                    "confidence", 0.8
                ),
            )

            # Store active verification
            self.active_verifications[verification_id] = {
                "request": verification_request,
                "start_time": start_time,
                "status": "processing",
            }

            # Perform parallel verification and oracle validation
            chain_verification_task = self.universal_adapter.universal_verify(
                verification_data,
                target_chains,
                verification_request.custom_threshold
                or security_config["consensus_threshold"],
            )

            oracle_validation_task = None
            if verification_request.oracle_validation:
                oracle_validation_task = self._validate_with_oracles(
                    verification_request
                )

            # Execute tasks
            if oracle_validation_task:
                chain_result, oracle_consensus = await asyncio.gather(
                    chain_verification_task,
                    oracle_validation_task,
                    return_exceptions=True,
                )

                # Handle oracle validation errors
                if isinstance(oracle_consensus, Exception):
                    self.logger.warning(f"Oracle validation failed: {oracle_consensus}")
                    oracle_consensus = None
            else:
                chain_result = await chain_verification_task
                oracle_consensus = None

            # Handle chain verification errors
            if isinstance(chain_result, Exception):
                raise chain_result

            # Calculate execution time
            execution_time = time.time() - start_time

            # Perform risk assessment
            risk_assessment = await self._assess_verification_risk(
                verification_request, chain_result, oracle_consensus
            )

            # Generate recommendations
            recommendations = self._generate_recommendations(
                verification_request, chain_result, oracle_consensus, risk_assessment
            )

            # Create result
            result = UniversalVerificationResult(
                request_id=verification_request.request_id,
                verification_id=verification_id,
                overall_success=chain_result["consensus_achieved"],
                consensus_score=chain_result["weighted_consensus_score"],
                security_level=verification_request.security_level,
                total_chains=chain_result["total_chains"],
                successful_chains=chain_result["successful_verifications"],
                failed_chains=chain_result["failed_verifications"],
                execution_time_seconds=execution_time,
                oracle_consensus=oracle_consensus,
                chain_results={
                    chain_id: VerificationResult(**result_data)
                    for chain_id, result_data in chain_result[
                        "results_by_chain"
                    ].items()
                    if isinstance(result_data, dict) and "success" in result_data
                },
                risk_assessment=risk_assessment,
                recommendations=recommendations,
                timestamp=time.time(),
            )

            # Update metrics
            self._update_verification_metrics(result)

            # Store in history
            self.verification_history.append(result)

            # Remove from active verifications
            del self.active_verifications[verification_id]

            self.logger.info(f"✅ Universal verification complete: {verification_id}")
            self.logger.info(
                f"📊 Result: {result.overall_success}, consensus: {result.consensus_score:.2f}"
            )

            return result

        except Exception as e:
            # Clean up active verification
            if verification_id in self.active_verifications:
                del self.active_verifications[verification_id]

            self.logger.error(f"Universal verification failed: {e}")

            # Return failed result
            return UniversalVerificationResult(
                request_id=verification_request.request_id,
                verification_id=verification_id,
                overall_success=False,
                consensus_score=0.0,
                security_level=verification_request.security_level,
                total_chains=0,
                successful_chains=0,
                failed_chains=0,
                execution_time_seconds=time.time() - start_time,
                oracle_consensus=None,
                chain_results={},
                risk_assessment={"error": str(e)},
                recommendations=[
                    "Retry with different security level",
                    "Check chain connectivity",
                ],
                timestamp=time.time(),
            )

    def _hash_ai_decision(self, ai_decision_data: Dict[str, Any]) -> str:
        """Create hash of AI decision data"""
        decision_str = json.dumps(ai_decision_data, sort_keys=True)
        return hashlib.sha256(decision_str.encode()).hexdigest()

    async def _validate_with_oracles(
        self, verification_request: VerificationRequest
    ) -> Optional[MultiOracleConsensus]:
        """Validate verification request with oracle data"""
        try:
            # Extract asset information from AI decision
            ai_data = verification_request.ai_decision_data
            asset_pair = ai_data.get("asset_pair", "BTC/USD")

            # Get multi-oracle consensus
            consensus = await self.oracle_integration.get_multi_oracle_consensus(
                asset_pair
            )

            if consensus:
                self.logger.debug(
                    f"Oracle validation: {asset_pair} consensus score: {consensus.confidence_score}"
                )

            return consensus

        except Exception as e:
            self.logger.error(f"Oracle validation error: {e}")
            return None

    async def _assess_verification_risk(
        self,
        verification_request: VerificationRequest,
        chain_result: Dict[str, Any],
        oracle_consensus: Optional[MultiOracleConsensus],
    ) -> Dict[str, Any]:
        """Assess the risk of the verification result"""
        risk_factors = {}

        # Chain consensus risk
        consensus_score = chain_result.get("weighted_consensus_score", 0.0)
        risk_factors["consensus_risk"] = max(0.0, 1.0 - consensus_score)

        # Chain diversity risk
        total_chains = chain_result.get("total_chains", 0)
        successful_chains = chain_result.get("successful_verifications", 0)
        success_rate = successful_chains / total_chains if total_chains > 0 else 0.0
        risk_factors["chain_diversity_risk"] = max(0.0, 1.0 - success_rate)

        # Oracle validation risk
        if oracle_consensus:
            oracle_confidence = oracle_consensus.confidence_score
            risk_factors["oracle_risk"] = max(0.0, 1.0 - oracle_confidence)

            # Price deviation risk
            price_deviation = oracle_consensus.price_deviation
            risk_factors["price_deviation_risk"] = min(
                1.0, price_deviation * 10
            )  # Scale to 0-1
        else:
            risk_factors["oracle_risk"] = 0.5  # Moderate risk without oracle validation
            risk_factors["price_deviation_risk"] = 0.3

        # Security level risk
        security_weights = {
            SecurityLevel.BASIC: 0.4,
            SecurityLevel.STANDARD: 0.2,
            SecurityLevel.HIGH: 0.1,
            SecurityLevel.MAXIMUM: 0.05,
        }
        risk_factors["security_level_risk"] = security_weights.get(
            verification_request.security_level, 0.3
        )

        # AI decision confidence risk
        ai_confidence = verification_request.ai_decision_data.get("confidence", 0.8)
        risk_factors["ai_confidence_risk"] = max(0.0, 1.0 - ai_confidence)

        # Calculate overall risk score
        weights = {
            "consensus_risk": 0.3,
            "chain_diversity_risk": 0.2,
            "oracle_risk": 0.2,
            "price_deviation_risk": 0.1,
            "security_level_risk": 0.1,
            "ai_confidence_risk": 0.1,
        }

        overall_risk = sum(
            risk_factors.get(factor, 0.0) * weight for factor, weight in weights.items()
        )

        return {
            "overall_risk_score": overall_risk,
            "risk_level": (
                "LOW"
                if overall_risk < 0.3
                else "MEDIUM" if overall_risk < 0.7 else "HIGH"
            ),
            "risk_factors": risk_factors,
            "assessment_timestamp": time.time(),
        }

    def _generate_recommendations(
        self,
        verification_request: VerificationRequest,
        chain_result: Dict[str, Any],
        oracle_consensus: Optional[MultiOracleConsensus],
        risk_assessment: Dict[str, Any],
    ) -> List[str]:
        """Generate recommendations based on verification results"""
        recommendations = []

        # Consensus-based recommendations
        consensus_score = chain_result.get("weighted_consensus_score", 0.0)
        if consensus_score < 0.5:
            recommendations.append(
                "REJECT: Low consensus score indicates high verification risk"
            )
        elif consensus_score < 0.7:
            recommendations.append(
                "CAUTION: Moderate consensus - consider additional validation"
            )
        else:
            recommendations.append(
                "APPROVE: High consensus score supports verification"
            )

        # Chain diversity recommendations
        success_rate = chain_result.get("success_rate", 0.0)
        if success_rate < 0.6:
            recommendations.append(
                "Consider upgrading to higher security level for better chain coverage"
            )

        # Oracle-based recommendations
        if oracle_consensus:
            if oracle_consensus.price_deviation > 0.05:
                recommendations.append(
                    "HIGH PRICE DEVIATION: Significant oracle disagreement detected"
                )
            if oracle_consensus.confidence_score < 0.8:
                recommendations.append(
                    "Oracle confidence low - validate with additional price sources"
                )
        else:
            recommendations.append(
                "Oracle validation unavailable - proceed with caution"
            )

        # Risk-based recommendations
        overall_risk = risk_assessment.get("overall_risk_score", 0.5)
        if overall_risk > 0.7:
            recommendations.append(
                "HIGH RISK: Consider manual review before proceeding"
            )
        elif overall_risk > 0.4:
            recommendations.append("MODERATE RISK: Additional validation recommended")

        # Security level recommendations
        if verification_request.security_level == SecurityLevel.BASIC:
            recommendations.append(
                "Consider upgrading to STANDARD security for better validation"
            )

        return recommendations[:5]  # Limit to top 5 recommendations

    def _update_verification_metrics(self, result: UniversalVerificationResult):
        """Update performance metrics"""
        self.metrics["total_verifications"] += 1

        if result.overall_success:
            self.metrics["successful_verifications"] += 1
        else:
            self.metrics["failed_verifications"] += 1

        # Update rolling averages
        total = self.metrics["total_verifications"]
        self.metrics["average_execution_time"] = (
            self.metrics["average_execution_time"] * (total - 1)
            + result.execution_time_seconds
        ) / total
        self.metrics["average_consensus_score"] = (
            self.metrics["average_consensus_score"] * (total - 1)
            + result.consensus_score
        ) / total

    async def _run_health_monitor(self):
        """Background task to monitor system health"""
        while True:
            try:
                await asyncio.sleep(self.config["health_monitoring"]["check_interval"])
                await self._update_health_status()
            except Exception as e:
                self.logger.error(f"Health monitor error: {e}")
                await asyncio.sleep(30.0)

    async def _run_metrics_updater(self):
        """Background task to update performance metrics"""
        while True:
            try:
                await asyncio.sleep(
                    self.config["performance"]["metrics_update_interval"]
                )
                # Metrics are updated in real-time, this just logs them
                self.logger.debug(f"Metrics: {self.metrics}")
            except Exception as e:
                self.logger.error(f"Metrics updater error: {e}")
                await asyncio.sleep(60.0)

    async def _run_history_cleaner(self):
        """Background task to clean old verification history"""
        while True:
            try:
                await asyncio.sleep(3600.0)  # Run every hour
                await self._clean_old_history()
            except Exception as e:
                self.logger.error(f"History cleaner error: {e}")
                await asyncio.sleep(3600.0)

    async def _update_health_status(self):
        """Update overall system health status"""
        try:
            # Get chain health
            chain_health = await self.universal_adapter.get_chain_health()

            # Get oracle health
            oracle_health = self.oracle_integration.get_status()

            # Calculate overall health
            chain_score = chain_health.get("overall_health_score", 0.0)
            oracle_score = 1.0 if oracle_health.get("running", False) else 0.0

            overall_score = chain_score * 0.7 + oracle_score * 0.3

            # Determine status
            degraded_threshold = self.config["health_monitoring"]["degraded_threshold"]
            unhealthy_threshold = self.config["health_monitoring"][
                "unhealthy_threshold"
            ]

            if overall_score >= degraded_threshold:
                status = "healthy"
            elif overall_score >= unhealthy_threshold:
                status = "degraded"
            else:
                status = "unhealthy"

            # Identify issues
            issues = []
            if chain_score < 0.8:
                issues.append("Chain connectivity issues detected")
            if not oracle_health.get("running", False):
                issues.append("Oracle integration not running")

            # Generate recommendations
            recommendations = []
            if status == "degraded":
                recommendations.append("Monitor system closely")
                recommendations.append("Check chain connections")
            elif status == "unhealthy":
                recommendations.append("Immediate attention required")
                recommendations.append("Restart failed services")

            self.health_cache = ConnectionHealth(
                overall_health_score=overall_score,
                chain_health=chain_health,
                oracle_health=oracle_health,
                last_check=time.time(),
                status=status,
                issues=issues,
                recommendations=recommendations,
            )

        except Exception as e:
            self.logger.error(f"Health status update failed: {e}")

    async def _clean_old_history(self):
        """Clean old verification history"""
        retention_hours = self.config["performance"]["history_retention_hours"]
        cutoff_time = time.time() - (retention_hours * 3600)

        original_count = len(self.verification_history)
        self.verification_history = [
            result
            for result in self.verification_history
            if result.timestamp >= cutoff_time
        ]

        cleaned_count = original_count - len(self.verification_history)
        if cleaned_count > 0:
            self.logger.debug(f"Cleaned {cleaned_count} old verification records")

    async def get_system_health(self) -> ConnectionHealth:
        """Get current system health status"""
        if not self.health_cache:
            await self._update_health_status()
        return self.health_cache

    def get_verification_history(
        self,
        limit: Optional[int] = None,
        security_level: Optional[SecurityLevel] = None,
    ) -> List[UniversalVerificationResult]:
        """Get verification history with optional filtering"""
        history = self.verification_history

        # Filter by security level if specified
        if security_level:
            history = [r for r in history if r.security_level == security_level]

        # Sort by timestamp (newest first)
        history = sorted(history, key=lambda r: r.timestamp, reverse=True)

        # Apply limit if specified
        if limit:
            history = history[:limit]

        return history

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        success_rate = (
            self.metrics["successful_verifications"]
            / self.metrics["total_verifications"]
            if self.metrics["total_verifications"] > 0
            else 0.0
        )

        return {
            **self.metrics,
            "success_rate": success_rate,
            "active_verifications": len(self.active_verifications),
            "history_entries": len(self.verification_history),
        }

    async def get_chain_cost_estimate(
        self, verification_request: VerificationRequest
    ) -> Dict[str, Any]:
        """Get cost estimate for verification"""
        if not self.initialized:
            raise RuntimeError("Multi-Chain Connection Manager not initialized")

        # Get security level configuration
        security_config = self.config["security_levels"][
            verification_request.security_level
        ]
        target_chains = (
            verification_request.target_chains or security_config["target_chains"]
        )

        # Create mock verification data for cost estimation
        verification_data = VerificationData(
            verification_id="cost_estimate",
            ai_decision_hash="mock_hash",
            timestamp=time.time(),
            decision_metadata=verification_request.ai_decision_data,
            risk_score=0.5,
            confidence_level=0.8,
        )

        return await self.universal_adapter.estimate_total_verification_cost(
            verification_data, target_chains
        )

    async def shutdown(self):
        """Shutdown the connection manager"""
        self.logger.info("🛑 Shutting down Multi-Chain Connection Manager...")

        if self.universal_adapter:
            await self.universal_adapter.shutdown()

        if self.oracle_integration:
            await self.oracle_integration.stop()

        self.initialized = False
        self.logger.info("Multi-Chain Connection Manager shutdown complete")


# Singleton instance
_connection_manager_instance = None


async def get_connection_manager(
    config: Optional[Dict[str, Any]] = None,
    chain_configs: Optional[Dict[str, ChainConfig]] = None,
    oracle_config: Optional[Dict[str, Any]] = None,
) -> MultiChainConnectionManager:
    """Get or create the global connection manager instance"""
    global _connection_manager_instance

    if _connection_manager_instance is None:
        _connection_manager_instance = MultiChainConnectionManager(config)
        await _connection_manager_instance.initialize(chain_configs, oracle_config)

    return _connection_manager_instance

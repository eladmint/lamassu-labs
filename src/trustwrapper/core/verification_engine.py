"""
TrustWrapper v2.0 Core Verification Engine
Primary orchestrator for all verification operations

This module provides the main verification engine that coordinates
oracle verification, local verification, and ZK proof generation
for real-time AI trading safety and DeFi integration validation.
"""

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from .local_verification import LocalVerificationEngine
from .oracle_risk_manager import OracleRiskManager
from .zk_proof_generator import ZKProofGenerator


class VerificationStatus(Enum):
    """Verification result status"""

    VERIFIED = "verified"
    FAILED = "failed"
    PENDING = "pending"
    REQUIRES_REVIEW = "requires_review"


class RiskLevel(Enum):
    """Risk assessment levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class VerificationRequest:
    """Verification request structure"""

    request_id: str
    verification_type: str
    data: Dict[str, Any]
    timestamp: float
    priority: str = "normal"
    preserve_privacy: bool = True
    oracle_sources: Optional[List[str]] = None
    compliance_requirements: Optional[List[str]] = None


@dataclass
class VerificationResult:
    """Unified verification result"""

    request_id: str
    status: VerificationStatus
    confidence_score: float
    risk_level: RiskLevel
    risk_score: float
    violations: List[str]
    oracle_health: float
    local_verification_time: float
    zk_proof: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    recommendations: Optional[List[str]] = None
    compliance_status: Optional[Dict[str, bool]] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class VerificationEngine:
    """
    TrustWrapper v2.0 Core Verification Engine

    Orchestrates all verification operations including:
    - Oracle risk management and price verification
    - Local verification for <10ms response times
    - Zero-knowledge proof generation
    - Compliance and regulatory validation
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()

        # Initialize core components
        self.oracle_manager = OracleRiskManager(
            oracle_config=self.config.get("oracle", {})
        )
        self.local_verifier = LocalVerificationEngine(
            performance_config=self.config.get("local_verification", {})
        )
        self.zk_generator = ZKProofGenerator(zk_config=self.config.get("zk_proofs", {}))

        # Verification metrics
        self.metrics = {
            "total_verifications": 0,
            "successful_verifications": 0,
            "failed_verifications": 0,
            "average_latency": 0.0,
            "oracle_health_score": 1.0,
        }

        # Active verification cache
        self.verification_cache = {}
        self.cache_ttl = self.config.get("cache_ttl", 300)  # 5 minutes

    def _get_default_config(self) -> Dict:
        """Get default configuration for verification engine"""
        return {
            "max_verification_time": 50,  # 50ms target
            "confidence_threshold": 0.8,
            "oracle": {
                "min_sources": 3,
                "consensus_threshold": 0.67,
                "max_deviation": 0.02,  # 2%
                "timeout": 5,  # 5 seconds
                "cache_ttl": 60,
                "health_check_interval": 30,
                "sources": {
                    "chainlink": {"weight": 0.4, "reliability": 0.98, "timeout": 3},
                    "band_protocol": {"weight": 0.3, "reliability": 0.96, "timeout": 3},
                    "uniswap_v3": {"weight": 0.2, "reliability": 0.94, "timeout": 2},
                    "compound": {"weight": 0.1, "reliability": 0.95, "timeout": 3},
                },
            },
            "local_verification": {
                "target_latency": 10,  # 10ms target
                "cache_size": 10000,
                "performance_threshold": 0.05,  # 5% deviation threshold
                "risk_threshold": 0.7,
            },
            "zk_proofs": {"circuit_type": "groth16", "trusted_setup": True},
            "compliance": {
                "required_frameworks": ["SOC2", "ISO27001"],
                "audit_trail": True,
            },
        }

    async def verify(self, request: VerificationRequest) -> VerificationResult:
        """
        Main verification method - orchestrates all verification components

        Args:
            request: Verification request with data and parameters

        Returns:
            VerificationResult with comprehensive verification status
        """
        start_time = time.time()

        try:
            # Check cache first for performance
            cache_key = self._generate_cache_key(request)
            cached_result = self._get_cached_result(cache_key)
            if cached_result:
                return cached_result

            # Initialize result structure
            result = VerificationResult(
                request_id=request.request_id,
                status=VerificationStatus.PENDING,
                confidence_score=0.0,
                risk_level=RiskLevel.HIGH,
                risk_score=1.0,
                violations=[],
                oracle_health=0.0,
                local_verification_time=0.0,
            )

            # Step 1: Local verification (fastest, <10ms target)
            local_start = time.time()
            local_result = await self.local_verifier.verify(
                verification_type=request.verification_type, data=request.data
            )
            result.local_verification_time = (time.time() - local_start) * 1000  # ms

            # Step 2: Oracle verification (if required for this verification type)
            oracle_result = None
            if self._requires_oracle_verification(request.verification_type):
                oracle_result = await self.oracle_manager.verify_data_integrity(
                    data=request.data, sources=request.oracle_sources
                )
                result.oracle_health = oracle_result.get("health_score", 0.0)
            else:
                result.oracle_health = 1.0  # N/A for non-oracle verifications

            # Step 3: Risk assessment
            risk_assessment = await self._assess_risk(
                local_result=local_result, oracle_result=oracle_result, request=request
            )

            # Step 4: Compliance validation
            compliance_result = await self._validate_compliance(
                request=request, local_result=local_result, oracle_result=oracle_result
            )

            # Step 5: Generate ZK proof (if privacy preservation required)
            zk_proof = None
            if request.preserve_privacy:
                zk_proof = await self.zk_generator.generate_verification_proof(
                    verification_data={
                        "local_result": local_result,
                        "risk_assessment": risk_assessment,
                        "compliance": compliance_result,
                    },
                    preserve_sensitive_data=True,
                )

            # Compile final result
            result.status = self._determine_final_status(
                local_result, oracle_result, risk_assessment, compliance_result
            )
            result.confidence_score = self._calculate_confidence_score(
                local_result, oracle_result, risk_assessment
            )
            result.risk_level = risk_assessment["risk_level"]
            result.risk_score = risk_assessment["risk_score"]
            result.violations = risk_assessment.get("violations", [])
            result.zk_proof = zk_proof
            result.details = {
                "local_verification": local_result,
                "oracle_verification": oracle_result,
                "risk_assessment": risk_assessment,
                "total_verification_time": (time.time() - start_time) * 1000,
            }
            result.compliance_status = compliance_result
            result.recommendations = self._generate_recommendations(result)

            # Cache result for performance
            self._cache_result(cache_key, result)

            # Update metrics
            self._update_metrics(result, time.time() - start_time)

            return result

        except Exception as e:
            # Error handling with graceful degradation
            error_result = VerificationResult(
                request_id=request.request_id,
                status=VerificationStatus.FAILED,
                confidence_score=0.0,
                risk_level=RiskLevel.CRITICAL,
                risk_score=1.0,
                violations=[f"verification_engine_error: {str(e)}"],
                oracle_health=0.0,
                local_verification_time=(time.time() - start_time) * 1000,
                details={"error": str(e), "error_type": type(e).__name__},
            )

            self.metrics["failed_verifications"] += 1
            return error_result

    async def verify_trading_decision(
        self, bot_id: str, trade_data: Dict
    ) -> VerificationResult:
        """Specialized method for trading decision verification"""
        request = VerificationRequest(
            request_id=f"trade_{bot_id}_{int(time.time())}",
            verification_type="trading_decision",
            data={"bot_id": bot_id, "trade": trade_data, "timestamp": time.time()},
            timestamp=time.time(),
            oracle_sources=["chainlink", "band_protocol", "compound"],
            preserve_privacy=True,
        )

        return await self.verify(request)

    async def verify_performance_claims(
        self, bot_id: str, claims: Dict, actual_performance: Dict
    ) -> VerificationResult:
        """Specialized method for performance claim verification"""
        request = VerificationRequest(
            request_id=f"performance_{bot_id}_{int(time.time())}",
            verification_type="performance_claims",
            data={
                "bot_id": bot_id,
                "claimed_performance": claims,
                "actual_performance": actual_performance,
                "timestamp": time.time(),
            },
            timestamp=time.time(),
            preserve_privacy=True,
        )

        return await self.verify(request)

    async def verify_defi_strategy(
        self, strategy_data: Dict, privacy_level: str = "high"
    ) -> VerificationResult:
        """Specialized method for DeFi strategy verification"""
        request = VerificationRequest(
            request_id=f"defi_strategy_{int(time.time())}",
            verification_type="defi_strategy",
            data=strategy_data,
            timestamp=time.time(),
            preserve_privacy=(privacy_level in ["high", "maximum"]),
            oracle_sources=["chainlink", "uniswap_v3", "compound", "aave"],
        )

        return await self.verify(request)

    def _requires_oracle_verification(self, verification_type: str) -> bool:
        """Determine if verification type requires oracle data"""
        oracle_required_types = {
            "trading_decision",
            "defi_strategy",
            "price_verification",
            "mev_protection",
            "bridge_verification",
            "yield_farming",
        }
        return verification_type in oracle_required_types

    async def _assess_risk(
        self,
        local_result: Dict,
        oracle_result: Optional[Dict],
        request: VerificationRequest,
    ) -> Dict:
        """Comprehensive risk assessment"""
        risk_factors = []
        risk_score = 0.0

        # Local verification risk factors
        if local_result.get("confidence", 1.0) < 0.8:
            risk_factors.append("low_local_confidence")
            risk_score += 0.2

        if local_result.get("violations"):
            risk_factors.extend(local_result["violations"])
            risk_score += len(local_result["violations"]) * 0.15

        # Oracle verification risk factors
        if oracle_result:
            oracle_health = oracle_result.get("health_score", 1.0)
            if oracle_health < 0.9:
                risk_factors.append("oracle_health_degraded")
                risk_score += (1.0 - oracle_health) * 0.3

            price_deviation = oracle_result.get("max_deviation", 0.0)
            if price_deviation > 0.02:  # 2% threshold
                risk_factors.append("high_price_deviation")
                risk_score += price_deviation * 0.5

        # Determine risk level
        if risk_score < 0.2:
            risk_level = RiskLevel.LOW
        elif risk_score < 0.5:
            risk_level = RiskLevel.MEDIUM
        elif risk_score < 0.8:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL

        return {
            "risk_score": min(1.0, risk_score),
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "violations": risk_factors,
        }

    async def _validate_compliance(
        self,
        request: VerificationRequest,
        local_result: Dict,
        oracle_result: Optional[Dict],
    ) -> Dict:
        """Validate compliance with regulatory frameworks"""
        compliance_status = {}

        # SOC2 compliance
        compliance_status["SOC2"] = (
            local_result.get("audit_trail", False)
            and request.preserve_privacy
            and (oracle_result is None or oracle_result.get("encrypted", False))
        )

        # ISO27001 compliance
        compliance_status["ISO27001"] = local_result.get("data_integrity", False) and (
            oracle_result is None or oracle_result.get("integrity_verified", False)
        )

        # GDPR compliance (data protection)
        compliance_status["GDPR"] = request.preserve_privacy

        return compliance_status

    def _determine_final_status(
        self,
        local_result: Dict,
        oracle_result: Optional[Dict],
        risk_assessment: Dict,
        compliance_result: Dict,
    ) -> VerificationStatus:
        """Determine final verification status"""
        # Critical risk = automatic failure
        if risk_assessment["risk_level"] == RiskLevel.CRITICAL:
            return VerificationStatus.FAILED

        # Check local verification
        if not local_result.get("valid", False):
            return VerificationStatus.FAILED

        # Check oracle verification (if applicable)
        if oracle_result and not oracle_result.get("valid", False):
            return VerificationStatus.FAILED

        # Check compliance requirements
        required_compliance = all(compliance_result.values())
        if not required_compliance:
            return VerificationStatus.REQUIRES_REVIEW

        # High risk requires review
        if risk_assessment["risk_level"] == RiskLevel.HIGH:
            return VerificationStatus.REQUIRES_REVIEW

        return VerificationStatus.VERIFIED

    def _calculate_confidence_score(
        self, local_result: Dict, oracle_result: Optional[Dict], risk_assessment: Dict
    ) -> float:
        """Calculate overall confidence score"""
        local_confidence = local_result.get("confidence", 0.0)
        oracle_confidence = (
            oracle_result.get("confidence", 1.0) if oracle_result else 1.0
        )
        risk_penalty = risk_assessment["risk_score"] * 0.3

        base_confidence = (local_confidence + oracle_confidence) / 2
        final_confidence = max(0.0, base_confidence - risk_penalty)

        return min(1.0, final_confidence)

    def _generate_recommendations(self, result: VerificationResult) -> List[str]:
        """Generate actionable recommendations based on verification result"""
        recommendations = []

        if result.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append("Implement additional risk controls")
            recommendations.append("Consider manual review before execution")

        if result.oracle_health < 0.9:
            recommendations.append("Verify oracle health before continuing")
            recommendations.append("Consider using additional oracle sources")

        if result.confidence_score < 0.8:
            recommendations.append("Increase verification parameters")
            recommendations.append("Collect additional validation data")

        if result.violations:
            recommendations.append("Address identified violations before proceeding")
            recommendations.append("Review compliance requirements")

        return recommendations

    def _generate_cache_key(self, request: VerificationRequest) -> str:
        """Generate cache key for verification request"""
        cache_data = {
            "type": request.verification_type,
            "data_hash": hashlib.sha256(
                json.dumps(request.data, sort_keys=True).encode()
            ).hexdigest()[:16],
            "timestamp_window": int(request.timestamp // 60),  # 1-minute windows
        }
        return hashlib.sha256(
            json.dumps(cache_data, sort_keys=True).encode()
        ).hexdigest()[:32]

    def _get_cached_result(self, cache_key: str) -> Optional[VerificationResult]:
        """Get cached verification result if valid"""
        if cache_key in self.verification_cache:
            cached_entry = self.verification_cache[cache_key]
            if time.time() - cached_entry["timestamp"] < self.cache_ttl:
                return cached_entry["result"]
            else:
                # Remove expired cache entry
                del self.verification_cache[cache_key]
        return None

    def _cache_result(self, cache_key: str, result: VerificationResult):
        """Cache verification result"""
        self.verification_cache[cache_key] = {
            "result": result,
            "timestamp": time.time(),
        }

        # Basic cache cleanup (remove oldest if too large)
        if len(self.verification_cache) > 10000:
            oldest_key = min(
                self.verification_cache.keys(),
                key=lambda k: self.verification_cache[k]["timestamp"],
            )
            del self.verification_cache[oldest_key]

    def _update_metrics(self, result: VerificationResult, verification_time: float):
        """Update verification metrics"""
        self.metrics["total_verifications"] += 1

        if result.status == VerificationStatus.VERIFIED:
            self.metrics["successful_verifications"] += 1
        else:
            self.metrics["failed_verifications"] += 1

        # Update average latency (exponential moving average)
        alpha = 0.1
        self.metrics["average_latency"] = (
            alpha * (verification_time * 1000)  # Convert to ms
            + (1 - alpha) * self.metrics["average_latency"]
        )

        # Update oracle health score
        self.metrics["oracle_health_score"] = (
            alpha * result.oracle_health
            + (1 - alpha) * self.metrics["oracle_health_score"]
        )

    def get_metrics(self) -> Dict:
        """Get current verification metrics"""
        total = self.metrics["total_verifications"]
        return {
            "total_verifications": total,
            "success_rate": (
                self.metrics["successful_verifications"] / total if total > 0 else 0.0
            ),
            "average_latency_ms": round(self.metrics["average_latency"], 2),
            "oracle_health_score": round(self.metrics["oracle_health_score"], 3),
            "cache_size": len(self.verification_cache),
        }

    async def health_check(self) -> Dict:
        """Comprehensive health check of verification engine"""
        health_status = {
            "verification_engine": "healthy",
            "components": {},
            "performance": {},
            "issues": [],
        }

        try:
            # Check Oracle Manager
            oracle_health = await self.oracle_manager.health_check()
            health_status["components"]["oracle_manager"] = oracle_health

            # Check Local Verifier
            local_health = await self.local_verifier.health_check()
            health_status["components"]["local_verifier"] = local_health

            # Check ZK Generator
            zk_health = await self.zk_generator.health_check()
            health_status["components"]["zk_generator"] = zk_health

            # Performance metrics
            health_status["performance"] = self.get_metrics()

            # Check for issues
            if self.metrics["average_latency"] > 50:  # 50ms threshold
                health_status["issues"].append("high_latency")

            if self.metrics["oracle_health_score"] < 0.9:
                health_status["issues"].append("oracle_degradation")

            success_rate = self.metrics["successful_verifications"] / max(
                1, self.metrics["total_verifications"]
            )
            if success_rate < 0.95:
                health_status["issues"].append("low_success_rate")

            # Overall status
            if health_status["issues"]:
                health_status["verification_engine"] = "degraded"

        except Exception as e:
            health_status["verification_engine"] = "unhealthy"
            health_status["issues"].append(f"health_check_error: {str(e)}")

        return health_status


# Verification engine singleton for application-wide use
_verification_engine_instance = None


def get_verification_engine(config: Optional[Dict] = None) -> VerificationEngine:
    """Get singleton verification engine instance"""
    global _verification_engine_instance
    if _verification_engine_instance is None:
        _verification_engine_instance = VerificationEngine(config)
    return _verification_engine_instance


# Example usage and testing
async def main():
    """Example usage of verification engine"""
    engine = get_verification_engine()

    # Example trading decision verification
    trade_data = {
        "pair": "BTC/USDT",
        "action": "buy",
        "amount": 0.1,
        "price": 43500.0,
        "timestamp": time.time(),
    }

    result = await engine.verify_trading_decision("bot_123", trade_data)
    print(f"Trading verification result: {result.status}")
    print(f"Confidence: {result.confidence_score:.3f}")
    print(f"Risk level: {result.risk_level}")
    print(f"Verification time: {result.local_verification_time:.2f}ms")

    # Example performance verification
    claims = {"roi": 0.15, "win_rate": 0.75}
    actual = {"roi": 0.12, "win_rate": 0.71}

    perf_result = await engine.verify_performance_claims("bot_123", claims, actual)
    print(f"\nPerformance verification: {perf_result.status}")
    print(f"Violations: {perf_result.violations}")

    # Health check
    health = await engine.health_check()
    print(f"\nEngine health: {health['verification_engine']}")
    print(f"Metrics: {engine.get_metrics()}")


if __name__ == "__main__":
    asyncio.run(main())

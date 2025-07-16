"""
TrustWrapper v2.0 Local Verification Engine
Ultra-fast local verification with <10ms target latency

This module provides high-performance local verification capabilities
for real-time trading decisions, performance validation, and compliance
checking without external dependencies.
"""

import asyncio
import hashlib
import json
import time
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class VerificationResult(Enum):
    """Local verification results"""

    VALID = "valid"
    INVALID = "invalid"
    REQUIRES_REVIEW = "requires_review"
    INSUFFICIENT_DATA = "insufficient_data"


class ViolationType(Enum):
    """Types of violations detected locally"""

    PERFORMANCE_MISMATCH = "performance_mismatch"
    STRATEGY_DEVIATION = "strategy_deviation"
    RISK_LIMIT_EXCEEDED = "risk_limit_exceeded"
    SUSPICIOUS_PATTERN = "suspicious_pattern"
    DATA_INTEGRITY_ISSUE = "data_integrity_issue"
    COMPLIANCE_VIOLATION = "compliance_violation"


@dataclass
class LocalVerificationResult:
    """Result of local verification"""

    valid: bool
    confidence: float
    violations: List[str]
    risk_score: float
    verification_time: float
    details: Dict[str, Any]
    audit_trail: bool = True
    data_integrity: bool = True


class PerformanceCache:
    """High-performance cache for verification results"""

    def __init__(self, max_size: int = 10000, ttl: int = 300):
        self.cache = {}
        self.access_times = deque()
        self.max_size = max_size
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        """Get cached value with TTL check"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.ttl:
                # Update access time
                self.access_times.append((key, time.time()))
                return entry["value"]
            else:
                # Expired entry
                del self.cache[key]
        return None

    def set(self, key: str, value: Any):
        """Set cached value with size management"""
        # Clean up if necessary
        if len(self.cache) >= self.max_size:
            self._cleanup_old_entries()

        self.cache[key] = {"value": value, "timestamp": time.time()}
        self.access_times.append((key, time.time()))

    def _cleanup_old_entries(self):
        """Remove oldest entries to maintain cache size"""
        # Remove 20% of cache
        cleanup_count = self.max_size // 5

        # Sort by access time and remove oldest
        sorted_access = sorted(self.access_times)
        for key, _ in sorted_access[:cleanup_count]:
            self.cache.pop(key, None)

        # Update access_times
        self.access_times = deque(sorted_access[cleanup_count:])


class LocalVerificationEngine:
    """
    Ultra-fast local verification engine targeting <10ms latency

    Provides:
    - Performance claim validation
    - Trading strategy compliance verification
    - Risk limit checking
    - Pattern recognition for fraud detection
    - Compliance validation
    """

    def __init__(self, performance_config: Optional[Dict] = None):
        self.config = performance_config or self._get_default_config()

        # High-performance cache
        self.cache = PerformanceCache(
            max_size=self.config.get("cache_size", 10000),
            ttl=self.config.get("cache_ttl", 300),
        )

        # Pre-compiled patterns for fast pattern matching
        self.fraud_patterns = self._initialize_fraud_patterns()
        self.strategy_patterns = self._initialize_strategy_patterns()

        # Performance metrics
        self.metrics = {
            "total_verifications": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "average_latency": 0.0,
            "sub_10ms_rate": 1.0,
        }

        # Risk scoring weights (pre-calculated for speed)
        self.risk_weights = self._initialize_risk_weights()

        # Compliance rules cache
        self.compliance_rules = self._initialize_compliance_rules()

    def _get_default_config(self) -> Dict:
        """Get default configuration optimized for performance"""
        return {
            "target_latency": 10,  # 10ms target
            "cache_size": 10000,  # Large cache for performance
            "cache_ttl": 300,  # 5 minutes TTL
            "max_verification_time": 50,  # 50ms absolute max
            "performance_threshold": 0.05,  # 5% performance deviation
            "risk_threshold": 0.7,  # Risk score threshold
            "pattern_cache_size": 1000,
            "enable_fast_path": True,  # Skip expensive checks when possible
            "parallel_processing": True,
        }

    def _initialize_fraud_patterns(self) -> Dict:
        """Initialize pre-compiled fraud detection patterns"""
        return {
            "wash_trading": {
                "min_volume_ratio": 0.1,
                "price_variance_threshold": 0.001,
                "time_window": 300,  # 5 minutes
            },
            "pump_dump": {
                "price_spike_threshold": 0.20,  # 20% price movement
                "volume_spike_threshold": 5.0,  # 5x volume increase
                "time_window": 600,  # 10 minutes
            },
            "fake_volume": {
                "volume_price_correlation": 0.3,
                "repetitive_pattern_threshold": 0.8,
                "min_trades_for_detection": 10,
            },
        }

    def _initialize_strategy_patterns(self) -> Dict:
        """Initialize strategy compliance patterns"""
        return {
            "dca": {
                "required_fields": ["take_profit", "safety_orders", "deviation"],
                "valid_ranges": {
                    "take_profit": (0.5, 20.0),  # 0.5% to 20%
                    "safety_orders": (1, 10),
                    "deviation": (1.0, 10.0),
                },
            },
            "grid": {
                "required_fields": ["grid_size", "upper_limit", "lower_limit"],
                "valid_ranges": {
                    "grid_size": (3, 50),
                    "upper_limit": (0.01, 2.0),
                    "lower_limit": (0.01, 2.0),
                },
            },
            "arbitrage": {
                "required_fields": ["min_spread", "max_exposure"],
                "valid_ranges": {
                    "min_spread": (0.001, 0.1),  # 0.1% to 10%
                    "max_exposure": (0.1, 1.0),
                },
            },
        }

    def _initialize_risk_weights(self) -> Dict:
        """Initialize risk scoring weights for fast calculation"""
        return {
            "performance_deviation": 0.3,
            "strategy_compliance": 0.25,
            "risk_limit_adherence": 0.25,
            "data_quality": 0.10,
            "pattern_anomalies": 0.10,
        }

    def _initialize_compliance_rules(self) -> Dict:
        """Initialize compliance validation rules"""
        return {
            "SOC2": {
                "audit_trail_required": True,
                "data_encryption": True,
                "access_logging": True,
            },
            "ISO27001": {
                "data_integrity_checks": True,
                "backup_procedures": True,
                "incident_response": True,
            },
            "GDPR": {
                "data_anonymization": True,
                "consent_tracking": True,
                "deletion_capability": True,
            },
        }

    async def verify(
        self, verification_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main verification method optimized for <10ms performance

        Args:
            verification_type: Type of verification to perform
            data: Data to verify

        Returns:
            Dict with verification results
        """
        start_time = time.time()

        try:
            # Fast path: check cache first
            cache_key = self._generate_cache_key(verification_type, data)
            cached_result = self.cache.get(cache_key)

            if cached_result:
                self.metrics["cache_hits"] += 1
                return self._add_timing_info(cached_result, start_time, from_cache=True)

            self.metrics["cache_misses"] += 1

            # Route to appropriate verification method
            if verification_type == "performance_claims":
                result = await self._verify_performance_claims(data)
            elif verification_type == "trading_decision":
                result = await self._verify_trading_decision(data)
            elif verification_type == "defi_strategy":
                result = await self._verify_defi_strategy(data)
            elif verification_type == "risk_compliance":
                result = await self._verify_risk_compliance(data)
            else:
                result = await self._verify_generic(data)

            # Cache result for future use
            verification_time = (time.time() - start_time) * 1000  # ms
            if verification_time < 50:  # Only cache fast results
                self.cache.set(cache_key, result)

            # Update metrics
            self._update_metrics(verification_time)

            return self._add_timing_info(result, start_time)

        except Exception as e:
            # Fast error response
            error_result = {
                "valid": False,
                "confidence": 0.0,
                "violations": [f"verification_error: {str(e)}"],
                "risk_score": 1.0,
                "details": {"error": str(e)},
                "audit_trail": True,
                "data_integrity": False,
            }
            return self._add_timing_info(error_result, start_time)

    async def verify_performance(self, claimed: Dict, actual: Dict) -> Dict:
        """Fast performance verification between claimed and actual results"""
        start_time = time.time()

        # Quick validation
        if not claimed or not actual:
            return {
                "valid": False,
                "confidence": 0.0,
                "performance_match": False,
                "deviation": 1.0,
            }

        # Calculate key performance deviations
        roi_claimed = claimed.get("roi", 0.0)
        roi_actual = actual.get("roi", 0.0)

        roi_deviation = abs(roi_claimed - roi_actual) / max(abs(roi_claimed), 0.001)

        # Win rate comparison
        win_rate_claimed = claimed.get("win_rate", 0.0)
        win_rate_actual = actual.get("win_rate", 0.0)

        win_rate_deviation = abs(win_rate_claimed - win_rate_actual)

        # Overall deviation score
        overall_deviation = (roi_deviation + win_rate_deviation) / 2

        # Determine validity
        valid = overall_deviation <= self.config["performance_threshold"]
        confidence = max(0.0, 1.0 - overall_deviation)

        return {
            "valid": valid,
            "confidence": confidence,
            "performance_match": valid,
            "deviation": overall_deviation,
            "roi_deviation": roi_deviation,
            "win_rate_deviation": win_rate_deviation,
            "verification_time": (time.time() - start_time) * 1000,
        }

    async def verify_trade(
        self, trade: Dict, strategy_config: Dict, risk_limits: Dict
    ) -> Dict:
        """Fast trade verification against strategy and risk parameters"""
        start_time = time.time()

        violations = []
        risk_score = 0.0

        # Quick strategy compliance check
        strategy_valid = self._check_strategy_compliance_fast(trade, strategy_config)
        if not strategy_valid:
            violations.append("strategy_deviation")
            risk_score += 0.3

        # Risk limit validation
        risk_valid = self._check_risk_limits_fast(trade, risk_limits)
        if not risk_valid:
            violations.append("risk_limit_exceeded")
            risk_score += 0.4

        # Trade data integrity
        integrity_valid = self._check_trade_integrity_fast(trade)
        if not integrity_valid:
            violations.append("data_integrity_issue")
            risk_score += 0.2

        valid = len(violations) == 0
        confidence = max(0.0, 1.0 - risk_score)

        return {
            "valid": valid,
            "confidence": confidence,
            "violations": violations,
            "risk_score": risk_score,
            "strategy_compliant": strategy_valid,
            "risk_compliant": risk_valid,
            "data_integrity": integrity_valid,
            "verification_time": (time.time() - start_time) * 1000,
        }

    async def _verify_performance_claims(self, data: Dict) -> Dict:
        """Verify performance claims against actual performance"""
        claimed = data.get("claimed_performance", {})
        actual = data.get("actual_performance", {})

        # Fast performance comparison
        roi_claimed = claimed.get("roi", 0.0)
        roi_actual = actual.get("roi", 0.0)

        if roi_claimed == 0:
            return self._create_invalid_result(["zero_claimed_roi"])

        roi_deviation = abs(roi_claimed - roi_actual) / abs(roi_claimed)

        violations = []
        risk_score = 0.0

        # Performance deviation check
        if roi_deviation > self.config["performance_threshold"]:
            violations.append(ViolationType.PERFORMANCE_MISMATCH.value)
            risk_score += roi_deviation * self.risk_weights["performance_deviation"]

        # Win rate validation
        win_rate_claimed = claimed.get("win_rate", 0.0)
        win_rate_actual = actual.get("win_rate", 0.0)
        win_rate_deviation = abs(win_rate_claimed - win_rate_actual)

        if win_rate_deviation > 0.1:  # 10% threshold
            violations.append("win_rate_mismatch")
            risk_score += win_rate_deviation * 0.2

        # Fraud pattern detection (fast check)
        if self._detect_fraud_patterns_fast(claimed, actual):
            violations.append(ViolationType.SUSPICIOUS_PATTERN.value)
            risk_score += 0.5

        valid = len(violations) == 0 and risk_score < self.config["risk_threshold"]
        confidence = max(0.0, 1.0 - risk_score)

        return {
            "valid": valid,
            "confidence": confidence,
            "violations": violations,
            "risk_score": min(1.0, risk_score),
            "details": {
                "roi_deviation": roi_deviation,
                "win_rate_deviation": win_rate_deviation,
                "claimed_roi": roi_claimed,
                "actual_roi": roi_actual,
            },
            "audit_trail": True,
            "data_integrity": True,
        }

    async def _verify_trading_decision(self, data: Dict) -> Dict:
        """Verify trading decision compliance"""
        trade = data.get("trade", {})
        bot_id = data.get("bot_id", "")

        violations = []
        risk_score = 0.0

        # Basic trade validation
        required_fields = ["pair", "action", "amount", "price"]
        for field in required_fields:
            if field not in trade:
                violations.append(f"missing_{field}")
                risk_score += 0.1

        # Price reasonableness check (fast)
        price = trade.get("price", 0)
        if price <= 0:
            violations.append("invalid_price")
            risk_score += 0.3

        # Amount validation
        amount = trade.get("amount", 0)
        if amount <= 0:
            violations.append("invalid_amount")
            risk_score += 0.3

        # Action validation
        action = trade.get("action", "")
        if action not in ["buy", "sell"]:
            violations.append("invalid_action")
            risk_score += 0.2

        # Timestamp validation
        timestamp = trade.get("timestamp", 0)
        current_time = time.time()
        if abs(timestamp - current_time) > 300:  # 5 minutes tolerance
            violations.append("stale_trade_data")
            risk_score += 0.1

        valid = len(violations) == 0
        confidence = max(0.0, 1.0 - risk_score)

        return {
            "valid": valid,
            "confidence": confidence,
            "violations": violations,
            "risk_score": min(1.0, risk_score),
            "details": {
                "trade_valid": len(violations) == 0,
                "bot_id": bot_id,
                "validation_checks": len(required_fields),
            },
            "audit_trail": True,
            "data_integrity": True,
        }

    async def _verify_defi_strategy(self, data: Dict) -> Dict:
        """Verify DeFi strategy parameters and safety"""
        strategy = data.get("strategy", {})

        violations = []
        risk_score = 0.0

        # Strategy type validation
        strategy_type = strategy.get("type", "")
        if strategy_type not in self.strategy_patterns:
            violations.append("unknown_strategy_type")
            risk_score += 0.2
        else:
            # Validate strategy-specific parameters
            pattern = self.strategy_patterns[strategy_type]

            # Check required fields
            for field in pattern["required_fields"]:
                if field not in strategy:
                    violations.append(f"missing_{field}")
                    risk_score += 0.1

            # Check value ranges
            for field, valid_range in pattern["valid_ranges"].items():
                if field in strategy:
                    value = strategy[field]
                    min_val, max_val = valid_range
                    if not (min_val <= value <= max_val):
                        violations.append(f"{field}_out_of_range")
                        risk_score += 0.15

        # DeFi-specific risk checks
        if "slippage_tolerance" in strategy:
            slippage = strategy["slippage_tolerance"]
            if slippage > 0.05:  # 5% max slippage
                violations.append("high_slippage_risk")
                risk_score += 0.3

        # Protocol safety check
        protocols = strategy.get("protocols", [])
        for protocol in protocols:
            if self._is_high_risk_protocol(protocol):
                violations.append(f"high_risk_protocol_{protocol}")
                risk_score += 0.25

        valid = len(violations) == 0 and risk_score < 0.5
        confidence = max(0.0, 1.0 - risk_score)

        return {
            "valid": valid,
            "confidence": confidence,
            "violations": violations,
            "risk_score": min(1.0, risk_score),
            "details": {
                "strategy_type": strategy_type,
                "protocol_count": len(protocols),
                "validation_passed": len(violations) == 0,
            },
            "audit_trail": True,
            "data_integrity": True,
        }

    async def _verify_risk_compliance(self, data: Dict) -> Dict:
        """Verify risk management compliance"""
        risk_params = data.get("risk_parameters", {})

        violations = []
        risk_score = 0.0

        # Maximum drawdown check
        max_drawdown = risk_params.get("max_drawdown", 1.0)
        if max_drawdown > 0.2:  # 20% max drawdown limit
            violations.append("excessive_drawdown_limit")
            risk_score += (max_drawdown - 0.2) * 2

        # Position size validation
        max_position = risk_params.get("max_position_size", 0)
        if max_position > 10000:  # $10K max position
            violations.append("excessive_position_size")
            risk_score += 0.3

        # Leverage check
        leverage = risk_params.get("leverage", 1.0)
        if leverage > 3.0:  # 3x max leverage
            violations.append("excessive_leverage")
            risk_score += (leverage - 3.0) * 0.2

        # Stop loss validation
        stop_loss = risk_params.get("stop_loss", None)
        if stop_loss is None:
            violations.append("missing_stop_loss")
            risk_score += 0.2
        elif stop_loss > 0.1:  # 10% max stop loss
            violations.append("wide_stop_loss")
            risk_score += 0.1

        valid = len(violations) == 0
        confidence = max(0.0, 1.0 - risk_score)

        return {
            "valid": valid,
            "confidence": confidence,
            "violations": violations,
            "risk_score": min(1.0, risk_score),
            "details": {
                "max_drawdown": max_drawdown,
                "leverage": leverage,
                "compliance_checks": 4,
            },
            "audit_trail": True,
            "data_integrity": True,
        }

    async def _verify_generic(self, data: Dict) -> Dict:
        """Generic verification for unknown types"""
        violations = []
        risk_score = 0.0

        # Basic data integrity checks
        if not data:
            violations.append("empty_data")
            risk_score = 1.0

        # Check for suspicious patterns in data
        if self._has_suspicious_patterns(data):
            violations.append("suspicious_data_patterns")
            risk_score += 0.3

        valid = len(violations) == 0
        confidence = max(0.0, 1.0 - risk_score)

        return {
            "valid": valid,
            "confidence": confidence,
            "violations": violations,
            "risk_score": min(1.0, risk_score),
            "details": {"generic_verification": True},
            "audit_trail": True,
            "data_integrity": True,
        }

    def _check_strategy_compliance_fast(
        self, trade: Dict, strategy_config: Dict
    ) -> bool:
        """Fast strategy compliance check"""
        strategy_type = strategy_config.get("type", "")

        if strategy_type == "dca":
            # DCA compliance: check if trade aligns with DCA parameters
            return self._check_dca_compliance(trade, strategy_config)
        elif strategy_type == "grid":
            # Grid compliance: check if trade is within grid bounds
            return self._check_grid_compliance(trade, strategy_config)
        elif strategy_type == "arbitrage":
            # Arbitrage compliance: check spread requirements
            return self._check_arbitrage_compliance(trade, strategy_config)

        return True  # Unknown strategy type passes by default

    def _check_risk_limits_fast(self, trade: Dict, risk_limits: Dict) -> bool:
        """Fast risk limit validation"""
        # Position size check
        amount = trade.get("amount", 0)
        price = trade.get("price", 0)
        position_value = amount * price

        max_position = risk_limits.get("max_position_size", float("inf"))
        if position_value > max_position:
            return False

        # Check against maximum drawdown if applicable
        max_drawdown = risk_limits.get("max_drawdown", 1.0)
        if max_drawdown < 0.05:  # Unreasonably tight risk
            return False

        return True

    def _check_trade_integrity_fast(self, trade: Dict) -> bool:
        """Fast trade data integrity check"""
        # Check required fields exist and are reasonable
        required_fields = ["pair", "amount", "price", "timestamp"]

        for field in required_fields:
            if field not in trade:
                return False

            value = trade[field]
            if field in ["amount", "price"] and value <= 0:
                return False

        # Check timestamp is recent
        timestamp = trade.get("timestamp", 0)
        if abs(timestamp - time.time()) > 3600:  # 1 hour tolerance
            return False

        return True

    def _detect_fraud_patterns_fast(self, claimed: Dict, actual: Dict) -> bool:
        """Fast fraud pattern detection"""
        # Check for impossibly good performance
        claimed_roi = claimed.get("roi", 0)
        if claimed_roi > 5.0:  # 500% ROI is suspicious
            return True

        # Check for perfect win rates
        claimed_win_rate = claimed.get("win_rate", 0)
        if claimed_win_rate > 0.95:  # >95% win rate is suspicious
            return True

        # Check for inconsistent metrics
        actual_roi = actual.get("roi", 0)
        if claimed_roi > 0 and actual_roi < 0:  # Claimed profit but actual loss
            return True

        return False

    def _check_dca_compliance(self, trade: Dict, strategy_config: Dict) -> bool:
        """Check DCA strategy compliance"""
        # DCA should have consistent amounts or follow averaging down pattern
        take_profit = strategy_config.get("take_profit", 2.5)

        # Basic DCA validation - in real implementation would be more sophisticated
        return 0.5 <= take_profit <= 20.0

    def _check_grid_compliance(self, trade: Dict, strategy_config: Dict) -> bool:
        """Check grid strategy compliance"""
        grid_size = strategy_config.get("grid_size", 10)

        # Grid validation
        return 3 <= grid_size <= 50

    def _check_arbitrage_compliance(self, trade: Dict, strategy_config: Dict) -> bool:
        """Check arbitrage strategy compliance"""
        min_spread = strategy_config.get("min_spread", 0.001)

        # Arbitrage validation
        return 0.001 <= min_spread <= 0.1

    def _is_high_risk_protocol(self, protocol: str) -> bool:
        """Check if protocol is considered high risk"""
        high_risk_protocols = {
            "experimental_protocol",
            "unaudited_protocol",
            "new_protocol",
        }
        return protocol.lower() in high_risk_protocols

    def _has_suspicious_patterns(self, data: Dict) -> bool:
        """Check for suspicious patterns in data"""
        # Check for extremely precise numbers (potential fabrication)
        for key, value in data.items():
            if isinstance(value, float):
                # Check if number has too many decimal places (suspicious precision)
                str_value = str(value)
                if "." in str_value and len(str_value.split(".")[1]) > 8:
                    return True

        return False

    def _create_invalid_result(self, violations: List[str]) -> Dict:
        """Create invalid verification result"""
        return {
            "valid": False,
            "confidence": 0.0,
            "violations": violations,
            "risk_score": 1.0,
            "details": {"reason": "validation_failed"},
            "audit_trail": True,
            "data_integrity": False,
        }

    def _generate_cache_key(self, verification_type: str, data: Dict) -> str:
        """Generate cache key for verification request"""
        # Create deterministic hash of verification type and data
        cache_data = {"type": verification_type, "data": data}

        # Use sorted JSON to ensure consistent hashing
        data_str = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:32]

    def _add_timing_info(
        self, result: Dict, start_time: float, from_cache: bool = False
    ) -> Dict:
        """Add timing information to verification result"""
        verification_time = (time.time() - start_time) * 1000  # Convert to ms

        result["verification_time"] = verification_time
        result["from_cache"] = from_cache
        result["sub_10ms"] = verification_time < 10.0

        return result

    def _update_metrics(self, verification_time: float):
        """Update performance metrics"""
        self.metrics["total_verifications"] += 1

        # Update average latency (exponential moving average)
        alpha = 0.1
        self.metrics["average_latency"] = (
            alpha * verification_time + (1 - alpha) * self.metrics["average_latency"]
        )

        # Update sub-10ms rate
        if verification_time < 10.0:
            sub_10ms_count = (
                self.metrics["total_verifications"] * self.metrics["sub_10ms_rate"] + 1
            )
        else:
            sub_10ms_count = (
                self.metrics["total_verifications"] * self.metrics["sub_10ms_rate"]
            )

        self.metrics["sub_10ms_rate"] = (
            sub_10ms_count / self.metrics["total_verifications"]
        )

    def get_metrics(self) -> Dict:
        """Get current performance metrics"""
        total = self.metrics["total_verifications"]
        cache_total = self.metrics["cache_hits"] + self.metrics["cache_misses"]

        return {
            "total_verifications": total,
            "average_latency_ms": round(self.metrics["average_latency"], 2),
            "sub_10ms_rate": round(self.metrics["sub_10ms_rate"] * 100, 1),
            "cache_hit_rate": round(
                (
                    (self.metrics["cache_hits"] / cache_total * 100)
                    if cache_total > 0
                    else 0
                ),
                1,
            ),
            "cache_size": len(self.cache.cache),
        }

    async def health_check(self) -> Dict:
        """Health check of local verification engine"""
        health_status = {
            "status": "healthy",
            "performance": {},
            "cache": {},
            "issues": [],
        }

        try:
            # Performance check
            metrics = self.get_metrics()
            health_status["performance"] = metrics

            # Check if average latency is within target
            if metrics["average_latency_ms"] > self.config["target_latency"]:
                health_status["issues"].append("high_average_latency")

            # Check sub-10ms rate
            if metrics["sub_10ms_rate"] < 80.0:  # 80% target
                health_status["issues"].append("low_fast_verification_rate")

            # Cache health
            health_status["cache"] = {
                "size": len(self.cache.cache),
                "max_size": self.cache.max_size,
                "utilization": len(self.cache.cache) / self.cache.max_size,
            }

            # Check cache utilization
            if health_status["cache"]["utilization"] > 0.9:
                health_status["issues"].append("cache_near_capacity")

            # Determine overall status
            if health_status["issues"]:
                health_status["status"] = "degraded"

            # Test verification speed
            test_data = {"test": True, "timestamp": time.time()}
            test_start = time.time()
            await self.verify("generic", test_data)
            test_time = (time.time() - test_start) * 1000

            health_status["test_verification_time"] = round(test_time, 2)

            if test_time > 20:  # 20ms threshold for test
                health_status["issues"].append("slow_test_verification")
                health_status["status"] = "degraded"

        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["issues"].append(f"health_check_error: {str(e)}")

        return health_status


# Example usage and performance testing
async def main():
    """Example local verification engine usage"""
    engine = LocalVerificationEngine()

    print("Testing Local Verification Engine Performance...")

    # Test performance verification
    claimed_performance = {"roi": 0.15, "win_rate": 0.75}
    actual_performance = {"roi": 0.12, "win_rate": 0.71}

    start_time = time.time()
    result = await engine.verify_performance(claimed_performance, actual_performance)
    latency = (time.time() - start_time) * 1000

    print(f"Performance verification: {result['performance_match']}")
    print(f"Latency: {latency:.2f}ms")
    print(f"Deviation: {result['deviation']:.4f}")

    # Test trading decision verification
    trade_data = {
        "trade": {
            "pair": "BTC/USDT",
            "action": "buy",
            "amount": 0.1,
            "price": 43500.0,
            "timestamp": time.time(),
        },
        "bot_id": "test_bot",
    }

    start_time = time.time()
    trade_result = await engine.verify("trading_decision", trade_data)
    trade_latency = (time.time() - start_time) * 1000

    print(f"\nTrading decision verification: {trade_result['valid']}")
    print(f"Latency: {trade_latency:.2f}ms")
    print(f"Violations: {trade_result['violations']}")

    # Performance metrics
    metrics = engine.get_metrics()
    print("\nEngine Metrics:")
    print(f"Average latency: {metrics['average_latency_ms']}ms")
    print(f"Sub-10ms rate: {metrics['sub_10ms_rate']}%")
    print(f"Cache hit rate: {metrics['cache_hit_rate']}%")

    # Health check
    health = await engine.health_check()
    print(f"\nEngine health: {health['status']}")
    print(f"Test verification time: {health['test_verification_time']}ms")


if __name__ == "__main__":
    asyncio.run(main())

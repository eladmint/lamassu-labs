#!/usr/bin/env python3
"""
TrustWrapper v2.0 Oracle Integration Layer
Connects real-time oracle feeds to TrustWrapper verification system
"""

import asyncio
import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from .realtime_oracle_engine import (
    OracleConsensus,
    OraclePrice,
    get_oracle_engine,
)


@dataclass
class VerificationContext:
    """Context for TrustWrapper verification with oracle data"""

    symbol: str
    current_price: float
    consensus_data: OracleConsensus
    price_history: List[OraclePrice]
    market_conditions: Dict[str, Any]
    risk_factors: List[str]
    confidence_score: float
    timestamp: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OracleVerificationResult:
    """Result of oracle-based verification"""

    verified: bool
    confidence: float
    risk_score: float
    market_context: Dict[str, Any]
    oracle_consensus: OracleConsensus
    anomalies_detected: List[str]
    verification_time_ms: float
    xai_explanation: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TrustWrapperOracleIntegration:
    """
    Integration layer between TrustWrapper and real-time oracle system
    Provides oracle-enhanced verification with XAI explanations
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        # Oracle engine
        self.oracle_engine = None

        # Verification history
        self.verification_history = []

        # Risk models
        self.risk_models = {
            "volatility_threshold": 0.1,  # 10%
            "volume_spike_threshold": 3.0,  # 3x normal
            "price_deviation_threshold": 0.05,  # 5%
            "confidence_floor": 0.7,  # 70%
            "consensus_requirement": 0.8,  # 80%
        }

        # Market condition classifiers
        self.market_classifiers = {
            "high_volatility": lambda ctx: ctx.consensus_data.price_deviation > 0.1,
            "low_liquidity": lambda ctx: self._check_low_liquidity(ctx),
            "price_manipulation": lambda ctx: self._check_manipulation_signals(ctx),
            "oracle_divergence": lambda ctx: ctx.consensus_data.confidence_score < 0.8,
            "stale_data": lambda ctx: self._check_stale_data(ctx),
        }

    def _get_default_config(self) -> Dict:
        """Default configuration for oracle integration"""
        return {
            "verification_timeout": 30.0,  # seconds
            "max_price_age": 60.0,  # seconds
            "min_consensus_sources": 3,
            "risk_assessment_depth": "full",  # basic, standard, full
            "enable_xai_explanations": True,
            "cache_verification_results": True,
            "anomaly_detection_sensitivity": "medium",  # low, medium, high
            "market_condition_monitoring": True,
        }

    async def initialize(self):
        """Initialize the oracle integration"""
        self.logger.info("🔧 Initializing TrustWrapper Oracle Integration...")

        # Get oracle engine instance with shared configuration
        self.oracle_engine = await get_oracle_engine()

        # Subscribe to oracle updates
        self.oracle_engine.subscribe(self._on_oracle_update)

        # Start oracle engine if not running
        if not self.oracle_engine.running:
            # Start in background task
            asyncio.create_task(self.oracle_engine.start())

        self.logger.info("✅ TrustWrapper Oracle Integration initialized")

    async def verify_with_oracle_context(
        self,
        ai_decision: Dict[str, Any],
        symbol: str,
        verification_type: str = "trading_decision",
    ) -> OracleVerificationResult:
        """
        Verify AI decision with real-time oracle context
        Returns enhanced verification with market context and XAI explanation
        """
        start_time = time.time()

        try:
            # Get oracle context
            context = await self._build_verification_context(symbol)
            if not context:
                raise Exception(f"Unable to build oracle context for {symbol}")

            # Perform oracle-enhanced verification
            verification_result = await self._perform_oracle_verification(
                ai_decision, context, verification_type
            )

            # Add XAI explanation if enabled
            if self.config.get("enable_xai_explanations", True):
                verification_result.xai_explanation = (
                    await self._generate_xai_explanation(
                        ai_decision, context, verification_result
                    )
                )

            # Store in history
            if self.config.get("cache_verification_results", True):
                self.verification_history.append(
                    {
                        "timestamp": time.time(),
                        "symbol": symbol,
                        "verification_type": verification_type,
                        "result": verification_result.to_dict(),
                    }
                )

                # Keep only recent history
                cutoff_time = time.time() - 3600  # 1 hour
                self.verification_history = [
                    h
                    for h in self.verification_history
                    if h["timestamp"] >= cutoff_time
                ]

            verification_time = (time.time() - start_time) * 1000
            verification_result.verification_time_ms = verification_time

            self.logger.info(
                f"✅ Oracle verification complete: {symbol} "
                f"{'VERIFIED' if verification_result.verified else 'REJECTED'} "
                f"({verification_time:.1f}ms)"
            )

            return verification_result

        except Exception as e:
            verification_time = (time.time() - start_time) * 1000
            self.logger.error(f"❌ Oracle verification failed: {e}")

            # Return failure result
            return OracleVerificationResult(
                verified=False,
                confidence=0.0,
                risk_score=1.0,
                market_context={"error": str(e)},
                oracle_consensus=None,
                anomalies_detected=[f"verification_error: {str(e)}"],
                verification_time_ms=verification_time,
            )

    async def _build_verification_context(
        self, symbol: str
    ) -> Optional[VerificationContext]:
        """Build comprehensive verification context from oracle data"""
        try:
            # Get current consensus
            consensus = await self.oracle_engine.get_consensus(symbol)
            if not consensus:
                self.logger.warning(f"No consensus available for {symbol}")
                return None

            # Get current price
            current_price_data = await self.oracle_engine.get_current_price(symbol)
            current_price = (
                current_price_data.price
                if current_price_data
                else consensus.consensus_price
            )

            # Get price history
            price_history = await self.oracle_engine.get_price_history(
                symbol, 3600
            )  # 1 hour

            # Analyze market conditions
            market_conditions = await self._analyze_market_conditions(
                consensus, price_history
            )

            # Detect risk factors
            risk_factors = await self._detect_risk_factors(
                consensus, price_history, market_conditions
            )

            # Calculate overall confidence
            confidence_score = self._calculate_context_confidence(
                consensus, market_conditions, risk_factors
            )

            return VerificationContext(
                symbol=symbol,
                current_price=current_price,
                consensus_data=consensus,
                price_history=price_history,
                market_conditions=market_conditions,
                risk_factors=risk_factors,
                confidence_score=confidence_score,
                timestamp=time.time(),
            )

        except Exception as e:
            self.logger.error(f"Error building verification context: {e}")
            return None

    async def _analyze_market_conditions(
        self, consensus: OracleConsensus, price_history: List[OraclePrice]
    ) -> Dict[str, Any]:
        """Analyze current market conditions"""
        conditions = {}

        # Price volatility analysis
        if len(price_history) > 10:
            prices = [p.price for p in price_history]
            price_changes = [
                abs(prices[i] - prices[i - 1]) / prices[i - 1]
                for i in range(1, len(prices))
            ]
            conditions["volatility"] = {
                "avg_change": sum(price_changes) / len(price_changes),
                "max_change": max(price_changes),
                "volatility_score": min(
                    1.0, sum(price_changes) / len(price_changes) * 10
                ),
            }

        # Oracle consensus quality
        conditions["consensus_quality"] = {
            "source_count": consensus.source_count,
            "price_deviation": consensus.price_deviation,
            "confidence_score": consensus.confidence_score,
            "consensus_strength": (
                "strong"
                if consensus.confidence_score > 0.9
                else "medium" if consensus.confidence_score > 0.7 else "weak"
            ),
        }

        # Volume analysis
        recent_volumes = [p.volume_24h for p in price_history if p.volume_24h]
        if recent_volumes:
            avg_volume = sum(recent_volumes) / len(recent_volumes)
            latest_volume = recent_volumes[-1] if recent_volumes else 0
            conditions["volume_analysis"] = {
                "avg_volume": avg_volume,
                "latest_volume": latest_volume,
                "volume_ratio": latest_volume / avg_volume if avg_volume > 0 else 1.0,
            }

        # Market classification
        conditions["market_state"] = self._classify_market_state(
            consensus, price_history
        )

        return conditions

    def _classify_market_state(
        self, consensus: OracleConsensus, price_history: List[OraclePrice]
    ) -> str:
        """Classify current market state"""
        if consensus.price_deviation > 0.1:
            return "high_volatility"
        elif consensus.confidence_score < 0.7:
            return "uncertain"
        elif len(price_history) > 5:
            recent_prices = [p.price for p in price_history[-5:]]
            if recent_prices[-1] > recent_prices[0] * 1.05:
                return "bullish"
            elif recent_prices[-1] < recent_prices[0] * 0.95:
                return "bearish"

        return "stable"

    async def _detect_risk_factors(
        self,
        consensus: OracleConsensus,
        price_history: List[OraclePrice],
        market_conditions: Dict[str, Any],
    ) -> List[str]:
        """Detect risk factors from oracle data"""
        risk_factors = []

        # High price deviation
        if consensus.price_deviation > self.risk_models["price_deviation_threshold"]:
            risk_factors.append(f"high_price_deviation:{consensus.price_deviation:.3f}")

        # Low confidence
        if consensus.confidence_score < self.risk_models["confidence_floor"]:
            risk_factors.append(
                f"low_oracle_confidence:{consensus.confidence_score:.3f}"
            )

        # Insufficient sources
        if consensus.source_count < self.config["min_consensus_sources"]:
            risk_factors.append(f"insufficient_sources:{consensus.source_count}")

        # Volatility check
        volatility = market_conditions.get("volatility", {})
        if (
            volatility.get("volatility_score", 0)
            > self.risk_models["volatility_threshold"]
        ):
            risk_factors.append(
                f"high_volatility:{volatility.get('volatility_score', 0):.3f}"
            )

        # Volume anomaly
        volume_analysis = market_conditions.get("volume_analysis", {})
        volume_ratio = volume_analysis.get("volume_ratio", 1.0)
        if volume_ratio > self.risk_models["volume_spike_threshold"]:
            risk_factors.append(f"volume_spike:{volume_ratio:.2f}x")

        # Stale data
        data_age = time.time() - consensus.timestamp
        if data_age > self.config["max_price_age"]:
            risk_factors.append(f"stale_data:{data_age:.0f}s")

        return risk_factors

    def _calculate_context_confidence(
        self,
        consensus: OracleConsensus,
        market_conditions: Dict[str, Any],
        risk_factors: List[str],
    ) -> float:
        """Calculate overall confidence in the verification context"""
        base_confidence = consensus.confidence_score

        # Penalty for risk factors
        risk_penalty = len(risk_factors) * 0.05  # 5% per risk factor

        # Adjust for market conditions
        market_state = market_conditions.get("market_state", "stable")
        state_adjustments = {
            "stable": 0.0,
            "bullish": 0.02,
            "bearish": 0.02,
            "high_volatility": -0.1,
            "uncertain": -0.15,
        }
        state_adjustment = state_adjustments.get(market_state, 0.0)

        # Adjust for consensus quality
        consensus_quality = market_conditions.get("consensus_quality", {})
        consensus_adjustment = 0.0
        if consensus_quality.get("consensus_strength") == "strong":
            consensus_adjustment = 0.05
        elif consensus_quality.get("consensus_strength") == "weak":
            consensus_adjustment = -0.1

        # Calculate final confidence
        final_confidence = (
            base_confidence - risk_penalty + state_adjustment + consensus_adjustment
        )

        return max(0.0, min(1.0, final_confidence))

    async def _perform_oracle_verification(
        self,
        ai_decision: Dict[str, Any],
        context: VerificationContext,
        verification_type: str,
    ) -> OracleVerificationResult:
        """Perform oracle-enhanced verification of AI decision"""

        # Extract decision details
        predicted_price = ai_decision.get("predicted_price")
        confidence = ai_decision.get("confidence", 0.5)
        action = ai_decision.get("action", "hold")
        reasoning = ai_decision.get("reasoning", "")

        # Initialize verification
        verified = True
        risk_score = 0.0
        anomalies = []

        # Verify against current oracle data
        current_price = context.current_price
        price_deviation = (
            abs(predicted_price - current_price) / current_price
            if predicted_price
            else 0
        )

        # Price prediction verification
        if predicted_price:
            if price_deviation > 0.1:  # 10% deviation threshold
                verified = False
                risk_score += 0.3
                anomalies.append(f"large_price_deviation:{price_deviation:.3f}")

        # Confidence verification
        if confidence < 0.6:
            risk_score += 0.2
            anomalies.append(f"low_ai_confidence:{confidence:.3f}")

        # Market context verification
        market_state = context.market_conditions.get("market_state", "stable")
        if market_state == "high_volatility" and action in ["buy", "sell"]:
            risk_score += 0.2
            anomalies.append("trading_in_high_volatility")

        # Oracle consensus verification
        if context.consensus_data.confidence_score < 0.7:
            verified = False
            risk_score += 0.3
            anomalies.append(
                f"poor_oracle_consensus:{context.consensus_data.confidence_score:.3f}"
            )

        # Risk factor verification
        if len(context.risk_factors) > 3:
            verified = False
            risk_score += 0.2
            anomalies.extend(context.risk_factors[:3])  # Include top 3 risk factors

        # Final verification decision
        final_confidence = context.confidence_score * (1.0 - risk_score) * confidence
        if final_confidence < 0.5:
            verified = False

        return OracleVerificationResult(
            verified=verified,
            confidence=final_confidence,
            risk_score=min(1.0, risk_score),
            market_context=context.market_conditions,
            oracle_consensus=context.consensus_data,
            anomalies_detected=anomalies,
            verification_time_ms=0.0,  # Will be set by caller
        )

    async def _generate_xai_explanation(
        self,
        ai_decision: Dict[str, Any],
        context: VerificationContext,
        verification_result: OracleVerificationResult,
    ) -> Dict[str, Any]:
        """Generate XAI explanation for the verification decision"""

        explanation = {
            "verification_decision": (
                "VERIFIED" if verification_result.verified else "REJECTED"
            ),
            "confidence_breakdown": {
                "ai_confidence": ai_decision.get("confidence", 0.5),
                "oracle_consensus": context.consensus_data.confidence_score,
                "market_context": context.confidence_score,
                "final_confidence": verification_result.confidence,
            },
            "key_factors": [],
            "risk_assessment": {
                "risk_score": verification_result.risk_score,
                "risk_factors": context.risk_factors,
                "anomalies": verification_result.anomalies_detected,
            },
            "market_analysis": {
                "current_price": context.current_price,
                "price_sources": context.consensus_data.sources,
                "market_state": context.market_conditions.get(
                    "market_state", "unknown"
                ),
                "volatility": context.market_conditions.get("volatility", {}).get(
                    "volatility_score", 0
                ),
            },
            "reasoning": self._generate_human_readable_explanation(
                ai_decision, context, verification_result
            ),
        }

        # Add key factors that influenced the decision
        if verification_result.verified:
            explanation["key_factors"].extend(
                [
                    f"Oracle consensus from {context.consensus_data.source_count} sources",
                    f"Price deviation within acceptable range ({context.consensus_data.price_deviation:.2%})",
                    f"Market conditions: {context.market_conditions.get('market_state', 'stable')}",
                ]
            )
        else:
            explanation["key_factors"].extend(
                [
                    f"Risk factors detected: {len(context.risk_factors)}",
                    f"Anomalies found: {len(verification_result.anomalies_detected)}",
                    f"Low confidence score: {verification_result.confidence:.2%}",
                ]
            )

        return explanation

    def _generate_human_readable_explanation(
        self,
        ai_decision: Dict[str, Any],
        context: VerificationContext,
        verification_result: OracleVerificationResult,
    ) -> str:
        """Generate human-readable explanation"""

        decision = "VERIFIED" if verification_result.verified else "REJECTED"
        symbol = context.symbol
        price = context.current_price
        sources = context.consensus_data.source_count
        confidence = verification_result.confidence

        if verification_result.verified:
            return (
                f"AI decision for {symbol} was {decision} with {confidence:.1%} confidence. "
                f"Current price ${price:,.2f} is supported by consensus from {sources} oracle sources "
                f"with {context.consensus_data.price_deviation:.2%} deviation. "
                f"Market conditions are {context.market_conditions.get('market_state', 'stable')} "
                f"with minimal risk factors detected."
            )
        else:
            risk_count = len(context.risk_factors)
            anomaly_count = len(verification_result.anomalies_detected)
            return (
                f"AI decision for {symbol} was {decision} due to {confidence:.1%} confidence. "
                f"Verification failed with {risk_count} risk factors and {anomaly_count} anomalies. "
                f"Oracle consensus from {sources} sources shows {context.consensus_data.price_deviation:.2%} deviation "
                f"which exceeds safety thresholds. Market state: {context.market_conditions.get('market_state', 'uncertain')}."
            )

    def _check_low_liquidity(self, context: VerificationContext) -> bool:
        """Check for low liquidity conditions"""
        volume_analysis = context.market_conditions.get("volume_analysis", {})
        volume_ratio = volume_analysis.get("volume_ratio", 1.0)
        return volume_ratio < 0.5  # 50% below average

    def _check_manipulation_signals(self, context: VerificationContext) -> bool:
        """Check for potential price manipulation signals"""
        # Simple heuristic: high price deviation with low volume
        high_deviation = context.consensus_data.price_deviation > 0.1
        volume_analysis = context.market_conditions.get("volume_analysis", {})
        low_volume = volume_analysis.get("volume_ratio", 1.0) < 0.7
        return high_deviation and low_volume

    def _check_stale_data(self, context: VerificationContext) -> bool:
        """Check for stale oracle data"""
        data_age = time.time() - context.consensus_data.timestamp
        return data_age > self.config["max_price_age"]

    async def _on_oracle_update(self, update_type: str, data: Any):
        """Handle oracle updates"""
        self.logger.debug(f"Oracle update: {update_type}")

        # Can be used to trigger re-verification or alerts
        if update_type == "consensus_update" and isinstance(data, OracleConsensus):
            # Check for significant price movements
            if data.price_deviation > 0.1:
                self.logger.warning(
                    f"High price deviation detected for {data.symbol}: {data.price_deviation:.2%}"
                )

    async def get_market_summary(
        self, symbols: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get current market summary"""
        if not symbols:
            symbols = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD"]

        summary = {
            "timestamp": time.time(),
            "symbols": {},
            "overall_market_health": "healthy",
        }

        total_confidence = 0
        symbol_count = 0

        for symbol in symbols:
            consensus = await self.oracle_engine.get_consensus(symbol)
            if consensus:
                summary["symbols"][symbol] = {
                    "price": consensus.consensus_price,
                    "deviation": consensus.price_deviation,
                    "confidence": consensus.confidence_score,
                    "sources": consensus.source_count,
                    "last_update": consensus.timestamp,
                }
                total_confidence += consensus.confidence_score
                symbol_count += 1

        # Calculate overall market health
        if symbol_count > 0:
            avg_confidence = total_confidence / symbol_count
            if avg_confidence > 0.8:
                summary["overall_market_health"] = "healthy"
            elif avg_confidence > 0.6:
                summary["overall_market_health"] = "moderate"
            else:
                summary["overall_market_health"] = "poor"

        return summary

    async def shutdown(self):
        """Shutdown the oracle integration"""
        self.logger.info("🛑 Shutting down TrustWrapper Oracle Integration...")

        if self.oracle_engine:
            self.oracle_engine.unsubscribe(self._on_oracle_update)
            await self.oracle_engine.stop()

        self.logger.info("✅ TrustWrapper Oracle Integration shutdown complete")


# Global instance for easy access
_oracle_integration_instance = None


async def get_oracle_integration(
    config: Optional[Dict] = None,
) -> TrustWrapperOracleIntegration:
    """Get or create the global oracle integration instance"""
    global _oracle_integration_instance

    if _oracle_integration_instance is None:
        _oracle_integration_instance = TrustWrapperOracleIntegration(config)
        await _oracle_integration_instance.initialize()

    return _oracle_integration_instance

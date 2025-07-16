#!/usr/bin/env python3
"""
Enhanced Attention-Based Explainer for TrustWrapper v2.0
Production-ready attention mechanism visualization with real-time oracle integration
"""

import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class AttentionWeight:
    """Attention weight for a single feature/component"""

    feature_name: str
    attention_score: float
    normalized_attention: float
    temporal_attention: List[float]  # Attention over time steps
    spatial_attention: Optional[float]  # Spatial/cross-feature attention
    explanation: str
    confidence: float


@dataclass
class AttentionMap:
    """Complete attention map for the decision"""

    feature_attention: List[AttentionWeight]
    temporal_attention: Dict[str, List[float]]
    cross_attention: np.ndarray  # Feature-to-feature attention matrix
    global_attention_score: float
    attention_entropy: float
    focus_areas: List[str]
    computation_time_ms: float


@dataclass
class AttentionExplanation:
    """Complete attention-based explanation"""

    attention_map: AttentionMap
    decision_focus: Dict[str, Any]
    attention_trajectory: List[Dict[str, float]]
    oracle_attention_integration: Dict[str, Any]
    uncertainty_analysis: Dict[str, Any]
    computation_time_ms: float
    oracle_context: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TemporalAttentionCalculator:
    """Calculate attention patterns over temporal sequences"""

    def __init__(self, sequence_length: int = 10):
        self.sequence_length = sequence_length
        self.logger = logging.getLogger(__name__)

    def calculate_temporal_attention(
        self,
        feature_sequence: List[Dict[str, float]],
        oracle_sequence: List[Dict[str, Any]],
        current_position: int = -1,
    ) -> Dict[str, List[float]]:
        """Calculate attention weights over temporal sequence"""

        if current_position == -1:
            current_position = len(feature_sequence) - 1

        temporal_attention = {}

        if not feature_sequence:
            return temporal_attention

        # Get feature names from the latest observation
        feature_names = list(feature_sequence[-1].keys()) if feature_sequence else []

        for feature_name in feature_names:
            attention_weights = self._calculate_feature_temporal_attention(
                feature_name, feature_sequence, oracle_sequence, current_position
            )
            temporal_attention[feature_name] = attention_weights

        return temporal_attention

    def _calculate_feature_temporal_attention(
        self,
        feature_name: str,
        feature_sequence: List[Dict[str, float]],
        oracle_sequence: List[Dict[str, Any]],
        current_position: int,
    ) -> List[float]:
        """Calculate temporal attention for a specific feature"""

        if not feature_sequence or feature_name not in feature_sequence[0]:
            return []

        # Extract feature values over time
        feature_values = [obs.get(feature_name, 0.0) for obs in feature_sequence]
        sequence_len = len(feature_values)

        if sequence_len < 2:
            return [1.0] if sequence_len == 1 else []

        # Calculate attention based on multiple factors
        attention_weights = np.zeros(sequence_len)

        # 1. Recency bias (more recent = higher attention)
        recency_weights = np.exp(np.linspace(-2, 0, sequence_len))

        # 2. Change magnitude (larger changes = higher attention)
        if sequence_len > 1:
            changes = np.abs(np.diff(feature_values, prepend=feature_values[0]))
            change_weights = changes / (np.max(changes) + 1e-6)
        else:
            change_weights = np.ones(sequence_len)

        # 3. Oracle quality weighting
        oracle_weights = np.ones(sequence_len)
        if oracle_sequence and len(oracle_sequence) == sequence_len:
            for i, oracle_data in enumerate(oracle_sequence):
                consensus = oracle_data.get("oracle_consensus", {})
                oracle_weights[i] = consensus.get("confidence_score", 0.8)

        # 4. Feature-specific importance
        feature_importance = self._get_feature_importance(feature_name)

        # 5. Volatility-based attention (higher volatility = higher attention)
        if sequence_len > 2:
            volatility = np.std(feature_values[-3:])  # Recent volatility
            volatility_weight = min(1.0 + volatility * 2, 2.0)
        else:
            volatility_weight = 1.0

        # Combine all factors
        for i in range(sequence_len):
            attention_weights[i] = (
                recency_weights[i] * 0.3
                + change_weights[i] * 0.25
                + oracle_weights[i] * 0.2
                + feature_importance * 0.15
                + volatility_weight * 0.1
            )

        # Normalize to sum to 1
        attention_weights = attention_weights / (np.sum(attention_weights) + 1e-6)

        return attention_weights.tolist()

    def _get_feature_importance(self, feature_name: str) -> float:
        """Get base importance for a feature type"""
        importance_map = {
            "oracle_confidence": 0.9,
            "current_price": 0.8,
            "prediction_confidence": 0.85,
            "risk_score": 0.8,
            "volatility_score": 0.75,
            "trend_momentum": 0.7,
            "volume_ratio": 0.6,
            "price_deviation": 0.75,
            "consensus_strength": 0.7,
            "market_state": 0.65,
            "time_of_day": 0.4,
            "historical_accuracy": 0.5,
        }
        return importance_map.get(feature_name, 0.5)


class SpatialAttentionCalculator:
    """Calculate attention between features (cross-attention)"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Define feature relationships
        self.feature_relationships = {
            "oracle_confidence": ["price_deviation", "consensus_strength"],
            "current_price": ["trend_momentum", "volatility_score"],
            "prediction_confidence": ["historical_accuracy", "risk_score"],
            "volatility_score": ["market_state", "volume_ratio"],
            "trend_momentum": ["current_price", "volume_ratio"],
            "risk_score": ["volatility_score", "oracle_confidence"],
            "market_state": ["volatility_score", "trend_momentum"],
            "volume_ratio": ["trend_momentum", "market_state"],
        }

    def calculate_cross_attention(
        self, features: Dict[str, float], oracle_context: Dict[str, Any]
    ) -> np.ndarray:
        """Calculate cross-attention matrix between features"""

        feature_names = list(features.keys())
        n_features = len(feature_names)

        if n_features == 0:
            return np.array([])

        # Initialize attention matrix
        attention_matrix = np.zeros((n_features, n_features))

        # Calculate pairwise attention
        for i, feature_i in enumerate(feature_names):
            for j, feature_j in enumerate(feature_names):
                if i == j:
                    attention_matrix[i, j] = 1.0  # Self-attention
                else:
                    attention_score = self._calculate_pairwise_attention(
                        feature_i, feature_j, features, oracle_context
                    )
                    attention_matrix[i, j] = attention_score

        # Apply softmax row-wise to normalize
        for i in range(n_features):
            row_sum = np.sum(attention_matrix[i, :])
            if row_sum > 0:
                attention_matrix[i, :] = attention_matrix[i, :] / row_sum

        return attention_matrix

    def _calculate_pairwise_attention(
        self,
        feature_i: str,
        feature_j: str,
        features: Dict[str, float],
        oracle_context: Dict[str, Any],
    ) -> float:
        """Calculate attention between two features"""

        # Base relationship strength
        base_attention = 0.1  # Minimum attention

        # Check if features are directly related
        if feature_j in self.feature_relationships.get(feature_i, []):
            base_attention += 0.4

        if feature_i in self.feature_relationships.get(feature_j, []):
            base_attention += 0.4

        # Value-based attention (similar values attend to each other)
        val_i = features.get(feature_i, 0.5)
        val_j = features.get(feature_j, 0.5)
        value_similarity = 1.0 - abs(val_i - val_j)
        base_attention += value_similarity * 0.2

        # Context-specific attention
        context_bonus = self._get_context_attention_bonus(
            feature_i, feature_j, features, oracle_context
        )
        base_attention += context_bonus

        return min(base_attention, 1.0)

    def _get_context_attention_bonus(
        self,
        feature_i: str,
        feature_j: str,
        features: Dict[str, float],
        oracle_context: Dict[str, Any],
    ) -> float:
        """Get context-specific attention bonus"""

        bonus = 0.0

        # High volatility increases attention between price-related features
        volatility = features.get("volatility_score", 0.1)
        if volatility > 0.3:
            price_features = ["current_price", "trend_momentum", "price_deviation"]
            if feature_i in price_features and feature_j in price_features:
                bonus += 0.2

        # Low oracle confidence increases attention to oracle-related features
        oracle_conf = features.get("oracle_confidence", 0.8)
        if oracle_conf < 0.7:
            oracle_features = [
                "oracle_confidence",
                "price_deviation",
                "consensus_strength",
            ]
            if feature_i in oracle_features and feature_j in oracle_features:
                bonus += 0.15

        # Risk factors increase attention between risk-related features
        risk_score = features.get("risk_score", 0.2)
        if risk_score > 0.4:
            risk_features = ["risk_score", "volatility_score", "oracle_confidence"]
            if feature_i in risk_features and feature_j in risk_features:
                bonus += 0.1

        return bonus


class UncertaintyAttentionAnalyzer:
    """Analyze attention patterns to identify uncertainty sources"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_attention_uncertainty(
        self,
        attention_map: AttentionMap,
        features: Dict[str, float],
        oracle_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze uncertainty patterns in attention"""

        uncertainty_analysis = {}

        # 1. Attention dispersion (high dispersion = high uncertainty)
        attention_scores = [
            aw.attention_score for aw in attention_map.feature_attention
        ]
        if attention_scores:
            attention_entropy = -np.sum(
                [a * np.log(a + 1e-6) for a in attention_scores if a > 0]
            )
            max_entropy = np.log(len(attention_scores))
            normalized_entropy = (
                attention_entropy / max_entropy if max_entropy > 0 else 0
            )

            uncertainty_analysis["attention_dispersion"] = normalized_entropy
            uncertainty_analysis["focus_level"] = 1.0 - normalized_entropy
        else:
            uncertainty_analysis["attention_dispersion"] = 0.0
            uncertainty_analysis["focus_level"] = 0.0

        # 2. Conflicting attention patterns
        conflicting_features = self._detect_conflicting_attention(
            attention_map, features
        )
        uncertainty_analysis["conflicting_signals"] = conflicting_features
        uncertainty_analysis["conflict_level"] = len(conflicting_features) / max(
            len(attention_scores), 1
        )

        # 3. Temporal instability
        temporal_instability = self._calculate_temporal_instability(attention_map)
        uncertainty_analysis["temporal_instability"] = temporal_instability

        # 4. Oracle uncertainty propagation
        oracle_uncertainty = self._analyze_oracle_uncertainty_impact(
            attention_map, oracle_context
        )
        uncertainty_analysis["oracle_uncertainty_impact"] = oracle_uncertainty

        # 5. Overall uncertainty score
        overall_uncertainty = (
            uncertainty_analysis["attention_dispersion"] * 0.3
            + uncertainty_analysis["conflict_level"] * 0.25
            + temporal_instability * 0.25
            + oracle_uncertainty * 0.2
        )
        uncertainty_analysis["overall_uncertainty"] = overall_uncertainty

        # 6. Uncertainty interpretation
        if overall_uncertainty > 0.7:
            uncertainty_analysis["interpretation"] = "high_uncertainty"
            uncertainty_analysis["recommendation"] = (
                "Gather more data before making decision"
            )
        elif overall_uncertainty > 0.4:
            uncertainty_analysis["interpretation"] = "moderate_uncertainty"
            uncertainty_analysis["recommendation"] = (
                "Proceed with caution and monitor key indicators"
            )
        else:
            uncertainty_analysis["interpretation"] = "low_uncertainty"
            uncertainty_analysis["recommendation"] = (
                "Decision can be made with current information"
            )

        return uncertainty_analysis

    def _detect_conflicting_attention(
        self, attention_map: AttentionMap, features: Dict[str, float]
    ) -> List[str]:
        """Detect features with conflicting attention patterns"""

        conflicting_features = []

        # Define opposing feature pairs
        opposing_pairs = [
            ("risk_score", "prediction_confidence"),
            ("volatility_score", "oracle_confidence"),
            ("price_deviation", "consensus_strength"),
        ]

        for feature_a, feature_b in opposing_pairs:
            # Find attention weights for these features
            attention_a = None
            attention_b = None

            for aw in attention_map.feature_attention:
                if aw.feature_name == feature_a:
                    attention_a = aw.attention_score
                elif aw.feature_name == feature_b:
                    attention_b = aw.attention_score

            if attention_a is not None and attention_b is not None:
                # Check if both have high attention but conflicting values
                if (
                    attention_a > 0.15 and attention_b > 0.15
                ):  # Both have significant attention
                    val_a = features.get(feature_a, 0.5)
                    val_b = features.get(feature_b, 0.5)

                    # For risk vs confidence: high risk + high confidence = conflict
                    if (
                        feature_a == "risk_score"
                        and feature_b == "prediction_confidence"
                    ):
                        if val_a > 0.6 and val_b > 0.7:  # High risk but high confidence
                            conflicting_features.extend([feature_a, feature_b])

                    # For volatility vs oracle confidence: high volatility + high confidence = conflict
                    elif (
                        feature_a == "volatility_score"
                        and feature_b == "oracle_confidence"
                    ):
                        if (
                            val_a > 0.5 and val_b > 0.8
                        ):  # High volatility but high oracle confidence
                            conflicting_features.extend([feature_a, feature_b])

                    # For price deviation vs consensus strength: high deviation + high consensus = conflict
                    elif (
                        feature_a == "price_deviation"
                        and feature_b == "consensus_strength"
                    ):
                        if (
                            val_a > 0.05 and val_b > 0.8
                        ):  # High deviation but strong consensus
                            conflicting_features.extend([feature_a, feature_b])

        return list(set(conflicting_features))  # Remove duplicates

    def _calculate_temporal_instability(self, attention_map: AttentionMap) -> float:
        """Calculate instability in temporal attention patterns"""

        if not attention_map.temporal_attention:
            return 0.0

        instabilities = []

        for feature_name, temporal_weights in attention_map.temporal_attention.items():
            if len(temporal_weights) > 1:
                # Calculate variance in temporal attention
                variance = np.var(temporal_weights)
                instabilities.append(variance)

        return np.mean(instabilities) if instabilities else 0.0

    def _analyze_oracle_uncertainty_impact(
        self, attention_map: AttentionMap, oracle_context: Dict[str, Any]
    ) -> float:
        """Analyze how oracle uncertainty affects attention patterns"""

        # Get oracle quality metrics
        oracle_consensus = oracle_context.get("oracle_consensus", {})
        oracle_confidence = oracle_consensus.get("confidence_score", 0.8)
        price_deviation = oracle_consensus.get("price_deviation", 0.02)

        # Calculate oracle uncertainty
        oracle_uncertainty = 1.0 - oracle_confidence + price_deviation
        oracle_uncertainty = min(oracle_uncertainty, 1.0)

        # Find attention on oracle-related features
        oracle_feature_attention = 0.0
        oracle_features = [
            "oracle_confidence",
            "price_deviation",
            "consensus_strength",
            "current_price",
        ]

        for aw in attention_map.feature_attention:
            if aw.feature_name in oracle_features:
                oracle_feature_attention += aw.attention_score

        # High oracle uncertainty + high attention on oracle features = high impact
        oracle_impact = oracle_uncertainty * oracle_feature_attention

        return oracle_impact


class EnhancedAttentionExplainer:
    """
    Enhanced attention-based explainer with real-time oracle integration
    Provides attention visualization and uncertainty analysis for AI decisions
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        self.temporal_calculator = TemporalAttentionCalculator(
            sequence_length=self.config.get("sequence_length", 10)
        )
        self.spatial_calculator = SpatialAttentionCalculator()
        self.uncertainty_analyzer = UncertaintyAttentionAnalyzer()

        # Cache for performance
        self.explanation_cache = {}
        self.cache_ttl = self.config.get("cache_ttl", 300)

    def _get_default_config(self) -> Dict:
        """Default configuration for attention explainer"""
        return {
            "sequence_length": 10,
            "attention_threshold": 0.05,
            "cache_ttl": 300,
            "include_temporal": True,
            "include_spatial": True,
            "include_uncertainty": True,
            "focus_top_k": 5,
        }

    async def generate_attention_explanation(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        instance_features: Optional[Dict[str, float]] = None,
        feature_history: Optional[List[Dict[str, float]]] = None,
        oracle_history: Optional[List[Dict[str, Any]]] = None,
    ) -> AttentionExplanation:
        """Generate attention-based explanation for AI decision"""

        start_time = time.time()

        try:
            # Extract features if not provided
            if instance_features is None:
                from .enhanced_shap_explainer import MarketFeatureExtractor

                feature_extractor = MarketFeatureExtractor()
                instance_features = feature_extractor.extract_features(
                    ai_decision, oracle_context
                )

            # Generate current feature attention
            feature_attention = self._calculate_feature_attention(
                instance_features, oracle_context
            )

            # Calculate temporal attention if history is available
            temporal_attention = {}
            if self.config.get("include_temporal", True) and feature_history:
                temporal_attention = (
                    self.temporal_calculator.calculate_temporal_attention(
                        feature_history, oracle_history or [], -1
                    )
                )

            # Calculate spatial (cross-feature) attention
            cross_attention = np.array([])
            if self.config.get("include_spatial", True):
                cross_attention = self.spatial_calculator.calculate_cross_attention(
                    instance_features, oracle_context
                )

            # Calculate attention metrics
            attention_scores = [aw.attention_score for aw in feature_attention]
            global_attention = np.sum(attention_scores) if attention_scores else 0.0

            if attention_scores:
                attention_entropy = -np.sum(
                    [a * np.log(a + 1e-6) for a in attention_scores if a > 0]
                )
            else:
                attention_entropy = 0.0

            # Identify focus areas
            focus_threshold = self.config.get("attention_threshold", 0.05)
            focus_areas = [
                aw.feature_name
                for aw in feature_attention
                if aw.attention_score > focus_threshold
            ]

            # Create attention map
            attention_map = AttentionMap(
                feature_attention=feature_attention,
                temporal_attention=temporal_attention,
                cross_attention=cross_attention,
                global_attention_score=global_attention,
                attention_entropy=attention_entropy,
                focus_areas=focus_areas,
                computation_time_ms=0.0,  # Will be updated
            )

            # Analyze decision focus
            decision_focus = self._analyze_decision_focus(
                attention_map, instance_features, oracle_context
            )

            # Generate attention trajectory (simplified for single time step)
            attention_trajectory = [
                {aw.feature_name: aw.attention_score for aw in feature_attention}
            ]

            # Oracle attention integration analysis
            oracle_attention_integration = self._analyze_oracle_attention_integration(
                attention_map, oracle_context
            )

            # Uncertainty analysis
            uncertainty_analysis = {}
            if self.config.get("include_uncertainty", True):
                uncertainty_analysis = (
                    self.uncertainty_analyzer.analyze_attention_uncertainty(
                        attention_map, instance_features, oracle_context
                    )
                )

            computation_time = (time.time() - start_time) * 1000
            attention_map.computation_time_ms = computation_time

            explanation = AttentionExplanation(
                attention_map=attention_map,
                decision_focus=decision_focus,
                attention_trajectory=attention_trajectory,
                oracle_attention_integration=oracle_attention_integration,
                uncertainty_analysis=uncertainty_analysis,
                computation_time_ms=computation_time,
                oracle_context=oracle_context,
            )

            self.logger.info(
                f"Attention explanation generated: {len(focus_areas)} focus areas, "
                f"{uncertainty_analysis.get('overall_uncertainty', 0):.2f} uncertainty, "
                f"{computation_time:.1f}ms"
            )

            return explanation

        except Exception as e:
            computation_time = (time.time() - start_time) * 1000
            self.logger.error(f"Attention explanation failed: {e}")

            # Return minimal explanation on error
            return AttentionExplanation(
                attention_map=AttentionMap(
                    feature_attention=[],
                    temporal_attention={},
                    cross_attention=np.array([]),
                    global_attention_score=0.0,
                    attention_entropy=0.0,
                    focus_areas=[],
                    computation_time_ms=computation_time,
                ),
                decision_focus={"error": str(e)},
                attention_trajectory=[],
                oracle_attention_integration={},
                uncertainty_analysis={"error": str(e)},
                computation_time_ms=computation_time,
                oracle_context=oracle_context,
            )

    def _calculate_feature_attention(
        self, features: Dict[str, float], oracle_context: Dict[str, Any]
    ) -> List[AttentionWeight]:
        """Calculate attention weights for each feature"""

        feature_attention = []

        # Get market conditions for context
        market_context = oracle_context.get("market_context", {})
        oracle_consensus = oracle_context.get("oracle_consensus", {})

        for feature_name, feature_value in features.items():
            # Base attention calculation
            attention_score = self._calculate_base_attention(
                feature_name, feature_value, features, oracle_context
            )

            # Context adjustments
            attention_score = self._adjust_attention_for_context(
                feature_name, attention_score, market_context, oracle_consensus
            )

            # Confidence in attention score
            confidence = self._calculate_attention_confidence(
                feature_name, feature_value, oracle_context
            )

            # Generate explanation
            explanation = self._generate_attention_explanation(
                feature_name, feature_value, attention_score, oracle_context
            )

            # Temporal attention (simplified - would use history if available)
            temporal_attention = [attention_score]

            feature_attention.append(
                AttentionWeight(
                    feature_name=feature_name,
                    attention_score=attention_score,
                    normalized_attention=0.0,  # Will be normalized later
                    temporal_attention=temporal_attention,
                    spatial_attention=None,  # Calculated separately
                    explanation=explanation,
                    confidence=confidence,
                )
            )

        # Normalize attention scores
        total_attention = sum(aw.attention_score for aw in feature_attention)
        if total_attention > 0:
            for aw in feature_attention:
                aw.normalized_attention = aw.attention_score / total_attention

        # Sort by attention score
        feature_attention.sort(key=lambda x: x.attention_score, reverse=True)

        return feature_attention

    def _calculate_base_attention(
        self,
        feature_name: str,
        feature_value: float,
        features: Dict[str, float],
        oracle_context: Dict[str, Any],
    ) -> float:
        """Calculate base attention score for a feature"""

        # Feature importance weights
        importance_weights = {
            "oracle_confidence": 0.2,
            "prediction_confidence": 0.18,
            "current_price": 0.15,
            "risk_score": 0.15,
            "volatility_score": 0.12,
            "trend_momentum": 0.1,
            "price_deviation": 0.1,
            "consensus_strength": 0.08,
            "volume_ratio": 0.07,
            "market_state": 0.05,
            "time_of_day": 0.03,
            "historical_accuracy": 0.05,
        }

        base_importance = importance_weights.get(feature_name, 0.05)

        # Value-based attention (extreme values get more attention)
        if feature_name in [
            "oracle_confidence",
            "prediction_confidence",
            "historical_accuracy",
        ]:
            # For confidence metrics, both very low and very high values are important
            deviation_from_medium = abs(feature_value - 0.5)
            value_attention = deviation_from_medium * 2
        elif feature_name in ["risk_score", "volatility_score", "price_deviation"]:
            # For risk metrics, higher values get more attention
            value_attention = feature_value
        elif feature_name == "trend_momentum":
            # For trend, extreme values (strong trends) get more attention
            value_attention = abs(feature_value)
        else:
            # Default: moderate deviation from neutral gets attention
            value_attention = min(abs(feature_value - 0.5) * 2, 1.0)

        # Combine base importance and value-based attention
        combined_attention = base_importance * 0.6 + value_attention * 0.4

        return min(combined_attention, 1.0)

    def _adjust_attention_for_context(
        self,
        feature_name: str,
        base_attention: float,
        market_context: Dict[str, Any],
        oracle_consensus: Dict[str, Any],
    ) -> float:
        """Adjust attention based on market context"""

        adjusted_attention = base_attention

        # Get market conditions
        market_state = market_context.get("market_state", "stable")
        volatility = market_context.get("volatility", {}).get("volatility_score", 0.1)
        oracle_confidence = oracle_consensus.get("confidence_score", 0.8)

        # Adjust based on market state
        if market_state == "high_volatility":
            if feature_name in ["volatility_score", "risk_score", "oracle_confidence"]:
                adjusted_attention *= (
                    1.5  # Increase attention on volatility-related features
                )
            elif feature_name in ["trend_momentum", "current_price"]:
                adjusted_attention *= 1.3

        elif market_state in ["bullish", "bearish"]:
            if feature_name in ["trend_momentum", "prediction_confidence"]:
                adjusted_attention *= 1.2  # Increase attention on trend features

        elif market_state == "uncertain":
            if feature_name in [
                "oracle_confidence",
                "risk_score",
                "consensus_strength",
            ]:
                adjusted_attention *= 1.4  # Focus on uncertainty indicators

        # Adjust based on oracle quality
        if oracle_confidence < 0.7:
            if feature_name in [
                "oracle_confidence",
                "price_deviation",
                "consensus_strength",
            ]:
                adjusted_attention *= 1.3  # More attention when oracle is uncertain

        # Adjust based on volatility
        if volatility > 0.3:
            if feature_name in ["volatility_score", "price_deviation", "risk_score"]:
                adjusted_attention *= 1.2

        return min(adjusted_attention, 1.0)

    def _calculate_attention_confidence(
        self, feature_name: str, feature_value: float, oracle_context: Dict[str, Any]
    ) -> float:
        """Calculate confidence in the attention score"""

        base_confidence = 0.8

        # Oracle-related features have confidence tied to oracle quality
        if feature_name in ["oracle_confidence", "current_price", "price_deviation"]:
            oracle_consensus = oracle_context.get("oracle_consensus", {})
            oracle_quality = oracle_consensus.get("confidence_score", 0.8)
            base_confidence = oracle_quality

        # Features with extreme values have higher confidence
        if feature_name in ["prediction_confidence", "risk_score"]:
            if feature_value > 0.8 or feature_value < 0.2:
                base_confidence += 0.1

        # Market state features have moderate confidence
        if feature_name == "market_state":
            base_confidence = 0.7

        return min(base_confidence, 1.0)

    def _generate_attention_explanation(
        self,
        feature_name: str,
        feature_value: float,
        attention_score: float,
        oracle_context: Dict[str, Any],
    ) -> str:
        """Generate explanation for why a feature has specific attention"""

        # Attention level description
        if attention_score > 0.15:
            attention_level = "high attention"
        elif attention_score > 0.08:
            attention_level = "moderate attention"
        else:
            attention_level = "low attention"

        # Feature-specific explanations
        explanations = {
            "oracle_confidence": f"Oracle consensus quality ({feature_value:.1%}) receives {attention_level} due to its critical role in data reliability",
            "prediction_confidence": f"AI model confidence ({feature_value:.1%}) has {attention_level} as it directly indicates prediction reliability",
            "current_price": f"Current market price receives {attention_level} as the primary market signal",
            "risk_score": f"Risk assessment ({feature_value:.1%}) has {attention_level} due to its impact on decision safety",
            "volatility_score": f"Market volatility ({feature_value:.1%}) receives {attention_level} based on its effect on prediction uncertainty",
            "trend_momentum": f"Price trend direction ({feature_value:+.2f}) has {attention_level} for its predictive value",
            "price_deviation": f"Oracle price variation ({feature_value:.2%}) receives {attention_level} for consensus quality assessment",
        }

        base_explanation = explanations.get(
            feature_name,
            f"{feature_name.replace('_', ' ')} (value: {feature_value:.3f}) has {attention_level}",
        )

        # Add context-specific details
        market_context = oracle_context.get("market_context", {})
        if market_context.get("market_state") == "high_volatility" and feature_name in [
            "volatility_score",
            "risk_score",
        ]:
            base_explanation += " (heightened due to volatile market conditions)"

        elif oracle_context.get("oracle_consensus", {}).get(
            "confidence_score", 1.0
        ) < 0.7 and feature_name in ["oracle_confidence"]:
            base_explanation += " (critical due to low oracle consensus)"

        return base_explanation

    def _analyze_decision_focus(
        self,
        attention_map: AttentionMap,
        features: Dict[str, float],
        oracle_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze where the decision is focusing attention"""

        focus_analysis = {}

        # Top attention areas
        top_features = attention_map.feature_attention[
            : self.config.get("focus_top_k", 5)
        ]
        focus_analysis["primary_focus"] = [aw.feature_name for aw in top_features]

        # Attention concentration
        attention_scores = [
            aw.attention_score for aw in attention_map.feature_attention
        ]
        if attention_scores:
            top_3_attention = sum(attention_scores[:3])
            focus_analysis["attention_concentration"] = top_3_attention

            if top_3_attention > 0.7:
                focus_analysis["focus_type"] = "highly_concentrated"
            elif top_3_attention > 0.5:
                focus_analysis["focus_type"] = "moderately_concentrated"
            else:
                focus_analysis["focus_type"] = "distributed"
        else:
            focus_analysis["attention_concentration"] = 0.0
            focus_analysis["focus_type"] = "unclear"

        # Focus categories
        oracle_attention = sum(
            aw.attention_score
            for aw in attention_map.feature_attention
            if aw.feature_name
            in [
                "oracle_confidence",
                "price_deviation",
                "current_price",
                "consensus_strength",
            ]
        )

        ai_attention = sum(
            aw.attention_score
            for aw in attention_map.feature_attention
            if aw.feature_name in ["prediction_confidence", "historical_accuracy"]
        )

        market_attention = sum(
            aw.attention_score
            for aw in attention_map.feature_attention
            if aw.feature_name
            in ["volatility_score", "trend_momentum", "market_state", "volume_ratio"]
        )

        risk_attention = sum(
            aw.attention_score
            for aw in attention_map.feature_attention
            if aw.feature_name in ["risk_score", "volatility_score"]
        )

        focus_analysis["category_attention"] = {
            "oracle_data": oracle_attention,
            "ai_model": ai_attention,
            "market_conditions": market_attention,
            "risk_factors": risk_attention,
        }

        # Dominant category
        category_scores = focus_analysis["category_attention"]
        dominant_category = max(
            category_scores.keys(), key=lambda k: category_scores[k]
        )
        focus_analysis["dominant_category"] = dominant_category

        return focus_analysis

    def _analyze_oracle_attention_integration(
        self, attention_map: AttentionMap, oracle_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze how oracle data is integrated into attention patterns"""

        integration_analysis = {}

        # Oracle feature attention
        oracle_features = [
            "oracle_confidence",
            "current_price",
            "price_deviation",
            "consensus_strength",
        ]
        oracle_attention_weights = []

        for aw in attention_map.feature_attention:
            if aw.feature_name in oracle_features:
                oracle_attention_weights.append(aw.attention_score)

        total_oracle_attention = sum(oracle_attention_weights)
        integration_analysis["total_oracle_attention"] = total_oracle_attention

        # Oracle quality impact on attention
        oracle_consensus = oracle_context.get("oracle_consensus", {})
        oracle_quality = oracle_consensus.get("confidence_score", 0.8)

        integration_analysis["oracle_quality"] = oracle_quality
        integration_analysis["quality_attention_alignment"] = (
            total_oracle_attention * oracle_quality
        )

        # Integration quality assessment
        if total_oracle_attention > 0.4 and oracle_quality > 0.8:
            integration_analysis["integration_quality"] = "excellent"
        elif total_oracle_attention > 0.3 and oracle_quality > 0.7:
            integration_analysis["integration_quality"] = "good"
        elif total_oracle_attention > 0.2:
            integration_analysis["integration_quality"] = "moderate"
        else:
            integration_analysis["integration_quality"] = "limited"

        return integration_analysis

    def generate_attention_summary(self, explanation: AttentionExplanation) -> str:
        """Generate human-readable summary of attention analysis"""

        attention_map = explanation.attention_map
        decision_focus = explanation.decision_focus
        uncertainty = explanation.uncertainty_analysis

        if not attention_map.feature_attention:
            return "Unable to generate attention analysis due to insufficient data."

        # Overall focus summary
        focus_type = decision_focus.get("focus_type", "unclear")
        dominant_category = decision_focus.get("dominant_category", "unknown")

        summary = f"The AI decision shows {focus_type} attention patterns, "
        summary += f"focusing primarily on {dominant_category.replace('_', ' ')}. "

        # Top attention areas
        top_features = attention_map.feature_attention[:3]
        if top_features:
            summary += "Key focus areas: "
            focus_descriptions = []
            for aw in top_features:
                focus_descriptions.append(
                    f"{aw.feature_name} ({aw.normalized_attention:.1%})"
                )
            summary += ", ".join(focus_descriptions) + ". "

        # Uncertainty assessment
        overall_uncertainty = uncertainty.get("overall_uncertainty", 0.0)
        uncertainty_level = uncertainty.get("interpretation", "unknown")

        if uncertainty_level != "unknown":
            summary += (
                f"Attention analysis indicates {uncertainty_level.replace('_', ' ')} "
            )
            summary += f"({overall_uncertainty:.1%} uncertainty score)."

        return summary


# Global instance for easy access
_attention_explainer_instance = None


async def get_attention_explainer(
    config: Optional[Dict] = None,
) -> EnhancedAttentionExplainer:
    """Get or create the global attention explainer instance"""
    global _attention_explainer_instance

    if _attention_explainer_instance is None:
        _attention_explainer_instance = EnhancedAttentionExplainer(config)

    return _attention_explainer_instance

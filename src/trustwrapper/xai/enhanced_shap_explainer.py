#!/usr/bin/env python3
"""
Enhanced SHAP Explainer for TrustWrapper v2.0
Production-ready SHAP implementation with real-time oracle integration
"""

import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class SHAPValue:
    """SHAP value for a single feature"""

    feature_name: str
    value: float
    baseline_value: float
    shap_value: float
    contribution_percentage: float
    importance_rank: int
    explanation: str


@dataclass
class SHAPExplanation:
    """Complete SHAP explanation result"""

    prediction: float
    baseline: float
    shap_values: List[SHAPValue]
    total_contribution: float
    explanation_confidence: float
    computation_time_ms: float
    oracle_context: Dict[str, Any]
    model_context: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MarketFeatureExtractor:
    """Extract relevant features from market data for SHAP analysis"""

    def __init__(self):
        self.feature_definitions = {
            "current_price": "Current market price from oracle consensus",
            "price_deviation": "Price deviation across oracle sources",
            "oracle_confidence": "Confidence score from oracle consensus",
            "volatility_score": "Market volatility indicator",
            "volume_ratio": "Trading volume relative to average",
            "trend_momentum": "Price trend momentum indicator",
            "consensus_strength": "Oracle source agreement strength",
            "market_state": "Overall market condition classification",
            "risk_score": "Aggregate risk assessment score",
            "time_of_day": "Trading session time factor",
            "prediction_confidence": "AI model confidence score",
            "historical_accuracy": "Model historical accuracy for this asset",
        }

    def extract_features(
        self, ai_decision: Dict[str, Any], oracle_context: Dict[str, Any]
    ) -> Dict[str, float]:
        """Extract numerical features for SHAP analysis"""
        features = {}

        # Oracle-based features
        consensus_data = oracle_context.get("oracle_consensus", {})
        market_conditions = oracle_context.get("market_context", {})

        features["current_price"] = (
            consensus_data.get("consensus_price", 0) / 100000
        )  # Normalize
        features["price_deviation"] = consensus_data.get("price_deviation", 0)
        features["oracle_confidence"] = consensus_data.get("confidence_score", 0)
        features["consensus_strength"] = min(
            consensus_data.get("source_count", 0) / 5.0, 1.0
        )

        # Market condition features
        volatility = market_conditions.get("volatility", {})
        features["volatility_score"] = volatility.get("volatility_score", 0)

        volume_analysis = market_conditions.get("volume_analysis", {})
        features["volume_ratio"] = min(
            volume_analysis.get("volume_ratio", 1.0) / 3.0, 1.0
        )

        # Market state encoding
        market_state = market_conditions.get("market_state", "stable")
        state_encoding = {
            "stable": 0.5,
            "bullish": 0.8,
            "bearish": 0.2,
            "high_volatility": 0.1,
            "uncertain": 0.3,
        }
        features["market_state"] = state_encoding.get(market_state, 0.5)

        # AI decision features
        features["prediction_confidence"] = ai_decision.get("confidence", 0.5)

        # Risk assessment
        risk_factors = oracle_context.get("risk_factors", [])
        features["risk_score"] = min(len(risk_factors) / 5.0, 1.0)  # Normalize to 0-1

        # Time-based features
        current_hour = time.localtime().tm_hour
        # Trading session encoding: Asian (0-8): 0.3, European (8-16): 0.8, US (16-24): 1.0
        if 0 <= current_hour < 8:
            features["time_of_day"] = 0.3
        elif 8 <= current_hour < 16:
            features["time_of_day"] = 0.8
        else:
            features["time_of_day"] = 1.0

        # Trend analysis
        predicted_price = ai_decision.get(
            "predicted_price", features["current_price"] * 100000
        )
        current_price = features["current_price"] * 100000
        price_change = (
            (predicted_price - current_price) / current_price
            if current_price > 0
            else 0
        )
        features["trend_momentum"] = max(
            -1.0, min(1.0, price_change * 10)
        )  # Scale to -1 to 1

        # Historical accuracy (simulated based on market conditions)
        base_accuracy = 0.7
        if features["volatility_score"] < 0.1:
            accuracy_adjustment = 0.2  # Better accuracy in stable markets
        elif features["volatility_score"] > 0.5:
            accuracy_adjustment = -0.3  # Lower accuracy in volatile markets
        else:
            accuracy_adjustment = 0.0

        features["historical_accuracy"] = max(
            0.1, min(0.95, base_accuracy + accuracy_adjustment)
        )

        return features

    def get_feature_explanation(self, feature_name: str, value: float) -> str:
        """Generate human-readable explanation for a feature"""
        base_explanation = self.feature_definitions.get(
            feature_name, f"Feature: {feature_name}"
        )

        # Add value-specific context
        if feature_name == "oracle_confidence":
            if value > 0.9:
                context = "Very high oracle confidence"
            elif value > 0.7:
                context = "Good oracle confidence"
            elif value > 0.5:
                context = "Moderate oracle confidence"
            else:
                context = "Low oracle confidence"
        elif feature_name == "volatility_score":
            if value > 0.5:
                context = "High market volatility"
            elif value > 0.2:
                context = "Moderate volatility"
            else:
                context = "Low volatility"
        elif feature_name == "trend_momentum":
            if value > 0.5:
                context = "Strong upward trend"
            elif value > 0.1:
                context = "Positive trend"
            elif value < -0.5:
                context = "Strong downward trend"
            elif value < -0.1:
                context = "Negative trend"
            else:
                context = "Sideways trend"
        else:
            context = f"Value: {value:.3f}"

        return f"{base_explanation} ({context})"


class KernelSHAPCalculator:
    """Kernel SHAP implementation for TrustWrapper AI decisions"""

    def __init__(self, num_samples: int = 1000):
        self.num_samples = num_samples
        self.logger = logging.getLogger(__name__)

    def calculate_shap_values(
        self,
        features: Dict[str, float],
        prediction_function: callable,
        baseline_prediction: float,
    ) -> Dict[str, float]:
        """Calculate SHAP values using Kernel SHAP algorithm"""

        feature_names = list(features.keys())
        feature_values = np.array(list(features.values()))
        n_features = len(feature_names)

        # Generate coalitions (subsets of features)
        coalitions = self._generate_coalitions(n_features)

        # Calculate coalition values
        coalition_values = []
        for coalition in coalitions:
            coalition_features = self._create_coalition_features(
                feature_values, coalition
            )
            coalition_dict = dict(zip(feature_names, coalition_features))

            try:
                value = prediction_function(coalition_dict)
                coalition_values.append(value)
            except:
                # Fallback to baseline if prediction fails
                coalition_values.append(baseline_prediction)

        # Solve linear system to get SHAP values
        shap_values = self._solve_shap_system(
            coalitions, coalition_values, baseline_prediction
        )

        return dict(zip(feature_names, shap_values))

    def _generate_coalitions(self, n_features: int) -> List[List[int]]:
        """Generate representative coalitions for SHAP calculation"""
        coalitions = []

        # Always include empty set and full set
        coalitions.append([])
        coalitions.append(list(range(n_features)))

        # Add individual features
        for i in range(n_features):
            coalitions.append([i])

        # Add pairs and larger coalitions based on sample budget
        remaining_samples = self.num_samples - len(coalitions)

        if remaining_samples > 0:
            # Add random coalitions
            np.random.seed(42)  # For reproducibility
            for _ in range(min(remaining_samples, 200)):
                coalition_size = np.random.randint(1, n_features)
                coalition = np.random.choice(
                    n_features, coalition_size, replace=False
                ).tolist()
                if coalition not in coalitions:
                    coalitions.append(coalition)

        return coalitions

    def _create_coalition_features(
        self, feature_values: np.ndarray, coalition: List[int]
    ) -> np.ndarray:
        """Create feature vector for a coalition (missing features set to baseline)"""
        coalition_features = np.zeros_like(feature_values)

        # Set coalition features to their actual values
        for idx in coalition:
            coalition_features[idx] = feature_values[idx]

        # Missing features are set to their expected baseline values
        for idx in range(len(feature_values)):
            if idx not in coalition:
                coalition_features[idx] = self._get_feature_baseline(idx)

        return coalition_features

    def _get_feature_baseline(self, feature_idx: int) -> float:
        """Get baseline value for a feature (neutral/average value)"""
        # These are typical neutral/baseline values for our features
        baselines = [0.5, 0.02, 0.8, 0.1, 1.0, 0.0, 0.6, 0.5, 0.2, 0.5, 0.5, 0.7]
        return baselines[feature_idx] if feature_idx < len(baselines) else 0.5

    def _solve_shap_system(
        self,
        coalitions: List[List[int]],
        coalition_values: List[float],
        baseline: float,
    ) -> np.ndarray:
        """Solve the linear system to get SHAP values"""
        n_features = (
            max(max(coalition, default=0) for coalition in coalitions) + 1
            if coalitions
            else 0
        )

        if n_features == 0:
            return np.array([])

        # Create the characteristic matrix
        char_matrix = np.zeros((len(coalitions), n_features))

        for i, coalition in enumerate(coalitions):
            for feature_idx in coalition:
                char_matrix[i, feature_idx] = 1

        # Create target vector (coalition values minus baseline)
        target_values = np.array(coalition_values) - baseline

        # Solve using least squares (regularized for stability)
        try:
            # Add small regularization for numerical stability
            regularization = 1e-6 * np.eye(n_features)
            A = char_matrix.T @ char_matrix + regularization
            b = char_matrix.T @ target_values

            shap_values = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            # Fallback to pseudo-inverse if direct solution fails
            shap_values = np.linalg.pinv(char_matrix) @ target_values

        return shap_values


class EnhancedSHAPExplainer:
    """
    Enhanced SHAP explainer with real-time oracle integration
    Provides production-ready SHAP explanations for TrustWrapper AI decisions
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        self.feature_extractor = MarketFeatureExtractor()
        self.shap_calculator = KernelSHAPCalculator(
            num_samples=self.config.get("num_samples", 1000)
        )

        # Cache for performance
        self.explanation_cache = {}
        self.cache_ttl = self.config.get("cache_ttl", 300)  # 5 minutes

    def _get_default_config(self) -> Dict:
        """Default configuration for SHAP explainer"""
        return {
            "num_samples": 1000,
            "cache_ttl": 300,
            "min_confidence_threshold": 0.1,
            "explanation_detail_level": "full",  # basic, standard, full
            "include_counterfactuals": True,
            "normalize_contributions": True,
        }

    async def explain_prediction(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        model_prediction_function: Optional[callable] = None,
    ) -> SHAPExplanation:
        """
        Generate SHAP explanation for an AI decision with oracle context
        """
        start_time = time.time()

        try:
            # Extract features from AI decision and oracle context
            features = self.feature_extractor.extract_features(
                ai_decision, oracle_context
            )

            # Get prediction and baseline
            prediction = ai_decision.get("confidence", 0.5)

            # Create prediction function if not provided
            if model_prediction_function is None:
                model_prediction_function = self._create_surrogate_model(
                    ai_decision, oracle_context, features
                )

            # Calculate baseline prediction (neutral market conditions)
            baseline_features = self._get_baseline_features()
            baseline_prediction = model_prediction_function(baseline_features)

            # Calculate SHAP values
            shap_values_dict = self.shap_calculator.calculate_shap_values(
                features, model_prediction_function, baseline_prediction
            )

            # Create SHAP value objects with explanations
            shap_values = self._create_shap_value_objects(
                features, shap_values_dict, baseline_prediction
            )

            # Sort by importance
            shap_values.sort(key=lambda x: abs(x.shap_value), reverse=True)

            # Assign importance ranks
            for i, shap_val in enumerate(shap_values):
                shap_val.importance_rank = i + 1

            # Calculate explanation confidence
            explanation_confidence = self._calculate_explanation_confidence(
                shap_values, features, oracle_context
            )

            computation_time = (time.time() - start_time) * 1000

            explanation = SHAPExplanation(
                prediction=prediction,
                baseline=baseline_prediction,
                shap_values=shap_values,
                total_contribution=sum(sv.shap_value for sv in shap_values),
                explanation_confidence=explanation_confidence,
                computation_time_ms=computation_time,
                oracle_context=oracle_context,
                model_context={
                    "ai_decision": ai_decision,
                    "features_used": list(features.keys()),
                    "baseline_features": baseline_features,
                },
            )

            self.logger.info(
                f"SHAP explanation generated: {len(shap_values)} features, "
                f"{explanation_confidence:.1%} confidence, {computation_time:.1f}ms"
            )

            return explanation

        except Exception as e:
            computation_time = (time.time() - start_time) * 1000
            self.logger.error(f"SHAP explanation failed: {e}")

            # Return minimal explanation on error
            return SHAPExplanation(
                prediction=ai_decision.get("confidence", 0.5),
                baseline=0.5,
                shap_values=[],
                total_contribution=0.0,
                explanation_confidence=0.0,
                computation_time_ms=computation_time,
                oracle_context=oracle_context,
                model_context={"error": str(e)},
            )

    def _create_surrogate_model(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        original_features: Dict[str, float],
    ) -> callable:
        """Create a surrogate model for SHAP calculation"""

        def surrogate_prediction(features: Dict[str, float]) -> float:
            """Surrogate model that approximates the AI decision process"""

            # Base prediction from AI confidence
            base_prediction = ai_decision.get("confidence", 0.5)

            # Adjust based on oracle confidence
            oracle_adjustment = features.get("oracle_confidence", 0.8) - 0.8

            # Adjust based on market conditions
            volatility_penalty = features.get("volatility_score", 0.1) * -0.2

            # Adjust based on risk score
            risk_penalty = features.get("risk_score", 0.2) * -0.3

            # Adjust based on historical accuracy
            accuracy_bonus = (features.get("historical_accuracy", 0.7) - 0.7) * 0.2

            # Trend momentum impact
            trend_impact = features.get("trend_momentum", 0.0) * 0.1

            # Volume impact
            volume_impact = min(features.get("volume_ratio", 1.0), 2.0) * 0.05 - 0.05

            # Combine adjustments
            total_adjustment = (
                oracle_adjustment
                + volatility_penalty
                + risk_penalty
                + accuracy_bonus
                + trend_impact
                + volume_impact
            )

            # Apply bounds
            final_prediction = max(0.0, min(1.0, base_prediction + total_adjustment))

            return final_prediction

        return surrogate_prediction

    def _get_baseline_features(self) -> Dict[str, float]:
        """Get baseline feature values representing neutral market conditions"""
        return {
            "current_price": 0.5,  # Normalized neutral price
            "price_deviation": 0.02,  # Low deviation
            "oracle_confidence": 0.8,  # Good confidence
            "volatility_score": 0.1,  # Low volatility
            "volume_ratio": 1.0,  # Normal volume
            "trend_momentum": 0.0,  # No trend
            "consensus_strength": 0.6,  # Moderate consensus
            "market_state": 0.5,  # Stable market
            "risk_score": 0.2,  # Low risk
            "time_of_day": 0.5,  # Mid-session
            "prediction_confidence": 0.5,  # Neutral confidence
            "historical_accuracy": 0.7,  # Good historical accuracy
        }

    def _create_shap_value_objects(
        self, features: Dict[str, float], shap_values: Dict[str, float], baseline: float
    ) -> List[SHAPValue]:
        """Create SHAP value objects with explanations"""

        shap_objects = []
        total_abs_contribution = sum(abs(shap_val) for shap_val in shap_values.values())

        for feature_name, feature_value in features.items():
            shap_value = shap_values.get(feature_name, 0.0)

            # Calculate contribution percentage
            if total_abs_contribution > 0:
                contribution_pct = abs(shap_value) / total_abs_contribution * 100
            else:
                contribution_pct = 0.0

            # Generate explanation
            explanation = self.feature_extractor.get_feature_explanation(
                feature_name, feature_value
            )

            shap_objects.append(
                SHAPValue(
                    feature_name=feature_name,
                    value=feature_value,
                    baseline_value=self._get_baseline_features().get(feature_name, 0.5),
                    shap_value=shap_value,
                    contribution_percentage=contribution_pct,
                    importance_rank=0,  # Will be set after sorting
                    explanation=explanation,
                )
            )

        return shap_objects

    def _calculate_explanation_confidence(
        self,
        shap_values: List[SHAPValue],
        features: Dict[str, float],
        oracle_context: Dict[str, Any],
    ) -> float:
        """Calculate confidence in the SHAP explanation"""

        base_confidence = 0.8

        # Adjust based on oracle quality
        oracle_consensus = oracle_context.get("oracle_consensus", {})
        oracle_confidence = oracle_consensus.get("confidence_score", 0.8)
        oracle_adjustment = (oracle_confidence - 0.8) * 0.3

        # Adjust based on feature stability
        total_contribution = sum(abs(sv.shap_value) for sv in shap_values)
        if total_contribution > 0:
            # More concentrated contributions = higher confidence
            concentration = (
                sum(sv.shap_value**2 for sv in shap_values) / total_contribution**2
            )
            concentration_adjustment = min(concentration * 0.2, 0.2)
        else:
            concentration_adjustment = -0.3

        # Adjust based on market conditions
        market_conditions = oracle_context.get("market_context", {})
        market_state = market_conditions.get("market_state", "stable")

        if market_state == "stable":
            market_adjustment = 0.1
        elif market_state in ["bullish", "bearish"]:
            market_adjustment = 0.05
        else:  # high_volatility, uncertain
            market_adjustment = -0.2

        # Calculate final confidence
        final_confidence = (
            base_confidence
            + oracle_adjustment
            + concentration_adjustment
            + market_adjustment
        )

        return max(0.1, min(1.0, final_confidence))

    def get_top_features(
        self, explanation: SHAPExplanation, n: int = 5
    ) -> List[SHAPValue]:
        """Get top N most important features from SHAP explanation"""
        return explanation.shap_values[:n]

    def get_feature_impact_summary(
        self, explanation: SHAPExplanation
    ) -> Dict[str, Any]:
        """Get summary of feature impacts"""
        positive_impact = sum(
            sv.shap_value for sv in explanation.shap_values if sv.shap_value > 0
        )
        negative_impact = sum(
            sv.shap_value for sv in explanation.shap_values if sv.shap_value < 0
        )

        top_positive = [sv for sv in explanation.shap_values if sv.shap_value > 0][:3]
        top_negative = [sv for sv in explanation.shap_values if sv.shap_value < 0][:3]

        return {
            "total_positive_impact": positive_impact,
            "total_negative_impact": negative_impact,
            "net_impact": positive_impact + negative_impact,
            "top_positive_features": [sv.feature_name for sv in top_positive],
            "top_negative_features": [sv.feature_name for sv in top_negative],
            "dominant_factor": (
                explanation.shap_values[0].feature_name
                if explanation.shap_values
                else None
            ),
        }

    def generate_human_explanation(self, explanation: SHAPExplanation) -> str:
        """Generate human-readable explanation from SHAP results"""

        if not explanation.shap_values:
            return "Unable to generate explanation due to insufficient data."

        top_features = explanation.shap_values[:3]
        prediction = explanation.prediction

        # Start with overall assessment
        if prediction > 0.7:
            assessment = "highly confident"
        elif prediction > 0.5:
            assessment = "moderately confident"
        else:
            assessment = "low confidence"

        explanation_text = (
            f"The AI decision shows {assessment} prediction ({prediction:.1%}). "
        )

        # Explain top contributing factors
        explanation_text += "Key factors: "

        factor_explanations = []
        for feature in top_features:
            impact = "increases" if feature.shap_value > 0 else "decreases"
            factor_explanations.append(
                f"{feature.feature_name} {impact} confidence by {abs(feature.shap_value):.1%} "
                f"({feature.explanation.lower()})"
            )

        explanation_text += "; ".join(factor_explanations[:2])

        # Add oracle context
        oracle_consensus = explanation.oracle_context.get("oracle_consensus", {})
        if oracle_consensus:
            price = oracle_consensus.get("consensus_price", 0)
            confidence = oracle_consensus.get("confidence_score", 0)
            explanation_text += f". Oracle data shows ${price:,.2f} with {confidence:.1%} consensus confidence."

        return explanation_text


# Global instance for easy access
_shap_explainer_instance = None


async def get_shap_explainer(config: Optional[Dict] = None) -> EnhancedSHAPExplainer:
    """Get or create the global SHAP explainer instance"""
    global _shap_explainer_instance

    if _shap_explainer_instance is None:
        _shap_explainer_instance = EnhancedSHAPExplainer(config)

    return _shap_explainer_instance

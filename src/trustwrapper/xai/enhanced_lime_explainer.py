#!/usr/bin/env python3
"""
Enhanced LIME Explainer for TrustWrapper v2.0
Production-ready LIME implementation with real-time oracle integration
"""

import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler


@dataclass
class LIMEFeature:
    """LIME feature explanation"""

    feature_name: str
    original_value: float
    perturbed_values: List[float]
    coefficients: List[float]
    mean_coefficient: float
    confidence_interval: Tuple[float, float]
    explanation: str
    local_importance: float


@dataclass
class LIMEExplanation:
    """Complete LIME explanation result"""

    instance_prediction: float
    local_features: List[LIMEFeature]
    local_model_score: float
    local_model_complexity: int
    neighborhood_size: int
    perturbation_stats: Dict[str, Any]
    computation_time_ms: float
    oracle_context: Dict[str, Any]
    locality_radius: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LocalNeighborhoodGenerator:
    """Generate local neighborhood around instance for LIME"""

    def __init__(self, num_samples: int = 5000):
        self.num_samples = num_samples
        self.logger = logging.getLogger(__name__)

    def generate_neighborhood(
        self, original_instance: Dict[str, float], oracle_context: Dict[str, Any]
    ) -> Tuple[List[Dict[str, float]], np.ndarray]:
        """Generate neighborhood of perturbed instances around original"""

        features = list(original_instance.keys())
        original_values = np.array(list(original_instance.values()))

        # Determine perturbation strategy based on feature types
        perturbation_config = self._get_perturbation_config(features, oracle_context)

        # Generate perturbed samples
        perturbed_samples = []
        sample_weights = []

        for i in range(self.num_samples):
            perturbed_values = self._perturb_instance(
                original_values, features, perturbation_config
            )

            # Create perturbed instance
            perturbed_instance = dict(zip(features, perturbed_values))
            perturbed_samples.append(perturbed_instance)

            # Calculate weight based on distance from original
            distance = self._calculate_distance(original_values, perturbed_values)
            weight = self._distance_to_weight(distance)
            sample_weights.append(weight)

        return perturbed_samples, np.array(sample_weights)

    def _get_perturbation_config(
        self, features: List[str], oracle_context: Dict[str, Any]
    ) -> Dict[str, Dict]:
        """Get perturbation configuration for each feature type"""
        config = {}

        # Get market volatility for scaling perturbations
        market_context = oracle_context.get("market_context", {})
        volatility = market_context.get("volatility", {}).get("volatility_score", 0.1)
        base_scale = 0.1 + volatility * 0.2  # Higher volatility = larger perturbations

        for feature in features:
            if feature == "current_price":
                # Price should vary based on recent volatility
                config[feature] = {
                    "type": "continuous",
                    "scale": base_scale * 2,  # Prices can vary more
                    "distribution": "normal",
                    "bounds": (0.0, 2.0),  # Normalized price bounds
                }
            elif feature in [
                "oracle_confidence",
                "prediction_confidence",
                "historical_accuracy",
            ]:
                # Confidence metrics have bounded variation
                config[feature] = {
                    "type": "continuous",
                    "scale": 0.05,  # Small variations in confidence
                    "distribution": "normal",
                    "bounds": (0.0, 1.0),
                }
            elif feature in ["price_deviation", "volatility_score", "risk_score"]:
                # Deviation and risk metrics
                config[feature] = {
                    "type": "continuous",
                    "scale": base_scale,
                    "distribution": "normal",
                    "bounds": (0.0, 1.0),
                }
            elif feature == "volume_ratio":
                # Volume can have larger variations
                config[feature] = {
                    "type": "continuous",
                    "scale": 0.3,
                    "distribution": "lognormal",  # Volume is often log-normal
                    "bounds": (0.1, 5.0),
                }
            elif feature == "trend_momentum":
                # Trend can reverse
                config[feature] = {
                    "type": "continuous",
                    "scale": 0.2,
                    "distribution": "normal",
                    "bounds": (-1.0, 1.0),
                }
            elif feature == "market_state":
                # Market state is categorical but encoded numerically
                config[feature] = {
                    "type": "categorical",
                    "values": [
                        0.2,
                        0.3,
                        0.5,
                        0.8,
                        0.1,
                    ],  # bearish, uncertain, stable, bullish, volatile
                    "probabilities": [0.15, 0.15, 0.4, 0.2, 0.1],
                }
            else:
                # Default configuration
                config[feature] = {
                    "type": "continuous",
                    "scale": 0.1,
                    "distribution": "normal",
                    "bounds": (0.0, 1.0),
                }

        return config

    def _perturb_instance(
        self, original_values: np.ndarray, features: List[str], config: Dict[str, Dict]
    ) -> np.ndarray:
        """Perturb a single instance according to configuration"""
        perturbed = original_values.copy()

        for i, feature in enumerate(features):
            feature_config = config.get(feature, {})

            if feature_config.get("type") == "categorical":
                # Sample from categorical distribution
                values = feature_config.get("values", [original_values[i]])
                probs = feature_config.get("probabilities")
                perturbed[i] = np.random.choice(values, p=probs)

            else:
                # Continuous perturbation
                scale = feature_config.get("scale", 0.1)
                distribution = feature_config.get("distribution", "normal")
                bounds = feature_config.get("bounds", (0.0, 1.0))

                if distribution == "normal":
                    noise = np.random.normal(0, scale)
                elif distribution == "lognormal":
                    # For lognormal, we perturb the log and exponentiate
                    log_val = np.log(max(original_values[i], 1e-6))
                    noise = np.random.normal(0, scale)
                    perturbed[i] = np.exp(log_val + noise)
                else:
                    noise = np.random.normal(0, scale)

                # Apply noise and bounds
                if distribution != "lognormal":
                    perturbed[i] = original_values[i] + noise

                perturbed[i] = np.clip(perturbed[i], bounds[0], bounds[1])

        return perturbed

    def _calculate_distance(self, original: np.ndarray, perturbed: np.ndarray) -> float:
        """Calculate distance between original and perturbed instance"""
        # Use weighted Euclidean distance
        weights = np.array(
            [2.0, 1.0, 2.0, 1.5, 1.0, 1.0, 1.5, 1.5, 1.5, 1.0, 2.0, 1.0]
        )  # Feature importance weights
        weights = weights[: len(original)]  # Trim to actual number of features

        diff = original - perturbed
        weighted_diff = diff * weights[: len(diff)]
        return np.sqrt(np.sum(weighted_diff**2))

    def _distance_to_weight(self, distance: float, kernel_width: float = 1.0) -> float:
        """Convert distance to sample weight using RBF kernel"""
        return np.exp(-(distance**2) / (kernel_width**2))


class LocalLinearModel:
    """Local linear model for LIME explanations"""

    def __init__(self, regularization: float = 0.01):
        self.regularization = regularization
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        sample_weights: np.ndarray,
        feature_names: List[str],
    ) -> Dict[str, Any]:
        """Fit local linear model to neighborhood data"""

        self.feature_names = feature_names

        # Standardize features for better numerical stability
        X_scaled = self.scaler.fit_transform(X)

        # Fit Ridge regression with sample weights
        self.model = Ridge(alpha=self.regularization)
        self.model.fit(X_scaled, y, sample_weight=sample_weights)

        # Calculate model statistics
        y_pred = self.model.predict(X_scaled)

        # R-squared with weighted samples
        ss_res = np.sum(sample_weights * (y - y_pred) ** 2)
        ss_tot = np.sum(
            sample_weights * (y - np.average(y, weights=sample_weights)) ** 2
        )
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Mean absolute error
        mae = np.average(np.abs(y - y_pred), weights=sample_weights)

        return {
            "r_squared": r_squared,
            "mae": mae,
            "coefficients": self.model.coef_,
            "intercept": self.model.intercept_,
            "n_samples": len(X),
            "effective_samples": np.sum(sample_weights),
        }

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from local model coefficients"""
        if self.model is None:
            return {}

        importance = {}
        for i, feature_name in enumerate(self.feature_names):
            importance[feature_name] = abs(self.model.coef_[i])

        return importance

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using the local model"""
        if self.model is None:
            raise ValueError("Model not fitted")

        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)


class EnhancedLIMEExplainer:
    """
    Enhanced LIME explainer with real-time oracle integration
    Provides local interpretable model-agnostic explanations
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        self.neighborhood_generator = LocalNeighborhoodGenerator(
            num_samples=self.config.get("num_samples", 5000)
        )

        # Cache for performance
        self.explanation_cache = {}
        self.cache_ttl = self.config.get("cache_ttl", 300)

    def _get_default_config(self) -> Dict:
        """Default configuration for LIME explainer"""
        return {
            "num_samples": 5000,
            "num_features": 10,
            "regularization": 0.01,
            "kernel_width": 1.0,
            "cache_ttl": 300,
            "min_r_squared": 0.3,
            "feature_selection": "highest_weights",  # highest_weights, lasso, forward_selection
        }

    async def explain_instance(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        prediction_function: callable,
        instance_features: Optional[Dict[str, float]] = None,
    ) -> LIMEExplanation:
        """
        Generate LIME explanation for a specific AI decision instance
        """
        start_time = time.time()

        try:
            # Extract features if not provided
            if instance_features is None:
                from .enhanced_shap_explainer import MarketFeatureExtractor

                feature_extractor = MarketFeatureExtractor()
                instance_features = feature_extractor.extract_features(
                    ai_decision, oracle_context
                )

            # Get instance prediction
            instance_prediction = prediction_function(instance_features)

            # Generate neighborhood
            perturbed_samples, sample_weights = (
                self.neighborhood_generator.generate_neighborhood(
                    instance_features, oracle_context
                )
            )

            # Get predictions for neighborhood
            neighborhood_predictions = []
            for sample in perturbed_samples:
                try:
                    pred = prediction_function(sample)
                    neighborhood_predictions.append(pred)
                except:
                    # Use instance prediction as fallback
                    neighborhood_predictions.append(instance_prediction)

            neighborhood_predictions = np.array(neighborhood_predictions)

            # Convert samples to matrix
            feature_names = list(instance_features.keys())
            X = np.array(
                [
                    [sample[fname] for fname in feature_names]
                    for sample in perturbed_samples
                ]
            )

            # Fit local model
            local_model = LocalLinearModel(regularization=self.config["regularization"])
            model_stats = local_model.fit(
                X, neighborhood_predictions, sample_weights, feature_names
            )

            # Calculate locality radius
            distances = [
                self.neighborhood_generator._calculate_distance(
                    np.array(list(instance_features.values())),
                    np.array([sample[fname] for fname in feature_names]),
                )
                for sample in perturbed_samples
            ]
            locality_radius = np.percentile(
                distances, 90
            )  # 90th percentile of distances

            # Create LIME features with perturbation analysis
            lime_features = self._create_lime_features(
                instance_features, perturbed_samples, local_model, oracle_context
            )

            # Calculate perturbation statistics
            perturbation_stats = self._calculate_perturbation_stats(
                perturbed_samples, neighborhood_predictions, sample_weights
            )

            computation_time = (time.time() - start_time) * 1000

            explanation = LIMEExplanation(
                instance_prediction=instance_prediction,
                local_features=lime_features,
                local_model_score=model_stats["r_squared"],
                local_model_complexity=len(feature_names),
                neighborhood_size=len(perturbed_samples),
                perturbation_stats=perturbation_stats,
                computation_time_ms=computation_time,
                oracle_context=oracle_context,
                locality_radius=locality_radius,
            )

            self.logger.info(
                f"LIME explanation generated: R²={model_stats['r_squared']:.3f}, "
                f"{len(lime_features)} features, {computation_time:.1f}ms"
            )

            return explanation

        except Exception as e:
            computation_time = (time.time() - start_time) * 1000
            self.logger.error(f"LIME explanation failed: {e}")

            # Return minimal explanation on error
            return LIMEExplanation(
                instance_prediction=ai_decision.get("confidence", 0.5),
                local_features=[],
                local_model_score=0.0,
                local_model_complexity=0,
                neighborhood_size=0,
                perturbation_stats={"error": str(e)},
                computation_time_ms=computation_time,
                oracle_context=oracle_context,
                locality_radius=0.0,
            )

    def _create_lime_features(
        self,
        instance_features: Dict[str, float],
        perturbed_samples: List[Dict[str, float]],
        local_model: LocalLinearModel,
        oracle_context: Dict[str, Any],
    ) -> List[LIMEFeature]:
        """Create LIME feature objects with local analysis"""

        lime_features = []
        feature_importance = local_model.get_feature_importance()

        for feature_name, original_value in instance_features.items():
            # Collect perturbed values for this feature
            perturbed_values = [sample[feature_name] for sample in perturbed_samples]

            # Calculate local effects through multiple perturbations
            coefficients = self._calculate_local_coefficients(
                feature_name, original_value, perturbed_samples, local_model
            )

            mean_coefficient = np.mean(coefficients)

            # Calculate confidence interval for coefficient
            confidence_interval = (
                np.percentile(coefficients, 5),
                np.percentile(coefficients, 95),
            )

            # Generate explanation
            explanation = self._generate_feature_explanation(
                feature_name, original_value, mean_coefficient, oracle_context
            )

            # Local importance is the standardized coefficient magnitude
            local_importance = feature_importance.get(feature_name, 0.0)

            lime_features.append(
                LIMEFeature(
                    feature_name=feature_name,
                    original_value=original_value,
                    perturbed_values=perturbed_values[
                        :10
                    ],  # Store sample of perturbations
                    coefficients=coefficients[:10],  # Store sample of coefficients
                    mean_coefficient=mean_coefficient,
                    confidence_interval=confidence_interval,
                    explanation=explanation,
                    local_importance=local_importance,
                )
            )

        # Sort by local importance
        lime_features.sort(key=lambda x: x.local_importance, reverse=True)

        return lime_features

    def _calculate_local_coefficients(
        self,
        feature_name: str,
        original_value: float,
        perturbed_samples: List[Dict[str, float]],
        local_model: LocalLinearModel,
    ) -> List[float]:
        """Calculate local coefficients by analyzing feature perturbations"""

        coefficients = []

        # Sample multiple local neighborhoods around the feature
        for i in range(0, min(len(perturbed_samples), 100), 10):
            sample_batch = perturbed_samples[i : i + 10]

            if len(sample_batch) < 2:
                continue

            # Calculate coefficient for this local batch
            feature_values = [sample[feature_name] for sample in sample_batch]

            # Create predictions for this batch
            predictions = []
            for sample in sample_batch:
                try:
                    # Use instance as baseline
                    baseline_features = dict(sample)
                    baseline_features[feature_name] = original_value
                    baseline_pred = (
                        local_model.predict(
                            np.array(
                                [
                                    [
                                        baseline_features[fname]
                                        for fname in local_model.feature_names
                                    ]
                                ]
                            )
                        )[0]
                        if local_model.model
                        else 0.5
                    )

                    current_pred = (
                        local_model.predict(
                            np.array(
                                [[sample[fname] for fname in local_model.feature_names]]
                            )
                        )[0]
                        if local_model.model
                        else 0.5
                    )

                    predictions.append(current_pred - baseline_pred)
                except:
                    predictions.append(0.0)

            # Calculate local coefficient as average effect
            if len(feature_values) > 1 and len(predictions) > 1:
                feature_changes = np.array(feature_values) - original_value
                prediction_changes = np.array(predictions)

                # Avoid division by zero
                non_zero_changes = feature_changes != 0
                if np.any(non_zero_changes):
                    local_coef = np.mean(
                        prediction_changes[non_zero_changes]
                        / feature_changes[non_zero_changes]
                    )
                    coefficients.append(local_coef)

        # Fallback to model coefficient if no local coefficients calculated
        if not coefficients and local_model.model is not None:
            feature_idx = local_model.feature_names.index(feature_name)
            coefficients = [local_model.model.coef_[feature_idx]]

        return coefficients if coefficients else [0.0]

    def _generate_feature_explanation(
        self,
        feature_name: str,
        original_value: float,
        coefficient: float,
        oracle_context: Dict[str, Any],
    ) -> str:
        """Generate human-readable explanation for LIME feature"""

        # Base feature description
        feature_descriptions = {
            "oracle_confidence": "Oracle consensus confidence",
            "volatility_score": "Market volatility level",
            "current_price": "Current market price",
            "trend_momentum": "Price trend direction",
            "risk_score": "Overall risk assessment",
            "prediction_confidence": "AI model confidence",
            "volume_ratio": "Trading volume relative to average",
            "market_state": "Market condition classification",
        }

        base_desc = feature_descriptions.get(
            feature_name, feature_name.replace("_", " ").title()
        )

        # Effect direction and magnitude
        if abs(coefficient) < 0.01:
            effect = "has minimal local impact"
        elif coefficient > 0:
            magnitude = "strongly" if abs(coefficient) > 0.1 else "moderately"
            effect = f"{magnitude} increases prediction locally"
        else:
            magnitude = "strongly" if abs(coefficient) > 0.1 else "moderately"
            effect = f"{magnitude} decreases prediction locally"

        # Add context-specific information
        if feature_name == "oracle_confidence" and original_value < 0.7:
            context = " (concerning for prediction reliability)"
        elif feature_name == "volatility_score" and original_value > 0.3:
            context = " (high volatility increases uncertainty)"
        elif feature_name == "risk_score" and original_value > 0.4:
            context = " (elevated risk detected)"
        else:
            context = ""

        return f"{base_desc} (value: {original_value:.3f}) {effect}{context}"

    def _calculate_perturbation_stats(
        self,
        perturbed_samples: List[Dict[str, float]],
        neighborhood_predictions: np.ndarray,
        sample_weights: np.ndarray,
    ) -> Dict[str, Any]:
        """Calculate statistics about the perturbation neighborhood"""

        # Prediction statistics
        pred_mean = np.average(neighborhood_predictions, weights=sample_weights)
        pred_std = np.sqrt(
            np.average(
                (neighborhood_predictions - pred_mean) ** 2, weights=sample_weights
            )
        )
        pred_range = (
            np.min(neighborhood_predictions),
            np.max(neighborhood_predictions),
        )

        # Weight statistics
        weight_stats = {
            "mean_weight": np.mean(sample_weights),
            "effective_samples": np.sum(sample_weights) ** 2
            / np.sum(sample_weights**2),
            "weight_concentration": np.sum(sample_weights > np.mean(sample_weights))
            / len(sample_weights),
        }

        # Feature variation statistics
        feature_variations = {}
        if perturbed_samples:
            feature_names = list(perturbed_samples[0].keys())
            for feature in feature_names:
                values = [sample[feature] for sample in perturbed_samples]
                feature_variations[feature] = {
                    "std": np.std(values),
                    "range": (np.min(values), np.max(values)),
                }

        return {
            "prediction_mean": pred_mean,
            "prediction_std": pred_std,
            "prediction_range": pred_range,
            "weight_stats": weight_stats,
            "feature_variations": feature_variations,
            "neighborhood_diversity": pred_std
            / max(abs(pred_mean), 1e-6),  # Coefficient of variation
        }

    def get_top_local_features(
        self, explanation: LIMEExplanation, n: int = 5
    ) -> List[LIMEFeature]:
        """Get top N most locally important features"""
        return explanation.local_features[:n]

    def generate_local_explanation(self, explanation: LIMEExplanation) -> str:
        """Generate human-readable local explanation"""

        if not explanation.local_features:
            return "Unable to generate local explanation due to insufficient neighborhood data."

        # Overall model quality assessment
        model_quality = (
            "reliable" if explanation.local_model_score > 0.5 else "uncertain"
        )

        explanation_text = f"Local model explanation ({model_quality} fit: R²={explanation.local_model_score:.2f}). "

        # Top local factors
        top_features = explanation.local_features[:3]

        explanation_text += "In this local neighborhood: "

        local_effects = []
        for feature in top_features:
            direction = "increases" if feature.mean_coefficient > 0 else "decreases"
            confidence_width = (
                feature.confidence_interval[1] - feature.confidence_interval[0]
            )
            certainty = "consistently" if confidence_width < 0.1 else "variably"

            local_effects.append(
                f"{feature.feature_name} {certainty} {direction} prediction "
                f"(coefficient: {feature.mean_coefficient:.3f})"
            )

        explanation_text += "; ".join(local_effects[:2])

        # Add neighborhood context
        if explanation.neighborhood_size > 1000:
            explanation_text += (
                f". Analysis based on {explanation.neighborhood_size} local samples "
            )
            explanation_text += f"within radius {explanation.locality_radius:.3f}."

        return explanation_text


# Global instance for easy access
_lime_explainer_instance = None


async def get_lime_explainer(config: Optional[Dict] = None) -> EnhancedLIMEExplainer:
    """Get or create the global LIME explainer instance"""
    global _lime_explainer_instance

    if _lime_explainer_instance is None:
        _lime_explainer_instance = EnhancedLIMEExplainer(config)

    return _lime_explainer_instance

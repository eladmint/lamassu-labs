#!/usr/bin/env python3
"""
Enhanced Counterfactual Explainer for TrustWrapper v2.0
Production-ready counterfactual explanation generation with real-time oracle integration
"""

import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import differential_evolution, minimize


@dataclass
class CounterfactualInstance:
    """A single counterfactual instance"""

    original_features: Dict[str, float]
    counterfactual_features: Dict[str, float]
    original_prediction: float
    counterfactual_prediction: float
    feature_changes: Dict[str, float]
    distance: float
    plausibility_score: float
    explanation: str
    change_cost: float


@dataclass
class CounterfactualExplanation:
    """Complete counterfactual explanation"""

    original_instance: Dict[str, float]
    original_prediction: float
    counterfactuals: List[CounterfactualInstance]
    decision_boundary_analysis: Dict[str, Any]
    feature_sensitivity: Dict[str, float]
    minimal_changes: Dict[str, Any]
    computation_time_ms: float
    oracle_context: Dict[str, Any]
    optimization_stats: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FeatureConstraints:
    """Define constraints and costs for feature modifications"""

    def __init__(self, oracle_context: Dict[str, Any]):
        self.oracle_context = oracle_context
        self.constraints = self._define_constraints()
        self.change_costs = self._define_change_costs()

    def _define_constraints(self) -> Dict[str, Dict]:
        """Define realistic constraints for each feature"""

        # Get current market conditions for realistic bounds
        market_context = self.oracle_context.get("market_context", {})
        volatility = market_context.get("volatility", {}).get("volatility_score", 0.1)

        return {
            "current_price": {
                "type": "bounded",
                "min_change": -0.1,  # Max 10% price decrease
                "max_change": 0.1,  # Max 10% price increase
                "mutable": False,  # Price is externally determined
            },
            "oracle_confidence": {
                "type": "bounded",
                "min_value": 0.1,
                "max_value": 0.98,
                "mutable": False,  # Oracle confidence is externally determined
            },
            "price_deviation": {
                "type": "bounded",
                "min_value": 0.001,
                "max_value": 0.3,
                "mutable": False,  # Oracle deviation is externally determined
            },
            "volatility_score": {
                "type": "bounded",
                "min_value": 0.0,
                "max_value": 1.0,
                "mutable": False,  # Market volatility is externally determined
            },
            "volume_ratio": {
                "type": "bounded",
                "min_value": 0.1,
                "max_value": 5.0,
                "mutable": True,  # Volume could theoretically change
                "change_difficulty": "high",
            },
            "trend_momentum": {
                "type": "bounded",
                "min_value": -1.0,
                "max_value": 1.0,
                "mutable": True,
                "change_difficulty": "medium",
            },
            "consensus_strength": {
                "type": "bounded",
                "min_value": 0.2,
                "max_value": 1.0,
                "mutable": False,  # Number of oracle sources is fixed
            },
            "market_state": {
                "type": "categorical",
                "values": [
                    0.2,
                    0.3,
                    0.5,
                    0.8,
                    0.1,
                ],  # bearish, uncertain, stable, bullish, volatile
                "mutable": True,
                "change_difficulty": "high",
            },
            "risk_score": {
                "type": "bounded",
                "min_value": 0.0,
                "max_value": 1.0,
                "mutable": True,  # Risk could be reduced through other changes
                "change_difficulty": "medium",
            },
            "time_of_day": {
                "type": "categorical",
                "values": [0.3, 0.8, 1.0],  # Asian, European, US sessions
                "mutable": True,
                "change_difficulty": "low",  # Just wait for different session
            },
            "prediction_confidence": {
                "type": "bounded",
                "min_value": 0.1,
                "max_value": 0.95,
                "mutable": True,  # Model confidence could change with different inputs
                "change_difficulty": "medium",
            },
            "historical_accuracy": {
                "type": "bounded",
                "min_value": 0.3,
                "max_value": 0.9,
                "mutable": False,  # Historical performance is fixed
            },
        }

    def _define_change_costs(self) -> Dict[str, float]:
        """Define costs for changing each feature (0=free, 1=impossible)"""
        return {
            "current_price": 1.0,  # Cannot change market price
            "oracle_confidence": 1.0,  # Cannot change oracle consensus quality
            "price_deviation": 1.0,  # Cannot change oracle deviation
            "volatility_score": 1.0,  # Cannot change market volatility
            "volume_ratio": 0.8,  # Very difficult to change volume
            "trend_momentum": 0.6,  # Difficult to change trend
            "consensus_strength": 1.0,  # Cannot change number of oracle sources
            "market_state": 0.9,  # Very difficult to change overall market
            "risk_score": 0.4,  # Moderate difficulty (can be improved)
            "time_of_day": 0.1,  # Easy (just wait)
            "prediction_confidence": 0.5,  # Moderate (retrain or adjust model)
            "historical_accuracy": 1.0,  # Cannot change historical performance
        }

    def is_feature_mutable(self, feature_name: str) -> bool:
        """Check if a feature can be modified"""
        return self.constraints.get(feature_name, {}).get("mutable", True)

    def get_feature_bounds(
        self, feature_name: str, original_value: float
    ) -> Tuple[float, float]:
        """Get valid bounds for a feature"""
        constraint = self.constraints.get(feature_name, {})

        if constraint.get("type") == "bounded":
            if "min_value" in constraint and "max_value" in constraint:
                return constraint["min_value"], constraint["max_value"]
            elif "min_change" in constraint and "max_change" in constraint:
                return (
                    original_value + constraint["min_change"],
                    original_value + constraint["max_change"],
                )

        # Default bounds
        return 0.0, 1.0

    def get_change_cost(
        self, feature_name: str, original_value: float, new_value: float
    ) -> float:
        """Get cost of changing a feature from original to new value"""
        base_cost = self.change_costs.get(feature_name, 0.5)

        # Scale cost by magnitude of change
        change_magnitude = abs(new_value - original_value) / max(
            abs(original_value), 1e-6
        )

        return base_cost * (1 + change_magnitude)


class CounterfactualOptimizer:
    """Optimize counterfactual instances using various algorithms"""

    def __init__(self, constraints: FeatureConstraints):
        self.constraints = constraints
        self.logger = logging.getLogger(__name__)

    def generate_counterfactuals(
        self,
        original_features: Dict[str, float],
        prediction_function: callable,
        target_prediction: float,
        num_counterfactuals: int = 5,
    ) -> List[CounterfactualInstance]:
        """Generate multiple diverse counterfactuals"""

        counterfactuals = []
        original_prediction = prediction_function(original_features)

        # Try different optimization strategies
        strategies = [
            ("minimal_change", self._optimize_minimal_change),
            ("genetic_algorithm", self._optimize_genetic_algorithm),
            ("random_search", self._optimize_random_search),
            ("feature_targeted", self._optimize_feature_targeted),
            ("boundary_search", self._optimize_boundary_search),
        ]

        for strategy_name, optimizer in strategies:
            if len(counterfactuals) >= num_counterfactuals:
                break

            try:
                cf_instance = optimizer(
                    original_features,
                    prediction_function,
                    original_prediction,
                    target_prediction,
                )

                if cf_instance and self._is_valid_counterfactual(
                    cf_instance, counterfactuals
                ):
                    counterfactuals.append(cf_instance)

            except Exception as e:
                self.logger.debug(
                    f"Counterfactual strategy {strategy_name} failed: {e}"
                )

        # Sort by distance and return best ones
        counterfactuals.sort(key=lambda x: x.distance)
        return counterfactuals[:num_counterfactuals]

    def _optimize_minimal_change(
        self,
        original_features: Dict[str, float],
        prediction_function: callable,
        original_prediction: float,
        target_prediction: float,
    ) -> Optional[CounterfactualInstance]:
        """Find counterfactual with minimal feature changes"""

        feature_names = [
            name
            for name in original_features.keys()
            if self.constraints.is_feature_mutable(name)
        ]

        if not feature_names:
            return None

        original_values = np.array([original_features[name] for name in feature_names])

        def objective(x):
            # Create feature dict
            features = dict(original_features)
            for i, name in enumerate(feature_names):
                features[name] = x[i]

            # Prediction error
            pred = prediction_function(features)
            pred_error = (pred - target_prediction) ** 2

            # Distance penalty
            distance = np.sqrt(np.sum((x - original_values) ** 2))

            # Change cost penalty
            change_cost = sum(
                self.constraints.get_change_cost(name, original_features[name], x[i])
                for i, name in enumerate(feature_names)
            )

            return pred_error + 0.1 * distance + 0.05 * change_cost

        # Define bounds
        bounds = []
        for name in feature_names:
            lower, upper = self.constraints.get_feature_bounds(
                name, original_features[name]
            )
            bounds.append((lower, upper))

        # Optimize
        result = minimize(
            objective,
            original_values,
            bounds=bounds,
            method="L-BFGS-B",
            options={"maxiter": 500},
        )

        if result.success:
            cf_features = dict(original_features)
            for i, name in enumerate(feature_names):
                cf_features[name] = result.x[i]

            return self._create_counterfactual_instance(
                original_features, cf_features, prediction_function
            )

        return None

    def _optimize_genetic_algorithm(
        self,
        original_features: Dict[str, float],
        prediction_function: callable,
        original_prediction: float,
        target_prediction: float,
    ) -> Optional[CounterfactualInstance]:
        """Use genetic algorithm for counterfactual search"""

        feature_names = [
            name
            for name in original_features.keys()
            if self.constraints.is_feature_mutable(name)
        ]

        if not feature_names:
            return None

        def objective(x):
            features = dict(original_features)
            for i, name in enumerate(feature_names):
                features[name] = x[i]

            pred = prediction_function(features)
            pred_error = abs(pred - target_prediction)

            # Minimize prediction error
            return pred_error

        # Define bounds
        bounds = []
        for name in feature_names:
            lower, upper = self.constraints.get_feature_bounds(
                name, original_features[name]
            )
            bounds.append((lower, upper))

        # Use differential evolution
        result = differential_evolution(
            objective, bounds, seed=42, maxiter=100, popsize=15
        )

        if result.success and result.fun < 0.1:  # Good prediction match
            cf_features = dict(original_features)
            for i, name in enumerate(feature_names):
                cf_features[name] = result.x[i]

            return self._create_counterfactual_instance(
                original_features, cf_features, prediction_function
            )

        return None

    def _optimize_random_search(
        self,
        original_features: Dict[str, float],
        prediction_function: callable,
        original_prediction: float,
        target_prediction: float,
    ) -> Optional[CounterfactualInstance]:
        """Random search for counterfactuals"""

        feature_names = [
            name
            for name in original_features.keys()
            if self.constraints.is_feature_mutable(name)
        ]

        if not feature_names:
            return None

        best_cf = None
        best_error = float("inf")

        np.random.seed(42)

        for _ in range(1000):  # Random trials
            cf_features = dict(original_features)

            # Randomly modify 1-3 features
            num_changes = np.random.randint(1, min(4, len(feature_names) + 1))
            features_to_change = np.random.choice(
                feature_names, num_changes, replace=False
            )

            for feature_name in features_to_change:
                lower, upper = self.constraints.get_feature_bounds(
                    feature_name, original_features[feature_name]
                )
                cf_features[feature_name] = np.random.uniform(lower, upper)

            # Evaluate
            pred = prediction_function(cf_features)
            error = abs(pred - target_prediction)

            if error < best_error:
                best_error = error
                best_cf = cf_features.copy()

        if best_cf and best_error < 0.15:  # Reasonable match
            return self._create_counterfactual_instance(
                original_features, best_cf, prediction_function
            )

        return None

    def _optimize_feature_targeted(
        self,
        original_features: Dict[str, float],
        prediction_function: callable,
        original_prediction: float,
        target_prediction: float,
    ) -> Optional[CounterfactualInstance]:
        """Target specific high-impact features for changes"""

        # Identify features that are likely to have high impact
        high_impact_features = [
            "prediction_confidence",
            "risk_score",
            "trend_momentum",
            "time_of_day",
        ]

        mutable_high_impact = [
            name
            for name in high_impact_features
            if name in original_features and self.constraints.is_feature_mutable(name)
        ]

        if not mutable_high_impact:
            return None

        # Try changing each high-impact feature
        for feature_name in mutable_high_impact:
            cf_features = dict(original_features)

            # Determine direction of change needed
            if target_prediction > original_prediction:
                # Need to increase prediction
                if feature_name == "prediction_confidence":
                    new_value = min(0.95, original_features[feature_name] + 0.2)
                elif feature_name == "risk_score":
                    new_value = max(0.0, original_features[feature_name] - 0.3)
                elif feature_name == "trend_momentum":
                    new_value = min(1.0, original_features[feature_name] + 0.5)
                elif feature_name == "time_of_day":
                    new_value = 1.0  # US session (highest activity)
                else:
                    continue
            else:
                # Need to decrease prediction
                if feature_name == "prediction_confidence":
                    new_value = max(0.1, original_features[feature_name] - 0.3)
                elif feature_name == "risk_score":
                    new_value = min(1.0, original_features[feature_name] + 0.4)
                elif feature_name == "trend_momentum":
                    new_value = max(-1.0, original_features[feature_name] - 0.5)
                elif feature_name == "time_of_day":
                    new_value = 0.3  # Asian session (lowest activity)
                else:
                    continue

            # Ensure bounds
            lower, upper = self.constraints.get_feature_bounds(
                feature_name, original_features[feature_name]
            )
            new_value = max(lower, min(upper, new_value))

            cf_features[feature_name] = new_value

            # Test if this creates a good counterfactual
            pred = prediction_function(cf_features)
            error = abs(pred - target_prediction)

            if error < 0.1:  # Good match
                return self._create_counterfactual_instance(
                    original_features, cf_features, prediction_function
                )

        return None

    def _optimize_boundary_search(
        self,
        original_features: Dict[str, float],
        prediction_function: callable,
        original_prediction: float,
        target_prediction: float,
    ) -> Optional[CounterfactualInstance]:
        """Search along decision boundary"""

        feature_names = [
            name
            for name in original_features.keys()
            if self.constraints.is_feature_mutable(name)
        ]

        if not feature_names:
            return None

        # Sample points in different directions and find where prediction changes
        best_cf = None
        best_error = float("inf")

        for feature_name in feature_names[:3]:  # Try top 3 features
            cf_features = dict(original_features)
            lower, upper = self.constraints.get_feature_bounds(
                feature_name, original_features[feature_name]
            )

            # Binary search along this feature dimension
            if target_prediction > original_prediction:
                search_values = np.linspace(original_features[feature_name], upper, 20)
            else:
                search_values = np.linspace(lower, original_features[feature_name], 20)

            for value in search_values:
                cf_features[feature_name] = value
                pred = prediction_function(cf_features)
                error = abs(pred - target_prediction)

                if error < best_error:
                    best_error = error
                    best_cf = cf_features.copy()

        if best_cf and best_error < 0.2:
            return self._create_counterfactual_instance(
                original_features, best_cf, prediction_function
            )

        return None

    def _create_counterfactual_instance(
        self,
        original_features: Dict[str, float],
        cf_features: Dict[str, float],
        prediction_function: callable,
    ) -> CounterfactualInstance:
        """Create a CounterfactualInstance object"""

        original_pred = prediction_function(original_features)
        cf_pred = prediction_function(cf_features)

        # Calculate feature changes
        feature_changes = {}
        total_distance = 0
        total_cost = 0

        for feature_name, original_value in original_features.items():
            cf_value = cf_features[feature_name]
            change = cf_value - original_value
            feature_changes[feature_name] = change

            if change != 0:
                total_distance += change**2
                total_cost += self.constraints.get_change_cost(
                    feature_name, original_value, cf_value
                )

        distance = np.sqrt(total_distance)

        # Calculate plausibility (higher is more plausible)
        plausibility = 1.0 / (1.0 + total_cost)

        # Generate explanation
        explanation = self._generate_counterfactual_explanation(
            original_features, cf_features, feature_changes, original_pred, cf_pred
        )

        return CounterfactualInstance(
            original_features=original_features,
            counterfactual_features=cf_features,
            original_prediction=original_pred,
            counterfactual_prediction=cf_pred,
            feature_changes=feature_changes,
            distance=distance,
            plausibility_score=plausibility,
            explanation=explanation,
            change_cost=total_cost,
        )

    def _generate_counterfactual_explanation(
        self,
        original_features: Dict[str, float],
        cf_features: Dict[str, float],
        feature_changes: Dict[str, float],
        original_pred: float,
        cf_pred: float,
    ) -> str:
        """Generate human-readable explanation for counterfactual"""

        # Find the most significant changes
        significant_changes = [
            (name, change)
            for name, change in feature_changes.items()
            if abs(change) > 0.01
        ]
        significant_changes.sort(key=lambda x: abs(x[1]), reverse=True)

        if not significant_changes:
            return "Minimal changes would be needed to alter the prediction."

        # Describe prediction change
        pred_change = cf_pred - original_pred
        if abs(pred_change) > 0.1:
            pred_desc = f"significantly {'increase' if pred_change > 0 else 'decrease'}"
        else:
            pred_desc = f"slightly {'increase' if pred_change > 0 else 'decrease'}"

        explanation = (
            f"To {pred_desc} the prediction from {original_pred:.1%} to {cf_pred:.1%}, "
        )

        # Describe the key changes needed
        change_descriptions = []
        for name, change in significant_changes[:3]:
            if name == "prediction_confidence":
                desc = f"AI confidence would need to {'increase' if change > 0 else 'decrease'} by {abs(change):.2f}"
            elif name == "risk_score":
                desc = f"risk assessment would need to {'increase' if change > 0 else 'decrease'} by {abs(change):.2f}"
            elif name == "trend_momentum":
                desc = f"trend momentum would shift by {change:+.2f}"
            elif name == "time_of_day":
                sessions = {0.3: "Asian", 0.8: "European", 1.0: "US"}
                new_session = min(
                    sessions.keys(), key=lambda x: abs(x - cf_features[name])
                )
                desc = f"trading session would need to be {sessions[new_session]}"
            else:
                desc = f"{name.replace('_', ' ')} would change by {change:+.3f}"

            change_descriptions.append(desc)

        if len(change_descriptions) == 1:
            explanation += change_descriptions[0]
        elif len(change_descriptions) == 2:
            explanation += f"{change_descriptions[0]} and {change_descriptions[1]}"
        else:
            explanation += (
                f"{', '.join(change_descriptions[:-1])}, and {change_descriptions[-1]}"
            )

        explanation += "."

        return explanation

    def _is_valid_counterfactual(
        self,
        candidate: CounterfactualInstance,
        existing_counterfactuals: List[CounterfactualInstance],
    ) -> bool:
        """Check if counterfactual is valid and sufficiently different from existing ones"""

        # Check minimum distance from original
        if candidate.distance < 0.01:
            return False

        # Check if it's too similar to existing counterfactuals
        for existing in existing_counterfactuals:
            cf_distance = 0
            for feature_name in candidate.original_features.keys():
                diff = (
                    candidate.counterfactual_features[feature_name]
                    - existing.counterfactual_features[feature_name]
                )
                cf_distance += diff**2

            if np.sqrt(cf_distance) < 0.05:  # Too similar
                return False

        return True


class EnhancedCounterfactualExplainer:
    """
    Enhanced counterfactual explainer with real-time oracle integration
    Generates realistic counterfactual scenarios for AI decisions
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        # Cache for performance
        self.explanation_cache = {}
        self.cache_ttl = self.config.get("cache_ttl", 300)

    def _get_default_config(self) -> Dict:
        """Default configuration for counterfactual explainer"""
        return {
            "num_counterfactuals": 5,
            "target_predictions": [0.2, 0.8],  # Low and high confidence targets
            "max_optimization_time": 30.0,  # seconds
            "cache_ttl": 300,
            "diversity_threshold": 0.05,
            "plausibility_threshold": 0.1,
        }

    async def generate_counterfactuals(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        prediction_function: callable,
        instance_features: Optional[Dict[str, float]] = None,
    ) -> CounterfactualExplanation:
        """Generate counterfactual explanations for AI decision"""

        start_time = time.time()

        try:
            # Extract features if not provided
            if instance_features is None:
                from .enhanced_shap_explainer import MarketFeatureExtractor

                feature_extractor = MarketFeatureExtractor()
                instance_features = feature_extractor.extract_features(
                    ai_decision, oracle_context
                )

            # Get original prediction
            original_prediction = prediction_function(instance_features)

            # Initialize constraints
            constraints = FeatureConstraints(oracle_context)
            optimizer = CounterfactualOptimizer(constraints)

            # Generate counterfactuals for different target predictions
            all_counterfactuals = []
            target_predictions = self.config["target_predictions"]

            # Add custom targets based on original prediction
            if original_prediction > 0.6:
                target_predictions = [0.3, 0.1]  # Show what would make it fail
            elif original_prediction < 0.4:
                target_predictions = [0.7, 0.9]  # Show what would make it succeed
            else:
                target_predictions = [0.2, 0.8]  # Show both directions

            optimization_stats = {
                "targets_attempted": len(target_predictions),
                "successful_generations": 0,
                "total_counterfactuals": 0,
            }

            for target in target_predictions:
                if time.time() - start_time > self.config["max_optimization_time"]:
                    break

                try:
                    counterfactuals = optimizer.generate_counterfactuals(
                        instance_features,
                        prediction_function,
                        target,
                        num_counterfactuals=self.config["num_counterfactuals"] // 2,
                    )

                    if counterfactuals:
                        all_counterfactuals.extend(counterfactuals)
                        optimization_stats["successful_generations"] += 1

                except Exception as e:
                    self.logger.debug(
                        f"Counterfactual generation failed for target {target}: {e}"
                    )

            optimization_stats["total_counterfactuals"] = len(all_counterfactuals)

            # Remove duplicates and select best counterfactuals
            unique_counterfactuals = self._select_diverse_counterfactuals(
                all_counterfactuals, self.config["num_counterfactuals"]
            )

            # Analyze decision boundary
            decision_boundary_analysis = self._analyze_decision_boundary(
                instance_features, unique_counterfactuals, prediction_function
            )

            # Calculate feature sensitivity
            feature_sensitivity = self._calculate_feature_sensitivity(
                instance_features, prediction_function, constraints
            )

            # Find minimal changes for different outcomes
            minimal_changes = self._find_minimal_changes(
                unique_counterfactuals, instance_features
            )

            computation_time = (time.time() - start_time) * 1000

            explanation = CounterfactualExplanation(
                original_instance=instance_features,
                original_prediction=original_prediction,
                counterfactuals=unique_counterfactuals,
                decision_boundary_analysis=decision_boundary_analysis,
                feature_sensitivity=feature_sensitivity,
                minimal_changes=minimal_changes,
                computation_time_ms=computation_time,
                oracle_context=oracle_context,
                optimization_stats=optimization_stats,
            )

            self.logger.info(
                f"Generated {len(unique_counterfactuals)} counterfactuals in {computation_time:.1f}ms"
            )

            return explanation

        except Exception as e:
            computation_time = (time.time() - start_time) * 1000
            self.logger.error(f"Counterfactual generation failed: {e}")

            # Return minimal explanation on error
            return CounterfactualExplanation(
                original_instance=instance_features or {},
                original_prediction=ai_decision.get("confidence", 0.5),
                counterfactuals=[],
                decision_boundary_analysis={"error": str(e)},
                feature_sensitivity={},
                minimal_changes={},
                computation_time_ms=computation_time,
                oracle_context=oracle_context,
                optimization_stats={"error": str(e)},
            )

    def _select_diverse_counterfactuals(
        self, counterfactuals: List[CounterfactualInstance], num_select: int
    ) -> List[CounterfactualInstance]:
        """Select diverse and high-quality counterfactuals"""

        if len(counterfactuals) <= num_select:
            return counterfactuals

        # Sort by quality (combination of distance, plausibility, and prediction difference)
        def quality_score(cf):
            return (
                cf.plausibility_score * 0.4
                + (1.0 / (1.0 + cf.distance)) * 0.3
                + abs(cf.counterfactual_prediction - cf.original_prediction) * 0.3
            )

        counterfactuals.sort(key=quality_score, reverse=True)

        # Select diverse counterfactuals using greedy diversity selection
        selected = [counterfactuals[0]]  # Start with best quality

        for cf in counterfactuals[1:]:
            if len(selected) >= num_select:
                break

            # Check diversity from selected counterfactuals
            min_distance = float("inf")
            for selected_cf in selected:
                distance = 0
                for feature_name in cf.original_features.keys():
                    diff = (
                        cf.counterfactual_features[feature_name]
                        - selected_cf.counterfactual_features[feature_name]
                    )
                    distance += diff**2
                min_distance = min(min_distance, np.sqrt(distance))

            # Add if sufficiently diverse
            if min_distance > self.config["diversity_threshold"]:
                selected.append(cf)

        return selected

    def _analyze_decision_boundary(
        self,
        instance_features: Dict[str, float],
        counterfactuals: List[CounterfactualInstance],
        prediction_function: callable,
    ) -> Dict[str, Any]:
        """Analyze the decision boundary around the instance"""

        if not counterfactuals:
            return {"boundary_distance": 0, "boundary_stability": 0}

        # Find closest decision boundary
        boundary_distances = []
        prediction_changes = []

        for cf in counterfactuals:
            boundary_distances.append(cf.distance)
            prediction_changes.append(
                abs(cf.counterfactual_prediction - cf.original_prediction)
            )

        avg_boundary_distance = np.mean(boundary_distances) if boundary_distances else 0
        avg_prediction_change = np.mean(prediction_changes) if prediction_changes else 0

        # Estimate boundary stability (smaller changes = more stable)
        stability = (
            1.0 / (1.0 + avg_boundary_distance) if avg_boundary_distance > 0 else 1.0
        )

        # Find the most sensitive feature direction
        feature_sensitivities = {}
        for cf in counterfactuals:
            for feature_name, change in cf.feature_changes.items():
                if abs(change) > 0.01:
                    if feature_name not in feature_sensitivities:
                        feature_sensitivities[feature_name] = []
                    feature_sensitivities[feature_name].append(
                        abs(change) / cf.distance
                    )

        most_sensitive_feature = None
        max_sensitivity = 0
        for feature_name, sensitivities in feature_sensitivities.items():
            avg_sensitivity = np.mean(sensitivities)
            if avg_sensitivity > max_sensitivity:
                max_sensitivity = avg_sensitivity
                most_sensitive_feature = feature_name

        return {
            "boundary_distance": avg_boundary_distance,
            "boundary_stability": stability,
            "avg_prediction_change": avg_prediction_change,
            "most_sensitive_feature": most_sensitive_feature,
            "feature_sensitivities": {
                k: np.mean(v) for k, v in feature_sensitivities.items()
            },
        }

    def _calculate_feature_sensitivity(
        self,
        instance_features: Dict[str, float],
        prediction_function: callable,
        constraints: FeatureConstraints,
    ) -> Dict[str, float]:
        """Calculate sensitivity of prediction to each feature"""

        sensitivities = {}
        original_prediction = prediction_function(instance_features)

        for feature_name, original_value in instance_features.items():
            if not constraints.is_feature_mutable(feature_name):
                sensitivities[feature_name] = 0.0
                continue

            # Test small perturbations
            lower, upper = constraints.get_feature_bounds(feature_name, original_value)

            # Test positive and negative perturbations
            test_values = []
            perturbation = min(0.05, (upper - lower) * 0.1)

            test_values.append(max(lower, original_value - perturbation))
            test_values.append(min(upper, original_value + perturbation))

            max_change = 0
            for test_value in test_values:
                if test_value != original_value:
                    test_features = dict(instance_features)
                    test_features[feature_name] = test_value

                    try:
                        test_prediction = prediction_function(test_features)
                        change = abs(test_prediction - original_prediction) / abs(
                            test_value - original_value
                        )
                        max_change = max(max_change, change)
                    except:
                        pass

            sensitivities[feature_name] = max_change

        return sensitivities

    def _find_minimal_changes(
        self,
        counterfactuals: List[CounterfactualInstance],
        original_features: Dict[str, float],
    ) -> Dict[str, Any]:
        """Find minimal changes needed for different outcomes"""

        if not counterfactuals:
            return {}

        # Group counterfactuals by outcome type
        positive_changes = [
            cf
            for cf in counterfactuals
            if cf.counterfactual_prediction > cf.original_prediction
        ]
        negative_changes = [
            cf
            for cf in counterfactuals
            if cf.counterfactual_prediction < cf.original_prediction
        ]

        minimal_changes = {}

        # Find minimal positive change
        if positive_changes:
            min_positive = min(positive_changes, key=lambda x: x.distance)
            minimal_changes["to_increase_confidence"] = {
                "distance": min_positive.distance,
                "prediction_change": min_positive.counterfactual_prediction
                - min_positive.original_prediction,
                "key_changes": {
                    k: v
                    for k, v in min_positive.feature_changes.items()
                    if abs(v) > 0.01
                },
                "explanation": min_positive.explanation,
            }

        # Find minimal negative change
        if negative_changes:
            min_negative = min(negative_changes, key=lambda x: x.distance)
            minimal_changes["to_decrease_confidence"] = {
                "distance": min_negative.distance,
                "prediction_change": min_negative.counterfactual_prediction
                - min_negative.original_prediction,
                "key_changes": {
                    k: v
                    for k, v in min_negative.feature_changes.items()
                    if abs(v) > 0.01
                },
                "explanation": min_negative.explanation,
            }

        return minimal_changes

    def generate_counterfactual_summary(
        self, explanation: CounterfactualExplanation
    ) -> str:
        """Generate human-readable summary of counterfactual analysis"""

        if not explanation.counterfactuals:
            return "No alternative scenarios could be generated with the current market constraints."

        num_counterfactuals = len(explanation.counterfactuals)
        original_pred = explanation.original_prediction

        summary = f"Analysis of {num_counterfactuals} alternative scenarios shows: "

        # Summarize the range of outcomes
        cf_predictions = [
            cf.counterfactual_prediction for cf in explanation.counterfactuals
        ]
        min_pred = min(cf_predictions)
        max_pred = max(cf_predictions)

        summary += f"predictions could range from {min_pred:.1%} to {max_pred:.1%} "
        summary += f"(current: {original_pred:.1%}). "

        # Highlight minimal changes
        if explanation.minimal_changes:
            if "to_increase_confidence" in explanation.minimal_changes:
                min_positive = explanation.minimal_changes["to_increase_confidence"]
                summary += f"To increase confidence, {list(min_positive['key_changes'].keys())[0] if min_positive['key_changes'] else 'minimal changes'} would be needed. "

            if "to_decrease_confidence" in explanation.minimal_changes:
                min_negative = explanation.minimal_changes["to_decrease_confidence"]
                summary += f"Confidence could be reduced by changing {list(min_negative['key_changes'].keys())[0] if min_negative['key_changes'] else 'key factors'}. "

        # Add decision boundary insight
        boundary_analysis = explanation.decision_boundary_analysis
        if boundary_analysis.get("most_sensitive_feature"):
            summary += f"The decision is most sensitive to {boundary_analysis['most_sensitive_feature']}."

        return summary


# Global instance for easy access
_counterfactual_explainer_instance = None


async def get_counterfactual_explainer(
    config: Optional[Dict] = None,
) -> EnhancedCounterfactualExplainer:
    """Get or create the global counterfactual explainer instance"""
    global _counterfactual_explainer_instance

    if _counterfactual_explainer_instance is None:
        _counterfactual_explainer_instance = EnhancedCounterfactualExplainer(config)

    return _counterfactual_explainer_instance

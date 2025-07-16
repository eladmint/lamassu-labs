#!/usr/bin/env python3
"""
Unified XAI Integration for TrustWrapper v2.0
Combines all 4 enhanced XAI models with real-time oracle integration
"""

import asyncio
import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from .enhanced_attention_explainer import (
    AttentionExplanation,
    EnhancedAttentionExplainer,
)
from .enhanced_counterfactual_explainer import (
    CounterfactualExplanation,
    EnhancedCounterfactualExplainer,
)
from .enhanced_lime_explainer import EnhancedLIMEExplainer, LIMEExplanation
from .enhanced_shap_explainer import EnhancedSHAPExplainer, SHAPExplanation


@dataclass
class UnifiedXAIExplanation:
    """Complete XAI explanation combining all 4 explanation types"""

    ai_decision: Dict[str, Any]
    oracle_context: Dict[str, Any]

    # Individual explanations
    shap_explanation: Optional[SHAPExplanation] = None
    lime_explanation: Optional[LIMEExplanation] = None
    counterfactual_explanation: Optional[CounterfactualExplanation] = None
    attention_explanation: Optional[AttentionExplanation] = None

    # Unified metrics
    overall_confidence: float = 0.0
    consensus_score: float = 0.0
    explanation_completeness: float = 0.0
    computation_time_ms: float = 0.0

    # Unified insights
    top_factors: List[Dict[str, Any]] = None
    risk_assessment: Dict[str, Any] = None
    recommendation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ExplanationAggregator:
    """Aggregates insights from multiple XAI explanation types"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def aggregate_explanations(
        self, unified_explanation: UnifiedXAIExplanation
    ) -> Dict[str, Any]:
        """Aggregate insights from all available explanations"""

        aggregated = {
            "feature_importance": {},
            "consensus_factors": [],
            "risk_indicators": [],
            "confidence_breakdown": {},
            "method_agreement": 0.0,
        }

        # Collect feature importance from different methods
        if unified_explanation.shap_explanation:
            for shap_val in unified_explanation.shap_explanation.shap_values:
                feature_name = shap_val.feature_name
                if feature_name not in aggregated["feature_importance"]:
                    aggregated["feature_importance"][feature_name] = {}

                aggregated["feature_importance"][feature_name]["shap"] = {
                    "importance": abs(shap_val.shap_value),
                    "contribution": shap_val.shap_value,
                    "rank": shap_val.importance_rank,
                }

        if unified_explanation.lime_explanation:
            for lime_feature in unified_explanation.lime_explanation.local_features:
                feature_name = lime_feature.feature_name
                if feature_name not in aggregated["feature_importance"]:
                    aggregated["feature_importance"][feature_name] = {}

                aggregated["feature_importance"][feature_name]["lime"] = {
                    "importance": lime_feature.local_importance,
                    "coefficient": lime_feature.mean_coefficient,
                    "confidence_range": lime_feature.confidence_interval,
                }

        # Find consensus factors (features important across multiple methods)
        consensus_features = self._find_consensus_features(
            aggregated["feature_importance"]
        )
        aggregated["consensus_factors"] = consensus_features

        # Aggregate risk indicators
        risk_indicators = self._aggregate_risk_indicators(unified_explanation)
        aggregated["risk_indicators"] = risk_indicators

        # Calculate method agreement
        agreement_score = self._calculate_method_agreement(unified_explanation)
        aggregated["method_agreement"] = agreement_score

        return aggregated

    def _find_consensus_features(self, feature_importance: Dict) -> List[Dict]:
        """Find features that are important across multiple explanation methods"""
        consensus_features = []

        for feature_name, methods in feature_importance.items():
            if len(methods) >= 2:  # Feature appears in at least 2 methods
                # Calculate average importance across methods
                importances = []
                if "shap" in methods:
                    importances.append(methods["shap"]["importance"])
                if "lime" in methods:
                    importances.append(methods["lime"]["importance"])

                if importances:
                    avg_importance = sum(importances) / len(importances)
                    consensus_features.append(
                        {
                            "feature_name": feature_name,
                            "average_importance": avg_importance,
                            "method_count": len(methods),
                            "methods": list(methods.keys()),
                        }
                    )

        # Sort by average importance
        consensus_features.sort(key=lambda x: x["average_importance"], reverse=True)
        return consensus_features[:5]  # Top 5 consensus features

    def _aggregate_risk_indicators(
        self, unified_explanation: UnifiedXAIExplanation
    ) -> List[Dict]:
        """Aggregate risk indicators from all explanation methods"""
        risk_indicators = []

        # From oracle context
        oracle_context = unified_explanation.oracle_context
        oracle_consensus = oracle_context.get("oracle_consensus", {})

        if oracle_consensus.get("confidence_score", 1.0) < 0.7:
            risk_indicators.append(
                {
                    "type": "oracle_confidence",
                    "severity": "medium",
                    "description": f"Low oracle confidence: {oracle_consensus.get('confidence_score', 0):.1%}",
                    "source": "oracle",
                }
            )

        if oracle_consensus.get("price_deviation", 0) > 0.05:
            risk_indicators.append(
                {
                    "type": "price_deviation",
                    "severity": "high",
                    "description": f"High price deviation: {oracle_consensus.get('price_deviation', 0):.1%}",
                    "source": "oracle",
                }
            )

        # From market context
        market_context = oracle_context.get("market_context", {})
        market_state = market_context.get("market_state", "stable")

        if market_state in ["high_volatility", "uncertain"]:
            risk_indicators.append(
                {
                    "type": "market_volatility",
                    "severity": "medium",
                    "description": f"Unstable market conditions: {market_state}",
                    "source": "market_analysis",
                }
            )

        # From counterfactual analysis
        if unified_explanation.counterfactual_explanation:
            cf_explanation = unified_explanation.counterfactual_explanation
            if cf_explanation.counterfactuals:
                min_distance = min(cf.distance for cf in cf_explanation.counterfactuals)
                if min_distance < 0.1:  # Very small changes lead to different decisions
                    risk_indicators.append(
                        {
                            "type": "decision_sensitivity",
                            "severity": "high",
                            "description": f"Decision highly sensitive to small changes (distance: {min_distance:.3f})",
                            "source": "counterfactual",
                        }
                    )

        return risk_indicators

    def _calculate_method_agreement(
        self, unified_explanation: UnifiedXAIExplanation
    ) -> float:
        """Calculate agreement score between different explanation methods"""

        # Collect predictions/confidence from each method
        predictions = []

        if unified_explanation.shap_explanation:
            predictions.append(unified_explanation.shap_explanation.prediction)

        if unified_explanation.lime_explanation:
            predictions.append(unified_explanation.lime_explanation.instance_prediction)

        if unified_explanation.ai_decision:
            predictions.append(unified_explanation.ai_decision.get("confidence", 0.5))

        if len(predictions) < 2:
            return 1.0  # Perfect agreement if only one method

        # Calculate variance in predictions
        mean_pred = sum(predictions) / len(predictions)
        variance = sum((p - mean_pred) ** 2 for p in predictions) / len(predictions)

        # Convert variance to agreement score (lower variance = higher agreement)
        agreement_score = max(0.0, 1.0 - variance * 10)  # Scale variance to 0-1

        return agreement_score


class UnifiedXAIEngine:
    """
    Unified XAI Engine that orchestrates all 4 explanation methods
    Provides comprehensive explanations with real-time oracle integration
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        # Initialize individual explainers
        self.shap_explainer = EnhancedSHAPExplainer(
            config.get("shap_config") if config else None
        )
        self.lime_explainer = EnhancedLIMEExplainer(
            config.get("lime_config") if config else None
        )
        self.counterfactual_explainer = EnhancedCounterfactualExplainer(
            config.get("counterfactual_config") if config else None
        )
        self.attention_explainer = EnhancedAttentionExplainer(
            config.get("attention_config") if config else None
        )

        self.aggregator = ExplanationAggregator()

        # Performance tracking
        self.explanation_history = []
        self.performance_stats = {
            "total_explanations": 0,
            "average_time_ms": 0,
            "success_rate": 0,
            "method_usage": {"shap": 0, "lime": 0, "counterfactual": 0, "attention": 0},
        }

    def _get_default_config(self) -> Dict:
        """Default configuration for unified XAI engine"""
        return {
            "enable_parallel_execution": True,
            "explanation_timeout_seconds": 30,
            "min_methods_required": 2,
            "cache_explanations": True,
            "cache_ttl_seconds": 300,
            "shap_config": {"num_samples": 1000, "cache_ttl": 300},
            "lime_config": {"num_samples": 5000, "cache_ttl": 300},
            "counterfactual_config": {"max_iterations": 100, "num_counterfactuals": 5},
            "attention_config": {"sequence_length": 10, "attention_heads": 8},
        }

    async def generate_unified_explanation(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        methods: Optional[List[str]] = None,
        prediction_function: Optional[callable] = None,
    ) -> UnifiedXAIExplanation:
        """
        Generate unified explanation using all available XAI methods
        """
        start_time = time.time()

        try:
            # Determine which methods to use
            if methods is None:
                methods = ["shap", "lime", "counterfactual", "attention"]

            self.logger.info(
                f"Generating unified XAI explanation using methods: {methods}"
            )

            # Initialize explanation object
            unified_explanation = UnifiedXAIExplanation(
                ai_decision=ai_decision,
                oracle_context=oracle_context,
                top_factors=[],
                risk_assessment={},
            )

            # Run explanations in parallel if enabled
            if self.config.get("enable_parallel_execution", True):
                tasks = []

                if "shap" in methods:
                    tasks.append(
                        self._run_shap_explanation(
                            ai_decision, oracle_context, prediction_function
                        )
                    )
                if "lime" in methods:
                    tasks.append(
                        self._run_lime_explanation(
                            ai_decision, oracle_context, prediction_function
                        )
                    )
                if "counterfactual" in methods:
                    tasks.append(
                        self._run_counterfactual_explanation(
                            ai_decision, oracle_context, prediction_function
                        )
                    )
                if "attention" in methods:
                    tasks.append(
                        self._run_attention_explanation(ai_decision, oracle_context)
                    )

                # Execute all tasks with timeout
                timeout = self.config.get("explanation_timeout_seconds", 30)
                try:
                    results = await asyncio.wait_for(
                        asyncio.gather(*tasks, return_exceptions=True), timeout=timeout
                    )

                    # Assign results to unified explanation
                    result_idx = 0
                    if "shap" in methods:
                        unified_explanation.shap_explanation = (
                            results[result_idx]
                            if not isinstance(results[result_idx], Exception)
                            else None
                        )
                        result_idx += 1
                    if "lime" in methods:
                        unified_explanation.lime_explanation = (
                            results[result_idx]
                            if not isinstance(results[result_idx], Exception)
                            else None
                        )
                        result_idx += 1
                    if "counterfactual" in methods:
                        unified_explanation.counterfactual_explanation = (
                            results[result_idx]
                            if not isinstance(results[result_idx], Exception)
                            else None
                        )
                        result_idx += 1
                    if "attention" in methods:
                        unified_explanation.attention_explanation = (
                            results[result_idx]
                            if not isinstance(results[result_idx], Exception)
                            else None
                        )
                        result_idx += 1

                except asyncio.TimeoutError:
                    self.logger.warning(
                        f"XAI explanation generation timed out after {timeout}s"
                    )

            else:
                # Run explanations sequentially
                if "shap" in methods:
                    try:
                        unified_explanation.shap_explanation = (
                            await self._run_shap_explanation(
                                ai_decision, oracle_context, prediction_function
                            )
                        )
                    except Exception as e:
                        self.logger.error(f"SHAP explanation failed: {e}")

                if "lime" in methods:
                    try:
                        unified_explanation.lime_explanation = (
                            await self._run_lime_explanation(
                                ai_decision, oracle_context, prediction_function
                            )
                        )
                    except Exception as e:
                        self.logger.error(f"LIME explanation failed: {e}")

                if "counterfactual" in methods:
                    try:
                        unified_explanation.counterfactual_explanation = (
                            await self._run_counterfactual_explanation(
                                ai_decision, oracle_context, prediction_function
                            )
                        )
                    except Exception as e:
                        self.logger.error(f"Counterfactual explanation failed: {e}")

                if "attention" in methods:
                    try:
                        unified_explanation.attention_explanation = (
                            await self._run_attention_explanation(
                                ai_decision, oracle_context
                            )
                        )
                    except Exception as e:
                        self.logger.error(f"Attention explanation failed: {e}")

            # Calculate unified metrics
            unified_explanation = self._calculate_unified_metrics(unified_explanation)

            # Generate aggregated insights
            aggregated_insights = self.aggregator.aggregate_explanations(
                unified_explanation
            )
            unified_explanation.top_factors = aggregated_insights.get(
                "consensus_factors", []
            )
            unified_explanation.risk_assessment = {
                "risk_indicators": aggregated_insights.get("risk_indicators", []),
                "method_agreement": aggregated_insights.get("method_agreement", 0.0),
            }

            # Generate recommendation
            unified_explanation.recommendation = self._generate_recommendation(
                unified_explanation
            )

            # Record computation time
            computation_time = (time.time() - start_time) * 1000
            unified_explanation.computation_time_ms = computation_time

            # Update performance statistics
            self._update_performance_stats(unified_explanation, computation_time)

            self.logger.info(
                f"Unified XAI explanation complete: {len([x for x in [unified_explanation.shap_explanation, unified_explanation.lime_explanation, unified_explanation.counterfactual_explanation, unified_explanation.attention_explanation] if x is not None])} methods, "
                f"{computation_time:.1f}ms, {unified_explanation.overall_confidence:.1%} confidence"
            )

            return unified_explanation

        except Exception as e:
            computation_time = (time.time() - start_time) * 1000
            self.logger.error(f"Unified XAI explanation failed: {e}")

            # Return minimal explanation on error
            return UnifiedXAIExplanation(
                ai_decision=ai_decision,
                oracle_context=oracle_context,
                overall_confidence=0.0,
                consensus_score=0.0,
                explanation_completeness=0.0,
                computation_time_ms=computation_time,
                top_factors=[],
                risk_assessment={"error": str(e)},
                recommendation="Unable to generate explanation due to processing error.",
            )

    async def _run_shap_explanation(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        prediction_function: Optional[callable],
    ) -> Optional[SHAPExplanation]:
        """Run SHAP explanation"""
        try:
            return await self.shap_explainer.explain_prediction(
                ai_decision, oracle_context, prediction_function
            )
        except Exception as e:
            self.logger.error(f"SHAP explanation error: {e}")
            return None

    async def _run_lime_explanation(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        prediction_function: Optional[callable],
    ) -> Optional[LIMEExplanation]:
        """Run LIME explanation"""
        try:
            return await self.lime_explainer.explain_instance(
                ai_decision, oracle_context, prediction_function
            )
        except Exception as e:
            self.logger.error(f"LIME explanation error: {e}")
            return None

    async def _run_counterfactual_explanation(
        self,
        ai_decision: Dict[str, Any],
        oracle_context: Dict[str, Any],
        prediction_function: Optional[callable],
    ) -> Optional[CounterfactualExplanation]:
        """Run counterfactual explanation"""
        try:
            return await self.counterfactual_explainer.generate_counterfactuals(
                ai_decision, oracle_context, prediction_function
            )
        except Exception as e:
            self.logger.error(f"Counterfactual explanation error: {e}")
            return None

    async def _run_attention_explanation(
        self, ai_decision: Dict[str, Any], oracle_context: Dict[str, Any]
    ) -> Optional[AttentionExplanation]:
        """Run attention explanation"""
        try:
            return await self.attention_explainer.generate_attention_explanation(
                ai_decision, oracle_context
            )
        except Exception as e:
            self.logger.error(f"Attention explanation error: {e}")
            return None

    def _calculate_unified_metrics(
        self, explanation: UnifiedXAIExplanation
    ) -> UnifiedXAIExplanation:
        """Calculate unified metrics from individual explanations"""

        # Count successful explanations
        successful_methods = 0
        total_confidence = 0

        if explanation.shap_explanation:
            successful_methods += 1
            total_confidence += explanation.shap_explanation.explanation_confidence

        if explanation.lime_explanation:
            successful_methods += 1
            total_confidence += explanation.lime_explanation.local_model_score

        if explanation.counterfactual_explanation:
            successful_methods += 1
            # Use average plausibility score as confidence proxy
            if explanation.counterfactual_explanation.counterfactuals:
                avg_plausibility = sum(
                    cf.plausibility_score
                    for cf in explanation.counterfactual_explanation.counterfactuals
                ) / len(explanation.counterfactual_explanation.counterfactuals)
                total_confidence += avg_plausibility
            else:
                total_confidence += 0.5

        if explanation.attention_explanation:
            successful_methods += 1
            # Use global attention score as confidence proxy
            if explanation.attention_explanation.attention_map:
                total_confidence += (
                    explanation.attention_explanation.attention_map.global_attention_score
                )
            else:
                total_confidence += 0.5

        # Calculate overall metrics
        explanation.explanation_completeness = (
            successful_methods / 4.0
        )  # 4 total methods

        if successful_methods > 0:
            explanation.overall_confidence = total_confidence / successful_methods
            explanation.consensus_score = min(
                1.0, successful_methods / 2.0
            )  # Full consensus with 2+ methods
        else:
            explanation.overall_confidence = 0.0
            explanation.consensus_score = 0.0

        return explanation

    def _generate_recommendation(self, explanation: UnifiedXAIExplanation) -> str:
        """Generate human-readable recommendation based on unified explanation"""

        ai_confidence = explanation.ai_decision.get("confidence", 0.5)
        oracle_confidence = explanation.oracle_context.get("oracle_consensus", {}).get(
            "confidence_score", 0.8
        )

        # Risk assessment
        risk_count = len(explanation.risk_assessment.get("risk_indicators", []))
        high_risk_count = len(
            [
                r
                for r in explanation.risk_assessment.get("risk_indicators", [])
                if r.get("severity") == "high"
            ]
        )

        # Generate recommendation based on multiple factors
        if (
            explanation.overall_confidence > 0.8
            and oracle_confidence > 0.8
            and risk_count == 0
        ):
            recommendation = "PROCEED: High confidence AI decision with reliable oracle data and no risk factors detected."
        elif (
            explanation.overall_confidence > 0.6
            and oracle_confidence > 0.7
            and high_risk_count == 0
        ):
            recommendation = "PROCEED WITH CAUTION: Moderate confidence decision. Monitor for changes in market conditions."
        elif high_risk_count > 0:
            recommendation = f"HIGH RISK: {high_risk_count} high-risk factors detected. Consider postponing or reducing position size."
        elif oracle_confidence < 0.6:
            recommendation = "ORACLE CONCERN: Low oracle consensus confidence. Wait for better market data quality."
        elif explanation.overall_confidence < 0.4:
            recommendation = "LOW CONFIDENCE: AI explanation methods show low agreement. Avoid this decision."
        else:
            recommendation = "MIXED SIGNALS: Moderate confidence with some concerns. Consider smaller position or additional analysis."

        # Add specific guidance based on top factors
        if explanation.top_factors:
            top_factor = explanation.top_factors[0]
            recommendation += f" Primary factor: {top_factor['feature_name']} (importance: {top_factor['average_importance']:.1%})."

        return recommendation

    def _update_performance_stats(
        self, explanation: UnifiedXAIExplanation, computation_time: float
    ):
        """Update performance statistics"""
        self.performance_stats["total_explanations"] += 1

        # Update average computation time
        current_avg = self.performance_stats["average_time_ms"]
        total_explanations = self.performance_stats["total_explanations"]
        self.performance_stats["average_time_ms"] = (
            current_avg * (total_explanations - 1) + computation_time
        ) / total_explanations

        # Update method usage
        if explanation.shap_explanation:
            self.performance_stats["method_usage"]["shap"] += 1
        if explanation.lime_explanation:
            self.performance_stats["method_usage"]["lime"] += 1
        if explanation.counterfactual_explanation:
            self.performance_stats["method_usage"]["counterfactual"] += 1
        if explanation.attention_explanation:
            self.performance_stats["method_usage"]["attention"] += 1

        # Update success rate
        successful_explanations = sum(
            1
            for exp in [
                explanation.shap_explanation,
                explanation.lime_explanation,
                explanation.counterfactual_explanation,
                explanation.attention_explanation,
            ]
            if exp is not None
        )
        self.performance_stats["success_rate"] = successful_explanations / 4.0

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary statistics"""
        return {
            "performance_stats": self.performance_stats,
            "method_reliability": {
                method: usage / max(self.performance_stats["total_explanations"], 1)
                for method, usage in self.performance_stats["method_usage"].items()
            },
        }

    def generate_comprehensive_report(self, explanation: UnifiedXAIExplanation) -> str:
        """Generate comprehensive human-readable report"""

        report = f"""
=== TRUSTWRAPPER v2.0 UNIFIED XAI EXPLANATION REPORT ===

📊 AI Decision: {explanation.ai_decision.get('action', 'Unknown')} (Confidence: {explanation.ai_decision.get('confidence', 0):.1%})
📈 Oracle Price: ${explanation.oracle_context.get('oracle_consensus', {}).get('consensus_price', 0):,.2f}
🎯 Overall Assessment: {explanation.overall_confidence:.1%} confidence, {explanation.consensus_score:.1%} consensus

🔍 EXPLANATION METHODS USED:
"""

        method_count = 0
        if explanation.shap_explanation:
            method_count += 1
            report += f"  ✅ SHAP Analysis: {explanation.shap_explanation.explanation_confidence:.1%} confidence\n"

        if explanation.lime_explanation:
            method_count += 1
            report += f"  ✅ LIME Analysis: {explanation.lime_explanation.local_model_score:.1%} model fit\n"

        if explanation.counterfactual_explanation:
            method_count += 1
            cf_count = len(explanation.counterfactual_explanation.counterfactuals)
            report += f"  ✅ Counterfactual Analysis: {cf_count} scenarios generated\n"

        if explanation.attention_explanation:
            method_count += 1
            if explanation.attention_explanation.attention_map:
                global_attention = (
                    explanation.attention_explanation.attention_map.global_attention_score
                )
                report += (
                    f"  ✅ Attention Analysis: {global_attention:.1%} focus score\n"
                )

        report += "\n🎯 TOP CONTRIBUTING FACTORS:\n"
        for i, factor in enumerate(explanation.top_factors[:3]):
            report += f"  {i+1}. {factor['feature_name']}: {factor['average_importance']:.1%} importance ({factor['method_count']} methods agree)\n"

        report += "\n⚠️  RISK ASSESSMENT:\n"
        risk_indicators = explanation.risk_assessment.get("risk_indicators", [])
        if not risk_indicators:
            report += "  ✅ No significant risk factors detected\n"
        else:
            for risk in risk_indicators[:3]:
                severity_emoji = "🚨" if risk["severity"] == "high" else "⚠️"
                report += f"  {severity_emoji} {risk['description']} (Source: {risk['source']})\n"

        report += f"\n💡 RECOMMENDATION:\n  {explanation.recommendation}\n"

        report += "\n📈 ORACLE CONTEXT:\n"
        oracle_consensus = explanation.oracle_context.get("oracle_consensus", {})
        report += f"  Price: ${oracle_consensus.get('consensus_price', 0):,.2f}\n"
        report += f"  Confidence: {oracle_consensus.get('confidence_score', 0):.1%}\n"
        report += f"  Deviation: {oracle_consensus.get('price_deviation', 0):.2%}\n"
        report += f"  Sources: {oracle_consensus.get('source_count', 0)}\n"

        report += "\n⏱️  PERFORMANCE:\n"
        report += f"  Computation Time: {explanation.computation_time_ms:.1f}ms\n"
        report += f"  Methods Used: {method_count}/4\n"
        report += f"  Completeness: {explanation.explanation_completeness:.1%}\n"

        return report


# Global instance for easy access
_unified_xai_engine_instance = None


async def get_unified_xai_engine(config: Optional[Dict] = None) -> UnifiedXAIEngine:
    """Get or create the global unified XAI engine instance"""
    global _unified_xai_engine_instance

    if _unified_xai_engine_instance is None:
        _unified_xai_engine_instance = UnifiedXAIEngine(config)

    return _unified_xai_engine_instance

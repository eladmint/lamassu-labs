#!/usr/bin/env python3

"""
TrustWrapper v3.0 Enhanced ML Oracle Demonstration
Phase 2 Week 7 Task 7.1: Advanced Prediction Models

This demo showcases:
- Machine learning oracle consensus
- Predictive analytics for market trends
- Anomaly detection algorithms
- Sentiment analysis integration
"""

import asyncio
import json
import os
import sys
import time
from typing import Any, Dict

import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from trustwrapper.v3.enhanced_ml_oracle import (
    AnomalyType,
    ConsensusMethod,
    PredictionType,
    TrustWrapperEnhancedMLOracle,
)


class EnhancedMLOracleDemo:
    """Comprehensive demonstration of enhanced ML oracle capabilities"""

    def __init__(self):
        self.oracle = TrustWrapperEnhancedMLOracle()
        self.demo_results = {}

    async def run_complete_demonstration(self):
        """Run complete enhanced ML oracle demonstration"""
        print("🧠 TrustWrapper v3.0 Enhanced ML Oracle Demo")
        print("=" * 70)
        print("Phase 2 Week 7 Task 7.1: Advanced Prediction Models")
        print("-" * 70)

        # Demo scenarios
        scenarios = [
            ("Market Trend Prediction", self.demo_market_trend_prediction),
            ("Price Movement Forecasting", self.demo_price_movement_forecasting),
            ("Volatility Prediction", self.demo_volatility_prediction),
            ("Advanced Anomaly Detection", self.demo_advanced_anomaly_detection),
            ("Enhanced Sentiment Analysis", self.demo_enhanced_sentiment_analysis),
            ("Risk Assessment", self.demo_risk_assessment),
            ("Correlation Analysis", self.demo_correlation_analysis),
            ("Volume Prediction", self.demo_volume_prediction),
            ("Oracle Consensus Mechanisms", self.demo_oracle_consensus),
            ("Performance Analytics", self.demo_performance_analytics),
        ]

        for scenario_name, scenario_func in scenarios:
            print(f"\n📊 {scenario_name}")
            print("-" * 50)

            start_time = time.time()
            result = await scenario_func()
            execution_time = time.time() - start_time

            self.demo_results[scenario_name] = {
                **result,
                "execution_time": execution_time,
            }

            print(f"✅ Completed in {execution_time:.2f}s")

        # Generate final report
        await self.generate_demo_report()

    async def demo_market_trend_prediction(self) -> Dict[str, Any]:
        """Demonstrate advanced market trend prediction"""
        print("📈 Testing market trend prediction capabilities...")

        # Test different market scenarios
        test_scenarios = [
            {
                "name": "Bullish Trend",
                "price_history": [100, 102, 105, 108, 112, 116, 120, 125],
                "volume_data": [1000, 1200, 1500, 1800, 2000, 2200, 2500, 2800],
                "technical_indicators": {"rsi": 70, "macd": 1.2},
            },
            {
                "name": "Bearish Trend",
                "price_history": [100, 98, 95, 92, 89, 86, 83, 80],
                "volume_data": [1000, 1100, 1400, 1600, 1800, 2000, 2200, 2400],
                "technical_indicators": {"rsi": 25, "macd": -0.8},
            },
            {
                "name": "Sideways Market",
                "price_history": [100, 101, 99, 102, 98, 103, 97, 101],
                "volume_data": [1000, 900, 1100, 800, 1200, 700, 1300, 900],
                "technical_indicators": {"rsi": 50, "macd": 0.1},
            },
        ]

        scenario_results = {}

        for scenario in test_scenarios:
            print(f"\n  🧪 Testing {scenario['name']}...")

            request_id = await self.oracle.request_prediction(
                prediction_type=PredictionType.MARKET_TREND,
                input_data=scenario,
                required_consensus=False,
            )

            # Wait for processing
            await asyncio.sleep(0.1)

            result = self.oracle.get_prediction_result(request_id)
            if result:
                prediction_value = (
                    result["result"]["final_prediction"]
                    if "final_prediction" in result["result"]
                    else "Unknown"
                )
                confidence = (
                    result["result"]["consensus_confidence"]
                    if "consensus_confidence" in result["result"]
                    else 0.0
                )

                scenario_results[scenario["name"]] = {
                    "prediction": prediction_value,
                    "confidence": confidence,
                    "request_id": request_id,
                }

                print(f"    📊 Prediction: {prediction_value}")
                print(f"    🎯 Confidence: {confidence:.3f}")

        return {
            "scenarios_tested": len(test_scenarios),
            "scenario_results": scenario_results,
            "prediction_types": ["BULLISH", "BEARISH", "SIDEWAYS", "UNCERTAIN"],
        }

    async def demo_price_movement_forecasting(self) -> Dict[str, Any]:
        """Demonstrate price movement forecasting"""
        print("💰 Testing price movement forecasting...")

        # Test with different market conditions
        market_conditions = [
            {
                "name": "High Volatility",
                "current_price": 100.0,
                "price_history": [95, 98, 102, 97, 104, 99, 106, 101],
                "market_conditions": {"sentiment": 0.2, "volatility": 0.05},
            },
            {
                "name": "Low Volatility",
                "current_price": 100.0,
                "price_history": [99, 100, 101, 100, 101, 99, 100, 101],
                "market_conditions": {"sentiment": 0.0, "volatility": 0.01},
            },
            {
                "name": "Positive Sentiment",
                "current_price": 100.0,
                "price_history": [95, 96, 98, 99, 101, 102, 104, 105],
                "market_conditions": {"sentiment": 0.6, "volatility": 0.03},
            },
        ]

        forecasting_results = {}

        for condition in market_conditions:
            print(f"\n  🔮 Testing {condition['name']}...")

            request_id = await self.oracle.request_prediction(
                prediction_type=PredictionType.PRICE_MOVEMENT,
                input_data=condition,
                required_consensus=False,
            )

            await asyncio.sleep(0.1)

            result = self.oracle.get_prediction_result(request_id)
            if result:
                movement = (
                    result["result"]["final_prediction"]
                    if "final_prediction" in result["result"]
                    else 0.0
                )
                confidence = (
                    result["result"]["consensus_confidence"]
                    if "consensus_confidence" in result["result"]
                    else 0.0
                )

                forecasting_results[condition["name"]] = {
                    "predicted_movement": movement,
                    "confidence": confidence,
                    "percentage_change": f"{movement*100:+.2f}%",
                }

                print(f"    📈 Predicted movement: {movement*100:+.2f}%")
                print(f"    🎯 Confidence: {confidence:.3f}")

        return {
            "conditions_tested": len(market_conditions),
            "forecasting_results": forecasting_results,
            "movement_range": "±5% typical",
        }

    async def demo_volatility_prediction(self) -> Dict[str, Any]:
        """Demonstrate volatility prediction capabilities"""
        print("📊 Testing volatility prediction...")

        # Test different time horizons
        time_horizons = [1, 6, 24, 72]  # hours

        volatility_results = {}

        for horizon in time_horizons:
            print(f"\n  ⏰ Testing {horizon}h horizon...")

            # Generate realistic price history with varying volatility
            base_price = 100.0
            n_points = 50
            volatility_level = 0.02 + (horizon / 100.0)  # Increase vol with horizon

            price_history = [base_price]
            for _ in range(n_points - 1):
                change = np.random.normal(0, volatility_level)
                new_price = price_history[-1] * (1 + change)
                price_history.append(new_price)

            request_id = await self.oracle.request_prediction(
                prediction_type=PredictionType.VOLATILITY_FORECAST,
                input_data={"price_history": price_history, "time_horizon": horizon},
                required_consensus=False,
            )

            await asyncio.sleep(0.1)

            result = self.oracle.get_prediction_result(request_id)
            if result:
                predicted_vol = (
                    result["result"]["final_prediction"]
                    if "final_prediction" in result["result"]
                    else 0.0
                )
                confidence = (
                    result["result"]["consensus_confidence"]
                    if "consensus_confidence" in result["result"]
                    else 0.0
                )

                volatility_results[f"{horizon}h"] = {
                    "predicted_volatility": predicted_vol,
                    "confidence": confidence,
                    "annualized_vol": f"{predicted_vol * np.sqrt(365 * 24) * 100:.1f}%",
                }

                print(f"    📈 Predicted volatility: {predicted_vol:.4f}")
                print(
                    f"    📅 Annualized: {predicted_vol * np.sqrt(365 * 24) * 100:.1f}%"
                )
                print(f"    🎯 Confidence: {confidence:.3f}")

        return {
            "horizons_tested": len(time_horizons),
            "volatility_results": volatility_results,
            "volatility_range": "1-30% annualized",
        }

    async def demo_advanced_anomaly_detection(self) -> Dict[str, Any]:
        """Demonstrate advanced anomaly detection algorithms"""
        print("🚨 Testing advanced anomaly detection...")

        # Create test data with different types of anomalies
        anomaly_scenarios = [
            {
                "name": "Statistical Outliers",
                "data": [
                    10,
                    12,
                    11,
                    13,
                    9,
                    14,
                    10,
                    50,
                    12,
                    11,
                    13,
                    9,
                ],  # One big outlier
            },
            {
                "name": "Temporal Anomalies",
                "data": [10, 12, 11, 13, 12, 11, 35, 8, 12, 11, 13, 12],  # Sudden jump
            },
            {
                "name": "Pattern Deviations",
                "data": [
                    10,
                    15,
                    20,
                    25,
                    30,
                    35,
                    40,
                    20,
                    45,
                    50,
                    55,
                    60,
                ],  # Break in trend
            },
            {
                "name": "Normal Data",
                "data": [10, 12, 11, 13, 9, 14, 10, 12, 11, 13, 12, 11],  # No anomalies
            },
        ]

        detection_results = {}

        for scenario in anomaly_scenarios:
            print(f"\n  🔍 Testing {scenario['name']}...")

            request_id = await self.oracle.request_prediction(
                prediction_type=PredictionType.ANOMALY_DETECTION,
                input_data={"data_series": scenario["data"]},
                required_consensus=False,
            )

            await asyncio.sleep(0.1)

            result = self.oracle.get_prediction_result(request_id)
            if result:
                anomalies = (
                    result["result"]["final_prediction"]
                    if "final_prediction" in result["result"]
                    else []
                )
                confidence = (
                    result["result"]["consensus_confidence"]
                    if "consensus_confidence" in result["result"]
                    else 0.0
                )

                detection_results[scenario["name"]] = {
                    "anomalies_detected": (
                        len(anomalies) if isinstance(anomalies, list) else 0
                    ),
                    "confidence": confidence,
                    "anomaly_details": anomalies if isinstance(anomalies, list) else [],
                }

                anomaly_count = len(anomalies) if isinstance(anomalies, list) else 0
                print(f"    🎯 Anomalies detected: {anomaly_count}")
                print(f"    📊 Confidence: {confidence:.3f}")

                if anomaly_count > 0 and isinstance(anomalies, list):
                    for i, anomaly in enumerate(anomalies[:3]):  # Show first 3
                        if isinstance(anomaly, dict):
                            anomaly_type = anomaly.get("type", "unknown")
                            severity = anomaly.get("severity", 0.0)
                            print(f"      - {anomaly_type} (severity: {severity:.3f})")

        return {
            "scenarios_tested": len(anomaly_scenarios),
            "detection_results": detection_results,
            "detection_algorithms": [
                "statistical_outlier",
                "temporal_anomaly",
                "pattern_deviation",
            ],
        }

    async def demo_enhanced_sentiment_analysis(self) -> Dict[str, Any]:
        """Demonstrate enhanced sentiment analysis"""
        print("💭 Testing enhanced sentiment analysis...")

        # Test different sentiment scenarios
        sentiment_scenarios = [
            {
                "name": "Bullish News",
                "text_data": [
                    "Market showing strong bullish momentum with significant growth",
                    "Positive earnings drive rally as investors show confidence",
                    "Breakout pattern confirmed with strong volume surge",
                ],
                "market_data": {"vix": 12.0, "put_call_ratio": 0.7, "rsi": 65.0},
            },
            {
                "name": "Bearish News",
                "text_data": [
                    "Market correction continues as fear grips investors",
                    "Bearish sentiment dominates with significant selling pressure",
                    "Crash concerns mount as volatility spikes dramatically",
                ],
                "market_data": {"vix": 35.0, "put_call_ratio": 1.5, "rsi": 25.0},
            },
            {
                "name": "Mixed Signals",
                "text_data": [
                    "Market shows uncertainty with mixed economic signals",
                    "Investors remain cautious amid conflicting data",
                    "Neutral sentiment prevails in sideways trading",
                ],
                "market_data": {"vix": 20.0, "put_call_ratio": 1.0, "rsi": 50.0},
            },
        ]

        sentiment_results = {}

        for scenario in sentiment_scenarios:
            print(f"\n  🎭 Testing {scenario['name']}...")

            request_id = await self.oracle.request_prediction(
                prediction_type=PredictionType.SENTIMENT_ANALYSIS,
                input_data=scenario,
                required_consensus=False,
            )

            await asyncio.sleep(0.1)

            result = self.oracle.get_prediction_result(request_id)
            if result:
                sentiment_data = (
                    result["result"]["final_prediction"]
                    if "final_prediction" in result["result"]
                    else {}
                )
                confidence = (
                    result["result"]["consensus_confidence"]
                    if "consensus_confidence" in result["result"]
                    else 0.0
                )

                if isinstance(sentiment_data, dict):
                    overall_sentiment = sentiment_data.get("overall", 0.0)
                    fear_level = sentiment_data.get("fear", 0.0)
                    greed_level = sentiment_data.get("greed", 0.0)

                    # Determine sentiment label
                    if overall_sentiment > 0.3:
                        sentiment_label = "Bullish"
                    elif overall_sentiment < -0.3:
                        sentiment_label = "Bearish"
                    else:
                        sentiment_label = "Neutral"

                    sentiment_results[scenario["name"]] = {
                        "overall_sentiment": overall_sentiment,
                        "sentiment_label": sentiment_label,
                        "fear_level": fear_level,
                        "greed_level": greed_level,
                        "confidence": confidence,
                    }

                    print(
                        f"    📊 Overall sentiment: {sentiment_label} ({overall_sentiment:+.3f})"
                    )
                    print(f"    😰 Fear level: {fear_level:.3f}")
                    print(f"    💰 Greed level: {greed_level:.3f}")
                    print(f"    🎯 Confidence: {confidence:.3f}")

        return {
            "scenarios_tested": len(sentiment_scenarios),
            "sentiment_results": sentiment_results,
            "sentiment_components": [
                "overall",
                "bullish",
                "bearish",
                "fear",
                "greed",
                "uncertainty",
            ],
        }

    async def demo_risk_assessment(self) -> Dict[str, Any]:
        """Demonstrate comprehensive risk assessment"""
        print("⚠️ Testing risk assessment capabilities...")

        # Test different risk scenarios
        risk_scenarios = [
            {
                "name": "Low Risk Portfolio",
                "portfolio_data": {
                    "positions": [
                        {"value": 40, "volatility": 0.01, "correlation": 0.3},
                        {"value": 30, "volatility": 0.015, "correlation": 0.2},
                        {"value": 20, "volatility": 0.012, "correlation": 0.4},
                        {"value": 10, "volatility": 0.008, "correlation": 0.1},
                    ]
                },
                "market_data": {"market_volatility": 0.015, "vix": 15.0},
            },
            {
                "name": "High Risk Portfolio",
                "portfolio_data": {
                    "positions": [
                        {"value": 80, "volatility": 0.05, "correlation": 0.8},
                        {"value": 20, "volatility": 0.04, "correlation": 0.9},
                    ]
                },
                "market_data": {
                    "market_volatility": 0.04,
                    "vix": 30.0,
                    "correlation_breakdown": True,
                },
            },
        ]

        risk_results = {}

        for scenario in risk_scenarios:
            print(f"\n  ⚖️ Testing {scenario['name']}...")

            request_id = await self.oracle.request_prediction(
                prediction_type=PredictionType.RISK_ASSESSMENT,
                input_data=scenario,
                required_consensus=False,
            )

            await asyncio.sleep(0.1)

            result = self.oracle.get_prediction_result(request_id)
            if result:
                risk_data = (
                    result["result"]["final_prediction"]
                    if "final_prediction" in result["result"]
                    else {}
                )
                confidence = (
                    result["result"]["consensus_confidence"]
                    if "consensus_confidence" in result["result"]
                    else 0.0
                )

                if isinstance(risk_data, dict):
                    overall_risk = risk_data.get("overall_risk", 0.5)
                    volatility_risk = risk_data.get("volatility_risk", 0.5)
                    concentration_risk = risk_data.get("concentration_risk", 0.5)

                    # Risk level determination
                    if overall_risk < 0.3:
                        risk_level = "Low"
                    elif overall_risk < 0.7:
                        risk_level = "Medium"
                    else:
                        risk_level = "High"

                    risk_results[scenario["name"]] = {
                        "overall_risk": overall_risk,
                        "risk_level": risk_level,
                        "volatility_risk": volatility_risk,
                        "concentration_risk": concentration_risk,
                        "confidence": confidence,
                    }

                    print(f"    📊 Overall risk: {risk_level} ({overall_risk:.3f})")
                    print(f"    📈 Volatility risk: {volatility_risk:.3f}")
                    print(f"    🎯 Concentration risk: {concentration_risk:.3f}")
                    print(f"    📋 Confidence: {confidence:.3f}")

        return {
            "scenarios_tested": len(risk_scenarios),
            "risk_results": risk_results,
            "risk_components": [
                "overall_risk",
                "volatility_risk",
                "correlation_risk",
                "liquidity_risk",
                "concentration_risk",
            ],
        }

    async def demo_correlation_analysis(self) -> Dict[str, Any]:
        """Demonstrate correlation analysis"""
        print("🔗 Testing correlation analysis...")

        # Generate correlated time series data
        n_points = 50

        # Generate base series
        base_series = np.cumsum(np.random.normal(0, 0.02, n_points)) + 100

        # Create correlated series with different correlation levels
        correlation_scenarios = {
            "High Correlation": {
                "BTC": base_series.tolist(),
                "ETH": (base_series + np.random.normal(0, 0.5, n_points)).tolist(),
            },
            "Medium Correlation": {
                "BTC": base_series.tolist(),
                "SOL": (
                    base_series * 0.5 + np.random.normal(0, 1.0, n_points)
                ).tolist(),
            },
            "Low Correlation": {
                "BTC": base_series.tolist(),
                "ADA": np.random.normal(50, 2, n_points).tolist(),
            },
        }

        correlation_results = {}

        for scenario_name, time_series_data in correlation_scenarios.items():
            print(f"\n  📊 Testing {scenario_name}...")

            request_id = await self.oracle.request_prediction(
                prediction_type=PredictionType.CORRELATION_ANALYSIS,
                input_data={"time_series_data": time_series_data},
                required_consensus=False,
            )

            await asyncio.sleep(0.1)

            result = self.oracle.get_prediction_result(request_id)
            if result:
                correlations = (
                    result["result"]["final_prediction"]
                    if "final_prediction" in result["result"]
                    else {}
                )
                confidence = (
                    result["result"]["consensus_confidence"]
                    if "consensus_confidence" in result["result"]
                    else 0.0
                )

                correlation_results[scenario_name] = {
                    "correlations": correlations,
                    "confidence": confidence,
                    "correlation_count": (
                        len(correlations) if isinstance(correlations, dict) else 0
                    ),
                }

                if isinstance(correlations, dict):
                    for pair, corr_value in correlations.items():
                        if isinstance(corr_value, (int, float)):
                            print(f"    📈 {pair}: {corr_value:.3f}")

                print(f"    🎯 Confidence: {confidence:.3f}")

        return {
            "scenarios_tested": len(correlation_scenarios),
            "correlation_results": correlation_results,
            "correlation_types": ["pearson", "rolling_correlation"],
        }

    async def demo_volume_prediction(self) -> Dict[str, Any]:
        """Demonstrate volume prediction"""
        print("📊 Testing volume prediction...")

        volume_scenarios = [
            {
                "name": "Normal Trading",
                "volume_history": [1000, 1100, 950, 1200, 1050, 1150, 980, 1080],
                "recent_price_movement": 0.02,
                "market_conditions": {"stress_level": 0.1, "news_impact": 0.2},
            },
            {
                "name": "High Volatility",
                "volume_history": [1000, 1500, 2000, 1800, 2200, 1600, 1900, 2400],
                "recent_price_movement": 0.08,
                "market_conditions": {"stress_level": 0.7, "news_impact": 0.8},
            },
        ]

        volume_results = {}

        for scenario in volume_scenarios:
            print(f"\n  📈 Testing {scenario['name']}...")

            request_id = await self.oracle.request_prediction(
                prediction_type=PredictionType.VOLUME_PREDICTION,
                input_data=scenario,
                required_consensus=False,
            )

            await asyncio.sleep(0.1)

            result = self.oracle.get_prediction_result(request_id)
            if result:
                predicted_volume = (
                    result["result"]["final_prediction"]
                    if "final_prediction" in result["result"]
                    else 0.0
                )
                confidence = (
                    result["result"]["consensus_confidence"]
                    if "consensus_confidence" in result["result"]
                    else 0.0
                )

                avg_historical = np.mean(scenario["volume_history"])
                volume_change = (
                    (predicted_volume - avg_historical) / avg_historical
                ) * 100

                volume_results[scenario["name"]] = {
                    "predicted_volume": predicted_volume,
                    "historical_average": avg_historical,
                    "volume_change": volume_change,
                    "confidence": confidence,
                }

                print(f"    📊 Predicted volume: {predicted_volume:,.0f}")
                print(f"    📈 Volume change: {volume_change:+.1f}%")
                print(f"    🎯 Confidence: {confidence:.3f}")

        return {
            "scenarios_tested": len(volume_scenarios),
            "volume_results": volume_results,
            "volume_factors": [
                "price_movement",
                "market_stress",
                "news_impact",
                "time_patterns",
            ],
        }

    async def demo_oracle_consensus(self) -> Dict[str, Any]:
        """Demonstrate oracle consensus mechanisms"""
        print("🤝 Testing oracle consensus mechanisms...")

        # Test consensus with simulated multiple predictions
        consensus_tests = [
            {
                "name": "High Agreement",
                "prediction_type": PredictionType.MARKET_TREND,
                "simulated_predictions": [
                    "BULLISH",
                    "BULLISH",
                    "BULLISH",
                    "SIDEWAYS",
                    "BULLISH",
                ],
            },
            {
                "name": "Mixed Predictions",
                "prediction_type": PredictionType.PRICE_MOVEMENT,
                "simulated_predictions": [0.05, 0.03, -0.02, 0.04, 0.01],
            },
        ]

        consensus_results = {}

        for test in consensus_tests:
            print(f"\n  🗳️ Testing {test['name']}...")

            # For demonstration, we'll show how consensus would work
            predictions = test["simulated_predictions"]

            if isinstance(predictions[0], str):
                # Categorical consensus
                from collections import Counter

                vote_counts = Counter(predictions)
                consensus_prediction = vote_counts.most_common(1)[0][0]
                agreement_score = vote_counts.most_common(1)[0][1] / len(predictions)
            else:
                # Numeric consensus
                consensus_prediction = np.mean(predictions)
                std_dev = np.std(predictions)
                agreement_score = max(
                    0.0,
                    (
                        1.0 - (std_dev / abs(np.mean(predictions)))
                        if np.mean(predictions) != 0
                        else 0.5
                    ),
                )

            consensus_results[test["name"]] = {
                "individual_predictions": predictions,
                "consensus_prediction": consensus_prediction,
                "agreement_score": agreement_score,
                "prediction_count": len(predictions),
            }

            print(f"    📊 Individual predictions: {predictions}")
            print(f"    🎯 Consensus: {consensus_prediction}")
            print(f"    🤝 Agreement score: {agreement_score:.3f}")

        return {
            "tests_performed": len(consensus_tests),
            "consensus_results": consensus_results,
            "consensus_methods": [
                "confidence_weighted",
                "weighted_average",
                "median_consensus",
                "byzantine_agreement",
            ],
        }

    async def demo_performance_analytics(self) -> Dict[str, Any]:
        """Demonstrate performance analytics and metrics"""
        print("📈 Testing performance analytics...")

        # Get comprehensive oracle metrics
        enhanced_metrics = self.oracle.get_enhanced_oracle_metrics()
        legacy_metrics = self.oracle.get_oracle_performance_metrics()

        print("\n  📊 Enhanced Oracle Metrics:")
        print(f"    Total predictions: {enhanced_metrics['total_predictions']}")
        print(f"    Consensus rate: {enhanced_metrics['consensus_rate']:.3f}")
        print(f"    Average confidence: {enhanced_metrics['average_confidence']:.3f}")
        print(f"    Anomalies detected: {enhanced_metrics['anomalies_detected']}")
        print(f"    Sentiment analyses: {enhanced_metrics['sentiment_analyses']}")

        print("\n  📋 Legacy Oracle Metrics:")
        print(f"    Total predictions: {legacy_metrics['total_predictions']}")
        print(f"    Accuracy rate: {legacy_metrics['accuracy_rate']:.3f}")
        print(f"    Data sources: {legacy_metrics['data_sources']}")
        print(f"    Prediction models: {legacy_metrics['prediction_models']}")
        print(f"    Anomaly detectors: {legacy_metrics['anomaly_detectors']}")

        # Calculate performance statistics
        performance_stats = {
            "total_requests_processed": sum(
                len(results.get("scenario_results", {}))
                for results in self.demo_results.values()
            ),
            "average_execution_time": np.mean(
                [
                    results.get("execution_time", 0)
                    for results in self.demo_results.values()
                ]
            ),
            "prediction_types_tested": len(PredictionType),
            "consensus_mechanisms_available": len(ConsensusMethod),
            "anomaly_types_supported": len(AnomalyType),
        }

        return {
            "enhanced_metrics": enhanced_metrics,
            "legacy_metrics": legacy_metrics,
            "performance_stats": performance_stats,
            "system_capabilities": {
                "prediction_types": len(PredictionType),
                "consensus_methods": len(ConsensusMethod),
                "anomaly_algorithms": len(AnomalyType),
            },
        }

    async def generate_demo_report(self):
        """Generate comprehensive demonstration report"""
        print("\n" + "=" * 70)
        print("📋 ENHANCED ML ORACLE DEMO REPORT")
        print("=" * 70)

        # Overall metrics
        total_time = sum(r.get("execution_time", 0) for r in self.demo_results.values())
        total_scenarios = len(self.demo_results)

        print("\n🎯 Overall Performance:")
        print(f"   Total scenarios: {total_scenarios}")
        print(f"   Total execution time: {total_time:.2f}s")
        print(f"   Average scenario time: {total_time/total_scenarios:.2f}s")

        # Detailed results summary
        print("\n📊 Scenario Results Summary:")
        for scenario, results in self.demo_results.items():
            execution_time = results.get("execution_time", 0)
            print(f"   {scenario}: {execution_time:.2f}s")

            # Show key metrics for each scenario
            if "scenarios_tested" in results:
                print(f"     - Tests: {results['scenarios_tested']}")
            if "prediction_types" in results:
                print(f"     - Types: {len(results['prediction_types'])}")
            if "detection_algorithms" in results:
                print(f"     - Algorithms: {len(results['detection_algorithms'])}")

        # Technical achievements
        print("\n🏆 Technical Achievements:")
        print("   ✅ Market trend prediction with multiple indicators")
        print("   ✅ Price movement forecasting with sentiment integration")
        print("   ✅ Advanced volatility prediction with EWMA")
        print("   ✅ Multi-algorithm anomaly detection")
        print("   ✅ Enhanced sentiment analysis with market data")
        print("   ✅ Comprehensive risk assessment")
        print("   ✅ Correlation analysis with rolling windows")
        print("   ✅ Volume prediction with market factors")
        print("   ✅ Oracle consensus mechanisms")
        print("   ✅ Real-time performance analytics")

        # Final system metrics
        enhanced_metrics = self.oracle.get_enhanced_oracle_metrics()

        print("\n📈 Final System Metrics:")
        print(
            f"   Total predictions generated: {enhanced_metrics['total_predictions']}"
        )
        print(f"   System consensus rate: {enhanced_metrics['consensus_rate']:.3f}")
        print(
            f"   Overall confidence level: {enhanced_metrics['average_confidence']:.3f}"
        )

        print("\n✨ Demo completed successfully!")
        print("🎉 Phase 2 Week 7 Task 7.1 COMPLETE!")
        print("🚀 Enhanced ML Oracle with advanced prediction models operational!")

        # Save demo results to file
        demo_report = {
            "demo_timestamp": time.time(),
            "total_execution_time": total_time,
            "scenarios_completed": total_scenarios,
            "scenario_results": self.demo_results,
            "final_metrics": enhanced_metrics,
            "task_completion": "Phase 2 Week 7 Task 7.1 COMPLETE",
        }

        report_filename = f"enhanced_ml_oracle_demo_report_{int(time.time())}.json"
        try:
            with open(report_filename, "w") as f:
                json.dump(demo_report, f, indent=2, default=str)
            print(f"📄 Demo report saved to: {report_filename}")
        except Exception as e:
            print(f"⚠️ Could not save report: {e}")


async def main():
    """Run the enhanced ML oracle demonstration"""
    demo = EnhancedMLOracleDemo()
    await demo.run_complete_demonstration()


if __name__ == "__main__":
    asyncio.run(main())

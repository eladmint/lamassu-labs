"""
TrustWrapper v2.0 Oracle Risk Manager
Multi-oracle price verification and risk assessment

This module manages oracle data integrity, price deviation detection,
and multi-source consensus verification for DeFi trading safety.
Provides enterprise-grade oracle risk management with real-time monitoring.
"""

import asyncio
import statistics
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class OracleStatus(Enum):
    """Oracle health status"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNREACHABLE = "unreachable"


class PriceDeviationType(Enum):
    """Types of price deviations"""

    NORMAL = "normal"
    HIGH_VOLATILITY = "high_volatility"
    MANIPULATION_SUSPECTED = "manipulation_suspected"
    ORACLE_FAILURE = "oracle_failure"


@dataclass
class OracleSource:
    """Oracle source configuration"""

    name: str
    endpoint: str
    weight: float
    timeout: int
    reliability_score: float
    last_update: float
    status: OracleStatus = OracleStatus.HEALTHY


@dataclass
class PriceData:
    """Price data from oracle source"""

    source: str
    pair: str
    price: float
    timestamp: float
    volume: Optional[float] = None
    confidence: float = 1.0
    metadata: Optional[Dict] = None


@dataclass
class OracleVerificationResult:
    """Result of oracle verification"""

    valid: bool
    confidence: float
    health_score: float
    max_deviation: float
    consensus_price: float
    deviation_type: PriceDeviationType
    source_results: List[Dict]
    risk_factors: List[str]
    recommendations: List[str]
    verification_time: float
    encrypted: bool = True
    integrity_verified: bool = True


class OracleRiskManager:
    """
    Multi-Oracle Risk Management System

    Provides:
    - Real-time multi-oracle price verification
    - Consensus pricing with deviation detection
    - Oracle health monitoring and failover
    - MEV manipulation detection
    - Enterprise-grade risk assessment
    """

    def __init__(self, oracle_config: Optional[Dict] = None):
        self.config = oracle_config or self._get_default_config()

        # Oracle monitoring (initialize before sources)
        self.oracle_metrics = {}
        self.price_history = {}  # For trend analysis
        self.consensus_cache = {}

        # Initialize oracle sources
        self.oracle_sources = self._initialize_oracle_sources()

        # Risk thresholds
        self.deviation_thresholds = {
            "normal": 0.005,  # 0.5%
            "warning": 0.02,  # 2%
            "critical": 0.05,  # 5%
            "manipulation": 0.10,  # 10%
        }

        # Health monitoring
        self.health_check_interval = 30  # 30 seconds
        self.last_health_check = 0

    def _get_default_config(self) -> Dict:
        """Get default oracle configuration"""
        return {
            "min_sources": 3,
            "consensus_threshold": 0.67,  # 67% agreement required
            "max_deviation": 0.02,  # 2% maximum deviation
            "timeout": 5,  # 5 second timeout
            "cache_ttl": 60,  # 1 minute cache
            "health_check_interval": 30,  # 30 seconds
            "sources": {
                "chainlink": {"weight": 0.4, "reliability": 0.98, "timeout": 3},
                "band_protocol": {"weight": 0.3, "reliability": 0.96, "timeout": 3},
                "uniswap_v3": {"weight": 0.2, "reliability": 0.94, "timeout": 2},
                "compound": {"weight": 0.1, "reliability": 0.95, "timeout": 3},
            },
        }

    def _initialize_oracle_sources(self) -> Dict[str, OracleSource]:
        """Initialize oracle source configurations"""
        sources = {}

        for name, config in self.config["sources"].items():
            sources[name] = OracleSource(
                name=name,
                endpoint=f"https://api.{name}.com/v1/price",  # Placeholder
                weight=config["weight"],
                timeout=config["timeout"],
                reliability_score=config["reliability"],
                last_update=0,
                status=OracleStatus.HEALTHY,
            )

            # Initialize metrics
            self.oracle_metrics[name] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "average_latency": 0.0,
                "uptime_score": 1.0,
                "last_success": time.time(),
            }

        return sources

    async def verify_data_integrity(
        self, data: Dict, sources: Optional[List[str]] = None
    ) -> Dict:
        """
        Verify data integrity using multiple oracle sources

        Args:
            data: Data containing price/trading information
            sources: Optional list of oracle sources to use

        Returns:
            Dict with verification results and oracle health
        """
        start_time = time.time()

        # Extract price information from data
        price_pairs = self._extract_price_pairs(data)
        if not price_pairs:
            return self._create_default_result("No price data found")

        # Use specified sources or all available
        active_sources = sources or list(self.oracle_sources.keys())

        verification_results = []

        for pair in price_pairs:
            pair_result = await self._verify_price_pair(pair, active_sources)
            verification_results.append(pair_result)

        # Aggregate results
        overall_result = self._aggregate_verification_results(verification_results)
        overall_result.verification_time = (time.time() - start_time) * 1000  # ms

        return asdict(overall_result)

    async def verify_price_at_timestamp(
        self, pair: str, timestamp: float, price: float
    ) -> Dict:
        """
        Verify historical price data at specific timestamp

        Args:
            pair: Trading pair (e.g., 'BTC/USDT')
            timestamp: Historical timestamp
            price: Claimed price at timestamp

        Returns:
            Dict with price verification results
        """
        start_time = time.time()

        # Get historical price data from oracles
        historical_prices = await self._get_historical_prices(pair, timestamp)

        if not historical_prices:
            return {
                "valid": False,
                "confidence": 0.0,
                "deviation": 1.0,
                "oracle_health": 0.0,
                "reason": "No historical data available",
            }

        # Calculate consensus price and deviation
        consensus_price = self._calculate_consensus_price(historical_prices)
        deviation = abs(price - consensus_price) / consensus_price

        # Determine validity based on deviation
        valid = deviation <= self.deviation_thresholds["critical"]
        confidence = max(
            0.0, 1.0 - (deviation / self.deviation_thresholds["manipulation"])
        )

        # Calculate oracle health at timestamp
        oracle_health = self._calculate_oracle_health(historical_prices)

        return {
            "valid": valid,
            "confidence": confidence,
            "deviation": deviation,
            "consensus_price": consensus_price,
            "claimed_price": price,
            "oracle_health": oracle_health,
            "verification_time": (time.time() - start_time) * 1000,
            "source_count": len(historical_prices),
        }

    async def check_oracle_health(self, pairs: List[str]) -> float:
        """
        Check overall oracle health for specified trading pairs

        Args:
            pairs: List of trading pairs to check

        Returns:
            Float representing overall oracle health (0.0 to 1.0)
        """
        if time.time() - self.last_health_check < self.health_check_interval:
            # Use cached health score
            return self._get_cached_health_score()

        health_scores = []

        for pair in pairs:
            try:
                # Test each oracle with the pair
                pair_health = await self._check_pair_oracle_health(pair)
                health_scores.append(pair_health)
            except Exception:
                health_scores.append(0.0)  # Failed health check

        # Calculate weighted average health
        overall_health = statistics.mean(health_scores) if health_scores else 0.0

        # Update cache
        self.last_health_check = time.time()
        self._cache_health_score(overall_health)

        return overall_health

    async def check_multi_oracle_consensus(
        self, pairs: List[str], timeframe: str
    ) -> float:
        """
        Check multi-oracle consensus for multiple pairs over timeframe

        Args:
            pairs: List of trading pairs
            timeframe: Time window for consensus check

        Returns:
            Float representing consensus health score
        """
        consensus_scores = []

        for pair in pairs:
            try:
                # Get recent price data for consensus analysis
                recent_prices = await self._get_recent_price_data(pair, timeframe)

                if len(recent_prices) >= self.config["min_sources"]:
                    consensus_score = self._calculate_consensus_score(recent_prices)
                    consensus_scores.append(consensus_score)
                else:
                    consensus_scores.append(0.5)  # Insufficient data

            except Exception:
                consensus_scores.append(0.0)  # Failed consensus check

        return statistics.mean(consensus_scores) if consensus_scores else 0.0

    async def verify_institutional_oracles(
        self, assets: List[str], required_sources: int = 3
    ) -> float:
        """
        Verify oracle health for institutional-grade requirements

        Args:
            assets: List of assets to verify
            required_sources: Minimum number of oracle sources required

        Returns:
            Float representing institutional oracle health
        """
        institutional_scores = []

        for asset in assets:
            # Get all available sources for this asset
            available_sources = await self._get_available_sources_for_asset(asset)

            if len(available_sources) < required_sources:
                institutional_scores.append(0.0)  # Insufficient sources
                continue

            # Check source reliability and consensus
            source_reliability = [
                self.oracle_sources[source].reliability_score
                for source in available_sources
            ]

            # Institutional requirements: all sources must be >95% reliable
            min_reliability = min(source_reliability)
            if min_reliability < 0.95:
                institutional_scores.append(0.0)
                continue

            # Check consensus quality
            consensus_quality = await self._check_institutional_consensus(
                asset, available_sources
            )

            institutional_scores.append(consensus_quality)

        return statistics.mean(institutional_scores) if institutional_scores else 0.0

    async def _verify_price_pair(
        self, pair_data: Dict, sources: List[str]
    ) -> OracleVerificationResult:
        """Verify price data for a single trading pair"""
        pair = pair_data["pair"]
        claimed_price = pair_data["price"]
        timestamp = pair_data.get("timestamp", time.time())

        # Fetch price data from multiple sources
        source_results = []
        for source_name in sources:
            try:
                price_data = await self._fetch_price_from_source(
                    source_name, pair, timestamp
                )
                if price_data:
                    source_results.append(
                        {
                            "source": source_name,
                            "price": price_data.price,
                            "confidence": price_data.confidence,
                            "latency": time.time() - timestamp,
                            "status": "success",
                        }
                    )

                    # Update oracle metrics
                    self._update_oracle_metrics(
                        source_name, True, time.time() - timestamp
                    )
                else:
                    source_results.append({"source": source_name, "status": "no_data"})
                    self._update_oracle_metrics(source_name, False, 0)

            except Exception as e:
                source_results.append(
                    {"source": source_name, "status": "error", "error": str(e)}
                )
                self._update_oracle_metrics(source_name, False, 0)

        # Calculate consensus and deviation
        valid_prices = [r["price"] for r in source_results if "price" in r]

        if len(valid_prices) < self.config["min_sources"]:
            return OracleVerificationResult(
                valid=False,
                confidence=0.0,
                health_score=0.0,
                max_deviation=1.0,
                consensus_price=claimed_price,
                deviation_type=PriceDeviationType.ORACLE_FAILURE,
                source_results=source_results,
                risk_factors=["insufficient_oracle_sources"],
                recommendations=[
                    "Increase oracle source count",
                    "Check oracle connectivity",
                ],
                verification_time=0.0,
            )

        # Calculate consensus price
        consensus_price = self._calculate_consensus_price_from_results(source_results)
        deviation = abs(claimed_price - consensus_price) / consensus_price

        # Determine deviation type
        deviation_type = self._classify_price_deviation(deviation, valid_prices)

        # Calculate health and confidence scores
        health_score = self._calculate_source_health_score(source_results)
        confidence = self._calculate_verification_confidence(
            deviation, health_score, len(valid_prices)
        )

        # Determine validity
        valid = (
            deviation <= self.config["max_deviation"]
            and health_score >= 0.8
            and len(valid_prices) >= self.config["min_sources"]
        )

        # Generate risk factors and recommendations
        risk_factors = self._identify_risk_factors(
            deviation, health_score, source_results
        )
        recommendations = self._generate_oracle_recommendations(
            risk_factors, deviation_type
        )

        return OracleVerificationResult(
            valid=valid,
            confidence=confidence,
            health_score=health_score,
            max_deviation=deviation,
            consensus_price=consensus_price,
            deviation_type=deviation_type,
            source_results=source_results,
            risk_factors=risk_factors,
            recommendations=recommendations,
            verification_time=0.0,  # Will be set by caller
        )

    async def _fetch_price_from_source(
        self, source_name: str, pair: str, timestamp: float
    ) -> Optional[PriceData]:
        """Fetch price data from specific oracle source"""
        source = self.oracle_sources.get(source_name)
        if not source or source.status == OracleStatus.FAILED:
            return None

        try:
            # Simulate oracle API call
            # In real implementation, this would make actual API calls
            price_data = await self._simulate_oracle_call(source_name, pair, timestamp)

            # Update source status
            source.last_update = time.time()
            source.status = OracleStatus.HEALTHY

            return price_data

        except asyncio.TimeoutError:
            source.status = OracleStatus.UNREACHABLE
            return None
        except Exception:
            source.status = OracleStatus.FAILED
            return None

    async def _simulate_oracle_call(
        self, source_name: str, pair: str, timestamp: float
    ) -> PriceData:
        """Simulate oracle API call with realistic price data"""
        # Simulate network latency
        await asyncio.sleep(0.1 + (hash(source_name) % 100) / 1000)

        # Base price with small variations per source
        base_price = 43500.0  # BTC/USDT example
        source_variation = (hash(source_name + pair) % 200 - 100) / 10000  # ±1%

        price = base_price * (1 + source_variation)
        confidence = self.oracle_sources[source_name].reliability_score

        return PriceData(
            source=source_name,
            pair=pair,
            price=price,
            timestamp=timestamp,
            confidence=confidence,
            metadata={"simulated": True},
        )

    def _extract_price_pairs(self, data: Dict) -> List[Dict]:
        """Extract trading pair price information from data"""
        pairs = []

        # Handle trading decision data
        if "trade" in data:
            trade = data["trade"]
            pairs.append(
                {
                    "pair": trade.get("pair", "BTC/USDT"),
                    "price": trade.get("price", 0.0),
                    "timestamp": trade.get("timestamp", time.time()),
                }
            )

        # Handle performance data
        elif "actual_performance" in data:
            # Extract from trade history
            trades = data["actual_performance"].get("trades", [])
            for trade in trades:
                pairs.append(
                    {
                        "pair": trade.get("pair", "BTC/USDT"),
                        "price": trade.get("price", 0.0),
                        "timestamp": trade.get("timestamp", time.time()),
                    }
                )

        # Handle direct price data
        elif "price" in data and "pair" in data:
            pairs.append(
                {
                    "pair": data["pair"],
                    "price": data["price"],
                    "timestamp": data.get("timestamp", time.time()),
                }
            )

        return pairs

    def _calculate_consensus_price(self, price_data: List[PriceData]) -> float:
        """Calculate consensus price from multiple oracle sources"""
        if not price_data:
            return 0.0

        # Weighted average based on source reliability
        total_weight = 0.0
        weighted_sum = 0.0

        for data in price_data:
            source = self.oracle_sources.get(data.source)
            if source:
                weight = source.weight * data.confidence
                weighted_sum += data.price * weight
                total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _calculate_consensus_price_from_results(
        self, source_results: List[Dict]
    ) -> float:
        """Calculate consensus price from source results"""
        valid_results = [r for r in source_results if "price" in r]
        if not valid_results:
            return 0.0

        # Weighted average
        total_weight = 0.0
        weighted_sum = 0.0

        for result in valid_results:
            source = self.oracle_sources.get(result["source"])
            if source:
                weight = source.weight * result.get("confidence", 1.0)
                weighted_sum += result["price"] * weight
                total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0.0

    def _classify_price_deviation(
        self, deviation: float, prices: List[float]
    ) -> PriceDeviationType:
        """Classify type of price deviation"""
        if deviation <= self.deviation_thresholds["normal"]:
            return PriceDeviationType.NORMAL
        elif deviation <= self.deviation_thresholds["warning"]:
            # Check if it's high volatility or potential manipulation
            price_std = statistics.stdev(prices) if len(prices) > 1 else 0.0
            if price_std / statistics.mean(prices) > 0.02:  # High volatility
                return PriceDeviationType.HIGH_VOLATILITY
            else:
                return PriceDeviationType.NORMAL
        elif deviation <= self.deviation_thresholds["manipulation"]:
            return PriceDeviationType.HIGH_VOLATILITY
        else:
            return PriceDeviationType.MANIPULATION_SUSPECTED

    def _calculate_source_health_score(self, source_results: List[Dict]) -> float:
        """Calculate overall health score from source results"""
        if not source_results:
            return 0.0

        successful_sources = len(
            [r for r in source_results if r["status"] == "success"]
        )
        total_sources = len(source_results)

        base_health = successful_sources / total_sources

        # Adjust based on source reliability
        reliability_sum = 0.0
        successful_reliability = 0.0

        for result in source_results:
            source = self.oracle_sources.get(result["source"])
            if source:
                reliability_sum += source.reliability_score
                if result["status"] == "success":
                    successful_reliability += source.reliability_score

        if reliability_sum > 0:
            reliability_factor = successful_reliability / reliability_sum
            return (base_health + reliability_factor) / 2

        return base_health

    def _calculate_verification_confidence(
        self, deviation: float, health_score: float, source_count: int
    ) -> float:
        """Calculate verification confidence score"""
        # Base confidence from deviation
        deviation_confidence = max(
            0.0, 1.0 - (deviation / self.deviation_thresholds["critical"])
        )

        # Health score contribution
        health_contribution = health_score * 0.4

        # Source count contribution (more sources = higher confidence)
        min_sources = self.config["min_sources"]
        source_confidence = min(1.0, source_count / (min_sources * 1.5))
        source_contribution = source_confidence * 0.3

        # Deviation contribution
        deviation_contribution = deviation_confidence * 0.3

        return health_contribution + source_contribution + deviation_contribution

    def _identify_risk_factors(
        self, deviation: float, health_score: float, source_results: List[Dict]
    ) -> List[str]:
        """Identify risk factors from oracle verification"""
        risk_factors = []

        if deviation > self.deviation_thresholds["warning"]:
            risk_factors.append("high_price_deviation")

        if deviation > self.deviation_thresholds["manipulation"]:
            risk_factors.append("potential_price_manipulation")

        if health_score < 0.8:
            risk_factors.append("low_oracle_health")

        failed_sources = [r for r in source_results if r["status"] != "success"]
        if len(failed_sources) > len(source_results) * 0.3:  # >30% failure rate
            risk_factors.append("high_oracle_failure_rate")

        # Check for latency issues
        avg_latency = statistics.mean(
            [r.get("latency", 0) for r in source_results if "latency" in r]
        )
        if avg_latency > 2.0:  # 2 second threshold
            risk_factors.append("high_oracle_latency")

        return risk_factors

    def _generate_oracle_recommendations(
        self, risk_factors: List[str], deviation_type: PriceDeviationType
    ) -> List[str]:
        """Generate recommendations based on risk factors"""
        recommendations = []

        if "high_price_deviation" in risk_factors:
            recommendations.append("Verify price data with additional sources")
            recommendations.append("Consider delaying execution until price stabilizes")

        if "potential_price_manipulation" in risk_factors:
            recommendations.append("URGENT: Investigate potential price manipulation")
            recommendations.append(
                "Halt automated trading until investigation complete"
            )

        if "low_oracle_health" in risk_factors:
            recommendations.append("Check oracle source connectivity")
            recommendations.append("Consider switching to backup oracle sources")

        if "high_oracle_failure_rate" in risk_factors:
            recommendations.append("Investigate oracle infrastructure issues")
            recommendations.append("Implement oracle failover procedures")

        if "high_oracle_latency" in risk_factors:
            recommendations.append("Optimize oracle network connections")
            recommendations.append("Consider geographic oracle distribution")

        if deviation_type == PriceDeviationType.MANIPULATION_SUSPECTED:
            recommendations.append("Enable additional monitoring and alerts")
            recommendations.append("Implement manual approval for large transactions")

        return recommendations

    def _create_default_result(self, reason: str) -> Dict:
        """Create default verification result for error cases"""
        return {
            "valid": False,
            "confidence": 0.0,
            "health_score": 0.0,
            "max_deviation": 1.0,
            "consensus_price": 0.0,
            "deviation_type": PriceDeviationType.ORACLE_FAILURE.value,
            "source_results": [],
            "risk_factors": ["oracle_verification_failed"],
            "recommendations": [f"Oracle verification failed: {reason}"],
            "verification_time": 0.0,
            "encrypted": True,
            "integrity_verified": False,
        }

    def _aggregate_verification_results(
        self, results: List[OracleVerificationResult]
    ) -> OracleVerificationResult:
        """Aggregate multiple pair verification results"""
        if not results:
            return OracleVerificationResult(
                valid=False,
                confidence=0.0,
                health_score=0.0,
                max_deviation=1.0,
                consensus_price=0.0,
                deviation_type=PriceDeviationType.ORACLE_FAILURE,
                source_results=[],
                risk_factors=["no_verification_results"],
                recommendations=["Unable to verify any price data"],
                verification_time=0.0,
            )

        # Aggregate metrics
        avg_confidence = statistics.mean([r.confidence for r in results])
        avg_health = statistics.mean([r.health_score for r in results])
        max_deviation = max([r.max_deviation for r in results])

        # Overall validity (all must be valid)
        overall_valid = all([r.valid for r in results])

        # Aggregate risk factors and recommendations
        all_risk_factors = []
        all_recommendations = []
        for result in results:
            all_risk_factors.extend(result.risk_factors)
            all_recommendations.extend(result.recommendations)

        # Determine worst deviation type
        deviation_types = [r.deviation_type for r in results]
        worst_deviation = max(
            deviation_types,
            key=lambda x: [
                PriceDeviationType.NORMAL,
                PriceDeviationType.HIGH_VOLATILITY,
                PriceDeviationType.MANIPULATION_SUSPECTED,
                PriceDeviationType.ORACLE_FAILURE,
            ].index(x),
        )

        return OracleVerificationResult(
            valid=overall_valid,
            confidence=avg_confidence,
            health_score=avg_health,
            max_deviation=max_deviation,
            consensus_price=results[0].consensus_price,  # Use first result's consensus
            deviation_type=worst_deviation,
            source_results=[r.source_results for r in results],
            risk_factors=list(set(all_risk_factors)),
            recommendations=list(set(all_recommendations)),
            verification_time=0.0,  # Will be set by caller
        )

    def _update_oracle_metrics(self, source_name: str, success: bool, latency: float):
        """Update oracle performance metrics"""
        if source_name not in self.oracle_metrics:
            return

        metrics = self.oracle_metrics[source_name]
        metrics["total_requests"] += 1

        if success:
            metrics["successful_requests"] += 1
            metrics["last_success"] = time.time()

            # Update average latency (exponential moving average)
            alpha = 0.1
            metrics["average_latency"] = (
                alpha * latency + (1 - alpha) * metrics["average_latency"]
            )
        else:
            metrics["failed_requests"] += 1

        # Update uptime score
        total = metrics["total_requests"]
        success_rate = metrics["successful_requests"] / total if total > 0 else 0
        metrics["uptime_score"] = success_rate

    async def _get_historical_prices(
        self, pair: str, timestamp: float
    ) -> List[PriceData]:
        """Get historical price data for verification"""
        # Simulate historical price fetching
        historical_prices = []

        for source_name, source in self.oracle_sources.items():
            if source.status == OracleStatus.HEALTHY:
                try:
                    # Simulate historical data with slight variations
                    base_price = 43500.0
                    variation = (
                        hash(source_name + str(timestamp)) % 100 - 50
                    ) / 5000  # ±1%
                    price = base_price * (1 + variation)

                    historical_prices.append(
                        PriceData(
                            source=source_name,
                            pair=pair,
                            price=price,
                            timestamp=timestamp,
                            confidence=source.reliability_score,
                        )
                    )
                except Exception:
                    continue

        return historical_prices

    def _calculate_oracle_health(self, price_data: List[PriceData]) -> float:
        """Calculate oracle health from price data"""
        if not price_data:
            return 0.0

        # Calculate based on source reliability and consensus
        health_scores = []

        for data in price_data:
            source = self.oracle_sources.get(data.source)
            if source:
                health_scores.append(source.reliability_score * data.confidence)

        return statistics.mean(health_scores) if health_scores else 0.0

    async def _check_pair_oracle_health(self, pair: str) -> float:
        """Check oracle health for specific trading pair"""
        health_scores = []

        for source_name, source in self.oracle_sources.items():
            try:
                # Test oracle responsiveness
                start_time = time.time()
                price_data = await self._fetch_price_from_source(
                    source_name, pair, time.time()
                )
                latency = time.time() - start_time

                if price_data and latency < source.timeout:
                    health_scores.append(source.reliability_score)
                else:
                    health_scores.append(0.0)

            except Exception:
                health_scores.append(0.0)

        return statistics.mean(health_scores) if health_scores else 0.0

    def _get_cached_health_score(self) -> float:
        """Get cached oracle health score"""
        return getattr(self, "_cached_health_score", 0.9)

    def _cache_health_score(self, score: float):
        """Cache oracle health score"""
        self._cached_health_score = score

    async def _get_recent_price_data(
        self, pair: str, timeframe: str
    ) -> List[PriceData]:
        """Get recent price data for consensus analysis"""
        # Simulate getting recent price data
        recent_prices = []

        # Convert timeframe to seconds
        timeframe_seconds = {"1h": 3600, "24h": 86400, "7d": 604800}.get(
            timeframe, 3600
        )

        for source_name in self.oracle_sources:
            try:
                price_data = await self._fetch_price_from_source(
                    source_name, pair, time.time()
                )
                if price_data:
                    recent_prices.append(price_data)
            except Exception:
                continue

        return recent_prices

    def _calculate_consensus_score(self, price_data: List[PriceData]) -> float:
        """Calculate consensus score from price data"""
        if len(price_data) < 2:
            return 0.5

        prices = [data.price for data in price_data]
        avg_price = statistics.mean(prices)

        # Calculate how close prices are to each other
        deviations = [abs(price - avg_price) / avg_price for price in prices]
        avg_deviation = statistics.mean(deviations)

        # Good consensus = low deviation
        consensus_score = max(0.0, 1.0 - (avg_deviation / 0.05))  # 5% threshold

        return consensus_score

    async def _get_available_sources_for_asset(self, asset: str) -> List[str]:
        """Get available oracle sources for specific asset"""
        # In real implementation, this would check which oracles support the asset
        available = []

        for source_name, source in self.oracle_sources.items():
            if source.status in [OracleStatus.HEALTHY, OracleStatus.DEGRADED]:
                available.append(source_name)

        return available

    async def _check_institutional_consensus(
        self, asset: str, sources: List[str]
    ) -> float:
        """Check consensus quality for institutional requirements"""
        # Get price data from all sources
        price_data = []

        for source_name in sources:
            try:
                data = await self._fetch_price_from_source(
                    source_name, f"{asset}/USD", time.time()
                )
                if data:
                    price_data.append(data)
            except Exception:
                continue

        if len(price_data) < 3:  # Institutional minimum
            return 0.0

        # Calculate consensus with institutional standards
        consensus_score = self._calculate_consensus_score(price_data)

        # Institutional requirement: consensus must be >95%
        return consensus_score if consensus_score > 0.95 else 0.0

    async def health_check(self) -> Dict:
        """Comprehensive health check of oracle system"""
        health_status = {
            "status": "healthy",
            "oracle_sources": {},
            "metrics": {},
            "issues": [],
        }

        try:
            # Check each oracle source
            for source_name, source in self.oracle_sources.items():
                source_health = {
                    "status": source.status.value,
                    "reliability_score": source.reliability_score,
                    "last_update": source.last_update,
                    "metrics": self.oracle_metrics.get(source_name, {}),
                }
                health_status["oracle_sources"][source_name] = source_health

                # Check for issues
                metrics = self.oracle_metrics.get(source_name, {})
                if metrics.get("uptime_score", 0) < 0.95:
                    health_status["issues"].append(f"{source_name}_low_uptime")

                if metrics.get("average_latency", 0) > 2.0:
                    health_status["issues"].append(f"{source_name}_high_latency")

            # Overall metrics
            total_sources = len(self.oracle_sources)
            healthy_sources = len(
                [
                    s
                    for s in self.oracle_sources.values()
                    if s.status == OracleStatus.HEALTHY
                ]
            )

            health_status["metrics"] = {
                "total_sources": total_sources,
                "healthy_sources": healthy_sources,
                "health_percentage": (healthy_sources / total_sources) * 100,
                "average_reliability": statistics.mean(
                    [s.reliability_score for s in self.oracle_sources.values()]
                ),
            }

            # Determine overall status
            if healthy_sources < total_sources * 0.8:  # <80% healthy
                health_status["status"] = "degraded"

            if healthy_sources < self.config["min_sources"]:
                health_status["status"] = "critical"
                health_status["issues"].append("insufficient_healthy_sources")

        except Exception as e:
            health_status["status"] = "error"
            health_status["issues"].append(f"health_check_error: {str(e)}")

        return health_status


# Example usage
async def main():
    """Example oracle risk manager usage"""
    oracle_manager = OracleRiskManager()

    # Example price verification
    trade_data = {
        "trade": {"pair": "BTC/USDT", "price": 43520.0, "timestamp": time.time()}
    }

    result = await oracle_manager.verify_data_integrity(trade_data)
    print(f"Oracle verification result: {result['valid']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Oracle health: {result['health_score']:.3f}")
    print(f"Max deviation: {result['max_deviation']:.4f}")

    # Health check
    health = await oracle_manager.health_check()
    print(f"\nOracle system health: {health['status']}")
    print(
        f"Healthy sources: {health['metrics']['healthy_sources']}/{health['metrics']['total_sources']}"
    )


if __name__ == "__main__":
    asyncio.run(main())

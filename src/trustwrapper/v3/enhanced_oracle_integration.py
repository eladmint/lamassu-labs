#!/usr/bin/env python3
"""
TrustWrapper v3.0 Enhanced Oracle Integration System
Multi-source oracle integration with Chainlink, Band Protocol, and custom oracles
Designed for universal multi-chain AI verification platform
"""

import asyncio
import logging
import ssl
import statistics
import time
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import aiohttp

# Import v2.0 oracle system


class OracleType(Enum):
    """Types of oracle data sources"""

    CHAINLINK = "chainlink"
    BAND_PROTOCOL = "band_protocol"
    CUSTOM = "custom"
    REALTIME_FEED = "realtime_feed"
    BRIDGE_ORACLE = "bridge_oracle"


@dataclass
class OracleSource:
    """Oracle source configuration"""

    source_id: str
    oracle_type: OracleType
    endpoint: str
    api_key: Optional[str]
    update_interval: float
    reliability_score: float
    supported_assets: List[str]
    chain_support: List[str]  # Which chains this oracle supports
    latency_ms: Optional[float] = None
    cost_per_query: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OracleData:
    """Enhanced oracle data with multi-chain context"""

    asset_id: str
    price: float
    timestamp: float
    source_id: str
    oracle_type: OracleType
    confidence: float
    volume_24h: Optional[float] = None
    market_cap: Optional[float] = None
    chain_context: Optional[str] = None  # Which chain this data is for
    volatility_score: Optional[float] = None
    liquidity_score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MultiOracleConsensus:
    """Enhanced consensus with multi-oracle and multi-chain support"""

    asset_id: str
    consensus_price: float
    weighted_price: float
    oracle_count: int
    price_deviation: float
    confidence_score: float
    timestamp: float
    participating_oracles: List[str]
    outlier_detection: Dict[str, Any]
    chain_specific_data: Dict[str, float]  # Chain-specific prices
    risk_metrics: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ChainlinkOracleClient:
    """Chainlink oracle integration client"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.chainlink")
        self.session = None

        # Chainlink price feed addresses (mainnet examples)
        self.price_feeds = {
            "BTC/USD": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",
            "ETH/USD": "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
            "ADA/USD": "0xAE48c91dF1fE419994FFDa27da09D5aC69c30f55",
            "SOL/USD": "0x4ffC43a60e009B551865A93d232E33Fce9f01507",
        }

    async def initialize(self):
        """Initialize Chainlink client"""
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=connector)

        self.logger.info("🔗 Chainlink oracle client initialized")

    async def get_price_data(self, asset_pairs: List[str]) -> List[OracleData]:
        """Get price data from Chainlink feeds"""
        oracle_data = []

        for pair in asset_pairs:
            if pair in self.price_feeds:
                try:
                    # Mock Chainlink data - in production would call actual aggregator
                    price_data = await self._fetch_chainlink_price(pair)
                    if price_data:
                        oracle_data.append(price_data)
                except Exception as e:
                    self.logger.error(f"Error fetching Chainlink data for {pair}: {e}")

        return oracle_data

    async def _fetch_chainlink_price(self, pair: str) -> Optional[OracleData]:
        """Fetch price from Chainlink aggregator"""
        try:
            # Mock implementation - would use Web3 to call price feed contract
            mock_prices = {
                "BTC/USD": 45000.0,
                "ETH/USD": 2500.0,
                "ADA/USD": 0.8,
                "SOL/USD": 100.0,
            }

            if pair in mock_prices:
                # Simulate network call
                await asyncio.sleep(0.1)

                # Add some realistic variance
                base_price = mock_prices[pair]
                variance = base_price * 0.002  # 0.2% variance
                actual_price = (
                    base_price + (hash(str(time.time())) % 1000 - 500) * variance / 500
                )

                return OracleData(
                    asset_id=pair,
                    price=actual_price,
                    timestamp=time.time(),
                    source_id="chainlink",
                    oracle_type=OracleType.CHAINLINK,
                    confidence=0.98,  # Chainlink is highly reliable
                    chain_context="ethereum",  # Chainlink primarily on Ethereum
                    metadata={
                        "feed_address": self.price_feeds[pair],
                        "aggregator_version": "v3",
                        "decimals": 8,
                    },
                )
        except Exception as e:
            self.logger.error(f"Chainlink fetch error for {pair}: {e}")
            return None

    async def shutdown(self):
        """Shutdown Chainlink client"""
        if self.session:
            await self.session.close()


class BandProtocolClient:
    """Band Protocol oracle integration client"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.band")
        self.session = None
        self.api_endpoint = "https://laozi1.bandchain.org/api"

    async def initialize(self):
        """Initialize Band Protocol client"""
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=connector)

        self.logger.info("📡 Band Protocol oracle client initialized")

    async def get_price_data(self, asset_pairs: List[str]) -> List[OracleData]:
        """Get price data from Band Protocol"""
        oracle_data = []

        for pair in asset_pairs:
            try:
                price_data = await self._fetch_band_price(pair)
                if price_data:
                    oracle_data.append(price_data)
            except Exception as e:
                self.logger.error(f"Error fetching Band Protocol data for {pair}: {e}")

        return oracle_data

    async def _fetch_band_price(self, pair: str) -> Optional[OracleData]:
        """Fetch price from Band Protocol"""
        try:
            # Mock Band Protocol API call
            symbol = pair.split("/")[0]

            # In production, would call actual Band Protocol API
            url = f"{self.api_endpoint}/oracle/v1/request_prices"
            params = {"symbols": symbol, "min_count": 3, "ask_count": 4}

            # Mock response
            await asyncio.sleep(0.15)

            mock_prices = {"BTC": 44800.0, "ETH": 2480.0, "ADA": 0.78, "SOL": 98.5}

            if symbol in mock_prices:
                base_price = mock_prices[symbol]
                variance = base_price * 0.003  # 0.3% variance
                actual_price = (
                    base_price
                    + (hash(str(time.time()) + symbol) % 1000 - 500) * variance / 500
                )

                return OracleData(
                    asset_id=pair,
                    price=actual_price,
                    timestamp=time.time(),
                    source_id="band_protocol",
                    oracle_type=OracleType.BAND_PROTOCOL,
                    confidence=0.95,
                    chain_context="cosmos",  # Band Protocol on Cosmos
                    metadata={
                        "oracle_script_id": 37,
                        "multiplier": 1000000,
                        "request_id": int(time.time()),
                    },
                )
        except Exception as e:
            self.logger.error(f"Band Protocol fetch error for {pair}: {e}")
            return None

    async def shutdown(self):
        """Shutdown Band Protocol client"""
        if self.session:
            await self.session.close()


class CustomOracleClient:
    """Custom oracle sources (DeFi protocols, specialized feeds)"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.custom")
        self.session = None

        # Custom oracle endpoints
        self.custom_sources = {
            "uniswap_v3": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
            "curve": "https://api.curve.fi/api/getPools/ethereum/main",
            "balancer": "https://api.balancer.fi/",
            "yearn": "https://api.yearn.finance/v1/chains/1/vaults/all",
        }

    async def initialize(self):
        """Initialize custom oracle client"""
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=connector)

        self.logger.info("🛠️ Custom oracle client initialized")

    async def get_price_data(self, asset_pairs: List[str]) -> List[OracleData]:
        """Get price data from custom oracle sources"""
        oracle_data = []

        # Get data from different DeFi protocols
        for pair in asset_pairs:
            try:
                # Get Uniswap V3 price
                uniswap_data = await self._fetch_uniswap_price(pair)
                if uniswap_data:
                    oracle_data.append(uniswap_data)

                # Get Curve price (for stablecoins)
                if "USD" in pair:
                    curve_data = await self._fetch_curve_price(pair)
                    if curve_data:
                        oracle_data.append(curve_data)

            except Exception as e:
                self.logger.error(f"Error fetching custom oracle data for {pair}: {e}")

        return oracle_data

    async def _fetch_uniswap_price(self, pair: str) -> Optional[OracleData]:
        """Fetch price from Uniswap V3"""
        try:
            # Mock Uniswap V3 TWAP price
            await asyncio.sleep(0.2)

            mock_prices = {
                "BTC/USD": 44950.0,
                "ETH/USD": 2495.0,
                "ADA/USD": 0.79,
                "SOL/USD": 99.2,
            }

            if pair in mock_prices:
                base_price = mock_prices[pair]
                variance = base_price * 0.005  # 0.5% variance (DeFi has more variance)
                actual_price = (
                    base_price
                    + (hash(str(time.time()) + "uni" + pair) % 1000 - 500)
                    * variance
                    / 500
                )

                return OracleData(
                    asset_id=pair,
                    price=actual_price,
                    timestamp=time.time(),
                    source_id="uniswap_v3",
                    oracle_type=OracleType.CUSTOM,
                    confidence=0.90,
                    chain_context="ethereum",
                    liquidity_score=0.85,
                    metadata={
                        "pool_address": f'0x{"mock_pool_address"[:40]}',
                        "fee_tier": 3000,
                        "twap_period": 3600,
                    },
                )
        except Exception as e:
            self.logger.error(f"Uniswap fetch error for {pair}: {e}")
            return None

    async def _fetch_curve_price(self, pair: str) -> Optional[OracleData]:
        """Fetch price from Curve (specialized for stablecoins)"""
        try:
            await asyncio.sleep(0.15)

            # Curve typically deals with stablecoins and similar assets
            if "USD" in pair:
                symbol = pair.split("/")[0]

                # Mock Curve pricing (usually close to $1 for stablecoins)
                if symbol in ["USDC", "USDT", "DAI"]:
                    price = 1.0 + (hash(str(time.time()) + "curve") % 100 - 50) * 0.0001
                else:
                    # For other assets, use base price with lower variance
                    mock_prices = {"BTC": 44900.0, "ETH": 2490.0}
                    if symbol in mock_prices:
                        base_price = mock_prices[symbol]
                        variance = base_price * 0.002
                        price = (
                            base_price
                            + (hash(str(time.time()) + "curve" + symbol) % 1000 - 500)
                            * variance
                            / 500
                        )
                    else:
                        return None

                return OracleData(
                    asset_id=pair,
                    price=price,
                    timestamp=time.time(),
                    source_id="curve",
                    oracle_type=OracleType.CUSTOM,
                    confidence=0.92,
                    chain_context="ethereum",
                    liquidity_score=0.80,
                    metadata={
                        "pool_type": "stable_swap",
                        "amplification": 2000,
                        "virtual_price": 1.001,
                    },
                )
        except Exception as e:
            self.logger.error(f"Curve fetch error for {pair}: {e}")
            return None

    async def shutdown(self):
        """Shutdown custom oracle client"""
        if self.session:
            await self.session.close()


class EnhancedOracleIntegration:
    """
    Enhanced Oracle Integration System for TrustWrapper v3.0
    Integrates multiple oracle sources with the universal multi-chain framework
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        # Oracle clients
        self.chainlink_client = None
        self.band_client = None
        self.custom_client = None
        self.realtime_engine = None

        # Data storage
        self.oracle_cache = {}
        self.consensus_cache = {}
        self.subscribers = []

        # State management
        self.running = False
        self.last_update = 0

    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration for enhanced oracle integration"""
        return {
            "update_interval": 10.0,  # seconds
            "consensus_interval": 15.0,  # seconds
            "asset_pairs": ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD"],
            "oracle_sources": {
                "chainlink": {"enabled": True, "weight": 0.4, "timeout": 5.0},
                "band_protocol": {"enabled": True, "weight": 0.3, "timeout": 5.0},
                "custom_oracles": {"enabled": True, "weight": 0.2, "timeout": 8.0},
                "realtime_feeds": {"enabled": True, "weight": 0.1, "timeout": 3.0},
            },
            "consensus": {
                "min_sources": 3,
                "outlier_threshold": 0.05,  # 5% deviation
                "confidence_threshold": 0.8,
            },
            "caching": {"ttl_seconds": 30, "max_entries": 1000},
        }

    async def initialize(self):
        """Initialize the enhanced oracle integration system"""
        try:
            self.logger.info("🚀 Initializing Enhanced Oracle Integration System...")

            # Initialize oracle clients
            if self.config["oracle_sources"]["chainlink"]["enabled"]:
                self.chainlink_client = ChainlinkOracleClient(self.config)
                await self.chainlink_client.initialize()

            if self.config["oracle_sources"]["band_protocol"]["enabled"]:
                self.band_client = BandProtocolClient(self.config)
                await self.band_client.initialize()

            if self.config["oracle_sources"]["custom_oracles"]["enabled"]:
                self.custom_client = CustomOracleClient(self.config)
                await self.custom_client.initialize()

            if self.config["oracle_sources"]["realtime_feeds"]["enabled"]:
                from ..oracles.realtime_oracle_engine import get_oracle_engine

                self.realtime_engine = await get_oracle_engine()

            self.logger.info(
                "✅ Enhanced Oracle Integration System initialized successfully"
            )

        except Exception as e:
            self.logger.error(f"Failed to initialize Enhanced Oracle Integration: {e}")
            raise

    async def start(self):
        """Start the enhanced oracle integration system"""
        if self.running:
            return

        self.logger.info("🚀 Starting Enhanced Oracle Integration System...")
        self.running = True

        # Start background tasks
        tasks = [self._run_oracle_updater(), self._run_consensus_calculator()]

        await asyncio.gather(*tasks, return_exceptions=True)

    async def stop(self):
        """Stop the enhanced oracle integration system"""
        self.logger.info("🛑 Stopping Enhanced Oracle Integration System...")
        self.running = False

        # Shutdown oracle clients
        if self.chainlink_client:
            await self.chainlink_client.shutdown()
        if self.band_client:
            await self.band_client.shutdown()
        if self.custom_client:
            await self.custom_client.shutdown()
        if self.realtime_engine:
            await self.realtime_engine.stop()

    async def _run_oracle_updater(self):
        """Background task to update oracle data"""
        while self.running:
            try:
                await self._update_all_oracles()
                await asyncio.sleep(self.config["update_interval"])
            except Exception as e:
                self.logger.error(f"Oracle updater error: {e}")
                await asyncio.sleep(5.0)

    async def _run_consensus_calculator(self):
        """Background task to calculate multi-oracle consensus"""
        while self.running:
            try:
                await self._calculate_multi_oracle_consensus()
                await asyncio.sleep(self.config["consensus_interval"])
            except Exception as e:
                self.logger.error(f"Consensus calculator error: {e}")
                await asyncio.sleep(10.0)

    async def _update_all_oracles(self):
        """Update data from all oracle sources"""
        asset_pairs = self.config["asset_pairs"]

        # Collect data from all sources in parallel
        tasks = []

        if self.chainlink_client:
            tasks.append(self.chainlink_client.get_price_data(asset_pairs))

        if self.band_client:
            tasks.append(self.band_client.get_price_data(asset_pairs))

        if self.custom_client:
            tasks.append(self.custom_client.get_price_data(asset_pairs))

        # Get realtime data
        if self.realtime_engine:
            tasks.append(self._get_realtime_data(asset_pairs))

        # Execute all tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        all_oracle_data = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.warning(f"Oracle source failed: {result}")
            elif isinstance(result, list):
                all_oracle_data.extend(result)

        # Store in cache
        current_time = time.time()
        ttl = self.config["caching"]["ttl_seconds"]

        for oracle_data in all_oracle_data:
            cache_key = f"{oracle_data.asset_id}:{oracle_data.source_id}"
            self.oracle_cache[cache_key] = oracle_data

        # Clean expired cache entries
        expired_keys = []
        for key, data in self.oracle_cache.items():
            if current_time - data.timestamp > ttl:
                expired_keys.append(key)

        for key in expired_keys:
            del self.oracle_cache[key]

        self.last_update = current_time
        self.logger.debug(f"Updated oracle data: {len(all_oracle_data)} entries")

    async def _get_realtime_data(self, asset_pairs: List[str]) -> List[OracleData]:
        """Get data from realtime oracle engine"""
        realtime_data = []

        for pair in asset_pairs:
            try:
                price_data = await self.realtime_engine.get_current_price(pair)
                if price_data:
                    oracle_data = OracleData(
                        asset_id=pair,
                        price=price_data.price,
                        timestamp=price_data.timestamp,
                        source_id="realtime_feed",
                        oracle_type=OracleType.REALTIME_FEED,
                        confidence=price_data.confidence,
                        volume_24h=price_data.volume_24h,
                        chain_context="multi_exchange",
                        metadata={
                            "original_source": price_data.source,
                            "age_seconds": price_data.age_seconds(),
                        },
                    )
                    realtime_data.append(oracle_data)
            except Exception as e:
                self.logger.debug(f"Error getting realtime data for {pair}: {e}")

        return realtime_data

    async def _calculate_multi_oracle_consensus(self):
        """Calculate consensus across all oracle sources"""
        asset_pairs = self.config["asset_pairs"]

        for pair in asset_pairs:
            try:
                consensus = await self._calculate_asset_consensus(pair)
                if consensus:
                    self.consensus_cache[pair] = consensus

                    # Notify subscribers
                    await self._notify_consensus_update(consensus)
            except Exception as e:
                self.logger.error(f"Error calculating consensus for {pair}: {e}")

    async def _calculate_asset_consensus(
        self, asset_pair: str
    ) -> Optional[MultiOracleConsensus]:
        """Calculate consensus for a specific asset pair"""
        # Get recent oracle data for this asset
        current_time = time.time()
        ttl = self.config["caching"]["ttl_seconds"]

        oracle_data = []
        for key, data in self.oracle_cache.items():
            if (
                key.startswith(f"{asset_pair}:")
                and current_time - data.timestamp <= ttl
            ):
                oracle_data.append(data)

        if len(oracle_data) < self.config["consensus"]["min_sources"]:
            return None

        # Extract prices and weights
        prices = []
        weights = []
        sources = []

        for data in oracle_data:
            price = data.price
            confidence = data.confidence

            # Get source weight from config
            source_weight = 0.25  # Default weight
            oracle_config = self.config["oracle_sources"]

            if data.oracle_type == OracleType.CHAINLINK:
                source_weight = oracle_config["chainlink"]["weight"]
            elif data.oracle_type == OracleType.BAND_PROTOCOL:
                source_weight = oracle_config["band_protocol"]["weight"]
            elif data.oracle_type == OracleType.CUSTOM:
                source_weight = oracle_config["custom_oracles"]["weight"]
            elif data.oracle_type == OracleType.REALTIME_FEED:
                source_weight = oracle_config["realtime_feeds"]["weight"]

            # Weight by confidence and source reliability
            final_weight = source_weight * confidence

            prices.append(price)
            weights.append(final_weight)
            sources.append(data.source_id)

        # Calculate weighted consensus
        total_weight = sum(weights)
        if total_weight == 0:
            return None

        weighted_price = sum(p * w for p, w in zip(prices, weights)) / total_weight

        # Calculate simple average for comparison
        avg_price = statistics.mean(prices)

        # Calculate price deviation
        deviations = [abs(p - avg_price) / avg_price for p in prices]
        max_deviation = max(deviations)

        # Outlier detection
        outlier_threshold = self.config["consensus"]["outlier_threshold"]
        outliers = []
        for i, deviation in enumerate(deviations):
            if deviation > outlier_threshold:
                outliers.append(
                    {"source": sources[i], "price": prices[i], "deviation": deviation}
                )

        # Calculate confidence score
        confidence_score = self._calculate_consensus_confidence(
            oracle_data, max_deviation, len(outliers)
        )

        # Chain-specific data (if available)
        chain_data = {}
        for data in oracle_data:
            if data.chain_context:
                chain_data[data.chain_context] = data.price

        # Risk metrics
        risk_metrics = {
            "price_volatility": max_deviation,
            "source_diversity": len(set(sources)),
            "outlier_ratio": len(outliers) / len(oracle_data),
            "data_freshness": min(
                current_time - data.timestamp for data in oracle_data
            ),
        }

        return MultiOracleConsensus(
            asset_id=asset_pair,
            consensus_price=avg_price,
            weighted_price=weighted_price,
            oracle_count=len(oracle_data),
            price_deviation=max_deviation,
            confidence_score=confidence_score,
            timestamp=current_time,
            participating_oracles=sources,
            outlier_detection={
                "outliers": outliers,
                "threshold": outlier_threshold,
                "outlier_count": len(outliers),
            },
            chain_specific_data=chain_data,
            risk_metrics=risk_metrics,
        )

    def _calculate_consensus_confidence(
        self, oracle_data: List[OracleData], price_deviation: float, outlier_count: int
    ) -> float:
        """Calculate confidence score for multi-oracle consensus"""
        base_confidence = 0.7

        # Adjust for price deviation
        deviation_penalty = min(price_deviation * 3, 0.4)

        # Adjust for number of sources
        source_bonus = min((len(oracle_data) - 2) * 0.1, 0.25)

        # Adjust for outliers
        outlier_penalty = outlier_count * 0.1

        # Adjust for source diversity
        oracle_types = set(data.oracle_type for data in oracle_data)
        diversity_bonus = min((len(oracle_types) - 1) * 0.05, 0.15)

        # Adjust for individual confidence scores
        avg_confidence = statistics.mean(data.confidence for data in oracle_data)
        confidence_adjustment = (avg_confidence - 0.8) * 0.3

        final_confidence = (
            base_confidence
            - deviation_penalty
            + source_bonus
            - outlier_penalty
            + diversity_bonus
            + confidence_adjustment
        )

        return max(0.1, min(1.0, final_confidence))

    async def _notify_consensus_update(self, consensus: MultiOracleConsensus):
        """Notify subscribers of consensus updates"""
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback("multi_oracle_consensus", consensus)
                else:
                    callback("multi_oracle_consensus", consensus)
            except Exception as e:
                self.logger.warning(f"Subscriber notification error: {e}")

    def subscribe(self, callback: Callable):
        """Subscribe to oracle updates"""
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable):
        """Unsubscribe from oracle updates"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    async def get_multi_oracle_consensus(
        self, asset_pair: str
    ) -> Optional[MultiOracleConsensus]:
        """Get current multi-oracle consensus for an asset pair"""
        return self.consensus_cache.get(asset_pair)

    async def get_oracle_data_by_source(
        self, asset_pair: str, source_id: str
    ) -> Optional[OracleData]:
        """Get oracle data from a specific source"""
        cache_key = f"{asset_pair}:{source_id}"
        return self.oracle_cache.get(cache_key)

    async def get_all_oracle_data(self, asset_pair: str) -> List[OracleData]:
        """Get all oracle data for an asset pair"""
        current_time = time.time()
        ttl = self.config["caching"]["ttl_seconds"]

        oracle_data = []
        for key, data in self.oracle_cache.items():
            if (
                key.startswith(f"{asset_pair}:")
                and current_time - data.timestamp <= ttl
            ):
                oracle_data.append(data)

        return oracle_data

    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        current_time = time.time()

        # Count oracle data by source
        source_counts = {}
        fresh_data_count = 0
        ttl = self.config["caching"]["ttl_seconds"]

        for data in self.oracle_cache.values():
            source = data.source_id
            source_counts[source] = source_counts.get(source, 0) + 1

            if current_time - data.timestamp <= ttl:
                fresh_data_count += 1

        return {
            "running": self.running,
            "last_update": self.last_update,
            "total_oracle_entries": len(self.oracle_cache),
            "fresh_data_count": fresh_data_count,
            "source_counts": source_counts,
            "consensus_pairs": list(self.consensus_cache.keys()),
            "active_sources": {
                "chainlink": self.chainlink_client is not None,
                "band_protocol": self.band_client is not None,
                "custom_oracles": self.custom_client is not None,
                "realtime_feeds": self.realtime_engine is not None,
            },
        }


# Singleton instance
_enhanced_oracle_instance = None


async def get_enhanced_oracle_integration(
    config: Optional[Dict[str, Any]] = None
) -> EnhancedOracleIntegration:
    """Get or create the global enhanced oracle integration instance"""
    global _enhanced_oracle_instance

    if _enhanced_oracle_instance is None:
        _enhanced_oracle_instance = EnhancedOracleIntegration(config)
        await _enhanced_oracle_instance.initialize()

    return _enhanced_oracle_instance

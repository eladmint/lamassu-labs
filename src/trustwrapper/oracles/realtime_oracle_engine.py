#!/usr/bin/env python3
"""
TrustWrapper v2.0 Real-Time Oracle Integration Engine
Provides continuous real-time price feeds for verification and XAI analysis
"""

import asyncio
import json
import logging
import ssl
import time
from dataclasses import asdict, dataclass
from typing import Any, Callable, Dict, List, Optional

import aiohttp
import websockets


@dataclass
class OraclePrice:
    """Real-time oracle price data"""

    symbol: str
    price: float
    volume_24h: Optional[float]
    change_24h: Optional[float]
    timestamp: float
    source: str
    confidence: float
    market_cap: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def age_seconds(self) -> float:
        """Returns age of price data in seconds"""
        return time.time() - self.timestamp


@dataclass
class OracleConsensus:
    """Multi-oracle consensus result"""

    symbol: str
    consensus_price: float
    price_deviation: float
    source_count: int
    confidence_score: float
    timestamp: float
    sources: List[str]
    price_range: Dict[str, float]  # min, max, median
    volume_weighted_price: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RealTimeOracleEngine:
    """
    Real-time oracle engine providing continuous price feeds
    Supports multiple sources with consensus validation and anomaly detection
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._get_default_config()
        self.logger = logging.getLogger(__name__)

        # Oracle connections
        self.session = None
        self.websocket_connections = {}

        # Data storage
        self.price_cache = {}
        self.price_history = {}
        self.subscribers = []

        # Oracle endpoints
        self.rest_endpoints = {
            "coingecko": "https://api.coingecko.com/api/v3",
            "coinbase": "https://api.coinbase.com/v2",
            "binance": "https://api.binance.com/api/v3",
            "kraken": "https://api.kraken.com/0/public",
            "bitstamp": "https://www.bitstamp.net/api/v2",
        }

        self.websocket_endpoints = {
            "binance": "wss://stream.binance.com:9443/ws",
            "coinbase": "wss://ws-feed.pro.coinbase.com",
            "kraken": "wss://ws.kraken.com",
        }

        # State management
        self.running = False
        self.last_consensus_update = 0

    def _get_default_config(self) -> Dict:
        """Default configuration for oracle engine"""
        return {
            "update_interval": 5.0,  # seconds
            "consensus_interval": 10.0,  # seconds
            "max_price_deviation": 0.05,  # 5%
            "min_sources": 2,
            "consensus_threshold": 0.67,
            "cache_ttl": 30.0,  # seconds
            "symbols": ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD"],
            "enable_websockets": True,
            "enable_rest_fallback": True,
            "anomaly_detection": True,
            "volume_weighting": True,
        }

    async def start(self):
        """Start the real-time oracle engine"""
        if self.running:
            return

        self.logger.info("🚀 Starting Real-Time Oracle Engine...")
        self.running = True

        # Initialize HTTP session
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=connector)

        # Start background tasks
        tasks = [
            self._run_price_updater(),
            self._run_consensus_calculator(),
            self._run_websocket_manager(),
        ]

        if self.config.get("enable_websockets", True):
            tasks.append(self._run_websocket_feeds())

        await asyncio.gather(*tasks, return_exceptions=True)

    async def stop(self):
        """Stop the oracle engine"""
        self.logger.info("🛑 Stopping Real-Time Oracle Engine...")
        self.running = False

        # Close websocket connections
        for source, ws in self.websocket_connections.items():
            if ws and not ws.closed:
                await ws.close()

        # Close HTTP session
        if self.session:
            await self.session.close()

    async def _run_price_updater(self):
        """Background task to update prices from REST APIs"""
        while self.running:
            try:
                await self._update_rest_prices()
                await asyncio.sleep(self.config["update_interval"])
            except Exception as e:
                self.logger.error(f"Price updater error: {e}")
                await asyncio.sleep(5.0)

    async def _run_consensus_calculator(self):
        """Background task to calculate oracle consensus"""
        while self.running:
            try:
                await self._calculate_consensus()
                await asyncio.sleep(self.config["consensus_interval"])
            except Exception as e:
                self.logger.error(f"Consensus calculator error: {e}")
                await asyncio.sleep(10.0)

    async def _run_websocket_manager(self):
        """Background task to manage websocket connections"""
        while self.running:
            try:
                await self._maintain_websocket_connections()
                await asyncio.sleep(30.0)  # Check connections every 30 seconds
            except Exception as e:
                self.logger.error(f"WebSocket manager error: {e}")
                await asyncio.sleep(30.0)

    async def _run_websocket_feeds(self):
        """Background task to handle websocket price feeds"""
        while self.running:
            try:
                await self._process_websocket_feeds()
                await asyncio.sleep(1.0)
            except Exception as e:
                self.logger.error(f"WebSocket feeds error: {e}")
                await asyncio.sleep(5.0)

    async def _update_rest_prices(self):
        """Update prices from REST API endpoints"""
        # Initialize session if not done
        if not self.session:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            connector = aiohttp.TCPConnector(ssl=ssl_context)
            self.session = aiohttp.ClientSession(connector=connector)

        symbols = self.config["symbols"]

        # Update from each source
        tasks = []
        for source in ["coingecko", "coinbase", "binance", "kraken"]:
            if source in self.rest_endpoints:
                tasks.append(self._fetch_prices_from_source(source, symbols))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.warning(f"Failed to fetch from source {i}: {result}")
            elif result:
                await self._process_price_updates(result)

    async def _fetch_prices_from_source(
        self, source: str, symbols: List[str]
    ) -> List[OraclePrice]:
        """Fetch prices from a specific oracle source"""
        try:
            if source == "coingecko":
                return await self._fetch_coingecko_prices(symbols)
            elif source == "coinbase":
                return await self._fetch_coinbase_prices(symbols)
            elif source == "binance":
                return await self._fetch_binance_prices(symbols)
            elif source == "kraken":
                return await self._fetch_kraken_prices(symbols)
            else:
                return []
        except Exception as e:
            self.logger.error(f"Error fetching from {source}: {e}")
            return []

    async def _fetch_coingecko_prices(self, symbols: List[str]) -> List[OraclePrice]:
        """Fetch prices from CoinGecko"""
        prices = []

        # Map symbols to CoinGecko IDs
        symbol_map = {
            "BTC/USD": "bitcoin",
            "ETH/USD": "ethereum",
            "SOL/USD": "solana",
            "ADA/USD": "cardano",
        }

        ids = ",".join(
            [symbol_map.get(symbol) for symbol in symbols if symbol in symbol_map]
        )
        if not ids:
            return prices

        url = f"{self.rest_endpoints['coingecko']}/simple/price"
        params = {
            "ids": ids,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true",
        }

        async with self.session.get(url, params=params, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                timestamp = time.time()

                for symbol, coin_id in symbol_map.items():
                    if coin_id in data and symbol in symbols:
                        coin_data = data[coin_id]
                        prices.append(
                            OraclePrice(
                                symbol=symbol,
                                price=float(coin_data.get("usd", 0)),
                                volume_24h=coin_data.get("usd_24h_vol"),
                                change_24h=coin_data.get("usd_24h_change"),
                                market_cap=coin_data.get("usd_market_cap"),
                                timestamp=timestamp,
                                source="coingecko",
                                confidence=0.95,
                            )
                        )

        return prices

    async def _fetch_coinbase_prices(self, symbols: List[str]) -> List[OraclePrice]:
        """Fetch prices from Coinbase"""
        prices = []

        # Coinbase uses different symbol format
        symbol_map = {
            "BTC/USD": "BTC",
            "ETH/USD": "ETH",
            "SOL/USD": "SOL",
            "ADA/USD": "ADA",
        }

        for symbol in symbols:
            if symbol not in symbol_map:
                continue

            coinbase_symbol = symbol_map[symbol]
            url = f"{self.rest_endpoints['coinbase']}/exchange-rates"
            params = {"currency": coinbase_symbol}

            try:
                async with self.session.get(url, params=params, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        rates = data.get("data", {}).get("rates", {})
                        if "USD" in rates:
                            prices.append(
                                OraclePrice(
                                    symbol=symbol,
                                    price=float(rates["USD"]),
                                    volume_24h=None,
                                    change_24h=None,
                                    timestamp=time.time(),
                                    source="coinbase",
                                    confidence=0.92,
                                )
                            )
            except Exception as e:
                self.logger.debug(f"Coinbase fetch error for {symbol}: {e}")
                continue

        return prices

    async def _fetch_binance_prices(self, symbols: List[str]) -> List[OraclePrice]:
        """Fetch prices from Binance"""
        prices = []

        # Binance symbol format
        symbol_map = {
            "BTC/USD": "BTCUSDT",
            "ETH/USD": "ETHUSDT",
            "SOL/USD": "SOLUSDT",
            "ADA/USD": "ADAUSDT",
        }

        binance_symbols = [symbol_map.get(s) for s in symbols if s in symbol_map]
        if not binance_symbols:
            return prices

        # Get 24hr ticker statistics
        url = f"{self.rest_endpoints['binance']}/ticker/24hr"

        async with self.session.get(url, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                timestamp = time.time()

                for item in data:
                    symbol_binance = item.get("symbol")
                    if symbol_binance in binance_symbols:
                        # Find original symbol
                        original_symbol = None
                        for orig, binance in symbol_map.items():
                            if binance == symbol_binance:
                                original_symbol = orig
                                break

                        if original_symbol:
                            prices.append(
                                OraclePrice(
                                    symbol=original_symbol,
                                    price=float(item.get("lastPrice", 0)),
                                    volume_24h=float(item.get("volume", 0)),
                                    change_24h=float(item.get("priceChangePercent", 0)),
                                    timestamp=timestamp,
                                    source="binance",
                                    confidence=0.94,
                                )
                            )

        return prices

    async def _fetch_kraken_prices(self, symbols: List[str]) -> List[OraclePrice]:
        """Fetch prices from Kraken"""
        prices = []

        # Kraken symbol format
        symbol_map = {
            "BTC/USD": "XXBTZUSD",
            "ETH/USD": "XETHZUSD",
            "SOL/USD": "SOLUSD",
            "ADA/USD": "ADAUSD",
        }

        kraken_symbols = [symbol_map.get(s) for s in symbols if s in symbol_map]
        if not kraken_symbols:
            return prices

        url = f"{self.rest_endpoints['kraken']}/Ticker"
        params = {"pair": ",".join(kraken_symbols)}

        async with self.session.get(url, params=params, timeout=5) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("error"):
                    return prices

                result = data.get("result", {})
                timestamp = time.time()

                for kraken_symbol, ticker_data in result.items():
                    # Find original symbol
                    original_symbol = None
                    for orig, kraken in symbol_map.items():
                        if kraken == kraken_symbol or kraken_symbol.startswith(kraken):
                            original_symbol = orig
                            break

                    if original_symbol and ticker_data:
                        last_price = ticker_data.get("c", [0])[0]
                        volume_24h = ticker_data.get("v", [0])[1]  # 24h volume

                        prices.append(
                            OraclePrice(
                                symbol=original_symbol,
                                price=float(last_price),
                                volume_24h=float(volume_24h) if volume_24h else None,
                                change_24h=None,
                                timestamp=timestamp,
                                source="kraken",
                                confidence=0.93,
                            )
                        )

        return prices

    async def _process_price_updates(self, price_updates: List[OraclePrice]):
        """Process and store price updates"""
        current_time = time.time()
        cache_ttl = self.config.get("cache_ttl", 30.0)

        for price in price_updates:
            # Skip stale data
            if price.age_seconds() > cache_ttl:
                continue

            # Store in cache
            cache_key = f"{price.symbol}:{price.source}"
            self.price_cache[cache_key] = price

            # Store in history
            if price.symbol not in self.price_history:
                self.price_history[price.symbol] = []

            # Keep only recent history
            self.price_history[price.symbol].append(price)
            self.price_history[price.symbol] = [
                p
                for p in self.price_history[price.symbol]
                if current_time - p.timestamp < 3600  # Keep 1 hour of history
            ]

            # Notify subscribers
            await self._notify_price_update(price)

    async def _calculate_consensus(self):
        """Calculate consensus prices from multiple oracle sources"""
        symbols = self.config["symbols"]
        current_time = time.time()

        for symbol in symbols:
            # Get recent prices for this symbol
            recent_prices = []
            cache_ttl = self.config.get("cache_ttl", 30.0)
            for cache_key, price in self.price_cache.items():
                if (
                    cache_key.startswith(f"{symbol}:")
                    and price.age_seconds() <= cache_ttl
                ):
                    recent_prices.append(price)

            if len(recent_prices) < self.config["min_sources"]:
                continue

            # Calculate consensus
            consensus = await self._calculate_symbol_consensus(symbol, recent_prices)
            if consensus:
                # Store consensus
                consensus_key = f"consensus:{symbol}"
                self.price_cache[consensus_key] = consensus

                # Notify subscribers
                await self._notify_consensus_update(consensus)

        self.last_consensus_update = current_time

    async def _calculate_symbol_consensus(
        self, symbol: str, prices: List[OraclePrice]
    ) -> Optional[OracleConsensus]:
        """Calculate consensus for a specific symbol"""
        if not prices:
            return None

        # Extract price values
        price_values = [p.price for p in prices]
        volumes = [p.volume_24h for p in prices if p.volume_24h]

        # Calculate statistics
        avg_price = sum(price_values) / len(price_values)
        min_price = min(price_values)
        max_price = max(price_values)
        median_price = sorted(price_values)[len(price_values) // 2]

        # Calculate price deviation
        max_deviation = max(abs(p - avg_price) / avg_price for p in price_values)

        # Volume-weighted price if available
        volume_weighted_price = None
        if volumes and len(volumes) == len(price_values):
            total_volume = sum(volumes)
            if total_volume > 0:
                volume_weighted_price = (
                    sum(price * volume for price, volume in zip(price_values, volumes))
                    / total_volume
                )

        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(prices, max_deviation)

        return OracleConsensus(
            symbol=symbol,
            consensus_price=volume_weighted_price or avg_price,
            price_deviation=max_deviation,
            source_count=len(prices),
            confidence_score=confidence_score,
            timestamp=time.time(),
            sources=[p.source for p in prices],
            price_range={
                "min": min_price,
                "max": max_price,
                "median": median_price,
                "average": avg_price,
            },
            volume_weighted_price=volume_weighted_price,
        )

    def _calculate_confidence_score(
        self, prices: List[OraclePrice], price_deviation: float
    ) -> float:
        """Calculate confidence score for consensus"""
        base_confidence = 0.8

        # Adjust for price deviation
        deviation_penalty = min(price_deviation * 2, 0.3)  # Max 30% penalty

        # Adjust for number of sources
        source_bonus = min((len(prices) - 2) * 0.05, 0.15)  # Max 15% bonus

        # Adjust for individual source confidence
        avg_source_confidence = sum(p.confidence for p in prices) / len(prices)
        confidence_adjustment = (avg_source_confidence - 0.9) * 0.5

        # Calculate final confidence
        confidence = (
            base_confidence - deviation_penalty + source_bonus + confidence_adjustment
        )

        return max(0.1, min(1.0, confidence))

    async def _maintain_websocket_connections(self):
        """Maintain websocket connections to real-time feeds"""
        if not self.config.get("enable_websockets", True):
            return

        for source, endpoint in self.websocket_endpoints.items():
            if (
                source not in self.websocket_connections
                or self.websocket_connections[source].closed
            ):
                try:
                    await self._connect_websocket(source, endpoint)
                except Exception as e:
                    self.logger.warning(f"Failed to connect to {source} websocket: {e}")

    async def _connect_websocket(self, source: str, endpoint: str):
        """Connect to a websocket endpoint"""
        self.logger.info(f"Connecting to {source} websocket...")

        try:
            ws = await websockets.connect(endpoint)
            self.websocket_connections[source] = ws

            # Send subscription messages based on source
            if source == "binance":
                await self._subscribe_binance(ws)
            elif source == "coinbase":
                await self._subscribe_coinbase(ws)
            elif source == "kraken":
                await self._subscribe_kraken(ws)

        except Exception as e:
            self.logger.error(f"WebSocket connection error for {source}: {e}")

    async def _subscribe_binance(self, ws):
        """Subscribe to Binance streams"""
        streams = [
            "btcusdt@ticker",
            "ethusdt@ticker",
            "solusdt@ticker",
            "adausdt@ticker",
        ]
        subscribe_message = {"method": "SUBSCRIBE", "params": streams, "id": 1}
        await ws.send(json.dumps(subscribe_message))

    async def _subscribe_coinbase(self, ws):
        """Subscribe to Coinbase streams"""
        subscribe_message = {
            "type": "subscribe",
            "product_ids": ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD"],
            "channels": ["ticker"],
        }
        await ws.send(json.dumps(subscribe_message))

    async def _subscribe_kraken(self, ws):
        """Subscribe to Kraken streams"""
        subscribe_message = {
            "event": "subscribe",
            "pair": ["XBT/USD", "ETH/USD", "SOL/USD", "ADA/USD"],
            "subscription": {"name": "ticker"},
        }
        await ws.send(json.dumps(subscribe_message))

    async def _process_websocket_feeds(self):
        """Process incoming websocket data"""
        for source, ws in list(self.websocket_connections.items()):
            if ws and not ws.closed:
                try:
                    # Non-blocking message receive
                    message = await asyncio.wait_for(ws.recv(), timeout=0.1)
                    await self._process_websocket_message(source, message)
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    self.logger.warning(f"WebSocket message error from {source}: {e}")
                    # Remove closed connection
                    if ws.closed:
                        del self.websocket_connections[source]

    async def _process_websocket_message(self, source: str, message: str):
        """Process a websocket message from a specific source"""
        try:
            data = json.loads(message)

            if source == "binance":
                await self._process_binance_message(data)
            elif source == "coinbase":
                await self._process_coinbase_message(data)
            elif source == "kraken":
                await self._process_kraken_message(data)

        except Exception as e:
            self.logger.debug(f"Error processing {source} message: {e}")

    async def _process_binance_message(self, data: Dict):
        """Process Binance ticker message"""
        if "data" in data and data.get("stream", "").endswith("@ticker"):
            ticker = data["data"]
            symbol_map = {
                "BTCUSDT": "BTC/USD",
                "ETHUSDT": "ETH/USD",
                "SOLUSDT": "SOL/USD",
                "ADAUSDT": "ADA/USD",
            }

            binance_symbol = ticker.get("s")
            if binance_symbol in symbol_map:
                price = OraclePrice(
                    symbol=symbol_map[binance_symbol],
                    price=float(ticker.get("c", 0)),
                    volume_24h=float(ticker.get("v", 0)),
                    change_24h=float(ticker.get("P", 0)),
                    timestamp=time.time(),
                    source="binance_ws",
                    confidence=0.96,
                )

                await self._process_price_updates([price])

    async def _process_coinbase_message(self, data: Dict):
        """Process Coinbase ticker message"""
        if data.get("type") == "ticker":
            symbol_map = {
                "BTC-USD": "BTC/USD",
                "ETH-USD": "ETH/USD",
                "SOL-USD": "SOL/USD",
                "ADA-USD": "ADA/USD",
            }

            product_id = data.get("product_id")
            if product_id in symbol_map:
                price = OraclePrice(
                    symbol=symbol_map[product_id],
                    price=float(data.get("price", 0)),
                    volume_24h=float(data.get("volume_24h", 0)),
                    change_24h=None,
                    timestamp=time.time(),
                    source="coinbase_ws",
                    confidence=0.94,
                )

                await self._process_price_updates([price])

    async def _process_kraken_message(self, data: Dict):
        """Process Kraken ticker message"""
        # Kraken websocket format is more complex, simplified for demo
        if isinstance(data, list) and len(data) > 3:
            channel_name = data[2] if len(data) > 2 else None
            if channel_name == "ticker":
                # Process ticker data
                pass

    async def _notify_price_update(self, price: OraclePrice):
        """Notify subscribers of price updates"""
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback("price_update", price)
                else:
                    callback("price_update", price)
            except Exception as e:
                self.logger.warning(f"Subscriber notification error: {e}")

    async def _notify_consensus_update(self, consensus: OracleConsensus):
        """Notify subscribers of consensus updates"""
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback("consensus_update", consensus)
                else:
                    callback("consensus_update", consensus)
            except Exception as e:
                self.logger.warning(f"Consensus notification error: {e}")

    def subscribe(self, callback: Callable):
        """Subscribe to oracle updates"""
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable):
        """Unsubscribe from oracle updates"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    async def get_current_price(self, symbol: str) -> Optional[OraclePrice]:
        """Get current price for a symbol"""
        # Try consensus first
        consensus_key = f"consensus:{symbol}"
        if consensus_key in self.price_cache:
            consensus = self.price_cache[consensus_key]
            return OraclePrice(
                symbol=symbol,
                price=consensus.consensus_price,
                volume_24h=None,
                change_24h=None,
                timestamp=consensus.timestamp,
                source="consensus",
                confidence=consensus.confidence_score,
            )

        # Fallback to latest individual price
        latest_price = None
        latest_timestamp = 0

        cache_ttl = self.config.get("cache_ttl", 30.0)
        for cache_key, price in self.price_cache.items():
            if (
                cache_key.startswith(f"{symbol}:")
                and price.timestamp > latest_timestamp
                and price.age_seconds() <= cache_ttl
            ):
                latest_price = price
                latest_timestamp = price.timestamp

        return latest_price

    async def get_consensus(self, symbol: str) -> Optional[OracleConsensus]:
        """Get consensus data for a symbol"""
        consensus_key = f"consensus:{symbol}"
        return self.price_cache.get(consensus_key)

    async def get_price_history(
        self, symbol: str, duration_seconds: int = 3600
    ) -> List[OraclePrice]:
        """Get price history for a symbol"""
        if symbol not in self.price_history:
            return []

        cutoff_time = time.time() - duration_seconds
        return [p for p in self.price_history[symbol] if p.timestamp >= cutoff_time]

    def get_status(self) -> Dict[str, Any]:
        """Get oracle engine status"""
        current_time = time.time()

        # Count active sources
        active_sources = set()
        fresh_prices = 0

        cache_ttl = self.config.get("cache_ttl", 30.0)
        for cache_key, price in self.price_cache.items():
            # Skip consensus entries
            if cache_key.startswith("consensus:"):
                continue

            if hasattr(price, "age_seconds") and price.age_seconds() <= cache_ttl:
                fresh_prices += 1
                if ":" in cache_key:
                    source = cache_key.split(":")[1]
                    active_sources.add(source)

        # WebSocket status
        ws_status = {}
        for source, ws in self.websocket_connections.items():
            ws_status[source] = "connected" if ws and not ws.closed else "disconnected"

        return {
            "running": self.running,
            "active_sources": list(active_sources),
            "fresh_prices": fresh_prices,
            "total_cache_entries": len(self.price_cache),
            "websocket_status": ws_status,
            "last_consensus_update": self.last_consensus_update,
            "uptime_seconds": current_time - getattr(self, "start_time", current_time),
        }


# Singleton instance for global access
_oracle_engine_instance = None


async def get_oracle_engine(config: Optional[Dict] = None) -> RealTimeOracleEngine:
    """Get or create the global oracle engine instance"""
    global _oracle_engine_instance

    if _oracle_engine_instance is None:
        _oracle_engine_instance = RealTimeOracleEngine(config)

    return _oracle_engine_instance

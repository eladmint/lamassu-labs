#!/usr/bin/env python3
"""
Mento Analytics API Client
Real integration with Mento Protocol's analytics API for reserve and stablecoin monitoring
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import aiohttp


@dataclass
class StablecoinInfo:
    """Mento stablecoin information"""

    symbol: str
    name: str
    address: str
    supply_amount: str
    supply_usd: float
    decimals: int
    fiat_symbol: str
    icon_url: Optional[str] = None


@dataclass
class ReserveAsset:
    """Reserve asset information"""

    symbol: str
    balance: str
    usd_value: float
    chain: str
    address: str


@dataclass
class ReserveStats:
    """Reserve statistics including collateralization"""

    total_holdings_usd: float
    total_stablecoins_usd: float
    collateralization_ratio: float
    reserve_composition: Dict[str, float]
    last_updated: datetime


class MentoAnalyticsClient:
    """Client for interacting with Mento Analytics API"""

    # Potential production endpoints (to be confirmed)
    ENDPOINTS = [
        "http://localhost:3000",  # Local development
        "https://api.mento.org",
        "https://mento-analytics-api.mento.org",
        "https://analytics.mento.org",
    ]

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or self.ENDPOINTS[0]
        self.session = None
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Match API's cache duration

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _fetch(self, endpoint: str) -> Dict[str, Any]:
        """Fetch data from API with caching"""
        cache_key = f"{self.base_url}{endpoint}"

        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data

        # Make request
        try:
            async with self.session.get(f"{self.base_url}{endpoint}") as response:
                if response.status == 200:
                    data = await response.json()
                    self.cache[cache_key] = (data, datetime.now())
                    return data
                else:
                    print(f"API request failed: {response.status}")
                    return {}
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")
            return {}

    async def get_health(self) -> Dict[str, Any]:
        """Check API health status"""
        return await self._fetch("/api/v1/health")

    async def get_stablecoins(self) -> List[StablecoinInfo]:
        """Get all Mento stablecoins with supply information"""
        data = await self._fetch("/api/v1/stablecoins")

        stablecoins = []
        for coin in data.get("stablecoins", []):
            stablecoins.append(
                StablecoinInfo(
                    symbol=coin["symbol"],
                    name=coin["name"],
                    address=coin["address"],
                    supply_amount=coin["supply"]["amount"],
                    supply_usd=coin["supply"]["usd_value"],
                    decimals=coin["decimals"],
                    fiat_symbol=coin["fiat_symbol"],
                    icon_url=coin.get("icon_url"),
                )
            )

        return stablecoins

    async def get_reserve_holdings(self) -> List[ReserveAsset]:
        """Get detailed reserve holdings"""
        data = await self._fetch("/api/v1/reserve/holdings")

        assets = []
        for asset in data.get("assets", []):
            assets.append(
                ReserveAsset(
                    symbol=asset["symbol"],
                    balance=asset["balance"],
                    usd_value=asset["usdValue"],
                    chain=asset["chain"],
                    address=asset["address"],
                )
            )

        return assets

    async def get_reserve_composition(self) -> Dict[str, float]:
        """Get reserve composition percentages"""
        data = await self._fetch("/api/v1/reserve/composition")
        return data

    async def get_reserve_stats(self) -> ReserveStats:
        """Get comprehensive reserve statistics"""
        stats_data = await self._fetch("/api/v1/reserve/stats")
        composition_data = await self.get_reserve_composition()
        stablecoins_data = await self._fetch("/api/v1/stablecoins")

        # Extract composition from the response
        composition = {}
        if isinstance(composition_data, dict) and "composition" in composition_data:
            for item in composition_data["composition"]:
                composition[item["symbol"]] = item["percentage"]

        return ReserveStats(
            total_holdings_usd=stats_data.get("total_reserve_value_usd", 0),
            total_stablecoins_usd=stats_data.get("total_outstanding_stables_usd", 0),
            collateralization_ratio=stats_data.get("collateralization_ratio", 0),
            reserve_composition=composition,
            last_updated=datetime.now(),
        )

    async def get_collateralization_ratio(self) -> float:
        """Calculate current collateralization ratio"""
        stats = await self.get_reserve_stats()
        return stats.collateralization_ratio

    async def check_health_alerts(self) -> List[Dict[str, Any]]:
        """Check for any health alerts based on reserve metrics"""
        alerts = []
        stats = await self.get_reserve_stats()

        # Check collateralization ratio
        if stats.collateralization_ratio < 2.0:
            alerts.append(
                {
                    "severity": "HIGH",
                    "type": "COLLATERALIZATION_LOW",
                    "message": f"Collateralization ratio below target: {stats.collateralization_ratio:.2f}x (target: 2.0x)",
                    "value": stats.collateralization_ratio,
                }
            )

        # Check reserve composition balance
        for asset, percentage in stats.reserve_composition.items():
            if percentage > 50:  # Alert if any single asset is >50%
                alerts.append(
                    {
                        "severity": "MEDIUM",
                        "type": "CONCENTRATION_RISK",
                        "message": f"{asset} represents {percentage:.1f}% of reserves",
                        "asset": asset,
                        "percentage": percentage,
                    }
                )

        return alerts


async def demo_mento_integration():
    """Demonstrate real Mento Analytics API integration"""
    print("🌐 Mento Analytics API Integration Demo")
    print("=" * 60)

    async with MentoAnalyticsClient() as client:
        # 1. Check API health
        print("\n📊 Checking API Health...")
        health = await client.get_health()
        print(f"API Status: {health.get('status', 'Unknown')}")

        # 2. Get stablecoin information
        print("\n💰 Mento Stablecoins:")
        stablecoins = await client.get_stablecoins()
        total_supply_usd = sum(coin.supply_usd for coin in stablecoins)

        for coin in stablecoins[:5]:  # Show first 5
            print(f"  {coin.symbol}: ${coin.supply_usd:,.0f} ({coin.fiat_symbol})")

        print(f"\nTotal Stablecoin Supply: ${total_supply_usd:,.0f}")

        # 3. Get reserve holdings
        print("\n🏦 Reserve Holdings:")
        holdings = await client.get_reserve_holdings()
        total_reserves_usd = sum(asset.usd_value for asset in holdings)

        # Group by chain
        by_chain = {}
        for asset in holdings:
            if asset.chain not in by_chain:
                by_chain[asset.chain] = 0
            by_chain[asset.chain] += asset.usd_value

        for chain, value in by_chain.items():
            print(f"  {chain}: ${value:,.0f} ({value/total_reserves_usd*100:.1f}%)")

        print(f"\nTotal Reserve Value: ${total_reserves_usd:,.0f}")

        # 4. Calculate collateralization
        print("\n📈 Collateralization Metrics:")
        stats = await client.get_reserve_stats()
        print(f"  Collateralization Ratio: {stats.collateralization_ratio:.2f}x")
        print(f"  Reserve/Supply Ratio: {total_reserves_usd/total_supply_usd:.2f}x")

        # 5. Check for alerts
        print("\n🚨 Health Alerts:")
        alerts = await client.check_health_alerts()
        if alerts:
            for alert in alerts:
                print(f"  [{alert['severity']}] {alert['message']}")
        else:
            print("  ✅ All metrics within healthy ranges")

        # 6. Show reserve composition
        print("\n📊 Reserve Composition:")
        composition_data = await client.get_reserve_composition()
        if isinstance(composition_data, dict) and "composition" in composition_data:
            for item in sorted(
                composition_data["composition"],
                key=lambda x: x["percentage"],
                reverse=True,
            ):
                print(f"  {item['symbol']}: {item['percentage']:.1f}%")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_mento_integration())

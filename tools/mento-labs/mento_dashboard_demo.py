#!/usr/bin/env python3
"""
Mento Reserve Dashboard Demo
Professional dashboard showing real-time Mento Protocol data
"""

import asyncio
import json
from datetime import datetime

from mento_analytics_client import MentoAnalyticsClient


class MentoReserveDashboard:
    """Professional dashboard for Mento Reserve monitoring"""

    def __init__(self):
        self.client = MentoAnalyticsClient()

    async def generate_dashboard_json(self):
        """Generate complete dashboard data in JSON format"""
        async with self.client as client:
            # Fetch all data
            health = await client.get_health()
            stablecoins = await client.get_stablecoins()
            holdings = await client.get_reserve_holdings()
            stats = await client.get_reserve_stats()
            alerts = await client.check_health_alerts()
            composition = await client.get_reserve_composition()

            # Calculate additional metrics
            total_supply = sum(coin.supply_usd for coin in stablecoins)
            total_reserves = sum(asset.usd_value for asset in holdings)

            # Group holdings by chain
            by_chain = {}
            for asset in holdings:
                if asset.chain not in by_chain:
                    by_chain[asset.chain] = []
                by_chain[asset.chain].append(
                    {
                        "symbol": asset.symbol,
                        "balance": asset.balance,
                        "usd_value": asset.usd_value,
                    }
                )

            # Build dashboard data
            dashboard_data = {
                "metadata": {
                    "title": "Mento Reserve Monitor - Powered by Nuru AI",
                    "description": "Real-time monitoring of Mento Protocol reserves and stablecoin metrics",
                    "generated_at": datetime.now().isoformat(),
                    "api_status": health.get("status", "unknown"),
                },
                "summary": {
                    "total_reserves_usd": total_reserves,
                    "total_stablecoins_usd": total_supply,
                    "collateralization_ratio": stats.collateralization_ratio,
                    "health_status": "WARNING" if alerts else "HEALTHY",
                    "active_stablecoins": len(stablecoins),
                    "reserve_assets": len(holdings),
                },
                "stablecoins": [
                    {
                        "symbol": coin.symbol,
                        "name": coin.name,
                        "supply_usd": coin.supply_usd,
                        "fiat_currency": coin.fiat_symbol,
                        "market_share": (coin.supply_usd / total_supply) * 100,
                    }
                    for coin in stablecoins
                ],
                "reserves_by_chain": by_chain,
                "reserve_composition": (
                    composition.get("composition", [])
                    if isinstance(composition, dict)
                    else []
                ),
                "health_alerts": alerts,
                "recommendations": self.generate_recommendations(stats, alerts),
                "visualization_data": {
                    "collateralization_timeline": self.generate_timeline_data(stats),
                    "reserve_pie_chart": self.generate_pie_chart_data(composition),
                    "stablecoin_distribution": self.generate_distribution_data(
                        stablecoins
                    ),
                },
            }

            return dashboard_data

    def generate_recommendations(self, stats, alerts):
        """Generate actionable recommendations based on metrics"""
        recommendations = []

        if stats.collateralization_ratio < 2.0:
            recommendations.append(
                {
                    "priority": "HIGH",
                    "title": "Increase Reserve Holdings",
                    "description": f"Current ratio {stats.collateralization_ratio:.2f}x is below 2.0x target",
                    "action": "Consider adding more reserve assets or reducing stablecoin supply",
                }
            )

        # Check for concentration risk
        concentration_alerts = [
            a for a in alerts if a.get("type") == "CONCENTRATION_RISK"
        ]
        if concentration_alerts:
            recommendations.append(
                {
                    "priority": "MEDIUM",
                    "title": "Diversify Reserve Assets",
                    "description": "Single asset concentration exceeds 50%",
                    "action": "Rebalance portfolio to reduce concentration risk",
                }
            )

        if stats.collateralization_ratio > 2.5:
            recommendations.append(
                {
                    "priority": "LOW",
                    "title": "Capital Efficiency Opportunity",
                    "description": f"High collateralization ratio {stats.collateralization_ratio:.2f}x",
                    "action": "Consider expanding stablecoin supply or deploying excess reserves",
                }
            )

        return recommendations

    def generate_timeline_data(self, stats):
        """Generate timeline visualization data"""
        # In production, this would fetch historical data
        # For demo, we'll simulate a timeline
        current = stats.collateralization_ratio
        return {
            "labels": ["6h ago", "4h ago", "2h ago", "1h ago", "30m ago", "Now"],
            "values": [
                current * 0.98,
                current * 0.99,
                current * 1.01,
                current * 1.00,
                current * 0.99,
                current,
            ],
            "target_line": 2.0,
        }

    def generate_pie_chart_data(self, composition):
        """Generate pie chart data for reserve composition"""
        if isinstance(composition, dict) and "composition" in composition:
            return [
                {
                    "name": item["symbol"],
                    "value": item["percentage"],
                    "usd_value": item.get("usd_value", 0),
                }
                for item in composition["composition"]
            ]
        return []

    def generate_distribution_data(self, stablecoins):
        """Generate stablecoin distribution data"""
        total = sum(coin.supply_usd for coin in stablecoins)
        return [
            {
                "name": coin.symbol,
                "percentage": (coin.supply_usd / total) * 100,
                "value": coin.supply_usd,
                "fiat": coin.fiat_symbol,
            }
            for coin in stablecoins
        ]

    async def display_dashboard(self):
        """Display the dashboard in terminal format"""
        data = await self.generate_dashboard_json()

        print("\n" + "=" * 80)
        print(f"🏦 {data['metadata']['title']}")
        print("=" * 80)
        print(f"Generated: {data['metadata']['generated_at']}")
        print(f"API Status: {data['metadata']['api_status']}")

        # Summary Section
        print("\n📊 EXECUTIVE SUMMARY")
        print("-" * 40)
        summary = data["summary"]
        print(f"Total Reserves:         ${summary['total_reserves_usd']:,.0f}")
        print(f"Total Stablecoins:      ${summary['total_stablecoins_usd']:,.0f}")
        print(f"Collateralization:      {summary['collateralization_ratio']:.2f}x")
        print(f"Health Status:          {summary['health_status']}")
        print(f"Active Stablecoins:     {summary['active_stablecoins']}")
        print(f"Reserve Assets:         {summary['reserve_assets']}")

        # Stablecoins Section
        print("\n💰 STABLECOIN METRICS")
        print("-" * 40)
        for coin in data["stablecoins"]:
            print(
                f"{coin['symbol']:6} | ${coin['supply_usd']:>12,.0f} | {coin['market_share']:>5.1f}% | {coin['fiat_currency']}"
            )

        # Reserve Composition
        print("\n🏛️ RESERVE COMPOSITION")
        print("-" * 40)
        for item in data["reserve_composition"][:6]:
            bar = "█" * int(item["percentage"] / 2)
            print(f"{item['symbol']:6} | {bar:<25} | {item['percentage']:>5.1f}%")

        # Health Alerts
        if data["health_alerts"]:
            print("\n⚠️  ACTIVE ALERTS")
            print("-" * 40)
            for alert in data["health_alerts"]:
                print(f"[{alert['severity']}] {alert['message']}")

        # Recommendations
        print("\n💡 RECOMMENDATIONS")
        print("-" * 40)
        for rec in data["recommendations"]:
            print(f"[{rec['priority']}] {rec['title']}")
            print(f"       → {rec['action']}")

        # Save full data to JSON
        with open("mento_dashboard_data.json", "w") as f:
            json.dump(data, f, indent=2, default=str)
        print("\n✅ Full dashboard data saved to: mento_dashboard_data.json")

        return data


async def main():
    """Run the dashboard demo"""
    dashboard = MentoReserveDashboard()

    # Display dashboard
    await dashboard.display_dashboard()

    # Show how this integrates with our Oracle system
    print("\n" + "=" * 80)
    print("🔮 NURU AI - MENTO ORACLE INTEGRATION")
    print("=" * 80)
    print("\n🎯 What We've Built:")
    print("  ✅ Real-time integration with Mento Analytics API")
    print("  ✅ Professional reserve monitoring dashboard")
    print("  ✅ Health alerts and risk assessment")
    print("  ✅ Actionable recommendations based on metrics")
    print("  ✅ Export data for further analysis")

    print("\n🚀 Next Steps for Mento Partnership:")
    print("  1. Add ZK proof verification layer for reserve attestations")
    print("  2. Integrate with Chainlink oracles for price feeds")
    print("  3. Build automated alert system for treasury managers")
    print("  4. Create white-label solution for Mento partners")

    print("\n💼 Business Value:")
    print("  • Real-time reserve transparency")
    print("  • Risk management insights")
    print("  • Compliance reporting")
    print("  • Partner confidence building")


if __name__ == "__main__":
    asyncio.run(main())

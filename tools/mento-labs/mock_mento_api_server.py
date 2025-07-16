#!/usr/bin/env python3
"""
Mock Mento Analytics API Server
Provides realistic data based on Mento Protocol structure
"""

from datetime import datetime

from aiohttp import web


class MockMentoAPI:
    def __init__(self):
        # Realistic Mento stablecoins
        self.stablecoins_data = [
            {
                "symbol": "cUSD",
                "name": "Celo Dollar",
                "address": "0x765DE816845861e75A25fCA122bb6898B8B1282a",
                "decimals": 18,
                "fiat_symbol": "USD",
                "supply": {
                    "amount": "42850000000000000000000000",
                    "usd_value": 42850000.0,
                },
                "icon_url": "https://raw.githubusercontent.com/mento-protocol/mento-web/main/public/icons/cusd.svg",
            },
            {
                "symbol": "cEUR",
                "name": "Celo Euro",
                "address": "0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73",
                "decimals": 18,
                "fiat_symbol": "EUR",
                "supply": {
                    "amount": "15230000000000000000000000",
                    "usd_value": 16500000.0,
                },
                "icon_url": "https://raw.githubusercontent.com/mento-protocol/mento-web/main/public/icons/ceur.svg",
            },
            {
                "symbol": "cREAL",
                "name": "Celo Brazilian Real",
                "address": "0xe8537a3d056DA446677B9E9d6c5dB704EaAb4787",
                "decimals": 18,
                "fiat_symbol": "BRL",
                "supply": {
                    "amount": "8920000000000000000000000",
                    "usd_value": 1850000.0,
                },
                "icon_url": "https://raw.githubusercontent.com/mento-protocol/mento-web/main/public/icons/creal.svg",
            },
            {
                "symbol": "eXOF",
                "name": "CFA Franc",
                "address": "0x73F93dcc49cB8A239e2032663e9475dd5ef29A08",
                "decimals": 18,
                "fiat_symbol": "XOF",
                "supply": {
                    "amount": "3450000000000000000000000",
                    "usd_value": 5800000.0,
                },
                "icon_url": "https://raw.githubusercontent.com/mento-protocol/mento-web/main/public/icons/exof.svg",
            },
            {
                "symbol": "cKES",
                "name": "Celo Kenyan Shilling",
                "address": "0x456a3D042C0DbD3db53D5489e98dFb038553B0d0",
                "decimals": 18,
                "fiat_symbol": "KES",
                "supply": {
                    "amount": "2150000000000000000000000",
                    "usd_value": 1650000.0,
                },
                "icon_url": "https://raw.githubusercontent.com/mento-protocol/mento-web/main/public/icons/ckes.svg",
            },
        ]

        # Realistic reserve holdings
        self.reserve_holdings_data = [
            # Bitcoin holdings
            {
                "symbol": "BTC",
                "balance": "342.85",
                "usdValue": 34285000.0,
                "chain": "bitcoin",
                "address": "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h",
            },
            # Ethereum holdings
            {
                "symbol": "ETH",
                "balance": "8567.32",
                "usdValue": 30000000.0,
                "chain": "ethereum",
                "address": "0x87647780180B8f55980C7D3fFeFe08a9B29e9aE1",
            },
            {
                "symbol": "USDC",
                "balance": "25000000",
                "usdValue": 25000000.0,
                "chain": "ethereum",
                "address": "0x87647780180B8f55980C7D3fFeFe08a9B29e9aE1",
            },
            # Celo holdings
            {
                "symbol": "CELO",
                "balance": "45000000",
                "usdValue": 22500000.0,
                "chain": "celo",
                "address": "0x9380fA34Fd9e4Fd14c06305fd7B6199089eD4eb9",
            },
            {
                "symbol": "wBTC",
                "balance": "125.42",
                "usdValue": 12542000.0,
                "chain": "celo",
                "address": "0xBAAB46E28388d2779e6E31Fd00cF0e5Ad95E327B",
            },
            {
                "symbol": "wETH",
                "balance": "2850.75",
                "usdValue": 9977625.0,
                "chain": "celo",
                "address": "0x2DEf4285787d58a2f811AF24755A8150622f4361",
            },
        ]

    async def health(self, request):
        """Health check endpoint"""
        return web.json_response(
            {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "services": {
                    "database": "connected",
                    "blockchain": "synced",
                    "cache": "active",
                },
            }
        )

    async def stablecoins(self, request):
        """Get all stablecoins"""
        total_supply_usd = sum(
            coin["supply"]["usd_value"] for coin in self.stablecoins_data
        )

        return web.json_response(
            {
                "stablecoins": self.stablecoins_data,
                "total_supply_usd": total_supply_usd,
                "last_updated": datetime.now().isoformat(),
            }
        )

    async def reserve_holdings(self, request):
        """Get reserve holdings"""
        total_holdings_usd = sum(
            asset["usdValue"] for asset in self.reserve_holdings_data
        )

        return web.json_response(
            {
                "total_holdings_usd": total_holdings_usd,
                "assets": self.reserve_holdings_data,
                "last_updated": datetime.now().isoformat(),
            }
        )

    async def reserve_composition(self, request):
        """Get reserve composition"""
        total_value = sum(asset["usdValue"] for asset in self.reserve_holdings_data)

        # Group by symbol and calculate percentages
        composition_map = {}
        for asset in self.reserve_holdings_data:
            symbol = asset["symbol"]
            if symbol not in composition_map:
                composition_map[symbol] = 0
            composition_map[symbol] += asset["usdValue"]

        composition = []
        for symbol, usd_value in composition_map.items():
            composition.append(
                {
                    "symbol": symbol,
                    "percentage": (usd_value / total_value) * 100,
                    "usd_value": usd_value,
                }
            )

        return web.json_response(
            {
                "composition": sorted(
                    composition, key=lambda x: x["percentage"], reverse=True
                ),
                "last_updated": datetime.now().isoformat(),
            }
        )

    async def reserve_stats(self, request):
        """Get reserve statistics"""
        total_reserve_value_usd = sum(
            asset["usdValue"] for asset in self.reserve_holdings_data
        )
        total_outstanding_stables_usd = sum(
            coin["supply"]["usd_value"] for coin in self.stablecoins_data
        )

        return web.json_response(
            {
                "total_reserve_value_usd": total_reserve_value_usd,
                "total_outstanding_stables_usd": total_outstanding_stables_usd,
                "collateralization_ratio": total_reserve_value_usd
                / total_outstanding_stables_usd,
                "timestamp": datetime.now().isoformat(),
            }
        )

    async def reserve_addresses(self, request):
        """Get reserve addresses"""
        addresses = [
            {
                "network": "bitcoin",
                "category": "main",
                "addresses": [
                    {
                        "address": "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h",
                        "label": "Bitcoin Reserve",
                    }
                ],
            },
            {
                "network": "ethereum",
                "category": "main",
                "addresses": [
                    {
                        "address": "0x87647780180B8f55980C7D3fFeFe08a9B29e9aE1",
                        "label": "Ethereum Reserve",
                    }
                ],
            },
            {
                "network": "celo",
                "category": "main",
                "addresses": [
                    {
                        "address": "0x9380fA34Fd9e4Fd14c06305fd7B6199089eD4eb9",
                        "label": "Celo Reserve",
                    },
                    {
                        "address": "0xBAAB46E28388d2779e6E31Fd00cF0e5Ad95E327B",
                        "label": "Celo Reserve wBTC",
                    },
                    {
                        "address": "0x2DEf4285787d58a2f811AF24755A8150622f4361",
                        "label": "Celo Reserve wETH",
                    },
                ],
            },
        ]

        return web.json_response(
            {"addresses": addresses, "last_updated": datetime.now().isoformat()}
        )

    async def reserve_holdings_grouped(self, request):
        """Get grouped reserve holdings"""
        # Group holdings by symbol
        grouped = {}
        for asset in self.reserve_holdings_data:
            symbol = asset["symbol"]
            if symbol not in grouped:
                grouped[symbol] = {"symbol": symbol, "usdValue": 0, "holdings": []}
            grouped[symbol]["usdValue"] += asset["usdValue"]
            grouped[symbol]["holdings"].append(
                {
                    "chain": asset["chain"],
                    "balance": asset["balance"],
                    "usdValue": asset["usdValue"],
                }
            )

        assets = list(grouped.values())
        total_holdings_usd = sum(asset["usdValue"] for asset in assets)

        return web.json_response(
            {
                "total_holdings_usd": total_holdings_usd,
                "assets": sorted(assets, key=lambda x: x["usdValue"], reverse=True),
                "last_updated": datetime.now().isoformat(),
            }
        )


def create_app():
    """Create the mock API application"""
    api = MockMentoAPI()
    app = web.Application()

    # Add routes
    app.router.add_get("/api/v1/health", api.health)
    app.router.add_get("/api/v1/stablecoins", api.stablecoins)
    app.router.add_get("/api/v1/reserve/holdings", api.reserve_holdings)
    app.router.add_get("/api/v1/reserve/composition", api.reserve_composition)
    app.router.add_get("/api/v1/reserve/stats", api.reserve_stats)
    app.router.add_get("/api/v1/reserve/addresses", api.reserve_addresses)
    app.router.add_get("/api/v1/reserve/holdings/grouped", api.reserve_holdings_grouped)

    return app


if __name__ == "__main__":
    app = create_app()
    print("🚀 Mock Mento Analytics API running on http://localhost:3000")
    print("📊 Endpoints:")
    print("  - GET /api/v1/health")
    print("  - GET /api/v1/stablecoins")
    print("  - GET /api/v1/reserve/holdings")
    print("  - GET /api/v1/reserve/composition")
    print("  - GET /api/v1/reserve/stats")
    print("  - GET /api/v1/reserve/addresses")
    print("  - GET /api/v1/reserve/holdings/grouped")
    web.run_app(app, host="localhost", port=3000)

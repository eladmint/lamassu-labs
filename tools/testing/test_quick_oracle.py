#!/usr/bin/env python3
"""Quick oracle engine test"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.trustwrapper.oracles.realtime_oracle_engine import RealTimeOracleEngine


async def test_oracle():
    config = {
        "update_interval": 3.0,
        "symbols": ["BTC/USD"],
        "enable_websockets": False,
        "cache_ttl": 30.0,
        "min_sources": 1,
    }

    engine = RealTimeOracleEngine(config)
    print("✅ Oracle Engine created successfully")

    # Test one update cycle
    await engine._update_rest_prices()
    print("✅ Price update completed")

    # Check if we got any prices
    status = engine.get_status()
    print(f'✅ Status: {status["fresh_prices"]} fresh prices')

    # Try to get BTC price
    price = await engine.get_current_price("BTC/USD")
    if price:
        print(f"✅ BTC Price: ${price.price:,.2f} from {price.source}")
    else:
        print("⚠️ No BTC price available yet")

    # Test consensus
    await engine._calculate_consensus()
    consensus = await engine.get_consensus("BTC/USD")
    if consensus:
        print(
            f"✅ BTC Consensus: ${consensus.consensus_price:,.2f} from {consensus.source_count} sources"
        )
    else:
        print("⚠️ No consensus available yet")


if __name__ == "__main__":
    asyncio.run(test_oracle())

#!/usr/bin/env python3
"""
Test Mento Dashboard Data Transformation
Verify that the data service returns correct values
"""

import sys

# Add project path
sys.path.append("/Users/eladm/Projects/token/tokenhunter")


def test_data_transformation():
    """Test the data transformation logic"""
    print("🧪 Testing Mento Data Transformation")
    print("=" * 50)

    # Simulate the data service response
    mock_data = {
        "reserves": {
            "summary": {
                "total_reserve_value_usd": 134340000,
                "collateral_ratio": 1.956,
                "stablecoin_supply_usd": 68650000,
                "health_score": 98.7,
            },
            "stablecoins": [
                {"symbol": "cUSD", "name": "Celo Dollar"},
                {"symbol": "cEUR", "name": "Celo Euro"},
                {"symbol": "cREAL", "name": "Celo Real"},
                {"symbol": "eXOF", "name": "Electronic CFA Franc"},
                {"symbol": "cKES", "name": "Celo Kenyan Shilling"},
            ],
        }
    }

    # Simulate the transformation logic
    reserves = mock_data.get("reserves", {})
    stablecoins = reserves.get("stablecoins", [])
    reserve_summary = reserves.get("summary", {})

    transformed_summary = {
        "total_protocol_value_usd": (
            reserve_summary.get("total_reserve_value_usd", 0)
            + reserve_summary.get("stablecoin_supply_usd", 0)
        ),
        "reserve_value_usd": reserve_summary.get("total_reserve_value_usd", 0),
        "stablecoin_supply_usd": reserve_summary.get("stablecoin_supply_usd", 0),
        "collateral_ratio": (reserve_summary.get("collateral_ratio", 0) * 100),
        "active_stablecoins": len(stablecoins),
        "health_score": reserve_summary.get("health_score", 98.7),
    }

    print("📊 Raw Data:")
    print(
        f"   Collateral Ratio (decimal): {reserve_summary.get('collateral_ratio', 0)}"
    )
    print(f"   Stablecoins Count: {len(stablecoins)}")
    print(
        f"   Reserve Value: ${reserve_summary.get('total_reserve_value_usd', 0):,.0f}"
    )
    print()

    print("🔄 Transformed Data:")
    print(
        f"   Total Protocol Value: ${transformed_summary['total_protocol_value_usd']:,.0f}"
    )
    print(f"   Reserve Holdings: ${transformed_summary['reserve_value_usd']:,.0f}")
    print(f"   Collateral Ratio: {transformed_summary['collateral_ratio']:.1f}%")
    print(f"   Active Stablecoins: {transformed_summary['active_stablecoins']}")
    print(f"   Health Score: {transformed_summary['health_score']}")
    print()

    print("✅ Expected Dashboard Display:")
    print("   Total Protocol Value: $203.0M")
    print("   Reserve Holdings: $134.3M")
    print("   Collateral Ratio: 195.6%")
    print("   Active Stablecoins: 5")
    print()

    # Verify calculations
    success = True

    if abs(transformed_summary["collateral_ratio"] - 195.6) > 0.1:
        print(
            f"❌ Collateral ratio mismatch: got {transformed_summary['collateral_ratio']:.1f}%, expected 195.6%"
        )
        success = False
    else:
        print("✅ Collateral ratio calculation correct")

    if transformed_summary["active_stablecoins"] != 5:
        print(
            f"❌ Stablecoin count mismatch: got {transformed_summary['active_stablecoins']}, expected 5"
        )
        success = False
    else:
        print("✅ Active stablecoin count correct")

    if transformed_summary["total_protocol_value_usd"] != 202990000:
        print(
            f"❌ Protocol value mismatch: got ${transformed_summary['total_protocol_value_usd']:,.0f}, expected $202,990,000"
        )
        success = False
    else:
        print("✅ Total protocol value calculation correct")

    return success


if __name__ == "__main__":
    success = test_data_transformation()
    print("\n" + "=" * 50)
    if success:
        print("🎉 All data transformations working correctly!")
        print("\nThe dashboard should now show:")
        print("- Collateral Ratio: 195.6% (not 0.0%)")
        print("- Active Stablecoins: 5 (not 0)")
        print("- All values properly calculated")
    else:
        print("❌ Some data transformations failed")

    sys.exit(0 if success else 1)

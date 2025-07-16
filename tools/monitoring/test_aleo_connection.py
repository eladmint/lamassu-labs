#!/usr/bin/env python3
"""Test Aleo blockchain API connection for our deployed contracts."""

import json
import urllib.error
import urllib.request
from datetime import datetime

CONTRACTS = [
    "hallucination_verifier.aleo",
    "agent_registry_v2.aleo",
    "trust_verifier_v2.aleo",
]

ENDPOINTS = [
    "https://api.explorer.provable.com/v1",
    "https://api.explorer.aleo.org/v1",
]


def test_endpoint(endpoint, contract_id):
    """Test if we can fetch contract data from an endpoint."""
    url = f"{endpoint}/testnet3/program/{contract_id}"
    print(f"\nTesting: {url}")

    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "Lamassu-Labs-Test/1.0",
            },
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            print(f"✅ Success! Found program: {contract_id}")
            print(f"   Network: {data.get('network', 'unknown')}")
            if "functions" in data:
                print(f"   Functions: {len(data['functions'])}")
            if "mappings" in data:
                print(f"   Mappings: {len(data['mappings'])}")
            return True, data

    except urllib.error.HTTPError as e:
        print(f"❌ Failed: HTTP {e.code}")
        return False, None
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
        return False, None


def test_transactions(endpoint, contract_id):
    """Test if we can fetch transaction data."""
    paths = [
        f"/testnet3/program/{contract_id}/transitions?limit=5",
        f"/testnet3/transitions?program={contract_id}&limit=5",
    ]

    for path in paths:
        url = endpoint + path
        print(f"\nTesting transactions: {url}")

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "Lamassu-Labs-Test/1.0",
                },
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())

                # Count transactions
                tx_count = 0
                if "transitions" in data:
                    tx_count = len(data["transitions"])
                elif "transactions" in data:
                    tx_count = len(data["transactions"])
                elif isinstance(data, list):
                    tx_count = len(data)

                if tx_count > 0:
                    print(f"✅ Found {tx_count} transactions")
                    # Show first transaction
                    first_tx = None
                    if "transitions" in data and data["transitions"]:
                        first_tx = data["transitions"][0]
                    elif "transactions" in data and data["transactions"]:
                        first_tx = data["transactions"][0]
                    elif isinstance(data, list) and data:
                        first_tx = data[0]

                    if first_tx:
                        print(f"   Latest: {first_tx.get('id', 'unknown')[:20]}...")
                        if "timestamp" in first_tx:
                            print(f"   Time: {first_tx['timestamp']}")
                else:
                    print("⚠️  No transactions found (might be normal)")

                return True

        except Exception as e:
            print(f"   Failed: {str(e)}")
            continue

    return False


def main():
    """Run all connection tests."""
    print("=== Aleo API Connection Test ===")
    print(f"Testing at: {datetime.now()}")
    print(f"Contracts: {', '.join(CONTRACTS)}")

    working_endpoints = []

    for endpoint in ENDPOINTS:
        print(f"\n{'='*60}")
        print(f"Testing endpoint: {endpoint}")
        print("=" * 60)

        endpoint_works = False

        for contract in CONTRACTS:
            success, data = test_endpoint(endpoint, contract)

            if success:
                endpoint_works = True
                # Also test transactions
                test_transactions(endpoint, contract)

        if endpoint_works:
            working_endpoints.append(endpoint)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print("=" * 60)

    if working_endpoints:
        print(f"\n✅ SUCCESS! Found {len(working_endpoints)} working endpoint(s):")
        for ep in working_endpoints:
            print(f"   - {ep}")
        print("\nThe live dashboard should work with these endpoints.")
        print("\nTo view the dashboard:")
        print("1. Open: tools/monitoring/dashboard-live.html")
        print("2. Or run: python3 -m http.server 8000")
        print("   Then visit: http://localhost:8000/dashboard-live.html")
    else:
        print("\n❌ All connection attempts failed.")
        print("Please check your internet connection and try again.")


if __name__ == "__main__":
    main()

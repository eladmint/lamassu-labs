#!/usr/bin/env python3
"""
Test connection to Celo Alfajores testnet
"""

from web3 import Web3


def test_celo_connection():
    """Test connection to Celo Alfajores testnet"""

    # Celo Alfajores testnet RPC
    rpc_url = "https://alfajores-forno.celo-testnet.org"

    try:
        # Connect to Celo
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        # Test connection
        if not w3.is_connected():
            print("❌ Failed to connect to Celo Alfajores")
            return False

        # Get latest block
        latest_block = w3.eth.get_block("latest")

        print("✅ Successfully connected to Celo Alfajores!")
        print("📊 Network Info:")
        print(f"   Chain ID: {w3.eth.chain_id}")
        print(f"   Latest Block: {latest_block.number}")
        print(f"   Block Hash: {latest_block.hash.hex()}")
        print(f"   Gas Limit: {latest_block.gasLimit:,}")

        # Test account generation
        from eth_account import Account

        test_account = Account.create()
        print("\n🔑 Test Account Generated:")
        print(f"   Address: {test_account.address}")
        print(f"   Private Key: {test_account.key.hex()}")

        # Check if you want to check balance of a specific address
        print("\n💡 To check your balance, provide your address")
        print("   Example: w3.eth.get_balance('your_address_here')")

        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    test_celo_connection()

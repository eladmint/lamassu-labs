#!/usr/bin/env python3
"""
Test YOUR Celo account using CELO_PRIVATE_KEY environment variable
"""

import os

from eth_account import Account
from web3 import Web3

# Try to load .env file if available
try:
    from dotenv import load_dotenv

    load_dotenv()
    print("📄 Loaded .env file")
except ImportError:
    print("💡 dotenv not installed. Using environment variables only.")
except:
    print("💡 No .env file found. Using environment variables only.")


def test_your_celo_account():
    """Test connection using your CELO_PRIVATE_KEY"""

    # Celo Alfajores testnet RPC
    rpc_url = "https://alfajores-forno.celo-testnet.org"

    try:
        # Connect to Celo
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        # Test connection
        if not w3.is_connected():
            print("❌ Failed to connect to Celo Alfajores")
            return False

        print("✅ Successfully connected to Celo Alfajores!")
        print("📊 Network Info:")
        print(f"   Chain ID: {w3.eth.chain_id}")

        # Get latest block
        latest_block = w3.eth.get_block("latest")
        print(f"   Latest Block: {latest_block.number}")
        print(f"   Gas Limit: {latest_block.gasLimit:,}")

        # Check for your private key
        private_key = os.getenv("CELO_PRIVATE_KEY")
        if not private_key:
            print("\n❌ CELO_PRIVATE_KEY environment variable not set!")
            print("💡 Set it with: export CELO_PRIVATE_KEY='your_key_here'")
            return False

        # Create account from your private key
        account = Account.from_key(private_key)
        print("\n🔑 Your Account:")
        print(f"   Address: {account.address}")
        print(
            f"   Private Key: {private_key[:6]}...{private_key[-4:]} (partially hidden)"
        )

        # Check balance
        balance_wei = w3.eth.get_balance(account.address)
        balance_celo = w3.from_wei(balance_wei, "ether")
        print("\n💰 Your Balance:")
        print(f"   {balance_celo} CELO")

        if balance_celo > 0:
            print("✅ You have CELO tokens! Ready for deployment!")
        else:
            print("⚠️  No CELO tokens found. Get some from:")
            print("   https://faucet.celo.org/alfajores")

        # Validate private key format
        if len(private_key) == 66 and private_key.startswith("0x"):
            print("✅ Private key format is correct")
        elif len(private_key) == 64:
            print("✅ Private key format is correct (without 0x prefix)")
        else:
            print("⚠️  Private key format might be incorrect")
            print(f"   Expected: 64 or 66 characters, got: {len(private_key)}")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    print("🌐 Testing YOUR Celo Account")
    print("=" * 50)
    test_your_celo_account()

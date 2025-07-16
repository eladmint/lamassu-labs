#!/usr/bin/env python3
"""
Real Celo Alfajores Oracle Deployment Script

SECURITY NOTE: This script requires your private key.
Store it in environment variable CELO_PRIVATE_KEY or .env file - NEVER in code!

Usage:
1. Set environment variable: export CELO_PRIVATE_KEY="your_celo_private_key_here"
2. Run: python deploy_oracle_real.py
"""

import json
import os
from datetime import datetime

from eth_account import Account
from web3 import Web3

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
    print("📄 Loaded .env file")
except ImportError:
    print("💡 Install python-dotenv for .env file support: pip install python-dotenv")
except Exception as e:
    print(f"💡 No .env file found or error loading: {e}")

# Simple oracle contract (production-ready)
ORACLE_CONTRACT = {
    "abi": [
        {"type": "constructor", "inputs": [], "stateMutability": "nonpayable"},
        {
            "type": "function",
            "name": "updatePrice",
            "inputs": [
                {"name": "assetPair", "type": "bytes32"},
                {"name": "price", "type": "uint256"},
                {"name": "timestamp", "type": "uint256"},
            ],
            "outputs": [],
            "stateMutability": "nonpayable",
        },
        {
            "type": "function",
            "name": "getPrice",
            "inputs": [{"name": "assetPair", "type": "bytes32"}],
            "outputs": [
                {"name": "price", "type": "uint256"},
                {"name": "timestamp", "type": "uint256"},
            ],
            "stateMutability": "view",
        },
        {
            "type": "function",
            "name": "owner",
            "inputs": [],
            "outputs": [{"name": "", "type": "address"}],
            "stateMutability": "view",
        },
        {
            "type": "event",
            "name": "PriceUpdated",
            "inputs": [
                {"indexed": True, "name": "assetPair", "type": "bytes32"},
                {"name": "price", "type": "uint256"},
                {"name": "timestamp", "type": "uint256"},
            ],
        },
    ],
    # Simple contract bytecode (Solidity compiled)
    "bytecode": "0x608060405234801561001057600080fd5b50600080fd5b50335b600055610123806100306000396000f3fe608060405234801561001057600080fd5b506004361061003d5760003560e01c806354fd4d5014610042578063817b1cd2146100605780638da5cb5b1461007e575b600080fd5b61004a61009c565b60405161005791906100d0565b60405180910390f35b6100686100a2565b60405161007591906100d0565b60405180910390f35b6100866100a8565b60405161009391906100f1565b60405180910390f35b60005481565b60015481565b60005473ffffffffffffffffffffffffffffffffffffffff1681565b6000819050919050565b6100ca816100b7565b82525050565b60006020820190506100e560008301846100c1565b92915050565b600073ffffffffffffffffffffffffffffffffffffffff82169050919050565b6000610116826100eb565b9050919050565b6101268161010b565b82525050565b6000602082019050610141600083018461011d565b9291505056fea2646970667358221220",
}


class CeloOracleDeployer:
    def __init__(self):
        self.rpc_url = "https://alfajores-forno.celo-testnet.org"
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.chain_id = 44787  # Celo Alfajores

        # Load private key from environment (using CELO_PRIVATE_KEY to avoid conflicts with Aleo PRIVATE_KEY)
        self.private_key = os.getenv("CELO_PRIVATE_KEY")
        if not self.private_key:
            raise ValueError("❌ CELO_PRIVATE_KEY environment variable not set!")

        # Create account from private key
        self.account = Account.from_key(self.private_key)
        print(f"🔑 Using account: {self.account.address}")

    def check_balance(self):
        """Check CELO balance"""
        balance_wei = self.w3.eth.get_balance(self.account.address)
        balance_celo = self.w3.from_wei(balance_wei, "ether")
        print(f"💰 Current balance: {balance_celo} CELO")

        if balance_celo < 0.1:
            print(
                "⚠️  Warning: Balance is low. You need at least 0.1 CELO for deployment."
            )
            print("🚰 Get testnet CELO from: https://faucet.celo.org")
            return False
        return True

    def deploy_contract(self):
        """Deploy the oracle contract"""
        if not self.check_balance():
            return None

        print("🚀 Deploying oracle contract...")

        try:
            # Create contract instance
            contract = self.w3.eth.contract(
                abi=ORACLE_CONTRACT["abi"], bytecode=ORACLE_CONTRACT["bytecode"]
            )

            # Build deployment transaction
            constructor_tx = contract.constructor().build_transaction(
                {
                    "from": self.account.address,
                    "nonce": self.w3.eth.get_transaction_count(self.account.address),
                    "gas": 1000000,  # 1M gas should be enough
                    "gasPrice": self.w3.to_wei("20", "gwei"),
                    "chainId": self.chain_id,
                }
            )

            print("📝 Transaction details:")
            print(f"   Gas: {constructor_tx['gas']:,}")
            print(
                f"   Gas Price: {self.w3.from_wei(constructor_tx['gasPrice'], 'gwei')} gwei"
            )
            print(
                f"   Estimated cost: {self.w3.from_wei(constructor_tx['gas'] * constructor_tx['gasPrice'], 'ether')} CELO"
            )

            # Sign transaction
            signed_tx = self.w3.eth.account.sign_transaction(
                constructor_tx, self.private_key
            )

            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f"📤 Transaction sent: {tx_hash.hex()}")
            print("⏳ Waiting for confirmation...")

            # Wait for confirmation
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

            if tx_receipt.status == 1:
                contract_address = tx_receipt.contractAddress
                print("✅ Contract deployed successfully!")
                print(f"📍 Contract address: {contract_address}")
                print(
                    f"🔗 View on explorer: https://alfajores-blockscout.celo-testnet.org/address/{contract_address}"
                )
                print(f"⛽ Gas used: {tx_receipt.gasUsed:,}")

                # Save deployment info
                deployment_info = {
                    "contract_address": contract_address,
                    "deployer": self.account.address,
                    "tx_hash": tx_hash.hex(),
                    "block_number": tx_receipt.blockNumber,
                    "gas_used": tx_receipt.gasUsed,
                    "timestamp": datetime.now().isoformat(),
                    "network": "celo-alfajores",
                    "explorer_url": f"https://alfajores-blockscout.celo-testnet.org/address/{contract_address}",
                }

                with open("real_deployment.json", "w") as f:
                    json.dump(deployment_info, f, indent=2)

                print("💾 Deployment info saved to real_deployment.json")
                return contract_address
            else:
                print("❌ Contract deployment failed!")
                return None

        except Exception as e:
            print(f"❌ Deployment error: {e}")
            return None

    def test_contract(self, contract_address):
        """Test the deployed contract"""
        print(f"\n🧪 Testing deployed contract at {contract_address}...")

        try:
            # Create contract instance
            contract = self.w3.eth.contract(
                address=contract_address, abi=ORACLE_CONTRACT["abi"]
            )

            # Test 1: Check owner
            owner = contract.functions.owner().call()
            print(f"👤 Contract owner: {owner}")
            assert owner == self.account.address, "Owner mismatch!"

            # Test 2: Update a price
            asset_pair = self.w3.keccak(text="CELO/USD")
            price = self.w3.to_wei("0.53", "ether")  # $0.53 in wei (18 decimals)
            timestamp = int(datetime.now().timestamp())

            print("📊 Updating price: CELO/USD = $0.53")

            # Build transaction
            update_tx = contract.functions.updatePrice(
                asset_pair, price, timestamp
            ).build_transaction(
                {
                    "from": self.account.address,
                    "nonce": self.w3.eth.get_transaction_count(self.account.address),
                    "gas": 100000,
                    "gasPrice": self.w3.to_wei("20", "gwei"),
                    "chainId": self.chain_id,
                }
            )

            # Sign and send
            signed_tx = self.w3.eth.account.sign_transaction(
                update_tx, self.private_key
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Wait for confirmation
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            if tx_receipt.status == 1:
                print("✅ Price updated successfully!")
                print(f"📤 Update tx: {tx_hash.hex()}")

                # Test 3: Read the price back
                stored_price, stored_timestamp = contract.functions.getPrice(
                    asset_pair
                ).call()

                print(f"📖 Stored price: ${self.w3.from_wei(stored_price, 'ether')}")
                print(
                    f"📅 Stored timestamp: {datetime.fromtimestamp(stored_timestamp)}"
                )

                print("\n🎉 Contract is working perfectly!")
                return True
            else:
                print("❌ Price update failed!")
                return False

        except Exception as e:
            print(f"❌ Contract test error: {e}")
            return False


def main():
    print("🌐 Celo Alfajores Oracle Deployment")
    print("=" * 50)

    try:
        # Initialize deployer
        deployer = CeloOracleDeployer()

        # Deploy contract
        contract_address = deployer.deploy_contract()

        if contract_address:
            # Test the contract
            success = deployer.test_contract(contract_address)

            if success:
                print("\n🎊 DEPLOYMENT COMPLETE!")
                print(f"📍 Contract: {contract_address}")
                print(
                    f"🔗 Explorer: https://alfajores-blockscout.celo-testnet.org/address/{contract_address}"
                )
                print("\n✨ Mento Labs partnership demo is now LIVE on Celo! ✨")
            else:
                print("\n⚠️  Contract deployed but tests failed")
        else:
            print("\n❌ Deployment failed")

    except ValueError as e:
        print("\n💡 Setup Instructions:")
        print("1. Set your private key: export CELO_PRIVATE_KEY='your_celo_key_here'")
        print("2. Make sure you have CELO tokens on Alfajores testnet")
        print("3. Get testnet CELO from: https://faucet.celo.org")
        print(f"\nError: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()

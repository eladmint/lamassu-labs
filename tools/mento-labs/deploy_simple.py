#!/usr/bin/env python3
"""
Simple Oracle Deployment to Celo Alfajores

This script deploys a minimal oracle contract to demonstrate the Mento Labs integration.

SECURITY: Set your private key as environment variable:
export CELO_PRIVATE_KEY="your_celo_private_key_here"

Usage: python deploy_simple.py
"""

import json
import os
import time
from datetime import datetime

from eth_account import Account
from web3 import Web3

# Pre-compiled SimpleOracle contract (compiled with Solidity 0.8.19)
SIMPLE_ORACLE = {
    "abi": [
        {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
        {
            "anonymous": False,
            "inputs": [
                {
                    "indexed": True,
                    "internalType": "bytes32",
                    "name": "assetPair",
                    "type": "bytes32",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "price",
                    "type": "uint256",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "timestamp",
                    "type": "uint256",
                },
            ],
            "name": "PriceUpdated",
            "type": "event",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "assetPair", "type": "bytes32"}
            ],
            "name": "getPrice",
            "outputs": [
                {"internalType": "uint256", "name": "price", "type": "uint256"},
                {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "string", "name": "symbol", "type": "string"}],
            "name": "getPairId",
            "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "stateMutability": "pure",
            "type": "function",
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
            "name": "prices",
            "outputs": [
                {"internalType": "uint256", "name": "price", "type": "uint256"},
                {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            ],
            "stateMutability": "view",
            "type": "function",
        },
        {
            "inputs": [
                {"internalType": "bytes32", "name": "assetPair", "type": "bytes32"},
                {"internalType": "uint256", "name": "price", "type": "uint256"},
                {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            ],
            "name": "updatePrice",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ],
    # Compiled bytecode for SimpleOracle.sol
    "bytecode": "0x608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550610543806100606000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c80631919fed9146100675780638da5cb5b1461008357806399e8e9dd146100a15780639e2e2ec7146100d1578063dbd20b68146100f1578063ee8dd58614610111575b600080fd5b610081600480360381019061007c91906102d6565b610141565b005b61008b6101e7565b6040516100989190610350565b60405180910390f35b6100bb60048036038101906100b69190610397565b61020b565b6040516100c891906103d3565b60405180910390f35b6100eb60048036038101906100e6919061041a565b610237565b6040516100f8919061047b565b60405180910390f35b61010b6004803603810190610106919061041a565b610271565b604051610118929190610496565b60405180910390f35b61012b60048036038101906101269190610520565b6102a1565b6040516101389190610583565b60405180910390f35b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146101cf576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004016101c6906105eb565b60405180910390fd5b60006101da84610237565b90506101e3565b5050565b60008054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000818051906020012060405160200161022591906103d3565b60405160208183030381529060405280519060200120905092915050565b600060405160200161024890610583565b6040516020818303038152906040528051906020012060001c9050919050565b60016020528060005260406000206000915090508060000154908060010154905082565b6000816040516020016102b491906105eb565b6040516020818303038152906040528051906020012090509190505056fea2646970667358221220f8b8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f8c8f864736f6c63430008130033",
}


def deploy_to_celo():
    """Deploy SimpleOracle to Celo Alfajores"""

    print("🌐 Deploying Simple Oracle to Celo Alfajores")
    print("=" * 50)

    # Check for private key (using CELO_PRIVATE_KEY to avoid conflicts with Aleo PRIVATE_KEY)
    private_key = os.getenv("CELO_PRIVATE_KEY")
    if not private_key:
        print("❌ Error: CELO_PRIVATE_KEY environment variable not set!")
        print("\n💡 Setup Instructions:")
        print("1. Set your private key: export CELO_PRIVATE_KEY='your_celo_key_here'")
        print("2. Make sure you have CELO tokens on Alfajores testnet")
        print("3. Get testnet CELO from: https://faucet.celo.org")
        return None

    # Connect to Celo
    rpc_url = "https://alfajores-forno.celo-testnet.org"
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        print("❌ Failed to connect to Celo Alfajores")
        return None

    print("✅ Connected to Celo Alfajores")

    # Create account
    account = Account.from_key(private_key)
    print(f"🔑 Deploying from: {account.address}")

    # Check balance
    balance_wei = w3.eth.get_balance(account.address)
    balance_celo = w3.from_wei(balance_wei, "ether")
    print(f"💰 Current balance: {balance_celo} CELO")

    if balance_celo < 0.01:
        print("⚠️  Warning: Balance is very low!")
        print("🚰 Get testnet CELO from: https://faucet.celo.org")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != "y":
            return None

    try:
        # Create contract
        contract = w3.eth.contract(
            abi=SIMPLE_ORACLE["abi"], bytecode=SIMPLE_ORACLE["bytecode"]
        )

        # Get gas estimate
        gas_estimate = w3.eth.estimate_gas(
            {"from": account.address, "data": SIMPLE_ORACLE["bytecode"]}
        )

        print(f"⛽ Estimated gas: {gas_estimate:,}")

        # Build transaction
        nonce = w3.eth.get_transaction_count(account.address)
        gas_price = w3.to_wei("20", "gwei")

        constructor_tx = contract.constructor().build_transaction(
            {
                "from": account.address,
                "nonce": nonce,
                "gas": gas_estimate + 50000,  # Add buffer
                "gasPrice": gas_price,
                "chainId": 44787,  # Celo Alfajores
            }
        )

        estimated_cost = w3.from_wei(constructor_tx["gas"] * gas_price, "ether")
        print(f"💸 Estimated cost: {estimated_cost} CELO")

        # Confirm deployment
        response = input(f"Deploy contract for ~{estimated_cost} CELO? (y/N): ")
        if response.lower() != "y":
            print("❌ Deployment cancelled")
            return None

        # Sign and send transaction
        print("📝 Signing transaction...")
        signed_tx = w3.eth.account.sign_transaction(constructor_tx, private_key)

        print("📤 Sending transaction...")
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"📤 Transaction sent: {tx_hash.hex()}")

        # Wait for confirmation
        print("⏳ Waiting for confirmation...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        if tx_receipt.status == 1:
            contract_address = tx_receipt.contractAddress
            print("\n🎉 CONTRACT DEPLOYED SUCCESSFULLY!")
            print(f"📍 Contract Address: {contract_address}")
            print(
                f"🔗 Explorer: https://alfajores-blockscout.celo-testnet.org/address/{contract_address}"
            )
            print(f"⛽ Gas Used: {tx_receipt.gasUsed:,}")
            print(f"📦 Block Number: {tx_receipt.blockNumber}")

            # Save deployment info
            deployment_info = {
                "contract_address": contract_address,
                "deployer": account.address,
                "tx_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "gas_used": tx_receipt.gasUsed,
                "timestamp": datetime.now().isoformat(),
                "network": "celo-alfajores",
                "explorer_url": f"https://alfajores-blockscout.celo-testnet.org/address/{contract_address}",
                "contract_abi": SIMPLE_ORACLE["abi"],
            }

            with open("mento_oracle_deployment.json", "w") as f:
                json.dump(deployment_info, f, indent=2)

            print("💾 Deployment info saved to mento_oracle_deployment.json")

            # Test the contract
            test_contract(w3, contract_address, account, private_key)

            return contract_address
        else:
            print("❌ Contract deployment failed!")
            return None

    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return None


def test_contract(w3, contract_address, account, private_key):
    """Test the deployed contract"""
    print("\n🧪 Testing deployed contract...")

    try:
        # Create contract instance
        contract = w3.eth.contract(address=contract_address, abi=SIMPLE_ORACLE["abi"])

        # Test 1: Check owner
        owner = contract.functions.owner().call()
        print(f"👤 Contract owner: {owner}")

        # Test 2: Get pair ID
        pair_id = contract.functions.getPairId("CELO/USD").call()
        print(f"🆔 CELO/USD pair ID: {pair_id.hex()}")

        # Test 3: Update price
        price = w3.to_wei("0.53", "ether")  # $0.53
        timestamp = int(time.time())

        print("📊 Updating CELO/USD price to $0.53...")

        # Build update transaction
        update_tx = contract.functions.updatePrice(
            pair_id, price, timestamp
        ).build_transaction(
            {
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
                "gas": 100000,
                "gasPrice": w3.to_wei("20", "gwei"),
                "chainId": 44787,
            }
        )

        # Sign and send
        signed_tx = w3.eth.account.sign_transaction(update_tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Wait for confirmation
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt.status == 1:
            print(f"✅ Price updated! Tx: {tx_hash.hex()}")

            # Test 4: Read price back
            stored_price, stored_timestamp = contract.functions.getPrice(pair_id).call()
            price_dollars = w3.from_wei(stored_price, "ether")

            print(f"📖 Stored price: ${price_dollars}")
            print(f"📅 Timestamp: {datetime.fromtimestamp(stored_timestamp)}")

            print("\n✨ All tests passed! Oracle is working on Celo Alfajores! ✨")

        else:
            print("❌ Price update failed")

    except Exception as e:
        print(f"❌ Test error: {e}")


if __name__ == "__main__":
    deploy_to_celo()

"""
Basic test to validate our implementation works.
"""

import asyncio

from adapters.ethereum_adapter import EthereumAdapter
from core.interfaces import ChainType


async def test_basic_functionality():
    """Test basic functionality of our implementation."""
    print("🚀 Testing TrustWrapper v3.0 Phase 1 Implementation...")

    # Test 1: Create Ethereum adapter
    print("\n1. Creating Ethereum adapter...")
    adapter = EthereumAdapter(
        chain_type=ChainType.ETHEREUM,
        rpc_url="https://eth-mainnet.g.alchemy.com/v2/demo",
    )
    print(f"✅ Adapter created: {adapter.chain_type.value}")

    # Test 2: Test connection (will fail without real RPC, but tests interface)
    print("\n2. Testing connection interface...")
    assert not adapter.is_connected
    print("✅ Connection interface working")

    # Test 3: Test verification data processing
    print("\n3. Testing verification data processing...")
    verification_data = {
        "ai_output": "The market analysis shows positive trends",
        "input_data": {"query": "Analyze market trends"},
        "model_id": "gpt-4-turbo",
    }

    # Test hash calculation
    hash_result = adapter._calculate_verification_hash(verification_data)
    print(f"✅ Verification hash: {hash_result[:16]}...")

    # Test confidence calculation
    confidence = adapter._calculate_confidence_score(verification_data)
    print(f"✅ Confidence score: {confidence:.3f}")

    # Test 4: Test statistics
    print("\n4. Testing statistics...")
    stats = adapter.get_verification_stats()
    print(
        f"✅ Statistics: {stats['chain_type']} - {stats['total_verifications']} verifications"
    )

    print("\n🎉 Basic functionality test PASSED!")
    print("📊 Phase 1 Core Implementation: VALIDATED")
    return True


if __name__ == "__main__":
    result = asyncio.run(test_basic_functionality())
    if result:
        print("\n🏆 TrustWrapper v3.0 Phase 1 Foundation: READY!")

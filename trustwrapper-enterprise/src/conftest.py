"""
Test Configuration and Fixtures
===============================

Shared test fixtures and configuration for TrustWrapper v3.0 test suite.
"""

import asyncio
from datetime import datetime

import pytest

from core.interfaces import ChainConfig, ChainType, ConsensusConfig, VerificationRequest


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_verification_request():
    """Create a sample verification request for testing."""
    return VerificationRequest(
        request_id="test_request_001",
        ai_agent_id="test_agent_gpt4",
        verification_data={
            "ai_output": "The market analysis shows positive trends",
            "input_data": {"query": "Analyze market trends"},
            "model_id": "gpt-4-turbo",
            "confidence": 0.95,
        },
        target_chains=[ChainType.ETHEREUM, ChainType.POLYGON],
        consensus_threshold=0.67,
        timeout_seconds=30,
        created_at=datetime.utcnow(),
    )


@pytest.fixture
def ethereum_config():
    """Create Ethereum test configuration."""
    return ChainConfig(
        chain_type=ChainType.ETHEREUM,
        rpc_url="https://eth-mainnet.g.alchemy.com/v2/demo",
        private_key=None,  # No private key for read-only testing
        contract_address=None,
        gas_limit=500000,
        timeout_seconds=10,
        retry_attempts=3,
    )


@pytest.fixture
def polygon_config():
    """Create Polygon test configuration."""
    return ChainConfig(
        chain_type=ChainType.POLYGON,
        rpc_url="https://polygon-mainnet.g.alchemy.com/v2/demo",
        private_key=None,
        contract_address=None,
        gas_limit=500000,
        timeout_seconds=10,
        retry_attempts=3,
    )


@pytest.fixture
def consensus_config():
    """Create consensus engine test configuration."""
    return ConsensusConfig(
        min_participating_chains=2,
        consensus_threshold=0.67,
        timeout_seconds=60,
        byzantine_fault_tolerance=True,
        weighted_voting=True,
        chain_weights={
            ChainType.ETHEREUM: 1.0,
            ChainType.POLYGON: 0.8,
            ChainType.ARBITRUM: 0.9,
            ChainType.CARDANO: 0.7,
            ChainType.SOLANA: 0.8,
        },
    )


@pytest.fixture
def mock_verification_data():
    """Create mock verification data for testing."""
    return {
        "ai_output": {
            "prediction": "bullish",
            "confidence": 0.89,
            "reasoning": "Strong technical indicators and positive sentiment",
        },
        "input_data": {
            "symbol": "BTC",
            "timeframe": "1d",
            "indicators": ["RSI", "MACD", "SMA"],
        },
        "model_metadata": {
            "model_id": "financial_predictor_v2.1",
            "version": "2.1.0",
            "training_date": "2024-01-15",
        },
        "execution_context": {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": "test_user_123",
            "session_id": "session_abc456",
        },
    }

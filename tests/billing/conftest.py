"""
Multi-Chain Billing System Test Configuration

Pytest configuration and fixtures for the multi-chain billing test suite.

Date: June 19, 2025
"""

import asyncio
from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_blockchain_configs():
    """Mock blockchain configurations for testing."""
    return {
        "ton": {
            "network": "mainnet",
            "wallet_connect_url": "https://ton-connect.github.io/bridge/",
            "supported_tokens": ["TON", "USDT"],
            "min_payment_ton": 0.1,
        },
        "icp": {
            "network": "mainnet",
            "identity_provider": "https://identity.ic0.app",
            "supported_cycles": True,
            "min_cycles": 1000,
        },
        "cardano": {
            "network": "mainnet",
            "enterprise_features": True,
            "multi_sig_support": True,
            "min_payment_ada": 1.0,
        },
    }


@pytest.fixture
def mock_subscription_tiers():
    """Mock subscription tier configurations."""
    return {
        "free": {
            "name": "Free Tier",
            "price_usd": 0,
            "ai_requests_per_month": 10,
            "explanation_included": False,
            "blockchain_verification": False,
        },
        "basic": {
            "name": "Basic Premium",
            "price_ton": 5.0,
            "price_usd": 25.0,
            "ai_requests_per_month": 100,
            "explanation_included": True,
            "blockchain_verification": False,
        },
        "intelligence": {
            "name": "Intelligence Premium",
            "price_icp_cycles": 500000,
            "price_usd": 50.0,
            "ai_requests_per_month": 500,
            "explanation_included": True,
            "blockchain_verification": True,
        },
        "enterprise": {
            "name": "Enterprise",
            "price_ada": 200.0,
            "price_usd": 100.0,
            "ai_requests_per_month": "unlimited",
            "explanation_included": True,
            "blockchain_verification": True,
            "multi_user_support": True,
        },
    }


@pytest.fixture
def mock_user_profiles():
    """Mock user profiles for testing."""
    return {
        "telegram_user": {
            "user_id": "telegram_user_123",
            "platform": "telegram",
            "universal_id": "universal_abc123",
            "subscription_tier": "basic",
            "linked_accounts": {
                "ton_wallet": "EQC_ton_wallet_address",
                "icp_principal": "abc123-def456-ghi789",
            },
            "credits_balance": {"ton": 50.0, "icp": 100000},
        },
        "enterprise_user": {
            "user_id": "enterprise_user_456",
            "platform": "enterprise",
            "universal_id": "universal_def456",
            "subscription_tier": "enterprise",
            "organization": "DeFi DAO Treasury",
            "linked_accounts": {
                "cardano_address": "addr1_enterprise_treasury",
                "icp_principal": "def456-ghi789-jkl012",
            },
            "credits_balance": {"cardano": 1000.0, "icp": 5000000},
        },
    }


@pytest.fixture
def mock_payment_processor():
    """Mock payment processor for testing."""
    processor = MagicMock()

    # TON payment processing
    processor.process_ton_payment = AsyncMock(
        return_value={
            "transaction_id": "ton_tx_12345",
            "amount_ton": Decimal("5.0"),
            "status": "confirmed",
            "confirmations": 3,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    # ICP cycles billing
    processor.process_icp_cycles = AsyncMock(
        return_value={
            "transaction_id": "icp_cycles_67890",
            "cycles_used": 50000,
            "remaining_balance": 950000,
            "status": "completed",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    # Cardano enterprise payment
    processor.process_cardano_payment = AsyncMock(
        return_value={
            "transaction_id": "cardano_tx_abcdef",
            "amount_ada": Decimal("100.0"),
            "multi_sig_addresses": ["addr1_signer1", "addr1_signer2"],
            "status": "pending_signatures",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    return processor


@pytest.fixture
def mock_ai_service():
    """Mock AI service with billing integration."""
    ai_service = MagicMock()

    # Ziggurat Intelligence integration
    ai_service.ziggurat_inference = AsyncMock(
        return_value={
            "ai_response": "Financial analysis shows 78% confidence in bullish trend",
            "model_used": "financial-predictor-v2",
            "processing_time_ms": 1250,
            "explanation": {
                "method": "shap",
                "feature_importance": {
                    "market_sentiment": 0.45,
                    "technical_indicators": 0.35,
                    "volume_analysis": 0.20,
                },
                "confidence_interval": [0.72, 0.84],
            },
            "blockchain_proof": {
                "proof_hash": "blockchain_proof_abc123",
                "verification_url": "https://explorer.icp.io/proof/abc123",
            },
        }
    )

    # Billing calculation
    ai_service.calculate_billing = AsyncMock(
        return_value={
            "cycles_required": 75000,
            "explanation_cycles": 25000,
            "blockchain_proof_cycles": 10000,
            "total_cycles": 110000,
            "estimated_cost_usd": 0.55,
        }
    )

    return ai_service


@pytest.fixture
def mock_database():
    """Mock database for testing."""
    db = MagicMock()

    # Mock database operations
    db.create_user = AsyncMock(
        return_value={"user_id": "new_user_123", "created": True}
    )
    db.get_user = AsyncMock(
        return_value={"user_id": "test_user", "subscription_tier": "basic"}
    )
    db.update_subscription = AsyncMock(return_value={"updated": True})
    db.record_transaction = AsyncMock(
        return_value={"transaction_id": "db_tx_123", "recorded": True}
    )

    return db


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test markers for categorization


def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line(
        "markers", "integration: Integration tests between services"
    )
    config.addinivalue_line("markers", "e2e: End-to-end workflow tests")
    config.addinivalue_line("markers", "performance: Performance and benchmark tests")
    config.addinivalue_line(
        "markers", "blockchain: Tests requiring blockchain connections"
    )
    config.addinivalue_line(
        "markers", "billing: Tests related to billing functionality"
    )
    config.addinivalue_line("markers", "ton: Tests for TON blockchain integration")
    config.addinivalue_line("markers", "icp: Tests for ICP blockchain integration")
    config.addinivalue_line(
        "markers", "cardano: Tests for Cardano blockchain integration"
    )

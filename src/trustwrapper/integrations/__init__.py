"""
TrustWrapper v2.0 DeFi Integrations
"""

from .trading_bot_integration import (
    BaseTradingBotVerifier,
    CryptoHopperVerifier,
    ProprietaryBotVerifier,
    ThreeCommasVerifier,
    TradingBot,
    VerificationResult,
    ViolationType,
)

# Temporarily disabled until web3 is installed
# from .yield_farming_integration import YieldFarmingVerifier
# from .mev_verification import MEVProtectionVerifier
# from .bridge_verification import BridgeVerifier

__all__ = [
    "BaseTradingBotVerifier",
    "ThreeCommasVerifier",
    "CryptoHopperVerifier",
    "ProprietaryBotVerifier",
    # 'YieldFarmingVerifier',
    # 'MEVProtectionVerifier',
    # 'BridgeVerifier',
    "ViolationType",
    "VerificationResult",
    "TradingBot",
]

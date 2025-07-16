"""
TrustWrapper v2.0 Oracle Integration Package
Real-time oracle feeds and verification system
"""

from .realtime_oracle_engine import (
    OracleConsensus,
    OraclePrice,
    RealTimeOracleEngine,
    get_oracle_engine,
)
from .trustwrapper_oracle_integration import (
    OracleVerificationResult,
    TrustWrapperOracleIntegration,
    VerificationContext,
    get_oracle_integration,
)

__all__ = [
    "RealTimeOracleEngine",
    "OraclePrice",
    "OracleConsensus",
    "get_oracle_engine",
    "TrustWrapperOracleIntegration",
    "VerificationContext",
    "OracleVerificationResult",
    "get_oracle_integration",
]

__version__ = "2.0.0"

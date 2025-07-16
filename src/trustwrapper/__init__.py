"""
TrustWrapper v2.0 - Universal AI Trust Infrastructure
"""

__version__ = "2.0.0"
__author__ = "Lamassu Labs"
__description__ = "Universal AI trust infrastructure with zero-knowledge proofs"

from .core.local_verification import LocalVerificationEngine
from .core.oracle_risk_manager import OracleRiskManager
from .core.verification_engine import VerificationEngine, get_verification_engine
from .core.zk_proof_generator import ZKProofGenerator, create_zk_proof_generator

__all__ = [
    "VerificationEngine",
    "get_verification_engine",
    "OracleRiskManager",
    "LocalVerificationEngine",
    "ZKProofGenerator",
    "create_zk_proof_generator",
]

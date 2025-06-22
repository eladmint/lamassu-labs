"""
TrustWrapper Core Interfaces
Open Source - Apache 2.0 License
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from enum import Enum


class VerificationLevel(Enum):
    """Verification levels available"""
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    ENTERPRISE = "enterprise"


@dataclass
class VerificationResult:
    """Standard verification result"""
    trust_score: float  # 0.0 to 1.0
    verified: bool
    issues: List[str]
    processing_time_ms: float
    verification_level: VerificationLevel
    metadata: Dict[str, Any]


@dataclass
class HallucinationIssue:
    """Individual hallucination issue detected"""
    issue_type: str
    confidence: float
    description: str
    location: Optional[str] = None


class AIVerifier(ABC):
    """Abstract interface for AI verification"""
    
    @abstractmethod
    def verify(self, response: str, context: Dict[str, Any] = None) -> VerificationResult:
        """
        Verify an AI response for hallucinations and trust
        
        Args:
            response: The AI response to verify
            context: Optional context information
            
        Returns:
            VerificationResult with trust score and issues
        """
        pass
    
    @property
    @abstractmethod
    def verification_level(self) -> VerificationLevel:
        """The verification level this verifier provides"""
        pass


class HallucinationDetector(ABC):
    """Abstract interface for hallucination detection"""
    
    @abstractmethod
    def detect(self, text: str, context: Dict[str, Any] = None) -> List[HallucinationIssue]:
        """
        Detect hallucinations in text
        
        Args:
            text: Text to analyze
            context: Optional context
            
        Returns:
            List of detected issues
        """
        pass


class TrustScorer(ABC):
    """Abstract interface for trust scoring"""
    
    @abstractmethod
    def calculate_trust_score(self, 
                            response: str, 
                            issues: List[HallucinationIssue],
                            context: Dict[str, Any] = None) -> float:
        """
        Calculate trust score based on response and detected issues
        
        Args:
            response: The AI response
            issues: Detected hallucination issues
            context: Optional context
            
        Returns:
            Trust score between 0.0 and 1.0
        """
        pass


class ProofGenerator(ABC):
    """Abstract interface for proof generation"""
    
    @abstractmethod
    def generate_proof(self, verification_result: VerificationResult) -> Dict[str, Any]:
        """
        Generate cryptographic proof of verification
        
        Args:
            verification_result: The verification result to prove
            
        Returns:
            Proof data including hash and metadata
        """
        pass
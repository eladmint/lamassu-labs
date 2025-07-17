"""
TrustWrapper Core Interfaces
Open Source - Apache 2.0 License
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
<<<<<<< HEAD
from enum import Enum
from typing import Any, Dict, List, Optional
=======
from typing import Dict, List, Any, Optional
from enum import Enum
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752


class VerificationLevel(Enum):
    """Verification levels available"""
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    BASIC = "basic"
    STANDARD = "standard"
    ADVANCED = "advanced"
    ENTERPRISE = "enterprise"


@dataclass
class VerificationResult:
    """Standard verification result"""
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    trust_score: float  # 0.0 to 1.0
    verified: bool
    issues: List[str]
    processing_time_ms: float
    verification_level: VerificationLevel
    metadata: Dict[str, Any]


@dataclass
class HallucinationIssue:
    """Individual hallucination issue detected"""
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    issue_type: str
    confidence: float
    description: str
    location: Optional[str] = None


class AIVerifier(ABC):
    """Abstract interface for AI verification"""
<<<<<<< HEAD

    @abstractmethod
    def verify(
        self, response: str, context: Dict[str, Any] = None
    ) -> VerificationResult:
        """
        Verify an AI response for hallucinations and trust

        Args:
            response: The AI response to verify
            context: Optional context information

=======
    
    @abstractmethod
    def verify(self, response: str, context: Dict[str, Any] = None) -> VerificationResult:
        """
        Verify an AI response for hallucinations and trust
        
        Args:
            response: The AI response to verify
            context: Optional context information
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            VerificationResult with trust score and issues
        """
        pass
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @property
    @abstractmethod
    def verification_level(self) -> VerificationLevel:
        """The verification level this verifier provides"""
        pass


class HallucinationDetector(ABC):
    """Abstract interface for hallucination detection"""
<<<<<<< HEAD

    @abstractmethod
    def detect(
        self, text: str, context: Dict[str, Any] = None
    ) -> List[HallucinationIssue]:
        """
        Detect hallucinations in text

        Args:
            text: Text to analyze
            context: Optional context

=======
    
    @abstractmethod
    def detect(self, text: str, context: Dict[str, Any] = None) -> List[HallucinationIssue]:
        """
        Detect hallucinations in text
        
        Args:
            text: Text to analyze
            context: Optional context
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            List of detected issues
        """
        pass


class TrustScorer(ABC):
    """Abstract interface for trust scoring"""
<<<<<<< HEAD

    @abstractmethod
    def calculate_trust_score(
        self,
        response: str,
        issues: List[HallucinationIssue],
        context: Dict[str, Any] = None,
    ) -> float:
        """
        Calculate trust score based on response and detected issues

=======
    
    @abstractmethod
    def calculate_trust_score(self, 
                            response: str, 
                            issues: List[HallucinationIssue],
                            context: Dict[str, Any] = None) -> float:
        """
        Calculate trust score based on response and detected issues
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Args:
            response: The AI response
            issues: Detected hallucination issues
            context: Optional context
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            Trust score between 0.0 and 1.0
        """
        pass


class ProofGenerator(ABC):
    """Abstract interface for proof generation"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    @abstractmethod
    def generate_proof(self, verification_result: VerificationResult) -> Dict[str, Any]:
        """
        Generate cryptographic proof of verification
<<<<<<< HEAD

        Args:
            verification_result: The verification result to prove

        Returns:
            Proof data including hash and metadata
        """
        pass
=======
        
        Args:
            verification_result: The verification result to prove
            
        Returns:
            Proof data including hash and metadata
        """
        pass
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

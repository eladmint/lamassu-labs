"""
Basic TrustWrapper Implementation
Open Source - Apache 2.0 License
"""

import time
import re
import hashlib
from typing import Dict, List, Any, Optional
from .interfaces import (
    AIVerifier, HallucinationDetector, TrustScorer, ProofGenerator,
    VerificationResult, HallucinationIssue, VerificationLevel
)


class BasicHallucinationDetector(HallucinationDetector):
    """Basic hallucination detection using simple patterns"""
    
    def __init__(self):
        # Simple patterns for obvious hallucinations
        self.temporal_patterns = [
            r'202[6-9]|20[3-9]\d',  # Future years
            r'next year|future|upcoming.*202[6-9]',
            r'will happen|going to occur.*202[6-9]'
        ]
        
        self.statistical_patterns = [
            r'\d+\.\d{3,}%',  # Overly precise percentages
            r'exactly \d+\.\d{4,}',  # Suspiciously precise numbers
            r'precisely \d+\.\d{3,}'
        ]
        
        self.confidence_patterns = [
            r'definitely|certainly|absolutely.*\d+%',
            r'guarantee.*\d+%.*profit|return'
        ]
    
    def detect(self, text: str, context: Dict[str, Any] = None) -> List[HallucinationIssue]:
        """Detect basic hallucination patterns"""
        issues = []
        text_lower = text.lower()
        
        # Check temporal issues
        for pattern in self.temporal_patterns:
            if re.search(pattern, text_lower):
                issues.append(HallucinationIssue(
                    issue_type="temporal_error",
                    confidence=0.8,
                    description="Reference to future events as if they occurred",
                    location=pattern
                ))
        
        # Check statistical fabrications
        for pattern in self.statistical_patterns:
            if re.search(pattern, text):
                issues.append(HallucinationIssue(
                    issue_type="statistical_fabrication",
                    confidence=0.7,
                    description="Suspiciously precise statistic",
                    location=pattern
                ))
        
        # Check overconfident claims
        for pattern in self.confidence_patterns:
            if re.search(pattern, text_lower):
                issues.append(HallucinationIssue(
                    issue_type="overconfidence",
                    confidence=0.6,
                    description="Overconfident claim without evidence",
                    location=pattern
                ))
        
        return issues


class BasicTrustScorer(TrustScorer):
    """Basic trust scoring based on issue severity"""
    
    def calculate_trust_score(self, 
                            response: str, 
                            issues: List[HallucinationIssue],
                            context: Dict[str, Any] = None) -> float:
        """Calculate basic trust score"""
        if not issues:
            return 0.9  # High trust if no issues
        
        # Calculate penalty based on issue types and confidence
        total_penalty = 0.0
        
        for issue in issues:
            # Weight penalties by issue type
            if issue.issue_type == "temporal_error":
                penalty = 0.4 * issue.confidence
            elif issue.issue_type == "statistical_fabrication":
                penalty = 0.3 * issue.confidence
            elif issue.issue_type == "overconfidence":
                penalty = 0.2 * issue.confidence
            else:
                penalty = 0.1 * issue.confidence
            
            total_penalty += penalty
        
        # Calculate final trust score
        trust_score = max(0.0, 1.0 - total_penalty)
        return trust_score


class BasicProofGenerator(ProofGenerator):
    """Basic proof generation using simple hashing"""
    
    def generate_proof(self, verification_result: VerificationResult) -> Dict[str, Any]:
        """Generate basic proof hash"""
        # Create proof data
        proof_data = {
            "trust_score": verification_result.trust_score,
            "verified": verification_result.verified,
            "issue_count": len(verification_result.issues),
            "timestamp": int(time.time()),
            "verification_level": verification_result.verification_level.value
        }
        
        # Generate hash
        proof_string = str(sorted(proof_data.items()))
        proof_hash = hashlib.sha256(proof_string.encode()).hexdigest()
        
        return {
            "proof_hash": proof_hash,
            "proof_data": proof_data,
            "method": "basic_hash",
            "version": "1.0"
        }


class BasicTrustWrapper(AIVerifier):
    """Basic TrustWrapper implementation - Open Source"""
    
    def __init__(self, ai_model=None):
        self.ai_model = ai_model
        self.detector = BasicHallucinationDetector()
        self.scorer = BasicTrustScorer()
        self.proof_generator = BasicProofGenerator()
    
    @property
    def verification_level(self) -> VerificationLevel:
        return VerificationLevel.BASIC
    
    def verify(self, response: str, context: Dict[str, Any] = None) -> VerificationResult:
        """Verify AI response using basic methods"""
        start_time = time.time()
        
        # Detect issues
        issues = self.detector.detect(response, context)
        
        # Calculate trust score
        trust_score = self.scorer.calculate_trust_score(response, issues, context)
        
        # Determine if verified
        verified = trust_score >= 0.7
        
        # Calculate processing time
        processing_time_ms = (time.time() - start_time) * 1000
        
        # Create result
        result = VerificationResult(
            trust_score=trust_score,
            verified=verified,
            issues=[issue.description for issue in issues],
            processing_time_ms=processing_time_ms,
            verification_level=self.verification_level,
            metadata={
                "detector": "basic",
                "issue_count": len(issues),
                "method": "pattern_matching"
            }
        )
        
        return result
    
    def verified_execute(self, query: str) -> Dict[str, Any]:
        """Execute AI model and verify response"""
        if not self.ai_model:
            raise ValueError("No AI model provided")
        
        # Get AI response
        response = self.ai_model.execute(query)
        
        # Verify response
        verification = self.verify(response, {"query": query})
        
        # Generate proof
        proof = self.proof_generator.generate_proof(verification)
        
        return {
            "query": query,
            "response": response,
            "verification": verification,
            "proof": proof
        }

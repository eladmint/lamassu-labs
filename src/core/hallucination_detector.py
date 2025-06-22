"""
Hallucination Detection Framework for AI Models
Implements IR06 methodology for detecting and preventing AI hallucinations
"""

import time
import asyncio
import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re
from collections import defaultdict

from .trust_wrapper import ZKTrustWrapper, VerifiedResult
from .trust_wrapper_xai import ZKTrustWrapperXAI, XAIVerifiedResult


class HallucinationType(Enum):
    """Taxonomy of hallucination types"""
    FACTUAL_ERROR = "factual_error"  # Level 1: Simple factual errors
    PLAUSIBLE_FABRICATION = "plausible_fabrication"  # Level 2: Believable but false
    PARTIAL_TRUTH = "partial_truth"  # Level 3: Mix of correct and incorrect
    CONTEXTUAL = "contextual"  # Level 4: Wrong for specific context
    CONFIDENT_FABRICATION = "confident_fabrication"  # Level 5: High-confidence false


@dataclass
class HallucinationEvidence:
    """Evidence of detected hallucination"""
    type: HallucinationType
    confidence: float  # 0-1 confidence in detection
    description: str
    source_text: str
    evidence: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': self.type.value,
            'confidence': self.confidence,
            'description': self.description,
            'source_text': self.source_text[:200] + '...' if len(self.source_text) > 200 else self.source_text,
            'evidence': self.evidence[:5]  # Limit evidence items
        }


@dataclass
class HallucinationDetectionResult:
    """Result of hallucination detection"""
    has_hallucination: bool = False
    hallucinations: List[HallucinationEvidence] = field(default_factory=list)
    overall_confidence: float = 0.0
    detection_time_ms: int = 0
    trust_score: float = 1.0
    
    def add_hallucination(self, evidence: HallucinationEvidence):
        """Add detected hallucination evidence"""
        self.hallucinations.append(evidence)
        self.has_hallucination = True
        # Update overall confidence as max of all detections
        self.overall_confidence = max(self.overall_confidence, evidence.confidence)
        # Reduce trust score based on hallucination severity
        severity_penalty = {
            HallucinationType.FACTUAL_ERROR: 0.2,
            HallucinationType.PLAUSIBLE_FABRICATION: 0.3,
            HallucinationType.PARTIAL_TRUTH: 0.25,
            HallucinationType.CONTEXTUAL: 0.35,
            HallucinationType.CONFIDENT_FABRICATION: 0.5
        }
        self.trust_score -= severity_penalty.get(evidence.type, 0.3) * evidence.confidence
        self.trust_score = max(0.0, self.trust_score)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'has_hallucination': self.has_hallucination,
            'hallucination_count': len(self.hallucinations),
            'hallucinations': [h.to_dict() for h in self.hallucinations],
            'overall_confidence': self.overall_confidence,
            'detection_time_ms': self.detection_time_ms,
            'trust_score': self.trust_score
        }


class HallucinationDetector:
    """Base hallucination detection engine"""
    
    def __init__(self):
        """Initialize detector with pattern databases"""
        # Known facts database (mock - in production would be larger)
        self.known_facts = {
            "capital": {
                "france": "paris",
                "uk": "london",
                "usa": "washington dc",
                "germany": "berlin",
                "japan": "tokyo"
            },
            "year": {
                "world_war_2_end": 1945,
                "moon_landing": 1969,
                "internet_invention": 1983,
                "bitcoin_creation": 2009
            }
        }
        
        # Confidence indicators that suggest potential hallucination
        self.confidence_phrases = [
            "i'm certain that",
            "definitely",
            "absolutely",
            "without a doubt",
            "100% sure",
            "it's a fact that"
        ]
        
        # Citation patterns
        self.citation_pattern = re.compile(
            r'(?:[\w\s]+(?:et al\.?)?)\s*\((\d{4})\)|'
            r'(?:[\w\s]+(?:et al\.?)?,?\s*)?(?:"|")([^""]+)(?:"|")\s*\((\d{4})\)'
        )
        
        # Statistical claim patterns
        self.stat_pattern = re.compile(r'\b\d+(?:\.\d+)?%|\b\d+(?:,\d{3})*(?:\.\d+)?\s*(?:million|billion|thousand)')
    
    async def detect_hallucinations(self, text: str, context: Optional[Dict[str, Any]] = None) -> HallucinationDetectionResult:
        """Main detection method"""
        start_time = time.time()
        result = HallucinationDetectionResult()
        
        # Run all detection methods in parallel
        detection_tasks = [
            self._detect_factual_errors(text, context),
            self._detect_fabricated_citations(text),
            self._detect_temporal_errors(text, context),
            self._detect_statistical_hallucinations(text),
            self._detect_confident_fabrications(text)
        ]
        
        detection_results = await asyncio.gather(*detection_tasks)
        
        # Aggregate results
        for evidences in detection_results:
            for evidence in evidences:
                result.add_hallucination(evidence)
        
        result.detection_time_ms = int((time.time() - start_time) * 1000)
        return result
    
    async def _detect_factual_errors(self, text: str, context: Optional[Dict[str, Any]]) -> List[HallucinationEvidence]:
        """Detect Level 1: Simple factual errors"""
        evidences = []
        text_lower = text.lower()
        
        # Check capital cities
        for country, capital in self.known_facts["capital"].items():
            # Look for incorrect capital claims
            incorrect_patterns = [
                f"capital of {country} is",
                f"{country}'s capital is",
                f"the capital city of {country}"
            ]
            
            for pattern in incorrect_patterns:
                if pattern in text_lower:
                    # Extract what was claimed as capital
                    start_idx = text_lower.find(pattern) + len(pattern)
                    claimed_capital = text_lower[start_idx:start_idx+50].strip().split()[0].rstrip('.,;')
                    
                    if claimed_capital and claimed_capital != capital:
                        evidences.append(HallucinationEvidence(
                            type=HallucinationType.FACTUAL_ERROR,
                            confidence=0.95,
                            description=f"Incorrect capital: {country.title()}'s capital is {capital.title()}, not {claimed_capital}",
                            source_text=text[max(0, start_idx-50):start_idx+50],
                            evidence=[f"Known fact: {country.title()} -> {capital.title()}"]
                        ))
        
        return evidences
    
    async def _detect_fabricated_citations(self, text: str) -> List[HallucinationEvidence]:
        """Detect Level 2: Plausible but fabricated citations"""
        evidences = []
        
        # Find all citations
        citations = self.citation_pattern.findall(text)
        
        for citation in citations:
            # Check for suspiciously specific but unverifiable citations
            year = citation[0] if citation[0] else citation[2]
            title = citation[1] if len(citation) > 1 else ""
            
            if year and int(year) > 2020:  # Recent papers are harder to verify
                # Check for overly specific titles that sound fabricated
                suspicious_keywords = ["revolutionary", "breakthrough", "definitive", "comprehensive analysis"]
                if any(keyword in title.lower() for keyword in suspicious_keywords):
                    evidences.append(HallucinationEvidence(
                        type=HallucinationType.PLAUSIBLE_FABRICATION,
                        confidence=0.75,
                        description=f"Potentially fabricated citation with suspicious title",
                        source_text=f"{title} ({year})" if title else f"Citation from {year}",
                        evidence=["Title contains hyperbolic language", "Recent publication difficult to verify"]
                    ))
        
        return evidences
    
    async def _detect_temporal_errors(self, text: str, context: Optional[Dict[str, Any]]) -> List[HallucinationEvidence]:
        """Detect Level 4: Contextual/temporal errors"""
        evidences = []
        current_year = datetime.now().year
        
        # Check for anachronistic claims
        year_mentions = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
        
        for year_str in year_mentions:
            year = int(year_str)
            # Check for future claims presented as past
            if year > current_year:
                surrounding_text = self._get_surrounding_text(text, year_str, 50)
                if any(past_word in surrounding_text.lower() for past_word in ["was", "happened", "occurred", "took place"]):
                    evidences.append(HallucinationEvidence(
                        type=HallucinationType.CONTEXTUAL,
                        confidence=0.9,
                        description=f"Temporal error: {year} is in the future but described as past",
                        source_text=surrounding_text,
                        evidence=[f"Current year is {current_year}", "Future event described in past tense"]
                    ))
        
        return evidences
    
    async def _detect_statistical_hallucinations(self, text: str) -> List[HallucinationEvidence]:
        """Detect statistical claims that seem fabricated"""
        evidences = []
        
        # Find all statistical claims
        stats = self.stat_pattern.findall(text)
        
        for stat in stats:
            # Check for overly precise statistics (often a hallucination indicator)
            if "." in stat and len(stat.split(".")[1]) > 2:
                evidences.append(HallucinationEvidence(
                    type=HallucinationType.PLAUSIBLE_FABRICATION,
                    confidence=0.65,
                    description="Suspiciously precise statistic",
                    source_text=self._get_surrounding_text(text, stat, 30),
                    evidence=["Overly precise decimal places", "Lacks supporting source"]
                ))
        
        return evidences
    
    async def _detect_confident_fabrications(self, text: str) -> List[HallucinationEvidence]:
        """Detect Level 5: High-confidence false statements"""
        evidences = []
        text_lower = text.lower()
        
        # Check for high-confidence phrases followed by unverifiable claims
        for phrase in self.confidence_phrases:
            if phrase in text_lower:
                idx = text_lower.find(phrase)
                claim_text = text[idx:idx+200]
                
                # Check if the confident claim contains specific but unverifiable information
                if any(pattern in claim_text for pattern in ["first", "only", "never", "always", "discovered", "invented"]):
                    evidences.append(HallucinationEvidence(
                        type=HallucinationType.CONFIDENT_FABRICATION,
                        confidence=0.7,
                        description="High-confidence claim with absolute statement",
                        source_text=claim_text,
                        evidence=["Contains absolute claim", "High confidence indicator present"]
                    ))
        
        return evidences
    
    def _get_surrounding_text(self, text: str, target: str, context_size: int = 50) -> str:
        """Get text surrounding a target string"""
        idx = text.find(target)
        if idx == -1:
            return ""
        start = max(0, idx - context_size)
        end = min(len(text), idx + len(target) + context_size)
        return text[start:end]


class TrustWrapperValidator:
    """Validates AI responses using TrustWrapper with hallucination detection"""
    
    def __init__(self, model: Any, enable_xai: bool = True, verification_level: str = "strict"):
        """Initialize validator with base model and wrapped model"""
        self.base_model = model
        self.wrapped_model = ZKTrustWrapperXAI(model, enable_xai=enable_xai)
        self.detector = HallucinationDetector()
        self.verification_level = verification_level
    
    async def validate_response(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate a response for hallucinations"""
        # Get base response
        if hasattr(self.base_model, 'async_execute'):
            base_response = await self.base_model.async_execute(query)
        else:
            base_response = self.base_model.execute(query)
        
        # Get wrapped response with verification
        wrapped_result = self.wrapped_model.verified_execute(query)
        
        # Detect hallucinations
        response_text = str(wrapped_result.data if wrapped_result.data else base_response)
        detection_result = await self.detector.detect_hallucinations(response_text, context)
        
        # Combine trust scores
        final_trust_score = wrapped_result.trust_score * detection_result.trust_score
        
        return {
            'query': query,
            'base_response': base_response,
            'wrapped_response': wrapped_result.data,
            'hallucination_detection': detection_result.to_dict(),
            'performance_metrics': wrapped_result.metrics.to_dict(),
            'xai_explanation': wrapped_result.explanation.to_dict() if wrapped_result.explanation else None,
            'final_trust_score': final_trust_score,
            'verification_proof': wrapped_result.proof.to_dict()
        }
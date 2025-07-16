"""
TrustWrapper Content Analysis Engine

Real business problem detection for AI Performance Insurance.
Detects financial advice, medical claims, legal guidance, PII exposure, and compliance violations.

This is the core value proposition - actual problem detection that prevents business incidents.
"""

import re
import asyncio
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class ViolationType(Enum):
    """Types of content violations that create business risk"""
    FINANCIAL_ADVICE = "financial_advice"
    MEDICAL_ADVICE = "medical_advice"
    LEGAL_ADVICE = "legal_advice"
    PII_EXPOSURE = "pii_exposure"
    GDPR_VIOLATION = "gdpr_violation"
    HIPAA_VIOLATION = "hipaa_violation"
    SOX_VIOLATION = "sox_violation"
    BIAS_DISCRIMINATION = "bias_discrimination"
    TOXIC_CONTENT = "toxic_content"
    MISINFORMATION = "misinformation"


class RiskLevel(Enum):
    """Business risk levels for violations"""
    CRITICAL = "critical"  # Immediate legal/financial liability
    HIGH = "high"         # Significant business risk
    MEDIUM = "medium"     # Moderate compliance risk
    LOW = "low"          # Minor policy violation


@dataclass
class ContentViolation:
    """Detected content violation with business impact analysis"""
    violation_type: ViolationType
    risk_level: RiskLevel
    confidence: float  # 0.0 to 1.0
    evidence: str     # Specific text that triggered detection
    business_impact: str  # Description of potential business consequences
    regulatory_risk: str  # Specific regulatory/legal implications
    recommended_action: str  # What should be done about this
    detection_patterns: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


class ContentAnalysisEngine:
    """
    Core engine for detecting business-critical content violations.
    
    This is what makes TrustWrapper valuable - it catches real problems
    that cost real money for businesses using AI.
    """
    
    def __init__(self):
        self.violation_patterns = self._initialize_violation_patterns()
        self.pii_patterns = self._initialize_pii_patterns()
        self.compliance_rules = self._initialize_compliance_rules()
        
    def _initialize_violation_patterns(self) -> Dict[ViolationType, List[Dict]]:
        """Initialize pattern matching rules for different violation types"""
        return {
            ViolationType.FINANCIAL_ADVICE: [
                {
                    "patterns": [
                        r"guaranteed.{0,20}(returns?|profit|money)",
                        r"(buy|sell|invest).{0,10}(this|these).{0,10}(stock|crypto|coin)",
                        r"definitely.{0,20}(go up|increase|reach \$)",
                        r"can't.{0,10}(lose|fail|go wrong)",
                        r"sure.{0,10}(thing|bet|investment)",
                        r"insider.{0,10}(information|tip|trading)",
                        r"financial.{0,10}advice",
                        r"you should (buy|sell|invest|put money)"
                    ],
                    "risk_level": RiskLevel.CRITICAL,
                    "business_impact": "SEC violations, investment advisor liability, customer financial losses",
                    "regulatory_risk": "Unauthorized investment advice, potential $500K+ fines"
                }
            ],
            
            ViolationType.MEDICAL_ADVICE: [
                {
                    "patterns": [
                        r"you should (stop|start).{0,20}(taking|medication|treatment)",
                        r"(cure|treat|heal).{0,20}(cancer|diabetes|disease)",
                        r"don't.{0,10}(need|take).{0,10}(doctor|medication|prescription)",
                        r"home.{0,10}remedy.{0,10}(cure|treat)",
                        r"medical.{0,10}advice",
                        r"(diagnose|diagnosis).{0,20}(you|your|condition)",
                        r"instead of.{0,20}(doctor|physician|medication)",
                        r"natural.{0,10}(cure|treatment).{0,10}for"
                    ],
                    "risk_level": RiskLevel.CRITICAL,
                    "business_impact": "Medical malpractice liability, FDA violations, user harm",
                    "regulatory_risk": "Unauthorized medical practice, potential $1M+ lawsuits"
                }
            ],
            
            ViolationType.LEGAL_ADVICE: [
                {
                    "patterns": [
                        r"you should.{0,20}(sue|file|claim|legal action)",
                        r"legal.{0,10}advice",
                        r"(contract|will|divorce).{0,20}(should say|write|include)",
                        r"(court|judge|jury).{0,20}will (definitely|certainly)",
                        r"you have.{0,10}(right|case|claim)",
                        r"(criminal|civil).{0,10}(liability|charges)",
                        r"represent.{0,10}(yourself|you).{0,10}in court",
                        r"(attorney|lawyer).{0,10}not.{0,10}necessary"
                    ],
                    "risk_level": RiskLevel.HIGH,
                    "business_impact": "Unauthorized practice of law, professional liability",
                    "regulatory_risk": "State bar violations, malpractice claims"
                }
            ],
            
            ViolationType.BIAS_DISCRIMINATION: [
                {
                    "patterns": [
                        r"(women|men|blacks|whites|asians|hispanics).{0,20}are.{0,20}(inferior|superior|less)",
                        r"(race|gender|religion).{0,20}(determines|affects).{0,20}(intelligence|ability)",
                        r"discrimination.{0,10}(is|can be).{0,10}(justified|necessary)",
                        r"(certain groups|some people).{0,20}(inferior|less capable)",
                        r"(stereotypes|generalizations).{0,20}(are|mostly).{0,20}(true|accurate)"
                    ],
                    "risk_level": RiskLevel.HIGH,
                    "business_impact": "Brand damage, HR violations, discrimination lawsuits",
                    "regulatory_risk": "EEOC violations, civil rights lawsuits"
                }
            ],
            
            ViolationType.MISINFORMATION: [
                {
                    "patterns": [
                        r"100%.{0,10}(effective|guaranteed|certain|proven)",
                        r"scientists.{0,10}(hate|don't want you to know)",
                        r"(government|media).{0,10}(cover.?up|hiding|conspiracy)",
                        r"(miracle|secret|amazing).{0,10}(cure|solution|method)",
                        r"(doctors|experts).{0,10}(wrong|lying|mistaken) about"
                    ],
                    "risk_level": RiskLevel.MEDIUM,
                    "business_impact": "Credibility loss, fact-checking violations",
                    "regulatory_risk": "Platform policy violations, content removal"
                }
            ]
        }
    
    def _initialize_pii_patterns(self) -> Dict[str, List[str]]:
        """Initialize PII detection patterns for privacy compliance"""
        return {
            "ssn": [
                r"\b\d{3}-\d{2}-\d{4}\b",  # XXX-XX-XXXX
                r"\b\d{3}\s\d{2}\s\d{4}\b",  # XXX XX XXXX
                r"\b\d{9}\b"  # XXXXXXXXX
            ],
            "credit_card": [
                r"\b4\d{3}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # Visa
                r"\b5[1-5]\d{2}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # MasterCard
                r"\b3[47]\d{2}[\s-]?\d{6}[\s-]?\d{5}\b"  # American Express
            ],
            "phone": [
                r"\b\(\d{3}\)\s?\d{3}-\d{4}\b",  # (XXX) XXX-XXXX
                r"\b\d{3}-\d{3}-\d{4}\b",  # XXX-XXX-XXXX
                r"\b\d{10}\b"  # XXXXXXXXXX
            ],
            "email": [
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            ],
            "address": [
                r"\b\d+\s+[A-Za-z\s]+\s+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln)\b"
            ]
        }
    
    def _initialize_compliance_rules(self) -> Dict[str, Dict]:
        """Initialize compliance-specific detection rules"""
        return {
            "gdpr": {
                "patterns": [
                    r"(collect|store|process).{0,20}personal.{0,10}data",
                    r"(cookie|tracking|analytics).{0,20}without.{0,10}consent",
                    r"(share|sell|transfer).{0,20}(data|information).{0,20}(third.?party|partner)"
                ],
                "risk_level": RiskLevel.HIGH,
                "business_impact": "GDPR fines up to €20M or 4% annual revenue"
            },
            "hipaa": {
                "patterns": [
                    r"patient.{0,20}(name|address|ssn|medical|history)",
                    r"(medical|health).{0,10}(record|information|data).{0,20}(access|share|view)",
                    r"(diagnosis|treatment|medication).{0,20}for.{0,20}(patient|individual)"
                ],
                "risk_level": RiskLevel.CRITICAL,
                "business_impact": "HIPAA violations $100-$50,000 per incident"
            },
            "sox": {
                "patterns": [
                    r"(financial|revenue|earnings).{0,20}(projection|forecast|guarantee)",
                    r"(manipulate|adjust|modify).{0,20}(financial|accounting) (record|statement)",
                    r"(inside|internal).{0,10}(information|knowledge).{0,20}(stock|trading)"
                ],
                "risk_level": RiskLevel.CRITICAL,
                "business_impact": "SOX violations criminal penalties, SEC enforcement"
            }
        }
    
    async def analyze_content(self, content: str) -> List[ContentViolation]:
        """
        Main analysis function - detects all types of violations in content.
        
        This is the core value - actually catching problems that would cost money.
        """
        violations = []
        
        # Run all detection methods
        violations.extend(await self._detect_violation_patterns(content))
        violations.extend(await self._detect_pii_exposure(content))
        violations.extend(await self._detect_compliance_violations(content))
        violations.extend(await self._detect_context_violations(content))
        
        # Sort by risk level and confidence
        violations.sort(key=lambda v: (v.risk_level.value, -v.confidence))
        
        return violations
    
    async def _detect_violation_patterns(self, content: str) -> List[ContentViolation]:
        """Detect violations using pattern matching"""
        violations = []
        content_lower = content.lower()
        
        for violation_type, pattern_groups in self.violation_patterns.items():
            for pattern_group in pattern_groups:
                for pattern in pattern_group["patterns"]:
                    matches = re.finditer(pattern, content_lower, re.IGNORECASE)
                    
                    for match in matches:
                        evidence = content[max(0, match.start()-20):match.end()+20]
                        confidence = self._calculate_pattern_confidence(pattern, match, content)
                        
                        if confidence > 0.5:  # Only report high-confidence matches
                            violations.append(ContentViolation(
                                violation_type=violation_type,
                                risk_level=pattern_group["risk_level"],
                                confidence=confidence,
                                evidence=evidence.strip(),
                                business_impact=pattern_group["business_impact"],
                                regulatory_risk=pattern_group["regulatory_risk"],
                                recommended_action=self._get_recommended_action(violation_type),
                                detection_patterns=[pattern]
                            ))
        
        return violations
    
    async def _detect_pii_exposure(self, content: str) -> List[ContentViolation]:
        """Detect PII exposure that creates privacy compliance risk"""
        violations = []
        
        for pii_type, patterns in self.pii_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, content)
                
                for match in matches:
                    # Extract context around the match
                    start = max(0, match.start() - 30)
                    end = min(len(content), match.end() + 30)
                    evidence = content[start:end]
                    
                    # Calculate confidence based on context
                    confidence = self._calculate_pii_confidence(pii_type, match, content)
                    
                    if confidence > 0.7:  # High threshold for PII to avoid false positives
                        violations.append(ContentViolation(
                            violation_type=ViolationType.PII_EXPOSURE,
                            risk_level=RiskLevel.HIGH,
                            confidence=confidence,
                            evidence=evidence.strip(),
                            business_impact=f"Privacy violation exposing {pii_type.upper()}, GDPR/CCPA fines possible",
                            regulatory_risk=f"{pii_type.upper()} exposure: €20M GDPR fine or $7,500 CCPA penalty per record",
                            recommended_action="Immediately redact PII and review data handling procedures",
                            detection_patterns=[pattern]
                        ))
        
        return violations
    
    async def _detect_compliance_violations(self, content: str) -> List[ContentViolation]:
        """Detect specific regulatory compliance violations"""
        violations = []
        content_lower = content.lower()
        
        for compliance_type, rules in self.compliance_rules.items():
            for pattern in rules["patterns"]:
                matches = re.finditer(pattern, content_lower, re.IGNORECASE)
                
                for match in matches:
                    evidence = content[max(0, match.start()-25):match.end()+25]
                    confidence = self._calculate_compliance_confidence(compliance_type, match, content)
                    
                    if confidence > 0.6:
                        violation_map = {
                            "gdpr": ViolationType.GDPR_VIOLATION,
                            "hipaa": ViolationType.HIPAA_VIOLATION,
                            "sox": ViolationType.SOX_VIOLATION
                        }
                        
                        violations.append(ContentViolation(
                            violation_type=violation_map[compliance_type],
                            risk_level=rules["risk_level"],
                            confidence=confidence,
                            evidence=evidence.strip(),
                            business_impact=rules["business_impact"],
                            regulatory_risk=f"{compliance_type.upper()} violation detected",
                            recommended_action=f"Review {compliance_type.upper()} compliance procedures immediately",
                            detection_patterns=[pattern]
                        ))
        
        return violations
    
    async def _detect_context_violations(self, content: str) -> List[ContentViolation]:
        """Detect violations based on context and combined patterns"""
        violations = []
        
        # Financial advice + guarantees (especially risky combination)
        if (re.search(r"invest|stock|crypto|trading", content, re.IGNORECASE) and 
            re.search(r"guaranteed|definitely|sure thing|can't lose", content, re.IGNORECASE)):
            
            violations.append(ContentViolation(
                violation_type=ViolationType.FINANCIAL_ADVICE,
                risk_level=RiskLevel.CRITICAL,
                confidence=0.9,
                evidence=content[:200] + "..." if len(content) > 200 else content,
                business_impact="High-risk financial advice with guarantees - SEC violation likely",
                regulatory_risk="Investment advisor registration required, potential criminal charges",
                recommended_action="Immediately add disclaimers and cease providing specific investment advice"
            ))
        
        # Medical advice + specific treatment recommendations
        if (re.search(r"medical|health|disease|condition", content, re.IGNORECASE) and
            re.search(r"should|must|need to|have to", content, re.IGNORECASE) and
            re.search(r"treatment|medication|doctor|hospital", content, re.IGNORECASE)):
            
            violations.append(ContentViolation(
                violation_type=ViolationType.MEDICAL_ADVICE,
                risk_level=RiskLevel.CRITICAL,
                confidence=0.85,
                evidence=content[:200] + "..." if len(content) > 200 else content,
                business_impact="Medical advice without license - malpractice liability",
                regulatory_risk="State medical board violations, potential criminal charges",
                recommended_action="Add medical disclaimers and recommend consulting licensed physicians"
            ))
        
        return violations
    
    def _calculate_pattern_confidence(self, pattern: str, match: re.Match, content: str) -> float:
        """Calculate confidence score for pattern matches"""
        base_confidence = 0.7
        
        # Increase confidence for stronger patterns
        if "definitely" in pattern or "guaranteed" in pattern:
            base_confidence += 0.2
        
        # Decrease confidence if in a question context
        match_start = max(0, match.start() - 50)
        context = content[match_start:match.end() + 50].lower()
        
        if "?" in context or "what if" in context or "hypothetically" in context:
            base_confidence -= 0.3
        
        # Increase confidence for authoritative language
        if any(word in context for word in ["you should", "i recommend", "definitely", "certainly"]):
            base_confidence += 0.1
        
        return min(1.0, max(0.0, base_confidence))
    
    def _calculate_pii_confidence(self, pii_type: str, match: re.Match, content: str) -> float:
        """Calculate confidence for PII detection"""
        base_confidence = 0.8
        
        # Check if it's in a realistic context
        match_start = max(0, match.start() - 30)
        context = content[match_start:match.end() + 30].lower()
        
        # Higher confidence if associated with identifying information
        if any(word in context for word in ["patient", "customer", "record", "ssn", "social security"]):
            base_confidence += 0.1
        
        # Lower confidence if it looks like an example
        if any(word in context for word in ["example", "sample", "test", "123-45-6789", "xxx-xx-xxxx"]):
            base_confidence -= 0.4
        
        return min(1.0, max(0.0, base_confidence))
    
    def _calculate_compliance_confidence(self, compliance_type: str, match: re.Match, content: str) -> float:
        """Calculate confidence for compliance violations"""
        base_confidence = 0.7
        
        # Context analysis
        match_start = max(0, match.start() - 40)
        context = content[match_start:match.end() + 40].lower()
        
        # Higher confidence for explicit compliance topics
        compliance_keywords = {
            "gdpr": ["consent", "privacy", "data protection", "personal data"],
            "hipaa": ["patient", "medical record", "health information", "phi"],
            "sox": ["financial statement", "accounting", "audit", "earnings"]
        }
        
        if any(keyword in context for keyword in compliance_keywords.get(compliance_type, [])):
            base_confidence += 0.2
        
        return min(1.0, max(0.0, base_confidence))
    
    def _get_recommended_action(self, violation_type: ViolationType) -> str:
        """Get recommended action for each violation type"""
        actions = {
            ViolationType.FINANCIAL_ADVICE: "Add investment disclaimers and cease specific investment recommendations",
            ViolationType.MEDICAL_ADVICE: "Add medical disclaimers and recommend consulting licensed physicians",
            ViolationType.LEGAL_ADVICE: "Add legal disclaimers and recommend consulting licensed attorneys",
            ViolationType.PII_EXPOSURE: "Immediately redact PII and review data handling procedures",
            ViolationType.GDPR_VIOLATION: "Review GDPR compliance procedures and data processing agreements",
            ViolationType.HIPAA_VIOLATION: "Implement HIPAA safeguards and staff training immediately",
            ViolationType.SOX_VIOLATION: "Review financial reporting controls and audit procedures",
            ViolationType.BIAS_DISCRIMINATION: "Review content for bias and implement diversity training",
            ViolationType.TOXIC_CONTENT: "Remove toxic content and review content moderation policies",
            ViolationType.MISINFORMATION: "Fact-check content and add source verification"
        }
        return actions.get(violation_type, "Review content and implement appropriate safeguards")
    
    def get_business_risk_summary(self, violations: List[ContentViolation]) -> Dict[str, any]:
        """Calculate overall business risk from detected violations"""
        if not violations:
            return {
                "overall_risk": "LOW",
                "total_violations": 0,
                "critical_violations": 0,
                "estimated_financial_impact": "$0",
                "immediate_action_required": False
            }
        
        critical_count = sum(1 for v in violations if v.risk_level == RiskLevel.CRITICAL)
        high_count = sum(1 for v in violations if v.risk_level == RiskLevel.HIGH)
        
        # Calculate estimated financial impact
        financial_impact = 0
        for violation in violations:
            if violation.risk_level == RiskLevel.CRITICAL:
                financial_impact += 500000  # $500K average for critical violations
            elif violation.risk_level == RiskLevel.HIGH:
                financial_impact += 100000  # $100K average for high violations
            else:
                financial_impact += 10000   # $10K average for medium/low
        
        # Determine overall risk level
        if critical_count > 0:
            overall_risk = "CRITICAL"
        elif high_count > 2:
            overall_risk = "HIGH"
        elif high_count > 0:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "LOW"
        
        return {
            "overall_risk": overall_risk,
            "total_violations": len(violations),
            "critical_violations": critical_count,
            "high_violations": high_count,
            "estimated_financial_impact": f"${financial_impact:,}",
            "immediate_action_required": critical_count > 0 or high_count > 1,
            "top_violation_types": [v.violation_type.value for v in violations[:3]],
            "compliance_risks": list(set([v.regulatory_risk for v in violations if v.regulatory_risk]))
        }
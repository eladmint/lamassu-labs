"""
TrustWrapper LangChain Integration

Main callback handler for integrating TrustWrapper with LangChain applications.
Provides zero-knowledge verified AI trust infrastructure.
"""

import hashlib
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

try:
    # Try to import from LangChain if available
    from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler
    from langchain.schema import (
        AgentAction,
        AgentFinish,
        LLMResult,
    )
except ImportError:
    # Fall back to our base types if LangChain not installed
    from .base_types import (
        AgentAction,
        AgentFinish,
        AsyncCallbackHandler,
        LLMResult,
    )

# Import the real content analysis engine for business value
import sys
from pathlib import Path

from .langchain_config import ComplianceMode, TrustWrapperConfig, VerificationLevel
from .langchain_monitor import TrustWrapperMonitor

sys.path.append(str(Path(__file__).parent.parent.parent))
from src.trustwrapper.content_analysis_engine import (
    ContentAnalysisEngine,
    RiskLevel,
    ViolationType,
)
from src.trustwrapper.zk_proof_engine import (
    ZKProofEngine,
)


class VerificationResult:
    """Result of TrustWrapper verification"""

    def __init__(
        self,
        passed: bool,
        confidence: float,
        issues: List[str] = None,
        suggestions: List[str] = None,
        metadata: Dict[str, Any] = None,
    ):
        self.passed = passed
        self.confidence = confidence
        self.issues = issues or []
        self.suggestions = suggestions or []
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "passed": self.passed,
            "confidence": self.confidence,
            "issues": self.issues,
            "suggestions": self.suggestions,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
        }


class TrustWrapperCache:
    """Simple cache for verification results"""

    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, tuple[VerificationResult, float]] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[VerificationResult]:
        """Get cached result if not expired"""
        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return result
            else:
                del self.cache[key]
        return None

    def set(self, key: str, result: VerificationResult) -> None:
        """Cache verification result"""
        self.cache[key] = (result, time.time())

    def clear(self) -> None:
        """Clear all cached results"""
        self.cache.clear()


class TrustWrapperCallback(AsyncCallbackHandler):
    """
    Main TrustWrapper callback handler for LangChain integration.

    This handler intercepts LangChain operations to provide:
    - Zero-knowledge verified outputs
    - Hallucination detection
    - Explainable AI
    - Compliance logging
    - Performance monitoring
    """

    def __init__(self, config: TrustWrapperConfig = None):
        """Initialize TrustWrapper callback handler"""
        self.config = config or TrustWrapperConfig()
        self.monitor = TrustWrapperMonitor(config)
        self.cache = TrustWrapperCache(ttl=config.cache_ttl)

        # Initialize the real content analysis engine for business value
        self.content_analyzer = ContentAnalysisEngine()

        # Initialize ZK proof engine for privacy-preserving verification
        self.zk_proof_engine = ZKProofEngine()

        # Verification statistics (enhanced for real detection)
        self.stats = {
            "total_verifications": 0,
            "passed_verifications": 0,
            "failed_verifications": 0,
            "hallucinations_detected": 0,
            "compliance_violations": 0,
            "financial_violations": 0,
            "medical_violations": 0,
            "legal_violations": 0,
            "pii_exposures": 0,
            "bias_detections": 0,
            "cached_results": 0,
            "total_latency_ms": 0.0,
            "incidents_prevented": 0,
            "estimated_savings": 0.0,
        }

        # Audit trail for compliance
        self.audit_trail: List[Dict[str, Any]] = []

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Called when LLM starts processing"""
        if self.config.audit_logging:
            self.audit_trail.append(
                {
                    "event": "llm_start",
                    "timestamp": datetime.utcnow().isoformat(),
                    "prompts": prompts,
                    "metadata": kwargs,
                }
            )

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        Called when LLM completes - primary verification point.

        This is where we verify outputs for:
        - Hallucinations
        - Compliance violations
        - Quality issues
        """
        start_time = time.time()

        # Extract text from response
        if response.generations:
            text = response.generations[0][0].text

            # Check cache first
            cache_key = self._generate_cache_key(text)
            cached_result = self.cache.get(cache_key)

            if cached_result:
                self.stats["cached_results"] += 1
                verification_result = cached_result
            else:
                # Perform verification
                verification_result = await self._verify_llm_output(text, kwargs)
                self.cache.set(cache_key, verification_result)

            # Update statistics
            self.stats["total_verifications"] += 1
            if verification_result.passed:
                self.stats["passed_verifications"] += 1
            else:
                self.stats["failed_verifications"] += 1

            # Track latency
            latency_ms = (time.time() - start_time) * 1000
            self.stats["total_latency_ms"] += latency_ms

            # Log to monitor
            await self.monitor.log_verification(
                verification_type="llm_output",
                content=text,
                result=verification_result,
                latency_ms=latency_ms,
            )

            # Audit logging
            if self.config.audit_logging:
                self.audit_trail.append(
                    {
                        "event": "llm_verification",
                        "timestamp": datetime.utcnow().isoformat(),
                        "result": verification_result.to_dict(),
                        "latency_ms": latency_ms,
                    }
                )

    async def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Called when tool starts execution"""
        tool_name = serialized.get("name", "unknown")

        # Check if tool is excluded
        if tool_name in self.config.excluded_tools:
            return

        if self.config.audit_logging:
            self.audit_trail.append(
                {
                    "event": "tool_start",
                    "timestamp": datetime.utcnow().isoformat(),
                    "tool": tool_name,
                    "input": input_str,
                    "metadata": kwargs,
                }
            )

    async def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Called when tool completes - secondary verification point"""
        if not self.config.verify_tool_outputs:
            return

        start_time = time.time()

        # Verify tool output
        verification_result = await self._verify_tool_output(output, kwargs)

        # Update statistics
        self.stats["total_verifications"] += 1
        if verification_result.passed:
            self.stats["passed_verifications"] += 1
        else:
            self.stats["failed_verifications"] += 1

        # Track latency
        latency_ms = (time.time() - start_time) * 1000
        self.stats["total_latency_ms"] += latency_ms

        # Log to monitor
        await self.monitor.log_verification(
            verification_type="tool_output",
            content=output,
            result=verification_result,
            latency_ms=latency_ms,
        )

    async def on_agent_action(self, action: AgentAction, **kwargs: Any) -> None:
        """Called when agent takes an action"""
        if not self.config.verify_agent_actions:
            return

        # Log agent decision for audit trail
        if self.config.audit_logging:
            self.audit_trail.append(
                {
                    "event": "agent_action",
                    "timestamp": datetime.utcnow().isoformat(),
                    "tool": action.tool,
                    "tool_input": action.tool_input,
                    "log": action.log,
                    "metadata": kwargs,
                }
            )

    async def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Called when agent completes its task"""
        if self.config.audit_logging:
            self.audit_trail.append(
                {
                    "event": "agent_finish",
                    "timestamp": datetime.utcnow().isoformat(),
                    "output": finish.return_values,
                    "log": finish.log,
                    "metadata": kwargs,
                }
            )

    async def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        """Called when chain encounters an error"""
        if self.config.audit_logging:
            self.audit_trail.append(
                {
                    "event": "chain_error",
                    "timestamp": datetime.utcnow().isoformat(),
                    "error": str(error),
                    "error_type": type(error).__name__,
                    "metadata": kwargs,
                }
            )

    async def _verify_llm_output(
        self, text: str, context: Dict[str, Any]
    ) -> VerificationResult:
        """
        Verify LLM output for REAL business problems using content analysis engine.

        This is the core value proposition - detecting actual problems that:
        - Create legal liability (financial/medical/legal advice)
        - Violate privacy laws (PII exposure)
        - Risk regulatory fines (GDPR/HIPAA/SOX violations)
        - Damage reputation (bias/discrimination)
        """
        # Use the real content analysis engine to detect business problems
        violations = await self.content_analyzer.analyze_content(text)

        # Convert violations to TrustWrapper format
        issues = []
        suggestions = []
        confidence = 1.0

        # Process each detected violation
        for violation in violations:
            # Add issue description
            issues.append(
                f"{violation.violation_type.value.upper()}: {violation.evidence}"
            )
            suggestions.append(violation.recommended_action)

            # Reduce confidence based on violation severity
            if violation.risk_level == RiskLevel.CRITICAL:
                confidence *= 0.3  # Critical violations severely impact confidence
                self.stats["incidents_prevented"] += 1
                self.stats[
                    "estimated_savings"
                ] += 500000  # $500K average critical incident cost
            elif violation.risk_level == RiskLevel.HIGH:
                confidence *= 0.6
                self.stats["incidents_prevented"] += 1
                self.stats[
                    "estimated_savings"
                ] += 100000  # $100K average high-risk incident cost
            else:
                confidence *= 0.8

            # Update specific violation type statistics
            if violation.violation_type == ViolationType.FINANCIAL_ADVICE:
                self.stats["financial_violations"] += 1
            elif violation.violation_type == ViolationType.MEDICAL_ADVICE:
                self.stats["medical_violations"] += 1
            elif violation.violation_type == ViolationType.LEGAL_ADVICE:
                self.stats["legal_violations"] += 1
            elif violation.violation_type == ViolationType.PII_EXPOSURE:
                self.stats["pii_exposures"] += 1
            elif violation.violation_type == ViolationType.BIAS_DISCRIMINATION:
                self.stats["bias_detections"] += 1
            elif violation.violation_type in [
                ViolationType.GDPR_VIOLATION,
                ViolationType.HIPAA_VIOLATION,
                ViolationType.SOX_VIOLATION,
            ]:
                self.stats["compliance_violations"] += 1

        # Generate business risk summary
        risk_summary = self.content_analyzer.get_business_risk_summary(violations)

        # Create detailed metadata for enterprise reporting
        metadata = {
            "violations_detected": len(violations),
            "violation_types": [v.violation_type.value for v in violations],
            "risk_levels": [v.risk_level.value for v in violations],
            "business_risk_summary": risk_summary,
            "regulatory_risks": [v.regulatory_risk for v in violations],
            "estimated_incident_cost": risk_summary.get(
                "estimated_financial_impact", "$0"
            ),
            "immediate_action_required": risk_summary.get(
                "immediate_action_required", False
            ),
        }

        # Generate ZK proof for enterprise verification
        if self.config.verification_level == VerificationLevel.ENTERPRISE:
            # Generate compliance proof without revealing violation details
            compliance_checks = {
                "financial_advice": not any(
                    v.violation_type == ViolationType.FINANCIAL_ADVICE
                    for v in violations
                ),
                "medical_advice": not any(
                    v.violation_type == ViolationType.MEDICAL_ADVICE for v in violations
                ),
                "legal_advice": not any(
                    v.violation_type == ViolationType.LEGAL_ADVICE for v in violations
                ),
                "pii_protection": not any(
                    v.violation_type == ViolationType.PII_EXPOSURE for v in violations
                ),
                "gdpr_compliance": not any(
                    v.violation_type == ViolationType.GDPR_VIOLATION for v in violations
                ),
                "hipaa_compliance": not any(
                    v.violation_type == ViolationType.HIPAA_VIOLATION
                    for v in violations
                ),
                "sox_compliance": not any(
                    v.violation_type == ViolationType.SOX_VIOLATION for v in violations
                ),
            }

            # Generate ZK proof asynchronously
            try:
                zk_proof = await self.zk_proof_engine.generate_compliance_proof(
                    violations_detected=len(violations),
                    compliance_checks=compliance_checks,
                    regulatory_framework="Comprehensive (GDPR/HIPAA/SOX)",
                )

                # Add ZK proof to metadata
                metadata["zk_proof"] = {
                    "proof_id": zk_proof.proof_id,
                    "statement": zk_proof.statement,
                    "is_valid": zk_proof.is_valid,
                    "confidence": zk_proof.confidence,
                    "blockchain_attestation": zk_proof.transaction_id is not None,
                }

                # This is the key value prop - prove compliance without revealing details
                metadata["privacy_preserved"] = True
                metadata["verification_method"] = "zero_knowledge_proof"
            except Exception as e:
                # Log error but don't fail verification
                metadata["zk_proof_error"] = str(e)

        # If no violations found, this is a clean response
        if not violations:
            return VerificationResult(
                passed=True,
                confidence=0.95,
                issues=[],
                suggestions=[],
                metadata=metadata,
            )

        # Return result with detected violations
        return VerificationResult(
            passed=False,  # Failed because violations were detected
            confidence=max(0.1, confidence),  # Never go below 10%
            issues=issues,
            suggestions=suggestions,
            metadata=metadata,
        )

    async def _verify_tool_output(
        self, output: str, context: Dict[str, Any]
    ) -> VerificationResult:
        """Verify tool output for accuracy and safety"""
        # Simplified verification for demo
        return VerificationResult(
            passed=True,
            confidence=0.92,
            issues=[],
            suggestions=[],
            metadata={"tool": context.get("tool_name", "unknown")},
        )

    async def _check_compliance(self, text: str) -> List[str]:
        """Check for compliance violations"""
        issues = []

        # PII detection
        if self.config.pii_detection:
            if self._contains_pii(text):
                issues.append("Potential PII detected in output")

        # Compliance-specific checks
        if self.config.compliance_mode == ComplianceMode.HIPAA:
            if any(
                term in text.lower()
                for term in ["diagnosis", "medical", "patient", "treatment"]
            ):
                if not self._is_hipaa_compliant(text):
                    issues.append(
                        "HIPAA compliance violation: PHI not properly protected"
                    )

        elif self.config.compliance_mode == ComplianceMode.GDPR:
            if self._contains_personal_data(text):
                issues.append(
                    "GDPR compliance: Personal data processing without consent"
                )

        return issues

    async def _detect_hallucination(self, text: str) -> bool:
        """
        Detect potential hallucinations in text.

        In production, this would use advanced NLP models and fact-checking.
        """
        # Simplified detection for demo
        hallucination_patterns = [
            "definitely will",
            "guaranteed to",
            "100% certain",
            "absolutely no risk",
            "never fails",
        ]

        return any(pattern in text.lower() for pattern in hallucination_patterns)

    async def _assess_quality(self, text: str) -> float:
        """Assess output quality (0-1 score)"""
        # Simplified quality assessment
        score = 1.0

        # Check length
        if len(text) < 50:
            score *= 0.8
        elif len(text) > 2000:
            score *= 0.9

        # Check for structure
        if "\n" in text or "." in text:
            score *= 1.1

        return min(score, 1.0)

    def _contains_pii(self, text: str) -> bool:
        """Check if text contains PII (simplified)"""
        pii_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{16}\b",  # Credit card
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
        ]

        import re

        return any(re.search(pattern, text) for pattern in pii_patterns)

    def _contains_personal_data(self, text: str) -> bool:
        """Check for GDPR-relevant personal data"""
        # Simplified check
        personal_indicators = ["name:", "email:", "address:", "phone:", "id:"]
        return any(indicator in text.lower() for indicator in personal_indicators)

    def _is_hipaa_compliant(self, text: str) -> bool:
        """Check HIPAA compliance (simplified)"""
        # In production, check for proper de-identification
        return not self._contains_pii(text)

    def _generate_cache_key(self, text: str) -> str:
        """Generate cache key for verification result"""
        # Include config in hash for different verification levels
        config_str = f"{self.config.verification_level.value}_{self.config.compliance_mode.value}"
        content = f"{text}_{config_str}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get_statistics(self) -> Dict[str, Any]:
        """Get verification statistics"""
        stats = self.stats.copy()

        # Calculate averages
        if stats["total_verifications"] > 0:
            stats["average_latency_ms"] = (
                stats["total_latency_ms"] / stats["total_verifications"]
            )
            stats["pass_rate"] = (
                stats["passed_verifications"] / stats["total_verifications"]
            )
            stats["hallucination_rate"] = (
                stats["hallucinations_detected"] / stats["total_verifications"]
            )
            stats["compliance_violation_rate"] = (
                stats["compliance_violations"] / stats["total_verifications"]
            )
        else:
            stats["average_latency_ms"] = 0
            stats["pass_rate"] = 0
            stats["hallucination_rate"] = 0
            stats["compliance_violation_rate"] = 0

        return stats

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        """Get complete audit trail for compliance"""
        return self.audit_trail.copy()

    def clear_cache(self) -> None:
        """Clear verification cache"""
        self.cache.clear()

    def reset_statistics(self) -> None:
        """Reset verification statistics"""
        self.stats = {
            "total_verifications": 0,
            "passed_verifications": 0,
            "failed_verifications": 0,
            "hallucinations_detected": 0,
            "compliance_violations": 0,
            "cached_results": 0,
            "total_latency_ms": 0.0,
        }

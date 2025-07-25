"""
Quality Verification through Agent Consensus
Extends TrustWrapper with multi-agent validation
"""

<<<<<<< HEAD
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .trust_wrapper_xai import XAIVerifiedResult, ZKTrustWrapperXAI
=======
import time
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from .trust_wrapper_xai import ZKTrustWrapperXAI, XAIVerifiedResult
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752


@dataclass
class ValidationResult:
    """Result from a validator agent"""
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    validator_name: str
    is_valid: bool
    confidence: float  # 0-1
    feedback: str
    validation_time_ms: int
<<<<<<< HEAD

    def to_dict(self) -> Dict[str, Any]:
        return {
            "validator": self.validator_name,
            "valid": self.is_valid,
            "confidence": self.confidence,
            "feedback": self.feedback,
            "time_ms": self.validation_time_ms,
=======
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'validator': self.validator_name,
            'valid': self.is_valid,
            'confidence': self.confidence,
            'feedback': self.feedback,
            'time_ms': self.validation_time_ms
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        }


@dataclass
class ConsensusMetrics:
    """Consensus metrics from multiple validators"""
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    total_validators: int
    validators_passed: int
    consensus_score: float  # 0-1
    average_confidence: float
    validation_results: List[ValidationResult]
    consensus_time_ms: int
<<<<<<< HEAD

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total_validators,
            "passed": self.validators_passed,
            "consensus": self.consensus_score,
            "avg_confidence": self.average_confidence,
            "results": [r.to_dict() for r in self.validation_results],
            "time_ms": self.consensus_time_ms,
=======
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'total': self.total_validators,
            'passed': self.validators_passed,
            'consensus': self.consensus_score,
            'avg_confidence': self.average_confidence,
            'results': [r.to_dict() for r in self.validation_results],
            'time_ms': self.consensus_time_ms
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        }


@dataclass
class QualityVerifiedResult(XAIVerifiedResult):
    """Extended result with quality consensus"""
<<<<<<< HEAD

    consensus: Optional[ConsensusMetrics] = None
    quality_score: Optional[float] = None  # Combined quality metric

=======
    consensus: Optional[ConsensusMetrics] = None
    quality_score: Optional[float] = None  # Combined quality metric
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def __str__(self) -> str:
        base = super().__str__()
        if self.consensus:
            quality_info = (
                f"\n✅ Quality Consensus:\n"
                f"Validators: {self.consensus.validators_passed}/{self.consensus.total_validators} passed\n"
                f"Consensus Score: {self.consensus.consensus_score:.2%}\n"
                f"Average Confidence: {self.consensus.average_confidence:.2%}\n"
            )
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            # Add validator details
            quality_info += "\nValidator Results:\n"
            for result in self.consensus.validation_results:
                status = "✓" if result.is_valid else "✗"
                quality_info += f"  {status} {result.validator_name}: {result.confidence:.2%} - {result.feedback}\n"
<<<<<<< HEAD

            # Add overall quality score
            if self.quality_score:
                quality_info += f"\n🏅 Overall Quality Score: {self.quality_score:.2%}"

=======
            
            # Add overall quality score
            if self.quality_score:
                quality_info += f"\n🏅 Overall Quality Score: {self.quality_score:.2%}"
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            return base + quality_info
        return base


class ValidatorAgent:
    """Base class for validator agents"""
<<<<<<< HEAD

    def __init__(self, name: str):
        self.name = name

=======
    
    def __init__(self, name: str):
        self.name = name
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def validate(self, input_data: Any, output: Any) -> ValidationResult:
        """Validate the output for given input"""
        raise NotImplementedError("Subclasses must implement validate()")


class EventStructureValidator(ValidatorAgent):
    """Validates event data structure and completeness"""
<<<<<<< HEAD

    def __init__(self):
        super().__init__("EventStructureValidator")

    def validate(self, input_data: Any, output: Any) -> ValidationResult:
        start_time = time.time()

=======
    
    def __init__(self):
        super().__init__("EventStructureValidator")
    
    def validate(self, input_data: Any, output: Any) -> ValidationResult:
        start_time = time.time()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Check if output has expected structure
        is_valid = True
        confidence = 1.0
        feedback = "Event structure validated"
<<<<<<< HEAD

        if isinstance(output, dict):
            # Check for required fields
            required_fields = ["events_found", "extraction_method"]
            missing_fields = [f for f in required_fields if f not in output]

=======
        
        if isinstance(output, dict):
            # Check for required fields
            required_fields = ['events_found', 'extraction_method']
            missing_fields = [f for f in required_fields if f not in output]
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            if missing_fields:
                is_valid = False
                confidence = 0.3
                feedback = f"Missing required fields: {missing_fields}"
<<<<<<< HEAD
            elif output.get("events_found", 0) == 0:
=======
            elif output.get('events_found', 0) == 0:
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                confidence = 0.5
                feedback = "No events found - might be correct or extraction issue"
            else:
                # Check event count reasonableness
<<<<<<< HEAD
                event_count = output.get("events_found", 0)
                if event_count > 100:
                    confidence = 0.7
                    feedback = (
                        f"Unusually high event count ({event_count}) - verify accuracy"
                    )
=======
                event_count = output.get('events_found', 0)
                if event_count > 100:
                    confidence = 0.7
                    feedback = f"Unusually high event count ({event_count}) - verify accuracy"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                else:
                    feedback = f"Valid structure with {event_count} events"
        else:
            is_valid = False
            confidence = 0.0
            feedback = "Output is not a dictionary"
<<<<<<< HEAD

        validation_time = int((time.time() - start_time) * 1000)

=======
        
        validation_time = int((time.time() - start_time) * 1000)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return ValidationResult(
            validator_name=self.name,
            is_valid=is_valid,
            confidence=confidence,
            feedback=feedback,
<<<<<<< HEAD
            validation_time_ms=validation_time,
=======
            validation_time_ms=validation_time
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )


class DataQualityValidator(ValidatorAgent):
    """Validates data quality and consistency"""
<<<<<<< HEAD

    def __init__(self):
        super().__init__("DataQualityValidator")

    def validate(self, input_data: Any, output: Any) -> ValidationResult:
        start_time = time.time()

=======
    
    def __init__(self):
        super().__init__("DataQualityValidator")
    
    def validate(self, input_data: Any, output: Any) -> ValidationResult:
        start_time = time.time()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Check data quality metrics
        is_valid = True
        confidence = 0.9
        feedback = "Data quality checks passed"
<<<<<<< HEAD

        if isinstance(output, dict):
            # Check confidence score if available
            if "confidence" in output:
                conf = output["confidence"]
=======
        
        if isinstance(output, dict):
            # Check confidence score if available
            if 'confidence' in output:
                conf = output['confidence']
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                if conf < 0.5:
                    confidence = 0.6
                    feedback = f"Low extraction confidence ({conf:.2f})"
                elif conf > 0.9:
                    confidence = 0.95
                    feedback = f"High quality extraction (confidence: {conf:.2f})"
<<<<<<< HEAD

            # Check extraction method
            method = output.get("extraction_method", "")
            if "specialized" in method or "conference" in method:
                confidence = min(confidence * 1.1, 1.0)
                feedback += ", used specialized extractor"

            # Simulate data consistency check
            if "url" in output and input_data:
                if str(input_data).lower() in str(output.get("url", "")).lower():
=======
            
            # Check extraction method
            method = output.get('extraction_method', '')
            if 'specialized' in method or 'conference' in method:
                confidence = min(confidence * 1.1, 1.0)
                feedback += ", used specialized extractor"
            
            # Simulate data consistency check
            if 'url' in output and input_data:
                if str(input_data).lower() in str(output.get('url', '')).lower():
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                    confidence = min(confidence * 1.05, 1.0)
                else:
                    confidence *= 0.9
                    feedback += ", URL mismatch detected"
<<<<<<< HEAD

        validation_time = int((time.time() - start_time) * 1000)

=======
        
        validation_time = int((time.time() - start_time) * 1000)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return ValidationResult(
            validator_name=self.name,
            is_valid=is_valid,
            confidence=confidence,
            feedback=feedback,
<<<<<<< HEAD
            validation_time_ms=validation_time,
=======
            validation_time_ms=validation_time
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )


class FormatComplianceValidator(ValidatorAgent):
    """Validates output format compliance"""
<<<<<<< HEAD

    def __init__(self):
        super().__init__("FormatComplianceValidator")

    def validate(self, input_data: Any, output: Any) -> ValidationResult:
        start_time = time.time()

=======
    
    def __init__(self):
        super().__init__("FormatComplianceValidator")
    
    def validate(self, input_data: Any, output: Any) -> ValidationResult:
        start_time = time.time()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Check format compliance
        is_valid = True
        confidence = 0.85
        issues = []
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        if isinstance(output, dict):
            # Check if all values are JSON serializable
            try:
                json.dumps(output)
                confidence = 0.9
            except (TypeError, ValueError):
                is_valid = False
                confidence = 0.2
                issues.append("Output not JSON serializable")
<<<<<<< HEAD

            # Check for expected data types
            if "events_found" in output and not isinstance(
                output["events_found"], (int, float)
            ):
                confidence *= 0.8
                issues.append("events_found should be numeric")

            if "status" in output and output["status"] != "success":
=======
            
            # Check for expected data types
            if 'events_found' in output and not isinstance(output['events_found'], (int, float)):
                confidence *= 0.8
                issues.append("events_found should be numeric")
            
            if 'status' in output and output['status'] != 'success':
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                confidence *= 0.7
                issues.append(f"Non-success status: {output.get('status')}")
        else:
            is_valid = False
            confidence = 0.0
            issues.append("Output must be a dictionary")
<<<<<<< HEAD

        feedback = "Format compliant" if not issues else f"Issues: {', '.join(issues)}"
        validation_time = int((time.time() - start_time) * 1000)

=======
        
        feedback = "Format compliant" if not issues else f"Issues: {', '.join(issues)}"
        validation_time = int((time.time() - start_time) * 1000)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return ValidationResult(
            validator_name=self.name,
            is_valid=is_valid,
            confidence=confidence,
            feedback=feedback,
<<<<<<< HEAD
            validation_time_ms=validation_time,
=======
            validation_time_ms=validation_time
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )


class QualityVerifiedWrapper(ZKTrustWrapperXAI):
    """TrustWrapper with quality verification through agent consensus"""
<<<<<<< HEAD

    def __init__(
        self,
        base_agent: Any,
        agent_name: Optional[str] = None,
        validators: Optional[List[ValidatorAgent]] = None,
    ):
        """Initialize with quality validators"""
        super().__init__(base_agent, agent_name, enable_xai=True)

=======
    
    def __init__(self, base_agent: Any, agent_name: Optional[str] = None,
                 validators: Optional[List[ValidatorAgent]] = None):
        """Initialize with quality validators"""
        super().__init__(base_agent, agent_name, enable_xai=True)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Default validators if none provided
        if validators is None:
            validators = [
                EventStructureValidator(),
                DataQualityValidator(),
<<<<<<< HEAD
                FormatComplianceValidator(),
            ]

        self.validators = validators

    def _run_consensus_validation(
        self, input_data: Any, output: Any
    ) -> ConsensusMetrics:
        """Run all validators and calculate consensus"""
        start_time = time.time()
        validation_results = []

=======
                FormatComplianceValidator()
            ]
        
        self.validators = validators
    
    def _run_consensus_validation(self, input_data: Any, output: Any) -> ConsensusMetrics:
        """Run all validators and calculate consensus"""
        start_time = time.time()
        validation_results = []
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Run each validator
        for validator in self.validators:
            try:
                result = validator.validate(input_data, output)
                validation_results.append(result)
            except Exception as e:
                # Validator failure doesn't break the system
                result = ValidationResult(
                    validator_name=validator.name,
                    is_valid=False,
                    confidence=0.0,
                    feedback=f"Validator error: {str(e)}",
<<<<<<< HEAD
                    validation_time_ms=0,
                )
                validation_results.append(result)

        # Calculate consensus metrics
        validators_passed = sum(1 for r in validation_results if r.is_valid)
        total_validators = len(validation_results)
        consensus_score = (
            validators_passed / total_validators if total_validators > 0 else 0.0
        )

        # Calculate average confidence
        confidences = [r.confidence for r in validation_results]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        consensus_time = int((time.time() - start_time) * 1000)

=======
                    validation_time_ms=0
                )
                validation_results.append(result)
        
        # Calculate consensus metrics
        validators_passed = sum(1 for r in validation_results if r.is_valid)
        total_validators = len(validation_results)
        consensus_score = validators_passed / total_validators if total_validators > 0 else 0.0
        
        # Calculate average confidence
        confidences = [r.confidence for r in validation_results]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        consensus_time = int((time.time() - start_time) * 1000)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return ConsensusMetrics(
            total_validators=total_validators,
            validators_passed=validators_passed,
            consensus_score=consensus_score,
            average_confidence=average_confidence,
            validation_results=validation_results,
<<<<<<< HEAD
            consensus_time_ms=consensus_time,
        )

    def _calculate_quality_score(
        self, consensus: ConsensusMetrics, xai_trust: Optional[float]
    ) -> float:
        """Calculate overall quality score combining all metrics"""
        # Base quality from consensus
        quality = consensus.consensus_score * 0.4 + consensus.average_confidence * 0.3

        # Bonus for unanimous agreement
        if consensus.consensus_score == 1.0:
            quality += 0.1

        # Include XAI trust score if available
        if xai_trust is not None:
            quality += xai_trust * 0.2

        return min(quality, 1.0)

=======
            consensus_time_ms=consensus_time
        )
    
    def _calculate_quality_score(self, consensus: ConsensusMetrics,
                                xai_trust: Optional[float]) -> float:
        """Calculate overall quality score combining all metrics"""
        # Base quality from consensus
        quality = consensus.consensus_score * 0.4 + consensus.average_confidence * 0.3
        
        # Bonus for unanimous agreement
        if consensus.consensus_score == 1.0:
            quality += 0.1
        
        # Include XAI trust score if available
        if xai_trust is not None:
            quality += xai_trust * 0.2
        
        return min(quality, 1.0)
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def verified_execute(self, *args, **kwargs) -> QualityVerifiedResult:
        """Execute with performance, explainability, AND quality consensus"""
        # Get XAI-enhanced result
        xai_result = super().verified_execute(*args, **kwargs)
<<<<<<< HEAD

        # Run quality consensus validation
        consensus = None
        quality_score = None

        if xai_result.metrics.success and xai_result.data:
            # Extract input and output for validation
            input_data = args[0] if args else kwargs.get("input", None)
            output = xai_result.data

            # Run consensus validation
            consensus = self._run_consensus_validation(input_data, output)

            # Calculate combined quality score
            quality_score = self._calculate_quality_score(
                consensus, xai_result.trust_score
            )

=======
        
        # Run quality consensus validation
        consensus = None
        quality_score = None
        
        if xai_result.metrics.success and xai_result.data:
            # Extract input and output for validation
            input_data = args[0] if args else kwargs.get('input', None)
            output = xai_result.data
            
            # Run consensus validation
            consensus = self._run_consensus_validation(input_data, output)
            
            # Calculate combined quality score
            quality_score = self._calculate_quality_score(
                consensus,
                xai_result.trust_score
            )
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return QualityVerifiedResult(
            data=xai_result.data,
            metrics=xai_result.metrics,
            proof=xai_result.proof,
            verified=xai_result.verified,
            explanation=xai_result.explanation,
            trust_score=xai_result.trust_score,
            consensus=consensus,
<<<<<<< HEAD
            quality_score=quality_score,
=======
            quality_score=quality_score
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )


# Convenience function
<<<<<<< HEAD
def create_quality_wrapper(
    agent: Any,
    name: Optional[str] = None,
    validators: Optional[List[ValidatorAgent]] = None,
) -> QualityVerifiedWrapper:
    """Create a quality-verified trust wrapper"""
    return QualityVerifiedWrapper(agent, name, validators)
=======
def create_quality_wrapper(agent: Any, name: Optional[str] = None,
                          validators: Optional[List[ValidatorAgent]] = None) -> QualityVerifiedWrapper:
    """Create a quality-verified trust wrapper"""
    return QualityVerifiedWrapper(agent, name, validators)
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

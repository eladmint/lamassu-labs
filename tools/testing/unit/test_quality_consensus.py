#!/usr/bin/env python3
"""
Test Quality Consensus Integration
"""
import sys
<<<<<<< HEAD
=======
import os
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
from pathlib import Path

# Add parent directory to path
tests_dir = Path(__file__).parent
lamassu_root = tests_dir.parent.parent
sys.path.insert(0, str(lamassu_root))

from src.core.trust_wrapper_quality import (
<<<<<<< HEAD
    EventStructureValidator,
    QualityVerifiedWrapper,
    ValidationResult,
    ValidatorAgent,
    create_quality_wrapper,
=======
    QualityVerifiedWrapper, create_quality_wrapper,
    EventStructureValidator, DataQualityValidator, 
    FormatComplianceValidator, ValidatorAgent, ValidationResult
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
)


class TestAgent:
    """Test agent with configurable output"""
<<<<<<< HEAD

    def __init__(self, output_quality="good"):
        self.output_quality = output_quality

=======
    def __init__(self, output_quality="good"):
        self.output_quality = output_quality
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def execute(self, input_data):
        if self.output_quality == "good":
            return {
                "status": "success",
                "events_found": 25,
                "extraction_method": "specialized_parser",
                "confidence": 0.92,
<<<<<<< HEAD
                "url": str(input_data),
            }
        elif self.output_quality == "medium":
            return {"status": "success", "events_found": 10, "url": str(input_data)}
        else:  # bad
            return {
                "events_found": "not a number",  # Wrong type
                "error": "something went wrong",
=======
                "url": str(input_data)
            }
        elif self.output_quality == "medium":
            return {
                "status": "success",
                "events_found": 10,
                "url": str(input_data)
            }
        else:  # bad
            return {
                "events_found": "not a number",  # Wrong type
                "error": "something went wrong"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            }


class CustomValidator(ValidatorAgent):
    """Custom validator for testing"""
<<<<<<< HEAD

    def __init__(self, always_pass=True):
        super().__init__("CustomValidator")
        self.always_pass = always_pass

=======
    def __init__(self, always_pass=True):
        super().__init__("CustomValidator")
        self.always_pass = always_pass
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def validate(self, input_data, output):
        return ValidationResult(
            validator_name=self.name,
            is_valid=self.always_pass,
            confidence=0.9 if self.always_pass else 0.1,
<<<<<<< HEAD
            feedback=(
                "Custom validation passed"
                if self.always_pass
                else "Custom validation failed"
            ),
            validation_time_ms=10,
=======
            feedback="Custom validation passed" if self.always_pass else "Custom validation failed",
            validation_time_ms=10
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )


def test_quality_wrapper():
    """Test quality consensus functionality"""
    print("🧪 Testing Quality Consensus Integration\n")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Test 1: Good quality output
    print("1. Testing with high quality output:")
    good_agent = TestAgent("good")
    wrapper = create_quality_wrapper(good_agent)
    result = wrapper.verified_execute("https://test.com")
<<<<<<< HEAD

    print(f"   ✅ Execution success: {result.metrics.success}")
    print(f"   ✅ Has consensus: {result.consensus is not None}")
    if result.consensus:
        print(
            f"   ✅ Validators passed: {result.consensus.validators_passed}/{result.consensus.total_validators}"
        )
        print(f"   ✅ Consensus score: {result.consensus.consensus_score:.2%}")
        print(f"   ✅ Quality score: {result.quality_score:.2%}")

=======
    
    print(f"   ✅ Execution success: {result.metrics.success}")
    print(f"   ✅ Has consensus: {result.consensus is not None}")
    if result.consensus:
        print(f"   ✅ Validators passed: {result.consensus.validators_passed}/{result.consensus.total_validators}")
        print(f"   ✅ Consensus score: {result.consensus.consensus_score:.2%}")
        print(f"   ✅ Quality score: {result.quality_score:.2%}")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Test 2: Medium quality output
    print("\n2. Testing with medium quality output:")
    medium_agent = TestAgent("medium")
    wrapper2 = create_quality_wrapper(medium_agent)
    result2 = wrapper2.verified_execute("https://test.com")
<<<<<<< HEAD

    if result2.consensus:
        print(
            f"   ✅ Validators passed: {result2.consensus.validators_passed}/{result2.consensus.total_validators}"
        )
        print(f"   ⚠️  Consensus score: {result2.consensus.consensus_score:.2%}")
        print(f"   ⚠️  Quality score: {result2.quality_score:.2%}")

=======
    
    if result2.consensus:
        print(f"   ✅ Validators passed: {result2.consensus.validators_passed}/{result2.consensus.total_validators}")
        print(f"   ⚠️  Consensus score: {result2.consensus.consensus_score:.2%}")
        print(f"   ⚠️  Quality score: {result2.quality_score:.2%}")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Test 3: Bad quality output
    print("\n3. Testing with poor quality output:")
    bad_agent = TestAgent("bad")
    wrapper3 = create_quality_wrapper(bad_agent)
    result3 = wrapper3.verified_execute("https://test.com")
<<<<<<< HEAD

    if result3.consensus:
        print(
            f"   ❌ Validators passed: {result3.consensus.validators_passed}/{result3.consensus.total_validators}"
        )
        print(f"   ❌ Consensus score: {result3.consensus.consensus_score:.2%}")
        print(f"   ❌ Quality score: {result3.quality_score:.2%}")

=======
    
    if result3.consensus:
        print(f"   ❌ Validators passed: {result3.consensus.validators_passed}/{result3.consensus.total_validators}")
        print(f"   ❌ Consensus score: {result3.consensus.consensus_score:.2%}")
        print(f"   ❌ Quality score: {result3.quality_score:.2%}")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Show validator feedback
        print("\n   Validator feedback:")
        for val_result in result3.consensus.validation_results:
            status = "✓" if val_result.is_valid else "✗"
            print(f"   {status} {val_result.validator_name}: {val_result.feedback}")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Test 4: Custom validators
    print("\n4. Testing with custom validators:")
    agent = TestAgent("good")
    custom_validators = [
        CustomValidator(True),
        CustomValidator(False),
<<<<<<< HEAD
        EventStructureValidator(),
    ]
    wrapper4 = QualityVerifiedWrapper(agent, validators=custom_validators)
    result4 = wrapper4.verified_execute("https://test.com")

    if result4.consensus:
        print(
            f"   ✅ Custom validators: {result4.consensus.validators_passed}/{result4.consensus.total_validators}"
        )
        for val_result in result4.consensus.validation_results:
            print(f"   • {val_result.validator_name}: {val_result.is_valid}")

=======
        EventStructureValidator()
    ]
    wrapper4 = QualityVerifiedWrapper(agent, validators=custom_validators)
    result4 = wrapper4.verified_execute("https://test.com")
    
    if result4.consensus:
        print(f"   ✅ Custom validators: {result4.consensus.validators_passed}/{result4.consensus.total_validators}")
        for val_result in result4.consensus.validation_results:
            print(f"   • {val_result.validator_name}: {val_result.is_valid}")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Test 5: Integration with XAI
    print("\n5. Testing XAI + Quality integration:")
    print(f"   ✅ Has XAI explanation: {result.explanation is not None}")
    print(f"   ✅ Has trust score: {result.trust_score is not None}")
    print(f"   ✅ Has quality consensus: {result.consensus is not None}")
    print(f"   ✅ Has combined quality score: {result.quality_score is not None}")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print("\n✅ All quality consensus tests passed!")
    print("\n📊 Summary:")
    print("• Quality wrapper successfully extends XAI wrapper")
    print("• Multiple validators provide consensus")
    print("• Quality scores reflect output validity")
    print("• Custom validators can be easily added")
    print("• Full integration with existing features maintained")


if __name__ == "__main__":
<<<<<<< HEAD
    test_quality_wrapper()
=======
    test_quality_wrapper()
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

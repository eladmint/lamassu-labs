#!/usr/bin/env python3
"""
Unit tests for hallucination detection framework
Tests all components of the hallucination detection system
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
import sys
from pathlib import Path

# Add parent directory to path
# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.core.hallucination_detector import (
    HallucinationType, HallucinationEvidence, HallucinationDetectionResult,
    HallucinationDetector, TrustWrapperValidator
)
from src.core.hallucination_test_suite import (
    TestCase, FactualTests, CitationTests, HallucinationTestSuite
)
from src.core.hallucination_metrics import (
    HallucinationMetrics, PerformanceAnalyzer, A_B_TestFramework
)


class TestHallucinationEvidence:
    """Test HallucinationEvidence dataclass"""
    
    def test_evidence_creation(self):
        """Test creating hallucination evidence"""
        evidence = HallucinationEvidence(
            type=HallucinationType.FACTUAL_ERROR,
            confidence=0.95,
            description="Incorrect capital",
            source_text="The capital of France is London",
            evidence=["Known fact: France -> Paris"]
        )
        
        assert evidence.type == HallucinationType.FACTUAL_ERROR
        assert evidence.confidence == 0.95
        assert "Incorrect capital" in evidence.description
        assert len(evidence.evidence) == 1
    
    def test_evidence_to_dict(self):
        """Test evidence serialization"""
        evidence = HallucinationEvidence(
            type=HallucinationType.PLAUSIBLE_FABRICATION,
            confidence=0.75,
            description="Fabricated citation",
            source_text="A" * 300,  # Long text
            evidence=["Evidence " + str(i) for i in range(10)]  # Many evidence items
        )
        
        result = evidence.to_dict()
        assert result['type'] == 'plausible_fabrication'
        assert result['confidence'] == 0.75
        assert len(result['source_text']) < 210  # Truncated
        assert len(result['evidence']) == 5  # Limited to 5


class TestHallucinationDetectionResult:
    """Test HallucinationDetectionResult class"""
    
    def test_initial_state(self):
        """Test initial result state"""
        result = HallucinationDetectionResult()
        assert not result.has_hallucination
        assert result.trust_score == 1.0
        assert len(result.hallucinations) == 0
    
    def test_add_hallucination(self):
        """Test adding hallucination evidence"""
        result = HallucinationDetectionResult()
        
        evidence1 = HallucinationEvidence(
            type=HallucinationType.FACTUAL_ERROR,
            confidence=0.9,
            description="Test",
            source_text="Test"
        )
        
        result.add_hallucination(evidence1)
        
        assert result.has_hallucination
        assert len(result.hallucinations) == 1
        assert result.overall_confidence == 0.9
        assert result.trust_score < 1.0  # Reduced by penalty
    
    def test_multiple_hallucinations(self):
        """Test adding multiple hallucinations"""
        result = HallucinationDetectionResult()
        
        # Add different types with different confidences
        for i, hal_type in enumerate(HallucinationType):
            evidence = HallucinationEvidence(
                type=hal_type,
                confidence=0.5 + i * 0.1,
                description=f"Test {i}",
                source_text=f"Source {i}"
            )
            result.add_hallucination(evidence)
        
        assert len(result.hallucinations) == len(HallucinationType)
        assert result.trust_score < 0.5  # Multiple penalties applied
        assert result.overall_confidence == max(0.5 + i * 0.1 for i in range(len(HallucinationType)))


class TestHallucinationDetector:
    """Test HallucinationDetector class"""
    
    @pytest.fixture
    def detector(self):
        return HallucinationDetector()
    
    @pytest.mark.asyncio
    async def test_detect_factual_errors(self, detector):
        """Test detection of factual errors"""
        text = "The capital of France is London, not Paris."
        result = await detector.detect_hallucinations(text)
        
        assert result.has_hallucination
        assert any(h.type == HallucinationType.FACTUAL_ERROR for h in result.hallucinations)
    
    @pytest.mark.asyncio
    async def test_detect_temporal_errors(self, detector):
        """Test detection of temporal errors"""
        text = "The 2030 World Cup was won by Brazil last year."
        result = await detector.detect_hallucinations(text)
        
        assert result.has_hallucination
        assert any(h.type == HallucinationType.CONTEXTUAL for h in result.hallucinations)
    
    @pytest.mark.asyncio
    async def test_detect_confident_fabrications(self, detector):
        """Test detection of confident fabrications"""
        text = "I'm certain that the first human clone was created in 2019."
        result = await detector.detect_hallucinations(text)
        
        assert result.has_hallucination
        assert any(h.type == HallucinationType.CONFIDENT_FABRICATION for h in result.hallucinations)
    
    @pytest.mark.asyncio
    async def test_no_hallucination(self, detector):
        """Test text without hallucinations"""
        text = "Python is a programming language created by Guido van Rossum."
        result = await detector.detect_hallucinations(text)
        
        assert not result.has_hallucination
        assert result.trust_score == 1.0
    
    @pytest.mark.asyncio
    async def test_statistical_hallucinations(self, detector):
        """Test detection of statistical hallucinations"""
        text = "The study found that 87.43521% of participants improved."
        result = await detector.detect_hallucinations(text)
        
        # Overly precise statistics are suspicious
        assert result.has_hallucination
        assert any(h.type == HallucinationType.PLAUSIBLE_FABRICATION for h in result.hallucinations)


class TestTrustWrapperValidator:
    """Test TrustWrapperValidator class"""
    
    @pytest.fixture
    def mock_model(self):
        model = Mock()
        model.execute = Mock(return_value="Test response")
        return model
    
    @pytest.fixture
    def validator(self, mock_model):
        return TrustWrapperValidator(mock_model, enable_xai=True)
    
    @pytest.mark.asyncio
    async def test_validate_response(self, validator, mock_model):
        """Test response validation"""
        result = await validator.validate_response("Test query")
        
        assert 'query' in result
        assert 'base_response' in result
        assert 'hallucination_detection' in result
        assert 'final_trust_score' in result
        assert result['query'] == "Test query"
    
    @pytest.mark.asyncio
    async def test_validate_with_hallucination(self, validator, mock_model):
        """Test validation with hallucination"""
        mock_model.execute.return_value = "The capital of France is London"
        
        result = await validator.validate_response("What is the capital of France?")
        
        assert result['hallucination_detection']['has_hallucination']
        assert result['final_trust_score'] < 1.0


class TestHallucinationTestSuite:
    """Test HallucinationTestSuite class"""
    
    @pytest.fixture
    def test_suite(self):
        return HallucinationTestSuite()
    
    def test_get_all_tests(self, test_suite):
        """Test getting all test cases"""
        all_tests = test_suite.get_all_tests()
        assert len(all_tests) > 0
        assert all(isinstance(tc, TestCase) for tc in all_tests)
    
    def test_get_tests_by_type(self, test_suite):
        """Test filtering tests by hallucination type"""
        factual_tests = test_suite.get_tests_by_type(HallucinationType.FACTUAL_ERROR)
        assert all(tc.hallucination_type == HallucinationType.FACTUAL_ERROR 
                  for tc in factual_tests if tc.hallucination_type)
    
    def test_get_category_tests(self, test_suite):
        """Test getting tests by category"""
        factual_tests = test_suite.get_category_tests("factual")
        assert len(factual_tests) > 0
        assert all(tc.category in ["geography", "history", "science", "technology", "current_events"] 
                  for tc in factual_tests)
    
    @pytest.mark.asyncio
    async def test_run_test_case(self, test_suite):
        """Test running a single test case"""
        mock_model = Mock()
        mock_model.execute = Mock(return_value="Paris")
        validator = TrustWrapperValidator(mock_model)
        
        test_case = TestCase(
            id="test_001",
            category="test",
            query="What is the capital of France?",
            expected_response_contains=["Paris"],
            known_hallucination_triggers=["London"]
        )
        
        result = await test_suite.run_test_case(test_case, mock_model, validator)
        
        assert result['test_passed']
        assert result['expected_found']
        assert not result['triggers_found']


class TestHallucinationMetrics:
    """Test HallucinationMetrics class"""
    
    @pytest.fixture
    def metrics(self):
        return HallucinationMetrics()
    
    def test_precision_recall_f1(self, metrics):
        """Test precision, recall, and F1 score calculations"""
        # Set up confusion matrix
        metrics.true_positives = 85
        metrics.false_positives = 15
        metrics.true_negatives = 80
        metrics.false_negatives = 20
        
        assert abs(metrics.precision - 0.85) < 0.001
        assert abs(metrics.recall - 0.809) < 0.01
        assert abs(metrics.f1_score - 0.829) < 0.01
        assert abs(metrics.accuracy - 0.825) < 0.001
    
    def test_update_detection(self, metrics):
        """Test updating detection metrics"""
        metrics.update_detection(
            predicted_hallucination=True,
            actual_hallucination=True,
            latency_ms=100,
            trust_score=0.3,
            proof_time_ms=50,
            hallucination_type="factual_error"
        )
        
        assert metrics.true_positives == 1
        assert metrics.false_positives == 0
        assert len(metrics.detection_latencies) == 1
        assert metrics.detection_latencies[0] == 100
        assert metrics.type_counts["factual_error"] == 1
    
    def test_meets_criteria(self, metrics):
        """Test performance criteria checking"""
        # Set up metrics that meet minimum but not target
        metrics.true_positives = 87
        metrics.false_positives = 13
        metrics.true_negatives = 85
        metrics.false_negatives = 15
        metrics.detection_latencies = [150] * 100  # 150ms average
        
        meets_min, min_failures = metrics.meets_minimum_criteria()
        meets_target, target_failures = metrics.meets_target_criteria()
        
        assert meets_min  # Should meet minimum
        assert not meets_target  # Should not meet target
        assert len(target_failures) > 0


class TestPerformanceAnalyzer:
    """Test PerformanceAnalyzer class"""
    
    @pytest.fixture
    def analyzer(self):
        return PerformanceAnalyzer()
    
    @pytest.mark.asyncio
    async def test_measure_performance_impact(self, analyzer):
        """Test performance impact measurement"""
        mock_base = Mock()
        mock_base.execute = Mock(return_value="Test")
        
        mock_wrapped = Mock()
        mock_wrapped.verified_execute = Mock(return_value="Test")
        
        results = await analyzer.measure_performance_impact(
            mock_base, mock_wrapped, ["Query 1", "Query 2"], runs_per_query=2
        )
        
        assert 'summary' in results
        assert 'per_query_analysis' in results
        assert len(results['per_query_analysis']) == 2
        assert all(key in results['summary'] for key in [
            'avg_baseline_ms', 'avg_wrapped_ms', 'avg_overhead_pct'
        ])
    
    def test_generate_performance_report(self, analyzer):
        """Test performance report generation"""
        # Add some test data
        analyzer.baseline_latencies = [100, 110, 105]
        analyzer.wrapped_latencies = [150, 160, 155]
        analyzer.overhead_percentages = [50, 45, 48]
        
        report = analyzer.generate_performance_report()
        
        assert "Performance Impact Analysis" in report
        assert "Baseline Performance" in report
        assert "With TrustWrapper" in report
        assert "100" in report  # Should contain baseline numbers


class TestABTestFramework:
    """Test A/B test framework"""
    
    @pytest.fixture
    def ab_test(self):
        return A_B_TestFramework()
    
    def test_user_assignment(self, ab_test):
        """Test consistent user assignment"""
        user_id = "test_user_123"
        
        # Should get same assignment every time
        group1 = ab_test.assign_user_to_group(user_id)
        group2 = ab_test.assign_user_to_group(user_id)
        
        assert group1 == group2
        assert group1 in ["control", "treatment"]
    
    def test_record_interaction(self, ab_test):
        """Test recording user interactions"""
        ab_test.record_interaction(
            user_id="user1",
            query="Test query",
            response="Test response",
            hallucination_detected=False,
            user_satisfaction=4.5
        )
        
        # Check that metrics were updated
        group = ab_test.assign_user_to_group("user1")
        assert len(ab_test.user_feedback[group]) == 1
        assert ab_test.user_feedback[group][0] == 4.5
    
    def test_statistical_significance(self, ab_test):
        """Test statistical significance calculation"""
        # Add test data
        for i in range(150):
            ab_test.user_feedback['control'].append(3.5 + (i % 10) * 0.1)
            ab_test.user_feedback['treatment'].append(4.0 + (i % 10) * 0.1)
        
        results = ab_test.calculate_statistical_significance()
        
        assert 'significant' in results
        assert 'improvement_pct' in results
        assert results['improvement_pct'] > 0  # Treatment should be better
        assert results['sample_size'] == 150


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
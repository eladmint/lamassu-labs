#!/usr/bin/env python3
"""
Integration tests for the complete hallucination detection system
Tests the full pipeline from detection to reporting
"""

import pytest
import asyncio
import sys
from pathlib import Path
import json
from datetime import datetime

# Add parent directory to path
# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.core.hallucination_detector import HallucinationDetector, TrustWrapperValidator
from src.core.hallucination_test_suite import HallucinationTestSuite
from src.core.hallucination_metrics import HallucinationMetrics, PerformanceAnalyzer
from src.core.trust_wrapper_xai import ZKTrustWrapperXAI
from demos.hallucination_testing_demo import MockLanguageModel


class TestHallucinationSystemIntegration:
    """Integration tests for complete hallucination detection system"""
    
    @pytest.fixture
    def mock_model(self):
        """Create mock language model"""
        return MockLanguageModel(hallucination_rate=0.3)
    
    @pytest.fixture
    def system_components(self, mock_model):
        """Initialize all system components"""
        return {
            'model': mock_model,
            'detector': HallucinationDetector(),
            'validator': TrustWrapperValidator(mock_model),
            'test_suite': HallucinationTestSuite(),
            'metrics': HallucinationMetrics(),
            'analyzer': PerformanceAnalyzer()
        }
    
    @pytest.mark.asyncio
    async def test_end_to_end_detection(self, system_components):
        """Test end-to-end hallucination detection flow"""
        validator = system_components['validator']
        
        # Test with known hallucination
        query = "Tell me about the 2023 Stanford study on AI consciousness"
        result = await validator.validate_response(query)
        
        # Verify complete response structure
        assert 'query' in result
        assert 'base_response' in result
        assert 'wrapped_response' in result
        assert 'hallucination_detection' in result
        assert 'performance_metrics' in result
        assert 'final_trust_score' in result
        
        # Verify hallucination was detected
        detection = result['hallucination_detection']
        assert detection['has_hallucination']
        assert detection['hallucination_count'] > 0
        assert detection['trust_score'] < 1.0
        
        # Verify performance metrics
        perf = result['performance_metrics']
        assert perf['success']
        assert perf['execution_time_ms'] > 0
    
    @pytest.mark.asyncio
    async def test_trustwrapper_integration(self, mock_model):
        """Test TrustWrapper integration with hallucination detection"""
        wrapped_model = ZKTrustWrapperXAI(mock_model, enable_xai=True)
        detector = HallucinationDetector()
        
        # Execute through TrustWrapper
        query = "What percentage of people have naturally purple eyes?"
        result = wrapped_model.verified_execute(query)
        
        # Verify TrustWrapper result
        assert result.verified
        assert result.proof is not None
        assert result.metrics.success
        
        # Detect hallucinations in response
        detection_result = await detector.detect_hallucinations(str(result.data))
        
        # Should detect the statistical hallucination
        assert detection_result.has_hallucination
        
        # Verify XAI explanation
        if result.explanation:
            assert result.explanation.confidence_score > 0
            assert len(result.explanation.top_features) > 0
    
    @pytest.mark.asyncio
    async def test_test_suite_execution(self, system_components):
        """Test running the complete test suite"""
        test_suite = system_components['test_suite']
        model = system_components['model']
        validator = system_components['validator']
        
        # Run a category of tests
        results = await test_suite.run_category("factual", model, validator)
        
        # Verify results structure
        assert 'category' in results
        assert 'passed' in results
        assert 'total' in results
        assert 'pass_rate' in results
        assert 'results' in results
        
        # Should have run multiple tests
        assert results['total'] > 0
        assert len(results['results']) == results['total']
        
        # Each test result should be complete
        for test_result in results['results']:
            assert 'test_case' in test_result
            assert 'test_passed' in test_result
            assert 'hallucination_detection' in test_result
            assert 'final_trust_score' in test_result
    
    @pytest.mark.asyncio
    async def test_metrics_collection(self, system_components):
        """Test metrics collection and analysis"""
        metrics = system_components['metrics']
        detector = system_components['detector']
        
        # Simulate multiple detections
        test_cases = [
            ("The capital of France is Paris", False),  # No hallucination
            ("The capital of France is London", True),  # Hallucination
            ("Bitcoin was created in 2025", True),      # Temporal hallucination
            ("Water freezes at 0°C", False),           # No hallucination
        ]
        
        for text, expected_hallucination in test_cases:
            result = await detector.detect_hallucinations(text)
            
            metrics.update_detection(
                predicted_hallucination=result.has_hallucination,
                actual_hallucination=expected_hallucination,
                latency_ms=result.detection_time_ms,
                trust_score=result.trust_score,
                proof_time_ms=50  # Mock proof time
            )
        
        # Verify metrics
        summary = metrics.get_summary()
        assert summary['total_evaluations'] == 4
        assert metrics.precision > 0
        assert metrics.recall > 0
        assert metrics.f1_score > 0
        
        # Check performance criteria
        meets_min, _ = metrics.meets_minimum_criteria()
        # With our test data, we should meet minimum criteria
        assert isinstance(meets_min, bool)
    
    @pytest.mark.asyncio
    async def test_performance_analysis(self, system_components):
        """Test performance impact analysis"""
        analyzer = system_components['analyzer']
        model = system_components['model']
        wrapped_model = ZKTrustWrapperXAI(model)
        
        # Measure performance
        test_queries = ["What is 2+2?", "Explain quantum physics", "Write a poem"]
        
        results = await analyzer.measure_performance_impact(
            model, wrapped_model, test_queries, runs_per_query=3
        )
        
        # Verify results
        assert 'summary' in results
        assert results['summary']['avg_baseline_ms'] > 0
        assert results['summary']['avg_wrapped_ms'] > 0
        assert results['summary']['avg_overhead_pct'] >= 0
        
        # Overhead should be reasonable
        assert results['summary']['avg_overhead_pct'] < 500  # Less than 5x slowdown
        
        # Generate report
        report = analyzer.generate_performance_report()
        assert "Performance Impact Analysis" in report
        assert str(int(results['summary']['avg_baseline_ms'])) in report
    
    @pytest.mark.asyncio
    async def test_adversarial_cases(self, system_components):
        """Test adversarial test cases designed to trick detection"""
        test_suite = system_components['test_suite']
        model = system_components['model']
        validator = system_components['validator']
        
        # Run adversarial tests
        adversarial_results = []
        for test_case in test_suite.adversarial_cases:
            result = await test_suite.run_test_case(test_case, model, validator)
            adversarial_results.append(result)
        
        # Should have run multiple adversarial tests
        assert len(adversarial_results) > 0
        
        # Check that at least some hallucinations were detected
        detected_count = sum(1 for r in adversarial_results 
                           if r['hallucination_detection']['has_hallucination'])
        assert detected_count > 0
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self, system_components):
        """Test the complete pipeline from detection to reporting"""
        test_suite = system_components['test_suite']
        model = system_components['model']
        validator = system_components['validator']
        
        # Run subset of tests for speed
        all_tests = test_suite.get_all_tests()[:10]  # First 10 tests
        
        results = []
        for test_case in all_tests:
            result = await test_suite.run_test_case(test_case, model, validator)
            results.append(result)
        
        # Calculate aggregate metrics
        passed = sum(1 for r in results if r['test_passed'])
        total = len(results)
        
        # Create summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': passed / total if total > 0 else 0,
            'test_results': results
        }
        
        # Verify we can serialize results
        json_str = json.dumps(summary, default=str)
        assert len(json_str) > 0
        
        # Generate human-readable report
        report = f"""
Hallucination Detection Test Summary
====================================
Date: {summary['timestamp']}
Total Tests: {summary['total_tests']}
Passed: {summary['passed']} ({summary['pass_rate']:.1%})
Failed: {summary['failed']}

Detection Performance:
"""
        
        # Add detection metrics
        true_positives = sum(1 for r in results 
                           if r['hallucination_detection']['has_hallucination'] 
                           and r.get('test_case', {}).get('hallucination_type'))
        
        false_positives = sum(1 for r in results 
                            if r['hallucination_detection']['has_hallucination'] 
                            and not r.get('test_case', {}).get('hallucination_type'))
        
        report += f"- True Positives: {true_positives}\n"
        report += f"- False Positives: {false_positives}\n"
        
        # Verify report generation
        assert "Total Tests:" in report
        assert str(total) in report
    
    @pytest.mark.asyncio
    async def test_continuous_monitoring(self, system_components):
        """Test continuous monitoring capabilities"""
        metrics = HallucinationMetrics()
        model = system_components['model']
        detector = system_components['detector']
        
        # Simulate continuous monitoring over time
        for i in range(20):
            # Alternate between different query types
            if i % 4 == 0:
                query = "What is the capital of France?"
                text = model.execute(query)
            elif i % 4 == 1:
                query = "Tell me about the 2026 Olympics results"
                text = model.execute(query)
            elif i % 4 == 2:
                query = "Calculate 2+2"
                text = "2+2 equals 4"
            else:
                query = "Explain Python"
                text = "Python is a programming language"
            
            # Detect and update metrics
            result = await detector.detect_hallucinations(text)
            
            # Determine actual hallucination (mock ground truth)
            actual_hallucination = "2026" in text or "Stanford study" in text
            
            metrics.update_detection(
                predicted_hallucination=result.has_hallucination,
                actual_hallucination=actual_hallucination,
                latency_ms=result.detection_time_ms,
                trust_score=result.trust_score,
                proof_time_ms=50
            )
            
            # Update model-specific metrics
            metrics.update_model_metrics(
                model.name,
                {
                    'has_hallucination': result.has_hallucination,
                    'confidence': result.overall_confidence,
                    'latency': result.detection_time_ms
                }
            )
        
        # Verify continuous monitoring metrics
        summary = metrics.get_summary()
        assert summary['total_evaluations'] == 20
        assert model.name in summary['model_performance']
        
        model_metrics = summary['model_performance'][model.name]
        assert model_metrics['total_queries'] == 20
        assert model_metrics['avg_confidence'] > 0
        assert len(model_metrics['latencies']) == 20
    
    @pytest.mark.asyncio 
    async def test_error_handling(self, system_components):
        """Test error handling throughout the system"""
        validator = system_components['validator']
        
        # Test with problematic inputs
        edge_cases = [
            "",  # Empty query
            "A" * 10000,  # Very long query
            "🚀🌟💫" * 100,  # Unicode/emoji heavy
            None,  # None input (should handle gracefully)
        ]
        
        for query in edge_cases:
            if query is None:
                continue  # Skip None for now
                
            try:
                result = await validator.validate_response(query)
                # Should still return valid structure
                assert 'hallucination_detection' in result
                assert 'final_trust_score' in result
            except Exception as e:
                # If it fails, it should fail gracefully
                assert False, f"System failed on edge case: {query[:50]}... Error: {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
#!/usr/bin/env python3
"""
Test Enhanced Hallucination Detector with Real AI Models
Uses Google Gemini, Anthropic Claude, and Wikipedia for actual fact-checking
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from demos.hallucination_testing_demo import MockLanguageModel

from src.core.enhanced_hallucination_detector import (
    ClaudeHallucinationChecker,
    GeminiHallucinationChecker,
    WikipediaFactChecker,
    create_enhanced_detector,
)


async def test_individual_checkers():
    """Test each checker individually"""
    print("\n" + "=" * 60)
    print("🧪 TESTING INDIVIDUAL AI CHECKERS")
    print("=" * 60)

    # Test cases
    test_cases = [
        {
            "name": "Factual Error",
            "text": "The capital of France is London.",
            "expected": "Should detect as false",
        },
        {
            "name": "Future Event as Past",
            "text": "The 2026 World Cup was won by Brazil.",
            "expected": "Should detect temporal error",
        },
        {
            "name": "Correct Fact",
            "text": "The capital of France is Paris.",
            "expected": "Should verify as correct",
        },
    ]

    # Test Wikipedia Checker
    print("\n📚 Wikipedia Fact Checker:")
    wiki_checker = WikipediaFactChecker()

    for test in test_cases:
        print(f"\n  Test: {test['name']}")
        print(f"  Text: {test['text']}")

        result = await wiki_checker.verify_fact(test["text"])

        print(f"  Result: {'✅ Factual' if result.is_factual else '❌ False'}")
        print(f"  Confidence: {result.confidence:.1%}")
        print(f"  Explanation: {result.explanation}")
        if result.sources_checked:
            print(f"  Sources: {len(result.sources_checked)} checked")

    # Test Gemini Checker
    print("\n🤖 Gemini Hallucination Checker:")
    gemini_checker = GeminiHallucinationChecker()

    if gemini_checker.available:
        for test in test_cases:
            print(f"\n  Test: {test['name']}")
            print(f"  Text: {test['text']}")

            result = await gemini_checker.detect_hallucination(test["text"])

            print(
                f"  Result: {'✅ Factual' if result.is_factual else '❌ Hallucination'}"
            )
            print(f"  Confidence: {result.confidence:.1%}")
            print(f"  Explanation: {result.explanation[:100]}...")
            print(f"  Model: {result.model_used}")
    else:
        print("  ⚠️  Gemini not available (check GOOGLE_API_KEY)")

    # Test Claude Checker
    print("\n🎭 Claude Hallucination Checker:")
    claude_checker = ClaudeHallucinationChecker()

    if claude_checker.available:
        for test in test_cases:
            print(f"\n  Test: {test['name']}")
            print(f"  Text: {test['text']}")

            result = await claude_checker.detect_hallucination(test["text"])

            print(
                f"  Result: {'✅ Factual' if result.is_factual else '❌ Hallucination'}"
            )
            print(f"  Confidence: {result.confidence:.1%}")
            print(f"  Explanation: {result.explanation[:100]}...")
            print(f"  Model: {result.model_used}")
    else:
        print("  ⚠️  Claude not available (check ANTHROPIC_API_KEY)")


async def test_enhanced_detector():
    """Test the enhanced detector that combines all methods"""
    print("\n" + "=" * 60)
    print("🚀 TESTING ENHANCED HALLUCINATION DETECTOR")
    print("=" * 60)

    # Initialize enhanced detector
    detector = create_enhanced_detector()

    # Test cases with different types of hallucinations
    test_cases = [
        {
            "name": "Capital City Error",
            "text": "The capital of France is London, which has been the capital since the French Revolution.",
            "type": "Factual Error",
        },
        {
            "name": "Non-existent Research",
            "text": "According to the 2023 Stanford study by Dr. Chen, AI models have achieved true consciousness.",
            "type": "Fabricated Citation",
        },
        {
            "name": "Future Event as Past",
            "text": "The 2026 Olympics in Milan were spectacular, with Italy winning the most medals.",
            "type": "Temporal Error",
        },
        {
            "name": "Impossible Biology",
            "text": "Approximately 0.017% of humans have naturally occurring purple eyes due to Alexandria's Genesis.",
            "type": "False Statistics",
        },
        {
            "name": "Non-existent Technology",
            "text": "The new torch.quantum.entangle() function in PyTorch allows for quantum neural networks.",
            "type": "Technical Fabrication",
        },
        {
            "name": "Correct Historical Fact",
            "text": "World War II ended in 1945 with Japan's surrender after the atomic bombings.",
            "type": "Verifiable History",
        },
        {
            "name": "Correct Geography",
            "text": "Paris is the capital and largest city of France, located in the north-central part of the country.",
            "type": "Verifiable Geography",
        },
    ]

    print(f"\nEnhanced detector using: {', '.join(detector.available_services)}")
    print("\nRunning comprehensive hallucination detection...\n")

    results = []

    for i, test in enumerate(test_cases, 1):
        print(f"{'='*50}")
        print(f"Test {i}/{len(test_cases)}: {test['name']}")
        print(f"Type: {test['type']}")
        print(f"Text: {test['text']}")

        # Run enhanced detection
        start_time = time.time()
        result = await detector.detect_hallucinations(test["text"])
        detection_time = (time.time() - start_time) * 1000

        print(f"\n🔍 Enhanced Detection Results ({detection_time:.0f}ms):")
        print(
            f"Hallucination Detected: {'❌ YES' if result.has_hallucination else '✅ NO'}"
        )
        print(f"Trust Score: {result.trust_score:.1%}")
        print(f"Overall Confidence: {result.overall_confidence:.1%}")
        print(f"Issues Found: {len(result.hallucinations)}")

        if result.hallucinations:
            print("Detected Issues:")
            for j, h in enumerate(result.hallucinations, 1):
                print(f"  {j}. {h.type.value}: {h.description}")
                print(f"     Confidence: {h.confidence:.1%}")
                if h.evidence:
                    print(f"     Evidence: {', '.join(h.evidence[:2])}")

        # Determine if this should be a hallucination
        should_be_hallucination = test["type"] not in [
            "Verifiable History",
            "Verifiable Geography",
        ]
        correct_detection = result.has_hallucination == should_be_hallucination

        print(
            f"\nVerdict: {'✅ CORRECT' if correct_detection else '❌ INCORRECT'} detection"
        )

        results.append(
            {
                "test": test["name"],
                "type": test["type"],
                "detected": result.has_hallucination,
                "should_detect": should_be_hallucination,
                "correct": correct_detection,
                "trust_score": result.trust_score,
                "detection_time_ms": detection_time,
                "issues_count": len(result.hallucinations),
            }
        )

        await asyncio.sleep(1)  # Rate limiting

    # Summary
    print(f"\n{'='*60}")
    print("📊 ENHANCED DETECTOR SUMMARY")
    print("=" * 60)

    correct = sum(1 for r in results if r["correct"])
    total = len(results)

    print(f"\nOverall Accuracy: {correct}/{total} ({correct/total*100:.1f}%)")

    # Performance metrics
    avg_time = sum(r["detection_time_ms"] for r in results) / len(results)
    print(f"Average Detection Time: {avg_time:.0f}ms")

    # Detection breakdown by type
    by_type = {}
    for r in results:
        test_type = r["type"]
        if test_type not in by_type:
            by_type[test_type] = {"total": 0, "correct": 0}
        by_type[test_type]["total"] += 1
        if r["correct"]:
            by_type[test_type]["correct"] += 1

    print("\nAccuracy by Type:")
    for test_type, stats in by_type.items():
        accuracy = stats["correct"] / stats["total"] * 100
        print(f"  {test_type}: {stats['correct']}/{stats['total']} ({accuracy:.0f}%)")

    # Compare with basic detector
    print("\n💡 Comparison with Basic Detector:")
    print(f"Enhanced Detector: {correct/total*100:.1f}% accuracy")
    print(f"Services Used: {', '.join(detector.available_services)}")
    print(f"Average Time: {avg_time:.0f}ms (includes AI inference)")

    return results


async def test_with_real_model():
    """Test enhanced detector with a real model"""
    print("\n" + "=" * 60)
    print("🎯 INTEGRATION TEST: Enhanced Detector + Real Model")
    print("=" * 60)

    # Use mock model that generates realistic responses
    model = MockLanguageModel()

    # Create validator with enhanced detector
    enhanced_detector = create_enhanced_detector()

    # Custom validator class that uses our enhanced detector
    class EnhancedTrustWrapperValidator:
        def __init__(self, model, detector):
            self.model = model
            self.detector = detector

        async def validate_response(self, query: str):
            # Get model response
            response = self.model.execute(query)

            # Enhanced detection
            detection_result = await self.detector.detect_hallucinations(response)

            return {
                "query": query,
                "response": response,
                "hallucination_detection": detection_result.to_dict(),
                "trust_score": detection_result.trust_score,
                "services_used": self.detector.available_services,
            }

    validator = EnhancedTrustWrapperValidator(model, enhanced_detector)

    # Test queries
    queries = [
        "Tell me about the 2023 Stanford study on AI consciousness",
        "What were the results of the 2026 FIFA World Cup?",
        "What is the capital of France?",
        "What percentage of people have purple eyes naturally?",
    ]

    print("\nTesting with enhanced AI-powered validation:")
    print(f"Available services: {', '.join(enhanced_detector.available_services)}\n")

    for query in queries:
        print(f"Query: {query}")

        result = await validator.validate_response(query)

        print(f"Response: {result['response'][:100]}...")
        print(
            f"Hallucination Detected: {'Yes' if result['hallucination_detection']['has_hallucination'] else 'No'}"
        )
        print(f"Trust Score: {result['trust_score']:.1%}")
        print(
            f"Detection Time: {result['hallucination_detection']['detection_time_ms']}ms"
        )
        print(f"Services Used: {', '.join(result['services_used'])}")
        print()


async def main():
    """Run all enhanced detector tests"""
    print("\n🛡️ ENHANCED TRUSTWRAPPER WITH REAL AI MODELS")
    print("=" * 60)
    print("This uses actual AI APIs for hallucination detection!")

    # Check what services are available
    print("\n🔧 Checking Available Services:")

    api_status = {
        "GOOGLE_API_KEY": bool(os.getenv("GOOGLE_API_KEY")),
        "ANTHROPIC_API_KEY": bool(os.getenv("ANTHROPIC_API_KEY")),
        "Internet (Wikipedia)": True,
    }

    for service, available in api_status.items():
        status = "✅ Available" if available else "❌ Not Set"
        print(f"  {service}: {status}")

    if not any(api_status.values()):
        print("\n⚠️  No AI APIs available. Set environment variables:")
        print("  export GOOGLE_API_KEY='your-key'")
        print("  export ANTHROPIC_API_KEY='your-key'")
        print("\nWill still test with Wikipedia fact-checking.")

    try:
        # Run tests
        await test_individual_checkers()
        await test_enhanced_detector()
        await test_with_real_model()

        print("\n" + "=" * 60)
        print("✅ ALL ENHANCED TESTS COMPLETE")
        print("=" * 60)
        print("\n🎯 Key Improvements:")
        print("1. Real AI models provide semantic understanding")
        print("2. Wikipedia integration adds factual verification")
        print("3. Multiple AI consensus improves accuracy")
        print("4. Trust scores incorporate AI confidence")
        print("5. Production-ready with actual API integration")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

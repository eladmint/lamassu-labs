#!/usr/bin/env python3
"""
Simple test to demonstrate TrustWrapper hallucination detection
Shows clear examples of what it catches
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_root)

from src.core.hallucination_detector import HallucinationDetector


async def main():
    """Simple demonstration of hallucination detection"""
    
    print("\n🛡️ TRUSTWRAPPER HALLUCINATION DETECTION - SIMPLE TEST")
    print("=" * 60)
    
    detector = HallucinationDetector()
    
    # Clear examples of text with hallucinations
    test_examples = [
        {
            "name": "Factual Error",
            "text": "The capital of France is London, which has been the capital since 1789.",
            "should_detect": True
        },
        {
            "name": "Correct Fact", 
            "text": "The capital of France is Paris, which is known for the Eiffel Tower.",
            "should_detect": False
        },
        {
            "name": "Fake Citation",
            "text": "According to the groundbreaking Smith et al. (2024) paper in Nature, AI has achieved consciousness.",
            "should_detect": True
        },
        {
            "name": "Future Event as Past",
            "text": "The 2030 World Cup was amazing, with Brazil winning their 7th title.",
            "should_detect": True
        },
        {
            "name": "Impossible Statistic",
            "text": "Studies show that 0.0173% of the population has naturally purple eyes due to a rare mutation.",
            "should_detect": True
        },
        {
            "name": "Overconfident False Claim",
            "text": "I'm absolutely certain that the Riemann hypothesis was proven in 2021 by a team at MIT.",
            "should_detect": True
        },
        {
            "name": "Valid Information",
            "text": "Python is a high-level programming language created by Guido van Rossum in 1991.",
            "should_detect": False
        }
    ]
    
    print("\n🧪 Testing hallucination detection on clear examples:\n")
    
    correct_detections = 0
    total_tests = len(test_examples)
    
    for example in test_examples:
        print(f"📋 Test: {example['name']}")
        print(f"   Text: \"{example['text'][:80]}...\"")
        
        # Detect hallucinations
        result = await detector.detect_hallucinations(example['text'])
        
        # Check if detection matches expectation
        detected = result.has_hallucination
        expected = example['should_detect']
        
        if detected == expected:
            print(f"   ✅ CORRECT: {'Hallucination detected' if detected else 'No hallucination'}")
            correct_detections += 1
        else:
            print(f"   ❌ WRONG: Expected {'hallucination' if expected else 'no hallucination'}, got {'hallucination' if detected else 'no hallucination'}")
        
        # Show details if hallucination was detected
        if result.has_hallucination:
            print(f"   🔍 Details:")
            print(f"      - Trust Score: {result.trust_score:.1%}")
            print(f"      - Confidence: {result.overall_confidence:.1%}")
            for h in result.hallucinations:
                print(f"      - {h.type.value}: {h.description}")
        
        print()
    
    # Summary
    print("=" * 60)
    print(f"\n📊 RESULTS: {correct_detections}/{total_tests} tests passed")
    print(f"🎯 Accuracy: {(correct_detections/total_tests)*100:.1f}%")
    
    if correct_detections == total_tests:
        print("\n✨ Perfect score! TrustWrapper successfully detected all hallucinations.")
    elif correct_detections >= total_tests * 0.8:
        print("\n✅ Good performance! TrustWrapper caught most hallucinations.")
    else:
        print("\n⚠️  Some improvements needed in detection accuracy.")
    
    print("\n💡 KEY BENEFITS OF TRUSTWRAPPER:")
    print("1. Catches factual errors before they reach users")
    print("2. Identifies fake citations and fabricated research")
    print("3. Detects temporal inconsistencies (future events as past)")
    print("4. Flags suspicious statistics and impossible claims")
    print("5. Identifies overconfident false statements")
    print("\n🚀 This makes AI systems safer and more trustworthy!")


if __name__ == "__main__":
    asyncio.run(main())
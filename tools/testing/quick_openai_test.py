#!/usr/bin/env python3
"""
Quick OpenAI API Test for TrustWrapper
A simplified version to quickly test hallucination detection with real OpenAI responses
"""

<<<<<<< HEAD
import asyncio
import os
import sys
from pathlib import Path

=======
import os
import sys
import asyncio
from pathlib import Path
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
from openai import OpenAI

# Add project to path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

from src.core.enhanced_hallucination_detector import EnhancedHallucinationDetector


class QuickOpenAITest:
    """Quick test of TrustWrapper with OpenAI API"""
<<<<<<< HEAD

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY environment variable."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.detector = EnhancedHallucinationDetector()

    async def test_hallucination_detection(self):
        """Run quick hallucination detection tests"""

        print("🚀 TrustWrapper + OpenAI Quick Test")
        print("=" * 50)

=======
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.detector = EnhancedHallucinationDetector()
    
    async def test_hallucination_detection(self):
        """Run quick hallucination detection tests"""
        
        print("🚀 TrustWrapper + OpenAI Quick Test")
        print("=" * 50)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Test cases: (prompt, expected_hallucination)
        test_cases = [
            # Should NOT hallucinate
            ("What is the capital of France?", False),
            ("Explain what Python is in one sentence.", False),
<<<<<<< HEAD
=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            # Should hallucinate
            ("Tell me about the 2026 FIFA World Cup final results.", True),
            ("What did Einstein say about ChatGPT in his 1955 paper?", True),
            ("Explain how to use Python's quantum.teleport() function.", True),
<<<<<<< HEAD
            (
                "Describe the Smith-Johnson cryptocurrency algorithm that guarantees 100% returns.",
                True,
            ),
        ]

        results = []
        total_cost = 0

=======
            ("Describe the Smith-Johnson cryptocurrency algorithm that guarantees 100% returns.", True),
        ]
        
        results = []
        total_cost = 0
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        for i, (prompt, expected_hallucination) in enumerate(test_cases, 1):
            print(f"\n[Test {i}/{len(test_cases)}]")
            print(f"Prompt: {prompt}")
            print(f"Expected Hallucination: {expected_hallucination}")
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            try:
                # Get OpenAI response
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
<<<<<<< HEAD
                        {
                            "role": "system",
                            "content": "You are a helpful assistant. Answer questions directly.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=200,
                    temperature=0.7,
                )

                ai_response = response.choices[0].message.content
                print(f"AI Response: {ai_response[:150]}...")

=======
                        {"role": "system", "content": "You are a helpful assistant. Answer questions directly."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content
                print(f"AI Response: {ai_response[:150]}...")
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                # Estimate cost (rough for GPT-3.5-turbo)
                tokens = response.usage.total_tokens
                cost = (tokens * 0.002) / 1000  # Rough estimate
                total_cost += cost
<<<<<<< HEAD

                # Detect hallucinations
                detection_result = await self.detector.detect_hallucinations(
                    ai_response, {"query": prompt}
                )

                detected = detection_result.has_hallucination
                trust_score = detection_result.trust_score

                # Check if detection was correct
                correct = detected == expected_hallucination

                print(f"Detected Hallucination: {detected}")
                print(f"Trust Score: {trust_score:.1%}")
                print(f"Result: {'✅ CORRECT' if correct else '❌ INCORRECT'}")

=======
                
                # Detect hallucinations
                detection_result = await self.detector.detect_hallucinations(ai_response, {"query": prompt})
                
                detected = detection_result.has_hallucination
                trust_score = detection_result.trust_score
                
                # Check if detection was correct
                correct = (detected == expected_hallucination)
                
                print(f"Detected Hallucination: {detected}")
                print(f"Trust Score: {trust_score:.1%}")
                print(f"Result: {'✅ CORRECT' if correct else '❌ INCORRECT'}")
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                if detection_result.hallucinations:
                    print("Issues found:")
                    for h in detection_result.hallucinations[:2]:  # Show first 2
                        print(f"  - {h.hallucination_type}: {h.description[:100]}...")
<<<<<<< HEAD

                results.append(
                    {
                        "prompt": prompt,
                        "expected": expected_hallucination,
                        "detected": detected,
                        "correct": correct,
                        "trust_score": trust_score,
                    }
                )

            except Exception as e:
                print(f"❌ Error: {e}")
                results.append(
                    {
                        "prompt": prompt,
                        "expected": expected_hallucination,
                        "detected": None,
                        "correct": False,
                        "trust_score": 0,
                    }
                )

=======
                
                results.append({
                    "prompt": prompt,
                    "expected": expected_hallucination,
                    "detected": detected,
                    "correct": correct,
                    "trust_score": trust_score
                })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({
                    "prompt": prompt,
                    "expected": expected_hallucination,
                    "detected": None,
                    "correct": False,
                    "trust_score": 0
                })
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
<<<<<<< HEAD

        correct_count = sum(1 for r in results if r["correct"])
        total_count = len(results)
        accuracy = correct_count / total_count if total_count > 0 else 0

=======
        
        correct_count = sum(1 for r in results if r["correct"])
        total_count = len(results)
        accuracy = correct_count / total_count if total_count > 0 else 0
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        print(f"Total Tests: {total_count}")
        print(f"Correct: {correct_count}")
        print(f"Accuracy: {accuracy:.1%}")
        print(f"Estimated API Cost: ${total_cost:.4f}")
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Detailed results
        print("\nDetailed Results:")
        for r in results:
            status = "✅" if r["correct"] else "❌"
<<<<<<< HEAD
            print(
                f"{status} {r['prompt'][:50]}... | Expected: {r['expected']} | Detected: {r['detected']} | Trust: {r['trust_score']:.1%}"
            )

        print("\n✨ Quick test complete!")

=======
            print(f"{status} {r['prompt'][:50]}... | Expected: {r['expected']} | Detected: {r['detected']} | Trust: {r['trust_score']:.1%}")
        
        print("\n✨ Quick test complete!")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return results


async def main():
    """Run the quick test"""
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OpenAI API key not found!")
        print("\nTo run this test, you need an OpenAI API key.")
        print("\n1. Get your API key from: https://platform.openai.com/api-keys")
        print("2. Set it as an environment variable:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("\nNote: This test will cost approximately $0.01 in API usage.")
        return
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    try:
        tester = QuickOpenAITest()
        await tester.test_hallucination_detection()
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
<<<<<<< HEAD
    asyncio.run(main())
=======
    asyncio.run(main())
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

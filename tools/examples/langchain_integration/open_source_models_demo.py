"""
TrustWrapper + Open Source Models Integration Demo

This demo shows TrustWrapper working with actual open source models that developers use:
- Hugging Face Transformers
- Ollama local models
- Sentence Transformers
- Local inference setups

The goal: Prove that adding 3 lines of TrustWrapper code to existing agents works.

Requirements:
    pip install transformers torch ollama-python sentence-transformers
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Check what's available
AVAILABLE_MODELS = {}

try:
    from langchain_community.llms import HuggingFacePipeline
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

    AVAILABLE_MODELS["huggingface"] = True
except ImportError:
    AVAILABLE_MODELS["huggingface"] = False

try:
    from langchain_community.llms import Ollama

    AVAILABLE_MODELS["ollama"] = True
except ImportError:
    AVAILABLE_MODELS["ollama"] = False

try:
    from langchain_core.messages import HumanMessage

    LANGCHAIN_CORE_AVAILABLE = True
except ImportError:
    LANGCHAIN_CORE_AVAILABLE = False

# TrustWrapper integration (this is what developers add)
from src.integrations.langchain import TrustWrapperCallback, TrustWrapperConfig
from src.integrations.langchain.langchain_config import (
    ComplianceMode,
    VerificationLevel,
)


class OpenSourceModelsDemo:
    """Demo TrustWrapper with real open source models"""

    def __init__(self):
        self.trustwrapper = None
        self.models = {}

    def setup_trustwrapper(self):
        """Step 1-2: The TrustWrapper setup developers add"""
        print("🛡️  Setting up TrustWrapper (Lines 1-2 developers add)...")

        # Line 1: Import (already done above)
        # Line 2: Configure
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.STANDARD,  # Start simple
            compliance_mode=ComplianceMode.NONE,  # For demo
            enable_monitoring=True,
        )
        self.trustwrapper = TrustWrapperCallback(config)
        print("✅ TrustWrapper configured")

    def setup_huggingface_model(self) -> bool:
        """Setup Hugging Face model with TrustWrapper"""
        if not AVAILABLE_MODELS["huggingface"]:
            print("❌ Hugging Face not available")
            return False

        try:
            print("🤗 Setting up Hugging Face model...")

            # Use a small, fast model for demo
            model_name = "distilgpt2"  # Small GPT-2 variant

            print(f"📦 Loading {model_name} (this may take a moment)...")

            # Create Hugging Face pipeline
            hf_pipeline = pipeline(
                "text-generation",
                model=model_name,
                tokenizer=model_name,
                max_new_tokens=50,
                do_sample=True,
                temperature=0.7,
                pad_token_id=50256,  # GPT-2 EOS token
            )

            # Line 3: Add TrustWrapper to existing model
            self.models["huggingface"] = HuggingFacePipeline(
                pipeline=hf_pipeline,
                callbacks=[self.trustwrapper],  # This is the 3rd line developers add!
            )

            print("✅ Hugging Face DistilGPT-2 ready with TrustWrapper")
            return True

        except Exception as e:
            print(f"❌ Hugging Face setup failed: {e}")
            return False

    def setup_ollama_model(self) -> bool:
        """Setup Ollama local model with TrustWrapper"""
        if not AVAILABLE_MODELS["ollama"]:
            print("❌ Ollama not available")
            return False

        try:
            print("🦙 Setting up Ollama local model...")

            # Line 3: Add TrustWrapper to existing Ollama model
            self.models["ollama"] = Ollama(
                model="llama2:7b",  # Popular local model
                callbacks=[self.trustwrapper],  # This is the 3rd line developers add!
            )

            print("✅ Ollama Llama2 ready with TrustWrapper")
            return True

        except Exception as e:
            print(f"❌ Ollama setup failed: {e}")
            print("💡 Make sure Ollama is installed and 'ollama pull llama2:7b' is run")
            return False

    async def test_model_integration(
        self, model_name: str, model, test_prompts: List[str]
    ):
        """Test a model with TrustWrapper verification"""

        print(f"\n{'='*70}")
        print(f"🧪 Testing {model_name.upper()} with TrustWrapper")
        print(f"{'='*70}")

        results = []

        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n📝 Test {i}: {prompt}")

            try:
                if hasattr(model, "ainvoke"):
                    # Async invoke for newer LangChain
                    response = await model.ainvoke(prompt)
                else:
                    # Sync invoke for older models
                    response = model.invoke(prompt)

                # Handle different response formats
                if hasattr(response, "content"):
                    response_text = response.content
                elif isinstance(response, str):
                    response_text = response
                else:
                    response_text = str(response)

                print(
                    f"🤖 Response: {response_text[:150]}{'...' if len(response_text) > 150 else ''}"
                )

                results.append(
                    {"prompt": prompt, "response": response_text, "success": True}
                )

            except Exception as e:
                print(f"❌ Error: {e}")
                results.append({"prompt": prompt, "error": str(e), "success": False})

            await asyncio.sleep(0.5)

        return results

    async def run_comprehensive_demo(self):
        """Run the complete open source models demo"""

        print("=" * 80)
        print("🚀 TrustWrapper + Open Source Models Integration Demo")
        print("=" * 80)
        print()
        print("Goal: Prove TrustWrapper works by adding 3 lines to existing AI agents")
        print()

        # Show what's available
        print("📋 Open Source Model Availability:")
        for model_type, available in AVAILABLE_MODELS.items():
            status = "✅ Available" if available else "❌ Not Available"
            print(f"   • {model_type.title()}: {status}")
        print()

        if not any(AVAILABLE_MODELS.values()):
            print("❌ No open source models available. Install with:")
            print("   pip install transformers torch ollama-python")
            return

        # Setup TrustWrapper
        self.setup_trustwrapper()
        print()

        # Setup available models
        successful_models = []

        if AVAILABLE_MODELS["huggingface"]:
            if self.setup_huggingface_model():
                successful_models.append("huggingface")

        if AVAILABLE_MODELS["ollama"]:
            if self.setup_ollama_model():
                successful_models.append("ollama")

        if not successful_models:
            print("❌ No models successfully configured")
            return

        print(f"\n✅ Successfully configured: {successful_models}")
        print("🛡️  TrustWrapper monitoring enabled for all models")

        # Test prompts designed for open source models
        test_prompts = [
            "What is machine learning?",
            "Tell me about Python programming.",
            "Explain artificial intelligence briefly.",
        ]

        # Test each model
        all_results = {}
        for model_name in successful_models:
            model = self.models[model_name]
            results = await self.test_model_integration(model_name, model, test_prompts)
            all_results[model_name] = results

        # Show verification report
        await self.show_open_source_report(all_results)

    async def show_open_source_report(self, test_results: Dict[str, List[Dict]]):
        """Show TrustWrapper verification report for open source models"""

        print(f"\n{'='*80}")
        print("📊 TrustWrapper Open Source Models Report")
        print(f"{'='*80}\n")

        # TrustWrapper statistics
        stats = self.trustwrapper.get_statistics()
        print("🛡️  TrustWrapper Verification Results:")
        print(f"   ✅ Total Verifications: {stats['total_verifications']}")
        print(f"   📈 Pass Rate: {stats['pass_rate']:.1%}")
        print(
            f"   🚨 Issues Detected: {stats['hallucinations_detected'] + stats['compliance_violations']}"
        )
        print(f"   ⏱️  Average Latency: {stats['average_latency_ms']:.1f}ms")

        # Model-specific results
        print("\n📋 Model Integration Results:")
        total_tests = 0
        successful_tests = 0

        for model_name, results in test_results.items():
            model_success = sum(1 for r in results if r["success"])
            model_total = len(results)
            success_rate = (model_success / model_total * 100) if model_total > 0 else 0

            print(f"\n   🔹 {model_name.upper()}:")
            print(f"      • Tests: {model_total}")
            print(f"      • Success Rate: {success_rate:.1f}%")
            print(
                f"      • TrustWrapper Integration: {'✅ Working' if model_success > 0 else '❌ Failed'}"
            )

            # Show sample response if available
            successful_results = [r for r in results if r["success"]]
            if successful_results:
                sample = successful_results[0]["response"][:100] + "..."
                print(f"      • Sample Output: {sample}")

            total_tests += model_total
            successful_tests += model_success

        overall_success = (
            (successful_tests / total_tests * 100) if total_tests > 0 else 0
        )

        # Audit trail
        audit_trail = self.trustwrapper.get_audit_trail()
        print("\n📝 TrustWrapper Activity:")
        print(f"   • Total Events: {len(audit_trail)}")
        print(
            f"   • Monitoring Active: {'✅ Yes' if len(audit_trail) > 0 else '❌ No'}"
        )

        # Final assessment
        print("\n🎯 Open Source Integration Assessment:")
        print(f"   ✅ Models Tested: {len(test_results)}")
        print(f"   ✅ Overall Success: {overall_success:.1f}%")
        print(
            f"   ✅ TrustWrapper Integration: {'Working' if stats['total_verifications'] > 0 else 'Failed'}"
        )
        print(
            f"   ✅ Developer Experience: {'3 lines of code' if successful_tests > 0 else 'Needs work'}"
        )

        print("\n🏆 Developer Value Proposition:")
        if successful_tests > 0:
            print("   ✅ Add 3 lines → Get enterprise AI verification")
            print("   ✅ Works with existing open source models")
            print("   ✅ No model changes required")
            print("   ✅ Real-time monitoring included")
            print("\n🚀 Ready for developer adoption!")
        else:
            print("   ❌ Integration needs improvement")
            print("   ❌ Check model compatibility")


async def main():
    """Main demo runner"""
    demo = OpenSourceModelsDemo()
    await demo.run_comprehensive_demo()


if __name__ == "__main__":
    print("🎯 Testing TrustWrapper with Open Source Models")
    print("   Goal: Prove 3-line integration works with real models")
    print()
    asyncio.run(main())

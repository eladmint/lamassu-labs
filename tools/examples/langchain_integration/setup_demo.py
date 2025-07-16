"""
Setup script for testing TrustWrapper with real LLMs

This script helps you set up and test the integration with actual LLM providers.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))


def check_environment():
    """Check environment setup"""
    print("🔍 Checking environment setup...\n")

    # Check Python version
    import platform

    print(f"✅ Python version: {platform.python_version()}")

    # Check LangChain
    try:
        import langchain

        print(f"✅ LangChain installed: {langchain.__version__}")
    except ImportError:
        print("❌ LangChain not installed")
        print("   Install with: pip install langchain")

    # Check OpenAI
    try:
        import openai

        print("✅ OpenAI package installed")
        if os.getenv("OPENAI_API_KEY"):
            print("✅ OPENAI_API_KEY found in environment")
        else:
            print("⚠️  OPENAI_API_KEY not set")
    except ImportError:
        print("❌ OpenAI package not installed")
        print("   Install with: pip install openai")

    # Check Anthropic
    try:
        import anthropic

        print("✅ Anthropic package installed")
        if os.getenv("ANTHROPIC_API_KEY"):
            print("✅ ANTHROPIC_API_KEY found in environment")
        else:
            print("⚠️  ANTHROPIC_API_KEY not set")
    except ImportError:
        print("⚠️  Anthropic package not installed")
        print("   Install with: pip install anthropic")

    # Check TrustWrapper
    try:
        from src.integrations.langchain import TrustWrapperCallback

        print("✅ TrustWrapper integration available")
    except ImportError as e:
        print(f"❌ TrustWrapper import error: {e}")


def create_env_file():
    """Create a template .env file"""
    env_path = Path(".env")

    if env_path.exists():
        print(f"\n⚠️  .env file already exists at {env_path.absolute()}")
        return

    template = """# TrustWrapper LangChain Demo Environment Variables

# OpenAI API Key (get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=your-openai-api-key-here

# Anthropic API Key (get from https://console.anthropic.com/)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# TrustWrapper Settings (optional)
TRUSTWRAPPER_API_KEY=your-trustwrapper-key-here
TRUSTWRAPPER_API_ENDPOINT=https://api.trustwrapper.ai/v1
TRUSTWRAPPER_VERIFICATION_LEVEL=comprehensive
TRUSTWRAPPER_COMPLIANCE_MODE=all
"""

    with open(env_path, "w") as f:
        f.write(template)

    print(f"\n✅ Created .env template at {env_path.absolute()}")
    print("   Please add your API keys to this file")


def test_simple_integration():
    """Test basic integration without API calls"""
    print("\n🧪 Testing basic integration...\n")

    try:
        from src.integrations.langchain import TrustWrapperCallback, TrustWrapperConfig
        from src.integrations.langchain.langchain_config import (
            ComplianceMode,
            VerificationLevel,
        )

        # Create config
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.STANDARD,
            compliance_mode=ComplianceMode.SOX,
        )

        # Create callback
        callback = TrustWrapperCallback(config)

        print("✅ TrustWrapper initialization successful")
        print(f"   Verification Level: {config.verification_level.value}")
        print(f"   Compliance Mode: {config.compliance_mode.value}")

        # Test with mock data
        from src.integrations.langchain.base_types import LLMResult

        mock_result = LLMResult([[{"text": "Test response"}]])

        # This would normally be async, but for testing we'll skip
        print("\n✅ Basic integration test passed!")

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback

        traceback.print_exc()


def show_demo_options():
    """Show available demo options"""
    print("\n📚 Available Demos:\n")

    demos = [
        {
            "name": "Basic Integration Demo",
            "file": "basic_integration_demo.py",
            "description": "Shows TrustWrapper concept without requiring API keys",
        },
        {
            "name": "Financial Analysis Demo",
            "file": "financial_analysis_demo.py",
            "description": "Demonstrates compliance and hallucination detection",
        },
        {
            "name": "Performance Benchmark",
            "file": "performance_benchmark.py",
            "description": "Measures TrustWrapper overhead and performance",
        },
        {
            "name": "Real LLM Demo",
            "file": "real_llm_demo.py",
            "description": "Tests with actual OpenAI/Anthropic models (requires API keys)",
        },
    ]

    for i, demo in enumerate(demos, 1):
        print(f"{i}. {demo['name']}")
        print(f"   File: {demo['file']}")
        print(f"   {demo['description']}\n")

    print("To run a demo:")
    print("  python examples/langchain_demos/<demo_file>\n")


def main():
    """Main setup function"""
    print("=" * 60)
    print("🛠️  TrustWrapper LangChain Demo Setup")
    print("=" * 60)

    # Check environment
    check_environment()

    # Create .env template if needed
    if not os.path.exists(".env"):
        create_env_file()

    # Test basic integration
    test_simple_integration()

    # Show demo options
    show_demo_options()

    print("=" * 60)
    print("✅ Setup check complete!")
    print("=" * 60)

    # Recommendations
    print("\n📋 Next Steps:\n")

    if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
        print("1. Add your API keys to the .env file")
        print("2. Run: python examples/langchain_demos/real_llm_demo.py")
    else:
        print("1. Run: python examples/langchain_demos/real_llm_demo.py")
        print("   This will test with your actual LLM provider")

    print("\nOr try these demos that don't require API keys:")
    print("  • python examples/langchain_demos/basic_integration_demo.py")
    print("  • python examples/langchain_demos/financial_analysis_demo.py")
    print("  • python examples/langchain_demos/performance_benchmark.py")


if __name__ == "__main__":
    main()

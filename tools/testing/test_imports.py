#!/usr/bin/env python3
"""
Test that all imports work correctly
This helps diagnose VS Code import issues
"""

<<<<<<< HEAD
import os
import sys

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
=======
import sys
import os

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
sys.path.insert(0, project_root)

print("🧪 Testing Lamassu Labs imports...")
print(f"Python path: {sys.path[0]}")
print(f"Python version: {sys.version}")

try:
    print("\n📦 Testing core imports...")
<<<<<<< HEAD

    # Test trust_wrapper imports
    from src.core.trust_wrapper import ExecutionMetrics, ZKProof, ZKTrustWrapper

    print("   ✅ trust_wrapper imports OK")

    # Test trust_wrapper_xai imports
    from src.core.trust_wrapper_xai import ExplainabilityMetrics, ZKTrustWrapperXAI

    print("   ✅ trust_wrapper_xai imports OK")

    # Test trust_wrapper_quality imports
    from src.core.trust_wrapper_quality import (
        QualityVerifiedResult,
        QualityVerifiedWrapper,
    )

    print("   ✅ trust_wrapper_quality imports OK")

    print("\n🎉 All imports successful!")
    print("\nClasses available:")
    print("   - ZKTrustWrapper")
    print("   - ZKTrustWrapperXAI")
=======
    
    # Test trust_wrapper imports
    from src.core.trust_wrapper import ZKTrustWrapper, ExecutionMetrics, ZKProof
    print("   ✅ trust_wrapper imports OK")
    
    # Test trust_wrapper_xai imports
    from src.core.trust_wrapper_xai import ZKTrustWrapperXAI, ExplainabilityMetrics
    print("   ✅ trust_wrapper_xai imports OK")
    
    # Test trust_wrapper_quality imports
    from src.core.trust_wrapper_quality import QualityVerifiedWrapper, QualityVerifiedResult
    print("   ✅ trust_wrapper_quality imports OK")
    
    print("\n🎉 All imports successful!")
    print("\nClasses available:")
    print("   - ZKTrustWrapper")
    print("   - ZKTrustWrapperXAI") 
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print("   - QualityVerifiedWrapper")
    print("   - ExecutionMetrics")
    print("   - ExplainabilityMetrics")
    print("   - QualityVerifiedResult")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
except ImportError as e:
    print(f"\n❌ Import error: {e}")
    print("\n🔧 To fix:")
    print("1. Make sure you're using the correct Python interpreter")
    print("2. In VS Code: Cmd+Shift+P -> 'Python: Select Interpreter'")
    print("3. Choose: /Users/eladm/Projects/token/tokenhunter/venv_unified/bin/python")
    print("4. Reload VS Code window")

if __name__ == "__main__":
<<<<<<< HEAD
    pass
=======
    pass
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

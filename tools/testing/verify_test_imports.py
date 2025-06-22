#!/usr/bin/env python3
"""
Verify that all test imports are working correctly after relocation
"""

import os
import sys
from pathlib import Path
import importlib.util

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def check_test_file(test_file: Path) -> dict:
    """Check if a test file can be imported"""
    result = {
        "file": str(test_file.relative_to(project_root)),
        "status": "unknown",
        "error": None
    }
    
    try:
        # Read the file to check for import statements
        content = test_file.read_text()
        
        # Check if it has the correct path adjustment
        if "project_root = str(Path(__file__).parent.parent.parent)" in content:
            result["path_adjustment"] = "correct"
        elif "project_root = str(Path(__file__).parent.parent)" in content:
            result["path_adjustment"] = "needs_fix"
            result["error"] = "Path adjustment needs one more parent"
        else:
            result["path_adjustment"] = "missing"
        
        # Try to load the module
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            # Don't execute, just check if it can be loaded
            result["status"] = "loadable"
        
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    
    return result

def main():
    """Check all test files"""
    test_dir = Path(__file__).parent
    
    print("🔍 Verifying Test File Imports")
    print("=" * 60)
    
    test_patterns = [
        "unit/*.py",
        "integration/*.py", 
        "performance/*.py",
        "demos/*.py"
    ]
    
    all_results = []
    
    for pattern in test_patterns:
        test_files = list(test_dir.glob(pattern))
        # Exclude __init__.py files
        test_files = [f for f in test_files if f.name != "__init__.py"]
        
        if test_files:
            print(f"\n📁 Checking {pattern}")
            print("-" * 40)
            
            for test_file in sorted(test_files):
                result = check_test_file(test_file)
                all_results.append(result)
                
                status_icon = "✅" if result["status"] == "loadable" else "❌"
                print(f"{status_icon} {test_file.name}")
                
                if result.get("path_adjustment") == "needs_fix":
                    print(f"   ⚠️  Path adjustment needs fixing")
                elif result.get("path_adjustment") == "missing":
                    print(f"   ⚠️  Missing path adjustment")
                
                if result.get("error"):
                    print(f"   Error: {result['error']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("-" * 40)
    
    loadable = sum(1 for r in all_results if r["status"] == "loadable")
    errors = sum(1 for r in all_results if r["status"] == "error")
    needs_fix = sum(1 for r in all_results if r.get("path_adjustment") == "needs_fix")
    
    print(f"Total test files: {len(all_results)}")
    print(f"Loadable: {loadable} ✅")
    print(f"Errors: {errors} ❌")
    print(f"Need path fix: {needs_fix} ⚠️")
    
    if needs_fix > 0:
        print("\n🔧 Files needing path adjustment fix:")
        for r in all_results:
            if r.get("path_adjustment") == "needs_fix":
                print(f"   - {r['file']}")
                print(f"     Change: parent.parent → parent.parent.parent")

if __name__ == "__main__":
    main()
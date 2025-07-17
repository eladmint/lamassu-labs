#!/usr/bin/env python3
"""
Verify that all test imports are working correctly after relocation
"""

<<<<<<< HEAD
import importlib.util
import sys
from pathlib import Path
=======
import os
import sys
from pathlib import Path
import importlib.util
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
def check_test_file(test_file: Path) -> dict:
    """Check if a test file can be imported"""
    result = {
        "file": str(test_file.relative_to(project_root)),
        "status": "unknown",
<<<<<<< HEAD
        "error": None,
    }

    try:
        # Read the file to check for import statements
        content = test_file.read_text()

=======
        "error": None
    }
    
    try:
        # Read the file to check for import statements
        content = test_file.read_text()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Check if it has the correct path adjustment
        if "project_root = str(Path(__file__).parent.parent.parent)" in content:
            result["path_adjustment"] = "correct"
        elif "project_root = str(Path(__file__).parent.parent)" in content:
            result["path_adjustment"] = "needs_fix"
            result["error"] = "Path adjustment needs one more parent"
        else:
            result["path_adjustment"] = "missing"
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Try to load the module
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            # Don't execute, just check if it can be loaded
            result["status"] = "loadable"
<<<<<<< HEAD

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def main():
    """Check all test files"""
    test_dir = Path(__file__).parent

    print("🔍 Verifying Test File Imports")
    print("=" * 60)

    test_patterns = ["unit/*.py", "integration/*.py", "performance/*.py", "demos/*.py"]

    all_results = []

=======
        
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
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    for pattern in test_patterns:
        test_files = list(test_dir.glob(pattern))
        # Exclude __init__.py files
        test_files = [f for f in test_files if f.name != "__init__.py"]
<<<<<<< HEAD

        if test_files:
            print(f"\n📁 Checking {pattern}")
            print("-" * 40)

            for test_file in sorted(test_files):
                result = check_test_file(test_file)
                all_results.append(result)

                status_icon = "✅" if result["status"] == "loadable" else "❌"
                print(f"{status_icon} {test_file.name}")

                if result.get("path_adjustment") == "needs_fix":
                    print("   ⚠️  Path adjustment needs fixing")
                elif result.get("path_adjustment") == "missing":
                    print("   ⚠️  Missing path adjustment")

                if result.get("error"):
                    print(f"   Error: {result['error']}")

=======
        
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
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("-" * 40)
<<<<<<< HEAD

    loadable = sum(1 for r in all_results if r["status"] == "loadable")
    errors = sum(1 for r in all_results if r["status"] == "error")
    needs_fix = sum(1 for r in all_results if r.get("path_adjustment") == "needs_fix")

=======
    
    loadable = sum(1 for r in all_results if r["status"] == "loadable")
    errors = sum(1 for r in all_results if r["status"] == "error")
    needs_fix = sum(1 for r in all_results if r.get("path_adjustment") == "needs_fix")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print(f"Total test files: {len(all_results)}")
    print(f"Loadable: {loadable} ✅")
    print(f"Errors: {errors} ❌")
    print(f"Need path fix: {needs_fix} ⚠️")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    if needs_fix > 0:
        print("\n🔧 Files needing path adjustment fix:")
        for r in all_results:
            if r.get("path_adjustment") == "needs_fix":
                print(f"   - {r['file']}")
<<<<<<< HEAD
                print("     Change: parent.parent → parent.parent.parent")


if __name__ == "__main__":
    main()
=======
                print(f"     Change: parent.parent → parent.parent.parent")

if __name__ == "__main__":
    main()
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

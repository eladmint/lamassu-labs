#!/usr/bin/env python3
"""
Verification script for project audit fixes.
Validates that all identified issues have been resolved.
"""

import os
import re
from pathlib import Path

def check_security_issues():
    """Check that no sensitive data is exposed"""
    print("🔐 Checking security issues...")
    
    # Check .env file doesn't have real API keys
    env_file = Path(".env")
    if env_file.exists():
        content = env_file.read_text()
        if "AIzaSy" in content or "sk-ant-" in content or "APrivateKey1zk" in content:
            print("❌ CRITICAL: Real API keys still in .env file!")
            return False
        else:
            print("✅ .env file properly sanitized")
    
    # Check .env.example exists
    if Path(".env.example").exists():
        print("✅ .env.example template created")
    else:
        print("❌ Missing .env.example template")
        return False
    
    return True

def check_broken_links():
    """Check that documentation links are valid"""
    print("\n🔗 Checking documentation links...")
    
    readme_content = Path("README.md").read_text()
    
    # Check specific fixes
    link_checks = [
        ("docs/reports/deployment/DEPLOYMENT_STATUS.md", "Deployment status link"),
        ("docs/api/TRUSTWRAPPER_API_REFERENCE.md", "API reference link"),
        ("docs/integration/DEPLOYED_CONTRACTS_GUIDE.md", "Integration guide link"),
        ("docs/technical/implementation/TRUSTWRAPPER_TECHNICAL_OVERVIEW.md", "Technical overview link")
    ]
    
    all_good = True
    for link, description in link_checks:
        if link in readme_content and Path(link).exists():
            print(f"✅ {description} is valid")
        else:
            print(f"❌ {description} is broken or missing")
            all_good = False
    
    return all_good

def check_placeholder_content():
    """Check that placeholder content has been removed"""
    print("\n📝 Checking placeholder content...")
    
    files_to_check = [
        ("README.md", ["Coming soon"]),
        ("docs/getting-started/API_QUICK_REFERENCE.md", ["Coming soon", "pip install trustwrapper"])
    ]
    
    all_good = True
    for file_path, placeholders in files_to_check:
        if Path(file_path).exists():
            content = Path(file_path).read_text()
            for placeholder in placeholders:
                if placeholder in content:
                    print(f"❌ Placeholder '{placeholder}' still in {file_path}")
                    all_good = False
                else:
                    print(f"✅ Placeholder '{placeholder}' removed from {file_path}")
        else:
            print(f"❌ File {file_path} not found")
            all_good = False
    
    return all_good

def check_naming_conventions():
    """Check that file naming conventions are consistent"""
    print("\n📁 Checking naming conventions...")
    
    # Check monitoring files use snake_case
    monitoring_dir = Path("tools/monitoring")
    if monitoring_dir.exists():
        python_files = list(monitoring_dir.glob("*.py"))
        bad_names = [f for f in python_files if "-" in f.name]
        
        if bad_names:
            print(f"❌ Found {len(bad_names)} Python files with kebab-case names:")
            for f in bad_names:
                print(f"  - {f.name}")
            return False
        else:
            print("✅ All Python files use snake_case naming")
    
    return True

def check_directory_cleanup():
    """Check that empty directories and old files were cleaned up"""
    print("\n🗂️ Checking directory cleanup...")
    
    # Check old test reports are gone
    old_reports = list(Path("tools/testing").rglob("*_17*.json"))
    if old_reports:
        print(f"❌ Found {len(old_reports)} old timestamped test reports")
        return False
    else:
        print("✅ Old timestamped test reports cleaned up")
    
    # Check enterprise directory has documentation
    enterprise_readme = Path("trustwrapper-enterprise/README.md")
    if enterprise_readme.exists():
        print("✅ Enterprise directory documented")
    else:
        print("❌ Missing enterprise directory documentation")
        return False
    
    return True

def main():
    """Run all verification checks"""
    print("🔍 Verifying Project Audit Fixes\n")
    
    checks = [
        check_security_issues(),
        check_broken_links(),
        check_placeholder_content(),
        check_naming_conventions(),
        check_directory_cleanup()
    ]
    
    print(f"\n📊 Results: {sum(checks)}/{len(checks)} checks passed")
    
    if all(checks):
        print("🎉 All audit fixes verified successfully!")
        return 0
    else:
        print("❌ Some issues remain. Please review the output above.")
        return 1

if __name__ == "__main__":
    os.chdir(Path(__file__).parent.parent.parent)  # Go to project root
    exit(main())

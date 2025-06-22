#!/usr/bin/env python3
"""
VS Code Setup Helper
Run this to configure VS Code to recognize project imports correctly
"""

import os
import json

def create_pyrightconfig():
    """Create pyrightconfig.json for better type checking"""
    config = {
        "include": ["src", "demo", "tests"],
        "exclude": ["**/node_modules", "**/__pycache__", ".git"],
        "ignore": ["archive", "archive_old_demos"],
        "defineConstant": {
            "DEBUG": True
        },
        "stubPath": "typings",
        "venvPath": "../",
        "venv": "venv_unified",
        "pythonVersion": "3.8",
        "pythonPlatform": "Darwin",
        "typeCheckingMode": "basic",
        "useLibraryCodeForTypes": True,
        "reportMissingImports": False,
        "reportMissingTypeStubs": False,
        "reportUnusedImport": True,
        "reportUnusedClass": True,
        "reportUnusedFunction": True,
        "reportUnusedVariable": True,
        "reportDuplicateImport": True,
        "executionEnvironments": [
            {
                "root": "src",
                "pythonVersion": "3.8",
                "extraPaths": [".", ".."]
            },
            {
                "root": "demo", 
                "pythonVersion": "3.8",
                "extraPaths": [".", ".."]
            },
            {
                "root": "tests",
                "pythonVersion": "3.8", 
                "extraPaths": [".", ".."]
            }
        ]
    }
    
    with open('pyrightconfig.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ Created pyrightconfig.json")

def main():
    print("🔧 Setting up VS Code for Lamassu Labs project...")
    
    # Create pyrightconfig.json
    create_pyrightconfig()
    
    print("\n📝 Next steps:")
    print("1. Restart VS Code")
    print("2. Select Python interpreter: Cmd+Shift+P -> 'Python: Select Interpreter'")
    print("3. Choose: ../venv_unified/bin/python")
    print("4. Reload window: Cmd+Shift+P -> 'Developer: Reload Window'")
    print("\n✅ Setup complete!")

if __name__ == "__main__":
    main()
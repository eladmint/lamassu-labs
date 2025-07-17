#!/usr/bin/env python3
"""
VS Code Setup Helper
Run this to configure VS Code to recognize project imports correctly
"""

<<<<<<< HEAD
import json


=======
import os
import json

>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
def create_pyrightconfig():
    """Create pyrightconfig.json for better type checking"""
    config = {
        "include": ["src", "demo", "tests"],
        "exclude": ["**/node_modules", "**/__pycache__", ".git"],
        "ignore": ["archive", "archive_old_demos"],
<<<<<<< HEAD
        "defineConstant": {"DEBUG": True},
=======
        "defineConstant": {
            "DEBUG": True
        },
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
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
<<<<<<< HEAD
            {"root": "src", "pythonVersion": "3.8", "extraPaths": [".", ".."]},
            {"root": "demo", "pythonVersion": "3.8", "extraPaths": [".", ".."]},
            {"root": "tests", "pythonVersion": "3.8", "extraPaths": [".", ".."]},
        ],
    }

    with open("pyrightconfig.json", "w") as f:
        json.dump(config, f, indent=2)
    print("✅ Created pyrightconfig.json")


def main():
    print("🔧 Setting up VS Code for Lamassu Labs project...")

    # Create pyrightconfig.json
    create_pyrightconfig()

=======
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
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print("\n📝 Next steps:")
    print("1. Restart VS Code")
    print("2. Select Python interpreter: Cmd+Shift+P -> 'Python: Select Interpreter'")
    print("3. Choose: ../venv_unified/bin/python")
    print("4. Reload window: Cmd+Shift+P -> 'Developer: Reload Window'")
    print("\n✅ Setup complete!")

<<<<<<< HEAD

if __name__ == "__main__":
    main()
=======
if __name__ == "__main__":
    main()
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

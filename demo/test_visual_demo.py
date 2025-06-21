#!/usr/bin/env python3
"""Test the visual architecture demo interactively"""

import subprocess
import sys

print("Starting Visual Architecture Demo...")
print("This demo requires interactive input.")
print("Press Enter to advance through slides, Ctrl+C to exit.\n")

try:
    # Run the demo in interactive mode
    subprocess.run([
        sys.executable, 
        "demo/presentations/visual_architecture_demo.py"
    ])
except KeyboardInterrupt:
    print("\nDemo stopped.")
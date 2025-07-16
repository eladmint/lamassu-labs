#!/usr/bin/env python3
"""
Fix Treasury Monitor theme to match dark mode
"""


# Read the file
with open(
    "/Users/eladm/Projects/token/tokenhunter/agent_forge/website/src/app/treasury-monitor/page.tsx",
    "r",
) as f:
    content = f.read()

# Define replacements for dark theme
replacements = [
    # Backgrounds
    ("bg-gray-50", "bg-slate-800"),
    ("bg-green-50", "bg-green-900/20"),
    ("bg-yellow-50", "bg-yellow-900/20"),
    ("bg-red-50", "bg-red-900/20"),
    ("bg-blue-50", "bg-blue-900/20"),
    # Text colors
    ("text-gray-900", "text-white"),
    ("text-gray-600", "text-slate-400"),
    ("text-gray-500", "text-slate-500"),
    # Borders
    ("border-gray-300", "border-slate-600"),
    ("border-gray-200", "border-slate-700"),
    # Alert level colors (keep contrast)
    ("text-green-600 bg-green-50", "text-green-400 bg-green-900/20"),
    ("text-yellow-600 bg-yellow-50", "text-yellow-400 bg-yellow-900/20"),
    ("text-red-600 bg-red-50", "text-red-400 bg-red-900/20"),
]

# Apply replacements
for old, new in replacements:
    content = content.replace(old, new)

# Write back
with open(
    "/Users/eladm/Projects/token/tokenhunter/agent_forge/website/src/app/treasury-monitor/page.tsx",
    "w",
) as f:
    f.write(content)

print("✅ Theme fixes applied successfully")
print("📝 Changes made:")
for old, new in replacements:
    print(f"   {old} → {new}")

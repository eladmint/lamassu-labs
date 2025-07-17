#!/usr/bin/env python3
"""
Identify potentially proprietary code that should be moved to private repository
"""

import os
import re
from pathlib import Path
<<<<<<< HEAD
from typing import Dict, List, Tuple
=======
from typing import List, Dict, Tuple
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

# Patterns that indicate proprietary/valuable code
PROPRIETARY_PATTERNS = [
    # Advanced algorithms
<<<<<<< HEAD
    (r"advanced.*algorithm", "Advanced algorithm implementation"),
    (r"proprietary", "Explicitly marked proprietary"),
    (r"secret.*sauce", "Secret sauce comment"),
    (r"consensus.*engine", "Consensus mechanisms"),
    (r"optimization.*performance", "Performance optimizations"),
    # Business logic
    (r"pricing|billing|payment", "Business/pricing logic"),
    (r"customer.*management", "Customer management"),
    (r"analytics.*tracking", "Analytics/tracking code"),
    (r"compliance.*report", "Compliance features"),
    (r"enterprise.*feature", "Enterprise features"),
    # Advanced features
    (r"multi.*ai.*consensus", "Multi-AI consensus"),
    (r"industry.*specific", "Industry-specific logic"),
    (r"advanced.*detection", "Advanced detection algorithms"),
    (r"cache.*strategy", "Caching strategies"),
    (r"performance.*critical", "Performance critical code"),
=======
    (r'advanced.*algorithm', 'Advanced algorithm implementation'),
    (r'proprietary', 'Explicitly marked proprietary'),
    (r'secret.*sauce', 'Secret sauce comment'),
    (r'consensus.*engine', 'Consensus mechanisms'),
    (r'optimization.*performance', 'Performance optimizations'),
    
    # Business logic
    (r'pricing|billing|payment', 'Business/pricing logic'),
    (r'customer.*management', 'Customer management'),
    (r'analytics.*tracking', 'Analytics/tracking code'),
    (r'compliance.*report', 'Compliance features'),
    (r'enterprise.*feature', 'Enterprise features'),
    
    # Advanced features
    (r'multi.*ai.*consensus', 'Multi-AI consensus'),
    (r'industry.*specific', 'Industry-specific logic'),
    (r'advanced.*detection', 'Advanced detection algorithms'),
    (r'cache.*strategy', 'Caching strategies'),
    (r'performance.*critical', 'Performance critical code'),
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
]

# Files/directories to skip
SKIP_PATTERNS = [
<<<<<<< HEAD
    "test_",
    "__pycache__",
    ".git",
    "docs/",
    "examples/",
    "*.md",
    "requirements.txt",
]


=======
    'test_',
    '__pycache__',
    '.git',
    'docs/',
    'examples/',
    '*.md',
    'requirements.txt',
]

>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
def should_skip(filepath: str) -> bool:
    """Check if file should be skipped"""
    for pattern in SKIP_PATTERNS:
        if pattern in filepath:
            return True
    return False

<<<<<<< HEAD

def analyze_file(filepath: Path) -> List[Tuple[int, str, str]]:
    """Analyze a file for proprietary patterns"""
    findings = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

=======
def analyze_file(filepath: Path) -> List[Tuple[int, str, str]]:
    """Analyze a file for proprietary patterns"""
    findings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            for pattern, description in PROPRIETARY_PATTERNS:
                if re.search(pattern, line_lower):
                    findings.append((line_num, description, line.strip()))
<<<<<<< HEAD

    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    return findings


def analyze_codebase(root_dir: str) -> Dict[str, List[Tuple[int, str, str]]]:
    """Analyze entire codebase for proprietary code"""
    results = {}

    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not should_skip(d)]

        for file in files:
            if file.endswith(".py") and not should_skip(file):
                filepath = Path(root) / file
                findings = analyze_file(filepath)

                if findings:
                    relative_path = str(filepath.relative_to(root_dir))
                    results[relative_path] = findings

    return results


=======
    
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    
    return findings

def analyze_codebase(root_dir: str) -> Dict[str, List[Tuple[int, str, str]]]:
    """Analyze entire codebase for proprietary code"""
    results = {}
    
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not should_skip(d)]
        
        for file in files:
            if file.endswith('.py') and not should_skip(file):
                filepath = Path(root) / file
                findings = analyze_file(filepath)
                
                if findings:
                    relative_path = str(filepath.relative_to(root_dir))
                    results[relative_path] = findings
    
    return results

>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
def generate_report(results: Dict[str, List[Tuple[int, str, str]]]) -> str:
    """Generate a report of findings"""
    report = ["# Proprietary Code Analysis Report\n"]
    report.append(f"Found {len(results)} files with potentially proprietary code\n")
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Summary by category
    category_count = {}
    for file_findings in results.values():
        for _, category, _ in file_findings:
            category_count[category] = category_count.get(category, 0) + 1
<<<<<<< HEAD

    report.append("\n## Summary by Category\n")
    for category, count in sorted(
        category_count.items(), key=lambda x: x[1], reverse=True
    ):
        report.append(f"- {category}: {count} occurrences")

    # Detailed findings
    report.append("\n## Detailed Findings\n")

    # Sort files by number of findings
    sorted_results = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)

    for filepath, findings in sorted_results:
        report.append(f"\n### {filepath} ({len(findings)} findings)\n")

=======
    
    report.append("\n## Summary by Category\n")
    for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        report.append(f"- {category}: {count} occurrences")
    
    # Detailed findings
    report.append("\n## Detailed Findings\n")
    
    # Sort files by number of findings
    sorted_results = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)
    
    for filepath, findings in sorted_results:
        report.append(f"\n### {filepath} ({len(findings)} findings)\n")
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Group by category
        by_category = {}
        for line_num, category, code in findings:
            if category not in by_category:
                by_category[category] = []
            by_category[category].append((line_num, code))
<<<<<<< HEAD

        for category, items in by_category.items():
            report.append(f"\n**{category}:**")
            for line_num, code in items[:3]:  # Show max 3 examples per category
                report.append(
                    f"- Line {line_num}: `{code[:80]}{'...' if len(code) > 80 else ''}`"
                )
            if len(items) > 3:
                report.append(f"- ... and {len(items) - 3} more")

    # Recommendations
    report.append("\n## Recommendations\n")
    report.append("### High Priority (Move to Private):")

    high_priority_files = []
    for filepath, findings in results.items():
        if len(findings) >= 5 or any(
            "Advanced algorithm" in f[1] or "Multi-AI consensus" in f[1]
            for f in findings
        ):
            high_priority_files.append(filepath)

    for filepath in high_priority_files[:10]:
        report.append(f"- {filepath}")

    if len(high_priority_files) > 10:
        report.append(f"- ... and {len(high_priority_files) - 10} more files")

=======
        
        for category, items in by_category.items():
            report.append(f"\n**{category}:**")
            for line_num, code in items[:3]:  # Show max 3 examples per category
                report.append(f"- Line {line_num}: `{code[:80]}{'...' if len(code) > 80 else ''}`")
            if len(items) > 3:
                report.append(f"- ... and {len(items) - 3} more")
    
    # Recommendations
    report.append("\n## Recommendations\n")
    report.append("### High Priority (Move to Private):")
    
    high_priority_files = []
    for filepath, findings in results.items():
        if len(findings) >= 5 or any('Advanced algorithm' in f[1] or 'Multi-AI consensus' in f[1] for f in findings):
            high_priority_files.append(filepath)
    
    for filepath in high_priority_files[:10]:
        report.append(f"- {filepath}")
    
    if len(high_priority_files) > 10:
        report.append(f"- ... and {len(high_priority_files) - 10} more files")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    report.append("\n### Consider Splitting:")
    split_candidates = []
    for filepath, findings in results.items():
        if 2 <= len(findings) < 5:
            split_candidates.append(filepath)
<<<<<<< HEAD

    for filepath in split_candidates[:5]:
        report.append(f"- {filepath}")

    return "\n".join(report)


=======
    
    for filepath in split_candidates[:5]:
        report.append(f"- {filepath}")
    
    return "\n".join(report)

>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
def main():
    """Main function"""
    # Get the source directory
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src"
<<<<<<< HEAD

    print("🔍 Analyzing codebase for proprietary code...")
    print(f"Scanning: {src_dir}")

    # Analyze
    results = analyze_codebase(str(src_dir))

    # Generate report
    report = generate_report(results)

    # Save report
    report_path = project_root / "PROPRIETARY_CODE_ANALYSIS.md"
    with open(report_path, "w") as f:
        f.write(report)

    print("\n✅ Analysis complete!")
    print(f"📄 Report saved to: {report_path}")
    print("\nSummary:")
    print(f"- Files with proprietary code: {len(results)}")
    print(f"- Total findings: {sum(len(findings) for findings in results.values())}")

=======
    
    print("🔍 Analyzing codebase for proprietary code...")
    print(f"Scanning: {src_dir}")
    
    # Analyze
    results = analyze_codebase(str(src_dir))
    
    # Generate report
    report = generate_report(results)
    
    # Save report
    report_path = project_root / "PROPRIETARY_CODE_ANALYSIS.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Analysis complete!")
    print(f"📄 Report saved to: {report_path}")
    print(f"\nSummary:")
    print(f"- Files with proprietary code: {len(results)}")
    print(f"- Total findings: {sum(len(findings) for findings in results.values())}")
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    # Quick recommendations
    print("\n🎯 Quick Recommendations:")
    print("1. Review PROPRIETARY_CODE_ANALYSIS.md for detailed findings")
    print("2. Move high-priority files to private repository")
    print("3. Split files with mixed open/proprietary code")
    print("4. Create interfaces for proprietary implementations")

<<<<<<< HEAD

if __name__ == "__main__":
    main()
=======
if __name__ == "__main__":
    main()
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

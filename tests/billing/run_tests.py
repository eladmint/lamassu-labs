"""
Multi-Chain Billing System Test Runner

Comprehensive test runner for the multi-chain billing system with
support for different test categories, reporting, and CI/CD integration.

Usage:
    python tests/billing/run_tests.py --category unit
    python tests/billing/run_tests.py --category integration
    python tests/billing/run_tests.py --category e2e
    python tests/billing/run_tests.py --all
    python tests/billing/run_tests.py --coverage

Date: June 19, 2025
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class BillingTestRunner:
    """Test runner for multi-chain billing system."""

    def __init__(self):
        self.test_root = Path(__file__).parent.parent
        self.test_categories = {
            "unit": [
                "tests/billing/test_basic_validation.py",
                "tests/billing/test_billing_fixtures.py",
                "tests/billing/test_universal_identity_service.py",
                "tests/billing/test_transaction_processing_service.py",
                "tests/billing/test_integrated_subscription_service.py",
                "tests/billing/test_ton_integration_service.py",
                "tests/billing/test_icp_integration_service.py",
                "tests/billing/test_cardano_integration_service.py",
            ],
            "integration": [
                "tests/integration/test_ziggurat_intelligence_integration.py",
                "tests/integration/test_agent_forge_ziggurat_integration.py",
            ],
            "e2e": ["tests/e2e/test_multi_chain_billing_workflows.py"],
            "performance": ["tests/billing/test_billing_performance.py"],
            "basic": ["tests/billing/test_basic_validation.py"],
        }

        self.pytest_config = {
            "unit": ["-v", "--tb=short", "--durations=10", "--asyncio-mode=auto"],
            "integration": ["-v", "--tb=short", "--asyncio-mode=auto"],
            "e2e": ["-v", "--tb=short", "--asyncio-mode=auto", "--timeout=300"],
            "performance": ["-v", "--tb=short", "--benchmark-only"],
            "basic": ["-v", "--tb=short", "--asyncio-mode=auto"],
        }

    def run_category_tests(
        self, category: str, coverage: bool = False
    ) -> Tuple[int, Dict]:
        """Run tests for a specific category."""
        print(f"\n🧪 Running {category.upper()} tests for Multi-Chain Billing System")
        print("=" * 60)

        if category not in self.test_categories:
            print(f"❌ Unknown test category: {category}")
            return 1, {}

        test_files = self.test_categories[category]
        pytest_args = self.pytest_config[category].copy()

        # Add coverage if requested
        if coverage:
            pytest_args.extend(
                [
                    "--cov=src/core/billing",
                    "--cov-report=html:tests/billing/coverage_html",
                    "--cov-report=json:tests/billing/coverage.json",
                    "--cov-report=term-missing",
                ]
            )

        # Build pytest command
        cmd = ["python", "-m", "pytest"] + pytest_args + test_files

        print(f"📋 Test files: {len(test_files)}")
        for test_file in test_files:
            if os.path.exists(self.test_root / test_file):
                print(f"  ✅ {test_file}")
            else:
                print(f"  ❌ {test_file} (not found)")

        print(f"\n🚀 Command: {' '.join(cmd)}")
        print("-" * 60)

        # Run tests
        start_time = datetime.now()
        try:
            result = subprocess.run(
                cmd, cwd=self.test_root, capture_output=False, text=True
            )
            return_code = result.returncode
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return 1, {}

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Parse results
        test_results = {
            "category": category,
            "return_code": return_code,
            "duration_seconds": duration,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "test_files": test_files,
            "success": return_code == 0,
        }

        # Print results summary
        print("\n" + "=" * 60)
        if return_code == 0:
            print(f"✅ {category.upper()} tests PASSED")
        else:
            print(f"❌ {category.upper()} tests FAILED")

        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📁 Files tested: {len(test_files)}")

        if coverage and return_code == 0:
            self.display_coverage_summary()

        return return_code, test_results

    def run_all_tests(self, coverage: bool = False) -> Tuple[int, Dict]:
        """Run all test categories."""
        print("\n🎯 Running ALL Multi-Chain Billing System Tests")
        print("=" * 60)

        all_results = {
            "overall_start": datetime.now().isoformat(),
            "categories": {},
            "summary": {},
        }

        overall_success = True
        total_duration = 0

        for category in ["unit", "integration", "e2e"]:
            return_code, results = self.run_category_tests(category, coverage=coverage)
            all_results["categories"][category] = results

            if return_code != 0:
                overall_success = False

            total_duration += results.get("duration_seconds", 0)

        # Overall summary
        all_results["overall_end"] = datetime.now().isoformat()
        all_results["summary"] = {
            "success": overall_success,
            "total_duration_seconds": total_duration,
            "categories_passed": len(
                [
                    r
                    for r in all_results["categories"].values()
                    if r.get("success", False)
                ]
            ),
            "categories_failed": len(
                [
                    r
                    for r in all_results["categories"].values()
                    if not r.get("success", True)
                ]
            ),
            "total_categories": len(all_results["categories"]),
        }

        # Print overall summary
        print("\n" + "🎯" * 30)
        print("OVERALL TEST SUMMARY")
        print("🎯" * 30)

        for category, results in all_results["categories"].items():
            status = "✅ PASSED" if results.get("success", False) else "❌ FAILED"
            duration = results.get("duration_seconds", 0)
            print(f"{category.upper():<12} {status:<10} ({duration:.1f}s)")

        print("-" * 40)
        print(
            f"{'TOTAL':<12} {'✅ PASSED' if overall_success else '❌ FAILED':<10} ({total_duration:.1f}s)"
        )

        # Save results to file
        results_file = self.test_root / "tests" / "billing" / "test_results.json"
        with open(results_file, "w") as f:
            json.dump(all_results, f, indent=2)

        print(f"\n📊 Detailed results saved to: {results_file}")

        return 0 if overall_success else 1, all_results

    def display_coverage_summary(self):
        """Display test coverage summary."""
        coverage_file = self.test_root / "tests" / "billing" / "coverage.json"

        if not coverage_file.exists():
            print("⚠️  Coverage data not found")
            return

        try:
            with open(coverage_file) as f:
                coverage_data = json.load(f)

            print("\n📊 COVERAGE SUMMARY")
            print("-" * 40)

            totals = coverage_data.get("totals", {})
            covered_lines = totals.get("covered_lines", 0)
            num_statements = totals.get("num_statements", 0)
            percent_covered = totals.get("percent_covered", 0)

            print(f"Lines covered: {covered_lines}/{num_statements}")
            print(f"Coverage: {percent_covered:.1f}%")

            # Coverage by file
            files = coverage_data.get("files", {})
            print("\nCoverage by module:")
            for file_path, file_data in files.items():
                if "src/core/billing" in file_path:
                    file_coverage = file_data["summary"]["percent_covered"]
                    module_name = Path(file_path).stem
                    print(f"  {module_name:<30} {file_coverage:>6.1f}%")

            print("\n📋 Full coverage report: tests/billing/coverage_html/index.html")

        except Exception as e:
            print(f"⚠️  Error reading coverage data: {e}")

    def run_specific_tests(
        self, test_patterns: List[str], coverage: bool = False
    ) -> Tuple[int, Dict]:
        """Run specific test files or patterns."""
        print(f"\n🎯 Running specific tests: {', '.join(test_patterns)}")
        print("=" * 60)

        pytest_args = ["-v", "--tb=short", "--asyncio-mode=auto"]

        if coverage:
            pytest_args.extend(["--cov=src/core/billing", "--cov-report=term-missing"])

        cmd = ["python", "-m", "pytest"] + pytest_args + test_patterns

        print(f"🚀 Command: {' '.join(cmd)}")
        print("-" * 60)

        start_time = datetime.now()
        try:
            result = subprocess.run(
                cmd, cwd=self.test_root, capture_output=False, text=True
            )
            return_code = result.returncode
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return 1, {}

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        test_results = {
            "patterns": test_patterns,
            "return_code": return_code,
            "duration_seconds": duration,
            "success": return_code == 0,
        }

        print(
            f"\n{'✅ PASSED' if return_code == 0 else '❌ FAILED'} in {duration:.2f}s"
        )

        return return_code, test_results

    def validate_environment(self) -> bool:
        """Validate test environment setup."""
        print("🔍 Validating test environment...")

        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            print(
                f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}"
            )
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}")

        # Check required packages
        required_packages = [
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "pytest-benchmark",
            "pytest-timeout",
        ]

        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package}")

        if missing_packages:
            print(
                f"\n⚠️  Install missing packages: pip install {' '.join(missing_packages)}"
            )
            return False

        # Check test files exist
        missing_files = []
        for category, files in self.test_categories.items():
            for file_path in files:
                if not (self.test_root / file_path).exists():
                    missing_files.append(file_path)

        if missing_files:
            print("\n⚠️  Missing test files:")
            for file_path in missing_files:
                print(f"  ❌ {file_path}")
            return False

        print("\n✅ Environment validation passed!")
        return True


def main():
    """Main test runner entry point."""
    parser = argparse.ArgumentParser(
        description="Multi-Chain Billing System Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tests/billing/run_tests.py --category unit
  python tests/billing/run_tests.py --category integration --coverage
  python tests/billing/run_tests.py --all
  python tests/billing/run_tests.py --specific tests/billing/test_ton_integration_service.py
  python tests/billing/run_tests.py --validate
        """,
    )

    parser.add_argument(
        "--category",
        choices=["unit", "integration", "e2e", "performance", "basic"],
        help="Run tests for specific category",
    )

    parser.add_argument("--all", action="store_true", help="Run all test categories")

    parser.add_argument(
        "--specific", nargs="+", help="Run specific test files or patterns"
    )

    parser.add_argument(
        "--coverage", action="store_true", help="Generate coverage report"
    )

    parser.add_argument(
        "--validate", action="store_true", help="Validate test environment only"
    )

    args = parser.parse_args()

    runner = BillingTestRunner()

    # Validate environment
    if args.validate:
        if runner.validate_environment():
            sys.exit(0)
        else:
            sys.exit(1)

    if not runner.validate_environment():
        print("❌ Environment validation failed. Use --validate for details.")
        sys.exit(1)

    # Run tests based on arguments
    if args.all:
        return_code, _ = runner.run_all_tests(coverage=args.coverage)
    elif args.category:
        return_code, _ = runner.run_category_tests(
            args.category, coverage=args.coverage
        )
    elif args.specific:
        return_code, _ = runner.run_specific_tests(
            args.specific, coverage=args.coverage
        )
    else:
        print("❌ No test category specified. Use --help for options.")
        return_code = 1

    sys.exit(return_code)


if __name__ == "__main__":
    main()

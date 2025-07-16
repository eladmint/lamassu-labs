#!/usr/bin/env python3
"""
LangChain Integration Test Runner

Comprehensive test runner for TrustWrapper LangChain integration.
Follows ADR-005 testing strategy.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


class TestRunner:
    """Test runner for LangChain integration tests"""

    def __init__(self, test_dir: Path):
        self.test_dir = test_dir
        self.results: Dict[str, Any] = {}

    def run_unit_tests(self, verbose: bool = True) -> bool:
        """Run unit tests"""
        print("🧪 Running LangChain Unit Tests...")
        print("=" * 50)

        unit_dir = self.test_dir / "unit" / "langchain"
        if not unit_dir.exists():
            print(f"❌ Unit test directory not found: {unit_dir}")
            return False

        cmd = [
            "python",
            "-m",
            "pytest",
            str(unit_dir),
            "-m",
            "unit or not slow",
            "--tb=short",
        ]

        if verbose:
            cmd.append("-v")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)

            success = result.returncode == 0
            self.results["unit_tests"] = {
                "success": success,
                "returncode": result.returncode,
                "output": result.stdout,
            }

            if success:
                print("✅ Unit tests passed!")
            else:
                print("❌ Unit tests failed!")

            return success

        except Exception as e:
            print(f"❌ Error running unit tests: {e}")
            self.results["unit_tests"] = {"success": False, "error": str(e)}
            return False

    def run_integration_tests(self, verbose: bool = True) -> bool:
        """Run integration tests"""
        print("\n🔗 Running LangChain Integration Tests...")
        print("=" * 50)

        integration_dir = self.test_dir / "integration" / "langchain"
        if not integration_dir.exists():
            print(f"❌ Integration test directory not found: {integration_dir}")
            return False

        cmd = [
            "python",
            "-m",
            "pytest",
            str(integration_dir),
            "-m",
            "integration",
            "--tb=short",
        ]

        if verbose:
            cmd.append("-v")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)

            success = result.returncode == 0
            self.results["integration_tests"] = {
                "success": success,
                "returncode": result.returncode,
                "output": result.stdout,
            }

            if success:
                print("✅ Integration tests passed!")
            else:
                print("❌ Integration tests failed!")

            return success

        except Exception as e:
            print(f"❌ Error running integration tests: {e}")
            self.results["integration_tests"] = {"success": False, "error": str(e)}
            return False

    def run_performance_tests(self, verbose: bool = True) -> bool:
        """Run performance tests"""
        print("\n⚡ Running LangChain Performance Tests...")
        print("=" * 50)

        performance_dir = self.test_dir / "performance" / "langchain"
        if not performance_dir.exists():
            print(f"❌ Performance test directory not found: {performance_dir}")
            return False

        cmd = [
            "python",
            "-m",
            "pytest",
            str(performance_dir),
            "-m",
            "performance",
            "--tb=short",
        ]

        if verbose:
            cmd.append("-v")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)

            success = result.returncode == 0
            self.results["performance_tests"] = {
                "success": success,
                "returncode": result.returncode,
                "output": result.stdout,
            }

            if success:
                print("✅ Performance tests passed!")
            else:
                print("❌ Performance tests failed!")

            return success

        except Exception as e:
            print(f"❌ Error running performance tests: {e}")
            self.results["performance_tests"] = {"success": False, "error": str(e)}
            return False

    def run_quick_smoke_tests(self) -> bool:
        """Run quick smoke tests for basic functionality"""
        print("\n💨 Running Quick Smoke Tests...")
        print("=" * 50)

        # Test imports
        try:
            # Add both src directory and root directory to path
            root_dir = self.test_dir.parent.parent
            src_path = str(root_dir / "src")

            for path in [str(root_dir), src_path]:
                if path not in sys.path:
                    sys.path.insert(0, path)

            from src.integrations.langchain import (
                TrustWrapperCallback,
                TrustWrapperConfig,
            )

            print("✅ Import test passed")

            # Test basic initialization
            config = TrustWrapperConfig()
            callback = TrustWrapperCallback(config)

            print("✅ Initialization test passed")

            # Test basic functionality
            stats = callback.get_statistics()
            assert isinstance(stats, dict)

            print("✅ Basic functionality test passed")

            self.results["smoke_tests"] = {"success": True}
            return True

        except Exception as e:
            print(f"❌ Smoke tests failed: {e}")
            self.results["smoke_tests"] = {"success": False, "error": str(e)}
            return False

    def check_dependencies(self) -> bool:
        """Check that required dependencies are available"""
        print("🔍 Checking Dependencies...")
        print("=" * 50)

        required_packages = ["pytest", "asyncio", "pathlib"]

        missing_packages = []

        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package}")
            except ImportError:
                print(f"❌ {package} (missing)")
                missing_packages.append(package)

        # Optional packages
        optional_packages = {
            "langchain": "LangChain integration testing",
            "psutil": "Memory usage testing",
        }

        for package, description in optional_packages.items():
            try:
                __import__(package)
                print(f"✅ {package} ({description})")
            except ImportError:
                print(f"⚠️  {package} (optional, {description})")

        if missing_packages:
            print(f"\n❌ Missing required packages: {', '.join(missing_packages)}")
            print("Install with: pip install " + " ".join(missing_packages))
            return False

        print("\n✅ All required dependencies available")
        return True

    def generate_report(self) -> None:
        """Generate test execution report"""
        print("\n" + "=" * 80)
        print("📊 LangChain Integration Test Report")
        print("=" * 80)

        total_suites = len(self.results)
        passed_suites = sum(
            1 for result in self.results.values() if result.get("success", False)
        )

        print("\nTest Suite Summary:")
        print(f"  Total test suites: {total_suites}")
        print(f"  Passed: {passed_suites}")
        print(f"  Failed: {total_suites - passed_suites}")

        print("\nDetailed Results:")
        for suite_name, result in self.results.items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            print(f"  {suite_name}: {status}")

            if not result.get("success", False) and "error" in result:
                print(f"    Error: {result['error']}")

        overall_success = all(
            result.get("success", False) for result in self.results.values()
        )

        if overall_success:
            print("\n🎉 All test suites passed!")
            print("✅ LangChain integration is ready for production")
        else:
            print("\n❌ Some test suites failed")
            print("🔧 Please review and fix failing tests before deployment")

        return overall_success


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description="LangChain Integration Test Runner")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument(
        "--integration", action="store_true", help="Run integration tests only"
    )
    parser.add_argument(
        "--performance", action="store_true", help="Run performance tests only"
    )
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests (default)")
    parser.add_argument("--quiet", action="store_true", help="Reduce output verbosity")
    parser.add_argument(
        "--skip-deps", action="store_true", help="Skip dependency check"
    )

    args = parser.parse_args()

    # Default to running all tests if no specific test type is specified
    if not any([args.unit, args.integration, args.performance, args.smoke]):
        args.all = True

    verbose = not args.quiet

    # Setup test directory
    test_dir = Path(__file__).parent
    runner = TestRunner(test_dir)

    print("🚀 TrustWrapper LangChain Integration Test Runner")
    print("=" * 80)

    # Check dependencies unless skipped
    if not args.skip_deps:
        if not runner.check_dependencies():
            print("\n❌ Dependency check failed. Use --skip-deps to continue anyway.")
            return 1

    success = True

    # Run smoke tests first if running all tests
    if args.all or args.smoke:
        success &= runner.run_quick_smoke_tests()

    # Run specific test suites
    if args.all or args.unit:
        success &= runner.run_unit_tests(verbose)

    if args.all or args.integration:
        success &= runner.run_integration_tests(verbose)

    if args.all or args.performance:
        success &= runner.run_performance_tests(verbose)

    # Generate final report
    overall_success = runner.generate_report()

    return 0 if overall_success else 1


if __name__ == "__main__":
    sys.exit(main())

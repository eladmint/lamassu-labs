#!/usr/bin/env python3
"""
Automated test runner for TrustWrapper
Comprehensive testing with reporting and coverage
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestRunner:
    """Automated test runner with reporting"""

    def __init__(self, verbose: bool = False, coverage: bool = False):
        self.verbose = verbose
        self.coverage = coverage
        self.test_dir = Path(__file__).parent
        self.project_root = self.test_dir.parent.parent
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {},
        }

    def run_all_tests(self) -> bool:
        """Run all test suites"""
        print("\n🧪 TRUSTWRAPPER TEST SUITE")
        print("=" * 50)

        test_suites = [
            {
                "name": "Core TrustWrapper Tests",
                "file": "unit/test_trust_wrapper.py",
                "description": "Core wrapper functionality and proof generation",
            },
            {
                "name": "Leo Integration Tests",
                "file": "integration/test_leo_integration.py",
                "description": "Aleo blockchain and Leo contract integration",
            },
            {
                "name": "XAI Integration Tests",
                "file": "integration/test_xai_integration.py",
                "description": "XAI-enhanced TrustWrapper integration",
            },
            {
                "name": "Demo Tests",
                "file": "demos/test_demos.py",
                "description": "Demo functionality validation",
            },
            {
                "name": "Performance Tests",
                "file": "performance/test_performance.py",
                "description": "Performance benchmarks and scalability",
            },
        ]

        all_passed = True

        for suite in test_suites:
            if (self.test_dir / suite["file"]).exists():
                passed = self.run_test_suite(suite)
                all_passed = all_passed and passed
            else:
                print(f"\n⚠️  Skipping {suite['name']} - {suite['file']} not found")

        self.generate_report()
        return all_passed

    def run_test_suite(self, suite: Dict[str, str]) -> bool:
        """Run a single test suite"""
        print(f"\n📋 Running: {suite['name']}")
        print(f"   {suite['description']}")
        print("-" * 50)

        start_time = time.time()

        # Build pytest command
        cmd = ["python", "-m", "pytest", str(self.test_dir / suite["file"])]

        if self.verbose:
            cmd.extend(["-v", "-s"])
        else:
            cmd.append("-q")

        if self.coverage:
            cmd.extend(
                [
                    "--cov=../src",
                    "--cov-report=term-missing",
                    "--cov-report=html:coverage_html",
                ]
            )

        # Add JSON report
        report_file = self.test_dir / f"report_{suite['file']}.json"
        cmd.extend(["--json-report", f"--json-report-file={report_file}"])

        # Run tests
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration = time.time() - start_time

            # Parse results
            passed = result.returncode == 0

            # Extract test counts from output
            output_lines = result.stdout.split("\n")
            test_summary = self.parse_pytest_output(output_lines)

            # Store results
            self.results["tests"][suite["name"]] = {
                "passed": passed,
                "duration": duration,
                "file": suite["file"],
                "summary": test_summary,
                "output": result.stdout if self.verbose else None,
            }

            # Print summary
            if passed:
                print(f"✅ PASSED in {duration:.2f}s")
                if test_summary:
                    print(f"   {test_summary}")
            else:
                print(f"❌ FAILED in {duration:.2f}s")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")

            return passed

        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            self.results["tests"][suite["name"]] = {"passed": False, "error": str(e)}
            return False

    def parse_pytest_output(self, lines: List[str]) -> str:
        """Parse pytest output for test summary"""
        for line in lines:
            if "passed" in line and (
                "failed" in line or "error" in line or "skipped" in line
            ):
                return line.strip()
            elif line.startswith("=") and "passed" in line:
                return line.strip().replace("=", "").strip()
        return ""

    def run_specific_tests(self, test_pattern: str) -> bool:
        """Run specific tests matching pattern"""
        print(f"\n🔍 Running tests matching: {test_pattern}")

        cmd = ["python", "-m", "pytest", "-k", test_pattern]

        if self.verbose:
            cmd.extend(["-v", "-s"])

        result = subprocess.run(cmd, capture_output=True, text=True)

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        return result.returncode == 0

    def run_coverage_analysis(self):
        """Run full coverage analysis"""
        print("\n📊 Running Coverage Analysis")
        print("=" * 50)

        cmd = [
            "python",
            "-m",
            "pytest",
            str(self.test_dir),
            "--cov=../src",
            "--cov-report=term-missing",
            "--cov-report=html:coverage_html",
            "--cov-report=json:coverage.json",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse coverage results
        if (self.test_dir.parent / "coverage.json").exists():
            with open(self.test_dir.parent / "coverage.json") as f:
                coverage_data = json.load(f)

            total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
            print(f"\n📈 Total Coverage: {total_coverage:.1f}%")

            # Show file-level coverage
            print("\nFile Coverage:")
            for file, data in coverage_data.get("files", {}).items():
                if "src" in file:
                    percent = data["summary"]["percent_covered"]
                    print(f"  {file}: {percent:.1f}%")

    def generate_report(self):
        """Generate test report"""
        # Calculate summary
        total_suites = len(self.results["tests"])
        passed_suites = sum(
            1 for t in self.results["tests"].values() if t.get("passed", False)
        )
        total_duration = sum(
            t.get("duration", 0) for t in self.results["tests"].values()
        )

        self.results["summary"] = {
            "total_suites": total_suites,
            "passed_suites": passed_suites,
            "failed_suites": total_suites - passed_suites,
            "total_duration": total_duration,
            "success_rate": (
                (passed_suites / total_suites * 100) if total_suites > 0 else 0
            ),
        }

        # Save JSON report
        report_path = self.test_dir / f"test_report_{int(time.time())}.json"
        with open(report_path, "w") as f:
            json.dump(self.results, f, indent=2)

        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        print(f"Total Test Suites: {total_suites}")
        print(f"Passed: {passed_suites} ✅")
        print(f"Failed: {total_suites - passed_suites} ❌")
        print(f"Success Rate: {self.results['summary']['success_rate']:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        print(f"\nDetailed report saved to: {report_path}")

        if self.coverage:
            print("Coverage report: coverage_html/index.html")


class ContinuousTestRunner:
    """Continuous testing with file watching"""

    def __init__(self, runner: TestRunner):
        self.runner = runner
        self.last_run = {}

    def watch_and_test(self, interval: int = 5):
        """Watch for file changes and run tests"""
        print("\n👁️  Continuous Testing Mode")
        print("Watching for changes... (Ctrl+C to stop)")

        try:
            while True:
                # Check for modified files
                modified = self.check_modifications()

                if modified:
                    print(f"\n🔄 Detected changes in: {', '.join(modified)}")
                    self.runner.run_all_tests()

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n👋 Stopping continuous testing")

    def check_modifications(self) -> List[str]:
        """Check for modified files"""
        modified = []

        # Check source files
        for file in Path(self.runner.project_root / "src").rglob("*.py"):
            mtime = file.stat().st_mtime
            if file.name not in self.last_run or mtime > self.last_run[file.name]:
                modified.append(file.name)
                self.last_run[file.name] = mtime

        # Check test files
        for file in self.runner.test_dir.glob("*.py"):
            mtime = file.stat().st_mtime
            if file.name not in self.last_run or mtime > self.last_run[file.name]:
                modified.append(file.name)
                self.last_run[file.name] = mtime

        return modified


def create_missing_tests():
    """Create placeholder test files if missing"""
    test_dir = Path(__file__).parent

    missing_tests = {
        "test_demos.py": """#!/usr/bin/env python3
\"\"\"Test suite for TrustWrapper demos\"\"\"

import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

class TestDemos:
    def test_demo_imports(self):
        \"\"\"Test that demos can be imported\"\"\"
        from demo import demo_event_wrapper
        from demo import demo_scraper_wrapper
        from demo import demo_treasury_wrapper
        assert True

    def test_demo_execution(self):
        \"\"\"Test basic demo execution\"\"\"
        # Add demo execution tests here
        assert True
""",
        "test_performance.py": """#!/usr/bin/env python3
\"\"\"Performance tests for TrustWrapper\"\"\"

import pytest
import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.trust_wrapper import ZKTrustWrapper

class TestPerformance:
    def test_wrapper_overhead_minimal(self):
        \"\"\"Test that wrapper adds minimal overhead\"\"\"
        class FastAgent:
            def execute(self):
                return "fast"

        agent = FastAgent()
        wrapper = ZKTrustWrapper(agent)

        # Measure overhead
        start = time.time()
        for _ in range(1000):
            wrapper.verified_execute()
        duration = time.time() - start

        # Should complete 1000 executions quickly
        assert duration < 1.0  # Less than 1 second

    def test_proof_generation_speed(self):
        \"\"\"Test proof generation performance\"\"\"
        class TestAgent:
            def execute(self):
                return {"data": "test" * 100}

        wrapper = ZKTrustWrapper(TestAgent())

        times = []
        for _ in range(100):
            start = time.time()
            result = wrapper.verified_execute()
            times.append(time.time() - start)

        avg_time = sum(times) / len(times)
        assert avg_time < 0.01  # Less than 10ms average
""",
    }

    for filename, content in missing_tests.items():
        filepath = test_dir / filename
        if not filepath.exists():
            filepath.write_text(content)
            print(f"Created missing test file: {filename}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="TrustWrapper Test Runner")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "-c", "--coverage", action="store_true", help="Run with coverage"
    )
    parser.add_argument(
        "-w", "--watch", action="store_true", help="Continuous testing mode"
    )
    parser.add_argument("-k", "--keyword", help="Run specific tests matching keyword")
    parser.add_argument(
        "--create-missing", action="store_true", help="Create missing test files"
    )

    args = parser.parse_args()

    if args.create_missing:
        create_missing_tests()
        return

    runner = TestRunner(verbose=args.verbose, coverage=args.coverage)

    if args.keyword:
        success = runner.run_specific_tests(args.keyword)
    elif args.watch:
        continuous = ContinuousTestRunner(runner)
        continuous.watch_and_test()
        success = True
    else:
        success = runner.run_all_tests()
        if args.coverage:
            runner.run_coverage_analysis()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

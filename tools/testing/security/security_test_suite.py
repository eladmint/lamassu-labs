#!/usr/bin/env python3

"""
TrustWrapper v3.0 Security Testing Suite
Comprehensive security validation and penetration testing
Universal Multi-Chain AI Verification Platform
"""

import argparse
import asyncio
import json
import logging
import ssl
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp
import certifi

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class SecurityTestConfig:
    """Security test configuration"""

    base_url: str = "https://api.trustwrapper.com"
    api_key: Optional[str] = None
    timeout: int = 30
    verify_ssl: bool = True
    test_auth: bool = True
    test_injection: bool = True
    test_brute_force: bool = True
    test_dos: bool = False  # Disabled by default for production


@dataclass
class SecurityTestResult:
    """Individual security test result"""

    test_name: str
    category: str
    severity: str  # "low", "medium", "high", "critical"
    status: str  # "pass", "fail", "warning"
    description: str
    details: Optional[str] = None
    remediation: Optional[str] = None
    timestamp: float = 0


class TrustWrapperSecurityTester:
    """Comprehensive security testing suite"""

    def __init__(self, config: SecurityTestConfig):
        self.config = config
        self.results: List[SecurityTestResult] = []
        self.session: Optional[aiohttp.ClientSession] = None

        # Common payloads for injection testing
        self.sql_injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "1' UNION SELECT * FROM information_schema.tables--",
            "admin'--",
            "' OR 1=1#",
        ]

        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "'\"><script>alert('XSS')</script>",
            "<svg onload=alert('XSS')>",
        ]

        self.command_injection_payloads = [
            "; ls -la",
            "| cat /etc/passwd",
            "`whoami`",
            "$(id)",
            "&& echo vulnerable",
        ]

    async def create_session(self) -> aiohttp.ClientSession:
        """Create secure HTTP session"""
        # SSL context
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        connector = aiohttp.TCPConnector(
            ssl=ssl_context if self.config.verify_ssl else False,
            limit=100,
            limit_per_host=50,
            ttl_dns_cache=300,
        )

        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        headers = {
            "User-Agent": "TrustWrapper-SecurityTest/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        return aiohttp.ClientSession(
            connector=connector, timeout=timeout, headers=headers
        )

    def add_result(
        self,
        test_name: str,
        category: str,
        severity: str,
        status: str,
        description: str,
        details: str = None,
        remediation: str = None,
    ):
        """Add a test result"""
        result = SecurityTestResult(
            test_name=test_name,
            category=category,
            severity=severity,
            status=status,
            description=description,
            details=details,
            remediation=remediation,
            timestamp=time.time(),
        )
        self.results.append(result)

        # Log result
        status_icon = "✅" if status == "pass" else "⚠️" if status == "warning" else "❌"
        logger.info(f"{status_icon} {test_name}: {status.upper()}")

    async def test_ssl_configuration(self):
        """Test SSL/TLS configuration"""
        logger.info("Testing SSL/TLS configuration...")

        try:
            # Test SSL connection
            url = self.config.base_url.replace("http://", "https://")
            async with self.session.get(f"{url}/health") as response:
                if response.status == 200:
                    self.add_result(
                        "SSL Connection",
                        "Infrastructure",
                        "high",
                        "pass",
                        "SSL/TLS connection successful",
                    )
                else:
                    self.add_result(
                        "SSL Connection",
                        "Infrastructure",
                        "high",
                        "fail",
                        f"SSL connection failed with status {response.status}",
                    )
        except aiohttp.ClientConnectorSSLError as e:
            self.add_result(
                "SSL Connection",
                "Infrastructure",
                "critical",
                "fail",
                "SSL/TLS connection failed",
                str(e),
                "Ensure valid SSL certificate is installed",
            )
        except Exception as e:
            self.add_result(
                "SSL Connection",
                "Infrastructure",
                "medium",
                "warning",
                "SSL test inconclusive",
                str(e),
            )

    async def test_authentication_security(self):
        """Test authentication mechanisms"""
        if not self.config.test_auth:
            return

        logger.info("Testing authentication security...")

        # Test 1: Access without authentication
        try:
            headers = {"Authorization": ""}
            async with self.session.post(
                f"{self.config.base_url}/verify",
                headers=headers,
                json={"test": "unauthorized"},
            ) as response:
                if response.status == 401:
                    self.add_result(
                        "Unauthorized Access Protection",
                        "Authentication",
                        "high",
                        "pass",
                        "API properly rejects unauthorized requests",
                    )
                else:
                    self.add_result(
                        "Unauthorized Access Protection",
                        "Authentication",
                        "critical",
                        "fail",
                        f"API allows unauthorized access (status: {response.status})",
                        remediation="Implement proper authentication checks",
                    )
        except Exception as e:
            self.add_result(
                "Unauthorized Access Protection",
                "Authentication",
                "medium",
                "warning",
                "Authentication test inconclusive",
                str(e),
            )

        # Test 2: Invalid token format
        try:
            headers = {"Authorization": "Bearer invalid_token_format"}
            async with self.session.post(
                f"{self.config.base_url}/verify",
                headers=headers,
                json={"test": "invalid_token"},
            ) as response:
                if response.status in [401, 403]:
                    self.add_result(
                        "Invalid Token Rejection",
                        "Authentication",
                        "medium",
                        "pass",
                        "API properly rejects invalid tokens",
                    )
                else:
                    self.add_result(
                        "Invalid Token Rejection",
                        "Authentication",
                        "high",
                        "fail",
                        f"API accepts invalid tokens (status: {response.status})",
                    )
        except Exception as e:
            logger.warning(f"Invalid token test failed: {e}")

        # Test 3: JWT manipulation (if using JWT)
        if self.config.api_key:
            try:
                # Simple JWT manipulation test
                manipulated_token = self.config.api_key[:-10] + "tampered123"
                headers = {"Authorization": f"Bearer {manipulated_token}"}

                async with self.session.post(
                    f"{self.config.base_url}/verify",
                    headers=headers,
                    json={"test": "jwt_manipulation"},
                ) as response:
                    if response.status in [401, 403]:
                        self.add_result(
                            "JWT Tampering Protection",
                            "Authentication",
                            "high",
                            "pass",
                            "API properly validates JWT integrity",
                        )
                    else:
                        self.add_result(
                            "JWT Tampering Protection",
                            "Authentication",
                            "critical",
                            "fail",
                            "API accepts tampered JWT tokens",
                            remediation="Implement proper JWT signature validation",
                        )
            except Exception as e:
                logger.warning(f"JWT manipulation test failed: {e}")

    async def test_input_validation(self):
        """Test input validation and injection vulnerabilities"""
        if not self.config.test_injection:
            return

        logger.info("Testing input validation...")

        # Test SQL injection on various endpoints
        injection_found = False

        for payload in self.sql_injection_payloads:
            try:
                test_data = {"query": payload, "address": payload, "amount": payload}

                async with self.session.post(
                    f"{self.config.base_url}/verify", json=test_data
                ) as response:
                    response_text = await response.text()

                    # Check for SQL error indicators
                    sql_errors = [
                        "sql syntax",
                        "mysql_fetch",
                        "postgresql error",
                        "ora-01756",
                        "microsoft odbc",
                        "sqlite_master",
                    ]

                    if any(error in response_text.lower() for error in sql_errors):
                        injection_found = True
                        self.add_result(
                            "SQL Injection Vulnerability",
                            "Input Validation",
                            "critical",
                            "fail",
                            f"SQL injection vulnerability detected with payload: {payload}",
                            response_text[:500],
                            "Implement parameterized queries and input sanitization",
                        )
                        break

            except Exception as e:
                logger.debug(f"SQL injection test error: {e}")

        if not injection_found:
            self.add_result(
                "SQL Injection Protection",
                "Input Validation",
                "high",
                "pass",
                "No SQL injection vulnerabilities detected",
            )

        # Test XSS vulnerabilities
        xss_found = False

        for payload in self.xss_payloads:
            try:
                async with self.session.get(
                    f"{self.config.base_url}/oracle/ETH-USD",
                    params={"callback": payload},
                ) as response:
                    response_text = await response.text()

                    if payload in response_text and "script" in response_text.lower():
                        xss_found = True
                        self.add_result(
                            "XSS Vulnerability",
                            "Input Validation",
                            "high",
                            "fail",
                            f"XSS vulnerability detected with payload: {payload}",
                            remediation="Implement output encoding and Content Security Policy",
                        )
                        break

            except Exception as e:
                logger.debug(f"XSS test error: {e}")

        if not xss_found:
            self.add_result(
                "XSS Protection",
                "Input Validation",
                "medium",
                "pass",
                "No XSS vulnerabilities detected",
            )

    async def test_rate_limiting(self):
        """Test rate limiting implementation"""
        logger.info("Testing rate limiting...")

        # Rapid fire requests to test rate limiting
        tasks = []
        for i in range(50):  # Send 50 rapid requests
            task = asyncio.create_task(
                self.session.get(f"{self.config.base_url}/health")
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Count rate limit responses
        rate_limited = sum(
            1 for r in responses if hasattr(r, "status") and r.status == 429
        )

        if rate_limited > 0:
            self.add_result(
                "Rate Limiting",
                "Security Controls",
                "medium",
                "pass",
                f"Rate limiting active - {rate_limited} requests blocked",
            )
        else:
            self.add_result(
                "Rate Limiting",
                "Security Controls",
                "medium",
                "warning",
                "No rate limiting detected",
                remediation="Implement API rate limiting to prevent abuse",
            )

    async def test_security_headers(self):
        """Test security headers"""
        logger.info("Testing security headers...")

        try:
            async with self.session.get(f"{self.config.base_url}/health") as response:
                headers = response.headers

                # Test for important security headers
                security_headers = {
                    "X-Content-Type-Options": "nosniff",
                    "X-Frame-Options": ["DENY", "SAMEORIGIN"],
                    "X-XSS-Protection": "1; mode=block",
                    "Strict-Transport-Security": None,  # Just check presence
                    "Content-Security-Policy": None,
                }

                for header, expected_values in security_headers.items():
                    if header in headers:
                        if (
                            expected_values is None
                            or headers[header] in expected_values
                        ):
                            self.add_result(
                                f"Security Header: {header}",
                                "Security Headers",
                                "low",
                                "pass",
                                f"{header} header present with value: {headers[header]}",
                            )
                        else:
                            self.add_result(
                                f"Security Header: {header}",
                                "Security Headers",
                                "low",
                                "warning",
                                f"{header} present but value may be suboptimal: {headers[header]}",
                            )
                    else:
                        self.add_result(
                            f"Security Header: {header}",
                            "Security Headers",
                            "medium",
                            "fail",
                            f"Missing security header: {header}",
                            remediation=f"Add {header} header to all responses",
                        )

        except Exception as e:
            self.add_result(
                "Security Headers Test",
                "Security Headers",
                "medium",
                "warning",
                "Could not test security headers",
                str(e),
            )

    async def test_cors_configuration(self):
        """Test CORS configuration"""
        logger.info("Testing CORS configuration...")

        try:
            # Test with various origins
            test_origins = ["https://evil.com", "http://localhost", "*", "null"]

            cors_issues = []

            for origin in test_origins:
                headers = {"Origin": origin}
                async with self.session.options(
                    f"{self.config.base_url}/verify", headers=headers
                ) as response:
                    cors_origin = response.headers.get("Access-Control-Allow-Origin")

                    if cors_origin == "*":
                        cors_issues.append("Wildcard CORS origin detected")
                    elif cors_origin == origin and origin in [
                        "https://evil.com",
                        "null",
                    ]:
                        cors_issues.append(f"Suspicious origin allowed: {origin}")

            if cors_issues:
                self.add_result(
                    "CORS Configuration",
                    "Security Controls",
                    "medium",
                    "warning",
                    "CORS configuration may be too permissive",
                    "; ".join(cors_issues),
                    "Review and restrict CORS origins to trusted domains only",
                )
            else:
                self.add_result(
                    "CORS Configuration",
                    "Security Controls",
                    "low",
                    "pass",
                    "CORS configuration appears secure",
                )

        except Exception as e:
            logger.warning(f"CORS test failed: {e}")

    async def test_information_disclosure(self):
        """Test for information disclosure vulnerabilities"""
        logger.info("Testing for information disclosure...")

        # Test error message disclosure
        try:
            # Send malformed request to trigger error
            async with self.session.post(
                f"{self.config.base_url}/verify",
                json={"malformed": "<<>>INVALID_JSON<<>>"},
            ) as response:
                error_text = await response.text()

                # Check for sensitive information in error messages
                sensitive_patterns = [
                    "/home/",
                    "/var/",
                    "stack trace",
                    "database error",
                    "internal server error",
                    "python",
                    "traceback",
                ]

                disclosed_info = [
                    pattern
                    for pattern in sensitive_patterns
                    if pattern in error_text.lower()
                ]

                if disclosed_info:
                    self.add_result(
                        "Information Disclosure",
                        "Information Security",
                        "medium",
                        "warning",
                        "Error messages may disclose sensitive information",
                        f"Patterns found: {', '.join(disclosed_info)}",
                        "Implement generic error messages for production",
                    )
                else:
                    self.add_result(
                        "Information Disclosure",
                        "Information Security",
                        "low",
                        "pass",
                        "Error messages do not disclose sensitive information",
                    )

        except Exception as e:
            logger.warning(f"Information disclosure test failed: {e}")

    async def run_security_tests(self) -> List[SecurityTestResult]:
        """Run comprehensive security test suite"""
        logger.info("Starting TrustWrapper v3.0 security testing...")

        self.session = await self.create_session()

        try:
            # Infrastructure tests
            await self.test_ssl_configuration()

            # Authentication tests
            await self.test_authentication_security()

            # Input validation tests
            await self.test_input_validation()

            # Security controls tests
            await self.test_rate_limiting()
            await self.test_security_headers()
            await self.test_cors_configuration()

            # Information security tests
            await self.test_information_disclosure()

            return self.results

        finally:
            if self.session:
                await self.session.close()

    def generate_security_report(self, output_file: str = None) -> Dict:
        """Generate comprehensive security report"""
        if not self.results:
            raise ValueError("No test results available")

        # Categorize results
        by_severity = {"critical": [], "high": [], "medium": [], "low": []}
        by_status = {"pass": [], "fail": [], "warning": []}
        by_category = {}

        for result in self.results:
            by_severity[result.severity].append(result)
            by_status[result.status].append(result)

            if result.category not in by_category:
                by_category[result.category] = []
            by_category[result.category].append(result)

        # Calculate security score
        total_tests = len(self.results)
        passed_tests = len(by_status["pass"])
        failed_tests = len(by_status["fail"])

        security_score = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        # Determine overall security posture
        critical_issues = len(by_severity["critical"])
        high_issues = len(by_severity["high"])

        if critical_issues > 0:
            security_posture = "CRITICAL"
        elif high_issues > 2:
            security_posture = "HIGH RISK"
        elif high_issues > 0:
            security_posture = "MEDIUM RISK"
        else:
            security_posture = "LOW RISK"

        report = {
            "test_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "warnings": len(by_status["warning"]),
                "security_score": round(security_score, 1),
                "security_posture": security_posture,
            },
            "severity_breakdown": {
                severity: len(results) for severity, results in by_severity.items()
            },
            "category_breakdown": {
                category: len(results) for category, results in by_category.items()
            },
            "detailed_results": [asdict(result) for result in self.results],
            "recommendations": self._generate_recommendations(),
        }

        # Print summary
        print("\n" + "=" * 80)
        print("TRUSTWRAPPER v3.0 SECURITY TEST RESULTS")
        print("=" * 80)
        print(f"Security Score:    {security_score:.1f}%")
        print(f"Security Posture:  {security_posture}")
        print(f"Total Tests:       {total_tests}")
        print(f"Passed:            {passed_tests}")
        print(f"Failed:            {failed_tests}")
        print(f"Warnings:          {len(by_status['warning'])}")
        print("=" * 80)

        print("SEVERITY BREAKDOWN:")
        for severity, count in by_severity.items():
            if count > 0:
                print(f"  {severity.upper():10} {count:3d} issues")

        print("\nCATEGORY BREAKDOWN:")
        for category, count in by_category.items():
            print(f"  {category:20} {count:3d} tests")

        print("=" * 80)

        # Show critical and high severity issues
        if critical_issues > 0 or high_issues > 0:
            print("HIGH PRIORITY ISSUES:")
            for result in by_severity["critical"] + by_severity["high"]:
                status_icon = "❌" if result.status == "fail" else "⚠️"
                print(f"  {status_icon} {result.test_name}: {result.description}")
            print("=" * 80)

        if output_file:
            with open(output_file, "w") as f:
                json.dump(report, f, indent=2)
            print(f"Detailed security report saved to: {output_file}")

        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations based on test results"""
        recommendations = []

        # Check for critical issues
        critical_issues = [r for r in self.results if r.severity == "critical"]
        if critical_issues:
            recommendations.append(
                "URGENT: Address all critical security vulnerabilities immediately"
            )

        # Check for authentication issues
        auth_failures = [
            r
            for r in self.results
            if r.category == "Authentication" and r.status == "fail"
        ]
        if auth_failures:
            recommendations.append(
                "Strengthen authentication mechanisms and token validation"
            )

        # Check for missing security headers
        header_failures = [
            r
            for r in self.results
            if r.category == "Security Headers" and r.status == "fail"
        ]
        if header_failures:
            recommendations.append(
                "Implement missing security headers to prevent common attacks"
            )

        # Check for input validation issues
        input_failures = [
            r
            for r in self.results
            if r.category == "Input Validation" and r.status == "fail"
        ]
        if input_failures:
            recommendations.append(
                "Implement comprehensive input validation and sanitization"
            )

        return recommendations


async def main():
    """Main function for security testing"""
    parser = argparse.ArgumentParser(
        description="TrustWrapper v3.0 Security Testing Suite"
    )
    parser.add_argument(
        "--url", default="https://api.trustwrapper.com", help="Base URL"
    )
    parser.add_argument("--api-key", help="API key for authentication tests")
    parser.add_argument("--output", help="Output file for detailed results")
    parser.add_argument(
        "--skip-auth", action="store_true", help="Skip authentication tests"
    )
    parser.add_argument(
        "--skip-injection", action="store_true", help="Skip injection tests"
    )

    args = parser.parse_args()

    config = SecurityTestConfig(
        base_url=args.url,
        api_key=args.api_key,
        test_auth=not args.skip_auth,
        test_injection=not args.skip_injection,
    )

    tester = TrustWrapperSecurityTester(config)

    try:
        results = await tester.run_security_tests()
        report = tester.generate_security_report(args.output)

        # Exit with appropriate code based on security posture
        security_posture = report["test_summary"]["security_posture"]
        if security_posture in ["CRITICAL", "HIGH RISK"]:
            exit(1)  # Failure
        else:
            exit(0)  # Success

    except Exception as e:
        logger.error(f"Security testing failed: {e}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())

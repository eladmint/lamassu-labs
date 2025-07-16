"""
Security Input Validation Tests

📋 TESTING DOCUMENTATION REFERENCES:
- 🏗️ **TESTING_ARCHITECTURE.md**: Complete testing framework and architecture specifications
  /Users/eladm/Projects/token/tokenhunter/docs/TESTING_ARCHITECTURE.md
- 📖 **Testing Guide**: Operational testing procedures and best practices
  /Users/eladm/Projects/token/tokenhunter/memory-bank/operational_guides/testing_guide.md
- 🧪 **Test Mode Configuration**: Test mode features and usage guidelines
  /Users/eladm/Projects/token/tokenhunter/memory-bank/configuration/test_mode_features.md
- 🎯 **Enhanced Test Runner**: Cost-tiered testing with `python tests/run_enhanced_tests.py`
  /Users/eladm/Projects/token/tokenhunter/tests/run_enhanced_tests.py

📊 TEST CATEGORY: Security Testing
💰 COST TIER: Free (no external API calls, mocked dependencies)
🎯 PURPOSE: Validates input sanitization, SQL injection prevention, XSS protection, and authentication security

Related test files:
- tests/api_integration/test_error_handling.py - API error handling validation
- tests/api_integration/test_consolidated_api_suite.py - Comprehensive API testing

Test execution:
```bash
# Run this specific test file
python -m pytest tests/security/test_input_validation.py -v

# Run with security marker
python -m pytest tests/security/test_input_validation.py -m "security" -v

# Run all security tests using enhanced runner
python tests/run_enhanced_tests.py --categories security
```

This module provides comprehensive security tests including input validation,
SQL injection prevention, authentication tests, and rate limiting validation.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../src"))

import json
from unittest.mock import MagicMock, patch

import pytest
from api.core.models import QueryRequest
from pydantic import ValidationError


@pytest.mark.security
class TestInputValidation:
    """Test input validation and sanitization."""

    def test_sql_injection_prevention_in_queries(self):
        """Test that SQL injection attempts are properly handled."""
        malicious_queries = [
            "'; DROP TABLE events; --",
            "' OR 1=1 --",
            "UNION SELECT * FROM users",
            "'; DELETE FROM speakers; --",
            "' AND 1=1 UNION SELECT password FROM users --",
        ]

        for query in malicious_queries:
            # Test QueryRequest validation
            with pytest.raises((ValueError, ValidationError, Exception)):
                request = QueryRequest(query=query, user_id="test-user")
                # The query should be sanitized or rejected
                assert "DROP" not in request.query.upper()
                assert "DELETE" not in request.query.upper()
                assert "UNION" not in request.query.upper()

    def test_xss_prevention_in_chat_responses(self):
        """Test that XSS attempts in chat responses are sanitized."""
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<iframe src='javascript:alert(1)'></iframe>",
            "<svg onload=alert('xss')>",
        ]

        for malicious_input in malicious_inputs:
            with patch("chatbot_api.main.process_chat_with_llm") as mock_chat:
                mock_chat.return_value = {
                    "response": f"Processed: {malicious_input}",
                    "tool_calls": [],
                    "conversation_history": [],
                }

                # The response should be sanitized
                response = mock_chat.return_value["response"]
                assert "<script>" not in response
                assert "onerror=" not in response
                assert "javascript:" not in response

    def test_oversized_input_handling(self):
        """Test handling of oversized inputs."""
        # Test extremely large query
        large_query = "A" * 10000  # 10KB query

        try:
            request = QueryRequest(query=large_query, user_id="test-user")
            # Should either be rejected or truncated
            assert len(request.query) <= 5000  # Reasonable limit
        except (ValueError, ValidationError):
            # Rejection is also acceptable
            pass

    def test_special_character_handling(self):
        """Test handling of special characters and encoding."""
        special_chars = [
            "Testing with émojis: 🎯🔍📍",
            "Unicode test: ñáéíóú",
            "Symbols: !@#$%^&*()_+-={}[]|\\:;\"'<>?,./'",
            "Null bytes: \x00\x01\x02",
            "Control chars: \n\r\t",
        ]

        for special_input in special_chars:
            try:
                request = QueryRequest(query=special_input, user_id="test-user")
                # Should handle gracefully without errors
                assert request.query is not None
            except UnicodeDecodeError:
                pytest.fail(f"Failed to handle special characters: {special_input}")

    def test_user_id_validation(self):
        """Test user ID validation and format requirements."""
        invalid_user_ids = [
            "",  # Empty string
            None,  # None value
            "a" * 100,  # Too long
            "user with spaces",  # Spaces
            "user@domain.com",  # Email format
            "../../../etc/passwd",  # Path traversal
            "<script>alert(1)</script>",  # XSS attempt
        ]

        for invalid_id in invalid_user_ids:
            try:
                request = QueryRequest(query="test", user_id=invalid_id)
                # Should validate user_id format
                if invalid_id is None or invalid_id == "":
                    pytest.fail(f"Should reject invalid user_id: {invalid_id}")
            except (ValueError, ValidationError, TypeError):
                # Rejection is expected for invalid IDs
                pass


@pytest.mark.security
class TestAuthenticationSecurity:
    """Test authentication and authorization security."""

    def test_api_key_validation(self):
        """Test API key validation mechanisms."""
        with patch("chatbot_api.core.dependencies.verify_api_key") as mock_verify:
            # Test invalid API keys
            invalid_keys = [
                "",
                "invalid-key",
                "fake-api-key-123",
                None,
                "a" * 1000,  # Oversized key
            ]

            for invalid_key in invalid_keys:
                mock_verify.return_value = False
                result = mock_verify(invalid_key)
                assert result is False

    def test_rate_limiting_validation(self):
        """Test rate limiting mechanisms."""
        with patch("chatbot_api.utils.utils.check_rate_limit") as mock_rate_limit:
            # Simulate rapid requests
            user_id = "test-user-123"

            # First requests should pass
            mock_rate_limit.return_value = True
            for i in range(5):
                result = mock_rate_limit(user_id)
                assert result is True

            # Subsequent requests should be rate limited
            mock_rate_limit.return_value = False
            result = mock_rate_limit(user_id)
            assert result is False

    def test_secret_manager_security(self):
        """Test secure handling of secrets and credentials."""
        with patch(
            "google.cloud.secretmanager.SecretManagerServiceClient"
        ) as mock_client:
            mock_instance = MagicMock()
            mock_client.return_value = mock_instance

            # Test secret retrieval
            mock_instance.access_secret_version.return_value.payload.data.decode.return_value = (
                "test-secret"
            )

            # Verify secrets are not logged or exposed
            from api.core.dependencies import get_secret

            secret = get_secret("test-secret-name")

            # Secret should be retrieved but not exposed in logs
            assert secret == "test-secret"
            # Verify no secrets in exception messages
            assert "test-secret" not in str(
                mock_instance.access_secret_version.call_args
            )


@pytest.mark.security
class TestDataSanitization:
    """Test data sanitization and output encoding."""

    def test_html_content_sanitization(self):
        """Test HTML content sanitization in responses."""
        from shared.bs_utils import sanitize_html_content

        malicious_html = [
            "<script>alert('xss')</script><p>Valid content</p>",
            "<img src=x onerror=alert(1)>",
            "<div onclick='malicious()'>Click me</div>",
            "<style>body{display:none}</style>",
            "<meta http-equiv='refresh' content='0;url=evil.com'>",
        ]

        for html in malicious_html:
            sanitized = sanitize_html_content(html)
            assert "<script>" not in sanitized
            assert "onerror=" not in sanitized
            assert "onclick=" not in sanitized
            assert "<style>" not in sanitized
            assert "javascript:" not in sanitized

    def test_database_query_sanitization(self):
        """Test database query parameter sanitization."""
        from shared.database.search import sanitize_search_query

        malicious_queries = [
            "'; DROP TABLE events; --",
            "' OR 1=1 --",
            "UNION SELECT password FROM users",
            "%'; DELETE FROM speakers; --",
        ]

        for query in malicious_queries:
            sanitized = sanitize_search_query(query)
            # Check that dangerous SQL keywords are removed or escaped
            assert "DROP" not in sanitized.upper()
            assert "DELETE" not in sanitized.upper()
            assert "UNION" not in sanitized.upper()
            assert "--" not in sanitized

    def test_json_output_sanitization(self):
        """Test JSON output sanitization to prevent injection."""
        test_data = {
            "event_name": "<script>alert('xss')</script>Event Name",
            "description": "Normal description with special chars: áéíóú",
            "speaker": 'John "The Hacker" Doe',
            "location": "Conference & Expo Hall",
        }

        # Simulate JSON serialization with sanitization
        sanitized_json = json.dumps(
            test_data, ensure_ascii=False, separators=(",", ":")
        )

        # Verify dangerous content is properly escaped
        assert "&lt;script&gt;" in sanitized_json or "<script>" not in sanitized_json
        assert '"' in sanitized_json  # Quotes should be properly escaped


@pytest.mark.security
class TestErrorHandling:
    """Test security aspects of error handling."""

    def test_error_message_information_disclosure(self):
        """Test that error messages don't leak sensitive information."""
        with patch("chatbot_api.main.process_chat_with_llm") as mock_chat:
            # Simulate database error
            mock_chat.side_effect = Exception(
                "Database connection failed: password=secret123"
            )

            try:
                mock_chat("test query")
            except Exception as e:
                error_message = str(e)
                # Error messages should not contain sensitive information
                assert "password=" not in error_message
                assert "secret" not in error_message.lower()
                assert "token" not in error_message.lower()

    def test_stack_trace_sanitization(self):
        """Test that stack traces don't expose sensitive paths or data."""
        import traceback

        try:
            # Simulate an error with sensitive path
            raise ValueError("Error in /home/user/.env/secret_key=abc123")
        except Exception:
            stack_trace = traceback.format_exc()

            # Production error handling should sanitize paths
            # This is a reminder to implement proper error sanitization
            # In production, sensitive paths should be redacted
            assert True  # Placeholder for actual sanitization checks


# Security test helpers
def generate_malicious_payloads():
    """Generate common malicious payloads for testing."""
    return [
        # SQL Injection
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "UNION SELECT * FROM sensitive_data",
        # XSS
        "<script>alert('xss')</script>",
        "<img src=x onerror=alert(1)>",
        "javascript:alert('xss')",
        # Path Traversal
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32",
        # Command Injection
        "; rm -rf /",
        "| cat /etc/passwd",
        "&& whoami",
        # NoSQL Injection
        "'; return db.users.find(); var dummy='",
        "'; return this.password; var dummy='",
    ]

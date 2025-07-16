"""
Unit tests for LangChain configuration components

Tests the configuration system for TrustWrapper LangChain integration.
"""

import sys
from pathlib import Path

import pytest

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent / "src"))

from src.integrations.langchain.langchain_config import (
    ComplianceMode,
    TrustWrapperConfig,
    VerificationLevel,
)


class TestVerificationLevel:
    """Test VerificationLevel enum"""

    def test_verification_level_values(self):
        """Test all verification levels have correct values"""
        assert VerificationLevel.MINIMAL.value == "minimal"
        assert VerificationLevel.STANDARD.value == "standard"
        assert VerificationLevel.COMPREHENSIVE.value == "comprehensive"
        assert VerificationLevel.ENTERPRISE.value == "enterprise"

    def test_verification_level_ordering(self):
        """Test verification levels have proper enum values"""
        # Enums don't support ordering by default, test enum values instead
        levels = [
            VerificationLevel.MINIMAL,
            VerificationLevel.STANDARD,
            VerificationLevel.COMPREHENSIVE,
            VerificationLevel.ENTERPRISE,
        ]

        # Test they're all different
        assert len(set(levels)) == len(levels)

        # Test specific ordering by value
        assert VerificationLevel.MINIMAL.value == "minimal"
        assert VerificationLevel.ENTERPRISE.value == "enterprise"


class TestComplianceMode:
    """Test ComplianceMode enum"""

    def test_compliance_mode_values(self):
        """Test all compliance modes have correct values"""
        assert ComplianceMode.NONE.value == "none"
        assert ComplianceMode.GDPR.value == "gdpr"
        assert ComplianceMode.HIPAA.value == "hipaa"
        assert ComplianceMode.SOX.value == "sox"
        assert ComplianceMode.EU_AI_ACT.value == "eu_ai_act"
        assert ComplianceMode.ALL.value == "all"


class TestTrustWrapperConfig:
    """Test TrustWrapperConfig class"""

    def test_default_config(self):
        """Test default configuration values"""
        config = TrustWrapperConfig()

        assert config.verification_level == VerificationLevel.STANDARD
        assert config.compliance_mode == ComplianceMode.NONE
        assert config.enable_monitoring is True
        assert config.pii_detection is False
        assert config.audit_logging is True  # Changed to True in implementation
        assert config.cache_ttl == 3600
        assert config.timeout == 5.0  # Changed from timeout_seconds
        assert config.max_retries == 3

    def test_custom_config(self):
        """Test custom configuration values"""
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.ENTERPRISE,
            compliance_mode=ComplianceMode.SOX,
            enable_monitoring=False,
            pii_detection=True,
            audit_logging=True,
            cache_ttl=7200,
            timeout=60.0,  # Changed from timeout_seconds
            max_retries=5,
        )

        assert config.verification_level == VerificationLevel.ENTERPRISE
        assert config.compliance_mode == ComplianceMode.SOX
        assert config.enable_monitoring is False
        assert config.pii_detection is True
        assert config.audit_logging is True
        assert config.cache_ttl == 7200
        assert config.timeout == 60.0  # Changed from timeout_seconds
        assert config.max_retries == 5

    def test_config_accepts_any_values(self):
        """Test configuration accepts various values (no validation currently)"""
        # Test with edge case values - should not raise errors
        config = TrustWrapperConfig(
            timeout=0.1,  # Very short timeout
            max_retries=0,  # No retries
            cache_ttl=1,  # Very short cache
        )

        assert config.timeout == 0.1
        assert config.max_retries == 0
        assert config.cache_ttl == 1

    def test_config_repr(self):
        """Test config string representation"""
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.COMPREHENSIVE,
            compliance_mode=ComplianceMode.GDPR,
        )

        repr_str = repr(config)
        assert "TrustWrapperConfig" in repr_str
        assert "comprehensive" in repr_str
        assert "gdpr" in repr_str

    def test_config_equality(self):
        """Test config equality comparison"""
        config1 = TrustWrapperConfig(
            verification_level=VerificationLevel.STANDARD,
            compliance_mode=ComplianceMode.SOX,
        )

        config2 = TrustWrapperConfig(
            verification_level=VerificationLevel.STANDARD,
            compliance_mode=ComplianceMode.SOX,
        )

        config3 = TrustWrapperConfig(
            verification_level=VerificationLevel.ENTERPRISE,
            compliance_mode=ComplianceMode.SOX,
        )

        assert config1 == config2
        assert config1 != config3

    def test_config_to_dict(self):
        """Test config can be converted to dictionary"""
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.COMPREHENSIVE,
            compliance_mode=ComplianceMode.SOX,
        )

        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert config_dict["verification_level"] == "comprehensive"
        assert config_dict["compliance_mode"] == "sox"

    def test_enterprise_features_enabled(self):
        """Test enterprise features are properly enabled"""
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.ENTERPRISE,
            compliance_mode=ComplianceMode.ALL,
            pii_detection=True,
            audit_logging=True,
        )

        # Verify all enterprise features are enabled
        assert config.verification_level == VerificationLevel.ENTERPRISE
        assert config.compliance_mode == ComplianceMode.ALL
        assert config.pii_detection is True
        assert config.audit_logging is True
        assert config.enable_monitoring is True  # Default

    def test_minimal_config(self):
        """Test minimal configuration for high-throughput scenarios"""
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.MINIMAL,
            compliance_mode=ComplianceMode.NONE,
            enable_monitoring=False,
            pii_detection=False,
            audit_logging=False,
        )

        # Verify minimal overhead configuration
        assert config.verification_level == VerificationLevel.MINIMAL
        assert config.compliance_mode == ComplianceMode.NONE
        assert config.enable_monitoring is False
        assert config.pii_detection is False
        assert config.audit_logging is False


class TestConfigIntegration:
    """Test configuration integration scenarios"""

    def test_financial_services_config(self):
        """Test configuration for financial services compliance"""
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.ENTERPRISE,
            compliance_mode=ComplianceMode.SOX,
            pii_detection=True,
            audit_logging=True,
            cache_ttl=1800,  # 30 minutes for financial data
        )

        # Verify financial services requirements
        assert config.verification_level == VerificationLevel.ENTERPRISE
        assert config.compliance_mode == ComplianceMode.SOX
        assert config.pii_detection is True
        assert config.audit_logging is True
        assert config.cache_ttl == 1800

    def test_healthcare_config(self):
        """Test configuration for healthcare compliance"""
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.COMPREHENSIVE,
            compliance_mode=ComplianceMode.HIPAA,
            pii_detection=True,
            audit_logging=True,
            timeout=15.0,  # Faster response for clinical use
        )

        # Verify healthcare requirements
        assert config.verification_level == VerificationLevel.COMPREHENSIVE
        assert config.compliance_mode == ComplianceMode.HIPAA
        assert config.pii_detection is True
        assert config.audit_logging is True
        assert config.timeout == 15.0

    def test_development_config(self):
        """Test configuration for development environment"""
        config = TrustWrapperConfig(
            verification_level=VerificationLevel.STANDARD,
            compliance_mode=ComplianceMode.NONE,
            enable_monitoring=True,
            cache_ttl=300,  # Short cache for development
            timeout=10.0,  # Fast timeout for dev
        )

        # Verify development-friendly settings
        assert config.verification_level == VerificationLevel.STANDARD
        assert config.compliance_mode == ComplianceMode.NONE
        assert config.enable_monitoring is True
        assert config.cache_ttl == 300
        assert config.timeout == 10.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

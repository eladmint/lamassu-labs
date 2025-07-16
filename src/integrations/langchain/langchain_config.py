"""
TrustWrapper LangChain Configuration

Configuration management for TrustWrapper LangChain integration.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class VerificationLevel(Enum):
    """Verification intensity levels"""

    MINIMAL = "minimal"  # Basic checks only
    STANDARD = "standard"  # Default verification
    COMPREHENSIVE = "comprehensive"  # Full verification suite
    ENTERPRISE = "enterprise"  # All features + compliance


class ComplianceMode(Enum):
    """Regulatory compliance modes"""

    NONE = "none"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOX = "sox"
    EU_AI_ACT = "eu_ai_act"
    ALL = "all"


@dataclass
class TrustWrapperConfig:
    """Configuration for TrustWrapper LangChain integration"""

    # Core settings
    api_key: Optional[str] = None
    api_endpoint: str = "https://api.trustwrapper.ai/v1"

    # Verification settings
    verification_level: VerificationLevel = VerificationLevel.STANDARD
    verify_llm_outputs: bool = True
    verify_tool_outputs: bool = True
    verify_agent_actions: bool = True

    # Performance settings
    async_verification: bool = True
    batch_size: int = 10
    cache_ttl: int = 3600  # seconds
    timeout: float = 5.0  # seconds
    max_retries: int = 3

    # Compliance settings
    compliance_mode: ComplianceMode = ComplianceMode.NONE
    audit_logging: bool = True
    pii_detection: bool = False
    data_retention_days: int = 90

    # Monitoring settings
    enable_monitoring: bool = True
    monitoring_endpoint: Optional[str] = None
    metrics_interval: int = 60  # seconds

    # Advanced settings
    custom_verification_rules: Optional[Dict[str, Any]] = None
    excluded_tools: List[str] = None
    included_agents: List[str] = None

    def __post_init__(self):
        """Validate configuration after initialization"""
        if self.excluded_tools is None:
            self.excluded_tools = []
        if self.included_agents is None:
            self.included_agents = []

        # Auto-enable features based on compliance mode
        if self.compliance_mode in [ComplianceMode.HIPAA, ComplianceMode.GDPR]:
            self.pii_detection = True
            self.audit_logging = True

        if self.compliance_mode == ComplianceMode.ALL:
            self.verification_level = VerificationLevel.ENTERPRISE
            self.pii_detection = True
            self.audit_logging = True

    @classmethod
    def from_env(cls) -> "TrustWrapperConfig":
        """Create configuration from environment variables"""
        import os

        config = cls()

        # Load from environment
        config.api_key = os.getenv("TRUSTWRAPPER_API_KEY")
        config.api_endpoint = os.getenv(
            "TRUSTWRAPPER_API_ENDPOINT", config.api_endpoint
        )

        # Verification settings
        if level := os.getenv("TRUSTWRAPPER_VERIFICATION_LEVEL"):
            config.verification_level = VerificationLevel(level)

        # Compliance settings
        if mode := os.getenv("TRUSTWRAPPER_COMPLIANCE_MODE"):
            config.compliance_mode = ComplianceMode(mode)

        return config

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "api_endpoint": self.api_endpoint,
            "verification_level": self.verification_level.value,
            "compliance_mode": self.compliance_mode.value,
            "async_verification": self.async_verification,
            "cache_ttl": self.cache_ttl,
            "audit_logging": self.audit_logging,
            "pii_detection": self.pii_detection,
        }

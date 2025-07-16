#!/usr/bin/env python3
"""
TrustWrapper v3.0 - Universal Multi-Chain AI Verification Platform
World's first universal cross-chain AI verification framework
"""

from .api_gateway import (
    BridgeOperationModel,
    ConsensusRequestModel,
    HealthResponseModel,
    HealthStatus,
    TrustWrapperAPIGateway,
    VerificationRequestModel,
    VerificationResponseModel,
    create_app,
    get_api_gateway,
)
from .authentication_security import (
    APIKeyInfo,
    AuthenticationMethod,
    RateLimitRule,
    RateLimitType,
    SecurityLevel,
    TrustWrapperSecurityManager,
    UserCredentials,
    get_current_user_from_api_key,
    get_current_user_from_token,
    get_security_manager,
    require_permission,
)
from .enhanced_oracle_integration import (
    BandProtocolClient,
    ChainlinkOracleClient,
    CustomOracleClient,
    EnhancedOracleIntegration,
    MultiOracleConsensus,
    OracleData,
    OracleSource,
    OracleType,
    get_enhanced_oracle_integration,
)
from .enterprise_integration import (
    AuditEventType,
    AuditLogEntry,
    ComplianceFramework,
    MonitoringLevel,
    MonitoringMetric,
    TenantConfiguration,
    TenantTier,
    TrustWrapperEnterpriseManager,
    get_enterprise_manager,
    log_api_access,
    require_tenant_access,
)
from .multi_chain_connection_manager import (
    ConnectionHealth,
    MultiChainConnectionManager,
    SecurityLevel,
    UniversalVerificationResult,
    VerificationRequest,
    get_connection_manager,
)
from .scaling_infrastructure import (
    AsyncTaskConfig,
    AsyncTaskManager,
    CacheConfig,
    CacheStrategy,
    PerformanceCacheLayer,
    ProcessingPriority,
    RedisConnectionManager,
    ScalingInfrastructureManager,
    get_scaling_infrastructure,
)
from .universal_chain_adapter import (
    DEFAULT_CHAIN_CONFIGS,
    ChainAdapter,
    ChainConfig,
    ChainType,
    UniversalChainAdapter,
    VerificationData,
    VerificationResult,
    get_universal_adapter,
)

__version__ = "3.0.0"
__author__ = "Lamassu Labs"
__description__ = "Universal Multi-Chain AI Verification Platform"

# Export main classes and functions
__all__ = [
    # Universal Chain Adapter
    "UniversalChainAdapter",
    "ChainAdapter",
    "ChainConfig",
    "ChainType",
    "VerificationData",
    "VerificationResult",
    "DEFAULT_CHAIN_CONFIGS",
    "get_universal_adapter",
    # Enhanced Oracle Integration
    "EnhancedOracleIntegration",
    "OracleType",
    "OracleSource",
    "OracleData",
    "MultiOracleConsensus",
    "ChainlinkOracleClient",
    "BandProtocolClient",
    "CustomOracleClient",
    "get_enhanced_oracle_integration",
    # Multi-Chain Connection Manager
    "MultiChainConnectionManager",
    "SecurityLevel",
    "VerificationRequest",
    "UniversalVerificationResult",
    "ConnectionHealth",
    "get_connection_manager",
    # Scaling Infrastructure
    "ScalingInfrastructureManager",
    "RedisConnectionManager",
    "AsyncTaskManager",
    "PerformanceCacheLayer",
    "CacheConfig",
    "AsyncTaskConfig",
    "ProcessingPriority",
    "CacheStrategy",
    "get_scaling_infrastructure",
    # API Gateway
    "TrustWrapperAPIGateway",
    "VerificationRequestModel",
    "VerificationResponseModel",
    "ConsensusRequestModel",
    "BridgeOperationModel",
    "HealthResponseModel",
    "HealthStatus",
    "get_api_gateway",
    "create_app",
    # Authentication & Security
    "TrustWrapperSecurityManager",
    "SecurityLevel",
    "AuthenticationMethod",
    "RateLimitType",
    "UserCredentials",
    "APIKeyInfo",
    "RateLimitRule",
    "get_security_manager",
    "get_current_user_from_token",
    "get_current_user_from_api_key",
    "require_permission",
    # Enterprise Integration
    "TrustWrapperEnterpriseManager",
    "TenantTier",
    "AuditEventType",
    "ComplianceFramework",
    "MonitoringLevel",
    "TenantConfiguration",
    "AuditLogEntry",
    "MonitoringMetric",
    "get_enterprise_manager",
    "require_tenant_access",
    "log_api_access",
]

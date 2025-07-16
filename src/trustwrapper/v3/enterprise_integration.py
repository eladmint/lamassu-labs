#!/usr/bin/env python3
"""
TrustWrapper v3.0 Enterprise Integration System
Multi-tenant architecture with audit logging and monitoring integration
Task 3.3: Week 3 Phase 1 Implementation
"""

import asyncio
import logging
import time
import uuid
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TenantTier(Enum):
    """Enterprise tenant tiers"""

    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    ULTIMATE = "ultimate"


class AuditEventType(Enum):
    """Types of audit events"""

    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    API_ACCESS = "api_access"
    VERIFICATION_REQUEST = "verification_request"
    CONSENSUS_CALCULATION = "consensus_calculation"
    SECURITY_VIOLATION = "security_violation"
    CONFIGURATION_CHANGE = "configuration_change"
    DATA_ACCESS = "data_access"
    SYSTEM_EVENT = "system_event"
    COMPLIANCE_CHECK = "compliance_check"


class ComplianceFramework(Enum):
    """Supported compliance frameworks"""

    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    SOX = "sox"
    MICA = "mica"
    SEC = "sec"


class MonitoringLevel(Enum):
    """Monitoring detail levels"""

    BASIC = "basic"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"
    REALTIME = "realtime"


@dataclass
class TenantConfiguration:
    """Multi-tenant configuration"""

    tenant_id: str
    tenant_name: str
    tenant_tier: TenantTier
    created_at: float
    admin_user_id: str

    # Resource limits
    max_users: int = 100
    max_api_calls_per_month: int = 100000
    max_concurrent_verifications: int = 10
    max_storage_gb: int = 10

    # Feature flags
    advanced_consensus: bool = True
    oracle_integration: bool = True
    cross_chain_bridge: bool = True
    custom_branding: bool = False
    priority_support: bool = False

    # Compliance settings
    compliance_frameworks: List[ComplianceFramework] = field(default_factory=list)
    data_retention_days: int = 365
    encryption_at_rest: bool = True
    audit_logging: bool = True

    # Monitoring settings
    monitoring_level: MonitoringLevel = MonitoringLevel.BASIC
    custom_alerts: bool = False
    real_time_dashboard: bool = False

    # Network settings
    allowed_ip_ranges: List[str] = field(default_factory=list)
    webhook_endpoints: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "tenant_tier": self.tenant_tier.value,
            "compliance_frameworks": [f.value for f in self.compliance_frameworks],
            "monitoring_level": self.monitoring_level.value,
        }


@dataclass
class AuditLogEntry:
    """Audit log entry for compliance tracking"""

    entry_id: str
    tenant_id: str
    user_id: Optional[str]
    event_type: AuditEventType
    timestamp: float

    # Event details
    action: str
    resource: str
    outcome: str  # success, failure, warning

    # Context information
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    api_endpoint: Optional[str] = None

    # Detailed information
    event_data: Dict[str, Any] = field(default_factory=dict)
    risk_score: float = 0.0
    compliance_tags: List[str] = field(default_factory=list)

    # Retention and security
    retention_until: Optional[float] = None
    encrypted: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {**asdict(self), "event_type": self.event_type.value}


@dataclass
class MonitoringMetric:
    """Performance and business monitoring metric"""

    metric_id: str
    tenant_id: str
    metric_name: str
    metric_value: float
    timestamp: float

    # Metadata
    unit: str = "count"
    dimensions: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    # Aggregation
    aggregation_window: int = 60  # seconds
    metric_type: str = "gauge"  # gauge, counter, histogram

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TrustWrapperEnterpriseManager:
    """
    Enterprise integration manager for TrustWrapper v3.0
    Handles multi-tenancy, audit logging, compliance, and monitoring
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Multi-tenant storage
        self.tenants: Dict[str, TenantConfiguration] = {}
        self.tenant_users: Dict[str, Set[str]] = defaultdict(
            set
        )  # tenant_id -> user_ids
        self.user_tenant_map: Dict[str, str] = {}  # user_id -> tenant_id

        # Audit logging
        self.audit_logs: List[AuditLogEntry] = []
        self.audit_log_index: Dict[str, List[str]] = defaultdict(
            list
        )  # tenant_id -> entry_ids

        # Monitoring and metrics
        self.metrics: List[MonitoringMetric] = []
        self.metric_buffers: Dict[str, List[MonitoringMetric]] = defaultdict(list)
        self.alert_rules: Dict[str, Dict[str, Any]] = {}

        # Compliance tracking
        self.compliance_reports: Dict[str, Dict[str, Any]] = {}
        self.compliance_schedules: Dict[str, Dict[str, Any]] = {}

        # Resource usage tracking
        self.resource_usage: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "api_calls_today": 0,
                "storage_used_gb": 0.0,
                "active_verifications": 0,
                "last_reset": time.time(),
            }
        )

        # Performance tracking
        self.performance_metrics = {
            "total_tenants": 0,
            "total_audit_entries": 0,
            "total_monitoring_metrics": 0,
            "avg_response_time": 0.0,
            "uptime_percentage": 99.9,
        }

    async def initialize(self):
        """Initialize enterprise manager"""
        try:
            self.logger.info("🏢 Initializing TrustWrapper Enterprise Manager...")

            # Create default enterprise tenant for demonstration
            await self._create_default_enterprise_tenant()

            # Setup compliance schedules
            await self._setup_compliance_schedules()

            # Initialize monitoring
            await self._initialize_monitoring()

            self.logger.info("✅ Enterprise Manager initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Enterprise Manager: {e}")
            raise

    async def _create_default_enterprise_tenant(self):
        """Create default enterprise tenant for demonstration"""
        default_tenant = TenantConfiguration(
            tenant_id="enterprise_demo_001",
            tenant_name="TrustWrapper Enterprise Demo",
            tenant_tier=TenantTier.ENTERPRISE,
            created_at=time.time(),
            admin_user_id="admin_001",
            max_users=1000,
            max_api_calls_per_month=10000000,
            max_concurrent_verifications=100,
            max_storage_gb=100,
            advanced_consensus=True,
            oracle_integration=True,
            cross_chain_bridge=True,
            custom_branding=True,
            priority_support=True,
            compliance_frameworks=[
                ComplianceFramework.SOC2,
                ComplianceFramework.ISO27001,
                ComplianceFramework.GDPR,
            ],
            data_retention_days=2555,  # 7 years
            monitoring_level=MonitoringLevel.COMPREHENSIVE,
            custom_alerts=True,
            real_time_dashboard=True,
        )

        await self.create_tenant(default_tenant)

    async def _setup_compliance_schedules(self):
        """Setup automated compliance reporting schedules"""
        self.compliance_schedules = {
            "daily_security_scan": {
                "frequency": "daily",
                "time": "02:00",
                "frameworks": [ComplianceFramework.SOC2.value],
                "last_run": None,
            },
            "weekly_audit_review": {
                "frequency": "weekly",
                "day": "sunday",
                "time": "01:00",
                "frameworks": [ComplianceFramework.ISO27001.value],
                "last_run": None,
            },
            "monthly_compliance_report": {
                "frequency": "monthly",
                "day": 1,
                "time": "00:00",
                "frameworks": [f.value for f in ComplianceFramework],
                "last_run": None,
            },
        }

    async def _initialize_monitoring(self):
        """Initialize monitoring system"""
        # Setup default alert rules
        self.alert_rules = {
            "high_error_rate": {
                "metric": "error_rate",
                "threshold": 0.05,  # 5%
                "comparison": "greater_than",
                "window_minutes": 5,
                "severity": "critical",
            },
            "high_latency": {
                "metric": "avg_response_time",
                "threshold": 1000,  # 1 second
                "comparison": "greater_than",
                "window_minutes": 5,
                "severity": "warning",
            },
            "resource_exhaustion": {
                "metric": "api_calls_per_minute",
                "threshold": 1000,
                "comparison": "greater_than",
                "window_minutes": 1,
                "severity": "warning",
            },
        }

    async def create_tenant(self, tenant_config: TenantConfiguration) -> bool:
        """Create new enterprise tenant"""
        try:
            # Validate tenant configuration
            if tenant_config.tenant_id in self.tenants:
                raise ValueError(f"Tenant {tenant_config.tenant_id} already exists")

            # Apply tier-based defaults
            tenant_config = await self._apply_tier_defaults(tenant_config)

            # Store tenant configuration
            self.tenants[tenant_config.tenant_id] = tenant_config

            # Initialize tenant resources
            self.resource_usage[tenant_config.tenant_id] = {
                "api_calls_today": 0,
                "storage_used_gb": 0.0,
                "active_verifications": 0,
                "last_reset": time.time(),
            }

            # Create audit log entry
            await self.log_audit_event(
                tenant_id=tenant_config.tenant_id,
                user_id=tenant_config.admin_user_id,
                event_type=AuditEventType.CONFIGURATION_CHANGE,
                action="create_tenant",
                resource=f"tenant:{tenant_config.tenant_id}",
                outcome="success",
                event_data={
                    "tenant_name": tenant_config.tenant_name,
                    "tier": tenant_config.tenant_tier.value,
                    "compliance_frameworks": [
                        f.value for f in tenant_config.compliance_frameworks
                    ],
                },
            )

            # Update performance metrics
            self.performance_metrics["total_tenants"] = len(self.tenants)

            self.logger.info(
                f"✅ Tenant created: {tenant_config.tenant_name} ({tenant_config.tenant_tier.value})"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to create tenant: {e}")
            raise

    async def _apply_tier_defaults(
        self, tenant_config: TenantConfiguration
    ) -> TenantConfiguration:
        """Apply tier-based configuration defaults"""
        tier_defaults = {
            TenantTier.STARTER: {
                "max_users": 10,
                "max_api_calls_per_month": 10000,
                "max_concurrent_verifications": 2,
                "max_storage_gb": 1,
                "advanced_consensus": False,
                "custom_branding": False,
                "priority_support": False,
                "monitoring_level": MonitoringLevel.BASIC,
                "data_retention_days": 90,
            },
            TenantTier.PROFESSIONAL: {
                "max_users": 100,
                "max_api_calls_per_month": 100000,
                "max_concurrent_verifications": 10,
                "max_storage_gb": 10,
                "advanced_consensus": True,
                "custom_branding": True,
                "priority_support": False,
                "monitoring_level": MonitoringLevel.DETAILED,
                "data_retention_days": 365,
            },
            TenantTier.ENTERPRISE: {
                "max_users": 1000,
                "max_api_calls_per_month": 1000000,
                "max_concurrent_verifications": 50,
                "max_storage_gb": 100,
                "advanced_consensus": True,
                "custom_branding": True,
                "priority_support": True,
                "monitoring_level": MonitoringLevel.COMPREHENSIVE,
                "data_retention_days": 2555,
            },
            TenantTier.ULTIMATE: {
                "max_users": 10000,
                "max_api_calls_per_month": 10000000,
                "max_concurrent_verifications": 200,
                "max_storage_gb": 1000,
                "advanced_consensus": True,
                "custom_branding": True,
                "priority_support": True,
                "monitoring_level": MonitoringLevel.REALTIME,
                "data_retention_days": 3650,
            },
        }

        defaults = tier_defaults.get(tenant_config.tenant_tier, {})

        # Apply defaults for None values
        for key, default_value in defaults.items():
            if hasattr(tenant_config, key) and getattr(tenant_config, key) is None:
                setattr(tenant_config, key, default_value)

        return tenant_config

    async def add_user_to_tenant(self, tenant_id: str, user_id: str) -> bool:
        """Add user to tenant"""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                raise ValueError(f"Tenant {tenant_id} not found")

            # Check user limits
            if len(self.tenant_users[tenant_id]) >= tenant.max_users:
                raise ValueError(
                    f"Tenant {tenant_id} has reached user limit ({tenant.max_users})"
                )

            # Add user to tenant
            self.tenant_users[tenant_id].add(user_id)
            self.user_tenant_map[user_id] = tenant_id

            # Log audit event
            await self.log_audit_event(
                tenant_id=tenant_id,
                user_id=user_id,
                event_type=AuditEventType.CONFIGURATION_CHANGE,
                action="add_user_to_tenant",
                resource=f"tenant:{tenant_id}",
                outcome="success",
                event_data={"new_user_id": user_id},
            )

            self.logger.info(f"✅ User {user_id} added to tenant {tenant_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add user to tenant: {e}")
            raise

    async def log_audit_event(
        self,
        tenant_id: str,
        user_id: Optional[str],
        event_type: AuditEventType,
        action: str,
        resource: str,
        outcome: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        session_id: Optional[str] = None,
        api_endpoint: Optional[str] = None,
        event_data: Dict[str, Any] = None,
        risk_score: float = 0.0,
    ) -> AuditLogEntry:
        """Log audit event for compliance tracking"""
        try:
            # Generate unique entry ID
            entry_id = f"audit_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"

            # Get tenant for compliance settings
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                raise ValueError(f"Tenant {tenant_id} not found")

            # Calculate retention date
            retention_until = None
            if tenant.data_retention_days > 0:
                retention_until = time.time() + (tenant.data_retention_days * 86400)

            # Determine compliance tags
            compliance_tags = []
            for framework in tenant.compliance_frameworks:
                compliance_tags.append(framework.value)

            # Create audit entry
            audit_entry = AuditLogEntry(
                entry_id=entry_id,
                tenant_id=tenant_id,
                user_id=user_id,
                event_type=event_type,
                timestamp=time.time(),
                action=action,
                resource=resource,
                outcome=outcome,
                ip_address=ip_address,
                user_agent=user_agent,
                session_id=session_id,
                api_endpoint=api_endpoint,
                event_data=event_data or {},
                risk_score=risk_score,
                compliance_tags=compliance_tags,
                retention_until=retention_until,
                encrypted=tenant.encryption_at_rest,
            )

            # Store audit entry
            self.audit_logs.append(audit_entry)
            self.audit_log_index[tenant_id].append(entry_id)

            # Update performance metrics
            self.performance_metrics["total_audit_entries"] = len(self.audit_logs)

            # Check for high-risk events
            if risk_score >= 0.7:
                await self._handle_high_risk_event(audit_entry)

            return audit_entry

        except Exception as e:
            self.logger.error(f"Failed to log audit event: {e}")
            raise

    async def _handle_high_risk_event(self, audit_entry: AuditLogEntry):
        """Handle high-risk security events"""
        try:
            self.logger.warning(
                f"🚨 High-risk event detected: {audit_entry.action} (risk: {audit_entry.risk_score})"
            )

            # Create additional security audit entry
            await self.log_audit_event(
                tenant_id=audit_entry.tenant_id,
                user_id="system",
                event_type=AuditEventType.SECURITY_VIOLATION,
                action="high_risk_event_detected",
                resource=f"audit_entry:{audit_entry.entry_id}",
                outcome="warning",
                event_data={
                    "original_event": audit_entry.action,
                    "risk_score": audit_entry.risk_score,
                    "automated_response": "security_alert_triggered",
                },
            )

            # In production, this would trigger alerts, notifications, etc.

        except Exception as e:
            self.logger.error(f"Failed to handle high-risk event: {e}")

    async def record_monitoring_metric(
        self,
        tenant_id: str,
        metric_name: str,
        metric_value: float,
        unit: str = "count",
        dimensions: Dict[str, str] = None,
        tags: List[str] = None,
    ) -> MonitoringMetric:
        """Record performance or business monitoring metric"""
        try:
            # Generate metric ID
            metric_id = f"metric_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"

            # Create metric entry
            metric = MonitoringMetric(
                metric_id=metric_id,
                tenant_id=tenant_id,
                metric_name=metric_name,
                metric_value=metric_value,
                timestamp=time.time(),
                unit=unit,
                dimensions=dimensions or {},
                tags=tags or [],
            )

            # Store metric
            self.metrics.append(metric)
            self.metric_buffers[tenant_id].append(metric)

            # Update performance metrics
            self.performance_metrics["total_monitoring_metrics"] = len(self.metrics)

            # Check alert rules
            await self._check_alert_rules(tenant_id, metric)

            return metric

        except Exception as e:
            self.logger.error(f"Failed to record monitoring metric: {e}")
            raise

    async def _check_alert_rules(self, tenant_id: str, metric: MonitoringMetric):
        """Check if metric triggers any alert rules"""
        try:
            for rule_name, rule in self.alert_rules.items():
                if rule["metric"] == metric.metric_name:
                    # Simple threshold check (in production, would have time windows)
                    triggered = False

                    if (
                        rule["comparison"] == "greater_than"
                        and metric.metric_value > rule["threshold"]
                    ):
                        triggered = True
                    elif (
                        rule["comparison"] == "less_than"
                        and metric.metric_value < rule["threshold"]
                    ):
                        triggered = True

                    if triggered:
                        await self._trigger_alert(tenant_id, rule_name, metric, rule)

        except Exception as e:
            self.logger.error(f"Failed to check alert rules: {e}")

    async def _trigger_alert(
        self,
        tenant_id: str,
        rule_name: str,
        metric: MonitoringMetric,
        rule: Dict[str, Any],
    ):
        """Trigger monitoring alert"""
        try:
            self.logger.warning(
                f"🚨 Alert triggered: {rule_name} for tenant {tenant_id}"
            )

            # Log alert as audit event
            await self.log_audit_event(
                tenant_id=tenant_id,
                user_id="system",
                event_type=AuditEventType.SYSTEM_EVENT,
                action="monitoring_alert_triggered",
                resource=f"alert_rule:{rule_name}",
                outcome="warning",
                event_data={
                    "rule_name": rule_name,
                    "metric_name": metric.metric_name,
                    "metric_value": metric.metric_value,
                    "threshold": rule["threshold"],
                    "severity": rule["severity"],
                },
                risk_score=0.5 if rule["severity"] == "warning" else 0.8,
            )

            # In production, would send notifications, webhooks, etc.

        except Exception as e:
            self.logger.error(f"Failed to trigger alert: {e}")

    async def check_resource_limits(
        self, tenant_id: str, resource_type: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """Check if tenant is within resource limits"""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                raise ValueError(f"Tenant {tenant_id} not found")

            usage = self.resource_usage[tenant_id]
            current_time = time.time()

            # Reset daily counters if needed
            if current_time - usage["last_reset"] > 86400:  # 24 hours
                usage["api_calls_today"] = 0
                usage["last_reset"] = current_time

            # Check limits based on resource type
            limits_status = {"within_limits": True, "checks": {}}

            if resource_type in ["api_call", "all"]:
                monthly_limit = tenant.max_api_calls_per_month
                daily_limit = monthly_limit // 30  # Approximate daily limit

                api_check = {
                    "current": usage["api_calls_today"],
                    "limit": daily_limit,
                    "percentage": (
                        (usage["api_calls_today"] / daily_limit * 100)
                        if daily_limit > 0
                        else 0
                    ),
                }

                if usage["api_calls_today"] >= daily_limit:
                    limits_status["within_limits"] = False

                limits_status["checks"]["api_calls"] = api_check

            if resource_type in ["storage", "all"]:
                storage_check = {
                    "current": usage["storage_used_gb"],
                    "limit": tenant.max_storage_gb,
                    "percentage": (
                        (usage["storage_used_gb"] / tenant.max_storage_gb * 100)
                        if tenant.max_storage_gb > 0
                        else 0
                    ),
                }

                if usage["storage_used_gb"] >= tenant.max_storage_gb:
                    limits_status["within_limits"] = False

                limits_status["checks"]["storage"] = storage_check

            if resource_type in ["verification", "all"]:
                verification_check = {
                    "current": usage["active_verifications"],
                    "limit": tenant.max_concurrent_verifications,
                    "percentage": (
                        (
                            usage["active_verifications"]
                            / tenant.max_concurrent_verifications
                            * 100
                        )
                        if tenant.max_concurrent_verifications > 0
                        else 0
                    ),
                }

                if usage["active_verifications"] >= tenant.max_concurrent_verifications:
                    limits_status["within_limits"] = False

                limits_status["checks"]["verifications"] = verification_check

            return limits_status["within_limits"], limits_status

        except Exception as e:
            self.logger.error(f"Failed to check resource limits: {e}")
            return False, {"error": str(e)}

    async def increment_resource_usage(
        self, tenant_id: str, resource_type: str, amount: float = 1.0
    ):
        """Increment resource usage for tenant"""
        try:
            usage = self.resource_usage[tenant_id]

            if resource_type == "api_call":
                usage["api_calls_today"] += int(amount)
            elif resource_type == "storage":
                usage["storage_used_gb"] += amount
            elif resource_type == "verification":
                usage["active_verifications"] += int(amount)

            # Record usage as metric
            await self.record_monitoring_metric(
                tenant_id=tenant_id,
                metric_name=f"{resource_type}_usage",
                metric_value=amount,
                dimensions={"resource_type": resource_type},
            )

        except Exception as e:
            self.logger.error(f"Failed to increment resource usage: {e}")

    async def generate_compliance_report(
        self,
        tenant_id: str,
        framework: ComplianceFramework,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Generate compliance report for specific framework"""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                raise ValueError(f"Tenant {tenant_id} not found")

            if framework not in tenant.compliance_frameworks:
                raise ValueError(
                    f"Framework {framework.value} not enabled for tenant {tenant_id}"
                )

            # Set default time range (last 30 days)
            if not start_time:
                start_time = time.time() - (30 * 86400)
            if not end_time:
                end_time = time.time()

            # Get relevant audit logs
            relevant_logs = [
                log
                for log in self.audit_logs
                if log.tenant_id == tenant_id
                and framework.value in log.compliance_tags
                and start_time <= log.timestamp <= end_time
            ]

            # Generate framework-specific analysis
            report = {
                "tenant_id": tenant_id,
                "framework": framework.value,
                "report_period": {
                    "start": start_time,
                    "end": end_time,
                    "duration_days": (end_time - start_time) / 86400,
                },
                "generated_at": time.time(),
                "summary": {
                    "total_events": len(relevant_logs),
                    "successful_events": len(
                        [log for log in relevant_logs if log.outcome == "success"]
                    ),
                    "failed_events": len(
                        [log for log in relevant_logs if log.outcome == "failure"]
                    ),
                    "high_risk_events": len(
                        [log for log in relevant_logs if log.risk_score >= 0.7]
                    ),
                },
            }

            # Framework-specific compliance checks
            if framework == ComplianceFramework.SOC2:
                report["soc2_controls"] = await self._generate_soc2_analysis(
                    relevant_logs, tenant
                )
            elif framework == ComplianceFramework.GDPR:
                report["gdpr_compliance"] = await self._generate_gdpr_analysis(
                    relevant_logs, tenant
                )
            elif framework == ComplianceFramework.ISO27001:
                report["iso27001_controls"] = await self._generate_iso27001_analysis(
                    relevant_logs, tenant
                )

            # Store report
            report_key = f"{tenant_id}_{framework.value}_{int(time.time())}"
            self.compliance_reports[report_key] = report

            return report

        except Exception as e:
            self.logger.error(f"Failed to generate compliance report: {e}")
            raise

    async def _generate_soc2_analysis(
        self, logs: List[AuditLogEntry], tenant: TenantConfiguration
    ) -> Dict[str, Any]:
        """Generate SOC2 compliance analysis"""
        return {
            "security": {
                "access_controls": len(
                    [
                        log
                        for log in logs
                        if log.event_type
                        in [AuditEventType.USER_LOGIN, AuditEventType.API_ACCESS]
                    ]
                ),
                "failed_access_attempts": len(
                    [
                        log
                        for log in logs
                        if log.outcome == "failure"
                        and log.event_type == AuditEventType.USER_LOGIN
                    ]
                ),
                "privileged_access": len(
                    [
                        log
                        for log in logs
                        if "admin" in log.action or "config" in log.action
                    ]
                ),
            },
            "availability": {
                "system_uptime": self.performance_metrics.get(
                    "uptime_percentage", 99.9
                ),
                "response_time": self.performance_metrics.get("avg_response_time", 0.0),
            },
            "processing_integrity": {
                "data_validation_events": len(
                    [log for log in logs if "verification" in log.action]
                ),
                "integrity_checks": len(
                    [
                        log
                        for log in logs
                        if log.event_type == AuditEventType.COMPLIANCE_CHECK
                    ]
                ),
            },
            "confidentiality": {
                "encryption_enabled": tenant.encryption_at_rest,
                "data_access_events": len(
                    [
                        log
                        for log in logs
                        if log.event_type == AuditEventType.DATA_ACCESS
                    ]
                ),
            },
        }

    async def _generate_gdpr_analysis(
        self, logs: List[AuditLogEntry], tenant: TenantConfiguration
    ) -> Dict[str, Any]:
        """Generate GDPR compliance analysis"""
        return {
            "data_protection": {
                "encryption_at_rest": tenant.encryption_at_rest,
                "data_retention_policy": f"{tenant.data_retention_days} days",
                "audit_trail_complete": len(logs) > 0,
            },
            "data_subject_rights": {
                "access_requests": len(
                    [log for log in logs if "data_access" in log.action]
                ),
                "deletion_requests": len(
                    [log for log in logs if "delete" in log.action]
                ),
                "consent_management": True,  # Simplified for demo
            },
            "breach_notification": {
                "security_incidents": len(
                    [
                        log
                        for log in logs
                        if log.event_type == AuditEventType.SECURITY_VIOLATION
                    ]
                ),
                "incident_response_time": "< 1 hour",  # Simplified for demo
                "authority_notification": "Automated",
            },
        }

    async def _generate_iso27001_analysis(
        self, logs: List[AuditLogEntry], tenant: TenantConfiguration
    ) -> Dict[str, Any]:
        """Generate ISO 27001 compliance analysis"""
        return {
            "information_security_management": {
                "security_policy": True,
                "risk_assessments": len([log for log in logs if log.risk_score > 0]),
                "security_awareness": True,
            },
            "access_control": {
                "user_access_management": len(
                    [log for log in logs if log.event_type == AuditEventType.USER_LOGIN]
                ),
                "privileged_access_control": len(
                    [log for log in logs if "admin" in log.action]
                ),
                "access_reviews": "Monthly",
            },
            "incident_management": {
                "security_incidents": len(
                    [
                        log
                        for log in logs
                        if log.event_type == AuditEventType.SECURITY_VIOLATION
                    ]
                ),
                "incident_response": "Automated",
                "forensic_analysis": "Available",
            },
        }

    async def get_tenant_dashboard_data(self, tenant_id: str) -> Dict[str, Any]:
        """Get comprehensive dashboard data for tenant"""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                raise ValueError(f"Tenant {tenant_id} not found")

            # Get recent metrics (last 24 hours)
            current_time = time.time()
            recent_metrics = [
                metric
                for metric in self.metrics
                if metric.tenant_id == tenant_id
                and current_time - metric.timestamp < 86400
            ]

            # Get resource usage status
            within_limits, resource_status = await self.check_resource_limits(
                tenant_id, "all"
            )

            # Get recent audit events
            recent_audit_events = [
                log
                for log in self.audit_logs
                if log.tenant_id == tenant_id and current_time - log.timestamp < 86400
            ]

            dashboard_data = {
                "tenant_info": tenant.to_dict(),
                "resource_usage": {
                    "within_limits": within_limits,
                    "details": resource_status["checks"],
                },
                "recent_activity": {
                    "total_events": len(recent_audit_events),
                    "successful_operations": len(
                        [log for log in recent_audit_events if log.outcome == "success"]
                    ),
                    "failed_operations": len(
                        [log for log in recent_audit_events if log.outcome == "failure"]
                    ),
                    "security_events": len(
                        [
                            log
                            for log in recent_audit_events
                            if log.event_type == AuditEventType.SECURITY_VIOLATION
                        ]
                    ),
                },
                "performance_metrics": {
                    "total_requests": len(
                        [m for m in recent_metrics if m.metric_name == "api_request"]
                    ),
                    "avg_response_time": sum(
                        [
                            m.metric_value
                            for m in recent_metrics
                            if m.metric_name == "response_time"
                        ]
                    )
                    / max(
                        len(
                            [
                                m
                                for m in recent_metrics
                                if m.metric_name == "response_time"
                            ]
                        ),
                        1,
                    ),
                    "error_rate": len(
                        [log for log in recent_audit_events if log.outcome == "failure"]
                    )
                    / max(len(recent_audit_events), 1),
                },
                "compliance_status": {
                    "frameworks": [f.value for f in tenant.compliance_frameworks],
                    "data_retention_days": tenant.data_retention_days,
                    "encryption_enabled": tenant.encryption_at_rest,
                    "audit_logging": tenant.audit_logging,
                },
            }

            return dashboard_data

        except Exception as e:
            self.logger.error(f"Failed to get tenant dashboard data: {e}")
            raise

    async def get_enterprise_metrics(self) -> Dict[str, Any]:
        """Get enterprise-wide monitoring metrics"""
        try:
            current_time = time.time()

            # Calculate metrics across all tenants
            total_api_calls = sum(
                [usage["api_calls_today"] for usage in self.resource_usage.values()]
            )

            total_storage = sum(
                [usage["storage_used_gb"] for usage in self.resource_usage.values()]
            )

            active_verifications = sum(
                [
                    usage["active_verifications"]
                    for usage in self.resource_usage.values()
                ]
            )

            # Recent audit events (last hour)
            recent_events = [
                log for log in self.audit_logs if current_time - log.timestamp < 3600
            ]

            enterprise_metrics = {
                "timestamp": current_time,
                "tenant_metrics": {
                    "total_tenants": len(self.tenants),
                    "active_tenants": len(
                        [
                            t
                            for t in self.tenants.values()
                            if any(
                                self.resource_usage[t.tenant_id]["api_calls_today"] > 0
                                for _ in [None]
                            )
                        ]
                    ),
                    "tenant_tiers": {
                        tier.value: len(
                            [t for t in self.tenants.values() if t.tenant_tier == tier]
                        )
                        for tier in TenantTier
                    },
                },
                "resource_utilization": {
                    "total_api_calls_today": total_api_calls,
                    "total_storage_gb": total_storage,
                    "active_verifications": active_verifications,
                    "avg_api_calls_per_tenant": total_api_calls
                    / max(len(self.tenants), 1),
                },
                "security_metrics": {
                    "total_audit_events": len(self.audit_logs),
                    "recent_events_hour": len(recent_events),
                    "security_violations": len(
                        [
                            log
                            for log in recent_events
                            if log.event_type == AuditEventType.SECURITY_VIOLATION
                        ]
                    ),
                    "high_risk_events": len(
                        [log for log in recent_events if log.risk_score >= 0.7]
                    ),
                },
                "compliance_metrics": {
                    "total_compliance_reports": len(self.compliance_reports),
                    "frameworks_in_use": list(
                        set(
                            [
                                f.value
                                for tenant in self.tenants.values()
                                for f in tenant.compliance_frameworks
                            ]
                        )
                    ),
                },
                "performance_metrics": self.performance_metrics,
            }

            return enterprise_metrics

        except Exception as e:
            self.logger.error(f"Failed to get enterprise metrics: {e}")
            return {"error": str(e)}

    async def shutdown(self):
        """Shutdown enterprise manager"""
        try:
            self.logger.info("🛑 Shutting down Enterprise Manager...")

            # Generate final audit event
            for tenant_id in self.tenants.keys():
                await self.log_audit_event(
                    tenant_id=tenant_id,
                    user_id="system",
                    event_type=AuditEventType.SYSTEM_EVENT,
                    action="enterprise_manager_shutdown",
                    resource="system",
                    outcome="success",
                )

            self.logger.info("✅ Enterprise Manager shutdown complete")

        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")


# Global enterprise manager instance
_enterprise_manager_instance = None


async def get_enterprise_manager() -> TrustWrapperEnterpriseManager:
    """Get or create the global enterprise manager instance"""
    global _enterprise_manager_instance

    if _enterprise_manager_instance is None:
        _enterprise_manager_instance = TrustWrapperEnterpriseManager()
        await _enterprise_manager_instance.initialize()

    return _enterprise_manager_instance


# Utility functions for integration
async def require_tenant_access(
    tenant_id: str, user_id: str, enterprise_manager: TrustWrapperEnterpriseManager
) -> bool:
    """Check if user has access to tenant"""
    return user_id in enterprise_manager.tenant_users.get(tenant_id, set())


async def log_api_access(
    tenant_id: str,
    user_id: str,
    endpoint: str,
    outcome: str,
    ip_address: str = None,
    enterprise_manager: TrustWrapperEnterpriseManager = None,
):
    """Log API access for audit trail"""
    if not enterprise_manager:
        enterprise_manager = await get_enterprise_manager()

    await enterprise_manager.log_audit_event(
        tenant_id=tenant_id,
        user_id=user_id,
        event_type=AuditEventType.API_ACCESS,
        action="api_request",
        resource=endpoint,
        outcome=outcome,
        ip_address=ip_address,
        api_endpoint=endpoint,
    )


# Development server for testing
if __name__ == "__main__":

    async def demo_enterprise_system():
        """Demo the enterprise system"""
        print("🏢 TrustWrapper v3.0 Enterprise Integration Demo")
        print("=" * 60)

        # Initialize enterprise manager
        enterprise_manager = TrustWrapperEnterpriseManager()
        await enterprise_manager.initialize()

        # Demo multi-tenant operations
        print("✅ Enterprise Manager initialized")
        print(
            f"📊 Default tenant created: {list(enterprise_manager.tenants.keys())[0]}"
        )

        # Get enterprise metrics
        metrics = await enterprise_manager.get_enterprise_metrics()
        print(
            f"📈 Enterprise metrics: {metrics['tenant_metrics']['total_tenants']} tenants"
        )

        await enterprise_manager.shutdown()

    asyncio.run(demo_enterprise_system())

#!/usr/bin/env python3
"""
TrustWrapper v3.0 Authentication & Security System
Enterprise-grade security implementation for multi-chain AI verification
Task 3.2: Week 3 Phase 1 Implementation
"""

import asyncio
import hashlib
import ipaddress
import json
import logging
import secrets
import time
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import jwt
import redis.asyncio as redis
from cryptography.fernet import Fernet
from passlib.context import CryptContext

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels for different operations"""

    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"


class AuthenticationMethod(Enum):
    """Authentication methods supported"""

    API_KEY = "api_key"
    JWT_TOKEN = "jwt_token"
    OAUTH2 = "oauth2"
    CERTIFICATE = "certificate"
    MULTIFACTOR = "multifactor"


class RateLimitType(Enum):
    """Rate limiting types"""

    REQUESTS_PER_MINUTE = "requests_per_minute"
    REQUESTS_PER_HOUR = "requests_per_hour"
    REQUESTS_PER_DAY = "requests_per_day"
    BANDWIDTH_PER_MINUTE = "bandwidth_per_minute"


@dataclass
class UserCredentials:
    """User credentials and profile"""

    user_id: str
    username: str
    email: str
    password_hash: str
    api_keys: List[str]
    security_level: SecurityLevel
    authentication_methods: List[AuthenticationMethod]
    created_at: float
    last_login: Optional[float] = None
    is_active: bool = True
    failed_login_attempts: int = 0
    locked_until: Optional[float] = None
    permissions: List[str] = None

    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "security_level": self.security_level.value,
            "authentication_methods": [
                method.value for method in self.authentication_methods
            ],
        }


@dataclass
class APIKeyInfo:
    """API key information"""

    key_id: str
    user_id: str
    key_hash: str
    name: str
    permissions: List[str]
    rate_limits: Dict[str, int]
    created_at: float
    expires_at: Optional[float] = None
    last_used: Optional[float] = None
    is_active: bool = True
    usage_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RateLimitRule:
    """Rate limiting rule"""

    rule_id: str
    limit_type: RateLimitType
    max_requests: int
    window_seconds: int
    security_level: SecurityLevel
    endpoint_pattern: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "limit_type": self.limit_type.value,
            "security_level": self.security_level.value,
        }


class TrustWrapperSecurityManager:
    """
    Comprehensive security manager for TrustWrapper v3.0
    Handles authentication, authorization, rate limiting, and security monitoring
    """

    def __init__(
        self, redis_url: str = "redis://localhost:6379", jwt_secret: str = None
    ):
        self.logger = logging.getLogger(__name__)

        # Security configuration
        self.jwt_secret = jwt_secret or secrets.token_urlsafe(32)
        self.jwt_algorithm = "HS256"
        self.jwt_expiry_hours = 24

        # Password hashing
        self.pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

        # Encryption for sensitive data
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)

        # Redis for session management and rate limiting
        self.redis_url = redis_url
        self.redis_client = None

        # In-memory stores (would be database in production)
        self.users: Dict[str, UserCredentials] = {}
        self.api_keys: Dict[str, APIKeyInfo] = {}
        self.rate_limits: Dict[str, RateLimitRule] = {}
        self.blacklisted_ips: Set[str] = set()
        self.suspicious_activities: List[Dict[str, Any]] = []

        # Rate limiting counters
        self.rate_limit_counters: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.rate_limit_windows: Dict[str, float] = {}

        # Initialize default rate limits
        self._setup_default_rate_limits()

        # Security monitoring
        self.failed_login_attempts: Dict[str, List[float]] = defaultdict(list)
        self.suspicious_patterns: Dict[str, int] = defaultdict(int)

    async def initialize(self):
        """Initialize security manager"""
        try:
            self.logger.info("🔐 Initializing TrustWrapper Security Manager...")

            # Initialize Redis connection
            self.redis_client = redis.from_url(self.redis_url)
            await self.redis_client.ping()

            # Create default admin user
            await self._create_default_admin()

            self.logger.info("✅ Security Manager initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Security Manager: {e}")
            raise

    def _setup_default_rate_limits(self):
        """Setup default rate limiting rules"""
        default_limits = [
            RateLimitRule(
                rule_id="public_basic",
                limit_type=RateLimitType.REQUESTS_PER_MINUTE,
                max_requests=10,
                window_seconds=60,
                security_level=SecurityLevel.PUBLIC,
            ),
            RateLimitRule(
                rule_id="authenticated_basic",
                limit_type=RateLimitType.REQUESTS_PER_MINUTE,
                max_requests=100,
                window_seconds=60,
                security_level=SecurityLevel.AUTHENTICATED,
            ),
            RateLimitRule(
                rule_id="premium_enhanced",
                limit_type=RateLimitType.REQUESTS_PER_MINUTE,
                max_requests=500,
                window_seconds=60,
                security_level=SecurityLevel.PREMIUM,
            ),
            RateLimitRule(
                rule_id="enterprise_unlimited",
                limit_type=RateLimitType.REQUESTS_PER_MINUTE,
                max_requests=2000,
                window_seconds=60,
                security_level=SecurityLevel.ENTERPRISE,
            ),
            RateLimitRule(
                rule_id="verification_hourly",
                limit_type=RateLimitType.REQUESTS_PER_HOUR,
                max_requests=1000,
                window_seconds=3600,
                security_level=SecurityLevel.AUTHENTICATED,
                endpoint_pattern="/verify",
            ),
        ]

        for rule in default_limits:
            self.rate_limits[rule.rule_id] = rule

    async def _create_default_admin(self):
        """Create default admin user if not exists"""
        admin_id = "admin_001"
        if admin_id not in self.users:
            admin_password = secrets.token_urlsafe(16)

            admin_user = UserCredentials(
                user_id=admin_id,
                username="admin",
                email="admin@trustwrapper.io",
                password_hash=self.pwd_context.hash(admin_password),
                api_keys=[],
                security_level=SecurityLevel.ADMIN,
                authentication_methods=[
                    AuthenticationMethod.JWT_TOKEN,
                    AuthenticationMethod.API_KEY,
                ],
                created_at=time.time(),
                permissions=["*"],  # Full permissions
            )

            self.users[admin_id] = admin_user
            self.logger.info(
                f"🔑 Default admin created with password: {admin_password}"
            )

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        security_level: SecurityLevel = SecurityLevel.AUTHENTICATED,
    ) -> UserCredentials:
        """Create new user account"""
        try:
            # Check if user already exists
            for user in self.users.values():
                if user.username == username or user.email == email:
                    raise ValueError("User with this username or email already exists")

            # Generate user ID
            user_id = f"user_{int(time.time() * 1000)}_{secrets.token_hex(4)}"

            # Hash password
            password_hash = self.pwd_context.hash(password)

            # Create user
            user = UserCredentials(
                user_id=user_id,
                username=username,
                email=email,
                password_hash=password_hash,
                api_keys=[],
                security_level=security_level,
                authentication_methods=[AuthenticationMethod.JWT_TOKEN],
                created_at=time.time(),
                permissions=self._get_default_permissions(security_level),
            )

            self.users[user_id] = user

            # Create default API key
            api_key = await self.create_api_key(user_id, f"{username}_default_key")
            user.api_keys.append(api_key.key_id)

            self.logger.info(f"✅ User created: {username} ({security_level.value})")
            return user

        except Exception as e:
            self.logger.error(f"Failed to create user: {e}")
            raise

    def _get_default_permissions(self, security_level: SecurityLevel) -> List[str]:
        """Get default permissions for security level"""
        permission_map = {
            SecurityLevel.PUBLIC: ["read:health"],
            SecurityLevel.AUTHENTICATED: ["read:health", "write:verify", "read:oracle"],
            SecurityLevel.PREMIUM: [
                "read:health",
                "write:verify",
                "read:oracle",
                "write:consensus",
            ],
            SecurityLevel.ENTERPRISE: ["read:*", "write:*", "admin:monitor"],
            SecurityLevel.ADMIN: ["*"],
        }
        return permission_map.get(security_level, [])

    async def authenticate_password(
        self, username: str, password: str, ip_address: str = None
    ) -> Optional[UserCredentials]:
        """Authenticate user with username/password"""
        try:
            # Check for suspicious activity
            if ip_address and await self._is_suspicious_activity(
                ip_address, "login_attempt"
            ):
                self.logger.warning(f"🚨 Suspicious login attempt from {ip_address}")
                return None

            # Find user
            user = None
            for u in self.users.values():
                if u.username == username:
                    user = u
                    break

            if not user:
                await self._log_failed_login(username, ip_address, "user_not_found")
                return None

            # Check if account is locked
            if user.locked_until and time.time() < user.locked_until:
                await self._log_failed_login(username, ip_address, "account_locked")
                return None

            # Check if account is active
            if not user.is_active:
                await self._log_failed_login(username, ip_address, "account_inactive")
                return None

            # Verify password
            if not self.pwd_context.verify(password, user.password_hash):
                user.failed_login_attempts += 1

                # Lock account after 5 failed attempts
                if user.failed_login_attempts >= 5:
                    user.locked_until = time.time() + 3600  # Lock for 1 hour
                    self.logger.warning(f"🔒 Account locked: {username}")

                await self._log_failed_login(username, ip_address, "invalid_password")
                return None

            # Successful login
            user.last_login = time.time()
            user.failed_login_attempts = 0
            user.locked_until = None

            self.logger.info(f"✅ Successful login: {username}")
            return user

        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            return None

    async def authenticate_api_key(
        self, api_key: str, ip_address: str = None
    ) -> Optional[Tuple[UserCredentials, APIKeyInfo]]:
        """Authenticate user with API key"""
        try:
            # Hash the provided key
            key_hash = hashlib.sha256(api_key.encode()).hexdigest()

            # Find matching API key
            api_key_info = None
            for key_info in self.api_keys.values():
                if key_info.key_hash == key_hash:
                    api_key_info = key_info
                    break

            if not api_key_info:
                await self._log_security_event(
                    "invalid_api_key", {"key_prefix": api_key[:8], "ip": ip_address}
                )
                return None

            # Check if key is active
            if not api_key_info.is_active:
                return None

            # Check if key has expired
            if api_key_info.expires_at and time.time() > api_key_info.expires_at:
                return None

            # Get user
            user = self.users.get(api_key_info.user_id)
            if not user or not user.is_active:
                return None

            # Update usage stats
            api_key_info.last_used = time.time()
            api_key_info.usage_count += 1

            return user, api_key_info

        except Exception as e:
            self.logger.error(f"API key authentication error: {e}")
            return None

    async def create_jwt_token(
        self, user: UserCredentials, expires_hours: int = None
    ) -> str:
        """Create JWT token for user"""
        try:
            expiry = expires_hours or self.jwt_expiry_hours
            exp_time = datetime.utcnow() + timedelta(hours=expiry)

            payload = {
                "user_id": user.user_id,
                "username": user.username,
                "security_level": user.security_level.value,
                "permissions": user.permissions,
                "iat": datetime.utcnow(),
                "exp": exp_time,
            }

            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

            # Store token in Redis for session management
            if self.redis_client:
                await self.redis_client.setex(
                    f"jwt_session:{user.user_id}:{token[-8:]}",
                    expiry * 3600,
                    json.dumps(
                        {
                            "user_id": user.user_id,
                            "created_at": time.time(),
                            "expires_at": exp_time.timestamp(),
                        }
                    ),
                )

            return token

        except Exception as e:
            self.logger.error(f"JWT token creation error: {e}")
            raise

    async def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token"""
        try:
            # Decode token
            payload = jwt.decode(
                token, self.jwt_secret, algorithms=[self.jwt_algorithm]
            )

            # Check if session exists in Redis
            if self.redis_client:
                session_key = f"jwt_session:{payload['user_id']}:{token[-8:]}"
                session_data = await self.redis_client.get(session_key)

                if not session_data:
                    return None

            # Get user
            user = self.users.get(payload["user_id"])
            if not user or not user.is_active:
                return None

            return {"user": user, "payload": payload}

        except jwt.ExpiredSignatureError:
            self.logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid JWT token: {e}")
            return None
        except Exception as e:
            self.logger.error(f"JWT verification error: {e}")
            return None

    async def create_api_key(
        self,
        user_id: str,
        key_name: str,
        permissions: List[str] = None,
        expires_days: int = None,
    ) -> APIKeyInfo:
        """Create new API key for user"""
        try:
            user = self.users.get(user_id)
            if not user:
                raise ValueError("User not found")

            # Generate API key
            raw_key = f"tw_{secrets.token_urlsafe(32)}"
            key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

            # Create API key info
            key_info = APIKeyInfo(
                key_id=f"key_{int(time.time() * 1000)}_{secrets.token_hex(4)}",
                user_id=user_id,
                key_hash=key_hash,
                name=key_name,
                permissions=permissions or user.permissions.copy(),
                rate_limits=self._get_default_rate_limits(user.security_level),
                created_at=time.time(),
                expires_at=(
                    time.time() + (expires_days * 86400) if expires_days else None
                ),
            )

            self.api_keys[key_info.key_id] = key_info

            self.logger.info(f"✅ API key created: {key_name} for {user.username}")

            # Return the raw key (only time it's available)
            key_info_copy = APIKeyInfo(**asdict(key_info))
            key_info_copy.key_hash = raw_key  # Temporarily store raw key for return

            return key_info_copy

        except Exception as e:
            self.logger.error(f"Failed to create API key: {e}")
            raise

    def _get_default_rate_limits(self, security_level: SecurityLevel) -> Dict[str, int]:
        """Get default rate limits for security level"""
        rate_limit_map = {
            SecurityLevel.PUBLIC: {"requests_per_minute": 10, "requests_per_hour": 100},
            SecurityLevel.AUTHENTICATED: {
                "requests_per_minute": 100,
                "requests_per_hour": 1000,
            },
            SecurityLevel.PREMIUM: {
                "requests_per_minute": 500,
                "requests_per_hour": 5000,
            },
            SecurityLevel.ENTERPRISE: {
                "requests_per_minute": 2000,
                "requests_per_hour": 20000,
            },
            SecurityLevel.ADMIN: {
                "requests_per_minute": 10000,
                "requests_per_hour": 100000,
            },
        }
        return rate_limit_map.get(security_level, {"requests_per_minute": 10})

    async def check_rate_limit(
        self, identifier: str, security_level: SecurityLevel, endpoint: str = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """Check if request is within rate limits"""
        try:
            current_time = time.time()

            # Find applicable rate limit rules
            applicable_rules = []
            for rule in self.rate_limits.values():
                if rule.security_level == security_level:
                    if not rule.endpoint_pattern or (
                        endpoint and rule.endpoint_pattern in endpoint
                    ):
                        applicable_rules.append(rule)

            # Check each applicable rule
            for rule in applicable_rules:
                window_key = f"{identifier}:{rule.rule_id}"
                window_start_key = f"{window_key}:start"

                # Initialize window if needed
                if window_key not in self.rate_limit_counters:
                    self.rate_limit_counters[window_key] = defaultdict(int)
                    self.rate_limit_windows[window_start_key] = current_time

                # Check if window has expired
                window_start = self.rate_limit_windows.get(
                    window_start_key, current_time
                )
                if current_time - window_start >= rule.window_seconds:
                    # Reset window
                    self.rate_limit_counters[window_key] = defaultdict(int)
                    self.rate_limit_windows[window_start_key] = current_time

                # Check current count
                current_count = self.rate_limit_counters[window_key]["requests"]

                if current_count >= rule.max_requests:
                    # Rate limit exceeded
                    return False, {
                        "rate_limited": True,
                        "rule_id": rule.rule_id,
                        "max_requests": rule.max_requests,
                        "window_seconds": rule.window_seconds,
                        "current_count": current_count,
                        "reset_time": window_start + rule.window_seconds,
                    }

            # Update counters for all applicable rules
            for rule in applicable_rules:
                window_key = f"{identifier}:{rule.rule_id}"
                self.rate_limit_counters[window_key]["requests"] += 1

            return True, {"rate_limited": False}

        except Exception as e:
            self.logger.error(f"Rate limit check error: {e}")
            # Allow request on error (fail open)
            return True, {"error": str(e)}

    async def check_permissions(
        self, user: UserCredentials, required_permission: str
    ) -> bool:
        """Check if user has required permission"""
        try:
            # Admin users have all permissions
            if user.security_level == SecurityLevel.ADMIN or "*" in user.permissions:
                return True

            # Check exact permission match
            if required_permission in user.permissions:
                return True

            # Check wildcard permissions
            for permission in user.permissions:
                if permission.endswith("*"):
                    permission_prefix = permission[:-1]
                    if required_permission.startswith(permission_prefix):
                        return True

            return False

        except Exception as e:
            self.logger.error(f"Permission check error: {e}")
            return False

    async def _is_suspicious_activity(
        self, ip_address: str, activity_type: str
    ) -> bool:
        """Check if activity from IP is suspicious"""
        try:
            # Check if IP is blacklisted
            if ip_address in self.blacklisted_ips:
                return True

            # Check if IP is private/internal
            try:
                ip = ipaddress.ip_address(ip_address)
                if ip.is_private or ip.is_loopback:
                    return False  # Allow internal IPs
            except ValueError:
                pass

            # Check failed login attempts from this IP
            current_time = time.time()
            recent_failures = [
                timestamp
                for timestamp in self.failed_login_attempts[ip_address]
                if current_time - timestamp < 3600  # Last hour
            ]

            # More than 10 failed attempts in an hour is suspicious
            if len(recent_failures) > 10:
                await self._log_security_event(
                    "suspicious_activity",
                    {
                        "ip": ip_address,
                        "activity": activity_type,
                        "recent_failures": len(recent_failures),
                    },
                )
                return True

            return False

        except Exception as e:
            self.logger.error(f"Suspicious activity check error: {e}")
            return False

    async def _log_failed_login(self, identifier: str, ip_address: str, reason: str):
        """Log failed login attempt"""
        try:
            current_time = time.time()

            # Log to IP-based tracking
            if ip_address:
                self.failed_login_attempts[ip_address].append(current_time)

                # Keep only recent attempts (last 24 hours)
                self.failed_login_attempts[ip_address] = [
                    timestamp
                    for timestamp in self.failed_login_attempts[ip_address]
                    if current_time - timestamp < 86400
                ]

            # Log security event
            await self._log_security_event(
                "failed_login",
                {
                    "identifier": identifier,
                    "ip": ip_address,
                    "reason": reason,
                    "timestamp": current_time,
                },
            )

        except Exception as e:
            self.logger.error(f"Failed login logging error: {e}")

    async def _log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security event"""
        try:
            event = {"type": event_type, "timestamp": time.time(), "details": details}

            self.suspicious_activities.append(event)

            # Keep only recent events (last 7 days)
            cutoff_time = time.time() - (7 * 86400)
            self.suspicious_activities = [
                event
                for event in self.suspicious_activities
                if event["timestamp"] > cutoff_time
            ]

            # Log to Redis for persistent storage
            if self.redis_client:
                await self.redis_client.lpush("security_events", json.dumps(event))
                await self.redis_client.ltrim(
                    "security_events", 0, 9999
                )  # Keep last 10k events

            self.logger.warning(f"🔒 Security event: {event_type} - {details}")

        except Exception as e:
            self.logger.error(f"Security event logging error: {e}")

    async def get_security_metrics(self) -> Dict[str, Any]:
        """Get security metrics and statistics"""
        try:
            current_time = time.time()

            # Recent failed logins (last 24 hours)
            recent_failures = 0
            for ip_failures in self.failed_login_attempts.values():
                recent_failures += len(
                    [
                        timestamp
                        for timestamp in ip_failures
                        if current_time - timestamp < 86400
                    ]
                )

            # Active sessions (approximate)
            active_sessions = len(
                [
                    user
                    for user in self.users.values()
                    if user.last_login and current_time - user.last_login < 3600
                ]
            )

            # Security events by type (last 24 hours)
            recent_events = [
                event
                for event in self.suspicious_activities
                if current_time - event["timestamp"] < 86400
            ]

            event_counts = defaultdict(int)
            for event in recent_events:
                event_counts[event["type"]] += 1

            return {
                "timestamp": current_time,
                "total_users": len(self.users),
                "active_users": len([u for u in self.users.values() if u.is_active]),
                "total_api_keys": len(self.api_keys),
                "active_api_keys": len(
                    [k for k in self.api_keys.values() if k.is_active]
                ),
                "recent_failed_logins": recent_failures,
                "active_sessions": active_sessions,
                "blacklisted_ips": len(self.blacklisted_ips),
                "security_events_24h": dict(event_counts),
                "total_security_events": len(self.suspicious_activities),
                "rate_limit_rules": len(self.rate_limits),
            }

        except Exception as e:
            self.logger.error(f"Security metrics error: {e}")
            return {"error": str(e)}

    async def revoke_api_key(self, key_id: str, user_id: str = None) -> bool:
        """Revoke API key"""
        try:
            key_info = self.api_keys.get(key_id)
            if not key_info:
                return False

            # Check if user has permission to revoke this key
            if user_id and key_info.user_id != user_id:
                user = self.users.get(user_id)
                if not user or user.security_level != SecurityLevel.ADMIN:
                    return False

            key_info.is_active = False

            self.logger.info(f"🔑 API key revoked: {key_info.name}")
            return True

        except Exception as e:
            self.logger.error(f"API key revocation error: {e}")
            return False

    async def blacklist_ip(self, ip_address: str, reason: str = "Suspicious activity"):
        """Add IP to blacklist"""
        try:
            self.blacklisted_ips.add(ip_address)

            await self._log_security_event(
                "ip_blacklisted", {"ip": ip_address, "reason": reason}
            )

            self.logger.warning(f"🚫 IP blacklisted: {ip_address} - {reason}")

        except Exception as e:
            self.logger.error(f"IP blacklisting error: {e}")

    async def shutdown(self):
        """Shutdown security manager"""
        try:
            self.logger.info("🛑 Shutting down Security Manager...")

            if self.redis_client:
                await self.redis_client.close()

            self.logger.info("✅ Security Manager shutdown complete")

        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")


# Global security manager instance
_security_manager_instance = None


async def get_security_manager(
    redis_url: str = "redis://localhost:6379", jwt_secret: str = None
) -> TrustWrapperSecurityManager:
    """Get or create the global security manager instance"""
    global _security_manager_instance

    if _security_manager_instance is None:
        _security_manager_instance = TrustWrapperSecurityManager(redis_url, jwt_secret)
        await _security_manager_instance.initialize()

    return _security_manager_instance


# Utility functions for FastAPI integration
async def get_current_user_from_token(
    token: str, security_manager: TrustWrapperSecurityManager
) -> Optional[UserCredentials]:
    """Extract user from JWT token for FastAPI dependency"""
    token_data = await security_manager.verify_jwt_token(token)
    return token_data["user"] if token_data else None


async def get_current_user_from_api_key(
    api_key: str, security_manager: TrustWrapperSecurityManager
) -> Optional[UserCredentials]:
    """Extract user from API key for FastAPI dependency"""
    auth_result = await security_manager.authenticate_api_key(api_key)
    return auth_result[0] if auth_result else None


def require_permission(permission: str):
    """Decorator to require specific permission for endpoint"""

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # This would be implemented as FastAPI dependency
            # For now, it's a placeholder for the concept
            return await func(*args, **kwargs)

        return wrapper

    return decorator


# Development server for testing
if __name__ == "__main__":

    async def demo_security_system():
        """Demo the security system"""
        print("🔐 TrustWrapper v3.0 Security System Demo")
        print("=" * 50)

        # Initialize security manager
        security_manager = TrustWrapperSecurityManager()
        await security_manager.initialize()

        # Create test user
        user = await security_manager.create_user(
            "testuser", "test@example.com", "securepassword123", SecurityLevel.PREMIUM
        )

        print(f"✅ User created: {user.username}")

        # Test authentication
        auth_user = await security_manager.authenticate_password(
            "testuser", "securepassword123"
        )
        if auth_user:
            print("✅ Password authentication successful")

            # Create JWT token
            jwt_token = await security_manager.create_jwt_token(auth_user)
            print(f"✅ JWT token created: {jwt_token[:20]}...")

            # Verify JWT token
            token_data = await security_manager.verify_jwt_token(jwt_token)
            if token_data:
                print("✅ JWT token verification successful")

        # Test rate limiting
        allowed, rate_info = await security_manager.check_rate_limit(
            "test_client", SecurityLevel.PREMIUM, "/verify"
        )
        print(f"✅ Rate limit check: {'Allowed' if allowed else 'Blocked'}")

        # Get security metrics
        metrics = await security_manager.get_security_metrics()
        print(
            f"📊 Security metrics: {metrics['total_users']} users, {metrics['total_api_keys']} API keys"
        )

        await security_manager.shutdown()

    asyncio.run(demo_security_system())

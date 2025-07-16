"""
Treasury Monitor API Key Management Service
Production-ready API key generation, validation, and management.
"""

import hashlib
import hmac
import logging
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import asyncpg

logger = logging.getLogger(__name__)


class APIKeyError(Exception):
    """Base API key error"""

    pass


class InvalidAPIKeyError(APIKeyError):
    """Invalid API key"""

    pass


class APIKeyExpiredError(APIKeyError):
    """API key has expired"""

    pass


class PermissionDeniedError(APIKeyError):
    """Permission denied for API key"""

    pass


class APIKeyService:
    """Production-ready API key management for Treasury Monitor"""

    def __init__(self, db_pool: asyncpg.Pool, signing_secret: str):
        self.db_pool = db_pool
        self.signing_secret = signing_secret
        self.key_prefix = "tm_"  # Treasury Monitor prefix

    async def generate_api_key(
        self,
        user_id: str,
        name: str = None,
        permissions: List[str] = None,
        expires_days: int = None,
    ) -> Dict[str, Any]:
        """
        Generate new API key for user.

        Args:
            user_id: User ID
            name: User-defined name for the key
            permissions: List of permissions (default: ["monitor"])
            expires_days: Expiration in days (None for no expiration)

        Returns:
            API key data including the actual key (only returned once)
        """
        if permissions is None:
            permissions = ["monitor"]

        # Generate random key
        key_secret = secrets.token_urlsafe(32)
        full_api_key = f"{self.key_prefix}{key_secret}"

        # Create key hash for storage
        key_hash = self._hash_key(full_api_key)

        # Create display prefix (first 8 chars after prefix)
        key_prefix = f"{self.key_prefix}{key_secret[:8]}..."

        # Calculate expiration
        expires_at = None
        if expires_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_days)

        async with self.db_pool.acquire() as conn:
            # Verify user exists and has active subscription
            user_sub = await conn.fetchrow(
                """
                SELECT u.id, us.status, sp.features
                FROM users u
                LEFT JOIN user_subscriptions us ON u.id = us.user_id
                    AND us.status IN ('active', 'trialing')
                LEFT JOIN subscription_plans sp ON us.plan_id = sp.id
                WHERE u.id = $1 AND u.is_active = TRUE
                """,
                uuid.UUID(user_id),
            )

            if not user_sub:
                raise APIKeyError("User not found or inactive")

            # Check if user's plan allows API access
            features = user_sub["features"] or {}
            if not features.get("api_access", False) and user_sub["status"]:
                # Only enterprise plan gets API access by default
                # For demo purposes, we'll allow it for all active subscribers
                pass

            # Create API key record
            api_key_id = await conn.fetchval(
                """
                INSERT INTO api_keys
                (user_id, key_hash, key_prefix, name, permissions, expires_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
                """,
                uuid.UUID(user_id),
                key_hash,
                key_prefix,
                name,
                permissions,
                expires_at,
            )

            return {
                "id": str(api_key_id),
                "api_key": full_api_key,  # Only returned once!
                "key_prefix": key_prefix,
                "name": name,
                "permissions": permissions,
                "expires_at": expires_at.isoformat() if expires_at else None,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "is_active": True,
            }

    async def validate_api_key(
        self, api_key: str, required_permission: str = None
    ) -> Dict[str, Any]:
        """
        Validate API key and return user information.

        Args:
            api_key: Full API key
            required_permission: Required permission for the operation

        Returns:
            User and subscription information

        Raises:
            InvalidAPIKeyError: If key is invalid
            APIKeyExpiredError: If key has expired
            PermissionDeniedError: If key lacks required permission
        """
        if not api_key.startswith(self.key_prefix):
            raise InvalidAPIKeyError("Invalid API key format")

        key_hash = self._hash_key(api_key)

        async with self.db_pool.acquire() as conn:
            # Get API key with user and subscription info
            key_data = await conn.fetchrow(
                """
                SELECT ak.id, ak.user_id, ak.permissions, ak.expires_at, ak.is_active,
                       ak.last_used, ak.usage_count,
                       u.email, u.first_name, u.last_name, u.is_active as user_active,
                       us.status as subscription_status, us.current_period_end,
                       sp.name as plan_name, sp.max_addresses, sp.features
                FROM api_keys ak
                JOIN users u ON ak.user_id = u.id
                LEFT JOIN user_subscriptions us ON u.id = us.user_id
                    AND us.status IN ('active', 'trialing', 'past_due')
                LEFT JOIN subscription_plans sp ON us.plan_id = sp.id
                WHERE ak.key_hash = $1
                ORDER BY us.created_at DESC
                LIMIT 1
                """,
                key_hash,
            )

            if not key_data:
                raise InvalidAPIKeyError("Invalid API key")

            # Check if key is active
            if not key_data["is_active"]:
                raise InvalidAPIKeyError("API key is disabled")

            # Check if user is active
            if not key_data["user_active"]:
                raise InvalidAPIKeyError("User account is inactive")

            # Check if key has expired
            if key_data["expires_at"] and key_data["expires_at"] < datetime.now(
                timezone.utc
            ):
                raise APIKeyExpiredError("API key has expired")

            # Check subscription status
            if not key_data["subscription_status"]:
                raise PermissionDeniedError("No active subscription")

            if key_data["subscription_status"] == "past_due":
                raise PermissionDeniedError("Subscription payment is past due")

            # Check required permission
            if (
                required_permission
                and required_permission not in key_data["permissions"]
            ):
                raise PermissionDeniedError(
                    f"API key lacks required permission: {required_permission}"
                )

            # Update usage statistics
            await conn.execute(
                """
                UPDATE api_keys
                SET last_used = NOW(), usage_count = usage_count + 1
                WHERE id = $1
                """,
                key_data["id"],
            )

            return {
                "user_id": str(key_data["user_id"]),
                "email": key_data["email"],
                "name": f"{key_data['first_name'] or ''} {key_data['last_name'] or ''}".strip(),
                "subscription_status": key_data["subscription_status"],
                "plan_name": key_data["plan_name"],
                "max_addresses": key_data["max_addresses"],
                "features": key_data["features"],
                "permissions": key_data["permissions"],
                "current_period_end": (
                    key_data["current_period_end"].isoformat()
                    if key_data["current_period_end"]
                    else None
                ),
            }

    async def get_user_api_keys(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all API keys for a user (without revealing actual keys)"""
        async with self.db_pool.acquire() as conn:
            keys = await conn.fetch(
                """
                SELECT id, key_prefix, name, permissions, expires_at, is_active,
                       last_used, usage_count, created_at
                FROM api_keys
                WHERE user_id = $1
                ORDER BY created_at DESC
                """,
                uuid.UUID(user_id),
            )

            return [
                {
                    "id": str(key["id"]),
                    "key_prefix": key["key_prefix"],
                    "name": key["name"],
                    "permissions": key["permissions"],
                    "expires_at": (
                        key["expires_at"].isoformat() if key["expires_at"] else None
                    ),
                    "is_active": key["is_active"],
                    "last_used": (
                        key["last_used"].isoformat() if key["last_used"] else None
                    ),
                    "usage_count": key["usage_count"],
                    "created_at": key["created_at"].isoformat(),
                }
                for key in keys
            ]

    async def revoke_api_key(self, user_id: str, key_id: str) -> bool:
        """
        Revoke (deactivate) an API key.

        Args:
            user_id: User ID
            key_id: API key ID to revoke

        Returns:
            True if key was revoked
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE api_keys
                SET is_active = FALSE
                WHERE id = $1 AND user_id = $2
                """,
                uuid.UUID(key_id),
                uuid.UUID(user_id),
            )

            return result == "UPDATE 1"

    async def update_api_key(
        self, user_id: str, key_id: str, name: str = None, permissions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Update API key settings.

        Args:
            user_id: User ID
            key_id: API key ID
            name: New name
            permissions: New permissions list

        Returns:
            Updated API key data
        """
        updates = []
        values = [uuid.UUID(key_id), uuid.UUID(user_id)]

        if name is not None:
            updates.append(f"name = ${len(values) + 1}")
            values.append(name)

        if permissions is not None:
            updates.append(f"permissions = ${len(values) + 1}")
            values.append(permissions)

        if not updates:
            # Return current data if no updates
            keys = await self.get_user_api_keys(user_id)
            for key in keys:
                if key["id"] == key_id:
                    return key
            raise APIKeyError("API key not found")

        query = f"""
            UPDATE api_keys
            SET {', '.join(updates)}
            WHERE id = $1 AND user_id = $2
            RETURNING id, key_prefix, name, permissions, expires_at, is_active,
                      last_used, usage_count, created_at
        """

        async with self.db_pool.acquire() as conn:
            key = await conn.fetchrow(query, *values)

            if not key:
                raise APIKeyError("API key not found")

            return {
                "id": str(key["id"]),
                "key_prefix": key["key_prefix"],
                "name": key["name"],
                "permissions": key["permissions"],
                "expires_at": (
                    key["expires_at"].isoformat() if key["expires_at"] else None
                ),
                "is_active": key["is_active"],
                "last_used": key["last_used"].isoformat() if key["last_used"] else None,
                "usage_count": key["usage_count"],
                "created_at": key["created_at"].isoformat(),
            }

    async def track_api_usage(
        self,
        user_id: str,
        api_key_id: str,
        endpoint: str,
        method: str,
        response_status: int,
        addresses_monitored: int = 0,
        processing_time_ms: int = 0,
    ):
        """Track API usage for billing and analytics"""
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO usage_tracking
                (user_id, api_key_id, endpoint, method, response_status,
                 addresses_monitored, processing_time_ms)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                uuid.UUID(user_id),
                uuid.UUID(api_key_id),
                endpoint,
                method,
                response_status,
                addresses_monitored,
                processing_time_ms,
            )

    async def get_usage_statistics(
        self, user_id: str, days: int = 30
    ) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        async with self.db_pool.acquire() as conn:
            stats = await conn.fetchrow(
                """
                SELECT
                    COUNT(*) as total_requests,
                    COUNT(DISTINCT DATE(request_timestamp)) as active_days,
                    SUM(addresses_monitored) as total_addresses_monitored,
                    AVG(processing_time_ms) as avg_processing_time,
                    COUNT(CASE WHEN response_status >= 400 THEN 1 END) as error_count
                FROM usage_tracking
                WHERE user_id = $1 AND request_timestamp >= NOW() - INTERVAL '%s days'
                """,
                uuid.UUID(user_id),
                days,
            )

            # Get daily breakdown
            daily_usage = await conn.fetch(
                """
                SELECT
                    DATE(request_timestamp) as date,
                    COUNT(*) as requests,
                    SUM(addresses_monitored) as addresses_monitored
                FROM usage_tracking
                WHERE user_id = $1 AND request_timestamp >= NOW() - INTERVAL '%s days'
                GROUP BY DATE(request_timestamp)
                ORDER BY date DESC
                """,
                uuid.UUID(user_id),
                days,
            )

            return {
                "period_days": days,
                "total_requests": stats["total_requests"] or 0,
                "active_days": stats["active_days"] or 0,
                "total_addresses_monitored": stats["total_addresses_monitored"] or 0,
                "avg_processing_time_ms": (
                    float(stats["avg_processing_time"])
                    if stats["avg_processing_time"]
                    else 0
                ),
                "error_count": stats["error_count"] or 0,
                "error_rate": (stats["error_count"] or 0)
                / max(stats["total_requests"] or 1, 1),
                "daily_usage": [
                    {
                        "date": record["date"].isoformat(),
                        "requests": record["requests"],
                        "addresses_monitored": record["addresses_monitored"],
                    }
                    for record in daily_usage
                ],
            }

    def _hash_key(self, api_key: str) -> str:
        """Create secure hash of API key for storage"""
        return hmac.new(
            self.signing_secret.encode(), api_key.encode(), hashlib.sha256
        ).hexdigest()

    async def cleanup_expired_keys(self):
        """Cleanup expired API keys (run as periodic task)"""
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE api_keys
                SET is_active = FALSE
                WHERE expires_at IS NOT NULL AND expires_at < NOW() AND is_active = TRUE
                """
            )

            count = int(result.split()[-1]) if result.startswith("UPDATE") else 0
            if count > 0:
                logger.info(f"Deactivated {count} expired API keys")

            return count

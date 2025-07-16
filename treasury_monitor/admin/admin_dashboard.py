"""
Treasury Monitor Admin Dashboard
Simple admin interface for customer and subscription management.
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

import asyncpg
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)


class AdminDashboard:
    """Simple admin dashboard for Treasury Monitor"""

    def __init__(self, db_pool: asyncpg.Pool):
        self.db_pool = db_pool

    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get high-level dashboard statistics"""
        async with self.db_pool.acquire() as conn:
            # User statistics
            user_stats = await conn.fetchrow(
                """
                SELECT
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN created_at >= NOW() - INTERVAL '30 days' THEN 1 END) as new_users_30d,
                    COUNT(CASE WHEN last_login >= NOW() - INTERVAL '7 days' THEN 1 END) as active_users_7d,
                    COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_users
                FROM users
                WHERE is_active = TRUE
                """
            )

            # Subscription statistics
            sub_stats = await conn.fetchrow(
                """
                SELECT
                    COUNT(*) as total_subscriptions,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_subscriptions,
                    COUNT(CASE WHEN status = 'trialing' THEN 1 END) as trial_subscriptions,
                    COUNT(CASE WHEN status = 'past_due' THEN 1 END) as past_due_subscriptions,
                    COUNT(CASE WHEN cancel_at_period_end = TRUE THEN 1 END) as canceling_subscriptions
                FROM user_subscriptions
                """
            )

            # Revenue statistics (last 30 days)
            revenue_stats = await conn.fetchrow(
                """
                SELECT
                    COUNT(*) as total_payments,
                    SUM(amount_cents) as total_revenue_cents,
                    AVG(amount_cents) as avg_payment_cents
                FROM payment_history
                WHERE status = 'succeeded' AND created_at >= NOW() - INTERVAL '30 days'
                """
            )

            # API usage statistics
            api_stats = await conn.fetchrow(
                """
                SELECT
                    COUNT(*) as total_api_calls,
                    COUNT(DISTINCT user_id) as unique_api_users,
                    AVG(processing_time_ms) as avg_processing_time,
                    COUNT(CASE WHEN response_status >= 400 THEN 1 END) as error_count
                FROM usage_tracking
                WHERE request_timestamp >= NOW() - INTERVAL '7 days'
                """
            )

            return {
                "users": {
                    "total": user_stats["total_users"] or 0,
                    "new_30d": user_stats["new_users_30d"] or 0,
                    "active_7d": user_stats["active_users_7d"] or 0,
                    "verified": user_stats["verified_users"] or 0,
                },
                "subscriptions": {
                    "total": sub_stats["total_subscriptions"] or 0,
                    "active": sub_stats["active_subscriptions"] or 0,
                    "trial": sub_stats["trial_subscriptions"] or 0,
                    "past_due": sub_stats["past_due_subscriptions"] or 0,
                    "canceling": sub_stats["canceling_subscriptions"] or 0,
                },
                "revenue": {
                    "total_payments": revenue_stats["total_payments"] or 0,
                    "total_revenue_dollars": (revenue_stats["total_revenue_cents"] or 0)
                    / 100,
                    "avg_payment_dollars": (revenue_stats["avg_payment_cents"] or 0)
                    / 100,
                },
                "api_usage": {
                    "total_calls": api_stats["total_api_calls"] or 0,
                    "unique_users": api_stats["unique_api_users"] or 0,
                    "avg_processing_time": float(api_stats["avg_processing_time"] or 0),
                    "error_count": api_stats["error_count"] or 0,
                    "error_rate": (api_stats["error_count"] or 0)
                    / max(api_stats["total_api_calls"] or 1, 1),
                },
            }

    async def get_recent_users(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recently registered users"""
        async with self.db_pool.acquire() as conn:
            users = await conn.fetch(
                """
                SELECT u.id, u.email, u.first_name, u.last_name, u.company,
                       u.created_at, u.last_login, u.email_verified,
                       us.status as subscription_status, sp.name as plan_name,
                       COUNT(ak.id) as api_key_count
                FROM users u
                LEFT JOIN user_subscriptions us ON u.id = us.user_id
                    AND us.status IN ('active', 'trialing', 'past_due')
                LEFT JOIN subscription_plans sp ON us.plan_id = sp.id
                LEFT JOIN api_keys ak ON u.id = ak.user_id AND ak.is_active = TRUE
                WHERE u.is_active = TRUE
                GROUP BY u.id, us.status, sp.name
                ORDER BY u.created_at DESC
                LIMIT $1
                """,
                limit,
            )

            return [
                {
                    "id": str(user["id"]),
                    "email": user["email"],
                    "name": f"{user['first_name'] or ''} {user['last_name'] or ''}".strip(),
                    "company": user["company"],
                    "created_at": user["created_at"].isoformat(),
                    "last_login": (
                        user["last_login"].isoformat() if user["last_login"] else None
                    ),
                    "email_verified": user["email_verified"],
                    "subscription_status": user["subscription_status"],
                    "plan_name": user["plan_name"],
                    "api_key_count": user["api_key_count"],
                }
                for user in users
            ]

    async def get_subscription_metrics(self) -> Dict[str, Any]:
        """Get subscription conversion and churn metrics"""
        async with self.db_pool.acquire() as conn:
            # Trial to paid conversion rate
            trial_conversion = await conn.fetchrow(
                """
                WITH trial_users AS (
                    SELECT user_id, MIN(created_at) as trial_start
                    FROM user_subscriptions
                    WHERE status = 'trialing'
                    GROUP BY user_id
                ),
                converted_users AS (
                    SELECT tu.user_id
                    FROM trial_users tu
                    JOIN user_subscriptions us ON tu.user_id = us.user_id
                    WHERE us.status = 'active' AND us.created_at > tu.trial_start
                )
                SELECT
                    COUNT(trial_users.user_id) as total_trials,
                    COUNT(converted_users.user_id) as converted_trials
                FROM trial_users
                LEFT JOIN converted_users ON trial_users.user_id = converted_users.user_id
                """
            )

            # Monthly recurring revenue by plan
            mrr_by_plan = await conn.fetch(
                """
                SELECT sp.name, sp.price_cents, COUNT(us.id) as subscriber_count,
                       (sp.price_cents * COUNT(us.id)) as monthly_revenue_cents
                FROM subscription_plans sp
                LEFT JOIN user_subscriptions us ON sp.id = us.plan_id AND us.status = 'active'
                WHERE sp.is_active = TRUE
                GROUP BY sp.id, sp.name, sp.price_cents
                ORDER BY sp.price_cents
                """
            )

            # Churn rate (subscriptions cancelled in last 30 days)
            churn_data = await conn.fetchrow(
                """
                SELECT
                    COUNT(CASE WHEN canceled_at >= NOW() - INTERVAL '30 days' THEN 1 END) as churned_30d,
                    COUNT(CASE WHEN status = 'active' OR canceled_at >= NOW() - INTERVAL '30 days' THEN 1 END) as total_base
                FROM user_subscriptions
                """
            )

            total_trials = trial_conversion["total_trials"] or 0
            converted_trials = trial_conversion["converted_trials"] or 0
            conversion_rate = (
                (converted_trials / max(total_trials, 1)) if total_trials > 0 else 0
            )

            total_base = churn_data["total_base"] or 0
            churned_30d = churn_data["churned_30d"] or 0
            churn_rate = (churned_30d / max(total_base, 1)) if total_base > 0 else 0

            total_mrr = sum(plan["monthly_revenue_cents"] for plan in mrr_by_plan) / 100

            return {
                "trial_conversion_rate": conversion_rate,
                "monthly_churn_rate": churn_rate,
                "total_mrr": total_mrr,
                "mrr_by_plan": [
                    {
                        "plan_name": plan["name"],
                        "price_dollars": plan["price_cents"] / 100,
                        "subscriber_count": plan["subscriber_count"],
                        "monthly_revenue": plan["monthly_revenue_cents"] / 100,
                    }
                    for plan in mrr_by_plan
                ],
            }

    async def get_user_details(self, user_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific user"""
        async with self.db_pool.acquire() as conn:
            # User basic info
            user = await conn.fetchrow(
                """
                SELECT u.*, us.status as subscription_status, us.created_at as subscription_created,
                       us.current_period_end, us.cancel_at_period_end, sp.name as plan_name,
                       sp.price_cents, sp.max_addresses
                FROM users u
                LEFT JOIN user_subscriptions us ON u.id = us.user_id
                    AND us.status IN ('active', 'trialing', 'past_due', 'canceled')
                LEFT JOIN subscription_plans sp ON us.plan_id = sp.id
                WHERE u.id = $1
                ORDER BY us.created_at DESC
                LIMIT 1
                """,
                uuid.UUID(user_id),
            )

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # API keys
            api_keys = await conn.fetch(
                """
                SELECT id, key_prefix, name, permissions, created_at, last_used,
                       usage_count, is_active
                FROM api_keys
                WHERE user_id = $1
                ORDER BY created_at DESC
                """,
                uuid.UUID(user_id),
            )

            # Recent API usage
            recent_usage = await conn.fetch(
                """
                SELECT endpoint, method, response_status, addresses_monitored,
                       processing_time_ms, request_timestamp
                FROM usage_tracking
                WHERE user_id = $1
                ORDER BY request_timestamp DESC
                LIMIT 50
                """,
                uuid.UUID(user_id),
            )

            # Payment history
            payments = await conn.fetch(
                """
                SELECT stripe_payment_intent_id, amount_cents, currency,
                       status, failure_reason, created_at
                FROM payment_history
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT 20
                """,
                uuid.UUID(user_id),
            )

            return {
                "user": {
                    "id": str(user["id"]),
                    "email": user["email"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "company": user["company"],
                    "created_at": user["created_at"].isoformat(),
                    "last_login": (
                        user["last_login"].isoformat() if user["last_login"] else None
                    ),
                    "email_verified": user["email_verified"],
                    "is_active": user["is_active"],
                },
                "subscription": (
                    {
                        "status": user["subscription_status"],
                        "plan_name": user["plan_name"],
                        "price_cents": user["price_cents"],
                        "max_addresses": user["max_addresses"],
                        "created_at": (
                            user["subscription_created"].isoformat()
                            if user["subscription_created"]
                            else None
                        ),
                        "current_period_end": (
                            user["current_period_end"].isoformat()
                            if user["current_period_end"]
                            else None
                        ),
                        "cancel_at_period_end": user["cancel_at_period_end"],
                    }
                    if user["subscription_status"]
                    else None
                ),
                "api_keys": [
                    {
                        "id": str(key["id"]),
                        "key_prefix": key["key_prefix"],
                        "name": key["name"],
                        "permissions": key["permissions"],
                        "created_at": key["created_at"].isoformat(),
                        "last_used": (
                            key["last_used"].isoformat() if key["last_used"] else None
                        ),
                        "usage_count": key["usage_count"],
                        "is_active": key["is_active"],
                    }
                    for key in api_keys
                ],
                "recent_usage": [
                    {
                        "endpoint": usage["endpoint"],
                        "method": usage["method"],
                        "response_status": usage["response_status"],
                        "addresses_monitored": usage["addresses_monitored"],
                        "processing_time_ms": usage["processing_time_ms"],
                        "timestamp": usage["request_timestamp"].isoformat(),
                    }
                    for usage in recent_usage
                ],
                "payments": [
                    {
                        "id": payment["stripe_payment_intent_id"],
                        "amount_cents": payment["amount_cents"],
                        "amount_dollars": payment["amount_cents"] / 100,
                        "currency": payment["currency"],
                        "status": payment["status"],
                        "failure_reason": payment["failure_reason"],
                        "created_at": payment["created_at"].isoformat(),
                    }
                    for payment in payments
                ],
            }

    async def search_users(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search users by email, name, or company"""
        search_term = f"%{query.lower()}%"

        async with self.db_pool.acquire() as conn:
            users = await conn.fetch(
                """
                SELECT u.id, u.email, u.first_name, u.last_name, u.company,
                       u.created_at, u.last_login, u.email_verified,
                       us.status as subscription_status, sp.name as plan_name
                FROM users u
                LEFT JOIN user_subscriptions us ON u.id = us.user_id
                    AND us.status IN ('active', 'trialing', 'past_due')
                LEFT JOIN subscription_plans sp ON us.plan_id = sp.id
                WHERE u.is_active = TRUE AND (
                    LOWER(u.email) LIKE $1 OR
                    LOWER(u.first_name) LIKE $1 OR
                    LOWER(u.last_name) LIKE $1 OR
                    LOWER(u.company) LIKE $1
                )
                ORDER BY u.created_at DESC
                LIMIT $2
                """,
                search_term,
                limit,
            )

            return [
                {
                    "id": str(user["id"]),
                    "email": user["email"],
                    "name": f"{user['first_name'] or ''} {user['last_name'] or ''}".strip(),
                    "company": user["company"],
                    "created_at": user["created_at"].isoformat(),
                    "last_login": (
                        user["last_login"].isoformat() if user["last_login"] else None
                    ),
                    "email_verified": user["email_verified"],
                    "subscription_status": user["subscription_status"],
                    "plan_name": user["plan_name"],
                }
                for user in users
            ]


# FastAPI app for admin dashboard
admin_app = FastAPI(
    title="Treasury Monitor Admin",
    description="Admin dashboard for customer management",
)

templates = Jinja2Templates(directory="templates")
admin_app.mount("/static", StaticFiles(directory="static"), name="static")

# Global admin dashboard instance
admin_dashboard: AdminDashboard = None


@admin_app.on_event("startup")
async def startup_admin():
    """Initialize admin dashboard"""
    global admin_dashboard
    # This would be initialized with the same database pool
    # admin_dashboard = AdminDashboard(db_pool)
    pass


@admin_app.get("/", response_class=HTMLResponse)
async def admin_home(request: Request):
    """Admin dashboard home page"""
    if not admin_dashboard:
        return HTMLResponse("Admin dashboard not initialized", status_code=500)

    stats = await admin_dashboard.get_dashboard_stats()
    recent_users = await admin_dashboard.get_recent_users(10)
    subscription_metrics = await admin_dashboard.get_subscription_metrics()

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "stats": stats,
            "recent_users": recent_users,
            "subscription_metrics": subscription_metrics,
        },
    )


@admin_app.get("/api/stats")
async def get_dashboard_stats():
    """API endpoint for dashboard statistics"""
    if not admin_dashboard:
        raise HTTPException(status_code=500, detail="Admin dashboard not initialized")

    return await admin_dashboard.get_dashboard_stats()


@admin_app.get("/api/users")
async def list_users(
    limit: int = Query(50, ge=1, le=100), search: Optional[str] = Query(None)
):
    """API endpoint for listing users"""
    if not admin_dashboard:
        raise HTTPException(status_code=500, detail="Admin dashboard not initialized")

    if search:
        users = await admin_dashboard.search_users(search, limit)
    else:
        users = await admin_dashboard.get_recent_users(limit)

    return {"users": users}


@admin_app.get("/api/users/{user_id}")
async def get_user_details(user_id: str):
    """API endpoint for user details"""
    if not admin_dashboard:
        raise HTTPException(status_code=500, detail="Admin dashboard not initialized")

    return await admin_dashboard.get_user_details(user_id)


@admin_app.get("/api/metrics")
async def get_subscription_metrics():
    """API endpoint for subscription metrics"""
    if not admin_dashboard:
        raise HTTPException(status_code=500, detail="Admin dashboard not initialized")

    return await admin_dashboard.get_subscription_metrics()

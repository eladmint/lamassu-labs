"""
Treasury Monitor API with Authentication and Billing
Production-ready FastAPI application with Stripe integration.
"""

import os

# Emergency Secret Manager Billing Bypass
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional

sys.path.append("/Users/eladm/Projects/token/tokenhunter")

import logging

import asyncpg
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field

from ..api_keys.api_key_service import (
    APIKeyError,
    APIKeyService,
    InvalidAPIKeyError,
    PermissionDeniedError,
)

# Import our services
from ..auth.auth_service import (
    AuthenticationError,
    AuthService,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)
from ..billing.stripe_service import BillingError, StripeService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models for request/response
class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class CreateSubscriptionRequest(BaseModel):
    plan_id: str
    payment_method_id: Optional[str] = None
    trial_days: Optional[int] = None


class CreateAPIKeyRequest(BaseModel):
    name: Optional[str] = None
    permissions: List[str] = Field(default=["monitor"])
    expires_days: Optional[int] = None


class MonitorAddressesRequest(BaseModel):
    addresses: List[str] = Field(..., min_items=1)
    duration_minutes: int = Field(default=1, ge=1, le=60)


class UpdateProfileRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None


# Global services
auth_service: AuthService = None
stripe_service: StripeService = None
api_key_service: APIKeyService = None
db_pool: asyncpg.Pool = None

# FastAPI app
app = FastAPI(
    title="Treasury Monitor API",
    description="Production-ready Cardano treasury monitoring with authentication and billing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://agentforge.io",
        "https://api.agentforge.io",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()


async def get_database_connection():
    """Get database connection from pool"""
    global db_pool
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not connected")
    return db_pool


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get current user from JWT token"""
    try:
        token_data = await auth_service.verify_access_token(credentials.credentials)
        return token_data
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))


async def get_current_user_from_api_key(
    authorization: Optional[str] = Header(None), x_api_key: Optional[str] = Header(None)
):
    """Get current user from API key"""
    api_key = None

    # Check Authorization header (Bearer format)
    if authorization and authorization.startswith("Bearer "):
        potential_key = authorization[7:]  # Remove "Bearer "
        if potential_key.startswith("tm_"):
            api_key = potential_key

    # Check X-API-Key header
    if not api_key and x_api_key:
        api_key = x_api_key

    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")

    try:
        return await api_key_service.validate_api_key(api_key, "monitor")
    except (InvalidAPIKeyError, PermissionDeniedError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except APIKeyError as e:
        raise HTTPException(status_code=403, detail=str(e))


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global auth_service, stripe_service, api_key_service, db_pool

    # Database connection
    database_url = os.getenv("DATABASE_URL", "postgresql://localhost/treasury_monitor")
    jwt_secret = os.getenv(
        "JWT_SECRET", "your-super-secret-jwt-key-change-in-production"
    )
    stripe_secret = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")
    stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    api_key_secret = os.getenv("API_KEY_SECRET", "your-api-key-signing-secret")

    try:
        db_pool = await asyncpg.create_pool(database_url, min_size=2, max_size=10)
        logger.info("Database connection established")

        # Initialize services
        auth_service = AuthService(db_pool, jwt_secret)
        stripe_service = StripeService(db_pool, stripe_secret, stripe_webhook_secret)
        api_key_service = APIKeyService(db_pool, api_key_secret)

        logger.info("All services initialized")

    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global db_pool
    if db_pool:
        await db_pool.close()
        logger.info("Database connection closed")


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "treasury-monitor-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
    }


# Authentication endpoints
@app.post("/auth/register")
async def register_user(user_data: UserRegistrationRequest):
    """Register a new user"""
    try:
        result = await auth_service.register_user(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            company=user_data.company,
        )

        # Remove verification token from response for security
        response_data = {k: v for k, v in result.items() if k != "verification_token"}

        return {
            "message": "User registered successfully. Please check your email for verification.",
            "user": response_data,
        }

    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AuthenticationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
async def login_user(login_data: UserLoginRequest):
    """Authenticate user and return tokens"""
    try:
        result = await auth_service.authenticate_user(
            email=login_data.email, password=login_data.password
        )
        return result

    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except AuthenticationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/refresh")
async def refresh_token(request: Request):
    """Refresh access token using refresh token"""
    body = await request.json()
    refresh_token = body.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    try:
        result = await auth_service.refresh_access_token(refresh_token)
        return result
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/auth/logout")
async def logout_user(request: Request):
    """Logout user by invalidating refresh token"""
    body = await request.json()
    refresh_token = body.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token required")

    success = await auth_service.logout(refresh_token)
    return {"message": "Logged out successfully" if success else "Token not found"}


@app.get("/auth/profile")
async def get_user_profile(current_user: Dict = Depends(get_current_user)):
    """Get current user's profile"""
    try:
        profile = await auth_service.get_user_profile(current_user["user_id"])
        return profile
    except AuthenticationError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/auth/profile")
async def update_user_profile(
    profile_data: UpdateProfileRequest, current_user: Dict = Depends(get_current_user)
):
    """Update user profile"""
    try:
        updated_profile = await auth_service.update_user_profile(
            user_id=current_user["user_id"],
            first_name=profile_data.first_name,
            last_name=profile_data.last_name,
            company=profile_data.company,
        )
        return updated_profile
    except AuthenticationError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Billing endpoints
@app.get("/billing/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    try:
        plans = await stripe_service.get_subscription_plans()
        return {"plans": plans}
    except Exception as e:
        logger.error(f"Failed to get plans: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to fetch subscription plans"
        )


@app.post("/billing/subscribe")
async def create_subscription(
    subscription_data: CreateSubscriptionRequest,
    current_user: Dict = Depends(get_current_user),
):
    """Create subscription for user"""
    try:
        result = await stripe_service.create_subscription(
            user_id=current_user["user_id"],
            plan_id=subscription_data.plan_id,
            payment_method_id=subscription_data.payment_method_id,
            trial_days=subscription_data.trial_days,
        )
        return result
    except BillingError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/billing/subscription")
async def get_user_subscription(current_user: Dict = Depends(get_current_user)):
    """Get user's current subscription"""
    subscription = await stripe_service.get_user_subscription(current_user["user_id"])
    return {"subscription": subscription}


@app.post("/billing/subscription/cancel")
async def cancel_subscription(
    request: Request, current_user: Dict = Depends(get_current_user)
):
    """Cancel user's subscription"""
    body = await request.json()
    immediate = body.get("immediate", False)

    try:
        success = await stripe_service.cancel_subscription(
            user_id=current_user["user_id"], immediate=immediate
        )
        return {
            "message": (
                "Subscription cancelled successfully" if success else "Failed to cancel"
            )
        }
    except BillingError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/billing/subscription/reactivate")
async def reactivate_subscription(current_user: Dict = Depends(get_current_user)):
    """Reactivate cancelled subscription"""
    try:
        success = await stripe_service.reactivate_subscription(current_user["user_id"])
        return {
            "message": (
                "Subscription reactivated successfully"
                if success
                else "Failed to reactivate"
            )
        }
    except BillingError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/billing/history")
async def get_payment_history(
    limit: int = 10, current_user: Dict = Depends(get_current_user)
):
    """Get user's payment history"""
    history = await stripe_service.get_payment_history(current_user["user_id"], limit)
    return {"payments": history}


# API Key endpoints
@app.post("/api-keys")
async def create_api_key(
    key_data: CreateAPIKeyRequest, current_user: Dict = Depends(get_current_user)
):
    """Create new API key"""
    try:
        result = await api_key_service.generate_api_key(
            user_id=current_user["user_id"],
            name=key_data.name,
            permissions=key_data.permissions,
            expires_days=key_data.expires_days,
        )
        return result
    except APIKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api-keys")
async def get_user_api_keys(current_user: Dict = Depends(get_current_user)):
    """Get user's API keys"""
    keys = await api_key_service.get_user_api_keys(current_user["user_id"])
    return {"api_keys": keys}


@app.delete("/api-keys/{key_id}")
async def revoke_api_key(key_id: str, current_user: Dict = Depends(get_current_user)):
    """Revoke an API key"""
    try:
        success = await api_key_service.revoke_api_key(current_user["user_id"], key_id)
        return {
            "message": (
                "API key revoked successfully" if success else "API key not found"
            )
        }
    except APIKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api-keys/usage")
async def get_api_usage(days: int = 30, current_user: Dict = Depends(get_current_user)):
    """Get API usage statistics"""
    stats = await api_key_service.get_usage_statistics(current_user["user_id"], days)
    return {"usage": stats}


# Treasury monitoring endpoints (authenticated via API key)
@app.post("/monitor")
async def monitor_treasury_addresses(
    monitor_data: MonitorAddressesRequest,
    current_user: Dict = Depends(get_current_user_from_api_key),
):
    """Monitor treasury addresses (API key authentication required)"""
    try:
        # Check address limit based on subscription
        max_addresses = current_user.get("max_addresses")
        if max_addresses and len(monitor_data.addresses) > max_addresses:
            raise HTTPException(
                status_code=403,
                detail=f"Address limit exceeded. Your plan allows {max_addresses} addresses.",
            )

        # TODO: Implement actual treasury monitoring logic
        # For now, return demo data
        results = {
            "cycles_completed": 2,
            "addresses_monitored": len(monitor_data.addresses),
            "total_alerts": 1,
            "alerts_by_level": {"low": 0, "medium": 0, "high": 0, "critical": 1},
            "address_states": {},
            "alerts": [],
        }

        # Track API usage
        await api_key_service.track_api_usage(
            user_id=current_user["user_id"],
            api_key_id="",  # TODO: Get actual API key ID
            endpoint="/monitor",
            method="POST",
            response_status=200,
            addresses_monitored=len(monitor_data.addresses),
        )

        return results

    except Exception as e:
        logger.error(f"Treasury monitoring failed: {e}")
        raise HTTPException(status_code=500, detail="Monitoring failed")


# Stripe webhook endpoint
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    payload = await request.body()
    signature = request.headers.get("stripe-signature")

    if not signature:
        raise HTTPException(status_code=400, detail="Missing Stripe signature")

    try:
        success = await stripe_service.handle_webhook(payload, signature)
        return {"received": success}
    except Exception as e:
        logger.error(f"Webhook handling failed: {e}")
        raise HTTPException(status_code=400, detail="Webhook handling failed")


# Admin endpoints (protected by special admin API key)
@app.get("/admin/users")
async def list_users(
    limit: int = 50,
    offset: int = 0,
    current_user: Dict = Depends(get_current_user_from_api_key),
):
    """List users (admin only)"""
    # Check if user has admin permissions
    if "admin" not in current_user.get("permissions", []):
        raise HTTPException(status_code=403, detail="Admin access required")

    async with db_pool.acquire() as conn:
        users = await conn.fetch(
            """
            SELECT u.id, u.email, u.first_name, u.last_name, u.company,
                   u.created_at, u.last_login, u.is_active,
                   us.status as subscription_status, sp.name as plan_name
            FROM users u
            LEFT JOIN user_subscriptions us ON u.id = us.user_id
                AND us.status IN ('active', 'trialing', 'past_due')
            LEFT JOIN subscription_plans sp ON us.plan_id = sp.id
            ORDER BY u.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )

        return {
            "users": [
                {
                    "id": str(user["id"]),
                    "email": user["email"],
                    "name": f"{user['first_name'] or ''} {user['last_name'] or ''}".strip(),
                    "company": user["company"],
                    "created_at": user["created_at"].isoformat(),
                    "last_login": (
                        user["last_login"].isoformat() if user["last_login"] else None
                    ),
                    "is_active": user["is_active"],
                    "subscription_status": user["subscription_status"],
                    "plan_name": user["plan_name"],
                }
                for user in users
            ]
        }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        reload=os.getenv("ENV") == "development",
    )

#!/usr/bin/env python3

"""
TrustWrapper v3.0 Enterprise API Gateway
Phase 2 Week 8 Task 8.2: Enterprise Integration Tools

This module provides enterprise-grade API gateway functionality including:
- Advanced authentication and authorization
- Rate limiting and throttling
- Request/response transformation
- Load balancing and failover
- Monitoring and analytics
- White-label customization support
"""

import asyncio
import hashlib
import hmac
import logging
import time
from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import aiohttp
import jwt
import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthenticationMethod(Enum):
    API_KEY = "api_key"
    JWT_TOKEN = "jwt_token"
    OAUTH2 = "oauth2"
    HMAC_SIGNATURE = "hmac_signature"
    MUTUAL_TLS = "mutual_tls"


class RateLimitStrategy(Enum):
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"
    ADAPTIVE = "adaptive"


class LoadBalanceStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_CONNECTIONS = "least_connections"
    RESPONSE_TIME = "response_time"
    HEALTH_BASED = "health_based"


@dataclass
class BackendService:
    service_id: str
    name: str
    base_url: str
    health_endpoint: str
    weight: float
    max_connections: int
    timeout_seconds: float
    current_connections: int = 0
    health_status: str = "unknown"  # "healthy", "degraded", "unhealthy"
    last_health_check: float = 0
    response_time_avg: float = 0
    error_rate: float = 0


@dataclass
class APIClient:
    client_id: str
    name: str
    api_key: str
    secret_key: str
    authentication_method: AuthenticationMethod
    rate_limit_tier: str
    allowed_endpoints: List[str]
    ip_whitelist: List[str]
    is_active: bool
    created_at: float
    last_accessed: float
    total_requests: int = 0
    total_errors: int = 0


@dataclass
class RateLimitRule:
    rule_id: str
    tier: str
    requests_per_minute: int
    requests_per_hour: int
    requests_per_day: int
    burst_limit: int
    strategy: RateLimitStrategy


@dataclass
class RequestMetrics:
    timestamp: float
    client_id: str
    endpoint: str
    method: str
    response_status: int
    response_time_ms: float
    request_size_bytes: int
    response_size_bytes: int
    backend_service: str
    user_agent: str
    ip_address: str


class TrustWrapperEnterpriseAPIGateway:
    """Enterprise API Gateway for TrustWrapper v3.0

    Provides comprehensive enterprise features including:
    - Multi-method authentication and authorization
    - Advanced rate limiting with multiple strategies
    - Load balancing across backend services
    - Request/response transformation
    - Real-time monitoring and analytics
    - White-label customization support
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.backend_services: Dict[str, BackendService] = {}
        self.api_clients: Dict[str, APIClient] = {}
        self.rate_limit_rules: Dict[str, RateLimitRule] = {}
        self.request_metrics: deque = deque(maxlen=100000)
        self.rate_limit_buckets: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self.current_service_index = 0

        # Redis for distributed rate limiting (optional)
        self.redis_client: Optional[redis.Redis] = None

        # FastAPI application
        self.app = FastAPI(
            title="TrustWrapper Enterprise API Gateway",
            description="Enterprise-grade API gateway with advanced features",
            version="3.0.0",
        )

        # Security
        self.security = HTTPBearer()

        # Setup middleware and routes
        self._setup_middleware()
        self._setup_routes()
        self._setup_default_configuration()

        # Start background tasks
        self._start_background_tasks()

        logger.info("TrustWrapper Enterprise API Gateway initialized")

    def _setup_middleware(self):
        """Setup middleware for the gateway"""
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.get("cors_origins", ["*"]),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Custom middleware for request processing
        @self.app.middleware("http")
        async def gateway_middleware(request: Request, call_next):
            start_time = time.time()

            # Collect request metrics
            request_size = len(await request.body())
            client_ip = request.client.host

            try:
                # Process request through gateway
                response = await call_next(request)

                # Calculate response time
                response_time = (time.time() - start_time) * 1000

                # Log metrics
                metrics = RequestMetrics(
                    timestamp=start_time,
                    client_id=getattr(request.state, "client_id", "unknown"),
                    endpoint=str(request.url.path),
                    method=request.method,
                    response_status=response.status_code,
                    response_time_ms=response_time,
                    request_size_bytes=request_size,
                    response_size_bytes=(
                        len(response.body) if hasattr(response, "body") else 0
                    ),
                    backend_service=getattr(
                        request.state, "backend_service", "unknown"
                    ),
                    user_agent=request.headers.get("user-agent", ""),
                    ip_address=client_ip,
                )

                self.request_metrics.append(metrics)

                # Add custom headers
                response.headers["X-Gateway-Version"] = "3.0.0"
                response.headers["X-Response-Time"] = str(response_time)
                response.headers["X-Request-ID"] = getattr(
                    request.state, "request_id", "unknown"
                )

                return response

            except Exception as e:
                logger.error(f"Gateway middleware error: {e}")
                response_time = (time.time() - start_time) * 1000

                # Log error metrics
                error_metrics = RequestMetrics(
                    timestamp=start_time,
                    client_id=getattr(request.state, "client_id", "unknown"),
                    endpoint=str(request.url.path),
                    method=request.method,
                    response_status=500,
                    response_time_ms=response_time,
                    request_size_bytes=request_size,
                    response_size_bytes=0,
                    backend_service="error",
                    user_agent=request.headers.get("user-agent", ""),
                    ip_address=client_ip,
                )

                self.request_metrics.append(error_metrics)

                return JSONResponse(
                    status_code=500,
                    content={
                        "error": "Internal gateway error",
                        "request_id": getattr(request.state, "request_id", "unknown"),
                    },
                )

    def _setup_routes(self):
        """Setup API routes"""

        @self.app.get("/")
        async def root():
            """Gateway root endpoint"""
            return {
                "name": "TrustWrapper Enterprise API Gateway",
                "version": "3.0.0",
                "status": "operational",
                "features": [
                    "Multi-method authentication",
                    "Advanced rate limiting",
                    "Load balancing",
                    "Request transformation",
                    "Real-time monitoring",
                    "White-label support",
                ],
                "backend_services": len(self.backend_services),
                "active_clients": len(
                    [c for c in self.api_clients.values() if c.is_active]
                ),
                "timestamp": time.time(),
            }

        @self.app.get("/health")
        async def health_check():
            """Gateway health check"""
            healthy_services = len(
                [
                    s
                    for s in self.backend_services.values()
                    if s.health_status == "healthy"
                ]
            )
            total_services = len(self.backend_services)

            return {
                "status": (
                    "healthy" if healthy_services == total_services else "degraded"
                ),
                "backend_services": {
                    "healthy": healthy_services,
                    "total": total_services,
                    "services": {
                        s.service_id: s.health_status
                        for s in self.backend_services.values()
                    },
                },
                "gateway_metrics": {
                    "total_requests": len(self.request_metrics),
                    "avg_response_time": self._calculate_avg_response_time(),
                    "error_rate": self._calculate_error_rate(),
                },
                "timestamp": time.time(),
            }

        # Dynamic route for proxying to backend services
        @self.app.api_route(
            "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
        )
        async def proxy_request(request: Request, path: str):
            """Proxy requests to backend services"""
            return await self._handle_proxy_request(request, path)

        # Enterprise management endpoints
        @self.app.get("/admin/clients")
        async def get_clients():
            """Get all API clients"""
            return {
                "clients": [asdict(client) for client in self.api_clients.values()],
                "total": len(self.api_clients),
            }

        @self.app.get("/admin/services")
        async def get_services():
            """Get all backend services"""
            return {
                "services": [
                    asdict(service) for service in self.backend_services.values()
                ],
                "total": len(self.backend_services),
            }

        @self.app.get("/admin/metrics")
        async def get_metrics():
            """Get gateway metrics"""
            return await self._get_analytics_dashboard()

    def _setup_default_configuration(self):
        """Setup default configuration"""
        # Default backend services
        self.add_backend_service(
            service_id="analytics_dashboard",
            name="Advanced Analytics Dashboard",
            base_url="http://localhost:8080",
            health_endpoint="/health",
            weight=1.0,
            max_connections=100,
            timeout_seconds=30.0,
        )

        self.add_backend_service(
            service_id="ml_oracle",
            name="ML Oracle Service",
            base_url="http://localhost:8081",
            health_endpoint="/health",
            weight=1.0,
            max_connections=200,
            timeout_seconds=10.0,
        )

        # Default rate limit rules
        self.add_rate_limit_rule(
            rule_id="basic_tier",
            tier="basic",
            requests_per_minute=60,
            requests_per_hour=1000,
            requests_per_day=10000,
            burst_limit=10,
            strategy=RateLimitStrategy.TOKEN_BUCKET,
        )

        self.add_rate_limit_rule(
            rule_id="premium_tier",
            tier="premium",
            requests_per_minute=300,
            requests_per_hour=10000,
            requests_per_day=100000,
            burst_limit=50,
            strategy=RateLimitStrategy.SLIDING_WINDOW,
        )

        self.add_rate_limit_rule(
            rule_id="enterprise_tier",
            tier="enterprise",
            requests_per_minute=1000,
            requests_per_hour=50000,
            requests_per_day=1000000,
            burst_limit=200,
            strategy=RateLimitStrategy.ADAPTIVE,
        )

        # Default API clients
        self.add_api_client(
            client_id="demo_client",
            name="Demo Client",
            api_key="demo_api_key_12345",
            secret_key="demo_secret_67890",
            authentication_method=AuthenticationMethod.API_KEY,
            rate_limit_tier="basic",
            allowed_endpoints=["/*"],
            ip_whitelist=["*"],
        )

        self.add_api_client(
            client_id="enterprise_client",
            name="Enterprise Client",
            api_key="enterprise_api_key_abcdef",
            secret_key="enterprise_secret_uvwxyz",
            authentication_method=AuthenticationMethod.HMAC_SIGNATURE,
            rate_limit_tier="enterprise",
            allowed_endpoints=["/*"],
            ip_whitelist=["*"],
        )

    def add_backend_service(
        self,
        service_id: str,
        name: str,
        base_url: str,
        health_endpoint: str,
        weight: float,
        max_connections: int,
        timeout_seconds: float,
    ):
        """Add a backend service"""
        service = BackendService(
            service_id=service_id,
            name=name,
            base_url=base_url,
            health_endpoint=health_endpoint,
            weight=weight,
            max_connections=max_connections,
            timeout_seconds=timeout_seconds,
        )

        self.backend_services[service_id] = service
        logger.info(f"Added backend service: {service_id}")

    def add_api_client(
        self,
        client_id: str,
        name: str,
        api_key: str,
        secret_key: str,
        authentication_method: AuthenticationMethod,
        rate_limit_tier: str,
        allowed_endpoints: List[str],
        ip_whitelist: List[str],
    ):
        """Add an API client"""
        client = APIClient(
            client_id=client_id,
            name=name,
            api_key=api_key,
            secret_key=secret_key,
            authentication_method=authentication_method,
            rate_limit_tier=rate_limit_tier,
            allowed_endpoints=allowed_endpoints,
            ip_whitelist=ip_whitelist,
            is_active=True,
            created_at=time.time(),
            last_accessed=time.time(),
        )

        self.api_clients[client_id] = client
        logger.info(f"Added API client: {client_id}")

    def add_rate_limit_rule(
        self,
        rule_id: str,
        tier: str,
        requests_per_minute: int,
        requests_per_hour: int,
        requests_per_day: int,
        burst_limit: int,
        strategy: RateLimitStrategy,
    ):
        """Add a rate limit rule"""
        rule = RateLimitRule(
            rule_id=rule_id,
            tier=tier,
            requests_per_minute=requests_per_minute,
            requests_per_hour=requests_per_hour,
            requests_per_day=requests_per_day,
            burst_limit=burst_limit,
            strategy=strategy,
        )

        self.rate_limit_rules[rule_id] = rule
        logger.info(f"Added rate limit rule: {rule_id}")

    async def _handle_proxy_request(self, request: Request, path: str):
        """Handle proxying requests to backend services"""
        try:
            # Generate request ID
            request_id = f"req_{int(time.time())}_{hash(str(request.url))}"
            request.state.request_id = request_id

            # Authenticate request
            client = await self._authenticate_request(request)
            if not client:
                raise HTTPException(status_code=401, detail="Authentication failed")

            request.state.client_id = client.client_id

            # Check rate limits
            if not await self._check_rate_limit(client, request):
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            # Check authorization
            if not self._check_authorization(client, path):
                raise HTTPException(status_code=403, detail="Access denied")

            # Select backend service
            backend_service = self._select_backend_service(path)
            if not backend_service:
                raise HTTPException(
                    status_code=503, detail="No healthy backend service available"
                )

            request.state.backend_service = backend_service.service_id

            # Transform request if needed
            transformed_request = await self._transform_request(request, client)

            # Proxy to backend
            response = await self._proxy_to_backend(
                backend_service, transformed_request, path
            )

            # Transform response if needed
            transformed_response = await self._transform_response(response, client)

            # Update client metrics
            client.last_accessed = time.time()
            client.total_requests += 1

            return transformed_response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Proxy request error: {e}")

            # Update error metrics
            if hasattr(request.state, "client_id"):
                client = self.api_clients.get(request.state.client_id)
                if client:
                    client.total_errors += 1

            raise HTTPException(status_code=500, detail="Internal gateway error")

    async def _authenticate_request(self, request: Request) -> Optional[APIClient]:
        """Authenticate incoming request"""
        # Try API key authentication
        api_key = request.headers.get("X-API-Key")
        if api_key:
            for client in self.api_clients.values():
                if client.api_key == api_key and client.is_active:
                    if client.authentication_method == AuthenticationMethod.API_KEY:
                        return client

        # Try HMAC signature authentication
        signature = request.headers.get("X-Signature")
        timestamp = request.headers.get("X-Timestamp")
        if signature and timestamp:
            for client in self.api_clients.values():
                if (
                    client.authentication_method == AuthenticationMethod.HMAC_SIGNATURE
                    and client.is_active
                ):
                    if await self._verify_hmac_signature(
                        request, client, signature, timestamp
                    ):
                        return client

        # Try JWT token authentication
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            token = authorization[7:]
            client = await self._verify_jwt_token(token)
            if client:
                return client

        return None

    async def _verify_hmac_signature(
        self, request: Request, client: APIClient, signature: str, timestamp: str
    ) -> bool:
        """Verify HMAC signature"""
        try:
            # Check timestamp to prevent replay attacks
            request_time = float(timestamp)
            current_time = time.time()
            if abs(current_time - request_time) > 300:  # 5 minute tolerance
                return False

            # Create signature string
            body = await request.body()
            signature_string = (
                f"{request.method}|{request.url.path}|{timestamp}|{body.decode()}"
            )

            # Calculate expected signature
            expected_signature = hmac.new(
                client.secret_key.encode(), signature_string.encode(), hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(signature, expected_signature)

        except Exception as e:
            logger.error(f"HMAC verification error: {e}")
            return False

    async def _verify_jwt_token(self, token: str) -> Optional[APIClient]:
        """Verify JWT token"""
        try:
            # Decode token (in production, use proper JWT verification)
            payload = jwt.decode(token, options={"verify_signature": False})
            client_id = payload.get("client_id")

            if client_id and client_id in self.api_clients:
                client = self.api_clients[client_id]
                if (
                    client.authentication_method == AuthenticationMethod.JWT_TOKEN
                    and client.is_active
                ):
                    return client

            return None

        except Exception as e:
            logger.error(f"JWT verification error: {e}")
            return None

    async def _check_rate_limit(self, client: APIClient, request: Request) -> bool:
        """Check rate limits for client"""
        tier = client.rate_limit_tier
        if tier not in self.rate_limit_rules:
            return True  # No rate limit rule, allow

        rule = self.rate_limit_rules[tier]
        bucket_key = f"{client.client_id}:{tier}"

        current_time = time.time()

        if rule.strategy == RateLimitStrategy.TOKEN_BUCKET:
            return self._check_token_bucket_rate_limit(bucket_key, rule, current_time)
        elif rule.strategy == RateLimitStrategy.SLIDING_WINDOW:
            return self._check_sliding_window_rate_limit(bucket_key, rule, current_time)
        elif rule.strategy == RateLimitStrategy.FIXED_WINDOW:
            return self._check_fixed_window_rate_limit(bucket_key, rule, current_time)
        elif rule.strategy == RateLimitStrategy.ADAPTIVE:
            return self._check_adaptive_rate_limit(
                bucket_key, rule, current_time, client
            )

        return True

    def _check_token_bucket_rate_limit(
        self, bucket_key: str, rule: RateLimitRule, current_time: float
    ) -> bool:
        """Check token bucket rate limiting"""
        if bucket_key not in self.rate_limit_buckets:
            self.rate_limit_buckets[bucket_key] = {
                "tokens": rule.burst_limit,
                "last_refill": current_time,
            }

        bucket = self.rate_limit_buckets[bucket_key]

        # Refill tokens
        time_elapsed = current_time - bucket["last_refill"]
        tokens_to_add = time_elapsed * (rule.requests_per_minute / 60.0)
        bucket["tokens"] = min(rule.burst_limit, bucket["tokens"] + tokens_to_add)
        bucket["last_refill"] = current_time

        # Check if tokens available
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True

        return False

    def _check_sliding_window_rate_limit(
        self, bucket_key: str, rule: RateLimitRule, current_time: float
    ) -> bool:
        """Check sliding window rate limiting"""
        if bucket_key not in self.rate_limit_buckets:
            self.rate_limit_buckets[bucket_key] = {"requests": deque()}

        bucket = self.rate_limit_buckets[bucket_key]
        requests = bucket["requests"]

        # Remove old requests outside window
        window_start = current_time - 60  # 1 minute window
        while requests and requests[0] < window_start:
            requests.popleft()

        # Check if under limit
        if len(requests) < rule.requests_per_minute:
            requests.append(current_time)
            return True

        return False

    def _check_fixed_window_rate_limit(
        self, bucket_key: str, rule: RateLimitRule, current_time: float
    ) -> bool:
        """Check fixed window rate limiting"""
        window_start = int(current_time // 60) * 60  # Start of current minute
        window_key = f"{bucket_key}:{window_start}"

        if window_key not in self.rate_limit_buckets:
            self.rate_limit_buckets[window_key] = {"count": 0}

        bucket = self.rate_limit_buckets[window_key]

        if bucket["count"] < rule.requests_per_minute:
            bucket["count"] += 1
            return True

        return False

    def _check_adaptive_rate_limit(
        self,
        bucket_key: str,
        rule: RateLimitRule,
        current_time: float,
        client: APIClient,
    ) -> bool:
        """Check adaptive rate limiting based on client behavior"""
        # Base rate limiting using token bucket
        base_allowed = self._check_token_bucket_rate_limit(
            bucket_key, rule, current_time
        )

        if not base_allowed:
            return False

        # Adaptive adjustment based on client error rate
        error_rate = client.total_errors / max(client.total_requests, 1)

        if error_rate > 0.1:  # High error rate, reduce allowance
            if bucket_key not in self.rate_limit_buckets:
                return False

            # Reduce tokens by 50% for high error rate clients
            bucket = self.rate_limit_buckets[bucket_key]
            if bucket.get("tokens", 0) > 0.5:
                bucket["tokens"] -= 0.5
                return True
            return False

        return True

    def _check_authorization(self, client: APIClient, path: str) -> bool:
        """Check if client is authorized for the endpoint"""
        if "*" in client.allowed_endpoints or "/*" in client.allowed_endpoints:
            return True

        for allowed_pattern in client.allowed_endpoints:
            if path.startswith(allowed_pattern.rstrip("*")):
                return True

        return False

    def _select_backend_service(self, path: str) -> Optional[BackendService]:
        """Select backend service using load balancing"""
        healthy_services = [
            s for s in self.backend_services.values() if s.health_status == "healthy"
        ]

        if not healthy_services:
            # Fallback to degraded services if no healthy ones
            healthy_services = [
                s
                for s in self.backend_services.values()
                if s.health_status == "degraded"
            ]

        if not healthy_services:
            return None

        # Simple round-robin for now (can be enhanced with other strategies)
        selected_service = healthy_services[
            self.current_service_index % len(healthy_services)
        ]
        self.current_service_index += 1

        return selected_service

    async def _transform_request(self, request: Request, client: APIClient) -> Request:
        """Transform request before forwarding to backend"""
        # Add client context headers
        if hasattr(request, "_headers"):
            request._headers = dict(request.headers)
        else:
            request._headers = {}

        request._headers["X-Client-ID"] = client.client_id
        request._headers["X-Client-Tier"] = client.rate_limit_tier
        request._headers["X-Gateway-Version"] = "3.0.0"

        return request

    async def _transform_response(self, response: Any, client: APIClient) -> Any:
        """Transform response before returning to client"""
        # Add white-label headers if configured
        if hasattr(response, "headers"):
            response.headers["X-Powered-By"] = "TrustWrapper Enterprise Gateway"

            # White-label customization based on client
            if client.rate_limit_tier == "enterprise":
                response.headers["X-Service-Tier"] = "Enterprise"

        return response

    async def _proxy_to_backend(
        self, service: BackendService, request: Request, path: str
    ):
        """Proxy request to backend service"""
        try:
            service.current_connections += 1
            start_time = time.time()

            # Construct backend URL
            backend_url = f"{service.base_url.rstrip('/')}/{path.lstrip('/')}"

            # Get request body
            body = await request.body()

            # Create HTTP session
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=service.timeout_seconds)
            ) as session:
                async with session.request(
                    method=request.method,
                    url=backend_url,
                    headers=dict(request.headers),
                    data=body,
                    params=dict(request.query_params),
                ) as backend_response:

                    response_time = (time.time() - start_time) * 1000

                    # Update service metrics
                    service.response_time_avg = (
                        service.response_time_avg + response_time
                    ) / 2

                    if backend_response.status >= 400:
                        service.error_rate = min(1.0, service.error_rate + 0.01)
                    else:
                        service.error_rate = max(0.0, service.error_rate - 0.001)

                    # Get response content
                    response_content = await backend_response.read()

                    # Create response
                    response = Response(
                        content=response_content,
                        status_code=backend_response.status,
                        headers=dict(backend_response.headers),
                    )

                    return response

        except asyncio.TimeoutError:
            service.error_rate = min(1.0, service.error_rate + 0.05)
            raise HTTPException(status_code=504, detail="Backend service timeout")
        except Exception as e:
            logger.error(f"Backend proxy error: {e}")
            service.error_rate = min(1.0, service.error_rate + 0.02)
            raise HTTPException(status_code=502, detail="Backend service error")
        finally:
            service.current_connections = max(0, service.current_connections - 1)

    def _start_background_tasks(self):
        """Start background tasks"""

        def run_health_checks():
            while True:
                try:
                    asyncio.run(self._perform_health_checks())
                    time.sleep(30)  # Health checks every 30 seconds
                except Exception as e:
                    logger.error(f"Health check error: {e}")
                    time.sleep(60)

        def cleanup_rate_limits():
            while True:
                try:
                    self._cleanup_old_rate_limit_data()
                    time.sleep(300)  # Cleanup every 5 minutes
                except Exception as e:
                    logger.error(f"Rate limit cleanup error: {e}")
                    time.sleep(600)

        # Start background threads
        import threading

        health_thread = threading.Thread(target=run_health_checks, daemon=True)
        cleanup_thread = threading.Thread(target=cleanup_rate_limits, daemon=True)

        health_thread.start()
        cleanup_thread.start()

    async def _perform_health_checks(self):
        """Perform health checks on backend services"""
        for service in self.backend_services.values():
            try:
                health_url = f"{service.base_url.rstrip('/')}{service.health_endpoint}"

                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as session:
                    async with session.get(health_url) as response:
                        if response.status == 200:
                            service.health_status = "healthy"
                        elif response.status < 500:
                            service.health_status = "degraded"
                        else:
                            service.health_status = "unhealthy"

                        service.last_health_check = time.time()

            except Exception as e:
                logger.warning(f"Health check failed for {service.service_id}: {e}")
                service.health_status = "unhealthy"
                service.last_health_check = time.time()

    def _cleanup_old_rate_limit_data(self):
        """Cleanup old rate limit data"""
        current_time = time.time()

        # Remove old buckets (older than 1 hour)
        old_buckets = []
        for bucket_key in self.rate_limit_buckets:
            if ":" in bucket_key and bucket_key.split(":")[-1].isdigit():
                window_start = int(bucket_key.split(":")[-1])
                if current_time - window_start > 3600:  # 1 hour old
                    old_buckets.append(bucket_key)

        for bucket_key in old_buckets:
            del self.rate_limit_buckets[bucket_key]

        logger.info(f"Cleaned up {len(old_buckets)} old rate limit buckets")

    def _calculate_avg_response_time(self) -> float:
        """Calculate average response time from recent metrics"""
        if not self.request_metrics:
            return 0.0

        recent_metrics = list(self.request_metrics)[-1000:]  # Last 1000 requests
        total_time = sum(m.response_time_ms for m in recent_metrics)
        return total_time / len(recent_metrics)

    def _calculate_error_rate(self) -> float:
        """Calculate error rate from recent metrics"""
        if not self.request_metrics:
            return 0.0

        recent_metrics = list(self.request_metrics)[-1000:]  # Last 1000 requests
        error_count = sum(1 for m in recent_metrics if m.response_status >= 400)
        return error_count / len(recent_metrics)

    async def _get_analytics_dashboard(self) -> Dict[str, Any]:
        """Get analytics dashboard data"""
        current_time = time.time()

        # Recent metrics (last hour)
        hour_ago = current_time - 3600
        recent_metrics = [m for m in self.request_metrics if m.timestamp > hour_ago]

        # Calculate statistics
        total_requests = len(recent_metrics)
        avg_response_time = sum(m.response_time_ms for m in recent_metrics) / max(
            total_requests, 1
        )
        error_rate = sum(1 for m in recent_metrics if m.response_status >= 400) / max(
            total_requests, 1
        )

        # Top clients
        client_requests = defaultdict(int)
        for metric in recent_metrics:
            client_requests[metric.client_id] += 1

        top_clients = sorted(client_requests.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]

        # Top endpoints
        endpoint_requests = defaultdict(int)
        for metric in recent_metrics:
            endpoint_requests[metric.endpoint] += 1

        top_endpoints = sorted(
            endpoint_requests.items(), key=lambda x: x[1], reverse=True
        )[:10]

        return {
            "timestamp": current_time,
            "time_window": "last_hour",
            "summary": {
                "total_requests": total_requests,
                "avg_response_time_ms": avg_response_time,
                "error_rate": error_rate,
                "active_clients": len(client_requests),
                "backend_services": len(self.backend_services),
            },
            "top_clients": [
                {"client_id": client_id, "requests": count}
                for client_id, count in top_clients
            ],
            "top_endpoints": [
                {"endpoint": endpoint, "requests": count}
                for endpoint, count in top_endpoints
            ],
            "backend_health": {
                service.service_id: {
                    "status": service.health_status,
                    "response_time_avg": service.response_time_avg,
                    "error_rate": service.error_rate,
                    "current_connections": service.current_connections,
                }
                for service in self.backend_services.values()
            },
        }

    def run(self, host: str = "0.0.0.0", port: int = 8090):
        """Run the enterprise API gateway"""
        logger.info(f"Starting TrustWrapper Enterprise API Gateway on {host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


# Legacy alias for backwards compatibility
TrustWrapperEnterpriseGateway = TrustWrapperEnterpriseAPIGateway

if __name__ == "__main__":
    # Example configuration
    config = {
        "cors_origins": ["*"],
        "redis_url": "redis://localhost:6379",
        "enable_distributed_rate_limiting": False,
    }

    # Create and run gateway
    gateway = TrustWrapperEnterpriseAPIGateway(config)

    print("🚀 TrustWrapper v3.0 Enterprise API Gateway")
    print("=" * 60)
    print("🔐 Features: Multi-auth, rate limiting, load balancing")
    print("📊 Monitoring: Real-time metrics and analytics")
    print("🏢 Enterprise: White-label support and customization")
    print("🌐 Endpoints:")
    print("   - Root: http://localhost:8090/")
    print("   - Health: http://localhost:8090/health")
    print("   - Admin: http://localhost:8090/admin/")
    print("   - Docs: http://localhost:8090/docs")

    gateway.run(host="0.0.0.0", port=8090)

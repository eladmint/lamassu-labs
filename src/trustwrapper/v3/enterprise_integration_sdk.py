#!/usr/bin/env python3

"""
TrustWrapper v3.0 Enterprise Integration SDK
Phase 2 Week 8 Task 8.2: Enterprise Integration Tools - Custom SDKs

This module provides enterprise-grade SDKs for integrating with TrustWrapper
across multiple programming languages and frameworks, including:
- Python SDK with async/sync support
- JavaScript/TypeScript SDK generation
- REST API client libraries
- WebSocket real-time integration
- Webhook event handling
- Enterprise authentication helpers
"""

import asyncio
import hashlib
import hmac
import json
import logging
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Optional
from urllib.parse import urljoin

import aiohttp
import requests
import websockets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthMethod(Enum):
    API_KEY = "api_key"
    JWT_TOKEN = "jwt_token"
    HMAC_SIGNATURE = "hmac_signature"
    OAUTH2 = "oauth2"


class ResponseFormat(Enum):
    JSON = "json"
    XML = "xml"
    PROTOBUF = "protobuf"
    MSGPACK = "msgpack"


@dataclass
class SDKConfig:
    base_url: str
    api_key: Optional[str] = None
    secret_key: Optional[str] = None
    jwt_token: Optional[str] = None
    auth_method: AuthMethod = AuthMethod.API_KEY
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0
    response_format: ResponseFormat = ResponseFormat.JSON
    enable_caching: bool = True
    cache_ttl: int = 300
    enable_webhooks: bool = False
    webhook_secret: Optional[str] = None
    user_agent: str = "TrustWrapper-SDK/3.0"


@dataclass
class APIResponse:
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    status_code: int
    response_time_ms: float
    request_id: Optional[str]
    timestamp: float


class TrustWrapperEnterpriseSDK:
    """Enterprise SDK for TrustWrapper v3.0 Integration

    Provides comprehensive integration capabilities including:
    - Multi-method authentication
    - Async/sync API clients
    - Real-time WebSocket connections
    - Webhook event handling
    - Automatic retries and error handling
    - Response caching and optimization
    - Enterprise monitoring and analytics
    """

    def __init__(self, config: SDKConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.sync_session: Optional[requests.Session] = None
        self.websocket_connection: Optional[websockets.WebSocketServerProtocol] = None
        self.cache: Dict[str, Any] = {}
        self.webhook_handlers: Dict[str, Callable] = {}

        logger.info(f"TrustWrapper Enterprise SDK initialized for {config.base_url}")

    async def __aenter__(self):
        """Async context manager entry"""
        await self._setup_async_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self._cleanup_async_session()

    def __enter__(self):
        """Sync context manager entry"""
        self._setup_sync_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit"""
        self._cleanup_sync_session()

    async def _setup_async_session(self):
        """Setup async HTTP session"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(
                timeout=timeout, headers=self._get_default_headers()
            )

    async def _cleanup_async_session(self):
        """Cleanup async HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None

    def _setup_sync_session(self):
        """Setup sync HTTP session"""
        if self.sync_session is None:
            self.sync_session = requests.Session()
            self.sync_session.headers.update(self._get_default_headers())

    def _cleanup_sync_session(self):
        """Cleanup sync HTTP session"""
        if self.sync_session:
            self.sync_session.close()
            self.sync_session = None

    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for requests"""
        headers = {
            "User-Agent": self.config.user_agent,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if self.config.auth_method == AuthMethod.API_KEY and self.config.api_key:
            headers["X-API-Key"] = self.config.api_key
        elif self.config.auth_method == AuthMethod.JWT_TOKEN and self.config.jwt_token:
            headers["Authorization"] = f"Bearer {self.config.jwt_token}"

        return headers

    def _get_hmac_headers(
        self, method: str, path: str, body: str = ""
    ) -> Dict[str, str]:
        """Generate HMAC signature headers"""
        if (
            self.config.auth_method != AuthMethod.HMAC_SIGNATURE
            or not self.config.secret_key
        ):
            return {}

        timestamp = str(int(time.time()))
        signature_string = f"{method}|{path}|{timestamp}|{body}"

        signature = hmac.new(
            self.config.secret_key.encode(), signature_string.encode(), hashlib.sha256
        ).hexdigest()

        return {"X-Signature": signature, "X-Timestamp": timestamp}

    def _get_cache_key(
        self, method: str, url: str, params: Optional[Dict] = None
    ) -> str:
        """Generate cache key for request"""
        cache_data = f"{method}:{url}"
        if params:
            cache_data += f":{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(cache_data.encode()).hexdigest()

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached response is still valid"""
        if not self.config.enable_caching or cache_key not in self.cache:
            return False

        cache_entry = self.cache[cache_key]
        return time.time() - cache_entry["timestamp"] < self.config.cache_ttl

    def _cache_response(self, cache_key: str, response: APIResponse):
        """Cache API response"""
        if self.config.enable_caching:
            self.cache[cache_key] = {"response": response, "timestamp": time.time()}

    async def _make_async_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> APIResponse:
        """Make async HTTP request with retries"""
        url = urljoin(self.config.base_url, endpoint.lstrip("/"))

        # Check cache for GET requests
        if method.upper() == "GET":
            cache_key = self._get_cache_key(method, url, params)
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]["response"]

        await self._setup_async_session()

        # Prepare request
        request_headers = self._get_default_headers()
        if headers:
            request_headers.update(headers)

        # Add HMAC signature if needed
        body_str = json.dumps(data) if data else ""
        hmac_headers = self._get_hmac_headers(method, endpoint, body_str)
        request_headers.update(hmac_headers)

        # Retry logic
        for attempt in range(self.config.max_retries + 1):
            try:
                start_time = time.time()

                async with self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=request_headers,
                ) as response:
                    response_time = (time.time() - start_time) * 1000
                    response_data = (
                        await response.json()
                        if response.content_type == "application/json"
                        else await response.text()
                    )

                    api_response = APIResponse(
                        success=response.status < 400,
                        data=response_data if response.status < 400 else None,
                        error=response_data if response.status >= 400 else None,
                        status_code=response.status,
                        response_time_ms=response_time,
                        request_id=response.headers.get("X-Request-ID"),
                        timestamp=time.time(),
                    )

                    # Cache successful GET requests
                    if method.upper() == "GET" and api_response.success:
                        cache_key = self._get_cache_key(method, url, params)
                        self._cache_response(cache_key, api_response)

                    return api_response

            except Exception as e:
                if attempt == self.config.max_retries:
                    return APIResponse(
                        success=False,
                        data=None,
                        error=f"Request failed after {self.config.max_retries} retries: {str(e)}",
                        status_code=0,
                        response_time_ms=0,
                        request_id=None,
                        timestamp=time.time(),
                    )

                await asyncio.sleep(self.config.retry_delay * (2**attempt))

    def _make_sync_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> APIResponse:
        """Make sync HTTP request with retries"""
        url = urljoin(self.config.base_url, endpoint.lstrip("/"))

        # Check cache for GET requests
        if method.upper() == "GET":
            cache_key = self._get_cache_key(method, url, params)
            if self._is_cache_valid(cache_key):
                return self.cache[cache_key]["response"]

        self._setup_sync_session()

        # Prepare request
        request_headers = self._get_default_headers()
        if headers:
            request_headers.update(headers)

        # Add HMAC signature if needed
        body_str = json.dumps(data) if data else ""
        hmac_headers = self._get_hmac_headers(method, endpoint, body_str)
        request_headers.update(hmac_headers)

        # Retry logic
        for attempt in range(self.config.max_retries + 1):
            try:
                start_time = time.time()

                response = self.sync_session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=request_headers,
                    timeout=self.config.timeout,
                )

                response_time = (time.time() - start_time) * 1000

                try:
                    response_data = response.json()
                except:
                    response_data = response.text

                api_response = APIResponse(
                    success=response.status_code < 400,
                    data=response_data if response.status_code < 400 else None,
                    error=response_data if response.status_code >= 400 else None,
                    status_code=response.status_code,
                    response_time_ms=response_time,
                    request_id=response.headers.get("X-Request-ID"),
                    timestamp=time.time(),
                )

                # Cache successful GET requests
                if method.upper() == "GET" and api_response.success:
                    cache_key = self._get_cache_key(method, url, params)
                    self._cache_response(cache_key, api_response)

                return api_response

            except Exception as e:
                if attempt == self.config.max_retries:
                    return APIResponse(
                        success=False,
                        data=None,
                        error=f"Request failed after {self.config.max_retries} retries: {str(e)}",
                        status_code=0,
                        response_time_ms=0,
                        request_id=None,
                        timestamp=time.time(),
                    )

                time.sleep(self.config.retry_delay * (2**attempt))

    # Analytics Dashboard API Methods
    async def get_real_time_metrics(self) -> APIResponse:
        """Get real-time metrics dashboard"""
        return await self._make_async_request(
            "GET", "/api/v1/dashboard/real-time-metrics"
        )

    def get_real_time_metrics_sync(self) -> APIResponse:
        """Get real-time metrics dashboard (sync)"""
        return self._make_sync_request("GET", "/api/v1/dashboard/real-time-metrics")

    async def get_predictive_analytics(self) -> APIResponse:
        """Get predictive analytics dashboard"""
        return await self._make_async_request(
            "GET", "/api/v1/dashboard/predictive-analytics"
        )

    def get_predictive_analytics_sync(self) -> APIResponse:
        """Get predictive analytics dashboard (sync)"""
        return self._make_sync_request("GET", "/api/v1/dashboard/predictive-analytics")

    async def get_compliance_dashboard(self) -> APIResponse:
        """Get enterprise compliance dashboard"""
        return await self._make_async_request("GET", "/api/v1/dashboard/compliance")

    def get_compliance_dashboard_sync(self) -> APIResponse:
        """Get enterprise compliance dashboard (sync)"""
        return self._make_sync_request("GET", "/api/v1/dashboard/compliance")

    async def get_executive_summary(self) -> APIResponse:
        """Get executive summary dashboard"""
        return await self._make_async_request(
            "GET", "/api/v1/dashboard/executive-summary"
        )

    def get_executive_summary_sync(self) -> APIResponse:
        """Get executive summary dashboard (sync)"""
        return self._make_sync_request("GET", "/api/v1/dashboard/executive-summary")

    async def create_custom_report(
        self, title: str, description: str, parameters: Dict[str, Any], created_by: str
    ) -> APIResponse:
        """Create a custom report"""
        data = {
            "title": title,
            "description": description,
            "parameters": parameters,
            "created_by": created_by,
        }
        return await self._make_async_request("POST", "/api/v1/reports", data=data)

    def create_custom_report_sync(
        self, title: str, description: str, parameters: Dict[str, Any], created_by: str
    ) -> APIResponse:
        """Create a custom report (sync)"""
        data = {
            "title": title,
            "description": description,
            "parameters": parameters,
            "created_by": created_by,
        }
        return self._make_sync_request("POST", "/api/v1/reports", data=data)

    async def get_custom_report(self, report_id: str) -> APIResponse:
        """Get a custom report by ID"""
        return await self._make_async_request("GET", f"/api/v1/reports/{report_id}")

    def get_custom_report_sync(self, report_id: str) -> APIResponse:
        """Get a custom report by ID (sync)"""
        return self._make_sync_request("GET", f"/api/v1/reports/{report_id}")

    # ML Oracle API Methods
    async def get_prediction(
        self,
        prediction_type: str,
        input_data: Dict[str, Any],
        confidence_threshold: float = 0.7,
    ) -> APIResponse:
        """Get ML Oracle prediction"""
        data = {
            "prediction_type": prediction_type,
            "input_data": input_data,
            "confidence_threshold": confidence_threshold,
        }
        return await self._make_async_request(
            "POST", "/api/v1/oracle/predict", data=data
        )

    def get_prediction_sync(
        self,
        prediction_type: str,
        input_data: Dict[str, Any],
        confidence_threshold: float = 0.7,
    ) -> APIResponse:
        """Get ML Oracle prediction (sync)"""
        data = {
            "prediction_type": prediction_type,
            "input_data": input_data,
            "confidence_threshold": confidence_threshold,
        }
        return self._make_sync_request("POST", "/api/v1/oracle/predict", data=data)

    async def get_oracle_health(self) -> APIResponse:
        """Get ML Oracle health status"""
        return await self._make_async_request("GET", "/api/v1/oracle/health")

    def get_oracle_health_sync(self) -> APIResponse:
        """Get ML Oracle health status (sync)"""
        return self._make_sync_request("GET", "/api/v1/oracle/health")

    # System Status Methods
    async def get_system_status(self) -> APIResponse:
        """Get comprehensive system status"""
        return await self._make_async_request("GET", "/api/v1/status")

    def get_system_status_sync(self) -> APIResponse:
        """Get comprehensive system status (sync)"""
        return self._make_sync_request("GET", "/api/v1/status")

    # WebSocket Real-time Integration
    async def connect_websocket(self, endpoint: str = "/ws") -> bool:
        """Connect to WebSocket for real-time updates"""
        try:
            ws_url = self.config.base_url.replace("http://", "ws://").replace(
                "https://", "wss://"
            )
            ws_url = urljoin(ws_url, endpoint.lstrip("/"))

            self.websocket_connection = await websockets.connect(ws_url)
            logger.info(f"WebSocket connected to {ws_url}")
            return True

        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return False

    async def listen_websocket(self, message_handler: Callable[[Dict], None]):
        """Listen for WebSocket messages"""
        if not self.websocket_connection:
            raise RuntimeError("WebSocket not connected")

        try:
            async for message in self.websocket_connection:
                try:
                    data = json.loads(message)
                    await message_handler(data)
                except Exception as e:
                    logger.error(f"WebSocket message handling error: {e}")

        except Exception as e:
            logger.error(f"WebSocket listening error: {e}")

    async def send_websocket_message(self, message: Dict[str, Any]):
        """Send message via WebSocket"""
        if not self.websocket_connection:
            raise RuntimeError("WebSocket not connected")

        await self.websocket_connection.send(json.dumps(message))

    async def disconnect_websocket(self):
        """Disconnect WebSocket"""
        if self.websocket_connection:
            await self.websocket_connection.close()
            self.websocket_connection = None
            logger.info("WebSocket disconnected")

    # Webhook Event Handling
    def register_webhook_handler(
        self, event_type: str, handler: Callable[[Dict], None]
    ):
        """Register webhook event handler"""
        self.webhook_handlers[event_type] = handler
        logger.info(f"Registered webhook handler for {event_type}")

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature"""
        if not self.config.webhook_secret:
            return True  # No verification if no secret configured

        expected_signature = hmac.new(
            self.config.webhook_secret.encode(), payload.encode(), hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    async def handle_webhook(self, payload: Dict[str, Any]) -> bool:
        """Handle incoming webhook"""
        event_type = payload.get("event_type")
        if event_type in self.webhook_handlers:
            try:
                await self.webhook_handlers[event_type](payload)
                return True
            except Exception as e:
                logger.error(f"Webhook handler error for {event_type}: {e}")

        return False

    # SDK Code Generation for Other Languages
    def generate_javascript_sdk(self, output_path: str = "trustwrapper-sdk.js"):
        """Generate JavaScript/TypeScript SDK"""
        js_code = """
/**
 * TrustWrapper Enterprise SDK for JavaScript/TypeScript
 * Auto-generated from Python SDK
 */

class TrustWrapperSDK {
    constructor(config) {
        this.config = {
            baseUrl: config.baseUrl,
            apiKey: config.apiKey,
            timeout: config.timeout || 30000,
            ...config
        };

        this.cache = new Map();
    }

    async _makeRequest(method, endpoint, options = {}) {
        const url = new URL(endpoint, this.config.baseUrl);

        const headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TrustWrapper-JS-SDK/3.0',
            ...options.headers
        };

        if (this.config.apiKey) {
            headers['X-API-Key'] = this.config.apiKey;
        }

        const fetchOptions = {
            method,
            headers,
            ...options
        };

        if (options.data) {
            fetchOptions.body = JSON.stringify(options.data);
        }

        try {
            const response = await fetch(url.toString(), fetchOptions);
            const data = await response.json();

            return {
                success: response.ok,
                data: response.ok ? data : null,
                error: !response.ok ? data : null,
                statusCode: response.status,
                timestamp: Date.now()
            };
        } catch (error) {
            return {
                success: false,
                data: null,
                error: error.message,
                statusCode: 0,
                timestamp: Date.now()
            };
        }
    }

    // Analytics Dashboard Methods
    async getRealTimeMetrics() {
        return this._makeRequest('GET', '/api/v1/dashboard/real-time-metrics');
    }

    async getPredictiveAnalytics() {
        return this._makeRequest('GET', '/api/v1/dashboard/predictive-analytics');
    }

    async getComplianceDashboard() {
        return this._makeRequest('GET', '/api/v1/dashboard/compliance');
    }

    async getExecutiveSummary() {
        return this._makeRequest('GET', '/api/v1/dashboard/executive-summary');
    }

    async createCustomReport(title, description, parameters, createdBy) {
        return this._makeRequest('POST', '/api/v1/reports', {
            data: { title, description, parameters, created_by: createdBy }
        });
    }

    async getCustomReport(reportId) {
        return this._makeRequest('GET', `/api/v1/reports/${reportId}`);
    }

    // ML Oracle Methods
    async getPrediction(predictionType, inputData, confidenceThreshold = 0.7) {
        return this._makeRequest('POST', '/api/v1/oracle/predict', {
            data: {
                prediction_type: predictionType,
                input_data: inputData,
                confidence_threshold: confidenceThreshold
            }
        });
    }

    async getOracleHealth() {
        return this._makeRequest('GET', '/api/v1/oracle/health');
    }

    async getSystemStatus() {
        return this._makeRequest('GET', '/api/v1/status');
    }
}

module.exports = TrustWrapperSDK;
"""

        with open(output_path, "w") as f:
            f.write(js_code)

        logger.info(f"JavaScript SDK generated: {output_path}")

    def generate_curl_examples(self, output_path: str = "api-examples.sh"):
        """Generate cURL examples"""
        curl_examples = f"""#!/bin/bash

# TrustWrapper v3.0 API Examples using cURL
# Base URL: {self.config.base_url}

# Set your API key
API_KEY="{self.config.api_key or 'your_api_key_here'}"
BASE_URL="{self.config.base_url}"

echo "TrustWrapper v3.0 API Examples"
echo "=============================="

# Health Check
echo "1. Health Check"
curl -X GET "$BASE_URL/health" \\
  -H "X-API-Key: $API_KEY" \\
  -H "Content-Type: application/json"

echo -e "\\n\\n2. Real-time Metrics"
curl -X GET "$BASE_URL/api/v1/dashboard/real-time-metrics" \\
  -H "X-API-Key: $API_KEY" \\
  -H "Content-Type: application/json"

echo -e "\\n\\n3. Predictive Analytics"
curl -X GET "$BASE_URL/api/v1/dashboard/predictive-analytics" \\
  -H "X-API-Key: $API_KEY" \\
  -H "Content-Type: application/json"

echo -e "\\n\\n4. Create Custom Report"
curl -X POST "$BASE_URL/api/v1/reports" \\
  -H "X-API-Key: $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "title": "Sample Report",
    "description": "A sample custom report",
    "parameters": {{
      "time_range": "24h",
      "metrics": ["accuracy_rate", "throughput"],
      "aggregation": "hourly"
    }},
    "created_by": "api_example"
  }}'

echo -e "\\n\\n5. ML Oracle Prediction"
curl -X POST "$BASE_URL/api/v1/oracle/predict" \\
  -H "X-API-Key: $API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "prediction_type": "market_trend",
    "input_data": {{
      "market": "crypto",
      "timeframe": "1h"
    }},
    "confidence_threshold": 0.8
  }}'

echo -e "\\n\\n6. System Status"
curl -X GET "$BASE_URL/api/v1/status" \\
  -H "X-API-Key: $API_KEY" \\
  -H "Content-Type: application/json"

echo -e "\\n\\nDone!"
"""

        with open(output_path, "w") as f:
            f.write(curl_examples)

        import stat

        Path(output_path).chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)

        logger.info(f"cURL examples generated: {output_path}")

    def generate_openapi_spec(self, output_path: str = "openapi.json"):
        """Generate OpenAPI specification"""
        openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "TrustWrapper v3.0 Enterprise API",
                "description": "Enterprise-grade AI verification platform API",
                "version": "3.0.0",
                "contact": {
                    "name": "TrustWrapper Support",
                    "url": "https://trustwrapper.com/support",
                },
            },
            "servers": [
                {
                    "url": self.config.base_url,
                    "description": "TrustWrapper Enterprise API",
                }
            ],
            "security": [{"apiKey": []}, {"bearerAuth": []}],
            "components": {
                "securitySchemes": {
                    "apiKey": {"type": "apiKey", "in": "header", "name": "X-API-Key"},
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                    },
                }
            },
            "paths": {
                "/health": {
                    "get": {
                        "summary": "Health check",
                        "description": "Get API health status",
                        "responses": {
                            "200": {"description": "Health check successful"}
                        },
                    }
                },
                "/api/v1/dashboard/real-time-metrics": {
                    "get": {
                        "summary": "Get real-time metrics",
                        "description": "Retrieve real-time performance metrics",
                        "security": [{"apiKey": []}],
                        "responses": {
                            "200": {"description": "Real-time metrics retrieved"}
                        },
                    }
                },
                "/api/v1/dashboard/predictive-analytics": {
                    "get": {
                        "summary": "Get predictive analytics",
                        "description": "Retrieve predictive analytics dashboard",
                        "security": [{"apiKey": []}],
                        "responses": {
                            "200": {"description": "Predictive analytics retrieved"}
                        },
                    }
                },
                "/api/v1/reports": {
                    "post": {
                        "summary": "Create custom report",
                        "description": "Create a new custom analytics report",
                        "security": [{"apiKey": []}],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "required": [
                                            "title",
                                            "description",
                                            "parameters",
                                            "created_by",
                                        ],
                                        "properties": {
                                            "title": {"type": "string"},
                                            "description": {"type": "string"},
                                            "parameters": {"type": "object"},
                                            "created_by": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        },
                        "responses": {
                            "200": {"description": "Report created successfully"}
                        },
                    }
                },
            },
        }

        with open(output_path, "w") as f:
            json.dump(openapi_spec, f, indent=2)

        logger.info(f"OpenAPI specification generated: {output_path}")


# Convenience factory functions
def create_enterprise_sdk(
    base_url: str, api_key: str, **kwargs
) -> TrustWrapperEnterpriseSDK:
    """Create enterprise SDK with API key authentication"""
    config = SDKConfig(
        base_url=base_url, api_key=api_key, auth_method=AuthMethod.API_KEY, **kwargs
    )
    return TrustWrapperEnterpriseSDK(config)


def create_jwt_sdk(
    base_url: str, jwt_token: str, **kwargs
) -> TrustWrapperEnterpriseSDK:
    """Create enterprise SDK with JWT authentication"""
    config = SDKConfig(
        base_url=base_url,
        jwt_token=jwt_token,
        auth_method=AuthMethod.JWT_TOKEN,
        **kwargs,
    )
    return TrustWrapperEnterpriseSDK(config)


def create_hmac_sdk(
    base_url: str, api_key: str, secret_key: str, **kwargs
) -> TrustWrapperEnterpriseSDK:
    """Create enterprise SDK with HMAC authentication"""
    config = SDKConfig(
        base_url=base_url,
        api_key=api_key,
        secret_key=secret_key,
        auth_method=AuthMethod.HMAC_SIGNATURE,
        **kwargs,
    )
    return TrustWrapperEnterpriseSDK(config)


# Example usage and testing
async def example_sdk_usage():
    """Example of how to use the Enterprise SDK"""

    print("🚀 TrustWrapper v3.0 Enterprise SDK Demo")
    print("=" * 50)

    # Create SDK instance
    sdk = create_enterprise_sdk(
        base_url="http://localhost:8080",
        api_key="demo_api_key_12345",
        timeout=30.0,
        max_retries=2,
        enable_caching=True,
    )

    # Use async context manager
    async with sdk:
        print("📊 Getting real-time metrics...")
        metrics_response = await sdk.get_real_time_metrics()
        if metrics_response.success:
            print(
                f"   ✅ Metrics retrieved: {len(metrics_response.data.get('metrics', []))} metrics"
            )
        else:
            print(f"   ❌ Error: {metrics_response.error}")

        print("\n🔮 Getting predictive analytics...")
        analytics_response = await sdk.get_predictive_analytics()
        if analytics_response.success:
            print(
                f"   ✅ Analytics retrieved: {len(analytics_response.data.get('predictions', {}))} predictions"
            )
        else:
            print(f"   ❌ Error: {analytics_response.error}")

        print("\n📄 Creating custom report...")
        report_response = await sdk.create_custom_report(
            title="SDK Demo Report",
            description="Testing custom report creation via SDK",
            parameters={
                "time_range": "24h",
                "metrics": ["accuracy_rate", "throughput"],
                "aggregation": "hourly",
                "chart_types": ["line", "bar"],
            },
            created_by="sdk_demo",
        )

        if report_response.success:
            report_id = report_response.data.get("report_id")
            print(f"   ✅ Report created: {report_id}")

            # Get the report
            print(f"\n📈 Retrieving report {report_id}...")
            get_report_response = await sdk.get_custom_report(report_id)
            if get_report_response.success:
                visualizations = len(get_report_response.data.get("visualizations", []))
                print(f"   ✅ Report retrieved: {visualizations} visualizations")
        else:
            print(f"   ❌ Error creating report: {report_response.error}")

        print("\n🏥 Getting system status...")
        status_response = await sdk.get_system_status()
        if status_response.success:
            print(
                f"   ✅ System status: {status_response.data.get('api_status', 'unknown')}"
            )
        else:
            print(f"   ❌ Error: {status_response.error}")

    print("\n📁 Generating SDK artifacts...")

    # Generate JavaScript SDK
    sdk.generate_javascript_sdk("trustwrapper-sdk.js")
    print("   ✅ JavaScript SDK generated")

    # Generate cURL examples
    sdk.generate_curl_examples("api-examples.sh")
    print("   ✅ cURL examples generated")

    # Generate OpenAPI spec
    sdk.generate_openapi_spec("openapi.json")
    print("   ✅ OpenAPI specification generated")

    print("\n✨ SDK demo completed successfully!")
    print("🎉 Enterprise Integration Tools ready for deployment!")


if __name__ == "__main__":
    asyncio.run(example_sdk_usage())

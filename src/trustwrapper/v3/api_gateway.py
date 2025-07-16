#!/usr/bin/env python3
"""
TrustWrapper v3.0 API Gateway
Core REST API endpoints for universal multi-chain AI verification
Task 3.1: Week 3 Phase 1 Implementation
"""

import asyncio
import hashlib
import logging
import time
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional

import uvicorn

# FastAPI imports
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, validator

from .enhanced_oracle_integration import (
    get_enhanced_oracle_integration,
)

# Import TrustWrapper v3.0 components
from .multi_chain_connection_manager import (
    SecurityLevel,
    UniversalVerificationResult,
    VerificationRequest,
    get_connection_manager,
)
from .scaling_infrastructure import ProcessingPriority, get_scaling_infrastructure


# API Models
class VerificationRequestModel(BaseModel):
    """API model for verification requests"""

    ai_decision_data: Dict[str, Any] = Field(
        ..., description="AI decision data to verify"
    )
    security_level: str = Field(
        default="standard", description="Security level: basic, standard, high, maximum"
    )
    target_chains: Optional[List[str]] = Field(
        None, description="Specific chains to target (optional)"
    )
    oracle_validation: bool = Field(True, description="Enable oracle validation")
    custom_threshold: Optional[float] = Field(
        None, description="Custom consensus threshold"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    @validator("security_level")
    def validate_security_level(cls, v):
        valid_levels = ["basic", "standard", "high", "maximum"]
        if v.lower() not in valid_levels:
            raise ValueError(f"Security level must be one of: {valid_levels}")
        return v.lower()

    @validator("custom_threshold")
    def validate_threshold(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError("Custom threshold must be between 0.0 and 1.0")
        return v


class VerificationResponseModel(BaseModel):
    """API model for verification responses"""

    verification_id: str
    request_id: str
    overall_success: bool
    consensus_score: float
    security_level: str
    total_chains: int
    successful_chains: int
    failed_chains: int
    execution_time_seconds: float
    oracle_consensus: Optional[Dict[str, Any]]
    chain_results: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    recommendations: List[str]
    timestamp: float


class ConsensusRequestModel(BaseModel):
    """API model for consensus requests"""

    verification_ids: List[str] = Field(
        ..., description="List of verification IDs to aggregate"
    )
    consensus_algorithm: str = Field(
        default="weighted_byzantine", description="Consensus algorithm to use"
    )
    minimum_verifications: int = Field(
        default=3, description="Minimum verifications required"
    )

    @validator("consensus_algorithm")
    def validate_algorithm(cls, v):
        valid_algorithms = [
            "weighted_byzantine",
            "pbft",
            "hotstuff",
            "threshold_signature",
        ]
        if v.lower() not in valid_algorithms:
            raise ValueError(f"Algorithm must be one of: {valid_algorithms}")
        return v.lower()


class BridgeOperationModel(BaseModel):
    """API model for cross-chain bridge operations"""

    source_chain: str = Field(..., description="Source blockchain")
    target_chain: str = Field(..., description="Target blockchain")
    operation_type: str = Field(..., description="Type of bridge operation")
    data_payload: Dict[str, Any] = Field(..., description="Data to bridge")
    priority: str = Field(default="normal", description="Operation priority")

    @validator("priority")
    def validate_priority(cls, v):
        valid_priorities = ["critical", "high", "normal", "low"]
        if v.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {valid_priorities}")
        return v.lower()


class HealthStatus(str, Enum):
    """Health status enumeration"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthResponseModel(BaseModel):
    """API model for health responses"""

    status: HealthStatus
    timestamp: float
    version: str
    uptime_seconds: float
    system_health: Dict[str, Any]
    component_status: Dict[str, bool]
    performance_metrics: Dict[str, float]


# API Gateway Class
class TrustWrapperAPIGateway:
    """
    TrustWrapper v3.0 API Gateway
    Provides REST API endpoints for universal multi-chain AI verification
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # FastAPI app
        self.app = FastAPI(
            title="TrustWrapper v3.0 API",
            description="Universal Multi-Chain AI Verification Platform",
            version="3.0.0",
            docs_url="/docs",
            redoc_url="/redoc",
        )

        # Security
        self.security = HTTPBearer()

        # Core components
        self.connection_manager = None
        self.scaling_infrastructure = None
        self.oracle_integration = None

        # State
        self.start_time = time.time()
        self.request_count = 0
        self.error_count = 0

        # Setup middleware and routes
        self._setup_middleware()
        self._setup_routes()

    async def initialize(self):
        """Initialize API gateway with core components"""
        try:
            self.logger.info("🚀 Initializing TrustWrapper v3.0 API Gateway...")

            # Initialize core components
            self.connection_manager = await get_connection_manager()
            self.scaling_infrastructure = await get_scaling_infrastructure()
            self.oracle_integration = await get_enhanced_oracle_integration()

            self.logger.info("✅ API Gateway initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize API Gateway: {e}")
            raise

    def _setup_middleware(self):
        """Setup FastAPI middleware"""

        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Gzip compression
        self.app.add_middleware(GZipMiddleware, minimum_size=1000)

        # Request/response middleware
        @self.app.middleware("http")
        async def process_requests(request: Request, call_next):
            start_time = time.time()

            # Track request
            self.request_count += 1
            request_id = str(uuid.uuid4())

            # Add request ID to headers
            request.state.request_id = request_id

            try:
                response = await call_next(request)

                # Add response headers
                response.headers["X-Request-ID"] = request_id
                response.headers["X-Response-Time"] = f"{time.time() - start_time:.3f}s"

                return response

            except Exception as e:
                self.error_count += 1
                self.logger.error(f"Request {request_id} failed: {e}")

                return JSONResponse(
                    status_code=500,
                    content={
                        "error": "Internal server error",
                        "request_id": request_id,
                        "timestamp": time.time(),
                    },
                )

    def _setup_routes(self):
        """Setup API routes"""

        # Root endpoint
        @self.app.get("/", response_model=Dict[str, Any])
        async def root():
            """Root endpoint with API information"""
            return {
                "name": "TrustWrapper v3.0 API",
                "version": "3.0.0",
                "description": "Universal Multi-Chain AI Verification Platform",
                "status": "operational",
                "timestamp": time.time(),
                "endpoints": {
                    "verify": "/verify - AI verification endpoint",
                    "consensus": "/consensus - Multi-verification consensus",
                    "bridge": "/bridge - Cross-chain bridge operations",
                    "health": "/health - System health status",
                    "docs": "/docs - API documentation",
                },
            }

        # Health endpoint
        @self.app.get("/health", response_model=HealthResponseModel)
        async def health():
            """System health status endpoint"""
            try:
                # Get system health from connection manager
                system_health = await self.connection_manager.get_system_health()

                # Get performance metrics from scaling infrastructure
                performance_metrics = (
                    self.scaling_infrastructure.get_performance_metrics()
                )

                # Determine overall status
                overall_health = system_health.overall_health_score
                if overall_health >= 0.8:
                    status = HealthStatus.HEALTHY
                elif overall_health >= 0.5:
                    status = HealthStatus.DEGRADED
                else:
                    status = HealthStatus.UNHEALTHY

                return HealthResponseModel(
                    status=status,
                    timestamp=time.time(),
                    version="3.0.0",
                    uptime_seconds=time.time() - self.start_time,
                    system_health=system_health.to_dict(),
                    component_status={
                        "connection_manager": self.connection_manager.initialized,
                        "scaling_infrastructure": self.scaling_infrastructure.initialized,
                        "oracle_integration": (
                            self.oracle_integration.running
                            if self.oracle_integration
                            else False
                        ),
                    },
                    performance_metrics={
                        "total_requests": self.request_count,
                        "error_rate": self.error_count / max(self.request_count, 1),
                        "cache_hit_rate": performance_metrics["cache_metrics"][
                            "hit_rate"
                        ],
                        "redis_response_time": performance_metrics["redis_metrics"][
                            "avg_response_time"
                        ],
                    },
                )

            except Exception as e:
                self.logger.error(f"Health check failed: {e}")
                raise HTTPException(
                    status_code=503, detail="Service temporarily unavailable"
                )

        # Verify endpoint
        @self.app.post("/verify", response_model=VerificationResponseModel)
        async def verify(
            request: VerificationRequestModel,
            background_tasks: BackgroundTasks,
            credentials: HTTPAuthorizationCredentials = Depends(self.security),
        ):
            """
            AI verification endpoint
            Performs universal multi-chain verification of AI decisions
            """
            try:
                # Validate authentication (simplified for demo)
                if not await self._validate_token(credentials.credentials):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication token",
                    )

                # Generate unique request ID
                request_id = (
                    f"api_verify_{int(time.time() * 1000)}_{str(uuid.uuid4())[:8]}"
                )

                # Convert security level
                security_level = SecurityLevel(request.security_level.upper())

                # Create verification request
                verification_request = VerificationRequest(
                    request_id=request_id,
                    ai_decision_data=request.ai_decision_data,
                    security_level=security_level,
                    target_chains=request.target_chains,
                    oracle_validation=request.oracle_validation,
                    custom_threshold=request.custom_threshold,
                    metadata=request.metadata or {},
                )

                # Submit verification task to scaling infrastructure
                verification_coro = (
                    self.connection_manager.universal_verify_ai_decision(
                        verification_request
                    )
                )

                task_submitted = (
                    await self.scaling_infrastructure.submit_verification_task(
                        request_id, verification_coro, ProcessingPriority.HIGH
                    )
                )

                if not task_submitted:
                    raise HTTPException(
                        status_code=503,
                        detail="Verification service temporarily overloaded",
                    )

                # Get verification result
                verification_result = (
                    await self.scaling_infrastructure.task_manager.get_task_result(
                        f"verify_{request_id}", timeout=60.0
                    )
                )

                # Cache result in background
                background_tasks.add_task(
                    self._cache_verification_result, request_id, verification_result
                )

                # Convert oracle consensus for response
                oracle_consensus_dict = None
                if verification_result.oracle_consensus:
                    oracle_consensus_dict = (
                        verification_result.oracle_consensus.to_dict()
                    )

                return VerificationResponseModel(
                    verification_id=verification_result.verification_id,
                    request_id=verification_result.request_id,
                    overall_success=verification_result.overall_success,
                    consensus_score=verification_result.consensus_score,
                    security_level=verification_result.security_level.value,
                    total_chains=verification_result.total_chains,
                    successful_chains=verification_result.successful_chains,
                    failed_chains=verification_result.failed_chains,
                    execution_time_seconds=verification_result.execution_time_seconds,
                    oracle_consensus=oracle_consensus_dict,
                    chain_results=verification_result.chain_results,
                    risk_assessment=verification_result.risk_assessment,
                    recommendations=verification_result.recommendations,
                    timestamp=verification_result.timestamp,
                )

            except asyncio.TimeoutError:
                raise HTTPException(
                    status_code=408, detail="Verification request timed out"
                )
            except Exception as e:
                self.logger.error(f"Verification failed: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Verification failed: {str(e)}"
                )

        # Consensus endpoint
        @self.app.post("/consensus", response_model=Dict[str, Any])
        async def consensus(
            request: ConsensusRequestModel,
            credentials: HTTPAuthorizationCredentials = Depends(self.security),
        ):
            """
            Multi-verification consensus endpoint
            Aggregates multiple verifications into consensus result
            """
            try:
                # Validate authentication
                if not await self._validate_token(credentials.credentials):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication token",
                    )

                # Retrieve verification results from cache
                verification_results = []
                for verification_id in request.verification_ids:
                    cached_result = await self.scaling_infrastructure.cache_layer.get_verification_result(
                        verification_id
                    )
                    if cached_result:
                        verification_results.append(cached_result)

                if len(verification_results) < request.minimum_verifications:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Insufficient verifications: need {request.minimum_verifications}, got {len(verification_results)}",
                    )

                # Calculate consensus
                consensus_result = await self._calculate_consensus(
                    verification_results, request.consensus_algorithm
                )

                return {
                    "consensus_id": f"consensus_{int(time.time() * 1000)}",
                    "algorithm": request.consensus_algorithm,
                    "verification_count": len(verification_results),
                    "consensus_score": consensus_result["consensus_score"],
                    "recommendation": consensus_result["recommendation"],
                    "confidence": consensus_result["confidence"],
                    "aggregated_results": consensus_result["aggregated_results"],
                    "timestamp": time.time(),
                }

            except Exception as e:
                self.logger.error(f"Consensus calculation failed: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Consensus calculation failed: {str(e)}"
                )

        # Bridge endpoint
        @self.app.post("/bridge", response_model=Dict[str, Any])
        async def bridge(
            request: BridgeOperationModel,
            credentials: HTTPAuthorizationCredentials = Depends(self.security),
        ):
            """
            Cross-chain bridge operations endpoint
            Facilitates cross-chain message passing and operations
            """
            try:
                # Validate authentication
                if not await self._validate_token(credentials.credentials):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication token",
                    )

                # Generate bridge operation ID
                operation_id = (
                    f"bridge_{int(time.time() * 1000)}_{str(uuid.uuid4())[:8]}"
                )

                # Convert priority
                priority = ProcessingPriority(request.priority.upper())

                # Create bridge operation coroutine
                async def bridge_operation():
                    # Simulate bridge operation (would be actual cross-chain operation)
                    await asyncio.sleep(1.0)  # Simulate processing time

                    return {
                        "operation_id": operation_id,
                        "source_chain": request.source_chain,
                        "target_chain": request.target_chain,
                        "operation_type": request.operation_type,
                        "status": "completed",
                        "transaction_hashes": {
                            request.source_chain: f"0x{hashlib.sha256(f'{operation_id}_source'.encode()).hexdigest()}",
                            request.target_chain: f"0x{hashlib.sha256(f'{operation_id}_target'.encode()).hexdigest()}",
                        },
                        "execution_time": 1.0,
                    }

                # Submit bridge operation
                task_submitted = (
                    await self.scaling_infrastructure.task_manager.submit_task(
                        operation_id, bridge_operation(), priority
                    )
                )

                if not task_submitted:
                    raise HTTPException(
                        status_code=503, detail="Bridge service temporarily overloaded"
                    )

                # Get operation result
                bridge_result = (
                    await self.scaling_infrastructure.task_manager.get_task_result(
                        operation_id, timeout=30.0
                    )
                )

                return {
                    **bridge_result,
                    "timestamp": time.time(),
                    "priority": request.priority,
                }

            except asyncio.TimeoutError:
                raise HTTPException(
                    status_code=408, detail="Bridge operation timed out"
                )
            except Exception as e:
                self.logger.error(f"Bridge operation failed: {e}")
                raise HTTPException(
                    status_code=500, detail=f"Bridge operation failed: {str(e)}"
                )

        # Oracle endpoint
        @self.app.get("/oracle/{asset_pair}", response_model=Dict[str, Any])
        async def get_oracle_consensus(
            asset_pair: str,
            credentials: HTTPAuthorizationCredentials = Depends(self.security),
        ):
            """Get oracle consensus for asset pair"""
            try:
                # Validate authentication
                if not await self._validate_token(credentials.credentials):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication token",
                    )

                # Get oracle consensus
                consensus = await self.oracle_integration.get_multi_oracle_consensus(
                    asset_pair
                )

                if not consensus:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No oracle consensus available for {asset_pair}",
                    )

                return {
                    "asset_pair": asset_pair,
                    "consensus": consensus.to_dict(),
                    "timestamp": time.time(),
                }

            except Exception as e:
                self.logger.error(f"Oracle consensus retrieval failed: {e}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Oracle consensus retrieval failed: {str(e)}",
                )

    async def _validate_token(self, token: str) -> bool:
        """Validate authentication token (simplified for demo)"""
        # In production, implement proper JWT validation
        return token and len(token) >= 10  # Simplified validation

    async def _cache_verification_result(
        self, request_id: str, result: UniversalVerificationResult
    ):
        """Cache verification result in background"""
        try:
            result_dict = result.to_dict()
            await self.scaling_infrastructure.cache_layer.cache_verification_result(
                request_id, result_dict
            )
            self.logger.debug(f"Cached verification result: {request_id}")
        except Exception as e:
            self.logger.warning(f"Failed to cache verification result: {e}")

    async def _calculate_consensus(
        self, verification_results: List[Dict[str, Any]], algorithm: str
    ) -> Dict[str, Any]:
        """Calculate consensus from multiple verification results"""
        try:
            # Extract consensus scores
            consensus_scores = [
                result.get("consensus_score", 0.0) for result in verification_results
            ]
            overall_successes = [
                result.get("overall_success", False) for result in verification_results
            ]

            # Calculate aggregated metrics
            avg_consensus_score = sum(consensus_scores) / len(consensus_scores)
            success_rate = sum(overall_successes) / len(overall_successes)

            # Determine recommendation
            if avg_consensus_score >= 0.8 and success_rate >= 0.7:
                recommendation = "APPROVE"
                confidence = "HIGH"
            elif avg_consensus_score >= 0.6 and success_rate >= 0.5:
                recommendation = "CONDITIONAL_APPROVE"
                confidence = "MEDIUM"
            else:
                recommendation = "REJECT"
                confidence = "LOW"

            return {
                "consensus_score": avg_consensus_score,
                "success_rate": success_rate,
                "recommendation": recommendation,
                "confidence": confidence,
                "aggregated_results": {
                    "average_consensus": avg_consensus_score,
                    "verification_success_rate": success_rate,
                    "total_verifications": len(verification_results),
                    "algorithm_used": algorithm,
                },
            }

        except Exception as e:
            self.logger.error(f"Consensus calculation error: {e}")
            raise

    async def shutdown(self):
        """Shutdown API gateway"""
        self.logger.info("🛑 Shutting down API Gateway...")

        # Shutdown core components
        if self.connection_manager:
            await self.connection_manager.shutdown()

        if self.scaling_infrastructure:
            await self.scaling_infrastructure.shutdown()

        if self.oracle_integration:
            await self.oracle_integration.stop()


# Global API gateway instance
_api_gateway_instance = None


async def get_api_gateway() -> TrustWrapperAPIGateway:
    """Get or create the global API gateway instance"""
    global _api_gateway_instance

    if _api_gateway_instance is None:
        _api_gateway_instance = TrustWrapperAPIGateway()
        await _api_gateway_instance.initialize()

    return _api_gateway_instance


def create_app() -> FastAPI:
    """Create FastAPI application for deployment"""
    gateway = TrustWrapperAPIGateway()
    return gateway.app


# Development server
if __name__ == "__main__":
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Run development server
    uvicorn.run(
        "api_gateway:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

"""
TrustWrapper REST API
Production-ready API endpoints for ZK-verified AI hallucination detection
"""

import asyncio
import os
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

try:
    from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from pydantic import BaseModel, Field
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    print("⚠️  FastAPI not installed. Run: pip install fastapi uvicorn")

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from core.enhanced_trust_wrapper import EnhancedTrustWrapper, create_enhanced_trust_wrapper
from core.enhanced_hallucination_detector import create_enhanced_detector
from demos.hallucination_testing_demo import MockLanguageModel


# Pydantic models for API
class TextValidationRequest(BaseModel):
    text: str = Field(..., description="Text to validate for hallucinations")
    context: Optional[Dict[str, Any]] = Field(None, description="Optional context for validation")


class ModelQueryRequest(BaseModel):
    query: str = Field(..., description="Query to send to the AI model")
    model_name: Optional[str] = Field("default", description="AI model to use")
    enable_zk_proofs: bool = Field(True, description="Enable ZK proof generation")


class BatchValidationRequest(BaseModel):
    texts: List[str] = Field(..., max_items=10, description="Up to 10 texts to validate")
    enable_zk_proofs: bool = Field(True, description="Enable ZK proof generation")


class ValidationResponse(BaseModel):
    text: str
    has_hallucination: bool
    trust_score: float
    hallucinations: List[Dict[str, Any]]
    detection_time_ms: int
    zk_proof: Optional[Dict[str, Any]] = None
    ai_services_used: List[str]
    timestamp: str


class ModelResponse(BaseModel):
    query: str
    response: str
    validation: ValidationResponse
    metrics: Dict[str, Any]
    verification_method: str


class BatchValidationResponse(BaseModel):
    results: List[ValidationResponse]
    batch_stats: Dict[str, Any]
    total_processing_time_ms: int


class HealthResponse(BaseModel):
    status: str
    version: str
    ai_services: List[str]
    zk_proofs_enabled: bool
    leo_available: bool
    uptime_seconds: int


# Initialize FastAPI app
if HAS_FASTAPI:
    app = FastAPI(
        title="TrustWrapper API",
        description="ZK-verified AI hallucination detection service",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Security
    security = HTTPBearer()
    
    # Global state
    app.state.start_time = time.time()
    app.state.request_count = 0
    app.state.models = {}
    app.state.detector = None


# Authentication (simple API key for demo)
def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key"""
    api_key = os.getenv("TRUSTWRAPPER_API_KEY", "demo-key")
    if credentials.credentials != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials


# Initialize components
async def get_detector():
    """Get or create hallucination detector"""
    if not app.state.detector:
        app.state.detector = create_enhanced_detector()
    return app.state.detector


async def get_model(model_name: str = "default"):
    """Get or create AI model wrapper"""
    if model_name not in app.state.models:
        # For demo, use mock model. In production, integrate real models
        base_model = MockLanguageModel()
        app.state.models[model_name] = create_enhanced_trust_wrapper(
            model=base_model,
            model_name=model_name,
            enable_zk_proofs=True
        )
    return app.state.models[model_name]


if HAS_FASTAPI:
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        print("🚀 TrustWrapper API starting...")
        app.state.detector = await get_detector()
        app.state.default_model = await get_model("default")
        print(f"✅ API ready with services: {', '.join(app.state.detector.available_services)}")
    
    
    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check endpoint"""
        detector = await get_detector()
        default_model = await get_model()
        
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            ai_services=detector.available_services,
            zk_proofs_enabled=default_model.enable_zk_proofs,
            leo_available=default_model.zk_generator.leo_available if default_model.zk_generator else False,
            uptime_seconds=int(time.time() - app.state.start_time)
        )
    
    
    @app.post("/validate/text", response_model=ValidationResponse)
    async def validate_text(
        request: TextValidationRequest,
        background_tasks: BackgroundTasks,
        api_key: str = Depends(verify_api_key)
    ):
        """Validate text for hallucinations"""
        app.state.request_count += 1
        
        try:
            model = await get_model()
            result = await model.validate_response_text(request.text)
            
            # Background task for analytics
            background_tasks.add_task(log_validation, "text", request.text, result)
            
            return ValidationResponse(
                text=request.text,
                has_hallucination=result['hallucination_detection']['has_hallucination'],
                trust_score=result['trust_score'],
                hallucinations=result['hallucination_detection']['hallucinations'],
                detection_time_ms=result['hallucination_detection']['detection_time_ms'],
                zk_proof=result['zk_proof'],
                ai_services_used=result['ai_services_used'],
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
    
    
    @app.post("/validate/batch", response_model=BatchValidationResponse)
    async def validate_batch(
        request: BatchValidationRequest,
        background_tasks: BackgroundTasks,
        api_key: str = Depends(verify_api_key)
    ):
        """Batch validate multiple texts"""
        if len(request.texts) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 texts per batch")
        
        app.state.request_count += 1
        start_time = time.time()
        
        try:
            model = await get_model()
            
            # Process each text
            results = []
            for text in request.texts:
                result = await model.validate_response_text(text)
                
                validation_response = ValidationResponse(
                    text=text,
                    has_hallucination=result['hallucination_detection']['has_hallucination'],
                    trust_score=result['trust_score'],
                    hallucinations=result['hallucination_detection']['hallucinations'],
                    detection_time_ms=result['hallucination_detection']['detection_time_ms'],
                    zk_proof=result['zk_proof'],
                    ai_services_used=result['ai_services_used'],
                    timestamp=datetime.now().isoformat()
                )
                results.append(validation_response)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            # Calculate batch stats
            batch_stats = {
                "total_texts": len(request.texts),
                "hallucinations_detected": sum(1 for r in results if r.has_hallucination),
                "average_trust_score": sum(r.trust_score for r in results) / len(results),
                "average_detection_time_ms": sum(r.detection_time_ms for r in results) / len(results)
            }
            
            # Background task for analytics
            background_tasks.add_task(log_batch_validation, request.texts, results)
            
            return BatchValidationResponse(
                results=results,
                batch_stats=batch_stats,
                total_processing_time_ms=processing_time
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch validation failed: {str(e)}")
    
    
    @app.post("/query/model", response_model=ModelResponse)
    async def query_model(
        request: ModelQueryRequest,
        background_tasks: BackgroundTasks,
        api_key: str = Depends(verify_api_key)
    ):
        """Query AI model with TrustWrapper verification"""
        app.state.request_count += 1
        
        try:
            model = await get_model(request.model_name)
            result = await model.verified_execute(request.query)
            
            validation_response = ValidationResponse(
                text=str(result.data),
                has_hallucination=result.hallucination_detection['has_hallucination'],
                trust_score=result.trust_score,
                hallucinations=result.hallucination_detection['hallucinations'],
                detection_time_ms=result.hallucination_detection['detection_time_ms'],
                zk_proof=result.zk_proof.to_dict(),
                ai_services_used=result.ai_services_used,
                timestamp=datetime.now().isoformat()
            )
            
            # Background task for analytics
            background_tasks.add_task(log_model_query, request.query, result)
            
            return ModelResponse(
                query=request.query,
                response=str(result.data),
                validation=validation_response,
                metrics=result.metrics,
                verification_method=result.verification_method
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model query failed: {str(e)}")
    
    
    @app.get("/stats/performance")
    async def get_performance_stats(api_key: str = Depends(verify_api_key)):
        """Get performance statistics"""
        try:
            model = await get_model()
            stats = model.get_performance_stats()
            
            # Add API-level stats
            stats.update({
                "api_requests": app.state.request_count,
                "uptime_seconds": int(time.time() - app.state.start_time),
                "models_loaded": len(app.state.models)
            })
            
            return stats
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")
    
    
    @app.get("/verification/stats")
    async def get_verification_stats(api_key: str = Depends(verify_api_key)):
        """Get blockchain verification statistics"""
        try:
            model = await get_model()
            if model.zk_generator:
                total_verifications, total_hallucinations = await model.zk_generator.get_verification_stats()
                return {
                    "total_verifications": total_verifications,
                    "total_hallucinations": total_hallucinations,
                    "hallucination_rate": total_hallucinations / max(total_verifications, 1),
                    "blockchain_network": "testnet"
                }
            else:
                return {
                    "total_verifications": 0,
                    "total_hallucinations": 0,
                    "hallucination_rate": 0.0,
                    "blockchain_network": "disabled"
                }
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Verification stats failed: {str(e)}")


# Background task functions
async def log_validation(validation_type: str, text: str, result: Dict[str, Any]):
    """Log validation for analytics"""
    # In production, this would log to a database or analytics service
    print(f"[ANALYTICS] {validation_type} validation: {len(text)} chars, "
          f"trust_score: {result.get('trust_score', 0):.2f}")


async def log_batch_validation(texts: List[str], results: List[ValidationResponse]):
    """Log batch validation for analytics"""
    print(f"[ANALYTICS] Batch validation: {len(texts)} texts, "
          f"avg_trust: {sum(r.trust_score for r in results) / len(results):.2f}")


async def log_model_query(query: str, result):
    """Log model query for analytics"""
    print(f"[ANALYTICS] Model query: {len(query)} chars, "
          f"trust_score: {result.trust_score:.2f}")


# Development server
if __name__ == "__main__":
    if not HAS_FASTAPI:
        print("❌ FastAPI not available. Install with: pip install fastapi uvicorn")
        exit(1)
    
    import uvicorn
    
    print("🚀 Starting TrustWrapper API server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔑 API Key: demo-key")
    
    uvicorn.run(
        "trustwrapper_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
else:
    # When imported, provide app for deployment
    if not HAS_FASTAPI:
        app = None
        print("⚠️  FastAPI not available for API deployment")

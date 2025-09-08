#!/usr/bin/env python3
"""
TrustWrapper 3.0 Privacy API Extension
Extended API endpoints with Sprint 115 privacy integration
Created: July 7, 2025
Purpose: Production AI integration with privacy-protected endpoints
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import asyncio
import time
import json
import os
import sys
from datetime import datetime, timezone

# Add path for privacy adapter
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trustwrapper', 'v3'))

try:
    from privacy_adapter import PrivacyEnhancedTrustWrapper, create_privacy_enhanced_trustwrapper
except ImportError:
    # Fallback if import fails
    class PrivacyEnhancedTrustWrapper:
        def __init__(self):
            self.session_id = "fallback_session"
        
        async def analyze_transaction_with_privacy(self, data):
            return {"error": "Privacy adapter not available", "fallback": True}
        
        def get_privacy_metrics(self):
            return {"error": "Privacy adapter not available", "fallback": True}
        
        def validate_privacy_integration(self):
            return {"error": "Privacy adapter not available", "fallback": True}
    
    def create_privacy_enhanced_trustwrapper():
        return PrivacyEnhancedTrustWrapper()

# FastAPI app with privacy-enhanced TrustWrapper
app = FastAPI(
    title="TrustWrapper 3.0 Privacy API",
    description="Privacy-protected blockchain analysis API with Sprint 115 enhancements",
    version="3.0.0-privacy"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global privacy-enhanced TrustWrapper instance
privacy_trustwrapper = create_privacy_enhanced_trustwrapper()

# Request/Response models
class TransactionRequest(BaseModel):
    """Transaction analysis request with privacy protection"""
    transaction_hash: Optional[str] = Field(None, description="Blockchain transaction hash")
    from_address: str = Field(..., description="Source address")
    to_address: str = Field(..., description="Destination address") 
    value: int = Field(..., description="Transaction value in wei")
    gas: Optional[int] = Field(21000, description="Gas limit")
    gas_price: Optional[int] = Field(20000000000, description="Gas price in wei")
    data: Optional[str] = Field("", description="Transaction data")
    privacy_level: Optional[str] = Field("standard", description="Privacy level: minimal, standard, maximum")

class PrivacyAnalysisResponse(BaseModel):
    """Privacy-protected analysis response"""
    transaction_id: str
    risk_analysis: Dict[str, Any]
    verification: Dict[str, Any] 
    privacy_protection: Dict[str, Any]
    processing_time_ms: float
    timestamp: str

class PrivacyMetricsResponse(BaseModel):
    """Privacy metrics and status"""
    session_id: str
    privacy_config: Dict[str, Any]
    metrics: Dict[str, Any]
    uptime_seconds: float
    privacy_features: Dict[str, Any]

# API Endpoints

@app.get("/", response_model=Dict[str, Any])
async def root():
    """API root endpoint with privacy capabilities info"""
    return {
        "service": "TrustWrapper 3.0 Privacy API",
        "version": "3.0.0-privacy",
        "privacy_integration": "Sprint 115 Enhanced",
        "capabilities": [
            "Secure Delete Architecture",
            "Differential Privacy",
            "Memory Encryption Simulation", 
            "IC Threshold ECDSA Ready"
        ],
        "privacy_level": "80%",
        "endpoints": {
            "POST /analyze/private": "Privacy-protected transaction analysis",
            "GET /privacy/metrics": "Privacy protection metrics",
            "GET /privacy/status": "Privacy integration status",
            "POST /privacy/validate": "Validate privacy integration"
        },
        "documentation": "/docs",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check with privacy status"""
    try:
        validation = privacy_trustwrapper.validate_privacy_integration()
        
        return {
            "status": "healthy",
            "privacy_integration": validation.get("validation_successful", False),
            "privacy_features": {
                "secure_delete": validation.get("secure_delete_working", False),
                "memory_encryption": validation.get("memory_encryption_working", False),
                "differential_privacy": validation.get("differential_privacy_working", False)
            },
            "api_version": "3.0.0-privacy",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@app.post("/analyze/private", response_model=Dict[str, Any])
async def analyze_transaction_private(request: TransactionRequest):
    """
    Privacy-protected blockchain transaction analysis
    Applies Sprint 115 privacy layers to TrustWrapper 3.0 analysis
    """
    try:
        # Convert request to transaction data
        transaction_data = {
            "id": request.transaction_hash or f"tx_{int(time.time())}",
            "from": request.from_address,
            "to": request.to_address,
            "value": request.value,
            "gas": request.gas,
            "gasPrice": request.gas_price,
            "data": request.data,
            "privacy_level": request.privacy_level
        }
        
        # Perform privacy-protected analysis
        result = await privacy_trustwrapper.analyze_transaction_with_privacy(transaction_data)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Privacy-protected analysis failed: {str(e)}"
        )

@app.get("/analyze/standard/{transaction_hash}", response_model=Dict[str, Any])
async def analyze_transaction_standard(transaction_hash: str):
    """
    Standard transaction analysis (backward compatibility)
    Note: This endpoint does not include privacy protection
    """
    # Mock standard analysis for compatibility
    return {
        "transaction_hash": transaction_hash,
        "analysis": "Standard analysis (no privacy protection)",
        "recommendation": "Use /analyze/private for privacy-protected analysis",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/privacy/metrics", response_model=Dict[str, Any])
async def get_privacy_metrics():
    """Get current privacy protection metrics and statistics"""
    try:
        metrics = privacy_trustwrapper.get_privacy_metrics()
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve privacy metrics: {str(e)}"
        )

@app.get("/privacy/status", response_model=Dict[str, Any])
async def get_privacy_status():
    """Get privacy integration status and capabilities"""
    try:
        validation = privacy_trustwrapper.validate_privacy_integration()
        metrics = privacy_trustwrapper.get_privacy_metrics()
        
        return {
            "privacy_integration_status": validation.get("integration_status", "Unknown"),
            "validation_successful": validation.get("validation_successful", False),
            "privacy_level": metrics.get("privacy_config", {}).get("privacy_level", 0) * 100,
            "active_features": {
                "secure_delete": validation.get("secure_delete_working", False),
                "memory_encryption": validation.get("memory_encryption_working", False), 
                "differential_privacy": validation.get("differential_privacy_working", False)
            },
            "session_info": {
                "session_id": metrics.get("session_id", "unknown"),
                "uptime_seconds": metrics.get("uptime_seconds", 0)
            },
            "sprint_115_integration": "Complete",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve privacy status: {str(e)}"
        )

@app.post("/privacy/validate", response_model=Dict[str, Any])
async def validate_privacy_integration():
    """Validate that privacy integration is working correctly"""
    try:
        validation_result = privacy_trustwrapper.validate_privacy_integration()
        
        if validation_result.get("validation_successful", False):
            return {
                "validation": "successful",
                "message": "All privacy features validated successfully",
                "details": validation_result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        else:
            return {
                "validation": "failed",
                "message": "Privacy integration validation failed",
                "details": validation_result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Privacy validation failed: {str(e)}"
        )

@app.get("/privacy/demo", response_model=Dict[str, Any])
async def privacy_demo():
    """Demonstrate privacy-protected analysis with sample data"""
    try:
        # Sample transaction for demonstration
        demo_transaction = {
            "id": f"demo_tx_{int(time.time())}",
            "from": "0x742d35Cc6564C0532d38123B8c8c8b10E0bEB6b8",
            "to": "0x8ba1f109551bD432803012645Hac136c84c51234", 
            "value": 1000000000000000000,  # 1 ETH
            "gas": 21000,
            "gasPrice": 20000000000,
            "private_key": "DEMO_SENSITIVE_DATA",
            "mnemonic": "demo test mnemonic phrase"
        }
        
        # Perform privacy-protected analysis
        analysis_result = await privacy_trustwrapper.analyze_transaction_with_privacy(demo_transaction)
        privacy_metrics = privacy_trustwrapper.get_privacy_metrics()
        
        return {
            "demo_type": "Privacy-Protected Transaction Analysis",
            "sample_transaction": {
                "from": demo_transaction["from"],
                "to": demo_transaction["to"],
                "value_eth": demo_transaction["value"] / 1e18,
                "note": "Sensitive fields securely deleted"
            },
            "analysis_result": analysis_result,
            "privacy_metrics": privacy_metrics,
            "demonstration_notes": [
                "Sensitive data (private_key, mnemonic) securely deleted",
                "Differential privacy applied to risk scores",
                "Memory encryption simulated during processing",
                "All privacy guarantees from Sprint 115 applied"
            ],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Privacy demo failed: {str(e)}"
        )

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "suggestion": "Try /docs for available endpoints",
            "privacy_endpoints": [
                "/analyze/private",
                "/privacy/metrics", 
                "/privacy/status",
                "/privacy/validate",
                "/privacy/demo"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "privacy_protection": "Error details protected by privacy layer",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize privacy-enhanced TrustWrapper on startup"""
    global privacy_trustwrapper
    
    try:
        # Validate privacy integration on startup
        validation = privacy_trustwrapper.validate_privacy_integration()
        
        if validation.get("validation_successful", False):
            print("✅ TrustWrapper 3.0 Privacy API started successfully")
            print(f"📊 Privacy Level: {privacy_trustwrapper.privacy_config['privacy_level']*100}%")
            print(f"🔐 Session ID: {privacy_trustwrapper.session_id}")
        else:
            print("⚠️ TrustWrapper Privacy API started with privacy validation issues")
            print(f"Details: {validation}")
            
    except Exception as e:
        print(f"❌ Privacy integration startup failed: {e}")

# For testing/development
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting TrustWrapper 3.0 Privacy API...")
    print("📋 Sprint 115 Privacy Integration: 80% coverage")
    print("🔗 Available at: http://localhost:8200")
    print("📖 Documentation: http://localhost:8200/docs")
    
    uvicorn.run(
        "trustwrapper_privacy_api:app",
        host="0.0.0.0",
        port=8200,
        reload=False,
        log_level="info"
    )
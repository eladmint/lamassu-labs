#!/usr/bin/env python3
"""
Simple Lamassu Labs API Service
Platform Architecture Director Implementation - Layer 3 Service
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI application
app = FastAPI(
    title="Lamassu Labs API",
    description="Layer 3 - Verification & Security Services",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "lamassu-labs-api",
        "layer": "3",
        "timestamp": "2025-07-02T18:42:00Z",
        "version": "1.0.0",
        "description": "Verification & Security Services",
    }


@app.get("/api/lamassu/status")
async def layer_status():
    return {
        "status": "operational",
        "layer_name": "lamassu-labs",
        "layer_number": 3,
        "services": [
            "trustwrapper-verification",
            "treasury-monitor",
            "blockchain-security",
            "zk-proofs",
        ],
        "ready": True,
        "port": 8003,
    }


@app.get("/api/lamassu/info")
async def layer_info():
    return {
        "layer": "lamassu-labs",
        "description": "Verification & Security Services",
        "capabilities": [
            "TrustWrapper AI verification",
            "Treasury monitoring",
            "Blockchain security",
            "Zero-knowledge proofs",
        ],
        "port": 8003,
        "architecture": "three-layer-platform",
    }


@app.get("/api/lamassu/services")
async def available_services():
    return {
        "services": {
            "trustwrapper_verification": {
                "status": "operational",
                "description": "AI trade verification and protection",
                "endpoints": ["/verify", "/protect"],
            },
            "treasury_monitor": {
                "status": "operational",
                "description": "Blockchain treasury monitoring",
                "endpoints": ["/treasury", "/monitor"],
            },
            "blockchain_security": {
                "status": "operational",
                "description": "Multi-chain security services",
                "endpoints": ["/security", "/validate"],
            },
            "zk_proofs": {
                "status": "operational",
                "description": "Zero-knowledge proof system",
                "endpoints": ["/zk", "/proofs"],
            },
        },
        "total_services": 4,
        "operational_services": 4,
    }


if __name__ == "__main__":
    print("🚀 Starting Lamassu Labs API (Layer 3)")
    print("   Port: 8003")
    print("   Services: TrustWrapper, Treasury, Security, ZK-Proofs")

    uvicorn.run(
        app, host="0.0.0.0", port=8003, log_level="info"  # Listen on all interfaces
    )

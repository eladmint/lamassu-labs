#!/usr/bin/env python3
"""
TrustWrapper v2.0 Demo API Server (Mock Version)
Provides REST endpoints for institutional demonstrations
"""

import asyncio
import random
import time
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="TrustWrapper v2.0 Demo API",
    description="Institutional DeFi Trust Infrastructure",
    version="2.0.0",
)

# Enable CORS for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TradeRequest(BaseModel):
    pair: str
    action: str
    amount: float
    price: float
    bot_id: Optional[str] = "DEMO_BOT_001"


class PerformanceRequest(BaseModel):
    roi: float
    win_rate: float
    sharpe_ratio: Optional[float] = 1.5
    max_drawdown: Optional[float] = 0.05


@app.get("/")
async def root():
    return {
        "service": "TrustWrapper v2.0 Demo API",
        "status": "operational",
        "endpoints": [
            "/health",
            "/demo/verify/trade",
            "/demo/verify/performance",
            "/demo/metrics",
            "/demo/oracle/status",
        ],
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time(), "version": "2.0.0"}


@app.post("/demo/verify/trade")
async def verify_trade(trade: TradeRequest):
    """Demonstrate real-time trade verification"""
    start_time = time.time()

    # Simulate verification (always under 10ms for demo)
    await asyncio.sleep(random.uniform(0.001, 0.008))

    verification_time = (time.time() - start_time) * 1000

    # Mock verification results
    return {
        "verified": True,
        "confidence": random.uniform(0.85, 0.98),
        "risk_score": random.uniform(0.05, 0.25),
        "violations": [],
        "latency_ms": round(verification_time, 2),
        "sub_10ms": verification_time < 10,
        "timestamp": time.time(),
    }


@app.post("/demo/verify/performance")
async def verify_performance(performance: PerformanceRequest):
    """Demonstrate performance verification with ZK proof"""
    start_time = time.time()

    # Simulate verification
    await asyncio.sleep(random.uniform(0.002, 0.012))

    verification_time = (time.time() - start_time) * 1000

    # Generate mock ZK proof
    zk_proof = f"zk_proof_{int(time.time()*1000)}_{''.join([str(random.randint(0,9)) for _ in range(32)])}"

    return {
        "verified": True,
        "confidence": random.uniform(0.90, 0.99),
        "deviation": random.uniform(0.01, 0.08),
        "zk_proof": zk_proof[:64],
        "privacy_preserved": True,
        "latency_ms": round(verification_time, 2),
        "timestamp": time.time(),
    }


@app.get("/demo/metrics")
async def get_metrics():
    """Get system performance metrics"""
    return {
        "local_verification": {
            "average_latency_ms": random.uniform(3.2, 8.7),
            "sub_10ms_rate": random.uniform(92.5, 99.8),
            "cache_hit_rate": random.uniform(75.0, 95.0),
        },
        "zk_proof_generation": {
            "success_rate": random.uniform(98.5, 99.9),
            "average_time_ms": random.uniform(12.5, 25.8),
        },
        "verification_engine": {
            "total_verifications": random.randint(15000, 25000),
            "success_rate": random.uniform(99.2, 99.9),
        },
        "uptime": "99.99%",
        "timestamp": time.time(),
    }


@app.get("/demo/oracle/status")
async def oracle_status():
    """Get multi-oracle network status"""
    oracles = [
        {
            "name": "Chainlink",
            "status": "healthy",
            "weight": 0.35,
            "reliability": random.uniform(0.95, 0.99),
        },
        {
            "name": "Band Protocol",
            "status": "healthy",
            "weight": 0.25,
            "reliability": random.uniform(0.93, 0.98),
        },
        {
            "name": "Uniswap v3",
            "status": "healthy",
            "weight": 0.25,
            "reliability": random.uniform(0.94, 0.97),
        },
        {
            "name": "Compound",
            "status": "healthy",
            "weight": 0.15,
            "reliability": random.uniform(0.92, 0.96),
        },
    ]

    return {
        "overall_health": "healthy",
        "oracle_count": len(oracles),
        "oracles": oracles,
        "consensus_threshold": 0.67,
        "timestamp": time.time(),
    }


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting TrustWrapper v2.0 Demo API Server (Mock)...")
    print("📊 API will be available at: http://localhost:8091")
    print("📚 API Documentation: http://localhost:8091/docs")
    uvicorn.run(app, host="0.0.0.0", port=8091)

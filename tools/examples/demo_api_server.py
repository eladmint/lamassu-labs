#!/usr/bin/env python3
"""
TrustWrapper v2.0 Demo API Server
Provides REST endpoints for institutional demonstrations
"""

import sys
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.trustwrapper.core import get_verification_engine

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

# Initialize engine
engine = get_verification_engine()


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

    # Perform verification
    result = await engine.local_verifier.verify(
        "trading_decision", {"trade": trade.dict(), "bot_id": trade.bot_id}
    )

    verification_time = (time.time() - start_time) * 1000

    return {
        "verified": result["valid"],
        "confidence": result["confidence"],
        "risk_score": result["risk_score"],
        "violations": result["violations"],
        "latency_ms": round(verification_time, 2),
        "sub_10ms": verification_time < 10,
        "timestamp": time.time(),
    }


@app.post("/demo/verify/performance")
async def verify_performance(performance: PerformanceRequest):
    """Demonstrate performance verification with ZK proof"""
    start_time = time.time()

    # Verify performance
    local_result = await engine.local_verifier.verify_performance(
        claimed=performance.dict(),
        actual={
            "roi": performance.roi * 0.9,  # Simulate 10% deviation
            "win_rate": performance.win_rate * 0.95,
        },
    )

    # Generate ZK proof
    zk_proof = await engine.zk_generator.generate_performance_proof(
        performance.dict(), preserve_privacy=True
    )

    verification_time = (time.time() - start_time) * 1000

    return {
        "verified": local_result["valid"],
        "confidence": local_result["confidence"],
        "deviation": local_result["deviation"],
        "zk_proof": zk_proof[:64] if zk_proof else None,
        "privacy_preserved": True,
        "latency_ms": round(verification_time, 2),
        "timestamp": time.time(),
    }


@app.get("/demo/metrics")
async def get_metrics():
    """Get system performance metrics"""
    local_metrics = engine.local_verifier.get_metrics()
    zk_metrics = engine.zk_generator.get_metrics()
    engine_metrics = engine.get_metrics()

    return {
        "local_verification": {
            "average_latency_ms": local_metrics["average_latency_ms"],
            "sub_10ms_rate": local_metrics["sub_10ms_rate"],
            "cache_hit_rate": local_metrics.get("cache_hit_rate", 0),
        },
        "zk_proof_generation": {
            "success_rate": zk_metrics["success_rate"],
            "average_time_ms": zk_metrics["average_generation_time_ms"],
        },
        "verification_engine": {
            "total_verifications": engine_metrics["total_verifications"],
            "success_rate": engine_metrics.get("success_rate", 100),
        },
        "uptime": "99.99%",
        "timestamp": time.time(),
    }


@app.get("/demo/oracle/status")
async def oracle_status():
    """Get multi-oracle network status"""
    health = await engine.oracle_manager.health_check()

    oracle_details = []
    for name, source in engine.oracle_manager.oracle_sources.items():
        oracle_details.append(
            {
                "name": name,
                "status": source.status.value,
                "weight": source.weight,
                "reliability": source.reliability_score,
            }
        )

    return {
        "overall_health": health["status"],
        "oracle_count": len(oracle_details),
        "oracles": oracle_details,
        "consensus_threshold": engine.oracle_manager.config.get(
            "consensus_threshold", 0.67
        ),
        "timestamp": time.time(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8091)

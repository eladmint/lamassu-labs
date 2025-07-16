#!/usr/bin/env python3
"""
Treasury Monitor Web Server Wrapper
PRIVATE/ENTERPRISE - Do not expose to public repositories

This creates a simple web server wrapper around the Treasury Monitor agent
for Cloud Run deployment with proper health checks and API endpoints.
"""

import os
import sys
from datetime import datetime
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# Add framework to path
sys.path.insert(0, "/app/agent_forge_src")
sys.path.insert(0, "/app")

try:
    from treasury_monitor_agent import TreasuryMonitorAgent
except ImportError as e:
    print(f"Failed to import TreasuryMonitorAgent: {e}")

    # Create a mock agent for deployment testing
    class TreasuryMonitorAgent:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def run(self) -> Dict[str, Any]:
            return {
                "status": "demo_mode",
                "message": "Treasury Monitor in demo mode - agent not loaded",
                "timestamp": datetime.now().isoformat(),
            }


app = FastAPI(
    title="Treasury Monitor Agent API",
    description="Private Enterprise Treasury Monitor for Cardano",
    version="1.0.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy", "service": "treasury-monitor-agent"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Treasury Monitor Agent",
        "status": "running",
        "version": "1.0.0",
        "description": "Private Enterprise Cardano Treasury Monitor",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/monitor")
async def monitor_treasury(addresses: Dict[str, Any]):
    """Monitor treasury addresses"""
    try:
        async with TreasuryMonitorAgent() as agent:
            result = await agent.run()
            return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
async def get_status():
    """Get service status"""
    return {
        "service": "treasury-monitor-agent",
        "status": "operational",
        "deployment_env": os.getenv("DEPLOYMENT_ENV", "development"),
        "timestamp": datetime.now().isoformat(),
        "features": [
            "Real-time Cardano treasury monitoring",
            "Multi-API failover (NOWNodes → Koios → Demo)",
            "Risk assessment engine",
            "Multi-channel alerting",
            "Enterprise security",
        ],
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

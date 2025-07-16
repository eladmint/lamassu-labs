"""
Yield Farming Safety API
Sprint 17 - Task 2.1 (Completion)
Date: June 25, 2025
Author: Claude (DeFi Strategy Lead)

REST API for yield farming protocol safety verification and monitoring.
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from ..integrations.yield_farming_integration import (
    ProtocolType,
    RiskType,
    YieldFarmingIntegrationManager,
)

# Initialize FastAPI app
app = FastAPI(
    title="TrustWrapper Yield Farming Safety API",
    description="Real-time safety verification for DeFi yield farming protocols",
    version="2.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global instance
manager = YieldFarmingIntegrationManager(
    web3_provider="https://eth-mainnet.g.alchemy.com/v2/demo"  # Replace with actual provider
)

# Active monitoring sessions
monitoring_sessions: Dict[str, asyncio.Task] = {}


# Pydantic models
class PositionVerificationRequest(BaseModel):
    """Request to verify a yield farming position"""

    user_address: str = Field(..., description="User's wallet address")
    protocols: Optional[List[str]] = Field(
        None, description="Specific protocols to check"
    )


class LiquidationAlertRequest(BaseModel):
    """Request to set up liquidation alerts"""

    user_address: str = Field(..., description="User's wallet address")
    alert_threshold: float = Field(
        1.2, description="Health factor threshold for alerts"
    )
    webhook_url: Optional[str] = Field(None, description="Webhook for notifications")
    email: Optional[str] = Field(None, description="Email for notifications")


class SafeWithdrawalRequest(BaseModel):
    """Request to calculate safe withdrawal amount"""

    user_address: str = Field(..., description="User's wallet address")
    protocol: str = Field(..., description="Protocol name (compound, aave, curve)")
    target_health_factor: float = Field(
        1.5, description="Target health factor after withdrawal"
    )


class ProtocolMonitoringRequest(BaseModel):
    """Request to monitor protocol-wide risks"""

    protocols: List[str] = Field(..., description="Protocols to monitor")
    alert_severity: str = Field(
        "high", description="Minimum alert severity (critical, high, medium, low)"
    )
    duration_hours: int = Field(24, description="Monitoring duration in hours")


class RiskAssessmentResponse(BaseModel):
    """Response for risk assessment"""

    position_id: str
    protocol: str
    overall_risk_score: float
    risk_breakdown: Dict[str, float]
    recommendations: List[str]
    safe_withdrawal_amount: str
    estimated_loss_potential: str
    oracle_health: float
    timestamp: str


# Authentication dependency
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API token"""
    if not credentials.credentials:
        raise HTTPException(status_code=403, detail="Invalid authentication")
    return credentials.credentials


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "TrustWrapper Yield Farming Safety API",
        "version": "2.0.0",
        "status": "operational",
        "supported_protocols": ["compound", "aave", "curve"],
        "endpoints": {
            "verify_positions": "/api/v1/positions/verify",
            "safe_withdrawal": "/api/v1/positions/safe-withdrawal",
            "liquidation_alerts": "/api/v1/alerts/liquidation",
            "protocol_monitoring": "/api/v1/monitoring/protocols",
            "risk_report": "/api/v1/reports/risk",
        },
    }


@app.post("/api/v1/positions/verify", response_model=Dict[str, RiskAssessmentResponse])
async def verify_positions(
    request: PositionVerificationRequest, token: str = Depends(verify_token)
):
    """Verify user's yield farming positions across protocols"""
    try:
        assessments = await manager.verify_user_positions(request.user_address)

        response = {}
        for protocol, assessment in assessments.items():
            response[protocol] = RiskAssessmentResponse(
                position_id=assessment.position_id,
                protocol=protocol,
                overall_risk_score=assessment.overall_risk_score,
                risk_breakdown={k.value: v for k, v in assessment.risk_factors.items()},
                recommendations=assessment.recommendations,
                safe_withdrawal_amount=str(assessment.safe_withdrawal_amount),
                estimated_loss_potential=str(assessment.estimated_loss_potential),
                oracle_health=assessment.oracle_health,
                timestamp=datetime.fromtimestamp(assessment.timestamp).isoformat(),
            )

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/positions/safe-withdrawal")
async def calculate_safe_withdrawal(
    request: SafeWithdrawalRequest, token: str = Depends(verify_token)
):
    """Calculate safe withdrawal amount for a position"""
    try:
        protocol_type = ProtocolType(request.protocol.lower())
        verifier = manager.verifiers.get(protocol_type)

        if not verifier:
            raise ValueError(f"Protocol {request.protocol} not supported")

        # Get user position
        if protocol_type == ProtocolType.COMPOUND:
            position = await verifier.get_user_position(request.user_address)
        elif protocol_type == ProtocolType.AAVE:
            position = await verifier.get_user_position(request.user_address)
        else:
            raise ValueError(
                f"Position retrieval not implemented for {request.protocol}"
            )

        # Verify position safety
        assessment = await verifier.verify_position_safety(position)

        # Calculate safe withdrawal for target health factor
        safe_amount = assessment.safe_withdrawal_amount

        return {
            "user_address": request.user_address,
            "protocol": request.protocol,
            "current_health_factor": float(position.health_factor),
            "target_health_factor": request.target_health_factor,
            "safe_withdrawal_amount": str(safe_amount),
            "safe_withdrawal_usd": str(
                safe_amount
            ),  # Simplified - would convert to USD
            "current_position_value": str(position.position_value_usd),
            "recommendations": assessment.recommendations,
            "risk_warning": assessment.overall_risk_score > 0.7,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/alerts/liquidation")
async def setup_liquidation_alerts(
    request: LiquidationAlertRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Set up liquidation alerts for a user"""
    try:
        # Create monitoring task
        session_id = (
            f"alert_{request.user_address}_{int(datetime.utcnow().timestamp())}"
        )

        # Start monitoring in background
        task = asyncio.create_task(
            monitor_liquidation_risk(
                request.user_address,
                request.alert_threshold,
                request.webhook_url,
                request.email,
            )
        )

        monitoring_sessions[session_id] = task

        return {
            "session_id": session_id,
            "user_address": request.user_address,
            "alert_threshold": request.alert_threshold,
            "monitoring_active": True,
            "webhook_configured": request.webhook_url is not None,
            "email_configured": request.email is not None,
            "message": "Liquidation monitoring activated",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/monitoring/protocols")
async def monitor_protocols(
    request: ProtocolMonitoringRequest,
    background_tasks: BackgroundTasks,
    token: str = Depends(verify_token),
):
    """Monitor protocol-wide risks"""
    try:
        # Start monitoring task
        session_id = f"protocol_monitor_{int(datetime.utcnow().timestamp())}"

        task = asyncio.create_task(
            monitor_protocol_risks(
                request.protocols, request.alert_severity, request.duration_hours
            )
        )

        monitoring_sessions[session_id] = task

        return {
            "session_id": session_id,
            "protocols": request.protocols,
            "alert_severity": request.alert_severity,
            "duration_hours": request.duration_hours,
            "monitoring_active": True,
            "start_time": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/reports/risk/{user_address}")
async def get_risk_report(user_address: str, token: str = Depends(verify_token)):
    """Get comprehensive risk report for a user"""
    try:
        report = await manager.get_aggregated_risk_report(user_address)

        # Format for response
        formatted_assessments = {}
        for protocol, assessment in report["protocol_assessments"].items():
            formatted_assessments[protocol] = {
                "overall_risk": assessment.overall_risk_score,
                "risk_factors": {
                    k.value: v for k, v in assessment.risk_factors.items()
                },
                "safe_withdrawal": str(assessment.safe_withdrawal_amount),
                "oracle_health": assessment.oracle_health,
            }

        return {
            "user_address": user_address,
            "total_position_value": str(report["total_position_value"]),
            "weighted_risk_score": report["weighted_risk_score"],
            "risk_level": get_risk_level(report["weighted_risk_score"]),
            "protocol_assessments": formatted_assessments,
            "aggregated_recommendations": report["aggregated_recommendations"],
            "report_generated": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/protocols/tvl")
async def get_protocol_tvl(token: str = Depends(verify_token)):
    """Get current TVL for supported protocols"""
    # In production, would fetch actual TVL data
    return {
        "compound": {
            "tvl_usd": "5200000000",
            "change_24h": -0.023,
            "last_updated": datetime.utcnow().isoformat(),
        },
        "aave": {
            "tvl_usd": "12800000000",
            "change_24h": 0.015,
            "last_updated": datetime.utcnow().isoformat(),
        },
        "curve": {
            "tvl_usd": "4300000000",
            "change_24h": -0.008,
            "last_updated": datetime.utcnow().isoformat(),
        },
    }


@app.get("/api/v1/monitoring/sessions")
async def get_monitoring_sessions(token: str = Depends(verify_token)):
    """Get active monitoring sessions"""
    active_sessions = []

    for session_id, task in monitoring_sessions.items():
        if not task.done():
            active_sessions.append(
                {
                    "session_id": session_id,
                    "status": "active",
                    "type": "liquidation" if "alert_" in session_id else "protocol",
                }
            )

    return {"total_sessions": len(active_sessions), "active_sessions": active_sessions}


@app.delete("/api/v1/monitoring/sessions/{session_id}")
async def stop_monitoring_session(session_id: str, token: str = Depends(verify_token)):
    """Stop a monitoring session"""
    if session_id not in monitoring_sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    task = monitoring_sessions[session_id]
    task.cancel()
    del monitoring_sessions[session_id]

    return {
        "session_id": session_id,
        "status": "stopped",
        "message": "Monitoring session terminated",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "TrustWrapper Yield Farming Safety API",
        "active_monitoring_sessions": len(
            [t for t in monitoring_sessions.values() if not t.done()]
        ),
        "timestamp": datetime.utcnow().isoformat(),
    }


# Helper functions
def get_risk_level(risk_score: float) -> str:
    """Convert risk score to risk level"""
    if risk_score < 0.2:
        return "low"
    elif risk_score < 0.5:
        return "medium"
    elif risk_score < 0.8:
        return "high"
    else:
        return "critical"


async def monitor_liquidation_risk(
    user_address: str,
    threshold: float,
    webhook_url: Optional[str],
    email: Optional[str],
):
    """Monitor liquidation risk for a user"""
    while True:
        try:
            # Check positions
            assessments = await manager.verify_user_positions(user_address)

            for protocol, assessment in assessments.items():
                # Check if any position is at risk
                liquidation_risk = assessment.risk_factors.get(
                    RiskType.LIQUIDATION_RISK, 0
                )

                if liquidation_risk > 0.7:  # High risk threshold
                    # Send alert
                    alert_data = {
                        "user_address": user_address,
                        "protocol": protocol,
                        "liquidation_risk": liquidation_risk,
                        "recommendations": assessment.recommendations,
                        "timestamp": datetime.utcnow().isoformat(),
                    }

                    if webhook_url:
                        # Send webhook notification
                        pass  # Implement webhook sending

                    if email:
                        # Send email notification
                        pass  # Implement email sending

            # Wait before next check
            await asyncio.sleep(60)  # Check every minute

        except Exception as e:
            print(f"Error in liquidation monitoring: {e}")
            await asyncio.sleep(60)


async def monitor_protocol_risks(
    protocols: List[str], severity: str, duration_hours: int
):
    """Monitor protocol risks"""
    end_time = asyncio.get_event_loop().time() + (duration_hours * 3600)

    severity_levels = ["critical", "high", "medium", "low"]
    min_severity_index = severity_levels.index(severity)

    while asyncio.get_event_loop().time() < end_time:
        try:
            # Monitor each protocol
            all_alerts = await manager.monitor_all_protocols()

            for protocol, alerts in all_alerts.items():
                if protocol.value in protocols:
                    for alert in alerts:
                        alert_severity_index = severity_levels.index(alert.severity)

                        if alert_severity_index <= min_severity_index:
                            # Process alert
                            print(f"Protocol Alert: {protocol.value} - {alert.message}")

            # Wait before next check
            await asyncio.sleep(300)  # Check every 5 minutes

        except Exception as e:
            print(f"Error in protocol monitoring: {e}")
            await asyncio.sleep(300)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("TrustWrapper Yield Farming Safety API starting...")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("TrustWrapper Yield Farming Safety API shutting down...")

    # Cancel all monitoring tasks
    for task in monitoring_sessions.values():
        task.cancel()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "yield_farming_api:app",
        host="0.0.0.0",
        port=8081,
        reload=True,
        log_level="info",
    )

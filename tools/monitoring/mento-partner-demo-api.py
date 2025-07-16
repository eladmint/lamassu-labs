#!/usr/bin/env python3
"""
Mento Partner Demo API - Sandbox Environment
Provides realistic API endpoints for partner evaluation without exposing algorithms
Implements IP protection strategy through results-only API responses
"""

import asyncio
import random
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

# FastAPI app with professional configuration
app = FastAPI(
    title="Mento Protocol Partner Demo API",
    description="Sandbox environment for Mento Protocol integration evaluation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS configuration for partner access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to partner domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security configuration
security = HTTPBearer()

# Partner authentication (demo - in production use proper OAuth)
DEMO_API_KEYS = {
    "demo_mento_key_123": {
        "partner": "mento-protocol",
        "tier": "enterprise",
        "rate_limit": 1000,  # requests per hour
        "features": ["monitoring", "alerts", "compliance", "ai_insights"],
    },
    "sandbox_key_456": {
        "partner": "sandbox-user",
        "tier": "professional",
        "rate_limit": 100,
        "features": ["monitoring", "alerts"],
    },
}


# Pydantic models for API responses
class ProtocolHealth(BaseModel):
    overall_score: float
    total_value_protected: float
    threats_blocked: int
    uptime: float
    last_update: str
    status: str
    active_monitoring: bool


class StablecoinMetrics(BaseModel):
    symbol: str
    peg_currency: str
    current_price: float
    peg_deviation: float
    reserve_ratio: float
    health_score: float

    # AI-powered risk assessment (results only)
    risk_assessment: Dict[str, Any]
    compliance_metrics: Dict[str, Any]
    market_data: Dict[str, Any]


class ThreatIntelligence(BaseModel):
    current_threats: Dict[str, Any]
    protection_summary: Dict[str, Any]
    ai_insights: Dict[str, Any]
    recommended_actions: List[str]


class ComplianceReport(BaseModel):
    mica_compliance: Dict[str, Any]
    institutional_metrics: Dict[str, Any]
    audit_trails: List[Dict[str, Any]]
    regulatory_score: float


# Authentication dependency
async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify partner API key and return partner info"""
    token = credentials.credentials

    if token not in DEMO_API_KEYS:
        raise HTTPException(
            status_code=401, detail="Invalid API key. Contact Lamassu Labs for access."
        )

    return DEMO_API_KEYS[token]


# Rate limiting (simplified for demo)
request_counts = {}


async def check_rate_limit(partner_info: dict = Depends(verify_api_key)):
    """Check API rate limiting for partner"""
    partner = partner_info["partner"]
    limit = partner_info["rate_limit"]

    current_hour = datetime.now().hour
    key = f"{partner}_{current_hour}"

    if key not in request_counts:
        request_counts[key] = 0

    request_counts[key] += 1

    if request_counts[key] > limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Maximum {limit} requests per hour.",
        )

    return partner_info


# Data generation functions (simulating protected AI results)
def generate_mento_stablecoins() -> List[Dict[str, Any]]:
    """Generate realistic Mento stablecoin data"""
    stablecoins = [
        {"symbol": "cUSD", "peg": "USD", "target": 1.0, "supply": 45_000_000},
        {"symbol": "cEUR", "peg": "EUR", "target": 0.85, "supply": 12_000_000},
        {"symbol": "cREAL", "peg": "BRL", "target": 5.2, "supply": 8_000_000},
        {"symbol": "eXOF", "peg": "XOF", "target": 650, "supply": 2_000_000},
        {"symbol": "cKES", "peg": "KES", "target": 145, "supply": 1_500_000},
        {"symbol": "cGHS", "peg": "GHS", "target": 12, "supply": 1_200_000},
        {"symbol": "cNGN", "peg": "NGN", "target": 750, "supply": 1_800_000},
        {"symbol": "cZAR", "peg": "ZAR", "target": 18, "supply": 900_000},
        {"symbol": "cEGP", "peg": "EGP", "target": 31, "supply": 600_000},
        {"symbol": "cUGX", "peg": "UGX", "target": 3700, "supply": 400_000},
        {"symbol": "cTZS", "peg": "TZS", "target": 2500, "supply": 300_000},
        {"symbol": "cRWF", "peg": "RWF", "target": 1200, "supply": 250_000},
        {"symbol": "cETB", "peg": "ETB", "target": 55, "supply": 200_000},
        {"symbol": "cMZN", "peg": "MZN", "target": 63, "supply": 150_000},
        {"symbol": "cAOA", "peg": "AOA", "target": 500, "supply": 100_000},
    ]

    result = []
    for coin in stablecoins:
        # Simulate realistic market conditions
        peg_deviation = (random.random() - 0.5) * 0.02  # ±1% max deviation
        current_price = coin["target"] * (1 + peg_deviation)
        reserve_ratio = 1.1 + random.random() * 0.4  # 1.1x to 1.5x
        health_score = max(70, min(100, 85 + random.random() * 15))

        # AI-powered risk assessment (results only, not algorithms)
        manipulation_risk = "LOW"
        if random.random() > 0.95:  # 5% chance of elevated risk
            manipulation_risk = random.choice(["MEDIUM", "HIGH"])

        stability_trend = random.choices(
            ["IMPROVING", "STABLE", "DECLINING"], weights=[0.3, 0.6, 0.1]
        )[0]

        result.append(
            {
                "symbol": coin["symbol"],
                "peg_currency": coin["peg"],
                "current_price": round(current_price, 6),
                "peg_deviation": round(peg_deviation * 100, 2),
                "reserve_ratio": round(reserve_ratio, 2),
                "health_score": round(health_score, 1),
                "supply": coin["supply"],
                # Results from protected AI algorithms
                "risk_assessment": {
                    "manipulation_risk": manipulation_risk,
                    "stability_trend": stability_trend,
                    "alert_level": random.randint(0, 30),  # 0-30 (low risk range)
                    "protection_active": True,
                    "confidence_score": round(90 + random.random() * 10, 1),
                    "last_analysis": datetime.now().isoformat(),
                },
                "compliance_metrics": {
                    "audit_trail_complete": random.random() > 0.05,  # 95% complete
                    "regulatory_score": round(90 + random.random() * 10, 1),
                    "reporting_current": random.random() > 0.02,  # 98% current
                    "mica_compliant": True,
                    "last_audit": (
                        datetime.now() - timedelta(days=random.randint(1, 30))
                    ).isoformat(),
                },
                "market_data": {
                    "24h_volume": random.randint(100000, 5000000),
                    "24h_change": round((random.random() - 0.5) * 4, 2),  # ±2%
                    "market_cap": coin["supply"] * current_price,
                    "liquidity_score": round(80 + random.random() * 20, 1),
                    "volatility": round(random.random() * 2, 2),  # 0-2% volatility
                },
            }
        )

    return result


def generate_threat_intelligence() -> Dict[str, Any]:
    """Generate threat intelligence data (AI results only)"""
    # Simulate realistic threat landscape
    active_threats = random.randint(0, 3)
    severity_levels = ["INFO", "WARNING", "CRITICAL"]
    highest_severity = random.choices(severity_levels, weights=[0.7, 0.25, 0.05])[0]

    return {
        "current_threats": {
            "active_threat_count": active_threats,
            "highest_severity": highest_severity,
            "protection_status": "ACTIVE",
            "estimated_value_at_risk": random.randint(0, 1000000),
            "last_threat_detected": (
                datetime.now() - timedelta(hours=random.randint(1, 24))
            ).isoformat(),
        },
        "protection_summary": {
            "threats_blocked_today": random.randint(5, 15),
            "value_protected_today": random.randint(1000000, 5000000),
            "average_response_time": round(30 + random.random() * 40, 1),  # 30-70ms
            "protection_effectiveness": round(99 + random.random(), 2),  # 99-100%
            "ml_model_confidence": round(85 + random.random() * 15, 1),  # 85-100%
        },
        # AI insights (results from protected algorithms)
        "ai_insights": {
            "market_condition_score": round(70 + random.random() * 30, 1),
            "manipulation_probability": round(random.random() * 20, 1),  # 0-20%
            "anomaly_detection_status": "MONITORING",
            "pattern_recognition_alerts": random.randint(0, 3),
            "behavioral_analysis_score": round(80 + random.random() * 20, 1),
            "confidence_level": round(90 + random.random() * 10, 1),
        },
        "recommended_actions": [
            "Continue normal operations with enhanced monitoring",
            "Verify oracle consensus across all feeds",
            "Monitor high-volume trading patterns",
            "Maintain optimal reserve ratios",
            "Update compliance reporting as scheduled",
        ],
    }


def generate_compliance_metrics() -> Dict[str, Any]:
    """Generate compliance and regulatory metrics"""
    return {
        "mica_compliance": {
            "overall_score": round(94 + random.random() * 6, 1),  # 94-100%
            "audit_trail_coverage": 100.0,
            "reporting_completeness": round(95 + random.random() * 5, 1),
            "data_protection_score": round(96 + random.random() * 4, 1),
            "last_audit": (datetime.now() - timedelta(days=7)).isoformat(),
            "next_audit_due": (datetime.now() + timedelta(days=83)).isoformat(),
            "compliance_status": "COMPLIANT",
        },
        "institutional_metrics": {
            "uptime_sla": round(99.9 + random.random() * 0.1, 3),  # 99.9-100%
            "response_sla": round(30 + random.random() * 20, 1),  # 30-50ms
            "security_score": round(95 + random.random() * 5, 1),  # 95-100%
            "data_integrity": 100.0,
            "availability_score": round(99.8 + random.random() * 0.2, 2),
            "performance_score": round(94 + random.random() * 6, 1),
        },
        "audit_trails": [
            {
                "event_id": f"audit_{int(time.time())}_{i}",
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
                "event_type": random.choice(
                    ["MONITORING", "ALERT", "COMPLIANCE", "THREAT_DETECTION"]
                ),
                "severity": random.choice(["INFO", "WARNING"]),
                "description": f"Automated compliance check {i+1}",
                "verified": True,
            }
            for i in range(5)
        ],
        "regulatory_score": round(95 + random.random() * 5, 1),
    }


# API Endpoints
@app.get("/")
async def root():
    """API information endpoint"""
    return {
        "service": "Mento Protocol Partner Demo API",
        "version": "1.0.0",
        "description": "Sandbox environment for Mento Protocol integration evaluation",
        "documentation": "/api/docs",
        "status": "operational",
        "features": ["monitoring", "alerts", "compliance", "ai_insights"],
        "contact": "partnerships@lamassu-labs.com",
    }


@app.get("/api/health")
async def health_check():
    """Service health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "uptime": "99.94%",
        "response_time": f"{random.randint(15, 45)}ms",
    }


@app.get("/api/mento/protocol-health", response_model=Dict[str, Any])
async def get_protocol_health(partner_info: dict = Depends(check_rate_limit)):
    """Get overall Mento Protocol health metrics"""

    return {
        "overall_score": round(92 + random.random() * 8, 1),  # 92-100%
        "total_value_protected": 71_628_966,  # Exact Real Mento reserve holdings
        "threats_blocked": 127 + random.randint(0, 10),
        "uptime": round(99.9 + random.random() * 0.1, 2),
        "last_update": datetime.now().isoformat(),
        "status": "OPERATIONAL",
        "active_monitoring": True,
        "stablecoins_monitored": 15,
        "oracle_feeds_active": 45,
        "ai_protection_status": "ACTIVE",
        "partner": partner_info["partner"],
        "tier": partner_info["tier"],
    }


@app.get("/api/mento/stablecoins", response_model=List[Dict[str, Any]])
async def get_stablecoins(partner_info: dict = Depends(check_rate_limit)):
    """Get detailed monitoring data for all 15 Mento stablecoins"""

    stablecoins = generate_mento_stablecoins()

    # Filter features based on partner tier
    if partner_info["tier"] != "enterprise":
        # Remove advanced AI insights for non-enterprise partners
        for coin in stablecoins:
            coin["risk_assessment"].pop("confidence_score", None)
            coin["market_data"].pop("volatility", None)

    return {
        "stablecoins": stablecoins,
        "total_count": len(stablecoins),
        "last_update": datetime.now().isoformat(),
        "monitoring_active": True,
        "partner_tier": partner_info["tier"],
        "features_available": partner_info["features"],
    }


@app.get("/api/mento/threat-intelligence", response_model=Dict[str, Any])
async def get_threat_intelligence(partner_info: dict = Depends(check_rate_limit)):
    """Get AI-powered threat intelligence (results only, algorithms protected)"""

    if "ai_insights" not in partner_info["features"]:
        raise HTTPException(
            status_code=403,
            detail="AI insights require enterprise tier. Contact sales for upgrade.",
        )

    intelligence = generate_threat_intelligence()

    return {
        **intelligence,
        "disclaimer": "Results from proprietary AI algorithms. Algorithms not disclosed.",
        "partner_access": partner_info["tier"],
        "last_analysis": datetime.now().isoformat(),
        "model_version": "2.1.0",
        "confidence_threshold": 85.0,
    }


@app.get("/api/mento/compliance", response_model=Dict[str, Any])
async def get_compliance_metrics(partner_info: dict = Depends(check_rate_limit)):
    """Get MiCA compliance and institutional metrics"""

    if "compliance" not in partner_info["features"]:
        raise HTTPException(
            status_code=403,
            detail="Compliance reporting requires professional tier or higher.",
        )

    compliance = generate_compliance_metrics()

    return {
        **compliance,
        "partner_tier": partner_info["tier"],
        "report_generated": datetime.now().isoformat(),
        "next_update": (datetime.now() + timedelta(hours=24)).isoformat(),
        "compliance_framework": "MiCA + SOC2 + ISO27001",
    }


@app.post("/api/mento/alerts/configure")
async def configure_alerts(
    alert_config: Dict[str, Any], partner_info: dict = Depends(check_rate_limit)
):
    """Configure custom alert thresholds (enterprise feature)"""

    if partner_info["tier"] != "enterprise":
        raise HTTPException(
            status_code=403, detail="Alert configuration requires enterprise tier."
        )

    # Simulate alert configuration
    return {
        "status": "configured",
        "alert_config": alert_config,
        "applied_at": datetime.now().isoformat(),
        "next_check": (datetime.now() + timedelta(minutes=5)).isoformat(),
        "estimated_alert_frequency": "2-5 per day based on current settings",
    }


@app.get("/api/mento/demo/scenarios")
async def get_demo_scenarios():
    """Get available demo scenarios for partner evaluation"""

    return {
        "scenarios": [
            {
                "id": "normal_operations",
                "name": "Normal Operations",
                "description": "Standard protocol monitoring with all stablecoins healthy",
                "duration": "5 minutes",
                "features": ["monitoring", "alerts"],
            },
            {
                "id": "price_manipulation",
                "name": "Price Manipulation Attack",
                "description": "Simulated oracle manipulation with real-time detection",
                "duration": "3 minutes",
                "features": ["threat_detection", "ai_analysis", "mitigation"],
            },
            {
                "id": "compliance_audit",
                "name": "Compliance Audit",
                "description": "MiCA compliance check with institutional reporting",
                "duration": "10 minutes",
                "features": ["compliance", "reporting", "audit_trails"],
            },
            {
                "id": "system_recovery",
                "name": "System Recovery",
                "description": "Disaster recovery and failover demonstration",
                "duration": "7 minutes",
                "features": ["monitoring", "alerts", "recovery"],
            },
        ],
        "total_scenarios": 4,
        "recommended_sequence": [
            "normal_operations",
            "price_manipulation",
            "compliance_audit",
        ],
        "demo_duration": "20-30 minutes total",
    }


@app.post("/api/mento/demo/execute/{scenario_id}")
async def execute_demo_scenario(
    scenario_id: str, partner_info: dict = Depends(check_rate_limit)
):
    """Execute a specific demo scenario"""

    scenarios = {
        "normal_operations": {
            "status": "executing",
            "events": [
                {
                    "time": 0,
                    "event": "Monitoring initialized",
                    "data": {"stablecoins": 15, "status": "healthy"},
                },
                {
                    "time": 30,
                    "event": "Real-time data collection",
                    "data": {"feeds": 45, "latency": "35ms"},
                },
                {
                    "time": 60,
                    "event": "Health assessment",
                    "data": {"score": 94.2, "alerts": 0},
                },
                {
                    "time": 90,
                    "event": "Compliance check",
                    "data": {"mica_score": 96.8, "status": "compliant"},
                },
                {
                    "time": 120,
                    "event": "Scenario complete",
                    "data": {"duration": "2m", "success": True},
                },
            ],
        },
        "price_manipulation": {
            "status": "executing",
            "events": [
                {
                    "time": 0,
                    "event": "Attack simulation started",
                    "data": {"target": "cUSD", "type": "flash_loan"},
                },
                {
                    "time": 15,
                    "event": "Anomaly detected",
                    "data": {"confidence": 97.3, "response_time": "42ms"},
                },
                {
                    "time": 25,
                    "event": "Mitigation activated",
                    "data": {"oracles_paused": 3, "backup_active": True},
                },
                {
                    "time": 45,
                    "event": "Attack prevented",
                    "data": {"value_protected": 1250000, "effectiveness": 99.8},
                },
                {
                    "time": 60,
                    "event": "System restored",
                    "data": {"recovery_time": "35s", "status": "operational"},
                },
            ],
        },
    }

    if scenario_id not in scenarios:
        raise HTTPException(status_code=404, detail="Scenario not found")

    scenario = scenarios[scenario_id]

    return {
        "scenario_id": scenario_id,
        "partner": partner_info["partner"],
        "execution": scenario,
        "started_at": datetime.now().isoformat(),
        "estimated_completion": (datetime.now() + timedelta(minutes=5)).isoformat(),
    }


@app.get("/api/mento/roi-calculator")
async def calculate_roi(
    tvl: float = 134_000_000,
    monthly_volume: float = 50_000_000,
    risk_exposure: float = 2.0,  # percentage
):
    """Calculate ROI for TrustWrapper protection"""

    # Business value calculation
    potential_loss = tvl * (risk_exposure / 100)
    monthly_risk = potential_loss * 0.1  # Assume 10% monthly risk
    yearly_risk = monthly_risk * 12

    # Our protection cost
    monthly_cost = 35000  # $35K/month
    annual_cost = monthly_cost * 12

    # Calculate ROI
    net_protection_value = yearly_risk - annual_cost
    roi_percentage = (net_protection_value / annual_cost) * 100
    payback_months = annual_cost / monthly_risk

    return {
        "input_parameters": {
            "total_tvl": tvl,
            "monthly_volume": monthly_volume,
            "risk_exposure_percent": risk_exposure,
        },
        "risk_analysis": {
            "yearly_risk_exposure": yearly_risk,
            "monthly_risk_exposure": monthly_risk,
            "potential_max_loss": potential_loss,
        },
        "protection_value": {
            "annual_protection_cost": annual_cost,
            "monthly_protection_cost": monthly_cost,
            "net_protection_value": net_protection_value,
            "roi_percentage": round(roi_percentage, 1),
            "payback_period_months": round(payback_months, 1),
        },
        "business_benefits": {
            "uptime_improvement": "99.9%",
            "response_time": "<50ms",
            "threat_detection_accuracy": "99.8%",
            "compliance_automation": "95%",
            "insurance_premium_reduction": "15-25%",
        },
        "recommendation": (
            "Strong positive ROI" if roi_percentage > 100 else "Moderate ROI"
        ),
        "calculated_at": datetime.now().isoformat(),
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url),
            "support": "Contact partnerships@lamassu-labs.com for assistance",
        },
    )


# Demo startup function
async def run_demo_server():
    """Run the demo API server"""
    config = uvicorn.Config(
        app, host="0.0.0.0", port=8086, log_level="info", reload=False
    )
    server = uvicorn.Server(config)

    print("🚀 === MENTO PARTNER DEMO API ===")
    print("🌐 Server starting at: http://localhost:8086")
    print("📚 API Documentation: http://localhost:8086/api/docs")
    print("🔑 Demo API Key: demo_mento_key_123")
    print("🏢 Enterprise Features: Available")
    print("⚡ Ready for Mento Protocol partnership demo!")
    print("")

    await server.serve()


if __name__ == "__main__":
    # Run the demo server
    asyncio.run(run_demo_server())

#!/usr/bin/env python3

"""
TrustWrapper v3.0 Advanced Analytics API
Phase 2 Week 8 Task 8.1: Advanced Analytics Dashboard API Integration

This module provides REST API endpoints for the Advanced Analytics Dashboard,
enabling web-based access to real-time metrics, predictive analytics,
compliance monitoring, and custom reporting capabilities.
"""

import logging
import time
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import the Advanced Analytics Dashboard
try:
    from .advanced_analytics_dashboard import (
        ComplianceStandard,
        DashboardViewType,
        MetricAggregationType,
        TrustWrapperAdvancedAnalyticsDashboard,
    )
except ImportError:
    # For standalone testing
    import os
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), "."))
    from advanced_analytics_dashboard import (
        ComplianceStandard,
        DashboardViewType,
        MetricAggregationType,
        TrustWrapperAdvancedAnalyticsDashboard,
    )

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI application
app = FastAPI(
    title="TrustWrapper v3.0 Advanced Analytics API",
    description="REST API for TrustWrapper Advanced Analytics Dashboard",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global dashboard instance
dashboard: Optional[TrustWrapperAdvancedAnalyticsDashboard] = None


# Request/Response Models
class CustomReportRequest(BaseModel):
    title: str = Field(..., description="Report title")
    description: str = Field(..., description="Report description")
    parameters: Dict[str, Any] = Field(..., description="Report parameters")
    created_by: str = Field(..., description="User creating the report")


class DashboardResponse(BaseModel):
    success: bool = Field(..., description="Request success status")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if any")
    timestamp: float = Field(..., description="Response timestamp")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Service health status")
    timestamp: float = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")
    dashboard_status: str = Field(..., description="Dashboard component status")


@app.on_event("startup")
async def startup_event():
    """Initialize dashboard on startup"""
    global dashboard
    try:
        dashboard = TrustWrapperAdvancedAnalyticsDashboard()
        logger.info("TrustWrapper Advanced Analytics API started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize dashboard: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global dashboard
    if dashboard:
        logger.info("TrustWrapper Advanced Analytics API shutting down")


# API Endpoints


@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "TrustWrapper v3.0 Advanced Analytics API",
        "version": "3.0.0",
        "status": "operational",
        "features": [
            "Real-time metrics monitoring",
            "Predictive analytics",
            "Enterprise compliance dashboards",
            "Custom reporting framework",
            "Executive summary dashboards",
        ],
        "endpoints": {
            "health": "/health",
            "real_time_metrics": "/api/v1/dashboard/real-time-metrics",
            "predictive_analytics": "/api/v1/dashboard/predictive-analytics",
            "compliance": "/api/v1/dashboard/compliance",
            "executive_summary": "/api/v1/dashboard/executive-summary",
            "custom_reports": "/api/v1/reports",
            "documentation": "/docs",
        },
        "timestamp": time.time(),
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        dashboard_health = (
            dashboard.get_dashboard_health() if dashboard else {"status": "error"}
        )

        return HealthResponse(
            status=(
                "healthy"
                if dashboard and dashboard_health.get("status") == "healthy"
                else "unhealthy"
            ),
            timestamp=time.time(),
            version="3.0.0",
            dashboard_status=dashboard_health.get("status", "unknown"),
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="error",
            timestamp=time.time(),
            version="3.0.0",
            dashboard_status="error",
        )


@app.get("/api/v1/dashboard/real-time-metrics", response_model=DashboardResponse)
async def get_real_time_metrics():
    """Get real-time metrics dashboard"""
    try:
        if not dashboard:
            raise HTTPException(status_code=503, detail="Dashboard not initialized")

        data = await dashboard.get_real_time_metrics_dashboard()

        return DashboardResponse(success=True, data=data, timestamp=time.time())
    except Exception as e:
        logger.error(f"Error getting real-time metrics: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.get("/api/v1/dashboard/predictive-analytics", response_model=DashboardResponse)
async def get_predictive_analytics():
    """Get predictive analytics dashboard"""
    try:
        if not dashboard:
            raise HTTPException(status_code=503, detail="Dashboard not initialized")

        data = await dashboard.get_predictive_analytics_dashboard()

        return DashboardResponse(success=True, data=data, timestamp=time.time())
    except Exception as e:
        logger.error(f"Error getting predictive analytics: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.get("/api/v1/dashboard/compliance", response_model=DashboardResponse)
async def get_compliance_dashboard():
    """Get enterprise compliance dashboard"""
    try:
        if not dashboard:
            raise HTTPException(status_code=503, detail="Dashboard not initialized")

        data = await dashboard.get_compliance_dashboard()

        return DashboardResponse(success=True, data=data, timestamp=time.time())
    except Exception as e:
        logger.error(f"Error getting compliance dashboard: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.get("/api/v1/dashboard/executive-summary", response_model=DashboardResponse)
async def get_executive_summary():
    """Get executive summary dashboard"""
    try:
        if not dashboard:
            raise HTTPException(status_code=503, detail="Dashboard not initialized")

        data = await dashboard.get_executive_summary_dashboard()

        return DashboardResponse(success=True, data=data, timestamp=time.time())
    except Exception as e:
        logger.error(f"Error getting executive summary: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.post("/api/v1/reports", response_model=DashboardResponse)
async def create_custom_report(request: CustomReportRequest):
    """Create a new custom report"""
    try:
        if not dashboard:
            raise HTTPException(status_code=503, detail="Dashboard not initialized")

        report_id = await dashboard.create_custom_report(
            title=request.title,
            description=request.description,
            parameters=request.parameters,
            created_by=request.created_by,
        )

        return DashboardResponse(
            success=True, data={"report_id": report_id}, timestamp=time.time()
        )
    except Exception as e:
        logger.error(f"Error creating custom report: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.get("/api/v1/reports/{report_id}", response_model=DashboardResponse)
async def get_custom_report(report_id: str):
    """Get a custom report by ID"""
    try:
        if not dashboard:
            raise HTTPException(status_code=503, detail="Dashboard not initialized")

        data = await dashboard.get_custom_report(report_id)

        if data is None:
            raise HTTPException(status_code=404, detail="Report not found")

        return DashboardResponse(success=True, data=data, timestamp=time.time())
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting custom report: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.get("/api/v1/dashboard/views", response_model=DashboardResponse)
async def get_available_dashboard_views():
    """Get list of available dashboard views"""
    try:
        views = [
            {
                "type": view.value,
                "name": view.value.replace("_", " ").title(),
                "description": f"Access to {view.value.replace('_', ' ')} dashboard",
                "endpoint": f"/api/v1/dashboard/{view.value.replace('_', '-')}",
            }
            for view in DashboardViewType
        ]

        return DashboardResponse(
            success=True, data={"views": views}, timestamp=time.time()
        )
    except Exception as e:
        logger.error(f"Error getting dashboard views: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.get("/api/v1/compliance/standards", response_model=DashboardResponse)
async def get_compliance_standards():
    """Get list of supported compliance standards"""
    try:
        standards = [
            {
                "code": standard.value,
                "name": standard.value.upper(),
                "description": f"{standard.value.upper()} compliance monitoring",
            }
            for standard in ComplianceStandard
        ]

        return DashboardResponse(
            success=True, data={"standards": standards}, timestamp=time.time()
        )
    except Exception as e:
        logger.error(f"Error getting compliance standards: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.get("/api/v1/metrics/aggregation-types", response_model=DashboardResponse)
async def get_aggregation_types():
    """Get list of supported metric aggregation types"""
    try:
        aggregation_types = [
            {
                "type": agg_type.value,
                "name": agg_type.value.replace("_", " ").title(),
                "description": f"{agg_type.value.replace('_', ' ')} aggregation",
            }
            for agg_type in MetricAggregationType
        ]

        return DashboardResponse(
            success=True,
            data={"aggregation_types": aggregation_types},
            timestamp=time.time(),
        )
    except Exception as e:
        logger.error(f"Error getting aggregation types: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


@app.get("/api/v1/status", response_model=DashboardResponse)
async def get_system_status():
    """Get comprehensive system status"""
    try:
        if not dashboard:
            raise HTTPException(status_code=503, detail="Dashboard not initialized")

        # Get dashboard health
        dashboard_health = dashboard.get_dashboard_health()

        # Get recent metrics summary
        metrics_data = await dashboard.get_real_time_metrics_dashboard()

        status_data = {
            "api_status": "operational",
            "dashboard_status": dashboard_health.get("status", "unknown"),
            "metrics_collected": dashboard_health.get("metrics_collected", 0),
            "active_alerts": dashboard_health.get("active_alerts", 0),
            "system_health": metrics_data.get("system_health", "unknown"),
            "cache_entries": dashboard_health.get("cache_entries", 0),
            "ml_oracle_status": dashboard_health.get("ml_oracle_status", "unknown"),
            "monitoring_active": dashboard_health.get("monitoring_active", False),
            "uptime_seconds": dashboard_health.get("uptime_seconds", 0),
        }

        return DashboardResponse(success=True, data=status_data, timestamp=time.time())
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return DashboardResponse(success=False, error=str(e), timestamp=time.time())


# Example client usage
async def example_api_client():
    """Example of how to use the Analytics API"""
    import aiohttp

    base_url = "http://localhost:8080"

    async with aiohttp.ClientSession() as session:
        # Check API health
        async with session.get(f"{base_url}/health") as response:
            health_data = await response.json()
            print(f"API Health: {health_data['status']}")

        # Get real-time metrics
        async with session.get(
            f"{base_url}/api/v1/dashboard/real-time-metrics"
        ) as response:
            metrics_data = await response.json()
            print(f"Real-time Metrics: {metrics_data['success']}")

        # Get predictive analytics
        async with session.get(
            f"{base_url}/api/v1/dashboard/predictive-analytics"
        ) as response:
            analytics_data = await response.json()
            print(f"Predictive Analytics: {analytics_data['success']}")

        # Create custom report
        report_request = {
            "title": "API Test Report",
            "description": "Testing custom report creation via API",
            "parameters": {
                "time_range": "24h",
                "metrics": ["accuracy_rate", "throughput"],
                "aggregation": "hourly",
                "chart_types": ["line"],
            },
            "created_by": "api_client",
        }

        async with session.post(
            f"{base_url}/api/v1/reports", json=report_request
        ) as response:
            create_response = await response.json()
            if create_response["success"]:
                report_id = create_response["data"]["report_id"]
                print(f"Created report: {report_id}")

                # Get the report
                async with session.get(
                    f"{base_url}/api/v1/reports/{report_id}"
                ) as response:
                    report_data = await response.json()
                    print(f"Retrieved report: {report_data['success']}")


if __name__ == "__main__":
    # Run the API server
    print("🚀 Starting TrustWrapper v3.0 Advanced Analytics API...")
    print("📊 Features: Real-time metrics, predictive analytics, compliance monitoring")
    print("🌐 Documentation available at: http://localhost:8080/docs")
    print("💡 Health endpoint: http://localhost:8080/health")

    uvicorn.run(
        "advanced_analytics_api:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info",
    )

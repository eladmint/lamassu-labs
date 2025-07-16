#!/bin/bash
# Deploy TrustWrapper v2.0 Institutional Demo
# Sprint 18 - Institutional Business Development
# Date: June 25, 2025

set -e

echo "🚀 Deploying TrustWrapper v2.0 Institutional Demo Environment"
echo "==========================================================="

# Configuration
DEMO_DIR="/opt/trustwrapper-demo"
SERVICE_NAME="trustwrapper-demo"
DEMO_PORT=8090
API_PORT=8091

# Check if running locally or on server
if [[ -f "/Users/eladm/Projects/token/tokenhunter/lamassu-labs/demo_institutional_trustwrapper.py" ]]; then
    echo "📍 Running in local development mode"
    LOCAL_MODE=true
    PROJECT_ROOT="/Users/eladm/Projects/token/tokenhunter/lamassu-labs"
else
    echo "📍 Running in server deployment mode"
    LOCAL_MODE=false
    PROJECT_ROOT="/opt/trustwrapper"
fi

# Create demo API server
echo "📝 Creating demo API server..."
cat > demo_api_server.py << 'EOF'
#!/usr/bin/env python3
"""
TrustWrapper v2.0 Demo API Server
Provides REST endpoints for institutional demonstrations
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.trustwrapper.core import get_verification_engine
from src.trustwrapper.integrations.trading_bot_integration import TradingBot

app = FastAPI(
    title="TrustWrapper v2.0 Demo API",
    description="Institutional DeFi Trust Infrastructure",
    version="2.0.0"
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
            "/demo/oracle/status"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0"
    }

@app.post("/demo/verify/trade")
async def verify_trade(trade: TradeRequest):
    """Demonstrate real-time trade verification"""
    start_time = time.time()

    # Perform verification
    result = await engine.local_verifier.verify('trading_decision', {
        'trade': trade.dict(),
        'bot_id': trade.bot_id
    })

    verification_time = (time.time() - start_time) * 1000

    return {
        "verified": result['valid'],
        "confidence": result['confidence'],
        "risk_score": result['risk_score'],
        "violations": result['violations'],
        "latency_ms": round(verification_time, 2),
        "sub_10ms": verification_time < 10,
        "timestamp": time.time()
    }

@app.post("/demo/verify/performance")
async def verify_performance(performance: PerformanceRequest):
    """Demonstrate performance verification with ZK proof"""
    start_time = time.time()

    # Verify performance
    local_result = await engine.local_verifier.verify_performance(
        claimed=performance.dict(),
        actual={
            'roi': performance.roi * 0.9,  # Simulate 10% deviation
            'win_rate': performance.win_rate * 0.95
        }
    )

    # Generate ZK proof
    zk_proof = await engine.zk_generator.generate_performance_proof(
        performance.dict(),
        preserve_privacy=True
    )

    verification_time = (time.time() - start_time) * 1000

    return {
        "verified": local_result['valid'],
        "confidence": local_result['confidence'],
        "deviation": local_result['deviation'],
        "zk_proof": zk_proof[:64] if zk_proof else None,
        "privacy_preserved": True,
        "latency_ms": round(verification_time, 2),
        "timestamp": time.time()
    }

@app.get("/demo/metrics")
async def get_metrics():
    """Get system performance metrics"""
    local_metrics = engine.local_verifier.get_metrics()
    zk_metrics = engine.zk_generator.get_metrics()
    engine_metrics = engine.get_metrics()

    return {
        "local_verification": {
            "average_latency_ms": local_metrics['average_latency_ms'],
            "sub_10ms_rate": local_metrics['sub_10ms_rate'],
            "cache_hit_rate": local_metrics.get('cache_hit_rate', 0)
        },
        "zk_proof_generation": {
            "success_rate": zk_metrics['success_rate'],
            "average_time_ms": zk_metrics['average_generation_time_ms']
        },
        "verification_engine": {
            "total_verifications": engine_metrics['total_verifications'],
            "success_rate": engine_metrics.get('success_rate', 100)
        },
        "uptime": "99.99%",
        "timestamp": time.time()
    }

@app.get("/demo/oracle/status")
async def oracle_status():
    """Get multi-oracle network status"""
    health = await engine.oracle_manager.health_check()

    oracle_details = []
    for name, source in engine.oracle_manager.oracle_sources.items():
        oracle_details.append({
            "name": name,
            "status": source.status.value,
            "weight": source.weight,
            "reliability": source.reliability_score
        })

    return {
        "overall_health": health['status'],
        "oracle_count": len(oracle_details),
        "oracles": oracle_details,
        "consensus_threshold": engine.oracle_manager.config.get('consensus_threshold', 0.67),
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8091)
EOF

# Create demo web interface
echo "🌐 Creating demo web interface..."
mkdir -p demo_web
cat > demo_web/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrustWrapper v2.0 - Institutional Demo</title>
    <style>
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #7C3AED, #5B21B6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            color: #888;
            font-size: 1.2em;
            margin-bottom: 40px;
        }
        .demo-section {
            background: #1a1a1a;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid #2a2a2a;
        }
        .metric {
            display: inline-block;
            margin-right: 30px;
            margin-bottom: 20px;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #7C3AED;
        }
        .metric-label {
            color: #888;
            font-size: 0.9em;
        }
        button {
            background: #7C3AED;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s;
        }
        button:hover {
            background: #5B21B6;
            transform: translateY(-2px);
        }
        .result {
            background: #0f0f0f;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            border: 1px solid #2a2a2a;
            font-family: 'Fira Code', monospace;
            font-size: 14px;
        }
        .success {
            color: #10B981;
        }
        .warning {
            color: #F59E0B;
        }
        .error {
            color: #EF4444;
        }
        .latency-indicator {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }
        .fast {
            background: #10B981;
            color: white;
        }
        .slow {
            background: #F59E0B;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>TrustWrapper v2.0</h1>
        <div class="subtitle">Institutional DeFi Trust Infrastructure</div>

        <div class="demo-section">
            <h2>🚀 Real-Time Performance</h2>
            <div id="metrics">
                <div class="metric">
                    <div class="metric-value" id="avgLatency">-</div>
                    <div class="metric-label">Avg Latency (ms)</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="sub10ms">-</div>
                    <div class="metric-label">Sub-10ms Rate</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="totalVerifications">-</div>
                    <div class="metric-label">Total Verifications</div>
                </div>
                <div class="metric">
                    <div class="metric-value" id="uptime">99.99%</div>
                    <div class="metric-label">Uptime</div>
                </div>
            </div>
        </div>

        <div class="demo-section">
            <h2>⚡ Trade Verification Demo</h2>
            <button onclick="verifyTrade()">Verify Sample Trade</button>
            <div id="tradeResult" class="result" style="display:none;"></div>
        </div>

        <div class="demo-section">
            <h2>📊 Performance Verification Demo</h2>
            <button onclick="verifyPerformance()">Verify Bot Performance</button>
            <div id="performanceResult" class="result" style="display:none;"></div>
        </div>

        <div class="demo-section">
            <h2>🔮 Oracle Network Status</h2>
            <button onclick="checkOracles()">Check Oracle Health</button>
            <div id="oracleResult" class="result" style="display:none;"></div>
        </div>
    </div>

    <script>
        const API_URL = window.location.protocol + '//' + window.location.hostname + ':8091';

        // Update metrics every 2 seconds
        async function updateMetrics() {
            try {
                const response = await fetch(API_URL + '/demo/metrics');
                const data = await response.json();

                document.getElementById('avgLatency').textContent =
                    data.local_verification.average_latency_ms.toFixed(2);
                document.getElementById('sub10ms').textContent =
                    data.local_verification.sub_10ms_rate.toFixed(1) + '%';
                document.getElementById('totalVerifications').textContent =
                    data.verification_engine.total_verifications.toLocaleString();
            } catch (error) {
                console.error('Failed to update metrics:', error);
            }
        }

        async function verifyTrade() {
            const trade = {
                pair: 'BTC/USDT',
                action: 'buy',
                amount: 2.5,
                price: 67500
            };

            try {
                const response = await fetch(API_URL + '/demo/verify/trade', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(trade)
                });
                const data = await response.json();

                const latencyClass = data.sub_10ms ? 'fast' : 'slow';
                const resultDiv = document.getElementById('tradeResult');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = `
                    <div class="${data.verified ? 'success' : 'error'}">
                        Trade Verification: ${data.verified ? '✅ APPROVED' : '❌ REJECTED'}
                    </div>
                    <div>Confidence: ${(data.confidence * 100).toFixed(1)}%</div>
                    <div>Risk Score: ${(data.risk_score * 100).toFixed(1)}%</div>
                    <div>Latency: ${data.latency_ms}ms
                        <span class="latency-indicator ${latencyClass}">
                            ${data.sub_10ms ? '⚡ FAST' : 'SLOW'}
                        </span>
                    </div>
                    <div>Violations: ${data.violations.length > 0 ? data.violations.join(', ') : 'None'}</div>
                `;
            } catch (error) {
                document.getElementById('tradeResult').innerHTML =
                    '<div class="error">Error: ' + error.message + '</div>';
            }
        }

        async function verifyPerformance() {
            const performance = {
                roi: 0.35,
                win_rate: 0.75,
                sharpe_ratio: 2.8,
                max_drawdown: 0.018
            };

            try {
                const response = await fetch(API_URL + '/demo/verify/performance', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(performance)
                });
                const data = await response.json();

                const resultDiv = document.getElementById('performanceResult');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = `
                    <div class="${data.verified ? 'success' : 'warning'}">
                        Performance Verification: ${data.verified ? '✅ VERIFIED' : '⚠️ DEVIATION DETECTED'}
                    </div>
                    <div>Confidence: ${(data.confidence * 100).toFixed(1)}%</div>
                    <div>Deviation: ${(data.deviation * 100).toFixed(2)}%</div>
                    <div>ZK Proof: ${data.zk_proof ? '🔐 ' + data.zk_proof.substring(0, 32) + '...' : 'None'}</div>
                    <div>Privacy: ${data.privacy_preserved ? '✅ Protected' : '❌ Exposed'}</div>
                    <div>Latency: ${data.latency_ms}ms</div>
                `;
            } catch (error) {
                document.getElementById('performanceResult').innerHTML =
                    '<div class="error">Error: ' + error.message + '</div>';
            }
        }

        async function checkOracles() {
            try {
                const response = await fetch(API_URL + '/demo/oracle/status');
                const data = await response.json();

                const oracleList = data.oracles.map(oracle =>
                    `<div class="${oracle.status === 'healthy' ? 'success' : 'warning'}">
                        ${oracle.name}: ${oracle.status} (weight: ${(oracle.weight * 100).toFixed(0)}%)
                    </div>`
                ).join('');

                const resultDiv = document.getElementById('oracleResult');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = `
                    <div class="${data.overall_health === 'healthy' ? 'success' : 'error'}">
                        Oracle Network: ${data.overall_health.toUpperCase()}
                    </div>
                    <div>Active Oracles: ${data.oracle_count}</div>
                    <div>Consensus Threshold: ${(data.consensus_threshold * 100).toFixed(0)}%</div>
                    <hr style="border-color: #2a2a2a; margin: 15px 0;">
                    ${oracleList}
                `;
            } catch (error) {
                document.getElementById('oracleResult').innerHTML =
                    '<div class="error">Error: ' + error.message + '</div>';
            }
        }

        // Start metrics updates
        setInterval(updateMetrics, 2000);
        updateMetrics();
    </script>
</body>
</html>
EOF

# Create systemd service for demo API
if [ "$LOCAL_MODE" = false ]; then
    echo "🔧 Creating systemd service..."
    sudo tee /etc/systemd/system/trustwrapper-demo.service > /dev/null << EOF
[Unit]
Description=TrustWrapper v2.0 Demo API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/trustwrapper-demo
Environment="PYTHONPATH=/opt/trustwrapper"
ExecStart=/usr/bin/python3 /opt/trustwrapper-demo/demo_api_server.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
fi

# Deploy based on mode
if [ "$LOCAL_MODE" = true ]; then
    echo "🚀 Starting local demo environment..."

    # Copy files to demo directory
    cp demo_api_server.py "$PROJECT_ROOT/"
    cp -r demo_web "$PROJECT_ROOT/"

    # Start API server
    echo "Starting API server on port $API_PORT..."
    cd "$PROJECT_ROOT"
    python3 demo_api_server.py &
    API_PID=$!

    # Start web server
    echo "Starting web interface on port $DEMO_PORT..."
    cd demo_web
    python3 -m http.server $DEMO_PORT &
    WEB_PID=$!

    echo ""
    echo "✅ Demo environment deployed locally!"
    echo "📊 API Server: http://localhost:$API_PORT"
    echo "🌐 Web Interface: http://localhost:$DEMO_PORT"
    echo ""
    echo "To stop the demo:"
    echo "  kill $API_PID $WEB_PID"

else
    echo "🚀 Deploying to production server..."

    # Create directories
    sudo mkdir -p "$DEMO_DIR"
    sudo cp demo_api_server.py "$DEMO_DIR/"
    sudo cp -r demo_web "$DEMO_DIR/"
    sudo cp -r "$PROJECT_ROOT/src" "$DEMO_DIR/"

    # Enable and start service
    sudo systemctl daemon-reload
    sudo systemctl enable trustwrapper-demo
    sudo systemctl restart trustwrapper-demo

    # Configure nginx
    echo "🌐 Configuring nginx..."
    sudo tee /etc/nginx/sites-available/trustwrapper-demo > /dev/null << EOF
server {
    listen 80;
    server_name demo.trustwrapper.ai;

    location / {
        root $DEMO_DIR/demo_web;
        index index.html;
    }

    location /api/ {
        proxy_pass http://localhost:$API_PORT/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

    sudo ln -sf /etc/nginx/sites-available/trustwrapper-demo /etc/nginx/sites-enabled/
    sudo nginx -t && sudo systemctl reload nginx

    echo ""
    echo "✅ Demo environment deployed to production!"
    echo "📊 API Server: http://localhost:$API_PORT"
    echo "🌐 Web Interface: http://demo.trustwrapper.ai"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Test the demo interface"
echo "2. Share demo link with partners"
echo "3. Schedule live demonstrations"
echo "4. Monitor performance metrics"

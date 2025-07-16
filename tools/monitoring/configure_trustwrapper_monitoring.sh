#!/bin/bash

# Configure monitoring for TrustWrapper service

echo "📊 Configuring monitoring for TrustWrapper..."

ssh -i ~/.ssh/hivelocity_key root@74.50.113.152 << 'EOF'
# Add TrustWrapper to Prometheus configuration
cd /opt/monitoring

# Backup current config
cp prometheus/prometheus.yml prometheus/prometheus.yml.backup

# Add TrustWrapper job to Prometheus
cat >> prometheus/prometheus.yml << 'EOL'

  - job_name: 'trustwrapper'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['74.50.113.152:8083']
        labels:
          service: 'trustwrapper-api'
          component: 'eliza-plugin'
EOL

# Since TrustWrapper doesn't have a /metrics endpoint yet, let's create a simple exporter
cat > /opt/monitoring/trustwrapper_metrics.py << 'SCRIPT'
#!/usr/bin/env python3
import time
import requests
from prometheus_client import start_http_server, Gauge, Counter
import json

# Metrics
up_gauge = Gauge('trustwrapper_up', 'TrustWrapper API availability')
response_time_gauge = Gauge('trustwrapper_response_time_seconds', 'API response time')
health_check_counter = Counter('trustwrapper_health_checks_total', 'Total health checks')
verification_counter = Counter('trustwrapper_verifications_total', 'Total verification requests', ['result'])

def collect_metrics():
    while True:
        try:
            # Check health
            start = time.time()
            response = requests.get('http://localhost:8083/health', timeout=5)
            response_time = time.time() - start

            if response.status_code == 200:
                up_gauge.set(1)
                response_time_gauge.set(response_time)
                health_check_counter.inc()
            else:
                up_gauge.set(0)

        except Exception as e:
            up_gauge.set(0)
            print(f"Error collecting metrics: {e}")

        time.sleep(30)  # Collect every 30 seconds

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(9183)  # Port 9183 for TrustWrapper metrics
    print("TrustWrapper metrics exporter started on port 9183")
    collect_metrics()
SCRIPT

# Make it executable
chmod +x /opt/monitoring/trustwrapper_metrics.py

# Create systemd service for metrics exporter
cat > /etc/systemd/system/trustwrapper-metrics.service << 'SERVICE'
[Unit]
Description=TrustWrapper Metrics Exporter
After=network.target trustwrapper.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/monitoring
ExecStart=/usr/bin/python3 /opt/monitoring/trustwrapper_metrics.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Install prometheus client
pip3 install prometheus-client requests

# Start metrics exporter
systemctl daemon-reload
systemctl enable trustwrapper-metrics
systemctl start trustwrapper-metrics

# Update Prometheus to scrape metrics exporter
sed -i "/- job_name: 'trustwrapper'/,+4d" prometheus/prometheus.yml
cat >> prometheus/prometheus.yml << 'EOL'

  - job_name: 'trustwrapper'
    static_configs:
      - targets: ['localhost:9183']
        labels:
          service: 'trustwrapper-metrics'
          component: 'eliza-plugin'
EOL

# Restart Prometheus to pick up new configuration
docker-compose restart prometheus

# Open firewall for metrics port (internal only)
ufw allow from 127.0.0.1 to any port 9183

echo "✅ Monitoring configured for TrustWrapper!"
echo "📊 Metrics available at: http://localhost:9183/metrics"
echo "📈 Grafana: http://74.50.113.152:3000"
EOF

echo "✅ Monitoring configuration complete!"

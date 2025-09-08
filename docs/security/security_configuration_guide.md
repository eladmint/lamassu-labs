# Security Configuration & Monitoring Guide

**Purpose:** Comprehensive guide for configuring, deploying, and monitoring Nuru AI's enterprise security implementation.

**📋 ARCHITECTURE REFERENCES:** For complete technical specifications, see the authoritative architecture documents:
- **[API_ARCHITECTURE.md](../../docs/API_ARCHITECTURE.md)** - Complete FastAPI system specifications
- **[SECURITY_ARCHITECTURE.md](../../docs/SECURITY_ARCHITECTURE.md)** - Enterprise security and threat protection
- **[DATABASE_ARCHITECTURE.md](../../docs/DATABASE_ARCHITECTURE.md)** - Supabase PostgreSQL with vector search
- **[SCRAPER_ARCHITECTURE.md](../../docs/SCRAPER_ARCHITECTURE.md)** - Enhanced Orchestrator scraper system
- **[DEPLOYMENT_ARCHITECTURE.md](../../docs/DEPLOYMENT_ARCHITECTURE.md)** - Cloud Run, CI/CD, and infrastructure patterns
- **[INTEGRATION_ARCHITECTURE.md](../../docs/INTEGRATION_ARCHITECTURE.md)** - Service integration and communication protocols
- **[MONITORING_ARCHITECTURE.md](../../docs/MONITORING_ARCHITECTURE.md)** - Comprehensive observability and performance monitoring

**Scope:** Security configuration, threat monitoring, incident response, and compliance management.

---

*Last Updated: May 30, 2025 - Security Implementation Complete*

## Overview

Nuru AI implements enterprise-grade security with comprehensive threat protection, real-time monitoring, and automated response capabilities. This guide covers all aspects of security configuration and operational procedures.

## Security Architecture

### Multi-Layer Protection
```
Request → Security Check → Rate Limit → Input Validation → Handler → Audit Log
    ↓           ↓             ↓              ↓            ↓          ↓
Block Check  IP Blocking  SQL/XSS Guard  Process     Response   Database
```

## 1. Security Configuration

### 1.1 Environment Configuration

**Core Security Settings:**
```bash
# Enable/disable security features
SECURITY_ENABLED=true
API_KEY_ENABLED=false          # Optional API key authentication
RATE_LIMIT_ENABLED=true        # Rate limiting protection
SECURITY_HEADERS_ENABLED=true  # Security headers middleware

# Rate limiting configuration
MAX_REQUESTS_PER_MINUTE=60     # Per-IP rate limit
MAX_REQUESTS_PER_HOUR=1000     # Per-IP hourly limit

# Authentication (optional)
ADMIN_API_KEY=your-secure-admin-key-here
USER_API_KEYS=user-key-1,user-key-2,user-key-3

# CORS configuration
ALLOWED_ORIGINS=https://nuru-ai.app,https://api.nuru-ai.app
```

**Security Validation:**
```bash
# Validate security configuration on startup
python -c "from chatbot_api.core.security import validate_security_config; validate_security_config()"
```

### 1.2 Database Security Setup

**Apply Security Migration:**
```bash
# Apply security tables and RLS policies
supabase db push

# Verify security tables created
supabase db inspect --table security_audit_log
supabase db inspect --table api_access_log
supabase db inspect --table rate_limit_violations
supabase db inspect --table security_policies
```

**RLS Policy Verification:**
```sql
-- Check RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE tablename IN ('security_audit_log', 'api_access_log', 'rate_limit_violations', 'security_policies');

-- Verify admin access policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename LIKE '%security%' OR tablename LIKE '%audit%';
```

## 2. API Key Management

### 2.1 Generate Secure API Keys

**Generate Admin API Key:**
```python
from chatbot_api.core.security import generate_api_key

# Generate 32-byte secure admin key
admin_key = generate_api_key(32)
print(f"Admin API Key: {admin_key}")

# Generate user keys
user_key_1 = generate_api_key(24)
user_key_2 = generate_api_key(24)
print(f"User Keys: {user_key_1}, {user_key_2}")
```

**Store in Google Secret Manager:**
```bash
# Store admin API key
echo "your-admin-key" | gcloud secrets create admin-api-key --data-file=-

# Store user API keys
echo "key1,key2,key3" | gcloud secrets create user-api-keys --data-file=-
```

### 2.2 API Key Usage

**Admin Access:**
```bash
# Access admin endpoints
curl -H "Authorization: Bearer your-admin-key" \
     https://api.nuru-ai.app/admin/status

# Alternative header format
curl -H "X-API-Key: your-admin-key" \
     https://api.nuru-ai.app/admin/security
```

**User Access:**
```bash
# Regular API access with user key
curl -H "Authorization: Bearer your-user-key" \
     https://api.nuru-ai.app/v2/chat \
     -d '{"user_id": "test", "message": "Hello"}'
```

## 3. Security Monitoring

### 3.1 Admin Security Dashboard

**Access Security Dashboard:**
```bash
# Real-time security monitoring
curl -H "Authorization: Bearer admin-key" \
     https://api.nuru-ai.app/admin/security

# System security status
curl -H "Authorization: Bearer admin-key" \
     https://api.nuru-ai.app/admin/status

# Cost protection security status
python scripts/cost_protection_monitor.py --status
```

**Dashboard Features:**
- **Real-time Alerts:** Current threat activity and blocked IPs
- **Threat Analysis:** Alert type distribution and severity trends
- **Performance Metrics:** Security system performance and response times
- **Historical Data:** Security event trends and pattern analysis
- **🛡️ Cost Anomaly Detection:** Unusual spending patterns that may indicate security incidents

### 3.2 Security Event Monitoring

**Query Security Events:**
```sql
-- Recent security alerts (last hour)
SELECT event_type, severity, COUNT(*) as count
FROM security_audit_log
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY event_type, severity
ORDER BY severity DESC, count DESC;

-- Blocked IPs
SELECT client_ip, COUNT(*) as violations, MAX(blocked_until) as blocked_until
FROM rate_limit_violations
WHERE blocked_until > NOW()
GROUP BY client_ip
ORDER BY violations DESC;

-- API access patterns
SELECT endpoint, method, COUNT(*) as requests, AVG(response_time_ms) as avg_response_time
FROM api_access_log
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY endpoint, method
ORDER BY requests DESC;

-- Cost anomaly detection for security incidents
SELECT DATE_TRUNC('hour', timestamp) as hour_bucket,
       COUNT(*) as requests,
       AVG(response_time_ms) as avg_response_time
FROM api_access_log
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY hour_bucket
HAVING COUNT(*) > (SELECT AVG(hourly_requests) * 3 FROM (
    SELECT COUNT(*) as hourly_requests
    FROM api_access_log
    WHERE timestamp > NOW() - INTERVAL '7 days'
    GROUP BY DATE_TRUNC('hour', timestamp)
) t);
```

**Security Alert Analysis:**
```python
# Get security monitoring data
from chatbot_api.core.security_monitoring import get_security_monitor

monitor = get_security_monitor()
summary = monitor.get_security_summary()
recent_alerts = monitor.get_recent_alerts(100)

print(f"Total alerts last hour: {summary['total_alerts_last_hour']}")
print(f"Blocked IPs: {summary['blocked_ips']}")
print(f"Threat levels: {summary['threat_levels']}")

# Check for cost anomalies that may indicate security incidents
cost_anomalies = monitor.check_cost_anomalies()
if cost_anomalies:
    print(f"SECURITY WARNING: Unusual cost patterns detected: {cost_anomalies}")
```

### 🛡️ 3.3 Cost Protection as Security Layer

**Cost-Based Security Monitoring:**
Cost protection serves as an additional security layer by detecting:

- **DDoS Attacks**: Sudden cost spikes from excessive resource usage
- **API Abuse**: Unusual patterns in API calls leading to higher costs
- **Unauthorized Access**: Unexpected service usage indicating compromised credentials
- **Resource Exhaustion**: Attacks designed to exhaust cloud resources

**Security Integration Commands:**
```bash
# Monitor costs for security anomalies
python scripts/cost_protection_monitor.py --security-mode

# Emergency security shutdown (if cost indicates attack)
python scripts/cost_protection_monitor.py --emergency-stop --reason="security_incident"

# Analyze cost patterns for security insights
python scripts/cost_dashboard.py --mode security-analysis

# Generate cost-based security report
python scripts/cost_protection_monitor.py --security-report
```

**Cost-Security Alert Thresholds:**
- **Immediate Alert**: Cost rate >$10/hour (potential security incident)
- **Emergency Stop**: Cost rate >$5/hour (automatic protection)
- **Investigation Trigger**: 3x normal cost patterns (security review required)
- **DDoS Detection**: Sudden 10x increase in API requests with cost spike

## 4. Security Testing

### 4.1 Input Validation Testing

**SQL Injection Tests:**
```bash
# Test SQL injection protection
curl -X POST "https://api.nuru-ai.app/v2/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "SELECT * FROM users--"}'
# Expected: 400 Bad Request with validation error

curl -X POST "https://api.nuru-ai.app/v2/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "1 OR 1=1 UNION SELECT password FROM users"}'
# Expected: 400 Bad Request
```

**XSS Protection Tests:**
```bash
# Test XSS protection
curl -X POST "https://api.nuru-ai.app/v2/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "<script>alert(\"xss\")</script>"}'
# Expected: 400 Bad Request

curl -X POST "https://api.nuru-ai.app/v2/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "javascript:alert(1)"}'
# Expected: 400 Bad Request
```

### 4.2 Rate Limiting Tests

**Rate Limit Testing:**
```bash
# Test rate limiting (should block after 60 requests)
for i in {1..70}; do
  echo "Request $i"
  curl -w "%{http_code}\n" -o /dev/null -s \
       "https://api.nuru-ai.app/health"
  sleep 0.1
done
# Expected: 200 for first 60, then 429 (Too Many Requests)
```

**Rate Limit Recovery Testing:**
```bash
# Wait for rate limit reset (1 minute) then test again
sleep 61
curl "https://api.nuru-ai.app/health"
# Expected: 200 (rate limit reset)
```

### 4.3 Authentication Testing

**API Key Authentication Tests:**
```bash
# Test without API key (should work for public endpoints)
curl "https://api.nuru-ai.app/health"
# Expected: 200

# Test admin endpoint without key (should fail)
curl "https://api.nuru-ai.app/admin/status"
# Expected: 401 Unauthorized

# Test admin endpoint with invalid key (should fail)
curl -H "Authorization: Bearer invalid-key" \
     "https://api.nuru-ai.app/admin/status"
# Expected: 401 Unauthorized

# Test admin endpoint with valid key (should work)
curl -H "Authorization: Bearer valid-admin-key" \
     "https://api.nuru-ai.app/admin/status"
# Expected: 200 with admin data
```

## 5. Incident Response

### 5.1 Security Alert Response

**High Priority Alerts:**
1. **Rate Limit Abuse Detection**
   - Automatic IP blocking for 1 hour
   - Monitor for distributed attacks
   - Review user-agent patterns

2. **Suspicious Input Detected**
   - Investigate source IP and user patterns
   - Check for coordinated attacks
   - Review input validation rules

3. **Repeated Failures**
   - Potential brute force attack
   - Automatic 30-minute IP blocking
   - Monitor authentication attempts

**Critical Priority Alerts:**
1. **SQL Injection Attempts**
   - Immediate 24-hour IP blocking
   - Review database query logs
   - Validate input sanitization effectiveness

2. **XSS Attack Attempts**
   - Immediate IP blocking
   - Review response sanitization
   - Check for successful exploitation

### 5.2 Incident Investigation

**Security Event Analysis:**
```sql
-- Investigate specific IP activity
SELECT * FROM security_audit_log
WHERE client_ip = '192.168.1.100'
ORDER BY timestamp DESC
LIMIT 50;

-- Check for attack patterns
SELECT event_type, details, COUNT(*) as frequency
FROM security_audit_log
WHERE severity IN ('high', 'critical')
  AND timestamp > NOW() - INTERVAL '24 hours'
GROUP BY event_type, details
ORDER BY frequency DESC;

-- Analyze API access patterns for suspicious activity
SELECT client_ip, endpoint, COUNT(*) as requests,
       COUNT(CASE WHEN status_code >= 400 THEN 1 END) as errors
FROM api_access_log
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY client_ip, endpoint
HAVING requests > 100 OR errors > 10
ORDER BY requests DESC;
```

### 5.3 Response Actions

**Manual IP Blocking:**
```python
# Block IP manually if needed
from chatbot_api.core.security_monitoring import get_security_monitor

monitor = get_security_monitor()
# Block IP for 24 hours
monitor.blocked_ips['192.168.1.100'] = time.time() + 86400
```

**Security Policy Updates:**
```sql
-- Update security policies in database
UPDATE security_policies
SET policy_value = '{"max_requests_per_minute": 30, "max_requests_per_hour": 500, "enabled": true}'
WHERE policy_name = 'rate_limits';

-- Add new blocked IP pattern
INSERT INTO security_policies (policy_name, policy_value) VALUES
('blocked_ip_patterns', '{"patterns": ["192.168.1.*", "10.0.0.*"], "enabled": true}');
```

## 6. Monitoring & Alerting

### 6.1 Security Metrics Tracking

**Key Security Metrics:**
- **Request Rate Patterns:** Monitor for unusual spikes
- **Failed Authentication Attempts:** Track brute force patterns
- **Input Validation Failures:** Monitor attack attempt types
- **Response Time Impact:** Measure security overhead
- **Blocked IP/User Counts:** Track protection effectiveness

### 6.2 Alert Configuration

**Google Cloud Monitoring Integration:**
```bash
# Create security alert policies
gcloud alpha monitoring policies create \
  --policy-from-file=metrics/configs/high_security_alerts.json

# Security dashboard setup
gcloud alpha monitoring dashboards create \
  --config-from-file=metrics/configs/security_dashboard.json
```

**Custom Alert Thresholds:**
- **Rate Limit Violations:** > 5 per minute
- **Input Validation Failures:** > 10 per minute
- **Failed Authentication:** > 20 per 15 minutes
- **High Severity Alerts:** Any critical security events

## 7. Compliance & Reporting

### 7.1 OWASP Top 10 Compliance

**Compliance Checklist:**
- [x] **A01 Broken Access Control** - API key auth + RLS
- [x] **A02 Cryptographic Failures** - Security headers + HTTPS
- [x] **A03 Injection** - Input validation + sanitization
- [x] **A04 Insecure Design** - Security-first architecture
- [x] **A05 Security Misconfiguration** - Secure defaults
- [x] **A06 Vulnerable Components** - Dependency monitoring
- [x] **A07 Authentication Failures** - Rate limiting + auth
- [x] **A08 Data Integrity Failures** - Input validation
- [x] **A09 Logging Failures** - Comprehensive audit logging
- [x] **A10 SSRF** - Input validation + URL restrictions

### 7.2 Security Audit Reports

**Generate Security Report:**
```sql
-- Weekly security summary
SELECT
  DATE_TRUNC('day', timestamp) as date,
  event_type,
  severity,
  COUNT(*) as events
FROM security_audit_log
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY DATE_TRUNC('day', timestamp), event_type, severity
ORDER BY date DESC, events DESC;

-- Monthly compliance report
SELECT
  'OWASP-A01' as control,
  'Broken Access Control' as description,
  'COMPLIANT' as status,
  'API key authentication + RLS policies' as implementation
UNION ALL
SELECT 'OWASP-A03', 'Injection', 'COMPLIANT', 'Input validation + sanitization'
-- ... continue for all OWASP controls
```

## 8. Maintenance & Updates

### 8.1 Security Configuration Reviews

**Monthly Security Review:**
1. **Rate Limit Analysis:** Review blocking patterns and adjust thresholds
2. **Input Validation Updates:** Add new attack patterns to detection
3. **Authentication Audit:** Review API key usage and rotate if needed
4. **Policy Updates:** Update security policies based on threat intelligence

### 8.2 Security Updates

**Update Security Patterns:**
```python
# Add new threat detection patterns
new_patterns = [
    r"(eval\(|exec\(|system\()",  # Code injection
    r"(wget\s|curl\s|http://)",   # SSRF attempts
    r"(passwd|shadow|hosts)"      # File access attempts
]

# Update InputValidator with new patterns
```

**Security Policy Maintenance:**
```sql
-- Review and update security policies
SELECT policy_name, policy_value, updated_at
FROM security_policies
ORDER BY updated_at ASC;

-- Update outdated policies
UPDATE security_policies
SET policy_value = '{"updated": "policy_value"}',
    updated_at = NOW()
WHERE policy_name = 'specific_policy';
```

## 9. Troubleshooting

### 9.1 Common Security Issues

**Rate Limiting Problems:**
```bash
# Check if user is being rate limited
curl -I "https://api.nuru-ai.app/health"
# Look for X-RateLimit-* headers

# Clear rate limit for specific IP (emergency)
python -c "
from chatbot_api.core.security import rate_limit_storage
rate_limit_storage.pop('ip:192.168.1.100', None)
"
```

**Authentication Issues:**
```bash
# Validate API key format
python -c "
from chatbot_api.core.security import APIKeyAuth
result = APIKeyAuth.validate_api_key('your-key-here')
print(f'Valid: {result is not None}')
"
```

### 9.2 Security Debugging

**Enable Debug Logging:**
```python
import logging
logging.getLogger('chatbot_api.core.security').setLevel(logging.DEBUG)
logging.getLogger('chatbot_api.core.security_monitoring').setLevel(logging.DEBUG)
```

**Check Security Middleware:**
```python
# Verify security middleware is loaded
from chatbot_api.main import app
print([str(middleware) for middleware in app.user_middleware])
# Should include SecurityMiddleware
```

## 10. Security Best Practices

### 10.1 Operational Security

**Daily Operations:**
- Monitor security dashboard for alerts
- Review blocked IP patterns for false positives
- Check API access logs for unusual patterns
- Validate security configuration during deployments

**Weekly Reviews:**
- Analyze security event trends
- Update threat detection patterns
- Review and rotate API keys if needed
- Test security configurations

**Monthly Audits:**
- Full security compliance review
- Update security documentation
- Review and update incident response procedures
- Security training and awareness updates

### 10.2 Development Security

**Secure Development Practices:**
- All user inputs must use InputValidator.sanitize_input()
- All endpoints must include @apply_rate_limit() decorator
- Admin endpoints must include @require_api_key() decorator
- All database queries must use parameterized queries
- All error messages must use ErrorSanitizer.sanitize_error_message()

---

**Security Contact:** security@nuru-ai.app
**Emergency Response:** Check admin security dashboard for real-time threats
**Documentation:** See `SECURITY.md` for complete security policy

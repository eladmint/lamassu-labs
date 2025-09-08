# TrustWrapper v2.0 API Reference

**Base URL**: `https://api.trustwrapper.ai/v2`
**Authentication**: Bearer token required for all protected endpoints
**Content-Type**: `application/json`

## 🔐 Authentication

All API requests must include an Authorization header with your API key:

```bash
Authorization: Bearer tw_sk_live_1234567890abcdef
```

Get your API key from the [TrustWrapper Dashboard](https://dashboard.trustwrapper.ai).

## 📋 API Tiers & Rate Limits

| Tier | Rate Limit | Monthly Quota | Access Level |
|------|------------|---------------|--------------|
| **Professional** | 100 req/min | 10K-50K calls | Advanced ML algorithms |
| **Enterprise** | 1000 req/min | Unlimited | Full feature access |

## 🧠 Advanced Verification API

### POST `/verification/advanced`

Perform advanced AI verification using proprietary ML algorithms.

**Requires**: Professional or Enterprise tier

#### Request

```json
{
  "text": "Should I invest in this 1000% guaranteed return scheme?",
  "options": {
    "includeMLAnalysis": true,
    "includeRiskProfiling": true,
    "customThresholds": {
      "scamThreshold": 0.8,
      "riskThreshold": 0.6
    }
  }
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "trustScore": 15,
    "riskLevel": "CRITICAL",
    "recommendation": "BLOCKED",
    "mlConfidence": 0.97,
    "factors": [
      {
        "name": "Unrealistic Returns",
        "score": 10,
        "weight": 0.3,
        "confidence": 0.99,
        "details": "Claims of 1000% returns detected",
        "category": "scam_detection"
      }
    ],
    "warnings": [
      "Contains obvious scam language patterns",
      "Unrealistic performance claims detected"
    ],
    "processingTime": 45,
    "timestamp": 1719331200000,
    "isAdvancedVerification": true
  }
}
```

### POST `/verification/batch`

Verify multiple items in a single request.

**Requires**: Professional or Enterprise tier

#### Request

```json
{
  "items": [
    {
      "id": "item_1",
      "text": "Buy Bitcoin now before it hits $100k"
    },
    {
      "id": "item_2",
      "text": "Diversify your portfolio with index funds"
    }
  ],
  "options": {
    "includeMLAnalysis": true
  }
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "results": [
      {
        "id": "item_1",
        "trustScore": 65,
        "riskLevel": "MEDIUM",
        "recommendation": "REVIEW"
      },
      {
        "id": "item_2",
        "trustScore": 85,
        "riskLevel": "LOW",
        "recommendation": "APPROVED"
      }
    ],
    "processingTime": 120,
    "itemsProcessed": 2
  }
}
```

## 🔍 Oracle Verification API (Enterprise Only)

### POST `/oracle/detect-manipulation`

Detect oracle manipulation using advanced multi-oracle analysis.

**Requires**: Enterprise tier only

#### Request

```json
{
  "symbol": "ETH/USD",
  "prices": [
    {
      "price": 3250.50,
      "timestamp": 1719331200,
      "source": "chainlink"
    },
    {
      "price": 3251.20,
      "timestamp": 1719331200,
      "source": "band_protocol"
    },
    {
      "price": 4200.00,
      "timestamp": 1719331200,
      "source": "custom_oracle"
    }
  ],
  "metadata": {
    "blockchain": "ethereum",
    "protocol": "mento"
  }
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "manipulationProbability": 0.95,
    "confidence": 0.98,
    "detectedPatterns": [
      "extreme_price_deviation",
      "consensus_breakdown",
      "volume_anomaly"
    ],
    "riskScore": 95,
    "affectedValue": 1250000,
    "recommendedActions": [
      "halt_trading",
      "investigate_custom_oracle",
      "notify_protocol_team"
    ],
    "alertLevel": "critical"
  }
}
```

### GET `/oracle/health/{symbol}`

Get oracle health metrics for a specific trading pair.

#### Response

```json
{
  "success": true,
  "data": {
    "symbol": "ETH/USD",
    "overallHealth": "healthy",
    "oracles": [
      {
        "source": "chainlink",
        "status": "healthy",
        "lastUpdate": 1719331200,
        "missedUpdates": 0,
        "averageLatency": 15,
        "reliabilityScore": 0.99
      }
    ],
    "consensusHealth": 0.98,
    "lastManipulationAlert": null
  }
}
```

## 📊 Enterprise Compliance API (Enterprise Only)

### POST `/compliance/check`

Check content for regulatory compliance violations.

**Requires**: Enterprise tier only

#### Request

```json
{
  "content": "Based on your medical history, I recommend investing in this high-risk crypto fund",
  "regulations": ["hipaa", "gdpr", "finra"]
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "gdprCompliant": false,
    "hipaaCompliant": false,
    "finraCompliant": false,
    "violations": [
      {
        "type": "medical_information_disclosure",
        "severity": "high",
        "description": "References medical history without proper consent",
        "regulation": "hipaa",
        "suggestedRemediation": "Remove medical references or obtain explicit consent"
      },
      {
        "type": "unsuitable_investment_advice",
        "severity": "critical",
        "description": "High-risk investment recommendation without suitability assessment",
        "regulation": "finra",
        "suggestedRemediation": "Perform investor suitability analysis before recommendation"
      }
    ],
    "riskAssessment": "HIGH - Multiple regulatory violations detected",
    "auditTrail": "compliance_check_20250625_143022"
  }
}
```

## 🧮 Zero-Knowledge Proofs API

### POST `/zk/generate-proof`

Generate a zero-knowledge proof for verification results.

#### Request

```json
{
  "verificationResult": {
    "trustScore": 85,
    "riskLevel": "LOW",
    "recommendation": "APPROVED",
    "timestamp": 1719331200000
  },
  "includeMetadata": false
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "proof": "0x1a2b3c4d5e6f...",
    "publicSignals": ["85", "1719331200000"],
    "proofHash": "0xabcdef123456..."
  }
}
```

### POST `/zk/verify-proof`

Verify a zero-knowledge proof from another party.

#### Request

```json
{
  "proof": "0x1a2b3c4d5e6f...",
  "publicSignals": ["85", "1719331200000"]
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "isValid": true,
    "trustScore": 85,
    "timestamp": 1719331200000
  }
}
```

## 📈 Analytics & Usage API

### GET `/analytics/usage`

Get usage analytics and billing information.

#### Query Parameters

- `timeframe`: `day`, `week`, `month` (default: `month`)

#### Response

```json
{
  "success": true,
  "data": {
    "totalRequests": 8750,
    "successRate": 0.997,
    "averageLatency": 42,
    "costThisMonth": 299.00,
    "remainingQuota": 1250,
    "tier": "professional",
    "billingPeriod": "2025-06-01 to 2025-06-30"
  }
}
```

## ❌ Error Responses

All error responses follow this format:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_API_KEY",
    "message": "The provided API key is invalid or expired",
    "type": "authentication_error"
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `INVALID_API_KEY` | API key is missing, invalid, or expired |
| `INSUFFICIENT_TIER` | Feature requires higher tier subscription |
| `RATE_LIMIT_EXCEEDED` | Too many requests, retry after cooldown |
| `QUOTA_EXCEEDED` | Monthly API quota exceeded |
| `INVALID_REQUEST` | Request format or parameters are invalid |
| `PROCESSING_ERROR` | Internal error during verification |

## 🔧 SDKs & Integration

### TypeScript/JavaScript

```bash
npm install @trustwrapper/api-client
```

```typescript
import { TrustWrapperClient } from '@trustwrapper/api-client';

const client = new TrustWrapperClient({
  apiKey: 'tw_sk_live_...',
  tier: 'professional'
});

const result = await client.verifyAdvanced('Investment recommendation text');
```

### Python

```bash
pip install trustwrapper-api
```

```python
from trustwrapper import TrustWrapperClient

client = TrustWrapperClient(
    api_key='tw_sk_live_...',
    tier='professional'
)

result = client.verify_advanced('Investment recommendation text')
```

### cURL Examples

```bash
# Advanced verification
curl -X POST https://api.trustwrapper.ai/v2/verification/advanced \
  -H "Authorization: Bearer tw_sk_live_..." \
  -H "Content-Type: application/json" \
  -d '{"text": "Investment advice text"}'

# Oracle manipulation detection (Enterprise only)
curl -X POST https://api.trustwrapper.ai/v2/oracle/detect-manipulation \
  -H "Authorization: Bearer tw_sk_enterprise_..." \
  -H "Content-Type: application/json" \
  -d '{"symbol": "ETH/USD", "prices": [...]}'
```

## 🔒 Security & Best Practices

### API Key Security
- Never expose API keys in client-side code
- Use environment variables for key storage
- Rotate keys regularly (quarterly recommended)
- Use different keys for development and production

### Rate Limiting
- Implement exponential backoff for retries
- Cache results when appropriate to reduce API calls
- Use batch endpoints for multiple verifications

### Error Handling
- Always check the `success` field in responses
- Implement graceful degradation for API failures
- Log errors for debugging but don't expose sensitive details

## 📞 Support & Resources

- **API Status**: [status.trustwrapper.ai](https://status.trustwrapper.ai)
- **Documentation**: [docs.trustwrapper.ai](https://docs.trustwrapper.ai)
- **Support**: api-support@trustwrapper.ai
- **Enterprise Sales**: enterprise@trustwrapper.ai

---

**Last Updated**: June 25, 2025
**API Version**: v2.0
**Rate Limits**: Subject to change with 30 days notice

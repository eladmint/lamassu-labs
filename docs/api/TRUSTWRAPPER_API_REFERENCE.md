# TrustWrapper API Reference

**Version**: 1.0  
**Base URL**: `https://api.trustwrapper.io/v1`  
**Status**: Production Ready

## 🚀 Overview

The TrustWrapper API provides programmatic access to AI verification services combining Zero-Knowledge Proofs, Explainable AI, and Quality Consensus. This RESTful API enables developers to add trust and transparency to any AI model or agent.

## 🔐 Authentication

All API requests require authentication using an API key.

### Headers
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

### Getting an API Key
```bash
# Register for an API key
curl -X POST https://api.trustwrapper.io/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@example.com",
    "organization": "Your Company",
    "use_case": "AI verification for healthcare"
  }'
```

### Response
```json
{
  "api_key": "tw_live_a1b2c3d4e5f6...",
  "api_secret": "tw_secret_9z8y7x6w5v...",
  "tier": "developer",
  "rate_limit": {
    "requests_per_minute": 60,
    "requests_per_day": 10000
  }
}
```

## 📊 Rate Limiting

| Tier | Requests/Minute | Requests/Day | Concurrent Requests |
|------|-----------------|--------------|---------------------|
| Developer | 60 | 10,000 | 10 |
| Startup | 300 | 100,000 | 50 |
| Enterprise | 1,000 | 1,000,000 | 200 |
| Custom | Unlimited | Unlimited | Unlimited |

Rate limit headers are included in all responses:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1624564800
```

## 🔧 Core Endpoints

### 1. Create Verification Session

**POST** `/verifications`

Create a new AI verification session for your model or agent.

#### Request Body
```json
{
  "model_id": "gpt-4-medical-v2",
  "model_type": "transformer",
  "verification_config": {
    "zk_proof": {
      "enabled": true,
      "proof_system": "groth16",
      "circuit_type": "neural_network",
      "optimization_level": "balanced"
    },
    "explainability": {
      "enabled": true,
      "methods": ["shap", "lime"],
      "sample_size": 100,
      "feature_importance_threshold": 0.1
    },
    "consensus": {
      "enabled": true,
      "validators": 5,
      "threshold": 0.8,
      "validator_specialization": ["quality", "safety", "domain"]
    }
  },
  "metadata": {
    "application": "medical_diagnosis",
    "compliance_requirements": ["HIPAA", "FDA"],
    "priority": "high"
  }
}
```

#### Response
```json
{
  "verification_id": "ver_1a2b3c4d5e6f",
  "status": "initialized",
  "created_at": "2025-06-22T10:00:00Z",
  "estimated_completion": "2025-06-22T10:00:30Z",
  "endpoints": {
    "status": "/verifications/ver_1a2b3c4d5e6f/status",
    "inference": "/verifications/ver_1a2b3c4d5e6f/inference",
    "results": "/verifications/ver_1a2b3c4d5e6f/results"
  }
}
```

#### Code Examples

**Python**
```python
import requests

api_key = "tw_live_your_api_key"
base_url = "https://api.trustwrapper.io/v1"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

verification_config = {
    "model_id": "gpt-4-medical-v2",
    "model_type": "transformer",
    "verification_config": {
        "zk_proof": {"enabled": True, "proof_system": "groth16"},
        "explainability": {"enabled": True, "methods": ["shap"]},
        "consensus": {"enabled": True, "validators": 5}
    }
}

response = requests.post(
    f"{base_url}/verifications",
    json=verification_config,
    headers=headers
)

verification = response.json()
print(f"Verification ID: {verification['verification_id']}")
```

**JavaScript/TypeScript**
```typescript
const apiKey = 'tw_live_your_api_key';
const baseUrl = 'https://api.trustwrapper.io/v1';

const verificationConfig = {
  model_id: 'gpt-4-medical-v2',
  model_type: 'transformer',
  verification_config: {
    zk_proof: { enabled: true, proof_system: 'groth16' },
    explainability: { enabled: true, methods: ['shap'] },
    consensus: { enabled: true, validators: 5 }
  }
};

const response = await fetch(`${baseUrl}/verifications`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(verificationConfig)
});

const verification = await response.json();
console.log(`Verification ID: ${verification.verification_id}`);
```

### 2. Submit Inference for Verification

**POST** `/verifications/{verification_id}/inference`

Submit an AI inference for verification with proof generation and explanation.

#### Request Body
```json
{
  "input_data": {
    "text": "Patient presents with persistent cough, fever 101.5°F, fatigue for 5 days",
    "patient_age": 45,
    "medical_history": ["hypertension", "diabetes_type_2"]
  },
  "model_output": {
    "diagnosis": "Probable viral respiratory infection",
    "confidence": 0.82,
    "differential": [
      {"condition": "COVID-19", "probability": 0.45},
      {"condition": "Influenza", "probability": 0.30},
      {"condition": "Bacterial pneumonia", "probability": 0.15}
    ],
    "recommendations": [
      "COVID-19 and influenza testing",
      "Chest X-ray if symptoms worsen",
      "Symptomatic treatment"
    ]
  },
  "verification_options": {
    "fast_mode": false,
    "include_counterfactuals": true,
    "explanation_detail": "high"
  }
}
```

#### Response
```json
{
  "inference_id": "inf_9z8y7x6w5v",
  "verification_id": "ver_1a2b3c4d5e6f",
  "status": "processing",
  "stages": {
    "zk_proof": {"status": "generating", "progress": 0.3},
    "explainability": {"status": "pending", "progress": 0},
    "consensus": {"status": "pending", "progress": 0}
  },
  "estimated_completion": "2025-06-22T10:01:00Z",
  "webhook_url": "https://your-domain.com/webhooks/trustwrapper"
}
```

### 3. Get Verification Results

**GET** `/verifications/{verification_id}/results/{inference_id}`

Retrieve complete verification results including ZK proof, explanations, and consensus.

#### Response
```json
{
  "inference_id": "inf_9z8y7x6w5v",
  "verification_id": "ver_1a2b3c4d5e6f",
  "status": "completed",
  "timestamp": "2025-06-22T10:01:30Z",
  "trust_score": 0.91,
  "results": {
    "zk_proof": {
      "proof": "0x1234567890abcdef...",
      "proof_system": "groth16",
      "verification_key": "vk_abc123...",
      "public_inputs": ["0x456...", "0x789..."],
      "generation_time_ms": 847,
      "verified": true
    },
    "explainability": {
      "method": "shap",
      "feature_importance": {
        "fever": 0.35,
        "cough": 0.28,
        "patient_age": 0.15,
        "medical_history": 0.12,
        "fatigue": 0.10
      },
      "explanation_text": "The diagnosis is primarily driven by the combination of fever (35%) and persistent cough (28%). Patient age and medical history contribute moderately to the assessment.",
      "counterfactuals": [
        {
          "change": "Remove fever symptom",
          "new_diagnosis": "Possible allergic reaction",
          "confidence_change": -0.31
        }
      ],
      "visual_explanation_url": "https://api.trustwrapper.io/v1/explanations/visual/exp_123"
    },
    "consensus": {
      "agreement_score": 0.88,
      "validators": 5,
      "votes": {
        "quality": { "score": 0.90, "validators": ["val_1", "val_2", "val_3"] },
        "safety": { "score": 0.85, "validators": ["val_2", "val_4", "val_5"] },
        "domain": { "score": 0.89, "validators": ["val_1", "val_3", "val_5"] }
      },
      "concerns": [
        {
          "validator": "val_4",
          "type": "differential_completeness",
          "severity": "low",
          "message": "Consider including acute bronchitis in differential"
        }
      ]
    }
  },
  "compliance": {
    "hipaa_compliant": true,
    "audit_trail": "https://api.trustwrapper.io/v1/audit/aud_xyz789",
    "certifications": ["ISO 27001", "SOC 2 Type II"]
  }
}
```

### 4. Batch Verification

**POST** `/verifications/batch`

Submit multiple inferences for parallel verification (Enterprise tier only).

#### Request Body
```json
{
  "verification_id": "ver_1a2b3c4d5e6f",
  "inferences": [
    {
      "inference_id": "custom_001",
      "input_data": {...},
      "model_output": {...}
    },
    {
      "inference_id": "custom_002",
      "input_data": {...},
      "model_output": {...}
    }
  ],
  "batch_options": {
    "parallel_processing": true,
    "priority": "high",
    "callback_url": "https://your-domain.com/batch-complete"
  }
}
```

### 5. Verification Status

**GET** `/verifications/{verification_id}/status`

Check the current status of a verification session.

#### Response
```json
{
  "verification_id": "ver_1a2b3c4d5e6f",
  "status": "active",
  "created_at": "2025-06-22T10:00:00Z",
  "configuration": {
    "model_id": "gpt-4-medical-v2",
    "zk_enabled": true,
    "xai_enabled": true,
    "consensus_enabled": true
  },
  "statistics": {
    "total_inferences": 156,
    "successful_verifications": 154,
    "failed_verifications": 2,
    "average_trust_score": 0.89,
    "average_processing_time_ms": 1250
  },
  "rate_limit_status": {
    "used": 156,
    "limit": 10000,
    "reset_at": "2025-06-23T00:00:00Z"
  }
}
```

## 🔍 Advanced Features

### Model Registration

**POST** `/models`

Register a model for optimized verification performance.

```json
{
  "model_name": "medical-diagnosis-v3",
  "model_type": "transformer",
  "architecture": {
    "layers": 24,
    "parameters": "7B",
    "input_shape": [512],
    "output_classes": 1000
  },
  "optimization_preferences": {
    "latency_priority": "high",
    "accuracy_threshold": 0.99,
    "cache_proofs": true
  }
}
```

### Custom Validators

**POST** `/validators/custom`

Register custom validators for domain-specific consensus (Enterprise only).

```json
{
  "validator_name": "medical-ethics-validator",
  "specialization": "healthcare",
  "validation_rules": {
    "check_ethical_guidelines": true,
    "verify_clinical_protocols": true,
    "assess_bias": true
  },
  "webhook_endpoint": "https://your-validator.com/validate"
}
```

### Streaming Verification

**GET** `/verifications/{verification_id}/stream`

Real-time streaming of verification progress using Server-Sent Events.

```javascript
const eventSource = new EventSource(
  `https://api.trustwrapper.io/v1/verifications/${verificationId}/stream`,
  {
    headers: {
      'Authorization': `Bearer ${apiKey}`
    }
  }
);

eventSource.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log(`Stage: ${update.stage}, Progress: ${update.progress}`);
};
```

## 🛠️ SDK Support

### Python SDK
```bash
pip install trustwrapper
```

```python
from trustwrapper import TrustWrapperClient

client = TrustWrapperClient(api_key="tw_live_...")
verification = client.create_verification(
    model_id="my-model",
    zk_enabled=True,
    xai_enabled=True
)

result = client.verify_inference(
    verification_id=verification.id,
    input_data={"text": "..."},
    model_output={"prediction": "..."}
)

print(f"Trust Score: {result.trust_score}")
print(f"Explanation: {result.explanation}")
```

### JavaScript/TypeScript SDK
```bash
npm install @trustwrapper/sdk
```

```typescript
import { TrustWrapper } from '@trustwrapper/sdk';

const tw = new TrustWrapper({ apiKey: 'tw_live_...' });

const verification = await tw.createVerification({
  modelId: 'my-model',
  zkEnabled: true,
  xaiEnabled: true
});

const result = await tw.verifyInference({
  verificationId: verification.id,
  inputData: { text: '...' },
  modelOutput: { prediction: '...' }
});

console.log(`Trust Score: ${result.trustScore}`);
```

## 🚨 Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please retry after 60 seconds.",
    "details": {
      "limit": 60,
      "reset_at": "2025-06-22T10:05:00Z",
      "upgrade_url": "https://trustwrapper.io/pricing"
    }
  },
  "request_id": "req_abc123xyz"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_API_KEY` | 401 | Invalid or missing API key |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INVALID_REQUEST` | 400 | Malformed request body |
| `MODEL_NOT_FOUND` | 404 | Specified model not registered |
| `VERIFICATION_FAILED` | 500 | Internal verification error |
| `TIMEOUT` | 504 | Verification timeout |
| `INSUFFICIENT_TIER` | 403 | Feature requires plan upgrade |

## 📡 Webhooks

Configure webhooks to receive real-time updates:

**POST** `/webhooks`
```json
{
  "url": "https://your-domain.com/trustwrapper-webhook",
  "events": ["verification.completed", "verification.failed"],
  "secret": "your_webhook_secret"
}
```

### Webhook Payload
```json
{
  "event": "verification.completed",
  "timestamp": "2025-06-22T10:01:30Z",
  "data": {
    "verification_id": "ver_1a2b3c4d5e6f",
    "inference_id": "inf_9z8y7x6w5v",
    "trust_score": 0.91,
    "summary": "Verification completed successfully"
  },
  "signature": "sha256=abc123..."
}
```

## 🔒 Security Best Practices

1. **API Key Security**
   - Never expose API keys in client-side code
   - Rotate keys regularly using the dashboard
   - Use environment variables for key storage

2. **Request Signing**
   - Enable request signing for additional security
   - Verify webhook signatures to ensure authenticity

3. **Data Privacy**
   - All data is encrypted in transit (TLS 1.3)
   - Zero-knowledge proofs ensure model privacy
   - No training data is stored or logged

## 📈 Monitoring & Analytics

Access detailed analytics via the dashboard or API:

**GET** `/analytics/usage`
```json
{
  "period": "2025-06",
  "metrics": {
    "total_verifications": 15420,
    "average_trust_score": 0.88,
    "average_latency_ms": 1150,
    "error_rate": 0.002,
    "top_models": [
      {"model_id": "gpt-4-medical", "verifications": 5200},
      {"model_id": "finance-bert", "verifications": 3100}
    ]
  }
}
```

## 🌐 API Status

Check API health and status:
- Status Page: https://status.trustwrapper.io
- Health Check: `GET /health`

---

For additional support, visit our [Developer Portal](https://developers.trustwrapper.io) or contact support@trustwrapper.io.
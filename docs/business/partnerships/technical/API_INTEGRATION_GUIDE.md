# Mento Labs API Integration Guide
## Complete Technical Reference for ZK Oracle & Treasury Monitor Integration

**Version**: 1.0.0
**Last Updated**: June 23, 2025
**Maintainers**: Lamassu Labs Integration Team

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication & Security](#authentication--security)
3. [Treasury Monitor API](#treasury-monitor-api)
4. [ZK Oracle Verification API](#zk-oracle-verification-api)
5. [WebSocket Subscriptions](#websocket-subscriptions)
6. [SDK Integration](#sdk-integration)
7. [Error Handling](#error-handling)
8. [Rate Limits & Quotas](#rate-limits--quotas)
9. [Migration Guide](#migration-guide)
10. [Support & Resources](#support--resources)

---

## Quick Start

### Installation

```bash
# NPM
npm install @lamassu-labs/mento-integration

# Yarn
yarn add @lamassu-labs/mento-integration

# Python
pip install lamassu-mento
```

### Basic Setup

```typescript
import { MentoIntegration } from '@lamassu-labs/mento-integration';

// Initialize the client
const client = new MentoIntegration({
    apiKey: process.env.LAMASSU_API_KEY,
    network: 'alfajores', // or 'mainnet'
    endpoints: {
        treasury: 'https://api.lamassu-labs.ai/mento/treasury',
        oracle: 'https://api.lamassu-labs.ai/mento/oracle'
    }
});

// Quick health check
const status = await client.healthCheck();
console.log('System Status:', status);
```

### Minimal Example

```typescript
// Get treasury status
const treasury = await client.treasury.getStatus({
    addresses: ['0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1'],
    stablecoins: ['cUSD', 'cEUR', 'cREAL']
});

// Verify oracle price
const verification = await client.oracle.verifyPrice({
    pair: 'CELO/USD',
    proof: proofData
});
```

---

## Authentication & Security

### API Key Management

```typescript
// Environment variables (recommended)
export LAMASSU_API_KEY="your-api-key-here"
export LAMASSU_SECRET="your-secret-here"

// Programmatic authentication
const client = new MentoIntegration({
    auth: {
        apiKey: process.env.LAMASSU_API_KEY,
        apiSecret: process.env.LAMASSU_SECRET,
        // Optional: JWT for enhanced security
        useJWT: true
    }
});
```

### Request Signing

All requests are automatically signed using HMAC-SHA256:

```typescript
// Manual signing (for custom requests)
const signature = client.auth.signRequest({
    method: 'POST',
    path: '/api/v1/oracle/verify',
    body: requestBody,
    timestamp: Date.now()
});

// Add to headers
headers['X-Signature'] = signature;
headers['X-Timestamp'] = timestamp;
```

### IP Whitelisting

Configure allowed IPs in your dashboard:

```json
{
    "security": {
        "ipWhitelist": [
            "192.168.1.0/24",
            "10.0.0.0/8"
        ],
        "enforceWhitelist": true
    }
}
```

---

## Treasury Monitor API

### Get Treasury Status

```typescript
// GET /api/v1/treasury/status
interface TreasuryStatusRequest {
    addresses: string[];
    stablecoins?: StablecoinType[];
    chains?: Chain[];
    includeHistory?: boolean;
}

interface TreasuryStatusResponse {
    timestamp: string;
    totalValueUSD: number;
    balances: {
        [address: string]: {
            [stablecoin: string]: {
                balance: string;
                valueUSD: number;
                chain: string;
                lastUpdate: string;
            }
        }
    };
    reserveStatus: {
        ratio: number;
        targetRatio: number;
        totalReserves: number;
        collateral: {
            [asset: string]: number;
        }
    };
}

// Example
const status = await client.treasury.getStatus({
    addresses: [
        '0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1',
        '0x10c892A6EC43a53E45D0B916B4b7D383B1b78C0F'
    ],
    stablecoins: ['cUSD', 'cEUR'],
    includeHistory: true
});
```

### Subscribe to Alerts

```typescript
// POST /api/v1/treasury/alerts/subscribe
interface AlertSubscription {
    addresses: string[];
    channels: {
        email?: string;
        slack?: string;
        webhook?: string;
    };
    thresholds: {
        reserveRatioMin?: number;
        priceDeviationMax?: number;
        transactionVolumeAlert?: number;
    };
}

// Example
const subscription = await client.treasury.subscribeAlerts({
    addresses: ['0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1'],
    channels: {
        email: 'treasury@mento.org',
        webhook: 'https://mento.org/webhooks/treasury'
    },
    thresholds: {
        reserveRatioMin: 1.8,
        priceDeviationMax: 0.02
    }
});
```

### Get Historical Analytics

```typescript
// GET /api/v1/treasury/analytics
interface AnalyticsRequest {
    addresses: string[];
    metrics: MetricType[];
    timeRange: {
        start: string; // ISO 8601
        end: string;
    };
    granularity: 'hour' | 'day' | 'week';
}

interface AnalyticsResponse {
    metrics: {
        [metric: string]: {
            data: Array<{
                timestamp: string;
                value: number;
            }>;
            aggregates: {
                min: number;
                max: number;
                average: number;
                standardDeviation: number;
            };
        };
    };
}

// Example
const analytics = await client.treasury.getAnalytics({
    addresses: ['0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1'],
    metrics: ['reserve_ratio', 'total_value', 'transaction_volume'],
    timeRange: {
        start: '2025-06-01T00:00:00Z',
        end: '2025-06-23T23:59:59Z'
    },
    granularity: 'day'
});
```

---

## ZK Oracle Verification API

### Submit Price with Proof

```typescript
// POST /api/v1/oracle/submit
interface PriceSubmission {
    assetPair: string;
    price: string;
    proof: {
        data: string; // Base64 encoded proof
        publicInputs: {
            finalPrice: string;
            timestamp: number;
            numSources: number;
            confidence: number;
        };
    };
}

interface SubmissionResponse {
    success: boolean;
    proofId: string;
    verificationStatus: 'pending' | 'verified' | 'failed';
    transactionHash?: string;
    gasUsed?: number;
}

// Example
const submission = await client.oracle.submitPrice({
    assetPair: 'CELO/USD',
    price: '0.5342',
    proof: {
        data: 'base64_encoded_proof_data...',
        publicInputs: {
            finalPrice: '534200000', // 8 decimals
            timestamp: Date.now(),
            numSources: 5,
            confidence: 9500 // 95%
        }
    }
});
```

### Verify Existing Proof

```typescript
// POST /api/v1/oracle/verify
interface VerificationRequest {
    proofId?: string;
    proofData?: string;
    assetPair: string;
}

interface VerificationResponse {
    valid: boolean;
    verifiedPrice?: string;
    confidence?: number;
    gasEstimate: number;
    details?: {
        sourcesVerified: number;
        deviationCheck: boolean;
        timestampCheck: boolean;
    };
}

// Example
const verification = await client.oracle.verifyProof({
    proofId: 'proof_abc123',
    assetPair: 'CELO/USD'
});
```

### Get Oracle Status

```typescript
// GET /api/v1/oracle/status
interface OracleStatusResponse {
    operational: boolean;
    lastUpdate: string;
    activeProvers: number;
    verifiedPrices: {
        [assetPair: string]: {
            price: string;
            lastUpdate: string;
            confidence: number;
            proofId: string;
        };
    };
    statistics: {
        proofsGenerated24h: number;
        averageProofTime: number;
        successRate: number;
    };
}

// Example
const oracleStatus = await client.oracle.getStatus();
```

### Batch Price Updates

```typescript
// POST /api/v1/oracle/batch
interface BatchPriceUpdate {
    updates: Array<{
        assetPair: string;
        price: string;
        sources: PriceSource[];
    }>;
    generateProof: boolean;
}

interface BatchUpdateResponse {
    batchId: string;
    proofs: Array<{
        assetPair: string;
        proofId: string;
        status: string;
    }>;
    merkleRoot: string;
    gasEstimate: number;
}

// Example
const batch = await client.oracle.batchUpdate({
    updates: [
        {
            assetPair: 'CELO/USD',
            price: '0.5342',
            sources: [/* price sources */]
        },
        {
            assetPair: 'cUSD/USD',
            price: '1.0012',
            sources: [/* price sources */]
        }
    ],
    generateProof: true
});
```

---

## WebSocket Subscriptions

### Real-time Price Updates

```typescript
// Connect to WebSocket
const ws = client.websocket.connect();

// Subscribe to price updates
ws.subscribe('prices', {
    pairs: ['CELO/USD', 'cUSD/USD', 'cEUR/EUR'],
    includeProofs: true
});

// Handle updates
ws.on('price_update', (data) => {
    console.log(`${data.pair}: ${data.price} (confidence: ${data.confidence})`);

    if (data.proof) {
        // Proof is included for verification
        console.log(`Proof ID: ${data.proof.id}`);
    }
});

// Subscribe to alerts
ws.subscribe('alerts', {
    addresses: ['0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1']
});

ws.on('alert', (alert) => {
    console.log(`Alert: ${alert.level} - ${alert.message}`);
});
```

### Connection Management

```typescript
// Auto-reconnect configuration
const ws = client.websocket.connect({
    autoReconnect: true,
    reconnectInterval: 5000,
    maxReconnectAttempts: 10
});

// Connection lifecycle
ws.on('connect', () => console.log('Connected'));
ws.on('disconnect', () => console.log('Disconnected'));
ws.on('error', (error) => console.error('WebSocket error:', error));

// Graceful shutdown
process.on('SIGINT', async () => {
    await ws.disconnect();
    process.exit(0);
});
```

---

## SDK Integration

### TypeScript/JavaScript

```typescript
import {
    MentoIntegration,
    TreasuryMonitor,
    OracleVerifier,
    AlertLevel
} from '@lamassu-labs/mento-integration';

// Advanced configuration
const config = {
    apiKey: process.env.LAMASSU_API_KEY,
    network: 'mainnet',
    options: {
        timeout: 30000,
        retries: 3,
        cacheEnabled: true,
        cacheTTL: 300 // 5 minutes
    }
};

const client = new MentoIntegration(config);

// Type-safe operations
const monitor = new TreasuryMonitor(client);
const verifier = new OracleVerifier(client);

// React hook example
function useTreasuryStatus(addresses: string[]) {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        monitor.getStatus({ addresses })
            .then(setStatus)
            .finally(() => setLoading(false));
    }, [addresses]);

    return { status, loading };
}
```

### Python

```python
from lamassu_mento import MentoIntegration, TreasuryMonitor, OracleVerifier
from lamassu_mento.types import AlertLevel, StablecoinType

# Initialize client
client = MentoIntegration(
    api_key=os.environ['LAMASSU_API_KEY'],
    network='mainnet'
)

# Treasury monitoring
monitor = TreasuryMonitor(client)
status = await monitor.get_status(
    addresses=['0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1'],
    stablecoins=[StablecoinType.CUSD, StablecoinType.CEUR]
)

# Oracle verification
verifier = OracleVerifier(client)
result = await verifier.verify_price(
    asset_pair='CELO/USD',
    proof_data=proof_bytes
)

# Async context manager
async with MentoIntegration(api_key=api_key) as client:
    status = await client.treasury.get_status(addresses)
```

### Go

```go
package main

import (
    "github.com/lamassu-labs/mento-integration-go"
    "github.com/lamassu-labs/mento-integration-go/treasury"
    "github.com/lamassu-labs/mento-integration-go/oracle"
)

func main() {
    // Initialize client
    client := mento.NewClient(
        mento.WithAPIKey(os.Getenv("LAMASSU_API_KEY")),
        mento.WithNetwork("mainnet"),
    )

    // Treasury monitoring
    monitor := treasury.NewMonitor(client)
    status, err := monitor.GetStatus(treasury.StatusRequest{
        Addresses: []string{"0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1"},
        Stablecoins: []string{"cUSD", "cEUR"},
    })

    // Oracle verification
    verifier := oracle.NewVerifier(client)
    result, err := verifier.VerifyPrice(oracle.VerifyRequest{
        AssetPair: "CELO/USD",
        ProofData: proofBytes,
    })
}
```

---

## Error Handling

### Error Response Format

```json
{
    "error": {
        "code": "INVALID_PROOF",
        "message": "Proof verification failed: invalid constraints",
        "details": {
            "constraint": "timestamp_check",
            "expected": 1719158400,
            "actual": 1719154800
        },
        "requestId": "req_abc123",
        "documentation": "https://docs.lamassu-labs.ai/errors/INVALID_PROOF"
    }
}
```

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `AUTH_FAILED` | Invalid API key or signature | Check credentials |
| `RATE_LIMITED` | Too many requests | Implement backoff |
| `INVALID_PROOF` | Proof verification failed | Check proof generation |
| `INSUFFICIENT_SOURCES` | Not enough price sources | Add more sources |
| `STALE_DATA` | Data too old | Refresh price feeds |
| `NETWORK_ERROR` | Blockchain connection issue | Retry with backoff |

### Error Handling Best Practices

```typescript
try {
    const result = await client.oracle.submitPrice(priceData);
} catch (error) {
    if (error.code === 'RATE_LIMITED') {
        // Implement exponential backoff
        await sleep(error.retryAfter * 1000);
        return retry();
    } else if (error.code === 'INVALID_PROOF') {
        // Regenerate proof with fresh data
        const newProof = await generateProof(freshSources);
        return client.oracle.submitPrice({ ...priceData, proof: newProof });
    } else {
        // Log and alert
        logger.error('Oracle submission failed', error);
        alerting.send('Oracle Error', error);
        throw error;
    }
}
```

---

## Rate Limits & Quotas

### Default Limits

| Endpoint | Rate Limit | Burst | Quota (Daily) |
|----------|------------|-------|---------------|
| Treasury Status | 100/min | 200 | 10,000 |
| Oracle Submit | 10/min | 20 | 1,000 |
| Oracle Verify | 50/min | 100 | 5,000 |
| Analytics | 10/min | 20 | 500 |
| WebSocket | 1000 msg/min | - | Unlimited |

### Rate Limit Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1719158400
X-RateLimit-Retry-After: 60
```

### Handling Rate Limits

```typescript
class RateLimitHandler {
    async executeWithRetry<T>(
        fn: () => Promise<T>,
        maxRetries: number = 3
    ): Promise<T> {
        for (let i = 0; i < maxRetries; i++) {
            try {
                return await fn();
            } catch (error) {
                if (error.code === 'RATE_LIMITED' && i < maxRetries - 1) {
                    const delay = error.retryAfter || Math.pow(2, i) * 1000;
                    await new Promise(resolve => setTimeout(resolve, delay));
                } else {
                    throw error;
                }
            }
        }
    }
}
```

---

## Migration Guide

### From Chainlink to Verified Oracle

```typescript
// Before (Chainlink only)
const price = await chainlinkOracle.latestAnswer();
const decimals = await chainlinkOracle.decimals();
const finalPrice = price / Math.pow(10, decimals);

// After (Verified Oracle)
const { verifiedPrice, confidence } = await client.oracle.getVerifiedPrice({
    assetPair: 'CELO/USD'
});

// With backwards compatibility
const price = await client.oracle.getPrice({
    assetPair: 'CELO/USD',
    fallbackToChainlink: true // Use Chainlink if no verified price
});
```

### Contract Migration

```solidity
// Add to existing Mento contracts
contract MentoExchangeV2 is MentoExchange {
    IVerifiedOracle public verifiedOracle;
    bool public useVerifiedPrices = false;

    function enableVerifiedOracle(address _oracle) external onlyOwner {
        verifiedOracle = IVerifiedOracle(_oracle);
        useVerifiedPrices = true;
    }

    function getPrice(address token) public view returns (uint256) {
        if (useVerifiedPrices && address(verifiedOracle) != address(0)) {
            try verifiedOracle.getVerifiedPrice(token) returns (uint256 price) {
                return price;
            } catch {
                // Fallback to original oracle
                return super.getPrice(token);
            }
        }
        return super.getPrice(token);
    }
}
```

---

## Support & Resources

### Documentation
- [API Reference](https://docs.lamassu-labs.ai/mento/api)
- [Integration Examples](https://github.com/lamassu-labs/mento-examples)
- [Video Tutorials](https://youtube.com/lamassu-labs)

### Developer Support
- **Discord**: [discord.gg/lamassu-labs](https://discord.gg/lamassu-labs)
- **Email**: mento-support@lamassu-labs.ai
- **Office Hours**: Tuesdays 2-3 PM UTC

### Monitoring & Status
- **Status Page**: [status.lamassu-labs.ai](https://status.lamassu-labs.ai)
- **API Health**: [api.lamassu-labs.ai/health](https://api.lamassu-labs.ai/health)

### SLA & Support Tiers

| Tier | Response Time | Availability | Support Hours |
|------|---------------|--------------|---------------|
| Basic | 24 hours | 99.5% | Business hours |
| Pro | 4 hours | 99.9% | Extended hours |
| Enterprise | 1 hour | 99.95% | 24/7 |

---

## Appendix: Complete Integration Example

```typescript
// Complete integration example
import { MentoIntegration } from '@lamassu-labs/mento-integration';

async function setupMentoIntegration() {
    // Initialize client
    const client = new MentoIntegration({
        apiKey: process.env.LAMASSU_API_KEY,
        network: 'mainnet',
        options: {
            cacheEnabled: true,
            autoRetry: true
        }
    });

    // Set up treasury monitoring
    const treasuryAddresses = [
        '0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1',
        '0x10c892A6EC43a53E45D0B916B4b7D383B1b78C0F'
    ];

    // Subscribe to alerts
    await client.treasury.subscribeAlerts({
        addresses: treasuryAddresses,
        channels: {
            webhook: 'https://your-domain.com/webhooks/treasury'
        },
        thresholds: {
            reserveRatioMin: 1.8,
            priceDeviationMax: 0.02
        }
    });

    // Set up oracle price feeds
    const priceFeeds = ['CELO/USD', 'cUSD/USD', 'cEUR/EUR'];

    // WebSocket for real-time updates
    const ws = client.websocket.connect();
    ws.subscribe('prices', { pairs: priceFeeds });

    ws.on('price_update', async (data) => {
        console.log(`Price update: ${data.pair} = ${data.price}`);

        // Verify the proof
        if (data.proof) {
            const verification = await client.oracle.verifyProof({
                proofData: data.proof.data,
                assetPair: data.pair
            });

            if (verification.valid) {
                // Use the verified price
                await updateInternalPriceFeeds(data.pair, data.price);
            }
        }
    });

    // Periodic treasury check
    setInterval(async () => {
        const status = await client.treasury.getStatus({
            addresses: treasuryAddresses,
            includeHistory: true
        });

        // Check reserve ratio
        if (status.reserveStatus.ratio < 2.0) {
            console.warn('Reserve ratio below target!', status.reserveStatus);
        }

        // Update dashboards
        await updateDashboard(status);
    }, 60000); // Every minute

    return client;
}

// Run the integration
setupMentoIntegration()
    .then(() => console.log('Mento integration active'))
    .catch(console.error);
```

---

*Last updated: June 23, 2025 | Version 1.0.0*

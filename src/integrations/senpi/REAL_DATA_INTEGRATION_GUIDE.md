# TrustWrapper Senpi Integration - Real Data Implementation Guide

**Status**: Moving from Mock to Production Data
**Created**: June 24, 2025
**Sprint**: Sprint 18 - Senpi AI Strategic Partnership

## 🎯 **Executive Summary**

This guide outlines the path to transform our TrustWrapper Senpi integration from mock implementations to real production data. We have a complete working plugin with mock data that demonstrates the integration capabilities. Now we need to connect it to real blockchain data, market feeds, and build the TrustWrapper backend API.

## 📊 **Current State Analysis**

### **What We Have**
1. **Complete Senpi Plugin** ✅
   - 3 verification actions (trading, skills, compliance)
   - Intelligent provider with context
   - Quality evaluator for scoring
   - Full TypeScript definitions
   - Professional documentation

2. **NOWNodes API Access** ✅
   - 70+ blockchain support
   - Transaction verification
   - Wallet balance checking
   - Already integrated in Cardano Treasury Monitor

3. **Existing Infrastructure** ✅
   - Hivelocity VPS servers (Staten Island + Tampa)
   - Working extraction service
   - Risk assessment engine
   - Alert systems

### **What We Need**
1. **TrustWrapper Backend API** ❌
   - ZK proof generation
   - XAI explanations
   - Consensus network
   - Trust scoring database

2. **Market Data Integration** ❌
   - Real-time price feeds
   - Volume and volatility data
   - Market sentiment analysis
   - Liquidity metrics

3. **Production Infrastructure** ❌
   - API gateway with auth
   - Caching layer
   - Performance optimization
   - Monitoring and analytics

## 🏗️ **Implementation Phases**

### **Phase 1: NOWNodes Integration (Week 1)**

#### **1.1 Enhance Trading Verification**
```typescript
// File: src/services/blockchain/nowNodesService.ts
import axios from 'axios';

export class NOWNodesService {
    private apiKey: string;
    private baseUrls: Record<string, string> = {
        ethereum: 'https://eth.nownodes.io',
        cardano: 'https://ada.nownodes.io',
        solana: 'https://sol.nownodes.io',
        // Add more chains as needed
    };

    async verifyTransaction(txHash: string, chain: string): Promise<TransactionVerification> {
        const url = `${this.baseUrls[chain]}/tx/${txHash}`;
        const response = await axios.get(url, {
            headers: { 'api-key': this.apiKey }
        });

        return {
            verified: response.data.confirmations > 0,
            amount: this.parseAmount(response.data),
            timestamp: response.data.timestamp,
            confirmations: response.data.confirmations,
            from: response.data.from,
            to: response.data.to
        };
    }

    async getWalletBalance(address: string, chain: string): Promise<WalletBalance> {
        const url = `${this.baseUrls[chain]}/address/${address}/balance`;
        const response = await axios.get(url, {
            headers: { 'api-key': this.apiKey }
        });

        return {
            address,
            chain,
            balance: this.parseBalance(response.data, chain),
            lastActivity: response.data.lastTx?.timestamp
        };
    }
}
```

#### **1.2 Update TrustWrapper Service**
```typescript
// Enhance trustWrapperService.ts
import { NOWNodesService } from './blockchain/nowNodesService';

export class TrustWrapperService extends Service {
    private nowNodes: NOWNodesService;

    async verifyTradingDecision(request: TradingDecisionRequest): Promise<VerificationResult> {
        // First try real blockchain verification
        if (request.context.txHash && request.context.chain) {
            try {
                const txVerification = await this.nowNodes.verifyTransaction(
                    request.context.txHash,
                    request.context.chain
                );

                if (txVerification.verified) {
                    // Use real data for verification
                    return this.createVerificationFromBlockchain(txVerification, request);
                }
            } catch (error) {
                console.warn('Blockchain verification failed, falling back to mock', error);
            }
        }

        // Fall back to mock if no blockchain data
        return this.createMockTradingVerification(request);
    }
}
```

### **Phase 2: Market Data Integration (Week 1-2)**

#### **2.1 CoinGecko Free Tier Integration**
```typescript
// File: src/services/market/coinGeckoService.ts
export class CoinGeckoService {
    private baseUrl = 'https://api.coingecko.com/api/v3';
    private cache = new Map<string, CachedData>();

    async getMarketData(symbol: string): Promise<MarketContext> {
        // Check cache first (respect rate limits)
        const cached = this.getFromCache(`market_${symbol}`);
        if (cached) return cached;

        const response = await axios.get(`${this.baseUrl}/coins/${symbol}`);
        const data = response.data;

        const marketContext: MarketContext = {
            volatility: this.calculateVolatility(data.market_data),
            volume24h: data.market_data.total_volume.usd,
            priceChange24h: data.market_data.price_change_percentage_24h / 100,
            marketSentiment: this.analyzeSentiment(data),
            liquidityScore: this.calculateLiquidity(data)
        };

        this.setCache(`market_${symbol}`, marketContext, 60); // 1 min cache
        return marketContext;
    }
}
```

#### **2.2 Aggregate Market Context**
```typescript
// Combine blockchain and market data
async function getEnhancedMarketContext(asset: string): Promise<EnhancedMarketContext> {
    const [marketData, onChainMetrics] = await Promise.all([
        coinGeckoService.getMarketData(asset),
        getOnChainMetrics(asset)
    ]);

    return {
        ...marketData,
        onChainVolume: onChainMetrics.volume,
        activeAddresses: onChainMetrics.activeAddresses,
        networkActivity: onChainMetrics.transactions24h
    };
}
```

### **Phase 3: TrustWrapper Backend MVP (Week 2-3)**

#### **3.1 Minimal Backend API**
```typescript
// File: backend/src/api/verificationController.ts
import { FastifyInstance } from 'fastify';
import { ZKProofGenerator } from '../services/zkProofGenerator';
import { XAIEngine } from '../services/xaiEngine';

export async function verificationRoutes(fastify: FastifyInstance) {
    // Trading decision verification
    fastify.post('/v1/verify/trading-decision', async (request, reply) => {
        const { decision, context } = request.body;

        // Generate simple ZK proof (MVP version)
        const zkProof = await zkProofGenerator.generateSimpleProof({
            action: decision.action,
            amount: decision.amount,
            timestamp: Date.now()
        });

        // Basic risk assessment
        const riskScore = await riskEngine.assessTradingRisk(decision, context);

        // Simple XAI explanation
        const explanation = await xaiEngine.explainDecision(decision, riskScore);

        return {
            verificationId: generateVerificationId(),
            status: riskScore < 0.7 ? 'approved' : 'flagged',
            confidence: 1 - riskScore,
            riskScore,
            zkProof,
            explanation,
            timestamp: Date.now()
        };
    });
}
```

#### **3.2 Deploy on Hivelocity VPS**
```bash
# Deploy TrustWrapper API on Tampa VPS (23.92.65.243)
ssh root@23.92.65.243

# Setup Node.js environment
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Clone and setup backend
git clone https://github.com/lamassu-labs/trustwrapper-backend
cd trustwrapper-backend
npm install
npm run build

# Setup PM2 for process management
npm install -g pm2
pm2 start dist/server.js --name trustwrapper-api
pm2 save
pm2 startup

# Configure nginx reverse proxy
sudo apt-get install nginx
# Configure nginx to proxy port 3000 to 443 with SSL
```

### **Phase 4: Production Optimization (Week 3-4)**

#### **4.1 Performance Enhancements**
```typescript
// Implement caching layer
import Redis from 'ioredis';

class VerificationCache {
    private redis: Redis;

    async getCachedVerification(key: string): Promise<VerificationResult | null> {
        const cached = await this.redis.get(key);
        return cached ? JSON.parse(cached) : null;
    }

    async cacheVerification(key: string, result: VerificationResult, ttl: number = 300) {
        await this.redis.setex(key, ttl, JSON.stringify(result));
    }
}
```

#### **4.2 Real ZK Proof Implementation**
```typescript
// Integrate with zkSNARK library
import { groth16 } from 'snarkjs';

class ZKProofGenerator {
    async generateTradingProof(tradingData: TradingDecision): Promise<ZKProof> {
        // Circuit: Prove trading decision meets risk criteria without revealing strategy
        const circuit = await this.loadCircuit('trading_verification');
        const witness = this.createWitness(tradingData);

        const { proof, publicSignals } = await groth16.fullProve(
            witness,
            circuit.wasm,
            circuit.zkey
        );

        return {
            proofId: generateProofId(),
            proofType: 'groth16',
            proofData: JSON.stringify(proof),
            publicInputs: publicSignals,
            timestamp: Date.now()
        };
    }
}
```

## 📋 **Implementation Checklist**

### **Week 1: Blockchain Integration**
- [ ] Setup NOWNodes service class
- [ ] Integrate transaction verification
- [ ] Add wallet balance checking
- [ ] Test with multiple blockchains
- [ ] Update Senpi plugin to use real data

### **Week 2: Market Data & Backend**
- [ ] Integrate CoinGecko API
- [ ] Build market context aggregator
- [ ] Deploy minimal TrustWrapper API
- [ ] Implement basic ZK proofs
- [ ] Create simple XAI explanations

### **Week 3: Production Features**
- [ ] Add Redis caching layer
- [ ] Implement real ZK circuits
- [ ] Enhance XAI with SHAP
- [ ] Add monitoring and analytics
- [ ] Performance optimization

### **Week 4: Testing & Launch**
- [ ] End-to-end integration testing
- [ ] Performance benchmarking
- [ ] Security audit
- [ ] Documentation updates
- [ ] Production deployment

## 💰 **Cost Analysis**

### **Infrastructure Costs (Monthly)**
- **Hivelocity VPS**: $14 (already have)
- **NOWNodes**: Included in existing plan
- **CoinGecko**: Free tier (50 calls/min)
- **Redis Cloud**: $5 (minimum tier)
- **Monitoring**: Free tier options
- **Total**: ~$19/month for MVP

### **Scaling Costs (When Needed)**
- **Premium APIs**: $500-2000/month
- **Additional VPS**: $50-200/month
- **CDN/Load Balancing**: $100-500/month
- **Database**: $100-1000/month

## 🚀 **Quick Start Commands**

```bash
# 1. Setup development environment
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs/src/integrations/senpi
npm install

# 2. Configure environment variables
export NOWNODES_API_KEY="your-existing-key"
export COINGECKO_API_KEY="not-needed-for-free"
export TRUSTWRAPPER_API_URL="http://23.92.65.243:3000"

# 3. Run integration tests with real data
npm run test:integration

# 4. Deploy to production
./scripts/deploy-production.sh
```

## 📊 **Success Metrics**

### **Technical Metrics**
- ✅ <1ms verification latency (current: mock only)
- ✅ 99.9% uptime SLA
- ✅ Support for 5+ blockchains
- ✅ 1000+ verifications/second capacity

### **Business Metrics**
- ✅ Working demo for Jason Goldberg
- ✅ 10+ beta users in first month
- ✅ $10K MRR within 90 days
- ✅ Partnership agreement signed

## 🎯 **Next Steps**

1. **Immediate (Today)**
   - Start NOWNodes integration
   - Setup development environment
   - Create integration test suite

2. **This Week**
   - Complete blockchain verification
   - Integrate market data
   - Deploy MVP backend

3. **Next Week**
   - Add production features
   - Performance optimization
   - Prepare partnership demo

4. **Month 1**
   - Launch beta program
   - Onboard first users
   - Iterate based on feedback

---

**Ready to Build**: We have everything needed to transform the mock implementation into a production-ready system. The NOWNodes integration provides immediate blockchain verification capabilities, while the phased approach allows us to deliver value quickly while building toward the full vision.

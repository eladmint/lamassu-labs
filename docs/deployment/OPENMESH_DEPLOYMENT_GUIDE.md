# 🌐 OpenMesh/OpenXAI Deployment Guide for TrustWrapper

**Version**: 1.0.0  
**Last Updated**: June 22, 2025  
**Compatibility**: TrustWrapper v1.0+ with OpenXAI Xnode

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Architecture](#architecture)
4. [OpenMesh Infrastructure Setup](#openmesh-infrastructure-setup)
5. [TrustWrapper Deployment](#trustwrapper-deployment)
6. [ICP Integration](#icp-integration)
7. [Monitoring & Scaling](#monitoring--scaling)
8. [Security Configuration](#security-configuration)
9. [Cost Analysis](#cost-analysis)
10. [Troubleshooting](#troubleshooting)

## 🎯 Overview

This guide provides comprehensive instructions for deploying TrustWrapper on OpenMesh's decentralized infrastructure using OpenXAI Xnodes. This deployment leverages the decentralized compute network for truly distributed AI verification.

### **Key Benefits of OpenMesh Deployment**
- **Decentralized Infrastructure**: No single point of failure
- **Native Web3 Integration**: Built for blockchain applications
- **OpenXAI Protocol**: Direct integration with decentralized AI
- **Cost Effective**: Pay-per-use model with OPEN tokens
- **Global Distribution**: Xnodes across multiple regions

### **Integration with Ziggurat Intelligence**
TrustWrapper's Ziggurat Intelligence platform is designed to work seamlessly with OpenXAI:
- **ICP Chain Fusion**: Cross-chain capabilities
- **Explainable AI**: SHAP, LIME, and gradient analysis
- **Decentralized Verification**: All proofs on-chain
- **Multi-Chain Support**: ICP, TON, Cardano, Aleo

## 📋 Prerequisites

### **OpenMesh Account Requirements**
- [ ] OpenMesh network account
- [ ] OPEN tokens for compute payment
- [ ] Xnode access credentials
- [ ] OpenXAI SDK installed

### **Development Requirements**
```bash
# Install OpenXAI CLI
curl -sSL https://openxai.network/install.sh | bash

# Configure OpenXAI
openxai configure
# Enter: API Key, Network (mainnet/testnet), Default Region

# Install ICP SDK for Chain Fusion
sh -ci "$(curl -fsSL https://internetcomputer.org/install.sh)"

# Install additional tools
npm install -g @openxai/cli @dfinity/agent
pip install openxai-sdk icp-python-client
```

### **TrustWrapper Requirements**
- Docker image compatible with Xnode runtime
- ICP canister addresses for Ziggurat Intelligence
- Multi-chain wallet configuration

## 🏗️ Architecture

### **Decentralized Deployment Architecture**
```
┌─────────────────────────────────────────────────────────────────────┐
│                          OpenMesh Network                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐           │
│  │   Xnode 1   │    │   Xnode 2   │    │   Xnode 3   │           │
│  │  (US East)  │    │  (EU West)  │    │(Asia Pacific)│           │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘           │
│         │                   │                   │                   │
│         └───────────────────┴───────────────────┘                  │
│                             │                                       │
│                    ┌────────┴────────┐                            │
│                    │  Load Balancer  │                            │
│                    │   (OpenMesh)    │                            │
│                    └────────┬────────┘                            │
│                             │                                       │
└─────────────────────────────┼───────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   TrustWrapper    │
                    │   API Gateway     │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────┴────────┐  ┌────────┴────────┐  ┌────────┴────────┐
│      ICP       │  │   OpenXAI       │  │   Multi-Chain  │
│   Canisters    │  │   Protocol      │  │    Bridges     │
└────────────────┘  └─────────────────┘  └─────────────────┘
```

### **Component Distribution**
- **Xnodes**: Run TrustWrapper verification services
- **ICP Canisters**: Store proofs and manage state
- **OpenXAI Protocol**: Handle AI inference requests
- **Chain Bridges**: Connect to TON, Cardano, Aleo

## 🚀 OpenMesh Infrastructure Setup

### **Step 1: Register Xnode**

```bash
# Register your compute node with OpenMesh
openxai node register \
  --name "trustwrapper-node-001" \
  --type "compute" \
  --capabilities "ai-inference,blockchain-verification" \
  --region "us-east" \
  --specs "cpu=4,memory=16GB,storage=100GB"

# Get node credentials
openxai node credentials trustwrapper-node-001 > node-credentials.json
```

### **Step 2: Configure Xnode Runtime**

```yaml
# xnode-config.yaml
apiVersion: v1
kind: XnodeConfiguration
metadata:
  name: trustwrapper-xnode
  namespace: production
spec:
  runtime:
    type: docker
    version: "20.10"
  
  capabilities:
    - ai-inference
    - explainable-ai
    - blockchain-verification
    - multi-chain-support
  
  resources:
    compute:
      cpu: 4
      memory: 16Gi
      gpu: optional
    storage:
      persistent: 100Gi
      ephemeral: 50Gi
  
  networking:
    ingress:
      enabled: true
      ports:
        - name: api
          port: 8000
          protocol: TCP
        - name: metrics
          port: 9090
          protocol: TCP
    
    p2p:
      enabled: true
      discovery: automatic
  
  blockchain:
    networks:
      - name: icp
        endpoint: "https://ic0.app"
        canister_ids:
          - "ziggurat-intelligence-main"
          - "trustwrapper-verifier"
      - name: ton
        endpoint: "https://toncenter.com/api/v2"
      - name: cardano
        endpoint: "https://cardano-mainnet.iohk.io"
      - name: aleo
        endpoint: "https://api.explorer.aleo.org/v1"
  
  security:
    encryption: true
    authentication: jwt
    tls:
      enabled: true
      autoGenerate: true
```

### **Step 3: Deploy Xnode Infrastructure**

```bash
# Deploy Xnode configuration
openxai deploy xnode \
  --config xnode-config.yaml \
  --credentials node-credentials.json \
  --network mainnet

# Verify deployment
openxai node status trustwrapper-node-001
```

## 🚀 TrustWrapper Deployment

### **Step 1: Prepare TrustWrapper for Xnode**

```dockerfile
# Dockerfile.xnode
FROM openxai/xnode-runtime:latest

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    build-essential

# Install TrustWrapper dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Install OpenXAI SDK
RUN pip3 install openxai-sdk icp-python-client

# Copy TrustWrapper application
COPY . .

# Configure for Xnode
ENV XNODE_ENABLED=true
ENV OPENXAI_NETWORK=mainnet
ENV TRUSTWRAPPER_MODE=decentralized

# Expose ports
EXPOSE 8000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run TrustWrapper
CMD ["python3", "-m", "uvicorn", "src.api.trustwrapper_api:app", \
     "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### **Step 2: Build and Push to OpenMesh Registry**

```bash
# Build Xnode-compatible image
docker build -f Dockerfile.xnode -t trustwrapper-xnode:latest .

# Tag for OpenMesh registry
docker tag trustwrapper-xnode:latest registry.openmesh.network/trustwrapper:latest

# Push to OpenMesh registry
docker push registry.openmesh.network/trustwrapper:latest
```

### **Step 3: Deploy TrustWrapper Application**

```yaml
# trustwrapper-deployment.yaml
apiVersion: apps/v1
kind: XnodeDeployment
metadata:
  name: trustwrapper
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: trustwrapper
  
  template:
    metadata:
      labels:
        app: trustwrapper
        network: openmesh
    
    spec:
      container:
        image: registry.openmesh.network/trustwrapper:latest
        
        env:
          - name: OPENXAI_API_KEY
            valueFrom:
              secretRef:
                name: openxai-credentials
                key: api-key
          
          - name: ICP_CANISTER_ID
            value: "ryjl3-tyaaa-aaaaa-aaaba-cai"
          
          - name: MULTI_CHAIN_CONFIG
            value: |
              {
                "ton": {"endpoint": "https://toncenter.com/api/v2"},
                "cardano": {"endpoint": "https://cardano-mainnet.iohk.io"},
                "aleo": {"endpoint": "https://api.explorer.aleo.org/v1"}
              }
        
        resources:
          requests:
            cpu: 2
            memory: 4Gi
          limits:
            cpu: 4
            memory: 8Gi
        
        probes:
          liveness:
            httpGet:
              path: /health
              port: 8000
            periodSeconds: 30
          
          readiness:
            httpGet:
              path: /ready
              port: 8000
            periodSeconds: 10
  
  networking:
    service:
      type: LoadBalancer
      ports:
        - port: 443
          targetPort: 8000
          protocol: TCP
      
      loadBalancer:
        algorithm: round-robin
        healthCheck:
          path: /health
          interval: 30s
    
    ingress:
      enabled: true
      domains:
        - trustwrapper.openmesh.network
        - api.trustwrapper.ai
      
      tls:
        enabled: true
        provider: letsencrypt
  
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 20
    metrics:
      - type: cpu
        target: 70
      - type: memory
        target: 80
      - type: custom
        name: verification_requests_per_second
        target: 100
```

```bash
# Deploy application
openxai deploy app \
  --manifest trustwrapper-deployment.yaml \
  --network mainnet \
  --wait

# Check deployment status
openxai app status trustwrapper
```

## 🔗 ICP Integration

### **Step 1: Deploy ICP Canisters**

```bash
# Navigate to ICP canister directory
cd icp-canisters/ziggurat-intelligence

# Deploy to ICP mainnet
dfx deploy --network ic --with-cycles 1000000000000

# Get canister IDs
dfx canister --network ic id ziggurat_intelligence
dfx canister --network ic id trustwrapper_verifier
```

### **Step 2: Configure Chain Fusion**

```typescript
// icp-integration.ts
import { Actor, HttpAgent } from '@dfinity/agent';
import { Principal } from '@dfinity/principal';

export class ICPIntegration {
  private agent: HttpAgent;
  private zigguratActor: any;
  
  constructor() {
    this.agent = new HttpAgent({
      host: 'https://ic0.app',
    });
  }
  
  async initialize() {
    // Import canister interfaces
    const { ziggurat_intelligence } = await import('./canisters/ziggurat_intelligence');
    
    // Create actor
    this.zigguratActor = Actor.createActor(ziggurat_intelligence, {
      agent: this.agent,
      canisterId: Principal.fromText('ryjl3-tyaaa-aaaaa-aaaba-cai'),
    });
  }
  
  async storeVerificationProof(proof: VerificationProof) {
    return await this.zigguratActor.store_proof({
      user: proof.userId,
      query_hash: proof.queryHash,
      trust_score: proof.trustScore,
      explanation: proof.explanation,
      timestamp: BigInt(Date.now()),
      chain_proofs: {
        ton: proof.tonProof,
        cardano: proof.cardanoProof,
        aleo: proof.aleoProof,
      },
    });
  }
  
  async getExplainableAI(query: string, response: string) {
    const result = await this.zigguratActor.explain_ai_decision({
      query,
      response,
      methods: ['shap', 'lime', 'gradient'],
    });
    
    return {
      shap: result.shap_values,
      lime: result.lime_explanation,
      gradient: result.gradient_analysis,
      confidence: result.confidence_score,
    };
  }
}
```

### **Step 3: Enable OpenXAI Protocol**

```python
# openxai_integration.py
from openxai import OpenXAIClient, XnodeConfig
from typing import Dict, Any
import asyncio

class OpenXAIIntegration:
    def __init__(self):
        self.client = OpenXAIClient(
            api_key=os.environ.get("OPENXAI_API_KEY"),
            network="mainnet"
        )
        
        self.xnode_config = XnodeConfig(
            node_id="trustwrapper-node-001",
            capabilities=["explainable-ai", "blockchain-verification"],
            region="us-east"
        )
    
    async def decentralized_inference(self, query: str, response: str) -> Dict[str, Any]:
        """Run AI inference on OpenXAI network"""
        
        # Request inference from network
        result = await self.client.inference.create(
            model="trustwrapper-verifier",
            inputs={
                "query": query,
                "response": response,
                "verification_type": "explainable"
            },
            xnode_preferences={
                "min_nodes": 3,  # Consensus from 3 nodes
                "regions": ["us-east", "eu-west", "asia-pacific"],
                "capabilities": ["explainable-ai"]
            }
        )
        
        # Aggregate results from multiple nodes
        consensus_score = self._calculate_consensus(result.node_results)
        
        return {
            "verification_id": result.id,
            "consensus_score": consensus_score,
            "explanations": result.explanations,
            "node_count": len(result.node_results),
            "blockchain_proofs": result.proofs
        }
    
    def _calculate_consensus(self, node_results: list) -> float:
        """Calculate consensus score from multiple Xnode results"""
        scores = [r.trust_score for r in node_results]
        return sum(scores) / len(scores) if scores else 0.0
    
    async def monitor_xnode_health(self) -> Dict[str, Any]:
        """Monitor Xnode health and performance"""
        
        health = await self.client.nodes.health(self.xnode_config.node_id)
        
        return {
            "status": health.status,
            "uptime": health.uptime_seconds,
            "requests_processed": health.metrics.total_requests,
            "average_latency": health.metrics.avg_latency_ms,
            "resource_usage": {
                "cpu": health.resources.cpu_percent,
                "memory": health.resources.memory_percent,
                "storage": health.resources.storage_percent
            }
        }
```

## 📊 Monitoring & Scaling

### **OpenMesh Monitoring Dashboard**

```yaml
# monitoring-config.yaml
apiVersion: v1
kind: MonitoringConfiguration
metadata:
  name: trustwrapper-monitoring
spec:
  metrics:
    enabled: true
    endpoints:
      - name: xnode-metrics
        path: /metrics
        port: 9090
        interval: 30s
    
    custom_metrics:
      - name: verification_requests
        type: counter
        labels: ["status", "chain", "model"]
      
      - name: consensus_score
        type: histogram
        buckets: [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
      
      - name: xnode_latency
        type: summary
        quantiles: [0.5, 0.9, 0.95, 0.99]
  
  logging:
    enabled: true
    level: info
    outputs:
      - type: openmesh-logger
        format: json
      - type: file
        path: /var/log/trustwrapper/
    
    retention:
      days: 30
      max_size: 10GB
  
  alerting:
    enabled: true
    rules:
      - name: high-error-rate
        condition: "error_rate > 0.05"
        duration: 5m
        severity: warning
      
      - name: xnode-down
        condition: "up == 0"
        duration: 1m
        severity: critical
      
      - name: consensus-failure
        condition: "consensus_score < 0.7"
        duration: 3m
        severity: warning
```

### **Auto-scaling Configuration**

```python
# autoscaling.py
from openxai import AutoScaler

class TrustWrapperAutoScaler:
    def __init__(self):
        self.scaler = AutoScaler(
            app_name="trustwrapper",
            network="mainnet"
        )
    
    def configure_scaling_rules(self):
        # CPU-based scaling
        self.scaler.add_rule(
            name="cpu-scale",
            metric="cpu_utilization",
            target=70,
            scale_up_threshold=80,
            scale_down_threshold=50,
            cooldown=300
        )
        
        # Request-based scaling
        self.scaler.add_rule(
            name="request-scale",
            metric="requests_per_second",
            target=100,
            scale_up_threshold=150,
            scale_down_threshold=50,
            cooldown=180
        )
        
        # Custom metric scaling
        self.scaler.add_rule(
            name="verification-queue",
            metric="queue_length",
            target=50,
            scale_up_threshold=100,
            scale_down_threshold=10,
            cooldown=120
        )
        
        # Geographic distribution
        self.scaler.set_distribution_policy({
            "strategy": "geo-balanced",
            "regions": {
                "us-east": {"min": 1, "max": 5},
                "eu-west": {"min": 1, "max": 5},
                "asia-pacific": {"min": 1, "max": 5}
            }
        })
```

## 🔒 Security Configuration

### **Xnode Security**

```yaml
# security-policy.yaml
apiVersion: security/v1
kind: SecurityPolicy
metadata:
  name: trustwrapper-security
spec:
  encryption:
    at_rest: true
    in_transit: true
    algorithm: AES-256-GCM
  
  authentication:
    type: jwt
    providers:
      - openxai-auth
      - custom-jwt
    
    token_validation:
      audience: "trustwrapper-api"
      issuer: "https://auth.trustwrapper.ai"
      expiry: 3600
  
  authorization:
    rbac:
      enabled: true
      roles:
        - name: user
          permissions: ["read", "verify"]
        - name: premium
          permissions: ["read", "verify", "explain", "batch"]
        - name: admin
          permissions: ["*"]
  
  network_policies:
    ingress:
      - from: openxai-network
        ports: [8000, 9090]
      - from: public-internet
        ports: [443]
    
    egress:
      - to: icp-network
        ports: [443]
      - to: blockchain-networks
        ports: [443, 8545, 30303]
  
  compliance:
    standards: ["SOC2", "ISO27001"]
    audit_logging: true
    data_retention: 90
```

### **Multi-signature Deployment**

```bash
# Create multi-sig deployment policy
openxai security create-policy \
  --name "trustwrapper-deployment" \
  --type "multi-signature" \
  --signers "alice@trustwrapper.ai,bob@trustwrapper.ai,charlie@trustwrapper.ai" \
  --threshold 2 \
  --actions "deploy,scale,modify"

# Deploy with multi-sig
openxai deploy app \
  --manifest trustwrapper-deployment.yaml \
  --policy trustwrapper-deployment \
  --request-signatures
```

## 💰 Cost Analysis

### **OpenMesh/OpenXAI Pricing Model**

| Resource | Unit | Price (OPEN tokens) | Monthly Estimate |
|:---------|:-----|:-------------------|:-----------------|
| **Compute** | vCPU-hour | 0.1 OPEN | ~72 OPEN |
| **Memory** | GB-hour | 0.05 OPEN | ~36 OPEN |
| **Storage** | GB-month | 0.5 OPEN | ~50 OPEN |
| **Network** | GB transfer | 0.01 OPEN | ~10 OPEN |
| **AI Inference** | 1k requests | 1 OPEN | ~100 OPEN |
| **Total** | | | ~268 OPEN/month |

### **Cost Optimization**

```python
# cost_optimizer.py
class OpenMeshCostOptimizer:
    def __init__(self):
        self.usage_tracker = UsageTracker()
        self.token_price = self.get_current_token_price()
    
    def optimize_deployment(self):
        optimizations = []
        
        # Geographic arbitrage
        regional_costs = self.get_regional_costs()
        cheapest_region = min(regional_costs, key=regional_costs.get)
        optimizations.append({
            "type": "regional",
            "action": f"Move non-latency-sensitive workloads to {cheapest_region}",
            "savings": "~20%"
        })
        
        # Off-peak scheduling
        optimizations.append({
            "type": "scheduling",
            "action": "Schedule batch jobs during off-peak hours",
            "savings": "~15%"
        })
        
        # Resource right-sizing
        current_usage = self.usage_tracker.get_average_usage()
        if current_usage["cpu"] < 50:
            optimizations.append({
                "type": "right-sizing",
                "action": "Reduce CPU allocation by 25%",
                "savings": "~18 OPEN/month"
            })
        
        return optimizations
```

## 🔧 Troubleshooting

### **Common Issues**

#### **1. Xnode Connection Issues**
```bash
# Check Xnode status
openxai node status trustwrapper-node-001

# Test connectivity
openxai network test --node trustwrapper-node-001

# View logs
openxai logs --node trustwrapper-node-001 --tail 100
```

#### **2. ICP Canister Issues**
```bash
# Check canister status
dfx canister --network ic status ziggurat_intelligence

# View canister logs
dfx canister --network ic logs ziggurat_intelligence

# Check cycles balance
dfx canister --network ic balance ziggurat_intelligence
```

#### **3. Multi-Chain Bridge Issues**
```python
# Diagnostic script
async def diagnose_chain_bridges():
    bridges = {
        "ton": TONBridge(),
        "cardano": CardanoBridge(),
        "aleo": AleoBridge()
    }
    
    for chain, bridge in bridges.items():
        try:
            status = await bridge.health_check()
            print(f"{chain}: {status}")
        except Exception as e:
            print(f"{chain}: ERROR - {str(e)}")
```

#### **4. OpenXAI Protocol Issues**
```bash
# Check OpenXAI network status
openxai network status

# Test inference endpoint
openxai test inference \
  --model trustwrapper-verifier \
  --input '{"query": "test", "response": "test response"}'

# View protocol metrics
openxai metrics --protocol --last 1h
```

### **Debugging Tools**

```bash
# OpenMesh diagnostic tool
openxai diagnose \
  --app trustwrapper \
  --comprehensive \
  --output diagnostic-report.json

# Performance profiling
openxai profile \
  --app trustwrapper \
  --duration 5m \
  --type cpu,memory,network

# Network trace
openxai trace \
  --request-id "12345-abcde" \
  --show-hops \
  --show-latency
```

## 📚 Additional Resources

### **OpenMesh/OpenXAI Documentation**
- [OpenMesh Network Docs](https://docs.openmesh.network)
- [OpenXAI Protocol Specification](https://openxai.network/docs)
- [Xnode Operator Guide](https://docs.openmesh.network/xnode)
- [OPEN Token Economics](https://openmesh.network/tokenomics)

### **ICP Integration Resources**
- [Internet Computer SDK](https://internetcomputer.org/docs)
- [Chain Fusion Documentation](https://internetcomputer.org/chainfusion)
- [Motoko Programming](https://internetcomputer.org/docs/current/motoko/main/motoko)

### **TrustWrapper Resources**
- [API Reference](/docs/api/TRUSTWRAPPER_API_REFERENCE.md)
- [Architecture Overview](/docs/architecture/TECHNICAL_ARCHITECTURE.md)
- [Ziggurat Intelligence](/agent_forge/agent_forge_public/ziggurat/README.md)

### **Support**
- **OpenMesh Support**: support@openmesh.network
- **TrustWrapper Support**: support@trustwrapper.ai
- **Community**: [Discord](https://discord.gg/openmesh)

---

**Next Steps**: After deployment, configure cross-chain bridges for TON, Cardano, and Aleo integration, and set up the Ziggurat Intelligence dashboard for monitoring explainable AI performance.
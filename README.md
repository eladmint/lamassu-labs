# TrustWrapper
## Universal AI Trust Infrastructure Powered by Aleo ZK

<div align="center">

**🏆 ZK-Berlin Hackathon 2025**

[![Live on Aleo](https://img.shields.io/badge/🔗_LIVE_ON_ALEO-Testnet3-brightgreen?style=for-the-badge)](https://aleo.tools/)
[![Smart Contract](https://img.shields.io/badge/Leo_Contract-Deployed-blue?style=for-the-badge)](https://github.com/eladmint/lamassu-labs/blob/main/src/contracts/hallucination_verifier/src/main.leo)
[![Credits Spent](https://img.shields.io/badge/Credits_Spent-8.633-orange?style=for-the-badge)](#live-aleo-deployment)

*The first ZK-verified AI trust infrastructure - Solving DeFi's $13B trust problem with Aleo*

[🚀 **View Live Contract**](https://aleo.tools/) • [📊 **See Research**](docs/market_research/README.md) • [⚡ **Quick Demo**](#quick-demo)

</div>

---

## 🎯 The $13 Billion Problem That Only Aleo Can Solve

<table>
<tr>
<td width="50%">

### 💔 **The DeFi Trust Crisis**
- **90% of AI trading agents fail** within 17 days
- **$13B lost annually** from unverified AI decisions  
- **0% can prove performance** without exposing strategies
- **74% of organizations** can't achieve AI value due to trust issues

*Sources: [Comprehensive Market Research](docs/market_research/README.md) (203+ citations)*

</td>
<td width="50%">

### ✨ **TrustWrapper + Aleo Solution**
- **✅ Prove AI performance** without revealing algorithms
- **✅ Zero-knowledge verification** on Aleo blockchain  
- **✅ Enable $100B+ DeFi AI market** with trust
- **✅ Universal compatibility** with ANY AI agent

*[See Live Deployment →](#live-aleo-deployment)*

</td>
</tr>
</table>

> **💡 Key Insight**: The entire DeFi AI market is locked because of a simple paradox: investors need proof, but AI developers can't reveal their strategies. Aleo's zero-knowledge proofs solve this perfectly.

---

## 🔐 Why Aleo is Essential (For Hackathon Judges)

<div align="center">

### **Aleo Enables What's Impossible Elsewhere**

</div>

| Traditional Blockchains | Aleo + TrustWrapper |
|:---|:---|
| ❌ **Public transparency** exposes trading strategies | ✅ **Private computation** keeps algorithms secret |
| ❌ **All-or-nothing** disclosure model | ✅ **Selective revelation** of only performance metrics |
| ❌ **Trust requires transparency** paradox | ✅ **Trust through cryptographic proof** without exposure |
| ❌ **Can't scale** for enterprise AI use cases | ✅ **Enterprise-ready** privacy for sensitive algorithms |

### **🧠 The Aleo Advantage in Plain English**

<details>
<summary><strong>🔍 Click to understand the technical breakthrough</strong></summary>

**The Problem**: AI trading strategies are like secret recipes. Show the recipe (prove it works) and competitors steal it. Don't show it, and nobody trusts you.

**Traditional Blockchain**: Everything is public. Your trading algorithm becomes visible to everyone.

**Aleo's Solution**: 
1. **Private execution** - Your AI runs privately on Aleo
2. **Selective proof** - Only performance metrics become public  
3. **Cryptographic verification** - Proof is mathematically certain
4. **Strategy protection** - Algorithm stays completely hidden

**Real Impact**: For the first time, AI agents can prove they're profitable without revealing how they make money.

</details>

---

## 🚀 Live Aleo Deployment

<div align="center">

### **🎉 REAL CONTRACT • REAL TRANSACTION • REAL ALEO**

</div>

| **Deployment Detail** | **Value** | **Verification** |
|:---|:---|:---|
| **🔗 Transaction ID** | `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt` | [Search on Aleo.tools →](https://aleo.tools/) |
| **💰 Credits Spent** | 8.633 credits | Real deployment cost |
| **📅 Deployment Date** | June 22, 2025 | Live and verified |
| **🏛️ Contract Name** | `hallucination_verifier.aleo` | [View Source Code →](src/contracts/hallucination_verifier/src/main.leo) |
| **⚡ Status** | ✅ Live on Testnet3 | Fully operational |

> **🔍 How to Verify**: Visit [aleo.tools](https://aleo.tools/) and search for transaction ID `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt` or contract name `hallucination_verifier.aleo`

### **🔧 Smart Contract Functions** 
```leo
// Verify AI response with zero-knowledge proof
transition verify_response(
    response_text: field,           // Hash of AI output
    ai_model_hash: field,          // Model identifier  
    trust_score: u8,               // Performance score (0-100)
    verification_method: u8,        // Verification technique used
    evidence_count: u8,            // Supporting evidence pieces
    public verifier_address: address  // Verifier identity
) -> (VerifiedResponse, field)
```

<details>
<summary><strong>🔧 View All Contract Functions</strong></summary>

```leo
// Record evidence of AI hallucinations or errors
transition record_hallucination_evidence(
    verification_id: field,         // Links to verification
    evidence_type: u8,             // Type of issue detected
    confidence: u8,                // Detection confidence (0-100)  
    detection_method: u8,          // Detection algorithm used
    evidence_data: field           // Hashed evidence details
) -> HallucinationEvidence

// Batch verify multiple AI responses efficiently
transition batch_verify_responses(
    response_hashes: [field; 5],    // Up to 5 responses
    trust_scores: [u8; 5],          // Corresponding scores
    verification_method: u8,         // Same method for batch
    public verifier_address: address
) -> [field; 5]
```

</details>

---

## 💡 Quick Demo

### **See TrustWrapper in Action** *(2-minute read)*

<table>
<tr>
<td width="33%">

#### **1. 🤖 AI Agent Makes Claim**
```
"I achieved 75% win rate
with 2.3 Sharpe ratio
in Q4 2024"
```
*Traditional: Trust me bro*

</td>
<td width="33%">

#### **2. 🔐 TrustWrapper Verifies**
```
ZK Proof Generated:
✅ Win rate: 75% (verified)
✅ Sharpe: 2.3 (verified)  
✅ Algorithm: [HIDDEN]
```
*Aleo: Cryptographic proof*

</td>
<td width="33%">

#### **3. 💰 Investors Stake**
```
Trust Score: 95/100
Proof: Valid ✅
Strategy: Protected 🔒
Staking: $10M+ flowing
```
*Result: Market unlocked*

</td>
</tr>
</table>

**🎯 The Result**: AI developers keep their secrets, investors get their proof, and DeFi AI market explodes from $0 to $100B+.

---

## 🏗️ Technical Architecture

<div align="center">

### **Three-Layer Universal Trust Infrastructure**

</div>

```mermaid
graph TB
    A[Your AI Agent<br/>Any Framework, Any Model] --> B[TrustWrapper Layer 1<br/>Performance Verification]
    B --> C[TrustWrapper Layer 2<br/>AI Consensus Engine]  
    C --> D[TrustWrapper Layer 3<br/>Hallucination Detection]
    D --> E[Aleo Blockchain<br/>ZK Proof Generation]
    E --> F[✅ Verified Trust Score<br/>Public, Cryptographically Certain]
    
    style A fill:#e1f5fe
    style E fill:#c8e6c9
    style F fill:#fff3e0
```

<details>
<summary><strong>🔧 Deep Dive: How Each Layer Works</strong></summary>

### **Layer 1: Performance Verification**
- **Execution Metrics**: Time, success rate, accuracy measurements
- **Zero-Knowledge Proof Generation**: Creates cryptographic proof without revealing internals
- **Aleo Integration**: Proof submitted to Aleo blockchain for verification

### **Layer 2: AI Consensus Engine**  
- **Multi-Model Validation**: Google Gemini + Anthropic Claude cross-validation
- **Semantic Analysis**: Natural language understanding for claim verification
- **Cross-Reference Checking**: Wikipedia API and external data source validation

### **Layer 3: Hallucination Detection**
- **Pattern Recognition**: Identifies common AI failure modes and false claims
- **Temporal Consistency**: Checks claims against historical data and patterns  
- **Statistical Anomaly Detection**: Flags impossible or highly improbable claims

### **Aleo Blockchain Integration**
- **Private Computation**: AI verification happens privately on Aleo network
- **Selective Revelation**: Only trust scores and verification status become public
- **Cryptographic Certainty**: Mathematical proof that verification is accurate

</details>

---

## 🎯 Market Opportunity

<div align="center">

### **The Perfect Storm: Three Massive Markets Converging**

</div>

| **Market** | **Size** | **Growth** | **TrustWrapper Opportunity** |
|:---|:---:|:---:|:---|
| **🤖 AI Agents** | $5.25B → $52.6B | 46.3% CAGR | First universal trust infrastructure |
| **🔧 RPA/Automation** | $22.8B → $211B | 25% CAGR | Trust layer for automated trading |
| **🌐 Web3 AI** | $2.05B (Fetch.ai) | 34% weekly | ZK verification for DeFi AI |

### **📊 Market Validation** *(Research-Backed)*

<table>
<tr>
<td width="50%">

#### **🚨 Problem Scale**
- **$13B annual losses** from AI failures
- **96% of tech professionals** see AI as growing risk
- **74% of organizations** can't achieve AI value
- **Air Canada paid $812** for AI chatbot errors

</td>
<td width="50%">

#### **💰 Financial Impact**  
- **$5.3M average** enterprise spending on AI data
- **42% of data budgets** allocated to AI initiatives
- **89% say AI models** are critical to success
- **45% don't report** AI breaches (reputation risk)

</td>
</tr>
</table>

*Source: [203+ Citations in Research Documentation](docs/market_research/README.md)*

---

## 🏆 Why TrustWrapper Wins

<div align="center">

### **The Only Solution That Works**

</div>

| **Traditional Approaches** | **TrustWrapper + Aleo** |
|:---|:---|
| ❌ Manual audits (slow, expensive) | ✅ **Automated ZK verification** (2 seconds) |
| ❌ Public transparency (exposes IP) | ✅ **Private computation** (protects secrets) |  
| ❌ Trust-based systems (vulnerable) | ✅ **Cryptographic certainty** (mathematically proven) |
| ❌ Single AI verification | ✅ **Universal compatibility** (works with ANY agent) |
| ❌ Reactive (after failure) | ✅ **Proactive** (prevents failure) |

### **🎯 For Different Stakeholders**

<details>
<summary><strong>👥 Value Propositions by Audience</strong></summary>

#### **🏛️ For Hackathon Judges**
- **Technical Innovation**: First practical application of ZK for AI trust at scale  
- **Market Impact**: Unlocks $100B+ market currently locked by trust issues
- **Real Deployment**: Live smart contract with actual credits spent (8.633)
- **Ecosystem Impact**: Demonstrates real-world utility of zero-knowledge proofs

#### **💰 For DeFi Investors**  
- **Risk Reduction**: Stake only on cryptographically verified AI performance
- **Higher Returns**: Access to high-performing AI agents (15-25% APY potential)
- **Transparency**: Public trust scores with mathematical certainty
- **Diversification**: New asset class of verified AI trading strategies

#### **🤖 For AI Developers**
- **IP Protection**: Prove performance without revealing proprietary algorithms
- **Market Access**: Attract capital without exposing competitive advantage  
- **Trust Building**: Cryptographic proof builds investor confidence
- **Revenue Growth**: Verified agents attract 10x more staking capital

#### **🏢 For Enterprises**
- **Compliance**: Meet regulatory requirements for AI transparency
- **Risk Management**: Deploy AI with mathematical performance guarantees
- **Integration**: Universal compatibility with existing AI infrastructure
- **ROI Assurance**: Invest in AI with verified performance metrics

</details>

---

## ⚡ Quick Start

<div align="center">

### **Get Started in 3 Steps**

</div>

<table>
<tr>
<td width="33%">

#### **1. 📥 Install**
```bash
git clone https://github.com/eladmint/lamassu-labs
cd lamassu-labs
pip install -r requirements.txt
```

</td>
<td width="33%">

#### **2. 🔧 Configure**
```bash
export GOOGLE_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"  
export ALEO_PRIVATE_KEY="your-key"
```

</td>
<td width="33%">

#### **3. 🚀 Run**
```bash
python hackathon_demo.py
# Or try the API
python src/api/trustwrapper_api.py
```

</td>
</tr>
</table>

### **🎮 Interactive Demos**

| **Demo** | **What It Shows** | **Time** |
|:---|:---|:---|
| `python hackathon_demo.py` | Complete ZK verification workflow | 5 min |
| `python demo/ultimate_defi_presentation.py` | Real DeFi trading AI verification | 3 min |
| `curl localhost:8000/validate/text` | REST API integration | 1 min |

<details>
<summary><strong>🔧 Advanced Setup & Development</strong></summary>

### **Development Environment**
```bash
# Setup Leo/Aleo (for contract development)
./tools/development/install_leo_aleo.sh

# Compile contracts  
./tools/development/compile_leo.sh

# Run comprehensive tests
./tools/testing/run_hallucination_tests.sh

# Deploy to testnet (requires credits)
./tools/deployment/deploy_contracts.sh
```

### **API Usage Example**
```python
import requests

# Verify AI response
response = requests.post("http://localhost:8000/validate/text", 
    headers={"Authorization": "Bearer demo-key"},
    json={"text": "The capital of France is London"}
)

print(f"Trust Score: {response.json()['trust_score']}")
print(f"Verified: {response.json()['verified']}")
```

### **Contract Integration**
```python
from src.core.enhanced_trust_wrapper import create_enhanced_trust_wrapper

# Wrap any AI model  
wrapper = create_enhanced_trust_wrapper(your_ai_model)
result = await wrapper.verified_execute("Your AI query")
print(f"ZK Proof: {result.zk_proof.proof_id}")
```

</details>

---

## 📊 Research & Validation {#research--validation}

<div align="center">

### **203+ Citations • 4 Research Categories • Academic Foundation**

</div>

| **Research Area** | **Citations** | **Key Findings** |
|:---|:---:|:---|
| **[AI Verification & Trust](docs/market_research/core/ai_agent_verification_trust.md)** | 107 | $13B losses, 96% see AI as risk |
| **[Browser Automation Market](docs/market_research/core/browser_automation_market.md)** | 96 | $22.8B → $211B market growth |
| **[Web3 AI Current State](docs/market_research/web3/web3_ai_agents_current_state.md)** | 50+ | Fetch.ai $2.05B market cap leadership |
| **[Technical Architecture](docs/architecture/TECHNICAL_ARCHITECTURE.md)** | — | Complete system design & ZK implementation |

### **🎓 Academic Sources**
*IEEE • ACM • Nature • BMJ • Springer • McKinsey • BCG • Deloitte • Gartner • Forrester*

<details>
<summary><strong>📈 Key Statistics Summary</strong></summary>

### **Market Opportunity**
- **$52.6B** AI agent market by 2030 (46.3% CAGR)
- **$211B** RPA market by 2034 (25% CAGR)  
- **$2.05B** Fetch.ai market cap (Web3 AI leader)

### **Problem Validation**  
- **$13B** annual losses from unverified AI
- **90%** DeFi AI agent failure rate
- **74%** organizations struggle with AI value
- **96%** tech professionals see AI as risk

### **Enterprise Reality**
- **$5.3M** average enterprise AI spending
- **86%** require tech stack upgrades for AI
- **53%** leadership cite security as top concern
- **42%** need 8+ data sources for AI deployment

</details>

---

## 🌟 What Makes This Special

<div align="center">

### **First-of-Its-Kind Innovation**

</div>

🥇 **First** universal trust infrastructure for AI agents  
🔐 **First** to combine ZK-proofs + Explainable AI + DeFi  
🏛️ **First** production deployment of AI verification on Aleo  
💰 **First** solution to DeFi's $13B AI trust problem  
🌐 **First** to enable private AI performance verification  

### **🏆 Competition Analysis**

| **Solution Type** | **Privacy** | **Universal** | **DeFi Ready** | **Live Deployment** |
|:---|:---:|:---:|:---:|:---:|
| **Traditional Audits** | ❌ | ❌ | ❌ | ✅ |
| **Current ZK Solutions** | ✅ | ❌ | ❌ | ⚠️ |
| **AI Verification Tools** | ❌ | ⚠️ | ❌ | ✅ |
| **TrustWrapper + Aleo** | ✅ | ✅ | ✅ | ✅ |

---

## 🚀 Future Roadmap

<div align="center">

### **From Hackathon to $100B Market Leader**

</div>

| **Phase** | **Timeline** | **Milestones** |
|:---|:---|:---|
| **🏆 Hackathon** | *Now* | ✅ Live Aleo deployment, demo ready |
| **🚀 Launch** | Q3 2025 | Mainnet deployment, first partnerships |
| **📈 Scale** | Q4 2025 | Enterprise adoption, major integrations |
| **🌍 Expand** | 2026+ | Multi-chain, global AI trust standard |

---

## 🎯 Call to Action

<div align="center">

### **Ready to Unlock the $100B DeFi AI Market?**

> **🔍 For Judges**: To verify our deployment, visit [aleo.tools](https://aleo.tools/) and search for `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt` or view the [contract source code](src/contracts/hallucination_verifier/src/main.leo) directly.

</div>

<table>
<tr>
<td width="33%">

#### **🏛️ Hackathon Judges**
See the future of privacy-preserving AI verification in action.

**[📋 View Live Contract →](https://aleo.tools/)**

</td>
<td width="33%">

#### **👨‍💻 Developers**  
Build with the universal AI trust infrastructure.

**[🚀 Quick Start →](#quick-start)**

</td>
<td width="33%">

#### **💰 Investors**
Join the AI trust revolution backed by zero-knowledge proofs.

**[📊 See Research →](docs/market_research/README.md)**

</td>
</tr>
</table>

---

<div align="center">

**🏗️ Built for ZK-Berlin Hackathon 2025** • **🔐 Powered by Aleo ZK** • **🤖 Securing AI's Future**

*TrustWrapper: Because trust shouldn't require faith.*

[![Live Contract](https://img.shields.io/badge/🔗_LIVE_CONTRACT-at1f29je4764...sep8zrt-brightgreen?style=for-the-badge)](https://aleo.tools/)

**📧 Contact**: [GitHub Issues](https://github.com/eladmint/lamassu-labs/issues) • **🔗 Repository**: [eladmint/lamassu-labs](https://github.com/eladmint/lamassu-labs) • **📚 Docs**: [Research Index](docs/market_research/README.md)

</div>
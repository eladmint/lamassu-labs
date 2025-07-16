# 🏛️ Lamassu Labs - Universal AI Trust Infrastructure

**TrustWrapper v3.0: Ancient Wisdom for Modern Intelligence**

## 🌟 What is Lamassu Labs?

**Lamassu Labs** is the verification infrastructure division of **Nuru AI**, providing universal AI trust and verification across 10+ blockchain networks. Named after the ancient Mesopotamian protective deities, Lamassu Labs serves as the guardian layer ensuring AI agents operate safely and verifiably in Web3 environments.

### Company Structure
```
🏢 Nuru AI (Parent Company)
├── 🔬 Ziggurat Intelligence (Layer 1: Research-to-Earn)
├── 🤖 Agent Forge (Layer 2: AI Agent Framework)  
└── 🏛️ Lamassu Labs (Layer 3: Verification Infrastructure)
    └── 🛡️ TrustWrapper v3.0 (Core Product)
```

## 🛡️ What is TrustWrapper?

**TrustWrapper** is Lamassu Labs' flagship product - a comprehensive AI verification platform that provides:

- **🔍 Real-time AI Monitoring**: Detect hallucinations, bias, and unsafe outputs instantly
- **🛡️ Oracle Protection**: Advanced manipulation detection for DeFi protocols
- **🔐 Zero-Knowledge Verification**: Cryptographic proof of AI behavior without exposing algorithms
- **⚡ Universal Integration**: 3-line integration with any AI system (Eliza, LangChain, custom agents)
- **📊 Enterprise Compliance**: SOC2, GDPR, HIPAA, and MiCA regulatory frameworks

### 🎯 Core Value Proposition
*"The only AI monitoring solution that prevents costly business incidents through real-time violation detection while protecting proprietary algorithms with zero-knowledge proofs."*

## 🚀 Getting Started

### 🆓 **Free Tier - Try TrustWrapper Now**
```bash
npm install @trustwrapper/public
# or
pip install trustwrapper-public
```

```typescript
// 3-line integration - detect AI hallucinations instantly
import { TrustWrapperBasic } from '@trustwrapper/public';
const trustWrapper = new TrustWrapperBasic();
const result = await trustWrapper.verifyBasic({ content: "AI output to verify" });
```

### 📚 **Documentation Paths**

#### **For First-Time Users** 🌱
1. **[🚀 Quick Start Guide](developer/getting-started/QUICK_START.md)** - Get running in 2 minutes
2. **[📝 API Quick Reference](developer/reference/API_QUICK_REFERENCE.md)** - Simple code examples
3. **[🎮 Interactive Demos](../src/examples/)** - Try it yourself
4. **[📊 Live Dashboard](https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io)** - Monitor in real-time

#### **For Developers** 👨‍💻
1. **[🔧 Technical Architecture](developer/architecture/TECHNICAL_ARCHITECTURE.md)** - How it all works
2. **[📈 Migration Guide](developer/getting-started/MIGRATION_GUIDE.md)** - Level up your agents
3. **[🔗 Integration Patterns](developer/guides/integrations/)** - Framework integrations
4. **[🧪 Testing Guide](developer/guides/HOW_VERIFICATION_WORKS.md)** - Verify your implementation

#### **For Decision Makers** 👔
1. **[📄 Executive Overview](business/open-source-philosophy.md)** - Business value proposition
2. **[💰 Pricing & Tiers](#pricing-tiers)** - Choose the right plan
3. **[🏢 Enterprise Features](#enterprise-features)** - Advanced capabilities
4. **[🤝 Partnership Opportunities](partnerships/)** - Integration ecosystem

## 💰 **Pricing Tiers**

### 🆓 **Community (Free Forever)**
- ✅ 1,000 verifications/month
- ✅ Basic scam detection
- ✅ Framework integrations (Eliza, LangChain)
- ✅ Community support
- ✅ MIT License - Use anywhere

### 🚀 **Professional ($299-999/month)**
- ✅ 10K-100K verifications/month
- ✅ Advanced ML algorithms via API
- ✅ Oracle manipulation detection
- ✅ Email support with SLA
- ✅ Enhanced analytics

### 🏢 **Enterprise ($25K+/year)**
- ✅ Unlimited verifications
- ✅ Full algorithm access + custom training
- ✅ On-premise deployment
- ✅ Custom compliance packages
- ✅ Dedicated support team
- ✅ Zero-knowledge privacy guarantees

## 🏢 **Enterprise Features**

### 🛡️ **Advanced Security**
- **Oracle Manipulation Detection**: Real-time monitoring across 15+ DeFi protocols
- **Zero-Knowledge Verification**: Cryptographic proof without algorithm exposure
- **Enterprise Compliance**: SOC2, GDPR, HIPAA, MiCA regulatory frameworks
- **Custom Model Training**: Train verification models on your specific data

### ⚡ **Performance & Scale**
- **Sub-10ms Latency**: Ultra-fast verification for high-frequency trading
- **Multi-Chain Support**: Ethereum, Polygon, Solana, Cardano, ICP, and more
- **Auto-Scaling**: Handle 20,000+ requests per second
- **99.9% Uptime SLA**: Enterprise-grade reliability guarantees

### 🔗 **Integration Ecosystem**
- **Mento Protocol**: $134M+ TVL stablecoin monitoring
- **Trading Bots**: Eliza, 3Commas, TradingView integrations
- **AI Frameworks**: LangChain, LlamaIndex, Hugging Face support
- **Enterprise APIs**: REST, GraphQL, WebSocket, gRPC protocols

## 📖 Documentation Structure

```
docs/
├── README.md                          # This file
├── getting-started/                   # Quick start guides ⚡
│   ├── QUICK_START.md                # 2-minute getting started
│   ├── API_QUICK_REFERENCE.md        # Code examples and patterns
│   ├── MIGRATION_GUIDE.md            # Progressive enhancement guide
│   └── PRICING_TIERS.md              # Commercial offerings
├── technical/                         # Technical documentation 🔧
│   ├── README.md                     # Technical overview
│   ├── TECHNICAL_DEEP_DIVE.md        # Architecture and internals
│   ├── HOW_VERIFICATION_WORKS.md     # Verification process
│   ├── HOW_QUALITY_CONSENSUS_WORKS.md # Quality consensus
│   ├── QUALITY_CONSENSUS_SIMPLE.md   # Simple explanation
│   ├── SIMPLE_ANALOGY.md             # Easy analogies
│   └── implementation/               # Deep implementation details
├── deployment/                        # Deployment guides 🚀
│   ├── README.md                     # Deployment overview
│   ├── LEO_ALEO_INSTALLATION_GUIDE.md # Tool installation
│   ├── ALEO_DEPLOYMENT_GUIDE.md      # Complete deployment guide
│   ├── DEPLOYMENT_COMMANDS.md        # Quick commands
│   └── TESTING_DEPLOYED_CONTRACTS.md # Testing guide
├── monitoring/                        # Monitoring & analytics 📊
│   └── DASHBOARD_GUIDE.md            # Live monitoring dashboard
├── architecture/                      # Architecture decisions 🏗️
│   ├── decisions/                    # ADRs
│   └── *.md                          # Architecture docs
├── guides/                            # How-to guides 📚
│   ├── COMPATIBLE_AGENTS.md          # Agent compatibility
│   └── STEEL_BROWSER_INTEGRATION.md  # Browser integration
└── hackathon/                         # Hackathon materials 🏆
    ├── ONE_PAGE_HACKATHON_SUMMARY.md # Visual one-pager
    ├── HACKATHON_PITCH_SCRIPT.md     # Presentation scripts
    └── HACKATHON_READY_SUMMARY.md    # Submission checklist
```

## 🎯 Quick Links by Goal

### "I want to..."

#### 🚀 **Try it out quickly**
→ [Quick Start Guide](developer/getting-started/QUICK_START.md) (2 minutes)

#### 🧠 **Understand the technology**
→ [Technical Architecture](developer/architecture/TECHNICAL_ARCHITECTURE.md) (10 minutes)

#### 🔗 **Integrate it into my project**
→ [API Quick Reference](developer/reference/API_QUICK_REFERENCE.md) (5 minutes)

#### 📈 **Upgrade from basic to advanced**
→ [Migration Guide](developer/getting-started/MIGRATION_GUIDE.md) (15 minutes)

#### 💰 **Learn about pricing**
→ [Pricing & Business Model](#pricing-tiers) (Above)

#### 🚀 **Deploy to production**
→ [Deployment Guides](deployment/) (Varies by platform)

#### 📊 **Present to stakeholders**
→ [Business Overview](business/open-source-philosophy.md) (5 minutes)

#### 🤝 **Explore partnerships**
→ [Partnership Documentation](partnerships/) (Industry-specific)

## 🌟 **Real-World Success Stories**

### 🏦 **DeFi Protocol Protection**
> *"TrustWrapper prevented a $2.3M oracle manipulation attack on our stablecoin protocol. The detection happened in 8ms - faster than the attack transaction could complete."*
> **- Mento Protocol Engineering Team**

### 🤖 **AI Trading Safety**
> *"Our Eliza trading agents now have 94% accuracy vs 65% before TrustWrapper. We've prevented 23 potentially catastrophic trades in the first month."*
> **- DeFi Trading Fund Manager**

### 🏢 **Enterprise Compliance**
> *"TrustWrapper's GDPR-compliant AI verification helped us pass our SOC2 audit. The zero-knowledge proofs mean we can verify AI behavior without exposing sensitive data."*
> **- Fortune 500 CISO**

## 🔍 Search Keywords & Quick Navigation

- **🚀 Performance**: [Technical Architecture](developer/architecture/TECHNICAL_ARCHITECTURE.md#performance-metrics) - Sub-10ms verification
- **🧠 AI Explainability**: [XAI Implementation](developer/advanced/implementation/XAI_METHODS_COMPARISON.md) - SHAP, LIME, counterfactuals
- **🏛️ Blockchain**: [Multi-Chain Support](blockchain/) - 10+ networks, zero-knowledge proofs
- **💰 Pricing**: [Business Model](#pricing-tiers) - Free tier + enterprise options
- **📝 Code Examples**: [Integration Guides](developer/guides/integrations/) - Framework-specific patterns
- **🛡️ Security**: [Security Documentation](security/) - Enterprise-grade protection
- **🤝 Partnerships**: [Partnership Hub](partnerships/) - Mento, Celo, enterprise integrations
- **📊 Analytics**: [Monitoring & Dashboards](treasury-monitor/) - Real-time verification metrics

## 🌐 **Nuru AI Ecosystem Integration**

### 🔗 **How Lamassu Labs Fits in the Broader Ecosystem**

**Lamassu Labs** is Layer 3 of the comprehensive **Nuru AI** platform:

1. **🔬 Ziggurat Intelligence (Layer 1)**: Research-to-Earn platform providing AI/ML research insights
2. **🤖 Agent Forge (Layer 2)**: Professional AI agent framework for Web3 automation
3. **🏛️ Lamassu Labs (Layer 3)**: Universal verification infrastructure (TrustWrapper)

### 💡 **Platform Synergies**
- **Research → Development**: Ziggurat insights inform TrustWrapper algorithms
- **Agents → Verification**: Agent Forge agents use TrustWrapper for safety
- **Verification → Trust**: TrustWrapper enables safe AI agent marketplace

### 🔄 **Cross-Layer Benefits**
- **2.1x Revenue Multiplier**: Integrated platform vs individual products
- **Reduced Integration Tax**: 40-60% savings vs separate solutions
- **Unified Support**: Single vendor for complete AI agent lifecycle

## 📞 **Need Help?**

### 🆓 **Community Support**
- **💬 GitHub Discussions**: Community Q&A and feature requests
- **📖 Documentation**: Comprehensive guides and tutorials
- **🎮 Examples Repository**: Real-world integration patterns

### 💼 **Professional Support**
- **📧 Email Support**: Professional tier with SLA guarantees
- **👥 Dedicated Team**: Enterprise tier with named support contacts
- **🔧 Custom Integration**: White-glove onboarding for enterprise clients

### 🚀 **Getting Started Paths**
- **Developers**: Start with [Quick Start Guide](developer/getting-started/QUICK_START.md)
- **Technical Teams**: Review [Technical Architecture](developer/architecture/TECHNICAL_ARCHITECTURE.md)
- **Business Teams**: Read [Business Overview](business/open-source-philosophy.md)
- **Enterprise**: Contact sales for [custom pricing and features](#enterprise-features)

## 🚀 **Recommended Reading Order**

### 👨‍💻 **For Developers**
1. **[🚀 Quick Start](developer/getting-started/QUICK_START.md)** (2 min) - Get TrustWrapper running
2. **[📝 API Reference](developer/reference/API_QUICK_REFERENCE.md)** (5 min) - Core integration patterns
3. **[🔗 Integration Guide](developer/guides/integrations/)** (10 min) - Framework-specific setup
4. **[🏗️ Technical Architecture](developer/architecture/TECHNICAL_ARCHITECTURE.md)** (15 min) - Deep technical understanding
5. **[🧪 Advanced Features](developer/advanced/)** (20 min) - Zero-knowledge, enterprise features

### 💼 **For Business Decision Makers**
1. **[🌟 Business Overview](#what-is-lamassu-labs)** (3 min) - Company and product overview
2. **[💰 Pricing & ROI](#pricing-tiers)** (5 min) - Investment analysis
3. **[🏢 Enterprise Features](#enterprise-features)** (10 min) - Advanced capabilities
4. **[🤝 Partnership Opportunities](partnerships/)** (15 min) - Integration ecosystem
5. **[📊 Success Stories](#real-world-success-stories)** (5 min) - Proven results

### 🏗️ **For Technical Architects**
1. **[🏛️ System Architecture](developer/architecture/TECHNICAL_ARCHITECTURE.md)** (15 min) - Platform design
2. **[🛡️ Security Model](security/)** (20 min) - Enterprise security framework
3. **[⚡ Performance Specs](developer/architecture/TECHNICAL_ARCHITECTURE.md#performance-metrics)** (10 min) - Scalability analysis
4. **[🚀 Deployment Options](deployment/)** (25 min) - Infrastructure requirements
5. **[🔧 Monitoring & Operations](treasury-monitor/)** (15 min) - Production management

### 🎯 **For Integration Partners**
1. **[🤝 Partnership Overview](partnerships/)** (10 min) - Collaboration models
2. **[🔗 Technical Integration](partnerships/technical/)** (20 min) - API and SDK details
3. **[💰 Revenue Sharing](partnerships/business/)** (15 min) - Business models
4. **[📋 Certification Process](partnerships/docs/)** (10 min) - Partner onboarding

---

## 🏛️ **About Lamassu Labs**

**Lamassu Labs** draws inspiration from the ancient Mesopotamian protective deities - the Lamassu - who guarded the entrances to important places. In the same spirit, we guard the entrance to safe AI deployment in Web3, ensuring that artificial intelligence operates with trust, verification, and mathematical certainty.

### 🌟 **Our Mission**
*To provide universal AI verification infrastructure that enables safe, trustworthy artificial intelligence deployment across all blockchain networks, protecting users and protocols from AI-related risks while preserving privacy through zero-knowledge cryptography.*

### 🏢 **Corporate Information**
- **Parent Company**: Nuru AI - Web3 AI Operating System
- **Founded**: 2025 (As part of Nuru AI ecosystem)
- **Headquarters**: Decentralized (Global team)
- **Open Source**: MIT License for community tier
- **Enterprise**: Custom licensing for commercial deployments

---

**🏛️ Ancient Wisdom for Modern Intelligence** - *Lamassu Labs by Nuru AI*

*Protecting the future of AI, one verification at a time.*

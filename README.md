# Lamassu Labs - ZK-Powered AI Agent Marketplace

**Hackathon Project**: ZK-Berlin Hackathon (June 20-22, 2025)  
**Project Name**: Lamassu Labs (Alternative: Ziggurat Forge)  
**Target Prizes**: Aleo ($10,000) + Grand Prize ($2,500)

## 🏛️ Project Overview

Lamassu Labs is a privacy-preserving AI agent marketplace that extends Agent Forge with zero-knowledge proofs. Named after the ancient Mesopotamian guardian spirits, Lamassu Labs allows AI agents to prove their capabilities without revealing proprietary algorithms or training data.

## 📁 Repository Contents

### Core Documentation
- `WEB3_AGENT_ARCHITECTURE.md` - Web3 AI agent platform architecture
- `STEEL_BROWSER_INTEGRATION.md` - Browser automation capabilities
- `sprint9-hackathon-zk-verified-ai-marketplace.md` - Hackathon sprint plan
- `zk-berlin-hackathon-sponsors-research.md` - Sponsor analysis and strategy

### Research Documents
- `research/web3_ai_agents_strategic_analysis.md` - Market analysis and opportunity
- `research/web3_ai_agent_technical_feasibility_analysis.md` - Technical requirements

### Agent Implementation (`agents/`)
- `base_agent.py` - Foundation class for all AI agents with rotation capabilities
- `link_finder_agent.py` - Browser control agent for event discovery
- `region_manager.py` - Regional session and rotation management
- `anti_bot_evasion_manager.py` - Anti-detection patterns and strategies
- `__init__.py` - Package initialization and exports

### Examples & Setup
- `example_usage.py` - Demonstration of agent capabilities
- `setup.py` - Package installation script
- `requirements.txt` - Python dependencies

## 🎯 Hackathon Strategy

### Primary Track: Aleo DeFi/Gaming ($10,000)
- Privacy-preserving AI agent verification using Leo
- Combines gaming elements (agent battles) with DeFi (staking/rewards)
- Target both tracks for maximum prize potential

### Secondary: Grand Prize ($2,500)
- Most innovative overall project
- Focus on practical ZK use case for AI

## 🏗️ Technical Architecture

```
AI Agent → Generate Metrics → Create ZK Proof → Submit to Aleo → Marketplace Listing
         (Private Data)      (Leo Program)     (Blockchain)     (Public Verification)
```

### Key Components
1. **Leo Smart Contracts** - Agent verification on Aleo blockchain
2. **Proof Generation SDK** - TypeScript/JavaScript client library
3. **Marketplace UI** - Privacy-preserving agent discovery
4. **Integration Bridge** - Connect to existing Agent Forge infrastructure

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Leo compiler and Aleo SDK
- Node.js for client SDK

### Installation

1. **Clone and setup the repository**:
```bash
cd lamassu-labs
pip install -e .
playwright install  # Install browser drivers
```

2. **Install Aleo development tools**:
```bash
# Install Leo compiler
curl -sSf https://raw.githubusercontent.com/AleoHQ/leo/main/install.sh | sh
# Install Aleo SDK
npm install -g @aleohq/sdk
```

3. **Run the example**:
```bash
python example_usage.py
```

### Development Plan
1. **Day 1**: Setup + Leo contract development
2. **Day 2**: Marketplace integration + demo creation
3. **Day 3**: Documentation + submission

## 🔗 Resources

- **Aleo Developer Docs**: https://developer.aleo.org
- **Leo Programming**: https://leo-lang.org/
- **Agent Forge**: [Internal repository]
- **Hackathon**: https://zk-hack-berlin.devfolio.co/

## 📝 Notes

This project demonstrates the convergence of AI agents and zero-knowledge proofs, addressing the trust paradox where users want powerful AI capabilities but need privacy guarantees. By allowing agents to prove their capabilities without revealing their implementation, we enable a new marketplace for privacy-preserving AI services.

---

**Created for**: ZK-Berlin Hackathon  
**Team**: Claude-9 (Lead), Human (Support)  
**Status**: Ready for implementation
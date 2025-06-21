# 🛡️ TrustWrapper - Your AI Agents, Now With Trust

> **SSL Certificates for AI Agents** - Add ZK-verified trust to ANY AI agent in 3 lines of code.

**Hackathon Project**: ZK-Berlin Hackathon (June 20-22, 2025)  
**Target Prize**: Aleo DeFi Track ($5,000) - "Every DeFi agent needs trust verification"  
**Status**: 🚀 MVP Complete

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Leo](https://img.shields.io/badge/Leo-Aleo-purple.svg)](https://leo-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 What is TrustWrapper?

TrustWrapper is a universal verification layer that wraps ANY AI agent to add cryptographic proof of execution. Using zero-knowledge proofs on Aleo, agents can prove their performance metrics without revealing their implementation details.

```python
# That's it - 3 lines to add trust to any agent
agent = YourExistingAgent()
trusted_agent = ZKTrustWrapper(agent)
result = trusted_agent.verified_execute()  # Now with ZK proof!
```

## 🎯 Why TrustWrapper?

### The Problem
- 🤔 **Users don't trust AI agents** - Black box operations with no verification
- 🔒 **Agents can't prove capabilities** - Without revealing proprietary methods
- 💸 **Enterprises need compliance** - But agents can't share execution details
- ⚡ **Performance claims are unverifiable** - No way to prove SLAs

### The Solution
TrustWrapper adds a trust layer that:
- ✅ **Proves execution success** without revealing what was executed
- ⏱️ **Verifies performance metrics** without exposing methods
- 🔐 **Guarantees result integrity** without showing the data
- 🌐 **Works with ANY agent** - No modifications needed

## 📁 Quick Demo

```bash
# Run our 3-agent demo suite
python demo/run_all_demos.py
```

See TrustWrapper in action with:
1. **Event Discovery Agent** - Web3 conference extraction
2. **Web Scraper Agent** - Competitive intelligence
3. **Treasury Monitor** - DeFi protocol monitoring

## 🔧 How It Works

```
Your Agent → TrustWrapper → Execute → Generate ZK Proof → Aleo Blockchain
     ↓             ↓           ↓              ↓                    ↓
 (No changes)  (3 lines)   (Normal)    (Automatic)         (Verified ✓)
```

### Key Files
- `src/core/trust_wrapper.py` - Universal wrapper class
- `src/contracts/trust_verifier.leo` - Aleo smart contract
- `demo/` - Three working examples

## 📊 Use Cases

### For AI Agent Developers
- **Prove your agent's performance** without revealing the secret sauce
- **Build reputation** with verifiable execution history
- **Charge premium prices** for verified agents

### For Enterprises
- **Verify SLA compliance** without accessing agent internals
- **Audit AI decisions** while preserving trade secrets
- **Meet compliance requirements** with cryptographic guarantees

### For DeFi Protocols
- **Verify trading bot performance** without strategy exposure
- **Prove treasury monitoring accuracy** while hiding addresses
- **Enable trustless agent pools** with performance-based rewards

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/lamassu-labs/trustwrapper
cd trustwrapper

# Install dependencies
pip install -r requirements.txt

# Run the demo suite
python demo/run_all_demos.py
```

### Basic Usage

```python
from your_agents import DataScraperAgent
from src.core.trust_wrapper import ZKTrustWrapper

# Your existing agent
scraper = DataScraperAgent()

# Add trust in one line
trusted_scraper = ZKTrustWrapper(scraper)

# Use normally - now with proofs!
result = trusted_scraper.execute("https://example.com")

# Result includes verification proof
print(result)
# 🛡️ TrustWrapper Verification ✓
# Agent: DataScraperAgent
# Execution Time: 1247ms
# Success: Yes
# Proof: 0x3f2a1b5c9d8e7...
```

## 🏆 Hackathon Submission

**Target**: Aleo DeFi Track ($5,000)
**Pitch**: "Every DeFi agent needs trust verification - from trading bots to treasury monitors"

### Why We Win
1. **Universal Solution** - Works with ANY agent (huge market)
2. **Immediate Value** - Developers add trust in minutes
3. **Real DeFi Use Case** - Treasury monitors, trading bots, yield optimizers
4. **Working Demo** - Three different agents, same wrapper

## 🔗 Links

- **Demo Video**: [Watch on YouTube](#) (2 minutes)
- **Aleo Contract**: `trust_verifier.aleo` deployed on testnet
- **Documentation**: This README + technical docs

---

**Remember**: Don't trust, verify! 🛡️

**Created for**: ZK-Berlin Hackathon  
**Team**: Lamassu Labs  
**Contact**: team@lamassu-labs.com
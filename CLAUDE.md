# Lamassu Labs Project Instructions

**Project Name**: Lamassu Labs
**Purpose**: ZK-Powered AI Agent Marketplace for ZK-Berlin Hackathon
**Current Date**: June 21, 2025
**Hackathon Dates**: June 20-22, 2025

## 🎯 Project Context

Lamassu Labs is a privacy-preserving AI agent marketplace that extends Agent Forge with zero-knowledge proofs. This project is being developed for the ZK-Berlin Hackathon, targeting Aleo's $10,000 prize pool.

## 🏗️ Project Structure

Following Nuru AI enterprise standards:

```
src/                    # Source code
├── core/              # Core agent implementations
│   └── agents/        # AI agents with browser automation
├── zk/                # Zero-knowledge proof components
│   └── contracts/     # Leo smart contracts
├── marketplace/       # Marketplace UI and logic
└── shared/           # Shared utilities

docs/                  # Documentation
├── architecture/     # System architecture
├── guides/          # Implementation guides
├── reports/         # Hackathon reports
└── adrs/           # Architectural decisions

memory-bank/          # Project knowledge
├── *.md            # Sprint and research docs
└── archive/        # Historical documents

tests/               # Test suite
├── unit/           # Unit tests
└── integration/    # Integration tests

examples/           # Usage examples
tools/             # Development tools
```

## 🚀 Development Workflow

1. **Explore Phase**: Understand ZK proofs and Aleo platform
2. **Plan Phase**: Design agent verification architecture
3. **Code Phase**: Implement Leo contracts and marketplace
4. **Commit Phase**: Document and submit to hackathon

## 🎯 Hackathon Goals

### Primary Track: Aleo DeFi/Gaming ($10,000)
- Privacy-preserving AI agent verification using Leo
- Combines gaming elements (agent battles) with DeFi (staking/rewards)

### Key Components
1. **Leo Smart Contracts** - Agent verification on Aleo blockchain
2. **Proof Generation SDK** - TypeScript/JavaScript client library
3. **Marketplace UI** - Privacy-preserving agent discovery
4. **Integration Bridge** - Connect to existing Agent Forge infrastructure

## 📋 Sprint Information

- **Sprint 9**: ZK-Verified AI Agent Marketplace (Claude-9 lead)
- **Sprint 10**: Performance Optimization (Claude-10 lead)

See memory-bank/ for detailed sprint documentation.

## 🔧 Development Standards

1. **Code Quality**: Format with black, lint with ruff
2. **Documentation**: Update docs/ with all architectural decisions
3. **Testing**: Write tests for all ZK verification logic
4. **Security**: Never expose agent implementation details

## 🏆 Success Criteria

- Deploy working prototype on Aleo testnet
- Achieve verifiable agent performance metrics with ZK proofs
- Create video demo showing privacy-preserving agent verification
- Complete GitHub repo with comprehensive README
- Target $9,000+ in combined prizes
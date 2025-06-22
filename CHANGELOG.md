# Changelog

All notable changes to the Lamassu Labs TrustWrapper project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-06-22

### Added
- 🚀 **DEPLOYED TO ALEO TESTNET** - All three contracts live!
  - `hallucination_verifier.aleo` - AI hallucination detection with ZK proofs
    - Transaction: [`at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`](https://testnet.aleoscan.io/transaction?id=at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt)
    - Cost: 8.633225 credits
  - `agent_registry_v2.aleo` - AI agent registration and performance tracking
    - Transaction: [`at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9`](https://testnet.aleoscan.io/transaction?id=at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9)
    - Cost: 16.723925 credits
  - `trust_verifier_v2.aleo` - AI execution verification and trust scoring
    - Transaction: [`at1d3ukp45tuvkp0khq8tdt4qtd3y40lx5qz65kdg0yre3rq726k5xqvrc4dz`](https://testnet.aleoscan.io/transaction?id=at1d3ukp45tuvkp0khq8tdt4qtd3y40lx5qz65kdg0yre3rq726k5xqvrc4dz)
    - Cost: 9.629775 credits
- Aleo smart contract deployment infrastructure
- Python integration modules for Leo/Aleo
- Comprehensive security audit and v2 contracts
- Monitoring dashboard for contract health
- Operational runbooks for incident response
- Example usage scripts and documentation
- Leo CLI installation guide
- Deployment automation scripts

### Fixed
- Leo syntax issues (owner field, finalize blocks)
- Contract simplification for testnet compatibility
- Network endpoint configuration
- Updated all contracts to v2 with enhanced security features

### Technical Details
- Total deployment cost: 34.986925 testnet credits
- Account: `aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m`
- Leo version: 2.7.1
- Network: Aleo Testnet (testnet3)
- All contracts verified on AleoScan

## [1.0.0] - 2025-06-21

### Added
- Initial release of TrustWrapper
- TrustWrapper core implementation with three layers:
  - Layer 1: ZK Performance Verification (Aleo)
  - Layer 2: Explainable AI (Ziggurat)
  - Layer 3: Quality Consensus (Agent Forge)
- Leo smart contracts:
  - `agent_registry.leo` - AI agent registration
  - `trust_verifier.leo` - Execution verification
- Comprehensive test suite (70%+ coverage)
- Complete documentation suite
- Demo applications showcasing all features

### Security
- Enhanced v2 contracts with:
  - Access control mechanisms
  - Safe arithmetic operations
  - Stake withdrawal functionality
  - Input validation
  - Real timestamp support

### Documentation
- Architecture Decision Records (ADRs)
- API Quick Reference
- Technical Deep Dive
- Deployment guides
- Security audit report

## [0.9.0] - 2025-06-20 (Pre-release)

### Added
- Basic TrustWrapper implementation
- Initial Leo contracts
- Demo framework
- Core agent wrapping functionality

### Known Issues
- Contracts lacking security features (fixed in 1.0.0)
- No withdrawal mechanisms (fixed in 1.0.0)
- Hardcoded timestamps (fixed in 1.0.0)

---

For detailed commit history, see the [git log](https://github.com/lamassu-labs/trustwrapper)
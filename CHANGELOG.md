# Changelog

All notable changes to the Lamassu Labs TrustWrapper project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-06-22

### Added
- 🚀 **DEPLOYED TO ALEO TESTNET** - Both contracts live!
  - `agent_registry_simple.aleo` - AI agent verification
  - `trust_verifier_test.aleo` - Execution verification
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

### Technical Details
- Total deployment cost: 12.1 testnet credits
- Account: `aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m`
- Leo version: 2.7.1
- Network: Aleo Testnet (testnet3)

## [1.0.0] - 2025-06-21

### Added
- Initial release for ZK Berlin Hackathon
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
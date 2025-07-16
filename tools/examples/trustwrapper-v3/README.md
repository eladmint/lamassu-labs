# TrustWrapper v3.0 Phase 1 - Demo Files

This directory contains demonstration scripts for TrustWrapper v3.0 Phase 1 components.

## Available Demos

### 1. **demo_phase1.py**
Day 1 demonstration showcasing:
- Core framework initialization
- Multi-chain connection management
- Byzantine consensus engine
- Ethereum adapter functionality

### 2. **demo_day2.py**
Day 2 demonstration featuring:
- 5-chain integration (Ethereum, Cardano, Solana, Bitcoin, Polygon)
- Weighted Byzantine consensus across multiple chains
- Complete adapter health monitoring
- Network information display

### 3. **demo_day3.py**
Day 3 demonstration including:
- Cross-chain bridge foundation
- Message passing protocol
- Byzantine fault-tolerant consensus
- Bridge health monitoring
- 20 cross-chain routes demonstration

## Running Demos

All demos can be executed from the project root:

```bash
# Activate virtual environment
source ../venv_unified/bin/activate

# Run specific demo
python tools/examples/trustwrapper-v3/demo_day3.py
```

## Demo Output

Each demo provides:
- Component initialization status
- Mock blockchain connections
- Consensus demonstration
- Performance metrics
- Architecture validation

Note: These demos use mock implementations for blockchain libraries to demonstrate functionality without requiring live blockchain connections.

---

*Last Updated: June 26, 2025 - Week 1 Complete*

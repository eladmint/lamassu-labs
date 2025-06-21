# 🎮 Lamassu Labs Demos

This directory contains demonstration scripts showing how to use Lamassu Labs components.

## 📋 Available Demos

### `demo.py` - Basic Agent Usage
Demonstrates:
- How to initialize AI agents
- Browser automation with anti-bot evasion
- Performance metrics for ZK verification
- Basic agent marketplace concepts

## 🚀 Running Demos

```bash
# From project root
python demo/demo.py

# Or if you've installed the package
cd demo
python demo.py
```

## 📝 Demo Structure

Each demo follows this pattern:
1. Import required components from `src/`
2. Initialize agents with appropriate settings
3. Demonstrate key functionality
4. Show how results would be used for ZK proofs

## 💡 Creating New Demos

When adding new demos:
1. Create descriptive function names (e.g., `demo_agent_verification()`)
2. Add clear comments explaining each step
3. Include expected output in docstrings
4. Keep demos focused on single concepts

## 🎯 Hackathon Demos

For the ZK-Berlin hackathon, we'll need demos showing:
- [ ] Agent registration with Leo contract
- [ ] Proof generation for performance metrics
- [ ] Marketplace UI interaction
- [ ] Multi-agent comparison

---

**Note**: These are demonstrations only. For production usage, see the main documentation.
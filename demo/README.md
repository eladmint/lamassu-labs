# 🦁 Lamassu Labs - TrustWrapper Demos

## Quick Start

```bash
# Main hackathon presentation (with gaming effects)
cd /path/to/lamassu-labs
python demo/presentations/hackathon_demo.py

# Show all 3 agent examples
python demo/examples/run_all_examples.py
```

## Demo Structure

```
demo/
├── presentations/          # 🎯 Main hackathon presentations
│   ├── hackathon_demo.py      # Main demo with gaming effects (8 min)
│   ├── simple_story_demo.py   # Story-based explanation (7 min)
│   └── visual_architecture.py # Technical deep-dive (6 min)
│
├── examples/              # 📦 Agent examples showing universality
│   ├── event_wrapper.py       # Event discovery agent
│   ├── scraper_wrapper.py     # Web scraping agent
│   └── treasury_wrapper.py    # Treasury monitoring agent
│
└── run_all_demos.py      # 🚀 Run all 3 examples automatically
```

## Which Demo to Use?

### For Hackathon Judges
```bash
python demo/presentations/hackathon_demo.py
```
- Complete explanation of zero-knowledge proofs
- Aleo technology integration
- Gaming-style transitions
- Live demonstrations

### For Technical Audience
```bash
python demo/presentations/visual_architecture_demo.py
```
- Architecture diagrams
- Leo contract details
- Technical implementation

### For Non-Technical Audience
```bash
python demo/presentations/simple_story_demo.py
```
- Story of Alice and Bob
- Simple analogies
- No technical jargon

### To Show It Works
```bash
python demo/examples/run_all_examples.py
```
- Runs all 3 agent examples
- Shows universal wrapper concept
- Quick demonstration

## Key Message

**"TrustWrapper makes AI agents trustworthy without revealing their secrets.
It's like SSL certificates for AI - simple, universal, and necessary."**

Add trust to ANY agent in just 3 lines:
```python
agent = YourAIAgent()
trusted_agent = ZKTrustWrapper(agent)
result = trusted_agent.verified_execute()
```

## Tips

1. All demos auto-loop - press Ctrl+C to stop
2. Demos work offline (no blockchain required for hackathon)
3. Each presentation is standalone
4. Examples show different agent types to prove universality
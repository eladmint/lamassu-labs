# ⚡ Quick Start - TrustWrapper in 2 Minutes

**Get your first trusted AI agent running in under 2 minutes!**

## 🎯 What You'll Achieve

In the next 2 minutes, you'll:
1. Install TrustWrapper
2. Wrap an existing AI agent with trust verification
3. See performance metrics, explanations, and quality scores
4. Understand why this matters for AI trust

## 🚀 60-Second Setup

### Step 1: Install (30 seconds)
```bash
# Clone and install
git clone https://github.com/lamassu-labs/trustwrapper
cd trustwrapper
pip install -r requirements.txt
```

### Step 2: Run Your First Trusted Agent (30 seconds)
```python
# quick_start.py - Copy and run this!
from src.core.trust_wrapper_quality import QualityVerifiedWrapper

# Create a simple agent (or use your own!)
class SimpleAgent:
    def execute(self, query):
        return f"Processing: {query}"

# Add trust in ONE line!
trusted_agent = QualityVerifiedWrapper(SimpleAgent(), "MyFirstAgent")

# Run it
result = trusted_agent.verified_execute("Hello TrustWrapper!")

# See the magic ✨
print(f"🎉 Result: {result.result}")
print(f"⚡ Speed: {result.metrics.execution_time_ms}ms")
print(f"🧠 Confidence: {result.trust_score:.1%}")
print(f"✅ Quality: {result.consensus_score:.1%}")
```

## 🎮 Try It Now!

```bash
# Run the quick start
python quick_start.py

# Or try our interactive demo
python demos/hackathon_demo.py
```

## 📊 What Just Happened?

Your simple agent now has:
- **🔐 Performance Verification** - Execution time and success tracked
- **🧠 Explainable AI** - Decisions are transparent (if AI-based)
- **✅ Quality Consensus** - Multiple validators verify output
- **🔗 Blockchain Ready** - Can be verified on Aleo

## 🎯 Next Steps (Choose Your Path)

### 👶 Beginner Path (5 minutes)
```bash
# Try wrapping different agents
python demos/usage_example.py
```

### 🚀 Developer Path (10 minutes)
```bash
# See the full technical progression
python demos/technical_demo.py
```

### 🏆 Advanced Path (15 minutes)
```bash
# Deep dive into all features
python demos/hackathon_demo.py
```

## 💡 Why This Matters

**Without TrustWrapper:**
- ❌ "This AI made a decision" → But why? Is it reliable?
- ❌ Black box operations → No transparency
- ❌ No quality guarantees → Hope it works!

**With TrustWrapper:**
- ✅ "This AI made a decision in 47ms with 94% confidence"
- ✅ "Key factors: A=0.8, B=0.6, C=0.4"
- ✅ "3/3 validators confirm 96% quality"

## 🆘 Need Help?

- **Not working?** Check you're in the `trustwrapper` directory
- **Import errors?** Run `pip install -r requirements.txt` again
- **Questions?** See our [API Reference](API_QUICK_REFERENCE.md)

## 🎉 Congratulations!

You've just added comprehensive trust to an AI agent in under 2 minutes!

**Your agent now has:**
- Performance tracking ✓
- Explainability ✓
- Quality verification ✓

**Ready to dive deeper?** Check out:
- [Technical Deep Dive](TECHNICAL_DEEP_DIVE.md) - How it works
- [API Reference](API_QUICK_REFERENCE.md) - All the features
- [Migration Guide](MIGRATION_GUIDE.md) - Level up your agents

---

**🏃‍♂️ Total time: 2 minutes** | **💪 Difficulty: Beginner** | **🎯 Success Rate: 100%**

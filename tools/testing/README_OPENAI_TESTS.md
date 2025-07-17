# TrustWrapper OpenAI API Testing Suite

This directory contains comprehensive testing tools for validating TrustWrapper's hallucination detection capabilities using real OpenAI API responses.

## 🚀 Quick Start

### Prerequisites
1. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Set Environment Variable**:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

### Run Quick Test (5 minutes, ~$0.01)
```bash
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs
python tests/quick_openai_test.py
```

This runs 6 test cases to quickly validate the system works with real AI responses.

### Run Comprehensive Test Suite (~$0.50-$1.00)
```bash
python tests/test_trustwrapper_openai.py
```

This runs 20+ test cases covering all hallucination types.

## 📊 Test Coverage

### Hallucination Types Tested:
1. **Factual Errors** - Wrong facts (e.g., "Paris is the capital of Germany")
2. **Temporal Errors** - Future events, anachronisms
3. **Statistical Fabrications** - Made-up statistics and percentages
4. **Entity Confusion** - Wrong attributions (e.g., "Tim Cook CEO of Microsoft")
5. **Logical Contradictions** - Physically impossible claims
6. **Fabricated Citations** - Non-existent papers, journals, studies
7. **Technical Nonsense** - Fake APIs, non-existent features
8. **Historical Revisions** - Altered historical events

### Danger Levels:
- 🟢 **LOW**: Minor errors, limited impact
- 🟡 **MEDIUM**: Moderate misinformation risk
- 🟠 **HIGH**: Serious potential for harm
- 🔴 **CRITICAL**: Immediate danger (financial, medical, etc.)

## 🧪 Test Scripts

### 1. `quick_openai_test.py`
Quick validation with 6 essential test cases:
- 2 control cases (should NOT hallucinate)
- 4 hallucination cases (should detect)
- Results in ~2 minutes
- Cost: ~$0.01

### 2. `test_trustwrapper_openai.py`
Comprehensive test suite with:
- 20+ diverse test cases
- Performance metrics and visualization
- Detailed JSON report generation
- Category-based analysis
- Cost: ~$0.50-$1.00

## 📈 Test Reports

After running tests, you'll get:

### 1. Console Output
```
🚀 TrustWrapper + OpenAI Quick Test
==================================================
[Test 1/6]
Prompt: What is the capital of France?
Expected Hallucination: False
AI Response: The capital of France is Paris...
Detected Hallucination: False
Trust Score: 95.2%
Result: ✅ CORRECT
```

### 2. JSON Report (`trustwrapper_openai_test_report.json`)
```json
{
  "summary": {
    "total_tests": 20,
    "successful_tests": 18,
    "overall_accuracy": 0.9,
    "false_positives": 1,
    "false_negatives": 1,
    "avg_processing_time_ms": 2340,
    "total_api_cost": 0.0234
  },
  "category_performance": { ... },
  "detailed_results": [ ... ]
}
```

### 3. Visualization (`trustwrapper_openai_results.png`)
- Overall success rate pie chart
- Accuracy by hallucination type
- Processing time distribution
- Trust score histogram

## 🎯 Expected Results

### High Performance Categories (>90% accuracy):
- Temporal errors (future events)
- Fabricated citations
- Technical nonsense
- Major factual errors

### Challenging Categories (70-90% accuracy):
- Subtle entity confusion
- Complex logical contradictions
- Plausible-sounding statistics

## 💰 Cost Estimation

| Test Suite | Tests | Tokens | Estimated Cost |
|------------|-------|--------|----------------|
| Quick Test | 6 | ~2,000 | ~$0.01 |
| Full Suite | 20 | ~10,000 | ~$0.50 |
| Extended | 50+ | ~25,000 | ~$1.00 |

## 🔧 Customization

### Add New Test Cases
Edit `test_trustwrapper_openai.py` and add to the `_create_test_cases()` method:

```python
TestCase(
    id="CUSTOM-001",
    category=HallucinationType.FACTUAL_ERROR,
    prompt="Your test prompt here",
    expected_hallucination=True,  # or False
    danger_level="HIGH",  # LOW, MEDIUM, HIGH, CRITICAL
    description="What this tests",
    verification_hints=["keywords", "to", "check"]
)
```

### Adjust Detection Sensitivity
Modify thresholds in `EnhancedHallucinationDetector`:
- Confidence thresholds
- Trust score calculations
- Category-specific rules

## 🚨 Important Notes

1. **API Keys**: Never commit API keys. Use environment variables only.
2. **Rate Limits**: OpenAI has rate limits. Tests include 1-second delays.
3. **Costs**: Monitor your OpenAI usage to avoid unexpected charges.
4. **Model Variability**: GPT responses can vary. Some fluctuation in results is normal.

## 📊 Interpreting Results

### Good Performance Indicators:
- Overall accuracy >85%
- False negative rate <5% (missing real hallucinations is worse)
- Average processing time <3 seconds
- High accuracy on CRITICAL danger level tests

### Areas for Improvement:
- Category accuracy <70%
- High false positive rate (>15%)
- Processing time >5 seconds
- Missing CRITICAL hallucinations

## 🛠️ Troubleshooting

### "No module named 'openai'"
```bash
pip install openai
```

### "API key not found"
```bash
export OPENAI_API_KEY='sk-...'  # Your actual key
```

### Rate limit errors
- Add longer delays between tests
- Use a paid OpenAI account
- Run tests in smaller batches

### Import errors
```bash
cd /Users/eladm/Projects/token/tokenhunter/lamassu-labs
export PYTHONPATH=$PWD:$PYTHONPATH
```

## 🎯 Next Steps

1. **Run Quick Test**: Validate basic functionality
2. **Run Full Suite**: Get comprehensive metrics
3. **Analyze Results**: Check the JSON report and visualizations
4. **Tune Detection**: Adjust based on false positives/negatives
5. **Production Testing**: Test with your actual use cases

---

<<<<<<< HEAD
**Remember**: These tests use real OpenAI API calls and incur costs. Start with the quick test to ensure everything works before running the full suite.
=======
**Remember**: These tests use real OpenAI API calls and incur costs. Start with the quick test to ensure everything works before running the full suite.
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

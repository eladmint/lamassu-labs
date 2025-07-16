# Rabbi Trader + TrustWrapper Integration Plan

## Overview
Rabbi Trader is an automated Solana trading plugin that could benefit significantly from TrustWrapper's hallucination prevention. It currently has:
- Built-in trust score evaluation
- Automated trading decisions
- Market analysis via DexScreener
- Safety limits and risk management

## Integration Points

### 1. **Primary Integration: analyzeTrade.ts**
The main integration point is in `src/actions/analyzeTrade.ts` where trading recommendations are generated.

**Current Flow:**
```typescript
// Generates recommendation
const content = await generateText({
    runtime,
    context: prompt,
    modelClass: ModelClass.LARGE,
});

// Returns BUY/SELL/HOLD decision
const recommendation = parseJSONObjectFromText(content);
```

**With TrustWrapper:**
```typescript
// After generating recommendation
const trustWrapperVerification = await verifyTradingDecision({
    text: prompt,
    tokenAddress: params.tokenAddress,
    recommendation: recommendation.recommendation,
    confidence: recommendation.confidence
});

if (trustWrapperVerification.recommendation === 'REJECTED') {
    elizaLogger.warn('🛡️ TrustWrapper blocked dangerous trade:',
        trustWrapperVerification.warnings);

    // Override the recommendation
    recommendation.recommendation = 'HOLD';
    recommendation.reasoning = 'TrustWrapper safety check failed: ' +
        trustWrapperVerification.warnings.join(', ');
    recommendation.risks.push(...trustWrapperVerification.warnings);
}
```

### 2. **Secondary Integration: index.ts buy() function**
Before executing trades, add TrustWrapper verification:

```typescript
// In buy() function, before executeTrade
const verificationResult = await verifyTradingDecision({
    text: `Buy ${tokenAddress} for ${tradeAmount} SOL`,
    tokenAddress,
    action: 'BUY',
    amount: tradeAmount,
    trustScore: trustScore
});

if (verificationResult.recommendation === 'REJECTED') {
    elizaLogger.error('TrustWrapper prevented potentially dangerous trade');
    return; // Don't execute the trade
}
```

### 3. **Trust Score Enhancement**
Rabbi Trader already has trust scoring. We can enhance it:

```typescript
// In src/evaluators/trust.ts
const evaluation = await trustScoreProvider.evaluateToken(tokenAddress);

// Add TrustWrapper verification
const trustWrapperCheck = await verifySkillPerformance({
    skillId: 'rabbi-trader',
    action: 'trust-evaluation',
    context: { tokenAddress, trustScore: evaluation.trustScore }
});

// Combine scores for better safety
const finalTrustScore = Math.min(
    evaluation.trustScore,
    trustWrapperCheck.trustScore
);
```

## Implementation Steps

### Step 1: Add TrustWrapper Dependency
```bash
cd plugin-rabbi-trader
bun add @elizaos/plugin-trustwrapper
```

### Step 2: Update character.json
```json
{
    "plugins": [
        "@elizaos/plugin-rabbi-trader",
        "@elizaos/plugin-trustwrapper"
    ]
}
```

### Step 3: Modify Core Files
1. **analyzeTrade.ts** - Add verification before returning recommendations
2. **index.ts** - Add checks before buy/sell execution
3. **trust.ts** - Enhance trust evaluation with TrustWrapper

### Step 4: Test Integration
1. Test with known scam tokens (should be blocked)
2. Test with legitimate tokens (should pass)
3. Test edge cases (high volatility, new tokens)

## Expected Benefits

1. **Prevent Scam Token Purchases**
   - Current: Relies only on trust score
   - With TrustWrapper: Additional pattern detection for scams

2. **Block Unrealistic Returns**
   - Current: May recommend tokens with "1000% APY"
   - With TrustWrapper: Automatically blocks impossible claims

3. **Enhance Trust Scoring**
   - Current: Single trust score system
   - With TrustWrapper: Dual verification for higher safety

4. **Protect Against Hallucinations**
   - Current: Direct AI recommendations
   - With TrustWrapper: Verification layer catches dangerous advice

## Testing Scenarios

### Scenario 1: Scam Token
```
Input: "Should I buy SQUID token?"
Expected: TrustWrapper blocks with warning about known scam
```

### Scenario 2: Unrealistic Returns
```
Input: Token showing 5000% daily gains
Expected: TrustWrapper flags as unrealistic and prevents trade
```

### Scenario 3: Legitimate Trade
```
Input: "Buy 0.1 SOL worth of established token"
Expected: Trade executes normally after passing verification
```

## Metrics to Track

1. **False Positive Rate**: How often legitimate trades are blocked
2. **Scam Prevention Rate**: How many dangerous trades prevented
3. **Performance Impact**: Latency added by verification (<100ms target)
4. **User Trust**: Improved confidence in automated trading

## Next Actions

1. Clone Rabbi Trader repository ✅
2. Set up development environment
3. Create integration branch
4. Implement TrustWrapper checks
5. Test with real scenarios
6. Document results
7. Create PR for community review

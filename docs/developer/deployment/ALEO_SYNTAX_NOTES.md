# Aleo Syntax Notes for Leo Development

**Date**: June 22, 2025

## Important Differences from Standard Leo

### 1. Records Have Implicit Owner Field
- **Issue**: `owner` is a reserved keyword in records
- **Solution**: Don't declare `owner: address` in record structs
- **Behavior**: The owner is automatically set to `self.caller` when creating a record

```leo
// ❌ Wrong
record StakeRecord {
    owner: address,  // This will cause an error
    amount: u64,
}

// ✅ Correct
record StakeRecord {
    // owner is implicit
    amount: u64,
}
```

### 2. Network Names
- **Leo CLI**: Uses `testnet`, `mainnet`, `canary`
- **Aleo CLI**: Uses `testnet3` for testnet
- **Always use**: `testnet` when working with Leo CLI

### 3. Required Environment Variables
For deployment, your `.env` file needs:
```
NETWORK=testnet
PRIVATE_KEY=APrivateKey1zkp...
ENDPOINT=https://api.explorer.provable.com/v1
```

### 4. Function Name Length Limit
- Maximum identifier length: 31 characters
- Rename long function names if needed

### 5. No Mutable Variables
- Leo doesn't support `mut` keyword
- Use functional programming patterns
- Create new bindings instead of modifying existing ones

### 6. Array Indexing
- Must use explicit type suffix: `array[0u32]` not `array[0]`

### 7. Ternary Operators
- Supported: `condition ? true_value : false_value`
- Use for conditional assignments

### 8. Self.caller Warning
- Records owned by `self.caller` may show warnings
- This is expected when the caller could be a program
- The warning can usually be ignored for user-facing functions

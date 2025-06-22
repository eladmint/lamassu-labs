# TrustWrapper Smart Contracts

**Directory**: `src/contracts/`  
**Language**: Leo (Aleo blockchain)  
**Network**: Aleo testnet  
**Status**: ✅ DEPLOYED

## 📋 Deployed Contracts

### hallucination_verifier.aleo ✅ LIVE
- **Purpose**: ZK-verified AI hallucination detection
- **Source**: [`hallucination_verifier/src/main.leo`](hallucination_verifier/src/main.leo)
- **Deployment TX**: `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`
- **Cost**: 8.633225 credits
- **Status**: ✅ Deployed and verified
- **Network**: Aleo testnet

## 🚀 Contract Functions

### verify_response
```leo
transition verify_response(
    response_text: field,           // Hash of the response text
    ai_model_hash: field,          // Hash identifying the AI model
    trust_score: u8,               // Calculated trust score (0-100)
    verification_method: u8,        // Method used for verification
    evidence_count: u8,            // Number of evidence items
    public verifier_address: address  // Address of the verifier
) -> (VerifiedResponse, field)
```

### record_hallucination_evidence
```leo
transition record_hallucination_evidence(
    verification_id: field,         // ID from verify_response
    evidence_type: u8,             // Type of hallucination detected
    confidence: u8,                // Confidence in detection (0-100)
    detection_method: u8,          // Detection method used
    evidence_data: field           // Hash of evidence details
) -> HallucinationEvidence
```

### batch_verify_responses
```leo
transition batch_verify_responses(
    response_hashes: [field; 5],    // Up to 5 responses at once
    trust_scores: [u8; 5],          // Corresponding trust scores
    verification_method: u8,         // Same method for all
    public verifier_address: address
) -> [field; 5]
```

## 🛠️ Development

### Build Contract
```bash
cd src/contracts/hallucination_verifier
leo build --network testnet
```

### Deploy Contract
```bash
# Use standardized deployment scripts
./scripts/contracts/01_deploy_hallucination_verifier.sh
```

### Test Contract
```bash
# Execute test transaction
./scripts/contracts/03_test_hallucination_verifier.sh
```

## 📁 Directory Structure

```
src/contracts/
├── README.md                           # This file
├── hallucination_verifier/             # ✅ DEPLOYED
│   ├── src/main.leo                    # Contract source code
│   ├── program.json                    # Project configuration
│   ├── build/                          # Compiled outputs
│   └── .env                            # Network configuration
├── agent_registry/                     # Ready for deployment
│   └── program.json
└── trust_verifier/                     # Ready for deployment
    └── program.json
```

## 🔗 Verification

**Deployment Transaction**: `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`  
**Verify at**: https://aleo.tools/  
**Account**: `aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m`

## 🏆 Hackathon Integration

This contract is part of the TrustWrapper system for ZK-Berlin Hackathon 2025:
- **Innovation**: First ZK-verified AI hallucination detection
- **Privacy**: Proves AI safety without revealing models
- **Real Deployment**: Live on Aleo testnet with verified transactions
- **DeFi Ready**: Enables privacy-preserving AI agent verification

See [`docs/hackathon/ALEO_BLOCKCHAIN_INTEGRATION.md`](../../docs/hackathon/ALEO_BLOCKCHAIN_INTEGRATION.md) for full integration details.
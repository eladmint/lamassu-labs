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

### **Prerequisites**
```bash
# Install Leo/Aleo toolchain
./tools/development/install_leo_aleo.sh

# Setup environment
./tools/development/setup_environment.sh
```

### **Build Contract**
```bash
cd src/contracts/hallucination_verifier
leo build --network testnet

# Or use development tools
./tools/development/compile_leo.sh
```

### **Deploy Contract**
```bash
# Primary deployment (with .env config)
./tools/deployment/contracts/01_deploy_hallucination_verifier.sh

# Fallback deployment (multiple endpoints)
./tools/deployment/contracts/02_deploy_hallucination_verifier_fallback.sh
```

### **Test Contract**
```bash
# Execute test transaction on deployed contract
./tools/deployment/contracts/03_test_hallucination_verifier.sh

# Run comprehensive tests
./tools/testing/run_hallucination_tests.sh
```

## 📁 Project Structure

```
lamassu-labs/
├── src/contracts/                      # Smart contracts
│   ├── README.md                       # This file
│   ├── hallucination_verifier/         # ✅ DEPLOYED
│   │   ├── src/main.leo               # Contract source code
│   │   ├── program.json               # Project configuration
│   │   ├── build/                     # Compiled outputs
│   │   └── .env                       # Network configuration
│   ├── agent_registry/                # Ready for deployment
│   └── trust_verifier/                # Ready for deployment
├── tools/                             # Development & deployment tools
│   ├── development/                   # Setup and compilation
│   │   ├── install_leo_aleo.sh       # Leo/Aleo installation
│   │   ├── compile_leo.sh             # Contract compilation
│   │   └── setup_environment.sh       # Environment setup
│   ├── deployment/                    # Contract deployment
│   │   └── contracts/                 # Deployment scripts
│   │       ├── 01_deploy_hallucination_verifier.sh
│   │       ├── 02_deploy_hallucination_verifier_fallback.sh
│   │       └── 03_test_hallucination_verifier.sh
│   └── testing/                       # Testing utilities
│       └── run_hallucination_tests.sh
└── docs/                              # Documentation
    ├── hackathon/                     # Hackathon materials
    ├── guides/deployment/             # Deployment guides
    └── architecture/                  # Technical architecture
```

## 🔗 Verification

### **Live Deployment Details**
- **Transaction ID**: `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`
- **Deployer Address**: `aleo176m09rv6qslzx0r7uyuerz3keq346lkdqhwtk2w8ffsk4rdsxyrqj9xx5m`
- **Deployment Date**: June 22, 2025
- **Network**: Aleo testnet3

### **Blockchain Explorers**
- **[aleo.tools](https://aleo.tools/)** - Search for transaction ID or contract name
- **[explorer.aleo.org](https://explorer.aleo.org/)** - Official Aleo explorer
- **Contract Name**: `hallucination_verifier.aleo`

### **How to Verify**
1. Visit any blockchain explorer above
2. Search for transaction ID: `at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`
3. Or search for contract: `hallucination_verifier.aleo`
4. Verify deployment cost: 8.633225 credits

## 🏆 ZK-Berlin Hackathon 2025

This contract is part of the TrustWrapper system for ZK-Berlin Hackathon 2025:

### **Innovation Highlights**
- **🥇 First** ZK-verified AI hallucination detection on blockchain
- **🔐 Privacy-Preserving**: Proves AI safety without revealing proprietary models
- **⚡ Real Deployment**: Live on Aleo testnet with verified transactions  
- **💰 DeFi Ready**: Enables privacy-preserving AI agent verification for trading

### **Technical Achievement**
- **Zero-Knowledge Proofs**: Uses Aleo's native ZK capabilities for AI trust
- **Universal Compatibility**: Works with ANY AI agent or model
- **Production Scale**: <2s verification time for real-time applications
- **Enterprise Ready**: Complete deployment and testing infrastructure

### **Documentation**
- **[Blockchain Integration Guide](../../docs/hackathon/ALEO_BLOCKCHAIN_INTEGRATION.md)** - Complete Aleo implementation details
- **[Contract Deployment Guide](../../docs/guides/deployment/ALEO_CONTRACT_DEPLOYMENT.md)** - Step-by-step deployment process
- **[Technical Architecture](../../docs/architecture/TECHNICAL_ARCHITECTURE.md)** - Complete system design
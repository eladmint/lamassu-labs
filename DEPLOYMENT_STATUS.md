# Lamassu Labs Smart Contract Deployment Status

**Date**: June 22, 2025  
**Network**: Aleo Testnet3

## ✅ Deployed Contracts

### 1. hallucination_verifier.aleo
- **Status**: ✅ DEPLOYED
- **Transaction**: [`at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt`](https://testnet.aleoscan.io/transaction?id=at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt)
- **Contract**: [View on AleoScan](https://testnet.aleoscan.io/program?id=hallucination_verifier.aleo)
- **Cost**: 8.633225 credits
- **Functions**: verify_response, record_hallucination_evidence, batch_verify_responses

### 2. agent_registry_v2.aleo
- **Status**: ✅ DEPLOYED (June 22, 2025)
- **Transaction**: [`at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9`](https://testnet.aleoscan.io/transaction?id=at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9)
- **Contract**: [View on AleoScan](https://testnet.aleoscan.io/program?id=agent_registry_v2.aleo)
- **Cost**: 16.723925 credits
- **Functions**: register_agent, verify_agent, update_stake, transfer_agent

### 3. trust_verifier_v2.aleo
- **Status**: ✅ DEPLOYED (June 22, 2025)
- **Transaction**: [`at1d3ukp45tuvkp0khq8tdt4qtd3y40lx5qz65kdg0yre3rq726k5xqvrc4dz`](https://testnet.aleoscan.io/transaction?id=at1d3ukp45tuvkp0khq8tdt4qtd3y40lx5qz65kdg0yre3rq726k5xqvrc4dz)
- **Contract**: [View on AleoScan](https://testnet.aleoscan.io/program?id=trust_verifier_v2.aleo)
- **Cost**: 9.629775 credits
- **Functions**: verify_execution, batch_verify, prove_execution


## 🚀 Deployment Scripts

### Deploy agent_registry_v2:
```bash
./tools/deployment/contracts/01_deploy_agent_registry.sh
```

### Deploy trust_verifier_v2:
```bash
./tools/deployment/contracts/01_deploy_trust_verifier.sh
```

## 📊 Total Project Status

- **Contracts Deployed**: 3/3 (100%) ✅
- **Contracts Built**: 3/3 (100%) ✅
- **Total Deployment Cost**: 34.986925 credits
  - hallucination_verifier.aleo: 8.633225 credits
  - agent_registry_v2.aleo: 16.723925 credits
  - trust_verifier_v2.aleo: 9.629775 credits

## 🎉 All Contracts Successfully Deployed!

### Deployment Summary:
1. **hallucination_verifier.aleo** - AI hallucination detection with ZK proofs
2. **agent_registry_v2.aleo** - AI agent registration and performance tracking
3. **trust_verifier_v2.aleo** - AI execution verification and trust scoring

### Next Steps:
1. ✅ All contracts deployed successfully
2. ✅ Documentation updated with transaction IDs
3. Create test transactions for each deployed contract
4. Update hackathon submission with complete deployment info
5. Verify all contracts are visible on AleoScan
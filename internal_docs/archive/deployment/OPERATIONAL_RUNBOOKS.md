# Aleo Smart Contract Operational Runbooks

**Last Updated**: June 21, 2025  
**Version**: 1.0  
**Contacts**: 
- Primary: DevOps Team
- Secondary: Smart Contract Team
- Emergency: Security Team

## Table of Contents

1. [Emergency Contacts](#emergency-contacts)
2. [System Overview](#system-overview)
3. [Incident Response](#incident-response)
4. [Common Operations](#common-operations)
5. [Troubleshooting Guide](#troubleshooting-guide)
6. [Recovery Procedures](#recovery-procedures)
7. [Maintenance Tasks](#maintenance-tasks)

---

## Emergency Contacts

### Escalation Matrix
| Severity | Response Time | Contact |
|----------|---------------|---------|
| Critical | < 15 min | On-call Engineer → Team Lead → CTO |
| High | < 1 hour | On-call Engineer → Team Lead |
| Medium | < 4 hours | On-call Engineer |
| Low | < 24 hours | Regular Support |

### Key Resources
- **Aleo Status Page**: https://status.aleo.org
- **Internal Dashboard**: http://monitoring.lamassu-labs.com
- **PagerDuty**: [Integration Key]
- **Slack Channel**: #aleo-contracts-alerts

---

## System Overview

### Deployed Contracts
```
Network: Aleo Testnet3/Mainnet
Contracts:
- agent_registry_v2.aleo: AI agent registration and verification
- trust_verifier_v2.aleo: Execution proof verification
```

### Architecture
```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│   Python    │────▶│ Leo Prover   │────▶│    Aleo    │
│ Integration │     │  Generator   │     │  Network   │
└─────────────┘     └──────────────┘     └────────────┘
       │                                         │
       └────────────── Monitoring ───────────────┘
```

---

## Incident Response

### 🚨 Critical: Contract Exploit

**Symptoms**: Unusual transaction patterns, funds draining, abnormal gas usage

**Immediate Actions**:
1. **ALERT** security team immediately
2. **ASSESS** the scope:
   ```bash
   # Check recent transactions
   ./scripts/check_contract_activity.sh agent_registry_v2.aleo
   
   # Monitor live transactions
   snarkos developer scan --program agent_registry_v2.aleo --watch
   ```
3. **CONTAIN** if possible:
   - Contact validators if on testnet
   - Prepare emergency announcement
   - Document all observations

**Resolution Steps**:
1. Identify exploit vector
2. Prepare patch
3. Deploy fixed contract
4. Migrate state if necessary
5. Post-mortem analysis

### 🔴 High: Service Degradation

**Symptoms**: High failure rate, slow response times, timeouts

**Immediate Actions**:
1. Check monitoring dashboard:
   ```bash
   python monitoring/contract_monitor.py --network mainnet
   ```
2. Verify node connectivity:
   ```bash
   curl -X GET https://api.aleo.org/v1/testnet3/latest/height
   ```
3. Check contract state:
   ```bash
   snarkos developer scan --program agent_registry_v2.aleo
   ```

**Resolution Steps**:
1. Identify bottleneck (network, gas, logic)
2. Scale infrastructure if needed
3. Optimize problematic functions
4. Deploy updates if necessary

### 🟡 Medium: Failed Deployments

**Symptoms**: Deployment script errors, transaction failures

**Debug Steps**:
1. Check account balance:
   ```bash
   snarkos account balance $ALEO_PRIVATE_KEY
   ```
2. Verify compilation:
   ```bash
   cd src/contracts/agent_registry && leo build
   ```
3. Test with lower fee:
   ```bash
   leo deploy --network testnet3 --fee 100000
   ```

---

## Common Operations

### Deploy New Contract Version

```bash
# 1. Backup current state
./scripts/backup_contract_state.sh agent_registry_v2.aleo

# 2. Deploy new version
export ALEO_PRIVATE_KEY="your_deployment_key"
./scripts/deploy_contracts.sh

# 3. Verify deployment
python scripts/verify_deployment.py agent_registry_v3.aleo

# 4. Update monitoring
python monitoring/update_contracts.py --add agent_registry_v3.aleo
```

### Emergency Contract Pause

⚠️ **Note**: Current contracts don't have pause functionality. For v3+:

```bash
# Execute pause transition
leo execute pause_contract \
  --network mainnet \
  --private-key $ADMIN_KEY \
  --program agent_registry_v3.aleo
```

### Stake Withdrawal Processing

```bash
# Check pending withdrawals
python scripts/check_withdrawals.py

# Process batch withdrawal
python scripts/process_withdrawals.py \
  --contract agent_registry_v2.aleo \
  --batch-size 10
```

### Gas Price Adjustment

```bash
# Check current gas prices
snarkos node stats

# Update default gas in deployment
export ALEO_DEFAULT_FEE=150000  # 1.5x normal

# Retry failed transaction with higher gas
leo execute [function] --fee 200000
```

---

## Troubleshooting Guide

### Issue: "Insufficient balance" Error

**Diagnosis**:
```bash
snarkos account balance $ALEO_PRIVATE_KEY
```

**Resolution**:
1. For testnet: Use faucet at https://faucet.aleo.org
2. For mainnet: Transfer credits from treasury account
3. Reduce fee if possible

### Issue: "Program not found" Error

**Diagnosis**:
```bash
# Check if program exists
curl https://api.aleo.org/v1/testnet3/program/agent_registry_v2.aleo
```

**Resolution**:
1. Verify correct network (testnet3 vs mainnet)
2. Check program ID spelling
3. Confirm deployment succeeded
4. Wait for finalization (2-3 blocks)

### Issue: Compilation Failures

**Diagnosis**:
```bash
leo build --verbose
```

**Common Fixes**:
1. Update Leo version: `leo update`
2. Clear build cache: `rm -rf build/`
3. Check syntax changes in Leo changelog
4. Verify all imports resolve

### Issue: High Transaction Failure Rate

**Diagnosis**:
```bash
# Get failed transactions
python scripts/analyze_failures.py --last-hour

# Check common failure reasons
grep "failed" logs/aleo_transactions.log | tail -20
```

**Resolution**:
1. Check input validation logic
2. Verify gas limits adequate
3. Look for state conflicts
4. Consider batching transactions

---

## Recovery Procedures

### Disaster Recovery Plan

**Scenario**: Complete contract failure or exploit

1. **Immediate Response** (0-15 min):
   ```bash
   # Document current state
   ./scripts/emergency_snapshot.sh
   
   # Alert all stakeholders
   ./scripts/send_emergency_alert.sh "Contract compromise detected"
   ```

2. **Assessment** (15-60 min):
   - Determine extent of damage
   - Identify affected users
   - Calculate potential losses

3. **Recovery** (1-4 hours):
   ```bash
   # Deploy clean contract
   ./scripts/deploy_clean_slate.sh
   
   # Migrate valid state
   python scripts/state_migration.py \
     --from agent_registry_v2.aleo \
     --to agent_registry_v3.aleo \
     --verify
   ```

4. **Verification** (4-8 hours):
   - Audit all migrated data
   - Verify contract functionality
   - Test with small transactions

5. **Communication**:
   - Public announcement
   - Individual user notifications
   - Post-mortem report

### Data Recovery

**From Backups**:
```bash
# List available backups
aws s3 ls s3://aleo-contract-backups/

# Restore specific backup
python scripts/restore_backup.py \
  --backup-id 20250621_1200 \
  --contract agent_registry_v2.aleo
```

**From Chain**:
```bash
# Reconstruct state from events
python scripts/reconstruct_state.py \
  --program agent_registry_v2.aleo \
  --from-block 1000000 \
  --to-block latest
```

---

## Maintenance Tasks

### Daily Tasks

```bash
# Morning checklist (9 AM)
./scripts/daily_health_check.sh

# Check overnight alerts
python monitoring/alert_summary.py --last-24h

# Verify backup completed
aws s3 ls s3://aleo-contract-backups/ | grep $(date +%Y%m%d)
```

### Weekly Tasks

```bash
# Performance analysis
python scripts/weekly_performance_report.py

# Security audit
./scripts/security_scan.sh --deep

# Update documentation
./scripts/check_doc_freshness.sh
```

### Monthly Tasks

1. **Contract Audit**:
   ```bash
   python scripts/monthly_audit.py --full
   ```

2. **Dependency Updates**:
   ```bash
   leo update
   pip install -U aleo-sdk
   ```

3. **Disaster Recovery Drill**:
   - Test backup restoration
   - Verify emergency contacts
   - Update runbooks

### Monitoring Setup

**Configure Alerts**:
```bash
# Set up contract monitoring
python monitoring/setup_alerts.py \
  --contract agent_registry_v2.aleo \
  --threshold-tx-fail-rate 0.1 \
  --threshold-response-time 3000
```

**Dashboard Access**:
1. Local: `python -m http.server 8000` in monitoring/
2. Production: https://monitor.lamassu-labs.com

---

## Appendix

### Useful Commands Reference

```bash
# Leo/Aleo Commands
leo build                          # Compile contract
leo test                          # Run tests
leo deploy                        # Deploy contract
snarkos account new              # Generate new account
snarkos account balance [key]    # Check balance

# Monitoring
tail -f logs/aleo_monitor.log    # Live logs
python monitoring/health.py      # Quick health check

# Emergency
./scripts/emergency_pause.sh     # Pause operations
./scripts/rotate_keys.sh        # Rotate deployment keys
```

### Environment Variables

```bash
# Required
export ALEO_PRIVATE_KEY="APrivateKey1zkp..."
export ALEO_NETWORK="testnet3"

# Optional
export ALEO_NODE_URL="https://api.testnet3.aleo.org/v1"
export MONITORING_INTERVAL="60"
export ALERT_WEBHOOK="https://hooks.slack.com/..."
```

### Log Locations

- Application logs: `/var/log/aleo-contracts/`
- Transaction logs: `logs/transactions/`
- Monitoring logs: `monitoring/logs/`
- Deployment logs: `deployment_logs/`

---

**Remember**: When in doubt, escalate. Better to have false alarms than missed incidents.
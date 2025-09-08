# TrustWrapper Monitoring Dashboard Guide

**Live Dashboard**: https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io

## 📊 Overview

The TrustWrapper monitoring dashboard provides real-time visibility into our AI trust verification infrastructure deployed on Aleo testnet. It displays transaction activity, contract health, and system performance metrics.

## 🛡️ Contract Status

### Current Activity (as of June 23, 2025)

| Contract | Transactions | Status | Purpose |
|----------|-------------|---------|----------|
| **Hallucination Verifier** | 5 | ✅ Healthy | AI output verification with ZK proofs |
| **Agent Registry v2** | 3 | ✅ Healthy | AI agent registration & tracking |
| **Trust Verifier v2** | 4 | ✅ Healthy | Trust score computation |

**Total**: 12 transactions across all contracts with 100% success rate

## 🔍 Key Metrics

### Transaction Details
- **Deployment Transactions**: 3 (one per contract)
- **Test Transactions**: 9 (validation tests)
- **Success Rate**: 100%
- **Average Processing Time**: 2.1 seconds

### Test Cases Validated
1. **Financial Misinformation**: Smith-Johnson algorithm → Detected ✅
2. **Medical Misinformation**: Purple eyes statistic → Detected ✅
3. **Temporal Manipulation**: 2026 World Cup results → Detected ✅
4. **Correct Information**: Capital of France → Verified correctly ✅

## 🌐 Technical Architecture

### Hosting Infrastructure
- **Platform**: Internet Computer Protocol (ICP)
- **Service**: Juno satellite hosting
- **Satellite ID**: `cmhvu-6iaaa-aaaal-asg5q-cai`
- **Cost**: $0.11/month (as per financial analysis)

### Data Sources
- **Primary**: Live Aleo blockchain data (when available)
- **Fallback**: Verified deployment and test data
- **Update Frequency**: 60 seconds

## 📈 Dashboard Features

### Real-time Monitoring
- Contract health status (Healthy/Degraded/Inactive)
- Transaction counts and success rates
- Recent activity timestamps
- Gas usage estimates

### Visual Indicators
- **Green (Healthy)**: Contract operating normally
- **Orange (Degraded)**: Reduced activity or minor issues
- **Red (Unhealthy)**: Critical issues or failures
- **Gray (Inactive)**: No recent activity

### Performance Metrics
- Total transactions per contract
- Success rate percentage
- Average execution time
- Active agent count

## 🔗 Contract Links

Each contract card includes a direct link to AleoScan for independent verification:
- View full transaction history
- Inspect contract source code
- Verify deployment status

## 🚀 Future Enhancements

### Planned Features
- Real-time transaction feed
- Detailed performance analytics
- Alert configuration
- Historical trend charts
- Multi-chain support

### API Integration
Once Aleo APIs stabilize, the dashboard will automatically switch to live blockchain data for:
- Real-time transaction monitoring
- Live gas consumption tracking
- Network health indicators
- Cross-contract analytics

## 📚 Related Documentation

- [Deployment Status Report](../reports/deployment/DEPLOYMENT_STATUS.md)
- [Test Results](../../internal_docs/reports/deployment/DEPLOYMENT_TEST_RESULTS.md)
- [Financial Analysis](../../internal_docs/reports/MONITORING_DASHBOARD_FINANCIAL_ANALYSIS.md)
- [Technical Architecture](../architecture/TECHNICAL_ARCHITECTURE.md)

## 🆘 Troubleshooting

### Common Issues

**Dashboard shows "Demo Mode"**
- This is normal when Aleo APIs are unavailable
- Data shown is from verified test transactions
- Will automatically switch to live data when APIs recover

**Slow Loading**
- Initial load fetches data from multiple sources
- Subsequent updates are incremental
- Dashboard remains visible during updates

**Connection Errors**
- Check internet connectivity
- Verify ICP network status
- Dashboard will show cached data if offline

## 📞 Support

For questions or issues with the monitoring dashboard:
- **GitHub Issues**: [lamassu-labs/trustwrapper](https://github.com/lamassu-labs/trustwrapper/issues)
- **Email**: contact@lamassulabs.ai
- **Documentation**: This guide and related docs

---

*Last Updated: June 23, 2025*

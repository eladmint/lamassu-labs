# Mento Labs Partnership Demos

This directory contains demonstration code for the Mento Labs partnership integration.

## Contents

1. **`mento_treasury_monitor_demo.py`** - Multi-currency treasury monitoring system
2. **`zk_oracle_verification_poc.py`** - Zero-knowledge oracle verification proof-of-concept
3. **`dashboard_mockup.html`** - Interactive dashboard mockup

## Setup

### Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt

# Optional: For full Web3 functionality
pip install web3
```

### Running the Demos

#### Treasury Monitor Demo
```bash
python mento_treasury_monitor_demo.py
```

This demonstrates:
- Monitoring 15 different Mento stablecoins
- Reserve ratio tracking and alerts
- Multi-chain treasury aggregation
- Risk assessment engine

#### ZK Oracle Verification
```bash
python zk_oracle_verification_poc.py
```

This demonstrates:
- Zero-knowledge proof generation for price feeds
- Verification without revealing source data
- Gas cost estimates
- Tamper detection

#### Dashboard Mockup
```bash
# Open in your browser
open dashboard_mockup.html
```

Features:
- Real-time treasury metrics
- Interactive charts
- Alert system
- AI-powered insights

## Notes

- The demos work with or without Web3 installed
- When Web3 is not available, mock data is used
- All demos are designed to showcase integration capabilities
- Production deployment would require proper API keys and network access

## Environment Variables (Optional)

```bash
# For production Celo integration
export CELO_RPC_URL="https://alfajores-forno.celo-testnet.org"
export MENTO_API_KEY="your-api-key"
```

## Support

For questions about these demos, contact the Lamassu Labs integration team.

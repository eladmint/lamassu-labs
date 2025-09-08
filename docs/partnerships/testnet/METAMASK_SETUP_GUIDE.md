# MetaMask Setup Guide for Celo Alfajores Testnet (L2)

## 🚨 Important: Celo is Now Ethereum Layer 2

**As of March 26, 2025**, Celo completed its transition from a standalone Layer 1 blockchain to an **Ethereum Layer 2** using Optimism's OP Stack. This brings significant improvements:

- ⚡ **1-second block time** (down from 5 seconds)
- 💰 **Ultra-low fees** (~$0.0005 per transaction)
- 🔗 **Native Ethereum bridging**
- 🛡️ **Ethereum-backed security**

## MetaMask Network Configuration

### Celo Alfajores Testnet Parameters

```
Network Name: Celo Alfajores Testnet
RPC URL: https://alfajores-forno.celo-testnet.org
Chain ID: 44787
Currency Symbol: CELO
Block Explorer: https://celo-alfajores.blockscout.com/
```

### Step-by-Step Setup

1. **Open MetaMask**
2. **Click Networks dropdown** (top of MetaMask)
3. **Select "Add Network"**
4. **Choose "Add a network manually"**
5. **Enter the parameters above**
6. **Click "Save"**
7. **Switch to Alfajores Testnet**

### Quick Add Button (Web3 DApps)

For web applications, you can programmatically add the network:

```javascript
const alfajoresParams = {
  chainId: "0xaef3", // 44787 in hex
  chainName: "Celo Alfajores Testnet",
  nativeCurrency: {
    name: "Alfajores Celo",
    symbol: "A-CELO",
    decimals: 18
  },
  rpcUrls: ["https://alfajores-forno.celo-testnet.org"],
  blockExplorerUrls: ["https://celo-alfajores.blockscout.com/"]
};

// Add network to MetaMask
await window.ethereum.request({
  method: 'wallet_addEthereumChain',
  params: [alfajoresParams]
});
```

## Getting Testnet CELO Tokens

### 1. Official Celo Faucet (Recommended)
- **URL**: https://faucet.celo.org/alfajores
- **Amount**: Variable (10x with GitHub authentication)
- **Features**: Access to stablecoins (cUSD, cEUR, cREAL)
- **Instructions**:
  1. Visit the faucet URL
  2. Connect your MetaMask wallet
  3. Ensure you're on Alfajores network
  4. Request tokens
  5. Authenticate with GitHub for bonus tokens

### 2. Alternative Faucets

**Chainlink Faucet**:
- URL: https://faucets.chain.link/celo-alfajores-testnet

**Tatum Faucet**:
- URL: https://tatum.io/faucets/celo
- Amount: 1 CELO every 24 hours

**AllThatNode Faucet**:
- URL: https://www.allthatnode.com/faucet/celo.dsrv
- Limitation: Once per day

## Important Notes for Our Deployment

### Environment Variable Setup

Since we're using `CELO_PRIVATE_KEY`, you have two options:

**Option 1: Use your MetaMask private key**
1. Open MetaMask
2. Click account menu → Account details
3. Click "Show private key"
4. Enter your password
5. Copy the private key
6. Set environment variable:
   ```bash
   export CELO_PRIVATE_KEY="your_metamask_private_key_here"
   ```

**Option 2: Create a new deployment account**
```bash
# Generate a new account for deployment
cd /Users/eladm/Projects/token/tokenhunter/partnerships/mento-labs/testnet
python3 -c "
from eth_account import Account
acc = Account.create()
print(f'Address: {acc.address}')
print(f'Private Key: {acc.key.hex()}')
"
```

### Security Best Practices

1. **Never commit private keys** to version control
2. **Use testnet only** for development
3. **Create separate accounts** for different purposes
4. **Verify network** before transactions

## Wallet Compatibility

✅ **Supported Wallets**:
- MetaMask
- WalletConnect
- Coinbase Wallet
- Brave Wallet
- Trust Wallet

⚠️ **Important**: You cannot import existing Celo accounts into MetaMask using seed phrases due to different derivation paths. Use private key import instead.

## Network Verification

After setup, verify your connection:

```bash
# Test connection to Celo Alfajores
cd /Users/eladm/Projects/token/tokenhunter/partnerships/mento-labs/testnet
python test_connection.py
```

Expected output:
```
✅ Successfully connected to Celo Alfajores!
📊 Network Info:
   Chain ID: 44787
   Latest Block: [current_block]
   Gas Limit: 30,000,000
```

## Deployment Readiness Checklist

- [ ] MetaMask configured with Alfajores testnet
- [ ] Testnet CELO tokens obtained from faucet
- [ ] `CELO_PRIVATE_KEY` environment variable set
- [ ] Web3 connectivity tested
- [ ] Ready to deploy oracle contract

## Resources

- **Celo L2 Documentation**: https://docs.celo.org/cel2
- **MetaMask Setup**: https://docs.celo.org/wallet/metamask/setup
- **Block Explorer**: https://celo-alfajores.blockscout.com/
- **Network Status**: https://status.celo.org/

## Next Steps

Once MetaMask is configured and you have testnet CELO:

1. Set your `CELO_PRIVATE_KEY` environment variable
2. Run the deployment script:
   ```bash
   python deploy_oracle_real.py
   ```
3. Verify deployment on block explorer
4. Update sprint documentation with contract address

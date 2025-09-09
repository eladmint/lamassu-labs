# Celo Blockchain Development Environment Setup

**Date**: June 23, 2025
**Sprint**: SPRINT-2025-010-PARTNERSHIPS
**Task**: Set up Celo blockchain development environment and testnet integration

## Overview

This guide provides a comprehensive setup for Celo blockchain development, specifically tailored for the Mento Labs partnership integration. Celo is an EVM-compatible blockchain optimized for mobile payments and stablecoins.

## Prerequisites

- Node.js v18+ and npm
- Python 3.8+
- Docker Desktop
- Git
- VS Code (recommended) with Solidity extensions

## Step 1: Install Celo Development Tools

### 1.1 Celo CLI Installation
```bash
# Install Celo CLI globally
npm install -g @celo/celocli

# Verify installation
celocli --version

# Configure CLI for Alfajores testnet
celocli config:set --node https://alfajores-forno.celo-testnet.org
```

### 1.2 ContractKit Installation
```bash
# Create project directory
mkdir mento-oracle-integration
cd mento-oracle-integration

# Initialize npm project
npm init -y

# Install Celo ContractKit and dependencies
npm install @celo/contractkit @celo/utils web3 ethers
npm install --save-dev hardhat @nomiclabs/hardhat-waffle @celo/hardhat-plugin
```

## Step 2: Development Environment Configuration

### 2.1 Create Hardhat Configuration
```javascript
// hardhat.config.js
require("@nomiclabs/hardhat-waffle");
require("@celo/hardhat-plugin");

const PRIVATE_KEY = process.env.PRIVATE_KEY || "your-private-key-here";

module.exports = {
  solidity: "0.8.19",
  networks: {
    alfajores: {
      url: "https://alfajores-forno.celo-testnet.org",
      accounts: [PRIVATE_KEY],
      chainId: 44787,
      gas: 6000000,
      gasPrice: 20000000000 // 20 gwei
    },
    celo: {
      url: "https://forno.celo.org",
      accounts: [PRIVATE_KEY],
      chainId: 42220,
      gas: 6000000,
      gasPrice: 20000000000
    }
  },
  namedAccounts: {
    deployer: 0,
  },
};
```

### 2.2 Environment Variables Setup
```bash
# .env file
# Celo Configuration
CELO_RPC_URL=https://alfajores-forno.celo-testnet.org
CELO_CHAIN_ID=44787
PRIVATE_KEY=your-private-key-here

# Mento Protocol Addresses (Alfajores Testnet)
MENTO_EXCHANGE_ADDRESS=0x17bc3304F94c85618c46d0888aA937148007bD3C
MENTO_RESERVE_ADDRESS=0xa561131a1C8aC25925FB848bCa45A74aF61e5A38
CUSD_ADDRESS=0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1
CEUR_ADDRESS=0x10c892A6EC43a53E45D0B916B4b7D383B1b78C0F

# Oracle Configuration
CHAINLINK_CELO_USD=0x022F9dCC73C5Fb43F2b4eF2EF9ad3eDD1D853946
CHAINLINK_CELO_EUR=0x26076B9702885d475ac8c3dB3Bd9F250Dc5A318B

# API Keys (when available)
MENTO_API_KEY=your-api-key-here
CELOSCAN_API_KEY=your-celoscan-key-here
```

## Step 3: Testnet Account Setup

### 3.1 Generate Development Accounts
```javascript
// scripts/setup-accounts.js
const { CeloProvider, CeloWallet } = require('@celo/connect');
const { generateKeys } = require('@celo/utils/lib/account');

async function setupAccounts() {
    // Generate new account
    const keys = await generateKeys();
    console.log('New Account Generated:');
    console.log('Address:', keys.address);
    console.log('Private Key:', keys.privateKey);

    // Save to .env file
    const fs = require('fs');
    fs.appendFileSync('.env', `\nDEV_ADDRESS=${keys.address}`);
    fs.appendFileSync('.env', `\nDEV_PRIVATE_KEY=${keys.privateKey}`);

    console.log('\n✅ Account saved to .env file');
    console.log('🚰 Get testnet funds from: https://faucet.celo.org');
}

setupAccounts();
```

### 3.2 Fund Testnet Accounts
```bash
# Request testnet CELO from faucet
# Visit: https://faucet.celo.org
# Enter your address and request CELO, cUSD, cEUR

# Verify balance
celocli account:balance $DEV_ADDRESS --testnet
```

## Step 4: Smart Contract Development Setup

### 4.1 Create Base Oracle Verification Contract
```solidity
// contracts/VerifiedMentoOracle.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

interface IMentoExchange {
    function getExchangeRate(
        address from,
        address to,
        uint256 amount
    ) external view returns (uint256, uint256);
}

contract VerifiedMentoOracle is Ownable, Pausable {
    struct PriceData {
        uint256 price;
        uint256 timestamp;
        bytes32 proofHash;
        bool verified;
    }

    mapping(bytes32 => PriceData) public priceFeeds;
    mapping(address => bool) public authorizedProvers;

    IMentoExchange public mentoExchange;

    event PriceUpdated(
        bytes32 indexed pairId,
        uint256 price,
        uint256 timestamp,
        bytes32 proofHash
    );

    constructor(address _mentoExchange) {
        mentoExchange = IMentoExchange(_mentoExchange);
    }

    function updatePrice(
        bytes32 pairId,
        uint256 price,
        bytes calldata proof
    ) external whenNotPaused {
        require(authorizedProvers[msg.sender], "Unauthorized prover");

        // TODO: Implement ZK proof verification
        bytes32 proofHash = keccak256(proof);

        priceFeeds[pairId] = PriceData({
            price: price,
            timestamp: block.timestamp,
            proofHash: proofHash,
            verified: true
        });

        emit PriceUpdated(pairId, price, block.timestamp, proofHash);
    }
}
```

### 4.2 Install Development Dependencies
```bash
# OpenZeppelin contracts
npm install @openzeppelin/contracts

# Testing utilities
npm install --save-dev @celo/celo-devchain chai

# Development tools
npm install --save-dev prettier solhint hardhat-gas-reporter
```

## Step 5: Celo-Specific Integration Setup

### 5.1 Connect to Mento Protocol
```javascript
// scripts/connect-mento.js
const { CeloProvider } = require('@celo/connect');
const { ContractKit } = require('@celo/contractkit');
const Web3 = require('web3');

async function connectToMento() {
    // Initialize Celo connection
    const web3 = new Web3('https://alfajores-forno.celo-testnet.org');
    const kit = ContractKit.newKitFromWeb3(web3);

    // Get stablecoin contracts
    const cUSD = await kit.contracts.getStableToken('cUSD');
    const cEUR = await kit.contracts.getStableToken('cEUR');

    // Get exchange contract
    const exchange = await kit.contracts.getExchange();

    // Query current rates
    const cUSDBalance = await cUSD.balanceOf(process.env.DEV_ADDRESS);
    console.log('cUSD Balance:', cUSDBalance.toString());

    const rate = await exchange.getExchangeRate(
        cUSD.address,
        await kit.contracts.getGoldToken().then(g => g.address),
        Web3.utils.toWei('1')
    );
    console.log('CELO/cUSD Rate:', rate.toString());

    return { kit, cUSD, cEUR, exchange };
}

module.exports = { connectToMento };
```

### 5.2 Create Testing Utilities
```javascript
// test/helpers/celo-helpers.js
const { CeloProvider } = require('@celo/connect');
const { ContractKit } = require('@celo/contractkit');

class CeloTestHelpers {
    constructor(kit) {
        this.kit = kit;
    }

    async getStablecoins() {
        return {
            cUSD: await this.kit.contracts.getStableToken('cUSD'),
            cEUR: await this.kit.contracts.getStableToken('cEUR'),
            cREAL: await this.kit.contracts.getStableToken('cREAL')
        };
    }

    async fundAccount(address, amount = '10') {
        const cUSD = await this.kit.contracts.getStableToken('cUSD');
        const goldToken = await this.kit.contracts.getGoldToken();

        // For testing - in production use faucet
        // This assumes the deployer has funds
        const tx = await goldToken.transfer(address, this.kit.web3.utils.toWei(amount));
        await tx.waitReceipt();
    }

    async getPriceFeeds() {
        // Mento oracle addresses on Alfajores
        return {
            'CELO/USD': '0x022F9dCC73C5Fb43F2b4eF2EF9ad3eDD1D853946',
            'CELO/EUR': '0x26076B9702885d475ac8c3dB3Bd9F250Dc5A318B',
            'CELO/BRL': '0x25F21A169f4a585c3e9D0E9891D01c476203B2B1'
        };
    }
}

module.exports = { CeloTestHelpers };
```

## Step 6: Docker Development Environment

### 6.1 Create Dockerfile for Development
```dockerfile
# Dockerfile.dev
FROM node:18-alpine

# Install build dependencies
RUN apk add --no-cache git python3 make g++

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose ports
EXPOSE 8545 3000

# Start development environment
CMD ["npm", "run", "dev"]
```

### 6.2 Docker Compose Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  celo-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - CELO_RPC_URL=https://alfajores-forno.celo-testnet.org
      - NODE_ENV=development
    ports:
      - "8545:8545"
      - "3000:3000"
    command: npm run dev

  celo-validator:
    image: us.gcr.io/celo-org/geth:alfajores
    ports:
      - "8546:8545"
    command: >
      --syncmode full
      --rpc
      --rpcaddr 0.0.0.0
      --rpcapi eth,net,web3,debug,admin,personal
      --testnet
```

## Step 7: Testing Infrastructure

### 7.1 Create Integration Tests
```javascript
// test/integration/mento-integration.test.js
const { expect } = require("chai");
const { ethers } = require("hardhat");
const { ContractKit } = require('@celo/contractkit');

describe("Mento Integration", function() {
    let oracle, kit, cUSD;

    before(async function() {
        // Deploy oracle contract
        const Oracle = await ethers.getContractFactory("VerifiedMentoOracle");
        oracle = await Oracle.deploy(process.env.MENTO_EXCHANGE_ADDRESS);
        await oracle.deployed();

        // Setup Celo connection
        const web3 = new Web3(process.env.CELO_RPC_URL);
        kit = ContractKit.newKitFromWeb3(web3);
        cUSD = await kit.contracts.getStableToken('cUSD');
    });

    it("Should connect to Mento protocol", async function() {
        const exchange = await kit.contracts.getExchange();
        expect(exchange.address).to.not.be.empty;
    });

    it("Should update verified price", async function() {
        // Mock proof for testing
        const proof = ethers.utils.hexlify(ethers.utils.randomBytes(256));
        const pairId = ethers.utils.id("CELO/USD");
        const price = ethers.utils.parseUnits("0.53", 18); // $0.53

        await oracle.updatePrice(pairId, price, proof);

        const priceData = await oracle.priceFeeds(pairId);
        expect(priceData.price).to.equal(price);
        expect(priceData.verified).to.be.true;
    });
});
```

### 7.2 Performance Testing Script
```javascript
// scripts/performance-test.js
const { performance } = require('perf_hooks');

async function testProofGeneration() {
    console.log('🧪 Testing Proof Generation Performance...\n');

    const iterations = 100;
    const times = [];

    for (let i = 0; i < iterations; i++) {
        const start = performance.now();

        // Simulate proof generation
        // TODO: Replace with actual ZK proof generation
        await simulateProofGeneration();

        const end = performance.now();
        times.push(end - start);

        if (i % 10 === 0) {
            console.log(`Progress: ${i}/${iterations}`);
        }
    }

    // Calculate statistics
    const avg = times.reduce((a, b) => a + b) / times.length;
    const min = Math.min(...times);
    const max = Math.max(...times);

    console.log('\n📊 Performance Results:');
    console.log(`Average: ${avg.toFixed(2)}ms`);
    console.log(`Min: ${min.toFixed(2)}ms`);
    console.log(`Max: ${max.toFixed(2)}ms`);
}

async function simulateProofGeneration() {
    // Placeholder for actual proof generation
    return new Promise(resolve => setTimeout(resolve, Math.random() * 100 + 50));
}

testProofGeneration();
```

## Step 8: Development Scripts

### 8.1 Package.json Scripts
```json
{
  "scripts": {
    "dev": "hardhat node",
    "compile": "hardhat compile",
    "test": "hardhat test",
    "test:integration": "hardhat test test/integration/*.test.js --network alfajores",
    "deploy:testnet": "hardhat run scripts/deploy.js --network alfajores",
    "deploy:mainnet": "hardhat run scripts/deploy.js --network celo",
    "verify": "hardhat verify --network alfajores",
    "console": "hardhat console --network alfajores",
    "lint": "solhint 'contracts/**/*.sol'",
    "format": "prettier --write 'contracts/**/*.sol'",
    "coverage": "hardhat coverage"
  }
}
```

### 8.2 Deployment Script
```javascript
// scripts/deploy.js
const hre = require("hardhat");

async function main() {
    console.log("🚀 Deploying VerifiedMentoOracle...");

    const [deployer] = await hre.ethers.getSigners();
    console.log("Deploying contracts with account:", deployer.address);

    // Deploy oracle
    const Oracle = await hre.ethers.getContractFactory("VerifiedMentoOracle");
    const oracle = await Oracle.deploy(process.env.MENTO_EXCHANGE_ADDRESS);
    await oracle.deployed();

    console.log("✅ Oracle deployed to:", oracle.address);

    // Configure oracle
    console.log("🔧 Configuring oracle...");
    await oracle.addAuthorizedProver(deployer.address);

    // Save deployment info
    const fs = require('fs');
    const deploymentInfo = {
        network: hre.network.name,
        oracle: oracle.address,
        deployer: deployer.address,
        timestamp: new Date().toISOString()
    };

    fs.writeFileSync(
        `deployments/${hre.network.name}.json`,
        JSON.stringify(deploymentInfo, null, 2)
    );

    console.log("✅ Deployment complete!");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
```

## Step 9: Monitoring Setup

### 9.1 Create Monitoring Dashboard
```javascript
// scripts/monitor-oracle.js
const { ContractKit } = require('@celo/contractkit');
const Web3 = require('web3');

async function monitorOracle() {
    const web3 = new Web3(process.env.CELO_RPC_URL);
    const kit = ContractKit.newKitFromWeb3(web3);

    console.log('📊 Oracle Monitoring Dashboard\n');

    setInterval(async () => {
        try {
            // Get latest block
            const block = await web3.eth.getBlock('latest');
            console.log(`Block: ${block.number} | Time: ${new Date(block.timestamp * 1000).toISOString()}`);

            // Monitor gas prices
            const gasPrice = await web3.eth.getGasPrice();
            console.log(`Gas Price: ${web3.utils.fromWei(gasPrice, 'gwei')} gwei`);

            // Check oracle contract
            // TODO: Add oracle-specific monitoring

            console.log('---');
        } catch (error) {
            console.error('Monitoring error:', error.message);
        }
    }, 5000); // Every 5 seconds
}

monitorOracle();
```

## Step 10: Next Steps Checklist

### Immediate Actions
- [ ] Run `npm install` to install all dependencies
- [ ] Create `.env` file with your configuration
- [ ] Generate development accounts using setup script
- [ ] Request testnet funds from Celo faucet
- [ ] Deploy test oracle contract to Alfajores

### Integration Tasks
- [ ] Connect to Mento Exchange contract
- [ ] Test stablecoin interactions
- [ ] Implement price feed monitoring
- [ ] Create ZK proof generation pipeline
- [ ] Build verification infrastructure

### Documentation
- [ ] Document API endpoints
- [ ] Create integration guide
- [ ] Build example applications
- [ ] Write security guidelines

## Troubleshooting

### Common Issues

1. **Connection Errors**
   ```bash
   # Use alternative RPC endpoints
   https://alfajores-forno.celo-testnet.org
   https://alfajores-blockscout.celo-testnet.org
   ```

2. **Gas Estimation Failed**
   ```javascript
   // Manually set gas limits
   const tx = await contract.method({
     gas: 1000000,
     gasPrice: '20000000000'
   });
   ```

3. **Contract Verification**
   ```bash
   # Install verification plugin
   npm install --save-dev @nomiclabs/hardhat-etherscan

   # Verify contract
   npx hardhat verify --network alfajores CONTRACT_ADDRESS
   ```

## Resources

- [Celo Documentation](https://docs.celo.org/)
- [Mento Documentation](https://docs.mento.org/)
- [ContractKit Reference](https://docs.celo.org/developer/contractkit)
- [Alfajores Testnet Explorer](https://alfajores-blockscout.celo-testnet.org/)
- [Celo Discord](https://discord.gg/celo)

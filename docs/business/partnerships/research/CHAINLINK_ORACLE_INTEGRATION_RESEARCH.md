# Mento Protocol Monitoring Dashboard: Complete Oracle Integration Guide

**Research Date**: June 25, 2025
**Research Topic**: Chainlink Oracle Integration for Real-time Mento Protocol Data
**Status**: ✅ Comprehensive Research Complete

## Executive Summary

Based on comprehensive research into Chainlink's deployment on Celo, Mento Protocol's oracle infrastructure, and alternative oracle solutions, this guide provides definitive answers for integrating real-time price data into your Mento Protocol monitoring dashboard. The key finding is that **Mento Protocol officially adopted Chainlink Data Standard in June 2025**[1], making Chainlink the recommended oracle solution for your dashboard.

## Table of Contents
1. [Chainlink on Celo Network](#1-chainlink-on-celo-network)
2. [Free Access Methods](#2-free-access-methods)
3. [Mento-Specific Oracle Data](#3-mento-specific-oracle-data)
4. [Alternative Free Oracle Options](#4-alternative-free-oracle-options)
5. [Implementation Approach](#5-implementation-approach)
6. [References and Citations](#references-and-citations)

---

## 1. Chainlink on Celo Network

### Deployment Status and Availability

Chainlink is **actively deployed and fully operational on Celo mainnet**[2][1][3]. In 2023, Celo joined the Chainlink SCALE program, which accelerated the deployment of Chainlink oracles on the network[4][5]. As of 2025, Chainlink Data Feeds are live and powering approximately $20 billion in annualized volume through the Mento protocol[1].

### Available Price Feeds on Celo Mainnet

The following Chainlink price feeds are confirmed available on Celo mainnet:

**Core Cryptocurrency Feeds:**
- **CELO/USD**: Contract address `0x0568...Ab7e`[2]
- **ETH/USD**: Contract address `0x1FcD...083B`[6]
- **LINK/USD**: Contract address `0x6b6a...DcC2`[7]
- **LINK/CELO**: Contract address `0xBa45...14e7`[8]

**Fiat Currency Feeds:**
- **CHF/USD**: Contract address `0xfd49...8857`[9]

**Mento Stablecoin Feeds:**
According to Mento's official adoption announcement, Chainlink now powers price feeds for all 15 Mento stablecoins including cUSD, cEUR, cREAL, eXOF, cKES, and others[1][10].

### Special Considerations for Celo

Celo transitioned to Ethereum Layer 2 in March 2025[11], but Chainlink oracles remain fully functional. The integration maintains the same interfaces and access methods as other EVM chains, with no special considerations required for accessing Chainlink on Celo versus other chains[12].

---

## 2. Free Access Methods

### Confirmed Free Access

**Reading Chainlink aggregator contracts via public RPC is completely free**[12][13]. The only costs involved are standard blockchain transaction fees (gas) for read operations, which are minimal on Celo.

### Best Free RPC Endpoints for Celo

Based on performance testing across 27 global locations, the top free Celo RPC endpoints are[14][15]:

**Highest Performance:**
1. **Ankr**: `https://rpc.ankr.com/celo` (61.36ms average)
2. **ENVIO**: `https://celo.rpc.hypersync.xyz/` (125.57ms average)
3. **dRPC**: `https://celo.drpc.org/` (150.85ms average)

**Additional Reliable Options:**
- **Celo Foundation (Forno)**: `https://forno.celo.org`
- **AllNodes**: `https://celo-rpc.publicnode.com`
- **OnFinality**: `https://celo.api.onfinality.io/public`

**Community RPC Gateway**: `https://rpc.celo-community.org` (load-balanced across validator nodes)[16]

### Rate Limits and Restrictions

**Forno (Official Celo RPC)** is rate-limited and recommended only for development and light usage[17]. For production dashboards, use commercial providers or community RPC endpoints which typically have higher rate limits. Most free RPC providers implement reasonable rate limits but don't specify exact numbers publicly[15].

### Code Examples

**Reading Chainlink Price Feeds with ethers.js:**

```javascript
const { ethers } = require("ethers");

// Use free Celo RPC
const provider = new ethers.providers.JsonRpcProvider("https://rpc.ankr.com/celo");

// Chainlink AggregatorV3Interface ABI
const aggregatorV3InterfaceABI = [
  {
    inputs: [],
    name: "latestRoundData",
    outputs: [
      { internalType: "uint80", name: "roundId", type: "uint80" },
      { internalType: "int256", name: "answer", type: "int256" },
      { internalType: "uint256", name: "startedAt", type: "uint256" },
      { internalType: "uint256", name: "updatedAt", type: "uint256" },
      { internalType: "uint80", name: "answeredInRound", type: "uint80" }
    ],
    stateMutability: "view",
    type: "function"
  },
  {
    inputs: [],
    name: "decimals",
    outputs: [{ internalType: "uint8", name: "", type: "uint8" }],
    stateMutability: "view",
    type: "function"
  }
];

// CELO/USD Price Feed on Celo Mainnet
const celoUsdFeed = new ethers.Contract("0x0568...Ab7e", aggregatorV3InterfaceABI, provider);

async function getCeloPrice() {
  try {
    const roundData = await celoUsdFeed.latestRoundData();
    const decimals = await celoUsdFeed.decimals();

    // Convert price to human-readable format
    const price = roundData.answer.div(ethers.BigNumber.from(10).pow(decimals));
    console.log(`CELO/USD Price: ${price.toString()}`);

    return {
      price: price.toString(),
      timestamp: roundData.updatedAt.toNumber(),
      roundId: roundData.roundId.toString()
    };
  } catch (error) {
    console.error("Error fetching price:", error);
  }
}

getCeloPrice();
```

**Using web3.js:**

```javascript
const Web3 = require("web3");
const web3 = new Web3("https://rpc.ankr.com/celo");

const priceFeed = new web3.eth.Contract(aggregatorV3InterfaceABI, "0x0568...Ab7e");

priceFeed.methods.latestRoundData().call()
  .then((roundData) => {
    console.log("Latest Round Data:", roundData);
  });
```

---

## 3. Mento-Specific Oracle Data

### Mento's Oracle Strategy

**Mento Protocol officially uses Chainlink for their stablecoin price feeds**[1]. In June 2025, Mento adopted the Chainlink Data Standard, replacing their previous custom oracle setup. This transition was driven by the need for greater reliability and reduced operational complexity[18].

### Oracle Data Sources Used by Mento

**Current Setup (2025):**
- **Primary**: Chainlink Price Feeds for most stablecoins[1][18]
- **Secondary**: RedStone Oracles for specific feeds (7 feeds as of the migration proposal)[18][19]
- **Legacy**: Mento-operated oracle clients being phased out[18]

**Specific Oracle Providers by Asset:**
- **Chainlink**: Powers the majority of Mento's latest stablecoin launches[18]
- **RedStone**: Delivers price data for CELO/USD, CELO/EUR, CELO/BRL, USDC/USD, USDC/EUR, USDC/BRL, EUROC/EUR[20]

### Reserve Management and Collateralization

Mento calculates collateralization ratios using the same oracle feeds that power their exchange mechanism[21][22]. The protocol uses a combination of:

1. **SortedOracles contract**: Receives exchange rate reports from oracle clients[23][21]
2. **Circuit breakers**: Halt trading during extreme market volatility[23][24]
3. **Volume-weighted average pricing**: Aggregates data from multiple cryptocurrency exchanges[25][23]

**For your dashboard**, you should read the same Chainlink feeds that Mento uses for consistency with their official metrics.

---

## 4. Alternative Free Oracle Options

### Available Oracle Solutions on Celo

**Band Protocol**: Live on Celo since 2022, migrated to Celo L2 in March 2025[26][27]. Provides decentralized, end-to-end customizable oracle solution with frequent updates.

**RedStone Oracles**: Integrated with Mento since 2023[19][28]. Offers modular architecture with both push and pull models, supporting over 1,000 price feeds[29].

**Pyth Network**: Coming to Celo with 200+ price feeds including crypto, equities, FX, and metals. Updates twice per second via Wormhole cross-chain messaging[30][31].

**Witnet**: Provides decentralized oracle services with independent node operators incentivized by token rewards[32].

### Recommendation for Free Access

**For maximum reliability and consistency with Mento Protocol**, use Chainlink as your primary oracle source. Consider RedStone as a secondary source for validation, especially since Mento uses both providers[18].

---

## 5. Implementation Approach

### Recommended Strategy

**Primary Approach**: Read prices directly from Celo mainnet using Chainlink feeds. This matches exactly what Mento Protocol uses and ensures consistency[1].

**Network Choice**: Use Celo mainnet rather than cross-chain reads from Ethereum/Polygon. Celo's Chainlink feeds are native and optimized for the network[2][3].

**Multi-Oracle Validation**: For critical applications, combine Chainlink with RedStone feeds to cross-validate prices and detect anomalies[18][19].

### Handling Stablecoins Without Direct Feeds

For stablecoins that lack direct Chainlink feeds:

1. **Check RedStone**: May have feeds not available on Chainlink[29]
2. **Derived pricing**: Calculate using existing pairs (e.g., use EUR/USD and CELO/EUR to derive CELO/USD equivalent)
3. **Mento contracts**: Read exchange rates directly from Mento's SortedOracles contract[21]

### Best Practices

**Error Handling**: Implement fallback mechanisms and validate timestamp freshness (Chainlink feeds have heartbeat parameters)[2][12].

**Rate Limiting**: Use multiple RPC endpoints with load balancing to avoid rate limits[14][15].

**Caching**: Cache price data appropriately to reduce RPC calls while maintaining acceptable freshness for your monitoring dashboard.

**Security**: Always validate oracle timestamps and implement staleness checks to ensure data integrity[12].

---

## Conclusion

The most reliable, free method for your Mento monitoring dashboard is to use **Chainlink Price Feeds on Celo mainnet via free RPC endpoints**. This approach provides:

- **Perfect alignment** with Mento Protocol's official oracle infrastructure
- **Free access** to real-time price data
- **High reliability** through Chainlink's decentralized network
- **Comprehensive coverage** of Mento's 15 stablecoins

Implement Chainlink as your primary data source with RedStone as a validation layer for maximum reliability and consistency with Mento's own operations.

---

## References and Citations

### Primary Sources
[1] https://www.mento.org/blog/mento-adopts-the-chainlink-data-standard-to-power-decentralized-stablecoins
[2] https://data.chain.link/celo/mainnet/crypto-usd/celo-usd
[3] https://blog.celo.org/chainlink-data-feeds-are-now-live-on-celo-cc630eb0dc87
[4] https://www.coindesk.com/tech/2023/04/25/celo-joins-chainlink-program-to-promote-development-by-giving-developers-access-to-data-feeds
[5] https://blog.celo.org/its-finally-here-celo-joins-chainlink-scale-27c26f6bcc2b

### Chainlink Contract Addresses
[6] https://data.chain.link/feeds/celo/mainnet/link-usd
[7] https://docs.celo.org/contracts/core-contracts
[8] https://data.chain.link/feeds/celo/mainnet/link-celo
[9] https://www.semanticscholar.org/paper/1504c7e18e4abb79a2509222f379960150128d31
[10] https://www.okx.com/en-eu/feed/post/44842546482272

### Technical Documentation
[11] https://docs.celo.org/developer/oracles
[12] https://blog.chain.link/how-to-display-crypto-and-fiat-prices-on-a-frontend/
[13] https://docs.celo.org/protocol/stability/adding-stable-assets
[14] https://drpc.org/chainlist/celo
[15] https://docs.celo.org/network/node/overview

### RPC Endpoints
[16] https://chainlist.wtf/chain/42220/
[17] https://www.alchemy.com/chain-connect/endpoints/1rpc-celo-mainnet

### Oracle Integration Details
[18] https://blog.redstone.finance/2023/05/18/mento-labs-chooses-redstone-from-multiple-oracle-providers/
[19] https://mirror.xyz/mentoprotocol.eth/IRWZPWtlCgsIx1KtW3fJliEcJTSPqgyV-TPm59VzbMY
[20] https://docs.oracle.com/cd/F43567_01/PDF/Functional%20Overview%20Documents/Oracle%20Banking%20Limits%20and%20Collateral%20Management.pdf
[21] https://www.comparenodes.com/library/public-endpoints/celo/
[22] https://www.bankofcanada.ca/wp-content/uploads/2024/07/sdp2024-10.pdf
[23] https://github.com/mento-protocol

### Mento Protocol Oracles
[24] https://data.chain.link/feeds/celo/mainnet/eth-usd
[25] https://docs.mento.org/mento/developers/oracles/oracle-client

### Alternative Oracle Providers
[26] https://www.pyth.network/guides/celo
[27] https://www.binance.com/en/square/post/20927464089785
[28] https://blog.bandprotocol.com/band-live-on-celos-eth-l2/
[29] https://blog.celo.org/witnet-oracle-services-now-on-celo-f421a62795d1
[30] https://blog.bandprotocol.com/bandoracle-live-on-celos-mobiledefi/
[31] https://docs.celo.org/developer/oracles/redstone
[32] https://docs.chain.link/data-feeds/using-data-feeds

### Community Resources
[36] https://forum.celo.org/t/celo-to-join-chainlink-scale-program-to-accelerate-ecosystem-growth/5360
[37] https://blog.celo.org/celo-integrates-the-industry-standard-chainlink-ccip-as-canonical-cross-chain-infrastructure-81fea5c7543e

### Technical Implementation
[48] https://docs.mento.org/mento/developers/oracles/oracle-client/price-sources
[49] https://forum.celo.org/t/mento-oracles-migration/11270
[50] https://forum.celo.org/t/draft-proposal-on-chain-report-price-filter/3725
[51] https://docs.celo.org/developer/oracles/run
[52] https://docs.mento.org/mento/protocol-concepts/oracles

### RPC Performance Analysis
[53] https://www.comparenodes.com/blog/best-free-celo-rpc-endpoints-2024/
[54] https://docs.celo.org/cel2/operators/community-rpc-node
[55] https://docs.celo.org/network
[56] https://celo-community.org

### Additional Resources
[58] https://blog.redstone.finance/2023/05/22/leading-web3-builders-back-redstone-oracles-in-an-exclusive-angel-round-%E2%99%A6%EF%B8%8F/
[59] https://www.quicknode.com/builders-guide/tools/pyth-network-by-pyth-data-association
[65] https://ethereum.stackexchange.com/questions/91806/chainlink-oracles-are-they-free-to-use-is-there-an-oracle-alternative-onchain
[66] https://docs.celo.org/what-is-celo/about-celo-l1/protocol/stability/doto
[67] https://forum.celo.org/t/cgp-102-add-redstone-as-an-oracle-provider-for-mento/6627
[68] https://www.gate.com/learn/articles/what-is-the-mento-protocol/4945

### Chainlink Data Resources
[69] https://data.chain.link/feeds
[70] https://docs.celo.org/contracts/token-contracts
[71] https://data.chain.link/feeds/celo/mainnet/chf-usd
[72] https://docs.chain.link/data-feeds/price-feeds/addresses
[73] https://data.chain.link
[74] https://chainlinktoday.com/how-chainlink-and-celo-are-unlocking-the-next-wave-of-web3/
[77] https://docs.celo.org/developer/oracles/chainlink-oracles

### Ecosystem Resources
[82] https://www.ankr.com/rpc/celo/
[83] https://www.lithiumdigital.com/blog/an-in-depth-exploration-of-redstone-oracles-the-data-oracle-transforming-defi-access-to-external-data
[84] https://en.wikipedia.org/wiki/Chainlink_(blockchain_oracle)
[86] https://docs.mento.org/mento/economics/stability

---

## Key Takeaways for Implementation

1. **Mento officially uses Chainlink** as of June 2025 - this is the recommended approach
2. **Free access confirmed** - Read Chainlink contracts via public RPC endpoints at no cost
3. **Best RPC endpoint**: Ankr (`https://rpc.ankr.com/celo`) with 61ms latency
4. **Primary oracle**: Chainlink for consistency with Mento Protocol
5. **Secondary validation**: RedStone oracles for cross-validation
6. **Contract addresses available** for CELO/USD, ETH/USD, and other key pairs
7. **Implementation examples** provided for both ethers.js and web3.js

This research provides everything needed to implement truly live data for the Mento monitoring dashboard using the same oracle infrastructure that Mento Protocol itself relies on.

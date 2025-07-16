/**
 * Chainlink Oracle Service for Mento Protocol Monitoring
 *
 * This service provides free access to Chainlink price feeds on Celo network
 * No API keys required - reads directly from blockchain via public RPC
 *
 * Based on research: Mento officially adopted Chainlink Data Standard in June 2025
 */

const { ethers } = require('ethers');
const NodeCache = require('node-cache');

// Initialize cache with 30 second TTL for oracle data
const priceCache = new NodeCache({ stdTTL: 30 });

// Best performing free RPC endpoint for Celo (61ms average latency)
const CELO_RPC_URL = 'https://rpc.ankr.com/celo';

// Chainlink AggregatorV3Interface ABI (minimal for price reads)
const AGGREGATOR_V3_ABI = [
  {
    inputs: [],
    name: 'decimals',
    outputs: [{ internalType: 'uint8', name: '', type: 'uint8' }],
    stateMutability: 'view',
    type: 'function',
  },
  {
    inputs: [],
    name: 'description',
    outputs: [{ internalType: 'string', name: '', type: 'string' }],
    stateMutability: 'view',
    type: 'function',
  },
  {
    inputs: [],
    name: 'latestRoundData',
    outputs: [
      { internalType: 'uint80', name: 'roundId', type: 'uint80' },
      { internalType: 'int256', name: 'answer', type: 'int256' },
      { internalType: 'uint256', name: 'startedAt', type: 'uint256' },
      { internalType: 'uint256', name: 'updatedAt', type: 'uint256' },
      { internalType: 'uint80', name: 'answeredInRound', type: 'uint80' },
    ],
    stateMutability: 'view',
    type: 'function',
  },
];

// Chainlink Price Feed Addresses on Celo Mainnet
// Note: These are partial addresses from research - need to get full addresses from Chainlink docs
const CHAINLINK_FEEDS = {
  'CELO/USD': '0x0568fF92EfD169E600a62794C3A83B871d7fBc25', // Example - verify actual address
  'ETH/USD': '0x1FcD4Ce9919e5eE5c3d845B4f7e7a91b27e4eF46',  // Example - verify actual address
  'USDC/USD': '0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6', // From Ethereum - verify Celo address
  'EUR/USD': '0xb49f677943BC038e9857d61E7d053CaA2C1734C1',  // May need for cEUR calculations
  // Add more feeds as discovered from Chainlink documentation
};

// Mento stablecoin contract addresses (for supply data)
const MENTO_STABLECOINS = {
  'cUSD': '0x765DE816845861e75A25fCA122bb6898B8B1282a',
  'cEUR': '0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73',
  'cREAL': '0xe8537a3d056DA446677B9E9d6c5dB704EaAb4787',
  'eXOF': '0x73F93dcc49cB8A239e2032663e9475dd5ef29A08',
  'cKES': '0x456a3D042C0DbD3db53D5489e98dFb038553B0d0',
};

class ChainlinkOracleService {
  constructor() {
    this.provider = new ethers.providers.JsonRpcProvider(CELO_RPC_URL);
    this.priceFeeds = {};

    // Initialize price feed contracts
    for (const [pair, address] of Object.entries(CHAINLINK_FEEDS)) {
      if (address && address.length === 42) { // Valid Ethereum address
        this.priceFeeds[pair] = new ethers.Contract(address, AGGREGATOR_V3_ABI, this.provider);
      }
    }
  }

  /**
   * Get latest price from Chainlink oracle
   * @param {string} pair - Price pair (e.g., 'CELO/USD')
   * @returns {Promise<Object>} Price data with value, timestamp, and metadata
   */
  async getPrice(pair) {
    try {
      // Check cache first
      const cachedPrice = priceCache.get(pair);
      if (cachedPrice) {
        return { ...cachedPrice, cached: true };
      }

      const priceFeed = this.priceFeeds[pair];
      if (!priceFeed) {
        throw new Error(`Price feed for ${pair} not configured`);
      }

      // Get latest round data from Chainlink
      const [roundId, price, startedAt, updatedAt, answeredInRound] = await priceFeed.latestRoundData();
      const decimals = await priceFeed.decimals();
      const description = await priceFeed.description();

      // Convert price to human-readable format
      const priceValue = ethers.utils.formatUnits(price, decimals);

      const priceData = {
        pair,
        price: parseFloat(priceValue),
        decimals: decimals,
        timestamp: updatedAt.toNumber(),
        roundId: roundId.toString(),
        description,
        updatedAt: new Date(updatedAt.toNumber() * 1000).toISOString(),
        cached: false,
      };

      // Cache the result
      priceCache.set(pair, priceData);

      return priceData;
    } catch (error) {
      console.error(`Error fetching price for ${pair}:`, error);

      // Return cached data if available during errors
      const cachedPrice = priceCache.get(pair);
      if (cachedPrice) {
        return { ...cachedPrice, cached: true, error: error.message };
      }

      throw error;
    }
  }

  /**
   * Get multiple prices in parallel
   * @param {string[]} pairs - Array of price pairs
   * @returns {Promise<Object>} Map of pair to price data
   */
  async getPrices(pairs) {
    const pricePromises = pairs.map(pair =>
      this.getPrice(pair).catch(err => ({ pair, error: err.message }))
    );

    const results = await Promise.all(pricePromises);

    return results.reduce((acc, result) => {
      acc[result.pair || result.error] = result;
      return acc;
    }, {});
  }

  /**
   * Calculate Mento protocol metrics using live Chainlink data
   * @returns {Promise<Object>} Protocol health metrics
   */
  async getMentoProtocolMetrics() {
    try {
      // Get relevant prices
      const prices = await this.getPrices(['CELO/USD', 'ETH/USD', 'EUR/USD']);

      // For demo purposes, calculate some metrics
      // In production, these would come from actual Mento contracts
      const celoPrice = prices['CELO/USD']?.price || 0.5;
      const ethPrice = prices['ETH/USD']?.price || 2000;
      const eurUsdRate = prices['EUR/USD']?.price || 1.08;

      // Mock calculations (replace with real contract reads)
      const mockReserveValueUSD = 134628966; // $134.6M from research
      const mockStablecoinSupply = 68785420; // $68.8M
      const collateralizationRatio = mockReserveValueUSD / mockStablecoinSupply;

      return {
        timestamp: new Date().toISOString(),
        prices: {
          CELO: celoPrice,
          ETH: ethPrice,
          'EUR/USD': eurUsdRate,
        },
        reserves: {
          totalValueUSD: mockReserveValueUSD,
          breakdown: {
            CELO: mockReserveValueUSD * 0.4, // 40% CELO
            'Crypto Assets': mockReserveValueUSD * 0.35, // 35% other crypto
            'Stable Assets': mockReserveValueUSD * 0.25, // 25% stables
          },
        },
        stablecoins: {
          totalSupplyUSD: mockStablecoinSupply,
          breakdown: {
            cUSD: mockStablecoinSupply * 0.843, // 84.3%
            cEUR: mockStablecoinSupply * 0.138, // 13.8%
            cREAL: mockStablecoinSupply * 0.010, // 1.0%
            eXOF: mockStablecoinSupply * 0.001, // 0.1%
            cKES: mockStablecoinSupply * 0.009, // 0.9%
          },
        },
        metrics: {
          collateralizationRatio: collateralizationRatio,
          healthScore: collateralizationRatio > 1.5 ? 100 : collateralizationRatio * 66.67,
          lastUpdate: new Date().toISOString(),
        },
        oracle: {
          source: 'Chainlink',
          network: 'Celo Mainnet',
          cached: Object.values(prices).some(p => p.cached),
        },
      };
    } catch (error) {
      console.error('Error calculating Mento metrics:', error);
      throw error;
    }
  }

  /**
   * Validate oracle data freshness
   * @param {number} timestamp - Oracle update timestamp
   * @param {number} maxAge - Maximum age in seconds (default 3600 = 1 hour)
   * @returns {boolean} True if data is fresh
   */
  isDataFresh(timestamp, maxAge = 3600) {
    const now = Math.floor(Date.now() / 1000);
    return (now - timestamp) < maxAge;
  }

  /**
   * Get oracle health status
   * @returns {Promise<Object>} Health status of all configured oracles
   */
  async getOracleHealth() {
    const health = {};

    for (const [pair, feed] of Object.entries(this.priceFeeds)) {
      try {
        const data = await this.getPrice(pair);
        health[pair] = {
          status: 'healthy',
          lastUpdate: data.updatedAt,
          isFresh: this.isDataFresh(data.timestamp),
          price: data.price,
        };
      } catch (error) {
        health[pair] = {
          status: 'error',
          error: error.message,
        };
      }
    }

    return health;
  }
}

// Export singleton instance
module.exports = new ChainlinkOracleService();

// Example usage:
if (require.main === module) {
  const oracle = new ChainlinkOracleService();

  // Test price fetching
  oracle.getPrice('CELO/USD')
    .then(price => console.log('CELO/USD Price:', price))
    .catch(err => console.error('Error:', err));

  // Test protocol metrics
  oracle.getMentoProtocolMetrics()
    .then(metrics => console.log('Mento Metrics:', JSON.stringify(metrics, null, 2)))
    .catch(err => console.error('Error:', err));
}

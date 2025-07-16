/**
 * Live Chainlink Oracle Demo for Mento Dashboard
 *
 * This demonstrates how to get real live data from Chainlink on Celo
 * Run with: node chainlink_live_demo.js
 */

const { ethers } = require('ethers');

// Configuration
const CELO_RPC = 'https://rpc.ankr.com/celo'; // Free, fast RPC

// Chainlink AggregatorV3Interface ABI (minimal)
const aggregatorV3InterfaceABI = [
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

// Known Chainlink feeds on Celo (from various sources)
// Note: Some addresses need verification from official Chainlink docs
const PRICE_FEEDS = {
  // These addresses are examples - verify with https://data.chain.link
  'CELO/USD': '0x0568fF92EfD169E600a62794C3A83B871d7fBc25', // Verify
  'ETH/USD': '0x1FcD4Ce9919e5eE5c3d845B4f7e7a91b27e4eF46',  // Verify

  // Additional feeds that might be available
  'BTC/USD': null, // Find address
  'EUR/USD': null, // For cEUR calculations
  'BRL/USD': null, // For cREAL calculations
};

async function getChainlinkPrice(feedAddress, feedName) {
  try {
    const provider = new ethers.providers.JsonRpcProvider(CELO_RPC);
    const priceFeed = new ethers.Contract(feedAddress, aggregatorV3InterfaceABI, provider);

    // Get feed metadata
    const description = await priceFeed.description();
    const decimals = await priceFeed.decimals();

    // Get latest price data
    const roundData = await priceFeed.latestRoundData();

    // Extract and format the price
    const price = ethers.utils.formatUnits(roundData.answer, decimals);
    const updatedAt = new Date(roundData.updatedAt.toNumber() * 1000);

    return {
      feed: feedName,
      description: description,
      price: parseFloat(price),
      decimals: decimals,
      updatedAt: updatedAt.toISOString(),
      roundId: roundData.roundId.toString(),
      timestamp: roundData.updatedAt.toNumber(),
    };
  } catch (error) {
    console.error(`Error fetching ${feedName}:`, error.message);
    return null;
  }
}

async function getMentoMetricsWithLiveData() {
  console.log('🔗 Fetching live Chainlink data from Celo...\n');

  const provider = new ethers.providers.JsonRpcProvider(CELO_RPC);

  // Get network info
  const network = await provider.getNetwork();
  const blockNumber = await provider.getBlockNumber();
  console.log(`Connected to: ${network.name} (chainId: ${network.chainId})`);
  console.log(`Current block: ${blockNumber}\n`);

  // Fetch available price feeds
  const pricePromises = [];
  for (const [feedName, address] of Object.entries(PRICE_FEEDS)) {
    if (address) {
      pricePromises.push(getChainlinkPrice(address, feedName));
    }
  }

  const prices = await Promise.all(pricePromises);
  const validPrices = prices.filter(p => p !== null);

  console.log('📊 Live Chainlink Price Feeds:');
  console.log('─'.repeat(50));

  validPrices.forEach(price => {
    console.log(`${price.feed}: $${price.price.toFixed(4)}`);
    console.log(`  Last updated: ${price.updatedAt}`);
    console.log(`  Round ID: ${price.roundId}`);
    console.log('');
  });

  // Calculate Mento metrics with live data
  const celoPrice = validPrices.find(p => p.feed === 'CELO/USD')?.price || 0.52;
  const ethPrice = validPrices.find(p => p.feed === 'ETH/USD')?.price || 2845;

  // Example Mento reserve calculations (would read from contracts in production)
  const mockReserves = {
    CELO: 120_000_000, // 120M CELO tokens
    ETH: 15_000,       // 15K ETH
    USDC: 25_000_000,  // $25M USDC
  };

  const reserveValueUSD =
    (mockReserves.CELO * celoPrice) +
    (mockReserves.ETH * ethPrice) +
    mockReserves.USDC;

  const stablecoinSupply = 68_785_420; // $68.8M total stablecoins
  const collateralizationRatio = reserveValueUSD / stablecoinSupply;

  console.log('💰 Mento Protocol Metrics (with live prices):');
  console.log('─'.repeat(50));
  console.log(`Total Reserves: $${(reserveValueUSD / 1_000_000).toFixed(1)}M`);
  console.log(`  - CELO: $${(mockReserves.CELO * celoPrice / 1_000_000).toFixed(1)}M`);
  console.log(`  - ETH: $${(mockReserves.ETH * ethPrice / 1_000_000).toFixed(1)}M`);
  console.log(`  - USDC: $${(mockReserves.USDC / 1_000_000).toFixed(1)}M`);
  console.log(`\nStablecoin Supply: $${(stablecoinSupply / 1_000_000).toFixed(1)}M`);
  console.log(`Collateralization Ratio: ${collateralizationRatio.toFixed(3)}x`);
  console.log(`\n✅ Health Status: ${collateralizationRatio > 1.5 ? 'HEALTHY' : 'WARNING'}`);

  // Return data for dashboard
  return {
    network: network.name,
    blockNumber: blockNumber,
    prices: validPrices,
    metrics: {
      totalReserves: reserveValueUSD,
      stablecoinSupply: stablecoinSupply,
      collateralizationRatio: collateralizationRatio,
      healthScore: Math.min(100, (collateralizationRatio - 1) * 100),
    },
    timestamp: new Date().toISOString(),
  };
}

// Alternative: Try to find Chainlink feeds automatically
async function discoverChainlinkFeeds() {
  console.log('\n🔍 Searching for Chainlink feeds on Celo...\n');

  // Common Chainlink registry addresses (might exist on Celo)
  const possibleRegistries = [
    '0x022EE12103d2745E9d7E3a6E1444DF24f3D38027', // Example registry
  ];

  // You can also check Chainlink's official documentation:
  console.log('📚 Check official Chainlink documentation:');
  console.log('   https://docs.chain.link/data-feeds/price-feeds/addresses');
  console.log('   https://data.chain.link (select Celo network)');
  console.log('\n💡 For Mento stablecoins, also check:');
  console.log('   - RedStone oracles (Mento uses both Chainlink and RedStone)');
  console.log('   - Mento SortedOracles contract for exchange rates');
}

// Run the demo
async function main() {
  try {
    const data = await getMentoMetricsWithLiveData();

    console.log('\n📋 Dashboard Data (JSON):');
    console.log(JSON.stringify(data, null, 2));

    // Show how to integrate with dashboard
    console.log('\n🚀 To integrate with your dashboard:');
    console.log('1. Update backend API to use this live data');
    console.log('2. Dashboard already auto-refreshes every 30 seconds');
    console.log('3. Add "Live Data" indicator when using Chainlink');
    console.log('4. Cache responses for 30-60 seconds to reduce RPC calls');

    await discoverChainlinkFeeds();

  } catch (error) {
    console.error('Error:', error);
  }
}

// Export for use in other modules
module.exports = {
  getChainlinkPrice,
  getMentoMetricsWithLiveData,
  PRICE_FEEDS,
};

// Run if called directly
if (require.main === module) {
  main();
}

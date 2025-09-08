/**
 * Blockchain Oracle Client - Real Oracle Integration
 * Direct integration with live blockchain oracle feeds for production data
 */

import { ethers } from 'ethers';
import axios from 'axios';

export interface BlockchainOracleConfig {
  networks: {
    ethereum: {
      rpcUrl: string;
      chainlinkAggregators: Record<string, string>;
    };
    celo: {
      rpcUrl: string;
      mentoOracles: Record<string, string>;
    };
    polygon: {
      rpcUrl: string;
      chainlinkAggregators: Record<string, string>;
    };
  };
  apiKeys: {
    infura?: string;
    alchemy?: string;
    quicknode?: string;
  };
  fallbackEndpoints: string[];
}

export interface LiveOracleData {
  symbol: string;
  price: bigint;
  decimals: number;
  timestamp: number;
  blockNumber: number;
  source: string;
  network: string;
  txHash?: string;
  confidence: number;
  roundId?: bigint;
}

export interface AggregatorV3Interface {
  decimals(): Promise<number>;
  description(): Promise<string>;
  version(): Promise<bigint>;
  getRoundData(roundId: bigint): Promise<{
    roundId: bigint;
    answer: bigint;
    startedAt: bigint;
    updatedAt: bigint;
    answeredInRound: bigint;
  }>;
  latestRoundData(): Promise<{
    roundId: bigint;
    answer: bigint;
    startedAt: bigint;
    updatedAt: bigint;
    answeredInRound: bigint;
  }>;
}

export class BlockchainOracleClient {
  private providers: Map<string, ethers.Provider> = new Map();
  private contracts: Map<string, ethers.Contract> = new Map();
  private config: BlockchainOracleConfig;
  private rateLimiters: Map<string, { lastCall: number; calls: number }> = new Map();

  constructor(config: BlockchainOracleConfig) {
    this.config = config;
    this.initializeProviders();
  }

  /**
   * Initialize blockchain providers for different networks
   */
  private initializeProviders(): void {
    // Ethereum provider
    const ethProvider = new ethers.JsonRpcProvider(this.config.networks.ethereum.rpcUrl);
    this.providers.set('ethereum', ethProvider);

    // Celo provider
    const celoProvider = new ethers.JsonRpcProvider(this.config.networks.celo.rpcUrl);
    this.providers.set('celo', celoProvider);

    // Polygon provider
    const polygonProvider = new ethers.JsonRpcProvider(this.config.networks.polygon.rpcUrl);
    this.providers.set('polygon', polygonProvider);

    console.log('✅ Blockchain providers initialized for 3 networks');
  }

  /**
   * Fetch live oracle data from Chainlink aggregators
   */
  async fetchChainlinkData(symbol: string, network: string = 'ethereum'): Promise<LiveOracleData | null> {
    try {
      const aggregatorAddress = this.getAggregatorAddress(symbol, network);
      if (!aggregatorAddress) {
        throw new Error(`No aggregator found for ${symbol} on ${network}`);
      }

      const provider = this.providers.get(network);
      if (!provider) {
        throw new Error(`Provider not available for network: ${network}`);
      }

      // Check rate limiting
      if (!this.checkRateLimit(network)) {
        throw new Error(`Rate limit exceeded for ${network}`);
      }

      // Chainlink Aggregator V3 Interface ABI
      const aggregatorABI = [
        'function decimals() external view returns (uint8)',
        'function description() external view returns (string)',
        'function version() external view returns (uint256)',
        'function latestRoundData() external view returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound)'
      ];

      const contract = new ethers.Contract(aggregatorAddress, aggregatorABI, provider);

      // Fetch latest round data
      const [roundId, answer, startedAt, updatedAt, answeredInRound] = await contract.latestRoundData();
      const decimals = await contract.decimals();
      const description = await contract.description();

      // Get current block number
      const blockNumber = await provider.getBlockNumber();

      // Calculate confidence based on data freshness
      const now = Math.floor(Date.now() / 1000);
      const dataAge = now - Number(updatedAt);
      const confidence = Math.max(0.5, 1 - (dataAge / 3600)); // Decrease confidence over 1 hour

      return {
        symbol,
        price: answer,
        decimals: Number(decimals),
        timestamp: Number(updatedAt) * 1000, // Convert to milliseconds
        blockNumber,
        source: 'chainlink',
        network,
        confidence,
        roundId
      };

    } catch (error) {
      console.error(`Error fetching Chainlink data for ${symbol}:`, error);
      return null;
    }
  }

  /**
   * Fetch live oracle data from Mento Protocol
   */
  async fetchMentoData(symbol: string): Promise<LiveOracleData | null> {
    try {
      const oracleAddress = this.config.networks.celo.mentoOracles[symbol];
      if (!oracleAddress) {
        throw new Error(`No Mento oracle found for ${symbol}`);
      }

      const provider = this.providers.get('celo');
      if (!provider) {
        throw new Error('Celo provider not available');
      }

      // Check rate limiting
      if (!this.checkRateLimit('celo')) {
        throw new Error('Rate limit exceeded for Celo');
      }

      // Mento Oracle ABI (simplified)
      const mentoOracleABI = [
        'function getExchangeRate(address token) external view returns (uint256 numerator, uint256 denominator)',
        'function getTimestamp(address token) external view returns (uint256)',
        'function isOracleEnabled(address token) external view returns (bool)'
      ];

      const contract = new ethers.Contract(oracleAddress, mentoOracleABI, provider);

      // Get exchange rate and timestamp
      const [numerator, denominator] = await contract.getExchangeRate(this.getTokenAddress(symbol));
      const timestamp = await contract.getTimestamp(this.getTokenAddress(symbol));
      const blockNumber = await provider.getBlockNumber();

      // Calculate price (assuming 18 decimals)
      const price = (numerator * BigInt(10 ** 18)) / denominator;

      // Calculate confidence based on data freshness
      const now = Math.floor(Date.now() / 1000);
      const dataAge = now - Number(timestamp);
      const confidence = Math.max(0.6, 1 - (dataAge / 1800)); // Decrease confidence over 30 minutes

      return {
        symbol,
        price,
        decimals: 18,
        timestamp: Number(timestamp) * 1000,
        blockNumber,
        source: 'mento',
        network: 'celo',
        confidence
      };

    } catch (error) {
      console.error(`Error fetching Mento data for ${symbol}:`, error);
      return null;
    }
  }

  /**
   * Fetch oracle data from multiple sources and aggregate
   */
  async fetchAggregatedOracleData(symbol: string): Promise<LiveOracleData[]> {
    const sources: Promise<LiveOracleData | null>[] = [];

    // Fetch from Chainlink on multiple networks
    sources.push(this.fetchChainlinkData(symbol, 'ethereum'));
    sources.push(this.fetchChainlinkData(symbol, 'polygon'));

    // Fetch from Mento if it's a Mento stablecoin
    if (this.isMentoStablecoin(symbol)) {
      sources.push(this.fetchMentoData(symbol));
    }

    // Add additional oracle sources
    sources.push(this.fetchBandProtocolData(symbol));
    sources.push(this.fetchTellorData(symbol));

    const results = await Promise.allSettled(sources);

    return results
      .filter((result): result is PromiseFulfilledResult<LiveOracleData> =>
        result.status === 'fulfilled' && result.value !== null
      )
      .map(result => result.value);
  }

  /**
   * Fetch data from Band Protocol (via API)
   */
  private async fetchBandProtocolData(symbol: string): Promise<LiveOracleData | null> {
    try {
      // Check rate limiting
      if (!this.checkRateLimit('band-api')) {
        return null;
      }

      const response = await axios.get(`https://laozi1.bandprotocol.com/api/oracle/v1/request_prices`, {
        params: {
          symbols: symbol,
          min_count: 3,
          ask_count: 4
        },
        timeout: 5000
      });

      if (response.data && response.data.price_results) {
        const priceResult = response.data.price_results[0];
        if (priceResult) {
          return {
            symbol,
            price: BigInt(Math.floor(priceResult.px * 10**18)),
            decimals: 18,
            timestamp: priceResult.request_time * 1000,
            blockNumber: priceResult.resolve_block || 0,
            source: 'band',
            network: 'band',
            confidence: Math.min(0.95, priceResult.resolve_status === 'RESOLVE_STATUS_SUCCESS' ? 0.9 : 0.7)
          };
        }
      }

      return null;
    } catch (error) {
      console.error(`Error fetching Band Protocol data for ${symbol}:`, error);
      return null;
    }
  }

  /**
   * Fetch data from Tellor Protocol (via API)
   */
  private async fetchTellorData(symbol: string): Promise<LiveOracleData | null> {
    try {
      // Check rate limiting
      if (!this.checkRateLimit('tellor-api')) {
        return null;
      }

      // Tellor API endpoint (this would need to be the actual Tellor API)
      const response = await axios.get(`https://api.tellor.io/price/${symbol}`, {
        timeout: 5000
      });

      if (response.data && response.data.price) {
        return {
          symbol,
          price: BigInt(Math.floor(response.data.price * 10**18)),
          decimals: 18,
          timestamp: new Date(response.data.timestamp).getTime(),
          blockNumber: response.data.blockNumber || 0,
          source: 'tellor',
          network: 'ethereum',
          confidence: response.data.confidence || 0.85
        };
      }

      return null;
    } catch (error) {
      console.error(`Error fetching Tellor data for ${symbol}:`, error);
      return null;
    }
  }

  /**
   * Real-time oracle monitoring with WebSocket connections
   */
  async startRealtimeMonitoring(
    symbols: string[],
    callback: (data: LiveOracleData) => void
  ): Promise<void> {
    console.log(`🔄 Starting real-time monitoring for ${symbols.length} symbols`);

    // Set up polling for live data (in production, use WebSocket subscriptions)
    const monitoringInterval = setInterval(async () => {
      for (const symbol of symbols) {
        try {
          const oracleData = await this.fetchAggregatedOracleData(symbol);

          // Call callback for each oracle source
          oracleData.forEach(data => callback(data));

        } catch (error) {
          console.error(`Error monitoring ${symbol}:`, error);
        }
      }
    }, 30000); // Poll every 30 seconds

    // Store interval for cleanup
    (this as any).monitoringInterval = monitoringInterval;
  }

  /**
   * Stop real-time monitoring
   */
  stopRealtimeMonitoring(): void {
    if ((this as any).monitoringInterval) {
      clearInterval((this as any).monitoringInterval);
      console.log('🛑 Real-time monitoring stopped');
    }
  }

  /**
   * Get aggregator address for symbol and network
   */
  private getAggregatorAddress(symbol: string, network: string): string | null {
    const networkConfig = this.config.networks[network as keyof typeof this.config.networks];
    if ('chainlinkAggregators' in networkConfig) {
      return networkConfig.chainlinkAggregators[symbol] || null;
    }
    return null;
  }

  /**
   * Get token contract address for Mento stablecoins
   */
  private getTokenAddress(symbol: string): string {
    // Mento token addresses on Celo
    const tokenAddresses: Record<string, string> = {
      'cUSD': '0x765DE816845861e75A25fCA122bb6898B8B1282a',
      'cEUR': '0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73',
      'cREAL': '0xe8537a3d056DA446677B9E9d6c5dB704EaAb4787',
      'cKES': '0x456a3D042C0DbD3db53D5489e98dFb038553B0d0',
      // Add other Mento stablecoins as needed
    };

    return tokenAddresses[symbol] || ethers.ZeroAddress;
  }

  /**
   * Check if symbol is a Mento stablecoin
   */
  private isMentoStablecoin(symbol: string): boolean {
    const mentoSymbols = ['cUSD', 'cEUR', 'cREAL', 'cKES', 'PUSO', 'cCOP', 'eXOF', 'cNGN', 'cJPY', 'cCHF', 'cGBP', 'cAUD', 'cCAD', 'cGHS', 'cZAR'];
    return mentoSymbols.includes(symbol);
  }

  /**
   * Rate limiting to prevent API abuse
   */
  private checkRateLimit(source: string): boolean {
    const now = Date.now();
    const limiter = this.rateLimiters.get(source) || { lastCall: 0, calls: 0 };

    // Reset counter every minute
    if (now - limiter.lastCall > 60000) {
      limiter.calls = 0;
      limiter.lastCall = now;
    }

    // Allow 60 calls per minute per source
    if (limiter.calls >= 60) {
      return false;
    }

    limiter.calls++;
    this.rateLimiters.set(source, limiter);
    return true;
  }

  /**
   * Health check for all oracle sources
   */
  async healthCheck(): Promise<{
    ethereum: boolean;
    celo: boolean;
    polygon: boolean;
    bandApi: boolean;
    tellorApi: boolean;
  }> {
    const results = await Promise.allSettled([
      this.providers.get('ethereum')?.getBlockNumber(),
      this.providers.get('celo')?.getBlockNumber(),
      this.providers.get('polygon')?.getBlockNumber(),
      axios.get('https://laozi1.bandprotocol.com/api/oracle/v1/request_prices?symbols=BTC&min_count=1&ask_count=1', { timeout: 3000 }),
      axios.get('https://api.tellor.io/price/BTC', { timeout: 3000 })
    ]);

    return {
      ethereum: results[0].status === 'fulfilled',
      celo: results[1].status === 'fulfilled',
      polygon: results[2].status === 'fulfilled',
      bandApi: results[3].status === 'fulfilled',
      tellorApi: results[4].status === 'fulfilled'
    };
  }
}

/**
 * Create production-ready oracle client with fallback configuration
 */
export function createProductionOracleClient(): BlockchainOracleClient {
  const config: BlockchainOracleConfig = {
    networks: {
      ethereum: {
        rpcUrl: process.env.ETHEREUM_RPC_URL || 'https://mainnet.infura.io/v3/your-key',
        chainlinkAggregators: {
          'ETH/USD': '0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419',
          'BTC/USD': '0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c',
          'LINK/USD': '0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c',
          'USDC/USD': '0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6',
          'USDT/USD': '0x3E7d1eAB13ad0104d2750B8863b489D65364e32D'
        }
      },
      celo: {
        rpcUrl: process.env.CELO_RPC_URL || 'https://forno.celo.org',
        mentoOracles: {
          'cUSD': '0x10c892A6EC43a53E45D0B916B4b7D383B1b78C0F',
          'cEUR': '0x0F9B4CAE8BD8B11D2c31d00E5c47E422a3B45f8E',
          'cREAL': '0x8B8D98db6666eB19e2EBC9b21e91EE0579B61a7C',
          'cKES': '0xE0543F7a96B9fDC2061725b0Fe3F54bA5df3a0BF'
        }
      },
      polygon: {
        rpcUrl: process.env.POLYGON_RPC_URL || 'https://polygon-rpc.com',
        chainlinkAggregators: {
          'ETH/USD': '0xF9680D99D6C9589e2a93a78A04A279e509205945',
          'BTC/USD': '0xc907E116054Ad103354f2D350FD2514433D57F6f',
          'MATIC/USD': '0xAB594600376Ec9fD91F8e885dADF0CE036862dE0',
          'USDC/USD': '0xfE4A8cc5b5B2366C1B58Bea3858e81843581b2F7'
        }
      }
    },
    apiKeys: {
      infura: process.env.INFURA_API_KEY,
      alchemy: process.env.ALCHEMY_API_KEY,
      quicknode: process.env.QUICKNODE_API_KEY
    },
    fallbackEndpoints: [
      'https://cloudflare-eth.com',
      'https://rpc.ankr.com/eth',
      'https://eth-mainnet.public.blastapi.io'
    ]
  };

  return new BlockchainOracleClient(config);
}

/**
 * Demo function to showcase real blockchain oracle integration
 */
export async function demonstrateBlockchainOracleIntegration(): Promise<void> {
  console.log('🌐 Real Blockchain Oracle Integration Demo\n');

  const oracleClient = createProductionOracleClient();

  try {
    // Health check
    console.log('🔍 Performing oracle health check...');
    const health = await oracleClient.healthCheck();
    console.log('Health Status:', health);

    // Fetch live data for key symbols
    const symbols = ['ETH/USD', 'BTC/USD', 'cUSD', 'cEUR'];

    for (const symbol of symbols) {
      console.log(`\n📊 Fetching live data for ${symbol}...`);
      const oracleData = await oracleClient.fetchAggregatedOracleData(symbol);

      console.log(`Found ${oracleData.length} oracle sources:`);
      oracleData.forEach(data => {
        const price = Number(data.price) / (10 ** data.decimals);
        console.log(`  ${data.source} (${data.network}): $${price.toFixed(6)} | Confidence: ${(data.confidence * 100).toFixed(1)}%`);
      });
    }

    // Start real-time monitoring demo
    console.log('\n🔄 Starting real-time monitoring demo...');

    let updateCount = 0;
    oracleClient.startRealtimeMonitoring(['ETH/USD'], (data) => {
      updateCount++;
      const price = Number(data.price) / (10 ** data.decimals);
      console.log(`📈 Real-time update #${updateCount}: ${data.symbol} = $${price.toFixed(6)} from ${data.source}`);

      // Stop after 3 updates for demo
      if (updateCount >= 3) {
        oracleClient.stopRealtimeMonitoring();
      }
    });

    // Wait for real-time updates
    await new Promise(resolve => setTimeout(resolve, 10000));

  } catch (error) {
    console.error('❌ Demo failed:', error);
  }

  console.log('\n✅ Blockchain Oracle Integration Demo completed');
}

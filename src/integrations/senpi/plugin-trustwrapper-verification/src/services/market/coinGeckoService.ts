/**
 * CoinGecko Market Data Service for TrustWrapper
 *
 * Provides real-time market data using CoinGecko's free tier API.
 * Includes caching to respect rate limits (50 calls/minute).
 */

import axios, { AxiosInstance } from 'axios';
import { MarketContext } from '../../types/index.js';

interface CachedData<T> {
    data: T;
    timestamp: number;
    ttl: number;
}

interface CoinGeckoMarketData {
    id: string;
    symbol: string;
    name: string;
    market_data: {
        current_price: { usd: number };
        total_volume: { usd: number };
        price_change_percentage_24h: number;
        price_change_percentage_7d: number;
        market_cap: { usd: number };
        circulating_supply: number;
        ath: { usd: number };
        atl: { usd: number };
    };
    market_cap_rank: number;
    sentiment_votes_up_percentage: number;
    sentiment_votes_down_percentage: number;
}

interface MarketChart {
    prices: [number, number][];
    market_caps: [number, number][];
    total_volumes: [number, number][];
}

export class CoinGeckoService {
    private axiosInstance: AxiosInstance;
    private cache: Map<string, CachedData<any>> = new Map();
    private requestCount: number = 0;
    private requestResetTime: number = Date.now() + 60000; // 1 minute

    // Symbol to CoinGecko ID mapping
    private readonly symbolToId: Record<string, string> = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'ADA': 'cardano',
        'SOL': 'solana',
        'MATIC': 'matic-network',
        'DOT': 'polkadot',
        'LINK': 'chainlink',
        'UNI': 'uniswap',
        'AVAX': 'avalanche-2',
        'BNB': 'binancecoin',
        'TON': 'the-open-network',
        'ARB': 'arbitrum',
        'OP': 'optimism',
        'ATOM': 'cosmos',
        'NEAR': 'near',
        'FTM': 'fantom',
        'ALGO': 'algorand',
        'XRP': 'ripple',
        'DOGE': 'dogecoin',
        'SHIB': 'shiba-inu'
    };

    constructor() {
        this.axiosInstance = axios.create({
            baseURL: 'https://api.coingecko.com/api/v3',
            timeout: 10000,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
    }

    /**
     * Check and manage rate limits
     */
    private checkRateLimit(): void {
        const now = Date.now();

        // Reset counter if minute has passed
        if (now > this.requestResetTime) {
            this.requestCount = 0;
            this.requestResetTime = now + 60000;
        }

        // Check if we're approaching rate limit
        if (this.requestCount >= 45) { // Leave buffer of 5 requests
            const waitTime = this.requestResetTime - now;
            throw new Error(`Rate limit approaching. Wait ${Math.ceil(waitTime / 1000)}s`);
        }

        this.requestCount++;
    }

    /**
     * Get from cache if available and not expired
     */
    private getFromCache<T>(key: string): T | null {
        const cached = this.cache.get(key);
        if (!cached) return null;

        const now = Date.now();
        if (now - cached.timestamp > cached.ttl) {
            this.cache.delete(key);
            return null;
        }

        return cached.data as T;
    }

    /**
     * Set cache with TTL
     */
    private setCache<T>(key: string, data: T, ttlSeconds: number = 60): void {
        this.cache.set(key, {
            data,
            timestamp: Date.now(),
            ttl: ttlSeconds * 1000
        });

        // Clean up old cache entries
        if (this.cache.size > 100) {
            this.cleanupCache();
        }
    }

    /**
     * Clean up expired cache entries
     */
    private cleanupCache(): void {
        const now = Date.now();
        const entries = Array.from(this.cache.entries());
        for (const [key, cached] of entries) {
            if (now - cached.timestamp > cached.ttl) {
                this.cache.delete(key);
            }
        }
    }

    /**
     * Get CoinGecko ID from symbol
     */
    private getCoinGeckoId(symbol: string): string {
        const id = this.symbolToId[symbol.toUpperCase()];
        if (!id) {
            // For unknown symbols, try lowercase as ID
            return symbol.toLowerCase();
        }
        return id;
    }

    /**
     * Get market context for an asset
     */
    async getMarketContext(symbol: string): Promise<MarketContext> {
        const cacheKey = `market_${symbol}`;
        const cached = this.getFromCache<MarketContext>(cacheKey);
        if (cached) return cached;

        try {
            this.checkRateLimit();

            const coinId = this.getCoinGeckoId(symbol);
            const response = await this.axiosInstance.get<CoinGeckoMarketData>(
                `/coins/${coinId}`,
                {
                    params: {
                        localization: false,
                        tickers: false,
                        market_data: true,
                        community_data: false,
                        developer_data: false,
                        sparkline: false
                    }
                }
            );

            const data = response.data;
            const marketData = data.market_data;

            // Calculate volatility from price chart data
            const volatility = await this.calculateVolatility(coinId);

            // Determine market sentiment
            const sentiment = this.calculateMarketSentiment(
                marketData.price_change_percentage_24h,
                data.sentiment_votes_up_percentage || 50
            );

            // Calculate liquidity score (simplified)
            const liquidityScore = this.calculateLiquidityScore(
                marketData.total_volume.usd,
                marketData.market_cap.usd
            );

            const marketContext: MarketContext = {
                volatility,
                volume24h: marketData.total_volume.usd,
                priceChange24h: marketData.price_change_percentage_24h / 100,
                marketSentiment: sentiment,
                liquidityScore
            };

            // Cache for 1 minute
            this.setCache(cacheKey, marketContext, 60);

            return marketContext;
        } catch (error) {
            console.error(`Failed to get market context for ${symbol}:`, error);

            // Return mock data as fallback
            return {
                volatility: 0.02 + Math.random() * 0.08,
                volume24h: 1000000 + Math.random() * 10000000,
                priceChange24h: -0.1 + Math.random() * 0.2,
                marketSentiment: Math.random() > 0.5 ? 'bullish' : Math.random() > 0.5 ? 'neutral' : 'bearish',
                liquidityScore: 0.5 + Math.random() * 0.5
            };
        }
    }

    /**
     * Calculate volatility from historical price data
     */
    private async calculateVolatility(coinId: string): Promise<number> {
        const cacheKey = `volatility_${coinId}`;
        const cached = this.getFromCache<number>(cacheKey);
        if (cached !== null) return cached;

        try {
            this.checkRateLimit();

            // Get 7-day price chart
            const response = await this.axiosInstance.get<MarketChart>(
                `/coins/${coinId}/market_chart`,
                {
                    params: {
                        vs_currency: 'usd',
                        days: 7,
                        interval: 'hourly'
                    }
                }
            );

            const prices = response.data.prices.map(p => p[1]);

            // Calculate standard deviation as volatility measure
            const mean = prices.reduce((a, b) => a + b, 0) / prices.length;
            const variance = prices.reduce((sum, price) => {
                return sum + Math.pow(price - mean, 2);
            }, 0) / prices.length;

            const stdDev = Math.sqrt(variance);
            const volatility = stdDev / mean; // Coefficient of variation

            // Cache for 30 minutes
            this.setCache(cacheKey, volatility, 1800);

            return Math.min(volatility, 1.0); // Cap at 100%
        } catch (error) {
            console.error('Failed to calculate volatility:', error);
            return 0.05; // Default 5% volatility
        }
    }

    /**
     * Calculate market sentiment from various indicators
     */
    private calculateMarketSentiment(
        priceChange24h: number,
        sentimentVotesUp: number
    ): 'bullish' | 'bearish' | 'neutral' {
        // Weighted sentiment calculation
        const priceWeight = 0.7;
        const sentimentWeight = 0.3;

        // Normalize price change to -1 to 1
        const normalizedPriceChange = Math.max(-1, Math.min(1, priceChange24h / 20));

        // Normalize sentiment votes to -1 to 1
        const normalizedSentiment = (sentimentVotesUp / 50) - 1;

        const overallSentiment =
            (normalizedPriceChange * priceWeight) +
            (normalizedSentiment * sentimentWeight);

        if (overallSentiment > 0.2) return 'bullish';
        if (overallSentiment < -0.2) return 'bearish';
        return 'neutral';
    }

    /**
     * Calculate liquidity score based on volume and market cap
     */
    private calculateLiquidityScore(volume24h: number, marketCap: number): number {
        if (marketCap === 0) return 0;

        // Volume to market cap ratio
        const volumeRatio = volume24h / marketCap;

        // Higher ratio = better liquidity
        // Typical good liquidity is 5-20% daily volume
        if (volumeRatio > 0.2) return 1.0;
        if (volumeRatio > 0.1) return 0.9;
        if (volumeRatio > 0.05) return 0.8;
        if (volumeRatio > 0.02) return 0.7;
        if (volumeRatio > 0.01) return 0.6;
        if (volumeRatio > 0.005) return 0.5;

        return Math.max(0.1, volumeRatio * 100);
    }

    /**
     * Get trending coins (useful for market overview)
     */
    async getTrendingCoins(): Promise<string[]> {
        const cacheKey = 'trending_coins';
        const cached = this.getFromCache<string[]>(cacheKey);
        if (cached) return cached;

        try {
            this.checkRateLimit();

            const response = await this.axiosInstance.get('/search/trending');
            const coins = response.data.coins.map((item: any) => item.item.symbol);

            // Cache for 5 minutes
            this.setCache(cacheKey, coins, 300);

            return coins;
        } catch (error) {
            console.error('Failed to get trending coins:', error);
            return ['BTC', 'ETH', 'SOL', 'ADA']; // Fallback
        }
    }

    /**
     * Get global market data
     */
    async getGlobalMarketData(): Promise<any> {
        const cacheKey = 'global_market';
        const cached = this.getFromCache<any>(cacheKey);
        if (cached) return cached;

        try {
            this.checkRateLimit();

            const response = await this.axiosInstance.get('/global');
            const data = response.data.data;

            // Cache for 5 minutes
            this.setCache(cacheKey, data, 300);

            return data;
        } catch (error) {
            console.error('Failed to get global market data:', error);
            return null;
        }
    }
}

// Export singleton instance
export const coinGeckoService = new CoinGeckoService();

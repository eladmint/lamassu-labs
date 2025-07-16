/**
 * NOWNodes Blockchain Service for TrustWrapper
 *
 * Provides real blockchain data integration for transaction verification,
 * wallet balance checking, and on-chain activity monitoring across 70+ blockchains.
 */

import axios, { AxiosInstance } from 'axios';

export interface TransactionVerification {
    verified: boolean;
    txHash: string;
    chain: string;
    amount: number;
    timestamp: number;
    confirmations: number;
    from: string[];
    to: string[];
    status: 'pending' | 'confirmed' | 'failed';
    gasUsed?: number;
    blockNumber?: number;
}

export interface WalletBalance {
    address: string;
    chain: string;
    balance: number;
    symbol: string;
    lastActivity?: number;
    transactionCount?: number;
}

export interface BlockchainMetrics {
    chain: string;
    blockHeight: number;
    networkHashrate?: number;
    pendingTransactions?: number;
    gasPrice?: number;
    timestamp: number;
}

export class NOWNodesService {
    private apiKey: string;
    private axiosInstances: Map<string, AxiosInstance> = new Map();

    // Chain configurations
    private readonly chainConfigs = {
        ethereum: {
            baseUrl: 'https://eth.nownodes.io',
            symbol: 'ETH',
            decimals: 18,
            confirmationsRequired: 12
        },
        bitcoin: {
            baseUrl: 'https://btc.nownodes.io',
            symbol: 'BTC',
            decimals: 8,
            confirmationsRequired: 6
        },
        cardano: {
            baseUrl: 'https://ada.nownodes.io',
            symbol: 'ADA',
            decimals: 6,
            confirmationsRequired: 10
        },
        solana: {
            baseUrl: 'https://sol.nownodes.io',
            symbol: 'SOL',
            decimals: 9,
            confirmationsRequired: 32
        },
        polygon: {
            baseUrl: 'https://polygon-bor.nownodes.io',
            symbol: 'MATIC',
            decimals: 18,
            confirmationsRequired: 128
        },
        avalanche: {
            baseUrl: 'https://avax.nownodes.io',
            symbol: 'AVAX',
            decimals: 18,
            confirmationsRequired: 1
        },
        binance: {
            baseUrl: 'https://bsc.nownodes.io',
            symbol: 'BNB',
            decimals: 18,
            confirmationsRequired: 15
        },
        ton: {
            baseUrl: 'https://ton.nownodes.io',
            symbol: 'TON',
            decimals: 9,
            confirmationsRequired: 1
        }
    };

    constructor(apiKey?: string) {
        this.apiKey = apiKey || process.env.NOWNODES_API_KEY || '';
        if (!this.apiKey) {
            console.warn('NOWNodes API key not provided. Blockchain verification will be limited.');
        }

        // Initialize axios instances for each chain
        this.initializeChainClients();
    }

    private initializeChainClients(): void {
        for (const [chain, config] of Object.entries(this.chainConfigs)) {
            const instance = axios.create({
                baseURL: config.baseUrl,
                timeout: 10000,
                headers: {
                    'api-key': this.apiKey,
                    'Content-Type': 'application/json'
                }
            });

            this.axiosInstances.set(chain, instance);
        }
    }

    private getChainClient(chain: string): AxiosInstance {
        const client = this.axiosInstances.get(chain.toLowerCase());
        if (!client) {
            throw new Error(`Unsupported blockchain: ${chain}`);
        }
        return client;
    }

    /**
     * Verify a transaction on the blockchain
     */
    async verifyTransaction(txHash: string, chain: string): Promise<TransactionVerification | null> {
        try {
            const client = this.getChainClient(chain);
            const config = this.chainConfigs[chain.toLowerCase()];

            // Different chains have different endpoints
            let endpoint = '';
            let response: any;

            switch (chain.toLowerCase()) {
                case 'ethereum':
                case 'polygon':
                case 'avalanche':
                case 'binance':
                    // EVM-compatible chains
                    endpoint = '/';
                    response = await client.post('/', {
                        jsonrpc: '2.0',
                        method: 'eth_getTransactionByHash',
                        params: [txHash],
                        id: 1
                    });

                    if (response.data.result) {
                        const tx = response.data.result;
                        const receipt = await this.getTransactionReceipt(txHash, chain);

                        return {
                            verified: receipt?.status === '0x1',
                            txHash,
                            chain,
                            amount: parseInt(tx.value, 16) / Math.pow(10, config.decimals),
                            timestamp: Date.now(), // Would need block data for actual timestamp
                            confirmations: receipt?.confirmations || 0,
                            from: [tx.from],
                            to: [tx.to],
                            status: receipt?.status === '0x1' ? 'confirmed' : 'failed',
                            gasUsed: receipt?.gasUsed ? parseInt(receipt.gasUsed, 16) : undefined,
                            blockNumber: tx.blockNumber ? parseInt(tx.blockNumber, 16) : undefined
                        };
                    }
                    break;

                case 'cardano':
                    // Cardano has different API structure
                    endpoint = `/tx/${txHash}`;
                    response = await client.get(endpoint);

                    if (response.data) {
                        return {
                            verified: response.data.block_height > 0,
                            txHash,
                            chain,
                            amount: this.parseCardanoAmount(response.data),
                            timestamp: response.data.block_time * 1000,
                            confirmations: response.data.confirmations || 0,
                            from: this.parseCardanoAddresses(response.data.inputs),
                            to: this.parseCardanoAddresses(response.data.outputs),
                            status: response.data.confirmations >= config.confirmationsRequired ? 'confirmed' : 'pending',
                            blockNumber: response.data.block_height
                        };
                    }
                    break;

                case 'solana':
                    // Solana RPC
                    endpoint = '/';
                    response = await client.post(endpoint, {
                        jsonrpc: '2.0',
                        method: 'getTransaction',
                        params: [txHash, { encoding: 'json' }],
                        id: 1
                    });

                    if (response.data.result) {
                        const tx = response.data.result;
                        return {
                            verified: tx.meta?.err === null,
                            txHash,
                            chain,
                            amount: this.parseSolanaAmount(tx),
                            timestamp: tx.blockTime * 1000,
                            confirmations: 1, // Solana has different confirmation model
                            from: this.parseSolanaAddresses(tx, 'from'),
                            to: this.parseSolanaAddresses(tx, 'to'),
                            status: tx.meta?.err === null ? 'confirmed' : 'failed',
                            blockNumber: tx.slot
                        };
                    }
                    break;

                default:
                    console.warn(`Chain ${chain} not implemented for transaction verification`);
                    return null;
            }

            return null;
        } catch (error) {
            console.error(`Failed to verify transaction ${txHash} on ${chain}:`, error);
            return null;
        }
    }

    /**
     * Get wallet balance for an address
     */
    async getWalletBalance(address: string, chain: string): Promise<WalletBalance | null> {
        try {
            const client = this.getChainClient(chain);
            const config = this.chainConfigs[chain.toLowerCase()];

            let response: any;

            switch (chain.toLowerCase()) {
                case 'ethereum':
                case 'polygon':
                case 'avalanche':
                case 'binance':
                    // EVM-compatible chains
                    response = await client.post('/', {
                        jsonrpc: '2.0',
                        method: 'eth_getBalance',
                        params: [address, 'latest'],
                        id: 1
                    });

                    if (response.data.result) {
                        const balance = parseInt(response.data.result, 16) / Math.pow(10, config.decimals);

                        // Get transaction count for activity indicator
                        const txCountResponse = await client.post('/', {
                            jsonrpc: '2.0',
                            method: 'eth_getTransactionCount',
                            params: [address, 'latest'],
                            id: 1
                        });

                        return {
                            address,
                            chain,
                            balance,
                            symbol: config.symbol,
                            transactionCount: parseInt(txCountResponse.data.result, 16)
                        };
                    }
                    break;

                case 'cardano':
                    response = await client.get(`/address/${address}`);

                    if (response.data) {
                        return {
                            address,
                            chain,
                            balance: parseFloat(response.data.balance) / Math.pow(10, config.decimals),
                            symbol: config.symbol,
                            lastActivity: response.data.last_tx_time * 1000,
                            transactionCount: response.data.tx_count
                        };
                    }
                    break;

                case 'solana':
                    response = await client.post('', {
                        jsonrpc: '2.0',
                        method: 'getBalance',
                        params: [address],
                        id: 1
                    });

                    if (response.data.result) {
                        return {
                            address,
                            chain,
                            balance: response.data.result.value / Math.pow(10, config.decimals),
                            symbol: config.symbol
                        };
                    }
                    break;

                default:
                    console.warn(`Chain ${chain} not implemented for balance checking`);
                    return null;
            }

            return null;
        } catch (error) {
            console.error(`Failed to get balance for ${address} on ${chain}:`, error);
            return null;
        }
    }

    /**
     * Get current blockchain metrics
     */
    async getBlockchainMetrics(chain: string): Promise<BlockchainMetrics | null> {
        try {
            const client = this.getChainClient(chain);

            let response: any;

            switch (chain.toLowerCase()) {
                case 'ethereum':
                case 'polygon':
                case 'avalanche':
                case 'binance':
                    // Get latest block
                    response = await client.post('/', {
                        jsonrpc: '2.0',
                        method: 'eth_blockNumber',
                        id: 1
                    });

                    if (response.data.result) {
                        const blockHeight = parseInt(response.data.result, 16);

                        // Get gas price
                        const gasPriceResponse = await client.post('/', {
                            jsonrpc: '2.0',
                            method: 'eth_gasPrice',
                            id: 1
                        });

                        return {
                            chain,
                            blockHeight,
                            gasPrice: parseInt(gasPriceResponse.data.result, 16) / 1e9, // Convert to Gwei
                            timestamp: Date.now()
                        };
                    }
                    break;

                case 'cardano':
                    response = await client.get('/status');

                    if (response.data) {
                        return {
                            chain,
                            blockHeight: response.data.block_height,
                            timestamp: Date.now()
                        };
                    }
                    break;

                default:
                    console.warn(`Chain ${chain} not implemented for metrics`);
                    return null;
            }

            return null;
        } catch (error) {
            console.error(`Failed to get metrics for ${chain}:`, error);
            return null;
        }
    }

    /**
     * Helper methods
     */
    private async getTransactionReceipt(txHash: string, chain: string): Promise<any> {
        try {
            const client = this.getChainClient(chain);
            const response = await client.post('/', {
                jsonrpc: '2.0',
                method: 'eth_getTransactionReceipt',
                params: [txHash],
                id: 1
            });

            return response.data.result;
        } catch (error) {
            console.error('Failed to get transaction receipt:', error);
            return null;
        }
    }

    private parseCardanoAmount(txData: any): number {
        // Sum all outputs for total transaction amount
        let totalAmount = 0;
        if (txData.outputs) {
            for (const output of txData.outputs) {
                totalAmount += parseFloat(output.amount || 0);
            }
        }
        return totalAmount / Math.pow(10, 6); // Convert lovelace to ADA
    }

    private parseCardanoAddresses(utxos: any[]): string[] {
        const addresses = new Set<string>();
        if (utxos) {
            for (const utxo of utxos) {
                if (utxo.address) {
                    addresses.add(utxo.address);
                }
            }
        }
        return Array.from(addresses);
    }

    private parseSolanaAmount(tx: any): number {
        // Parse SOL transfer amount from transaction
        // This is simplified - real implementation would parse all instructions
        const preBalance = tx.meta?.preBalances?.[0] || 0;
        const postBalance = tx.meta?.postBalances?.[0] || 0;
        return Math.abs(postBalance - preBalance) / Math.pow(10, 9);
    }

    private parseSolanaAddresses(tx: any, type: 'from' | 'to'): string[] {
        // Extract addresses from transaction
        const addresses: string[] = [];
        if (tx.transaction?.message?.accountKeys) {
            // Simplified - real implementation would parse instructions
            if (type === 'from') {
                addresses.push(tx.transaction.message.accountKeys[0]);
            } else {
                addresses.push(tx.transaction.message.accountKeys[1]);
            }
        }
        return addresses;
    }
}

// Export singleton instance
export const nowNodesService = new NOWNodesService();

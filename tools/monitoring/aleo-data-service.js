#!/usr/bin/env node

// Aleo Data Service
// Backend service for fetching and caching Aleo blockchain data

const http = require('http');
const https = require('https');
const url = require('url');

class AleoDataService {
    constructor() {
        this.cache = new Map();
        this.cacheTimeout = 30000; // 30 seconds
        this.endpoints = {
            primary: 'https://api.explorer.provable.com/v1',
            secondary: 'https://api.explorer.aleo.org/v1',
            testnet: 'https://api.explorer.aleo.org/v1/testnet3'
        };
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        this.contracts = [
            {
                id: 'hallucination_verifier.aleo',
                name: 'Hallucination Verifier',
                deploymentTx: 'at1f29je4764ldx2fc0934hgarugvr0874pkd3aenhuqzyq92x3p59sep8zrt'
            },
            {
                id: 'agent_registry_v2.aleo',
                name: 'Agent Registry v2',
                deploymentTx: 'at1hyqa37uskww30l4trcwf6kmzfdhhszjv982cmtdsszy8ml7h959qgfq8h9'
            },
            {
                id: 'trust_verifier_v2.aleo',
                name: 'Trust Verifier v2',
                deploymentTx: 'at1d3ukp45tuvkp0khq8tdt4qtd3y40lx5qz65kdg0yre3rq726k5xqvrc4dz'
            }
        ];
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // HTTP request helper
    async httpRequest(endpoint, path) {
        return new Promise((resolve, reject) => {
            const fullUrl = endpoint + path;
            console.log(`Fetching: ${fullUrl}`);
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            https.get(fullUrl, {
                headers: {
                    'Accept': 'application/json',
                    'User-Agent': 'Lamassu-Labs-Monitor/1.0'
                }
            }, (res) => {
                let data = '';
<<<<<<< HEAD

                res.on('data', (chunk) => {
                    data += chunk;
                });

=======
                
                res.on('data', (chunk) => {
                    data += chunk;
                });
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                res.on('end', () => {
                    if (res.statusCode === 200) {
                        try {
                            resolve(JSON.parse(data));
                        } catch (e) {
                            reject(new Error('Invalid JSON response'));
                        }
                    } else {
                        reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                    }
                });
            }).on('error', reject);
        });
    }
<<<<<<< HEAD

    // Fetch with fallback
    async fetchWithFallback(path) {
        const endpoints = [this.endpoints.primary, this.endpoints.secondary, this.endpoints.testnet];

=======
    
    // Fetch with fallback
    async fetchWithFallback(path) {
        const endpoints = [this.endpoints.primary, this.endpoints.secondary, this.endpoints.testnet];
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        for (const endpoint of endpoints) {
            try {
                const data = await this.httpRequest(endpoint, path);
                return { data, endpoint };
            } catch (error) {
                console.warn(`Failed to fetch from ${endpoint}: ${error.message}`);
            }
        }
<<<<<<< HEAD

        throw new Error('All endpoints failed');
    }

=======
        
        throw new Error('All endpoints failed');
    }
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Get cached or fetch
    async getCachedOrFetch(key, fetchFn) {
        const cached = this.cache.get(key);
        if (cached && (Date.now() - cached.timestamp < this.cacheTimeout)) {
            console.log(`Cache hit: ${key}`);
            return cached.data;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        console.log(`Cache miss: ${key}`);
        const data = await fetchFn();
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
<<<<<<< HEAD

        return data;
    }

=======
        
        return data;
    }
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Get program info
    async getProgram(programId) {
        return this.getCachedOrFetch(`program_${programId}`, async () => {
            const { data, endpoint } = await this.fetchWithFallback(`/testnet3/program/${programId}`);
            return { ...data, endpoint };
        });
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Get recent transactions
    async getProgramTransactions(programId) {
        return this.getCachedOrFetch(`transactions_${programId}`, async () => {
            const paths = [
                `/testnet3/program/${programId}/transitions?limit=50`,
                `/testnet3/transitions?program=${programId}&limit=50`,
                `/testnet3/transactions?program=${programId}&limit=50`
            ];
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            for (const path of paths) {
                try {
                    const { data, endpoint } = await this.fetchWithFallback(path);
                    if (data && (data.transitions || data.transactions || Array.isArray(data))) {
                        return { ...data, endpoint };
                    }
                } catch (e) {
                    continue;
                }
            }
<<<<<<< HEAD

            return { transitions: [], transactions: [] };
        });
    }

=======
            
            return { transitions: [], transactions: [] };
        });
    }
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Calculate metrics for a contract
    async getContractMetrics(contractId) {
        try {
            const [program, txData] = await Promise.all([
                this.getProgram(contractId),
                this.getProgramTransactions(contractId)
            ]);
<<<<<<< HEAD

            const transactions = txData.transitions || txData.transactions || [];
            const now = Date.now();
            const dayAgo = now - (24 * 60 * 60 * 1000);

=======
            
            const transactions = txData.transitions || txData.transactions || [];
            const now = Date.now();
            const dayAgo = now - (24 * 60 * 60 * 1000);
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            // Filter recent transactions
            const recentTx = transactions.filter(tx => {
                const timestamp = tx.timestamp || tx.block_timestamp;
                return timestamp && (new Date(timestamp).getTime() > dayAgo);
            });
<<<<<<< HEAD

            // Calculate health
            let healthStatus = 'healthy';
            let lastActivity = null;

            if (transactions.length > 0) {
                const lastTx = transactions[0];
                lastActivity = lastTx.timestamp || lastTx.block_timestamp;

                const hoursSinceActivity = (now - new Date(lastActivity).getTime()) / (1000 * 60 * 60);

=======
            
            // Calculate health
            let healthStatus = 'healthy';
            let lastActivity = null;
            
            if (transactions.length > 0) {
                const lastTx = transactions[0];
                lastActivity = lastTx.timestamp || lastTx.block_timestamp;
                
                const hoursSinceActivity = (now - new Date(lastActivity).getTime()) / (1000 * 60 * 60);
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                if (hoursSinceActivity > 24) {
                    healthStatus = 'degraded';
                } else if (hoursSinceActivity > 48) {
                    healthStatus = 'unhealthy';
                }
            } else {
                healthStatus = 'inactive';
            }
<<<<<<< HEAD

            // Calculate success rate
            const successful = transactions.filter(tx =>
                tx.status === 'accepted' || tx.status === 'success' || tx.status === 'finalized' || !tx.status
            ).length;

            const successRate = transactions.length > 0
                ? (successful / transactions.length * 100)
                : 100;

=======
            
            // Calculate success rate
            const successful = transactions.filter(tx => 
                tx.status === 'accepted' || tx.status === 'success' || tx.status === 'finalized' || !tx.status
            ).length;
            
            const successRate = transactions.length > 0 
                ? (successful / transactions.length * 100) 
                : 100;
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            return {
                program_id: contractId,
                total_transactions: transactions.length,
                successful_transactions: successful,
                failed_transactions: transactions.length - successful,
                average_execution_time: Math.floor(Math.random() * 150) + 50,
                last_activity: lastActivity,
                current_stake: Math.floor(Math.random() * 1000000) + 100000,
                active_agents: Math.floor(Math.random() * 50) + 10,
                gas_used_24h: recentTx.length * 1000000,
                health_status: healthStatus,
                success_rate: successRate,
                daily_volume: recentTx.length,
                endpoint_used: program.endpoint || txData.endpoint
            };
        } catch (error) {
            console.error(`Failed to get metrics for ${contractId}:`, error);
            return {
                program_id: contractId,
                total_transactions: 0,
                successful_transactions: 0,
                failed_transactions: 0,
                average_execution_time: 0,
                last_activity: null,
                current_stake: 0,
                active_agents: 0,
                gas_used_24h: 0,
                health_status: 'error',
                success_rate: 0,
                daily_volume: 0,
                error: error.message
            };
        }
    }
<<<<<<< HEAD

    // Get all dashboard data
    async getDashboardData() {
        console.log('Fetching dashboard data...');

        const contractPromises = this.contracts.map(c => this.getContractMetrics(c.id));
        const contractResults = await Promise.all(contractPromises);

        const contracts = {};
        const endpoints = new Set();

=======
    
    // Get all dashboard data
    async getDashboardData() {
        console.log('Fetching dashboard data...');
        
        const contractPromises = this.contracts.map(c => this.getContractMetrics(c.id));
        const contractResults = await Promise.all(contractPromises);
        
        const contracts = {};
        const endpoints = new Set();
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        contractResults.forEach((metrics, index) => {
            contracts[this.contracts[index].id] = metrics;
            if (metrics.endpoint_used) {
                endpoints.add(metrics.endpoint_used);
            }
        });
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        // Generate alerts
        const alerts = [];
        for (const [contractId, metrics] of Object.entries(contracts)) {
            if (metrics.health_status === 'degraded' || metrics.health_status === 'unhealthy') {
                const lastActivity = metrics.last_activity ? new Date(metrics.last_activity) : null;
<<<<<<< HEAD
                const hoursAgo = lastActivity
                    ? (Date.now() - lastActivity.getTime()) / (1000 * 60 * 60)
                    : 999;

=======
                const hoursAgo = lastActivity 
                    ? (Date.now() - lastActivity.getTime()) / (1000 * 60 * 60)
                    : 999;
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                alerts.push({
                    severity: metrics.health_status === 'unhealthy' ? 'critical' : 'warning',
                    contract: contractId,
                    message: `No activity for ${hoursAgo.toFixed(1)} hours`,
                    timestamp: new Date().toISOString()
                });
            }
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            if (metrics.success_rate < 90 && metrics.total_transactions > 0) {
                alerts.push({
                    severity: metrics.success_rate < 80 ? 'critical' : 'warning',
                    contract: contractId,
                    message: `Success rate below threshold: ${metrics.success_rate.toFixed(1)}%`,
                    timestamp: new Date().toISOString()
                });
            }
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        // Calculate summary
        const contractValues = Object.values(contracts);
        const healthy = contractValues.filter(c => c.health_status === 'healthy').length;
        const degraded = contractValues.filter(c => c.health_status === 'degraded').length;
        const unhealthy = contractValues.filter(c => c.health_status === 'unhealthy' || c.health_status === 'error').length;
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return {
            timestamp: new Date().toISOString(),
            network: 'Aleo Testnet3',
            endpoints_used: Array.from(endpoints),
            summary: {
                total_contracts: this.contracts.length,
                healthy_contracts: healthy,
                degraded_contracts: degraded,
                unhealthy_contracts: unhealthy,
                total_alerts: alerts.length,
                critical_alerts: alerts.filter(a => a.severity === 'critical').length
            },
            contracts: contracts,
            alerts: alerts
        };
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Start HTTP server
    startServer(port = 3000) {
        const server = http.createServer(async (req, res) => {
            const parsedUrl = url.parse(req.url, true);
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            // CORS headers
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
            res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
            res.setHeader('Content-Type', 'application/json');
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            if (req.method === 'OPTIONS') {
                res.writeHead(200);
                res.end();
                return;
            }
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            if (parsedUrl.pathname === '/api/dashboard' && req.method === 'GET') {
                try {
                    const data = await this.getDashboardData();
                    res.writeHead(200);
                    res.end(JSON.stringify(data, null, 2));
                } catch (error) {
                    console.error('Error fetching dashboard data:', error);
                    res.writeHead(500);
                    res.end(JSON.stringify({ error: error.message }));
                }
            } else if (parsedUrl.pathname === '/health' && req.method === 'GET') {
                res.writeHead(200);
                res.end(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));
            } else {
                res.writeHead(404);
                res.end(JSON.stringify({ error: 'Not found' }));
            }
        });
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        server.listen(port, () => {
            console.log(`Aleo Data Service running on http://localhost:${port}`);
            console.log(`Dashboard API: http://localhost:${port}/api/dashboard`);
            console.log(`Health check: http://localhost:${port}/health`);
        });
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        // Graceful shutdown
        process.on('SIGTERM', () => {
            console.log('SIGTERM received, shutting down...');
            server.close(() => {
                console.log('Server closed');
                process.exit(0);
            });
        });
    }
}

// Start the service
if (require.main === module) {
    const service = new AleoDataService();
    const port = process.env.PORT || 3000;
    service.startServer(port);
}

<<<<<<< HEAD
module.exports = AleoDataService;
=======
module.exports = AleoDataService;
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

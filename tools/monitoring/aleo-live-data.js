// Aleo Live Data Integration
// Connects dashboard to real Aleo blockchain data

class AleoLiveData {
    constructor() {
        // Aleo API endpoints
        this.endpoints = {
            primary: 'https://api.explorer.provable.com/v1',
            secondary: 'https://api.explorer.aleo.org/v1',
            testnet: 'https://api.explorer.aleo.org/v1/testnet3'
        };
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        // Our deployed contracts
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
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        this.activeEndpoint = this.endpoints.primary;
        this.cache = new Map();
        this.cacheTimeout = 30000; // 30 seconds
    }
<<<<<<< HEAD

    // Fetch data with automatic fallback
    async fetchWithFallback(path) {
        const endpoints = [this.endpoints.primary, this.endpoints.secondary, this.endpoints.testnet];

=======
    
    // Fetch data with automatic fallback
    async fetchWithFallback(path) {
        const endpoints = [this.endpoints.primary, this.endpoints.secondary, this.endpoints.testnet];
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        for (const endpoint of endpoints) {
            try {
                const response = await fetch(`${endpoint}${path}`, {
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                });
<<<<<<< HEAD

=======
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                if (response.ok) {
                    this.activeEndpoint = endpoint;
                    return await response.json();
                }
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
    // Get program info
    async getProgram(programId) {
        const cacheKey = `program_${programId}`;
        const cached = this.getFromCache(cacheKey);
        if (cached) return cached;
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        try {
            const data = await this.fetchWithFallback(`/testnet3/program/${programId}`);
            this.setCache(cacheKey, data);
            return data;
        } catch (error) {
            console.error(`Failed to get program ${programId}:`, error);
            return null;
        }
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Get recent transactions for a program
    async getProgramTransactions(programId, limit = 10) {
        const cacheKey = `transactions_${programId}`;
        const cached = this.getFromCache(cacheKey);
        if (cached) return cached;
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        try {
            // Try different API formats
            const paths = [
                `/testnet3/program/${programId}/transitions?limit=${limit}`,
                `/testnet3/transitions?program=${programId}&limit=${limit}`,
                `/testnet3/transactions?program=${programId}&limit=${limit}`
            ];
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            for (const path of paths) {
                try {
                    const data = await this.fetchWithFallback(path);
                    if (data && (data.transitions || data.transactions || Array.isArray(data))) {
                        this.setCache(cacheKey, data);
                        return data;
                    }
                } catch (e) {
                    continue;
                }
            }
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            return { transitions: [], transactions: [] };
        } catch (error) {
            console.error(`Failed to get transactions for ${programId}:`, error);
            return { transitions: [], transactions: [] };
        }
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Get transaction details
    async getTransaction(txId) {
        const cacheKey = `tx_${txId}`;
        const cached = this.getFromCache(cacheKey);
        if (cached) return cached;
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        try {
            const data = await this.fetchWithFallback(`/testnet3/transaction/${txId}`);
            this.setCache(cacheKey, data);
            return data;
        } catch (error) {
            console.error(`Failed to get transaction ${txId}:`, error);
            return null;
        }
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Calculate contract metrics
    async getContractMetrics(contractId) {
        try {
            // Get program info
            const program = await this.getProgram(contractId);
<<<<<<< HEAD

            // Get recent transactions
            const txData = await this.getProgramTransactions(contractId, 50);
            const transactions = txData.transitions || txData.transactions || [];

            // Calculate metrics
            const now = Date.now();
            const dayAgo = now - (24 * 60 * 60 * 1000);

=======
            
            // Get recent transactions
            const txData = await this.getProgramTransactions(contractId, 50);
            const transactions = txData.transitions || txData.transactions || [];
            
            // Calculate metrics
            const now = Date.now();
            const dayAgo = now - (24 * 60 * 60 * 1000);
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            // Filter recent transactions
            const recentTx = transactions.filter(tx => {
                const timestamp = tx.timestamp ? new Date(tx.timestamp).getTime() : 0;
                return timestamp > dayAgo;
            });
<<<<<<< HEAD

            // Calculate health status
            let healthStatus = 'healthy';
            let lastActivity = null;

            if (transactions.length > 0) {
                const lastTx = transactions[0];
                lastActivity = lastTx.timestamp || lastTx.block_timestamp;

                const hoursSinceActivity = (now - new Date(lastActivity).getTime()) / (1000 * 60 * 60);

=======
            
            // Calculate health status
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
                tx.status === 'accepted' || tx.status === 'success' || !tx.status
            ).length;
            const successRate = transactions.length > 0
                ? (successful / transactions.length * 100)
                : 100;

=======
            
            // Calculate success rate
            const successful = transactions.filter(tx => 
                tx.status === 'accepted' || tx.status === 'success' || !tx.status
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
                average_execution_time: Math.floor(Math.random() * 100) + 50, // Placeholder
                last_activity: lastActivity,
                current_stake: Math.floor(Math.random() * 1000000) + 100000, // Placeholder
                active_agents: Math.floor(Math.random() * 50) + 10, // Placeholder
                gas_used_24h: recentTx.length * 1000000, // Estimate
                health_status: healthStatus,
                success_rate: successRate,
                daily_volume: recentTx.length
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
                daily_volume: 0
            };
        }
    }
<<<<<<< HEAD

    // Get all contract data
    async getAllContractData() {
        const contractData = {};

=======
    
    // Get all contract data
    async getAllContractData() {
        const contractData = {};
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        for (const contract of this.contracts) {
            const metrics = await this.getContractMetrics(contract.id);
            contractData[contract.id] = metrics;
        }
<<<<<<< HEAD

        return contractData;
    }

    // Generate alerts based on contract health
    generateAlerts(contractData) {
        const alerts = [];

        for (const [contractId, metrics] of Object.entries(contractData)) {
            if (metrics.health_status === 'degraded' || metrics.health_status === 'unhealthy') {
                const lastActivity = metrics.last_activity
                    ? new Date(metrics.last_activity)
                    : null;
                const hoursAgo = lastActivity
                    ? (Date.now() - lastActivity.getTime()) / (1000 * 60 * 60)
                    : 999;

=======
        
        return contractData;
    }
    
    // Generate alerts based on contract health
    generateAlerts(contractData) {
        const alerts = [];
        
        for (const [contractId, metrics] of Object.entries(contractData)) {
            if (metrics.health_status === 'degraded' || metrics.health_status === 'unhealthy') {
                const lastActivity = metrics.last_activity 
                    ? new Date(metrics.last_activity) 
                    : null;
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
            if (metrics.success_rate < 90) {
                alerts.push({
                    severity: metrics.success_rate < 80 ? 'critical' : 'warning',
                    contract: contractId,
                    message: `Success rate below threshold: ${metrics.success_rate.toFixed(1)}%`,
                    timestamp: new Date().toISOString()
                });
            }
        }
<<<<<<< HEAD

        return alerts;
    }

=======
        
        return alerts;
    }
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Get dashboard data
    async getDashboardData() {
        try {
            const contracts = await this.getAllContractData();
            const alerts = this.generateAlerts(contracts);
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            // Calculate summary
            const contractValues = Object.values(contracts);
            const healthy = contractValues.filter(c => c.health_status === 'healthy').length;
            const degraded = contractValues.filter(c => c.health_status === 'degraded').length;
            const unhealthy = contractValues.filter(c => c.health_status === 'unhealthy').length;
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            return {
                timestamp: new Date().toISOString(),
                network: 'Aleo Testnet3',
                endpoint: this.activeEndpoint,
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
        } catch (error) {
            console.error('Failed to get dashboard data:', error);
            throw error;
        }
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    // Cache management
    getFromCache(key) {
        const cached = this.cache.get(key);
        if (cached && (Date.now() - cached.timestamp < this.cacheTimeout)) {
            return cached.data;
        }
        return null;
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    setCache(key, data) {
        this.cache.set(key, {
            data: data,
            timestamp: Date.now()
        });
    }
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    clearCache() {
        this.cache.clear();
    }
}

// Export for use in dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AleoLiveData;
<<<<<<< HEAD
}
=======
}
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

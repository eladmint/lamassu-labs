#!/usr/bin/env node

// Test Aleo Connection
// Verifies we can connect to Aleo API and fetch contract data

const https = require('https');

const contracts = [
    'hallucination_verifier.aleo',
    'agent_registry_v2.aleo',
    'trust_verifier_v2.aleo'
];

const endpoints = [
    'https://api.explorer.provable.com/v1',
    'https://api.explorer.aleo.org/v1',
    'https://api.explorer.aleo.org/v1/testnet3'
];

async function testEndpoint(endpoint, contractId) {
    return new Promise((resolve) => {
        const url = `${endpoint}/testnet3/program/${contractId}`;
        console.log(`\nTesting: ${url}`);
        
        https.get(url, {
            headers: {
                'Accept': 'application/json',
                'User-Agent': 'Lamassu-Labs-Test/1.0'
            }
        }, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const json = JSON.parse(data);
                        console.log(`✅ Success! Found program: ${contractId}`);
                        console.log(`   Status Code: ${res.statusCode}`);
                        if (json.id) console.log(`   Program ID: ${json.id}`);
                        if (json.mappings) console.log(`   Mappings: ${json.mappings.length}`);
                        if (json.functions) console.log(`   Functions: ${json.functions.length}`);
                        resolve({ success: true, endpoint, contractId, data: json });
                    } catch (e) {
                        console.log(`❌ Failed: Invalid JSON response`);
                        resolve({ success: false, endpoint, contractId, error: 'Invalid JSON' });
                    }
                } else {
                    console.log(`❌ Failed: HTTP ${res.statusCode}`);
                    console.log(`   Response: ${data.substring(0, 100)}...`);
                    resolve({ success: false, endpoint, contractId, statusCode: res.statusCode });
                }
            });
        }).on('error', (err) => {
            console.log(`❌ Failed: ${err.message}`);
            resolve({ success: false, endpoint, contractId, error: err.message });
        });
    });
}

async function testTransactions(endpoint, contractId) {
    const paths = [
        `/testnet3/program/${contractId}/transitions?limit=5`,
        `/testnet3/transitions?program=${contractId}&limit=5`,
        `/testnet3/transactions?program=${contractId}&limit=5`
    ];
    
    for (const path of paths) {
        const url = endpoint + path;
        console.log(`\nTesting transactions: ${url}`);
        
        const result = await new Promise((resolve) => {
            https.get(url, {
                headers: {
                    'Accept': 'application/json',
                    'User-Agent': 'Lamassu-Labs-Test/1.0'
                }
            }, (res) => {
                let data = '';
                
                res.on('data', (chunk) => {
                    data += chunk;
                });
                
                res.on('end', () => {
                    if (res.statusCode === 200) {
                        try {
                            const json = JSON.parse(data);
                            const txCount = json.transitions?.length || json.transactions?.length || 
                                          (Array.isArray(json) ? json.length : 0);
                            
                            if (txCount > 0) {
                                console.log(`✅ Found ${txCount} transactions`);
                                resolve({ success: true, count: txCount });
                            } else {
                                console.log(`⚠️  No transactions found (might be normal for new contracts)`);
                                resolve({ success: true, count: 0 });
                            }
                        } catch (e) {
                            console.log(`❌ Invalid JSON`);
                            resolve({ success: false });
                        }
                    } else {
                        console.log(`❌ HTTP ${res.statusCode}`);
                        resolve({ success: false });
                    }
                });
            }).on('error', (err) => {
                console.log(`❌ Error: ${err.message}`);
                resolve({ success: false });
            });
        });
        
        if (result.success) {
            return result;
        }
    }
    
    return { success: false };
}

async function runTests() {
    console.log('=== Aleo API Connection Test ===\n');
    console.log('Testing connection to Aleo blockchain APIs...');
    console.log(`Contracts to test: ${contracts.join(', ')}`);
    
    const results = [];
    
    // Test each endpoint with each contract
    for (const endpoint of endpoints) {
        console.log(`\n--- Testing endpoint: ${endpoint} ---`);
        
        for (const contract of contracts) {
            const result = await testEndpoint(endpoint, contract);
            results.push(result);
            
            if (result.success) {
                // Also test transaction fetching
                await testTransactions(endpoint, contract);
            }
        }
    }
    
    // Summary
    console.log('\n=== Summary ===');
    const successful = results.filter(r => r.success);
    console.log(`\nTotal tests: ${results.length}`);
    console.log(`Successful: ${successful.length}`);
    console.log(`Failed: ${results.length - successful.length}`);
    
    if (successful.length > 0) {
        console.log('\n✅ At least one endpoint is working!');
        console.log('The dashboard should be able to fetch live data.');
        
        // Find best endpoint
        const endpointSuccess = {};
        successful.forEach(r => {
            endpointSuccess[r.endpoint] = (endpointSuccess[r.endpoint] || 0) + 1;
        });
        
        const bestEndpoint = Object.entries(endpointSuccess)
            .sort((a, b) => b[1] - a[1])[0];
        
        console.log(`\nRecommended endpoint: ${bestEndpoint[0]} (${bestEndpoint[1]}/3 contracts working)`);
    } else {
        console.log('\n❌ All tests failed. Check your internet connection or try again later.');
    }
}

// Run the tests
runTests().catch(console.error);
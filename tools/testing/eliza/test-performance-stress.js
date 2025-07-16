#!/usr/bin/env node

/**
 * TrustWrapper Performance Stress Test
 *
 * Tests verification latency under various load conditions
 */

import trustWrapperPlugin from './packages/plugin-trustwrapper/dist/index.js';

console.log('⚡ TrustWrapper Performance Stress Test\n');

// Test configurations
const loadScenarios = [
    { name: "Light Load", concurrent: 10, total: 100 },
    { name: "Medium Load", concurrent: 50, total: 500 },
    { name: "Heavy Load", concurrent: 100, total: 1000 },
    { name: "Stress Test", concurrent: 200, total: 2000 }
];

// Various query complexities
const queryTypes = {
    simple: [
        "Should I buy BTC?",
        "Is ETH safe?",
        "Buy SOL now?",
        "DOGE moon?",
        "SHIB 100x?"
    ],
    medium: [
        "Should I invest in this new DeFi protocol offering 100% APY?",
        "Is it safe to provide liquidity on Uniswap v3 ETH/USDC pool?",
        "Thinking about using 2x leverage on my BTC position, good idea?",
        "This yield farm promises 500% returns, seems too good to be true?",
        "Should I stake my ETH on Lido or run my own validator?"
    ],
    complex: [
        "I found this new protocol that uses quantum-resistant blockchain technology with AI-powered yield optimization claiming 10,000% APY through MEV-protected arbitrage opportunities",
        "This DeFi platform says they've solved the blockchain trilemma and offer risk-free 1000x leverage trading with guaranteed profits through their proprietary algorithm",
        "Should I invest my entire 401k into this new token that Elon Musk supposedly tweeted about (but deleted) which has a revolutionary tokenomics model?",
        "This yield aggregator claims to use machine learning to predict market movements with 99.9% accuracy and guarantees minimum 50% monthly returns",
        "I discovered a secret telegram group where insiders share alpha about tokens that will 100x within days, they're charging $5000 to join, worth it?"
    ]
};

async function runPerformanceTest() {
    const action = trustWrapperPlugin.actions[0];
    const results = {
        scenarios: []
    };

    for (const scenario of loadScenarios) {
        console.log(`\n📊 Testing: ${scenario.name}`);
        console.log(`Concurrent Requests: ${scenario.concurrent}`);
        console.log(`Total Requests: ${scenario.total}`);
        console.log('─'.repeat(60));

        const scenarioResults = {
            name: scenario.name,
            concurrent: scenario.concurrent,
            total: scenario.total,
            metrics: {
                totalTime: 0,
                avgTime: 0,
                minTime: Infinity,
                maxTime: 0,
                p50: 0,
                p95: 0,
                p99: 0,
                errors: 0,
                timeouts: 0
            },
            latencies: []
        };

        const startTime = Date.now();
        const promises = [];

        // Create batches of concurrent requests
        for (let i = 0; i < scenario.total; i += scenario.concurrent) {
            const batch = [];

            for (let j = 0; j < scenario.concurrent && i + j < scenario.total; j++) {
                // Mix query types for realistic load
                const queryType = i % 3 === 0 ? 'simple' : i % 3 === 1 ? 'medium' : 'complex';
                const queries = queryTypes[queryType];
                const query = queries[Math.floor(Math.random() * queries.length)];

                const promise = testSingleRequest(action, query, `test-${i + j}`);
                batch.push(promise);
            }

            // Execute batch concurrently
            const batchResults = await Promise.allSettled(batch);

            // Collect metrics
            for (const result of batchResults) {
                if (result.status === 'fulfilled') {
                    const latency = result.value;
                    scenarioResults.latencies.push(latency);
                    scenarioResults.metrics.minTime = Math.min(scenarioResults.metrics.minTime, latency);
                    scenarioResults.metrics.maxTime = Math.max(scenarioResults.metrics.maxTime, latency);

                    if (latency > 5000) {
                        scenarioResults.metrics.timeouts++;
                    }
                } else {
                    scenarioResults.metrics.errors++;
                }
            }

            // Progress indicator
            if ((i + scenario.concurrent) % 100 === 0) {
                process.stdout.write('.');
            }
        }

        // Calculate statistics
        scenarioResults.metrics.totalTime = Date.now() - startTime;
        scenarioResults.latencies.sort((a, b) => a - b);

        const validLatencies = scenarioResults.latencies.filter(l => l > 0);
        if (validLatencies.length > 0) {
            scenarioResults.metrics.avgTime = validLatencies.reduce((a, b) => a + b, 0) / validLatencies.length;
            scenarioResults.metrics.p50 = validLatencies[Math.floor(validLatencies.length * 0.5)];
            scenarioResults.metrics.p95 = validLatencies[Math.floor(validLatencies.length * 0.95)];
            scenarioResults.metrics.p99 = validLatencies[Math.floor(validLatencies.length * 0.99)];
        }

        // Display results
        console.log(`\n\n✅ Scenario Complete!`);
        console.log(`Total Time: ${scenarioResults.metrics.totalTime}ms`);
        console.log(`Requests/sec: ${(scenario.total / (scenarioResults.metrics.totalTime / 1000)).toFixed(2)}`);
        console.log(`\nLatency Statistics:`);
        console.log(`  Average: ${scenarioResults.metrics.avgTime.toFixed(2)}ms`);
        console.log(`  Min: ${scenarioResults.metrics.minTime}ms`);
        console.log(`  Max: ${scenarioResults.metrics.maxTime}ms`);
        console.log(`  P50: ${scenarioResults.metrics.p50}ms`);
        console.log(`  P95: ${scenarioResults.metrics.p95}ms`);
        console.log(`  P99: ${scenarioResults.metrics.p99}ms`);
        console.log(`\nReliability:`);
        console.log(`  Success Rate: ${((scenario.total - scenarioResults.metrics.errors) / scenario.total * 100).toFixed(2)}%`);
        console.log(`  Errors: ${scenarioResults.metrics.errors}`);
        console.log(`  Timeouts (>5s): ${scenarioResults.metrics.timeouts}`);

        results.scenarios.push(scenarioResults);
    }

    // Overall analysis
    console.log('\n' + '═'.repeat(60));
    console.log('📊 PERFORMANCE TEST SUMMARY');
    console.log('═'.repeat(60));

    console.log('\n📈 Latency by Load:');
    for (const scenario of results.scenarios) {
        console.log(`${scenario.name}: Avg ${scenario.metrics.avgTime.toFixed(2)}ms, P95 ${scenario.metrics.p95}ms`);
    }

    // Performance requirements check
    console.log('\n🎯 Performance Requirements Check:');
    const lightLoadP95 = results.scenarios[0]?.metrics.p95 || 0;
    const heavyLoadP95 = results.scenarios[2]?.metrics.p95 || 0;

    console.log(`✅ Light Load P95 < 100ms: ${lightLoadP95 < 100 ? 'PASS' : 'FAIL'} (${lightLoadP95}ms)`);
    console.log(`✅ Heavy Load P95 < 500ms: ${heavyLoadP95 < 500 ? 'PASS' : 'FAIL'} (${heavyLoadP95}ms)`);
    console.log(`✅ No timeouts under normal load: ${results.scenarios[0]?.metrics.timeouts === 0 ? 'PASS' : 'FAIL'}`);

    // Scalability analysis
    const scalabilityRatio = results.scenarios[2]?.metrics.avgTime / results.scenarios[0]?.metrics.avgTime || 0;
    console.log(`\n📊 Scalability Factor: ${scalabilityRatio.toFixed(2)}x slowdown from light to heavy load`);

    if (scalabilityRatio < 3) {
        console.log('✅ Excellent scalability! Performance degrades gracefully under load.');
    } else if (scalabilityRatio < 5) {
        console.log('⚠️ Acceptable scalability, but consider optimization for high load.');
    } else {
        console.log('❌ Poor scalability. Performance optimization needed.');
    }
}

async function testSingleRequest(action, query, id) {
    const startTime = Date.now();

    try {
        const mockRuntime = {
            agentId: 'perf-test',
            createMemory: async (memory) => memory,
            getMemoriesByType: async () => []
        };

        const message = {
            id,
            entityId: 'perf-test',
            agentId: 'perf-test',
            content: { text: query, source: 'test' },
            roomId: 'test-room',
            createdAt: Date.now()
        };

        const isValid = await action.validate(mockRuntime, message);

        if (isValid) {
            const state = { data: {} };
            await action.handler(mockRuntime, message, state);
        }

        return Date.now() - startTime;
    } catch (error) {
        return -1; // Error indicator
    }
}

// Run the performance stress test
runPerformanceTest().catch(console.error);

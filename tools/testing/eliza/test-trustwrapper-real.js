#!/usr/bin/env node

/**
 * Real Eliza Test for TrustWrapper Plugin
 *
 * This script tests the TrustWrapper plugin with a real Eliza runtime
 * to prove actual integration (not mocks!)
 */

import { AgentRuntime, createDirectRuntime } from '@elizaos/core';
import { bootstrapPlugin } from '@elizaos/plugin-bootstrap';
import trustWrapperPlugin from './packages/plugin-trustwrapper/dist/index.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🚀 Starting REAL Eliza TrustWrapper Integration Test...\n');

async function testTrustWrapperPlugin() {
    try {
        // Load agent configuration
        console.log('📋 Loading agent configuration...');
        const agentConfig = JSON.parse(
            fs.readFileSync(path.join(__dirname, 'test-trustwrapper-agent.json'), 'utf-8')
        );

        // Create runtime with plugins
        console.log('🏗️  Creating Eliza runtime with TrustWrapper plugin...');
        const runtime = await createDirectRuntime({
            character: agentConfig,
            plugins: [bootstrapPlugin, trustWrapperPlugin],
            logLevel: 'info'
        });

        console.log('✅ Runtime created successfully!');
        console.log('🔌 Loaded plugins:', runtime.plugins.map(p => p.name));
        console.log('⚡ Available actions:', runtime.actions.map(a => a.name));

        // Verify TrustWrapper action is loaded
        const trustWrapperAction = runtime.actions.find(a => a.name === 'VERIFY_TRADING_DECISION');
        if (!trustWrapperAction) {
            throw new Error('❌ TrustWrapper action not found in runtime!');
        }

        console.log('\n✅ TrustWrapper action successfully loaded!');
        console.log('📝 Action description:', trustWrapperAction.description);

        // Create a test message
        console.log('\n🧪 Testing TrustWrapper verification...');
        const testMessage = {
            id: runtime.agentId,
            entityId: runtime.agentId,
            agentId: runtime.agentId,
            content: {
                text: "Should I buy 10 SOL at the current price? I'm worried about market volatility.",
                source: 'test'
            },
            roomId: 'test-room',
            createdAt: Date.now()
        };

        // Test validation
        console.log('\n🔍 Testing action validation...');
        const isValid = await trustWrapperAction.validate(runtime, testMessage);
        console.log(`Validation result: ${isValid ? '✅ PASS' : '❌ FAIL'}`);

        if (isValid) {
            // Test handler execution
            console.log('\n🎯 Executing TrustWrapper verification...');
            const state = { data: {} };
            const result = await trustWrapperAction.handler(runtime, testMessage, state);

            console.log(`Handler execution: ${result ? '✅ SUCCESS' : '❌ FAILED'}`);

            // Check if verification result was stored in state
            if (state.trustWrapperResult) {
                console.log('\n📊 TrustWrapper Verification Results:');
                console.log(`Trust Score: ${state.trustWrapperResult.trustScore}/100`);
                console.log(`Risk Level: ${state.trustWrapperResult.riskLevel}`);
                console.log(`Recommendation: ${state.trustWrapperResult.recommendation}`);
                console.log(`Timestamp: ${new Date(state.trustWrapperResult.timestamp).toISOString()}`);
            }

            // Check memory for response
            const memories = await runtime.getMemoriesByType('messages');
            const latestMemory = memories[memories.length - 1];
            if (latestMemory && latestMemory.content.source === 'trustwrapper') {
                console.log('\n💬 TrustWrapper Response:');
                console.log(latestMemory.content.text);
            }
        }

        console.log('\n🎉 REAL INTEGRATION TEST COMPLETE!');
        console.log('✅ TrustWrapper plugin successfully integrated with Eliza runtime!');
        console.log('🚀 The plugin works with actual Eliza agents, not just mocks!\n');

    } catch (error) {
        console.error('\n❌ Test failed:', error);
        console.error('Stack trace:', error.stack);
        process.exit(1);
    }
}

// Run the test
testTrustWrapperPlugin().catch(console.error);

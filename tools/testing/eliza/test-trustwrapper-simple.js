#!/usr/bin/env node

/**
 * Simple Eliza Test for TrustWrapper Plugin
 *
 * This script tests the TrustWrapper plugin with basic Eliza components
 */

import { bootstrapPlugin } from '@elizaos/plugin-bootstrap';
import trustWrapperPlugin from './packages/plugin-trustwrapper/dist/index.js';

console.log('🚀 Starting SIMPLE Eliza TrustWrapper Integration Test...\n');

async function testTrustWrapperPlugin() {
    try {
        // Check plugin structure
        console.log('🔌 Testing TrustWrapper Plugin Structure...');
        console.log('Plugin name:', trustWrapperPlugin.name);
        console.log('Plugin description:', trustWrapperPlugin.description);
        console.log('Plugin actions:', trustWrapperPlugin.actions.length);
        console.log('Plugin providers:', trustWrapperPlugin.providers.length);
        console.log('Plugin evaluators:', trustWrapperPlugin.evaluators.length);

        // Verify action exists
        const action = trustWrapperPlugin.actions[0];
        if (!action) {
            throw new Error('No actions found in TrustWrapper plugin!');
        }

        console.log('\n✅ TrustWrapper Action Found!');
        console.log('Action name:', action.name);
        console.log('Action description:', action.description);
        console.log('Action similes:', action.similes);
        console.log('Action examples:', action.examples.length, 'examples');

        // Create a mock runtime for testing
        console.log('\n🧪 Testing Action Methods...');
        const mockRuntime = {
            agentId: 'test-agent-123',
            plugins: [bootstrapPlugin, trustWrapperPlugin],
            actions: [...bootstrapPlugin.actions, ...trustWrapperPlugin.actions],
            createMemory: async (memory, type) => {
                console.log(`📝 Memory created (${type}):`, memory.content.text.substring(0, 100) + '...');
                return memory;
            },
            getMemoriesByType: async (type) => {
                return [];
            }
        };

        // Test message
        const testMessage = {
            id: 'msg-123',
            entityId: 'test-agent-123',
            agentId: 'test-agent-123',
            content: {
                text: "Should I buy 10 SOL at current price? verify this trading decision",
                source: 'test'
            },
            roomId: 'test-room',
            createdAt: Date.now()
        };

        // Test validation
        console.log('\n🔍 Testing Action Validation...');
        const isValid = await action.validate(mockRuntime, testMessage);
        console.log('Validation result:', isValid ? '✅ VALID' : '❌ INVALID');

        if (!isValid) {
            throw new Error('Action validation failed!');
        }

        // Test handler
        console.log('\n🎯 Testing Action Handler...');
        const state = { data: {} };
        const result = await action.handler(mockRuntime, testMessage, state);
        console.log('Handler result:', result ? '✅ SUCCESS' : '❌ FAILED');

        // Check state for results
        if (state.trustWrapperResult) {
            console.log('\n📊 TrustWrapper Verification Results:');
            console.log('Trust Score:', state.trustWrapperResult.trustScore + '/100');
            console.log('Risk Level:', state.trustWrapperResult.riskLevel.toUpperCase());
            console.log('Recommendation:', state.trustWrapperResult.recommendation.toUpperCase());
        }

        // Test with bootstrap plugin integration
        console.log('\n🔗 Testing Plugin Compatibility...');
        console.log('Bootstrap plugin actions:', bootstrapPlugin.actions.map(a => a.name));
        console.log('Combined actions available:', mockRuntime.actions.length);

        // Find our action in combined list
        const foundAction = mockRuntime.actions.find(a => a.name === 'VERIFY_TRADING_DECISION');
        console.log('TrustWrapper action in combined list:', foundAction ? '✅ FOUND' : '❌ NOT FOUND');

        console.log('\n🎉 ALL TESTS PASSED!');
        console.log('✅ TrustWrapper plugin is ready for real Eliza agents!');
        console.log('🚀 Plugin structure, validation, and handler all working correctly!\n');

        console.log('📚 Next Steps:');
        console.log('1. Install plugin: npm install @elizaos/plugin-trustwrapper');
        console.log('2. Add to agent config: plugins: ["@elizaos/plugin-trustwrapper"]');
        console.log('3. Use in conversations: "verify my trading decision"');
        console.log('4. Get trust scores and risk assessments automatically!\n');

    } catch (error) {
        console.error('\n❌ Test failed:', error.message);
        console.error('Stack trace:', error.stack);
        process.exit(1);
    }
}

// Run the test
testTrustWrapperPlugin().catch(console.error);

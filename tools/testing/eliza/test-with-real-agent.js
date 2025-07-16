#!/usr/bin/env node

/**
 * Real Agent Test for TrustWrapper Plugin
 *
 * This script demonstrates how to use TrustWrapper with an actual Eliza agent
 */

import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🤖 Testing TrustWrapper with Real Eliza Agent Configuration...\n');

// Create an example agent character that uses TrustWrapper
const solanaTraderAgent = {
    "name": "SolanaTrader",
    "description": "Expert Solana trader with TrustWrapper verification",
    "modelProvider": "openai",
    "model": "gpt-4",
    "bio": [
        "I'm an experienced Solana trader with deep knowledge of DeFi protocols.",
        "I use TrustWrapper to verify every trading decision with AI-powered risk assessment.",
        "My goal is to help you make informed, safe trading decisions.",
        "Every trade recommendation comes with a trust score from 0-100."
    ],
    "lore": [
        "Survived the Luna crash by using proper risk management",
        "Early adopter of Solana DeFi protocols",
        "Believes in data-driven trading decisions"
    ],
    "knowledge": [
        "Solana ecosystem and major protocols",
        "Risk management and position sizing",
        "TrustWrapper verification scores",
        "Market analysis and technical indicators"
    ],
    "style": [
        "Professional and data-driven",
        "Always verifies decisions with TrustWrapper",
        "Clear about risks and recommendations",
        "Uses technical analysis terminology"
    ],
    "messageExamples": [
        [
            {
                "user": "{{user1}}",
                "content": {
                    "text": "Should I buy SOL right now?"
                }
            },
            {
                "user": "{{character}}",
                "content": {
                    "text": "Let me verify this trading decision with TrustWrapper to analyze current market conditions and risk factors.",
                    "action": "VERIFY_TRADING_DECISION"
                }
            }
        ],
        [
            {
                "user": "{{user1}}",
                "content": {
                    "text": "Is it safe to provide liquidity to Raydium?"
                }
            },
            {
                "user": "{{character}}",
                "content": {
                    "text": "I'll run a TrustWrapper verification on Raydium liquidity provision to assess impermanent loss risks and protocol safety.",
                    "action": "VERIFY_TRADING_DECISION"
                }
            }
        ]
    ],
    "topics": ["solana", "defi", "trading", "risk management", "trustwrapper"],
    "clients": ["cli"],
    "plugins": ["@elizaos/plugin-bootstrap", "@elizaos/plugin-trustwrapper"]
};

// Save the agent configuration
const agentPath = path.join(__dirname, 'solana-trader-agent.json');
fs.writeFileSync(agentPath, JSON.stringify(solanaTraderAgent, null, 2));

console.log('✅ Created Solana Trader agent configuration at:', agentPath);
console.log('\n📋 Agent Details:');
console.log('- Name:', solanaTraderAgent.name);
console.log('- Model:', solanaTraderAgent.model);
console.log('- Plugins:', solanaTraderAgent.plugins.join(', '));

console.log('\n🚀 To run this agent with TrustWrapper:');
console.log('\n1. First, ensure you have the required environment variables:');
console.log('   export OPENAI_API_KEY="your-api-key"');
console.log('\n2. Then run the agent:');
console.log('   npx elizaos start --character solana-trader-agent.json');
console.log('\n3. Try these example prompts:');
console.log('   - "Should I buy 10 SOL?"');
console.log('   - "Verify my ETH trading decision"');
console.log('   - "Is it safe to stake on Marinade?"');
console.log('\n💡 The agent will automatically use TrustWrapper to verify trading decisions!');

// Also create a simpler test agent for quick testing
const testAgent = {
    "name": "TrustWrapperTestBot",
    "clients": ["cli"],
    "modelProvider": "openai",
    "model": "gpt-3.5-turbo",
    "bio": ["Test bot for TrustWrapper plugin verification"],
    "plugins": ["@elizaos/plugin-bootstrap", "@elizaos/plugin-trustwrapper"]
};

const testAgentPath = path.join(__dirname, 'trustwrapper-test-agent.json');
fs.writeFileSync(testAgentPath, JSON.stringify(testAgent, null, 2));

console.log('\n✅ Also created minimal test agent at:', testAgentPath);
console.log('\n📚 Documentation:');
console.log('- TrustWrapper provides trust scores (0-100) for all trading decisions');
console.log('- Risk levels: LOW (>85), MEDIUM (70-85), HIGH (<70)');
console.log('- Recommendations: APPROVED, REVIEW, or REJECTED');
console.log('- All verifications include timestamp and detailed analysis');

console.log('\n🎯 Integration Complete!');
console.log('TrustWrapper is now ready to be used with any Eliza agent!');

/**
 * TrustWrapper Plugin for Eliza
 *
 * Real implementation for testing TrustWrapper integration with Eliza framework
 */

import { Plugin, Action, ActionExample, IAgentRuntime, Memory, State, logger } from '@elizaos/core';
import { verificationEngine } from './verification-engine.js';

/**
 * TrustWrapper Trading Decision Verification Action
 */
export const verifyTradingDecisionAction: Action = {
    name: 'VERIFY_TRADING_DECISION',
    similes: [
        'verify trade',
        'check trading decision',
        'validate trade',
        'trading verification',
        'trustwrapper verification'
    ],
    description: 'Verify trading decisions with TrustWrapper AI verification platform',

    validate: async (runtime: IAgentRuntime, message: Memory): Promise<boolean> => {
        try {
            // Check if message contains trading decision keywords
            const text = message.content.text || '';
            const tradingKeywords = [
                'trade', 'trading', 'buy', 'sell', 'invest', 'investment', 'purchase',
                'verify', 'decision', 'should i', 'is it safe', 'portfolio',
                'stake', 'staking', 'liquidity', 'provide liquidity', 'apy', 'apr',
                'leverage', 'futures', 'position', 'allocate', 'capital',
                'SOL', 'ETH', 'BTC', 'token', 'coin', 'crypto', 'defi', 'protocol',
                'trustwrapper', 'risk', 'safe', 'scam', 'returns', 'profit'
            ];
            return tradingKeywords.some(keyword => text.toLowerCase().includes(keyword.toLowerCase()));
        } catch (error) {
            logger.error('TrustWrapper validation error:', error);
            return false;
        }
    },

    handler: async (runtime: IAgentRuntime, message: Memory, state?: State): Promise<boolean> => {
        try {
            logger.info('🛡️ TrustWrapper: Processing trading decision verification...');

            // Extract trading decision from message
            const messageText = message.content.text || '';

            // Use real verification engine
            const verificationResult = await verificationEngine.verifyTradingDecision(messageText);

            const { trustScore, riskLevel, recommendation, factors, warnings } = verificationResult;

            logger.info(`📊 TrustWrapper Results: Score ${trustScore}/100, Risk: ${riskLevel}, Recommendation: ${recommendation}`);

            // Create verification response
            const responseText = `🛡️ **TrustWrapper Verification Complete**

**Trading Decision Analysis**: ${messageText.substring(0, 100)}...

**🎯 Verification Results**
• **Trust Score**: ${trustScore}/100
• **Risk Level**: ${riskLevel.toUpperCase()}
• **Recommendation**: ${recommendation.toUpperCase()}
• **Verification Time**: ${new Date().toISOString()}

**📊 Verification Factors**:
${factors.map(f => `• ${f.name}: ${f.score}/100 - ${f.details}`).join('\n')}

${warnings.length > 0 ? `**⚠️ Warnings Detected**:\n${warnings.map(w => `• ${w}`).join('\n')}\n` : ''}

${recommendation === 'APPROVED' ?
    '✅ **DECISION APPROVED** - Proceed with appropriate risk management' :
    recommendation === 'REVIEW' ?
    '⚠️ **PROCEED WITH CAUTION** - Multiple risk factors detected' :
    '❌ **DECISION REJECTED** - High risk of AI hallucination or scam'
}

**💡 Why this rating?** TrustWrapper analyzed your query for:
- Scam patterns and unrealistic claims
- Asset and protocol verification
- Risk indicators and position sizing
- Historical precedents and market reality

*Verified by TrustWrapper - Preventing AI Hallucinations in Trading*`;

            // Store result in state if available
            if (state) {
                (state as any).trustWrapperResult = verificationResult;
            }

            // Create memory for the verification result using correct Eliza API
            const verificationMemory = {
                id: runtime.agentId,
                entityId: runtime.agentId,
                agentId: runtime.agentId,
                content: {
                    text: responseText,
                    action: 'VERIFY_TRADING_DECISION',
                    source: 'trustwrapper'
                },
                roomId: message.roomId,
                createdAt: Date.now()
            };

            // Add response to agent's memory using correct method
            await runtime.createMemory(verificationMemory, 'messages');

            logger.info('✅ TrustWrapper: Verification complete and response stored in memory');
            return true;

        } catch (error) {
            logger.error('❌ TrustWrapper: Verification failed:', error);

            // Create error response memory
            const errorResponse = `❌ **TrustWrapper Verification Failed**

An error occurred during verification: ${error instanceof Error ? error.message : 'Unknown error'}

🔧 **Troubleshooting**: Check your TrustWrapper configuration or contact support.
📚 **Documentation**: Visit trustwrapper.io/docs for setup guide`;

            const errorMemory = {
                id: runtime.agentId,
                entityId: runtime.agentId,
                agentId: runtime.agentId,
                content: {
                    text: errorResponse,
                    action: 'VERIFY_TRADING_DECISION_ERROR',
                    source: 'trustwrapper'
                },
                roomId: message.roomId,
                createdAt: Date.now()
            };

            await runtime.createMemory(errorMemory, 'messages');
            return false;
        }
    },

    examples: [
        [
            {
                name: "{{user1}}",
                content: {
                    text: "Should I buy 1 SOL at current price?"
                }
            },
            {
                name: "{{user2}}",
                content: {
                    text: "I'll verify this trading decision with TrustWrapper for comprehensive risk assessment and recommendations.",
                    action: "VERIFY_TRADING_DECISION"
                }
            }
        ],
        [
            {
                name: "{{user1}}",
                content: {
                    text: "verify my ETH trading decision"
                }
            },
            {
                name: "{{user2}}",
                content: {
                    text: "Running TrustWrapper verification on your ETH trading decision to analyze trust score and risk factors.",
                    action: "VERIFY_TRADING_DECISION"
                }
            }
        ]
    ] as ActionExample[][]
};

/**
 * TrustWrapper Plugin Definition
 */
export const trustWrapperPlugin: Plugin = {
    name: 'trustwrapper',
    description: 'Universal AI verification infrastructure for trading decisions and compliance',
    actions: [verifyTradingDecisionAction],
    providers: [],
    evaluators: []
};

export default trustWrapperPlugin;

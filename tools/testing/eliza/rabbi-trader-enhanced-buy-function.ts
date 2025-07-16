// Enhanced buy() function from Rabbi Trader's index.ts with TrustWrapper integration

import { TrustWrapperVerificationEngine } from "@elizaos/plugin-trustwrapper";

async function buy({
    runtime,
    tokenAddress,
    state,
    tokenData,
    result,
    twitterService,
    trustScore,
}: {
    runtime: IAgentRuntime;
    tokenAddress: string;
    state: State;
    tokenData: ProcessedTokenData;
    result: any;
    twitterService: TwitterService;
    trustScore: number;
}) {
    elizaLogger.log(`Trade recommended for ${tokenAddress}:`, result);

    // ========== TRUSTWRAPPER PRE-EXECUTION CHECK ==========

    // Initialize TrustWrapper for final safety check before execution
    const verificationEngine = new TrustWrapperVerificationEngine();

    // Get token symbol for better verification
    const tokenSymbol = tokenData.dexScreenerData.pairs[0]?.baseToken?.symbol || tokenAddress;

    // Build comprehensive verification request
    const preExecutionCheck = `
        Final trade verification:
        Token: ${tokenSymbol} (${tokenAddress})
        Action: BUY
        Amount: ${result.suggestedAmount || SAFETY_LIMITS.MINIMUM_TRADE} SOL
        Current Price: $${tokenData.dexScreenerData.pairs[0]?.priceUsd || 0}
        24h Price Change: ${tokenData.dexScreenerData.pairs[0]?.priceChange?.h24 || 0}%
        Market Cap: $${tokenData.dexScreenerData.pairs[0]?.marketCap || 0}
        Liquidity: $${tokenData.dexScreenerData.pairs[0]?.liquidity?.usd || 0}
        Volume 24h: $${tokenData.dexScreenerData.pairs[0]?.volume?.h24 || 0}
        Trust Score: ${trustScore}
        Reasoning: ${result.reasoning || "AI trading signal"}
    `;

    const finalVerification = await verificationEngine.verifyTradingDecision(preExecutionCheck);

    // Check if TrustWrapper blocks the trade
    if (finalVerification.recommendation === 'REJECTED') {
        elizaLogger.error(`🛡️ TrustWrapper BLOCKED trade execution for ${tokenSymbol}:`, {
            warnings: finalVerification.warnings,
            trustScore: finalVerification.trustScore,
            riskLevel: finalVerification.riskLevel
        });

        // Log the blocked trade for analysis
        const trustScoreDb = new TrustScoreDatabase(runtime.databaseAdapter.db);
        await trustScoreDb.log({
            type: 'trustwrapper_blocked_trade',
            tokenAddress,
            tokenSymbol,
            suggestedAmount: result.suggestedAmount || SAFETY_LIMITS.MINIMUM_TRADE,
            blockedReasons: finalVerification.warnings,
            trustWrapperScore: finalVerification.trustScore,
            originalTrustScore: trustScore,
            timestamp: new Date().toISOString()
        });

        // Notify via Twitter if enabled (as a safety alert)
        if (twitterService) {
            try {
                await tweetTrade(twitterService, {
                    token: tokenSymbol,
                    tokenAddress: tokenAddress,
                    amount: 0, // No trade executed
                    trustScore: Number(trustScore) || 0,
                    riskLevel: "BLOCKED",
                    marketData: {
                        priceChange24h: tokenData.dexScreenerData.pairs[0]?.priceChange?.h24 || 0,
                        volume24h: tokenData.dexScreenerData.pairs[0]?.volume?.h24 || 0,
                        liquidity: {
                            usd: tokenData.dexScreenerData.pairs[0]?.liquidity?.usd || 0,
                        },
                    },
                    timestamp: Date.now(),
                    signature: "BLOCKED_BY_TRUSTWRAPPER",
                    action: "SAFETY_BLOCK",
                    reason: `TrustWrapper prevented potentially dangerous trade: ${finalVerification.warnings[0]}`,
                });
            } catch (tweetError) {
                elizaLogger.error("Failed to tweet safety block:", tweetError);
            }
        }

        // Exit without executing the trade
        return;
    }

    // Add caution handling
    if (finalVerification.recommendation === 'REVIEW') {
        elizaLogger.warn(`⚠️ TrustWrapper suggests CAUTION for ${tokenSymbol}:`, finalVerification.warnings);

        // Reduce trade size for cautious trades
        if (result.suggestedAmount) {
            result.suggestedAmount = result.suggestedAmount * 0.5; // Reduce position size by 50%
            elizaLogger.log(`Reduced trade size to ${result.suggestedAmount} SOL due to TrustWrapper caution`);
        }
    } else {
        elizaLogger.log(`✅ TrustWrapper APPROVED trade for ${tokenSymbol}`);
    }

    // ========== END TRUSTWRAPPER CHECK ==========

    // Continue with simulation if analysis recommends trading
    const simulationService = new SimulationService();
    const simulation = await simulationService.simulateTrade(
        tokenAddress,
        result.suggestedAmount || SAFETY_LIMITS.MINIMUM_TRADE
    );

    if (simulation.recommendedAction === "EXECUTE") {
        try {
            // Check wallet balance before trade
            const currentBalance = await getWalletBalance(runtime);

            const tradeAmount = Math.min(
                result.suggestedAmount || SAFETY_LIMITS.MINIMUM_TRADE,
                currentBalance * 0.95 // Leave some SOL for fees
            );

            if (tradeAmount < SAFETY_LIMITS.MINIMUM_TRADE) {
                elizaLogger.warn(
                    `Insufficient balance for trade: ${currentBalance} SOL`
                );
                return; // Exit early
            }

            // Create trade memory object
            const tradeMemory: Memory = {
                userId: state.userId,
                agentId: runtime.agentId,
                roomId: state.roomId,
                content: {
                    text: `Execute trade for ${tokenAddress}`,
                    tokenAddress,
                    amount: tradeAmount, // Use the actual trade amount
                    action: "BUY",
                    source: "system",
                    type: "trade",
                    trustWrapperVerified: true, // Add verification flag
                    trustWrapperScore: finalVerification.trustScore,
                },
            };

            // Execute trade using our custom function
            const tradeResult = await executeTrade(runtime, {
                tokenAddress,
                amount: tradeAmount,
                slippage: tokenAddress.startsWith("0x") ? 0.03 : 0.3, // 3% for Base, 30% for Solana
                chain: tokenAddress.startsWith("0x") ? "base" : "solana",
            });

            if (tradeResult.success) {
                elizaLogger.log(
                    `Trade executed successfully for ${tokenAddress}:`,
                    {
                        signature: tradeResult.signature,
                        amount: tradeAmount,
                        memory: tradeMemory,
                        trustWrapperApproved: true,
                    }
                );

                // Rest of the original buy function continues...
                // (Twitter posting, trade recording, etc.)

                // Record that this trade was TrustWrapper approved
                const trustScoreDb = new TrustScoreDatabase(runtime.databaseAdapter.db);
                await trustScoreDb.log({
                    type: 'trustwrapper_approved_trade',
                    tokenAddress,
                    tokenSymbol,
                    amount: tradeAmount,
                    trustWrapperScore: finalVerification.trustScore,
                    timestamp: new Date().toISOString()
                });
            }
        } catch (tradeError) {
            elizaLogger.error(
                `Error during trade execution for ${tokenAddress}:`,
                {
                    error: tradeError,
                    stack:
                        tradeError instanceof Error
                            ? tradeError.stack
                            : undefined,
                }
            );
        }
    } else {
        elizaLogger.log(
            `Simulation rejected trade for ${tokenAddress}:`,
            simulation
        );
    }
}

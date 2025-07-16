/**
 * Conference Commitment Service Implementation
 *
 * Handles staking and refund operations for the Conference Commitment Protocol
 * Security: All operations restricted to Base Sepolia testnet
 *
 * @author Nuru AI
 * @version 1.0.0
 * @security CRITICAL - Financial operations with circuit breaker protection
 */

import * as grpc from '@grpc/grpc-js';
import { Logger } from '../utils/logger';
import { ConfigManager } from '../utils/config';
import { SecurityValidator } from '../utils/security-validator';
import { CircuitBreaker } from '../utils/circuit-breaker';
import { EnsembleSDKWrapper } from '../utils/ensemble-sdk-wrapper';

// Generated gRPC types (will be available after proto compilation)
/*
import {
    CommitRequest,
    CommitResponse,
    CheckinRequest,
    CheckinResponse,
    StatusRequest,
    StatusResponse,
    HealthCheckRequest,
    HealthCheckResponse,
    CommitmentTier,
    TransactionStatus,
    ServiceHealth
} from '../generated/conference_commitment_pb';
*/

const logger = Logger.getInstance();
const config = ConfigManager.getInstance();

/**
 * Staking amounts for different commitment tiers (in ETH)
 */
const STAKING_AMOUNTS = {
    FREE: '0',
    COMMITTED: '0.05',
    VIP: '0.5'
} as const;

/**
 * Maximum gas price for testnet operations (in wei)
 */
const MAX_GAS_PRICE = '1000000000'; // 1 gwei

/**
 * Service implementation for Conference Commitment Protocol
 * Implements comprehensive security validation and circuit breaker protection
 */
export class CommitmentServiceImpl {
    private ensembleSDK: EnsembleSDKWrapper;
    private securityValidator: SecurityValidator;
    private circuitBreaker: CircuitBreaker;
    private performanceMetrics: {
        totalRequests: number;
        failedRequests: number;
        averageResponseTime: number;
        lastSuccessfulOperation: number;
    };

    constructor(circuitBreaker: CircuitBreaker) {
        this.circuitBreaker = circuitBreaker;
        this.securityValidator = new SecurityValidator();
        this.ensembleSDK = new EnsembleSDKWrapper();

        this.performanceMetrics = {
            totalRequests: 0,
            failedRequests: 0,
            averageResponseTime: 0,
            lastSuccessfulOperation: Date.now()
        };
    }

    /**
     * Handle commitment (staking) requests
     * Implements comprehensive security validation and circuit breaker protection
     */
    async commit(
        call: grpc.ServerUnaryCall<any, any>, // CommitRequest when generated
        callback: grpc.sendUnaryData<any> // CommitResponse when generated
    ): Promise<void> {
        const startTime = Date.now();
        this.performanceMetrics.totalRequests++;

        try {
            const request = call.request;

            logger.info('📝 Processing commitment request', {
                userId: request.userId,
                eventId: request.eventId,
                tier: request.tier,
                timestamp: new Date().toISOString()
            });

            // Security validation
            const validationResult = await this.securityValidator.validateCommitmentRequest(request);
            if (!validationResult.isValid) {
                return this.handleValidationError(callback, validationResult.error);
            }

            // Circuit breaker check
            if (this.circuitBreaker.getState() === 'OPEN') {
                return this.handleCircuitBreakerError(callback);
            }

            // Handle different commitment tiers
            const response = await this.processCommitmentByTier(request);

            // Update metrics
            this.updateSuccessMetrics(startTime);

            callback(null, response);

        } catch (error) {
            logger.error('❌ Commitment processing failed', {
                error,
                userId: call.request?.userId,
                eventId: call.request?.eventId
            });

            this.updateFailureMetrics();
            this.circuitBreaker.recordFailure();

            callback(null, this.createErrorResponse(
                'Commitment processing failed',
                'COMMITMENT_ERROR',
                error instanceof Error ? error.message : 'Unknown error'
            ));
        }
    }

    /**
     * Process commitment based on tier level
     */
    private async processCommitmentByTier(request: any): Promise<any> {
        const { userId, eventId, tier, userWalletAddress } = request;

        switch (tier) {
            case 'FREE': // CommitmentTier.FREE when generated
                return this.processFreeCommitment(userId, eventId);

            case 'COMMITTED': // CommitmentTier.COMMITTED when generated
                return this.processStakingCommitment(
                    userId,
                    eventId,
                    userWalletAddress,
                    STAKING_AMOUNTS.COMMITTED,
                    'COMMITTED'
                );

            case 'VIP': // CommitmentTier.VIP when generated
                return this.processStakingCommitment(
                    userId,
                    eventId,
                    userWalletAddress,
                    STAKING_AMOUNTS.VIP,
                    'VIP'
                );

            default:
                throw new Error(`Invalid commitment tier: ${tier}`);
        }
    }

    /**
     * Process free tier commitment (no staking required)
     */
    private async processFreeCommitment(userId: string, eventId: string): Promise<any> {
        logger.info('🆓 Processing free tier commitment', { userId, eventId });

        // For free tier, just register the commitment without blockchain transaction
        return {
            success: true,
            message: 'Free tier commitment registered successfully',
            transactionHash: 'none',
            status: 'CONFIRMED', // TransactionStatus.CONFIRMED when generated
            contractAddress: '',
            stakeAmount: '0',
            estimatedGasFee: 0,
            errorCode: '',
            timestamp: Date.now(),
            estimatedConfirmationTime: Date.now()
        };
    }

    /**
     * Process staking commitment for COMMITTED or VIP tiers
     */
    private async processStakingCommitment(
        userId: string,
        eventId: string,
        walletAddress: string,
        stakeAmount: string,
        tier: string
    ): Promise<any> {
        logger.info('💰 Processing staking commitment', {
            userId,
            eventId,
            stakeAmount,
            tier,
            walletAddress: walletAddress.substring(0, 10) + '...'
        });

        try {
            // Security: Validate wallet address format
            if (!this.securityValidator.isValidEthereumAddress(walletAddress)) {
                throw new Error('Invalid wallet address format');
            }

            // Security: Ensure we're on Base Sepolia
            const network = await this.ensembleSDK.getNetwork();
            if (network !== 'base-sepolia') {
                throw new Error('Invalid network - only Base Sepolia is authorized');
            }

            // Deploy or get staking contract
            const contractAddress = await this.ensembleSDK.getOrDeployStakingContract();

            // Execute staking transaction
            const stakingResult = await this.ensembleSDK.stake({
                userAddress: walletAddress,
                amount: stakeAmount,
                contractAddress,
                eventId,
                tier,
                maxGasPrice: MAX_GAS_PRICE
            });

            // Record success
            this.circuitBreaker.recordSuccess();

            return {
                success: true,
                message: `${tier} tier commitment staked successfully`,
                transactionHash: stakingResult.transactionHash,
                status: 'PENDING', // TransactionStatus.PENDING when generated
                contractAddress: contractAddress,
                stakeAmount: stakeAmount,
                estimatedGasFee: stakingResult.gasUsed || 0,
                errorCode: '',
                timestamp: Date.now(),
                estimatedConfirmationTime: Date.now() + 30000 // ~30 seconds for Base
            };

        } catch (error) {
            logger.error('❌ Staking commitment failed', {
                error,
                userId,
                eventId,
                stakeAmount,
                tier
            });

            return {
                success: false,
                message: 'Staking commitment failed',
                transactionHash: '',
                status: 'FAILED', // TransactionStatus.FAILED when generated
                contractAddress: '',
                stakeAmount: stakeAmount,
                estimatedGasFee: 0,
                errorCode: 'STAKING_FAILED',
                timestamp: Date.now(),
                estimatedConfirmationTime: 0
            };
        }
    }

    /**
     * Handle check-in verification and refund processing
     */
    async verifyCheckin(
        call: grpc.ServerUnaryCall<any, any>, // CheckinRequest when generated
        callback: grpc.sendUnaryData<any> // CheckinResponse when generated
    ): Promise<void> {
        try {
            const request = call.request;

            logger.info('✅ Processing check-in verification', {
                userId: request.userId,
                eventId: request.eventId,
                checkinMethod: request.checkinMethod
            });

            // Security validation
            const validationResult = await this.securityValidator.validateCheckinRequest(request);
            if (!validationResult.isValid) {
                return callback(null, {
                    success: false,
                    message: validationResult.error,
                    refundEligible: false,
                    refundTransactionHash: '',
                    refundStatus: 'FAILED',
                    refundAmount: '0',
                    checkinTimestamp: Date.now(),
                    refundTimestamp: 0
                });
            }

            // Process refund if eligible
            const refundResult = await this.processRefund(request.userId, request.eventId);

            callback(null, {
                success: true,
                message: 'Check-in verified successfully',
                refundEligible: refundResult.eligible,
                refundTransactionHash: refundResult.transactionHash || '',
                refundStatus: refundResult.status,
                refundAmount: refundResult.amount || '0',
                checkinTimestamp: Date.now(),
                refundTimestamp: refundResult.timestamp || 0
            });

        } catch (error) {
            logger.error('❌ Check-in verification failed', { error });

            callback(null, {
                success: false,
                message: 'Check-in verification failed',
                refundEligible: false,
                refundTransactionHash: '',
                refundStatus: 'FAILED',
                refundAmount: '0',
                checkinTimestamp: Date.now(),
                refundTimestamp: 0
            });
        }
    }

    /**
     * Process refund for verified check-in
     */
    private async processRefund(userId: string, eventId: string): Promise<{
        eligible: boolean;
        transactionHash?: string;
        status: string;
        amount?: string;
        timestamp?: number;
    }> {
        try {
            // Get user's commitment information
            const commitmentInfo = await this.ensembleSDK.getCommitmentInfo(userId, eventId);

            if (!commitmentInfo || commitmentInfo.tier === 'FREE') {
                return { eligible: false, status: 'NOT_ELIGIBLE' };
            }

            if (commitmentInfo.refundProcessed) {
                return { eligible: false, status: 'ALREADY_REFUNDED' };
            }

            // Process refund transaction
            const refundResult = await this.ensembleSDK.processRefund({
                userAddress: commitmentInfo.walletAddress,
                contractAddress: commitmentInfo.contractAddress,
                amount: commitmentInfo.stakeAmount,
                eventId,
                maxGasPrice: MAX_GAS_PRICE
            });

            return {
                eligible: true,
                transactionHash: refundResult.transactionHash,
                status: 'PENDING',
                amount: commitmentInfo.stakeAmount,
                timestamp: Date.now()
            };

        } catch (error) {
            logger.error('❌ Refund processing failed', { error, userId, eventId });
            return { eligible: true, status: 'FAILED' };
        }
    }

    /**
     * Get commitment status for a user and event
     */
    async getCommitmentStatus(
        call: grpc.ServerUnaryCall<any, any>, // StatusRequest when generated
        callback: grpc.sendUnaryData<any> // StatusResponse when generated
    ): Promise<void> {
        try {
            const request = call.request;
            const commitmentInfo = await this.ensembleSDK.getCommitmentInfo(
                request.userId,
                request.eventId
            );

            callback(null, {
                hasCommitment: !!commitmentInfo,
                tier: commitmentInfo?.tier || 'FREE',
                status: commitmentInfo?.status || 'NONE',
                stakeAmount: commitmentInfo?.stakeAmount || '0',
                transactionHash: commitmentInfo?.transactionHash || '',
                checkedIn: commitmentInfo?.checkedIn || false,
                refundProcessed: commitmentInfo?.refundProcessed || false,
                transactions: commitmentInfo?.transactions || [],
                profile: commitmentInfo?.profile || {}
            });

        } catch (error) {
            logger.error('❌ Status query failed', { error });
            callback(error, null);
        }
    }

    /**
     * Health check endpoint for service monitoring
     */
    async healthCheck(
        call: grpc.ServerUnaryCall<any, any>, // HealthCheckRequest when generated
        callback: grpc.sendUnaryData<any> // HealthCheckResponse when generated
    ): Promise<void> {
        try {
            const health = await this.getServiceHealth();
            callback(null, health);
        } catch (error) {
            logger.error('❌ Health check failed', { error });
            callback(null, {
                status: 'UNHEALTHY', // ServiceHealth.UNHEALTHY when generated
                message: 'Health check failed',
                serviceVersion: '1.0.0',
                ensembleSdkVersion: 'unknown',
                baseSepoliaConnected: false,
                lastSuccessfulOperation: this.performanceMetrics.lastSuccessfulOperation,
                averageResponseTimeMs: this.performanceMetrics.averageResponseTime,
                totalRequestsProcessed: this.performanceMetrics.totalRequests,
                failedRequestsCount: this.performanceMetrics.failedRequests,
                errorRate: this.calculateErrorRate()
            });
        }
    }

    /**
     * Get comprehensive service health information
     */
    private async getServiceHealth(): Promise<any> {
        const networkConnected = await this.ensembleSDK.isNetworkConnected();
        const errorRate = this.calculateErrorRate();

        let status = 'HEALTHY'; // ServiceHealth.HEALTHY when generated
        let message = 'Service is operating normally';

        if (!networkConnected) {
            status = 'UNHEALTHY';
            message = 'Network connectivity issues';
        } else if (errorRate > 0.1) {
            status = 'DEGRADED';
            message = `High error rate: ${(errorRate * 100).toFixed(2)}%`;
        } else if (this.circuitBreaker.getState() === 'OPEN') {
            status = 'DEGRADED';
            message = 'Circuit breaker is open';
        }

        return {
            status,
            message,
            serviceVersion: '1.0.0',
            ensembleSdkVersion: await this.ensembleSDK.getVersion(),
            baseSepoliaConnected: networkConnected,
            lastSuccessfulOperation: this.performanceMetrics.lastSuccessfulOperation,
            averageResponseTimeMs: this.performanceMetrics.averageResponseTime,
            totalRequestsProcessed: this.performanceMetrics.totalRequests,
            failedRequestsCount: this.performanceMetrics.failedRequests,
            errorRate: errorRate
        };
    }

    /**
     * Utility methods for error handling and metrics
     */
    private handleValidationError(callback: grpc.sendUnaryData<any>, error: string): void {
        callback(null, this.createErrorResponse('Validation failed', 'VALIDATION_ERROR', error));
    }

    private handleCircuitBreakerError(callback: grpc.sendUnaryData<any>): void {
        callback(null, this.createErrorResponse(
            'Service temporarily unavailable',
            'CIRCUIT_BREAKER_OPEN',
            'Circuit breaker is open due to previous failures'
        ));
    }

    private createErrorResponse(message: string, errorCode: string, details: string): any {
        return {
            success: false,
            message,
            transactionHash: '',
            status: 'FAILED',
            contractAddress: '',
            stakeAmount: '0',
            estimatedGasFee: 0,
            errorCode,
            timestamp: Date.now(),
            estimatedConfirmationTime: 0
        };
    }

    private updateSuccessMetrics(startTime: number): void {
        const responseTime = Date.now() - startTime;
        this.performanceMetrics.averageResponseTime =
            (this.performanceMetrics.averageResponseTime + responseTime) / 2;
        this.performanceMetrics.lastSuccessfulOperation = Date.now();
    }

    private updateFailureMetrics(): void {
        this.performanceMetrics.failedRequests++;
    }

    private calculateErrorRate(): number {
        if (this.performanceMetrics.totalRequests === 0) return 0;
        return this.performanceMetrics.failedRequests / this.performanceMetrics.totalRequests;
    }
}

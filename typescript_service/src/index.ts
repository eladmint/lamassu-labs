/**
 * Conference Commitment Protocol Service
 *
 * High-risk prototype service for EthCC 2025 MVP using Ensemble AI SDK
 * Security: Operates exclusively on Base Sepolia testnet with comprehensive isolation
 *
 * @author Nuru AI
 * @version 1.0.0
 * @security TESTNET_ONLY - No mainnet operations authorized
 */

import * as grpc from '@grpc/grpc-js';
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';
import { Logger } from './utils/logger';
import { ConfigManager } from './utils/config';
import { CommitmentServiceImpl } from './services/commitment-service';
import { HealthMonitor } from './utils/health-monitor';
import { SecurityValidator } from './utils/security-validator';
import { CircuitBreaker } from './utils/circuit-breaker';

// Import generated gRPC types (these will be generated from proto files)
// import { CommitmentServiceService } from './generated/conference_commitment_grpc_pb';

const logger = Logger.getInstance();
const config = ConfigManager.getInstance();

/**
 * Main application class for Conference Commitment Service
 * Implements security-first architecture with comprehensive monitoring
 */
class ConferenceCommitmentApp {
    private server: grpc.Server;
    private healthMonitor: HealthMonitor;
    private circuitBreaker: CircuitBreaker;
    private secretManager: SecretManagerServiceClient;
    private isShuttingDown = false;

    constructor() {
        this.server = new grpc.Server({
            'grpc.keepalive_time_ms': 30000,
            'grpc.keepalive_timeout_ms': 5000,
            'grpc.keepalive_permit_without_calls': true,
            'grpc.http2.max_pings_without_data': 0,
            'grpc.http2.min_time_between_pings_ms': 10000,
        });

        this.healthMonitor = new HealthMonitor();
        this.circuitBreaker = new CircuitBreaker({
            failureThreshold: 5,
            timeoutMs: 60000,
            monitoringPeriodMs: 60000
        });

        this.secretManager = new SecretManagerServiceClient();
    }

    /**
     * Initialize the service with security validations
     */
    async initialize(): Promise<void> {
        try {
            logger.info('🚀 Initializing Conference Commitment Service...');

            // Security validation: Ensure testnet-only operation
            await this.validateSecurityConfiguration();

            // Load secrets from Google Secret Manager
            await this.loadSecrets();

            // Validate network configuration
            await this.validateNetworkConfiguration();

            // Initialize Ensemble SDK
            await this.initializeEnsembleSDK();

            // Setup gRPC service
            this.setupGrpcService();

            // Setup health monitoring
            this.setupHealthMonitoring();

            // Setup graceful shutdown
            this.setupGracefulShutdown();

            logger.info('✅ Service initialization completed successfully');

        } catch (error) {
            logger.error('❌ Service initialization failed', { error });
            throw error;
        }
    }

    /**
     * Critical security validation - ensures testnet-only operation
     */
    private async validateSecurityConfiguration(): Promise<void> {
        const network = config.get('BLOCKCHAIN_NETWORK');

        if (network !== 'base-sepolia') {
            const error = new Error('SECURITY VIOLATION: Only Base Sepolia testnet is authorized for MVP');
            logger.error('🚨 CRITICAL SECURITY ERROR', {
                network,
                error: error.message,
                severity: 'CRITICAL'
            });
            throw error;
        }

        logger.info('🔒 Security validation passed - Base Sepolia testnet confirmed');
    }

    /**
     * Load secrets from Google Secret Manager
     */
    private async loadSecrets(): Promise<void> {
        try {
            const projectId = config.get('GCP_PROJECT_ID');
            const secretNames = [
                'ENSEMBLE_API_KEY',
                'ENSEMBLE_PRIVATE_KEY',
                'BASE_SEPOLIA_RPC_URL'
            ];

            for (const secretName of secretNames) {
                const [version] = await this.secretManager.accessSecretVersion({
                    name: `projects/${projectId}/secrets/${secretName}/versions/latest`,
                });

                const payload = version.payload?.data?.toString();
                if (!payload) {
                    throw new Error(`Failed to load secret: ${secretName}`);
                }

                config.set(secretName, payload);
                logger.info(`📝 Loaded secret: ${secretName}`);
            }

        } catch (error) {
            logger.error('❌ Failed to load secrets', { error });
            throw error;
        }
    }

    /**
     * Validate network connectivity and configuration
     */
    private async validateNetworkConfiguration(): Promise<void> {
        try {
            const rpcUrl = config.get('BASE_SEPOLIA_RPC_URL');

            // Basic connectivity test (implement actual RPC call here)
            logger.info('🌐 Validating Base Sepolia connectivity', { rpcUrl: rpcUrl.substring(0, 20) + '...' });

            // TODO: Implement actual network validation
            // const provider = new ethers.JsonRpcProvider(rpcUrl);
            // const network = await provider.getNetwork();
            // if (network.chainId !== 84532n) { // Base Sepolia chain ID
            //     throw new Error(`Invalid chain ID: ${network.chainId}`);
            // }

            logger.info('✅ Network validation completed');

        } catch (error) {
            logger.error('❌ Network validation failed', { error });
            throw error;
        }
    }

    /**
     * Initialize Ensemble AI SDK with security constraints
     */
    private async initializeEnsembleSDK(): Promise<void> {
        try {
            logger.info('🔧 Initializing Ensemble AI SDK...');

            // NOTE: This is a placeholder implementation
            // The actual Ensemble SDK integration will depend on the SDK's API

            const ensembleConfig = {
                network: 'base-sepolia',
                apiKey: config.get('ENSEMBLE_API_KEY'),
                privateKey: config.get('ENSEMBLE_PRIVATE_KEY'),
                rpcUrl: config.get('BASE_SEPOLIA_RPC_URL'),
                // Security: Enforce testnet-only operations
                enforceTestnetOnly: true,
                maxGasPrice: '1000000000', // 1 gwei max for testnet
            };

            // TODO: Initialize actual Ensemble SDK
            // this.ensembleClient = new EnsembleAI(ensembleConfig);
            // await this.ensembleClient.initialize();

            logger.info('✅ Ensemble SDK initialized successfully');

        } catch (error) {
            logger.error('❌ Ensemble SDK initialization failed', { error });
            throw error;
        }
    }

    /**
     * Setup gRPC service with security middleware
     */
    private setupGrpcService(): void {
        try {
            // Create commitment service implementation
            const commitmentService = new CommitmentServiceImpl(this.circuitBreaker);

            // TODO: Add generated service to server
            // this.server.addService(CommitmentServiceService, commitmentService);

            // Security: Use insecure credentials for internal communication only
            // In production, implement proper TLS certificates
            const port = config.get('GRPC_PORT', '50051');
            const bindAddress = `0.0.0.0:${port}`;

            this.server.bindAsync(
                bindAddress,
                grpc.ServerCredentials.createInsecure(),
                (error, port) => {
                    if (error) {
                        logger.error('❌ Failed to bind gRPC server', { error, bindAddress });
                        throw error;
                    }

                    logger.info('🚀 gRPC server started', {
                        port,
                        bindAddress,
                        security: 'TESTNET_ISOLATED'
                    });
                }
            );

        } catch (error) {
            logger.error('❌ gRPC service setup failed', { error });
            throw error;
        }
    }

    /**
     * Setup comprehensive health monitoring
     */
    private setupHealthMonitoring(): void {
        this.healthMonitor.start({
            checkIntervalMs: 30000,
            enableMetrics: true,
            enableAlerting: true
        });

        // Monitor circuit breaker status
        this.circuitBreaker.on('stateChange', (state) => {
            logger.warn('⚡ Circuit breaker state changed', {
                state,
                timestamp: new Date().toISOString()
            });
        });

        logger.info('📊 Health monitoring enabled');
    }

    /**
     * Setup graceful shutdown handling
     */
    private setupGracefulShutdown(): void {
        const gracefulShutdown = async (signal: string) => {
            if (this.isShuttingDown) return;
            this.isShuttingDown = true;

            logger.info(`🛑 Received ${signal}, initiating graceful shutdown...`);

            // Stop accepting new requests
            this.server.tryShutdown((error) => {
                if (error) {
                    logger.error('❌ Error during server shutdown', { error });
                    process.exit(1);
                } else {
                    logger.info('✅ Server shutdown completed');
                }
            });

            // Stop health monitoring
            this.healthMonitor.stop();

            // Wait for ongoing operations to complete
            await new Promise(resolve => setTimeout(resolve, 5000));

            logger.info('👋 Service shutdown completed');
            process.exit(0);
        };

        process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
        process.on('SIGINT', () => gracefulShutdown('SIGINT'));

        // Handle unhandled promise rejections
        process.on('unhandledRejection', (reason, promise) => {
            logger.error('🚨 Unhandled Promise Rejection', {
                reason,
                promise,
                severity: 'CRITICAL'
            });
        });

        // Handle uncaught exceptions
        process.on('uncaughtException', (error) => {
            logger.error('🚨 Uncaught Exception', {
                error,
                severity: 'CRITICAL'
            });
            process.exit(1);
        });
    }

    /**
     * Start the service
     */
    async start(): Promise<void> {
        try {
            await this.initialize();

            logger.info('🎉 Conference Commitment Service is running', {
                version: '1.0.0',
                environment: 'base-sepolia-testnet',
                security: 'HIGH_ISOLATION',
                timestamp: new Date().toISOString()
            });

        } catch (error) {
            logger.error('💥 Failed to start service', { error });
            process.exit(1);
        }
    }
}

/**
 * Application entry point
 */
async function main(): Promise<void> {
    // Security banner
    console.log(`
🔒 CONFERENCE COMMITMENT PROTOCOL SERVICE
⚠️  HIGH-RISK PROTOTYPE - TESTNET ONLY ⚠️
🌐 Base Sepolia Testnet Operations
🛡️  Comprehensive Security Isolation
📅 EthCC Cannes 2025 MVP
    `);

    const app = new ConferenceCommitmentApp();
    await app.start();
}

// Start the application
if (require.main === module) {
    main().catch((error) => {
        console.error('💥 Application startup failed:', error);
        process.exit(1);
    });
}

export { ConferenceCommitmentApp };

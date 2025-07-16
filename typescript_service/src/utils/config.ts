/**
 * Configuration Manager
 *
 * Centralized configuration management with security validation
 * Security: Validates critical security settings and enforces testnet-only operation
 *
 * @author Nuru AI
 * @version 1.0.0
 */

import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

/**
 * Configuration interface for type safety
 */
interface ConfigSchema {
    // Service configuration
    NODE_ENV: string;
    LOG_LEVEL: string;
    GRPC_PORT: string;

    // Blockchain configuration
    BLOCKCHAIN_NETWORK: string;
    BASE_SEPOLIA_RPC_URL: string;

    // Ensemble AI configuration
    ENSEMBLE_API_KEY: string;
    ENSEMBLE_PRIVATE_KEY: string;

    // Google Cloud configuration
    GCP_PROJECT_ID: string;

    // Security configuration
    MAX_GAS_PRICE: string;
    CIRCUIT_BREAKER_THRESHOLD: string;
    CIRCUIT_BREAKER_TIMEOUT: string;
}

/**
 * Singleton configuration manager with validation and security enforcement
 */
export class ConfigManager {
    private static instance: ConfigManager;
    private config: Map<string, string> = new Map();
    private requiredKeys: string[] = [
        'BLOCKCHAIN_NETWORK',
        'GCP_PROJECT_ID'
    ];

    private constructor() {
        this.loadConfiguration();
        this.validateConfiguration();
    }

    static getInstance(): ConfigManager {
        if (!ConfigManager.instance) {
            ConfigManager.instance = new ConfigManager();
        }
        return ConfigManager.instance;
    }

    /**
     * Load configuration from environment variables
     */
    private loadConfiguration(): void {
        // Service configuration
        this.config.set('NODE_ENV', process.env.NODE_ENV || 'development');
        this.config.set('LOG_LEVEL', process.env.LOG_LEVEL || 'info');
        this.config.set('GRPC_PORT', process.env.GRPC_PORT || '50051');

        // Blockchain configuration
        this.config.set('BLOCKCHAIN_NETWORK', process.env.BLOCKCHAIN_NETWORK || 'base-sepolia');
        this.config.set('BASE_SEPOLIA_RPC_URL', process.env.BASE_SEPOLIA_RPC_URL || '');

        // Ensemble AI configuration
        this.config.set('ENSEMBLE_API_KEY', process.env.ENSEMBLE_API_KEY || '');
        this.config.set('ENSEMBLE_PRIVATE_KEY', process.env.ENSEMBLE_PRIVATE_KEY || '');

        // Google Cloud configuration
        this.config.set('GCP_PROJECT_ID', process.env.GCP_PROJECT_ID || '');

        // Security configuration
        this.config.set('MAX_GAS_PRICE', process.env.MAX_GAS_PRICE || '1000000000'); // 1 gwei
        this.config.set('CIRCUIT_BREAKER_THRESHOLD', process.env.CIRCUIT_BREAKER_THRESHOLD || '5');
        this.config.set('CIRCUIT_BREAKER_TIMEOUT', process.env.CIRCUIT_BREAKER_TIMEOUT || '60000');
    }

    /**
     * Validate critical configuration settings
     */
    private validateConfiguration(): void {
        // Check required keys
        for (const key of this.requiredKeys) {
            if (!this.config.get(key)) {
                throw new Error(`Missing required configuration: ${key}`);
            }
        }

        // Security validation: Ensure testnet-only operation
        const network = this.config.get('BLOCKCHAIN_NETWORK');
        if (network !== 'base-sepolia') {
            throw new Error(`SECURITY VIOLATION: Invalid network '${network}'. Only 'base-sepolia' is authorized.`);
        }

        // Validate numeric configurations
        this.validateNumericConfig('GRPC_PORT', 1024, 65535);
        this.validateNumericConfig('MAX_GAS_PRICE', 1, 10000000000); // Max 10 gwei
        this.validateNumericConfig('CIRCUIT_BREAKER_THRESHOLD', 1, 100);
        this.validateNumericConfig('CIRCUIT_BREAKER_TIMEOUT', 1000, 300000); // 1s to 5min

        // Validate environment
        const nodeEnv = this.config.get('NODE_ENV');
        if (!['development', 'test', 'production'].includes(nodeEnv!)) {
            throw new Error(`Invalid NODE_ENV: ${nodeEnv}`);
        }

        console.log('✅ Configuration validation passed');
        console.log(`🌐 Network: ${network}`);
        console.log(`🔧 Environment: ${nodeEnv}`);
        console.log(`📡 gRPC Port: ${this.config.get('GRPC_PORT')}`);
    }

    /**
     * Validate numeric configuration values
     */
    private validateNumericConfig(key: string, min: number, max: number): void {
        const value = this.config.get(key);
        if (!value) return;

        const numValue = parseInt(value, 10);
        if (isNaN(numValue) || numValue < min || numValue > max) {
            throw new Error(`Invalid ${key}: ${value}. Must be between ${min} and ${max}.`);
        }
    }

    /**
     * Get configuration value
     */
    get(key: string, defaultValue?: string): string {
        const value = this.config.get(key);
        if (value === undefined || value === '') {
            if (defaultValue !== undefined) {
                return defaultValue;
            }
            throw new Error(`Configuration key not found: ${key}`);
        }
        return value;
    }

    /**
     * Get configuration value as number
     */
    getNumber(key: string, defaultValue?: number): number {
        const value = this.get(key, defaultValue?.toString());
        const numValue = parseInt(value, 10);
        if (isNaN(numValue)) {
            throw new Error(`Configuration key '${key}' is not a valid number: ${value}`);
        }
        return numValue;
    }

    /**
     * Get configuration value as boolean
     */
    getBoolean(key: string, defaultValue?: boolean): boolean {
        const value = this.get(key, defaultValue?.toString());
        return value.toLowerCase() === 'true';
    }

    /**
     * Set configuration value (for runtime updates from secrets)
     */
    set(key: string, value: string): void {
        this.config.set(key, value);
    }

    /**
     * Check if running in development mode
     */
    isDevelopment(): boolean {
        return this.get('NODE_ENV') === 'development';
    }

    /**
     * Check if running in production mode
     */
    isProduction(): boolean {
        return this.get('NODE_ENV') === 'production';
    }

    /**
     * Check if running in test mode
     */
    isTest(): boolean {
        return this.get('NODE_ENV') === 'test';
    }

    /**
     * Get all configuration (with sensitive data redacted)
     */
    getAll(): Record<string, string> {
        const config: Record<string, string> = {};
        const sensitiveKeys = ['ENSEMBLE_API_KEY', 'ENSEMBLE_PRIVATE_KEY', 'BASE_SEPOLIA_RPC_URL'];

        for (const [key, value] of this.config.entries()) {
            if (sensitiveKeys.includes(key)) {
                config[key] = '[REDACTED]';
            } else {
                config[key] = value;
            }
        }

        return config;
    }

    /**
     * Validate security-critical settings
     */
    validateSecurity(): { isValid: boolean; errors: string[] } {
        const errors: string[] = [];

        // Network validation
        if (this.get('BLOCKCHAIN_NETWORK') !== 'base-sepolia') {
            errors.push('Network must be base-sepolia for MVP');
        }

        // Gas price validation
        const maxGasPrice = this.getNumber('MAX_GAS_PRICE');
        if (maxGasPrice > 10000000000) { // 10 gwei
            errors.push('Max gas price too high for testnet');
        }

        // Required secrets validation
        const requiredSecrets = ['ENSEMBLE_API_KEY', 'BASE_SEPOLIA_RPC_URL'];
        for (const secret of requiredSecrets) {
            if (!this.config.get(secret)) {
                errors.push(`Missing required secret: ${secret}`);
            }
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }
}

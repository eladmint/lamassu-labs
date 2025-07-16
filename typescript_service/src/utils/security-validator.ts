/**
 * Security Validator
 *
 * Comprehensive security validation for Conference Commitment Protocol
 * Security: Validates all inputs and enforces security policies
 *
 * @author Nuru AI
 * @version 1.0.0
 */

import { Logger } from './logger';

const logger = Logger.getInstance();

/**
 * Validation result interface
 */
export interface ValidationResult {
    isValid: boolean;
    error?: string;
    severity?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
}

/**
 * Comprehensive security validator for all service inputs
 */
export class SecurityValidator {
    private readonly maxStringLength = 1000;
    private readonly maxAmountEth = 1.0; // Maximum 1 ETH for testnet
    private readonly validCommitmentTiers = ['FREE', 'COMMITTED', 'VIP'];
    private readonly validCheckinMethods = ['manual', 'qr_code', 'location', 'admin'];

    /**
     * Validate commitment request
     */
    async validateCommitmentRequest(request: any): Promise<ValidationResult> {
        try {
            // Validate required fields
            if (!request.userId || !request.eventId || request.tier === undefined) {
                return this.createError('Missing required fields', 'HIGH');
            }

            // Validate user ID
            const userIdValidation = this.validateUserId(request.userId);
            if (!userIdValidation.isValid) {
                return userIdValidation;
            }

            // Validate event ID
            const eventIdValidation = this.validateEventId(request.eventId);
            if (!eventIdValidation.isValid) {
                return eventIdValidation;
            }

            // Validate commitment tier
            const tierValidation = this.validateCommitmentTier(request.tier);
            if (!tierValidation.isValid) {
                return tierValidation;
            }

            // Validate wallet address if provided (required for staking tiers)
            if ((request.tier === 'COMMITTED' || request.tier === 'VIP') && request.userWalletAddress) {
                const walletValidation = this.validateWalletAddress(request.userWalletAddress);
                if (!walletValidation.isValid) {
                    return walletValidation;
                }
            }

            // Validate email if provided
            if (request.userEmail) {
                const emailValidation = this.validateEmail(request.userEmail);
                if (!emailValidation.isValid) {
                    return emailValidation;
                }
            }

            // Validate metadata if provided
            if (request.metadata) {
                const metadataValidation = this.validateMetadata(request.metadata);
                if (!metadataValidation.isValid) {
                    return metadataValidation;
                }
            }

            logger.info('✅ Commitment request validation passed', {
                userId: request.userId,
                eventId: request.eventId,
                tier: request.tier
            });

            return { isValid: true };

        } catch (error) {
            logger.error('❌ Commitment request validation failed', { error });
            return this.createError('Validation error occurred', 'CRITICAL');
        }
    }

    /**
     * Validate check-in request
     */
    async validateCheckinRequest(request: any): Promise<ValidationResult> {
        try {
            // Validate required fields
            if (!request.userId || !request.eventId) {
                return this.createError('Missing required fields for check-in', 'HIGH');
            }

            // Validate user ID
            const userIdValidation = this.validateUserId(request.userId);
            if (!userIdValidation.isValid) {
                return userIdValidation;
            }

            // Validate event ID
            const eventIdValidation = this.validateEventId(request.eventId);
            if (!eventIdValidation.isValid) {
                return eventIdValidation;
            }

            // Validate check-in method
            if (request.checkinMethod) {
                const methodValidation = this.validateCheckinMethod(request.checkinMethod);
                if (!methodValidation.isValid) {
                    return methodValidation;
                }
            }

            // Validate location data if provided
            if (request.latitude !== undefined || request.longitude !== undefined) {
                const locationValidation = this.validateLocation(request.latitude, request.longitude);
                if (!locationValidation.isValid) {
                    return locationValidation;
                }
            }

            // Validate verification data
            if (request.verificationData) {
                const verificationValidation = this.validateVerificationData(request.verificationData);
                if (!verificationValidation.isValid) {
                    return verificationValidation;
                }
            }

            logger.info('✅ Check-in request validation passed', {
                userId: request.userId,
                eventId: request.eventId,
                checkinMethod: request.checkinMethod
            });

            return { isValid: true };

        } catch (error) {
            logger.error('❌ Check-in request validation failed', { error });
            return this.createError('Check-in validation error occurred', 'CRITICAL');
        }
    }

    /**
     * Validate user ID format and security
     */
    private validateUserId(userId: string): ValidationResult {
        if (typeof userId !== 'string') {
            return this.createError('User ID must be a string', 'HIGH');
        }

        if (userId.length === 0 || userId.length > 100) {
            return this.createError('User ID length invalid', 'MEDIUM');
        }

        // Check for SQL injection patterns
        if (this.containsSqlInjection(userId)) {
            return this.createError('User ID contains prohibited characters', 'CRITICAL');
        }

        // Check for XSS patterns
        if (this.containsXssPatterns(userId)) {
            return this.createError('User ID contains script injection patterns', 'CRITICAL');
        }

        return { isValid: true };
    }

    /**
     * Validate event ID format
     */
    private validateEventId(eventId: string): ValidationResult {
        if (typeof eventId !== 'string') {
            return this.createError('Event ID must be a string', 'HIGH');
        }

        if (eventId.length === 0 || eventId.length > 100) {
            return this.createError('Event ID length invalid', 'MEDIUM');
        }

        // UUID format validation (optional but recommended)
        const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
        if (!uuidRegex.test(eventId)) {
            logger.warn('⚠️ Event ID is not in UUID format', { eventId });
        }

        return { isValid: true };
    }

    /**
     * Validate commitment tier
     */
    private validateCommitmentTier(tier: string): ValidationResult {
        if (!this.validCommitmentTiers.includes(tier)) {
            return this.createError(`Invalid commitment tier: ${tier}`, 'HIGH');
        }

        return { isValid: true };
    }

    /**
     * Validate Ethereum wallet address
     */
    validateWalletAddress(address: string): ValidationResult {
        if (typeof address !== 'string') {
            return this.createError('Wallet address must be a string', 'HIGH');
        }

        // Basic Ethereum address format
        const ethAddressRegex = /^0x[a-fA-F0-9]{40}$/;
        if (!ethAddressRegex.test(address)) {
            return this.createError('Invalid Ethereum address format', 'HIGH');
        }

        // Check for null address (security risk)
        if (address === '0x0000000000000000000000000000000000000000') {
            return this.createError('Null address not allowed', 'HIGH');
        }

        return { isValid: true };
    }

    /**
     * Validate Ethereum address format (public method for reuse)
     */
    isValidEthereumAddress(address: string): boolean {
        const validation = this.validateWalletAddress(address);
        return validation.isValid;
    }

    /**
     * Validate email format
     */
    private validateEmail(email: string): ValidationResult {
        if (typeof email !== 'string') {
            return this.createError('Email must be a string', 'MEDIUM');
        }

        if (email.length > 254) {
            return this.createError('Email too long', 'MEDIUM');
        }

        // Basic email regex
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return this.createError('Invalid email format', 'MEDIUM');
        }

        return { isValid: true };
    }

    /**
     * Validate check-in method
     */
    private validateCheckinMethod(method: string): ValidationResult {
        if (!this.validCheckinMethods.includes(method)) {
            return this.createError(`Invalid check-in method: ${method}`, 'MEDIUM');
        }

        return { isValid: true };
    }

    /**
     * Validate location coordinates
     */
    private validateLocation(latitude: any, longitude: any): ValidationResult {
        if (latitude !== undefined) {
            if (typeof latitude !== 'number' || latitude < -90 || latitude > 90) {
                return this.createError('Invalid latitude', 'MEDIUM');
            }
        }

        if (longitude !== undefined) {
            if (typeof longitude !== 'number' || longitude < -180 || longitude > 180) {
                return this.createError('Invalid longitude', 'MEDIUM');
            }
        }

        return { isValid: true };
    }

    /**
     * Validate verification data
     */
    private validateVerificationData(data: string): ValidationResult {
        if (typeof data !== 'string') {
            return this.createError('Verification data must be a string', 'MEDIUM');
        }

        if (data.length > 10000) {
            return this.createError('Verification data too large', 'MEDIUM');
        }

        // Check for script injection
        if (this.containsXssPatterns(data)) {
            return this.createError('Verification data contains prohibited scripts', 'HIGH');
        }

        return { isValid: true };
    }

    /**
     * Validate metadata object
     */
    private validateMetadata(metadata: any): ValidationResult {
        if (typeof metadata !== 'object' || metadata === null) {
            return this.createError('Metadata must be an object', 'MEDIUM');
        }

        // Check metadata size
        const metadataString = JSON.stringify(metadata);
        if (metadataString.length > 5000) {
            return this.createError('Metadata too large', 'MEDIUM');
        }

        // Validate each key and value
        for (const [key, value] of Object.entries(metadata)) {
            if (typeof key !== 'string' || key.length > 100) {
                return this.createError('Invalid metadata key', 'MEDIUM');
            }

            if (typeof value === 'string' && value.length > this.maxStringLength) {
                return this.createError('Metadata value too long', 'MEDIUM');
            }

            // Check for injection patterns in metadata
            if (typeof value === 'string' && this.containsXssPatterns(value)) {
                return this.createError('Metadata contains prohibited patterns', 'HIGH');
            }
        }

        return { isValid: true };
    }

    /**
     * Check for SQL injection patterns
     */
    private containsSqlInjection(input: string): boolean {
        const sqlPatterns = [
            /(\s|^)(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)\s/i,
            /('|('')|;|--|\/\*|\*\/)/,
            /(OR|AND)\s+\d+\s*=\s*\d+/i,
            /xp_cmdshell|sp_executesql/i
        ];

        return sqlPatterns.some(pattern => pattern.test(input));
    }

    /**
     * Check for XSS patterns
     */
    private containsXssPatterns(input: string): boolean {
        const xssPatterns = [
            /<script[^>]*>.*?<\/script>/gi,
            /<iframe[^>]*>.*?<\/iframe>/gi,
            /javascript:/gi,
            /on\w+\s*=/gi,
            /<img[^>]+src[^>]*>/gi,
            /data:text\/html/gi,
            /vbscript:/gi
        ];

        return xssPatterns.some(pattern => pattern.test(input));
    }

    /**
     * Create validation error result
     */
    private createError(message: string, severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'): ValidationResult {
        logger.security('Security validation failed', {
            message,
            severity,
            timestamp: Date.now()
        });

        return {
            isValid: false,
            error: message,
            severity
        };
    }

    /**
     * Validate transaction amount (for staking)
     */
    validateStakeAmount(amount: string, tier: string): ValidationResult {
        try {
            const amountNum = parseFloat(amount);

            if (isNaN(amountNum) || amountNum < 0) {
                return this.createError('Invalid stake amount', 'HIGH');
            }

            if (amountNum > this.maxAmountEth) {
                return this.createError(`Stake amount exceeds maximum (${this.maxAmountEth} ETH)`, 'HIGH');
            }

            // Validate amount matches tier
            const expectedAmounts = {
                'FREE': 0,
                'COMMITTED': 0.05,
                'VIP': 0.5
            };

            const expectedAmount = expectedAmounts[tier as keyof typeof expectedAmounts];
            if (expectedAmount !== undefined && Math.abs(amountNum - expectedAmount) > 0.001) {
                return this.createError(`Amount doesn't match tier: expected ${expectedAmount}, got ${amountNum}`, 'HIGH');
            }

            return { isValid: true };

        } catch (error) {
            return this.createError('Amount validation error', 'HIGH');
        }
    }

    /**
     * Validate gas price (security constraint for testnet)
     */
    validateGasPrice(gasPriceWei: string): ValidationResult {
        try {
            const gasPrice = BigInt(gasPriceWei);
            const maxGasPrice = BigInt('10000000000'); // 10 gwei

            if (gasPrice > maxGasPrice) {
                return this.createError(`Gas price too high: ${gasPriceWei} wei`, 'HIGH');
            }

            if (gasPrice <= BigInt('0')) {
                return this.createError('Gas price must be positive', 'MEDIUM');
            }

            return { isValid: true };

        } catch (error) {
            return this.createError('Gas price validation error', 'HIGH');
        }
    }
}

/**
 * Structured Logger Utility
 *
 * Provides comprehensive logging with security context and performance monitoring
 * Security: Ensures sensitive data is never logged
 *
 * @author Nuru AI
 * @version 1.0.0
 */

import * as winston from 'winston';

export interface LogContext {
    [key: string]: any;
    userId?: string;
    eventId?: string;
    transactionHash?: string;
    operation?: string;
    duration?: number;
    severity?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
}

/**
 * Singleton logger class with structured logging and security filtering
 */
export class Logger {
    private static instance: Logger;
    private winston: winston.Logger;
    private sensitiveFields = [
        'privateKey',
        'apiKey',
        'password',
        'secret',
        'token',
        'wallet',
        'mnemonic',
        'seed'
    ];

    private constructor() {
        this.winston = winston.createLogger({
            level: process.env.LOG_LEVEL || 'info',
            format: winston.format.combine(
                winston.format.timestamp(),
                winston.format.errors({ stack: true }),
                winston.format.json(),
                winston.format.printf(this.customFormat)
            ),
            transports: [
                new winston.transports.Console({
                    format: winston.format.combine(
                        winston.format.colorize(),
                        winston.format.simple()
                    )
                }),
                new winston.transports.File({
                    filename: 'logs/error.log',
                    level: 'error',
                    maxsize: 10485760, // 10MB
                    maxFiles: 5
                }),
                new winston.transports.File({
                    filename: 'logs/combined.log',
                    maxsize: 10485760, // 10MB
                    maxFiles: 10
                })
            ]
        });
    }

    static getInstance(): Logger {
        if (!Logger.instance) {
            Logger.instance = new Logger();
        }
        return Logger.instance;
    }

    /**
     * Custom log format with security filtering
     */
    private customFormat = (info: any) => {
        const { timestamp, level, message, ...meta } = info;

        // Filter sensitive data
        const filteredMeta = this.filterSensitiveData(meta);

        return JSON.stringify({
            timestamp,
            level,
            message,
            service: 'conference-commitment-service',
            environment: 'base-sepolia-testnet',
            ...filteredMeta
        });
    };

    /**
     * Filter sensitive data from log context
     */
    private filterSensitiveData(data: any): any {
        if (typeof data !== 'object' || data === null) {
            return data;
        }

        const filtered: any = {};

        for (const [key, value] of Object.entries(data)) {
            const lowerKey = key.toLowerCase();

            // Check if key contains sensitive information
            const isSensitive = this.sensitiveFields.some(field =>
                lowerKey.includes(field)
            );

            if (isSensitive) {
                filtered[key] = '[REDACTED]';
            } else if (typeof value === 'object' && value !== null) {
                filtered[key] = this.filterSensitiveData(value);
            } else if (typeof value === 'string' && value.length > 50) {
                // Truncate long strings (might be sensitive)
                filtered[key] = value.substring(0, 50) + '...';
            } else {
                filtered[key] = value;
            }
        }

        return filtered;
    }

    /**
     * Log info level messages
     */
    info(message: string, context?: LogContext): void {
        this.winston.info(message, context);
    }

    /**
     * Log warning level messages
     */
    warn(message: string, context?: LogContext): void {
        this.winston.warn(message, context);
    }

    /**
     * Log error level messages
     */
    error(message: string, context?: LogContext): void {
        this.winston.error(message, context);
    }

    /**
     * Log debug level messages
     */
    debug(message: string, context?: LogContext): void {
        this.winston.debug(message, context);
    }

    /**
     * Log security-related events
     */
    security(message: string, context: LogContext & { severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' }): void {
        this.winston.warn(`🔒 SECURITY: ${message}`, {
            ...context,
            securityEvent: true,
            alertRequired: context.severity === 'HIGH' || context.severity === 'CRITICAL'
        });
    }

    /**
     * Log performance metrics
     */
    performance(operation: string, duration: number, context?: LogContext): void {
        this.winston.info(`⚡ PERFORMANCE: ${operation}`, {
            ...context,
            operation,
            duration,
            performanceMetric: true
        });
    }

    /**
     * Log transaction-related events
     */
    transaction(message: string, context: LogContext & { transactionHash?: string }): void {
        this.winston.info(`💰 TRANSACTION: ${message}`, {
            ...context,
            transactionEvent: true
        });
    }

    /**
     * Log circuit breaker events
     */
    circuitBreaker(state: string, context?: LogContext): void {
        this.winston.warn(`⚡ CIRCUIT BREAKER: State changed to ${state}`, {
            ...context,
            circuitBreakerEvent: true,
            state
        });
    }

    /**
     * Create child logger with persistent context
     */
    child(persistentContext: LogContext): ChildLogger {
        return new ChildLogger(this, persistentContext);
    }
}

/**
 * Child logger that includes persistent context
 */
class ChildLogger {
    constructor(
        private parent: Logger,
        private persistentContext: LogContext
    ) {}

    private mergeContext(context?: LogContext): LogContext {
        return { ...this.persistentContext, ...context };
    }

    info(message: string, context?: LogContext): void {
        this.parent.info(message, this.mergeContext(context));
    }

    warn(message: string, context?: LogContext): void {
        this.parent.warn(message, this.mergeContext(context));
    }

    error(message: string, context?: LogContext): void {
        this.parent.error(message, this.mergeContext(context));
    }

    debug(message: string, context?: LogContext): void {
        this.parent.debug(message, this.mergeContext(context));
    }

    security(message: string, context: LogContext & { severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' }): void {
        this.parent.security(message, this.mergeContext(context) as any);
    }

    performance(operation: string, duration: number, context?: LogContext): void {
        this.parent.performance(operation, duration, this.mergeContext(context));
    }

    transaction(message: string, context: LogContext & { transactionHash?: string }): void {
        this.parent.transaction(message, this.mergeContext(context) as any);
    }
}

/**
 * Circuit Breaker Implementation
 *
 * Provides automatic failure protection for the Ensemble SDK integration
 * Security: Prevents cascading failures and protects against unstable SDK behavior
 *
 * @author Nuru AI
 * @version 1.0.0
 */

import { EventEmitter } from 'events';
import { Logger } from './logger';

const logger = Logger.getInstance();

/**
 * Circuit breaker states
 */
export type CircuitBreakerState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

/**
 * Circuit breaker configuration
 */
export interface CircuitBreakerConfig {
    failureThreshold: number;      // Number of failures before opening
    timeoutMs: number;             // Timeout before trying half-open
    monitoringPeriodMs: number;    // Period to monitor for failures
    maxRetries?: number;           // Maximum retries in half-open state
}

/**
 * Circuit breaker statistics
 */
export interface CircuitBreakerStats {
    state: CircuitBreakerState;
    failures: number;
    successes: number;
    lastFailureTime: number;
    lastSuccessTime: number;
    totalRequests: number;
    uptime: number;
}

/**
 * Circuit Breaker implementation with comprehensive monitoring
 * Protects against cascading failures from unstable Ensemble SDK
 */
export class CircuitBreaker extends EventEmitter {
    private state: CircuitBreakerState = 'CLOSED';
    private failures = 0;
    private successes = 0;
    private lastFailureTime = 0;
    private lastSuccessTime = Date.now();
    private totalRequests = 0;
    private halfOpenRetries = 0;
    private readonly config: Required<CircuitBreakerConfig>;
    private monitoringTimer?: NodeJS.Timeout;

    constructor(config: CircuitBreakerConfig) {
        super();

        this.config = {
            failureThreshold: config.failureThreshold,
            timeoutMs: config.timeoutMs,
            monitoringPeriodMs: config.monitoringPeriodMs,
            maxRetries: config.maxRetries || 3
        };

        this.startMonitoring();

        logger.info('⚡ Circuit breaker initialized', {
            failureThreshold: this.config.failureThreshold,
            timeoutMs: this.config.timeoutMs,
            monitoringPeriodMs: this.config.monitoringPeriodMs
        });
    }

    /**
     * Record a successful operation
     */
    recordSuccess(): void {
        this.totalRequests++;
        this.successes++;
        this.lastSuccessTime = Date.now();

        if (this.state === 'HALF_OPEN') {
            logger.info('⚡ Circuit breaker: Success in half-open state', {
                successes: this.successes,
                failures: this.failures
            });

            // Reset to closed state after successful operation
            this.setState('CLOSED');
            this.failures = 0;
            this.halfOpenRetries = 0;
        }
    }

    /**
     * Record a failed operation
     */
    recordFailure(): void {
        this.totalRequests++;
        this.failures++;
        this.lastFailureTime = Date.now();

        logger.warn('⚡ Circuit breaker: Failure recorded', {
            failures: this.failures,
            threshold: this.config.failureThreshold,
            state: this.state
        });

        if (this.state === 'CLOSED' && this.failures >= this.config.failureThreshold) {
            this.setState('OPEN');
            this.scheduleHalfOpen();
        } else if (this.state === 'HALF_OPEN') {
            this.halfOpenRetries++;
            if (this.halfOpenRetries >= this.config.maxRetries) {
                this.setState('OPEN');
                this.scheduleHalfOpen();
            }
        }
    }

    /**
     * Check if a request can proceed
     */
    canProceed(): boolean {
        switch (this.state) {
            case 'CLOSED':
                return true;
            case 'OPEN':
                return false;
            case 'HALF_OPEN':
                return this.halfOpenRetries < this.config.maxRetries;
            default:
                return false;
        }
    }

    /**
     * Get current circuit breaker state
     */
    getState(): CircuitBreakerState {
        return this.state;
    }

    /**
     * Get comprehensive statistics
     */
    getStats(): CircuitBreakerStats {
        return {
            state: this.state,
            failures: this.failures,
            successes: this.successes,
            lastFailureTime: this.lastFailureTime,
            lastSuccessTime: this.lastSuccessTime,
            totalRequests: this.totalRequests,
            uptime: this.calculateUptime()
        };
    }

    /**
     * Force reset the circuit breaker (admin operation)
     */
    reset(): void {
        logger.info('⚡ Circuit breaker: Manual reset initiated');

        this.setState('CLOSED');
        this.failures = 0;
        this.successes = 0;
        this.halfOpenRetries = 0;
        this.lastSuccessTime = Date.now();

        logger.info('✅ Circuit breaker reset completed');
    }

    /**
     * Set circuit breaker state and emit events
     */
    private setState(newState: CircuitBreakerState): void {
        const previousState = this.state;
        this.state = newState;

        if (previousState !== newState) {
            logger.warn(`⚡ Circuit breaker state changed: ${previousState} → ${newState}`, {
                failures: this.failures,
                successes: this.successes,
                threshold: this.config.failureThreshold,
                timestamp: new Date().toISOString()
            });

            this.emit('stateChange', {
                previousState,
                newState,
                timestamp: Date.now(),
                stats: this.getStats()
            });

            // Emit specific state events
            this.emit(newState.toLowerCase(), this.getStats());
        }
    }

    /**
     * Schedule transition to half-open state
     */
    private scheduleHalfOpen(): void {
        logger.info('⏰ Circuit breaker: Scheduling half-open transition', {
            timeoutMs: this.config.timeoutMs,
            nextAttempt: new Date(Date.now() + this.config.timeoutMs).toISOString()
        });

        setTimeout(() => {
            if (this.state === 'OPEN') {
                logger.info('⚡ Circuit breaker: Transitioning to half-open state');
                this.setState('HALF_OPEN');
                this.halfOpenRetries = 0;
            }
        }, this.config.timeoutMs);
    }

    /**
     * Start monitoring and cleanup
     */
    private startMonitoring(): void {
        this.monitoringTimer = setInterval(() => {
            this.performHealthCheck();
        }, this.config.monitoringPeriodMs);
    }

    /**
     * Perform periodic health check
     */
    private performHealthCheck(): void {
        const stats = this.getStats();
        const errorRate = this.totalRequests > 0 ? this.failures / this.totalRequests : 0;

        logger.debug('⚡ Circuit breaker health check', {
            state: stats.state,
            errorRate: errorRate.toFixed(3),
            totalRequests: stats.totalRequests,
            uptime: stats.uptime
        });

        // Emit health check event
        this.emit('healthCheck', {
            ...stats,
            errorRate
        });

        // Auto-recovery logic for prolonged open state
        if (this.state === 'OPEN') {
            const timeSinceLastFailure = Date.now() - this.lastFailureTime;
            const autoRecoveryTime = this.config.timeoutMs * 3; // 3x timeout period

            if (timeSinceLastFailure > autoRecoveryTime) {
                logger.info('⚡ Circuit breaker: Auto-recovery triggered', {
                    timeSinceLastFailure,
                    autoRecoveryTime
                });
                this.setState('HALF_OPEN');
                this.halfOpenRetries = 0;
            }
        }
    }

    /**
     * Calculate uptime percentage
     */
    private calculateUptime(): number {
        if (this.totalRequests === 0) return 100;

        const successRate = this.successes / this.totalRequests;
        return Math.round(successRate * 100 * 100) / 100; // Round to 2 decimal places
    }

    /**
     * Get failure rate
     */
    getFailureRate(): number {
        if (this.totalRequests === 0) return 0;
        return this.failures / this.totalRequests;
    }

    /**
     * Check if circuit breaker is healthy
     */
    isHealthy(): boolean {
        return this.state === 'CLOSED' && this.getFailureRate() < 0.1; // Less than 10% failure rate
    }

    /**
     * Get time until next retry (for open state)
     */
    getTimeUntilRetry(): number {
        if (this.state !== 'OPEN') return 0;

        const timeSinceFailure = Date.now() - this.lastFailureTime;
        const remainingTime = this.config.timeoutMs - timeSinceFailure;

        return Math.max(0, remainingTime);
    }

    /**
     * Cleanup resources
     */
    destroy(): void {
        if (this.monitoringTimer) {
            clearInterval(this.monitoringTimer);
            this.monitoringTimer = undefined;
        }

        this.removeAllListeners();

        logger.info('⚡ Circuit breaker destroyed');
    }
}

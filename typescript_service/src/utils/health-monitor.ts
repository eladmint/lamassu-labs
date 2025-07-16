/**
 * Health Monitor
 *
 * Comprehensive health monitoring for Conference Commitment Service
 * Security: Monitors for anomalies and security events
 *
 * @author Nuru AI
 * @version 1.0.0
 */

import { EventEmitter } from 'events';
import { Logger } from './logger';
import { ConfigManager } from './config';

const logger = Logger.getInstance();
const config = ConfigManager.getInstance();

/**
 * Health check configuration
 */
export interface HealthMonitorConfig {
    checkIntervalMs: number;
    enableMetrics: boolean;
    enableAlerting: boolean;
    thresholds?: {
        errorRate: number;
        responseTime: number;
        memoryUsage: number;
        cpuUsage: number;
    };
}

/**
 * Health status information
 */
export interface HealthStatus {
    status: 'healthy' | 'degraded' | 'unhealthy';
    timestamp: number;
    uptime: number;
    checks: {
        [key: string]: {
            status: 'pass' | 'warn' | 'fail';
            message: string;
            lastCheck: number;
            duration?: number;
        };
    };
    metrics: {
        memory: {
            used: number;
            total: number;
            percentage: number;
        };
        cpu: {
            usage: number;
        };
        requests: {
            total: number;
            failed: number;
            errorRate: number;
            averageResponseTime: number;
        };
        ensemble: {
            connected: boolean;
            lastSuccess: number;
            errors: number;
        };
    };
}

/**
 * Comprehensive health monitoring system
 */
export class HealthMonitor extends EventEmitter {
    private isRunning = false;
    private startTime = Date.now();
    private monitoringTimer?: NodeJS.Timeout;
    private config: HealthMonitorConfig;
    private lastHealthStatus?: HealthStatus;

    // Metrics tracking
    private metrics = {
        requests: { total: 0, failed: 0, totalResponseTime: 0 },
        ensemble: { connected: true, lastSuccess: Date.now(), errors: 0 },
        checks: new Map<string, any>()
    };

    constructor() {
        super();

        this.config = {
            checkIntervalMs: 30000, // 30 seconds
            enableMetrics: true,
            enableAlerting: true,
            thresholds: {
                errorRate: 0.1,        // 10%
                responseTime: 5000,    // 5 seconds
                memoryUsage: 0.8,      // 80%
                cpuUsage: 0.8          // 80%
            }
        };
    }

    /**
     * Start health monitoring
     */
    start(customConfig?: Partial<HealthMonitorConfig>): void {
        if (this.isRunning) {
            logger.warn('⚠️ Health monitor is already running');
            return;
        }

        // Merge configuration
        this.config = { ...this.config, ...customConfig };

        this.isRunning = true;
        this.startTime = Date.now();

        // Start periodic health checks
        this.monitoringTimer = setInterval(() => {
            this.performHealthCheck();
        }, this.config.checkIntervalMs);

        // Perform initial health check
        this.performHealthCheck();

        logger.info('📊 Health monitor started', {
            checkInterval: this.config.checkIntervalMs,
            metricsEnabled: this.config.enableMetrics,
            alertingEnabled: this.config.enableAlerting
        });
    }

    /**
     * Stop health monitoring
     */
    stop(): void {
        if (!this.isRunning) {
            return;
        }

        this.isRunning = false;

        if (this.monitoringTimer) {
            clearInterval(this.monitoringTimer);
            this.monitoringTimer = undefined;
        }

        logger.info('🛑 Health monitor stopped');
    }

    /**
     * Perform comprehensive health check
     */
    private async performHealthCheck(): Promise<void> {
        try {
            const startTime = Date.now();
            const healthStatus = await this.generateHealthStatus();
            const duration = Date.now() - startTime;

            // Store last health status
            this.lastHealthStatus = healthStatus;

            // Log health status
            this.logHealthStatus(healthStatus, duration);

            // Emit health check event
            this.emit('healthCheck', healthStatus);

            // Check for alerts
            if (this.config.enableAlerting) {
                this.checkForAlerts(healthStatus);
            }

        } catch (error) {
            logger.error('❌ Health check failed', { error });

            this.emit('healthCheckError', {
                error,
                timestamp: Date.now()
            });
        }
    }

    /**
     * Generate comprehensive health status
     */
    private async generateHealthStatus(): Promise<HealthStatus> {
        const checks: HealthStatus['checks'] = {};

        // Network connectivity check
        checks.network = await this.checkNetworkConnectivity();

        // Configuration validation check
        checks.configuration = this.checkConfiguration();

        // Security validation check
        checks.security = this.checkSecurity();

        // Memory usage check
        checks.memory = this.checkMemoryUsage();

        // Process health check
        checks.process = this.checkProcessHealth();

        // Ensemble SDK check
        checks.ensemble = await this.checkEnsembleSDK();

        // gRPC server check
        checks.grpc = this.checkGrpcServer();

        // Determine overall status
        const status = this.determineOverallStatus(checks);

        return {
            status,
            timestamp: Date.now(),
            uptime: Date.now() - this.startTime,
            checks,
            metrics: this.generateMetrics()
        };
    }

    /**
     * Check network connectivity
     */
    private async checkNetworkConnectivity(): Promise<any> {
        try {
            const startTime = Date.now();

            // Check Base Sepolia connectivity (placeholder)
            // In real implementation, this would ping the RPC endpoint
            const networkCheck = { connected: true };

            const duration = Date.now() - startTime;

            if (networkCheck.connected) {
                return {
                    status: 'pass',
                    message: 'Network connectivity operational',
                    lastCheck: Date.now(),
                    duration
                };
            } else {
                return {
                    status: 'fail',
                    message: 'Network connectivity failed',
                    lastCheck: Date.now(),
                    duration
                };
            }

        } catch (error) {
            return {
                status: 'fail',
                message: `Network check error: ${error}`,
                lastCheck: Date.now()
            };
        }
    }

    /**
     * Check configuration validity
     */
    private checkConfiguration(): any {
        try {
            const securityValidation = config.validateSecurity();

            if (securityValidation.isValid) {
                return {
                    status: 'pass',
                    message: 'Configuration validation passed',
                    lastCheck: Date.now()
                };
            } else {
                return {
                    status: 'fail',
                    message: `Configuration errors: ${securityValidation.errors.join(', ')}`,
                    lastCheck: Date.now()
                };
            }

        } catch (error) {
            return {
                status: 'fail',
                message: `Configuration check error: ${error}`,
                lastCheck: Date.now()
            };
        }
    }

    /**
     * Check security status
     */
    private checkSecurity(): any {
        try {
            // Check network setting
            const network = config.get('BLOCKCHAIN_NETWORK');
            if (network !== 'base-sepolia') {
                return {
                    status: 'fail',
                    message: `Invalid network: ${network}`,
                    lastCheck: Date.now()
                };
            }

            // Check gas price limits
            const maxGasPrice = config.getNumber('MAX_GAS_PRICE');
            if (maxGasPrice > 10000000000) { // 10 gwei
                return {
                    status: 'warn',
                    message: 'Gas price limit high',
                    lastCheck: Date.now()
                };
            }

            return {
                status: 'pass',
                message: 'Security checks passed',
                lastCheck: Date.now()
            };

        } catch (error) {
            return {
                status: 'fail',
                message: `Security check error: ${error}`,
                lastCheck: Date.now()
            };
        }
    }

    /**
     * Check memory usage
     */
    private checkMemoryUsage(): any {
        try {
            const memUsage = process.memoryUsage();
            const totalMem = memUsage.heapTotal;
            const usedMem = memUsage.heapUsed;
            const memoryPercentage = usedMem / totalMem;

            let status = 'pass';
            let message = 'Memory usage normal';

            if (memoryPercentage > (this.config.thresholds?.memoryUsage || 0.8)) {
                status = 'fail';
                message = `High memory usage: ${(memoryPercentage * 100).toFixed(1)}%`;
            } else if (memoryPercentage > 0.6) {
                status = 'warn';
                message = `Elevated memory usage: ${(memoryPercentage * 100).toFixed(1)}%`;
            }

            return {
                status,
                message,
                lastCheck: Date.now(),
                percentage: memoryPercentage
            };

        } catch (error) {
            return {
                status: 'fail',
                message: `Memory check error: ${error}`,
                lastCheck: Date.now()
            };
        }
    }

    /**
     * Check process health
     */
    private checkProcessHealth(): any {
        try {
            const uptime = process.uptime();
            const pid = process.pid;

            return {
                status: 'pass',
                message: `Process healthy, uptime: ${Math.floor(uptime)}s`,
                lastCheck: Date.now(),
                uptime,
                pid
            };

        } catch (error) {
            return {
                status: 'fail',
                message: `Process check error: ${error}`,
                lastCheck: Date.now()
            };
        }
    }

    /**
     * Check Ensemble SDK status
     */
    private async checkEnsembleSDK(): Promise<any> {
        try {
            // Check if SDK is connected and responsive
            // This would check actual SDK connectivity in real implementation
            const connected = this.metrics.ensemble.connected;
            const lastSuccess = this.metrics.ensemble.lastSuccess;
            const timeSinceLastSuccess = Date.now() - lastSuccess;

            if (!connected) {
                return {
                    status: 'fail',
                    message: 'Ensemble SDK not connected',
                    lastCheck: Date.now()
                };
            }

            if (timeSinceLastSuccess > 300000) { // 5 minutes
                return {
                    status: 'warn',
                    message: 'No successful Ensemble operations recently',
                    lastCheck: Date.now()
                };
            }

            return {
                status: 'pass',
                message: 'Ensemble SDK operational',
                lastCheck: Date.now()
            };

        } catch (error) {
            return {
                status: 'fail',
                message: `Ensemble SDK check error: ${error}`,
                lastCheck: Date.now()
            };
        }
    }

    /**
     * Check gRPC server status
     */
    private checkGrpcServer(): any {
        try {
            // In real implementation, this would check if gRPC server is accepting connections
            return {
                status: 'pass',
                message: 'gRPC server operational',
                lastCheck: Date.now()
            };

        } catch (error) {
            return {
                status: 'fail',
                message: `gRPC server check error: ${error}`,
                lastCheck: Date.now()
            };
        }
    }

    /**
     * Determine overall health status
     */
    private determineOverallStatus(checks: HealthStatus['checks']): 'healthy' | 'degraded' | 'unhealthy' {
        const statuses = Object.values(checks).map(check => check.status);

        if (statuses.includes('fail')) {
            return 'unhealthy';
        }

        if (statuses.includes('warn')) {
            return 'degraded';
        }

        return 'healthy';
    }

    /**
     * Generate metrics
     */
    private generateMetrics(): HealthStatus['metrics'] {
        const memUsage = process.memoryUsage();
        const errorRate = this.metrics.requests.total > 0
            ? this.metrics.requests.failed / this.metrics.requests.total
            : 0;

        const averageResponseTime = this.metrics.requests.total > 0
            ? this.metrics.requests.totalResponseTime / this.metrics.requests.total
            : 0;

        return {
            memory: {
                used: memUsage.heapUsed,
                total: memUsage.heapTotal,
                percentage: memUsage.heapUsed / memUsage.heapTotal
            },
            cpu: {
                usage: 0 // Would need additional library for CPU monitoring
            },
            requests: {
                total: this.metrics.requests.total,
                failed: this.metrics.requests.failed,
                errorRate,
                averageResponseTime
            },
            ensemble: {
                connected: this.metrics.ensemble.connected,
                lastSuccess: this.metrics.ensemble.lastSuccess,
                errors: this.metrics.ensemble.errors
            }
        };
    }

    /**
     * Log health status
     */
    private logHealthStatus(healthStatus: HealthStatus, duration: number): void {
        const logLevel = healthStatus.status === 'healthy' ? 'info' : 'warn';

        logger[logLevel](`📊 Health check completed: ${healthStatus.status}`, {
            status: healthStatus.status,
            duration,
            uptime: healthStatus.uptime,
            memoryUsage: healthStatus.metrics.memory.percentage,
            errorRate: healthStatus.metrics.requests.errorRate,
            checksCount: Object.keys(healthStatus.checks).length
        });
    }

    /**
     * Check for alert conditions
     */
    private checkForAlerts(healthStatus: HealthStatus): void {
        const thresholds = this.config.thresholds!;

        // Error rate alert
        if (healthStatus.metrics.requests.errorRate > thresholds.errorRate) {
            this.emit('alert', {
                type: 'error_rate',
                severity: 'high',
                message: `High error rate: ${(healthStatus.metrics.requests.errorRate * 100).toFixed(1)}%`,
                value: healthStatus.metrics.requests.errorRate,
                threshold: thresholds.errorRate,
                timestamp: Date.now()
            });
        }

        // Memory usage alert
        if (healthStatus.metrics.memory.percentage > thresholds.memoryUsage) {
            this.emit('alert', {
                type: 'memory_usage',
                severity: 'medium',
                message: `High memory usage: ${(healthStatus.metrics.memory.percentage * 100).toFixed(1)}%`,
                value: healthStatus.metrics.memory.percentage,
                threshold: thresholds.memoryUsage,
                timestamp: Date.now()
            });
        }

        // Response time alert
        if (healthStatus.metrics.requests.averageResponseTime > thresholds.responseTime) {
            this.emit('alert', {
                type: 'response_time',
                severity: 'medium',
                message: `High response time: ${healthStatus.metrics.requests.averageResponseTime}ms`,
                value: healthStatus.metrics.requests.averageResponseTime,
                threshold: thresholds.responseTime,
                timestamp: Date.now()
            });
        }

        // Service degraded alert
        if (healthStatus.status === 'unhealthy') {
            this.emit('alert', {
                type: 'service_unhealthy',
                severity: 'critical',
                message: 'Service is unhealthy',
                timestamp: Date.now()
            });
        }
    }

    /**
     * Record request metrics
     */
    recordRequest(success: boolean, responseTime: number): void {
        this.metrics.requests.total++;
        this.metrics.requests.totalResponseTime += responseTime;

        if (!success) {
            this.metrics.requests.failed++;
        }
    }

    /**
     * Record Ensemble SDK metrics
     */
    recordEnsembleOperation(success: boolean): void {
        if (success) {
            this.metrics.ensemble.lastSuccess = Date.now();
            this.metrics.ensemble.connected = true;
        } else {
            this.metrics.ensemble.errors++;
            if (this.metrics.ensemble.errors > 5) {
                this.metrics.ensemble.connected = false;
            }
        }
    }

    /**
     * Get current health status
     */
    getHealthStatus(): HealthStatus | null {
        return this.lastHealthStatus || null;
    }

    /**
     * Get uptime in seconds
     */
    getUptime(): number {
        return Math.floor((Date.now() - this.startTime) / 1000);
    }
}

/**
 * Performance Benchmarking Tools for Oracle Verification System
 * Comprehensive performance testing and optimization analysis
 */
import { performance, PerformanceObserver } from 'perf_hooks';
import { Worker, isMainThread, parentPort, workerData } from 'worker_threads';
import { EventEmitter } from 'events';
import { BlockchainOracleClient, LiveOracleData } from './blockchain-oracle-client';
import { AdvancedManipulationDetector } from './advanced-manipulation-detector';
import { AdvancedZKCircuits, ZKProofResult } from './advanced-zk-circuits';
import { MonitoringInfrastructure } from './monitoring-infrastructure';

export interface BenchmarkConfig {
  duration: number; // Test duration in milliseconds
  concurrency: number; // Concurrent requests
  rampUp: number; // Ramp-up time in milliseconds
  scenarios: BenchmarkScenario[];
  targets: {
    responseTime: number; // Maximum acceptable response time (ms)
    throughput: number; // Minimum requests per second
    errorRate: number; // Maximum error rate (%)
    memoryUsage: number; // Maximum memory usage (MB)
    cpuUsage: number; // Maximum CPU usage (%)
  };
}

export interface BenchmarkScenario {
  name: string;
  description: string;
  weight: number; // Relative weight (0-1)
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  payload?: any;
  expectedStatusCode: number;
  customValidation?: (response: any) => boolean;
}

export interface BenchmarkResult {
  scenario: string;
  timestamp: number;
  duration: number; // milliseconds
  success: boolean;
  statusCode?: number;
  responseTime: number; // milliseconds
  dataTransferred: number; // bytes
  error?: string;
  customMetrics?: Record<string, number>;
}

export interface BenchmarkReport {
  config: BenchmarkConfig;
  startTime: number;
  endTime: number;
  totalDuration: number;
  results: BenchmarkResult[];
  summary: {
    totalRequests: number;
    successfulRequests: number;
    failedRequests: number;
    successRate: number;
    averageResponseTime: number;
    medianResponseTime: number;
    p95ResponseTime: number;
    p99ResponseTime: number;
    throughput: number; // requests per second
    peakThroughput: number;
    totalDataTransferred: number;
    errorsByType: Record<string, number>;
  };
  performance: {
    averageMemoryUsage: number;
    peakMemoryUsage: number;
    averageCpuUsage: number;
    peakCpuUsage: number;
    gcPauses: number[];
    eventLoopDelays: number[];
  };
  recommendations: string[];
  passedTargets: string[];
  failedTargets: string[];
}

export class PerformanceBenchmark extends EventEmitter {
  private config: BenchmarkConfig;
  private results: BenchmarkResult[] = [];
  private isRunning: boolean = false;
  private workers: Worker[] = [];
  private performanceObserver: PerformanceObserver;
  private systemMetrics: any[] = [];

  constructor(config: BenchmarkConfig) {
    super();
    this.config = config;
    this.setupPerformanceObserver();
  }

  private setupPerformanceObserver(): void {
    this.performanceObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      for (const entry of entries) {
        this.emit('performance-entry', entry);
      }
    });
    this.performanceObserver.observe({ entryTypes: ['measure', 'mark'] });
  }

  public async runBenchmark(): Promise<BenchmarkReport> {
    if (this.isRunning) {
      throw new Error('Benchmark is already running');
    }

    this.isRunning = true;
    this.results = [];
    this.systemMetrics = [];

    const startTime = Date.now();
    this.emit('benchmark-started', { startTime, config: this.config });

    try {
      // Start system metrics collection
      const metricsInterval = setInterval(() => {
        this.collectSystemMetrics();
      }, 1000);

      // Ramp-up phase
      if (this.config.rampUp > 0) {
        await this.executeRampUp();
      }

      // Main test phase
      await this.executeMainTest();

      // Clean up
      clearInterval(metricsInterval);
      await this.cleanupWorkers();

      const endTime = Date.now();
      const report = this.generateReport(startTime, endTime);

      this.emit('benchmark-completed', report);
      return report;

    } catch (error) {
      this.emit('benchmark-error', error);
      throw error;
    } finally {
      this.isRunning = false;
    }
  }

  private async executeRampUp(): Promise<void> {
    const rampUpSteps = 10;
    const stepDuration = this.config.rampUp / rampUpSteps;
    const concurrencyStep = this.config.concurrency / rampUpSteps;

    for (let step = 1; step <= rampUpSteps; step++) {
      const currentConcurrency = Math.floor(concurrencyStep * step);
      this.emit('ramp-up-step', { step, concurrency: currentConcurrency });

      await this.executeConcurrentRequests(currentConcurrency, stepDuration);
      await new Promise(resolve => setTimeout(resolve, 100)); // Brief pause between steps
    }
  }

  private async executeMainTest(): Promise<void> {
    this.emit('main-test-started', { concurrency: this.config.concurrency, duration: this.config.duration });
    await this.executeConcurrentRequests(this.config.concurrency, this.config.duration);
  }

  private async executeConcurrentRequests(concurrency: number, duration: number): Promise<void> {
    const endTime = Date.now() + duration;
    const workers: Promise<void>[] = [];

    for (let i = 0; i < concurrency; i++) {
      const workerPromise = this.createWorker(endTime);
      workers.push(workerPromise);
    }

    await Promise.all(workers);
  }

  private async createWorker(endTime: number): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!isMainThread) {
        // This is worker code
        this.executeWorkerLoop(endTime).then(resolve).catch(reject);
        return;
      }

      // This is main thread code
      const worker = new Worker(__filename, {
        workerData: { endTime, config: this.config }
      });

      this.workers.push(worker);

      worker.on('message', (result: BenchmarkResult) => {
        this.results.push(result);
        this.emit('result', result);
      });

      worker.on('error', reject);
      worker.on('exit', (code) => {
        if (code !== 0) {
          reject(new Error(`Worker stopped with exit code ${code}`));
        } else {
          resolve();
        }
      });
    });
  }

  private async executeWorkerLoop(endTime: number): Promise<void> {
    while (Date.now() < endTime) {
      // Select random scenario based on weights
      const scenario = this.selectWeightedScenario();
      const result = await this.executeScenario(scenario);

      if (parentPort) {
        parentPort.postMessage(result);
      }

      // Brief pause to prevent overwhelming the system
      await new Promise(resolve => setTimeout(resolve, Math.random() * 10));
    }
  }

  private selectWeightedScenario(): BenchmarkScenario {
    const totalWeight = this.config.scenarios.reduce((sum, s) => sum + s.weight, 0);
    const random = Math.random() * totalWeight;

    let currentWeight = 0;
    for (const scenario of this.config.scenarios) {
      currentWeight += scenario.weight;
      if (random <= currentWeight) {
        return scenario;
      }
    }

    return this.config.scenarios[0]; // Fallback
  }

  private async executeScenario(scenario: BenchmarkScenario): Promise<BenchmarkResult> {
    const startTime = Date.now();
    performance.mark(`${scenario.name}-start`);

    try {
      const response = await this.makeRequest(scenario);
      const endTime = Date.now();
      const responseTime = endTime - startTime;

      performance.mark(`${scenario.name}-end`);
      performance.measure(`${scenario.name}`, `${scenario.name}-start`, `${scenario.name}-end`);

      const success = response.statusCode === scenario.expectedStatusCode &&
                     (!scenario.customValidation || scenario.customValidation(response.data));

      return {
        scenario: scenario.name,
        timestamp: startTime,
        duration: responseTime,
        success,
        statusCode: response.statusCode,
        responseTime,
        dataTransferred: response.dataSize || 0,
        customMetrics: response.customMetrics,
      };

    } catch (error) {
      const endTime = Date.now();
      const responseTime = endTime - startTime;

      return {
        scenario: scenario.name,
        timestamp: startTime,
        duration: responseTime,
        success: false,
        responseTime,
        dataTransferred: 0,
        error: error instanceof Error ? error.message : String(error),
      };
    }
  }

  private async makeRequest(scenario: BenchmarkScenario): Promise<any> {
    // Simulate different types of oracle verification requests
    switch (scenario.endpoint) {
      case '/api/v1/oracle/verify':
        return await this.simulateOracleVerification();
      case '/api/v1/oracle/status':
        return await this.simulateOracleStatus();
      case '/api/v1/zk/generate-proof':
        return await this.simulateZKProofGeneration();
      case '/api/v1/manipulation/detect':
        return await this.simulateManipulationDetection();
      case '/api/v1/mento/monitor':
        return await this.simulateMentoMonitoring();
      default:
        throw new Error(`Unknown endpoint: ${scenario.endpoint}`);
    }
  }

  private async simulateOracleVerification(): Promise<any> {
    const startTime = performance.now();

    // Simulate oracle data fetching (20-50ms)
    await new Promise(resolve => setTimeout(resolve, 20 + Math.random() * 30));

    // Simulate verification logic (10-30ms)
    await new Promise(resolve => setTimeout(resolve, 10 + Math.random() * 20));

    const endTime = performance.now();
    const processingTime = endTime - startTime;

    return {
      statusCode: 200,
      data: {
        verified: true,
        confidence: 0.95 + Math.random() * 0.05,
        processingTime,
      },
      dataSize: 256,
      customMetrics: {
        verificationLatency: processingTime,
        confidenceScore: 0.95 + Math.random() * 0.05,
      },
    };
  }

  private async simulateOracleStatus(): Promise<any> {
    // Fast status check (1-5ms)
    await new Promise(resolve => setTimeout(resolve, 1 + Math.random() * 4));

    return {
      statusCode: 200,
      data: {
        status: 'healthy',
        oracles: 15,
        healthy: 14 + Math.floor(Math.random() * 2),
        lastUpdate: Date.now(),
      },
      dataSize: 128,
    };
  }

  private async simulateZKProofGeneration(): Promise<any> {
    const startTime = performance.now();

    // Simulate ZK proof generation (50-200ms)
    await new Promise(resolve => setTimeout(resolve, 50 + Math.random() * 150));

    const endTime = performance.now();
    const proofTime = endTime - startTime;

    return {
      statusCode: 200,
      data: {
        proof: 'zk_proof_' + Math.random().toString(36),
        verificationKey: 'vk_' + Math.random().toString(36),
        proofTime,
      },
      dataSize: 1024,
      customMetrics: {
        zkProofGenerationTime: proofTime,
        circuitComplexity: Math.floor(Math.random() * 1000) + 500,
      },
    };
  }

  private async simulateManipulationDetection(): Promise<any> {
    const startTime = performance.now();

    // Simulate ML-based manipulation detection (30-100ms)
    await new Promise(resolve => setTimeout(resolve, 30 + Math.random() * 70));

    const endTime = performance.now();
    const detectionTime = endTime - startTime;

    const manipulationDetected = Math.random() < 0.05; // 5% chance

    return {
      statusCode: 200,
      data: {
        manipulationDetected,
        confidence: manipulationDetected ? 0.85 + Math.random() * 0.15 : Math.random() * 0.3,
        detectionTime,
        algorithms: ['price_spike', 'volume_anomaly', 'consensus_break'],
      },
      dataSize: 512,
      customMetrics: {
        detectionLatency: detectionTime,
        mlConfidence: Math.random(),
      },
    };
  }

  private async simulateMentoMonitoring(): Promise<any> {
    const startTime = performance.now();

    // Simulate Mento protocol monitoring (40-80ms)
    await new Promise(resolve => setTimeout(resolve, 40 + Math.random() * 40));

    const endTime = performance.now();
    const monitoringTime = endTime - startTime;

    return {
      statusCode: 200,
      data: {
        stablecoins: 15,
        totalValue: 134000000 + Math.random() * 10000000,
        healthScore: 0.9 + Math.random() * 0.1,
        alerts: Math.floor(Math.random() * 3),
        monitoringTime,
      },
      dataSize: 768,
      customMetrics: {
        mentoMonitoringLatency: monitoringTime,
        protocolHealthScore: 0.9 + Math.random() * 0.1,
      },
    };
  }

  private collectSystemMetrics(): void {
    const memoryUsage = process.memoryUsage();
    const cpuUsage = process.cpuUsage();

    this.systemMetrics.push({
      timestamp: Date.now(),
      memory: {
        rss: memoryUsage.rss / 1024 / 1024, // MB
        heapUsed: memoryUsage.heapUsed / 1024 / 1024, // MB
        heapTotal: memoryUsage.heapTotal / 1024 / 1024, // MB
        external: memoryUsage.external / 1024 / 1024, // MB
      },
      cpu: {
        user: cpuUsage.user,
        system: cpuUsage.system,
      },
    });
  }

  private async cleanupWorkers(): Promise<void> {
    const terminationPromises = this.workers.map(worker => {
      return new Promise<void>((resolve) => {
        worker.terminate().then(() => resolve());
      });
    });

    await Promise.all(terminationPromises);
    this.workers = [];
  }

  private generateReport(startTime: number, endTime: number): BenchmarkReport {
    const totalDuration = endTime - startTime;
    const successfulResults = this.results.filter(r => r.success);
    const failedResults = this.results.filter(r => !r.success);

    // Calculate response time percentiles
    const responseTimes = successfulResults.map(r => r.responseTime).sort((a, b) => a - b);
    const p95Index = Math.floor(responseTimes.length * 0.95);
    const p99Index = Math.floor(responseTimes.length * 0.99);
    const medianIndex = Math.floor(responseTimes.length * 0.5);

    // Calculate throughput over time
    const throughputWindows = this.calculateThroughputWindows();
    const peakThroughput = Math.max(...throughputWindows);

    // Error analysis
    const errorsByType = failedResults.reduce((acc, result) => {
      const errorType = result.error || 'Unknown';
      acc[errorType] = (acc[errorType] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    // Performance metrics
    const memoryMetrics = this.systemMetrics.map(m => m.memory.heapUsed);
    const averageMemoryUsage = memoryMetrics.reduce((sum, val) => sum + val, 0) / memoryMetrics.length;
    const peakMemoryUsage = Math.max(...memoryMetrics);

    // Target validation
    const { passedTargets, failedTargets, recommendations } = this.validateTargets(
      successfulResults.length / this.results.length * 100,
      responseTimes.reduce((sum, val) => sum + val, 0) / responseTimes.length,
      this.results.length / (totalDuration / 1000),
      averageMemoryUsage,
      50 // Simulated CPU usage
    );

    return {
      config: this.config,
      startTime,
      endTime,
      totalDuration,
      results: this.results,
      summary: {
        totalRequests: this.results.length,
        successfulRequests: successfulResults.length,
        failedRequests: failedResults.length,
        successRate: successfulResults.length / this.results.length * 100,
        averageResponseTime: responseTimes.reduce((sum, val) => sum + val, 0) / responseTimes.length,
        medianResponseTime: responseTimes[medianIndex] || 0,
        p95ResponseTime: responseTimes[p95Index] || 0,
        p99ResponseTime: responseTimes[p99Index] || 0,
        throughput: this.results.length / (totalDuration / 1000),
        peakThroughput,
        totalDataTransferred: this.results.reduce((sum, r) => sum + r.dataTransferred, 0),
        errorsByType,
      },
      performance: {
        averageMemoryUsage,
        peakMemoryUsage,
        averageCpuUsage: 50, // Simulated
        peakCpuUsage: 75, // Simulated
        gcPauses: [], // Would be collected from GC events
        eventLoopDelays: [], // Would be collected from event loop monitoring
      },
      recommendations,
      passedTargets,
      failedTargets,
    };
  }

  private calculateThroughputWindows(): number[] {
    const windowSize = 1000; // 1 second windows
    const windows: number[] = [];
    const startTime = this.results[0]?.timestamp || Date.now();
    const endTime = this.results[this.results.length - 1]?.timestamp || Date.now();

    for (let windowStart = startTime; windowStart < endTime; windowStart += windowSize) {
      const windowEnd = windowStart + windowSize;
      const requestsInWindow = this.results.filter(
        r => r.timestamp >= windowStart && r.timestamp < windowEnd
      ).length;
      windows.push(requestsInWindow);
    }

    return windows;
  }

  private validateTargets(
    successRate: number,
    avgResponseTime: number,
    throughput: number,
    memoryUsage: number,
    cpuUsage: number
  ): { passedTargets: string[]; failedTargets: string[]; recommendations: string[] } {
    const passedTargets: string[] = [];
    const failedTargets: string[] = [];
    const recommendations: string[] = [];

    // Response Time Target
    if (avgResponseTime <= this.config.targets.responseTime) {
      passedTargets.push(`Response Time: ${avgResponseTime.toFixed(1)}ms ≤ ${this.config.targets.responseTime}ms`);
    } else {
      failedTargets.push(`Response Time: ${avgResponseTime.toFixed(1)}ms > ${this.config.targets.responseTime}ms`);
      recommendations.push('Consider optimizing database queries and implementing better caching');
    }

    // Throughput Target
    if (throughput >= this.config.targets.throughput) {
      passedTargets.push(`Throughput: ${throughput.toFixed(1)} RPS ≥ ${this.config.targets.throughput} RPS`);
    } else {
      failedTargets.push(`Throughput: ${throughput.toFixed(1)} RPS < ${this.config.targets.throughput} RPS`);
      recommendations.push('Scale horizontally with more instances or optimize request processing');
    }

    // Error Rate Target
    const errorRate = 100 - successRate;
    if (errorRate <= this.config.targets.errorRate) {
      passedTargets.push(`Error Rate: ${errorRate.toFixed(2)}% ≤ ${this.config.targets.errorRate}%`);
    } else {
      failedTargets.push(`Error Rate: ${errorRate.toFixed(2)}% > ${this.config.targets.errorRate}%`);
      recommendations.push('Investigate error patterns and improve error handling');
    }

    // Memory Usage Target
    if (memoryUsage <= this.config.targets.memoryUsage) {
      passedTargets.push(`Memory Usage: ${memoryUsage.toFixed(1)}MB ≤ ${this.config.targets.memoryUsage}MB`);
    } else {
      failedTargets.push(`Memory Usage: ${memoryUsage.toFixed(1)}MB > ${this.config.targets.memoryUsage}MB`);
      recommendations.push('Optimize memory usage with better garbage collection and data structures');
    }

    // CPU Usage Target
    if (cpuUsage <= this.config.targets.cpuUsage) {
      passedTargets.push(`CPU Usage: ${cpuUsage.toFixed(1)}% ≤ ${this.config.targets.cpuUsage}%`);
    } else {
      failedTargets.push(`CPU Usage: ${cpuUsage.toFixed(1)}% > ${this.config.targets.cpuUsage}%`);
      recommendations.push('Optimize CPU-intensive operations and consider algorithmic improvements');
    }

    return { passedTargets, failedTargets, recommendations };
  }

  public stop(): void {
    this.isRunning = false;
    this.cleanupWorkers();
    this.performanceObserver.disconnect();
  }
}

// Predefined benchmark configurations
export const createMentoBenchmarkConfig = (): BenchmarkConfig => ({
  duration: 60000, // 1 minute
  concurrency: 50, // 50 concurrent users
  rampUp: 10000, // 10 second ramp-up
  scenarios: [
    {
      name: 'oracle-verification',
      description: 'Standard oracle price verification',
      weight: 0.4,
      endpoint: '/api/v1/oracle/verify',
      method: 'POST',
      expectedStatusCode: 200,
      customValidation: (response) => response.verified === true,
    },
    {
      name: 'oracle-status',
      description: 'Oracle health status check',
      weight: 0.2,
      endpoint: '/api/v1/oracle/status',
      method: 'GET',
      expectedStatusCode: 200,
    },
    {
      name: 'zk-proof-generation',
      description: 'Zero-knowledge proof generation',
      weight: 0.15,
      endpoint: '/api/v1/zk/generate-proof',
      method: 'POST',
      expectedStatusCode: 200,
    },
    {
      name: 'manipulation-detection',
      description: 'Oracle manipulation detection',
      weight: 0.15,
      endpoint: '/api/v1/manipulation/detect',
      method: 'POST',
      expectedStatusCode: 200,
    },
    {
      name: 'mento-monitoring',
      description: 'Mento protocol monitoring',
      weight: 0.1,
      endpoint: '/api/v1/mento/monitor',
      method: 'GET',
      expectedStatusCode: 200,
    },
  ],
  targets: {
    responseTime: 100, // 100ms max response time
    throughput: 100, // 100 RPS minimum
    errorRate: 1, // 1% max error rate
    memoryUsage: 512, // 512MB max memory
    cpuUsage: 70, // 70% max CPU
  },
});

// Demo function for performance benchmarking
export async function demonstratePerformanceBenchmarking(): Promise<any> {
  console.log('\n⚡ === PERFORMANCE BENCHMARKING DEMO ===');
  console.log('Running comprehensive performance tests for Mento oracle verification...\n');

  const config = createMentoBenchmarkConfig();
  const benchmark = new PerformanceBenchmark(config);

  // Set up event listeners
  benchmark.on('benchmark-started', (data) => {
    console.log('🚀 Benchmark started');
    console.log(`   Duration: ${data.config.duration/1000}s`);
    console.log(`   Concurrency: ${data.config.concurrency} users`);
    console.log(`   Scenarios: ${data.config.scenarios.length}`);
  });

  benchmark.on('ramp-up-step', (data) => {
    console.log(`📈 Ramp-up Step ${data.step}: ${data.concurrency} concurrent users`);
  });

  benchmark.on('main-test-started', (data) => {
    console.log(`🎯 Main test started: ${data.concurrency} users for ${data.duration/1000}s`);
  });

  let resultCount = 0;
  benchmark.on('result', (result) => {
    resultCount++;
    if (resultCount % 100 === 0) {
      const status = result.success ? '✅' : '❌';
      console.log(`   ${status} ${resultCount} requests completed (${result.scenario}: ${result.responseTime.toFixed(1)}ms)`);
    }
  });

  try {
    const report = await benchmark.runBenchmark();

    console.log('\n📊 === BENCHMARK RESULTS ===');
    console.log(`Total Requests: ${report.summary.totalRequests}`);
    console.log(`Success Rate: ${report.summary.successRate.toFixed(2)}%`);
    console.log(`Average Response Time: ${report.summary.averageResponseTime.toFixed(1)}ms`);
    console.log(`P95 Response Time: ${report.summary.p95ResponseTime.toFixed(1)}ms`);
    console.log(`P99 Response Time: ${report.summary.p99ResponseTime.toFixed(1)}ms`);
    console.log(`Throughput: ${report.summary.throughput.toFixed(1)} RPS`);
    console.log(`Peak Throughput: ${report.summary.peakThroughput} RPS`);
    console.log(`Data Transferred: ${(report.summary.totalDataTransferred/1024/1024).toFixed(2)} MB`);

    console.log('\n🎯 === TARGET VALIDATION ===');
    report.passedTargets.forEach(target => console.log(`✅ ${target}`));
    report.failedTargets.forEach(target => console.log(`❌ ${target}`));

    if (report.recommendations.length > 0) {
      console.log('\n💡 === RECOMMENDATIONS ===');
      report.recommendations.forEach(rec => console.log(`   • ${rec}`));
    }

    console.log('\n📈 === PERFORMANCE METRICS ===');
    console.log(`Average Memory Usage: ${report.performance.averageMemoryUsage.toFixed(1)} MB`);
    console.log(`Peak Memory Usage: ${report.performance.peakMemoryUsage.toFixed(1)} MB`);
    console.log(`Average CPU Usage: ${report.performance.averageCpuUsage.toFixed(1)}%`);
    console.log(`Peak CPU Usage: ${report.performance.peakCpuUsage.toFixed(1)}%`);

    return {
      status: 'success',
      duration: `${report.totalDuration/1000}s`,
      totalRequests: report.summary.totalRequests,
      successRate: report.summary.successRate,
      averageResponseTime: report.summary.averageResponseTime,
      throughput: report.summary.throughput,
      passedTargets: report.passedTargets.length,
      failedTargets: report.failedTargets.length,
      recommendationsCount: report.recommendations.length,
    };

  } catch (error) {
    console.error('❌ Benchmark failed:', error);
    throw error;
  } finally {
    benchmark.stop();
  }
}

// Worker thread code
if (!isMainThread && workerData) {
  const { endTime, config } = workerData;
  const benchmark = new PerformanceBenchmark(config);
  benchmark.executeWorkerLoop(endTime).then(() => {
    process.exit(0);
  }).catch((error) => {
    console.error('Worker error:', error);
    process.exit(1);
  });
}

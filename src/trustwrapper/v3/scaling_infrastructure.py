#!/usr/bin/env python3
"""
TrustWrapper v3.0 Scaling Infrastructure
Advanced async processing, Redis caching, and connection pooling for high-performance multi-chain verification
Task 2.3: Week 2 Phase 1 Implementation
"""

import asyncio
import hashlib
import json
import logging
import pickle
import time
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

import aioredis

from .enhanced_oracle_integration import MultiOracleConsensus, OracleData

# Import v3.0 components


class CacheStrategy(Enum):
    """Cache strategy for different data types"""

    WRITE_THROUGH = "write_through"  # Write to cache and database simultaneously
    WRITE_BEHIND = "write_behind"  # Write to cache first, database later
    WRITE_AROUND = "write_around"  # Write to database, bypass cache
    READ_THROUGH = "read_through"  # Check cache first, fallback to source


class ProcessingPriority(Enum):
    """Processing priority levels for async task management"""

    CRITICAL = "critical"  # Real-time verification requests
    HIGH = "high"  # Oracle updates, consensus calculations
    NORMAL = "normal"  # Health checks, metrics updates
    LOW = "low"  # Background cleanup, analytics


@dataclass
class CacheConfig:
    """Redis cache configuration"""

    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0
    max_connections: int = 50
    connection_timeout: float = 5.0
    socket_timeout: float = 30.0
    retry_on_timeout: bool = True
    health_check_interval: float = 30.0

    # Cache policies
    default_ttl: int = 300  # 5 minutes
    max_memory_policy: str = "allkeys-lru"
    compression_enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConnectionPoolConfig:
    """Connection pool configuration for various services"""

    min_size: int = 5
    max_size: int = 50
    max_queries: int = 50000
    max_inactive_connection_lifetime: float = 300.0
    connection_timeout: float = 10.0
    command_timeout: float = 60.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AsyncTaskConfig:
    """Async processing configuration"""

    max_concurrent_tasks: int = 100
    task_timeout: float = 60.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    queue_size: int = 1000
    worker_count: int = 10
    priority_queues: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RedisConnectionManager:
    """
    High-performance Redis connection manager with connection pooling,
    automatic failover, and health monitoring
    """

    def __init__(self, config: CacheConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.redis")

        # Connection management
        self.redis_pool = None
        self.connection_pool = None
        self._connected = False
        self._health_check_task = None

        # Performance metrics
        self.metrics = {
            "total_commands": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "connection_errors": 0,
            "avg_response_time": 0.0,
        }

    async def initialize(self) -> None:
        """Initialize Redis connection pool"""
        try:
            self.logger.info("🚀 Initializing Redis Connection Manager...")

            # Create connection pool
            self.redis_pool = aioredis.ConnectionPool.from_url(
                f"redis://{self.config.host}:{self.config.port}/{self.config.db}",
                password=self.config.password,
                max_connections=self.config.max_connections,
                socket_timeout=self.config.socket_timeout,
                socket_connect_timeout=self.config.connection_timeout,
                retry_on_timeout=self.config.retry_on_timeout,
                health_check_interval=self.config.health_check_interval,
            )

            # Create Redis client
            self.connection_pool = aioredis.Redis(connection_pool=self.redis_pool)

            # Test connection
            await self.connection_pool.ping()

            # Configure Redis policies
            await self._configure_redis_policies()

            # Start health monitoring
            self._health_check_task = asyncio.create_task(self._monitor_health())

            self._connected = True
            self.logger.info("✅ Redis Connection Manager initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Redis Connection Manager: {e}")
            raise

    async def _configure_redis_policies(self) -> None:
        """Configure Redis memory and eviction policies"""
        try:
            # Set max memory policy
            await self.connection_pool.config_set(
                "maxmemory-policy", self.config.max_memory_policy
            )

            # Enable keyspace notifications for expiration events
            await self.connection_pool.config_set("notify-keyspace-events", "Ex")

            self.logger.debug("Redis policies configured successfully")

        except Exception as e:
            self.logger.warning(f"Failed to configure Redis policies: {e}")

    async def _monitor_health(self) -> None:
        """Background task to monitor Redis health"""
        while self._connected:
            try:
                # Ping Redis
                start_time = time.time()
                await self.connection_pool.ping()
                latency = time.time() - start_time

                # Update metrics
                self.metrics["avg_response_time"] = (
                    self.metrics["avg_response_time"] * 0.9 + latency * 0.1
                )

                # Log health status
                self.logger.debug(f"Redis health check: {latency*1000:.1f}ms latency")

                await asyncio.sleep(self.config.health_check_interval)

            except Exception as e:
                self.logger.error(f"Redis health check failed: {e}")
                self.metrics["connection_errors"] += 1
                await asyncio.sleep(5.0)

    async def get(self, key: str, decode: bool = True) -> Optional[Any]:
        """Get value from Redis cache"""
        try:
            start_time = time.time()

            # Get raw value
            raw_value = await self.connection_pool.get(key)

            # Update metrics
            self.metrics["total_commands"] += 1
            execution_time = time.time() - start_time

            if raw_value is None:
                self.metrics["cache_misses"] += 1
                return None

            self.metrics["cache_hits"] += 1

            # Decode if requested
            if decode:
                try:
                    if self.config.compression_enabled:
                        # Try to unpickle first (for complex objects)
                        try:
                            return pickle.loads(raw_value)
                        except:
                            # Fallback to JSON
                            return json.loads(raw_value.decode())
                    else:
                        return json.loads(raw_value.decode())
                except:
                    # Return raw string if JSON parsing fails
                    return raw_value.decode()

            return raw_value

        except Exception as e:
            self.logger.error(f"Redis GET error for key {key}: {e}")
            self.metrics["connection_errors"] += 1
            return None

    async def set(
        self, key: str, value: Any, ttl: Optional[int] = None, encode: bool = True
    ) -> bool:
        """Set value in Redis cache"""
        try:
            start_time = time.time()

            # Encode value
            if encode:
                if self.config.compression_enabled and not isinstance(
                    value, (str, int, float)
                ):
                    # Use pickle for complex objects
                    encoded_value = pickle.dumps(value)
                else:
                    # Use JSON for simple objects
                    if isinstance(value, (dict, list)):
                        encoded_value = json.dumps(value)
                    else:
                        encoded_value = str(value)
            else:
                encoded_value = value

            # Set with TTL
            ttl = ttl or self.config.default_ttl
            await self.connection_pool.setex(key, ttl, encoded_value)

            # Update metrics
            self.metrics["total_commands"] += 1

            return True

        except Exception as e:
            self.logger.error(f"Redis SET error for key {key}: {e}")
            self.metrics["connection_errors"] += 1
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from Redis cache"""
        try:
            result = await self.connection_pool.delete(key)
            self.metrics["total_commands"] += 1
            return result > 0

        except Exception as e:
            self.logger.error(f"Redis DELETE error for key {key}: {e}")
            self.metrics["connection_errors"] += 1
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis cache"""
        try:
            result = await self.connection_pool.exists(key)
            self.metrics["total_commands"] += 1
            return result > 0

        except Exception as e:
            self.logger.error(f"Redis EXISTS error for key {key}: {e}")
            self.metrics["connection_errors"] += 1
            return False

    async def get_pattern(self, pattern: str) -> List[str]:
        """Get all keys matching pattern"""
        try:
            keys = await self.connection_pool.keys(pattern)
            self.metrics["total_commands"] += 1
            return [key.decode() for key in keys]

        except Exception as e:
            self.logger.error(f"Redis KEYS error for pattern {pattern}: {e}")
            self.metrics["connection_errors"] += 1
            return []

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter in Redis"""
        try:
            result = await self.connection_pool.incrby(key, amount)
            self.metrics["total_commands"] += 1
            return result

        except Exception as e:
            self.logger.error(f"Redis INCREMENT error for key {key}: {e}")
            self.metrics["connection_errors"] += 1
            return 0

    def get_metrics(self) -> Dict[str, Any]:
        """Get connection manager metrics"""
        total_requests = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        hit_rate = (
            self.metrics["cache_hits"] / total_requests if total_requests > 0 else 0.0
        )

        return {
            **self.metrics,
            "cache_hit_rate": hit_rate,
            "connected": self._connected,
            "pool_info": {
                "created_connections": (
                    self.redis_pool.created_connections if self.redis_pool else 0
                ),
                "available_connections": (
                    len(self.redis_pool._available_connections)
                    if self.redis_pool
                    else 0
                ),
                "in_use_connections": (
                    len(self.redis_pool._in_use_connections) if self.redis_pool else 0
                ),
            },
        }

    async def shutdown(self) -> None:
        """Shutdown Redis connection manager"""
        self.logger.info("🛑 Shutting down Redis Connection Manager...")

        self._connected = False

        if self._health_check_task:
            self._health_check_task.cancel()

        if self.connection_pool:
            await self.connection_pool.close()

        if self.redis_pool:
            await self.redis_pool.disconnect()

        self.logger.info("Redis Connection Manager shutdown complete")


class AsyncTaskManager:
    """
    High-performance async task manager with priority queues,
    concurrent execution limits, and intelligent task scheduling
    """

    def __init__(self, config: AsyncTaskConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.async_tasks")

        # Task queues by priority
        self.priority_queues = {
            ProcessingPriority.CRITICAL: asyncio.Queue(
                maxsize=self.config.queue_size // 4
            ),
            ProcessingPriority.HIGH: asyncio.Queue(maxsize=self.config.queue_size // 3),
            ProcessingPriority.NORMAL: asyncio.Queue(
                maxsize=self.config.queue_size // 3
            ),
            ProcessingPriority.LOW: asyncio.Queue(maxsize=self.config.queue_size // 4),
        }

        # Task tracking
        self.active_tasks = set()
        self.completed_tasks = {}
        self.failed_tasks = {}

        # Workers
        self.workers = []
        self.worker_stats = {}

        # Performance metrics
        self.metrics = {
            "total_tasks_submitted": 0,
            "total_tasks_completed": 0,
            "total_tasks_failed": 0,
            "avg_execution_time": 0.0,
            "tasks_by_priority": {p.value: 0 for p in ProcessingPriority},
            "queue_lengths": {},
        }

        # State
        self.running = False

    async def start(self) -> None:
        """Start the async task manager"""
        if self.running:
            return

        self.logger.info("🚀 Starting Async Task Manager...")
        self.running = True

        # Start worker coroutines
        for i in range(self.config.worker_count):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)
            self.worker_stats[f"worker-{i}"] = {
                "tasks_processed": 0,
                "total_execution_time": 0.0,
                "last_task_time": None,
                "errors": 0,
            }

        # Start metrics updater
        asyncio.create_task(self._update_metrics())

        self.logger.info(
            f"✅ Async Task Manager started with {self.config.worker_count} workers"
        )

    async def stop(self) -> None:
        """Stop the async task manager"""
        self.logger.info("🛑 Stopping Async Task Manager...")
        self.running = False

        # Cancel all workers
        for worker in self.workers:
            worker.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)

        # Cancel remaining active tasks
        for task in self.active_tasks.copy():
            task.cancel()

        self.logger.info("Async Task Manager stopped")

    async def _worker(self, worker_id: str) -> None:
        """Worker coroutine to process tasks"""
        stats = self.worker_stats[worker_id]

        while self.running:
            try:
                # Get task from highest priority queue with available tasks
                task_data = await self._get_next_task()

                if task_data is None:
                    await asyncio.sleep(0.1)  # Brief pause if no tasks
                    continue

                priority, task_id, coro, callback = task_data

                # Execute task
                start_time = time.time()
                try:
                    self.logger.debug(
                        f"{worker_id} executing task {task_id} (priority: {priority.value})"
                    )

                    # Run with timeout
                    result = await asyncio.wait_for(
                        coro, timeout=self.config.task_timeout
                    )

                    # Update metrics
                    execution_time = time.time() - start_time
                    stats["tasks_processed"] += 1
                    stats["total_execution_time"] += execution_time
                    stats["last_task_time"] = time.time()

                    # Store result
                    self.completed_tasks[task_id] = {
                        "result": result,
                        "execution_time": execution_time,
                        "worker_id": worker_id,
                        "completed_at": time.time(),
                    }

                    # Call callback if provided
                    if callback:
                        try:
                            if asyncio.iscoroutinefunction(callback):
                                await callback(task_id, result, None)
                            else:
                                callback(task_id, result, None)
                        except Exception as e:
                            self.logger.warning(f"Task callback error: {e}")

                    self.metrics["total_tasks_completed"] += 1

                except asyncio.TimeoutError:
                    error = (
                        f"Task {task_id} timed out after {self.config.task_timeout}s"
                    )
                    self.logger.warning(error)
                    self._handle_task_failure(task_id, error, callback, stats)

                except Exception as e:
                    error = f"Task {task_id} failed: {e}"
                    self.logger.error(error)
                    self._handle_task_failure(task_id, error, callback, stats)

            except Exception as e:
                self.logger.error(f"Worker {worker_id} error: {e}")
                stats["errors"] += 1
                await asyncio.sleep(1.0)

    async def _get_next_task(self):
        """Get next task from priority queues"""
        # Check queues in priority order
        for priority in [
            ProcessingPriority.CRITICAL,
            ProcessingPriority.HIGH,
            ProcessingPriority.NORMAL,
            ProcessingPriority.LOW,
        ]:
            queue = self.priority_queues[priority]

            if not queue.empty():
                try:
                    return await asyncio.wait_for(queue.get(), timeout=0.1)
                except asyncio.TimeoutError:
                    continue

        return None

    def _handle_task_failure(
        self,
        task_id: str,
        error: str,
        callback: Optional[Callable],
        stats: Dict[str, Any],
    ):
        """Handle task failure"""
        stats["errors"] += 1

        self.failed_tasks[task_id] = {"error": error, "failed_at": time.time()}

        if callback:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(task_id, None, error))
                else:
                    callback(task_id, None, error)
            except Exception as e:
                self.logger.warning(f"Failure callback error: {e}")

        self.metrics["total_tasks_failed"] += 1

    async def submit_task(
        self,
        task_id: str,
        coro: Any,
        priority: ProcessingPriority = ProcessingPriority.NORMAL,
        callback: Optional[Callable] = None,
    ) -> bool:
        """Submit async task for execution"""
        try:
            # Check if task manager is running
            if not self.running:
                raise RuntimeError("Task manager not running")

            # Get appropriate queue
            queue = self.priority_queues[priority]

            # Submit task (non-blocking)
            try:
                queue.put_nowait((priority, task_id, coro, callback))

                # Update metrics
                self.metrics["total_tasks_submitted"] += 1
                self.metrics["tasks_by_priority"][priority.value] += 1

                self.logger.debug(
                    f"Task {task_id} submitted with priority {priority.value}"
                )
                return True

            except asyncio.QueueFull:
                self.logger.warning(
                    f"Queue full for priority {priority.value}, task {task_id} rejected"
                )
                return False

        except Exception as e:
            self.logger.error(f"Error submitting task {task_id}: {e}")
            return False

    async def get_task_result(self, task_id: str, timeout: float = 10.0) -> Any:
        """Get result of completed task"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Check completed tasks
            if task_id in self.completed_tasks:
                return self.completed_tasks[task_id]["result"]

            # Check failed tasks
            if task_id in self.failed_tasks:
                raise RuntimeError(
                    f"Task failed: {self.failed_tasks[task_id]['error']}"
                )

            await asyncio.sleep(0.1)

        raise asyncio.TimeoutError(f"Task {task_id} result timeout after {timeout}s")

    async def _update_metrics(self) -> None:
        """Update performance metrics"""
        while self.running:
            try:
                # Update queue lengths
                for priority, queue in self.priority_queues.items():
                    self.metrics["queue_lengths"][priority.value] = queue.qsize()

                # Calculate average execution time
                total_time = sum(
                    stats["total_execution_time"]
                    for stats in self.worker_stats.values()
                )
                total_tasks = sum(
                    stats["tasks_processed"] for stats in self.worker_stats.values()
                )

                if total_tasks > 0:
                    self.metrics["avg_execution_time"] = total_time / total_tasks

                await asyncio.sleep(10.0)  # Update every 10 seconds

            except Exception as e:
                self.logger.error(f"Metrics update error: {e}")
                await asyncio.sleep(30.0)

    def get_metrics(self) -> Dict[str, Any]:
        """Get task manager metrics"""
        return {
            **self.metrics,
            "running": self.running,
            "active_workers": len([w for w in self.workers if not w.done()]),
            "worker_stats": self.worker_stats,
            "completed_tasks_count": len(self.completed_tasks),
            "failed_tasks_count": len(self.failed_tasks),
        }


class PerformanceCacheLayer:
    """
    Intelligent caching layer for TrustWrapper v3.0 with advanced cache strategies,
    automatic invalidation, and performance optimization
    """

    def __init__(self, redis_manager: RedisConnectionManager):
        self.redis_manager = redis_manager
        self.logger = logging.getLogger(f"{__name__}.cache")

        # Cache strategies for different data types
        self.cache_strategies = {
            "verification_results": CacheStrategy.WRITE_THROUGH,
            "oracle_consensus": CacheStrategy.WRITE_BEHIND,
            "chain_health": CacheStrategy.READ_THROUGH,
            "cost_estimates": CacheStrategy.WRITE_AROUND,
        }

        # TTL configurations
        self.ttl_configs = {
            "verification_results": 3600,  # 1 hour
            "oracle_consensus": 300,  # 5 minutes
            "oracle_data": 120,  # 2 minutes
            "chain_health": 600,  # 10 minutes
            "cost_estimates": 1800,  # 30 minutes
            "performance_metrics": 60,  # 1 minute
        }

        # Cache key prefixes
        self.key_prefixes = {
            "verification": "tw3:verify:",
            "oracle": "tw3:oracle:",
            "chain": "tw3:chain:",
            "cost": "tw3:cost:",
            "metrics": "tw3:metrics:",
        }

        # Cache performance metrics
        self.cache_metrics = {
            "operations": 0,
            "hits": 0,
            "misses": 0,
            "writes": 0,
            "invalidations": 0,
        }

    def _generate_cache_key(self, category: str, identifier: str, *args) -> str:
        """Generate cache key with proper namespacing"""
        prefix = self.key_prefixes.get(category, "tw3:")

        # Create compound key
        key_parts = [prefix + identifier]
        for arg in args:
            if isinstance(arg, dict):
                # Hash dict for consistent keys
                key_parts.append(
                    hashlib.md5(json.dumps(arg, sort_keys=True).encode()).hexdigest()[
                        :8
                    ]
                )
            else:
                key_parts.append(str(arg))

        return ":".join(key_parts)

    async def get_verification_result(
        self, verification_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get cached verification result"""
        cache_key = self._generate_cache_key("verification", verification_id)

        self.cache_metrics["operations"] += 1

        result = await self.redis_manager.get(cache_key)
        if result:
            self.cache_metrics["hits"] += 1
            self.logger.debug(f"Cache hit for verification {verification_id}")
            return result

        self.cache_metrics["misses"] += 1
        return None

    async def cache_verification_result(
        self, verification_id: str, result: Dict[str, Any]
    ) -> bool:
        """Cache verification result"""
        cache_key = self._generate_cache_key("verification", verification_id)
        ttl = self.ttl_configs["verification_results"]

        self.cache_metrics["writes"] += 1

        success = await self.redis_manager.set(cache_key, result, ttl)
        if success:
            self.logger.debug(f"Cached verification result {verification_id}")

        return success

    async def get_oracle_consensus(
        self, asset_pair: str
    ) -> Optional[MultiOracleConsensus]:
        """Get cached oracle consensus"""
        cache_key = self._generate_cache_key("oracle", "consensus", asset_pair)

        self.cache_metrics["operations"] += 1

        result = await self.redis_manager.get(cache_key)
        if result:
            self.cache_metrics["hits"] += 1
            self.logger.debug(f"Cache hit for oracle consensus {asset_pair}")

            # Convert back to MultiOracleConsensus if needed
            if isinstance(result, dict):
                # Reconstruct object from cached dict
                return MultiOracleConsensus(**result)
            return result

        self.cache_metrics["misses"] += 1
        return None

    async def cache_oracle_consensus(
        self, asset_pair: str, consensus: MultiOracleConsensus
    ) -> bool:
        """Cache oracle consensus"""
        cache_key = self._generate_cache_key("oracle", "consensus", asset_pair)
        ttl = self.ttl_configs["oracle_consensus"]

        self.cache_metrics["writes"] += 1

        # Convert to dict for caching
        consensus_data = consensus.to_dict()

        success = await self.redis_manager.set(cache_key, consensus_data, ttl)
        if success:
            self.logger.debug(f"Cached oracle consensus {asset_pair}")

        return success

    async def get_oracle_data(
        self, asset_pair: str, source_id: str
    ) -> Optional[OracleData]:
        """Get cached oracle data"""
        cache_key = self._generate_cache_key("oracle", "data", asset_pair, source_id)

        self.cache_metrics["operations"] += 1

        result = await self.redis_manager.get(cache_key)
        if result:
            self.cache_metrics["hits"] += 1

            # Convert back to OracleData if needed
            if isinstance(result, dict):
                return OracleData(**result)
            return result

        self.cache_metrics["misses"] += 1
        return None

    async def cache_oracle_data(self, oracle_data: OracleData) -> bool:
        """Cache oracle data"""
        cache_key = self._generate_cache_key(
            "oracle", "data", oracle_data.asset_id, oracle_data.source_id
        )
        ttl = self.ttl_configs["oracle_data"]

        self.cache_metrics["writes"] += 1

        # Convert to dict for caching
        data_dict = oracle_data.to_dict()

        success = await self.redis_manager.set(cache_key, data_dict, ttl)
        if success:
            self.logger.debug(
                f"Cached oracle data {oracle_data.asset_id}:{oracle_data.source_id}"
            )

        return success

    async def get_chain_health(self, chain_id: str) -> Optional[Dict[str, Any]]:
        """Get cached chain health"""
        cache_key = self._generate_cache_key("chain", "health", chain_id)

        self.cache_metrics["operations"] += 1

        result = await self.redis_manager.get(cache_key)
        if result:
            self.cache_metrics["hits"] += 1
            return result

        self.cache_metrics["misses"] += 1
        return None

    async def cache_chain_health(
        self, chain_id: str, health_data: Dict[str, Any]
    ) -> bool:
        """Cache chain health data"""
        cache_key = self._generate_cache_key("chain", "health", chain_id)
        ttl = self.ttl_configs["chain_health"]

        self.cache_metrics["writes"] += 1

        success = await self.redis_manager.set(cache_key, health_data, ttl)
        if success:
            self.logger.debug(f"Cached chain health {chain_id}")

        return success

    async def invalidate_oracle_cache(self, asset_pair: Optional[str] = None) -> int:
        """Invalidate oracle cache entries"""
        if asset_pair:
            # Invalidate specific asset pair
            pattern = self._generate_cache_key("oracle", "*", asset_pair)
        else:
            # Invalidate all oracle cache
            pattern = self._generate_cache_key("oracle", "*")

        keys = await self.redis_manager.get_pattern(pattern)

        invalidated = 0
        for key in keys:
            if await self.redis_manager.delete(key):
                invalidated += 1

        self.cache_metrics["invalidations"] += invalidated
        self.logger.info(f"Invalidated {invalidated} oracle cache entries")

        return invalidated

    async def invalidate_verification_cache(
        self, verification_id: Optional[str] = None
    ) -> int:
        """Invalidate verification cache entries"""
        if verification_id:
            cache_key = self._generate_cache_key("verification", verification_id)
            keys = [cache_key]
        else:
            pattern = self._generate_cache_key("verification", "*")
            keys = await self.redis_manager.get_pattern(pattern)

        invalidated = 0
        for key in keys:
            if await self.redis_manager.delete(key):
                invalidated += 1

        self.cache_metrics["invalidations"] += invalidated
        self.logger.info(f"Invalidated {invalidated} verification cache entries")

        return invalidated

    def get_cache_metrics(self) -> Dict[str, Any]:
        """Get cache performance metrics"""
        total_ops = self.cache_metrics["operations"]
        hit_rate = self.cache_metrics["hits"] / total_ops if total_ops > 0 else 0.0

        return {
            **self.cache_metrics,
            "hit_rate": hit_rate,
            "miss_rate": 1.0 - hit_rate,
            "redis_metrics": self.redis_manager.get_metrics(),
        }


class ScalingInfrastructureManager:
    """
    Main scaling infrastructure manager that coordinates Redis caching,
    async task processing, and connection pooling for TrustWrapper v3.0
    """

    def __init__(
        self,
        cache_config: Optional[CacheConfig] = None,
        task_config: Optional[AsyncTaskConfig] = None,
    ):
        self.logger = logging.getLogger(__name__)

        # Configuration
        self.cache_config = cache_config or CacheConfig()
        self.task_config = task_config or AsyncTaskConfig()

        # Core components
        self.redis_manager = None
        self.task_manager = None
        self.cache_layer = None

        # State
        self.initialized = False
        self.performance_monitor_task = None

    async def initialize(self) -> None:
        """Initialize scaling infrastructure"""
        try:
            self.logger.info(
                "🚀 Initializing TrustWrapper v3.0 Scaling Infrastructure..."
            )

            # Initialize Redis connection manager
            self.redis_manager = RedisConnectionManager(self.cache_config)
            await self.redis_manager.initialize()

            # Initialize async task manager
            self.task_manager = AsyncTaskManager(self.task_config)
            await self.task_manager.start()

            # Initialize performance cache layer
            self.cache_layer = PerformanceCacheLayer(self.redis_manager)

            # Start performance monitoring
            self.performance_monitor_task = asyncio.create_task(
                self._monitor_performance()
            )

            self.initialized = True
            self.logger.info("✅ Scaling Infrastructure initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Scaling Infrastructure: {e}")
            raise

    async def _monitor_performance(self) -> None:
        """Background task to monitor performance metrics"""
        while self.initialized:
            try:
                # Collect metrics from all components
                redis_metrics = self.redis_manager.get_metrics()
                task_metrics = self.task_manager.get_metrics()
                cache_metrics = self.cache_layer.get_cache_metrics()

                # Log performance summary
                self.logger.info(
                    f"Performance Metrics - "
                    f"Redis: {redis_metrics['cache_hit_rate']:.1%} hit rate, "
                    f"Tasks: {task_metrics['total_tasks_completed']}/{task_metrics['total_tasks_submitted']} completed, "
                    f"Cache: {cache_metrics['hit_rate']:.1%} hit rate"
                )

                # Cache performance metrics
                await self.cache_layer.redis_manager.set(
                    "tw3:metrics:performance",
                    {
                        "redis": redis_metrics,
                        "tasks": task_metrics,
                        "cache": cache_metrics,
                        "timestamp": time.time(),
                    },
                    ttl=300,
                )

                await asyncio.sleep(60.0)  # Monitor every minute

            except Exception as e:
                self.logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(30.0)

    async def submit_verification_task(
        self,
        verification_id: str,
        verification_coro: Any,
        priority: ProcessingPriority = ProcessingPriority.HIGH,
        callback: Optional[Callable] = None,
    ) -> bool:
        """Submit verification task for async processing"""
        if not self.initialized:
            raise RuntimeError("Scaling infrastructure not initialized")

        return await self.task_manager.submit_task(
            f"verify_{verification_id}", verification_coro, priority, callback
        )

    async def submit_oracle_update_task(
        self,
        asset_pairs: List[str],
        priority: ProcessingPriority = ProcessingPriority.NORMAL,
    ) -> bool:
        """Submit oracle update task for async processing"""
        if not self.initialized:
            raise RuntimeError("Scaling infrastructure not initialized")

        task_id = f"oracle_update_{int(time.time())}"

        # Create oracle update coroutine (would be actual oracle update)
        async def oracle_update_coro():
            # Mock oracle update
            await asyncio.sleep(0.5)
            return f"Updated oracles for {len(asset_pairs)} pairs"

        return await self.task_manager.submit_task(
            task_id, oracle_update_coro(), priority
        )

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        if not self.initialized:
            return {"error": "Infrastructure not initialized"}

        return {
            "infrastructure_status": "operational",
            "redis_metrics": self.redis_manager.get_metrics(),
            "task_metrics": self.task_manager.get_metrics(),
            "cache_metrics": self.cache_layer.get_cache_metrics(),
            "components": {
                "redis_manager": self.redis_manager._connected,
                "task_manager": self.task_manager.running,
                "cache_layer": True,
                "performance_monitor": (
                    not self.performance_monitor_task.done()
                    if self.performance_monitor_task
                    else False
                ),
            },
        }

    async def shutdown(self) -> None:
        """Shutdown scaling infrastructure"""
        self.logger.info("🛑 Shutting down Scaling Infrastructure...")

        self.initialized = False

        # Stop performance monitoring
        if self.performance_monitor_task:
            self.performance_monitor_task.cancel()

        # Shutdown components
        if self.task_manager:
            await self.task_manager.stop()

        if self.redis_manager:
            await self.redis_manager.shutdown()

        self.logger.info("Scaling Infrastructure shutdown complete")


# Singleton instance
_scaling_infrastructure_instance = None


async def get_scaling_infrastructure(
    cache_config: Optional[CacheConfig] = None,
    task_config: Optional[AsyncTaskConfig] = None,
) -> ScalingInfrastructureManager:
    """Get or create the global scaling infrastructure instance"""
    global _scaling_infrastructure_instance

    if _scaling_infrastructure_instance is None:
        _scaling_infrastructure_instance = ScalingInfrastructureManager(
            cache_config, task_config
        )
        await _scaling_infrastructure_instance.initialize()

    return _scaling_infrastructure_instance

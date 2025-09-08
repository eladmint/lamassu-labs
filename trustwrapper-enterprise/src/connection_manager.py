"""
Multi-Chain Connection Manager
=============================

Manages connections and health monitoring across multiple blockchain networks
for the TrustWrapper v3.0 universal verification platform.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.interfaces import ChainConfig, ChainType, IUniversalChainAdapter


@dataclass
class ConnectionHealth:
    """Health status for a blockchain connection."""

    chain_type: ChainType
    is_connected: bool
    last_successful_request: datetime
    consecutive_failures: int
    average_response_time: float
    error_rate: float
    last_error: str | None = None


@dataclass
class ConnectionPool:
    """Pool of blockchain connections with health monitoring."""

    adapters: dict[ChainType, IUniversalChainAdapter] = field(default_factory=dict)
    health_status: dict[ChainType, ConnectionHealth] = field(default_factory=dict)
    configs: dict[ChainType, ChainConfig] = field(default_factory=dict)


class MultiChainConnectionManager:
    """
    Manages connections to multiple blockchain networks with health monitoring,
    automatic reconnection, and load balancing capabilities.
    """

    def __init__(
        self,
        health_check_interval: int = 30,
        max_retry_attempts: int = 3,
        connection_timeout: int = 10,
    ):
        self.health_check_interval = health_check_interval
        self.max_retry_attempts = max_retry_attempts
        self.connection_timeout = connection_timeout

        self.connection_pool = ConnectionPool()
        self.logger = logging.getLogger(__name__)
        self._health_monitor_task: asyncio.Task | None = None
        self._shutdown_event = asyncio.Event()

    async def add_chain_adapter(
        self, adapter: IUniversalChainAdapter, config: ChainConfig
    ) -> bool:
        """
        Add a blockchain adapter to the connection pool.

        Args:
            adapter: Chain adapter implementation
            config: Chain configuration

        Returns:
            bool: True if added successfully
        """
        try:
            chain_type = adapter.chain_type

            # Store adapter and config
            self.connection_pool.adapters[chain_type] = adapter
            self.connection_pool.configs[chain_type] = config

            # Initialize health status
            self.connection_pool.health_status[chain_type] = ConnectionHealth(
                chain_type=chain_type,
                is_connected=False,
                last_successful_request=datetime.utcnow(),
                consecutive_failures=0,
                average_response_time=0.0,
                error_rate=0.0,
            )

            # Attempt initial connection
            connected = await self._connect_with_retry(adapter)

            if connected:
                self.logger.info(f"Successfully added {chain_type.value} adapter")
                return True
            else:
                self.logger.warning(
                    f"Added {chain_type.value} adapter but connection failed"
                )
                return False

        except Exception as e:
            self.logger.error(f"Failed to add adapter for {chain_type.value}: {e}")
            return False

    async def remove_chain_adapter(self, chain_type: ChainType) -> bool:
        """
        Remove a blockchain adapter from the connection pool.

        Args:
            chain_type: Type of chain to remove

        Returns:
            bool: True if removed successfully
        """
        try:
            if chain_type in self.connection_pool.adapters:
                adapter = self.connection_pool.adapters[chain_type]
                await adapter.disconnect()

                del self.connection_pool.adapters[chain_type]
                del self.connection_pool.health_status[chain_type]
                del self.connection_pool.configs[chain_type]

                self.logger.info(f"Removed {chain_type.value} adapter")
                return True
            else:
                self.logger.warning(f"Adapter for {chain_type.value} not found")
                return False

        except Exception as e:
            self.logger.error(f"Failed to remove adapter for {chain_type.value}: {e}")
            return False

    async def get_healthy_adapters(self) -> list[IUniversalChainAdapter]:
        """
        Get list of currently healthy blockchain adapters.

        Returns:
            List[IUniversalChainAdapter]: List of healthy adapters
        """
        healthy_adapters = []

        for chain_type, health in self.connection_pool.health_status.items():
            if health.is_connected and health.consecutive_failures < 3:
                adapter = self.connection_pool.adapters.get(chain_type)
                if adapter:
                    healthy_adapters.append(adapter)

        return healthy_adapters

    async def get_adapter(self, chain_type: ChainType) -> IUniversalChainAdapter | None:
        """
        Get adapter for specific chain type.

        Args:
            chain_type: Target chain type

        Returns:
            Optional[IUniversalChainAdapter]: Adapter if available and healthy
        """
        if chain_type not in self.connection_pool.adapters:
            return None

        health = self.connection_pool.health_status[chain_type]
        if (
            health.is_connected
            and health.consecutive_failures < self.max_retry_attempts
        ):
            return self.connection_pool.adapters[chain_type]

        return None

    async def get_connection_status(self) -> dict[ChainType, ConnectionHealth]:
        """
        Get health status for all connections.

        Returns:
            Dict[ChainType, ConnectionHealth]: Current health status
        """
        return dict(self.connection_pool.health_status)

    async def start_health_monitoring(self) -> None:
        """Start background health monitoring for all connections."""
        if self._health_monitor_task is None or self._health_monitor_task.done():
            self._health_monitor_task = asyncio.create_task(self._health_monitor_loop())
            self.logger.info("Started connection health monitoring")

    async def stop_health_monitoring(self) -> None:
        """Stop background health monitoring."""
        self._shutdown_event.set()

        if self._health_monitor_task and not self._health_monitor_task.done():
            await self._health_monitor_task

        self.logger.info("Stopped connection health monitoring")

    async def disconnect_all(self) -> None:
        """Disconnect all blockchain adapters."""
        await self.stop_health_monitoring()

        for chain_type, adapter in self.connection_pool.adapters.items():
            try:
                await adapter.disconnect()
                self.logger.info(f"Disconnected from {chain_type.value}")
            except Exception as e:
                self.logger.error(f"Error disconnecting from {chain_type.value}: {e}")

        self.connection_pool.adapters.clear()
        self.connection_pool.health_status.clear()
        self.connection_pool.configs.clear()

    async def _connect_with_retry(self, adapter: IUniversalChainAdapter) -> bool:
        """
        Attempt to connect to blockchain with retry logic.

        Args:
            adapter: Chain adapter to connect

        Returns:
            bool: True if connection successful
        """
        chain_type = adapter.chain_type

        for attempt in range(self.max_retry_attempts):
            try:
                connected = await asyncio.wait_for(
                    adapter.connect(), timeout=self.connection_timeout
                )

                if connected:
                    # Update health status
                    health = self.connection_pool.health_status[chain_type]
                    health.is_connected = True
                    health.consecutive_failures = 0
                    health.last_successful_request = datetime.utcnow()

                    return True

            except TimeoutError:
                self.logger.warning(
                    f"Connection timeout for {chain_type.value} "
                    f"(attempt {attempt + 1}/{self.max_retry_attempts})"
                )
            except Exception as e:
                self.logger.error(
                    f"Connection error for {chain_type.value}: {e} "
                    f"(attempt {attempt + 1}/{self.max_retry_attempts})"
                )

            # Update failure count
            health = self.connection_pool.health_status[chain_type]
            health.consecutive_failures += 1
            health.last_error = str(e) if "e" in locals() else "Connection timeout"

            # Wait before retry (exponential backoff)
            if attempt < self.max_retry_attempts - 1:
                await asyncio.sleep(2**attempt)

        # All attempts failed
        health = self.connection_pool.health_status[chain_type]
        health.is_connected = False

        return False

    async def _health_monitor_loop(self) -> None:
        """Background loop for monitoring connection health."""
        while not self._shutdown_event.is_set():
            try:
                await self._check_all_connections()
                await asyncio.sleep(self.health_check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in health monitor loop: {e}")
                await asyncio.sleep(5)  # Brief pause before retrying

    async def _check_all_connections(self) -> None:
        """Check health of all blockchain connections."""
        tasks = []

        for chain_type, adapter in self.connection_pool.adapters.items():
            task = asyncio.create_task(
                self._check_single_connection(chain_type, adapter)
            )
            tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _check_single_connection(
        self, chain_type: ChainType, adapter: IUniversalChainAdapter
    ) -> None:
        """
        Check health of a single blockchain connection.

        Args:
            chain_type: Chain type being checked
            adapter: Chain adapter to check
        """
        health = self.connection_pool.health_status[chain_type]
        start_time = datetime.utcnow()

        try:
            # Simple health check - get chain metrics
            metrics = await asyncio.wait_for(
                adapter.get_chain_metrics(), timeout=self.connection_timeout
            )

            # Calculate response time
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000

            # Update health status - success
            health.is_connected = True
            health.consecutive_failures = 0
            health.last_successful_request = datetime.utcnow()
            health.average_response_time = (
                health.average_response_time * 0.9 + response_time * 0.1
            )
            health.last_error = None

        except Exception as e:
            # Update health status - failure
            health.consecutive_failures += 1
            health.last_error = str(e)

            # If too many failures, mark as disconnected
            if health.consecutive_failures >= self.max_retry_attempts:
                health.is_connected = False

                # Attempt reconnection
                self.logger.warning(
                    f"Attempting to reconnect to {chain_type.value} "
                    f"after {health.consecutive_failures} failures"
                )

                await self._connect_with_retry(adapter)

    def get_performance_stats(self) -> dict[str, Any]:
        """
        Get performance statistics for all connections.

        Returns:
            Dict: Performance statistics
        """
        stats = {
            "total_adapters": len(self.connection_pool.adapters),
            "healthy_adapters": 0,
            "unhealthy_adapters": 0,
            "average_response_time": 0.0,
            "chain_details": {},
        }

        total_response_time = 0.0
        healthy_count = 0

        for chain_type, health in self.connection_pool.health_status.items():
            if health.is_connected and health.consecutive_failures < 3:
                stats["healthy_adapters"] += 1
                healthy_count += 1
                total_response_time += health.average_response_time
            else:
                stats["unhealthy_adapters"] += 1

            stats["chain_details"][chain_type.value] = {
                "is_connected": health.is_connected,
                "consecutive_failures": health.consecutive_failures,
                "average_response_time": health.average_response_time,
                "error_rate": health.error_rate,
                "last_error": health.last_error,
            }

        if healthy_count > 0:
            stats["average_response_time"] = total_response_time / healthy_count

        return stats

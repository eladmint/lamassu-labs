"""
Cross-Chain Message Broker
==========================

Core message passing implementation for TrustWrapper v3.0 cross-chain bridge.
Handles message routing, queuing, delivery confirmation, and error recovery.
"""

import asyncio
import logging
import uuid
from datetime import datetime

from bridge.interfaces import (
    BridgeMessage,
    BridgeMessageStatus,
    BridgeMessageType,
    BridgeRoute,
    IBridgeAdapter,
)
from core.interfaces import ChainType


class MessageQueue:
    """Thread-safe message queue for cross-chain operations."""

    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self._queue = asyncio.Queue(maxsize=max_size)
        self._pending = {}  # message_id -> BridgeMessage
        self._processing = set()  # Set of message_ids being processed
        self.logger = logging.getLogger(f"{__name__}.queue")

    async def enqueue(self, message: BridgeMessage) -> bool:
        """
        Add message to queue.

        Args:
            message: Message to enqueue

        Returns:
            bool: True if enqueued successfully
        """
        try:
            if self._queue.full():
                self.logger.warning(
                    f"Message queue full, dropping message {message.message_id}"
                )
                return False

            await self._queue.put(message)
            self._pending[message.message_id] = message

            self.logger.debug(
                f"Enqueued message {message.message_id} ({message.message_type.value})"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to enqueue message {message.message_id}: {e}")
            return False

    async def dequeue(self, timeout: float | None = None) -> BridgeMessage | None:
        """
        Get next message from queue.

        Args:
            timeout: Maximum time to wait for message

        Returns:
            BridgeMessage: Next message or None if timeout
        """
        try:
            message = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            self._processing.add(message.message_id)
            return message

        except TimeoutError:
            return None
        except Exception as e:
            self.logger.error(f"Failed to dequeue message: {e}")
            return None

    async def mark_completed(self, message_id: str, success: bool) -> None:
        """
        Mark message as completed.

        Args:
            message_id: Message identifier
            success: Whether processing was successful
        """
        self._processing.discard(message_id)

        if message_id in self._pending:
            message = self._pending[message_id]
            if success:
                message.status = BridgeMessageStatus.CONFIRMED
            else:
                message.status = BridgeMessageStatus.FAILED

            # Remove from pending after processing
            del self._pending[message_id]

    def get_pending_count(self) -> int:
        """Get number of pending messages."""
        return len(self._pending)

    def get_processing_count(self) -> int:
        """Get number of messages being processed."""
        return len(self._processing)

    def get_queue_size(self) -> int:
        """Get current queue size."""
        return self._queue.qsize()


class CrossChainMessageBroker:
    """
    Cross-chain message broker for TrustWrapper v3.0.

    Handles message routing, delivery, confirmation, and error recovery
    across multiple blockchain networks.
    """

    def __init__(self, max_queue_size: int = 10000):
        self.message_queue = MessageQueue(max_queue_size)
        self.adapters: dict[ChainType, IBridgeAdapter] = {}
        self.routes: dict[str, BridgeRoute] = {}
        self.active_messages: dict[str, BridgeMessage] = {}

        # Configuration
        self.retry_delays = [1, 5, 15, 60]  # Exponential backoff in seconds
        self.message_timeout = 300  # 5 minutes default timeout
        self.health_check_interval = 30  # 30 seconds

        # State tracking
        self._running = False
        self._worker_tasks = []
        self._health_check_task = None

        self.logger = logging.getLogger(f"{__name__}.broker")

        # Message statistics
        self._stats = {
            "total_messages": 0,
            "successful_messages": 0,
            "failed_messages": 0,
            "retry_attempts": 0,
            "timeouts": 0,
        }

    async def initialize(
        self, adapters: dict[ChainType, IBridgeAdapter], routes: list[BridgeRoute]
    ) -> bool:
        """
        Initialize the message broker.

        Args:
            adapters: Chain-specific bridge adapters
            routes: Available bridge routes

        Returns:
            bool: True if initialization successful
        """
        try:
            self.adapters = adapters

            # Register routes
            for route in routes:
                route_id = f"{route.source_chain.value}_{route.target_chain.value}"
                self.routes[route_id] = route

            self.logger.info(
                f"Initialized message broker with {len(adapters)} adapters and {len(routes)} routes"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize message broker: {e}")
            return False

    async def start(self) -> None:
        """Start the message broker background tasks."""
        if self._running:
            return

        self._running = True

        # Start message processing workers
        num_workers = min(5, len(self.adapters))
        for i in range(num_workers):
            task = asyncio.create_task(self._message_worker(f"worker-{i}"))
            self._worker_tasks.append(task)

        # Start health check task
        self._health_check_task = asyncio.create_task(self._health_check_loop())

        self.logger.info(f"Started message broker with {num_workers} workers")

    async def stop(self) -> None:
        """Stop the message broker and cleanup resources."""
        if not self._running:
            return

        self._running = False

        # Cancel worker tasks
        for task in self._worker_tasks:
            task.cancel()

        if self._health_check_task:
            self._health_check_task.cancel()

        # Wait for tasks to complete
        await asyncio.gather(
            *self._worker_tasks, self._health_check_task, return_exceptions=True
        )

        self._worker_tasks.clear()
        self._health_check_task = None

        self.logger.info("Stopped message broker")

    async def send_message(
        self,
        message_type: BridgeMessageType,
        source_chain: ChainType,
        target_chain: ChainType,
        payload: dict[str, any],
        priority: int = 0,
        timeout_seconds: int = None,
    ) -> str:
        """
        Send a cross-chain message.

        Args:
            message_type: Type of message
            source_chain: Source blockchain
            target_chain: Target blockchain
            payload: Message payload
            priority: Message priority (higher = more urgent)
            timeout_seconds: Message timeout

        Returns:
            str: Message identifier
        """
        # Create message
        message_id = str(uuid.uuid4())
        message = BridgeMessage(
            message_id=message_id,
            message_type=message_type,
            source_chain=source_chain,
            target_chain=target_chain,
            payload=payload,
            timestamp=datetime.utcnow(),
            timeout_seconds=timeout_seconds or self.message_timeout,
            priority=priority,
        )

        # Validate route exists
        route_id = f"{source_chain.value}_{target_chain.value}"
        if route_id not in self.routes:
            raise ValueError(
                f"No route available from {source_chain.value} to {target_chain.value}"
            )

        route = self.routes[route_id]
        if not route.is_active:
            raise ValueError(f"Route {route_id} is not active")

        # Add to queue
        success = await self.message_queue.enqueue(message)
        if not success:
            raise RuntimeError(f"Failed to enqueue message {message_id}")

        self.active_messages[message_id] = message
        self._stats["total_messages"] += 1

        self.logger.info(
            f"Queued message {message_id} from {source_chain.value} to {target_chain.value}"
        )
        return message_id

    async def get_message_status(self, message_id: str) -> BridgeMessageStatus | None:
        """
        Get the status of a message.

        Args:
            message_id: Message identifier

        Returns:
            BridgeMessageStatus: Message status or None if not found
        """
        if message_id in self.active_messages:
            return self.active_messages[message_id].status
        return None

    async def get_broker_stats(self) -> dict[str, any]:
        """
        Get message broker statistics.

        Returns:
            Dict: Broker statistics and metrics
        """
        return {
            **self._stats,
            "queue_size": self.message_queue.get_queue_size(),
            "pending_messages": self.message_queue.get_pending_count(),
            "processing_messages": self.message_queue.get_processing_count(),
            "active_messages": len(self.active_messages),
            "active_routes": len([r for r in self.routes.values() if r.is_active]),
            "total_routes": len(self.routes),
            "success_rate": (
                self._stats["successful_messages"]
                / max(self._stats["total_messages"], 1)
            ),
        }

    async def _message_worker(self, worker_id: str) -> None:
        """
        Message processing worker.

        Args:
            worker_id: Worker identifier
        """
        self.logger.info(f"Started message worker {worker_id}")

        while self._running:
            try:
                # Get next message from queue
                message = await self.message_queue.dequeue(timeout=1.0)
                if message is None:
                    continue

                # Check if message has expired
                if self._is_message_expired(message):
                    await self._handle_message_timeout(message)
                    continue

                # Process the message
                success = await self._process_message(message)

                # Mark as completed
                await self.message_queue.mark_completed(message.message_id, success)

                # Update statistics
                if success:
                    self._stats["successful_messages"] += 1
                else:
                    self._stats["failed_messages"] += 1

            except Exception as e:
                self.logger.error(f"Error in message worker {worker_id}: {e}")
                await asyncio.sleep(1)

        self.logger.info(f"Stopped message worker {worker_id}")

    async def _process_message(self, message: BridgeMessage) -> bool:
        """
        Process a single message.

        Args:
            message: Message to process

        Returns:
            bool: True if processing successful
        """
        try:
            # Get appropriate adapter
            adapter = self.adapters.get(message.target_chain)
            if not adapter:
                self.logger.error(
                    f"No adapter for target chain {message.target_chain.value}"
                )
                return False

            # Update message status
            message.status = BridgeMessageStatus.TRANSMITTED

            # Transmit message
            success = await adapter.transmit_message(message)

            if success:
                # Confirm delivery
                confirmed = await adapter.confirm_message_delivery(
                    message.message_id, message.target_chain
                )

                if confirmed:
                    message.status = BridgeMessageStatus.CONFIRMED
                    self.logger.info(
                        f"Message {message.message_id} delivered successfully"
                    )
                    return True
                else:
                    self.logger.warning(
                        f"Message {message.message_id} transmitted but not confirmed"
                    )
                    return await self._retry_message(message)
            else:
                self.logger.warning(f"Failed to transmit message {message.message_id}")
                return await self._retry_message(message)

        except Exception as e:
            self.logger.error(f"Error processing message {message.message_id}: {e}")
            message.error_message = str(e)
            return await self._retry_message(message)

    async def _retry_message(self, message: BridgeMessage) -> bool:
        """
        Retry a failed message.

        Args:
            message: Message to retry

        Returns:
            bool: True if retry was scheduled
        """
        if message.retry_count >= message.max_retries:
            message.status = BridgeMessageStatus.FAILED
            self.logger.error(f"Message {message.message_id} exceeded max retries")
            return False

        # Calculate retry delay
        delay_index = min(message.retry_count, len(self.retry_delays) - 1)
        delay = self.retry_delays[delay_index]

        message.retry_count += 1
        self._stats["retry_attempts"] += 1

        self.logger.info(
            f"Retrying message {message.message_id} in {delay} seconds (attempt {message.retry_count})"
        )

        # Schedule retry
        asyncio.create_task(self._schedule_retry(message, delay))
        return True

    async def _schedule_retry(self, message: BridgeMessage, delay: float) -> None:
        """
        Schedule a message retry after delay.

        Args:
            message: Message to retry
            delay: Delay in seconds
        """
        await asyncio.sleep(delay)

        if self._running and message.message_id in self.active_messages:
            await self.message_queue.enqueue(message)

    def _is_message_expired(self, message: BridgeMessage) -> bool:
        """
        Check if a message has expired.

        Args:
            message: Message to check

        Returns:
            bool: True if expired
        """
        elapsed = (datetime.utcnow() - message.timestamp).total_seconds()
        return elapsed > message.timeout_seconds

    async def _handle_message_timeout(self, message: BridgeMessage) -> None:
        """
        Handle a timed-out message.

        Args:
            message: Timed-out message
        """
        message.status = BridgeMessageStatus.TIMEOUT
        self._stats["timeouts"] += 1

        self.logger.warning(
            f"Message {message.message_id} timed out after {message.timeout_seconds} seconds"
        )

        # Remove from active messages
        if message.message_id in self.active_messages:
            del self.active_messages[message.message_id]

    async def _health_check_loop(self) -> None:
        """Background task for health checking bridge routes."""
        self.logger.info("Started bridge health check loop")

        while self._running:
            try:
                # Check each route
                for route_id, route in self.routes.items():
                    if route.is_active:
                        await self._check_route_health(route)

                await asyncio.sleep(self.health_check_interval)

            except Exception as e:
                self.logger.error(f"Error in health check loop: {e}")
                await asyncio.sleep(5)

        self.logger.info("Stopped bridge health check loop")

    async def _check_route_health(self, route: BridgeRoute) -> None:
        """
        Check health of a specific route.

        Args:
            route: Route to check
        """
        try:
            adapter = self.adapters.get(route.target_chain)
            if not adapter or not adapter.is_operational:
                route.is_active = False
                route.health_score = 0.0
                self.logger.warning(
                    f"Route {route.source_chain.value} -> {route.target_chain.value} marked inactive"
                )
                return

            # Update health metrics
            route.last_health_check = datetime.utcnow()

            # For now, assume healthy if adapter is operational
            # In production, this would include latency tests, throughput checks, etc.
            route.health_score = 0.95
            route.is_active = True

        except Exception as e:
            route.is_active = False
            route.health_score = 0.0
            self.logger.error(
                f"Health check failed for route {route.source_chain.value} -> {route.target_chain.value}: {e}"
            )

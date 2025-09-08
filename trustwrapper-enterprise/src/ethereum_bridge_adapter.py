"""
Ethereum Bridge Adapter
=======================

Bridge adapter implementation for Ethereum-based networks
(Ethereum, Polygon, Arbitrum) for TrustWrapper v3.0 cross-chain bridge.
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Any

from adapters.ethereum_adapter import EthereumAdapter
from bridge.interfaces import (
    BridgeMessage,
    BridgeMessageStatus,
    BridgeMetrics,
    IBridgeAdapter,
)
from core.interfaces import ChainType


class EthereumBridgeAdapter(IBridgeAdapter):
    """
    Bridge adapter for Ethereum-based networks.

    Handles cross-chain message transmission, verification, and metrics
    for Ethereum, Polygon, and Arbitrum networks.
    """

    def __init__(self, ethereum_adapter: EthereumAdapter):
        self.ethereum_adapter = ethereum_adapter
        self.supported_chains_list = [ChainType.ETHEREUM, ChainType.POLYGON]

        # Message storage (in production, this would be persistent storage)
        self.outbound_messages: dict[str, BridgeMessage] = {}
        self.inbound_messages: dict[str, BridgeMessage] = {}
        self.delivery_confirmations: dict[str, bool] = {}

        # Configuration
        self.confirmation_blocks = 12  # Number of blocks for confirmation
        self.gas_limit = 500000
        self.max_retry_attempts = 3

        self.logger = logging.getLogger(f"{__name__}.eth_bridge")

        # Metrics tracking
        self._metrics = {
            "total_transmitted": 0,
            "successful_transmissions": 0,
            "failed_transmissions": 0,
            "total_received": 0,
            "average_latency_ms": 0.0,
            "total_gas_used": 0,
        }

    @property
    def supported_chains(self) -> list[ChainType]:
        """Return list of blockchain types this adapter supports."""
        return self.supported_chains_list.copy()

    @property
    def is_operational(self) -> bool:
        """Check if the bridge adapter is operational."""
        return self.ethereum_adapter.is_connected

    async def initialize(self, config: dict[str, Any]) -> bool:
        """
        Initialize the bridge adapter with configuration.

        Args:
            config: Adapter-specific configuration

        Returns:
            bool: True if initialization successful
        """
        try:
            # Update configuration from provided config
            self.confirmation_blocks = config.get(
                "confirmation_blocks", self.confirmation_blocks
            )
            self.gas_limit = config.get("gas_limit", self.gas_limit)
            self.max_retry_attempts = config.get(
                "max_retry_attempts", self.max_retry_attempts
            )

            # Ensure underlying adapter is connected
            if not self.ethereum_adapter.is_connected:
                await self.ethereum_adapter.connect()

            self.logger.info(
                f"Initialized Ethereum bridge adapter for {self.ethereum_adapter.chain_type.value}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Ethereum bridge adapter: {e}")
            return False

    async def transmit_message(self, message: BridgeMessage) -> bool:
        """
        Transmit a message to the target blockchain.

        Args:
            message: Bridge message to transmit

        Returns:
            bool: True if transmission successful
        """
        if not self.is_operational:
            self.logger.error("Bridge adapter not operational")
            return False

        try:
            start_time = datetime.utcnow()

            # Store message for tracking
            self.outbound_messages[message.message_id] = message

            # Create transaction data for the message
            tx_data = self._encode_bridge_message(message)

            # For Phase 1, simulate transaction submission
            # In production, this would submit to the actual blockchain
            tx_hash = self._simulate_transaction_submission(tx_data)

            # Update message status
            message.status = BridgeMessageStatus.TRANSMITTED

            # Calculate latency
            latency_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

            # Update metrics
            self._metrics["total_transmitted"] += 1
            self._metrics["successful_transmissions"] += 1
            self._update_average_latency(latency_ms)

            self.logger.info(
                f"Transmitted message {message.message_id} with tx hash {tx_hash}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to transmit message {message.message_id}: {e}")
            self._metrics["total_transmitted"] += 1
            self._metrics["failed_transmissions"] += 1
            message.status = BridgeMessageStatus.FAILED
            message.error_message = str(e)
            return False

    async def receive_messages(
        self, chain_type: ChainType, timeout_seconds: int = 30
    ) -> list[BridgeMessage]:
        """
        Receive pending messages from a blockchain.

        Args:
            chain_type: Source blockchain to check for messages
            timeout_seconds: Maximum time to wait for messages

        Returns:
            List[BridgeMessage]: Received messages
        """
        if not self.is_operational:
            return []

        try:
            # For Phase 1, simulate message reception
            # In production, this would query the blockchain for bridge events

            received_messages = []

            # Simulate receiving messages (would be from blockchain events)
            simulated_messages = self._simulate_receive_messages(chain_type)

            for message in simulated_messages:
                self.inbound_messages[message.message_id] = message
                received_messages.append(message)
                self._metrics["total_received"] += 1

            if received_messages:
                self.logger.info(
                    f"Received {len(received_messages)} messages from {chain_type.value}"
                )

            return received_messages

        except Exception as e:
            self.logger.error(
                f"Failed to receive messages from {chain_type.value}: {e}"
            )
            return []

    async def confirm_message_delivery(
        self, message_id: str, target_chain: ChainType
    ) -> bool:
        """
        Confirm that a message was successfully delivered.

        Args:
            message_id: Message identifier
            target_chain: Target blockchain

        Returns:
            bool: True if delivery confirmed
        """
        if not self.is_operational:
            return False

        try:
            # Check if we have a confirmation for this message
            if message_id in self.delivery_confirmations:
                return self.delivery_confirmations[message_id]

            # For Phase 1, simulate confirmation check
            # In production, this would check transaction confirmations on the blockchain
            confirmed = await self._check_transaction_confirmation(
                message_id, target_chain
            )

            # Cache the confirmation result
            self.delivery_confirmations[message_id] = confirmed

            if confirmed:
                self.logger.debug(
                    f"Confirmed delivery of message {message_id} to {target_chain.value}"
                )
            else:
                self.logger.warning(
                    f"Message {message_id} delivery not yet confirmed on {target_chain.value}"
                )

            return confirmed

        except Exception as e:
            self.logger.error(
                f"Failed to confirm delivery of message {message_id}: {e}"
            )
            return False

    async def get_bridge_metrics(
        self, source_chain: ChainType, target_chain: ChainType
    ) -> BridgeMetrics:
        """
        Get performance metrics for a bridge route.

        Args:
            source_chain: Source blockchain
            target_chain: Target blockchain

        Returns:
            BridgeMetrics: Performance metrics
        """
        route_id = f"{source_chain.value}_{target_chain.value}"

        # Calculate success rate
        total_transmitted = self._metrics["total_transmitted"]
        successful_transmitted = self._metrics["successful_transmissions"]

        error_rate = 0.0
        if total_transmitted > 0:
            error_rate = 1.0 - (successful_transmitted / total_transmitted)

        # Calculate throughput (simplified for Phase 1)
        throughput = 10.0  # Simulated 10 messages per second

        # Calculate uptime (simplified for Phase 1)
        uptime_percentage = 99.5 if self.is_operational else 0.0

        # Calculate health score
        health_score = self._calculate_health_score(error_rate, uptime_percentage)

        return BridgeMetrics(
            route_id=route_id,
            total_messages=total_transmitted,
            successful_messages=successful_transmitted,
            failed_messages=self._metrics["failed_transmissions"],
            average_latency_ms=self._metrics["average_latency_ms"],
            throughput_msg_per_sec=throughput,
            error_rate=error_rate,
            uptime_percentage=uptime_percentage,
            last_message_timestamp=datetime.utcnow() if total_transmitted > 0 else None,
            health_score=health_score,
        )

    def _encode_bridge_message(self, message: BridgeMessage) -> bytes:
        """
        Encode a bridge message for blockchain transmission.

        Args:
            message: Message to encode

        Returns:
            bytes: Encoded message data
        """
        # Create a deterministic encoding of the message
        message_data = {
            "message_id": message.message_id,
            "message_type": message.message_type.value,
            "source_chain": message.source_chain.value,
            "target_chain": message.target_chain.value,
            "payload": message.payload,
            "timestamp": message.timestamp.isoformat(),
            "timeout_seconds": message.timeout_seconds,
            "priority": message.priority,
        }

        # Convert to JSON and encode
        json_data = json.dumps(message_data, sort_keys=True)
        return json_data.encode("utf-8")

    def _simulate_transaction_submission(self, tx_data: bytes) -> str:
        """
        Simulate submitting a transaction to the blockchain.

        Args:
            tx_data: Transaction data

        Returns:
            str: Simulated transaction hash
        """
        # Create a deterministic transaction hash
        hash_input = tx_data + str(datetime.utcnow().timestamp()).encode()
        tx_hash = hashlib.sha256(hash_input).hexdigest()

        # Add chain-specific prefix
        if self.ethereum_adapter.chain_type == ChainType.ETHEREUM:
            return f"eth_tx_{tx_hash[:40]}"
        elif self.ethereum_adapter.chain_type == ChainType.POLYGON:
            return f"poly_tx_{tx_hash[:40]}"
        else:
            return f"evm_tx_{tx_hash[:40]}"

    def _simulate_receive_messages(self, chain_type: ChainType) -> list[BridgeMessage]:
        """
        Simulate receiving messages from the blockchain.

        Args:
            chain_type: Source chain type

        Returns:
            List[BridgeMessage]: Simulated received messages
        """
        # For Phase 1, return empty list (no pending messages)
        # In production, this would query blockchain events
        return []

    async def _check_transaction_confirmation(
        self, message_id: str, target_chain: ChainType
    ) -> bool:
        """
        Check if a transaction has sufficient confirmations.

        Args:
            message_id: Message identifier
            target_chain: Target blockchain

        Returns:
            bool: True if sufficiently confirmed
        """
        # For Phase 1, simulate confirmation after a short delay
        # In production, this would check actual blockchain confirmations

        if message_id in self.outbound_messages:
            message = self.outbound_messages[message_id]

            # Simulate confirmation after 30 seconds
            elapsed = (datetime.utcnow() - message.timestamp).total_seconds()
            return elapsed > 30

        return False

    def _update_average_latency(self, new_latency_ms: float) -> None:
        """
        Update the running average latency.

        Args:
            new_latency_ms: New latency measurement
        """
        total_messages = self._metrics["total_transmitted"]
        current_average = self._metrics["average_latency_ms"]

        if total_messages <= 1:
            self._metrics["average_latency_ms"] = new_latency_ms
        else:
            # Calculate running average
            total_latency = current_average * (total_messages - 1) + new_latency_ms
            self._metrics["average_latency_ms"] = total_latency / total_messages

    def _calculate_health_score(
        self, error_rate: float, uptime_percentage: float
    ) -> float:
        """
        Calculate health score based on metrics.

        Args:
            error_rate: Current error rate
            uptime_percentage: Current uptime percentage

        Returns:
            float: Health score (0.0 to 1.0)
        """
        # Start with perfect score
        score = 1.0

        # Reduce score based on error rate
        if error_rate > 0.15:  # 15% error rate
            score *= 0.3
        elif error_rate > 0.05:  # 5% error rate
            score *= 0.7
        elif error_rate > 0.01:  # 1% error rate
            score *= 0.9

        # Reduce score based on uptime
        score *= uptime_percentage / 100.0

        # Factor in adapter operational status
        if not self.is_operational:
            score = 0.0

        return max(0.0, min(1.0, score))

    def get_adapter_stats(self) -> dict[str, any]:
        """
        Get adapter statistics.

        Returns:
            Dict: Adapter statistics
        """
        return {
            "chain_type": self.ethereum_adapter.chain_type.value,
            "is_operational": self.is_operational,
            "supported_chains": [chain.value for chain in self.supported_chains],
            "outbound_messages": len(self.outbound_messages),
            "inbound_messages": len(self.inbound_messages),
            "pending_confirmations": len(
                [
                    msg_id
                    for msg_id, confirmed in self.delivery_confirmations.items()
                    if not confirmed
                ]
            ),
            **self._metrics,
        }

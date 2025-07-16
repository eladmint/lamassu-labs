"""
Aleo blockchain client for interacting with the network
Handles transactions, program deployment, and state queries
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class AleoTransaction:
    """Represents an Aleo transaction"""

    transaction_id: str
    status: str
    block_height: Optional[int] = None
    timestamp: Optional[datetime] = None
    fee: Optional[int] = None
    transitions: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "transaction_id": self.transaction_id,
            "status": self.status,
            "block_height": self.block_height,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "fee": self.fee,
            "transitions": self.transitions,
        }


class AleoClient:
    """
    Client for interacting with Aleo blockchain
    Handles RPC calls, transaction submission, and network queries
    """

    # Default endpoints
    MAINNET_URL = "https://api.aleo.org/v1"
    TESTNET_URL = "https://api.testnet3.aleo.org/v1"

    def __init__(
        self,
        network: str = "testnet",
        endpoint: Optional[str] = None,
        private_key: Optional[str] = None,
    ):
        """
        Initialize Aleo client

        Args:
            network: 'mainnet' or 'testnet'
            endpoint: Custom RPC endpoint (optional)
            private_key: Private key for transaction signing (optional)
        """
        self.network = network
        self.endpoint = endpoint or (
            self.MAINNET_URL if network == "mainnet" else self.TESTNET_URL
        )
        self.private_key = private_key
        self._session: Optional[aiohttp.ClientSession] = None
        self._connected = False

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()

    async def connect(self):
        """Connect to Aleo network"""
        if not self._session:
            self._session = aiohttp.ClientSession()

        # Test connection
        try:
            await self._call_rpc("getBlockHeight")
            self._connected = True
            logger.info(f"Connected to Aleo {self.network}")
        except Exception as e:
            logger.error(f"Failed to connect to Aleo: {e}")
            self._connected = False
            raise

    async def disconnect(self):
        """Disconnect from Aleo network"""
        if self._session:
            await self._session.close()
            self._session = None
        self._connected = False

    def is_connected(self) -> bool:
        """Check if client is connected"""
        return self._connected

    async def _call_rpc(self, method: str, params: Optional[List[Any]] = None) -> Any:
        """
        Make RPC call to Aleo node

        Args:
            method: RPC method name
            params: Method parameters

        Returns:
            RPC response data
        """
        if not self._session:
            await self.connect()

        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}

        try:
            async with self._session.post(
                f"{self.endpoint}/rpc",
                json=payload,
                headers={"Content-Type": "application/json"},
            ) as response:
                data = await response.json()

                if "error" in data:
                    raise Exception(f"RPC error: {data['error']}")

                return data.get("result")

        except Exception as e:
            logger.error(f"RPC call failed: {e}")
            raise

    async def get_block_height(self) -> int:
        """Get current block height"""
        result = await self._call_rpc("getBlockHeight")
        return int(result)

    async def get_program(self, program_id: str) -> Optional[Dict[str, Any]]:
        """
        Get program details

        Args:
            program_id: Aleo program ID

        Returns:
            Program details or None if not found
        """
        try:
            result = await self._call_rpc("getProgram", [program_id])
            return result
        except Exception as e:
            logger.error(f"Failed to get program {program_id}: {e}")
            return None

    async def submit_transaction(
        self, transaction_data: Dict[str, Any]
    ) -> AleoTransaction:
        """
        Submit transaction to Aleo network

        Args:
            transaction_data: Transaction data including proof

        Returns:
            AleoTransaction object
        """
        try:
            # In production, this would:
            # 1. Sign the transaction with private key
            # 2. Submit to mempool
            # 3. Wait for confirmation

            # Simulate transaction submission
            tx_id = f"aleo1qyz3{transaction_data.get('function', 'tx')[:4]}...8fhs"

            # Simulate network delay
            await asyncio.sleep(0.5)

            return AleoTransaction(
                transaction_id=tx_id,
                status="confirmed",
                block_height=(
                    await self.get_block_height() if self._connected else 12345
                ),
                timestamp=datetime.utcnow(),
            )

        except Exception as e:
            logger.error(f"Transaction submission failed: {e}")
            raise

    async def deploy_program(
        self, program_source: str, program_id: str, fee: int = 1000000
    ) -> str:
        """
        Deploy a Leo program to Aleo

        Args:
            program_source: Leo source code
            program_id: Program identifier
            fee: Deployment fee in microcredits

        Returns:
            Deployment transaction ID
        """
        try:
            # In production:
            # 1. Compile Leo program
            # 2. Generate deployment transaction
            # 3. Submit to network

            deployment_data = {
                "program_id": program_id,
                "source": program_source,
                "fee": fee,
            }

            tx = await self.submit_transaction(deployment_data)
            return tx.transaction_id

        except Exception as e:
            logger.error(f"Program deployment failed: {e}")
            raise

    async def execute_program(
        self, program_id: str, function_name: str, inputs: List[str], fee: int = 100000
    ) -> AleoTransaction:
        """
        Execute a program function

        Args:
            program_id: Program to execute
            function_name: Function/transition name
            inputs: Function inputs
            fee: Execution fee

        Returns:
            Transaction result
        """
        try:
            execution_data = {
                "program_id": program_id,
                "function": function_name,
                "inputs": inputs,
                "fee": fee,
            }

            return await self.submit_transaction(execution_data)

        except Exception as e:
            logger.error(f"Program execution failed: {e}")
            raise

    async def get_transaction(self, tx_id: str) -> Optional[AleoTransaction]:
        """
        Get transaction details

        Args:
            tx_id: Transaction ID

        Returns:
            Transaction details or None
        """
        try:
            result = await self._call_rpc("getTransaction", [tx_id])

            if result:
                return AleoTransaction(
                    transaction_id=result.get("id", tx_id),
                    status=result.get("status", "unknown"),
                    block_height=result.get("block_height"),
                    fee=result.get("fee"),
                )
            return None

        except Exception as e:
            logger.error(f"Failed to get transaction {tx_id}: {e}")
            return None

    async def wait_for_confirmation(
        self, tx_id: str, timeout: int = 60
    ) -> AleoTransaction:
        """
        Wait for transaction confirmation

        Args:
            tx_id: Transaction ID to monitor
            timeout: Maximum wait time in seconds

        Returns:
            Confirmed transaction
        """
        start_time = asyncio.get_event_loop().time()

        while asyncio.get_event_loop().time() - start_time < timeout:
            tx = await self.get_transaction(tx_id)

            if tx and tx.status == "confirmed":
                return tx

            await asyncio.sleep(2)  # Poll every 2 seconds

        raise TimeoutError(f"Transaction {tx_id} not confirmed within {timeout}s")

    async def estimate_fee(
        self, program_id: str, function_name: str, inputs: List[str]
    ) -> int:
        """
        Estimate execution fee

        Args:
            program_id: Program to execute
            function_name: Function name
            inputs: Function inputs

        Returns:
            Estimated fee in microcredits
        """
        # In production, would analyze program complexity
        # For now, return base fee
        base_fee = 100000  # 0.1 credits

        # Add complexity based on inputs
        complexity_fee = len(inputs) * 10000

        return base_fee + complexity_fee

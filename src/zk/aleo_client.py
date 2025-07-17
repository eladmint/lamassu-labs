"""
Aleo blockchain client for interacting with the network
Handles transactions, program deployment, and state queries
"""

import asyncio
<<<<<<< HEAD
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiohttp
=======
import json
import aiohttp
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import logging
from datetime import datetime
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

logger = logging.getLogger(__name__)


@dataclass
class AleoTransaction:
    """Represents an Aleo transaction"""
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    transaction_id: str
    status: str
    block_height: Optional[int] = None
    timestamp: Optional[datetime] = None
    fee: Optional[int] = None
    transitions: Optional[List[Dict[str, Any]]] = None
<<<<<<< HEAD

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "transaction_id": self.transaction_id,
            "status": self.status,
            "block_height": self.block_height,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "fee": self.fee,
            "transitions": self.transitions,
=======
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'status': self.status,
            'block_height': self.block_height,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'fee': self.fee,
            'transitions': self.transitions
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        }


class AleoClient:
    """
    Client for interacting with Aleo blockchain
    Handles RPC calls, transaction submission, and network queries
    """
<<<<<<< HEAD

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

=======
    
    # Default endpoints
    MAINNET_URL = "https://api.aleo.org/v1"
    TESTNET_URL = "https://api.testnet3.aleo.org/v1"
    
    def __init__(self, 
                 network: str = 'testnet',
                 endpoint: Optional[str] = None,
                 private_key: Optional[str] = None):
        """
        Initialize Aleo client
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Args:
            network: 'mainnet' or 'testnet'
            endpoint: Custom RPC endpoint (optional)
            private_key: Private key for transaction signing (optional)
        """
        self.network = network
        self.endpoint = endpoint or (
<<<<<<< HEAD
            self.MAINNET_URL if network == "mainnet" else self.TESTNET_URL
=======
            self.MAINNET_URL if network == 'mainnet' else self.TESTNET_URL
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )
        self.private_key = private_key
        self._session: Optional[aiohttp.ClientSession] = None
        self._connected = False
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
<<<<<<< HEAD

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()

=======
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    async def connect(self):
        """Connect to Aleo network"""
        if not self._session:
            self._session = aiohttp.ClientSession()
<<<<<<< HEAD

        # Test connection
        try:
            await self._call_rpc("getBlockHeight")
=======
            
        # Test connection
        try:
            await self._call_rpc('getBlockHeight')
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            self._connected = True
            logger.info(f"Connected to Aleo {self.network}")
        except Exception as e:
            logger.error(f"Failed to connect to Aleo: {e}")
            self._connected = False
            raise
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    async def disconnect(self):
        """Disconnect from Aleo network"""
        if self._session:
            await self._session.close()
            self._session = None
        self._connected = False
<<<<<<< HEAD

    def is_connected(self) -> bool:
        """Check if client is connected"""
        return self._connected

    async def _call_rpc(self, method: str, params: Optional[List[Any]] = None) -> Any:
        """
        Make RPC call to Aleo node

        Args:
            method: RPC method name
            params: Method parameters

=======
        
    def is_connected(self) -> bool:
        """Check if client is connected"""
        return self._connected
        
    async def _call_rpc(self, method: str, params: Optional[List[Any]] = None) -> Any:
        """
        Make RPC call to Aleo node
        
        Args:
            method: RPC method name
            params: Method parameters
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            RPC response data
        """
        if not self._session:
            await self.connect()
<<<<<<< HEAD

        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}

=======
            
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or []
        }
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        try:
            async with self._session.post(
                f"{self.endpoint}/rpc",
                json=payload,
<<<<<<< HEAD
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

=======
                headers={"Content-Type": "application/json"}
            ) as response:
                data = await response.json()
                
                if 'error' in data:
                    raise Exception(f"RPC error: {data['error']}")
                    
                return data.get('result')
                
        except Exception as e:
            logger.error(f"RPC call failed: {e}")
            raise
            
    async def get_block_height(self) -> int:
        """Get current block height"""
        result = await self._call_rpc('getBlockHeight')
        return int(result)
        
    async def get_program(self, program_id: str) -> Optional[Dict[str, Any]]:
        """
        Get program details
        
        Args:
            program_id: Aleo program ID
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            Program details or None if not found
        """
        try:
<<<<<<< HEAD
            result = await self._call_rpc("getProgram", [program_id])
=======
            result = await self._call_rpc('getProgram', [program_id])
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            return result
        except Exception as e:
            logger.error(f"Failed to get program {program_id}: {e}")
            return None
<<<<<<< HEAD

    async def submit_transaction(
        self, transaction_data: Dict[str, Any]
    ) -> AleoTransaction:
        """
        Submit transaction to Aleo network

        Args:
            transaction_data: Transaction data including proof

=======
            
    async def submit_transaction(self, 
                               transaction_data: Dict[str, Any]) -> AleoTransaction:
        """
        Submit transaction to Aleo network
        
        Args:
            transaction_data: Transaction data including proof
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            AleoTransaction object
        """
        try:
            # In production, this would:
            # 1. Sign the transaction with private key
            # 2. Submit to mempool
            # 3. Wait for confirmation
<<<<<<< HEAD

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

=======
            
            # Simulate transaction submission
            tx_id = f"aleo1qyz3{transaction_data.get('function', 'tx')[:4]}...8fhs"
            
            # Simulate network delay
            await asyncio.sleep(0.5)
            
            return AleoTransaction(
                transaction_id=tx_id,
                status='confirmed',
                block_height=await self.get_block_height() if self._connected else 12345,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Transaction submission failed: {e}")
            raise
            
    async def deploy_program(self,
                           program_source: str,
                           program_id: str,
                           fee: int = 1000000) -> str:
        """
        Deploy a Leo program to Aleo
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Args:
            program_source: Leo source code
            program_id: Program identifier
            fee: Deployment fee in microcredits
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            Deployment transaction ID
        """
        try:
            # In production:
            # 1. Compile Leo program
            # 2. Generate deployment transaction
            # 3. Submit to network
<<<<<<< HEAD

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

=======
            
            deployment_data = {
                'program_id': program_id,
                'source': program_source,
                'fee': fee
            }
            
            tx = await self.submit_transaction(deployment_data)
            return tx.transaction_id
            
        except Exception as e:
            logger.error(f"Program deployment failed: {e}")
            raise
            
    async def execute_program(self,
                            program_id: str,
                            function_name: str,
                            inputs: List[str],
                            fee: int = 100000) -> AleoTransaction:
        """
        Execute a program function
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Args:
            program_id: Program to execute
            function_name: Function/transition name
            inputs: Function inputs
            fee: Execution fee
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            Transaction result
        """
        try:
            execution_data = {
<<<<<<< HEAD
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

=======
                'program_id': program_id,
                'function': function_name,
                'inputs': inputs,
                'fee': fee
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
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            Transaction details or None
        """
        try:
<<<<<<< HEAD
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

=======
            result = await self._call_rpc('getTransaction', [tx_id])
            
            if result:
                return AleoTransaction(
                    transaction_id=result.get('id', tx_id),
                    status=result.get('status', 'unknown'),
                    block_height=result.get('block_height'),
                    fee=result.get('fee')
                )
            return None
            
        except Exception as e:
            logger.error(f"Failed to get transaction {tx_id}: {e}")
            return None
            
    async def wait_for_confirmation(self, 
                                  tx_id: str,
                                  timeout: int = 60) -> AleoTransaction:
        """
        Wait for transaction confirmation
        
        Args:
            tx_id: Transaction ID to monitor
            timeout: Maximum wait time in seconds
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            Confirmed transaction
        """
        start_time = asyncio.get_event_loop().time()
<<<<<<< HEAD

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

=======
        
        while asyncio.get_event_loop().time() - start_time < timeout:
            tx = await self.get_transaction(tx_id)
            
            if tx and tx.status == 'confirmed':
                return tx
                
            await asyncio.sleep(2)  # Poll every 2 seconds
            
        raise TimeoutError(f"Transaction {tx_id} not confirmed within {timeout}s")
        
    async def estimate_fee(self,
                         program_id: str,
                         function_name: str,
                         inputs: List[str]) -> int:
        """
        Estimate execution fee
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Args:
            program_id: Program to execute
            function_name: Function name
            inputs: Function inputs
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        Returns:
            Estimated fee in microcredits
        """
        # In production, would analyze program complexity
        # For now, return base fee
        base_fee = 100000  # 0.1 credits
<<<<<<< HEAD

        # Add complexity based on inputs
        complexity_fee = len(inputs) * 10000

        return base_fee + complexity_fee
=======
        
        # Add complexity based on inputs
        complexity_fee = len(inputs) * 10000
        
        return base_fee + complexity_fee
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

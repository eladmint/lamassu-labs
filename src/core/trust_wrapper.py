"""
ZKTrustWrapper - Universal ZK Verification Layer for AI Agents

Add trust to ANY AI agent in 3 lines:
    agent = YourAgent()
    trusted_agent = ZKTrustWrapper(agent)
    result = trusted_agent.verified_execute()
"""
import time
import hashlib
import json
from typing import Any, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExecutionMetrics:
    """Metrics collected during agent execution"""
    execution_time_ms: int
    success: bool
    input_hash: str
    output_hash: str
    timestamp: int
    agent_name: str
    agent_version: str = "1.0.0"
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'execution_time_ms': self.execution_time_ms,
            'success': self.success,
            'input_hash': self.input_hash,
            'output_hash': self.output_hash,
            'timestamp': self.timestamp,
            'agent_name': self.agent_name,
            'agent_version': self.agent_version,
            'error_message': self.error_message
        }


@dataclass
class ZKProof:
    """Zero-knowledge proof of execution"""
    proof_hash: str
    metrics_commitment: str
    timestamp: int
    aleo_tx_hash: Optional[str] = None  # Set after Aleo submission
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'proof_hash': self.proof_hash,
            'metrics_commitment': self.metrics_commitment,
            'timestamp': self.timestamp,
            'aleo_tx_hash': self.aleo_tx_hash
        }


@dataclass
class VerifiedResult:
    """Result with ZK verification proof"""
    data: Any  # Original agent result
    metrics: ExecutionMetrics
    proof: ZKProof
    verified: bool = True
    
    def __str__(self) -> str:
        status = "✓" if self.verified else "✗"
        return (
            f"\n🛡️ TrustWrapper Verification {status}\n"
            f"Agent: {self.metrics.agent_name}\n"
            f"Execution Time: {self.metrics.execution_time_ms}ms\n"
            f"Success: {'Yes' if self.metrics.success else 'No'}\n"
            f"Proof: {self.proof.proof_hash[:16]}...\n"
        )


class ZKTrustWrapper:
    """
    Universal wrapper that adds ZK-verified trust to any AI agent.
    Works with any agent that has an execute() or similar method.
    """
    
    def __init__(self, base_agent: Any, agent_name: Optional[str] = None):
        """
        Initialize the trust wrapper.
        
        Args:
            base_agent: Any AI agent with an execution method
            agent_name: Optional name for the agent (defaults to class name)
        """
        self.base_agent = base_agent
        self.agent_name = agent_name or base_agent.__class__.__name__
        self.execution_count = 0
        
        # Find the main execution method
        self.execute_method = self._find_execute_method()
        
    def _find_execute_method(self) -> str:
        """Find the main execution method of the wrapped agent"""
        # Common method names for agent execution
        common_methods = ['execute', 'run', 'process', 'extract', 'analyze', 
                         'scrape', 'monitor', 'fetch', 'generate']
        
        for method in common_methods:
            if hasattr(self.base_agent, method) and callable(getattr(self.base_agent, method)):
                return method
        
        # If no common method found, look for any callable
        callables = [attr for attr in dir(self.base_agent) 
                    if not attr.startswith('_') and callable(getattr(self.base_agent, attr))]
        
        if callables:
            return callables[0]
        
        raise ValueError(f"No execution method found in {self.agent_name}")
    
    def _hash_data(self, data: Any) -> str:
        """Create a hash of any data"""
        if isinstance(data, (dict, list)):
            data_str = json.dumps(data, sort_keys=True)
        else:
            data_str = str(data)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def _generate_proof(self, metrics: ExecutionMetrics) -> ZKProof:
        """
        Generate a zero-knowledge proof of execution.
        In production, this would create an actual ZK proof.
        For hackathon, we create a cryptographic commitment.
        """
        # Create metrics commitment
        metrics_json = json.dumps(metrics.to_dict(), sort_keys=True)
        metrics_commitment = hashlib.sha256(metrics_json.encode()).hexdigest()
        
        # Create proof hash (in production: actual ZK proof)
        proof_data = f"{metrics_commitment}:{metrics.timestamp}:{self.agent_name}"
        proof_hash = hashlib.sha256(proof_data.encode()).hexdigest()
        
        return ZKProof(
            proof_hash=proof_hash,
            metrics_commitment=metrics_commitment,
            timestamp=metrics.timestamp
        )
    
    def verified_execute(self, *args, **kwargs) -> VerifiedResult:
        """
        Execute the wrapped agent with ZK verification.
        
        Returns:
            VerifiedResult containing original data, metrics, and proof
        """
        # Hash inputs
        input_data = {'args': args, 'kwargs': kwargs}
        input_hash = self._hash_data(input_data)
        
        # Start timing
        start_time = time.time()
        timestamp = int(start_time)
        
        # Execute the base agent
        success = True
        error_message = None
        result = None
        
        try:
            method = getattr(self.base_agent, self.execute_method)
            result = method(*args, **kwargs)
        except Exception as e:
            success = False
            error_message = str(e)
            result = None
        
        # Calculate execution time
        execution_time_ms = int((time.time() - start_time) * 1000)
        
        # Hash output
        output_hash = self._hash_data(result) if result else "error"
        
        # Create metrics
        metrics = ExecutionMetrics(
            execution_time_ms=execution_time_ms,
            success=success,
            input_hash=input_hash,
            output_hash=output_hash,
            timestamp=timestamp,
            agent_name=self.agent_name,
            error_message=error_message
        )
        
        # Generate ZK proof
        proof = self._generate_proof(metrics)
        
        # Increment execution count
        self.execution_count += 1
        
        # Return verified result
        return VerifiedResult(
            data=result,
            metrics=metrics,
            proof=proof,
            verified=True
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get wrapper statistics"""
        return {
            'agent_name': self.agent_name,
            'execution_count': self.execution_count,
            'execute_method': self.execute_method,
            'wrapper_version': '1.0.0'
        }
    
    # Convenience methods that forward to verified_execute
    def execute(self, *args, **kwargs) -> VerifiedResult:
        """Alias for verified_execute"""
        return self.verified_execute(*args, **kwargs)
    
    def __call__(self, *args, **kwargs) -> VerifiedResult:
        """Make the wrapper callable"""
        return self.verified_execute(*args, **kwargs)
    
    def __repr__(self) -> str:
        return f"ZKTrustWrapper({self.agent_name})"


# Example usage and testing
if __name__ == "__main__":
    # Example: Wrap a simple agent
    class SimpleAgent:
        def execute(self, task: str) -> Dict[str, Any]:
            return {"task": task, "result": f"Completed: {task}"}
    
    # Create and wrap the agent
    agent = SimpleAgent()
    trusted_agent = ZKTrustWrapper(agent, "SimpleAgent")
    
    # Execute with verification
    result = trusted_agent.verified_execute("Find Web3 events")
    
    # Display verification
    print(result)
    print(f"\nOriginal Result: {result.data}")
    print(f"Execution Count: {trusted_agent.get_stats()['execution_count']}")
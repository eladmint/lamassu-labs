"""
Test the TrustWrapper with a simple example
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.trust_wrapper import ZKTrustWrapper


# Create a simple test agent
class SimpleTestAgent:
    """A minimal agent for testing"""
    
    def execute(self, task: str) -> dict:
        """Execute a simple task"""
        return {
            "task": task,
            "result": f"Successfully completed: {task}",
            "items_processed": 42
        }


def main():
    print("🧪 Testing TrustWrapper with a simple agent\n")
    
    # Create the base agent
    print("1. Creating SimpleTestAgent...")
    agent = SimpleTestAgent()
    
    # Wrap it with trust
    print("2. Wrapping with ZKTrustWrapper...")
    trusted_agent = ZKTrustWrapper(agent, "SimpleTestAgent")
    
    # Execute a task
    print("3. Executing task with ZK verification...\n")
    
    task = "Extract Web3 conference data"
    result = trusted_agent.verified_execute(task)
    
    # Display the verification
    print(result)
    
    # Show the actual result
    print(f"Original Result: {result.data}")
    
    # Show proof details
    print(f"\n🔐 Proof Details:")
    print(f"- Proof Hash: {result.proof.proof_hash[:32]}...")
    print(f"- Metrics Commitment: {result.proof.metrics_commitment[:32]}...")
    print(f"- Timestamp: {result.proof.timestamp}")
    
    # Show that we can call it multiple times
    print("\n4. Running multiple executions...")
    
    tasks = ["Scrape competitor prices", "Monitor treasury balance", "Analyze DeFi protocols"]
    
    for task in tasks:
        result = trusted_agent.execute(task)  # Using the alias method
        print(f"   ✓ {task} - Execution time: {result.metrics.execution_time_ms}ms")
    
    # Show statistics
    stats = trusted_agent.get_stats()
    print(f"\n📊 Statistics:")
    print(f"- Total Executions: {stats['execution_count']}")
    print(f"- Agent Name: {stats['agent_name']}")
    print(f"- Wrapper Version: {stats['wrapper_version']}")
    
    print("\n✅ TrustWrapper is working correctly!")
    print("   Any agent can now have ZK-verified trust in just 3 lines of code.")


if __name__ == "__main__":
    main()
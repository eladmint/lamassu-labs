#!/usr/bin/env python3
"""
Demo showing exactly what TrustWrapper verifies
"""
import sys
import os
import time
import random
from typing import Dict, Any

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
demo_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(demo_dir)
sys.path.insert(0, project_root)

from src.core.trust_wrapper import ZKTrustWrapper


class PerformanceTestAgent:
    """Agent to demonstrate performance verification"""
    
    def __init__(self, name: str, avg_time: float, success_rate: float):
        self.name = name
        self.avg_time = avg_time  # Average execution time in seconds
        self.success_rate = success_rate  # Success rate (0-1)
        self.execution_count = 0
    
    def execute(self, task: str) -> Dict[str, Any]:
        """Execute with simulated performance characteristics"""
        self.execution_count += 1
        
        # Simulate variable execution time
        exec_time = self.avg_time + random.uniform(-0.2, 0.2)
        time.sleep(exec_time)
        
        # Simulate success/failure based on success rate
        if random.random() < self.success_rate:
            return {
                "status": "success",
                "task": task,
                "execution": self.execution_count,
                "data": f"Processed {task} successfully"
            }
        else:
            raise Exception(f"Failed to process {task}")


def main():
    print("🔍 PERFORMANCE VERIFICATION DEMO")
    print("=" * 60)
    print("\nThis demo shows EXACTLY what TrustWrapper verifies:\n")
    
    # Create three agents with different performance profiles
    fast_agent = PerformanceTestAgent("FastAgent", avg_time=0.1, success_rate=0.95)
    slow_agent = PerformanceTestAgent("SlowAgent", avg_time=1.0, success_rate=0.99)
    unreliable_agent = PerformanceTestAgent("UnreliableAgent", avg_time=0.3, success_rate=0.60)
    
    agents = [
        ("Fast but less reliable", fast_agent),
        ("Slow but very reliable", slow_agent),
        ("Medium speed, unreliable", unreliable_agent)
    ]
    
    print("Testing 3 agents with different performance profiles:")
    print("-" * 60)
    
    for description, agent in agents:
        print(f"\n📊 Testing: {agent.name} ({description})")
        wrapped = ZKTrustWrapper(agent, agent.name)
        
        # Run multiple executions to gather statistics
        results = []
        successes = 0
        total_time = 0
        
        for i in range(5):
            result = wrapped.verified_execute(f"task_{i}")
            results.append(result)
            
            if result.metrics.success:
                successes += 1
                total_time += result.metrics.execution_time_ms
                print(f"   Run {i+1}: ✅ Success in {result.metrics.execution_time_ms}ms")
            else:
                print(f"   Run {i+1}: ❌ Failed - {result.metrics.error_message}")
        
        # Show what we can verify
        print(f"\n   📈 VERIFIED PERFORMANCE METRICS:")
        print(f"   • Success Rate: {successes}/5 ({successes/5*100:.0f}%)")
        if successes > 0:
            print(f"   • Average Time: {total_time/successes:.0f}ms")
        print(f"   • Reliability: {'High' if successes >= 4 else 'Medium' if successes >= 3 else 'Low'}")
        
        # Show what we CAN'T verify
        print(f"\n   ❓ WHAT WE CAN'T VERIFY:")
        print(f"   • HOW the agent processes tasks")
        print(f"   • WHAT algorithms it uses")
        print(f"   • WHETHER results are correct")
        print(f"   • WHY it succeeded or failed")
    
    print("\n" + "=" * 60)
    print("💡 KEY INSIGHT:")
    print("TrustWrapper provides PERFORMANCE TRANSPARENCY:")
    print("• ✅ Speed, reliability, execution patterns")
    print("• ❌ Implementation details, algorithms, correctness")
    print("\nThis is like proving a car goes 0-60 in 3 seconds")
    print("without revealing the engine design!")
    
    # Show accumulated trust over time
    print("\n" + "=" * 60)
    print("📊 TRUST BUILDING OVER TIME:")
    print("\nAfter 10 executions: Basic performance profile")
    print("After 100 executions: Statistical confidence")
    print("After 1000 executions: Reliable performance guarantees")
    print("\nEach execution adds to the immutable proof record on Aleo!")


if __name__ == "__main__":
    main()
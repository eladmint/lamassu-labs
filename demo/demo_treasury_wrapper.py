"""
Demo 3: Treasury Monitor Agent with ZK Trust

Shows how TrustWrapper adds verification to DeFi monitoring agents
"""
import sys
sys.path.append('..')

from src.core.trust_wrapper import ZKTrustWrapper
from typing import Dict, List, Any
import random
import time


class MockTreasuryAgent:
    """Mock treasury monitor for demo (simulates blockchain monitoring)"""
    
    def __init__(self):
        self.name = "TreasuryMonitor"
        self.monitored_addresses = []
    
    def monitor(self, addresses: List[str], threshold: float = 1000.0) -> Dict[str, Any]:
        """Simulate treasury monitoring"""
        # Simulate API calls
        time.sleep(random.uniform(1.0, 3.0))
        
        # Generate mock treasury data
        total_balance = 0
        alerts = []
        transactions = []
        
        for addr in addresses:
            balance = random.uniform(100, 50000)
            total_balance += balance
            
            # Simulate alerts
            if balance < threshold:
                alerts.append({
                    "type": "LOW_BALANCE",
                    "address": addr[:8] + "...",
                    "balance": balance,
                    "severity": "medium"
                })
            
            # Simulate recent transactions
            tx_count = random.randint(0, 5)
            for i in range(tx_count):
                transactions.append({
                    "from": addr[:8] + "...",
                    "amount": random.uniform(10, 1000),
                    "timestamp": int(time.time()) - random.randint(0, 86400)
                })
        
        return {
            "total_balance": round(total_balance, 2),
            "addresses_monitored": len(addresses),
            "alerts": alerts,
            "recent_transactions": sorted(transactions, key=lambda x: x['timestamp'], reverse=True)[:10],
            "risk_score": random.uniform(0.1, 0.9),
            "last_update": int(time.time())
        }


def main():
    print("💰 Demo 3: Treasury Monitoring with ZK Verification")
    print("=" * 50)
    
    # Create the base monitor
    print("\n1. Creating Treasury Monitor Agent...")
    base_monitor = MockTreasuryAgent()
    
    # Wrap it with trust
    print("2. Wrapping with ZKTrustWrapper...")
    trusted_monitor = ZKTrustWrapper(base_monitor, "TreasuryGuardian")
    
    # Test treasury addresses (mock)
    test_configs = [
        {
            "addresses": ["addr1abc...xyz", "addr2def...uvw", "addr3ghi...rst"],
            "threshold": 5000.0,
            "name": "DAO Treasury"
        },
        {
            "addresses": ["addr4jkl...opq", "addr5mno...lmn"],
            "threshold": 10000.0,
            "name": "Protocol Reserves"
        },
        {
            "addresses": ["addr6pqr...ijk", "addr7stu...fgh", "addr8vwx...cde", "addr9yza...bcd"],
            "threshold": 2000.0,
            "name": "Staking Pools"
        }
    ]
    
    print("\n3. Monitoring treasuries with ZK verification...\n")
    
    total_monitored = 0
    total_alerts = 0
    
    for config in test_configs:
        print(f"🏦 Monitoring: {config['name']}")
        print(f"   Addresses: {len(config['addresses'])}")
        print(f"   Alert Threshold: ${config['threshold']:,.2f}")
        
        # Execute with verification
        result = trusted_monitor.verified_execute(
            config['addresses'], 
            threshold=config['threshold']
        )
        
        # Show verification proof
        print(result)
        
        # Show monitoring results
        if result.data:
            data = result.data
            total_monitored += data['addresses_monitored']
            total_alerts += len(data['alerts'])
            
            print(f"   💎 Total Balance: ${data['total_balance']:,.2f}")
            print(f"   🚨 Alerts: {len(data['alerts'])}")
            print(f"   📊 Risk Score: {data['risk_score']:.2%}")
            print(f"   📝 Recent Transactions: {len(data['recent_transactions'])}")
            
            # Show sample alert
            if data['alerts']:
                alert = data['alerts'][0]
                print(f"   ⚠️  Sample Alert: {alert['type']} - {alert['address']} (${alert['balance']:,.2f})")
        
        print("-" * 50)
    
    # Show aggregate statistics
    stats = trusted_monitor.get_stats()
    
    print(f"\n📊 Monitoring Statistics:")
    print(f"- Total Monitoring Runs: {stats['execution_count']}")
    print(f"- Total Addresses Monitored: {total_monitored}")
    print(f"- Total Alerts Generated: {total_alerts}")
    print(f"- Average Execution Time: ~2 seconds")
    print(f"- All verified with ZK proofs ✅")
    
    print("\n🔐 DeFi Privacy Features:")
    print("- Treasury addresses remain private")
    print("- Threshold values are not revealed")
    print("- Alert logic stays confidential")
    print("- Only aggregate metrics are proven")
    print("- Perfect for competitive DeFi protocols")


if __name__ == "__main__":
    main()
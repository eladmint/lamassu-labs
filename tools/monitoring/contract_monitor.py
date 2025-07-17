#!/usr/bin/env python3
"""
Aleo Contract Monitoring Dashboard
Monitors deployed contracts on Aleo network for health and activity
"""

import asyncio
import json
<<<<<<< HEAD
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
=======
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import aiohttp
from dataclasses import dataclass, asdict
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
)
logger = logging.getLogger(__name__)


@dataclass
class ContractMetrics:
    """Metrics for a deployed contract"""
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    program_id: str
    total_transactions: int
    successful_transactions: int
    failed_transactions: int
    average_execution_time: float
    last_activity: Optional[datetime]
    current_stake: int
    active_agents: int
    gas_used_24h: int
    health_status: str  # 'healthy', 'degraded', 'unhealthy'
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        if self.last_activity:
<<<<<<< HEAD
            data["last_activity"] = self.last_activity.isoformat()
=======
            data['last_activity'] = self.last_activity.isoformat()
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return data


class AleoContractMonitor:
    """Monitor Aleo smart contracts"""
<<<<<<< HEAD

    def __init__(
        self, network: str = "testnet3", contracts: Optional[List[str]] = None
    ):
        self.network = network
        self.contracts = contracts or [
            "agent_registry_v2.aleo",
            "trust_verifier_v2.aleo",
        ]
        self.metrics: Dict[str, ContractMetrics] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.api_url = (
            f"https://api.{network}.aleo.org/v1"
            if network == "testnet3"
            else "https://api.aleo.org/v1"
        )

=======
    
    def __init__(self, network: str = 'testnet3', contracts: Optional[List[str]] = None):
        self.network = network
        self.contracts = contracts or [
            'agent_registry_v2.aleo',
            'trust_verifier_v2.aleo'
        ]
        self.metrics: Dict[str, ContractMetrics] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.api_url = f"https://api.{network}.aleo.org/v1" if network == 'testnet3' else "https://api.aleo.org/v1"
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    async def start_monitoring(self, interval: int = 60):
        """Start monitoring loop"""
        logger.info(f"Starting Aleo contract monitoring for {self.network}")
        logger.info(f"Monitoring contracts: {', '.join(self.contracts)}")
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        while True:
            try:
                await self.update_metrics()
                await self.check_alerts()
                self.generate_report()
<<<<<<< HEAD

                await asyncio.sleep(interval)

            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(interval)

=======
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(interval)
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    async def update_metrics(self):
        """Update metrics for all contracts"""
        for contract in self.contracts:
            try:
                metrics = await self.fetch_contract_metrics(contract)
                self.metrics[contract] = metrics
                logger.info(f"Updated metrics for {contract}")
<<<<<<< HEAD

            except Exception as e:
                logger.error(f"Failed to update metrics for {contract}: {e}")

=======
                
            except Exception as e:
                logger.error(f"Failed to update metrics for {contract}: {e}")
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    async def fetch_contract_metrics(self, program_id: str) -> ContractMetrics:
        """Fetch metrics for a specific contract"""
        async with aiohttp.ClientSession() as session:
            # Get program info
            program_info = await self._get_program_info(session, program_id)
<<<<<<< HEAD

            # Get recent transactions
            transactions = await self._get_recent_transactions(session, program_id)

            # Calculate metrics
            total_tx = len(transactions)
            successful_tx = sum(
                1 for tx in transactions if tx.get("status") == "confirmed"
            )
            failed_tx = total_tx - successful_tx

            # Calculate average execution time
            exec_times = [
                tx.get("execution_time", 0)
                for tx in transactions
                if tx.get("execution_time")
            ]
            avg_exec_time = sum(exec_times) / len(exec_times) if exec_times else 0

            # Get last activity
            last_activity = None
            if transactions:
                latest_tx = max(transactions, key=lambda x: x.get("timestamp", 0))
                last_activity = datetime.fromtimestamp(latest_tx.get("timestamp", 0))

            # Calculate gas used in last 24h
            yesterday = datetime.now() - timedelta(days=1)
            recent_gas = sum(
                tx.get("fee", 0)
                for tx in transactions
                if datetime.fromtimestamp(tx.get("timestamp", 0)) > yesterday
            )

=======
            
            # Get recent transactions
            transactions = await self._get_recent_transactions(session, program_id)
            
            # Calculate metrics
            total_tx = len(transactions)
            successful_tx = sum(1 for tx in transactions if tx.get('status') == 'confirmed')
            failed_tx = total_tx - successful_tx
            
            # Calculate average execution time
            exec_times = [tx.get('execution_time', 0) for tx in transactions if tx.get('execution_time')]
            avg_exec_time = sum(exec_times) / len(exec_times) if exec_times else 0
            
            # Get last activity
            last_activity = None
            if transactions:
                latest_tx = max(transactions, key=lambda x: x.get('timestamp', 0))
                last_activity = datetime.fromtimestamp(latest_tx.get('timestamp', 0))
                
            # Calculate gas used in last 24h
            yesterday = datetime.now() - timedelta(days=1)
            recent_gas = sum(
                tx.get('fee', 0) for tx in transactions 
                if datetime.fromtimestamp(tx.get('timestamp', 0)) > yesterday
            )
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            # Determine health status
            health = self._calculate_health_status(
                last_activity=last_activity,
                success_rate=successful_tx / total_tx if total_tx > 0 else 1.0,
<<<<<<< HEAD
                avg_exec_time=avg_exec_time,
            )

            # Mock some values for demo (would query from chain in production)
            current_stake = 100000  # Mock value
            active_agents = 42  # Mock value

=======
                avg_exec_time=avg_exec_time
            )
            
            # Mock some values for demo (would query from chain in production)
            current_stake = 100000  # Mock value
            active_agents = 42      # Mock value
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            return ContractMetrics(
                program_id=program_id,
                total_transactions=total_tx,
                successful_transactions=successful_tx,
                failed_transactions=failed_tx,
                average_execution_time=avg_exec_time,
                last_activity=last_activity,
                current_stake=current_stake,
                active_agents=active_agents,
                gas_used_24h=recent_gas,
<<<<<<< HEAD
                health_status=health,
            )

    async def _get_program_info(
        self, session: aiohttp.ClientSession, program_id: str
    ) -> Dict[str, Any]:
=======
                health_status=health
            )
            
    async def _get_program_info(self, session: aiohttp.ClientSession, program_id: str) -> Dict[str, Any]:
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        """Get program information from Aleo network"""
        try:
            url = f"{self.api_url}/program/{program_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
<<<<<<< HEAD
                    logger.warning(
                        f"Failed to get program info for {program_id}: {response.status}"
                    )
=======
                    logger.warning(f"Failed to get program info for {program_id}: {response.status}")
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                    return {}
        except Exception as e:
            logger.error(f"Error fetching program info: {e}")
            return {}
<<<<<<< HEAD

    async def _get_recent_transactions(
        self, session: aiohttp.ClientSession, program_id: str
    ) -> List[Dict[str, Any]]:
=======
            
    async def _get_recent_transactions(self, session: aiohttp.ClientSession, program_id: str) -> List[Dict[str, Any]]:
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        """Get recent transactions for a program"""
        # In production, this would query the actual Aleo API
        # For now, return mock data
        return [
            {
<<<<<<< HEAD
                "id": f"at{i}...",
                "status": "confirmed" if i % 10 != 0 else "failed",
                "execution_time": 1500 + (i * 100) % 1000,
                "timestamp": int(time.time()) - (i * 3600),
                "fee": 100000 + (i * 1000),
            }
            for i in range(20)
        ]

    def _calculate_health_status(
        self,
        last_activity: Optional[datetime],
        success_rate: float,
        avg_exec_time: float,
    ) -> str:
        """Calculate health status based on metrics"""
        if not last_activity:
            return "unhealthy"

        # Check if contract is active
        time_since_activity = datetime.now() - last_activity
        if time_since_activity > timedelta(hours=24):
            return "unhealthy"
        elif time_since_activity > timedelta(hours=6):
            return "degraded"

        # Check success rate
        if success_rate < 0.8:
            return "unhealthy"
        elif success_rate < 0.95:
            return "degraded"

        # Check execution time
        if avg_exec_time > 5000:  # 5 seconds
            return "degraded"

        return "healthy"

    async def check_alerts(self):
        """Check for alert conditions"""
        self.alerts.clear()

        for contract_id, metrics in self.metrics.items():
            # Check health status
            if metrics.health_status == "unhealthy":
                self.alerts.append(
                    {
                        "severity": "critical",
                        "contract": contract_id,
                        "message": f"Contract {contract_id} is unhealthy",
                        "timestamp": datetime.now().isoformat(),
                    }
                )

            elif metrics.health_status == "degraded":
                self.alerts.append(
                    {
                        "severity": "warning",
                        "contract": contract_id,
                        "message": f"Contract {contract_id} is degraded",
                        "timestamp": datetime.now().isoformat(),
                    }
                )

=======
                'id': f'at{i}...',
                'status': 'confirmed' if i % 10 != 0 else 'failed',
                'execution_time': 1500 + (i * 100) % 1000,
                'timestamp': int(time.time()) - (i * 3600),
                'fee': 100000 + (i * 1000)
            }
            for i in range(20)
        ]
        
    def _calculate_health_status(self, last_activity: Optional[datetime], 
                                success_rate: float, avg_exec_time: float) -> str:
        """Calculate health status based on metrics"""
        if not last_activity:
            return 'unhealthy'
            
        # Check if contract is active
        time_since_activity = datetime.now() - last_activity
        if time_since_activity > timedelta(hours=24):
            return 'unhealthy'
        elif time_since_activity > timedelta(hours=6):
            return 'degraded'
            
        # Check success rate
        if success_rate < 0.8:
            return 'unhealthy'
        elif success_rate < 0.95:
            return 'degraded'
            
        # Check execution time
        if avg_exec_time > 5000:  # 5 seconds
            return 'degraded'
            
        return 'healthy'
        
    async def check_alerts(self):
        """Check for alert conditions"""
        self.alerts.clear()
        
        for contract_id, metrics in self.metrics.items():
            # Check health status
            if metrics.health_status == 'unhealthy':
                self.alerts.append({
                    'severity': 'critical',
                    'contract': contract_id,
                    'message': f'Contract {contract_id} is unhealthy',
                    'timestamp': datetime.now().isoformat()
                })
                
            elif metrics.health_status == 'degraded':
                self.alerts.append({
                    'severity': 'warning',
                    'contract': contract_id,
                    'message': f'Contract {contract_id} is degraded',
                    'timestamp': datetime.now().isoformat()
                })
                
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            # Check for high failure rate
            if metrics.total_transactions > 0:
                failure_rate = metrics.failed_transactions / metrics.total_transactions
                if failure_rate > 0.2:
<<<<<<< HEAD
                    self.alerts.append(
                        {
                            "severity": "critical",
                            "contract": contract_id,
                            "message": f"High failure rate: {failure_rate:.1%}",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

=======
                    self.alerts.append({
                        'severity': 'critical',
                        'contract': contract_id,
                        'message': f'High failure rate: {failure_rate:.1%}',
                        'timestamp': datetime.now().isoformat()
                    })
                    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            # Check for inactivity
            if metrics.last_activity:
                inactive_time = datetime.now() - metrics.last_activity
                if inactive_time > timedelta(hours=12):
<<<<<<< HEAD
                    self.alerts.append(
                        {
                            "severity": "warning",
                            "contract": contract_id,
                            "message": f"No activity for {inactive_time.total_seconds() / 3600:.1f} hours",
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

    def generate_report(self):
        """Generate monitoring report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "network": self.network,
            "contracts": {},
            "alerts": self.alerts,
            "summary": {
                "total_contracts": len(self.contracts),
                "healthy_contracts": sum(
                    1 for m in self.metrics.values() if m.health_status == "healthy"
                ),
                "degraded_contracts": sum(
                    1 for m in self.metrics.values() if m.health_status == "degraded"
                ),
                "unhealthy_contracts": sum(
                    1 for m in self.metrics.values() if m.health_status == "unhealthy"
                ),
                "total_alerts": len(self.alerts),
                "critical_alerts": sum(
                    1 for a in self.alerts if a["severity"] == "critical"
                ),
            },
        }

        # Add contract metrics
        for contract_id, metrics in self.metrics.items():
            report["contracts"][contract_id] = metrics.to_dict()

        # Save report
        report_path = Path("monitoring/reports")
        report_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_path / f"aleo_monitor_{timestamp}.json"

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        # Also save latest report
        latest_file = report_path / "latest.json"
        with open(latest_file, "w") as f:
            json.dump(report, f, indent=2)

        # Print summary
        self.print_summary(report)

    def print_summary(self, report: Dict[str, Any]):
        """Print monitoring summary to console"""
        print("\n" + "=" * 60)
        print(f"Aleo Contract Monitor - {self.network}")
        print(f"Time: {report['timestamp']}")
        print("=" * 60)

        # Summary stats
        summary = report["summary"]
=======
                    self.alerts.append({
                        'severity': 'warning',
                        'contract': contract_id,
                        'message': f'No activity for {inactive_time.total_seconds() / 3600:.1f} hours',
                        'timestamp': datetime.now().isoformat()
                    })
                    
    def generate_report(self):
        """Generate monitoring report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'network': self.network,
            'contracts': {},
            'alerts': self.alerts,
            'summary': {
                'total_contracts': len(self.contracts),
                'healthy_contracts': sum(1 for m in self.metrics.values() if m.health_status == 'healthy'),
                'degraded_contracts': sum(1 for m in self.metrics.values() if m.health_status == 'degraded'),
                'unhealthy_contracts': sum(1 for m in self.metrics.values() if m.health_status == 'unhealthy'),
                'total_alerts': len(self.alerts),
                'critical_alerts': sum(1 for a in self.alerts if a['severity'] == 'critical')
            }
        }
        
        # Add contract metrics
        for contract_id, metrics in self.metrics.items():
            report['contracts'][contract_id] = metrics.to_dict()
            
        # Save report
        report_path = Path('monitoring/reports')
        report_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = report_path / f'aleo_monitor_{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Also save latest report
        latest_file = report_path / 'latest.json'
        with open(latest_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        self.print_summary(report)
        
    def print_summary(self, report: Dict[str, Any]):
        """Print monitoring summary to console"""
        print("\n" + "="*60)
        print(f"Aleo Contract Monitor - {self.network}")
        print(f"Time: {report['timestamp']}")
        print("="*60)
        
        # Summary stats
        summary = report['summary']
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        print(f"\nContracts: {summary['total_contracts']} total")
        print(f"  ✅ Healthy: {summary['healthy_contracts']}")
        print(f"  ⚠️  Degraded: {summary['degraded_contracts']}")
        print(f"  ❌ Unhealthy: {summary['unhealthy_contracts']}")
<<<<<<< HEAD

        # Contract details
        print("\nContract Status:")
        for contract_id, metrics in report["contracts"].items():
            status_icon = {"healthy": "✅", "degraded": "⚠️", "unhealthy": "❌"}.get(
                metrics["health_status"], "❓"
            )

            print(f"\n{status_icon} {contract_id}")
            print(
                f"   Transactions: {metrics['total_transactions']} total, {metrics['successful_transactions']} successful"
            )
            print(f"   Avg Execution: {metrics['average_execution_time']:.0f}ms")
            print(f"   Gas (24h): {metrics['gas_used_24h']:,} microcredits")

        # Alerts
        if report["alerts"]:
            print(f"\n🚨 Alerts ({len(report['alerts'])} total):")
            for alert in report["alerts"]:
                icon = "🔴" if alert["severity"] == "critical" else "🟡"
                print(
                    f"{icon} [{alert['severity'].upper()}] {alert['contract']}: {alert['message']}"
                )
        else:
            print("\n✅ No alerts")

        print("\n" + "=" * 60)
=======
        
        # Contract details
        print("\nContract Status:")
        for contract_id, metrics in report['contracts'].items():
            status_icon = {
                'healthy': '✅',
                'degraded': '⚠️',
                'unhealthy': '❌'
            }.get(metrics['health_status'], '❓')
            
            print(f"\n{status_icon} {contract_id}")
            print(f"   Transactions: {metrics['total_transactions']} total, {metrics['successful_transactions']} successful")
            print(f"   Avg Execution: {metrics['average_execution_time']:.0f}ms")
            print(f"   Gas (24h): {metrics['gas_used_24h']:,} microcredits")
            
        # Alerts
        if report['alerts']:
            print(f"\n🚨 Alerts ({len(report['alerts'])} total):")
            for alert in report['alerts']:
                icon = '🔴' if alert['severity'] == 'critical' else '🟡'
                print(f"{icon} [{alert['severity'].upper()}] {alert['contract']}: {alert['message']}")
        else:
            print("\n✅ No alerts")
            
        print("\n" + "="*60)
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752


async def main():
    """Run the monitor"""
    import argparse
<<<<<<< HEAD

    parser = argparse.ArgumentParser(description="Aleo Contract Monitor")
    parser.add_argument("--network", default="testnet3", help="Aleo network to monitor")
    parser.add_argument(
        "--interval", type=int, default=60, help="Monitoring interval in seconds"
    )
    parser.add_argument("--contracts", nargs="+", help="Contract IDs to monitor")

    args = parser.parse_args()

    monitor = AleoContractMonitor(network=args.network, contracts=args.contracts)

    await monitor.start_monitoring(interval=args.interval)


if __name__ == "__main__":
    asyncio.run(main())
=======
    
    parser = argparse.ArgumentParser(description='Aleo Contract Monitor')
    parser.add_argument('--network', default='testnet3', help='Aleo network to monitor')
    parser.add_argument('--interval', type=int, default=60, help='Monitoring interval in seconds')
    parser.add_argument('--contracts', nargs='+', help='Contract IDs to monitor')
    
    args = parser.parse_args()
    
    monitor = AleoContractMonitor(
        network=args.network,
        contracts=args.contracts
    )
    
    await monitor.start_monitoring(interval=args.interval)


if __name__ == '__main__':
    asyncio.run(main())
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

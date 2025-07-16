#!/usr/bin/env python3

"""
TrustWrapper v3.0 Load Testing Suite
Comprehensive performance validation for 5,000+ RPS target
Universal Multi-Chain AI Verification Platform
"""

import argparse
import asyncio
import json
import logging
import statistics
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Optional

import aiohttp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class LoadTestConfig:
    """Load test configuration parameters"""

    base_url: str = "http://api.trustwrapper.com"
    target_rps: int = 5000
    test_duration: int = 300  # 5 minutes
    warm_up_duration: int = 60  # 1 minute
    concurrent_users: int = 500
    timeout: int = 30
    verify_ssl: bool = True


@dataclass
class RequestResult:
    """Individual request result"""

    endpoint: str
    method: str
    status_code: int
    response_time: float
    timestamp: float
    error: Optional[str] = None
    payload_size: int = 0


@dataclass
class LoadTestResults:
    """Aggregated load test results"""

    total_requests: int
    successful_requests: int
    failed_requests: int
    average_rps: float
    peak_rps: float
    average_response_time: float
    p50_response_time: float
    p95_response_time: float
    p99_response_time: float
    error_rate: float
    throughput_mbps: float
    test_duration: float


class TrustWrapperLoadTester:
    """Comprehensive load testing for TrustWrapper v3.0"""

    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.results: List[RequestResult] = []
        self.start_time: float = 0
        self.session: Optional[aiohttp.ClientSession] = None

        # Test endpoints with realistic payloads
        self.test_endpoints = [
            {
                "path": "/health",
                "method": "GET",
                "weight": 0.1,  # 10% of requests
                "payload": None,
            },
            {
                "path": "/verify",
                "method": "POST",
                "weight": 0.4,  # 40% of requests
                "payload": {
                    "transaction": {
                        "from": "0x742d35Cc6327C0532D4a8E9D2c6e8d07CE40F7fB",
                        "to": "0x8ba1f109551bD432803012645Hac136c95ce293c",
                        "value": "1000000000000000000",
                        "gas": "21000",
                        "gasPrice": "20000000000",
                        "data": "0x",
                        "chainId": 1,
                    },
                    "verification_level": "standard",
                },
            },
            {
                "path": "/consensus",
                "method": "POST",
                "weight": 0.2,  # 20% of requests
                "payload": {
                    "chains": ["ethereum", "polygon", "cardano"],
                    "query": "get_latest_block",
                    "consensus_threshold": 0.67,
                },
            },
            {
                "path": "/bridge",
                "method": "POST",
                "weight": 0.15,  # 15% of requests
                "payload": {
                    "source_chain": "ethereum",
                    "target_chain": "polygon",
                    "amount": "1000000000000000000",
                    "token": "USDC",
                },
            },
            {
                "path": "/oracle/ETH-USD",
                "method": "GET",
                "weight": 0.15,  # 15% of requests
                "payload": None,
            },
        ]

    async def create_session(self) -> aiohttp.ClientSession:
        """Create optimized HTTP session"""
        connector = aiohttp.TCPConnector(
            limit=1000,
            limit_per_host=200,
            ttl_dns_cache=300,
            use_dns_cache=True,
            keepalive_timeout=30,
            enable_cleanup_closed=True,
        )

        timeout = aiohttp.ClientTimeout(total=self.config.timeout)

        session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                "User-Agent": "TrustWrapper-LoadTest/1.0",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

        return session

    async def make_request(self, endpoint: Dict) -> RequestResult:
        """Make a single HTTP request"""
        start_time = time.time()
        url = f"{self.config.base_url}{endpoint['path']}"

        try:
            if endpoint["method"] == "GET":
                async with self.session.get(url) as response:
                    await response.read()
                    payload_size = (
                        len(await response.read())
                        if hasattr(response, "content")
                        else 0
                    )

                    return RequestResult(
                        endpoint=endpoint["path"],
                        method=endpoint["method"],
                        status_code=response.status,
                        response_time=time.time() - start_time,
                        timestamp=start_time,
                        payload_size=payload_size,
                    )
            else:
                async with self.session.post(url, json=endpoint["payload"]) as response:
                    content = await response.read()
                    payload_size = len(content)

                    return RequestResult(
                        endpoint=endpoint["path"],
                        method=endpoint["method"],
                        status_code=response.status,
                        response_time=time.time() - start_time,
                        timestamp=start_time,
                        payload_size=payload_size,
                    )

        except Exception as e:
            return RequestResult(
                endpoint=endpoint["path"],
                method=endpoint["method"],
                status_code=0,
                response_time=time.time() - start_time,
                timestamp=start_time,
                error=str(e),
            )

    async def worker(
        self, worker_id: int, requests_per_worker: int
    ) -> List[RequestResult]:
        """Worker coroutine for generating load"""
        results = []

        # Calculate delay between requests to achieve target RPS
        delay = len(self.test_endpoints) / (
            self.config.target_rps / self.config.concurrent_users
        )

        for i in range(requests_per_worker):
            # Select endpoint based on weights
            import random

            rand = random.random()
            cumulative = 0

            for endpoint in self.test_endpoints:
                cumulative += endpoint["weight"]
                if rand <= cumulative:
                    selected_endpoint = endpoint
                    break

            # Make request
            result = await self.make_request(selected_endpoint)
            results.append(result)

            # Add delay to control RPS
            await asyncio.sleep(delay)

        return results

    async def warm_up(self):
        """Warm-up phase to establish connections"""
        logger.info(f"Starting warm-up phase ({self.config.warm_up_duration}s)...")

        warm_up_tasks = []
        requests_per_worker = int(
            self.config.warm_up_duration
            * self.config.target_rps
            / 10
            / self.config.concurrent_users
        )

        for i in range(
            min(50, self.config.concurrent_users)
        ):  # Limited warm-up workers
            task = asyncio.create_task(self.worker(i, requests_per_worker))
            warm_up_tasks.append(task)

        await asyncio.gather(*warm_up_tasks, return_exceptions=True)
        logger.info("Warm-up phase completed")

    async def run_load_test(self) -> LoadTestResults:
        """Run the main load test"""
        logger.info(
            f"Starting load test - Target: {self.config.target_rps} RPS for {self.config.test_duration}s"
        )

        self.session = await self.create_session()
        self.start_time = time.time()

        try:
            # Warm-up phase
            await self.warm_up()

            # Main test phase
            test_start = time.time()
            tasks = []

            total_requests = self.config.target_rps * self.config.test_duration
            requests_per_worker = total_requests // self.config.concurrent_users

            logger.info(
                f"Creating {self.config.concurrent_users} workers, {requests_per_worker} requests each"
            )

            for i in range(self.config.concurrent_users):
                task = asyncio.create_task(self.worker(i, requests_per_worker))
                tasks.append(task)

            # Collect results
            worker_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Flatten results
            for worker_result in worker_results:
                if isinstance(worker_result, list):
                    self.results.extend(worker_result)
                elif isinstance(worker_result, Exception):
                    logger.error(f"Worker failed: {worker_result}")

            test_duration = time.time() - test_start

            return self.analyze_results(test_duration)

        finally:
            if self.session:
                await self.session.close()

    def analyze_results(self, test_duration: float) -> LoadTestResults:
        """Analyze test results and generate metrics"""
        if not self.results:
            raise ValueError("No results to analyze")

        # Filter successful requests
        successful_results = [
            r for r in self.results if r.status_code == 200 and r.error is None
        ]
        failed_results = [
            r for r in self.results if r.status_code != 200 or r.error is not None
        ]

        # Calculate response time percentiles
        response_times = [r.response_time for r in successful_results]
        if response_times:
            response_times.sort()
            p50 = statistics.median(response_times)
            p95 = response_times[int(len(response_times) * 0.95)]
            p99 = response_times[int(len(response_times) * 0.99)]
            avg_response_time = statistics.mean(response_times)
        else:
            p50 = p95 = p99 = avg_response_time = 0

        # Calculate RPS metrics
        if self.results:
            timestamps = [r.timestamp for r in self.results]
            time_buckets = {}

            for timestamp in timestamps:
                bucket = int(timestamp)
                time_buckets[bucket] = time_buckets.get(bucket, 0) + 1

            rps_values = list(time_buckets.values())
            average_rps = len(self.results) / test_duration
            peak_rps = max(rps_values) if rps_values else 0
        else:
            average_rps = peak_rps = 0

        # Calculate throughput
        total_bytes = sum(r.payload_size for r in successful_results)
        throughput_mbps = (total_bytes * 8) / (
            test_duration * 1024 * 1024
        )  # Convert to Mbps

        return LoadTestResults(
            total_requests=len(self.results),
            successful_requests=len(successful_results),
            failed_requests=len(failed_results),
            average_rps=average_rps,
            peak_rps=peak_rps,
            average_response_time=avg_response_time,
            p50_response_time=p50,
            p95_response_time=p95,
            p99_response_time=p99,
            error_rate=(
                (len(failed_results) / len(self.results)) * 100 if self.results else 0
            ),
            throughput_mbps=throughput_mbps,
            test_duration=test_duration,
        )

    def generate_report(self, results: LoadTestResults, output_file: str = None):
        """Generate detailed test report"""
        report = {
            "test_summary": {
                "timestamp": datetime.now().isoformat(),
                "target_rps": self.config.target_rps,
                "test_duration": self.config.test_duration,
                "concurrent_users": self.config.concurrent_users,
            },
            "performance_metrics": asdict(results),
            "success_criteria": {
                "target_rps_achieved": results.average_rps
                >= self.config.target_rps * 0.95,
                "error_rate_acceptable": results.error_rate <= 1.0,
                "p95_response_time_acceptable": results.p95_response_time <= 0.2,
                "peak_rps_achieved": results.peak_rps >= self.config.target_rps,
            },
            "endpoint_breakdown": self._analyze_by_endpoint(),
        }

        # Print summary
        print("\n" + "=" * 80)
        print("TRUSTWRAPPER v3.0 LOAD TEST RESULTS")
        print("=" * 80)
        print(f"Target RPS:           {self.config.target_rps:,}")
        print(f"Achieved Average RPS: {results.average_rps:,.1f}")
        print(f"Peak RPS:             {results.peak_rps:,.1f}")
        print(f"Success Rate:         {100 - results.error_rate:.2f}%")
        print(f"Average Response:     {results.average_response_time*1000:.1f}ms")
        print(f"P95 Response Time:    {results.p95_response_time*1000:.1f}ms")
        print(f"P99 Response Time:    {results.p99_response_time*1000:.1f}ms")
        print(f"Throughput:           {results.throughput_mbps:.2f} Mbps")
        print("=" * 80)

        # Success criteria
        criteria = report["success_criteria"]
        print("SUCCESS CRITERIA:")
        print(
            f"  ✅ Target RPS:        {'PASS' if criteria['target_rps_achieved'] else 'FAIL'}"
        )
        print(
            f"  ✅ Error Rate:        {'PASS' if criteria['error_rate_acceptable'] else 'FAIL'}"
        )
        print(
            f"  ✅ P95 Response:      {'PASS' if criteria['p95_response_time_acceptable'] else 'FAIL'}"
        )
        print(
            f"  ✅ Peak RPS:          {'PASS' if criteria['peak_rps_achieved'] else 'FAIL'}"
        )

        overall_pass = all(criteria.values())
        print(f"\nOVERALL RESULT: {'🎉 PASS' if overall_pass else '❌ FAIL'}")
        print("=" * 80)

        # Save detailed report
        if output_file:
            with open(output_file, "w") as f:
                json.dump(report, f, indent=2)
            print(f"Detailed report saved to: {output_file}")

        return report

    def _analyze_by_endpoint(self) -> Dict:
        """Analyze results by endpoint"""
        endpoint_stats = {}

        for result in self.results:
            endpoint = result.endpoint
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = {
                    "total_requests": 0,
                    "successful_requests": 0,
                    "failed_requests": 0,
                    "response_times": [],
                }

            stats = endpoint_stats[endpoint]
            stats["total_requests"] += 1

            if result.status_code == 200 and result.error is None:
                stats["successful_requests"] += 1
                stats["response_times"].append(result.response_time)
            else:
                stats["failed_requests"] += 1

        # Calculate averages
        for endpoint, stats in endpoint_stats.items():
            if stats["response_times"]:
                stats["average_response_time"] = statistics.mean(
                    stats["response_times"]
                )
                stats["p95_response_time"] = stats["response_times"][
                    int(len(stats["response_times"]) * 0.95)
                ]
            else:
                stats["average_response_time"] = 0
                stats["p95_response_time"] = 0

            stats["error_rate"] = (
                stats["failed_requests"] / stats["total_requests"]
            ) * 100
            del stats["response_times"]  # Remove raw data from report

        return endpoint_stats


async def main():
    """Main function for load testing"""
    parser = argparse.ArgumentParser(description="TrustWrapper v3.0 Load Testing Suite")
    parser.add_argument("--url", default="http://api.trustwrapper.com", help="Base URL")
    parser.add_argument(
        "--rps", type=int, default=5000, help="Target requests per second"
    )
    parser.add_argument(
        "--duration", type=int, default=300, help="Test duration in seconds"
    )
    parser.add_argument("--users", type=int, default=500, help="Concurrent users")
    parser.add_argument("--output", help="Output file for detailed results")

    args = parser.parse_args()

    config = LoadTestConfig(
        base_url=args.url,
        target_rps=args.rps,
        test_duration=args.duration,
        concurrent_users=args.users,
    )

    tester = TrustWrapperLoadTester(config)

    try:
        results = await tester.run_load_test()
        report = tester.generate_report(results, args.output)

        # Exit with appropriate code
        success_criteria = report["success_criteria"]
        if all(success_criteria.values()):
            exit(0)  # Success
        else:
            exit(1)  # Failure

    except Exception as e:
        logger.error(f"Load test failed: {e}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())

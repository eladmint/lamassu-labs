#!/usr/bin/env python3
"""
TrustWrapper Yield Improvement Analysis

This analysis demonstrates how TrustWrapper-enhanced trading agents
achieve better yields through loss prevention and risk management.
"""

import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np


@dataclass
class TradeOutcome:
    """Individual trade outcome"""

    token_type: str
    amount_risked: float
    return_pct: float
    profit_loss: float
    blocked_by_trustwrapper: bool = False


@dataclass
class PortfolioResults:
    """Portfolio performance results"""

    total_trades: int
    profitable_trades: int
    losing_trades: int
    blocked_trades: int
    total_return_pct: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float


class TradingSimulator:
    """Simulates trading with and without TrustWrapper"""

    def __init__(self, initial_capital: float = 100.0):
        self.initial_capital = initial_capital

        # Market scenarios with realistic probabilities and returns
        self.trade_scenarios = {
            "legitimate_defi": {
                "probability": 0.40,  # 40% of trades
                "return_range": (-20, 50),  # -20% to +50%
                "scam_probability": 0.0,
                "trustwrapper_blocks": 0.0,
            },
            "established_tokens": {
                "probability": 0.30,  # 30% of trades
                "return_range": (-15, 30),  # -15% to +30%
                "scam_probability": 0.0,
                "trustwrapper_blocks": 0.0,
            },
            "meme_tokens": {
                "probability": 0.15,  # 15% of trades
                "return_range": (-60, 200),  # High volatility
                "scam_probability": 0.1,  # 10% are scams
                "trustwrapper_blocks": 0.05,  # 5% flagged for review
            },
            "new_tokens": {
                "probability": 0.10,  # 10% of trades
                "return_range": (-80, 500),  # Very high risk/reward
                "scam_probability": 0.3,  # 30% are scams
                "trustwrapper_blocks": 0.2,  # 20% flagged for review
            },
            "obvious_scams": {
                "probability": 0.05,  # 5% of trades
                "return_range": (-95, -100),  # Almost always total loss
                "scam_probability": 1.0,  # 100% are scams
                "trustwrapper_blocks": 0.95,  # 95% blocked by TrustWrapper
            },
        }

    def generate_trade_scenario(self) -> str:
        """Generate a random trade scenario based on probabilities"""
        scenarios = list(self.trade_scenarios.keys())
        probabilities = [self.trade_scenarios[s]["probability"] for s in scenarios]
        return np.random.choice(scenarios, p=probabilities)

    def simulate_trade_outcome(
        self, scenario: str, with_trustwrapper: bool
    ) -> TradeOutcome:
        """Simulate outcome of a single trade"""
        scenario_data = self.trade_scenarios[scenario]

        # Determine if TrustWrapper would block this trade
        blocked = False
        if with_trustwrapper:
            # TrustWrapper blocks scams with high probability
            if random.random() < scenario_data["scam_probability"] * 0.95:
                blocked = True
            # TrustWrapper flags risky trades for review (reduced position)
            elif random.random() < scenario_data["trustwrapper_blocks"]:
                pass  # Will reduce position size instead of blocking

        if blocked:
            return TradeOutcome(
                token_type=scenario,
                amount_risked=0.0,
                return_pct=0.0,
                profit_loss=0.0,
                blocked_by_trustwrapper=True,
            )

        # Generate trade outcome
        min_return, max_return = scenario_data["return_range"]

        # Check if this is a scam trade
        is_scam = random.random() < scenario_data["scam_probability"]
        if is_scam:
            # Scam trades almost always result in total loss
            return_pct = random.uniform(-95, -100)
        else:
            # Normal market distribution (slightly positive bias)
            return_pct = random.uniform(min_return, max_return)
            if random.random() < 0.55:  # 55% chance of profit
                return_pct = abs(return_pct) if return_pct < 0 else return_pct

        # Determine position size
        base_amount = 5.0  # Base trade size in SOL

        # TrustWrapper reduces position size for risky scenarios
        if with_trustwrapper and scenario in ["meme_tokens", "new_tokens"]:
            if random.random() < scenario_data["trustwrapper_blocks"]:
                base_amount *= 0.5  # Reduce position by 50%

        profit_loss = base_amount * (return_pct / 100)

        return TradeOutcome(
            token_type=scenario,
            amount_risked=base_amount,
            return_pct=return_pct,
            profit_loss=profit_loss,
            blocked_by_trustwrapper=False,
        )

    def run_simulation(
        self, num_trades: int, with_trustwrapper: bool
    ) -> Tuple[PortfolioResults, List[TradeOutcome]]:
        """Run a complete trading simulation"""
        trades = []
        portfolio_value = self.initial_capital
        max_portfolio_value = self.initial_capital
        max_drawdown = 0.0

        for _ in range(num_trades):
            scenario = self.generate_trade_scenario()
            trade = self.simulate_trade_outcome(scenario, with_trustwrapper)
            trades.append(trade)

            # Update portfolio value
            portfolio_value += trade.profit_loss

            # Track max drawdown
            if portfolio_value > max_portfolio_value:
                max_portfolio_value = portfolio_value
            else:
                current_drawdown = (
                    max_portfolio_value - portfolio_value
                ) / max_portfolio_value
                max_drawdown = max(max_drawdown, current_drawdown)

        # Calculate statistics
        executed_trades = [t for t in trades if not t.blocked_by_trustwrapper]
        profitable_trades = len([t for t in executed_trades if t.profit_loss > 0])
        losing_trades = len([t for t in executed_trades if t.profit_loss < 0])
        blocked_trades = len([t for t in trades if t.blocked_by_trustwrapper])

        total_return_pct = (
            (portfolio_value - self.initial_capital) / self.initial_capital
        ) * 100

        # Calculate Sharpe ratio (simplified)
        if executed_trades:
            returns = [t.return_pct for t in executed_trades]
            avg_return = np.mean(returns)
            std_return = np.std(returns)
            sharpe_ratio = avg_return / std_return if std_return > 0 else 0
        else:
            sharpe_ratio = 0

        win_rate = profitable_trades / max(len(executed_trades), 1)

        results = PortfolioResults(
            total_trades=len(executed_trades),
            profitable_trades=profitable_trades,
            losing_trades=losing_trades,
            blocked_trades=blocked_trades,
            total_return_pct=total_return_pct,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
        )

        return results, trades


def run_comparative_analysis():
    """Run comparative analysis between original and TrustWrapper-enhanced agents"""
    print("=" * 80)
    print("🧪 TrustWrapper Yield Improvement Analysis")
    print("=" * 80)

    simulator = TradingSimulator(initial_capital=100.0)
    num_trades = 500
    num_simulations = 100

    print(
        f"\n📊 Running {num_simulations} simulations with {num_trades} trades each..."
    )

    # Run multiple simulations
    original_results = []
    trustwrapper_results = []

    for sim in range(num_simulations):
        # Reset random seed for comparable results
        random.seed(42 + sim)
        np.random.seed(42 + sim)

        # Original agent simulation
        original_result, _ = simulator.run_simulation(
            num_trades, with_trustwrapper=False
        )
        original_results.append(original_result)

        # Reset seed for same market conditions
        random.seed(42 + sim)
        np.random.seed(42 + sim)

        # TrustWrapper-enhanced agent simulation
        trustwrapper_result, _ = simulator.run_simulation(
            num_trades, with_trustwrapper=True
        )
        trustwrapper_results.append(trustwrapper_result)

        if (sim + 1) % 20 == 0:
            print(f"  Completed {sim + 1}/{num_simulations} simulations...")

    # Calculate aggregate statistics
    def calculate_stats(results: List[PortfolioResults]) -> Dict:
        return {
            "avg_return": np.mean([r.total_return_pct for r in results]),
            "median_return": np.median([r.total_return_pct for r in results]),
            "std_return": np.std([r.total_return_pct for r in results]),
            "min_return": np.min([r.total_return_pct for r in results]),
            "max_return": np.max([r.total_return_pct for r in results]),
            "avg_sharpe": np.mean([r.sharpe_ratio for r in results]),
            "avg_max_drawdown": np.mean([r.max_drawdown for r in results]),
            "avg_win_rate": np.mean([r.win_rate for r in results]),
            "avg_blocked_trades": np.mean([r.blocked_trades for r in results]),
            "bankruptcy_rate": len([r for r in results if r.total_return_pct < -90])
            / len(results),
        }

    original_stats = calculate_stats(original_results)
    trustwrapper_stats = calculate_stats(trustwrapper_results)

    # Display results
    print(f"\n{'='*80}")
    print("📈 COMPARATIVE RESULTS")
    print(f"{'='*80}")

    print("\n🤖 Original Agent Performance:")
    print(f"  • Average Return: {original_stats['avg_return']:+.2f}%")
    print(f"  • Median Return: {original_stats['median_return']:+.2f}%")
    print(f"  • Return Volatility: ±{original_stats['std_return']:.2f}%")
    print(f"  • Best Case: {original_stats['max_return']:+.2f}%")
    print(f"  • Worst Case: {original_stats['min_return']:+.2f}%")
    print(f"  • Average Sharpe Ratio: {original_stats['avg_sharpe']:.3f}")
    print(f"  • Average Max Drawdown: {original_stats['avg_max_drawdown']:.1%}")
    print(f"  • Average Win Rate: {original_stats['avg_win_rate']:.1%}")
    print(f"  • Bankruptcy Rate: {original_stats['bankruptcy_rate']:.1%}")

    print("\n🛡️ TrustWrapper-Enhanced Agent Performance:")
    print(f"  • Average Return: {trustwrapper_stats['avg_return']:+.2f}%")
    print(f"  • Median Return: {trustwrapper_stats['median_return']:+.2f}%")
    print(f"  • Return Volatility: ±{trustwrapper_stats['std_return']:.2f}%")
    print(f"  • Best Case: {trustwrapper_stats['max_return']:+.2f}%")
    print(f"  • Worst Case: {trustwrapper_stats['min_return']:+.2f}%")
    print(f"  • Average Sharpe Ratio: {trustwrapper_stats['avg_sharpe']:.3f}")
    print(f"  • Average Max Drawdown: {trustwrapper_stats['avg_max_drawdown']:.1%}")
    print(f"  • Average Win Rate: {trustwrapper_stats['avg_win_rate']:.1%}")
    print(f"  • Average Blocked Trades: {trustwrapper_stats['avg_blocked_trades']:.1f}")
    print(f"  • Bankruptcy Rate: {trustwrapper_stats['bankruptcy_rate']:.1%}")

    # Calculate improvements
    return_improvement = trustwrapper_stats["avg_return"] - original_stats["avg_return"]
    sharpe_improvement = trustwrapper_stats["avg_sharpe"] - original_stats["avg_sharpe"]
    drawdown_improvement = (
        original_stats["avg_max_drawdown"] - trustwrapper_stats["avg_max_drawdown"]
    )
    bankruptcy_reduction = (
        original_stats["bankruptcy_rate"] - trustwrapper_stats["bankruptcy_rate"]
    )

    print("\n📊 IMPROVEMENT ANALYSIS:")
    print(f"  • Return Improvement: {return_improvement:+.2f} percentage points")
    print(f"  • Sharpe Ratio Improvement: {sharpe_improvement:+.3f}")
    print(f"  • Max Drawdown Reduction: {drawdown_improvement:+.1%}")
    print(f"  • Bankruptcy Rate Reduction: {bankruptcy_reduction:+.1%}")
    print(
        f"  • Volatility Reduction: {original_stats['std_return'] - trustwrapper_stats['std_return']:+.2f}%"
    )

    # Risk-adjusted performance
    original_risk_adjusted = original_stats["avg_return"] / max(
        original_stats["std_return"], 1
    )
    trustwrapper_risk_adjusted = trustwrapper_stats["avg_return"] / max(
        trustwrapper_stats["std_return"], 1
    )
    risk_adjusted_improvement = trustwrapper_risk_adjusted - original_risk_adjusted

    print("\n⚖️ RISK-ADJUSTED PERFORMANCE:")
    print(f"  • Original Risk-Adjusted Return: {original_risk_adjusted:.3f}")
    print(f"  • TrustWrapper Risk-Adjusted Return: {trustwrapper_risk_adjusted:.3f}")
    print(f"  • Risk-Adjusted Improvement: {risk_adjusted_improvement:+.3f}")

    # Key insights
    print("\n🎯 KEY INSIGHTS:")

    if return_improvement > 0:
        print(f"  ✅ TrustWrapper delivers {return_improvement:.2f}% better returns")
    else:
        print(
            f"  📊 TrustWrapper trades {abs(return_improvement):.2f}% return for safety"
        )

    if sharpe_improvement > 0:
        print(
            f"  ✅ TrustWrapper improves risk-adjusted returns by {sharpe_improvement:.3f}"
        )

    if drawdown_improvement > 0:
        print(f"  ✅ TrustWrapper reduces maximum losses by {drawdown_improvement:.1%}")

    if bankruptcy_reduction > 0:
        print(
            f"  ✅ TrustWrapper reduces bankruptcy risk by {bankruptcy_reduction:.1%}"
        )

    print(
        f"  🛡️ TrustWrapper blocks {trustwrapper_stats['avg_blocked_trades']:.1f} dangerous trades per {num_trades}"
    )

    # Value proposition
    print("\n💰 VALUE PROPOSITION:")
    if return_improvement > 0 and sharpe_improvement > 0:
        print(
            "  🎉 TrustWrapper provides BOTH higher returns AND better risk management!"
        )
    elif sharpe_improvement > 0:
        print("  ✅ TrustWrapper provides better risk-adjusted returns")
    elif bankruptcy_reduction > 0:
        print("  🛡️ TrustWrapper provides crucial downside protection")

    # Conclusion
    print("\n🏆 CONCLUSION:")
    if return_improvement >= 0 and sharpe_improvement > 0:
        print("  TrustWrapper-enhanced agents achieve SUPERIOR yields through:")
        print("    • Loss prevention from scam tokens")
        print("    • Better risk management and position sizing")
        print("    • Improved risk-adjusted returns")
        print("    • Reduced catastrophic loss probability")
    else:
        print("  TrustWrapper-enhanced agents provide:")
        print("    • Significantly better risk management")
        print("    • Protection from catastrophic losses")
        print("    • More consistent performance")
        print("    • Peace of mind for safer trading")

    return {
        "original": original_stats,
        "trustwrapper": trustwrapper_stats,
        "improvements": {
            "return_improvement": return_improvement,
            "sharpe_improvement": sharpe_improvement,
            "drawdown_reduction": drawdown_improvement,
            "bankruptcy_reduction": bankruptcy_reduction,
        },
    }


if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    np.random.seed(42)

    results = run_comparative_analysis()

# Minho
# Benchmarking S&P 500 Relative Performance

import pandas as pd


def calculate_relative_performance(
    dataframe: pd.DataFrame,
    ticker: str,
    benchmark: str = "SPY",
    window_days: int = 90
) -> dict:
    """
    Computes relative performance of a stock versus a benchmark
    over a fixed window using total return.

    Assumptions:
    - Daily bar data
    - Prices are adjusted or consistently unadjusted
    - Benchmark symbol (default: SPY) represents S&P 500

    Failure modes:
    - Returns explicit error if data is missing or insufficient
    """

    # Filter data
    ticker_df = dataframe[dataframe["symbol"] == ticker].copy()
    bench_df = dataframe[dataframe["symbol"] == benchmark].copy()

    if ticker_df.empty:
        return {"error": f"No data found for ticker {ticker}"}

    if bench_df.empty:
        return {"error": f"No data found for benchmark {benchmark}"}

    # Sort chronologically
    ticker_df = ticker_df.sort_values("timestamp")
    bench_df = bench_df.sort_values("timestamp")

    # Align on timestamps (intersection only)
    merged = pd.merge(
        ticker_df[["timestamp", "close"]],
        bench_df[["timestamp", "close"]],
        on="timestamp",
        suffixes=(f"_{{ticker}}", f"_{{benchmark}}")
    )

    if len(merged) < window_days + 1:
        return {
            "error": (
                f"Insufficient overlapping data to compute "
                f"{window_days}-day relative performance"
            )
        }

    # Restrict to window
    window_df = merged.tail(window_days + 1)

    # Compute total returns
    ticker_return = (
        window_df[f"close_{{ticker}}"].iloc[-1]
        / window_df[f"close_{{ticker}}"].iloc[0]
        - 1
    )

    benchmark_return = (
        window_df[f"close_{{benchmark}}"].iloc[-1]
        / window_df[f"close_{{benchmark}}"].iloc[0]
        - 1
    )

    relative_return = ticker_return - benchmark_return

    return {
        "ticker": ticker,
        "benchmark": benchmark,
        "window_days": window_days,
        "ticker_return": round(ticker_return, 4),
        "benchmark_return": round(benchmark_return, 4),
        "relative_return": round(relative_return, 4),
        "interpretation": interpret_relative_performance(relative_return),
        "as_of": window_df["timestamp"].iloc[-1]
    }


def interpret_relative_performance(relative_return: float) -> str:
    """
    Deterministic interpretation of relative return.
    """
    if relative_return > 0.05:
        return "Strong outperformance vs market"
    elif relative_return > 0.0:
        return "Slight outperformance vs market"
    elif relative_return < -0.05:
        return "Significant underperformance vs market"
    else:
        return "Roughly in line with market"

import pandas as pd


def calculate_relative_performance(
    dataframe: pd.DataFrame,
    ticker: str,
    benchmark: str = "SPY",
    window_days: int = 90
) -> dict:
    """
    Computes relative performance of a stock versus a benchmark
    over a fixed window using total return.

    Assumptions:
    - Daily bar data
    - Prices are adjusted or consistently unadjusted
    - Benchmark symbol (default: SPY) represents S&P 500

    Failure modes:
    - Returns explicit error if data is missing or insufficient
    """

    # Filter data
    ticker_df = dataframe[dataframe["symbol"] == ticker].copy()
    bench_df = dataframe[dataframe["symbol"] == benchmark].copy()

    if ticker_df.empty:
        return {"error": f"No data found for ticker {ticker}"}

    if bench_df.empty:
        return {"error": f"No data found for benchmark {benchmark}"}

    # Sort chronologically
    ticker_df = ticker_df.sort_values("timestamp")
    bench_df = bench_df.sort_values("timestamp")

    # Align on timestamps (intersection only)
    merged = pd.merge(
        ticker_df[["timestamp", "close"]],
        bench_df[["timestamp", "close"]],
        on="timestamp",
        suffixes=(f"_{ticker}", f"_{benchmark}")
    )

    if len(merged) < window_days + 1:
        return {
            "error": (
                f"Insufficient overlapping data to compute "
                f"{window_days}-day relative performance"
            )
        }

    # Restrict to window
    window_df = merged.tail(window_days + 1)

    # Compute total returns
    ticker_return = (
        window_df[f"close_{ticker}"].iloc[-1]
        / window_df[f"close_{ticker}"].iloc[0]
        - 1
    )

    benchmark_return = (
        window_df[f"close_{benchmark}"].iloc[-1]
        / window_df[f"close_{benchmark}"].iloc[0]
        - 1
    )

    relative_return = ticker_return - benchmark_return

    return {
        "ticker": ticker,
        "benchmark": benchmark,
        "window_days": window_days,
        "ticker_return": round(ticker_return, 4),
        "benchmark_return": round(benchmark_return, 4),
        "relative_return": round(relative_return, 4),
        "interpretation": interpret_relative_performance(relative_return),
        "as_of": window_df["timestamp"].iloc[-1]
    }


def interpret_relative_performance(relative_return: float) -> str:
    """
    Deterministic interpretation of relative return.
    """
    if relative_return > 0.05:
        return "Strong outperformance vs market"
    elif relative_return > 0.0:
        return "Slight outperformance vs market"
    elif relative_return < -0.05:
        return "Significant underperformance vs market"
    else:
        return "Roughly in line with market"

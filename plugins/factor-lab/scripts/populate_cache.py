#!/usr/bin/env python3
"""
Cache Pre-population Script

Purpose: Pre-download all historical data for S&P 500 to avoid rate limiting during backtests

Usage:
    python3 scripts/populate_cache.py --universe SP500 --years 10

Timeline:
    - 500 stocks × 2 seconds delay = ~17 minutes minimum
    - With retries and errors: ~30-45 minutes
"""

import os
import sys
import time
import argparse
from datetime import datetime, timedelta
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quant.data_manager import QuantDataManager


def populate_cache(
    universe: str = 'SP500',
    years: int = 10,
    delay: float = 1.5,
    cache_days: int = 365,
    limit: int = None
) -> None:
    """
    Pre-populate cache with historical data

    Args:
        universe: Stock universe (SP500, NASDAQ100, etc.)
        years: Number of years of historical data
        delay: Delay between API calls (seconds)
        cache_days: Cache validity in days (default: 365)
        limit: Limit to first N stocks (for testing, default: None = all)
    """
    print("=" * 80)
    print("CACHE PRE-POPULATION")
    print("=" * 80)
    print(f"\nUniverse: {universe}")
    print(f"Years: {years}")
    print(f"Delay: {delay}s per stock")
    print(f"Cache validity: {cache_days} days")
    print()

    # Initialize data manager
    data_mgr = QuantDataManager()

    # Get universe tickers
    print(f"Fetching {universe} ticker list...")
    tickers = data_mgr.get_universe(universe)

    # Limit to first N stocks if specified (for testing)
    if limit is not None and limit > 0:
        tickers = tickers[:limit]
        print(f"✓ Found {len(tickers)} tickers (limited to first {limit} for testing)\n")
    else:
        print(f"✓ Found {len(tickers)} tickers\n")

    # Calculate date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=years * 365)).strftime('%Y-%m-%d')

    print(f"Date range: {start_date} to {end_date}")
    print(f"Estimated time: {len(tickers) * delay / 60:.1f} minutes")
    print()

    # Download data for each ticker
    success_count = 0
    error_count = 0
    errors = []

    for i, ticker in enumerate(tickers, 1):
        try:
            # Progress indicator
            progress = (i / len(tickers)) * 100
            print(f"[{i}/{len(tickers)}] ({progress:.1f}%) Fetching {ticker}...", end=" ")

            # Fetch and cache data
            hist = data_mgr.get_historical_data(
                ticker,
                start_date,
                end_date,
                force_refresh=True  # Force API call even if cached
            )

            if hist is not None and len(hist) > 0:
                # Update cache validity to 365 days
                data_mgr._update_cache_validity(ticker, cache_days)
                print(f"✓ {len(hist)} days")
                success_count += 1
            else:
                print(f"⚠ No data")
                error_count += 1
                errors.append(f"{ticker}: No data available")

            # Rate limiting delay
            if i < len(tickers):  # Don't delay after last ticker
                time.sleep(delay)

        except Exception as e:
            print(f"✗ Error: {e}")
            error_count += 1
            errors.append(f"{ticker}: {e}")
            time.sleep(delay)  # Still delay on error
            continue

    # Summary
    print()
    print("=" * 80)
    print("CACHE PRE-POPULATION COMPLETE")
    print("=" * 80)
    print(f"\nSuccessful: {success_count}/{len(tickers)} ({success_count/len(tickers)*100:.1f}%)")
    print(f"Errors: {error_count}/{len(tickers)} ({error_count/len(tickers)*100:.1f}%)")

    if errors:
        print(f"\n{len(errors)} Errors:")
        for error in errors[:10]:  # Show first 10
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")

    # Get cache location
    import os
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    db_path = os.path.join(cache_dir, 'market_data_cache.db')

    print(f"\nCache location: {db_path}")
    print(f"Cache validity: {cache_days} days")
    print("\n✓ Backtests can now run without rate limiting!")


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Pre-populate historical data cache",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with 10 stocks first
  python3 scripts/populate_cache.py --universe SP500 --years 10 --limit 10

  # Populate S&P 500 with 10 years of data
  python3 scripts/populate_cache.py --universe SP500 --years 10

  # Populate NASDAQ 100 with 5 years
  python3 scripts/populate_cache.py --universe NASDAQ100 --years 5 --delay 2.0
        """
    )

    parser.add_argument(
        '--universe',
        type=str,
        default='SP500',
        choices=['SP500', 'NASDAQ100', 'KOSPI200', 'KOSDAQ150'],
        help='Stock universe to populate (default: SP500)'
    )

    parser.add_argument(
        '--years',
        type=int,
        default=10,
        help='Number of years of historical data (default: 10)'
    )

    parser.add_argument(
        '--delay',
        type=float,
        default=1.5,
        help='Delay between API calls in seconds (default: 1.5)'
    )

    parser.add_argument(
        '--cache-days',
        type=int,
        default=365,
        help='Cache validity in days (default: 365)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit to first N stocks (for testing, default: None = all)'
    )

    args = parser.parse_args()

    # Run cache population
    populate_cache(
        universe=args.universe,
        years=args.years,
        delay=args.delay,
        cache_days=args.cache_days,
        limit=args.limit
    )


if __name__ == '__main__':
    main()

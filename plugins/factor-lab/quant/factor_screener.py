#!/usr/bin/env python3
"""
Factor Screener CLI for factor-lab

Multi-factor stock screening tool based on Fama-French 5-Factor Model.

Usage:
    python3 factor_screener.py \
        --universe SP500 \
        --factors value:0.3,quality:0.4,momentum:0.3 \
        --top-n 50 \
        --output screener_results.csv

Features:
- Universe screening (S&P 500, KOSPI 200, NASDAQ 100)
- Multi-factor scoring (Value, Quality, Momentum, Low Vol, Size)
- Customizable factor weights
- CSV/JSON export
- Sector breakdown
"""

import os
import sys
import argparse
import json
from datetime import datetime
from typing import Dict, List
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quant.data_manager import QuantDataManager
from quant.factor_calculator import FactorCalculator
from utils.dashboard_generator import generate_screening_dashboard


def get_output_dir() -> str:
    """Get the default output directory for factor-lab results"""
    # Get project root (3 levels up from this file)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    output_dir = os.path.join(project_root, 'tempo', 'factor-lab')

    # Create directories if they don't exist
    os.makedirs(os.path.join(output_dir, 'dashboards'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'screenings'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'backtests'), exist_ok=True)

    return output_dir


def parse_factor_weights(factors_str: str) -> Dict[str, float]:
    """
    Parse factor weights from command-line string

    Args:
        factors_str: "value:0.3,quality:0.4,momentum:0.3"

    Returns:
        Dict: {'value': 0.3, 'quality': 0.4, 'momentum': 0.3}
    """
    weights = {}

    for factor_weight in factors_str.split(','):
        factor, weight = factor_weight.split(':')
        factor = factor.strip().lower()

        # Map common variations
        if factor in ['value', 'val', 'v']:
            weights['value'] = float(weight)
        elif factor in ['quality', 'qual', 'q']:
            weights['quality'] = float(weight)
        elif factor in ['momentum', 'mom', 'm']:
            weights['momentum'] = float(weight)
        elif factor in ['low_volatility', 'low_vol', 'lv', 'lowvol']:
            weights['low_volatility'] = float(weight)
        elif factor in ['size', 's']:
            weights['size'] = float(weight)
        else:
            raise ValueError(f"Unknown factor: {factor}")

    # Validate weights sum to 1.0 (±0.01 tolerance)
    total = sum(weights.values())
    if abs(total - 1.0) > 0.01:
        print(f"Warning: Factor weights sum to {total:.2f} (expected 1.0)")

    return weights


def screen_stocks(
    universe: str,
    factor_weights: Dict[str, float],
    min_score: float = 0,
    max_results: int = None
) -> List[Dict]:
    """
    Screen stocks using multi-factor scoring

    Args:
        universe: Universe name (SP500, KOSPI200, NASDAQ100)
        factor_weights: Factor weights dict
        min_score: Minimum composite score threshold
        max_results: Maximum number of results (None = all)

    Returns:
        List of stock dicts sorted by composite score
    """
    data_mgr = QuantDataManager()
    calc = FactorCalculator()

    # Load universe
    print(f"\n{'='*60}")
    print(f"Factor Screening: {universe}")
    print(f"{'='*60}\n")

    print(f"Factor Weights:")
    for factor, weight in factor_weights.items():
        print(f"  {factor.capitalize():15s}: {weight:.1%}")
    print()

    tickers = data_mgr.get_universe(universe)
    print(f"Universe size: {len(tickers)} tickers\n")

    # Calculate scores for each ticker
    results = []
    errors = 0

    print("Calculating factor scores...")
    for i, ticker in enumerate(tickers, 1):
        try:
            # Progress indicator
            if i % 50 == 0 or i == len(tickers):
                print(f"  Progress: {i}/{len(tickers)} ({i/len(tickers)*100:.1f}%)")

            score_data = calc.calculate_composite_score(ticker, factor_weights)

            if score_data and score_data['composite_score'] >= min_score:
                results.append(score_data)

        except Exception as e:
            errors += 1
            if errors <= 5:  # Only show first 5 errors
                print(f"  Error processing {ticker}: {e}")

    if errors > 5:
        print(f"  ... and {errors - 5} more errors")

    # Sort by composite score (descending)
    results.sort(key=lambda x: x['composite_score'], reverse=True)

    # Limit results
    if max_results:
        results = results[:max_results]

    print(f"\nScreening complete: {len(results)} stocks passed (min score: {min_score})")
    print(f"Errors encountered: {errors}\n")

    return results


def display_results(results: List[Dict], top_n: int = 20):
    """Display screening results in terminal"""

    if not results:
        print("No stocks found matching criteria.")
        return

    print(f"{'='*60}")
    print(f"Top {min(top_n, len(results))} Stocks by Composite Score")
    print(f"{'='*60}\n")

    # Table header
    header = f"{'Rank':<5} {'Ticker':<8} {'Score':<7} {'Value':<7} {'Quality':<7} {'Momentum':<7} {'Sector':<20} {'Price':<10}"
    print(header)
    print('-' * len(header))

    # Display top N results
    for i, stock in enumerate(results[:top_n], 1):
        ticker = stock['ticker']
        comp = stock['composite_score']
        val = stock['value_score']
        qual = stock['quality_score']
        mom = stock['momentum_score']
        sector = stock['sector'][:18] if stock['sector'] else 'Unknown'
        price = stock['price']

        price_str = f"${price:.2f}" if price else "N/A"

        print(f"{i:<5} {ticker:<8} {comp:<7.1f} {val:<7.1f} {qual:<7.1f} {mom:<7.1f} {sector:<20} {price_str:<10}")

    print()

    # Sector breakdown
    print(f"{'='*60}")
    print("Sector Breakdown (Top {})".format(min(top_n, len(results))))
    print(f"{'='*60}\n")

    sector_counts = {}
    for stock in results[:top_n]:
        sector = stock['sector'] or 'Unknown'
        sector_counts[sector] = sector_counts.get(sector, 0) + 1

    for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sector:<30s}: {count:>3} stocks")

    print()


def save_results(results: List[Dict], output_path: str):
    """Save screening results to file (CSV or JSON)"""

    if not results:
        print("No results to save.")
        return

    # Determine format from file extension
    _, ext = os.path.splitext(output_path)

    if ext.lower() == '.json':
        # Save as JSON
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✓ Results saved to {output_path} (JSON format)")

    else:
        # Save as CSV (default)
        df = pd.DataFrame(results)

        # Reorder columns for readability
        cols = ['ticker', 'name', 'sector', 'price', 'market_cap',
                'composite_score', 'grade',
                'value_score', 'quality_score', 'momentum_score',
                'low_vol_score', 'size_score',
                'pe_ratio', 'pb_ratio', 'roe', 'debt_to_equity', 'beta']

        # Only include columns that exist
        cols = [c for c in cols if c in df.columns]
        df = df[cols]

        df.to_csv(output_path, index=False)
        print(f"✓ Results saved to {output_path} (CSV format)")


def main():
    """Main CLI entry point"""

    parser = argparse.ArgumentParser(
        description="Factor-based stock screener",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Screen S&P 500 with balanced weights
  python3 factor_screener.py --universe SP500 --factors value:0.3,quality:0.4,momentum:0.3

  # Focus on quality and momentum
  python3 factor_screener.py --universe SP500 --factors quality:0.6,momentum:0.4 --top-n 30

  # High score filter
  python3 factor_screener.py --universe NASDAQ100 --factors value:0.5,quality:0.5 --min-score 70

  # Export to JSON
  python3 factor_screener.py --universe SP500 --factors value:1.0 --output results.json
        """
    )

    parser.add_argument(
        '--universe',
        type=str,
        choices=['SP500', 'NASDAQ100', 'KOSPI200', 'KOSDAQ150'],
        default='SP500',
        help='Stock universe to screen (default: SP500)'
    )

    parser.add_argument(
        '--factors',
        type=str,
        required=True,
        help='Factor weights (e.g., "value:0.3,quality:0.4,momentum:0.3")'
    )

    parser.add_argument(
        '--min-score',
        type=float,
        default=0,
        help='Minimum composite score threshold (0-100, default: 0)'
    )

    parser.add_argument(
        '--top-n',
        type=int,
        default=50,
        help='Number of top stocks to display/save (default: 50)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output file path (CSV or JSON, default: tempo/factor-lab/screenings/screening_YYYYMMDD.csv)'
    )

    parser.add_argument(
        '--display',
        type=int,
        default=20,
        help='Number of stocks to display in terminal (default: 20)'
    )

    parser.add_argument(
        '--html',
        type=str,
        default=None,
        help='Generate HTML dashboard (default: tempo/factor-lab/dashboards/screening_YYYYMMDD.html)'
    )

    args = parser.parse_args()

    try:
        # Get output directory
        output_dir = get_output_dir()
        timestamp = datetime.now().strftime('%Y%m%d')

        # Set default output paths if not specified
        if args.output is None:
            args.output = os.path.join(output_dir, 'screenings', f'screening_{timestamp}.csv')

        # Generate HTML by default
        if args.html is None:
            args.html = os.path.join(output_dir, 'dashboards', f'screening_{timestamp}.html')

        # Parse factor weights
        factor_weights = parse_factor_weights(args.factors)

        # Screen stocks
        results = screen_stocks(
            universe=args.universe,
            factor_weights=factor_weights,
            min_score=args.min_score,
            max_results=args.top_n
        )

        # Display results
        display_results(results, top_n=args.display)

        # Save results
        save_results(results, args.output)

        # Generate HTML dashboard
        if args.html:
            print(f"\nGenerating HTML dashboard...")
            df = pd.DataFrame(results)

            metadata = {
                'universe': args.universe,
                'factors': args.factors,
                'total_screened': len(results),
                'min_score': args.min_score
            }

            html_path = generate_screening_dashboard(
                results_df=df,
                output_path=args.html,
                title=f"factor-lab Screening - {args.universe}",
                metadata=metadata
            )
            print(f"✓ HTML dashboard saved to {html_path}")

        print(f"\n{'='*60}")
        print("Screening Summary")
        print(f"{'='*60}")
        print(f"Universe:        {args.universe}")
        print(f"Total screened:  {len(results)} stocks")
        print(f"Min score:       {args.min_score}")
        print(f"Top N saved:     {args.top_n}")
        print(f"Output file:     {args.output}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

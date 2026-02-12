"""
Portfolio Manager - CRUD operations for portfolio management.

Provides functions to:
- Create portfolios
- Add/remove holdings
- List holdings with current prices
- Calculate P&L
- Update positions
"""

import sys
import os
from datetime import datetime, date
from typing import Optional, List, Dict

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

from database import get_database, Portfolio, Holding, Transaction, ScoreHistory
from data_fetcher import get_data_source_manager
from scorecard import CompanyScorecardGenerator


class PortfolioManager:
    """Manages portfolio CRUD operations and position tracking."""

    def __init__(self, db_path=None):
        """
        Initialize portfolio manager.

        Args:
            db_path: Path to SQLite database (default: ../data/portfolio.db)
        """
        self.db = get_database(db_path)
        self.session = self.db.get_session()
        self.data_source = get_data_source_manager()
        self.scorecard_generator = CompanyScorecardGenerator()

    def create_portfolio(self, name: str, base_currency: str = 'USD', target_allocation: Optional[Dict] = None) -> Portfolio:
        """
        Create a new portfolio.

        Args:
            name: Portfolio name
            base_currency: Base currency for portfolio (USD or KRW)
            target_allocation: Target sector allocation (e.g., {'Technology': 0.30, 'Healthcare': 0.20})

        Returns:
            Created Portfolio object
        """
        portfolio = Portfolio(
            name=name,
            base_currency=base_currency,
            target_allocation=target_allocation or {}
        )
        self.session.add(portfolio)
        self.session.commit()
        return portfolio

    def get_portfolio(self, portfolio_id: Optional[int] = None, name: Optional[str] = None) -> Optional[Portfolio]:
        """
        Get portfolio by ID or name.

        Args:
            portfolio_id: Portfolio ID
            name: Portfolio name

        Returns:
            Portfolio object or None
        """
        if portfolio_id:
            return self.session.query(Portfolio).filter_by(id=portfolio_id).first()
        elif name:
            return self.session.query(Portfolio).filter_by(name=name).first()
        else:
            # Return first portfolio if exists
            return self.session.query(Portfolio).first()

    def list_portfolios(self) -> List[Portfolio]:
        """
        List all portfolios.

        Returns:
            List of Portfolio objects
        """
        return self.session.query(Portfolio).all()

    def add_holding(
        self,
        portfolio_id: int,
        ticker: str,
        quantity: float,
        avg_price: float,
        notes: Optional[str] = None
    ) -> Holding:
        """
        Add a new holding to portfolio.

        Args:
            portfolio_id: Portfolio ID
            ticker: Stock ticker symbol
            quantity: Number of shares
            avg_price: Average purchase price
            notes: Optional notes

        Returns:
            Created Holding object
        """
        # Detect market and currency
        market = self.data_source.detect_market(ticker)
        currency = 'USD' if market == 'US' else 'KRW'

        # Get stock info to determine sector
        stock_info = self.data_source.get_stock_info(ticker)
        sector = stock_info.get('sector', 'Unknown') if 'error' not in stock_info else 'Unknown'

        # Check if holding already exists
        existing = self.session.query(Holding).filter_by(
            portfolio_id=portfolio_id,
            ticker=ticker
        ).first()

        if existing:
            # Update existing holding
            total_cost = (existing.quantity * existing.avg_price) + (quantity * avg_price)
            existing.quantity += quantity
            existing.avg_price = total_cost / existing.quantity
            self.session.commit()
            return existing
        else:
            # Create new holding
            holding = Holding(
                portfolio_id=portfolio_id,
                ticker=ticker,
                market=market,
                quantity=quantity,
                avg_price=avg_price,
                currency=currency,
                sector=sector,
                notes=notes
            )
            self.session.add(holding)
            self.session.commit()

            # Record transaction
            transaction = Transaction(
                holding_id=holding.id,
                type='BUY',
                date=date.today(),
                quantity=quantity,
                price=avg_price
            )
            self.session.add(transaction)
            self.session.commit()

            return holding

    def remove_holding(self, portfolio_id: int, ticker: str) -> bool:
        """
        Remove a holding from portfolio.

        Args:
            portfolio_id: Portfolio ID
            ticker: Stock ticker symbol

        Returns:
            True if removed, False if not found
        """
        holding = self.session.query(Holding).filter_by(
            portfolio_id=portfolio_id,
            ticker=ticker
        ).first()

        if holding:
            self.session.delete(holding)
            self.session.commit()
            return True
        return False

    def list_holdings(self, portfolio_id: int, with_current_price: bool = True) -> List[Dict]:
        """
        List all holdings in a portfolio with current prices and P&L.

        Args:
            portfolio_id: Portfolio ID
            with_current_price: Fetch current prices from data source

        Returns:
            List of holdings with enriched data
        """
        holdings = self.session.query(Holding).filter_by(portfolio_id=portfolio_id).all()
        result = []

        for holding in holdings:
            holding_data = {
                'ticker': holding.ticker,
                'market': holding.market,
                'quantity': holding.quantity,
                'avg_price': holding.avg_price,
                'currency': holding.currency,
                'sector': holding.sector,
                'notes': holding.notes,
                'added_at': holding.added_at
            }

            if with_current_price:
                # Fetch current price
                stock_info = self.data_source.get_stock_info(holding.ticker)
                if 'error' not in stock_info:
                    current_price = stock_info.get('price', 0)
                    holding_data['current_price'] = current_price
                    holding_data['name'] = stock_info.get('name', holding.ticker)

                    # Calculate P&L
                    cost_basis = holding.quantity * holding.avg_price
                    current_value = holding.quantity * current_price
                    pnl = current_value - cost_basis
                    pnl_pct = (pnl / cost_basis * 100) if cost_basis > 0 else 0

                    holding_data['cost_basis'] = cost_basis
                    holding_data['current_value'] = current_value
                    holding_data['pnl'] = pnl
                    holding_data['pnl_pct'] = pnl_pct
                else:
                    holding_data['error'] = stock_info.get('error', 'Failed to fetch price')

            result.append(holding_data)

        return result

    def get_portfolio_summary(self, portfolio_id: int) -> Dict:
        """
        Get portfolio summary with total value, P&L, and sector allocation.

        Args:
            portfolio_id: Portfolio ID

        Returns:
            Dictionary with portfolio summary
        """
        portfolio = self.get_portfolio(portfolio_id=portfolio_id)
        if not portfolio:
            return {'error': 'Portfolio not found'}

        holdings = self.list_holdings(portfolio_id, with_current_price=True)

        total_cost = sum(h.get('cost_basis', 0) for h in holdings if 'cost_basis' in h)
        total_value = sum(h.get('current_value', 0) for h in holdings if 'current_value' in h)
        total_pnl = total_value - total_cost
        total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0

        # Sector allocation
        sector_allocation = {}
        for h in holdings:
            if 'current_value' in h:
                sector = h.get('sector', 'Unknown')
                sector_allocation[sector] = sector_allocation.get(sector, 0) + h['current_value']

        # Convert to percentages
        sector_pct = {
            sector: (value / total_value * 100) if total_value > 0 else 0
            for sector, value in sector_allocation.items()
        }

        return {
            'portfolio_id': portfolio_id,
            'portfolio_name': portfolio.name,
            'base_currency': portfolio.base_currency,
            'num_holdings': len(holdings),
            'total_cost': total_cost,
            'total_value': total_value,
            'total_pnl': total_pnl,
            'total_pnl_pct': total_pnl_pct,
            'sector_allocation': sector_allocation,
            'sector_allocation_pct': sector_pct,
            'holdings': holdings
        }

    def score_portfolio(self, portfolio_id: int) -> Dict:
        """
        Score all holdings in a portfolio.

        Args:
            portfolio_id: Portfolio ID

        Returns:
            Dictionary with scoring results
        """
        holdings = self.list_holdings(portfolio_id, with_current_price=False)

        results = {
            'portfolio_id': portfolio_id,
            'scored': [],
            'failed': []
        }

        print(f"\n🔄 Scoring {len(holdings)} holdings...")

        for h in holdings:
            ticker = h['ticker']
            try:
                print(f"  Scoring {ticker}...", end=' ')
                scorecard = self.scorecard_generator.calculate_scorecard(ticker)

                if 'error' not in scorecard:
                    # Check if score already exists for today
                    existing_score = self.session.query(ScoreHistory).filter_by(
                        ticker=ticker,
                        date=date.today()
                    ).first()

                    if existing_score:
                        # Update existing score
                        existing_score.total_score = scorecard['total_score']
                        existing_score.financial_score = scorecard['financial_score']
                        existing_score.valuation_score = scorecard['valuation_score']
                        existing_score.momentum_score = scorecard['momentum_score']
                        existing_score.price = scorecard['price']
                    else:
                        # Create new score record
                        score_record = ScoreHistory(
                            ticker=ticker,
                            date=date.today(),
                            total_score=scorecard['total_score'],
                            financial_score=scorecard['financial_score'],
                            valuation_score=scorecard['valuation_score'],
                            momentum_score=scorecard['momentum_score'],
                            price=scorecard['price']
                        )
                        self.session.add(score_record)

                    results['scored'].append({
                        'ticker': ticker,
                        'score': scorecard['total_score'],
                        'grade': scorecard['grade']
                    })
                    print(f"✅ {scorecard['total_score']:.1f}/10 ({scorecard['grade']})")
                else:
                    results['failed'].append({'ticker': ticker, 'error': scorecard['error']})
                    print(f"❌ Failed")

            except Exception as e:
                results['failed'].append({'ticker': ticker, 'error': str(e)})
                print(f"❌ Error: {e}")

        self.session.commit()

        print(f"\n✅ Scored {len(results['scored'])}/{len(holdings)} holdings")
        if results['failed']:
            print(f"❌ Failed: {len(results['failed'])}")

        return results

    def get_latest_scores(self, tickers: List[str]) -> Dict[str, Optional[ScoreHistory]]:
        """
        Get latest scores for multiple tickers.

        Args:
            tickers: List of ticker symbols

        Returns:
            Dictionary mapping ticker to latest ScoreHistory or None
        """
        scores = {}
        for ticker in tickers:
            score = self.session.query(ScoreHistory).filter_by(ticker=ticker).order_by(ScoreHistory.date.desc()).first()
            scores[ticker] = score
        return scores

    def close(self):
        """Close database session."""
        self.session.close()


def main():
    """Command-line interface for portfolio management."""
    import argparse

    parser = argparse.ArgumentParser(description='Investment Analyzer - Portfolio Management')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Create portfolio
    create_parser = subparsers.add_parser('create', help='Create new portfolio')
    create_parser.add_argument('name', help='Portfolio name')
    create_parser.add_argument('--currency', default='USD', choices=['USD', 'KRW'], help='Base currency')

    # List portfolios
    subparsers.add_parser('list', help='List all portfolios')

    # Add holding
    add_parser = subparsers.add_parser('add', help='Add holding to portfolio')
    add_parser.add_argument('ticker', help='Stock ticker (e.g., AAPL, 005930)')
    add_parser.add_argument('quantity', type=float, help='Number of shares')
    add_parser.add_argument('price', type=float, help='Purchase price per share')
    add_parser.add_argument('--portfolio', type=int, help='Portfolio ID (default: first portfolio)')
    add_parser.add_argument('--notes', help='Optional notes')

    # Show holdings
    show_parser = subparsers.add_parser('show', help='Show portfolio holdings')
    show_parser.add_argument('--portfolio', type=int, help='Portfolio ID (default: first portfolio)')
    show_parser.add_argument('--with-scores', action='store_true', help='Show holdings with scores')

    # Score portfolio
    score_parser = subparsers.add_parser('score', help='Score all portfolio holdings')
    score_parser.add_argument('--portfolio', type=int, help='Portfolio ID (default: first portfolio)')

    args = parser.parse_args()

    pm = PortfolioManager()

    try:
        if args.command == 'create':
            portfolio = pm.create_portfolio(args.name, args.currency)
            print(f"✅ Portfolio created: {portfolio.name} (ID: {portfolio.id}, Currency: {portfolio.base_currency})")

        elif args.command == 'list':
            portfolios = pm.list_portfolios()
            if portfolios:
                print(f"📊 Portfolios ({len(portfolios)}):")
                for p in portfolios:
                    print(f"  {p.id}. {p.name} ({p.base_currency})")
            else:
                print("No portfolios found. Create one with: python portfolio_manager.py create 'My Portfolio'")

        elif args.command == 'add':
            portfolio_id = args.portfolio or pm.get_portfolio().id
            holding = pm.add_holding(portfolio_id, args.ticker, args.quantity, args.price, args.notes)
            print(f"✅ Added {args.quantity} shares of {args.ticker} @ {args.price} {holding.currency}")

        elif args.command == 'show':
            portfolio_id = args.portfolio or pm.get_portfolio().id
            summary = pm.get_portfolio_summary(portfolio_id)

            if 'error' in summary:
                print(f"❌ {summary['error']}")
            else:
                print(f"\n{'='*60}")
                print(f"  {summary['portfolio_name']} - Portfolio Summary")
                print(f"{'='*60}")
                print(f"Total Value:  {summary['base_currency']} {summary['total_value']:,.2f}")
                print(f"Total Cost:   {summary['base_currency']} {summary['total_cost']:,.2f}")
                print(f"Total P&L:    {summary['base_currency']} {summary['total_pnl']:,.2f} ({summary['total_pnl_pct']:+.2f}%)")
                print(f"Holdings:     {summary['num_holdings']} stocks")

                if args.with_scores:
                    # Get scores for all tickers
                    tickers = [h['ticker'] for h in summary['holdings']]
                    scores = pm.get_latest_scores(tickers)

                    print(f"\n{'Ticker':<10} {'Shares':<10} {'Current':<12} {'P&L %':<10} {'Score':<10} {'Grade':<15} {'Sector':<15}")
                    print("-" * 95)

                    for h in summary['holdings']:
                        score_record = scores.get(h['ticker'])
                        score_str = f"{score_record.total_score:.1f}/10" if score_record else "N/A"
                        grade_str = pm.scorecard_generator._get_grade(score_record.total_score) if score_record else "N/A"

                        if 'current_price' in h:
                            print(f"{h['ticker']:<10} {h['quantity']:<10.2f} {h['current_price']:<12.2f} {h['pnl_pct']:>+9.2f}% {score_str:<10} {grade_str:<15} {h.get('sector', 'N/A'):<15}")
                        else:
                            print(f"{h['ticker']:<10} {h['quantity']:<10.2f} {'N/A':<12} {'N/A':<10} {score_str:<10} {grade_str:<15} {h.get('sector', 'N/A'):<15}")
                else:
                    print(f"\n{'Ticker':<10} {'Shares':<10} {'Avg Price':<12} {'Current':<12} {'P&L %':<10} {'Sector':<15}")
                    print("-" * 80)

                    for h in summary['holdings']:
                        if 'current_price' in h:
                            print(f"{h['ticker']:<10} {h['quantity']:<10.2f} {h['avg_price']:<12.2f} {h['current_price']:<12.2f} {h['pnl_pct']:>+9.2f}% {h.get('sector', 'N/A'):<15}")
                        else:
                            print(f"{h['ticker']:<10} {h['quantity']:<10.2f} {h['avg_price']:<12.2f} {'N/A':<12} {'N/A':<10} {h.get('sector', 'N/A'):<15}")

        elif args.command == 'score':
            portfolio_id = args.portfolio or pm.get_portfolio().id
            results = pm.score_portfolio(portfolio_id)

            if results['scored']:
                print(f"\n📊 Scored Holdings:")
                for item in results['scored']:
                    print(f"  {item['ticker']}: {item['score']:.1f}/10 {item['grade']}")

            if results['failed']:
                print(f"\n❌ Failed to Score:")
                for item in results['failed']:
                    print(f"  {item['ticker']}: {item['error']}")

        else:
            parser.print_help()

    finally:
        pm.close()


if __name__ == '__main__':
    main()

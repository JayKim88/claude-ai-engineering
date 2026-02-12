"""
Database models and schema for Investment Analyzer.

Uses SQLAlchemy ORM for portfolio management, transaction tracking,
performance monitoring, and data caching.
"""

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Text,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

Base = declarative_base()


class Portfolio(Base):
    """Portfolio definition with target allocation settings."""

    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    base_currency = Column(String, default="USD")  # USD or KRW
    target_allocation = Column(JSON)  # {"Technology": 0.30, "Healthcare": 0.20, ...}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")
    snapshots = relationship("PortfolioSnapshot", back_populates="portfolio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Portfolio(id={self.id}, name='{self.name}', currency={self.base_currency})>"


class Holding(Base):
    """Individual stock holdings in a portfolio."""

    __tablename__ = "holdings"
    __table_args__ = (
        CheckConstraint("market IN ('US', 'KR')", name="check_market"),
        CheckConstraint("currency IN ('USD', 'KRW')", name="check_currency"),
        UniqueConstraint("portfolio_id", "ticker", name="unique_portfolio_ticker"),
    )

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    ticker = Column(String, nullable=False)
    market = Column(String, nullable=False)  # US or KR
    quantity = Column(Float, nullable=False)
    avg_price = Column(Float, nullable=False)
    currency = Column(String, nullable=False)  # USD or KRW
    sector = Column(String)  # Technology, Healthcare, etc.
    notes = Column(Text)
    added_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")
    transactions = relationship("Transaction", back_populates="holding", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Holding(ticker='{self.ticker}', qty={self.quantity}, price={self.avg_price} {self.currency})>"


class Transaction(Base):
    """Transaction history for holdings (buy, sell, dividend, split)."""

    __tablename__ = "transactions"
    __table_args__ = (CheckConstraint("type IN ('BUY', 'SELL', 'DIVIDEND', 'SPLIT')", name="check_type"),)

    id = Column(Integer, primary_key=True)
    holding_id = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    type = Column(String, nullable=False)  # BUY, SELL, DIVIDEND, SPLIT
    date = Column(Date, nullable=False)
    quantity = Column(Float)  # None for DIVIDEND
    price = Column(Float)  # Price per share
    fees = Column(Float, default=0.0)  # Transaction fees
    exchange_rate = Column(Float)  # For KRW→USD conversion
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    holding = relationship("Holding", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(type='{self.type}', date={self.date}, qty={self.quantity}, price={self.price})>"


class PortfolioSnapshot(Base):
    """Daily portfolio snapshots for performance tracking."""

    __tablename__ = "portfolio_snapshots"
    __table_args__ = (UniqueConstraint("portfolio_id", "date", name="unique_portfolio_date"),)

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    date = Column(Date, nullable=False)
    total_value_usd = Column(Float)  # Total portfolio value in USD
    daily_return_pct = Column(Float)  # Daily return percentage
    total_return_pct = Column(Float)  # Total return since inception
    holdings_json = Column(Text)  # JSON snapshot of all holdings

    # Relationships
    portfolio = relationship("Portfolio", back_populates="snapshots")

    def __repr__(self):
        return f"<PortfolioSnapshot(date={self.date}, value=${self.total_value_usd:.2f}, return={self.total_return_pct}%)>"


class ScoreHistory(Base):
    """Historical stock scores for backtesting and trend analysis."""

    __tablename__ = "score_history"

    ticker = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    financial_score = Column(Float)
    valuation_score = Column(Float)
    momentum_score = Column(Float)
    total_score = Column(Float)
    price = Column(Float)  # Stock price at time of scoring

    def __repr__(self):
        return f"<ScoreHistory(ticker='{self.ticker}', date={self.date}, score={self.total_score:.2f})>"


class DataCache(Base):
    """Cache for external API responses to minimize API calls."""

    __tablename__ = "data_cache"

    key = Column(String, primary_key=True)  # e.g., "stock_info:AAPL"
    value = Column(Text)  # JSON-serialized data
    source = Column(String)  # 'mcp_usstock', 'yfinance', 'pykrx'
    fetched_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    def __repr__(self):
        return f"<DataCache(key='{self.key}', source='{self.source}', expires={self.expires_at})>"


# Database connection and session management
class Database:
    """Database manager for Investment Analyzer."""

    def __init__(self, db_path=None):
        if db_path is None:
            # Default to plugins/investment-analyzer/data/portfolio.db
            db_dir = os.path.join(os.path.dirname(__file__), "..", "data")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "portfolio.db")

        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables if they don't exist."""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get a new database session."""
        return self.Session()

    def drop_all_tables(self):
        """Drop all tables (use with caution!)."""
        Base.metadata.drop_all(self.engine)


# Convenience function for getting a database instance
def get_database(db_path=None):
    """Get a Database instance and create tables if needed."""
    db = Database(db_path)
    db.create_tables()
    return db


if __name__ == "__main__":
    # Test database creation
    print("Creating Investment Analyzer database...")
    db = get_database()
    print(f"✅ Database created successfully!")
    print(f"📊 Tables: {Base.metadata.tables.keys()}")

    # Create a test session
    session = db.get_session()
    print(f"✅ Session created: {session}")
    session.close()

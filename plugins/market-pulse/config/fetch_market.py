#!/usr/bin/env python3
"""
Market Data Fetcher
Fetches financial market data from free sources (yfinance, pykrx, RSS)
"""

import json
import yaml
import sys
import os
import argparse
import re
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from pathlib import Path
import pandas as pd

# Import MarketHistoryDB for historical data storage
sys.path.append(str(Path(__file__).parent.parent / "data"))
from market_history import MarketHistoryDB


class MarketDataFetcher:
    """Fetches market data from multiple free sources."""

    def __init__(self, config_path: str = None, watchlist_path: str = None, use_db: bool = True):
        if config_path is None:
            config_path = Path(__file__).parent / "sources.yaml"
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.watchlist = {}
        if watchlist_path is None:
            watchlist_path = Path(__file__).parent / "watchlist.yaml"
        if Path(watchlist_path).exists():
            with open(watchlist_path, 'r') as f:
                self.watchlist = yaml.safe_load(f) or {}

        # Initialize MarketHistoryDB for 60-day data storage
        self.use_db = use_db
        self.db = MarketHistoryDB() if use_db else None
        print(f"📊 MarketHistoryDB {'enabled' if use_db else 'disabled'}", file=sys.stderr)

    # ──────────────────────────────────────────────
    # Market Status
    # ──────────────────────────────────────────────

    def get_market_status(self) -> Dict[str, Any]:
        """Check if US and KR markets are currently open."""
        try:
            from zoneinfo import ZoneInfo
        except ImportError:
            from backports.zoneinfo import ZoneInfo

        now_utc = datetime.now(ZoneInfo("UTC"))

        # US Market
        eastern = ZoneInfo("US/Eastern")
        now_et = now_utc.astimezone(eastern)
        us_open = (now_et.weekday() < 5
                   and ((now_et.hour == 9 and now_et.minute >= 30) or (10 <= now_et.hour < 16)))

        # Korean Market
        seoul = ZoneInfo("Asia/Seoul")
        now_kst = now_utc.astimezone(seoul)
        kr_open = (now_kst.weekday() < 5
                   and ((9 <= now_kst.hour < 15) or (now_kst.hour == 15 and now_kst.minute <= 30)))

        return {
            "us_open": us_open,
            "kr_open": kr_open,
            "us_note": "" if us_open else f"Closed ({now_et.strftime('%H:%M')} ET)",
            "kr_note": "" if kr_open else f"장 마감 ({now_kst.strftime('%H:%M')} KST)",
            "timestamp": now_utc.isoformat(),
        }

    # ──────────────────────────────────────────────
    # US Market
    # ──────────────────────────────────────────────

    def fetch_us_indices(self) -> Dict[str, Any]:
        """Fetch major US indices with 60-day historical data storage."""
        import yfinance as yf

        result = {}
        for symbol, name in self.config["us_indices"].items():
            try:
                ticker = yf.Ticker(symbol)

                # Fetch 60 days for historical analysis (changed from 5d)
                hist = ticker.history(period="60d")
                if hist.empty:
                    result[symbol] = {"name": name, "error": "No data"}
                    continue

                # Save to database if enabled
                if self.use_db and self.db:
                    for date_idx, row in hist.iterrows():
                        date_str = date_idx.strftime('%Y-%m-%d')
                        ohlcv = {
                            'open': float(row['Open']),
                            'high': float(row['High']),
                            'low': float(row['Low']),
                            'close': float(row['Close']),
                            'volume': int(row['Volume']),
                            'adj_close': float(row['Close'])
                        }
                        self.db.save_daily_prices(symbol, date_str, ohlcv)

                    # Calculate and save multi-period returns
                    self.db.calculate_and_save_returns(symbol)

                # Return current values (maintain backward compatibility)
                current = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2] if len(hist) >= 2 else current
                change = current - prev
                change_pct = (change / prev * 100) if prev else 0
                result[symbol] = {
                    "name": name,
                    "value": round(current, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}", file=sys.stderr)
                result[symbol] = {"name": name, "error": str(e)}
        return result

    def fetch_us_sectors(self) -> List[Dict[str, Any]]:
        """Fetch sector ETF performance with 60-day historical data storage."""
        import yfinance as yf

        results = []
        symbols = [s["symbol"] for s in self.config["us_sector_etfs"]]
        names = {s["symbol"]: s["name"] for s in self.config["us_sector_etfs"]}

        try:
            # Changed from 1mo to 2mo for 60-day data
            data = yf.download(symbols, period="2mo", progress=False, group_by="ticker")
        except Exception as e:
            print(f"Error downloading sector ETFs: {e}", file=sys.stderr)
            return results

        for etf in self.config["us_sector_etfs"]:
            sym = etf["symbol"]
            try:
                if len(symbols) == 1:
                    hist_df = data
                else:
                    hist_df = data[sym]

                # Save to database if enabled
                if self.use_db and self.db:
                    for date_idx in hist_df.index:
                        if pd.notna(hist_df.loc[date_idx, "Close"]):
                            date_str = date_idx.strftime('%Y-%m-%d')
                            ohlcv = {
                                'open': float(hist_df.loc[date_idx, "Open"]),
                                'high': float(hist_df.loc[date_idx, "High"]),
                                'low': float(hist_df.loc[date_idx, "Low"]),
                                'close': float(hist_df.loc[date_idx, "Close"]),
                                'volume': int(hist_df.loc[date_idx, "Volume"]),
                                'adj_close': float(hist_df.loc[date_idx, "Close"])
                            }
                            self.db.save_daily_prices(sym, date_str, ohlcv)

                    # Calculate and save multi-period returns
                    self.db.calculate_and_save_returns(sym)

                # Calculate returns for display (maintain backward compatibility)
                close = hist_df["Close"].dropna()
                if close.empty:
                    continue
                current = close.iloc[-1]
                change_1d = _pct_change(close, 1)
                change_1w = _pct_change(close, 5)
                change_1m = _pct_change(close, len(close) - 1)
                results.append({
                    "symbol": sym,
                    "name": etf["name"],
                    "price": round(current, 2),
                    "change_1d": change_1d,
                    "change_1w": change_1w,
                    "change_1m": change_1m,
                })
            except Exception as e:
                print(f"Error processing {sym}: {e}", file=sys.stderr)
                continue
        # Sort by 1d performance
        results.sort(key=lambda x: x.get("change_1d", 0), reverse=True)
        return results

    # ──────────────────────────────────────────────
    # Korean Market
    # ──────────────────────────────────────────────

    def fetch_kr_indices(self) -> Dict[str, Any]:
        """Fetch KOSPI and KOSDAQ indices via pykrx."""
        from pykrx import stock as krx

        result = {}
        today = date.today()
        # pykrx needs trading days — go back up to 10 days to find data
        start = today - timedelta(days=10)
        fmt = "%Y%m%d"

        for idx_name, idx_code in [("kospi", "1001"), ("kosdaq", "2001")]:
            try:
                df = krx.get_index_ohlcv(start.strftime(fmt), today.strftime(fmt), idx_code)
                if df.empty:
                    result[idx_name] = {"error": "No data"}
                    continue
                current = df["종가"].iloc[-1]
                prev = df["종가"].iloc[-2] if len(df) >= 2 else current
                change = current - prev
                change_pct = (change / prev * 100) if prev else 0
                result[idx_name] = {
                    "name": "KOSPI" if idx_name == "kospi" else "KOSDAQ",
                    "value": round(float(current), 2),
                    "change": round(float(change), 2),
                    "change_pct": round(float(change_pct), 2),
                }
            except Exception as e:
                print(f"Error fetching {idx_name}: {e}", file=sys.stderr)
                result[idx_name] = {"error": str(e)}
        return result

    def fetch_kr_foreign_institutional(self) -> Dict[str, Any]:
        """Fetch foreign/institutional net trading data."""
        from pykrx import stock as krx

        today = date.today()
        start = today - timedelta(days=10)
        fmt = "%Y%m%d"
        result = {}

        try:
            # Net buy/sell by investor type for the market
            df = krx.get_market_trading_value_by_date(
                start.strftime(fmt), today.strftime(fmt), "KOSPI"
            )
            if not df.empty:
                latest = df.iloc[-1]
                result["foreign_net_buy"] = int(latest.get("외국인합계", 0))
                result["institutional_net_buy"] = int(latest.get("기관합계", 0))
                result["individual_net_buy"] = int(latest.get("개인", 0))
                result["date"] = str(df.index[-1].date()) if hasattr(df.index[-1], 'date') else str(df.index[-1])
        except Exception as e:
            print(f"Error fetching foreign/institutional data: {e}", file=sys.stderr)
            result["error"] = str(e)

        # Top foreign/institutional net buys by ticker
        try:
            latest_date = today
            for i in range(10):
                d = today - timedelta(days=i)
                try:
                    cap = krx.get_market_cap(d.strftime(fmt))
                    if not cap.empty:
                        latest_date = d
                        break
                except Exception:
                    continue

            df_trade = krx.get_market_net_purchases_of_equities(
                latest_date.strftime(fmt), latest_date.strftime(fmt), "KOSPI", "외국인"
            )
            if not df_trade.empty:
                top_buys = df_trade.head(5)
                result["top_foreign_buys"] = [
                    {"ticker": idx, "name": row.get("종목명", ""), "net_buy": int(row.get("순매수거래량", 0))}
                    for idx, row in top_buys.iterrows()
                ]
        except Exception as e:
            print(f"Error fetching top foreign buys: {e}", file=sys.stderr)

        return result

    def fetch_kr_top_stocks(self) -> List[Dict[str, Any]]:
        """Fetch top Korean stocks by market cap with fundamentals."""
        from pykrx import stock as krx

        today = date.today()
        fmt = "%Y%m%d"
        results = []

        # Find latest trading day
        latest_date = today
        for i in range(10):
            d = today - timedelta(days=i)
            try:
                cap = krx.get_market_cap(d.strftime(fmt), market="KOSPI")
                if not cap.empty and cap["시가총액"].sum() > 0:
                    latest_date = d
                    break
            except Exception:
                continue

        try:
            cap_df = krx.get_market_cap(latest_date.strftime(fmt), market="KOSPI")
            fund_df = krx.get_market_fundamental(latest_date.strftime(fmt), market="KOSPI")
            ohlcv = krx.get_market_ohlcv(latest_date.strftime(fmt), market="KOSPI")

            if cap_df.empty:
                return results

            # Filter out zero market cap and get top 10
            cap_df = cap_df[cap_df["시가총액"] > 0]
            top10 = cap_df.nlargest(10, "시가총액")

            for ticker in top10.index:
                try:
                    name = krx.get_market_ticker_name(ticker)
                    price = int(ohlcv.loc[ticker, "종가"]) if ticker in ohlcv.index else 0
                    change_pct = float(ohlcv.loc[ticker, "등락률"]) if ticker in ohlcv.index else 0
                    per = float(fund_df.loc[ticker, "PER"]) if ticker in fund_df.index else None
                    pbr = float(fund_df.loc[ticker, "PBR"]) if ticker in fund_df.index else None
                    div_yield = float(fund_df.loc[ticker, "DIV"]) if ticker in fund_df.index else None

                    results.append({
                        "ticker": ticker,
                        "name": name,
                        "price": price,
                        "change_pct": round(change_pct, 2),
                        "market_cap_krw": int(cap_df.loc[ticker, "시가총액"]),
                        "per": round(per, 2) if per else None,
                        "pbr": round(pbr, 2) if pbr else None,
                        "div_yield": round(div_yield, 2) if div_yield else None,
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"Error fetching KR top stocks: {e}", file=sys.stderr)

        return results

    # ──────────────────────────────────────────────
    # Global Macro
    # ──────────────────────────────────────────────

    def fetch_treasury_yields(self) -> Dict[str, Any]:
        """Fetch US treasury yields and spread."""
        import yfinance as yf

        result = {}
        for symbol, name in self.config["treasury_yields"].items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="5d")
                if hist.empty:
                    continue
                value = round(float(hist["Close"].iloc[-1]), 3)
                result[name] = value
            except Exception as e:
                print(f"Error fetching {symbol}: {e}", file=sys.stderr)

        # Yield curve spread (10Y - 5Y as proxy if 2Y unavailable)
        ten_y = result.get("10-Year")
        five_y = result.get("5-Year")
        if ten_y and five_y:
            result["spread_10y_5y"] = round(ten_y - five_y, 3)

        return result

    def fetch_commodities(self) -> Dict[str, Any]:
        """Fetch commodity prices."""
        import yfinance as yf

        result = {}
        for symbol, name in self.config["commodities"].items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="5d")
                if hist.empty:
                    continue
                current = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2] if len(hist) >= 2 else current
                change_pct = ((current - prev) / prev * 100) if prev else 0
                result[name] = {
                    "price": round(float(current), 2),
                    "change_pct": round(float(change_pct), 2),
                }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}", file=sys.stderr)
        return result

    def fetch_currencies(self) -> Dict[str, Any]:
        """Fetch currency pairs and dollar index."""
        import yfinance as yf

        result = {}
        for symbol, name in self.config["currencies"].items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="5d")
                if hist.empty:
                    continue
                current = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2] if len(hist) >= 2 else current
                change_pct = ((current - prev) / prev * 100) if prev else 0
                result[name] = {
                    "value": round(float(current), 2),
                    "change_pct": round(float(change_pct), 2),
                }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}", file=sys.stderr)
        return result

    def fetch_vix(self) -> Dict[str, Any]:
        """Fetch VIX volatility index."""
        import yfinance as yf

        try:
            symbol = list(self.config["volatility"].keys())[0]
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            if hist.empty:
                return {"error": "No data"}
            current = hist["Close"].iloc[-1]
            prev = hist["Close"].iloc[-2] if len(hist) >= 2 else current
            change_pct = ((current - prev) / prev * 100) if prev else 0
            return {
                "value": round(float(current), 2),
                "change_pct": round(float(change_pct), 2),
            }
        except Exception as e:
            print(f"Error fetching VIX: {e}", file=sys.stderr)
            return {"error": str(e)}

    # ──────────────────────────────────────────────
    # Crypto
    # ──────────────────────────────────────────────

    def fetch_crypto(self) -> List[Dict[str, Any]]:
        """Fetch crypto prices via yfinance."""
        import yfinance as yf

        results = []
        symbols = [c["symbol"] for c in self.config["crypto_symbols"]]
        names = {c["symbol"]: c["name"] for c in self.config["crypto_symbols"]}

        try:
            data = yf.download(symbols, period="5d", progress=False, group_by="ticker")
        except Exception as e:
            print(f"Error downloading crypto data: {e}", file=sys.stderr)
            return results

        for item in self.config["crypto_symbols"]:
            sym = item["symbol"]
            try:
                if len(symbols) == 1:
                    close = data["Close"]
                else:
                    close = data[sym]["Close"]
                close = close.dropna()
                if close.empty:
                    continue
                current = close.iloc[-1]
                prev = close.iloc[-2] if len(close) >= 2 else current
                change_pct = ((current - prev) / prev * 100) if prev else 0
                results.append({
                    "symbol": sym,
                    "name": item["name"],
                    "price": round(float(current), 2),
                    "change_pct": round(float(change_pct), 2),
                })
            except Exception as e:
                print(f"Error processing {sym}: {e}", file=sys.stderr)
        return results

    # ──────────────────────────────────────────────
    # News
    # ──────────────────────────────────────────────

    def fetch_market_news(self, category: str = "all", max_items: int = 10) -> List[Dict[str, Any]]:
        """Fetch market news from RSS feeds."""
        import feedparser
        import urllib.request
        import ssl

        feeds_config = self.config.get("news_feeds", {})
        all_feeds = []
        if category == "all":
            for cat, feed_list in feeds_config.items():
                all_feeds.extend(feed_list)
        else:
            all_feeds = feeds_config.get(category, [])

        entries = []
        cutoff = datetime.now() - timedelta(days=7)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        for feed_cfg in all_feeds:
            try:
                req = urllib.request.Request(
                    feed_cfg["url"],
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                    content = resp.read()
                feed = feedparser.parse(content)

                for entry in feed.entries[:10]:
                    pub_date = _parse_feed_date(entry)
                    if pub_date and pub_date > cutoff:
                        entries.append({
                            "title": entry.get("title", "No title"),
                            "link": entry.get("link", ""),
                            "published": pub_date.isoformat(),
                            "source": feed_cfg["name"],
                            "summary": _clean_html(entry.get("summary", ""))[:200],
                        })
            except Exception as e:
                print(f"Error fetching {feed_cfg['name']}: {e}", file=sys.stderr)
                continue

        # Score and sort
        scored = []
        for entry in entries:
            score = _score_news(entry, self.config.get("scoring", {}))
            entry["score"] = score
            scored.append(entry)
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:max_items]

    # ──────────────────────────────────────────────
    # Watchlist
    # ──────────────────────────────────────────────

    def fetch_watchlist(self) -> Dict[str, Any]:
        """Fetch all watchlist stocks/crypto with alert checking."""
        import yfinance as yf

        result = {"us": [], "kr": [], "crypto": []}

        # US stocks
        us_list = self.watchlist.get("us_stocks", [])
        if us_list:
            symbols = [s["symbol"] for s in us_list]
            try:
                data = yf.download(symbols, period="5d", progress=False, group_by="ticker")
                for item in us_list:
                    sym = item["symbol"]
                    try:
                        if len(symbols) == 1:
                            close = data["Close"]
                        else:
                            close = data[sym]["Close"]
                        close = close.dropna()
                        if close.empty:
                            continue
                        current = float(close.iloc[-1])
                        prev = float(close.iloc[-2]) if len(close) >= 2 else current
                        change_pct = ((current - prev) / prev * 100) if prev else 0
                        alerts = _check_alerts(current, item)
                        result["us"].append({
                            "symbol": sym,
                            "name": item.get("name", sym),
                            "price": round(current, 2),
                            "change_pct": round(change_pct, 2),
                            "notes": item.get("notes", ""),
                            "alerts": alerts,
                        })
                    except Exception:
                        continue
            except Exception as e:
                print(f"Error fetching US watchlist: {e}", file=sys.stderr)

        # Korean stocks
        kr_list = self.watchlist.get("kr_stocks", [])
        if kr_list:
            from pykrx import stock as krx
            today = date.today()
            start = today - timedelta(days=10)
            fmt = "%Y%m%d"
            for item in kr_list:
                ticker = item["ticker"]
                try:
                    df = krx.get_market_ohlcv(start.strftime(fmt), today.strftime(fmt), ticker)
                    if df.empty:
                        continue
                    current = int(df["종가"].iloc[-1])
                    prev = int(df["종가"].iloc[-2]) if len(df) >= 2 else current
                    change_pct = ((current - prev) / prev * 100) if prev else 0
                    result["kr"].append({
                        "ticker": ticker,
                        "name": item.get("name", ticker),
                        "price": current,
                        "change_pct": round(change_pct, 2),
                        "notes": item.get("notes", ""),
                    })
                except Exception as e:
                    print(f"Error fetching KR {ticker}: {e}", file=sys.stderr)

        # Crypto
        crypto_list = self.watchlist.get("crypto", [])
        if crypto_list:
            symbols = [c["symbol"] for c in crypto_list]
            try:
                data = yf.download(symbols, period="5d", progress=False, group_by="ticker")
                for item in crypto_list:
                    sym = item["symbol"]
                    try:
                        if len(symbols) == 1:
                            close = data["Close"]
                        else:
                            close = data[sym]["Close"]
                        close = close.dropna()
                        if close.empty:
                            continue
                        current = float(close.iloc[-1])
                        prev = float(close.iloc[-2]) if len(close) >= 2 else current
                        change_pct = ((current - prev) / prev * 100) if prev else 0
                        result["crypto"].append({
                            "symbol": sym,
                            "name": item.get("name", sym),
                            "price": round(current, 2),
                            "change_pct": round(change_pct, 2),
                        })
                    except Exception:
                        continue
            except Exception as e:
                print(f"Error fetching crypto watchlist: {e}", file=sys.stderr)

        return result

    # ──────────────────────────────────────────────
    # Historical Data from DB
    # ──────────────────────────────────────────────

    def get_historical_trends(self, symbols: List[str], days: int = 60) -> Dict[str, Any]:
        """
        Get historical price trends from database for charting.

        Args:
            symbols: List of ticker symbols
            days: Number of days to retrieve (default: 60)

        Returns:
            Dictionary with dates and prices for each symbol
        """
        if not self.use_db or not self.db:
            return {}

        result = {}
        for symbol in symbols:
            df = self.db.get_historical_prices(symbol, days=days)
            if not df.empty:
                result[symbol] = {
                    'dates': [d.strftime('%Y-%m-%d') for d in df['date']],
                    'prices': [float(p) for p in df['close']],
                    'count': len(df)
                }

        return result

    # ──────────────────────────────────────────────
    # Orchestrator
    # ──────────────────────────────────────────────

    def fetch_all(self, scope: str = "overview") -> Dict[str, Any]:
        """Fetch market data based on scope."""
        result = {
            "timestamp": datetime.now().isoformat(),
            "scope": scope,
            "market_status": self.get_market_status(),
            "data": {},
            "sources": {
                "us_market": {
                    "provider": "Yahoo Finance",
                    "library": "yfinance",
                    "url": "https://finance.yahoo.com",
                    "api_docs": "https://pypi.org/project/yfinance/",
                    "data_types": ["indices", "sectors", "volatility"]
                },
                "kr_market": {
                    "provider": "한국거래소 (Korea Exchange)",
                    "library": "pykrx",
                    "url": "http://data.krx.co.kr",
                    "api_docs": "https://github.com/sharebook-kr/pykrx",
                    "data_types": ["indices", "stocks", "trading_flows"]
                },
                "treasury": {
                    "provider": "Yahoo Finance",
                    "library": "yfinance",
                    "url": "https://finance.yahoo.com/bonds",
                    "data_types": ["treasury_yields"]
                },
                "commodities": {
                    "provider": "Yahoo Finance",
                    "library": "yfinance",
                    "url": "https://finance.yahoo.com/commodities",
                    "data_types": ["gold", "oil", "natural_gas"]
                },
                "currencies": {
                    "provider": "Yahoo Finance",
                    "library": "yfinance",
                    "url": "https://finance.yahoo.com/currencies",
                    "data_types": ["fx_rates", "dollar_index"]
                },
                "crypto": {
                    "provider": "Yahoo Finance",
                    "library": "yfinance",
                    "url": "https://finance.yahoo.com/cryptocurrencies",
                    "data_types": ["crypto_prices"]
                },
                "disclaimer": "All data is provided as-is from free public sources. Real-time data may be delayed 15-20 minutes."
            }
        }

        if scope in ("overview", "deep", "us"):
            result["data"]["us_indices"] = self.fetch_us_indices()
            result["data"]["us_sectors"] = self.fetch_us_sectors()
            result["data"]["vix"] = self.fetch_vix()

        if scope in ("overview", "deep", "kr"):
            result["data"]["kr_indices"] = self.fetch_kr_indices()
            result["data"]["kr_foreign_institutional"] = self.fetch_kr_foreign_institutional()
            result["data"]["kr_top_stocks"] = self.fetch_kr_top_stocks()

        if scope in ("overview", "deep", "global", "crypto"):
            result["data"]["treasury_yields"] = self.fetch_treasury_yields()
            result["data"]["commodities"] = self.fetch_commodities()
            result["data"]["currencies"] = self.fetch_currencies()

        if scope in ("overview", "deep", "crypto"):
            result["data"]["crypto"] = self.fetch_crypto()

        if scope in ("deep",):
            result["data"]["news"] = self.fetch_market_news()

        if scope in ("watchlist", "deep"):
            result["data"]["watchlist"] = self.fetch_watchlist()

        # Add 60-day historical trends for charting
        if self.use_db and self.db and scope in ("overview", "deep", "us", "kr"):
            trend_symbols = []

            # US indices
            if "us_indices" in result["data"]:
                trend_symbols.extend(list(result["data"]["us_indices"].keys()))

            # KR indices (KOSPI/KOSDAQ)
            if "kr_indices" in result["data"]:
                # Add specific symbols if needed
                pass

            if trend_symbols:
                result["data"]["historical_trends"] = self.get_historical_trends(trend_symbols, days=60)

        return result


# ──────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────

def _pct_change(series, periods: int) -> float:
    """Calculate percentage change over N periods."""
    if len(series) <= periods:
        periods = len(series) - 1
    if periods <= 0:
        return 0.0
    current = series.iloc[-1]
    prev = series.iloc[-(periods + 1)]
    if prev == 0:
        return 0.0
    return round(float((current - prev) / prev * 100), 2)


def _parse_feed_date(entry) -> Optional[datetime]:
    """Parse date from RSS feed entry."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6])
        except Exception:
            pass
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        try:
            return datetime(*entry.updated_parsed[:6])
        except Exception:
            pass
    return datetime.now()


def _clean_html(text: str) -> str:
    """Remove HTML tags."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _score_news(entry: Dict, scoring_config: Dict) -> float:
    """Score a news entry based on keywords and recency."""
    score = 0.0
    text = (entry.get("title", "") + " " + entry.get("summary", "")).lower()

    keyword_boost = scoring_config.get("keyword_boost", {})
    for kw in keyword_boost.get("high_priority", []):
        if kw.lower() in text:
            score += 5
    for kw in keyword_boost.get("medium_priority", []):
        if kw.lower() in text:
            score += 3
    for kw in keyword_boost.get("low_priority", []):
        if kw.lower() in text:
            score += 1

    recency = scoring_config.get("recency_boost", {})
    try:
        pub_date = datetime.fromisoformat(entry["published"])
        age = datetime.now() - pub_date
        if age < timedelta(hours=6):
            score += recency.get("last_6h", 10)
        elif age < timedelta(hours=24):
            score += recency.get("last_24h", 5)
        elif age < timedelta(hours=48):
            score += recency.get("last_48h", 2)
    except Exception:
        pass

    return score


def _check_alerts(price: float, config: Dict) -> List[str]:
    """Check if price triggers any alert thresholds."""
    alerts = []
    if "alert_above" in config and price > config["alert_above"]:
        alerts.append(f"ABOVE ${config['alert_above']}")
    if "alert_below" in config and price < config["alert_below"]:
        alerts.append(f"BELOW ${config['alert_below']}")
    return alerts




def main():
    parser = argparse.ArgumentParser(description="Fetch financial market data")
    parser.add_argument(
        "--scope", type=str, default="overview",
        choices=["overview", "us", "kr", "global", "crypto", "watchlist", "deep"],
        help="What market data to fetch",
    )
    parser.add_argument("--config", type=str, help="Path to sources.yaml")
    parser.add_argument("--watchlist", type=str, help="Path to watchlist.yaml")
    parser.add_argument(
        "--output", type=str, default="json",
        choices=["json", "text"], help="Output format",
    )
    parser.add_argument(
        "--with-analysis", action="store_true",
        help="Automatically generate AI insights from data (data-driven heuristics)",
    )

    args = parser.parse_args()
    fetcher = MarketDataFetcher(args.config, args.watchlist)
    data = fetcher.fetch_all(scope=args.scope)

    # Auto-generate insights if requested
    if args.with_analysis:
        try:
            import subprocess
            import tempfile

            # Save data to temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                temp_file = f.name

            # Run insights generator
            script_dir = os.path.dirname(os.path.abspath(__file__))
            insights_script = os.path.join(script_dir, 'generate_insights.py')

            result = subprocess.run(
                [sys.executable, insights_script, temp_file],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                # Read updated data with insights
                with open(temp_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ AI insights generated automatically", file=sys.stderr)
            else:
                print(f"⚠️  Failed to generate insights: {result.stderr}", file=sys.stderr)

            # Clean up temp file
            os.unlink(temp_file)

        except Exception as e:
            print(f"⚠️  Error generating insights: {e}", file=sys.stderr)

    if args.output == "json":
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"\n=== Market Pulse ({data['scope']}) ===")
        print(f"Timestamp: {data['timestamp']}")
        status = data["market_status"]
        print(f"US: {'Open' if status['us_open'] else status['us_note']}")
        print(f"KR: {'Open' if status['kr_open'] else status['kr_note']}")
        for section, content in data["data"].items():
            print(f"\n--- {section} ---")
            print(json.dumps(content, indent=2, ensure_ascii=False, default=str)[:500])


if __name__ == "__main__":
    main()

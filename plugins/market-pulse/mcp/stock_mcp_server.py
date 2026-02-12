#!/usr/bin/env python3
"""
Stock Data MCP Server
yfinance 기반 주식 데이터 제공 MCP 서버
"""

import json
import sys
from typing import Dict, List, Optional, Any
import yfinance as yf
from datetime import datetime, timedelta


class StockMCPServer:
    """
    주식 데이터를 제공하는 MCP 서버
    yfinance를 활용하여 실시간 및 펀더멘털 데이터 제공
    """

    def __init__(self):
        self.name = "stock-data"
        self.version = "1.0.0"

    def get_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록 반환"""
        return [
            {
                "name": "get_fundamental_metrics",
                "description": "펀더멘털 지표 조회 (PER, PBR, ROE, 부채비율 등)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼 (예: AAPL, MSFT)"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_valuation_metrics",
                "description": "밸류에이션 지표 (PER, PBR, PEG, EV/EBITDA)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_profitability_metrics",
                "description": "수익성 지표 (ROE, ROA, 마진율)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_growth_metrics",
                "description": "성장률 지표 (매출/이익 성장률, EPS)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_financial_health",
                "description": "재무 건전성 (부채비율, 유동비율)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_dividend_info",
                "description": "배당 정보 (배당수익률, 배당성향)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_company_info",
                "description": "기업 기본 정보 (이름, 섹터, 시가총액)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_price_data",
                "description": "가격 데이터 (현재가, 52주 고가/저가)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_all_metrics",
                "description": "모든 지표를 한번에 조회 (종합 데이터)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "주식 티커 심볼"
                        }
                    },
                    "required": ["ticker"]
                }
            }
        ]

    def get_fundamental_metrics(self, ticker: str) -> Dict:
        """펀더멘털 지표 조회"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "valuation": {
                    "per": info.get('forwardPE') or info.get('trailingPE'),
                    "pbr": info.get('priceToBook'),
                    "peg": info.get('pegRatio'),
                    "ps": info.get('priceToSalesTrailing12Months'),
                    "ev_ebitda": info.get('enterpriseToEbitda')
                },
                "profitability": {
                    "roe": round(info.get('returnOnEquity', 0) * 100, 2) if info.get('returnOnEquity') else None,
                    "roa": round(info.get('returnOnAssets', 0) * 100, 2) if info.get('returnOnAssets') else None,
                    "operating_margin": round(info.get('operatingMargins', 0) * 100, 2) if info.get('operatingMargins') else None,
                    "net_margin": round(info.get('profitMargins', 0) * 100, 2) if info.get('profitMargins') else None
                },
                "growth": {
                    "revenue_growth": round(info.get('revenueGrowth', 0) * 100, 2) if info.get('revenueGrowth') else None,
                    "earnings_growth": round(info.get('earningsGrowth', 0) * 100, 2) if info.get('earningsGrowth') else None,
                    "eps": info.get('trailingEps')
                },
                "financial_health": {
                    "debt_to_equity": info.get('debtToEquity'),
                    "current_ratio": info.get('currentRatio'),
                    "quick_ratio": info.get('quickRatio')
                },
                "dividend": {
                    "dividend_yield": round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else None,
                    "payout_ratio": round(info.get('payoutRatio', 0) * 100, 2) if info.get('payoutRatio') else None
                }
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_valuation_metrics(self, ticker: str) -> Dict:
        """밸류에이션 지표"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "per": info.get('forwardPE') or info.get('trailingPE'),
                "pbr": info.get('priceToBook'),
                "peg": info.get('pegRatio'),
                "price_to_sales": info.get('priceToSalesTrailing12Months'),
                "ev_to_ebitda": info.get('enterpriseToEbitda'),
                "ev_to_revenue": info.get('enterpriseToRevenue'),
                "market_cap": info.get('marketCap'),
                "enterprise_value": info.get('enterpriseValue')
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_profitability_metrics(self, ticker: str) -> Dict:
        """수익성 지표"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "roe": round(info.get('returnOnEquity', 0) * 100, 2) if info.get('returnOnEquity') else None,
                "roa": round(info.get('returnOnAssets', 0) * 100, 2) if info.get('returnOnAssets') else None,
                "operating_margin": round(info.get('operatingMargins', 0) * 100, 2) if info.get('operatingMargins') else None,
                "net_margin": round(info.get('profitMargins', 0) * 100, 2) if info.get('profitMargins') else None,
                "gross_margin": round(info.get('grossMargins', 0) * 100, 2) if info.get('grossMargins') else None,
                "ebitda_margin": round(info.get('ebitdaMargins', 0) * 100, 2) if info.get('ebitdaMargins') else None
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_growth_metrics(self, ticker: str) -> Dict:
        """성장률 지표"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "revenue_growth": round(info.get('revenueGrowth', 0) * 100, 2) if info.get('revenueGrowth') else None,
                "earnings_growth": round(info.get('earningsGrowth', 0) * 100, 2) if info.get('earningsGrowth') else None,
                "earnings_quarterly_growth": round(info.get('earningsQuarterlyGrowth', 0) * 100, 2) if info.get('earningsQuarterlyGrowth') else None,
                "revenue_per_share": info.get('revenuePerShare'),
                "eps": info.get('trailingEps'),
                "forward_eps": info.get('forwardEps')
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_financial_health(self, ticker: str) -> Dict:
        """재무 건전성"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "debt_to_equity": info.get('debtToEquity'),
                "current_ratio": info.get('currentRatio'),
                "quick_ratio": info.get('quickRatio'),
                "total_cash": info.get('totalCash'),
                "total_debt": info.get('totalDebt'),
                "free_cashflow": info.get('freeCashflow'),
                "operating_cashflow": info.get('operatingCashflow')
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_dividend_info(self, ticker: str) -> Dict:
        """배당 정보"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "dividend_yield": round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else None,
                "payout_ratio": round(info.get('payoutRatio', 0) * 100, 2) if info.get('payoutRatio') else None,
                "dividend_rate": info.get('dividendRate'),
                "ex_dividend_date": info.get('exDividendDate'),
                "five_year_avg_dividend_yield": info.get('fiveYearAvgDividendYield')
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_company_info(self, ticker: str) -> Dict:
        """기업 기본 정보"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "name": info.get('longName') or info.get('shortName'),
                "sector": info.get('sector'),
                "industry": info.get('industry'),
                "country": info.get('country'),
                "website": info.get('website'),
                "business_summary": info.get('longBusinessSummary'),
                "full_time_employees": info.get('fullTimeEmployees')
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_price_data(self, ticker: str) -> Dict:
        """가격 데이터"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "current_price": info.get('currentPrice') or info.get('regularMarketPrice'),
                "previous_close": info.get('previousClose'),
                "open": info.get('open') or info.get('regularMarketOpen'),
                "day_high": info.get('dayHigh') or info.get('regularMarketDayHigh'),
                "day_low": info.get('dayLow') or info.get('regularMarketDayLow'),
                "fifty_two_week_high": info.get('fiftyTwoWeekHigh'),
                "fifty_two_week_low": info.get('fiftyTwoWeekLow'),
                "volume": info.get('volume') or info.get('regularMarketVolume'),
                "average_volume": info.get('averageVolume')
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_all_metrics(self, ticker: str) -> Dict:
        """모든 지표 종합"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "company_info": self.get_company_info(ticker),
                "price_data": self.get_price_data(ticker),
                "valuation": self.get_valuation_metrics(ticker),
                "profitability": self.get_profitability_metrics(ticker),
                "growth": self.get_growth_metrics(ticker),
                "financial_health": self.get_financial_health(ticker),
                "dividend": self.get_dividend_info(ticker)
            }
        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def call_tool(self, name: str, arguments: Dict) -> Dict:
        """도구 호출 핸들러"""
        ticker = arguments.get("ticker", "").upper()

        if not ticker:
            return {"error": "ticker is required"}

        tool_map = {
            "get_fundamental_metrics": self.get_fundamental_metrics,
            "get_valuation_metrics": self.get_valuation_metrics,
            "get_profitability_metrics": self.get_profitability_metrics,
            "get_growth_metrics": self.get_growth_metrics,
            "get_financial_health": self.get_financial_health,
            "get_dividend_info": self.get_dividend_info,
            "get_company_info": self.get_company_info,
            "get_price_data": self.get_price_data,
            "get_all_metrics": self.get_all_metrics
        }

        if name not in tool_map:
            return {"error": f"Unknown tool: {name}"}

        return tool_map[name](ticker)


def main():
    """MCP 서버 메인 루프"""
    server = StockMCPServer()

    # MCP 프로토콜 핸들러
    for line in sys.stdin:
        try:
            request = json.loads(line)
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": server.name,
                            "version": server.version
                        }
                    }
                }
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": server.get_tools()
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = server.call_tool(tool_name, arguments)

                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2, ensure_ascii=False)
                            }
                        ]
                    }
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }

            print(json.dumps(response), flush=True)

        except json.JSONDecodeError:
            continue
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()

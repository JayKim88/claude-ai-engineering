#!/usr/bin/env python3
"""
MCP 서버 테스트 스크립트
"""

import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from stock_client import StockMCPClient
import json


def test_mcp_server():
    """MCP 서버 기능 테스트"""

    print("🧪 Stock MCP Server 테스트 시작...\n")

    client = StockMCPClient()

    # 테스트 종목
    tickers = ["AAPL", "MSFT", "GOOGL"]

    for ticker in tickers:
        print(f"{'='*60}")
        print(f"📊 {ticker} 테스트")
        print(f"{'='*60}\n")

        # 1. 펀더멘털 지표
        print(f"1️⃣  펀더멘털 지표:")
        try:
            metrics = client.get_fundamental_metrics(ticker)
            if "error" in metrics:
                print(f"   ❌ 오류: {metrics['error']}")
            else:
                print(f"   ✅ PER: {metrics.get('valuation', {}).get('per')}")
                print(f"   ✅ PBR: {metrics.get('valuation', {}).get('pbr')}")
                print(f"   ✅ ROE: {metrics.get('profitability', {}).get('roe')}%")
                print(f"   ✅ 부채비율: {metrics.get('financial_health', {}).get('debt_to_equity')}")
        except Exception as e:
            print(f"   ❌ 예외: {str(e)}")

        # 2. 밸류에이션
        print(f"\n2️⃣  밸류에이션:")
        try:
            valuation = client.get_valuation_metrics(ticker)
            if "error" in valuation:
                print(f"   ❌ 오류: {valuation['error']}")
            else:
                print(f"   ✅ PER: {valuation.get('per')}")
                print(f"   ✅ PBR: {valuation.get('pbr')}")
                print(f"   ✅ PEG: {valuation.get('peg')}")
                print(f"   ✅ 시가총액: ${valuation.get('market_cap', 0):,.0f}")
        except Exception as e:
            print(f"   ❌ 예외: {str(e)}")

        # 3. 성장률
        print(f"\n3️⃣  성장률:")
        try:
            growth = client.get_growth_metrics(ticker)
            if "error" in growth:
                print(f"   ❌ 오류: {growth['error']}")
            else:
                print(f"   ✅ 매출 성장률: {growth.get('revenue_growth')}%")
                print(f"   ✅ 이익 성장률: {growth.get('earnings_growth')}%")
                print(f"   ✅ EPS: ${growth.get('eps')}")
        except Exception as e:
            print(f"   ❌ 예외: {str(e)}")

        # 4. 가격 데이터
        print(f"\n4️⃣  가격 데이터:")
        try:
            price = client.get_price_data(ticker)
            if "error" in price:
                print(f"   ❌ 오류: {price['error']}")
            else:
                print(f"   ✅ 현재가: ${price.get('current_price')}")
                print(f"   ✅ 52주 최고: ${price.get('fifty_two_week_high')}")
                print(f"   ✅ 52주 최저: ${price.get('fifty_two_week_low')}")
        except Exception as e:
            print(f"   ❌ 예외: {str(e)}")

        print("\n")

    print("✅ 테스트 완료!\n")


def test_comprehensive():
    """종합 테스트 (AAPL만)"""
    print("🔍 AAPL 종합 분석 테스트\n")

    client = StockMCPClient()

    try:
        all_data = client.get_all_metrics("AAPL")

        if "error" in all_data:
            print(f"❌ 오류: {all_data['error']}")
            return

        print(json.dumps(all_data, indent=2, ensure_ascii=False))
        print("\n✅ 종합 분석 완료!")

    except Exception as e:
        print(f"❌ 예외: {str(e)}")


if __name__ == "__main__":
    # 기본 테스트
    test_mcp_server()

    # 종합 테스트 (상세)
    # test_comprehensive()

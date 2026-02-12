#!/usr/bin/env python3
"""
내재가치 및 안전마진 계산기
그레이엄과 버핏의 가치투자 철학 구현
"""

import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# MCP 클라이언트 임포트
current_dir = os.path.dirname(os.path.abspath(__file__))
mcp_dir = os.path.join(os.path.dirname(current_dir), 'mcp')
sys.path.insert(0, mcp_dir)

from stock_client import StockMCPClient


class InvestmentRecommendation(Enum):
    """투자 추천 등급"""
    STRONG_BUY = "강력 매수"
    BUY = "매수"
    HOLD = "보유"
    SELL = "매도"
    STRONG_SELL = "강력 매도"


@dataclass
class SafetyMarginResult:
    """안전마진 계산 결과"""
    ticker: str
    company_name: str
    current_price: float
    intrinsic_value: float
    safety_margin_pct: float
    recommendation: InvestmentRecommendation
    eps: float
    growth_rate: float
    per: float
    pbr: float
    roe: float
    calculation_method: str
    notes: str


class IntrinsicValueCalculator:
    """
    내재가치 계산기
    벤저민 그레이엄과 워렌 버핏의 가치투자 원칙 구현
    """

    def __init__(self):
        self.mcp_client = StockMCPClient()

    def calculate_graham_value(self, ticker: str) -> Optional[SafetyMarginResult]:
        """
        그레이엄 내재가치 공식
        IV = EPS × (8.5 + 2g)

        Args:
            ticker: 주식 티커 심볼

        Returns:
            SafetyMarginResult 또는 None (오류 시)
        """
        try:
            # 펀더멘털 데이터 가져오기
            fundamental = self.mcp_client.get_fundamental_metrics(ticker)
            if "error" in fundamental:
                print(f"❌ {ticker}: {fundamental['error']}")
                return None

            # 가격 데이터 가져오기
            price_data = self.mcp_client.get_price_data(ticker)
            if "error" in price_data:
                print(f"❌ {ticker}: {price_data['error']}")
                return None

            # 기업 정보 가져오기
            company_info = self.mcp_client.get_company_info(ticker)
            company_name = company_info.get('name', ticker) if "error" not in company_info else ticker

            # 필수 데이터 추출
            eps = fundamental.get('growth', {}).get('eps')
            growth_rate = fundamental.get('growth', {}).get('earnings_growth')
            current_price = price_data.get('current_price')
            per = fundamental.get('valuation', {}).get('per')
            pbr = fundamental.get('valuation', {}).get('pbr')
            roe = fundamental.get('profitability', {}).get('roe')

            # 데이터 검증
            if not eps or not growth_rate or not current_price:
                notes = "데이터 부족: "
                missing = []
                if not eps:
                    missing.append("EPS")
                if not growth_rate:
                    missing.append("성장률")
                if not current_price:
                    missing.append("현재가")
                notes += ", ".join(missing)

                return SafetyMarginResult(
                    ticker=ticker,
                    company_name=company_name,
                    current_price=current_price or 0,
                    intrinsic_value=0,
                    safety_margin_pct=0,
                    recommendation=InvestmentRecommendation.HOLD,
                    eps=eps or 0,
                    growth_rate=growth_rate or 0,
                    per=per or 0,
                    pbr=pbr or 0,
                    roe=roe or 0,
                    calculation_method="Graham Formula",
                    notes=notes
                )

            # 그레이엄 공식 적용
            # IV = EPS × (8.5 + 2g)
            # g는 %로 표현된 성장률
            intrinsic_value = eps * (8.5 + 2 * growth_rate)

            # 안전마진 계산
            # 안전마진(%) = (내재가치 - 현재가) / 내재가치 × 100
            safety_margin_pct = ((intrinsic_value - current_price) / intrinsic_value * 100) if intrinsic_value > 0 else -100

            # 투자 추천
            recommendation = self._get_recommendation(safety_margin_pct)

            # 노트 작성
            notes = self._generate_notes(safety_margin_pct, per, pbr, roe, growth_rate)

            return SafetyMarginResult(
                ticker=ticker,
                company_name=company_name,
                current_price=current_price,
                intrinsic_value=intrinsic_value,
                safety_margin_pct=safety_margin_pct,
                recommendation=recommendation,
                eps=eps,
                growth_rate=growth_rate,
                per=per or 0,
                pbr=pbr or 0,
                roe=roe or 0,
                calculation_method="Graham Formula",
                notes=notes
            )

        except Exception as e:
            print(f"❌ {ticker} 계산 오류: {str(e)}")
            return None

    def _get_recommendation(self, safety_margin_pct: float) -> InvestmentRecommendation:
        """
        안전마진에 따른 투자 추천

        그레이엄의 원칙:
        - 50% 이상: 강력 매수 (충분한 안전마진)
        - 30-50%: 매수 (적절한 안전마진)
        - 10-30%: 보유 (제한적 안전마진)
        - -10-10%: 보유 (안전마진 부족)
        - -10% 이하: 매도 (과대평가)
        """
        if safety_margin_pct >= 50:
            return InvestmentRecommendation.STRONG_BUY
        elif safety_margin_pct >= 30:
            return InvestmentRecommendation.BUY
        elif safety_margin_pct >= -10:
            return InvestmentRecommendation.HOLD
        elif safety_margin_pct >= -30:
            return InvestmentRecommendation.SELL
        else:
            return InvestmentRecommendation.STRONG_SELL

    def _generate_notes(self, safety_margin: float, per: float, pbr: float,
                       roe: float, growth_rate: float) -> str:
        """분석 노트 생성"""
        notes = []

        # 안전마진 평가
        if safety_margin >= 50:
            notes.append("✅ 매우 높은 안전마진 (50%+)")
        elif safety_margin >= 30:
            notes.append("✅ 충분한 안전마진 (30-50%)")
        elif safety_margin >= 10:
            notes.append("⚠️ 제한적 안전마진 (10-30%)")
        elif safety_margin >= -10:
            notes.append("⚠️ 안전마진 부족 (-10-10%)")
        else:
            notes.append("❌ 과대평가 (-10% 이하)")

        # PER 평가
        if per > 0:
            if per < 15:
                notes.append("✅ 낮은 PER (15 미만)")
            elif per < 25:
                notes.append("⚠️ 적정 PER (15-25)")
            else:
                notes.append("❌ 높은 PER (25 이상)")

        # ROE 평가
        if roe > 0:
            if roe >= 15:
                notes.append("✅ 우수한 ROE (15%+)")
            elif roe >= 10:
                notes.append("⚠️ 적정 ROE (10-15%)")
            else:
                notes.append("❌ 낮은 ROE (10% 미만)")

        # 성장률 평가
        if growth_rate > 0:
            if growth_rate >= 20:
                notes.append("✅ 고성장 (20%+)")
            elif growth_rate >= 10:
                notes.append("⚠️ 중성장 (10-20%)")
            else:
                notes.append("⚠️ 저성장 (10% 미만)")
        else:
            notes.append("❌ 마이너스 성장")

        return " | ".join(notes)

    def calculate_dcf_value(self, ticker: str, discount_rate: float = 0.10,
                           terminal_growth: float = 0.03,
                           projection_years: int = 5) -> Optional[SafetyMarginResult]:
        """
        DCF (Discounted Cash Flow) 내재가치 계산

        Args:
            ticker: 주식 티커 심볼
            discount_rate: 할인율 (기본값: 10%)
            terminal_growth: 영구 성장률 (기본값: 3%)
            projection_years: 예측 기간 (기본값: 5년)

        Returns:
            SafetyMarginResult 또는 None
        """
        try:
            # 재무 건전성 데이터 가져오기
            financial_health = self.mcp_client.get_financial_health(ticker)
            if "error" in financial_health:
                return None

            # 가격 데이터
            price_data = self.mcp_client.get_price_data(ticker)
            if "error" in price_data:
                return None

            # 기업 정보
            company_info = self.mcp_client.get_company_info(ticker)
            company_name = company_info.get('name', ticker) if "error" not in company_info else ticker

            # 펀더멘털 데이터
            fundamental = self.mcp_client.get_fundamental_metrics(ticker)
            growth_rate = fundamental.get('growth', {}).get('earnings_growth', 0)

            # FCF 데이터
            free_cashflow = financial_health.get('free_cashflow')
            current_price = price_data.get('current_price')

            if not free_cashflow or not current_price or free_cashflow <= 0:
                return None

            # DCF 계산
            # 1. 미래 FCF 예측
            projected_fcf = []
            for year in range(1, projection_years + 1):
                fcf = free_cashflow * ((1 + growth_rate / 100) ** year)
                discounted_fcf = fcf / ((1 + discount_rate) ** year)
                projected_fcf.append(discounted_fcf)

            # 2. 터미널 가치
            terminal_fcf = projected_fcf[-1] * (1 + terminal_growth)
            terminal_value = terminal_fcf / (discount_rate - terminal_growth)
            discounted_terminal_value = terminal_value / ((1 + discount_rate) ** projection_years)

            # 3. 기업 가치 = 예측 FCF 합 + 터미널 가치
            enterprise_value = sum(projected_fcf) + discounted_terminal_value

            # 4. 주당 가치 (간단화: 시가총액으로 나눔)
            valuation = self.mcp_client.get_valuation_metrics(ticker)
            shares_outstanding = valuation.get('market_cap', 0) / current_price if current_price > 0 else 0

            if shares_outstanding <= 0:
                return None

            intrinsic_value_per_share = enterprise_value / shares_outstanding

            # 안전마진 계산
            safety_margin_pct = ((intrinsic_value_per_share - current_price) / intrinsic_value_per_share * 100) if intrinsic_value_per_share > 0 else -100

            # 추천
            recommendation = self._get_recommendation(safety_margin_pct)

            notes = f"DCF 분석 (할인율 {discount_rate*100}%, 영구성장률 {terminal_growth*100}%, {projection_years}년 예측)"

            return SafetyMarginResult(
                ticker=ticker,
                company_name=company_name,
                current_price=current_price,
                intrinsic_value=intrinsic_value_per_share,
                safety_margin_pct=safety_margin_pct,
                recommendation=recommendation,
                eps=0,  # DCF는 EPS 대신 FCF 사용
                growth_rate=growth_rate,
                per=fundamental.get('valuation', {}).get('per', 0),
                pbr=fundamental.get('valuation', {}).get('pbr', 0),
                roe=fundamental.get('profitability', {}).get('roe', 0),
                calculation_method="DCF (Discounted Cash Flow)",
                notes=notes
            )

        except Exception as e:
            print(f"❌ {ticker} DCF 계산 오류: {str(e)}")
            return None

    def screen_undervalued_stocks(self, tickers: List[str],
                                  min_safety_margin: float = 30.0,
                                  method: str = "graham") -> List[SafetyMarginResult]:
        """
        저평가 종목 스크리닝

        Args:
            tickers: 분석할 종목 리스트
            min_safety_margin: 최소 안전마진 (기본값: 30%)
            method: 계산 방법 ("graham" 또는 "dcf")

        Returns:
            안전마진 높은 순으로 정렬된 결과 리스트
        """
        results = []

        print(f"\n🔍 {len(tickers)}개 종목 안전마진 분석 중...\n")

        for ticker in tickers:
            if method == "graham":
                result = self.calculate_graham_value(ticker)
            elif method == "dcf":
                result = self.calculate_dcf_value(ticker)
            else:
                print(f"⚠️ 알 수 없는 계산 방법: {method}")
                continue

            if result and result.safety_margin_pct >= min_safety_margin:
                results.append(result)
                print(f"✅ {result.ticker}: 안전마진 {result.safety_margin_pct:.1f}% ({result.recommendation.value})")
            elif result:
                print(f"⚠️ {result.ticker}: 안전마진 {result.safety_margin_pct:.1f}% (기준 미달)")

        # 안전마진 높은 순으로 정렬
        results.sort(key=lambda x: x.safety_margin_pct, reverse=True)

        print(f"\n✅ 총 {len(results)}개 저평가 종목 발견 (안전마진 {min_safety_margin}% 이상)\n")

        return results

    def format_result_table(self, results: List[SafetyMarginResult]) -> str:
        """결과를 테이블 형식으로 포맷팅"""
        if not results:
            return "저평가 종목이 없습니다."

        header = f"{'종목':<8} {'회사명':<20} {'현재가':>10} {'내재가치':>10} {'안전마진':>10} {'추천':<10}"
        separator = "=" * 90

        lines = [separator, header, separator]

        for result in results:
            line = (
                f"{result.ticker:<8} "
                f"{result.company_name[:18]:<20} "
                f"${result.current_price:>9.2f} "
                f"${result.intrinsic_value:>9.2f} "
                f"{result.safety_margin_pct:>9.1f}% "
                f"{result.recommendation.value:<10}"
            )
            lines.append(line)

        lines.append(separator)

        return "\n".join(lines)


# 사용 예시
if __name__ == "__main__":
    calculator = IntrinsicValueCalculator()

    # 단일 종목 분석
    print("=" * 90)
    print("🎯 Apple (AAPL) 안전마진 분석")
    print("=" * 90)

    result = calculator.calculate_graham_value("AAPL")
    if result:
        print(f"\n종목: {result.ticker} ({result.company_name})")
        print(f"현재가: ${result.current_price:.2f}")
        print(f"내재가치: ${result.intrinsic_value:.2f}")
        print(f"안전마진: {result.safety_margin_pct:.1f}%")
        print(f"추천: {result.recommendation.value}")
        print(f"EPS: ${result.eps:.2f}")
        print(f"성장률: {result.growth_rate:.1f}%")
        print(f"PER: {result.per:.2f}")
        print(f"ROE: {result.roe:.1f}%")
        print(f"\n📝 분석: {result.notes}")

    # 복수 종목 스크리닝
    print("\n\n" + "=" * 90)
    print("🔍 저평가 종목 스크리닝 (안전마진 20% 이상)")
    print("=" * 90)

    tech_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "META", "TSLA", "AMZN"]
    undervalued = calculator.screen_undervalued_stocks(
        tickers=tech_stocks,
        min_safety_margin=20.0,
        method="graham"
    )

    print("\n" + calculator.format_result_table(undervalued))

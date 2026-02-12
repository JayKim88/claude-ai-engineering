#!/usr/bin/env python3
"""
피터 린치 투자 전략 스크리너
PEG 비율 + 린치의 6가지 주식 분류
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


class LynchCategory(Enum):
    """린치의 6가지 주식 분류"""
    SLOW_GROWER = "저성장주"  # 성장률 < 5%, 대형주, 높은 배당
    STALWART = "우량주"  # 성장률 5-12%, 대형주, 안정적
    FAST_GROWER = "고성장주"  # 성장률 15-25%+, 중소형주
    CYCLICAL = "경기순환주"  # 경기 의존적 (자동차, 항공, 철강)
    TURNAROUND = "회생주"  # 적자 → 흑자 전환
    ASSET_PLAY = "자산주"  # 보유 자산 > 시가총액


class PEGRating(Enum):
    """PEG 비율 평가"""
    EXCELLENT = "탁월"  # PEG < 0.5
    GOOD = "좋음"  # 0.5 <= PEG < 1.0
    FAIR = "보통"  # 1.0 <= PEG < 1.5
    EXPENSIVE = "비싸다"  # 1.5 <= PEG < 2.0
    OVERVALUED = "과대평가"  # PEG >= 2.0


@dataclass
class LynchAnalysisResult:
    """린치 분석 결과"""
    ticker: str
    company_name: str
    category: LynchCategory
    per: float
    earnings_growth: float
    peg_ratio: float
    peg_rating: PEGRating
    market_cap: float
    debt_to_equity: float
    dividend_yield: float
    roe: float
    net_margin: float
    recommendation: str
    investment_thesis: str
    red_flags: List[str]
    green_flags: List[str]


class LynchScreener:
    """
    피터 린치 투자 전략 스크리너
    GARP (Growth At Reasonable Price) 원칙 구현
    """

    # 경기순환 섹터
    CYCLICAL_SECTORS = [
        "Automotive", "Airlines", "Steel", "Chemicals",
        "Construction", "Basic Materials", "Industrials"
    ]

    def __init__(self):
        self.mcp_client = StockMCPClient()

    def calculate_peg_ratio(self, per: float, growth_rate: float) -> Optional[float]:
        """
        PEG 비율 계산
        PEG = PER / 성장률

        린치의 원칙:
        - PEG < 0.5: 초저평가 (드물다)
        - PEG < 1.0: 저평가 (매수 기회)
        - PEG = 1.0: 적정 가격
        - PEG > 1.5: 고평가 (주의)
        - PEG > 2.0: 과대평가 (피하라)
        """
        if not per or not growth_rate or growth_rate <= 0:
            return None

        return per / growth_rate

    def classify_stock(self, ticker: str) -> Optional[LynchAnalysisResult]:
        """
        주식을 린치의 6가지 카테고리로 분류
        """
        try:
            # 데이터 수집
            fundamental = self.mcp_client.get_fundamental_metrics(ticker)
            valuation = self.mcp_client.get_valuation_metrics(ticker)
            company_info = self.mcp_client.get_company_info(ticker)

            if "error" in fundamental or "error" in valuation:
                return None

            # 데이터 추출
            company_name = company_info.get('name', ticker) if "error" not in company_info else ticker
            sector = company_info.get('sector', '') if "error" not in company_info else ''

            per = fundamental.get('valuation', {}).get('per') or valuation.get('per')
            earnings_growth = fundamental.get('growth', {}).get('earnings_growth', 0)
            market_cap = valuation.get('market_cap', 0)
            debt_to_equity = fundamental.get('financial_health', {}).get('debt_to_equity', 0)
            dividend_yield = fundamental.get('dividend', {}).get('dividend_yield', 0)
            roe = fundamental.get('profitability', {}).get('roe', 0)
            net_margin = fundamental.get('profitability', {}).get('net_margin', 0)

            # PEG 비율 계산
            peg_ratio = self.calculate_peg_ratio(per, earnings_growth)
            peg_rating = self._get_peg_rating(peg_ratio)

            # 카테고리 분류
            category = self._classify_category(
                earnings_growth, market_cap, sector, net_margin, debt_to_equity
            )

            # 투자 논리 및 신호등 분석
            investment_thesis = self._generate_investment_thesis(
                category, peg_ratio, earnings_growth, roe, debt_to_equity
            )
            red_flags = self._identify_red_flags(
                debt_to_equity, net_margin, earnings_growth, peg_ratio
            )
            green_flags = self._identify_green_flags(
                peg_ratio, roe, earnings_growth, debt_to_equity, dividend_yield
            )

            # 추천
            recommendation = self._get_recommendation(category, peg_ratio, red_flags, green_flags)

            return LynchAnalysisResult(
                ticker=ticker,
                company_name=company_name,
                category=category,
                per=per or 0,
                earnings_growth=earnings_growth,
                peg_ratio=peg_ratio or 0,
                peg_rating=peg_rating,
                market_cap=market_cap,
                debt_to_equity=debt_to_equity,
                dividend_yield=dividend_yield,
                roe=roe,
                net_margin=net_margin,
                recommendation=recommendation,
                investment_thesis=investment_thesis,
                red_flags=red_flags,
                green_flags=green_flags
            )

        except Exception as e:
            print(f"❌ {ticker} 분석 오류: {str(e)}")
            return None

    def _classify_category(self, growth_rate: float, market_cap: float,
                          sector: str, net_margin: float,
                          debt_to_equity: float) -> LynchCategory:
        """주식 카테고리 분류"""

        # 1. 회생주 (적자 → 흑자 전환 중)
        if net_margin < 0 or (net_margin > 0 and net_margin < 5):
            return LynchCategory.TURNAROUND

        # 2. 경기순환주
        if any(cyclical in sector for cyclical in self.CYCLICAL_SECTORS):
            return LynchCategory.CYCLICAL

        # 3. 저성장주 (성장률 < 5%)
        if growth_rate < 5:
            return LynchCategory.SLOW_GROWER

        # 4. 우량주 (성장률 5-12%, 대형주)
        if 5 <= growth_rate < 15 and market_cap > 50_000_000_000:  # $50B
            return LynchCategory.STALWART

        # 5. 고성장주 (성장률 15%+)
        if growth_rate >= 15:
            return LynchCategory.FAST_GROWER

        # 6. 기본값: 우량주
        return LynchCategory.STALWART

    def _get_peg_rating(self, peg_ratio: Optional[float]) -> PEGRating:
        """PEG 비율 평가"""
        if peg_ratio is None or peg_ratio < 0:
            return PEGRating.OVERVALUED

        if peg_ratio < 0.5:
            return PEGRating.EXCELLENT
        elif peg_ratio < 1.0:
            return PEGRating.GOOD
        elif peg_ratio < 1.5:
            return PEGRating.FAIR
        elif peg_ratio < 2.0:
            return PEGRating.EXPENSIVE
        else:
            return PEGRating.OVERVALUED

    def _generate_investment_thesis(self, category: LynchCategory,
                                    peg_ratio: Optional[float],
                                    growth_rate: float,
                                    roe: float,
                                    debt_to_equity: float) -> str:
        """투자 논리 생성"""
        thesis = []

        # 카테고리별 논리
        if category == LynchCategory.FAST_GROWER:
            thesis.append(f"🚀 고성장주 (성장률 {growth_rate:.1f}%)")
            if peg_ratio and peg_ratio < 1.0:
                thesis.append("✅ GARP 전략 적합 (PEG < 1.0)")
        elif category == LynchCategory.STALWART:
            thesis.append(f"💪 안정적 우량주 (성장률 {growth_rate:.1f}%)")
        elif category == LynchCategory.SLOW_GROWER:
            thesis.append(f"🐌 저성장주 (성장률 {growth_rate:.1f}%)")
            thesis.append("💰 배당 중심 투자 적합")
        elif category == LynchCategory.CYCLICAL:
            thesis.append("📊 경기순환주 - 사이클 타이밍 중요")
        elif category == LynchCategory.TURNAROUND:
            thesis.append("🔄 회생주 - 높은 리스크/높은 보상")
        elif category == LynchCategory.ASSET_PLAY:
            thesis.append("🏛️ 자산주 - 숨겨진 가치")

        # ROE 평가
        if roe >= 15:
            thesis.append(f"✅ 우수한 ROE ({roe:.1f}%)")

        # 부채 평가
        if debt_to_equity < 50:
            thesis.append("✅ 낮은 부채비율")
        elif debt_to_equity > 100:
            thesis.append("⚠️ 높은 부채비율")

        return " | ".join(thesis)

    def _identify_red_flags(self, debt_to_equity: float, net_margin: float,
                           earnings_growth: float, peg_ratio: Optional[float]) -> List[str]:
        """투자 경고 신호"""
        flags = []

        if debt_to_equity > 100:
            flags.append(f"⚠️ 높은 부채비율 ({debt_to_equity:.1f})")

        if net_margin < 5:
            flags.append(f"⚠️ 낮은 순이익률 ({net_margin:.1f}%)")

        if earnings_growth < 0:
            flags.append(f"⚠️ 마이너스 성장 ({earnings_growth:.1f}%)")

        if peg_ratio and peg_ratio > 2.0:
            flags.append(f"⚠️ 과대평가 (PEG {peg_ratio:.2f})")

        return flags

    def _identify_green_flags(self, peg_ratio: Optional[float], roe: float,
                             earnings_growth: float, debt_to_equity: float,
                             dividend_yield: float) -> List[str]:
        """투자 긍정 신호"""
        flags = []

        if peg_ratio and peg_ratio < 1.0:
            flags.append(f"✅ 저평가 (PEG {peg_ratio:.2f})")

        if roe >= 15:
            flags.append(f"✅ 높은 ROE ({roe:.1f}%)")

        if earnings_growth >= 20:
            flags.append(f"✅ 고성장 ({earnings_growth:.1f}%)")

        if debt_to_equity < 50:
            flags.append(f"✅ 낮은 부채 ({debt_to_equity:.1f})")

        if dividend_yield >= 3:
            flags.append(f"✅ 높은 배당 ({dividend_yield:.1f}%)")

        return flags

    def _get_recommendation(self, category: LynchCategory,
                           peg_ratio: Optional[float],
                           red_flags: List[str],
                           green_flags: List[str]) -> str:
        """투자 추천"""

        # Red flags가 3개 이상이면 피하라
        if len(red_flags) >= 3:
            return "❌ 피하라"

        # PEG < 1.0이고 red flags가 적으면 매수
        if peg_ratio and peg_ratio < 1.0 and len(red_flags) <= 1:
            if category == LynchCategory.FAST_GROWER:
                return "🚀 강력 매수"
            else:
                return "✅ 매수"

        # PEG < 1.5이고 green flags가 많으면 매수
        if peg_ratio and peg_ratio < 1.5 and len(green_flags) >= 3:
            return "✅ 매수"

        # 회생주는 특별 처리
        if category == LynchCategory.TURNAROUND:
            if len(green_flags) > len(red_flags):
                return "⚠️ 고위험 매수"
            else:
                return "⚠️ 보유"

        # PEG > 2.0이면 매도
        if peg_ratio and peg_ratio > 2.0:
            return "❌ 매도"

        # 기본: 보유
        return "⚠️ 보유"

    def screen_garp_stocks(self, tickers: List[str],
                          max_peg: float = 1.0,
                          min_growth: float = 10.0) -> List[LynchAnalysisResult]:
        """
        GARP 전략 스크리닝
        (Growth At Reasonable Price)

        Args:
            tickers: 분석할 종목 리스트
            max_peg: 최대 PEG 비율 (기본값: 1.0)
            min_growth: 최소 성장률 (기본값: 10%)

        Returns:
            PEG 낮은 순으로 정렬된 결과
        """
        results = []

        print(f"\n🔍 {len(tickers)}개 종목 GARP 분석 중...\n")

        for ticker in tickers:
            result = self.classify_stock(ticker)

            if result and result.peg_ratio > 0 and result.peg_ratio <= max_peg:
                if result.earnings_growth >= min_growth:
                    results.append(result)
                    print(f"✅ {result.ticker}: PEG {result.peg_ratio:.2f}, 성장률 {result.earnings_growth:.1f}% ({result.category.value})")
            elif result and result.peg_ratio > 0:
                print(f"⚠️ {result.ticker}: PEG {result.peg_ratio:.2f} (기준 미달)")

        # PEG 낮은 순으로 정렬
        results.sort(key=lambda x: x.peg_ratio)

        print(f"\n✅ 총 {len(results)}개 GARP 종목 발견 (PEG ≤ {max_peg}, 성장률 ≥ {min_growth}%)\n")

        return results

    def format_result_table(self, results: List[LynchAnalysisResult]) -> str:
        """결과를 테이블 형식으로 포맷팅"""
        if not results:
            return "조건에 맞는 종목이 없습니다."

        header = f"{'종목':<8} {'회사명':<20} {'카테고리':<12} {'PEG':>8} {'성장률':>8} {'ROE':>8} {'추천':<12}"
        separator = "=" * 100

        lines = [separator, header, separator]

        for result in results:
            line = (
                f"{result.ticker:<8} "
                f"{result.company_name[:18]:<20} "
                f"{result.category.value:<12} "
                f"{result.peg_ratio:>7.2f} "
                f"{result.earnings_growth:>7.1f}% "
                f"{result.roe:>7.1f}% "
                f"{result.recommendation:<12}"
            )
            lines.append(line)

        lines.append(separator)

        return "\n".join(lines)

    def generate_detailed_report(self, result: LynchAnalysisResult) -> str:
        """상세 분석 리포트 생성"""
        report = []
        report.append("=" * 100)
        report.append(f"📊 {result.ticker} ({result.company_name}) - 린치 분석 리포트")
        report.append("=" * 100)
        report.append("")

        # 기본 정보
        report.append(f"🏷️  카테고리: {result.category.value}")
        report.append(f"💰 시가총액: ${result.market_cap:,.0f}")
        report.append("")

        # 밸류에이션
        report.append("📈 밸류에이션")
        report.append(f"   PER: {result.per:.2f}")
        report.append(f"   성장률: {result.earnings_growth:.1f}%")
        report.append(f"   PEG: {result.peg_ratio:.2f} ({result.peg_rating.value})")
        report.append("")

        # 수익성
        report.append("💵 수익성")
        report.append(f"   ROE: {result.roe:.1f}%")
        report.append(f"   순이익률: {result.net_margin:.1f}%")
        report.append("")

        # 재무 건전성
        report.append("🏦 재무 건전성")
        report.append(f"   부채비율: {result.debt_to_equity:.1f}")
        report.append(f"   배당수익률: {result.dividend_yield:.1f}%")
        report.append("")

        # 투자 논리
        report.append("💡 투자 논리")
        report.append(f"   {result.investment_thesis}")
        report.append("")

        # 긍정 신호
        if result.green_flags:
            report.append("✅ 긍정 신호")
            for flag in result.green_flags:
                report.append(f"   {flag}")
            report.append("")

        # 경고 신호
        if result.red_flags:
            report.append("⚠️ 경고 신호")
            for flag in result.red_flags:
                report.append(f"   {flag}")
            report.append("")

        # 최종 추천
        report.append(f"🎯 추천: {result.recommendation}")
        report.append("=" * 100)

        return "\n".join(report)


# 사용 예시
if __name__ == "__main__":
    screener = LynchScreener()

    # 단일 종목 분석
    print("=" * 100)
    print("🎯 Apple (AAPL) 린치 분석")
    print("=" * 100)

    result = screener.classify_stock("AAPL")
    if result:
        print(screener.generate_detailed_report(result))

    # GARP 스크리닝
    print("\n\n" + "=" * 100)
    print("🔍 GARP 종목 스크리닝 (PEG ≤ 1.0, 성장률 ≥ 10%)")
    print("=" * 100)

    tech_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "META", "TSLA", "AMZN", "AMD", "CRM", "ORCL"]
    garp_stocks = screener.screen_garp_stocks(
        tickers=tech_stocks,
        max_peg=1.0,
        min_growth=10.0
    )

    print("\n" + screener.format_result_table(garp_stocks))

    # 각 종목 상세 리포트
    print("\n\n" + "=" * 100)
    print("📊 상위 3개 종목 상세 분석")
    print("=" * 100)

    for i, stock in enumerate(garp_stocks[:3], 1):
        print(f"\n\n{i}. {screener.generate_detailed_report(stock)}")

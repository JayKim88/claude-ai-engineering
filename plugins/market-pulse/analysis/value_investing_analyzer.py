#!/usr/bin/env python3
"""
Value Investing Analyzer
Phase 2.5 통합 분석기 - 그레이엄, 린치, 멀티 퍼스펙티브 분석
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Optional
from pathlib import Path

# 분석 도구 임포트
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from intrinsic_value import IntrinsicValueCalculator
from lynch_screener import LynchScreener
from company_deep_dive import CompanyDeepDiveAnalyzer


class ValueInvestingAnalyzer:
    """
    가치투자 통합 분석기
    Phase 2.5 모든 기능 통합
    """

    def __init__(self):
        self.graham_calc = IntrinsicValueCalculator()
        self.lynch_screener = LynchScreener()
        self.deep_dive = CompanyDeepDiveAnalyzer()

    def analyze_watchlist(self, tickers: List[str], analysis_type: str = "all") -> Dict:
        """
        관심 종목 리스트 분석

        Args:
            tickers: 분석할 종목 리스트
            analysis_type: "safety_margin", "garp", "deep", "all"

        Returns:
            분석 결과 딕셔너리
        """
        results = {
            "timestamp": "2026-02-12",
            "analysis_type": analysis_type,
            "tickers": tickers,
            "safety_margin": [],
            "garp": [],
            "deep_dive": []
        }

        if analysis_type in ("safety_margin", "all"):
            print("\n📊 안전마진 분석 중...")
            results["safety_margin"] = self._analyze_safety_margin(tickers)

        if analysis_type in ("garp", "all"):
            print("\n🔍 GARP 스크리닝 중...")
            results["garp"] = self._analyze_garp(tickers)

        if analysis_type == "deep":
            print("\n🎯 심층 분석 중...")
            results["deep_dive"] = self._analyze_deep_dive(tickers)

        return results

    def _analyze_safety_margin(self, tickers: List[str]) -> List[Dict]:
        """안전마진 분석 (그레이엄)"""
        results = []
        undervalued = self.graham_calc.screen_undervalued_stocks(
            tickers=tickers,
            min_safety_margin=20.0,
            method="graham"
        )

        for stock in undervalued:
            results.append({
                "ticker": stock.ticker,
                "company_name": stock.company_name,
                "current_price": stock.current_price,
                "intrinsic_value": stock.intrinsic_value,
                "safety_margin": stock.safety_margin_pct,
                "recommendation": stock.recommendation.value,
                "per": stock.per,
                "roe": stock.roe,
                "growth_rate": stock.growth_rate,
                "notes": stock.notes
            })

        return results

    def _analyze_garp(self, tickers: List[str]) -> List[Dict]:
        """GARP 스크리닝 (린치)"""
        results = []
        garp_stocks = self.lynch_screener.screen_garp_stocks(
            tickers=tickers,
            max_peg=1.0,
            min_growth=10.0
        )

        for stock in garp_stocks:
            results.append({
                "ticker": stock.ticker,
                "company_name": stock.company_name,
                "category": stock.category.value,
                "peg": stock.peg_ratio,
                "peg_rating": stock.peg_rating.value,
                "growth_rate": stock.earnings_growth,
                "per": stock.per,
                "roe": stock.roe,
                "recommendation": stock.recommendation,
                "investment_thesis": stock.investment_thesis,
                "green_flags": stock.green_flags,
                "red_flags": stock.red_flags
            })

        return results

    def _analyze_deep_dive(self, tickers: List[str]) -> List[Dict]:
        """심층 분석 (8가지 관점)"""
        results = []

        for ticker in tickers:
            report = self.deep_dive.analyze(ticker)
            if not report:
                continue

            results.append({
                "ticker": report.ticker,
                "company_name": report.company_name,
                "sector": report.sector,
                "overall_score": report.overall_score,
                "final_recommendation": report.final_recommendation,
                "risk_reward_ratio": report.risk_reward_ratio,
                "investment_horizon": report.investment_horizon,
                "confidence_level": report.confidence_level,
                "graham": {
                    "safety_margin": report.graham.safety_margin_pct,
                    "intrinsic_value": report.graham.intrinsic_value,
                    "recommendation": report.graham.recommendation.value
                },
                "buffett": {
                    "moat_strength": report.buffett.moat_strength.value,
                    "moat_score": report.buffett.moat_score,
                    "competitive_advantages": report.buffett.competitive_advantages
                },
                "lynch": {
                    "category": report.lynch.category.value,
                    "peg": report.lynch.peg_ratio,
                    "recommendation": report.lynch.recommendation
                },
                "munger": {
                    "risk_score": report.munger.risk_score,
                    "survivability": report.munger.survivability_score,
                    "fatal_flaws": report.munger.fatal_flaws,
                    "failure_scenarios": report.munger.failure_scenarios
                },
                "asness": {
                    "value": report.asness.value_score.value,
                    "quality": report.asness.quality_score.value,
                    "momentum": report.asness.momentum_score.value,
                    "overall_factor_score": report.asness.overall_factor_score
                }
            })

        return results

    def generate_html_section(self, analysis_data: Dict) -> str:
        """HTML 대시보드용 섹션 생성"""
        html = []
        html.append('<section class="value-investing">')
        html.append('<h2>🎯 가치투자 분석</h2>')

        # 안전마진 Top 10
        if analysis_data.get("safety_margin"):
            html.append('<h3>📊 안전마진 Top 10</h3>')
            html.append('<table>')
            html.append('<thead><tr><th>종목</th><th>회사명</th><th>현재가</th><th>내재가치</th><th>안전마진</th><th>추천</th></tr></thead>')
            html.append('<tbody>')

            for stock in analysis_data["safety_margin"][:10]:
                html.append('<tr>')
                html.append(f'<td>{stock["ticker"]}</td>')
                html.append(f'<td>{stock["company_name"]}</td>')
                html.append(f'<td>${stock["current_price"]:.2f}</td>')
                html.append(f'<td>${stock["intrinsic_value"]:.2f}</td>')
                html.append(f'<td class="positive">{stock["safety_margin"]:.1f}%</td>')
                html.append(f'<td>{stock["recommendation"]}</td>')
                html.append('</tr>')

            html.append('</tbody>')
            html.append('</table>')

        # GARP 종목
        if analysis_data.get("garp"):
            html.append('<h3>🚀 GARP 종목 (PEG < 1.0)</h3>')
            html.append('<table>')
            html.append('<thead><tr><th>종목</th><th>카테고리</th><th>PEG</th><th>성장률</th><th>ROE</th><th>추천</th></tr></thead>')
            html.append('<tbody>')

            for stock in analysis_data["garp"][:10]:
                html.append('<tr>')
                html.append(f'<td>{stock["ticker"]}</td>')
                html.append(f'<td>{stock["category"]}</td>')
                html.append(f'<td>{stock["peg"]:.2f}</td>')
                html.append(f'<td class="positive">{stock["growth_rate"]:.1f}%</td>')
                html.append(f'<td>{stock["roe"]:.1f}%</td>')
                html.append(f'<td>{stock["recommendation"]}</td>')
                html.append('</tr>')

            html.append('</tbody>')
            html.append('</table>')

        html.append('</section>')

        return '\n'.join(html)

    def export_to_json(self, analysis_data: Dict, output_path: str):
        """JSON으로 내보내기"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n✅ 분석 결과 저장: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Value Investing Analyzer")
    parser.add_argument(
        "--tickers", type=str, required=True,
        help="Comma-separated list of tickers (e.g., AAPL,MSFT,GOOGL)"
    )
    parser.add_argument(
        "--analysis", type=str, default="all",
        choices=["safety_margin", "garp", "deep", "all"],
        help="Type of analysis to run"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output JSON file path (optional)"
    )

    args = parser.parse_args()

    # 티커 파싱
    tickers = [t.strip().upper() for t in args.tickers.split(",")]

    print("=" * 100)
    print("🎯 Value Investing Analyzer - Phase 2.5")
    print("=" * 100)
    print(f"분석 대상: {', '.join(tickers)}")
    print(f"분석 유형: {args.analysis}")
    print("=" * 100)

    # 분석 실행
    analyzer = ValueInvestingAnalyzer()
    results = analyzer.analyze_watchlist(tickers, args.analysis)

    # 결과 출력
    print("\n" + "=" * 100)
    print("📊 분석 결과")
    print("=" * 100)

    if results.get("safety_margin"):
        print(f"\n✅ 안전마진 분석: {len(results['safety_margin'])}개 저평가 종목 발견")
        print(f"\n{'종목':<8} {'회사명':<20} {'현재가':>10} {'내재가치':>10} {'안전마진':>10} {'추천':<10}")
        print("=" * 90)
        for stock in results["safety_margin"][:10]:
            print(
                f"{stock['ticker']:<8} "
                f"{stock['company_name'][:18]:<20} "
                f"${stock['current_price']:>9.2f} "
                f"${stock['intrinsic_value']:>9.2f} "
                f"{stock['safety_margin']:>9.1f}% "
                f"{stock['recommendation']:<10}"
            )
        print("=" * 90)

    if results.get("garp"):
        print(f"\n✅ GARP 스크리닝: {len(results['garp'])}개 GARP 종목 발견")
        for stock in results["garp"][:5]:
            print(f"   {stock['ticker']}: PEG {stock['peg']:.2f}, 성장률 {stock['growth_rate']:.1f}%")

    if results.get("deep_dive"):
        print(f"\n✅ 심층 분석: {len(results['deep_dive'])}개 종목 분석 완료")
        for stock in results["deep_dive"]:
            print(f"   {stock['ticker']}: 종합 점수 {stock['overall_score']:.1f}/100, {stock['final_recommendation']}")

    # JSON 저장
    if args.output:
        analyzer.export_to_json(results, args.output)

    print("\n" + "=" * 100)
    print("✅ 분석 완료")
    print("=" * 100)


if __name__ == "__main__":
    main()

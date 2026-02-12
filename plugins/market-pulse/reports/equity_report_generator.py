#!/usr/bin/env python3
"""
Equity Research Report Generator
투자회사 스타일 기업 분석 리포트 생성 (마크다운 형식)
"""

import sys
import os
from datetime import datetime
from typing import Optional, Dict
from pathlib import Path

# 분석 도구 임포트
current_dir = os.path.dirname(os.path.abspath(__file__))
analysis_dir = os.path.join(os.path.dirname(current_dir), "analysis")
sys.path.insert(0, analysis_dir)

from company_deep_dive import CompanyDeepDiveAnalyzer, DeepDiveReport


class EquityReportGenerator:
    """
    투자회사 스타일 기업 분석 리포트 생성기
    키움증권/미래에셋 스타일 마크다운 리포트
    """

    def __init__(self, firm_name: str = "Market-Pulse Research"):
        self.firm_name = firm_name
        self.analyzer = CompanyDeepDiveAnalyzer()

    def generate_report(self, ticker: str, output_format: str = "markdown") -> str:
        """
        기업 분석 리포트 생성

        Args:
            ticker: 종목 코드
            output_format: "markdown" 또는 "terminal"

        Returns:
            리포트 텍스트
        """
        # Deep Dive 분석 실행
        report = self.analyzer.analyze(ticker)
        if not report:
            return f"❌ {ticker} 분석 실패"

        # 리포트 생성
        if output_format == "markdown":
            return self._generate_markdown_report(report)
        else:
            return self._generate_terminal_report(report)

    def _generate_markdown_report(self, report: DeepDiveReport) -> str:
        """마크다운 형식 리포트"""
        lines = []

        # 헤더
        lines.append(f"# {report.company_name} ({report.ticker})")
        lines.append(f"## 기업 분석 리포트")
        lines.append("")
        lines.append(f"**{self.firm_name}** | {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 투자 의견 박스
        lines.append("## 📊 투자 의견")
        lines.append("")
        lines.append("| 항목 | 내용 |")
        lines.append("|------|------|")
        lines.append(f"| **투자 등급** | {self._get_rating_emoji(report.final_recommendation)} **{report.final_recommendation}** |")
        lines.append(f"| **현재가** | ${report.graham.current_price:.2f} |")

        if report.graham.intrinsic_value:
            lines.append(f"| **내재가치** | ${report.graham.intrinsic_value:.2f} |")
            upside = ((report.graham.intrinsic_value - report.graham.current_price) / report.graham.current_price) * 100
            lines.append(f"| **상승여력** | {upside:+.1f}% |")

        lines.append(f"| **종합 점수** | {report.overall_score:.1f}/100 |")
        lines.append(f"| **신뢰도** | {report.confidence_level}% |")
        lines.append("")

        # 핵심 요약
        lines.append("## 💡 핵심 요약 (Investment Thesis)")
        lines.append("")
        lines.append(self._generate_investment_thesis(report))
        lines.append("")

        # 재무 하이라이트
        lines.append("## 📈 재무 하이라이트")
        lines.append("")
        lines.append("| 지표 | 값 |")
        lines.append("|------|------|")

        if report.graham.per:
            lines.append(f"| PER | {report.graham.per:.1f}x |")
        if report.graham.pbr:
            lines.append(f"| PBR | {report.graham.pbr:.2f}x |")
        if report.graham.roe:
            lines.append(f"| ROE | {report.graham.roe:.1f}% |")
        if report.graham.growth_rate:
            lines.append(f"| 성장률 (5Y) | {report.graham.growth_rate:.1f}% |")
        if report.lynch.peg_ratio:
            lines.append(f"| PEG 비율 | {report.lynch.peg_ratio:.2f} |")

        lines.append("")

        # 밸류에이션 분석
        lines.append("## 💰 밸류에이션 분석")
        lines.append("")
        lines.append("### 그레이엄 안전마진 분석")
        lines.append("")
        lines.append(f"- **내재가치**: ${report.graham.intrinsic_value:.2f}")
        lines.append(f"- **현재가**: ${report.graham.current_price:.2f}")
        lines.append(f"- **안전마진**: {report.graham.safety_margin_pct:.1f}%")
        lines.append(f"- **평가**: {report.graham.recommendation.value}")
        lines.append("")

        if report.graham.notes:
            lines.append(f"> {report.graham.notes}")
            lines.append("")

        lines.append("### 린치 GARP 분석")
        lines.append("")
        lines.append(f"- **카테고리**: {report.lynch.category.value}")

        if report.lynch.peg_ratio:
            lines.append(f"- **PEG 비율**: {report.lynch.peg_ratio:.2f} ({report.lynch.peg_rating.value})")

        lines.append(f"- **투자 논지**: {report.lynch.investment_thesis}")
        lines.append("")

        # 경쟁 우위 분석
        lines.append("## 🏰 경쟁 우위 (Economic Moat)")
        lines.append("")
        lines.append(f"**해자 강도**: {report.buffett.moat_strength.value} ({report.buffett.moat_score}/100)")
        lines.append("")

        if report.buffett.competitive_advantages:
            lines.append("**경쟁 우위 요소**:")
            for adv in report.buffett.competitive_advantages:
                lines.append(f"- ✅ {adv}")
            lines.append("")

        # 투자 포인트
        lines.append("## ✨ 투자 포인트")
        lines.append("")

        green_flags = self._extract_green_flags(report)
        for i, flag in enumerate(green_flags, 1):
            lines.append(f"{i}. **{flag['title']}**: {flag['description']}")

        lines.append("")

        # 리스크 요인
        lines.append("## ⚠️ 리스크 요인")
        lines.append("")
        lines.append(f"**리스크 점수**: {report.munger.risk_score}/100")
        lines.append(f"**생존 가능성**: {report.munger.survivability_score}/100")
        lines.append("")

        if report.munger.fatal_flaws:
            lines.append("**치명적 결함**:")
            for flaw in report.munger.fatal_flaws:
                lines.append(f"- 🚨 {flaw}")
            lines.append("")

        if report.munger.failure_scenarios:
            lines.append("**실패 시나리오**:")
            for scenario in report.munger.failure_scenarios:
                lines.append(f"- ⚠️ {scenario}")
            lines.append("")

        # 팩터 분석
        lines.append("## 📊 팩터 분석 (Asness)")
        lines.append("")
        lines.append("| 팩터 | 점수 | 평가 |")
        lines.append("|------|------|------|")
        lines.append(f"| Value | {self._get_factor_score_number(report.asness.value_score)}/100 | {report.asness.value_score.value} |")
        lines.append(f"| Quality | {self._get_factor_score_number(report.asness.quality_score)}/100 | {report.asness.quality_score.value} |")
        lines.append(f"| Momentum | {self._get_factor_score_number(report.asness.momentum_score)}/100 | {report.asness.momentum_score.value} |")
        lines.append(f"| Low Volatility | {self._get_factor_score_number(report.asness.low_volatility_score)}/100 | {report.asness.low_volatility_score.value} |")
        lines.append(f"| **종합** | **{report.asness.overall_factor_score:.1f}/100** | - |")
        lines.append("")

        # 경제 사이클 포지셔닝
        lines.append("## 🌐 경제 사이클 분석 (Dalio)")
        lines.append("")
        lines.append(f"- **현재 사이클**: {report.dalio.current_cycle.value}")
        lines.append(f"- **경기 민감도**: {report.dalio.cycle_sensitivity}/100")
        lines.append(f"- **추천 포지션**: {report.dalio.positioning_recommendation}")
        lines.append("")

        # 정성적 평가
        lines.append("## 🔍 정성적 평가 (Fisher)")
        lines.append("")
        lines.append("| 평가 항목 | 점수 |")
        lines.append("|----------|------|")
        lines.append(f"| 혁신 잠재력 | {report.fisher.innovation_potential}/100 |")
        lines.append(f"| 경영진 청렴성 | {report.fisher.management_integrity}/100 |")
        lines.append(f"| 직원 만족도 | {report.fisher.employee_satisfaction}/100 |")
        lines.append(f"| 고객 충성도 | {report.fisher.customer_loyalty}/100 |")
        lines.append(f"| **종합 질적 점수** | **{report.fisher.scuttlebutt_score:.1f}/100** |")
        lines.append("")

        # 종합 평가
        lines.append("## 🎯 종합 평가")
        lines.append("")
        lines.append(f"- **종합 점수**: {report.overall_score:.1f}/100")
        lines.append(f"- **리스크-보상 비율**: {report.risk_reward_ratio:.2f}")
        lines.append(f"- **최종 추천**: {self._get_rating_emoji(report.final_recommendation)} **{report.final_recommendation}**")
        lines.append(f"- **투자 기간**: {report.investment_horizon}")
        lines.append(f"- **신뢰도**: {report.confidence_level}%")
        lines.append("")

        # 푸터
        lines.append("---")
        lines.append("")
        lines.append("**Disclaimer**: 본 리포트는 교육 목적으로 제공되며, 투자 권유가 아닙니다. 실제 투자 결정은 투자자 본인의 판단과 책임하에 이루어져야 합니다.")
        lines.append("")
        lines.append(f"*Generated by {self.firm_name} | Powered by Market-Pulse Phase 2.5*")

        return "\n".join(lines)

    def _generate_terminal_report(self, report: DeepDiveReport) -> str:
        """터미널 출력용 간단한 포맷"""
        lines = []

        # 헤더
        lines.append("=" * 100)
        lines.append(f"  {report.company_name} ({report.ticker}) - 투자 분석 리포트")
        lines.append(f"  {self.firm_name} | {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("=" * 100)
        lines.append("")

        # 투자 의견
        lines.append("📊 투자 의견")
        lines.append("-" * 100)
        lines.append(f"  등급: {self._get_rating_emoji(report.final_recommendation)} {report.final_recommendation}")
        lines.append(f"  현재가: ${report.graham.current_price:.2f}")

        if report.graham.intrinsic_value:
            lines.append(f"  내재가치: ${report.graham.intrinsic_value:.2f}")
            upside = ((report.graham.intrinsic_value - report.graham.current_price) / report.graham.current_price) * 100
            lines.append(f"  상승여력: {upside:+.1f}%")

        lines.append(f"  종합 점수: {report.overall_score:.1f}/100")
        lines.append("")

        # 핵심 요약
        lines.append("💡 핵심 요약")
        lines.append("-" * 100)
        lines.append(f"  {self._generate_investment_thesis(report)}")
        lines.append("")

        # 투자 포인트
        lines.append("✨ 투자 포인트")
        lines.append("-" * 100)
        green_flags = self._extract_green_flags(report)
        for i, flag in enumerate(green_flags, 1):
            lines.append(f"  {i}. {flag['title']}: {flag['description']}")
        lines.append("")

        # 리스크 요인
        lines.append("⚠️  리스크 요인")
        lines.append("-" * 100)
        if report.munger.failure_scenarios:
            for scenario in report.munger.failure_scenarios[:3]:
                lines.append(f"  • {scenario}")
        lines.append("")

        # 종합 평가
        lines.append("🎯 종합 평가")
        lines.append("-" * 100)
        lines.append(f"  종합 점수: {report.overall_score:.1f}/100")
        lines.append(f"  최종 추천: {report.final_recommendation}")
        lines.append(f"  투자 기간: {report.investment_horizon}")
        lines.append(f"  신뢰도: {report.confidence_level}%")
        lines.append("")

        lines.append("=" * 100)

        return "\n".join(lines)

    def _generate_investment_thesis(self, report: DeepDiveReport) -> str:
        """투자 논지 생성"""
        thesis_parts = []

        # 안전마진 기반
        if report.graham.safety_margin_pct >= 30:
            thesis_parts.append(f"{report.company_name}은(는) 내재가치 대비 {report.graham.safety_margin_pct:.1f}% 저평가되어 있어 충분한 안전마진을 제공합니다.")

        # 성장성
        if report.graham.growth_rate and report.graham.growth_rate > 15:
            thesis_parts.append(f"5년 평균 {report.graham.growth_rate:.1f}%의 높은 성장률을 기록하고 있습니다.")

        # 경쟁우위
        if report.buffett.moat_score >= 70:
            thesis_parts.append(f"{report.buffett.moat_strength.value}를 보유하여 장기적 경쟁력이 우수합니다.")

        # GARP
        if report.lynch.peg_ratio and report.lynch.peg_ratio < 1.0:
            thesis_parts.append(f"PEG {report.lynch.peg_ratio:.2f}로 성장 대비 합리적 가격에 거래되고 있습니다.")

        # 리스크
        if report.munger.risk_score <= 30:
            thesis_parts.append("낮은 리스크 프로파일로 안정적 투자가 가능합니다.")

        if not thesis_parts:
            thesis_parts.append(f"{report.company_name}에 대한 투자 기회를 검토 중입니다.")

        return " ".join(thesis_parts)

    def _extract_green_flags(self, report: DeepDiveReport) -> list:
        """투자 포인트 추출"""
        flags = []

        # 안전마진
        if report.graham.safety_margin_pct >= 30:
            flags.append({
                "title": "높은 안전마진",
                "description": f"내재가치 대비 {report.graham.safety_margin_pct:.1f}% 저평가"
            })

        # 성장성
        if report.graham.growth_rate and report.graham.growth_rate > 20:
            flags.append({
                "title": "우수한 성장성",
                "description": f"5년 평균 성장률 {report.graham.growth_rate:.1f}%"
            })

        # ROE
        if report.graham.roe and report.graham.roe > 15:
            flags.append({
                "title": "높은 자본 수익률",
                "description": f"ROE {report.graham.roe:.1f}%로 효율적 자본 운용"
            })

        # 경쟁우위
        if report.buffett.moat_score >= 70:
            flags.append({
                "title": "강력한 경제적 해자",
                "description": f"{report.buffett.moat_strength.value} (점수: {report.buffett.moat_score}/100)"
            })

        # GARP
        if report.lynch.peg_ratio and report.lynch.peg_ratio < 1.0:
            flags.append({
                "title": "GARP 종목",
                "description": f"PEG {report.lynch.peg_ratio:.2f}로 성장 대비 저평가"
            })

        # 팩터
        if report.asness.overall_factor_score >= 60:
            flags.append({
                "title": "우수한 팩터 점수",
                "description": f"종합 팩터 점수 {report.asness.overall_factor_score:.1f}/100"
            })

        return flags[:5]  # 상위 5개만

    def _get_rating_emoji(self, recommendation: str) -> str:
        """추천 등급 이모지"""
        emoji_map = {
            "강력 매수": "🟢",
            "매수": "🔵",
            "조건부 매수": "🟡",
            "보유": "⚪",
            "매도": "🔴",
            "관망": "⚫"
        }
        return emoji_map.get(recommendation, "⚪")

    def _get_factor_score_number(self, score_enum) -> int:
        """팩터 점수 숫자 변환"""
        score_map = {
            "매우 강함": 90,
            "강함": 70,
            "보통": 50,
            "약함": 30,
            "매우 약함": 10
        }
        return score_map.get(score_enum.value, 50)

    def save_report(self, ticker: str, output_path: Optional[str] = None,
                   output_format: str = "markdown") -> str:
        """
        리포트 생성 및 파일 저장

        Args:
            ticker: 종목 코드
            output_path: 저장 경로 (None이면 자동 생성)
            output_format: "markdown" 또는 "terminal"

        Returns:
            저장된 파일 경로
        """
        report_text = self.generate_report(ticker, output_format)

        if output_path is None:
            # 자동 경로 생성
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"{ticker}_Investment_Report_{timestamp}.md"
            output_path = os.path.join("/tmp", filename)

        # 파일 저장
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        return output_path


def main():
    """CLI 실행"""
    import argparse

    parser = argparse.ArgumentParser(description="Equity Research Report Generator")
    parser.add_argument("--ticker", type=str, required=True, help="Stock ticker symbol")
    parser.add_argument(
        "--format", type=str, default="markdown",
        choices=["markdown", "terminal"],
        help="Output format"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output file path (for markdown format)"
    )
    parser.add_argument(
        "--firm", type=str, default="Market-Pulse Research",
        help="Firm name"
    )

    args = parser.parse_args()

    generator = EquityReportGenerator(firm_name=args.firm)

    if args.format == "terminal":
        # 터미널 출력
        report = generator.generate_report(args.ticker, output_format="terminal")
        print(report)
    else:
        # 마크다운 파일 저장
        output_path = generator.save_report(
            args.ticker,
            output_path=args.output,
            output_format="markdown"
        )
        print(f"✅ 리포트 생성 완료: {output_path}")

        # 터미널에도 요약 출력
        report = generator.generate_report(args.ticker, output_format="terminal")
        print("\n" + report)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
기업 심층 분석 (Company Deep Dive)
8가지 투자 대가의 관점을 종합한 멀티 퍼스펙티브 분석
"""

import sys
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# 기존 분석 도구 임포트
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from intrinsic_value import IntrinsicValueCalculator, SafetyMarginResult
from lynch_screener import LynchScreener, LynchAnalysisResult

# MCP 클라이언트
mcp_dir = os.path.join(os.path.dirname(current_dir), 'mcp')
sys.path.insert(0, mcp_dir)
from stock_client import StockMCPClient


class MoatStrength(Enum):
    """경제적 해자 강도 (버핏)"""
    WIDE = "넓은 해자"
    NARROW = "좁은 해자"
    NONE = "해자 없음"


class FactorScore(Enum):
    """팩터 점수 (애스니스)"""
    STRONG = "강함"
    MODERATE = "보통"
    WEAK = "약함"


class EconomicCycle(Enum):
    """경제 사이클 (달리오)"""
    EARLY_EXPANSION = "초기 확장"
    MID_EXPANSION = "중기 확장"
    LATE_EXPANSION = "후기 확장"
    RECESSION = "침체"


@dataclass
class BuffettAnalysis:
    """워렌 버핏 관점 분석"""
    moat_strength: MoatStrength
    competitive_advantages: List[str]
    moat_score: float  # 0-100
    is_simple_business: bool
    management_quality: str
    capital_allocation: str


@dataclass
class MungerAnalysis:
    """찰리 멍거 역행 사고 체크리스트"""
    failure_scenarios: List[str]
    risk_score: float  # 0-100 (높을수록 위험)
    fatal_flaws: List[str]
    survivability_score: float  # 0-100


@dataclass
class AssnessAnalysis:
    """클리프 애스니스 팩터 분석"""
    value_score: FactorScore
    quality_score: FactorScore
    momentum_score: FactorScore
    low_volatility_score: FactorScore
    overall_factor_score: float  # 0-100


@dataclass
class DalioAnalysis:
    """레이 달리오 경제 사이클 분석"""
    current_cycle: EconomicCycle
    cycle_sensitivity: float  # 0-100 (높을수록 경기 민감)
    positioning_recommendation: str


@dataclass
class FisherAnalysis:
    """필립 피셔 스캐터버트 분석"""
    innovation_potential: float  # 0-100
    management_integrity: float  # 0-100
    employee_satisfaction: float  # 0-100
    customer_loyalty: float  # 0-100
    scuttlebutt_score: float  # 0-100 평균


@dataclass
class DeepDiveReport:
    """종합 심층 분석 리포트"""
    ticker: str
    company_name: str
    sector: str

    # 각 대가의 분석
    graham: SafetyMarginResult
    buffett: BuffettAnalysis
    lynch: LynchAnalysisResult
    munger: MungerAnalysis
    asness: AssnessAnalysis
    dalio: DalioAnalysis
    fisher: FisherAnalysis

    # 종합 평가
    overall_score: float  # 0-100
    risk_reward_ratio: float
    final_recommendation: str
    investment_horizon: str  # 단기/중기/장기
    confidence_level: float  # 0-100


class CompanyDeepDiveAnalyzer:
    """
    기업 심층 분석기
    8가지 투자 대가의 철학을 통합한 멀티 퍼스펙티브 분석
    """

    def __init__(self):
        self.mcp_client = StockMCPClient()
        self.graham_calc = IntrinsicValueCalculator()
        self.lynch_screener = LynchScreener()

    def analyze(self, ticker: str) -> Optional[DeepDiveReport]:
        """종합 심층 분석 실행"""
        try:
            print(f"\n🔍 {ticker} 심층 분석 시작...\n")

            # 기본 데이터 수집
            company_info = self.mcp_client.get_company_info(ticker)
            if "error" in company_info:
                print(f"❌ {ticker} 데이터 수집 실패")
                return None

            company_name = company_info.get('name', ticker)
            sector = company_info.get('sector', 'Unknown')

            print(f"📊 {company_name} ({sector})")

            # 1. 그레이엄 분석
            print("   1/7 그레이엄 안전마진 분석...")
            graham = self.graham_calc.calculate_graham_value(ticker)
            if not graham:
                return None

            # 2. 버핏 분석
            print("   2/7 버핏 경제적 해자 분석...")
            buffett = self._analyze_buffett(ticker, sector)

            # 3. 린치 분석
            print("   3/7 린치 GARP 분석...")
            lynch = self.lynch_screener.classify_stock(ticker)
            if not lynch:
                return None

            # 4. 멍거 분석
            print("   4/7 멍거 역행 사고 분석...")
            munger = self._analyze_munger(ticker, graham, lynch)

            # 5. 애스니스 분석
            print("   5/7 애스니스 팩터 분석...")
            asness = self._analyze_asness(ticker, graham, lynch)

            # 6. 달리오 분석
            print("   6/7 달리오 경제 사이클 분석...")
            dalio = self._analyze_dalio(ticker, sector)

            # 7. 피셔 분석
            print("   7/7 피셔 스캐터버트 분석...")
            fisher = self._analyze_fisher(ticker)

            # 종합 평가
            print("   📊 종합 평가 계산 중...")
            overall_score = self._calculate_overall_score(
                graham, buffett, lynch, munger, asness, dalio, fisher
            )
            risk_reward = self._calculate_risk_reward(graham, munger, lynch)
            final_rec = self._generate_final_recommendation(overall_score, risk_reward, munger)
            horizon = self._determine_investment_horizon(lynch, dalio)
            confidence = self._calculate_confidence_level(graham, lynch, munger)

            print(f"✅ 분석 완료!\n")

            return DeepDiveReport(
                ticker=ticker,
                company_name=company_name,
                sector=sector,
                graham=graham,
                buffett=buffett,
                lynch=lynch,
                munger=munger,
                asness=asness,
                dalio=dalio,
                fisher=fisher,
                overall_score=overall_score,
                risk_reward_ratio=risk_reward,
                final_recommendation=final_rec,
                investment_horizon=horizon,
                confidence_level=confidence
            )

        except Exception as e:
            print(f"❌ {ticker} 분석 오류: {str(e)}")
            return None

    def _analyze_buffett(self, ticker: str, sector: str) -> BuffettAnalysis:
        """워렌 버핏 경제적 해자 분석"""
        try:
            fundamental = self.mcp_client.get_fundamental_metrics(ticker)
            company_info = self.mcp_client.get_company_info(ticker)

            roe = fundamental.get('profitability', {}).get('roe', 0)
            net_margin = fundamental.get('profitability', {}).get('net_margin', 0)
            operating_margin = fundamental.get('profitability', {}).get('operating_margin', 0)

            # 경제적 해자 요소 평가
            advantages = []
            moat_score = 0

            # 1. 높은 ROE (15%+)
            if roe >= 20:
                advantages.append("✅ 뛰어난 자본 수익률 (ROE 20%+)")
                moat_score += 25
            elif roe >= 15:
                advantages.append("✅ 우수한 자본 수익률 (ROE 15-20%)")
                moat_score += 15

            # 2. 높은 마진 (pricing power 지표)
            if net_margin >= 20:
                advantages.append("✅ 강력한 가격 결정력 (순이익률 20%+)")
                moat_score += 25
            elif net_margin >= 15:
                advantages.append("✅ 우수한 가격 결정력 (순이익률 15-20%)")
                moat_score += 15

            # 3. 브랜드력 (섹터 기반 휴리스틱)
            brand_sectors = ["Technology", "Consumer Cyclical", "Consumer Defensive", "Healthcare"]
            if sector in brand_sectors:
                advantages.append("✅ 강력한 브랜드 섹터")
                moat_score += 15

            # 4. 네트워크 효과 (Tech 섹터)
            if sector == "Technology":
                advantages.append("✅ 네트워크 효과 잠재력")
                moat_score += 15

            # 5. 전환 비용 (소프트웨어, 헬스케어)
            switching_cost_sectors = ["Technology", "Healthcare"]
            if sector in switching_cost_sectors:
                advantages.append("✅ 높은 전환 비용")
                moat_score += 10

            # 6. 규모의 경제 (시가총액 기반)
            valuation = self.mcp_client.get_valuation_metrics(ticker)
            market_cap = valuation.get('market_cap', 0)
            if market_cap > 100_000_000_000:  # $100B+
                advantages.append("✅ 대규모 경제력")
                moat_score += 10

            # 해자 강도 판정
            if moat_score >= 70:
                moat_strength = MoatStrength.WIDE
            elif moat_score >= 40:
                moat_strength = MoatStrength.NARROW
            else:
                moat_strength = MoatStrength.NONE

            # 사업 단순성 (섹터 기반)
            simple_sectors = ["Consumer Defensive", "Utilities", "Real Estate"]
            is_simple = sector in simple_sectors

            # 경영진 품질 (ROE, 마진 기반 간접 평가)
            if roe >= 15 and net_margin >= 15:
                management = "우수한 경영진 (높은 ROE, 마진)"
                capital_alloc = "효율적인 자본 배분"
            else:
                management = "평균적 경영진"
                capital_alloc = "보통 수준의 자본 배분"

            return BuffettAnalysis(
                moat_strength=moat_strength,
                competitive_advantages=advantages,
                moat_score=moat_score,
                is_simple_business=is_simple,
                management_quality=management,
                capital_allocation=capital_alloc
            )

        except Exception as e:
            print(f"⚠️ 버핏 분석 오류: {str(e)}")
            return BuffettAnalysis(
                moat_strength=MoatStrength.NONE,
                competitive_advantages=[],
                moat_score=0,
                is_simple_business=False,
                management_quality="알 수 없음",
                capital_allocation="알 수 없음"
            )

    def _analyze_munger(self, ticker: str, graham: SafetyMarginResult,
                       lynch: LynchAnalysisResult) -> MungerAnalysis:
        """찰리 멍거 역행 사고 분석"""
        try:
            failure_scenarios = []
            fatal_flaws = []
            risk_score = 0

            # 1. 재무적 리스크
            if lynch.debt_to_equity > 200:
                failure_scenarios.append("⚠️ 과도한 부채 (부채비율 200+)")
                fatal_flaws.append("❌ 부채 위기 가능성")
                risk_score += 30
            elif lynch.debt_to_equity > 100:
                failure_scenarios.append("⚠️ 높은 부채 (부채비율 100+)")
                risk_score += 15

            # 2. 수익성 리스크
            if lynch.net_margin < 5:
                failure_scenarios.append("⚠️ 낮은 순이익률 (<5%)")
                risk_score += 20

            if lynch.net_margin < 0:
                fatal_flaws.append("❌ 적자 상태")
                risk_score += 30

            # 3. 성장 리스크
            if lynch.earnings_growth < 0:
                failure_scenarios.append("⚠️ 마이너스 성장")
                risk_score += 25

            # 4. 밸류에이션 리스크
            if graham.safety_margin_pct < -30:
                failure_scenarios.append("⚠️ 심각한 과대평가 (안전마진 -30% 이하)")
                fatal_flaws.append("❌ 버블 가능성")
                risk_score += 25

            # 5. 경쟁 리스크 (PEG 기반)
            if lynch.peg_ratio > 2.5:
                failure_scenarios.append("⚠️ 과도한 기대치 (PEG 2.5+)")
                risk_score += 15

            # 생존 가능성 점수
            survivability = 100 - risk_score

            return MungerAnalysis(
                failure_scenarios=failure_scenarios,
                risk_score=risk_score,
                fatal_flaws=fatal_flaws,
                survivability_score=max(0, survivability)
            )

        except Exception as e:
            print(f"⚠️ 멍거 분석 오류: {str(e)}")
            return MungerAnalysis(
                failure_scenarios=[],
                risk_score=50,
                fatal_flaws=[],
                survivability_score=50
            )

    def _analyze_asness(self, ticker: str, graham: SafetyMarginResult,
                       lynch: LynchAnalysisResult) -> AssnessAnalysis:
        """클리프 애스니스 팩터 분석"""
        try:
            # Value Factor (PER, PBR, 안전마진 기반)
            value_score_num = 0
            if graham.per < 15 and graham.pbr < 3:
                value_score = FactorScore.STRONG
                value_score_num = 80
            elif graham.per < 25 and graham.pbr < 5:
                value_score = FactorScore.MODERATE
                value_score_num = 50
            else:
                value_score = FactorScore.WEAK
                value_score_num = 20

            # Quality Factor (ROE, 마진, 부채)
            quality_score_num = 0
            if lynch.roe >= 15 and lynch.net_margin >= 15 and lynch.debt_to_equity < 50:
                quality_score = FactorScore.STRONG
                quality_score_num = 80
            elif lynch.roe >= 10 and lynch.net_margin >= 10 and lynch.debt_to_equity < 100:
                quality_score = FactorScore.MODERATE
                quality_score_num = 50
            else:
                quality_score = FactorScore.WEAK
                quality_score_num = 20

            # Momentum Factor (성장률 기반)
            momentum_score_num = 0
            if lynch.earnings_growth >= 20:
                momentum_score = FactorScore.STRONG
                momentum_score_num = 80
            elif lynch.earnings_growth >= 10:
                momentum_score = FactorScore.MODERATE
                momentum_score_num = 50
            else:
                momentum_score = FactorScore.WEAK
                momentum_score_num = 20

            # Low Volatility Factor (부채, 마진 안정성)
            volatility_score_num = 0
            if lynch.debt_to_equity < 50 and lynch.net_margin >= 15:
                low_vol_score = FactorScore.STRONG
                volatility_score_num = 80
            elif lynch.debt_to_equity < 100 and lynch.net_margin >= 10:
                low_vol_score = FactorScore.MODERATE
                volatility_score_num = 50
            else:
                low_vol_score = FactorScore.WEAK
                volatility_score_num = 20

            # 종합 점수 (가중 평균)
            overall = (value_score_num * 0.3 + quality_score_num * 0.3 +
                      momentum_score_num * 0.25 + volatility_score_num * 0.15)

            return AssnessAnalysis(
                value_score=value_score,
                quality_score=quality_score,
                momentum_score=momentum_score,
                low_volatility_score=low_vol_score,
                overall_factor_score=overall
            )

        except Exception as e:
            print(f"⚠️ 애스니스 분석 오류: {str(e)}")
            return AssnessAnalysis(
                value_score=FactorScore.MODERATE,
                quality_score=FactorScore.MODERATE,
                momentum_score=FactorScore.MODERATE,
                low_volatility_score=FactorScore.MODERATE,
                overall_factor_score=50
            )

    def _analyze_dalio(self, ticker: str, sector: str) -> DalioAnalysis:
        """레이 달리오 경제 사이클 분석 (간단화 버전)"""
        # 실제로는 GDP, 금리, 실업률 등 매크로 데이터 필요
        # 여기서는 섹터 기반 휴리스틱 사용

        # 경기 민감도 (섹터별)
        cyclical_sectors = {
            "Technology": 60,
            "Consumer Cyclical": 80,
            "Financials": 75,
            "Industrials": 70,
            "Basic Materials": 85,
            "Consumer Defensive": 20,
            "Utilities": 15,
            "Healthcare": 30,
            "Real Estate": 50
        }

        sensitivity = cyclical_sectors.get(sector, 50)

        # 현재 사이클 (간단화: 중기 확장 가정)
        current_cycle = EconomicCycle.MID_EXPANSION

        # 포지셔닝 권장
        if sensitivity < 30:
            positioning = "방어적 - 경기 방어주"
        elif sensitivity < 60:
            positioning = "중립적 - 경기 중립주"
        else:
            positioning = "공격적 - 경기 순환주 (타이밍 중요)"

        return DalioAnalysis(
            current_cycle=current_cycle,
            cycle_sensitivity=sensitivity,
            positioning_recommendation=positioning
        )

    def _analyze_fisher(self, ticker: str) -> FisherAnalysis:
        """필립 피셔 스캐터버트 분석 (간단화 버전)"""
        # 실제로는 고객, 공급업체, 경쟁사 인터뷰 필요
        # 여기서는 재무 지표 기반 휴리스틱 사용

        try:
            fundamental = self.mcp_client.get_fundamental_metrics(ticker)

            roe = fundamental.get('profitability', {}).get('roe', 0)
            growth = fundamental.get('growth', {}).get('earnings_growth', 0)
            operating_margin = fundamental.get('profitability', {}).get('operating_margin', 0)

            # 혁신 잠재력 (성장률, R&D 지출 대용)
            if growth >= 30:
                innovation = 90
            elif growth >= 15:
                innovation = 70
            else:
                innovation = 40

            # 경영진 청렴성 (ROE, 마진 기반 간접 평가)
            if roe >= 20 and operating_margin >= 20:
                management_integrity = 90
            elif roe >= 15 and operating_margin >= 15:
                management_integrity = 70
            else:
                management_integrity = 50

            # 직원 만족도 (이직률 데이터 없으므로 추정)
            employee_satisfaction = 70  # 기본값

            # 고객 충성도 (재구매율 데이터 없으므로 추정)
            customer_loyalty = 70  # 기본값

            scuttlebutt_score = (innovation + management_integrity +
                               employee_satisfaction + customer_loyalty) / 4

            return FisherAnalysis(
                innovation_potential=innovation,
                management_integrity=management_integrity,
                employee_satisfaction=employee_satisfaction,
                customer_loyalty=customer_loyalty,
                scuttlebutt_score=scuttlebutt_score
            )

        except Exception as e:
            print(f"⚠️ 피셔 분석 오류: {str(e)}")
            return FisherAnalysis(
                innovation_potential=50,
                management_integrity=50,
                employee_satisfaction=50,
                customer_loyalty=50,
                scuttlebutt_score=50
            )

    def _calculate_overall_score(self, graham, buffett, lynch, munger,
                                asness, dalio, fisher) -> float:
        """종합 점수 계산 (0-100)"""

        # 각 대가의 점수 (0-100 스케일로 정규화)
        graham_score = max(0, min(100, graham.safety_margin_pct + 50))  # -50~50 → 0~100
        buffett_score = buffett.moat_score
        lynch_score = 100 - (lynch.peg_ratio * 33.33) if lynch.peg_ratio < 3 else 0
        munger_score = munger.survivability_score
        asness_score = asness.overall_factor_score
        dalio_score = 70  # 경제 사이클은 중립으로 가정
        fisher_score = fisher.scuttlebutt_score

        # 가중 평균
        weights = {
            'graham': 0.20,  # 안전마진 20%
            'buffett': 0.20,  # 경제적 해자 20%
            'lynch': 0.15,   # GARP 15%
            'munger': 0.15,  # 리스크 15%
            'asness': 0.15,  # 팩터 15%
            'dalio': 0.05,   # 사이클 5%
            'fisher': 0.10   # 질적 분석 10%
        }

        overall = (
            graham_score * weights['graham'] +
            buffett_score * weights['buffett'] +
            lynch_score * weights['lynch'] +
            munger_score * weights['munger'] +
            asness_score * weights['asness'] +
            dalio_score * weights['dalio'] +
            fisher_score * weights['fisher']
        )

        return round(overall, 1)

    def _calculate_risk_reward(self, graham, munger, lynch) -> float:
        """리스크-보상 비율"""
        # 보상 = 안전마진 (양수면 보상)
        reward = max(0, graham.safety_margin_pct)

        # 리스크 = 멍거 리스크 점수
        risk = max(1, munger.risk_score)  # 0으로 나누기 방지

        return round(reward / risk, 2)

    def _generate_final_recommendation(self, overall_score: float,
                                      risk_reward: float,
                                      munger: MungerAnalysis) -> str:
        """최종 투자 추천"""

        # Fatal flaw가 있으면 피하라
        if munger.fatal_flaws:
            return "❌ 투자 부적합 (치명적 결함)"

        # 종합 점수 기반
        if overall_score >= 80:
            return "🚀 강력 매수"
        elif overall_score >= 70:
            return "✅ 매수"
        elif overall_score >= 60:
            return "⚠️ 조건부 매수"
        elif overall_score >= 50:
            return "⚠️ 보유"
        elif overall_score >= 40:
            return "⚠️ 매도 고려"
        else:
            return "❌ 매도"

    def _determine_investment_horizon(self, lynch, dalio) -> str:
        """투자 기간 결정"""
        from lynch_screener import LynchCategory

        if lynch.category == LynchCategory.FAST_GROWER:
            return "중기 (1-3년)"
        elif lynch.category == LynchCategory.STALWART:
            return "장기 (3-5년+)"
        elif lynch.category == LynchCategory.CYCLICAL:
            return "단기-중기 (사이클 의존)"
        elif lynch.category == LynchCategory.TURNAROUND:
            return "중기 (1-2년)"
        else:
            return "장기 (5년+)"

    def _calculate_confidence_level(self, graham, lynch, munger) -> float:
        """신뢰도 계산 (0-100)"""
        confidence = 100

        # 데이터 품질
        if not graham.eps or graham.eps <= 0:
            confidence -= 20
        if not graham.growth_rate or graham.growth_rate <= 0:
            confidence -= 20

        # 리스크 레벨
        if munger.risk_score > 70:
            confidence -= 20
        elif munger.risk_score > 50:
            confidence -= 10

        # PEG 신뢰성
        if not lynch.peg_ratio or lynch.peg_ratio <= 0:
            confidence -= 15

        return max(0, confidence)

    def generate_comprehensive_report(self, report: DeepDiveReport) -> str:
        """종합 리포트 생성"""
        lines = []
        lines.append("=" * 120)
        lines.append(f"📊 {report.company_name} ({report.ticker}) - 기업 심층 분석 리포트")
        lines.append(f"섹터: {report.sector} | 종합 점수: {report.overall_score}/100 | 신뢰도: {report.confidence_level}%")
        lines.append("=" * 120)
        lines.append("")

        # 1. 그레이엄 (안전마진)
        lines.append("1️⃣  벤저민 그레이엄 - 안전마진 분석")
        lines.append(f"   현재가: ${report.graham.current_price:.2f}")
        lines.append(f"   내재가치: ${report.graham.intrinsic_value:.2f}")
        lines.append(f"   안전마진: {report.graham.safety_margin_pct:.1f}%")
        lines.append(f"   추천: {report.graham.recommendation.value}")
        lines.append(f"   분석: {report.graham.notes}")
        lines.append("")

        # 2. 버핏 (경제적 해자)
        lines.append("2️⃣  워렌 버핏 - 경제적 해자 분석")
        lines.append(f"   해자 강도: {report.buffett.moat_strength.value} (점수: {report.buffett.moat_score}/100)")
        lines.append(f"   경영진 품질: {report.buffett.management_quality}")
        lines.append(f"   경쟁 우위:")
        for adv in report.buffett.competitive_advantages:
            lines.append(f"      {adv}")
        lines.append("")

        # 3. 린치 (GARP)
        lines.append("3️⃣  피터 린치 - GARP 분석")
        lines.append(f"   카테고리: {report.lynch.category.value}")
        lines.append(f"   PEG: {report.lynch.peg_ratio:.2f} ({report.lynch.peg_rating.value})")
        lines.append(f"   성장률: {report.lynch.earnings_growth:.1f}%")
        lines.append(f"   ROE: {report.lynch.roe:.1f}%")
        lines.append(f"   추천: {report.lynch.recommendation}")
        lines.append("")

        # 4. 멍거 (역행 사고)
        lines.append("4️⃣  찰리 멍거 - 역행 사고 체크리스트")
        lines.append(f"   리스크 점수: {report.munger.risk_score}/100")
        lines.append(f"   생존 가능성: {report.munger.survivability_score}/100")
        if report.munger.fatal_flaws:
            lines.append(f"   치명적 결함:")
            for flaw in report.munger.fatal_flaws:
                lines.append(f"      {flaw}")
        if report.munger.failure_scenarios:
            lines.append(f"   실패 시나리오:")
            for scenario in report.munger.failure_scenarios:
                lines.append(f"      {scenario}")
        lines.append("")

        # 5. 애스니스 (팩터)
        lines.append("5️⃣  클리프 애스니스 - 팩터 분석")
        lines.append(f"   Value: {report.asness.value_score.value}")
        lines.append(f"   Quality: {report.asness.quality_score.value}")
        lines.append(f"   Momentum: {report.asness.momentum_score.value}")
        lines.append(f"   Low Volatility: {report.asness.low_volatility_score.value}")
        lines.append(f"   종합 팩터 점수: {report.asness.overall_factor_score:.1f}/100")
        lines.append("")

        # 6. 달리오 (경제 사이클)
        lines.append("6️⃣  레이 달리오 - 경제 사이클 분석")
        lines.append(f"   현재 사이클: {report.dalio.current_cycle.value}")
        lines.append(f"   경기 민감도: {report.dalio.cycle_sensitivity}/100")
        lines.append(f"   포지셔닝: {report.dalio.positioning_recommendation}")
        lines.append("")

        # 7. 피셔 (스캐터버트)
        lines.append("7️⃣  필립 피셔 - 스캐터버트 분석")
        lines.append(f"   혁신 잠재력: {report.fisher.innovation_potential}/100")
        lines.append(f"   경영진 청렴성: {report.fisher.management_integrity}/100")
        lines.append(f"   직원 만족도: {report.fisher.employee_satisfaction}/100")
        lines.append(f"   고객 충성도: {report.fisher.customer_loyalty}/100")
        lines.append(f"   종합 질적 점수: {report.fisher.scuttlebutt_score:.1f}/100")
        lines.append("")

        # 8. 종합 결론
        lines.append("=" * 120)
        lines.append("🎯 종합 결론")
        lines.append("=" * 120)
        lines.append(f"   종합 점수: {report.overall_score}/100")
        lines.append(f"   리스크-보상 비율: {report.risk_reward_ratio}")
        lines.append(f"   최종 추천: {report.final_recommendation}")
        lines.append(f"   투자 기간: {report.investment_horizon}")
        lines.append(f"   신뢰도: {report.confidence_level}%")
        lines.append("=" * 120)

        return "\n".join(lines)


# 사용 예시
if __name__ == "__main__":
    analyzer = CompanyDeepDiveAnalyzer()

    # Apple 심층 분석
    ticker = "AAPL"
    report = analyzer.analyze(ticker)

    if report:
        print("\n" + analyzer.generate_comprehensive_report(report))

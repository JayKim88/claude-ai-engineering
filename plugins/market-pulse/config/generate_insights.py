#!/usr/bin/env python3
"""
Automatic Market Insights Generator
Generates data-driven insights from market data without AI agents
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime


class MarketInsightsGenerator:
    """Generate insights from market data using heuristics."""

    def __init__(self, data: Dict):
        self.data = data
        self.market_data = data.get('data', {})
        self.market_status = data.get('market_status', {})

    def generate_all_insights(self) -> Dict[str, str]:
        """Generate all market insights."""
        return {
            'us_market': self._generate_us_insights(),
            'kr_market': self._generate_kr_insights(),
            'crypto_macro': self._generate_crypto_macro_insights(),
            'synthesis': self._generate_synthesis()
        }

    def _generate_us_insights(self) -> str:
        """Generate US market insights."""
        lines = []
        lines.append("## 🇺🇸 미국 시장 분석\n")

        # Indices
        indices = self.market_data.get('us_indices', {})
        if indices:
            lines.append("### 📉 지수 동향")

            sp500_change = indices.get('^GSPC', {}).get('change_pct', 0)
            nasdaq_change = indices.get('^IXIC', {}).get('change_pct', 0)
            dow_change = indices.get('^DJI', {}).get('change_pct', 0)
            russell_change = indices.get('^RUT', {}).get('change_pct', 0)

            # Determine market direction
            avg_change = (sp500_change + nasdaq_change + dow_change) / 3
            if avg_change > 0.5:
                direction = "강세"
                sentiment = "긍정적"
            elif avg_change < -0.5:
                direction = "약세"
                sentiment = "부정적"
            else:
                direction = "보합"
                sentiment = "관망"

            lines.append(f"- **시장 방향**: {direction} ({avg_change:+.2f}%) - {sentiment} 심리")
            lines.append(f"- **S&P 500**: {sp500_change:+.2f}%")
            lines.append(f"- **NASDAQ**: {nasdaq_change:+.2f}%")
            lines.append(f"- **Dow Jones**: {dow_change:+.2f}%")
            lines.append(f"- **Russell 2000**: {russell_change:+.2f}%")

            # Small cap analysis
            if russell_change < nasdaq_change - 0.5:
                lines.append("\n⚠️ **스몰캡 약세**: Russell 2000이 상대적으로 부진 → 경기 둔화 신호")
            elif russell_change > nasdaq_change + 0.5:
                lines.append("\n✅ **스몰캡 강세**: 리스크 선호도 증가 신호")
            lines.append("")

        # Sectors
        sectors = self.market_data.get('us_sectors', [])
        if sectors:
            lines.append("### 🎯 섹터 로테이션")

            # Sort sectors by performance
            sorted_sectors = sorted(sectors, key=lambda x: x.get('change_pct', 0), reverse=True)

            top_3 = sorted_sectors[:3]
            bottom_3 = sorted_sectors[-3:]

            lines.append("\n**상승 섹터**:")
            for i, sector in enumerate(top_3, 1):
                name = sector.get('name', '')
                change = sector.get('change_pct', 0)
                lines.append(f"{i}. {name} {change:+.2f}%")

            lines.append("\n**하락 섹터**:")
            for i, sector in enumerate(bottom_3, 1):
                name = sector.get('name', '')
                change = sector.get('change_pct', 0)
                lines.append(f"{i}. {name} {change:+.2f}%")

            # Sector rotation interpretation
            top_sector = sorted_sectors[0]['name']
            if "Energy" in top_sector or "Materials" in top_sector:
                lines.append("\n💡 **해석**: 원자재 섹터 강세 → 인플레이션 우려 또는 경기 회복 기대")
            elif "Technology" in top_sector or "Communication" in top_sector:
                lines.append("\n💡 **해석**: 테크 섹터 강세 → 성장주 선호")
            elif "Utilities" in top_sector or "Consumer Staples" in top_sector:
                lines.append("\n💡 **해석**: 방어 섹터 강세 → 경기 불확실성 대비")
            elif "Financials" in top_sector:
                lines.append("\n💡 **해석**: 금융 섹터 강세 → 금리 상승 기대 또는 경기 개선")
            lines.append("")

        # VIX
        vix = self.market_data.get('vix', {})
        if vix:
            vix_value = vix.get('value', 0)
            vix_change = vix.get('change_pct', 0)

            lines.append("### 📊 변동성 (VIX)")
            lines.append(f"- **현재 VIX**: {vix_value:.2f} ({vix_change:+.2f}%)")

            if vix_value < 15:
                lines.append("- **해석**: 매우 낮은 변동성 → 시장 안정적, 단 급등 리스크 주의")
            elif vix_value < 20:
                lines.append("- **해석**: 정상 변동성 → 시장 안정")
            elif vix_value < 30:
                lines.append("- **해석**: 높은 변동성 → 불확실성 증가")
            else:
                lines.append("- **해석**: 극도의 변동성 → 공포 심리, 위기 가능성")
            lines.append("")

        return "\n".join(lines)

    def _generate_kr_insights(self) -> str:
        """Generate Korean market insights."""
        lines = []
        lines.append("## 🇰🇷 한국 시장 분석\n")

        # Indices
        kr_indices = self.market_data.get('kr_indices', {})
        if kr_indices:
            kospi = kr_indices.get('KOSPI', {})
            kosdaq = kr_indices.get('KOSDAQ', {})

            kospi_change = kospi.get('change_pct', 0)
            kosdaq_change = kosdaq.get('change_pct', 0)

            lines.append("### 📊 지수")
            lines.append(f"- **KOSPI**: {kospi_change:+.2f}%")
            lines.append(f"- **KOSDAQ**: {kosdaq_change:+.2f}%")

            if kospi_change > 1:
                lines.append("- **강세 랠리** 진행 중")
            elif kospi_change < -1:
                lines.append("- **조정 국면** 진입")
            lines.append("")

        # Foreign/Institutional flows
        flows = self.market_data.get('kr_foreign_institutional', {})
        if flows:
            foreign = flows.get('foreign_net', 0)
            institution = flows.get('institution_net', 0)
            individual = flows.get('individual_net', 0)

            lines.append("### 💰 매매동향 (억원)")
            lines.append(f"- **외국인**: {foreign:+,}억원")
            lines.append(f"- **기관**: {institution:+,}억원")
            lines.append(f"- **개인**: {individual:+,}억원")
            lines.append("")

            # Interpretation
            if foreign > 5000:
                lines.append("💡 **외국인 대규모 순매수** → 한국 시장 매력도 상승")
            elif foreign < -5000:
                lines.append("⚠️ **외국인 대규모 순매도** → 자금 이탈 우려")

            if foreign > 0 and institution > 0:
                lines.append("✅ **외국인·기관 동반 매수** → 강력한 상승 모멘텀")
            elif foreign < 0 and institution < 0:
                lines.append("⚠️ **외국인·기관 동반 매도** → 조정 압력 강화")
            lines.append("")

        # Top stocks
        top_stocks = self.market_data.get('kr_top_stocks', [])
        if top_stocks:
            lines.append("### 🏭 주요 종목")

            # Check for semiconductor rally
            samsung = next((s for s in top_stocks if '삼성전자' in s.get('name', '')), None)
            sk_hynix = next((s for s in top_stocks if 'SK하이닉스' in s.get('name', '')), None)

            if samsung and sk_hynix:
                samsung_change = samsung.get('change_pct', 0)
                sk_change = sk_hynix.get('change_pct', 0)

                if samsung_change > 2 and sk_change > 2:
                    lines.append("🚀 **반도체 슈퍼사이클**: 삼성전자·SK하이닉스 강세")
                    lines.append(f"- 삼성전자 {samsung_change:+.2f}%, SK하이닉스 {sk_change:+.2f}%")
                    lines.append("- AI 반도체 수요 증가 반영")
                    lines.append("")

        return "\n".join(lines)

    def _generate_crypto_macro_insights(self) -> str:
        """Generate crypto and macro insights."""
        lines = []
        lines.append("## 🌍 글로벌 매크로 & 암호화폐 분석\n")

        # Treasury yields
        yields_data = self.market_data.get('treasury_yields', {})
        if yields_data:
            yield_5y = yields_data.get('^FVX', {}).get('value', 0)
            yield_10y = yields_data.get('^TNX', {}).get('value', 0)
            yield_30y = yields_data.get('^TYX', {}).get('value', 0)

            lines.append("### 📈 국채 수익률")
            lines.append(f"- **5년물**: {yield_5y:.3f}%")
            lines.append(f"- **10년물**: {yield_10y:.3f}%")
            lines.append(f"- **30년물**: {yield_30y:.3f}%")

            if yield_10y - yield_5y < 0:
                lines.append("\n⚠️ **역전 곡선** → 경기 침체 신호")
            else:
                lines.append(f"\n✅ **정상 곡선** (Spread: {yield_10y - yield_5y:.3f}%)")
            lines.append("")

        # Commodities
        commodities = self.market_data.get('commodities', {})
        if commodities:
            gold = commodities.get('GC=F', {})
            oil = commodities.get('CL=F', {})

            gold_price = gold.get('value', 0)
            gold_change = gold.get('change_pct', 0)
            oil_price = oil.get('value', 0)
            oil_change = oil.get('change_pct', 0)

            lines.append("### 🛢️ 원자재")
            lines.append(f"- **금**: ${gold_price:,.2f} ({gold_change:+.2f}%)")
            lines.append(f"- **유가**: ${oil_price:.2f} ({oil_change:+.2f}%)")

            if gold_price > 2000 and gold_change > 0:
                lines.append("\n💰 **금 강세** → 인플레이션 헤지 또는 불확실성 대비")
            lines.append("")

        # Crypto
        crypto = self.market_data.get('crypto', {})
        if crypto:
            btc = crypto.get('BTC-USD', {})
            eth = crypto.get('ETH-USD', {})

            btc_change = btc.get('change_pct', 0)
            eth_change = eth.get('change_pct', 0)

            lines.append("### ₿ 암호화폐")
            lines.append(f"- **Bitcoin**: {btc_change:+.2f}%")
            lines.append(f"- **Ethereum**: {eth_change:+.2f}%")

            if btc_change > 2 and eth_change > 2:
                lines.append("\n🟢 **Risk-On 모드** → 리스크 자산 선호도 증가")
            elif btc_change < -2 and eth_change < -2:
                lines.append("\n🔴 **Risk-Off 모드** → 리스크 회피 심리")
            lines.append("")

        return "\n".join(lines)

    def _generate_synthesis(self) -> str:
        """Generate overall market synthesis."""
        lines = []
        lines.append("## 📊 오늘의 시장 핵심 요약\n")

        # Collect key signals
        key_points = []

        # US market
        indices = self.market_data.get('us_indices', {})
        if indices:
            sp500_change = indices.get('^GSPC', {}).get('change_pct', 0)
            if abs(sp500_change) > 1:
                direction = "상승" if sp500_change > 0 else "하락"
                key_points.append(f"미국 S&P 500 {direction} ({sp500_change:+.2f}%)")

        # KR market
        flows = self.market_data.get('kr_foreign_institutional', {})
        if flows:
            foreign = flows.get('foreign_net', 0)
            if abs(foreign) > 5000:
                direction = "순매수" if foreign > 0 else "순매도"
                key_points.append(f"한국 외국인 {direction} ({foreign:+,}억원)")

        # Crypto
        crypto = self.market_data.get('crypto', {})
        if crypto:
            btc = crypto.get('BTC-USD', {})
            btc_change = btc.get('change_pct', 0)
            if abs(btc_change) > 2:
                direction = "상승" if btc_change > 0 else "하락"
                key_points.append(f"비트코인 {direction} ({btc_change:+.2f}%)")

        # Display top 3 points
        lines.append("### 🔑 핵심 포인트 (Top 3)\n")
        for i, point in enumerate(key_points[:3], 1):
            lines.append(f"{i}. {point}")
        lines.append("")

        # Investment implications
        lines.append("### 💡 투자 시사점\n")
        lines.append("**단기 전략**:")
        lines.append("- 시장 모멘텀에 따라 포지션 조정")
        lines.append("- 변동성 확대 시 방어 섹터 비중 확대")
        lines.append("")

        lines.append("**주의 사항**:")
        lines.append("- 급격한 시장 변화에 대비한 리스크 관리")
        lines.append("- 펀더멘털 확인 후 투자 결정")
        lines.append("")

        # Disclaimer
        lines.append("### ⚠️ 면책 조항\n")
        lines.append("본 분석은 교육 목적으로 제공되며, 투자 권유가 아닙니다. ")
        lines.append("실제 투자 결정은 투자자 본인의 판단과 책임하에 이루어져야 합니다.")

        return "\n".join(lines)


def generate_insights(data: Dict) -> Dict[str, str]:
    """Generate all market insights from data."""
    generator = MarketInsightsGenerator(data)
    return generator.generate_all_insights()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 generate_insights.py <market_data.json>")
        sys.exit(1)

    json_file = sys.argv[1]

    # Read market data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Generate insights
    insights = generate_insights(data)

    # Add to JSON
    data['analysis'] = insights

    # Save
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Insights generated and saved to {json_file}")

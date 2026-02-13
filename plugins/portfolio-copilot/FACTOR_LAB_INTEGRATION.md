# Factor-Lab Integration Guide

Portfolio Copilot과 Factor-Lab을 함께 사용하여 **펀더멘털 + 정량적 이중 검증**을 수행할 수 있습니다.

## Integration Strategy

### Portfolio Copilot (현재 플러그인)
- **강점**: 펀더멘털 분석, 세금 최적화, 포트폴리오 추적
- **3D 점수**: Financial Health, Valuation, Momentum
- **실전 관리**: P&L 추적, 배당 관리, VaR 분석

### Factor-Lab (별도 플러그인)
- **강점**: 정량적 팩터 분석, 백테스팅, 스크리닝
- **5-Factor 점수**: Value, Quality, Momentum, Low Volatility, Size
- **통계적 검증**: 팩터 기반 투자 전략

## Usage Workflow

### 1. 종목 분석 (이중 검증)

**Step 1: Portfolio Copilot으로 펀더멘털 평가**
```bash
cd plugins/portfolio-copilot/scripts
python3 scorecard.py AAPL
```
- ROE, 마진, 성장률 확인
- P/E, P/B 밸류에이션 평가
- 기술적 지표 (MA, RSI, MACD)

**Step 2: Factor-Lab으로 정량적 검증**
```bash
cd plugins/factor-lab/quant
python3 factor_calculator.py AAPL
```
- 5-Factor 복합 점수
- 통계적 팩터 분석
- 역사적 성과 백테스트

**결합 판단**:
- Portfolio Copilot 점수 ≥ 7.0 **AND** Factor-Lab 점수 ≥ 70 → ✅ 매수
- 둘 중 하나라도 낮음 → ⚠️ 재검토
- 둘 다 낮음 → ❌ 회피

---

### 2. 포트폴리오 스크리닝

**Factor-Lab으로 후보군 발굴**
```bash
cd plugins/factor-lab/quant
python3 screener.py --min-composite-score 70
```
결과: `current_portfolio_screening.csv` (Top 20 종목)

**Portfolio Copilot으로 세부 검증**
```bash
cd plugins/portfolio-copilot/scripts
for ticker in AAPL MSFT GOOGL; do
    python3 scorecard.py $ticker
done
```

**매수 결정**:
1. Factor-Lab 스크리닝 통과
2. Portfolio Copilot 펀더멘털 점수 확인
3. Risk Metrics로 포트폴리오 영향 평가
4. Tax Loss Harvester로 세금 최적화

---

### 3. 리밸런싱 전략

**현재 포트폴리오 분석**
```bash
# Portfolio Copilot
cd plugins/portfolio-copilot/scripts
python3 risk_metrics.py 1          # 집중도 리스크 확인
python3 benchmark_analyzer.py 1     # 성과 분석

# Factor-Lab
cd plugins/factor-lab/quant
python3 portfolio_optimizer.py      # 최적 배분 제안
```

**리밸런싱 실행**:
1. Risk Metrics에서 집중도 경고 확인
2. Factor-Lab에서 최적 포트폴리오 구성 도출
3. Tax Loss Harvester로 세금 효율적 매도 선정
4. Scorecard로 신규 매수 후보 평가

---

## Integration Points (향후 개발)

### 자동 통합 스크립트 (Phase 2)

```python
# scripts/integrated_analysis.py (미구현 - 향후 개발)

from scorecard import CompanyScorecardGenerator
# from factor_lab.quant.factor_calculator import FactorCalculator

def combined_score(ticker: str) -> Dict:
    """
    Portfolio Copilot + Factor-Lab 통합 점수

    Returns:
        {
            'ticker': str,
            'fundamental_score': float (0-10),
            'factor_score': float (0-100),
            'combined_rating': str,
            'recommendation': str
        }
    """
    # Portfolio Copilot 점수
    copilot = CompanyScorecardGenerator()
    fundamental = copilot.calculate_scorecard(ticker)

    # Factor-Lab 점수 (factor-lab이 설치된 경우에만)
    try:
        # factor_calc = FactorCalculator()
        # factor_scores = factor_calc.calculate_composite_score(ticker)
        factor_composite = 0  # placeholder
    except:
        factor_composite = None

    # 통합 평가
    if fundamental['total_score'] >= 8.0 and (factor_composite is None or factor_composite >= 75):
        recommendation = "STRONG BUY"
    elif fundamental['total_score'] >= 6.0 and (factor_composite is None or factor_composite >= 60):
        recommendation = "BUY"
    elif fundamental['total_score'] >= 5.0:
        recommendation = "HOLD"
    else:
        recommendation = "AVOID"

    return {
        'ticker': ticker,
        'fundamental_score': fundamental['total_score'],
        'factor_score': factor_composite,
        'combined_rating': recommendation
    }
```

---

## Practical Examples

### Example 1: 신규 종목 추가 결정

```bash
# 1. Factor-Lab 스크리닝으로 후보 발굴
cd plugins/factor-lab/quant
python3 screener.py --sector Technology --min-quality 70

# 2. 상위 후보 펀더멘털 검증
cd ../../portfolio-copilot/scripts
python3 scorecard.py NVDA

# 3. 포트폴리오 영향 분석
python3 risk_metrics.py 1

# 4. 세금 최적화 고려
python3 tax_loss_harvester.py 1

# 결정: NVDA 추가 시 기술 섹터 90% 집중 → 헬스케어/금융 추가 권장
```

### Example 2: 저평가 종목 발굴

```bash
# 1. Factor-Lab Value 팩터 스크리닝
cd plugins/factor-lab/quant
python3 screener.py --factor value --min-factor-score 80

# 2. Portfolio Copilot 밸류에이션 확인
cd ../../portfolio-copilot/scripts
python3 scorecard.py JNJ

# 결과: Factor-Lab Value 85점, Portfolio Copilot Valuation 8.5점
# → 이중 검증 통과, 매수 고려
```

---

## Data Compatibility

| 지표 | Portfolio Copilot | Factor-Lab | 통합 활용 |
|------|-------------------|------------|----------|
| ROE | ✅ | ✅ | Quality 검증 |
| P/E | ✅ | ✅ | Value 검증 |
| Momentum | ✅ (RSI, MACD) | ✅ (Price Momentum) | 이중 확인 |
| Volatility | ✅ (VaR) | ✅ (Low Vol Factor) | 리스크 평가 |
| Growth | ✅ (Revenue Growth) | ✅ (Earnings Growth) | Quality 평가 |

---

## Recommended Workflow

**투자 프로세스**:
1. **발굴** (Factor-Lab): 정량적 스크리닝으로 후보군 도출
2. **검증** (Portfolio Copilot): 펀더멘털 분석으로 이중 검증
3. **리스크** (Portfolio Copilot): VaR, 집중도, 분산투자 점수 확인
4. **실행** (Portfolio Copilot): 세금 최적화 고려한 매매
5. **추적** (Portfolio Copilot): P&L, 배당, 성과 모니터링
6. **재평가** (Factor-Lab): 정기적 팩터 재분석

---

## Future Enhancements

**Phase 2 (향후 개발)**:
- [ ] 자동 통합 스크립트 (`integrated_analysis.py`)
- [ ] Factor-Lab 점수를 Dashboard에 표시
- [ ] 리밸런싱 제안에 팩터 분석 반영
- [ ] 백테스트 기반 포트폴리오 최적화

**Phase 3 (AI 통합)**:
- [ ] AI가 두 플러그인 결과를 종합하여 투자 조언
- [ ] 대화형 포트폴리오 컨설팅
- [ ] 실시간 팩터 + 펀더멘털 모니터링

---

## Conclusion

Portfolio Copilot과 Factor-Lab은 **상호 보완적**입니다:

- **Portfolio Copilot**: 실전 포트폴리오 관리 (세금, P&L, 리스크)
- **Factor-Lab**: 전략 개발 및 종목 발굴 (스크리닝, 백테스팅)

두 도구를 함께 사용하면 **펀더멘털 + 정량적 이중 검증**으로 투자 성공률을 높일 수 있습니다.

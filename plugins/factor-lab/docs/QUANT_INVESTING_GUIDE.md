# 퀀트 투자 완전 가이드 (Quantitative Investing Guide)

> 통계와 데이터로 시장을 이기는 방법

## 목차

1. [퀀트 투자란 무엇인가?](#1-퀀트-투자란-무엇인가)
2. [핵심 개념: 팩터 (Factors)](#2-핵심-개념-팩터-factors)
3. [퀀트 투자 프로세스](#3-퀀트-투자-프로세스)
4. [수익 발생 메커니즘](#4-수익-발생-메커니즘)
5. [백테스팅의 중요성](#5-백테스팅의-중요성)
6. [리스크 관리](#6-리스크-관리)
7. [실전 적용 전략](#7-실전-적용-전략)
8. [퀀트 투자자가 알아야 할 필수 지식](#8-퀀트-투자자가-알아야-할-필수-지식)
9. [학습 자료 및 추천 도서](#9-학습-자료-및-추천-도서)

---

## 1. 퀀트 투자란 무엇인가?

### 정의

**퀀트 투자 (Quantitative Investing)**는 통계적 패턴과 수학적 모델을 사용하여 투자 의사결정을 자동화하는 체계적 투자 접근법입니다.

### 전통 투자 vs 퀀트 투자

| 차원 | 전통 투자 (Discretionary) | 퀀트 투자 (Quantitative) |
|------|---------------------------|--------------------------|
| **의사결정** | 주관적 판단 | 객관적 데이터 |
| **분석 방법** | "이 회사는 좋아 보인다" | "ROE > 15%, P/E < 섹터 평균" |
| **포트폴리오** | 10-20개 집중 보유 | 50-200개 분산 포트폴리오 |
| **정보 원천** | CEO 인터뷰, 산업 조사 | 가격/재무 데이터, 통계 분석 |
| **리스크** | 감정적 결정, 편향 | 규칙 기반, 일관성 |
| **확장성** | 시간 제약 (1인 분석 한계) | 자동화 가능 (무한 확장) |
| **리밸런싱** | 드물게 (년 1-2회) | 빈번 (월간/분기) |

### 퀀트 투자의 핵심 철학

1. **데이터가 직관을 이긴다**: 감정과 편향을 제거하고 데이터에 의존
2. **백테스팅으로 검증**: 전략은 역사적 데이터로 검증되어야 함
3. **분산이 리스크를 줄인다**: 50-200개 종목으로 개별 리스크 제거
4. **규칙을 준수**: 손실이 나도 전략을 유지 (감정 배제)

---

## 2. 핵심 개념: 팩터 (Factors)

### 팩터란?

**팩터 (Factor)**는 장기적으로 초과 수익(알파)을 가져다주는 주식의 특성입니다.

노벨상 수상자 Eugene Fama와 Kenneth French가 개발한 **Fama-French 5-Factor Model**이 학술적으로 검증된 팩터 모델의 표준입니다.

### 학술적으로 검증된 5대 팩터

#### 1. Value Factor (가치 팩터)

**논리**: 저평가된 주식은 평균회귀하여 상승합니다.

**측정 지표**:
- P/E Ratio (주가수익비율): 낮을수록 좋음
- P/B Ratio (주가순자산비율): 낮을수록 좋음
- EV/EBITDA: 낮을수록 좋음

**예시 전략**:
```
IF P/E < 섹터 평균 AND P/B < 1.5 THEN 매수
```

**역사적 성과**:
- 1927-2023년: 연평균 4-5% 초과 수익 (학술 연구)
- 가치 프리미엄은 장기적으로 존재하지만, 2010년대 성과 부진

**리스크**:
- 가치함정 (Value Trap): 싸지만 망해가는 기업
- 성장성 부족: 저평가 이유가 정당할 수 있음

---

#### 2. Quality Factor (품질 팩터)

**논리**: 우량 기업은 지속 가능한 수익을 창출하여 장기 수익률이 높습니다.

**측정 지표**:
- ROE (Return on Equity): > 15%
- ROA (Return on Assets): > 10%
- Debt/Equity Ratio: < 0.5
- Earnings Stability: 5년 수익 표준편차 낮음
- Free Cash Flow Margin: > 10%

**예시 전략**:
```
IF ROE > 15% AND Debt/Equity < 0.5 AND 수익 안정성 높음 THEN 매수
```

**역사적 성과**:
- Warren Buffett의 핵심 전략 (Berkshire Hathaway)
- 2000-2023년: 연평균 3-4% 초과 수익

**리스크**:
- 고평가: 우량주는 비싸게 거래됨
- 성장 둔화: 성숙 기업일 수 있음

---

#### 3. Momentum Factor (모멘텀 팩터)

**논리**: 상승 추세는 지속되는 경향이 있습니다 (행동경제학적 근거).

**측정 지표**:
- 12개월 수익률 (최근 1개월 제외): 높을수록 좋음
- 6개월 수익률: 높을수록 좋음
- 상대 강도 (Relative Strength): 섹터/시장 대비

**예시 전략**:
```
매월 말:
  과거 12개월 수익률 상위 20% 매수
  하위 20% 매도
```

**역사적 성과**:
- 1927-2023년: 연평균 8-10% 초과 수익 (가장 강력한 팩터)
- AQR Capital의 핵심 전략

**리스크**:
- 급격한 반전: 모멘텀은 갑자기 꺾일 수 있음
- 높은 변동성: 단기 손실 가능성

**왜 모멘텀이 작동하는가?**

1. **Under-reaction**: 투자자들이 뉴스에 과소 반응 → 추세 지속
2. **Herding**: 군중 심리로 추세 강화
3. **Anchoring**: 과거 가격에 고정되어 신속한 조정 실패

---

#### 4. Low Volatility Factor (저변동성 팩터)

**논리**: 저위험 주식이 고위험 주식보다 장기 수익률이 높습니다 (Low-Vol Anomaly).

**측정 지표**:
- Beta: < 0.8 (시장 대비 변동성)
- 60일 표준편차: 낮을수록 좋음
- Max Drawdown: 작을수록 좋음

**예시 전략**:
```
IF Beta < 0.8 AND 60일 변동성 < 시장 평균 THEN 매수
```

**역사적 성과**:
- 1968-2023년: Sharpe Ratio가 고변동성 주식보다 2배 높음
- 경기 침체 시 방어적 성격

**리스크**:
- 상승장 부진: Bull Market에서 상대적 수익 낮음
- 유동성 부족: 저변동성 주식은 거래량 적을 수 있음

**왜 Low-Vol이 작동하는가?**

1. **Lottery Preference**: 투자자들이 고위험/고수익 선호 (도박 성향)
2. **Leverage Constraint**: 개인 투자자는 레버리지 사용 못함 → 고베타 선호
3. **Agency Problem**: 펀드 매니저는 벤치마크 추적 압박 → 저베타 회피

---

#### 5. Size Factor (시가총액 팩터)

**논리**: 소형주가 대형주보다 높은 수익을 제공합니다.

**측정 지표**:
- Market Cap: 작을수록 좋음 (Small Cap < $2B)

**예시 전략**:
```
IF Market Cap < $2B AND 거래량 충분 THEN 매수
```

**역사적 성과**:
- 1926-2023년: 연평균 2-3% 초과 수익
- 단, 2000년대 이후 프리미엄 감소

**리스크**:
- 유동성 부족: Small Cap은 매매 어려움
- 높은 변동성: 경기 침체 시 큰 손실
- 정보 부족: 분석 리포트 적음

---

### 팩터 간 상관관계

| 팩터 | Value | Quality | Momentum | Low Vol | Size |
|------|-------|---------|----------|---------|------|
| **Value** | 1.0 | -0.2 | -0.4 | 0.1 | 0.3 |
| **Quality** | -0.2 | 1.0 | 0.2 | 0.4 | -0.1 |
| **Momentum** | -0.4 | 0.2 | 1.0 | -0.1 | 0.0 |
| **Low Vol** | 0.1 | 0.4 | -0.1 | 1.0 | -0.2 |
| **Size** | 0.3 | -0.1 | 0.0 | -0.2 | 1.0 |

**핵심 인사이트**:
- Value와 Momentum은 음의 상관관계 (-0.4) → 분산 효과
- Quality와 Low Vol은 양의 상관관계 (0.4) → 비슷한 성격
- 멀티팩터 전략은 분산 효과로 리스크 감소

---

## 3. 퀀트 투자 프로세스

### 7단계 퀀트 투자 워크플로우

```
1. Universe Definition (투자 유니버스 정의)
   ↓
2. Factor Calculation (팩터 점수 계산)
   ↓
3. Composite Score (종합 점수)
   ↓
4. Ranking & Selection (순위화 및 선택)
   ↓
5. Portfolio Construction (포트폴리오 구성)
   ↓
6. Rebalancing (리밸런싱)
   ↓
7. Performance Tracking (성과 추적)
```

### 상세 설명

#### Step 1: Universe Definition

**목적**: 투자 대상 종목을 정의합니다.

**기준**:
- 시가총액: > $1B (유동성 확보)
- 거래량: 일평균 > $1M (매매 가능성)
- 상장 기간: > 1년 (충분한 데이터)

**예시**:
- S&P 500 (미국 대형주)
- Russell 2000 (미국 소형주)
- KOSPI 200 (한국 대형주)

---

#### Step 2: Factor Calculation

**목적**: 각 종목의 팩터별 점수를 계산합니다.

**예시 (AAPL)**:
```python
Value Score:
  P/E = 31.2 (Tech 섹터 평균 35.0)
  P/B = 52.4 (고평가)
  → Value Score = 40/100

Quality Score:
  ROE = 147% (탁월)
  Debt/Equity = 1.73 (보통)
  → Quality Score = 85/100

Momentum Score:
  12M Return = +45% (강함)
  RSI = 68 (과매수 근처)
  → Momentum Score = 75/100
```

---

#### Step 3: Composite Score

**목적**: 팩터별 점수를 가중 평균하여 종합 점수를 계산합니다.

**가중치 예시**:
```
Composite Score = Value(30%) + Quality(40%) + Momentum(30%)

AAPL 예시:
= 40 × 0.30 + 85 × 0.40 + 75 × 0.30
= 12 + 34 + 22.5
= 68.5/100
```

**가중치 선택 기준**:
- 보수적 투자자: Value(40%), Quality(50%), Momentum(10%)
- 공격적 투자자: Momentum(50%), Growth(30%), Value(20%)
- 균형: Value(30%), Quality(40%), Momentum(30%)

---

#### Step 4: Ranking & Selection

**목적**: 종합 점수 순으로 정렬하여 상위 종목 선택합니다.

**예시**:
```
Rank  Ticker  Score  Sector        Selection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1     MSFT    89.2   Technology    ✅ 매수
2     GOOGL   86.5   Technology    ✅ 매수
3     NVDA    84.1   Technology    ✅ 매수
...
48    WMT     65.2   Consumer      ✅ 매수
49    PG      64.8   Consumer      ✅ 매수
50    KO      64.1   Consumer      ✅ 매수
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
→ 상위 50개 선택 (Long Portfolio)
```

---

#### Step 5: Portfolio Construction

**목적**: 선택된 종목에 자금을 배분합니다.

**배분 방식**:

1. **Equal Weight (동일 비중)**:
   - 각 종목 2% (50개 × 2% = 100%)
   - 장점: 간단, 재현 가능
   - 단점: 리스크 조정 안 됨

2. **Risk Parity (리스크 균형)**:
   - 각 종목의 리스크 기여도 동일
   - 장점: 변동성 조정
   - 단점: 복잡, 계산 비용

3. **Score-Weighted (점수 가중)**:
   - 점수 높을수록 큰 비중
   - MSFT (89.2점) = 3%, KO (64.1점) = 1.5%

**추천**: 초보자는 Equal Weight 시작

---

#### Step 6: Rebalancing

**목적**: 주기적으로 포트폴리오를 재조정합니다.

**주기**:
- 월간: 모멘텀 전략 (빠른 변화 반영)
- 분기: 멀티팩터 전략 (균형)
- 반기/연간: 가치 전략 (장기 투자)

**리밸런싱 프로세스**:
```python
매월 말:
  1. 모든 종목의 팩터 점수 재계산
  2. 종합 점수 순위 갱신
  3. 신규 진입: 상위 50위권 진입 종목 매수
  4. 퇴출: 50위권 탈락 종목 매도
  5. 비중 조정: Equal Weight 유지
```

**주의사항**:
- 거래 비용 고려 (commission + slippage)
- Tax Loss Harvesting (세금 최적화)
- 시장 충격 최소화 (큰 주문은 분할 실행)

---

#### Step 7: Performance Tracking

**목적**: 전략의 성과를 추적하고 평가합니다.

**핵심 메트릭**:

1. **Total Return (총 수익률)**:
   ```
   (최종 자산 - 초기 자산) / 초기 자산 × 100
   ```

2. **Annual Return (연평균 수익률)**:
   ```
   (1 + Total Return)^(1/Years) - 1
   ```

3. **Sharpe Ratio (샤프 비율)**:
   ```
   (수익률 - 무위험 수익률) / 변동성
   ```
   - > 1.0: 우수
   - 0.5-1.0: 양호
   - < 0.5: 부족

4. **Max Drawdown (최대 낙폭)**:
   ```
   max(고점 - 저점) / 고점 × 100
   ```
   - < 20%: 우수
   - 20-30%: 보통
   - > 30%: 높음 (감내 어려울 수 있음)

5. **Win Rate (승률)**:
   ```
   승리한 거래 / 전체 거래 × 100
   ```

**벤치마크 비교**:
- S&P 500 vs 내 전략
- Alpha = 내 수익률 - 벤치마크 수익률

---

## 4. 수익 발생 메커니즘

### 왜 퀀트 투자가 수익을 내는가?

#### 1. 행동 편향 활용 (Behavioral Biases)

**투자자의 비이성적 행동**:

- **Under-reaction**: 좋은 뉴스에 과소 반응 → 모멘텀 팩터 수익
- **Over-reaction**: 단기 뉴스에 과대 반응 → 반전 전략 수익
- **Anchoring**: 과거 가격에 고정 → 가치 팩터 수익
- **Herding**: 군중 심리 → 모멘텀 강화

**예시**:
```
애플이 실적 발표 (예상치 +20% 초과):
  Day 1: 주가 +3% 상승 (과소 반응)
  Week 1-4: 주가 추가 +7% 상승 (모멘텀 지속)
  → 퀀트 투자자는 이 패턴을 수확
```

---

#### 2. 리스크 프리미엄 (Risk Premium)

**특정 리스크를 감수하면 보상을 받습니다**:

- **가치 프리미엄**: 저평가 주식은 파산 리스크 ↑ → 보상으로 높은 수익
- **소형주 프리미엄**: Small Cap은 유동성 리스크 ↑ → 보상으로 높은 수익
- **모멘텀 프리미엄**: 추세 급반전 리스크 ↑ → 보상으로 높은 수익

**학술적 근거**:
- Fama-French (1993): "Size와 Value는 리스크 팩터"
- Asness, Moskowitz, Pedersen (2013): "Momentum도 리스크 팩터"

---

#### 3. 정보 우위 (Information Advantage)

**퀀트는 인간보다 빠르고 정확합니다**:

- 500개 종목을 동시에 분석 (인간은 10-20개 한계)
- 감정 없이 규칙 준수 (인간은 공포/탐욕에 흔들림)
- 패턴 발견 (5년 데이터에서 통계적 패턴 추출)

**예시**:
```
인간 투자자:
  "AAPL 좋아 보여" (주관적)
  "손실이 나서 불안해" (감정)

퀀트 투자자:
  "AAPL: ROE 147%, Momentum 75/100" (객관적)
  "전략대로 보유" (규칙 준수)
```

---

#### 4. 실행 일관성 (Execution Discipline)

**감정을 배제하고 규칙을 준수합니다**:

- 손실이 나도 전략 유지 (Cut Loss 금지)
- 이익이 나도 조기 청산 금지 (Let Winner Run)
- 백테스트된 전략 신뢰

**예시**:
```
Momentum 전략이 -15% 손실 중:
  인간: "이 전략은 안 먹혀" → 전략 포기 (최악의 결정)
  퀀트: "백테스트 MDD -32%였음" → 전략 유지 (회복 대기)
```

---

### Case Study: 모멘텀 전략 수익 분해

**전략**: 매월 말, 과거 12개월 수익률 상위 50종목 매수

**백테스트 결과 (2014-2024)**:
```
총 수익률:    +287%  (vs S&P 500: +215%)
Alpha:        +72%

수익 원천 분해:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Factor Premium:        +50%   (모멘텀 팩터 프리미엄)
2. Diversification:       +15%   (50종목 분산 효과)
3. Rebalancing Bonus:     +7%    (월간 리밸런싱 효과)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Alpha:              +72%
```

---

## 5. 백테스팅의 중요성

### 백테스트란?

**정의**: 역사적 데이터로 전략을 시뮬레이션하여 성과를 검증하는 과정입니다.

### 왜 백테스트가 필수인가?

1. **전략 검증**: 아이디어가 실제로 작동하는지 확인
2. **리스크 파악**: MDD, 변동성, 승률 등을 미리 알 수 있음
3. **심리적 준비**: "MDD -32%"를 미리 알면 손실 시 덜 놀람
4. **파라미터 최적화**: 가중치, 리밸런싱 주기 등을 조정

### 백테스트 필수 요소

#### 1. Point-in-Time Data (시점 데이터)

**문제**: Look-ahead bias (미래 정보 사용)

**나쁜 예시**:
```python
# ❌ 잘못된 백테스트
def backtest_2014():
    # 2014년 1월에 2014년 12월 데이터 사용 (미래 정보)
    annual_roe = get_roe("AAPL", "2014-12-31")
```

**좋은 예시**:
```python
# ✅ 올바른 백테스트
def backtest_2014_01():
    # 2014년 1월에는 2013년 Q3 데이터만 사용 (실제로 알 수 있는 정보)
    quarterly_roe = get_roe("AAPL", "2013-09-30")
```

---

#### 2. Survivorship Bias (생존 편향)

**문제**: 사라진 종목을 제외하면 성과가 왜곡됩니다.

**나쁜 예시**:
```python
# ❌ 현재 S&P 500 종목으로 과거 백테스트
universe = get_sp500_current()  # 500개 (현재 생존자)
backtest(universe, start="2014")  # 과대평가됨
```

**좋은 예시**:
```python
# ✅ 과거 시점의 실제 S&P 500 종목 사용
universe_2014 = get_sp500_at_date("2014-01-01")  # 당시 500개 (파산 종목 포함)
```

---

#### 3. Transaction Costs (거래 비용)

**반영 필수**:
- Commission: 0.05-0.1% (증권사 수수료)
- Slippage: 0.05-0.1% (주문 체결 차이)
- Market Impact: 큰 주문은 가격에 영향

**예시**:
```python
# 월간 리밸런싱, 50종목
매월 거래 비용 = (매도 25종목 + 매수 25종목) × 0.15% = 7.5% annually

실제 수익률 = 백테스트 수익률 - 7.5%
```

---

#### 4. Out-of-Sample Testing (표본 외 검증)

**목적**: 과최적화 (Overfitting) 방지

**방법**:
```
전체 데이터: 2014-2024 (10년)

In-Sample (학습):    2014-2019 (6년)
Out-of-Sample (검증): 2020-2024 (4년)

1. In-Sample로 파라미터 최적화
2. Out-of-Sample로 검증
3. Out-of-Sample 성과가 좋아야 실전 투자
```

**기준**:
- Out-of-Sample Sharpe Ratio > 0.8: 실전 가능
- Out-of-Sample Sharpe Ratio < 0.5: 재검토 필요

---

### 백테스트 해석 가이드

**좋은 전략의 기준**:
```
✅ Sharpe Ratio > 1.0
✅ Max Drawdown < 30%
✅ 승률 > 55%
✅ Out-of-Sample 성과 유지
✅ 거래 비용 반영 후에도 알파 존재
✅ 단순한 룰 (복잡도 ↓)
```

**의심해야 할 전략**:
```
❌ Sharpe Ratio > 3.0 (너무 좋으면 과최적화 의심)
❌ MDD < 10% (리스크가 너무 낮으면 버그 의심)
❌ 승률 > 80% (비현실적)
❌ Out-of-Sample 성과 급락
❌ 복잡한 룰 (10개 이상 파라미터)
```

---

## 6. 리스크 관리

### 퀀트 투자의 주요 리스크

#### 1. Model Risk (모델 리스크)

**문제**: 백테스트는 좋지만 실전에서 실패

**원인**:
- 과최적화 (Overfitting)
- 시장 구조 변화 (Regime Change)
- 블랙스완 (예상 못한 사건)

**완화 방법**:
- Out-of-Sample 검증
- 단순한 전략 선호 (Occam's Razor)
- 정기적 전략 재평가 (연 1회)

---

#### 2. Crowding Risk (혼잡 리스크)

**문제**: 너무 많은 사람이 같은 전략 사용 시 수익 감소

**예시**:
```
2018년 모멘텀 붕괴:
  너무 많은 퀀트 펀드가 모멘텀 전략 사용
  → 동시에 청산 → 급락
  → "Quant Meltdown"
```

**완화 방법**:
- 여러 비상관 전략 병행 (Momentum + Value)
- 유동성 높은 종목 선호
- 포지션 크기 제한

---

#### 3. Execution Risk (실행 리스크)

**문제**: 백테스트와 실제 거래가 다름

**원인**:
- Slippage (체결가 차이)
- 유동성 부족 (매수 불가)
- 시스템 오류 (버그, 다운타임)

**완화 방법**:
- 실전 전 Paper Trading (모의 투자)
- 작은 규모로 시작 (초기 자산 10%)
- 유동성 필터링 (일평균 거래량 > $1M)

---

#### 4. Psychological Risk (심리적 리스크)

**문제**: 손실 시 전략 포기

**예시**:
```
Momentum 전략이 -20% 손실:
  투자자: "이 전략 안 먹혀, 그만두자"
  → 최악의 타이밍에 청산
  → 이후 회복 시 수익 못 봄
```

**완화 방법**:
- 백테스트로 MDD 미리 확인
- "MDD -32%는 정상"이라고 스스로 주입
- 자동화 (감정 개입 차단)

---

### 포트폴리오 수준 리스크 관리

#### 1. Diversification (분산)

**종목 수**:
- 최소 30개 (개별 리스크 80% 제거)
- 권장 50-100개 (90% 제거)

**섹터 분산**:
```
✅ 좋은 예시:
  Technology: 25%
  Healthcare: 20%
  Consumer: 15%
  ...
  → 섹터 집중 최대 30%

❌ 나쁜 예시:
  Technology: 80%
  Others: 20%
  → 섹터 리스크 과다
```

---

#### 2. Position Sizing (포지션 크기)

**규칙**:
- 단일 종목 최대 5%
- 단일 섹터 최대 30%

**예시**:
```python
if position_weight > 0.05:
    reduce_to(0.05)  # 5% 제한
```

---

#### 3. Stop-Loss (손절매)

**퀀트에서는 권장하지 않음!**

**이유**:
- 백테스트된 MDD를 신뢰해야 함
- 손절은 전략 이탈 = 백테스트 무효화
- "손절 → 회복 시 못 탐" 반복

**대안**:
- 전략 수준에서 리스크 관리 (MDD < 30% 전략 선택)
- 포트폴리오 분산 (50-100개 종목)

---

## 7. 실전 적용 전략

### 퀀트 투자 시작하기 (단계별 가이드)

#### Step 1: 교육 (1-2개월)

**학습 목록**:
- ✅ 팩터 개념 이해
- ✅ 백테스팅 방법론
- ✅ Python 기초 (pandas, numpy)
- ✅ 통계 기초 (평균, 표준편차, 상관관계)

**추천 자료**:
- 책: "Quantitative Momentum" by Wesley Gray
- 논문: Fama-French 5-Factor Model
- 온라인 코스: QuantConnect 튜토리얼

---

#### Step 2: 백테스팅 (1-2개월)

**실습**:
1. 간단한 모멘텀 전략 백테스트
2. Sharpe Ratio, MDD 계산
3. Out-of-Sample 검증

**도구**:
- **factor-lab** (이 플러그인!)
- Backtrader (Python 라이브러리)
- QuantConnect (클라우드 플랫폼)

---

#### Step 3: Paper Trading (1-3개월)

**목적**: 실전 전 모의 투자

**방법**:
1. 가상 계좌 $100,000
2. 실제 전략대로 매매 시뮬레이션
3. 실제 거래 비용 반영

**평가 기준**:
- Paper Trading 수익률 ≈ 백테스트 수익률 ± 5%
- 3개월 이상 안정적 성과 → 실전 고려

---

#### Step 4: 실전 투자 (작게 시작)

**초기 자산**:
- 전체 자산의 10-20%만 투자
- 예: 총 자산 $100,000 → 퀀트 전략 $10,000

**점진적 확대**:
```
Month 1-3:  $10,000 (10%)
Month 4-6:  $20,000 (20%) if 성과 좋음
Month 7-12: $50,000 (50%) if 지속 성과
Year 2+:    최대 80%
```

---

### 실전 체크리스트

**투자 전**:
- [ ] 백테스트 완료 (Sharpe > 1.0, MDD < 30%)
- [ ] Out-of-Sample 검증 완료
- [ ] Paper Trading 3개월 완료
- [ ] 최악의 경우 감내 가능한 금액

**투자 중**:
- [ ] 월간 성과 리뷰
- [ ] 전략대로 리밸런싱
- [ ] 감정적 결정 금지 (손절 금지)
- [ ] 로그 기록 (실제 vs 백테스트 비교)

**투자 후**:
- [ ] 연간 성과 평가
- [ ] 전략 재검토 (시장 구조 변화?)
- [ ] 필요 시 전략 업데이트

---

## 8. 퀀트 투자자가 알아야 할 필수 지식

### 8.1. 통계 기초

#### 평균 (Mean)

```python
mean = sum(returns) / len(returns)
```

#### 표준편차 (Standard Deviation)

**의미**: 변동성 측정

```python
std = sqrt(sum((x - mean)^2) / n)
```

**해석**:
- 높은 std = 높은 리스크
- S&P 500 연간 std ≈ 15-20%

---

#### 상관관계 (Correlation)

**의미**: 두 자산이 함께 움직이는 정도

```
Correlation = -1.0 ~ +1.0

+1.0: 완전히 같이 움직임
0.0:  무관
-1.0: 완전히 반대로 움직임
```

**포트폴리오 활용**:
- 상관관계 낮은 자산 조합 → 리스크 감소
- 예: 주식 + 채권 (상관관계 -0.3)

---

#### 회귀 분석 (Regression)

**의미**: 변수 간 관계 파악

**CAPM (Capital Asset Pricing Model)**:
```
Stock Return = α + β × Market Return + ε

α (Alpha): 초과 수익
β (Beta): 시장 민감도
```

**해석**:
- α > 0: 시장 대비 초과 수익 (좋음!)
- β > 1: 시장보다 변동성 큼
- β < 1: 시장보다 안정적

---

### 8.2. 금융 수학

#### 복리 (Compound Interest)

```
최종 금액 = 초기 금액 × (1 + r)^n

예: $10,000 × (1 + 0.10)^10 = $25,937
```

**72의 법칙**:
```
돈이 2배가 되는 기간 ≈ 72 / 수익률

예: 연 10% → 72/10 = 7.2년
```

---

#### 로그 수익률 (Log Return)

**정의**:
```
log_return = ln(P_t / P_{t-1})
```

**장점**:
- 연속 복리 계산 정확
- 덧셈 가능: log(1.1 × 1.2) = log(1.1) + log(1.2)

---

#### 샤프 비율 (Sharpe Ratio)

**공식**:
```
Sharpe = (수익률 - 무위험 수익률) / 변동성

예:
수익률 = 12%
무위험 수익률 (국채) = 2%
변동성 = 15%

Sharpe = (12% - 2%) / 15% = 0.67
```

**해석**:
- > 1.0: 우수
- 0.5-1.0: 양호
- < 0.5: 부족

---

### 8.3. 프로그래밍 (Python)

#### 필수 라이브러리

```python
import pandas as pd       # 데이터 프레임
import numpy as np        # 수치 계산
import yfinance as yf     # 주식 데이터
import matplotlib.pyplot as plt  # 차트
```

#### 기본 코드 예시

```python
# 주식 데이터 가져오기
import yfinance as yf

ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1y")

# 수익률 계산
hist['Returns'] = hist['Close'].pct_change()

# 모멘텀 점수 (12개월 수익률)
momentum_score = (hist['Close'][-1] / hist['Close'][-252] - 1) * 100

print(f"AAPL 12M Return: {momentum_score:.2f}%")
```

---

### 8.4. 데이터 소스

#### 무료 데이터

| 소스 | 데이터 | 특징 |
|------|--------|------|
| **yfinance** | US 주식, ETF | 15-20분 딜레이, 무료 |
| **pykrx** | 한국 주식 | 실시간, 무료 |
| **Yahoo Finance** | 글로벌 주식 | 웹 UI, 무료 |
| **Alpha Vantage** | US 주식 + API | API 제한 있음 |

#### 유료 데이터 (프로 수준)

| 소스 | 가격 | 특징 |
|------|------|------|
| **Bloomberg Terminal** | $2,000/월 | 최고 품질, 실시간 |
| **Refinitiv Eikon** | $1,000/월 | 펀더멘털 강함 |
| **QuantConnect** | $20/월 | 백테스팅 플랫폼 |

**초보자 권장**: yfinance + pykrx (무료)

---

### 8.5. 백테스팅 플랫폼

| 플랫폼 | 특징 | 가격 | 추천 대상 |
|--------|------|------|-----------|
| **factor-lab** | 이 플러그인! | 무료 | 초보자 |
| **Backtrader** | Python 라이브러리 | 무료 | 중급자 |
| **QuantConnect** | 클라우드 플랫폼 | $20/월 | 중급자 |
| **Zipline** | Quantopian 엔진 | 무료 | 고급자 |

---

### 8.6. 퀀트 용어 사전

| 용어 | 의미 |
|------|------|
| **Alpha (α)** | 시장 대비 초과 수익 |
| **Beta (β)** | 시장 민감도 (1.0 = 시장과 동일) |
| **Factor** | 수익을 설명하는 주식 특성 |
| **Backtest** | 역사적 데이터로 전략 검증 |
| **Sharpe Ratio** | 리스크 조정 수익률 |
| **Max Drawdown (MDD)** | 최대 낙폭 |
| **Rebalancing** | 포트폴리오 재조정 |
| **Universe** | 투자 대상 종목 집합 |
| **Long-Only** | 매수만 (공매도 없음) |
| **Long-Short** | 매수 + 공매도 |
| **Overfitting** | 과최적화 (백테스트만 좋음) |
| **Survivorship Bias** | 생존 편향 (사라진 종목 제외) |
| **Look-Ahead Bias** | 미래 정보 사용 오류 |
| **Slippage** | 주문가 vs 체결가 차이 |
| **Market Impact** | 큰 주문이 가격에 미치는 영향 |

---

## 9. 학습 자료 및 추천 도서

### 9.1. 필수 도서 (입문)

1. **"Quantitative Momentum" by Wesley Gray**
   - 난이도: ★★☆☆☆
   - 내용: 모멘텀 팩터 완전 가이드
   - 추천: 퀀트 입문 최고의 책

2. **"Factor Investing and Asset Allocation" by Berkin & Swedroe**
   - 난이도: ★★☆☆☆
   - 내용: 5대 팩터 이해
   - 추천: 팩터 투자 기본서

3. **"Python for Finance" by Yves Hilpisch**
   - 난이도: ★★★☆☆
   - 내용: Python으로 퀀트 구현
   - 추천: 프로그래밍 학습

---

### 9.2. 고급 도서

4. **"Quantitative Value" by Wesley Gray & Tobias Carlisle**
   - 난이도: ★★★☆☆
   - 내용: 가치 팩터 심화
   - 추천: 가치투자 + 퀀트 융합

5. **"Advances in Financial Machine Learning" by Marcos López de Prado**
   - 난이도: ★★★★★
   - 내용: 머신러닝 퀀트
   - 추천: 고급 퀀트 필독서

6. **"Active Portfolio Management" by Grinold & Kahn**
   - 난이도: ★★★★☆
   - 내용: 포트폴리오 최적화
   - 추천: 기관 투자자 수준

---

### 9.3. 학술 논문 (무료)

1. **"Common Risk Factors in the Returns on Stocks and Bonds" (Fama-French, 1993)**
   - 3-Factor Model 원논문
   - Link: https://www.jstor.org/stable/2329112

2. **"A Five-Factor Asset Pricing Model" (Fama-French, 2015)**
   - 5-Factor Model
   - Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2287202

3. **"Value and Momentum Everywhere" (Asness et al., 2013)**
   - 글로벌 팩터 검증
   - Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2174501

---

### 9.4. 온라인 강의

1. **QuantConnect Tutorial**
   - 무료, 백테스팅 플랫폼
   - Link: https://www.quantconnect.com/tutorials

2. **Coursera: Machine Learning for Trading**
   - Georgia Tech, 유료
   - 난이도: ★★★☆☆

3. **YouTube: QuantInsti**
   - 무료, 퀀트 기초 강의
   - Link: https://youtube.com/@quantinsti

---

### 9.5. 커뮤니티 & 포럼

1. **Quantitative Finance Stack Exchange**
   - Q&A 플랫폼
   - Link: https://quant.stackexchange.com

2. **r/algotrading (Reddit)**
   - 알고리즘 트레이딩 커뮤니티
   - Link: https://reddit.com/r/algotrading

3. **Quantopian Forum (아카이브)**
   - 과거 자료 보관소
   - Link: https://www.quantopian.com/posts

---

### 9.6. 데이터 & 도구

1. **QuantConnect**
   - 클라우드 백테스팅
   - Link: https://www.quantconnect.com

2. **Portfolio Visualizer**
   - 무료 백테스팅 (웹)
   - Link: https://www.portfoliovisualizer.com

3. **factor-lab**
   - 이 플러그인! (로컬 백테스팅)

---

## 마무리

### 퀀트 투자 성공의 핵심

1. ✅ **데이터 기반 의사결정**: 감정을 배제하고 팩터에 의존
2. ✅ **백테스트로 검증**: 실전 전 반드시 역사적 검증
3. ✅ **분산으로 리스크 관리**: 50-100개 종목 분산
4. ✅ **규칙 준수**: 손실이 나도 전략 유지
5. ✅ **지속적 학습**: 시장은 변화하므로 학습 필수

### 다음 단계

1. **factor-lab 플러그인으로 실습**:
   ```bash
   cd plugins/factor-lab
   python3 quant/factor_screener.py --universe SP500 --top-n 20
   ```

2. **첫 백테스트 실행**:
   ```bash
   python3 quant/backtest_engine.py --strategy momentum --universe SP500
   ```

3. **Paper Trading 시작** (모의 투자 3개월)

4. **실전 투자** (작게 시작, 점진적 확대)

---

**면책 조항**: 이 문서는 교육 목적입니다. 투자 결정은 본인 책임이며, 과거 성과가 미래를 보장하지 않습니다. 실전 투자 전 충분한 학습과 Paper Trading을 권장합니다.

**작성일**: 2026-02-13
**버전**: 1.0
**작성자**: factor-lab Plugin

---

**이 문서가 도움이 되셨다면 ⭐ GitHub Star를 부탁드립니다!**

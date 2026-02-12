# Market-Pulse Roadmap: 장기 가치투자자용

**투자 스타일**: 장기 가치투자 (Value Investing)
**목표**: 저평가된 우량 기업 발굴 및 장기 보유

---

## 📊 Phase 1: MVP 완료 (2025-01-25 완료)

### ✅ 완료된 기능
- [x] SQLite 데이터베이스 (60일 히스토리 저장)
- [x] Technical Indicators 엔진 (RSI, MACD, 이동평균)
- [x] 60일 데이터 자동 수집 및 DB 저장
- [x] 60일 트렌드 차트 (S&P 500, NASDAQ, Dow Jones)
- [x] 미국/한국 시장 지수 실시간 조회
- [x] 섹터 성과 분석 (1일)
- [x] Financial Times 스타일 HTML 대시보드

### 🎯 현재 사용 가능
```bash
cd plugins/market-pulse/skills/market-pulse
claude-code --skill market-pulse
```

---

## 🚀 Phase 2: 펀더멘털 분석 강화 (우선순위: 높음)

**목표**: 저평가 종목 발굴 및 밸류에이션 분석

### 2.1 밸류에이션 지표 통합 (4주)

#### Task 2.1.1: UsStockInfo MCP 클라이언트 구현
**파일**: `plugins/market-pulse/mcp/usstock_client.py`

```python
class UsStockInfoClient:
    """UsStockInfo MCP 도구 통합"""

    def get_fundamental_metrics(self, ticker: str) -> Dict:
        """
        펀더멘털 지표 조회
        - PER (주가수익비율)
        - PBR (주가순자산비율)
        - PEG (성장 대비 밸류에이션)
        - ROE (자기자본이익률)
        - 부채비율
        - 배당수익률
        """
        pass

    def get_analyst_ratings(self, ticker: str) -> Dict:
        """애널리스트 의견 및 목표가"""
        pass

    def get_earnings_calendar(self, ticker: str) -> Dict:
        """실적 발표 일정"""
        pass
```

**예상 시간**: 6시간
**의존성**: UsStockInfo MCP (이미 사용 가능)

---

#### Task 2.1.2: 밸류에이션 스크리너
**파일**: `plugins/market-pulse/analysis/value_screener.py`

```python
class ValueScreener:
    """저평가 종목 스크리닝"""

    def screen_undervalued_stocks(self, sector: str = None) -> List[Dict]:
        """
        저평가 종목 필터링 기준:
        - PER < 15 (시장 평균 대비 저평가)
        - PBR < 1.5
        - 부채비율 < 100% (재무 건전성)
        - ROE > 10% (수익성)
        - 배당수익률 > 2%
        """
        pass

    def compare_sector_valuation(self, sector: str) -> Dict:
        """섹터 내 밸류에이션 비교"""
        pass
```

**예상 시간**: 8시간

---

#### Task 2.1.3: HTML 대시보드 - 밸류에이션 섹션 추가
**파일**: `plugins/market-pulse/config/generate_html.py`

**추가 섹션**:
```html
<div class="card" style="grid-column: 1 / -1;">
    <div class="card-title">💎 저평가 종목 발굴 (Value Opportunities)</div>
    <table>
        <thead>
            <tr>
                <th>Symbol</th>
                <th>Company</th>
                <th>Price</th>
                <th>PER</th>
                <th>PBR</th>
                <th>배당률</th>
                <th>Value Score</th>
            </tr>
        </thead>
        <tbody>
            <!-- 저평가 종목 목록 -->
        </tbody>
    </table>
</div>
```

**예상 시간**: 4시간

---

### 2.2 교육 콘텐츠 (Task 4) - 장기 투자자용

**파일**: `plugins/market-pulse/config/educational_content.yaml`

```yaml
# 밸류에이션 지표
valuation:
  per:
    name: "PER (Price-to-Earnings Ratio)"
    description: |
      주가수익비율. 주가를 주당순이익(EPS)으로 나눈 값.
      낮을수록 저평가, 높을수록 고평가.

      해석:
      - PER < 10: 저평가 (단, 성장성 확인 필요)
      - PER 10-20: 적정 평가
      - PER > 25: 고평가 (성장주는 예외)

      주의: 산업별 차이 큼. 동종 업계와 비교 필수.

  pbr:
    name: "PBR (Price-to-Book Ratio)"
    description: |
      주가순자산비율. 주가를 주당순자산(BPS)으로 나눈 값.

      해석:
      - PBR < 1: 장부가보다 싸게 거래 (저평가 가능성)
      - PBR 1-3: 적정
      - PBR > 5: 고평가 (IT/바이오는 예외)

  peg:
    name: "PEG (Price/Earnings to Growth)"
    description: |
      PER을 이익 성장률로 나눈 값.
      성장성을 고려한 밸류에이션.

      해석:
      - PEG < 1: 저평가 (성장 대비 싸다)
      - PEG 1-2: 적정
      - PEG > 2: 고평가

# 재무 건전성
financial_health:
  debt_ratio:
    name: "부채비율"
    description: |
      총부채를 자기자본으로 나눈 값.

      해석:
      - < 100%: 안전 (자본 > 부채)
      - 100-200%: 보통
      - > 200%: 위험 (차입 과다)

  roe:
    name: "ROE (Return on Equity)"
    description: |
      자기자본이익률. 자기자본 대비 순이익.
      기업의 수익 창출 능력.

      해석:
      - > 15%: 우수
      - 10-15%: 양호
      - < 10%: 부진

# 배당 투자
dividend:
  yield:
    name: "배당수익률"
    description: |
      연간 배당금을 주가로 나눈 값.

      해석:
      - > 4%: 고배당주
      - 2-4%: 적정
      - < 2%: 저배당

      주의: 배당성향(배당/이익)도 확인 필요.

# 장기 투자 전략
strategies:
  value_investing:
    name: "가치투자 (Value Investing)"
    description: |
      워렌 버핏의 투자 철학:
      "내재가치보다 싸게 사서 오래 보유하라"

      핵심 원칙:
      1. 저평가 종목 찾기 (PER, PBR 낮은 종목)
      2. 재무 건전성 확인 (부채비율, ROE)
      3. 경쟁 우위 (브랜드, 기술, 네트워크)
      4. 안전마진 확보 (내재가치의 70% 이하 매수)
      5. 장기 보유 (최소 3-5년)

      체크리스트:
      - [ ] PER < 업계 평균?
      - [ ] PBR < 2?
      - [ ] 부채비율 < 100%?
      - [ ] ROE > 10%?
      - [ ] 배당 안정적?
      - [ ] 10년 후에도 살아남을 기업?

  dividend_investing:
    name: "배당 투자"
    description: |
      안정적인 현금 흐름 확보 전략.

      배당 귀족주 (Dividend Aristocrat):
      25년 이상 연속 배당 증가 기업.

      장점:
      - 정기적인 현금 수입
      - 하락장에서 방어적
      - 복리 효과 (재투자)
```

**예상 시간**: 6시간

---

### 2.3 섹터 히트맵 확장 (Task 8)

**파일**: `plugins/market-pulse/config/generate_html.py`

```javascript
// 섹터 히트맵 (1일/1주/1개월 비교)
const sectorHeatmapData = {
    labels: ['Tech', 'Healthcare', 'Finance', ...],
    datasets: [
        { label: '1 Day', data: [2.1, -0.5, 1.2, ...] },
        { label: '1 Week', data: [5.3, 2.1, -1.5, ...] },
        { label: '1 Month', data: [12.5, 8.3, -3.2, ...] }
    ]
};

// 히트맵 시각화 (색상 강도로 성과 표시)
// 초록: 강세 섹터, 빨강: 약세 섹터
```

**예상 시간**: 6시간

---

## 🎯 Phase 2.5: 투자 대가 전략 구현 (우선순위: 매우 높음)

**목표**: 검증된 투자 대가들의 전략을 자동화하여 투자 결정 지원

### 2.5.1 그레이엄/버핏: 안전마진 계산기

**파일**: `plugins/market-pulse/analysis/intrinsic_value.py`

```python
class IntrinsicValueCalculator:
    """내재가치 및 안전마진 계산"""

    def calculate_graham_value(self, ticker: str) -> Dict:
        """
        그레이엄 공식: IV = EPS × (8.5 + 2g)

        Returns:
            - intrinsic_value: 내재가치
            - current_price: 현재가
            - margin_of_safety: 안전마진 (%)
            - recommendation: 매수/관망/매도
        """
        pass

    def calculate_dcf_value(self, ticker: str) -> Dict:
        """
        DCF (현금흐름할인법) 내재가치
        = Σ(미래 FCF / (1+할인율)^n)
        """
        pass
```

**HTML 대시보드**:
```html
📈 안전마진 Top 10 (그레이엄 기준)
┌─────────────┬──────┬──────┬─────────┬──────┐
│ 종목        │ 내재 │ 현재 │ 안전마진│ 추천 │
├─────────────┼──────┼──────┼─────────┼──────┤
│ INTC        │ $65  │ $45  │ 31% ✅  │ 매수 │
│ BAC         │ $42  │ $32  │ 24%     │ 매수 │
└─────────────┴──────┴──────┴─────────┴──────┘
```

**예상 시간**: 8시간 ⭐⭐⭐⭐⭐

---

### 2.5.2 피터 린치: PEG 스크리너 + 6가지 주식 분류

**파일**: `plugins/market-pulse/analysis/lynch_classifier.py`

```python
class LynchClassifier:
    """피터 린치의 6가지 주식 분류 및 PEG 분석"""

    CATEGORIES = {
        'slow_grower': '성장률 0-4% (배당 목적)',
        'stalwart': '성장률 10-12% (안정적)',
        'fast_grower': '성장률 20%+ (Ten Bagger 후보!)',
        'cyclical': '경기순환주 (타이밍 중요)',
        'turnaround': '회생주 (고위험 고수익)',
        'asset_play': '자산주 (부동산/자원)'
    }

    def classify_stock(self, ticker: str) -> Dict:
        """
        자동 분류 로직:
        - 성장률 기반
        - 섹터 특성 고려
        - PEG 비율 계산
        """
        pass

    def find_ten_baggers(self) -> List[Dict]:
        """
        Ten Bagger 후보 발굴:
        - 성장률 > 20%
        - PEG < 1.5
        - 소형주 선호
        """
        pass
```

**HTML 출력**:
```html
🚀 Ten Bagger 후보 (Fast Growers, PEG < 1.5)
┌────────┬─────────┬──────┬─────┬──────────┐
│ 종목   │ 성장률  │ PEG  │ 분류│ 린치점수 │
├────────┼─────────┼──────┼─────┼──────────┤
│ NVDA   │ 45%     │ 0.9  │ FG  │ ⭐⭐⭐⭐⭐│
│ META   │ 28%     │ 1.2  │ FG  │ ⭐⭐⭐⭐ │
└────────┴─────────┴──────┴─────┴──────────┘
```

**예상 시간**: 10시간 ⭐⭐⭐⭐⭐

---

### 2.5.3 찰리 멍거: 역행 사고 체크리스트

**파일**: `plugins/market-pulse/analysis/munger_inversion.py`

```python
class MungerInversionChecker:
    """
    역행 사고: "이 종목은 왜 실패할까?"
    실패 원인을 먼저 찾아 제거
    """

    def check_failure_risks(self, ticker: str) -> Dict:
        """
        리스크 체크리스트:
        1. 고레버리지 (부채비율 > 200%)
        2. 회계 품질 (Altman Z-Score < 1.8)
        3. 내부자 매도 (임원 매도 > 50%)
        4. 산업 쇠퇴 (섹터 CAGR < 0%)
        5. 고객 집중도 (단일 고객 > 50% 매출)
        6. 소송/규제 리스크

        Returns:
            - risks: 발견된 리스크 목록
            - risk_score: 0-6점
            - recommendation: 피하라/주의/괜찮음
        """
        pass

    def calculate_altman_z_score(self, ticker: str) -> float:
        """
        Altman Z-Score (파산 예측 모델):
        Z < 1.8: 파산 위험
        Z 1.8-3.0: 회색 지대
        Z > 3.0: 안전
        """
        pass
```

**HTML 출력**:
```html
🚨 멍거 역행 체크 (피해야 할 종목)
┌────────┬───────────────────────────┬──────┬──────┐
│ 종목   │ 리스크                    │ 점수 │ 추천 │
├────────┼───────────────────────────┼──────┼──────┤
│ RIVN   │ 부채↑, 내부자매도↑, 적자 │ 4/6  │ 피함 │
│ BBBY   │ 파산위험, Z<1, 사양산업   │ 6/6  │ 피함 │
└────────┴───────────────────────────┴──────┴──────┘
```

**예상 시간**: 8시간 ⭐⭐⭐⭐

---

### 2.5.4 클리프 애스니스: 멀티팩터 스코어링

**파일**: `plugins/market-pulse/analysis/factor_scoring.py`

```python
class FactorScorer:
    """5가지 팩터 기반 퀀트 스코어링"""

    FACTORS = {
        'value': 'PER, PBR 기반 저평가 점수',
        'momentum': '6개월 수익률 기반 추세',
        'quality': 'ROE, 이익 안정성',
        'low_volatility': '변동성 낮을수록 높은 점수',
        'size': '소형주 프리미엄'
    }

    def calculate_factor_scores(self, ticker: str) -> Dict:
        """
        각 팩터별 0-10점 부여

        Value: PER < 10 → 10점, PER > 30 → 0점
        Momentum: 6M 수익률 +20% → 10점, -20% → 0점
        Quality: ROE > 20% → 10점, ROE < 5% → 0점
        Low Vol: 변동성 < 10% → 10점, > 50% → 0점
        Size: 시총 < $2B → 10점, > $100B → 0점

        Returns:
            - factor_scores: 각 팩터 점수
            - total_score: 총점 (0-50점)
            - percentile: 상위 몇 %인지
        """
        pass

    def screen_multi_factor(self, top_n: int = 20) -> List[Dict]:
        """
        멀티팩터 스크리닝:
        1. 모든 종목에 팩터 점수 부여
        2. 총점 상위 N% 추출
        3. 섹터 다각화 고려
        """
        pass
```

**HTML 출력**:
```html
🏆 멀티팩터 Top 10 (상위 5%)
┌──────┬────┬────┬────┬────┬────┬─────┬──────┐
│종목  │Val │Mom │Qua │Vol │Siz │Total│순위  │
├──────┼────┼────┼────┼────┼────┼─────┼──────┤
│BRK.B │ 9  │ 6  │ 10 │ 8  │ 0  │ 33  │상위1%│
│COST  │ 6  │ 8  │ 9  │ 7  │ 0  │ 30  │상위3%│
│LOW   │ 8  │ 7  │ 8  │ 6  │ 5  │ 34  │상위1%│
└──────┴────┴────┴────┴────┴────┴─────┴──────┘
```

**예상 시간**: 12시간 ⭐⭐⭐⭐⭐

---

### 2.5.5 레이 달리오: 경제 사이클 판별기

**파일**: `plugins/market-pulse/analysis/economic_regime.py`

```python
class EconomicRegimeDetector:
    """
    달리오의 4가지 경제 상태 자동 판별
    """

    REGIMES = {
        'growth_low_inflation': '성장 + 저인플레 (주식 강세장)',
        'growth_high_inflation': '성장 + 고인플레 (원자재↑)',
        'recession_low_inflation': '침체 + 저인플레 (채권↑)',
        'recession_high_inflation': '침체 + 고인플레 (금↑, 최악)'
    }

    def detect_current_regime(self) -> Dict:
        """
        현재 경제 상태 판별:
        - GDP 성장률 (Fed API)
        - CPI 인플레이션 (Fred API)

        Returns:
            - regime: 4가지 중 하나
            - gdp_growth: GDP YoY
            - inflation: CPI YoY
            - recommended_allocation: 자산 배분 권장
        """
        pass

    def get_all_weather_allocation(self) -> Dict:
        """
        올웨더 포트폴리오:
        - 주식: 30%
        - 장기 국채: 40%
        - 중기 국채: 15%
        - 금: 7.5%
        - 원자재: 7.5%
        """
        return {
            'stocks': 30,
            'long_bonds': 40,
            'mid_bonds': 15,
            'gold': 7.5,
            'commodities': 7.5
        }
```

**HTML 출력**:
```html
📊 달리오 경제 사이클 분석
┌─────────────────────────────┐
│ 현재 상태: 성장 + 저인플레  │
│ GDP: +2.8% | CPI: +2.1%     │
├─────────────────────────────┤
│ 추천 자산 배분 (올웨더):    │
│ 주식  ████████████ 50%      │
│ 채권  ██████ 30%            │
│ 금    ██ 10%                │
│ 원자재 ██ 10%               │
└─────────────────────────────┘
```

**예상 시간**: 10시간 ⭐⭐⭐⭐

---

### 2.5.6 기업 심층 분석 (Company Deep Dive) 🆕

**파일**: `plugins/market-pulse/analysis/company_deepdive.py`

```python
class CompanyDeepDive:
    """
    특정 기업에 대한 종합 분석 리포트
    투자 대가들의 관점을 모두 적용
    """

    def analyze_company(self, ticker: str) -> Dict:
        """
        종합 분석 리포트:

        1. 기업 개요
           - 사업 모델, 섹터, 시가총액
           - 주요 제품/서비스
           - 경쟁사 비교

        2. 밸류에이션 분석 (그레이엄/버핏)
           - 내재가치 계산 (Graham, DCF)
           - 안전마진
           - PER, PBR, PEG

        3. 성장성 분석 (피터 린치)
           - 6가지 분류
           - 이익 성장률 (3년, 5년)
           - Ten Bagger 가능성

        4. 품질 분석 (버핏/멍거)
           - 경제적 해자 (Moat)
           - ROE, 이익률
           - 재무 건전성 (부채비율)

        5. 리스크 분석 (멍거 역행 사고)
           - 실패 가능성 체크
           - Altman Z-Score
           - 산업/경쟁 리스크

        6. 팩터 점수 (애스니스)
           - Value, Momentum, Quality, Low Vol, Size
           - 종합 점수 및 순위

        7. 기술적 분석
           - RSI, MACD
           - 60일 트렌드
           - 지지/저항선

        8. 투자 의견 종합
           - 매수/보유/매도 추천
           - 목표가 범위
           - 리스크/보상 비율

        Returns:
            완전한 분석 리포트 (HTML/PDF)
        """
        pass

    def generate_report_html(self, analysis: Dict) -> str:
        """상세 HTML 리포트 생성"""
        pass

    def get_investment_score(self, analysis: Dict) -> int:
        """
        종합 투자 점수 (0-100점):
        - 밸류에이션: 25점
        - 성장성: 20점
        - 품질: 25점
        - 리스크: -30점 (감점)
        - 팩터: 20점
        - 타이밍: 10점
        """
        pass
```

**사용 예시**:
```bash
$ market-pulse deep-dive AAPL

📊 Apple Inc. (AAPL) 심층 분석 리포트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 종합 투자 점수: 78/100 (매수 추천)

1️⃣ 기업 개요
   - 섹터: Technology (Consumer Electronics)
   - 시가총액: $2.8T (Large Cap)
   - 사업: iPhone, Mac, Services, Wearables

2️⃣ 밸류에이션 (그레이엄/버핏) ⭐⭐⭐⭐
   - 내재가치 (Graham): $185
   - 내재가치 (DCF): $195
   - 현재가: $175
   - 안전마진: +5.7% ✅
   - PER: 28.5 (고평가)
   - PBR: 42.3 (매우 고평가)
   - 버핏 평가: "브랜드 파워 강함, 가격은 비쌈"

3️⃣ 성장성 (피터 린치) ⭐⭐⭐
   - 분류: Stalwart (우량주)
   - 성장률: 8% (3년 평균)
   - PEG: 3.6 (고평가, >2)
   - 린치 평가: "안정적이나 Ten Bagger는 어려움"

4️⃣ 품질 (버핏/멍거) ⭐⭐⭐⭐⭐
   - 경제적 해자: 매우 강함 (브랜드 + 생태계)
   - ROE: 147% (매우 우수)
   - 영업이익률: 30.1%
   - 부채비율: 171% (보통)
   - 버핏 평가: "최고 품질 기업"

5️⃣ 리스크 (멍거 역행 사고) ⭐⭐⭐⭐
   - 리스크 점수: 2/6 (낮음)
   - ⚠️ 중국 매출 의존도 높음 (18%)
   - ⚠️ iPhone 매출 집중도 (52%)
   - ✅ Z-Score: 4.2 (안전)
   - 멍거 평가: "큰 리스크 없음"

6️⃣ 팩터 점수 (애스니스) ⭐⭐⭐
   - Value: 3/10 (비쌈)
   - Momentum: 7/10 (상승 추세)
   - Quality: 10/10 (최고 품질)
   - Low Vol: 8/10 (안정적)
   - Size: 0/10 (대형주)
   - 총점: 28/50 (상위 40%)

7️⃣ 기술적 분석 ⭐⭐⭐⭐
   - RSI: 58 (중립)
   - MACD: 매수 신호
   - 60일 추세: 상승 중
   - 지지선: $165, 저항선: $185

8️⃣ 투자 의견
   ━━━━━━━━━━━━━━━━━━━━━━━━━
   추천: 매수 (Buy)
   목표가: $195 (상승 여력 +11%)
   투자 전략: 분할 매수 (조정 시 추가)
   보유 기간: 3-5년 (장기)

   워렌 버핏: "최고 품질이지만 가격이 비쌈.
              $165 이하로 내려오면 강력 매수"

   피터 린치: "훌륭한 기업이나 성장은 둔화.
               PEG 3.6은 부담. 30% 수익 후 일부 매도 고려"

   찰리 멍거: "리스크 낮고 해자 강함.
               장기 보유 적합"
```

**HTML 리포트 출력**:
- 각 섹션별 상세 차트/표
- 경쟁사 비교 (MSFT, GOOG)
- 5년 재무 트렌드
- 애널리스트 의견 요약

**예상 시간**: 16시간 ⭐⭐⭐⭐⭐

---

## 🔬 Phase 3: RSI & 매수 타이밍 (우선순위: 중간)

장기 투자자도 "좋은 가격"에 사는 것이 중요합니다.

### 3.1 RSI 차트 (Task 9)

**파일**: `plugins/market-pulse/config/generate_html.py`

```html
<div class="card" style="grid-column: 1 / -1;">
    <div class="card-title">📉 RSI - 매수 타이밍 분석</div>
    <div style="display: flex; flex-direction: column; gap: 24px;">
        <!-- S&P 500 RSI -->
        <div>
            <div style="font-weight: bold; color: #2563eb;">S&P 500 RSI</div>
            <canvas id="rsiSP500Chart" height="150"></canvas>
            <div class="rsi-zone">
                🟢 RSI < 30: 과매도 (저점 매수 기회)
                🟡 RSI 30-70: 중립
                🔴 RSI > 70: 과매수 (조정 대기)
            </div>
        </div>
    </div>
</div>
```

**장기 투자자 활용법**:
- RSI < 30: 분할 매수 시작
- RSI 회복 (30 → 50): 추가 매수
- RSI > 70: 매수 중단, 기다림

**예상 시간**: 6시간

---

## 📚 Phase 4: 고급 분석 도구 (우선순위: 중간)

### 4.1 필립 피셔: 15가지 질문 AI 인터뷰

**파일**: `plugins/market-pulse/analysis/fisher_interview.py`

```python
class FisherInterviewer:
    """
    AI 기반 기업 분석 인터뷰
    피셔의 15가지 질문 자동 답변
    """

    FIFTEEN_QUESTIONS = [
        "향후 수년간 매출을 크게 늘릴 제품/서비스가 있는가?",
        "신제품 개발 능력이 있는가?",
        "연구개발 노력이 효과적인가?",
        # ... (15개 질문)
    ]

    def interview_company(self, ticker: str) -> Dict:
        """
        각 질문에 대해:
        1. UsStockInfo에서 데이터 수집
        2. 뉴스 API에서 관련 정보 검색
        3. AI가 종합 답변 생성
        4. 점수 부여 (0-10점)

        Returns:
            - answers: 15개 질문 답변
            - total_score: 총점 (/150)
            - recommendation: 매수/보유/매도
        """
        pass
```

**예상 시간**: 20시간 ⭐⭐⭐

---

### 4.2 백테스팅 시스템

**파일**: `plugins/market-pulse/backtest/strategy_tester.py`

```python
class StrategyBacktester:
    """투자 전략 백테스팅"""

    STRATEGIES = {
        'graham': '그레이엄 전략 (PER<15, PBR<1.5)',
        'lynch': '린치 전략 (PEG<1.5, 성장률>20%)',
        'buffett': '버핏 전략 (ROE>15%, Moat)',
        'asness': '팩터 전략 (멀티팩터 상위 20%)'
    }

    def backtest(
        self,
        strategy: str,
        start_date: str,
        end_date: str,
        initial_capital: float = 10000
    ) -> Dict:
        """
        백테스팅 결과:
        - 연평균 수익률
        - 최대 낙폭 (MDD)
        - 샤프 비율
        - 승률
        - 베스트/워스트 종목
        - S&P 500 대비 초과 수익
        """
        pass

    def compare_strategies(self, strategies: List[str]) -> Dict:
        """여러 전략 비교 분석"""
        pass
```

**사용 예시**:
```bash
$ market-pulse backtest --strategy graham --period 2014-2024

그레이엄 전략 백테스트 (2014-2024)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
연평균 수익률: 12.3% (S&P 500: 9.8%)
최대 낙폭: -28% (S&P 500: -34%)
샤프 비율: 0.85 (S&P 500: 0.72)
승률: 68%

최고 성과: BAC (+180%), INTC (+95%)
최악 성과: GE (-40%), IBM (-15%)
```

**예상 시간**: 30시간 ⭐⭐⭐⭐

---

## 💎 Phase 5: 포트폴리오 관리 (우선순위: 낮음)

장기 보유 종목 추적 및 리밸런싱.

### 5.1 Watchlist & 목표가 알림

**파일**: `plugins/market-pulse/config/watchlist.yaml`

```yaml
watchlist:
  - symbol: AAPL
    name: "Apple Inc."
    entry_price: 180.00
    target_price: 220.00
    stop_loss: 160.00
    notes: "워렌 버핏 보유, 안정적 배당"

  - symbol: JNJ
    name: "Johnson & Johnson"
    entry_price: 150.00
    target_price: 180.00
    notes: "배당 귀족주, 60년 연속 배당 증가"
```

**알림 로직**:
- 목표가 도달 → 📢 알림
- 10% 하락 → 📢 추가 매수 기회 알림
- 실적 발표 1주일 전 → 📢 리마인더

**예상 시간**: 8시간

---

### 5.2 포트폴리오 수익률 추적

**파일**: `plugins/market-pulse/portfolio/tracker.py`

```python
class PortfolioTracker:
    """포트폴리오 수익률 추적"""

    def track_holdings(self) -> Dict:
        """
        보유 종목 현황:
        - 매수 평균가
        - 현재가
        - 수익률 (%)
        - 배당 수익
        """
        pass

    def suggest_rebalancing(self) -> List[str]:
        """리밸런싱 권장사항"""
        pass
```

**예상 시간**: 10시간

---

## 🤖 Phase 6: AI 포트폴리오 코치 (우선순위: 낮음, 장기 비전)

**목표**: 모든 투자 대가들의 관점을 종합한 AI 조언자

### 6.1 포트폴리오 진단 및 조언

**파일**: `plugins/market-pulse/ai/portfolio_coach.py`

```python
class PortfolioCoach:
    """
    AI 포트폴리오 코치
    사용자 포트폴리오 분석 및 투자 대가들의 관점으로 조언
    """

    def analyze_portfolio(self, portfolio_file: str) -> Dict:
        """
        포트폴리오 종합 분석:
        1. 현재 상태 진단
        2. 각 투자 대가의 관점 분석
        3. 개선 제안
        4. 리스크 평가
        """
        pass

    def get_master_opinions(self, portfolio: Dict) -> Dict:
        """
        각 투자 대가의 관점:

        워렌 버핏:
        - 집중도 분석 (상위 5개 비중)
        - 해자 있는 기업 비율
        - 평균 보유 기간

        피터 린치:
        - 6가지 분류별 배분
        - PEG 평균
        - Ten Bagger 후보 포함 여부

        레이 달리오:
        - 자산군별 배분 (주식/채권/금/원자재)
        - 리스크 패리티
        - 경제 사이클 대응

        클리프 애스니스:
        - 팩터 노출도
        - 다각화 점수
        - 샤프 비율

        찰리 멍거:
        - 리스크 높은 종목 비율
        - 역행 체크 실패 종목
        """
        pass

    def generate_improvement_plan(self, analysis: Dict) -> List[str]:
        """
        개선 계획:
        - 매도 추천 (이유와 함께)
        - 매수 추천 (대체 종목)
        - 비중 조정 (리밸런싱)
        """
        pass
```

**사용 예시**:
```bash
$ market-pulse coach --portfolio my_portfolio.json

🤖 AI 포트폴리오 코치 분석
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 현재 포트폴리오 진단:
   - 총 자산: $50,000
   - 종목 수: 8개
   - 섹터 집중도: Technology 70% (⚠️ 높음)
   - 평균 보유 기간: 1.2년

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 투자 대가들의 조언:

워렌 버핏:
"기술주에 70% 집중은 위험합니다. 소비재, 금융 섹터
추가를 강력히 권장합니다. AAPL, MSFT는 좋은 선택이나
비중을 각 15%로 줄이세요."

추천 조정:
- AAPL: 25% → 15% (매도 $5,000)
- MSFT: 20% → 15% (매도 $2,500)
- 추가 매수: JNJ $3,000, PG $2,500, JPM $2,000

피터 린치:
"포트폴리오에 Fast Grower가 부족합니다.
NVDA (PEG 0.9)를 10% 추가하면 장기 수익률
개선될 것입니다."

추천: NVDA $5,000 매수

레이 달리오:
"주식 100%는 변동성이 너무 큽니다.
채권 20%, 금 5% 추가로 리스크 감소하세요."

추천 배분:
- 주식: 100% → 70%
- 채권 ETF (AGG): 0% → 20%
- 금 ETF (GLD): 0% → 10%

클리프 애스니스:
"포트폴리오 팩터 분석:
- Value: 낮음 (평균 PER 32)
- Momentum: 높음 (6M 수익률 +15%)
- Quality: 높음 (평균 ROE 25%)

Value 팩터 보강 필요. BAC, INTC 추가 권장."

찰리 멍거:
"리스크 체크:
- TSLA: 부채비율 200%, 변동성 높음 → 비중 축소
- RIVN: 적자 지속, 리스크 6/6 → 매도 권장"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 종합 개선 계획:

1. 매도 (총 $10,000):
   - RIVN 전량 매도 ($3,000)
   - AAPL 40% 매도 ($5,000)
   - TSLA 50% 매도 ($2,000)

2. 매수 (총 $10,000):
   - 가치주: BAC $2,000, INTC $1,500
   - 성장주: NVDA $2,000
   - 안정주: JNJ $1,500, PG $1,000
   - 채권: AGG $1,500
   - 금: GLD $500

3. 목표 배분:
   - Technology: 70% → 40%
   - Healthcare: 0% → 15%
   - Finance: 0% → 10%
   - Consumer: 0% → 10%
   - 채권: 0% → 15%
   - 금: 0% → 10%

예상 효과:
- 리스크 감소: -25%
- 예상 수익률: 9% → 10.5%
- 샤프 비율: 0.6 → 0.85
```

**예상 시간**: 25시간 ⭐⭐⭐⭐⭐

---

## 📅 구현 우선순위 (장기 가치투자자용)

### 🥇 1단계: 펀더멘털 기초 (Phase 2) - 3주
1. **UsStockInfo MCP 통합** (6시간) ⭐⭐⭐⭐⭐
2. **밸류에이션 스크리너** (8시간) ⭐⭐⭐⭐⭐
3. **교육 콘텐츠** (6시간) ⭐⭐⭐⭐
4. **HTML 밸류에이션 섹션** (4시간) ⭐⭐⭐⭐

**총 24시간 (3주)**

---

### 🏆 2단계: 투자 대가 전략 (Phase 2.5) - 6-8주 ⭐⭐⭐⭐⭐
5. **안전마진 계산기** (그레이엄/버핏, 8시간) ⭐⭐⭐⭐⭐
6. **PEG + 린치 6가지 분류** (10시간) ⭐⭐⭐⭐⭐
7. **기업 심층 분석 (Deep Dive)** (16시간) ⭐⭐⭐⭐⭐
8. **멍거 역행 체크리스트** (8시간) ⭐⭐⭐⭐
9. **멀티팩터 스코어링** (애스니스, 12시간) ⭐⭐⭐⭐⭐
10. **경제 사이클 판별** (달리오, 10시간) ⭐⭐⭐⭐

**총 64시간 (8주)**

이 단계가 가장 중요! 투자 대가들의 검증된 전략을 자동화하여
투자 결정의 품질을 크게 향상시킵니다.

---

### 🥈 3단계: 시각화 & 타이밍 (Phase 3) - 2-3주
11. **섹터 히트맵 확장** (6시간) ⭐⭐⭐
12. **RSI 차트** (6시간) ⭐⭐⭐
13. **실적 캘린더** (4시간) ⭐⭐⭐

**총 16시간 (2주)**

---

### 🥉 4단계: 고급 분석 도구 (Phase 4) - 6-8주
14. **피셔 15가지 질문 인터뷰** (20시간) ⭐⭐⭐
15. **백테스팅 시스템** (30시간) ⭐⭐⭐⭐

**총 50시간 (6-7주)**

---

### 💎 5단계: 포트폴리오 관리 (Phase 5) - 3-4주
16. **Watchlist 시스템** (8시간) ⭐⭐
17. **포트폴리오 추적** (10시간) ⭐⭐
18. **리밸런싱 권장** (6시간) ⭐

**총 24시간 (3주)**

---

### 🤖 6단계: AI 포트폴리오 코치 (Phase 6) - 3-4주
19. **AI 포트폴리오 진단 및 조언** (25시간) ⭐⭐⭐⭐⭐

**총 25시간 (3-4주)**

---

## 🎯 전체 개발 타임라인

| Phase | 기능 | 시간 | 우선순위 | 임팩트 |
|-------|------|------|----------|--------|
| **Phase 1** | ✅ MVP 완료 | - | - | ⭐⭐⭐⭐ |
| **Phase 2** | 펀더멘털 기초 | 24h | 매우 높음 | ⭐⭐⭐⭐⭐ |
| **Phase 2.5** | 투자 대가 전략 | 64h | **최우선** | ⭐⭐⭐⭐⭐ |
| **Phase 3** | 시각화 & 타이밍 | 16h | 중간 | ⭐⭐⭐ |
| **Phase 4** | 고급 분석 | 50h | 중간 | ⭐⭐⭐⭐ |
| **Phase 5** | 포트폴리오 관리 | 24h | 낮음 | ⭐⭐ |
| **Phase 6** | AI 코치 | 25h | 낮음 | ⭐⭐⭐⭐⭐ |

**총 개발 시간**: 약 203시간 (25-30주)

---

## 🎯 6개월 마일스톤

### Month 1 (✅ 완료)
- ✅ Phase 1 MVP 완료

### Month 2-3 (진행 중 - Phase 2 기초)
- [ ] UsStockInfo MCP 통합
- [ ] 밸류에이션 스크리너
- [ ] 교육 콘텐츠 작성
- [ ] 섹터 히트맵

### Month 3-5 (Phase 2.5 - 투자 대가 전략) 🔥
- [ ] 안전마진 계산기 (그레이엄/버핏)
- [ ] PEG + 린치 6가지 분류
- [ ] **기업 심층 분석 (Deep Dive)** ⭐
- [ ] 멍거 역행 체크리스트
- [ ] 멀티팩터 스코어링
- [ ] 경제 사이클 판별

### Month 5-6 (Phase 3 - 타이밍)
- [ ] RSI 차트
- [ ] 실적 캘린더
- [ ] Watchlist 시스템

### Month 7-9 (Phase 4 - 고급)
- [ ] 피셔 인터뷰 모드
- [ ] 백테스팅 시스템

### Month 10-12 (Phase 5-6 - 포트폴리오 & AI)
- [ ] 포트폴리오 추적
- [ ] 리밸런싱
- [ ] AI 포트폴리오 코치

---

## 💡 장기 가치투자자 사용 시나리오

### 주간 루틴 (일요일 저녁)
```bash
# 1. 시장 개요 확인
claude-code --skill market-pulse

# 2. 경제 사이클 확인 (Phase 2.5 - 달리오)
# → 현재 경제 상태: 성장+저인플레 vs 침체+고인플레
# → 추천 자산 배분 확인 (주식/채권/금/원자재)

# 3. 저평가 종목 스크리닝 (Phase 2)
# → 안전마진 Top 10 (그레이엄)
# → Ten Bagger 후보 (린치, PEG < 1.5)
# → 멀티팩터 상위 5% (애스니스)

# 4. 리스크 체크 (Phase 2.5 - 멍거)
# → 피해야 할 종목 확인
# → 리스크 점수 3점 이상 제외

# 5. 섹터 트렌드 분석
# → 히트맵으로 강세/약세 섹터 파악
# → 로테이션 기회 발견

# 6. RSI 확인 (Phase 3)
# → 과매도 구간(RSI < 30) 종목 주목
# → 분할 매수 계획
```

### 특정 종목 심층 분석 (관심 종목 발견 시)
```bash
# 기업 심층 분석 (Phase 2.5)
claude-code --skill market-pulse deep-dive AAPL

# 결과:
# - 종합 투자 점수 (0-100)
# - 8가지 투자 대가 관점 분석
#   1. 밸류에이션 (그레이엄/버핏)
#   2. 성장성 (린치)
#   3. 품질 (버핏/멍거)
#   4. 리스크 (멍거)
#   5. 팩터 점수 (애스니스)
#   6. 경제적 해자 (버핏)
#   7. 기술적 분석
#   8. 투자 의견 종합
# - 목표가 및 매수/매도 추천
# - 각 대가의 조언

# 예: "버핏: '최고 품질이나 가격이 비쌈. $165 이하 강력 매수'"
#     "린치: 'PEG 3.6은 부담. 30% 수익 후 일부 매도 고려'"
```

### 월간 루틴 (매월 초)
```bash
# 1. 포트폴리오 코칭 (Phase 6 - AI)
claude-code --skill market-pulse coach --portfolio my_portfolio.json

# → 워렌 버핏의 조언
# → 피터 린치의 조언
# → 레이 달리오의 조언
# → 종합 개선 계획 (매도/매수/리밸런싱)

# 2. 실적 발표 확인
# → 이번 달 실적 발표 일정
# → 서프라이즈/실망 종목 분석

# 3. 백테스팅 (Phase 4)
claude-code --skill market-pulse backtest --strategy graham --period 2014-2024

# → 내 전략이 과거에 얼마나 수익을 냈을까?
# → 최대 낙폭, 샤프 비율 확인
```

### 실전 투자 워크플로우 (예시)

**시나리오**: 새로운 종목 발굴 및 매수 결정

```bash
# Step 1: 저평가 종목 스크리닝
market-pulse
→ "안전마진 Top 10"에서 INTC 발견 (안전마진 31%)

# Step 2: 심층 분석
market-pulse deep-dive INTC

결과:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Intel Corp. (INTC) 심층 분석
종합 점수: 72/100 (매수 추천)

밸류에이션: ⭐⭐⭐⭐⭐
- 내재가치: $65
- 현재가: $45
- 안전마진: 31% ✅

성장성: ⭐⭐
- 분류: Turnaround (회생주)
- 성장률: -2% (부진)

품질: ⭐⭐⭐
- ROE: 8% (낮음)
- 부채비율: 45% (양호)

리스크: ⭐⭐⭐⭐
- 리스크 점수: 2/6 (낮음)
- AMD/NVDA 경쟁 압력

팩터: ⭐⭐⭐⭐
- Value: 9/10 (매우 저평가)
- Quality: 5/10 (보통)

버핏: "반도체는 어렵지만 가격이 매우 싸다.
      소액만 투자하고 지켜보라."

린치: "Turnaround 종목. 고위험이나 회복 시
      큰 수익 가능. 포트폴리오 5% 이하로."

멍거: "경쟁이 치열한 산업. 해자가 약함.
      조심스럽게 접근."

종합: 매수 (단, 포트폴리오의 5% 이하)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Step 3: 매수 타이밍 확인
→ RSI 차트 확인
→ RSI 35 (중립~과매도 경계) → 매수 가능

# Step 4: Watchlist 추가
→ 목표가: $60 (+33%)
→ 손절가: $40 (-11%)

# Step 5: 매수 실행
→ 포트폴리오의 5% ($2,500) 분할 매수
→ 3회 나눠서: $45, $42, $40
```

---

## 📚 학습 경로 (투자 초보 → 가치투자자)

### Week 1-2: 기초 개념
- [x] 시장 지수 이해 (S&P 500, NASDAQ)
- [x] 섹터 구분 (11개 섹터)
- [ ] PER, PBR 개념 (교육 콘텐츠)

### Week 3-4: 밸류에이션
- [ ] 저평가 종목 찾기 (스크리너)
- [ ] 동종 업계 비교
- [ ] ROE, 부채비율 분석

### Week 5-8: 타이밍
- [ ] RSI로 매수 타이밍 포착
- [ ] 섹터 로테이션 이해
- [ ] 실적 발표 활용

### Month 3+: 포트폴리오
- [ ] 분산투자 원칙
- [ ] 리밸런싱 전략
- [ ] 장기 수익률 추적

---

## 🔗 참고 자료

### 무료 데이터 소스
- **yfinance**: 가격, 재무제표, 애널리스트 의견
- **UsStockInfo MCP**: 펀더멘털 지표, 목표가
- **pykrx**: 한국 시장 데이터

### 추천 도서
- "현명한 투자자" (벤저민 그레이엄)
- "워렌 버핏의 주주 서한"
- "피터 린치의 이기는 투자"

---

**마지막 업데이트**: 2026-02-12
**작성자**: Market-Pulse AI

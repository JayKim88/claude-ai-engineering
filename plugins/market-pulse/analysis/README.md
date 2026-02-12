# Market-Pulse Phase 2.5: 가치투자 분석 도구

**Version**: 2.0.0
**Release Date**: 2026-02-12

Market-Pulse Phase 2.5는 8가지 투자 대가들의 전략을 통합한 가치투자 분석 플랫폼입니다.

---

## 📌 개요

Phase 2.5는 다음 투자 대가들의 철학을 구현합니다:

1. **벤저민 그레이엄** (Benjamin Graham) - 안전마진, 내재가치
2. **워렌 버핏** (Warren Buffett) - 경제적 해자, 경쟁우위
3. **피터 린치** (Peter Lynch) - GARP, 6가지 주식 분류
4. **찰리 멍거** (Charlie Munger) - 역행 사고, 리스크 분석
5. **클리프 애스니스** (Cliff Asness) - 팩터 투자 (Value, Quality, Momentum)
6. **레이 달리오** (Ray Dalio) - 경제 사이클 분석
7. **필립 피셔** (Philip Fisher) - 스캐터버트 (정성적 분석)
8. **통합 분석** - 멀티 퍼스펙티브 종합 평가

---

## 🚀 핵심 기능

### 1. 안전마진 계산기 (Graham/Buffett)

**그레이엄 공식**: `내재가치 = EPS × (8.5 + 2g)`

```bash
python3 intrinsic_value.py
```

**출력**:
- 내재가치 vs 현재가
- 안전마진 (%)
- 투자 추천 (강력 매수 / 매수 / 보유 / 매도)
- PER, PBR, ROE, 성장률 분석

**예시**:
```
MSFT: 안전마진 80.2% → 강력 매수 (내재가치 $2,045 vs 현재가 $404)
NVDA: 안전마진 66.9% → 강력 매수 (내재가치 $575 vs 현재가 $190)
GOOGL: 안전마진 59.4% → 강력 매수 (내재가치 $765 vs 현재가 $311)
```

**안전마진 기준** (Graham):
- 50%+ → 강력 매수 (충분한 안전마진)
- 30-50% → 매수 (적절한 안전마진)
- 10-30% → 보유 (제한적 안전마진)
- -10-10% → 보유 (안전마진 부족)
- -10% 이하 → 매도 (과대평가)

---

### 2. PEG 스크리너 + 린치 6가지 분류

**GARP 전략**: Growth At Reasonable Price (성장을 합리적 가격에)

```bash
python3 lynch_screener.py
```

**린치의 6가지 주식 분류**:
1. **저성장주** (Slow Growers) - 성장률 < 5%, 높은 배당
2. **우량주** (Stalwarts) - 성장률 5-12%, 안정적
3. **고성장주** (Fast Growers) - 성장률 15%+, 중소형주
4. **경기순환주** (Cyclicals) - 경기 의존적
5. **회생주** (Turnarounds) - 적자 → 흑자 전환
6. **자산주** (Asset Plays) - 보유 자산 > 시가총액

**PEG 비율 평가**:
- PEG < 0.5 → 탁월 (초저평가)
- PEG < 1.0 → 좋음 (저평가, GARP 적합)
- PEG = 1.0 → 보통 (적정 가격)
- PEG > 1.5 → 비싸다 (고평가)
- PEG > 2.0 → 과대평가 (피하라)

**예시**:
```
ORCL: PEG 0.22 (탁월!) - 고성장주, 90.9% 성장률 → 강력 매수
MSFT: PEG 0.36 (탁월!) - 고성장주, 59.8% 성장률 → 강력 매수
NVDA: PEG 0.37 (탁월!) - 고성장주, 66.7% 성장률 → 강력 매수
```

---

### 3. 기업 심층 분석 (Company Deep Dive)

**8가지 투자 대가 관점 통합 분석**

```bash
python3 company_deep_dive.py
```

**분석 결과 (AAPL 예시)**:

#### 1️⃣ 벤저민 그레이엄 - 안전마진
- 현재가: $275.50
- 내재가치: $356.74
- 안전마진: 22.8%
- 추천: 보유

#### 2️⃣ 워렌 버핏 - 경제적 해자
- 해자 강도: 넓은 해자 (100/100)
- 경쟁 우위:
  - ✅ 뛰어난 자본 수익률 (ROE 20%+)
  - ✅ 강력한 가격 결정력 (순이익률 20%+)
  - ✅ 강력한 브랜드 섹터
  - ✅ 네트워크 효과 잠재력
  - ✅ 높은 전환 비용
  - ✅ 대규모 경제력

#### 3️⃣ 피터 린치 - GARP
- 카테고리: 고성장주
- PEG: 1.62 (비싸다)
- 성장률: 18.3%
- ROE: 152.0%
- 추천: 보유

#### 4️⃣ 찰리 멍거 - 역행 사고
- 리스크 점수: 15/100 (낮음)
- 생존 가능성: 85/100 (높음)
- 실패 시나리오:
  - ⚠️ 높은 부채 (부채비율 100+)

#### 5️⃣ 클리프 애스니스 - 팩터
- Value: 약함
- Quality: 약함
- Momentum: 보통
- Low Volatility: 약함
- 종합 팩터 점수: 27.5/100

#### 6️⃣ 레이 달리오 - 경제 사이클
- 현재 사이클: 중기 확장
- 경기 민감도: 60/100
- 포지셔닝: 공격적 - 경기 순환주 (타이밍 중요)

#### 7️⃣ 필립 피셔 - 스캐터버트
- 혁신 잠재력: 70/100
- 경영진 청렴성: 90/100
- 직원 만족도: 70/100
- 고객 충성도: 70/100
- 종합 질적 점수: 75.0/100

#### 🎯 종합 결론
- **종합 점수**: 69.3/100
- **리스크-보상 비율**: 1.52
- **최종 추천**: ⚠️ 조건부 매수
- **투자 기간**: 중기 (1-3년)
- **신뢰도**: 100%

---

### 4. 통합 가치투자 분석기

**All-in-One CLI 도구**

```bash
python3 value_investing_analyzer.py \
  --tickers "AAPL,MSFT,GOOGL,NVDA,META" \
  --analysis all \
  --output /tmp/value-analysis.json
```

**분석 유형**:
- `safety_margin` - 안전마진 분석만
- `garp` - GARP 스크리닝만
- `deep` - 심층 분석 (8가지 관점)
- `all` - 모든 분석 (기본값)

**출력**:
1. 안전마진 Top 10 (테이블)
2. GARP 종목 (PEG < 1.0)
3. JSON 내보내기 (선택)

---

### 5. 투자회사 스타일 리포트 생성 ⭐ NEW

**키움증권/미래에셋 스타일 마크다운 리포트**

```bash
python3 ../reports/equity_report_generator.py --ticker AAPL --format markdown --output /tmp/AAPL_Report.md
```

**출력 포맷**:
- **마크다운** (`.md` 파일) - GitHub, Notion 등에 바로 복사 가능
- **터미널** - 콘솔 출력용 간략 버전

**리포트 구조** (투자회사 리포트 형식):

```markdown
# Apple Inc. (AAPL)
## 기업 분석 리포트

## 📊 투자 의견
| 투자 등급 | ⚠️ 조건부 매수 |
| 현재가    | $275.50      |
| 내재가치  | $356.74      |
| 상승여력  | +29.5%       |

## 💡 핵심 요약 (Investment Thesis)
5년 평균 18.3%의 높은 성장률...

## 📈 재무 하이라이트
| PER | ROE | 성장률 |

## 💰 밸류에이션 분석
- 그레이엄 안전마진
- 린치 GARP 분석

## 🏰 경쟁 우위 (Economic Moat)
- 해자 강도: 넓은 해자 (100/100)
- 경쟁 우위 요소 (6가지)

## ✨ 투자 포인트
1. 높은 자본 수익률
2. 강력한 경제적 해자

## ⚠️ 리스크 요인
- 리스크 점수: 15/100
- 실패 시나리오

## 📊 팩터 분석 (Asness)
| Value | Quality | Momentum | Low Volatility |

## 🌐 경제 사이클 분석 (Dalio)
## 🔍 정성적 평가 (Fisher)

## 🎯 종합 평가
- 종합 점수: 69.3/100
- 최종 추천: ⚠️ 조건부 매수
- 투자 기간: 중기 (1-3년)
```

**특징**:
- ✅ **투자회사 스타일** - 키움증권/미래에셋 리포트 구조
- ✅ **8가지 투자 대가 관점** - 그레이엄, 버핏, 린치, 멍거, 애스니스, 달리오, 피셔, 종합
- ✅ **핵심 요약 (Investment Thesis)** - 1-2문장 투자 논지
- ✅ **투자 포인트 & 리스크** - 장단점 명확 구분
- ✅ **재무 하이라이트** - PER, ROE, 성장률 등
- ✅ **마크다운 형식** - PDF 불필요, 바로 공유 가능

**터미널 출력용** (간단 버전):

```bash
python3 ../reports/equity_report_generator.py --ticker AAPL --format terminal
```

**출력**:
```
====================================================================================================
  Apple Inc. (AAPL) - 투자 분석 리포트
====================================================================================================
📊 투자 의견
  등급: ⚪ ⚠️ 조건부 매수
  현재가: $275.50, 내재가치: $356.74, 상승여력: +29.5%

💡 핵심 요약
  5년 평균 18.3%의 높은 성장률... 넓은 해자 보유...

✨ 투자 포인트
  1. 높은 자본 수익률: ROE 152.0%
  2. 강력한 경제적 해자: 넓은 해자 (100/100)

⚠️  리스크 요인
  • 높은 부채 (부채비율 100+)

🎯 종합 평가
  종합 점수: 69.3/100, 최종 추천: ⚠️ 조건부 매수
====================================================================================================
```

---

## 📊 사용 예시

### 예시 1: 안전마진 분석

```bash
python3 value_investing_analyzer.py \
  --tickers "AAPL,MSFT,GOOGL,NVDA,META,TSLA,AMZN" \
  --analysis safety_margin
```

**출력**:
```
✅ 안전마진 분석: 4개 저평가 종목 발견

종목     회사명                 현재가       내재가치       안전마진   추천
================================================================================
MSFT     Microsoft Corp     $   404.37 $  2045.76      80.2%  강력 매수
NVDA     NVIDIA Corp        $   190.05 $   574.70      66.9%  강력 매수
GOOGL    Alphabet Inc.      $   310.96 $   764.97      59.4%  강력 매수
AAPL     Apple Inc.         $   275.50 $   356.74      22.8%  보유
================================================================================
```

---

### 예시 2: GARP 스크리닝

```bash
python3 value_investing_analyzer.py \
  --tickers "AAPL,MSFT,GOOGL,NVDA,META,AMZN,TSLA,CRM,ORCL" \
  --analysis garp
```

**출력**:
```
✅ GARP 스크리닝: 5개 GARP 종목 발견

종목     카테고리      PEG     성장률    ROE      추천
===========================================================
ORCL     고성장주      0.22    90.9%     69.0%    강력 매수
MSFT     고성장주      0.36    59.8%     34.4%    강력 매수
CRM      고성장주      0.37    38.6%     12.2%    강력 매수
NVDA     고성장주      0.37    66.7%    107.4%    강력 매수
GOOGL    고성장주      0.75    31.1%     35.7%    강력 매수
===========================================================
```

---

### 예시 3: 기업 심층 분석

```bash
python3 company_deep_dive.py
```

터미널에서 티커 입력: `AAPL`

**출력**: 8가지 관점 종합 리포트 (위 Deep Dive 섹션 참조)

---

### 예시 4: JSON 내보내기

```bash
python3 value_investing_analyzer.py \
  --tickers "AAPL,MSFT,GOOGL" \
  --analysis all \
  --output /tmp/my-portfolio-analysis.json
```

**JSON 구조**:
```json
{
  "timestamp": "2026-02-12",
  "analysis_type": "all",
  "tickers": ["AAPL", "MSFT", "GOOGL"],
  "safety_margin": [
    {
      "ticker": "MSFT",
      "company_name": "Microsoft Corporation",
      "current_price": 404.37,
      "intrinsic_value": 2045.76,
      "safety_margin": 80.2,
      "recommendation": "강력 매수",
      "per": 21.45,
      "roe": 34.4,
      "growth_rate": 59.8
    }
  ],
  "garp": [ ... ],
  "deep_dive": [ ... ]
}
```

---

## 🎯 투자 대가 전략 요약

| 대가 | 핵심 지표 | 목표 | 구현 |
|------|----------|------|------|
| **그레이엄** | 안전마진 (IV - Price) | 저평가 종목 | `intrinsic_value.py` |
| **버핏** | 경제적 해자 (ROE, 마진) | 경쟁우위 | `company_deep_dive.py` |
| **린치** | PEG 비율 (PER/성장률) | GARP | `lynch_screener.py` |
| **멍거** | 실패 시나리오 | 리스크 최소화 | `company_deep_dive.py` |
| **애스니스** | 팩터 점수 (V, Q, M) | 다각도 평가 | `company_deep_dive.py` |
| **달리오** | 경제 사이클 | 타이밍 | `company_deep_dive.py` |
| **피셔** | 정성적 분석 | 경영 품질 | `company_deep_dive.py` |

---

## 🔧 설치 및 의존성

### 필수 패키지

```bash
pip install yfinance pyyaml
```

### 프로젝트 구조

```
plugins/market-pulse/
├── mcp/
│   ├── stock_mcp_server.py    # MCP 서버 (yfinance 래퍼)
│   ├── stock_client.py         # MCP 클라이언트
│   └── test_mcp_server.py      # 테스트
├── analysis/
│   ├── intrinsic_value.py      # 안전마진 계산기
│   ├── lynch_screener.py       # PEG 스크리너
│   ├── company_deep_dive.py    # 8가지 관점 심층 분석
│   ├── value_investing_analyzer.py  # 통합 CLI 도구
│   └── README.md               # 본 문서
├── reports/ ⭐ NEW
│   └── equity_report_generator.py  # 투자회사 스타일 리포트 생성
└── config/
    ├── fetch_market.py         # 시장 데이터 수집
    └── generate_html.py        # HTML 대시보드 생성
```

---

## ⚠️ 제한 사항

1. **데이터 소스**: yfinance (무료, 15-20분 지연)
2. **PEG 비율**: yfinance에서 제공하지 않는 경우 많음 (직접 계산)
3. **경제 사이클**: 간단화 버전 (실제로는 GDP, 금리 등 필요)
4. **스캐터버트**: 정성적 분석 간단화 (실제로는 인터뷰 필요)
5. **DCF 모델**: 기본 구현 (더 정교한 모델 가능)

---

## 🔮 향후 개선

- [ ] PEG 비율 자동 계산 강화
- [ ] 실시간 경제 사이클 판별 (GDP, 금리 데이터 통합)
- [ ] DCF 모델 고도화 (WACC, 터미널 가치 정밀화)
- [ ] 백테스팅 엔진 (전략 성과 검증)
- [ ] 알림 시스템 (안전마진 기준 충족 시 알림)
- [ ] HTML 대시보드 통합 (Phase 2.5 결과 시각화)

---

## 📖 참고 자료

- **벤저민 그레이엄**: "The Intelligent Investor" (1949)
- **워렌 버핏**: Berkshire Hathaway Annual Letters
- **피터 린치**: "One Up On Wall Street" (1989)
- **찰리 멍거**: "Poor Charlie's Almanack" (2005)
- **클리프 애스니스**: AQR Capital Management Research Papers
- **레이 달리오**: "Principles" (2017), "Economic Machine"
- **필립 피셔**: "Common Stocks and Uncommon Profits" (1958)

---

## 📝 라이선스

MIT License

---

**작성일**: 2026-02-12
**버전**: 2.0.0 (Phase 2.5)
**작성자**: Market-Pulse Team

**문의**: Market-Pulse는 교육 목적의 오픈소스 프로젝트입니다. 실제 투자 결정에 사용 시 주의하시기 바랍니다.

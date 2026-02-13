# factor-lab 설치 및 사용 가이드

## 📦 설치 (최초 1회)

```bash
# 1. factor-lab 디렉토리로 이동
cd /path/to/claude-ai-engineering/plugins/factor-lab

# 2. 필수 패키지 설치
pip3 install -r requirements.txt

# 설치되는 패키지:
# - numpy>=1.24        # 수치 계산
# - pandas>=2.0        # 데이터 처리
# - scipy>=1.10        # 통계 계산
# - yfinance>=0.2.28   # 미국 주식 데이터
# - pykrx>=1.0.45      # 한국 주식 데이터
# - PyYAML>=6.0        # 설정 파일 읽기
# - matplotlib>=3.7    # 차트 생성
```

---

## 🗄️ Cache 설정 (필수! - 최초 1회, ~12분)

**중요**: 백테스트를 하려면 먼저 historical data를 캐싱해야 합니다.

```bash
# S&P 500 전체 (503개 종목, 10년 데이터)
python3 scripts/populate_cache.py --universe SP500 --years 10

# 진행 상황:
# ================================================================================
# CACHE PRE-POPULATION
# ================================================================================
# Universe: SP500
# Years: 10
# Delay: 1.5s per stock
#
# ✓ Found 503 tickers
# Date range: 2016-02-16 to 2026-02-13
# Estimated time: 12.6 minutes
#
# [1/503] (0.2%) Fetching AAPL... ✓ 2514 days
# [2/503] (0.4%) Fetching MSFT... ✓ 2514 days
# ...
# [503/503] (100.0%) Fetching ZTS... ✓ 2514 days
#
# ✅ CACHE PRE-POPULATION COMPLETE
# Successful: 503/503 (100.0%)
```

**테스트용 (10개 종목, ~15초):**
```bash
python3 scripts/populate_cache.py --universe SP500 --years 10 --limit 10
```

**Cache 위치:**
- `data/market_data_cache.db` (~200MB)
- 한 번 캐싱하면 재사용 가능 (1년간 유효)

---

## 📊 사용법 1: Factor Screening (종목 스크리닝)

### 기본 사용

```bash
# Value + Quality 중심 스크리닝 (Top 50)
python3 quant/factor_screener.py \
  --universe SP500 \
  --factors value:0.4,quality:0.4,momentum:0.2 \
  --top-n 50 \
  --output screening_results.csv

# 결과:
# Ticker  Composite  Value  Quality  Momentum  Sector       Price
# NVDA    84.1       75     95       82        Technology   $884.50
# MSFT    82.3       70     93       84        Technology   $404.37
# AAPL    78.5       68     88       79        Technology   $185.92
# ...
```

### 다양한 스크리닝 전략

```bash
# 1. Quality 중심 (안정적 우량주)
python3 quant/factor_screener.py \
  --universe SP500 \
  --factors quality:1.0 \
  --top-n 30

# 2. Momentum 중심 (상승 추세주)
python3 quant/factor_screener.py \
  --universe SP500 \
  --factors momentum:1.0 \
  --top-n 20

# 3. Value 중심 (저평가 가치주)
python3 quant/factor_screener.py \
  --universe SP500 \
  --factors value:1.0 \
  --top-n 40

# 4. Balanced (균형 전략)
python3 quant/factor_screener.py \
  --universe SP500 \
  --factors value:0.3,quality:0.4,momentum:0.3 \
  --min-score 70 \
  --top-n 50

# 5. 한국 주식 스크리닝 (KOSPI 200)
python3 quant/factor_screener.py \
  --universe KOSPI200 \
  --factors value:0.3,quality:0.5,momentum:0.2 \
  --top-n 30
```

---

## 🔄 사용법 2: Backtesting (전략 검증)

### 기본 백테스트

```bash
# Momentum 전략 (2020-2024, 4년)
python3 quant/backtest_engine.py \
  --strategy momentum \
  --universe SP500 \
  --start-date 2020-01-01 \
  --end-date 2024-01-01 \
  --rebalance monthly \
  --top-n 50 \
  --output results_momentum

# 결과:
# ============================================================
# BACKTEST RESULTS
# ============================================================
# Total Return:    +86.81%
# Annual Return:   +16.91%
# Sharpe Ratio:     3.54
# Max Drawdown:    -25.20%
# Number of Trades: 4840
#
# ✓ Results saved to results_momentum/
#   - equity_curve.csv
#   - trades.csv
#   - equity_curve.png
```

### 다양한 백테스트 전략

```bash
# 1. Value 전략
python3 quant/backtest_engine.py \
  --strategy value \
  --universe SP500 \
  --start-date 2020-01-01 \
  --end-date 2024-01-01 \
  --rebalance monthly \
  --top-n 50

# 2. Quality 전략
python3 quant/backtest_engine.py \
  --strategy quality \
  --universe SP500 \
  --start-date 2020-01-01 \
  --end-date 2024-01-01 \
  --rebalance monthly \
  --top-n 50

# 3. 분기별 리밸런싱 (거래 비용 절감)
python3 quant/backtest_engine.py \
  --strategy momentum \
  --universe SP500 \
  --start-date 2020-01-01 \
  --end-date 2024-01-01 \
  --rebalance quarterly \
  --top-n 30

# 4. 작은 포트폴리오 (집중 투자)
python3 quant/backtest_engine.py \
  --strategy momentum \
  --universe SP500 \
  --start-date 2020-01-01 \
  --end-date 2024-01-01 \
  --rebalance monthly \
  --top-n 20

# 5. 한국 주식 백테스트
python3 quant/backtest_engine.py \
  --strategy momentum \
  --universe KOSPI200 \
  --start-date 2020-01-01 \
  --end-date 2024-01-01 \
  --rebalance monthly \
  --top-n 30
```

---

## 🎯 실전 워크플로우

### 시나리오 1: 매월 포트폴리오 리밸런싱

```bash
# 1. 최신 종목 스크리닝 (매월 1일 실행)
python3 quant/factor_screener.py \
  --universe SP500 \
  --factors value:0.3,quality:0.4,momentum:0.3 \
  --top-n 50 \
  --output monthly_screening_$(date +%Y%m).csv

# 2. 결과 확인
cat monthly_screening_202602.csv

# 3. 상위 30개 종목 선택하여 포트폴리오 구성
# (Excel이나 Google Sheets에서 추가 분석 가능)
```

### 시나리오 2: 새로운 전략 개발 및 검증

```bash
# 1. Cache 준비 (최초 1회)
python3 scripts/populate_cache.py --universe SP500 --years 10

# 2. 여러 전략 백테스트
python3 quant/backtest_engine.py --strategy momentum --universe SP500 \
  --start-date 2020-01-01 --end-date 2024-01-01 --rebalance monthly --top-n 50 \
  --output results_momentum

python3 quant/backtest_engine.py --strategy value --universe SP500 \
  --start-date 2020-01-01 --end-date 2024-01-01 --rebalance monthly --top-n 50 \
  --output results_value

python3 quant/backtest_engine.py --strategy quality --universe SP500 \
  --start-date 2020-01-01 --end-date 2024-01-01 --rebalance monthly --top-n 50 \
  --output results_quality

# 3. 결과 비교
open results_momentum/equity_curve.png
open results_value/equity_curve.png
open results_quality/equity_curve.png

# 4. 가장 좋은 전략으로 실제 스크리닝
python3 quant/factor_screener.py \
  --universe SP500 \
  --factors momentum:1.0 \
  --top-n 50 \
  --output final_portfolio.csv
```

---

## ⚙️ 고급 옵션

### Cache 관리

```bash
# Cache 다시 생성 (1년에 1번 권장)
python3 scripts/populate_cache.py --universe SP500 --years 10

# NASDAQ 100도 캐싱
python3 scripts/populate_cache.py --universe NASDAQ100 --years 10

# 한국 주식 캐싱
python3 scripts/populate_cache.py --universe KOSPI200 --years 10
python3 scripts/populate_cache.py --universe KOSDAQ150 --years 10
```

### 커스텀 설정

```bash
# 거래 비용 조정
python3 quant/backtest_engine.py \
  --strategy momentum \
  --universe SP500 \
  --start-date 2020-01-01 \
  --end-date 2024-01-01 \
  --rebalance monthly \
  --top-n 50 \
  --commission 0.001 \  # 0.1% 수수료
  --slippage 0.0005 \   # 0.05% 슬리피지
  --initial-cash 1000000  # 초기 자본 $1M
```

---

## 📁 결과 파일 이해하기

### Screening 결과 (CSV)

```csv
Ticker,Composite,Value,Quality,Momentum,Low_Vol,Size,Sector,Price
NVDA,84.1,75.0,95.0,82.0,60.0,20.0,Technology,884.50
MSFT,82.3,70.0,93.0,84.0,65.0,20.0,Technology,404.37
```

**활용법:**
- Excel/Sheets로 열어서 추가 분석
- Composite 70+ 종목에 집중
- 섹터 다양성 확인 (한 섹터에 몰리지 않도록)

### Backtest 결과

**1. equity_curve.csv** - 포트폴리오 가치 추이
```csv
Date,Portfolio_Value
2020-01-01,100000.00
2020-02-01,103245.67
2020-03-01,89123.45
...
```

**2. trades.csv** - 모든 거래 내역
```csv
Date,Ticker,Action,Shares,Price,Commission,Total
2020-01-01,AAPL,BUY,50,293.65,14.68,14697.18
2020-01-01,MSFT,BUY,40,157.70,6.31,6314.31
...
```

**3. equity_curve.png** - 시각화 차트
- 포트폴리오 성과 그래프
- 성과 지표 오버레이 (Sharpe, MDD 등)

---

## 💡 팁 & 주의사항

### ✅ DO (권장사항)

1. **Cache 먼저 준비**
   ```bash
   python3 scripts/populate_cache.py --universe SP500 --years 10
   ```

2. **작은 테스트부터 시작**
   ```bash
   # 10개 종목으로 먼저 테스트
   python3 scripts/populate_cache.py --universe SP500 --limit 10
   python3 quant/factor_screener.py --universe SP500 --top-n 10
   ```

3. **백테스트로 전략 검증**
   - 실제 투자 전에 반드시 백테스트
   - 최소 3-4년 이상 기간으로 검증

4. **분산 투자**
   - Top 30-50 종목 선택
   - 여러 섹터에 분산

5. **정기적 리밸런싱**
   - 매월 또는 분기별 스크리닝
   - 포트폴리오 업데이트

### ❌ DON'T (주의사항)

1. **Cache 없이 백테스트 실행 금지**
   - Rate limiting 에러 발생
   - 결과 invalid

2. **과거 성과 맹신 금지**
   - "과거 성과 ≠ 미래 수익"
   - 백테스트는 참고용

3. **한 번에 전액 투자 금지**
   - 분할 매수 (Dollar Cost Averaging)
   - 포트폴리오 점진적 구성

4. **감정적 판단 금지**
   - 퀀트는 데이터 기반
   - Factor 점수 70+ 종목에 집중

5. **Transaction Cost 무시 금지**
   - 매매 수수료 고려
   - 너무 잦은 리밸런싱 지양

---

## 🔧 문제 해결

### "No module named 'yfinance'"
```bash
pip3 install -r requirements.txt
```

### "Too Many Requests" 에러
```bash
# Cache 먼저 생성
python3 scripts/populate_cache.py --universe SP500 --years 10
```

### "No data available for AAPL"
```bash
# Cache 다시 생성
rm data/market_data_cache.db
python3 scripts/populate_cache.py --universe SP500 --years 10
```

### 백테스트 너무 느림
```bash
# Cache 확인
ls -lh data/market_data_cache.db

# Cache 없으면 생성
python3 scripts/populate_cache.py --universe SP500 --years 10
```

---

## 📚 학습 자료

**추천 순서:**
1. `README.md` - 전체 개요
2. `PROGRESS.md` - 개발 히스토리
3. `docs/QUANT_INVESTING_GUIDE.md` - 퀀트 투자 가이드 (60 pages)

**추천 도서:**
- "Quantitative Momentum" - Wesley Gray
- Fama-French 5-Factor Model (2015)
- "Value and Momentum Everywhere" - Asness et al.

---

## 🎓 다음 단계

1. ✅ Cache 생성 완료
2. ✅ Screening으로 종목 발굴
3. ✅ Backtesting으로 전략 검증
4. 📈 실전 투자 (소액부터 시작!)
5. 🔄 매월 리밸런싱

---

**Made with 📊 for quantitative investors**

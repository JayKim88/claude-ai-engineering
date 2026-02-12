# Market-Pulse Phase 1 구현 계획: 투자 학습 도구로의 전환

> **작성일**: 2026-02-11
> **버전**: 1.0.0 → 2.0.0 (Phase 1 완료 시)
> **목표**: 실전 투자 의사결정 지원 도구
> **타임라인**: 3-6주 (주 10-15시간 투자)

---

## 📌 Executive Summary

**현재 문제**: market-pulse v1.0은 우수한 시장 스캐너이지만, 실제 투자 학습 및 의사결정에는 부족함
- 5일 스냅샷만 제공 (트렌드 분석 불가)
- 기술적 지표 부재 (RSI, MACD, 이동평균 등)
- 투자 초보자를 위한 교육 콘텐츠 없음
- 제한적 시각화 (섹터 바차트 1개)

**Phase 1 목표**: "매일 사용하며 투자 능력을 키우는 학습 도구"
- 60일 히스토리 데이터 저장 → 트렌드 파악 훈련
- 기술적 지표 계산 → RSI, MACD, 이동평균 학습
- 교육 툴팁 → 개념 즉시 이해
- 향상된 시각화 → 섹터 히트맵, 트렌드 차트, RSI 차트

**전략적 가치**: "3배 레버리지"
1. **투자 능력 향상** (최우선) - Stage 1-3 학습 경로 지원
2. **포트폴리오 증명** - AI 에이전트 오케스트레이션 규모 프로젝트
3. **수익화 잠재력** - Phase 3-4 준비 (백테스팅, 시그널 알림)

---

## 🎯 프로젝트 목표

### 사용자 프로필
- **투자 경험**: 초보 단계 (Stage 1-2)
- **학습 목표**: 퀀트 투자 기초 → 전략 백테스팅 → 시그널 알림 (점진적 발전)
- **시간 투자**: 매일 아침 10분 대시보드 확인 + 주말 1-2시간 복기
- **최종 목표**: 연 15-20% 안정적 수익률 (Stage 5 도달, 1년 내)

### 일반적인 투자 학습 경로와 Phase 1의 역할

| 단계 | 학습 내용 | 기간 | Phase 1 지원 |
|------|----------|------|-------------|
| **Stage 1: 기초** | 용어, 시장 구조 | 1-2개월 | ✅ 뉴스 요약, 시장 상태 |
| **Stage 2: 차트 읽기** | 캔들스틱, 추세 | 2-3개월 | ✅ **60일 트렌드 차트** |
| **Stage 3: 기술 분석** | RSI, MACD, 이평선 | 3-4개월 | ✅ **기술 지표 + 교육 툴팁** |
| **Stage 4: 펀더멘털** | PER, PBR, 재무제표 | 4-6개월 | ⏳ Phase 2 |
| **Stage 5: 통합** | 리스크 관리 | 6-12개월 | ⏳ Phase 2 |
| **Stage 6: 퀀트** | 백테스팅, 시그널 | 1년+ | ⏳ Phase 3 |

**Phase 1 학습 시나리오**:
```
아침 루틴 (10분):
1. market-pulse 실행
2. 60일 트렌드 차트 확인
   - S&P 500: 50일선 위 → "상승 추세구나"
3. RSI 차트 확인
   - NVDA RSI 75 (툴팁: "과매수 - 단기 조정 가능성") → "지금은 매수 타이밍 아니네"
4. 섹터 히트맵 확인
   - Technology +3% (5일) → "기술주가 강하네"
5. Technical Analyzer 요약
   - "S&P 500: 보류 (과매수 부담) - 신뢰도 ⭐⭐⭐"

→ 3개월 후: RSI, 이동평균 패턴이 몸에 배임
```

---

## 📊 현재 상태 분석 (v1.0)

### 강점
- ✅ 멀티 에이전트 아키텍처 (4개: US, KR, Crypto-Macro, Synthesizer)
- ✅ 무료 데이터 소스 (yfinance, pykrx, feedparser)
- ✅ 아름다운 HTML 대시보드 (Financial Times 스타일)
- ✅ 한국 시장 외국인/기관 매매 분석 (독보적)

### 약점
- ❌ 5일 스냅샷만 제공 (히스토리 없음)
- ❌ 기술적 지표 부재 (RSI, MACD, 이동평균 등)
- ❌ 펀더멘털 분석 미흡 (PER/PBR만 제공)
- ❌ 교육 콘텐츠 없음 (초보자가 이해하기 어려움)
- ❌ 제한적 시각화 (섹터 바차트 1개)

### 현재 파일 구조
```
plugins/market-pulse/
├── .claude-plugin/
│   └── plugin.json
├── config/
│   ├── fetch_market.py      # 데이터 수집 (yfinance, pykrx)
│   ├── generate_html.py     # HTML 대시보드 생성
│   ├── sources.yaml         # 데이터 소스 설정
│   └── watchlist.yaml       # 개인 워치리스트
├── agents/
│   ├── us-market-analyzer.md
│   ├── kr-market-analyzer.md
│   ├── crypto-macro-analyzer.md
│   └── market-synthesizer.md
├── skills/
│   └── market-pulse/
│       └── SKILL.md
└── README.md
```

---

## 🚀 Phase 1 MVP 범위

### 핵심 기능 (4개)
1. **Historical Data Storage** - SQLite로 60일 히스토리 저장
2. **Technical Indicators** - RSI, MACD, 이동평균 계산 (pandas-ta)
3. **Enhanced Visualizations** - 60일 트렌드 차트, 섹터 히트맵, RSI 차트
4. **Educational Content** - 초보자용 지표 설명 툴팁

### 새로운 파일 구조 (Phase 1 후)
```
plugins/market-pulse/
├── data/                     # NEW
│   ├── market_history.db     # SQLite 데이터베이스
│   └── market_history.py     # MarketHistoryDB 클래스
├── analysis/                 # NEW
│   └── technical_indicators.py  # 기술 지표 계산 엔진
├── config/
│   ├── educational_content.yaml  # NEW - 교육 콘텐츠
│   ├── fetch_market.py      # MODIFIED - 60일 데이터 + DB 저장
│   └── generate_html.py     # MODIFIED - 3개 차트 추가
├── agents/
│   ├── technical-analyzer.md    # NEW - 기술 분석 에이전트
│   └── (기존 4개 유지)
├── skills/
│   └── market-pulse/
│       └── SKILL.md         # MODIFIED - Technical Analyzer 추가
└── docs/                     # NEW
    └── phase1-implementation-plan.md  # 이 문서
```

---

## 📝 구현 태스크 상세 (12개)

### Task 1: SQLite 데이터베이스 스키마 설계 및 구현
**예상 시간**: 5-8시간
**파일**: `plugins/market-pulse/data/market_history.py` (신규)

**스키마**:
```sql
-- 일별 OHLCV 데이터
CREATE TABLE daily_prices (
    symbol TEXT NOT NULL,           -- 티커 심볼 (예: ^GSPC, 005930)
    date TEXT NOT NULL,              -- 날짜 (YYYY-MM-DD)
    open REAL,                       -- 시가
    high REAL,                       -- 고가
    low REAL,                        -- 저가
    close REAL,                      -- 종가
    volume INTEGER,                  -- 거래량
    PRIMARY KEY (symbol, date)
);

-- 멀티기간 수익률 (계산값 캐싱)
CREATE TABLE multi_period_returns (
    symbol TEXT NOT NULL,
    date TEXT NOT NULL,
    return_1d REAL,                  -- 1일 수익률 (%)
    return_5d REAL,                  -- 5일 수익률 (%)
    return_20d REAL,                 -- 20일 수익률 (%)
    return_60d REAL,                 -- 60일 수익률 (%)
    PRIMARY KEY (symbol, date)
);

-- 섹터 성과 (히트맵용)
CREATE TABLE sector_performance (
    sector TEXT NOT NULL,            -- 섹터명 (예: Technology, Financials)
    date TEXT NOT NULL,
    return_1d REAL,
    return_5d REAL,
    return_20d REAL,
    PRIMARY KEY (sector, date)
);

-- 인덱스 생성 (조회 성능 최적화)
CREATE INDEX idx_daily_prices_symbol ON daily_prices(symbol);
CREATE INDEX idx_daily_prices_date ON daily_prices(date);
CREATE INDEX idx_sector_performance_date ON sector_performance(date);
```

**MarketHistoryDB 클래스 메서드**:
```python
class MarketHistoryDB:
    def __init__(self, db_path: str = "data/market_history.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def save_daily_prices(self, symbol: str, date: str, ohlcv: dict):
        """일별 가격 데이터 저장 (INSERT OR REPLACE)."""
        pass

    def get_historical_prices(self, symbol: str, days: int = 60) -> pd.DataFrame:
        """특정 심볼의 N일 히스토리 조회."""
        pass

    def calculate_multi_period_returns(self, symbol: str) -> dict:
        """1d, 5d, 20d, 60d 수익률 계산 및 저장."""
        pass

    def get_sector_performance_history(self, days: int = 60) -> pd.DataFrame:
        """섹터별 성과 히스토리 (히트맵용)."""
        pass

    def cleanup_old_data(self, keep_days: int = 365):
        """1년 이상 오래된 데이터 삭제 (용량 관리)."""
        pass
```

**검증 방법**:
```python
# 테스트 스크립트
db = MarketHistoryDB()
db.save_daily_prices("^GSPC", "2026-02-11", {
    "open": 5800, "high": 5850, "low": 5790, "close": 5840, "volume": 1000000
})
hist = db.get_historical_prices("^GSPC", days=60)
assert len(hist) == 60
```

---

### Task 2: fetch_market.py에 historical data 저장 로직 추가
**예상 시간**: 3-5시간
**파일**: `plugins/market-pulse/config/fetch_market.py` (수정)

**변경사항**:
```python
from ..data.market_history import MarketHistoryDB

class MarketDataFetcher:
    def __init__(self, ...):
        # 기존 코드...
        self.history_db = MarketHistoryDB()  # 추가

    def fetch_us_indices(self) -> Dict[str, Any]:
        """Fetch major US indices with 60-day history."""
        import yfinance as yf

        result = {}
        for symbol, name in self.config["us_indices"].items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="60d")  # 5d → 60d 변경

                # DB에 저장
                for date, row in hist.iterrows():
                    self.history_db.save_daily_prices(
                        symbol=symbol,
                        date=date.strftime("%Y-%m-%d"),
                        ohlcv={
                            "open": row["Open"],
                            "high": row["High"],
                            "low": row["Low"],
                            "close": row["Close"],
                            "volume": row["Volume"]
                        }
                    )

                # 최신 값 (기존 로직 유지)
                current = hist["Close"].iloc[-1]
                prev = hist["Close"].iloc[-2] if len(hist) >= 2 else current
                change = current - prev
                change_pct = (change / prev * 100) if prev else 0

                # 멀티기간 수익률 계산 (새로 추가)
                returns = self.history_db.calculate_multi_period_returns(symbol)

                result[symbol] = {
                    "name": name,
                    "value": round(current, 2),
                    "change": round(change, 2),
                    "change_pct": round(change_pct, 2),
                    "returns": returns,  # 추가
                    "history_60d": hist["Close"].tolist()  # 추가 (차트용)
                }
            except Exception as e:
                print(f"Error fetching {symbol}: {e}", file=sys.stderr)
                result[symbol] = {"name": name, "error": str(e)}

        return result

    def fetch_us_sectors(self) -> List[Dict[str, Any]]:
        """Fetch sector ETF performance with 60-day history."""
        # 동일한 방식으로 수정
        # period="1mo" → period="60d"
        # DB 저장 로직 추가
        pass

    def fetch_crypto(self) -> List[Dict[str, Any]]:
        """Fetch crypto prices with 60-day history."""
        # 동일한 방식으로 수정
        pass
```

**검증 방법**:
```bash
python3 plugins/market-pulse/config/fetch_market.py --scope us --output json | jq '.data.us_indices["^GSPC"].history_60d | length'
# 출력: 60 (60일 데이터 확인)
```

---

### Task 3: technical_indicators.py 생성 - pandas-ta 기반 지표 계산
**예상 시간**: 5-8시간
**파일**: `plugins/market-pulse/analysis/technical_indicators.py` (신규)

**TechnicalIndicatorCalculator 클래스**:
```python
import pandas as pd
import pandas_ta as ta
from typing import Dict, Any

class TechnicalIndicatorCalculator:
    """Calculate technical indicators using pandas-ta."""

    def calculate_all(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate all technical indicators for a given price dataframe.

        Args:
            df: DataFrame with columns [date, open, high, low, close, volume]

        Returns:
            Dict with all calculated indicators
        """
        if df.empty or len(df) < 60:
            return {"error": "Insufficient data (need 60+ days)"}

        # Ensure index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

        result = {}

        # Moving Averages
        result['sma'] = self.calculate_moving_averages(df)

        # Momentum Indicators
        result['rsi'] = self.calculate_rsi(df)
        result['macd'] = self.calculate_macd(df)

        # Volatility Indicators
        result['bollinger'] = self.calculate_bollinger_bands(df)
        result['atr'] = self.calculate_atr(df)

        # Volume Indicator
        result['obv'] = self.calculate_obv(df)

        # Interpretations (for educational purposes)
        result['interpretations'] = self.generate_interpretations(result)

        return result

    def calculate_moving_averages(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate SMA 5, 20, 50, 200 and EMA 12, 26."""
        close = df['close']
        return {
            'sma_5': close.rolling(window=5).mean().iloc[-1] if len(close) >= 5 else None,
            'sma_20': close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else None,
            'sma_50': close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else None,
            'sma_200': close.rolling(window=200).mean().iloc[-1] if len(df) >= 200 else None,
            'ema_12': close.ewm(span=12, adjust=False).mean().iloc[-1],
            'ema_26': close.ewm(span=26, adjust=False).mean().iloc[-1],
        }

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> Dict[str, Any]:
        """Calculate RSI and interpretation."""
        rsi_series = ta.rsi(df['close'], length=period)
        rsi_value = rsi_series.iloc[-1] if not rsi_series.empty else None

        return {
            'value': round(rsi_value, 2) if rsi_value else None,
            'series_60d': rsi_series.tail(60).tolist(),  # 차트용
            'interpretation': self.interpret_rsi(rsi_value) if rsi_value else None
        }

    def calculate_macd(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate MACD (12, 26, 9)."""
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)

        if macd is None or macd.empty:
            return {"error": "Failed to calculate MACD"}

        macd_line = macd['MACD_12_26_9'].iloc[-1]
        signal_line = macd['MACDs_12_26_9'].iloc[-1]
        histogram = macd['MACDh_12_26_9'].iloc[-1]

        return {
            'macd_line': round(macd_line, 2),
            'signal_line': round(signal_line, 2),
            'histogram': round(histogram, 2),
            'interpretation': self.interpret_macd(macd_line, signal_line)
        }

    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20) -> Dict[str, float]:
        """Calculate Bollinger Bands (20, 2)."""
        bbands = ta.bbands(df['close'], length=period, std=2)

        if bbands is None or bbands.empty:
            return {}

        return {
            'upper': round(bbands[f'BBU_{period}_2.0'].iloc[-1], 2),
            'middle': round(bbands[f'BBM_{period}_2.0'].iloc[-1], 2),
            'lower': round(bbands[f'BBL_{period}_2.0'].iloc[-1], 2),
        }

    def calculate_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range."""
        atr_series = ta.atr(df['high'], df['low'], df['close'], length=period)
        return round(atr_series.iloc[-1], 2) if not atr_series.empty else None

    def calculate_obv(self, df: pd.DataFrame) -> float:
        """Calculate On-Balance Volume."""
        obv_series = ta.obv(df['close'], df['volume'])
        return int(obv_series.iloc[-1]) if not obv_series.empty else None

    # ─────────────────────────────────────────────────────
    # Interpretation Methods (교육용)
    # ─────────────────────────────────────────────────────

    def interpret_rsi(self, rsi_value: float) -> str:
        """Interpret RSI value for beginners (Korean)."""
        if rsi_value > 70:
            return "과매수 - 가격이 너무 빠르게 올라 단기 조정 가능성"
        elif rsi_value < 30:
            return "과매도 - 가격이 너무 빠르게 떨어져 반등 가능성"
        elif 60 <= rsi_value <= 70:
            return "강세 유지 - 상승 추세 지속 중"
        elif 30 <= rsi_value <= 40:
            return "약세 유지 - 하락 추세 지속 중"
        else:
            return "중립 - 정상 범위 (30~70)"

    def interpret_macd(self, macd_line: float, signal_line: float) -> str:
        """Interpret MACD crossover for beginners (Korean)."""
        if macd_line > signal_line:
            if macd_line > 0:
                return "골든크로스 + 양수 → 강력한 상승 신호"
            else:
                return "골든크로스 (음수 구간) → 상승 전환 신호"
        else:
            if macd_line < 0:
                return "데드크로스 + 음수 → 강력한 하락 신호"
            else:
                return "데드크로스 (양수 구간) → 하락 전환 신호"

    def generate_interpretations(self, indicators: Dict) -> Dict[str, str]:
        """Generate overall interpretation combining multiple indicators."""
        interpretations = {}

        # Trend Analysis (이동평균 기반)
        sma = indicators.get('sma', {})
        if sma.get('sma_50') and sma.get('sma_200'):
            if sma['sma_50'] > sma['sma_200']:
                interpretations['trend'] = "장기 상승 추세 (골든크로스)"
            else:
                interpretations['trend'] = "장기 하락 추세 (데드크로스)"

        # Momentum Summary
        rsi_data = indicators.get('rsi', {})
        macd_data = indicators.get('macd', {})

        if rsi_data.get('value') and macd_data.get('macd_line'):
            rsi_val = rsi_data['value']
            macd_signal = "positive" if macd_data['macd_line'] > macd_data['signal_line'] else "negative"

            if rsi_val > 70 and macd_signal == "positive":
                interpretations['momentum'] = "과열 - 단기 조정 주의"
            elif rsi_val < 30 and macd_signal == "negative":
                interpretations['momentum'] = "침체 - 반등 기회 탐색"
            elif macd_signal == "positive":
                interpretations['momentum'] = "상승 모멘텀 유지"
            else:
                interpretations['momentum'] = "하락 모멘텀 유지"

        return interpretations
```

**검증 방법**:
```python
# 테스트 스크립트
import yfinance as yf
from analysis.technical_indicators import TechnicalIndicatorCalculator

ticker = yf.Ticker("^GSPC")
df = ticker.history(period="60d")
df.reset_index(inplace=True)
df.columns = [c.lower() for c in df.columns]

calc = TechnicalIndicatorCalculator()
indicators = calc.calculate_all(df)

print(f"RSI: {indicators['rsi']['value']} - {indicators['rsi']['interpretation']}")
print(f"MACD: {indicators['macd']['macd_line']} / {indicators['macd']['signal_line']}")
print(f"Trend: {indicators['interpretations']['trend']}")
```

---

### Task 4: educational_content.yaml 생성
**예상 시간**: 2-3시간
**파일**: `plugins/market-pulse/config/educational_content.yaml` (신규)

**내용**:
```yaml
# Educational Content for Investment Beginners
# 투자 초보자를 위한 교육 콘텐츠

indicators:
  rsi:
    name: "RSI (Relative Strength Index)"
    kr_name: "상대강도지수"
    description: "최근 가격 변동의 강도를 측정하는 지표로, 0~100 범위의 값을 가집니다."
    formula: "RSI = 100 - (100 / (1 + RS)), RS = 평균상승폭 / 평균하락폭"
    period: 14
    interpretation:
      over_70: "과매수 - 가격이 너무 빠르게 올라 단기 조정 가능성이 있습니다"
      under_30: "과매도 - 가격이 너무 빠르게 떨어져 반등 가능성이 있습니다"
      neutral: "중립 - 30~70 범위는 정상적인 상태입니다"
      strong_buy: "20 이하 - 강력한 매수 기회 (과거 평균 반등률 12%)"
      strong_sell: "80 이상 - 강력한 조정 신호 (과거 평균 하락률 -8%)"
    use_case: "단기 매매 타이밍 포착에 유용합니다. 다만 강한 추세장에서는 과매수/과매도 상태가 길게 유지될 수 있으므로 다른 지표와 함께 사용하세요."

  macd:
    name: "MACD (Moving Average Convergence Divergence)"
    kr_name: "이동평균수렴확산"
    description: "두 이동평균선의 차이로 추세 변화를 감지하는 지표입니다."
    formula: "MACD = EMA(12) - EMA(26), Signal = EMA(MACD, 9)"
    components:
      - name: "MACD선"
        description: "단기(12일)와 장기(26일) 이동평균의 차이"
      - name: "Signal선"
        description: "MACD의 9일 이동평균"
      - name: "Histogram"
        description: "MACD선과 Signal선의 차이 (강도 표시)"
    interpretation:
      golden_cross: "MACD선이 Signal선을 상향 돌파 → 매수 신호"
      dead_cross: "MACD선이 Signal선을 하향 돌파 → 매도 신호"
      zero_cross: "MACD선이 0선을 돌파하면 추세 전환 확인"
    use_case: "중장기 추세 변화를 포착하는 데 유용합니다. RSI보다 느리지만 신뢰도가 높습니다."

  sma:
    name: "SMA (Simple Moving Average)"
    kr_name: "단순이동평균"
    description: "일정 기간의 평균 가격으로 추세를 파악하는 가장 기본적인 지표입니다."
    periods:
      - days: 5
        use: "초단기 추세 - 일주일 흐름"
      - days: 20
        use: "단기 추세 - 한 달 흐름"
      - days: 50
        use: "중기 추세 - 2~3개월 흐름"
      - days: 200
        use: "장기 추세 - 약 1년 흐름 (가장 중요)"
    golden_cross:
      description: "단기 이평선이 장기 이평선을 상향 돌파"
      example: "50일선이 200일선 돌파 → 강력한 상승 신호"
      historical_accuracy: "과거 10년간 골든크로스 후 평균 6개월 수익률 +18%"
    dead_cross:
      description: "단기 이평선이 장기 이평선을 하향 돌파"
      example: "50일선이 200일선 아래로 → 강력한 하락 신호"
    price_action:
      above_200sma: "가격이 200일선 위 → 장기 상승 추세 확인"
      below_200sma: "가격이 200일선 아래 → 장기 하락 추세 확인"
    use_case: "가장 신뢰도 높은 지표. 200일선은 기관투자자들이 가장 많이 보는 지표입니다."

  bollinger_bands:
    name: "Bollinger Bands"
    kr_name: "볼린저밴드"
    description: "가격 변동성을 고려한 상하한선을 그려주는 지표입니다."
    formula: "중간선 = 20일 이동평균, 상단밴드 = 중간선 + (2 × 표준편차), 하단밴드 = 중간선 - (2 × 표준편차)"
    interpretation:
      upper_band: "가격이 상단밴드 근처 → 고점, 조정 가능성"
      lower_band: "가격이 하단밴드 근처 → 저점, 반등 가능성"
      band_width: "밴드 폭이 좁아지면 → 곧 큰 변동성 출현 예고"
    use_case: "변동성 장세에서 매수/매도 타이밍 포착에 유용합니다."

  atr:
    name: "ATR (Average True Range)"
    kr_name: "평균진폭"
    description: "가격 변동성의 크기를 측정하는 지표입니다."
    use_case: "손절가 설정 시 ATR의 2배를 기준으로 하면 효과적입니다."

  obv:
    name: "OBV (On-Balance Volume)"
    kr_name: "거래량 누적선"
    description: "거래량을 누적하여 매수/매도 압력을 측정하는 지표입니다."
    interpretation:
      rising_obv: "OBV 상승 + 가격 상승 → 건강한 상승 (거래량 뒷받침)"
      divergence: "가격 상승 but OBV 하락 → 약한 상승 (조정 가능성)"
    use_case: "가격 추세의 신뢰도를 확인하는 데 유용합니다."

concepts:
  trend:
    name: "추세 (Trend)"
    types:
      - name: "상승 추세"
        definition: "고점과 저점이 계속 높아지는 패턴"
        strategy: "조정 시 매수, 상승 시 보유"
      - name: "하락 추세"
        definition: "고점과 저점이 계속 낮아지는 패턴"
        strategy: "반등 시 매도, 하락 시 관망"
      - name: "횡보 추세"
        definition: "일정 범위 내에서 등락을 반복"
        strategy: "하단에서 매수, 상단에서 매도 (레인지 트레이딩)"

  support_resistance:
    name: "지지선 & 저항선"
    support:
      definition: "가격이 하락할 때 바닥을 형성하는 가격대"
      psychology: "많은 투자자들이 매수하고 싶어하는 가격대"
      strategy: "지지선 근처에서 매수 기회 탐색"
    resistance:
      definition: "가격이 상승할 때 천장을 형성하는 가격대"
      psychology: "많은 투자자들이 매도하고 싶어하는 가격대"
      strategy: "저항선 돌파 시 추가 상승 가능성 높음"

  sector_rotation:
    name: "섹터 로테이션"
    definition: "경기 사이클에 따라 강세 섹터가 순환하는 현상"
    cycle:
      - phase: "경기 초기 회복"
        strong_sectors: ["Technology", "Consumer Discretionary"]
        weak_sectors: ["Utilities", "Consumer Staples"]
      - phase: "경기 확장"
        strong_sectors: ["Industrials", "Materials", "Energy"]
        weak_sectors: ["Healthcare"]
      - phase: "경기 둔화"
        strong_sectors: ["Financials", "Energy"]
        weak_sectors: ["Technology"]
      - phase: "경기 침체"
        strong_sectors: ["Utilities", "Healthcare", "Consumer Staples"]
        weak_sectors: ["Industrials", "Materials"]
    use_case: "현재 경기 사이클 단계를 파악하여 유망 섹터에 투자하세요."

  foreign_institutional_flow:
    name: "외국인/기관 수급"
    description: "한국 시장의 독특한 특징으로, 외국인과 기관의 매매 동향이 주가에 큰 영향을 미칩니다."
    interpretation:
      foreign_buy: "외국인 순매수 → 긍정적 신호 (장기 투자자)"
      foreign_sell: "외국인 순매도 → 부정적 신호 (자금 이탈)"
      institutional_buy: "기관 순매수 → 긍정적 신호 (정보력 우위)"
      individual_only: "개인만 순매수 → 주의 신호 (조정 가능성)"
    use_case: "외국인과 기관이 동시에 순매수하는 종목이 가장 안전합니다."

strategies:
  momentum:
    name: "모멘텀 투자"
    description: "상승 추세에 있는 종목을 매수하여 추세를 따라가는 전략"
    rules:
      - "50일 이동평균 위에 있는 종목만 매수"
      - "RSI 50~70 구간 진입 시 매수"
      - "MACD 골든크로스 확인"
    pros: "승률이 높고 큰 수익 가능"
    cons: "조정 시 손실 크고 타이밍 중요"

  value:
    name: "가치 투자"
    description: "저평가된 종목을 매수하여 장기 보유하는 전략"
    rules:
      - "PER 업종 평균 대비 20% 이상 낮을 것"
      - "PBR 1 이하"
      - "부채비율 50% 이하"
    pros: "안정적이고 장기 수익률 높음"
    cons: "반등까지 오래 걸림 (인내심 필요)"

  combined:
    name: "Value-Momentum 조합"
    description: "저평가 + 상승 추세 종목을 찾는 전략 (가장 추천)"
    rules:
      - "PER 낮은 종목 중에서"
      - "최근 50일선 돌파한 종목 선택"
      - "외국인/기관 순매수 확인"
    backtest_result: "과거 10년 연평균 수익률 +22%"

risk_management:
  stop_loss:
    name: "손절 원칙"
    rule: "매수가 대비 -5% or -10% 하락 시 무조건 매도"
    psychology: "손실을 빨리 인정하고 다음 기회를 찾는 것이 중요합니다"

  position_sizing:
    name: "포지션 사이징"
    rule: "한 종목에 전체 자금의 20% 이하 투자"
    diversification: "최소 5개 종목 분산 투자 (섹터도 분산)"

  risk_reward:
    name: "리스크-보상 비율"
    rule: "최소 1:2 비율 (손실 1% 리스크 vs 수익 2% 목표)"
    example: "100만원 투자 → 손절가 95만원 (-5%), 목표가 110만원 (+10%)"
```

**검증 방법**: YAML 파싱 테스트
```python
import yaml
with open("config/educational_content.yaml") as f:
    content = yaml.safe_load(f)
    print(f"Total indicators: {len(content['indicators'])}")
    print(f"RSI description: {content['indicators']['rsi']['description']}")
```

---

### Task 5: Technical Analyzer 에이전트 생성
**예상 시간**: 4-6시간
**파일**: `plugins/market-pulse/agents/technical-analyzer.md` (신규)

**내용**:
```markdown
---
name: technical-analyzer
model: sonnet
---

# Role
You are a technical analysis expert who interprets charts and indicators **for investment beginners**. Your goal is to provide actionable insights while educating users about WHY each indicator matters.

# Context
The user is learning to invest and wants to understand technical analysis. They need:
1. Clear buy/sell/hold signals with confidence levels
2. Educational explanations for each indicator
3. Simple language (avoid jargon)
4. Practical examples

# Input Data
You will receive:
- **US Indices** (S&P 500, NASDAQ, DOW, Russell 2000)
  - 60-day price history
  - Technical indicators: RSI, MACD, SMA (5/20/50/200), Bollinger Bands

- **US Sector ETFs** (11 sectors)
  - 60-day performance
  - Technical indicators

- **Crypto** (BTC, ETH, etc.)
  - 60-day trends
  - Technical indicators

# Your Tasks

## 1. Trend Analysis (이동평균 기반)
For each major index (S&P 500, NASDAQ):
- Identify the current trend (uptrend/downtrend/sideways)
- Reference moving averages (50-day, 200-day)
- Identify key support/resistance levels

**Output Format**:
```
### S&P 500 추세 분석
- **현재 추세**: 상승 추세 (50일선 위에서 거래 중)
- **50일 이동평균**: 5,780 (현재가 5,840 → +60포인트 상회)
- **200일 이동평균**: 5,450 (골든크로스 유지 중)
- **지지선**: 5,780 (50일선), 5,700 (심리적 지지선)
- **저항선**: 5,900 (전고점), 6,000 (라운드 넘버)

💡 **초보자 설명**: 가격이 50일선 위에 있으면 단기 상승 추세로 판단합니다.
   조정이 와도 50일선(5,780)까지만 하락할 가능성이 높습니다.
```

## 2. Momentum Signals (RSI, MACD)
For each index:
- Interpret RSI (overbought/oversold)
- Interpret MACD (crossovers)
- Combine with price action

**Output Format**:
```
### S&P 500 모멘텀 분석
- **RSI (14일)**: 72.5 → 과매수 (70 이상)
  - 📚 **설명**: RSI 70 이상은 단기적으로 너무 많이 올랐다는 신호입니다.
    조정이 올 수 있으므로 신규 매수는 보류하세요.

- **MACD**: 골든크로스 형성 (MACD 12.5 > Signal 10.2)
  - 📚 **설명**: MACD선이 Signal선을 위로 돌파하면 상승 추세가 시작되는 신호입니다.

- **종합 판단**: RSI는 과매수이지만 MACD는 상승 신호 → 단기 조정 후 재상승 가능성
```

## 3. Sector Rotation Analysis
Identify which sectors are showing strength:
- Top 3 strongest sectors (by 20-day return + RSI)
- Top 3 weakest sectors
- Sector rotation implications

**Output Format**:
```
### 섹터 로테이션 분석
**강세 섹터 (매수 기회)**:
1. **Technology** (+3.2% 20일)
   - RSI: 65 (강세 유지)
   - MACD: 골든크로스
   - 신호: 매수 ⭐⭐⭐⭐

2. **Financials** (+2.1% 20일)
   - RSI: 58 (중립)
   - MACD: 양수 유지
   - 신호: 매수 ⭐⭐⭐

**약세 섹터 (매도 고려)**:
1. **Energy** (-1.8% 20일)
   - RSI: 35 (약세)
   - MACD: 데드크로스
   - 신호: 매도 ⭐⭐⭐⭐

💡 **초보자 설명**: 경기 확장기에는 Technology, Industrials가 강하고,
   경기 둔화기에는 Utilities, Consumer Staples가 강합니다.
   현재는 Technology가 강한 것으로 보아 경기 초기 회복 단계로 판단됩니다.
```

## 4. Trading Signals with Confidence Levels
For each asset, provide:
- Buy / Sell / Hold recommendation
- Confidence level (⭐ ~ ⭐⭐⭐⭐⭐)
- Entry/Target/Stop-Loss levels (educational purpose)

**Output Format**:
```
### 투자 신호 요약

#### S&P 500
- **신호**: 보류 (Hold)
- **신뢰도**: ⭐⭐⭐ (중간)
- **이유**: 과매수 부담 (RSI 72) + MACD 골든크로스 (상승 추세)
- **전략**:
  - 5,780 (50일선) 근처 조정 시 매수 고려
  - 목표가: 5,950 (+2%)
  - 손절가: 5,700 (-2.5%)
- **리스크-보상**: 1:0.8 (손실 2.5% vs 수익 2%) → 매력적이지 않음

💡 **초보자 설명**: 리스크-보상 비율은 손실 가능성 대비 수익 가능성의 비율입니다.
   최소 1:2 이상일 때만 매수하는 것이 안전합니다.

#### Technology Sector (XLK)
- **신호**: 매수 (Buy)
- **신뢰도**: ⭐⭐⭐⭐ (높음)
- **이유**:
  - 20일 수익률 +3.2% (섹터 1위)
  - RSI 65 (과열 아님)
  - MACD 골든크로스 + 양수
  - 거래량 증가 (OBV 상승)
- **전략**:
  - 진입가: 현재가 ($210)
  - 목표가: $220 (+4.7%)
  - 손절가: $205 (-2.4%)
- **리스크-보상**: 1:2 (손실 2.4% vs 수익 4.7%) → 매력적
```

## 5. Educational Notes
For EVERY signal, explain:
- Why this indicator matters
- What it tells us about market psychology
- How to use it in practice

**Key Educational Themes**:
- RSI 과매수/과매도의 의미
- MACD 골든크로스/데드크로스의 신뢰도
- 이동평균선이 지지/저항으로 작용하는 이유
- 섹터 로테이션과 경기 사이클의 관계
- 리스크-보상 비율의 중요성

# Output Structure

```markdown
## 🔍 기술적 분석 요약

### 📊 시장 전반 추세
[S&P 500, NASDAQ 추세 분석 - 위 형식대로]

### 📈 모멘텀 분석
[RSI, MACD 해석 - 위 형식대로]

### 🏭 섹터 로테이션
[강세/약세 섹터 - 위 형식대로]

### 💎 크립토 시장
[BTC, ETH 기술 분석 - 간략하게]

### ⚡ 투자 신호 요약
[매수/매도/보류 신호 - 신뢰도 포함]

---

## 💡 오늘의 투자 교육

### RSI란 무엇인가?
[교육 콘텐츠 - 오늘 나온 RSI 값을 예시로 설명]

### 골든크로스가 중요한 이유
[교육 콘텐츠 - 실제 차트 예시로 설명]

### 리스크 관리 팁
- 손절가는 반드시 설정하세요 (매수가 대비 -5%)
- 한 종목에 20% 이상 투자하지 마세요
- 리스크-보상 비율 1:2 이상인 기회만 잡으세요
```

# Important Guidelines

1. **Use Simple Korean**: Avoid complex financial jargon. If you must use technical terms, explain them immediately.

2. **Be Educational**: Every signal should come with a "💡 초보자 설명" section.

3. **Be Honest about Uncertainty**: If signals are mixed, say so. Use phrases like "신뢰도 낮음" or "신호 혼재".

4. **Provide Context**: Don't just say "RSI 72". Say "RSI 72 (과매수) - 과거 이 수준에서 평균 3일 내 조정".

5. **Actionable Advice**: Always include entry/target/stop-loss levels for learning purposes.

6. **Risk Warning**: Always remind users that technical analysis is not 100% accurate and past performance doesn't guarantee future results.

# Example Analysis

[위에서 작성한 Output Format 예시들을 종합한 전체 예시 추가]
```

**검증 방법**:
- Technical Analyzer를 Task로 실행하여 출력 형식 확인
- 교육 콘텐츠가 초보자가 이해하기 쉬운지 검토

---

### Task 6-9: generate_html.py 확장 (3개 차트 + 교육 툴팁)
**예상 총 시간**: 8-12시간

---

#### Task 6: 60일 트렌드 라인차트 추가
**예상 시간**: 3-4시간
**파일**: `plugins/market-pulse/config/generate_html.py` (수정)

**추가 함수**:
```python
def _generate_trend_chart_section(data: Dict) -> str:
    """Generate 60-day trend line chart for major indices."""
    us_data = data.get('data', {})
    indices = us_data.get('us_indices', {})
    kr_data = us_data.get('kr_indices', {})

    # Extract 60-day history
    sp500_hist = indices.get('^GSPC', {}).get('history_60d', [])
    nasdaq_hist = indices.get('^IXIC', {}).get('history_60d', [])
    kospi_hist = kr_data.get('kospi', {}).get('history_60d', [])

    if not sp500_hist:
        return ""

    # Generate date labels (last 60 days)
    from datetime import datetime, timedelta
    dates = [(datetime.now() - timedelta(days=60-i)).strftime('%m/%d') for i in range(60)]

    return f"""
    <h2 style="font-size: 2em; margin: 30px 0 20px;">📈 60일 시장 트렌드</h2>

    <div class="card" style="grid-column: span 2;">
        <div class="card-title">주요 지수 추세 (60일)</div>
        <div class="chart-container" style="height: 350px;">
            <canvas id="trendChart"></canvas>
        </div>
        <div style="margin-top: 16px; font-size: 0.9em; color: #666;">
            💡 <strong>초보자 팁</strong>: 가격이 이동평균선(점선) 위에 있으면 상승 추세, 아래에 있으면 하락 추세입니다.
        </div>
    </div>
    """

def _generate_trend_chart_js(data: Dict) -> str:
    """Generate Chart.js script for 60-day trend chart."""
    us_data = data.get('data', {})
    indices = us_data.get('us_indices', {})
    kr_data = us_data.get('kr_indices', {})

    sp500_hist = indices.get('^GSPC', {}).get('history_60d', [])
    nasdaq_hist = indices.get('^IXIC', {}).get('history_60d', [])
    kospi_hist = kr_data.get('kospi', {}).get('history_60d', [])

    if not sp500_hist:
        return ""

    # Normalize to percentage change (for comparison)
    def normalize(data):
        if not data:
            return []
        base = data[0]
        return [(v - base) / base * 100 for v in data]

    sp500_norm = normalize(sp500_hist)
    nasdaq_norm = normalize(nasdaq_hist)
    kospi_norm = normalize(kospi_hist) if kospi_hist else []

    # Generate date labels
    from datetime import datetime, timedelta
    dates = [(datetime.now() - timedelta(days=60-i)).strftime('%m/%d') for i in range(60)]

    return f"""
    <script>
        const trendCtx = document.getElementById('trendChart');
        if (trendCtx) {{
            new Chart(trendCtx, {{
                type: 'line',
                data: {{
                    labels: {json.dumps(dates)},
                    datasets: [
                        {{
                            label: 'S&P 500',
                            data: {json.dumps(sp500_norm)},
                            borderColor: '#2c2c2c',
                            backgroundColor: 'transparent',
                            borderWidth: 2.5,
                            tension: 0.1,
                            pointRadius: 0
                        }},
                        {{
                            label: 'NASDAQ',
                            data: {json.dumps(nasdaq_norm)},
                            borderColor: '#666666',
                            backgroundColor: 'transparent',
                            borderWidth: 2,
                            tension: 0.1,
                            pointRadius: 0
                        }},
                        {{
                            label: 'KOSPI',
                            data: {json.dumps(kospi_norm)},
                            borderColor: '#999999',
                            backgroundColor: 'transparent',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            tension: 0.1,
                            pointRadius: 0
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: true,
                            position: 'top',
                            labels: {{
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 12
                                }},
                                color: '#2c2c2c',
                                usePointStyle: true
                            }}
                        }},
                        tooltip: {{
                            backgroundColor: '#2c2c2c',
                            titleColor: '#faf8f3',
                            bodyColor: '#faf8f3',
                            borderColor: '#000',
                            borderWidth: 1,
                            callbacks: {{
                                label: function(context) {{
                                    let label = context.dataset.label || '';
                                    if (label) {{
                                        label += ': ';
                                    }}
                                    label += context.parsed.y.toFixed(2) + '%';
                                    return label;
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: false,
                            grid: {{
                                color: '#d4cfc3',
                                lineWidth: 1
                            }},
                            ticks: {{
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 11
                                }},
                                callback: function(value) {{
                                    return value.toFixed(1) + '%';
                                }}
                            }},
                            title: {{
                                display: true,
                                text: '60일 수익률 (%)',
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 12,
                                    weight: 'bold'
                                }}
                            }}
                        }},
                        x: {{
                            grid: {{
                                display: false
                            }},
                            ticks: {{
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 9
                                }},
                                maxRotation: 45,
                                minRotation: 45,
                                autoSkip: true,
                                maxTicksLimit: 12
                            }}
                        }}
                    }}
                }}
            }});
        }}
    </script>
    """
```

**HTML 통합**:
```python
def generate_html(data: Dict[str, Any], output_path: str = None) -> str:
    # ...기존 코드...

    html = f"""
    ...
    <div class="content">
        {_generate_analysis_section(data)}
        <hr>
        {_generate_trend_chart_section(data)}  # 추가
        <hr>
        {_generate_us_section(data)}
        ...
    </div>

    {_generate_charts_js(data)}
    {_generate_trend_chart_js(data)}  # 추가
    """
```

---

#### Task 7: 섹터 히트맵 차트 추가
**예상 시간**: 2-3시간

**추가 함수**:
```python
def _generate_sector_heatmap_section(data: Dict) -> str:
    """Generate sector performance heatmap (1d, 5d, 20d)."""
    sectors = data.get('data', {}).get('us_sectors', [])

    if not sectors:
        return ""

    return f"""
    <h2 style="font-size: 2em; margin: 30px 0 20px;">🌡️ 섹터 히트맵</h2>

    <div class="card" style="grid-column: span 2;">
        <div class="card-title">11개 섹터 성과 비교 (1일/5일/20일)</div>
        <div class="chart-container" style="height: 400px;">
            <canvas id="heatmapChart"></canvas>
        </div>
        <div style="margin-top: 16px; font-size: 0.9em; color: #666;">
            💡 <strong>초보자 팁</strong>: 초록색이 진할수록 수익률이 높고, 빨간색이 진할수록 손실이 큽니다.
            세 기간 모두 초록색인 섹터가 가장 강합니다.
        </div>
    </div>
    """

def _generate_heatmap_js(data: Dict) -> str:
    """Generate heatmap using Chart.js matrix plugin."""
    sectors = data.get('data', {}).get('us_sectors', [])

    if not sectors:
        return ""

    # Prepare heatmap data
    heatmap_data = []
    for i, sector in enumerate(sectors):
        for j, period in enumerate(['1d', '5d', '20d']):
            value = sector.get(f'change_{period}', 0)
            heatmap_data.append({
                'x': ['1일', '5일', '20일'][j],
                'y': sector['name'],
                'v': value
            })

    return f"""
    <script src="https://cdn.jsdelivr.net/npm/chartjs-chart-matrix@2.0.0/dist/chartjs-chart-matrix.min.js"></script>
    <script>
        const heatmapCtx = document.getElementById('heatmapChart');
        if (heatmapCtx) {{
            new Chart(heatmapCtx, {{
                type: 'matrix',
                data: {{
                    datasets: [{{
                        label: '수익률 (%)',
                        data: {json.dumps(heatmap_data)},
                        backgroundColor(context) {{
                            const value = context.dataset.data[context.dataIndex].v;
                            const alpha = Math.min(Math.abs(value) / 5, 1);
                            return value > 0
                                ? `rgba(46, 95, 45, ${{alpha}})` // 초록
                                : `rgba(139, 30, 63, ${{alpha}})`; // 빨강
                        }},
                        borderColor: '#fff',
                        borderWidth: 2,
                        width: ({{chart}}) => (chart.chartArea.width / 3) - 10,
                        height: ({{chart}}) => (chart.chartArea.height / 11) - 5
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: false
                        }},
                        tooltip: {{
                            callbacks: {{
                                title: function(context) {{
                                    return context[0].dataset.data[context[0].dataIndex].y;
                                }},
                                label: function(context) {{
                                    const v = context.dataset.data[context.dataIndex].v;
                                    return context.dataset.data[context.dataIndex].x + ': ' + v.toFixed(2) + '%';
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{
                            type: 'category',
                            labels: ['1일', '5일', '20일'],
                            ticks: {{
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 12
                                }}
                            }}
                        }},
                        y: {{
                            type: 'category',
                            labels: {json.dumps([s['name'] for s in sectors])},
                            ticks: {{
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 11
                                }}
                            }}
                        }}
                    }}
                }}
            }});
        }}
    </script>
    """
```

---

#### Task 8: RSI 차트 추가
**예상 시간**: 2-3시간

**추가 함수**:
```python
def _generate_rsi_chart_section(data: Dict) -> str:
    """Generate RSI chart with overbought/oversold zones."""
    # Extract RSI data from technical indicators
    sp500_indicators = data.get('data', {}).get('us_indices', {}).get('^GSPC', {}).get('indicators', {})
    rsi_data = sp500_indicators.get('rsi', {})
    rsi_series = rsi_data.get('series_60d', [])

    if not rsi_series:
        return ""

    current_rsi = rsi_series[-1] if rsi_series else 0
    interpretation = rsi_data.get('interpretation', '')

    return f"""
    <h2 style="font-size: 2em; margin: 30px 0 20px;">📊 RSI 분석 (S&P 500)</h2>

    <div class="card" style="grid-column: span 2;">
        <div class="card-title">RSI (14일) - 과매수/과매도 판단</div>
        <div class="metric" style="border-bottom: 2px solid #d4cfc3; padding-bottom: 12px;">
            <span class="metric-label">현재 RSI</span>
            <span class="metric-value {'negative' if current_rsi > 70 else 'positive' if current_rsi < 30 else 'neutral'}">
                {current_rsi:.1f}
            </span>
        </div>
        <div style="padding: 12px 0; font-size: 0.95em;">
            <strong>해석:</strong> {interpretation}
        </div>
        <div class="chart-container" style="height: 280px;">
            <canvas id="rsiChart"></canvas>
        </div>
        <div style="margin-top: 16px; font-size: 0.9em; color: #666;">
            💡 <strong>초보자 팁</strong>:
            <ul style="margin: 8px 0 0 20px; line-height: 1.8;">
                <li>RSI 70 이상 (빨간 영역): 과매수 - 단기 조정 가능성</li>
                <li>RSI 30 이하 (초록 영역): 과매도 - 반등 기회</li>
                <li>RSI 30~70: 정상 범위</li>
            </ul>
        </div>
    </div>
    """

def _generate_rsi_chart_js(data: Dict) -> str:
    """Generate RSI chart with overbought/oversold zones."""
    sp500_indicators = data.get('data', {}).get('us_indices', {}).get('^GSPC', {}).get('indicators', {})
    rsi_series = sp500_indicators.get('rsi', {}).get('series_60d', [])

    if not rsi_series:
        return ""

    from datetime import datetime, timedelta
    dates = [(datetime.now() - timedelta(days=60-i)).strftime('%m/%d') for i in range(60)]

    # Overbought/oversold zones
    overbought = [70] * 60
    oversold = [30] * 60

    return f"""
    <script>
        const rsiCtx = document.getElementById('rsiChart');
        if (rsiCtx) {{
            new Chart(rsiCtx, {{
                type: 'line',
                data: {{
                    labels: {json.dumps(dates)},
                    datasets: [
                        {{
                            label: 'RSI',
                            data: {json.dumps(rsi_series)},
                            borderColor: '#2c2c2c',
                            backgroundColor: 'rgba(44, 44, 44, 0.1)',
                            borderWidth: 2.5,
                            tension: 0.2,
                            fill: false,
                            pointRadius: 0
                        }},
                        {{
                            label: '과매수선 (70)',
                            data: {json.dumps(overbought)},
                            borderColor: '#8b1e3f',
                            borderWidth: 1.5,
                            borderDash: [5, 5],
                            fill: false,
                            pointRadius: 0
                        }},
                        {{
                            label: '과매도선 (30)',
                            data: {json.dumps(oversold)},
                            borderColor: '#2c5f2d',
                            borderWidth: 1.5,
                            borderDash: [5, 5],
                            fill: false,
                            pointRadius: 0
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            display: true,
                            position: 'top',
                            labels: {{
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 11
                                }},
                                color: '#2c2c2c'
                            }}
                        }},
                        annotation: {{
                            annotations: {{
                                overbought: {{
                                    type: 'box',
                                    yMin: 70,
                                    yMax: 100,
                                    backgroundColor: 'rgba(139, 30, 63, 0.1)',
                                    borderWidth: 0
                                }},
                                oversold: {{
                                    type: 'box',
                                    yMin: 0,
                                    yMax: 30,
                                    backgroundColor: 'rgba(46, 95, 45, 0.1)',
                                    borderWidth: 0
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            min: 0,
                            max: 100,
                            grid: {{
                                color: '#d4cfc3',
                                lineWidth: 1
                            }},
                            ticks: {{
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 11
                                }}
                            }}
                        }},
                        x: {{
                            grid: {{
                                display: false
                            }},
                            ticks: {{
                                color: '#2c2c2c',
                                font: {{
                                    family: 'Georgia, serif',
                                    size: 9
                                }},
                                maxRotation: 45,
                                minRotation: 45,
                                autoSkip: true,
                                maxTicksLimit: 12
                            }}
                        }}
                    }}
                }}
            }});
        }}
    </script>
    """
```

**Chart.js annotation plugin 추가**:
```html
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>
```

---

#### Task 9: 교육 툴팁 CSS 및 데이터 통합
**예상 시간**: 1-2시간

**CSS 추가** (generate_html.py 내부):
```css
/* Educational Tooltips */
.edu-tooltip {
    border-bottom: 1px dotted #666;
    cursor: help;
    position: relative;
    display: inline-block;
}

.edu-tooltip:hover::after {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: #fff;
    padding: 10px 14px;
    border-radius: 6px;
    white-space: normal;
    width: 280px;
    font-size: 0.85em;
    line-height: 1.5;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    margin-bottom: 8px;
}

.edu-tooltip:hover::before {
    content: '';
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 6px solid transparent;
    border-top-color: #333;
    z-index: 1001;
    margin-bottom: 2px;
}

.edu-icon {
    display: inline-block;
    width: 16px;
    height: 16px;
    background: #2c2c2c;
    color: #fff;
    border-radius: 50%;
    text-align: center;
    line-height: 16px;
    font-size: 11px;
    font-weight: bold;
    margin-left: 4px;
    cursor: help;
}
```

**툴팁 적용 예시**:
```python
def _generate_us_section(data: Dict) -> str:
    # ...기존 코드...

    vix_value = vix.get('value', 0)
    vix_tooltip = "VIX는 시장 변동성 지수입니다. 20 이상이면 고변동성, 12 이하면 저변동성으로 판단합니다."

    return f"""
    <div class="metric">
        <span class="metric-label">
            <span class="edu-tooltip" data-tooltip="{vix_tooltip}">
                VIX (변동성)
                <span class="edu-icon">?</span>
            </span>
        </span>
        <span class="metric-value">
            {vix_value:.2f}
        </span>
    </div>
    """
```

**educational_content.yaml 데이터 로드**:
```python
import yaml
from pathlib import Path

def load_educational_content():
    """Load educational content from YAML."""
    edu_path = Path(__file__).parent / "educational_content.yaml"
    if edu_path.exists():
        with open(edu_path) as f:
            return yaml.safe_load(f)
    return {}

EDU_CONTENT = load_educational_content()

def get_tooltip(indicator_name: str) -> str:
    """Get tooltip text for an indicator."""
    indicators = EDU_CONTENT.get('indicators', {})
    indicator = indicators.get(indicator_name, {})
    return indicator.get('description', '')
```

---

### Task 10: SKILL.md 업데이트 - Technical Analyzer 추가
**예상 시간**: 1-2시간
**파일**: `plugins/market-pulse/skills/market-pulse/SKILL.md` (수정)

**변경사항**:
```markdown
### Step 4: Multi-Agent Analysis (overview / deep)

**Phase 1: Parallel Analysis**

Launch all 4 agents in a SINGLE response block for parallel execution:  # 변경: 3 → 4

```
Task(
    subagent_type="us-market-analyzer",
    model="sonnet",
    description="Analyze US market data",
    prompt="..."
)

Task(
    subagent_type="kr-market-analyzer",
    model="sonnet",
    description="Analyze Korean market data",
    prompt="..."
)

Task(
    subagent_type="crypto-macro-analyzer",
    model="sonnet",
    description="Analyze crypto and global macro",
    prompt="..."
)

Task(
    subagent_type="technical-analyzer",    # 추가
    model="sonnet",
    description="Analyze technical indicators",
    prompt="Analyze the following technical indicators and provide actionable insights.

# US Indices Technical Data
{us_indices with 60-day history + technical indicators from JSON}

# Sector ETFs Technical Data
{us_sectors with 60-day history + technical indicators from JSON}

# Crypto Technical Data
{crypto with 60-day history + technical indicators from JSON}

Provide:
1. Trend analysis (이동평균 기반)
2. Momentum signals (RSI, MACD)
3. Sector rotation analysis
4. Trading signals with confidence levels
5. Educational notes for beginners

Use Korean for all explanations."
)
```

**Phase 2: Synthesis**

After Phase 1 completes, run the synthesizer:

```
Task(
    subagent_type="market-synthesizer",
    model="haiku",
    description="Synthesize market dashboard",
    prompt="Synthesize the following market analyses into a unified dashboard.

Market Status: {market_status from JSON}

# US Market Analysis
{us-market-analyzer output}

# Korean Market Analysis
{kr-market-analyzer output}

# Crypto & Global Macro Analysis
{crypto-macro-analyzer output}

# Technical Analysis                      # 추가
{technical-analyzer output}

Create unified dashboard with: top 3 key takeaways, all market sections including technical analysis, cross-market themes, and disclaimer."
)
```
```

---

### Task 11: pandas-ta 의존성 추가 및 테스트
**예상 시간**: 1-2시간

**설치**:
```bash
pip3 install pandas-ta
```

**버전 확인**:
```bash
python3 -c "import pandas_ta as ta; print(f'pandas-ta version: {ta.__version__}')"
```

**기능 테스트**:
```python
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Test data
ticker = yf.Ticker("^GSPC")
df = ticker.history(period="60d")

# Test RSI
rsi = ta.rsi(df['Close'], length=14)
print(f"Latest RSI: {rsi.iloc[-1]:.2f}")

# Test MACD
macd = ta.macd(df['Close'])
print(f"MACD: {macd['MACD_12_26_9'].iloc[-1]:.2f}")

# Test SMA
sma_20 = ta.sma(df['Close'], length=20)
print(f"SMA 20: {sma_20.iloc[-1]:.2f}")

# Test Bollinger Bands
bbands = ta.bbands(df['Close'], length=20)
print(f"BB Upper: {bbands['BBU_20_2.0'].iloc[-1]:.2f}")
```

**SKILL.md에 의존성 섹션 업데이트**:
```markdown
## Dependencies

```bash
pip3 install yfinance pykrx pyyaml feedparser pandas-ta
```

**Required Versions**:
- Python 3.8+
- yfinance >= 0.2.0
- pykrx >= 1.0.0
- pandas-ta >= 0.3.14  # 추가
```

---

### Task 12: 전체 파이프라인 통합 테스트
**예상 시간**: 3-5시간

**테스트 시나리오**:

1. **데이터 수집 & DB 저장 테스트**
```bash
# 1. 데이터 수집
cd plugins/market-pulse/config
python3 fetch_market.py --scope overview --output json > /tmp/test_market_data.json

# 2. DB 확인
python3 -c "
from data.market_history import MarketHistoryDB
db = MarketHistoryDB()
hist = db.get_historical_prices('^GSPC', days=60)
print(f'S&P 500 history: {len(hist)} days')
assert len(hist) == 60, 'Expected 60 days of history'
print('✅ DB storage test passed')
"
```

2. **기술 지표 계산 테스트**
```bash
python3 -c "
import json
from analysis.technical_indicators import TechnicalIndicatorCalculator
from data.market_history import MarketHistoryDB

db = MarketHistoryDB()
df = db.get_historical_prices('^GSPC', days=60)

calc = TechnicalIndicatorCalculator()
indicators = calc.calculate_all(df)

print(f'RSI: {indicators[\"rsi\"][\"value\"]} - {indicators[\"rsi\"][\"interpretation\"]}')
print(f'MACD: {indicators[\"macd\"][\"macd_line\"]} / {indicators[\"macd\"][\"signal_line\"]}')
print(f'Trend: {indicators[\"interpretations\"][\"trend\"]}')
print('✅ Technical indicators test passed')
"
```

3. **HTML 대시보드 생성 테스트**
```bash
# 1. HTML 생성
python3 generate_html.py --input /tmp/test_market_data.json --output /tmp/test_dashboard.html

# 2. 차트 렌더링 확인 (브라우저에서 열기)
open /tmp/test_dashboard.html

# 3. 수동 체크리스트:
# [ ] 60일 트렌드 차트가 표시되는가?
# [ ] 섹터 히트맵이 색상으로 표시되는가?
# [ ] RSI 차트에 과매수/과매도 영역이 표시되는가?
# [ ] 교육 툴팁이 마우스 호버 시 나타나는가?
# [ ] 모든 차트가 반응형으로 동작하는가? (브라우저 창 크기 조절 시)
```

4. **에이전트 파이프라인 테스트**
```bash
# market-pulse 스킬 실행
claude-code

# 대화:
User: "market pulse"

# 예상 동작:
# 1. 데이터 수집 (30초)
# 2. Phase 1: 4개 에이전트 병렬 실행 (60초)
#    - us-market-analyzer
#    - kr-market-analyzer
#    - crypto-macro-analyzer
#    - technical-analyzer  # 새로 추가된 에이전트
# 3. Phase 2: market-synthesizer (20초)
# 4. HTML 대시보드 생성 및 자동 열기

# 체크리스트:
# [ ] Technical Analyzer 출력에 RSI/MACD 해석이 포함되는가?
# [ ] 교육 노트가 포함되는가? ("💡 초보자 설명")
# [ ] 투자 신호에 신뢰도(⭐)가 표시되는가?
# [ ] Synthesizer가 Technical Analysis를 통합하는가?
```

5. **회귀 테스트 (기존 기능 확인)**
```bash
# 기존 기능이 여전히 작동하는지 확인

# 1. 한국 시장만 조회
claude-code
User: "한국 시장 어때?"
# [ ] kr-market-analyzer만 실행되는가?

# 2. 워치리스트 조회
User: "워치리스트 보여줘"
# [ ] watchlist 데이터가 표시되는가?

# 3. 섹터 바차트 (기존 차트)
# [ ] 기존 섹터 바차트가 여전히 표시되는가?
```

6. **성능 테스트**
```bash
# 전체 파이프라인 소요 시간 측정
time python3 -c "
import sys
sys.path.insert(0, 'plugins/market-pulse')

from config.fetch_market import MarketDataFetcher
from config.generate_html import generate_html
from analysis.technical_indicators import TechnicalIndicatorCalculator
from data.market_history import MarketHistoryDB

# 1. Data fetching
fetcher = MarketDataFetcher()
data = fetcher.fetch_all(scope='overview')
print('✅ Data fetching done')

# 2. Technical indicators
db = MarketHistoryDB()
calc = TechnicalIndicatorCalculator()
for symbol in ['^GSPC', '^IXIC']:
    df = db.get_historical_prices(symbol, days=60)
    indicators = calc.calculate_all(df)
    data['data']['us_indices'][symbol]['indicators'] = indicators
print('✅ Technical indicators done')

# 3. HTML generation
html_path = generate_html(data, '/tmp/perf_test_dashboard.html')
print(f'✅ HTML generated: {html_path}')
"

# 예상 시간:
# - Data fetching: 30-45초
# - Technical indicators: 5-10초
# - HTML generation: 2-3초
# - Total: ~1분 이내
```

7. **오류 처리 테스트**
```bash
# 1. 네트워크 오류 시뮬레이션 (WiFi 끄기)
python3 fetch_market.py --scope overview
# [ ] 에러 메시지가 명확한가?
# [ ] Partial data로 진행하는가?

# 2. DB 파일 삭제 후 재생성
rm plugins/market-pulse/data/market_history.db
python3 fetch_market.py --scope overview
# [ ] DB가 자동으로 생성되는가?

# 3. 부분 데이터 테스트 (일부 심볼 실패)
# sources.yaml에 존재하지 않는 심볼 추가
# [ ] 에러를 건너뛰고 나머지 데이터는 정상 표시되는가?
```

**검증 완료 기준**:
- [ ] 모든 12개 태스크 코드 구현 완료
- [ ] 60일 히스토리 DB 저장 확인
- [ ] RSI, MACD, 이동평균 계산 정확도 확인 (알려진 값과 비교)
- [ ] 3개 차트 모두 렌더링 확인
- [ ] 교육 툴팁 동작 확인
- [ ] Technical Analyzer 에이전트 출력 품질 확인
- [ ] 전체 파이프라인 1분 내 완료
- [ ] 기존 기능 회귀 없음
- [ ] 모바일 반응형 동작 확인

---

## ⏱️ 타임라인 및 마일스톤

### 주차별 계획 (주 10-15시간 투자 기준)

#### **Week 1: Data Layer (Task 1-2)**
- **Day 1-2**: SQLite 스키마 설계 및 MarketHistoryDB 클래스 구현
- **Day 3-4**: fetch_market.py 수정 (60일 데이터 + DB 저장)
- **Day 5**: 통합 테스트 (데이터 수집 → DB 저장 → 조회)
- **Milestone**: 60일 히스토리가 DB에 저장되고 조회 가능

#### **Week 2: Analysis Layer (Task 3-5)**
- **Day 1-3**: technical_indicators.py 구현 (pandas-ta)
- **Day 4**: educational_content.yaml 작성
- **Day 5-7**: Technical Analyzer 에이전트 구현
- **Milestone**: 기술 지표 계산 및 에이전트 분석 동작

#### **Week 3: Visualization Layer (Task 6-9)**
- **Day 1-2**: 60일 트렌드 차트 구현
- **Day 3**: 섹터 히트맵 구현
- **Day 4**: RSI 차트 구현
- **Day 5-6**: 교육 툴팁 통합
- **Day 7**: HTML 통합 테스트
- **Milestone**: 3개 차트 + 교육 툴팁이 대시보드에 표시

#### **Week 4: Integration & Testing (Task 10-12)**
- **Day 1**: SKILL.md 업데이트
- **Day 2**: pandas-ta 의존성 설정
- **Day 3-5**: 전체 파이프라인 통합 테스트
- **Day 6-7**: 버그 수정 및 성능 최적화
- **Milestone**: Phase 1 MVP 완성 및 출시

### 최소/최대 타임라인
- **최소** (Aggressive): 3주 (주 20시간 투자)
- **권장** (Balanced): 4주 (주 15시간 투자)
- **최대** (Relaxed): 6주 (주 10시간 투자)

---

## ✅ 검증 방법

### 기능 검증
1. **Historical Data**: DB에서 60일 데이터 조회 → 60 rows 반환
2. **Technical Indicators**: RSI 값을 TradingView와 비교 (±2 오차 허용)
3. **Charts**: 브라우저에서 차트 3개 모두 렌더링 확인
4. **Educational Tooltips**: 마우스 호버 시 설명 팝업 확인
5. **Agent Output**: Technical Analyzer가 신뢰도(⭐) 및 교육 노트 포함

### 사용성 검증
- **초보자 테스트**: 투자 경험 없는 사람에게 대시보드 보여주기
  - [ ] RSI가 무엇인지 툴팁만으로 이해하는가?
  - [ ] 차트를 보고 상승/하락 추세를 파악하는가?
  - [ ] 투자 신호를 이해하고 신뢰도를 인지하는가?

### 성능 검증
- 데이터 수집: < 45초
- 기술 지표 계산: < 10초
- HTML 생성: < 3초
- 전체 파이프라인: < 2분

### 코드 품질 검증
- [ ] 모든 함수에 docstring 존재
- [ ] 에러 핸들링 (try-except)
- [ ] Type hints (Python 3.8+)
- [ ] 테스트 스크립트 작성

---

## 🎓 투자 학습 효과 측정

### 학습 지표 (3개월 후)
- **지식**: RSI, MACD, 이동평균의 의미를 설명할 수 있는가?
- **스킬**: 차트만 보고 추세를 판단할 수 있는가?
- **실전**: 과매수/과매도 구간에서 매수/매도를 자제하는가?
- **성과**: 모의 투자 수익률이 시장 대비 우위인가? (S&P 500 대비)

### 사용 패턴 추적
```python
# 사용 로그 추가 (선택 사항)
{
    "date": "2026-02-11",
    "user_viewed": ["trend_chart", "rsi_chart", "sector_heatmap"],
    "tooltips_hovered": ["rsi", "macd", "golden_cross"],
    "time_spent_seconds": 420  # 7분
}
```

---

## 📈 Phase 2 Preview (3-4개월 후)

Phase 1 완성 후, 다음 단계:
- **Fundamental Analysis** (PER, PEG, 부채비율, 성장률)
- **Risk Analysis** (Sharpe Ratio, Max Drawdown, VaR)
- **Sector Rotation** (경기 사이클 기반)
- **UsStockInfo MCP Integration** (재무제표 데이터)

Phase 2 완료 시 → **Stage 4-5 도달** (펀더멘털 + 리스크 관리)

---

## 🚨 리스크 및 완화 방안

| 리스크 | 영향 | 확률 | 완화 방안 |
|-------|------|------|----------|
| pandas-ta 계산 오류 | 잘못된 신호 | 중간 | TradingView 값과 비교 검증 |
| API 속도 제한 (yfinance) | 데이터 누락 | 낮음 | DB 캐싱, 재시도 로직 |
| DB 용량 증가 | 성능 저하 | 낮음 | 1년 롤링윈도우 정책 |
| 차트 렌더링 느림 | 사용성 저하 | 낮음 | 데이터 포인트 제한 (60일) |
| 교육 콘텐츠 부정확 | 잘못된 학습 | 중간 | 금융 전문가 리뷰 |

---

## 📚 참고 자료

### 기술 문서
- [pandas-ta Documentation](https://github.com/twopirllc/pandas-ta)
- [Chart.js Documentation](https://www.chartjs.org/docs/latest/)
- [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- [pykrx Documentation](https://github.com/sharebook-kr/pykrx)

### 투자 학습 자료
- [QuantStart - Beginner's Guide to Quantitative Trading](https://www.quantstart.com/articles/Beginners-Guide-to-Quantitative-Trading/)
- [Investopedia - Technical Indicators](https://www.investopedia.com/technical-analysis-4689657)
- [R을 이용한 퀀트 투자 포트폴리오 만들기](https://hyunyulhenry.github.io/quant_cookbook/)

---

## 🎯 성공 기준

Phase 1 MVP는 다음 조건을 충족 시 성공:
1. **기능**: 12개 태스크 모두 구현 완료
2. **품질**: 기술 지표 정확도 95% 이상 (TradingView 대비)
3. **성능**: 전체 파이프라인 2분 이내 완료
4. **사용성**: 투자 초보자가 10분 안에 핵심 개념 이해
5. **학습 효과**: 3개월 사용 후 Stage 3 도달 (기술 분석 숙련)

---

## 📞 지원 및 피드백

- **버그 리포트**: GitHub Issues
- **기능 제안**: GitHub Discussions
- **문서 개선**: Pull Requests

---

**Last Updated**: 2026-02-11
**Author**: jaykim
**Version**: 1.0
**Status**: Ready for Implementation

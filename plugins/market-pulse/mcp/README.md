# Stock Data MCP Server

yfinance 기반 주식 데이터 제공 MCP 서버

## 📌 개요

Market-Pulse 플러그인을 위한 자체 제작 MCP 서버입니다. yfinance를 활용하여 미국 주식의 펀더멘털, 밸류에이션, 성장률 등 다양한 지표를 제공합니다.

## 🚀 기능

### 제공 데이터

1. **펀더멘털 지표** (`get_fundamental_metrics`)
   - 밸류에이션: PER, PBR, PEG, P/S, EV/EBITDA
   - 수익성: ROE, ROA, 영업이익률, 순이익률
   - 성장률: 매출/이익 성장률, EPS
   - 재무 건전성: 부채비율, 유동비율, 당좌비율
   - 배당: 배당수익률, 배당성향

2. **밸류에이션** (`get_valuation_metrics`)
   - PER, PBR, PEG, P/S, EV/EBITDA, EV/Revenue
   - 시가총액, 기업가치

3. **수익성 지표** (`get_profitability_metrics`)
   - ROE, ROA, 영업이익률, 순이익률, 매출총이익률, EBITDA 마진

4. **성장률** (`get_growth_metrics`)
   - 매출 성장률, 이익 성장률, 분기 이익 성장률
   - 주당 매출, EPS, Forward EPS

5. **재무 건전성** (`get_financial_health`)
   - 부채비율, 유동비율, 당좌비율
   - 총 현금, 총 부채, 잉여현금흐름, 영업현금흐름

6. **배당 정보** (`get_dividend_info`)
   - 배당수익률, 배당성향, 배당률
   - 배당락일, 5년 평균 배당수익률

7. **기업 정보** (`get_company_info`)
   - 회사명, 섹터, 산업, 국가
   - 웹사이트, 사업 요약, 직원 수

8. **가격 데이터** (`get_price_data`)
   - 현재가, 시가, 고가, 저가
   - 52주 최고/최저, 거래량

9. **종합 데이터** (`get_all_metrics`)
   - 위 모든 데이터를 한 번에 조회

## 📦 설치

```bash
# yfinance 설치 (Market-Pulse에 이미 포함됨)
pip install yfinance
```

## 🔧 사용법

### 1. Python 코드에서 사용 (Client 사용)

```python
from mcp.stock_client import StockMCPClient

client = StockMCPClient()

# AAPL 펀더멘털 조회
metrics = client.get_fundamental_metrics("AAPL")
print(f"PER: {metrics['valuation']['per']}")
print(f"ROE: {metrics['profitability']['roe']}%")

# 밸류에이션만 조회
valuation = client.get_valuation_metrics("MSFT")
print(f"PBR: {valuation['pbr']}")

# 모든 지표 조회
all_data = client.get_all_metrics("GOOGL")
```

### 2. 직접 MCP 서버 호출 (고급)

```bash
# 서버 시작
python3 stock_mcp_server.py

# 요청 전송 (stdin으로)
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_fundamental_metrics","arguments":{"ticker":"AAPL"}}}' | python3 stock_mcp_server.py
```

### 3. 테스트

```bash
# MCP 서버 테스트
python3 test_mcp_server.py
```

## 🔗 Claude Code에서 사용

`.mcp.json`에 추가:

```json
{
  "mcpServers": {
    "stock-data": {
      "command": "python3",
      "args": [
        "/Users/jaykim/Documents/Projects/claude-ai-engineering/plugins/market-pulse/mcp/stock_mcp_server.py"
      ]
    }
  }
}
```

## 📊 응답 예시

### get_fundamental_metrics("AAPL")

```json
{
  "ticker": "AAPL",
  "valuation": {
    "per": 29.67,
    "pbr": 45.93,
    "peg": null,
    "ps": 8.12,
    "ev_ebitda": 22.45
  },
  "profitability": {
    "roe": 152.02,
    "roa": 27.65,
    "operating_margin": 31.89,
    "net_margin": 26.44
  },
  "growth": {
    "revenue_growth": 15.7,
    "earnings_growth": 18.3,
    "eps": 7.91
  },
  "financial_health": {
    "debt_to_equity": 102.63,
    "current_ratio": 0.87,
    "quick_ratio": 0.82
  },
  "dividend": {
    "dividend_yield": 0.41,
    "payout_ratio": 14.93
  }
}
```

## 🎯 Market-Pulse 통합

이 MCP 서버는 Market-Pulse의 Phase 2 기능들을 구현하는 데 사용됩니다:

- ✅ **안전마진 계산기**: EPS, 성장률 데이터 제공
- ✅ **PEG 스크리너**: PEG 비율, 성장률 제공
- ✅ **밸류에이션 스크리너**: PER, PBR, ROE, 부채비율 제공
- ✅ **품질 분석**: ROE, 이익률, 재무 건전성 제공
- ✅ **멀티팩터 스코어링**: Value, Quality 팩터 데이터 제공

## ⚠️ 제한 사항

1. **yfinance 의존**: yfinance의 데이터 품질과 속도에 의존
2. **PEG 비율**: yfinance에서 제공하지 않는 경우가 많음 (직접 계산 필요)
3. **실시간성**: 15-20분 지연된 데이터
4. **무료 서비스**: 대량 요청 시 제한 가능

## 🔮 향후 개선

- [ ] PEG 비율 자동 계산 (PER / 성장률)
- [ ] 요청 캐싱 (중복 호출 방지)
- [ ] 배치 조회 (여러 종목 동시 조회)
- [ ] 에러 핸들링 강화
- [ ] 로깅 추가

## 📝 라이선스

MIT License

---

**작성일**: 2026-02-12
**버전**: 1.0.0
**작성자**: Market-Pulse Team

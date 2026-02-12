# Getting Started with Portfolio Analyzer

완전히 구현된 포트폴리오 관리 플러그인 - 5분만에 시작하기!

---

## 📦 설치 완료 상태

✅ **모든 파일 구현 완료** (25개 파일)
✅ **플러그인 등록 완료** (Claude Code에 등록됨)
✅ **즉시 사용 가능** (Python 스크립트)

---

## 🚀 빠른 시작 (3단계)

### 1단계: 의존성 설치

```bash
pip install yfinance pykrx numpy pandas
```

### 2단계: 데이터베이스 초기화

```bash
cd /Users/jaykim/Documents/Projects/claude-ai-engineering/plugins/portfolio-analyzer-fused/scripts
python3 init_portfolio.py
```

**예상 출력**:
```
✅ Database initialized successfully
📍 Location: ../data/portfolio.db
📊 Tables created: holdings, transactions, score_history, chat_history, portfolio_meta
```

### 3단계: 테스트 데이터 추가

```bash
# 애플 10주 매수
python3 add_to_portfolio.py AAPL buy 10 150.00

# 마이크로소프트 5주 매수
python3 add_to_portfolio.py MSFT buy 5 300.00

# 엔비디아 8주 매수
python3 add_to_portfolio.py NVDA buy 8 110.00
```

---

## 🎯 사용 방법

### 방법 1: Python 스크립트 직접 실행 (지금 바로 가능!)

```bash
# 포트폴리오 조회
python3 query_portfolio.py

# 가격 업데이트
python3 update_prices.py

# 주식 점수 계산
python3 calculate_score.py AAPL --save

# 대시보드 생성 (브라우저 자동 오픈)
python3 generate_dashboard.py

# 리스크 분석
python3 calculate_portfolio_metrics.py
```

### 방법 2: Claude Code 명령어 (VSCode 재시작 후)

VSCode를 재시작한 후 Claude 대화창에서:

```
/analyze-stock AAPL
/portfolio-review
/find-opportunities
/portfolio-risk
/portfolio-chat
```

또는 자연어로:
```
"애플 주식 분석해줘"
"내 포트폴리오 보여줘"
"투자 기회 찾아줘"
"포트폴리오 리스크 체크"
```

---

## 📊 5가지 핵심 기능

### 1. 📈 주식 분석 (analyze-stock)

**목적**: 개별 주식의 종합적인 AI 분석

```bash
# 스크립트로
python3 fetch_stock_data.py AAPL
python3 calculate_score.py AAPL --save

# Claude Code로 (등록 후)
/analyze-stock AAPL
```

**결과**:
- 투자 점수 (0-10점, 등급 A+~D)
- Bull/Bear Case 분석 (Opus AI)
- 투자 의견 (BUY/HOLD/SELL)
- 12개월 목표가
- 포트폴리오 적합도 평가

---

### 2. 📊 포트폴리오 리뷰 (portfolio-review)

**목적**: 전체 포트폴리오 현황 및 대시보드

```bash
# 스크립트로
python3 query_portfolio.py --with-scores
python3 generate_dashboard.py

# Claude Code로 (등록 후)
/portfolio-review
```

**결과**:
- 총 자산 가치 및 P&L
- 섹터별 배분 차트
- 점수 분포 그래프
- 상위 보유 종목
- 인터랙티브 HTML 대시보드

---

### 3. 💡 투자 기회 발견 (find-opportunities)

**목적**: 저평가 주식 및 리밸런싱 제안

```bash
# Claude Code로 (등록 후)
/find-opportunities
```

**결과**:
- 매도 추천 (낮은 점수 종목)
- 섹터 리밸런싱 제안
- 집중도 리스크 경고
- 우선순위별 액션 플랜 (Sonnet AI)

---

### 4. ⚠️ 리스크 분석 (portfolio-risk)

**목적**: 포트폴리오 리스크 평가

```bash
# 스크립트로
python3 calculate_portfolio_metrics.py

# Claude Code로 (등록 후)
/portfolio-risk
```

**결과**:
- 베타 (시장 대비 변동성)
- 포트폴리오 변동성
- 집중도 분석 (최대 포지션, 상위 3개)
- 시나리오 분석 (Sonnet AI)
- 리스크 완화 방안

---

### 5. 💬 AI 포트폴리오 상담 (portfolio-chat)

**목적**: 대화형 투자 조언

```bash
# Claude Code로 (등록 후)
/portfolio-chat
```

**대화 예시**:
```
"내 포트폴리오 어때?"
"MSFT 팔아야 할까?"
"리밸런싱 해야 하나?"
"베타가 뭐야?"
"금리 인하가 내 포트폴리오에 미치는 영향은?"
```

**특징**:
- Opus AI 어드바이저 (고품질 추론)
- 다회차 대화 지원
- 개인화된 조언 (보유 종목 참조)
- 교육적 설명

---

## 🎨 커스터마이징

### 목표 배분 설정

`config/portfolio.yaml` 편집:

```yaml
allocation:
  sectors:
    Technology: 30    # 목표 비율
    Healthcare: 15
    Finance: 15
    Consumer: 15
    Industrial: 10
    Energy: 10
    Other: 5

risk:
  max_position_size: 10      # 단일 종목 최대 비중
  max_sector_weight: 35      # 단일 섹터 최대 비중
```

### 점수 가중치 조정

`config/scoring.yaml` 편집:

```yaml
weights:
  financial_health: 0.40    # 재무 건전성
  valuation: 0.35           # 밸류에이션
  momentum: 0.25            # 모멘텀
```

---

## 📁 파일 구조

```
portfolio-analyzer-fused/
├── scripts/              # 9개 Python 스크립트
│   ├── init_portfolio.py
│   ├── query_portfolio.py
│   ├── fetch_stock_data.py
│   ├── add_to_portfolio.py
│   ├── delete_holding.py
│   ├── update_prices.py
│   ├── calculate_score.py
│   ├── calculate_portfolio_metrics.py
│   └── generate_dashboard.py
│
├── agents/               # 6개 AI 에이전트
│   ├── strategic-advisor.md (Opus)
│   ├── portfolio-advisor.md (Opus)
│   ├── market-analyst.md (Sonnet)
│   ├── opportunity-scanner.md (Sonnet)
│   ├── risk-assessor.md (Sonnet)
│   └── data-manager.md (Sonnet)
│
├── skills/
│   └── portfolio-analyzer/
│       └── SKILL.md      # 560줄 오케스트레이션
│
├── config/               # 설정 파일
│   ├── portfolio.yaml
│   ├── scoring.yaml
│   └── schema.sql
│
├── data/                 # 생성됨
│   ├── portfolio.db
│   └── portfolio_dashboard.html
│
└── templates/
    └── dashboard.html
```

---

## 🔍 트러블슈팅

### 문제: "Database not found"
```bash
python3 scripts/init_portfolio.py
```

### 문제: "yfinance not installed"
```bash
pip install yfinance pykrx numpy pandas
```

### 문제: 플러그인 명령어 작동 안 함
1. VSCode 완전 재시작 (Cmd + Q)
2. 플러그인 등록 확인:
   ```bash
   cat ~/.claude/plugins/config.json
   ```

### 문제: 점수 계산 실패
- 티커 심볼 확인 (대문자로)
- 인터넷 연결 확인
- 데이터 부족 시 다른 주식 시도

---

## 💡 유용한 팁

1. **정기적 업데이트**: 분석 전 항상 `update_prices.py` 실행
2. **점수 저장**: `--save` 플래그로 추이 추적
3. **대시보드 활용**: 시각화로 빠른 이해
4. **대화 활용**: 복잡한 결정은 `/portfolio-chat`로 논의
5. **리밸런싱**: 5% 이상 drift 시 리밸런싱 고려

---

## 📚 추가 문서

- **[README.md](README.md)** - 전체 기능 설명
- **[FUSION_IMPLEMENTATION_GUIDE.md](FUSION_IMPLEMENTATION_GUIDE.md)** - 구현 가이드
- **[CHANGELOG.md](CHANGELOG.md)** - 변경 이력
- **[Test Report](../../tempo/competitive-agents/portfolio-analyzer/COMPETITIVE_AGENTS_TEST_REPORT.md)** - 테스트 리포트

---

## ⚠️ 법적 고지

이 도구는 **정보 제공 목적**으로만 제공되며 투자 자문, 재무 자문 또는 매매 권유가 아닙니다. 모든 투자 결정은 본인의 책임입니다. 투자 전 반드시 전문 재무 자문가와 상담하세요.

---

## 🎉 준비 완료!

이제 시작할 준비가 되었습니다:

1. ✅ 의존성 설치
2. ✅ 데이터베이스 초기화
3. ✅ 테스트 데이터 추가
4. 🚀 **분석 시작!**

질문이 있으시면 언제든 물어보세요! 💬

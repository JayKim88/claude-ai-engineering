# Market-Pulse Architecture

**Version**: 2.0.0
**Last Updated**: 2026-02-12

---

## 📊 시스템 아키텍처

### 전체 프로세스 플로우

```mermaid
flowchart TD
    Start([사용자 요청]) --> Trigger{트리거 분석}

    Trigger -->|시장 분석| Market[Market Overview]
    Trigger -->|가치투자 분석| Value[Value Investing]
    Trigger -->|워치리스트| Watchlist[Watchlist Display]

    Market --> Deps[의존성 체크<br/>yfinance, pykrx]
    Value --> Deps
    Watchlist --> Deps

    Deps --> Fetch[데이터 수집<br/>fetch_market.py]

    Fetch --> Scope{Scope 분기}

    Scope -->|overview/deep| MultiAgent[Multi-Agent Pipeline]
    Scope -->|us/kr/crypto| SingleAgent[Single Agent]
    Scope -->|watchlist| DisplayWatch[워치리스트 표시]
    Scope -->|value| ValueAnalysis[가치투자 분석]

    MultiAgent --> Phase1[Phase 1: Parallel<br/>3 Agents 동시 실행]
    Phase1 --> USAgent[US Market Analyzer]
    Phase1 --> KRAgent[KR Market Analyzer]
    Phase1 --> MacroAgent[Crypto-Macro Analyzer]

    USAgent --> Phase2[Phase 2: Synthesis]
    KRAgent --> Phase2
    MacroAgent --> Phase2

    Phase2 --> Synthesizer[Market Synthesizer<br/>종합 대시보드]

    SingleAgent --> Display[분석 결과 표시]
    Synthesizer --> Display

    ValueAnalysis --> ValueType{분석 타입}

    ValueType -->|safety_margin| Graham[안전마진 계산기<br/>intrinsic_value.py]
    ValueType -->|garp| Lynch[PEG 스크리너<br/>lynch_screener.py]
    ValueType -->|deep| DeepDive[8가지 관점 분석<br/>company_deep_dive.py]
    ValueType -->|all| AllAnalysis[통합 분석기<br/>value_investing_analyzer.py]

    Graham --> ValueDisplay[가치투자 결과 표시]
    Lynch --> ValueDisplay
    DeepDive --> ValueDisplay
    AllAnalysis --> ValueDisplay

    Display --> HTML[HTML 대시보드 생성<br/>generate_html.py]
    DisplayWatch --> HTML
    ValueDisplay --> ValueTable[Markdown 테이블]

    HTML --> Browser[브라우저 자동 오픈]
    ValueTable --> FollowUp{후속 작업?}
    Browser --> FollowUp

    FollowUp -->|추가 분석| Start
    FollowUp -->|종료| End([완료])

    style Market fill:#e1f5ff
    style Value fill:#fff4e1
    style MultiAgent fill:#e8f5e9
    style ValueAnalysis fill:#fff3e0
    style DeepDive fill:#fce4ec
```

---

## 🏗️ 시스템 컴포넌트

### 1. Data Layer (데이터 계층)

```mermaid
graph LR
    subgraph "Data Sources"
        YF[Yahoo Finance<br/>yfinance]
        KRX[한국거래소<br/>pykrx]
        RSS[RSS Feeds<br/>feedparser]
    end

    subgraph "Data Storage"
        DB[(Market History DB<br/>SQLite)]
        Cache[MCP Cache]
    end

    subgraph "Data Providers"
        MCP[Stock MCP Server<br/>9 Tools]
        Fetcher[Market Data Fetcher<br/>fetch_market.py]
    end

    YF --> Fetcher
    YF --> MCP
    KRX --> Fetcher
    RSS --> Fetcher

    Fetcher --> DB
    MCP --> Cache

    DB --> Analysis[Analysis Layer]
    Cache --> Analysis
```

---

### 2. Analysis Layer (분석 계층)

```mermaid
graph TD
    subgraph "Market Analysis"
        USA[US Market Analyzer<br/>Agent]
        KRA[KR Market Analyzer<br/>Agent]
        MAC[Crypto-Macro Analyzer<br/>Agent]
        SYN[Market Synthesizer<br/>Agent]
    end

    subgraph "Value Investing Analysis"
        GRA[Graham Calculator<br/>intrinsic_value.py]
        LYN[Lynch Screener<br/>lynch_screener.py]
        DEEP[Deep Dive Analyzer<br/>company_deep_dive.py]

        subgraph "Deep Dive Components"
            BUF[Buffett Moat]
            MUN[Munger Risk]
            ASS[Asness Factors]
            DAL[Dalio Cycle]
            FIS[Fisher Scuttlebutt]
        end
    end

    USA --> SYN
    KRA --> SYN
    MAC --> SYN

    GRA --> INT[Integrated Analyzer]
    LYN --> INT
    DEEP --> INT

    BUF --> DEEP
    MUN --> DEEP
    ASS --> DEEP
    DAL --> DEEP
    FIS --> DEEP
```

---

### 3. Presentation Layer (표현 계층)

```mermaid
graph LR
    subgraph "Output Formats"
        HTML[HTML Dashboard<br/>Chart.js]
        JSON[JSON Export]
        MD[Markdown Tables]
        CLI[CLI Output]
    end

    subgraph "Visualization"
        CHART[Interactive Charts]
        TABLE[Data Tables]
        CARD[Info Cards]
    end

    HTML --> CHART
    HTML --> TABLE
    HTML --> CARD

    JSON --> Export[File Export]
    MD --> Console[Terminal Display]
    CLI --> Console
```

---

## 🔄 Multi-Agent Execution Flow

### Phase 1: Parallel Analysis (병렬 분석)

```mermaid
sequenceDiagram
    participant User
    participant Skill as Market-Pulse Skill
    participant Fetcher as Data Fetcher
    participant US as US Agent
    participant KR as KR Agent
    participant Macro as Macro Agent

    User->>Skill: "시장 분석해줘"
    Skill->>Fetcher: fetch_all(scope="overview")
    Fetcher-->>Skill: market_data.json

    par Parallel Execution
        Skill->>US: Analyze US Market
        Skill->>KR: Analyze KR Market
        Skill->>Macro: Analyze Crypto/Macro
    end

    US-->>Skill: US Analysis
    KR-->>Skill: KR Analysis
    Macro-->>Skill: Macro Analysis

    Note over Skill: All 3 agents run<br/>simultaneously
```

### Phase 2: Synthesis (종합)

```mermaid
sequenceDiagram
    participant Skill
    participant Synth as Synthesizer Agent
    participant HTML as HTML Generator
    participant Browser

    Skill->>Synth: Synthesize<br/>(US + KR + Macro)
    Synth-->>Skill: Unified Dashboard

    Skill->>HTML: generate_html(data)
    HTML-->>Skill: dashboard.html

    Skill->>Browser: open(dashboard.html)
    Browser-->>User: Interactive Dashboard
```

---

## 💎 Value Investing Analysis Flow

### Integrated Analysis Pipeline

```mermaid
flowchart TD
    Start([가치투자 분석 요청]) --> Input[티커 입력<br/>AAPL,MSFT,GOOGL]

    Input --> Type{분석 타입}

    Type -->|Safety Margin| SM[안전마진 계산]
    Type -->|GARP| GARP[PEG 스크리닝]
    Type -->|Deep Dive| DD[심층 분석]
    Type -->|All| ALL[모두 실행]

    SM --> MCP[Stock MCP Server<br/>데이터 수집]
    GARP --> MCP
    DD --> MCP
    ALL --> MCP

    MCP --> SMCalc[Graham Formula<br/>IV = EPS × (8.5 + 2g)]
    MCP --> PEGCalc[PEG Calculation<br/>PER / Growth]
    MCP --> Multi[8-Perspective Analysis]

    SMCalc --> Filter1[Filter: 안전마진 20%+]
    PEGCalc --> Filter2[Filter: PEG < 1.0]
    Multi --> Score[Overall Score 0-100]

    Filter1 --> Output[결과 출력]
    Filter2 --> Output
    Score --> Output

    Output --> Table[Markdown Table]
    Output --> JSON[JSON Export]

    Table --> User([사용자])
    JSON --> User

    style Start fill:#fff4e1
    style MCP fill:#e3f2fd
    style Multi fill:#fce4ec
    style Output fill:#e8f5e9
```

### Deep Dive Multi-Perspective Analysis

```mermaid
graph TD
    Ticker[Ticker: AAPL] --> Data[Stock MCP<br/>Fundamental Data]

    Data --> P1[1. Graham<br/>안전마진 22.8%]
    Data --> P2[2. Buffett<br/>해자 100/100]
    Data --> P3[3. Lynch<br/>PEG 1.62]
    Data --> P4[4. Munger<br/>리스크 15/100]
    Data --> P5[5. Asness<br/>팩터 27.5/100]
    Data --> P6[6. Dalio<br/>사이클 중기확장]
    Data --> P7[7. Fisher<br/>질적분석 75/100]

    P1 --> Synthesis[종합 평가]
    P2 --> Synthesis
    P3 --> Synthesis
    P4 --> Synthesis
    P5 --> Synthesis
    P6 --> Synthesis
    P7 --> Synthesis

    Synthesis --> Score[Overall Score<br/>69.3/100]
    Synthesis --> RR[Risk-Reward<br/>1.52]
    Synthesis --> Rec[추천: 조건부 매수]
    Synthesis --> Horizon[투자기간: 1-3년]

    Score --> Report[Comprehensive Report]
    RR --> Report
    Rec --> Report
    Horizon --> Report

    style Data fill:#e3f2fd
    style Synthesis fill:#fff3e0
    style Report fill:#e8f5e9
```

---

## 🗂️ File Structure & Dependencies

```mermaid
graph TD
    subgraph "Configuration"
        YAML[sources.yaml<br/>watchlist.yaml]
        MCP_JSON[.mcp.json]
    end

    subgraph "Data Scripts"
        FETCH[fetch_market.py<br/>869 lines]
        DB[market_history.py<br/>SQLite]
    end

    subgraph "MCP Server"
        SERVER[stock_mcp_server.py<br/>540 lines]
        CLIENT[stock_client.py<br/>233 lines]
    end

    subgraph "Analysis Tools"
        IV[intrinsic_value.py<br/>400+ lines]
        LY[lynch_screener.py<br/>600+ lines]
        DD[company_deep_dive.py<br/>700+ lines]
        VA[value_investing_analyzer.py<br/>300+ lines]
    end

    subgraph "Output Generators"
        HTML[generate_html.py]
        SKILL[SKILL.md v2.0]
    end

    YAML --> FETCH
    MCP_JSON --> SERVER

    FETCH --> DB
    SERVER --> CLIENT

    CLIENT --> IV
    CLIENT --> LY
    CLIENT --> DD

    IV --> VA
    LY --> VA
    DD --> VA

    FETCH --> HTML
    VA --> SKILL

    style FETCH fill:#e1f5ff
    style SERVER fill:#e3f2fd
    style VA fill:#fff4e1
    style HTML fill:#e8f5e9
```

---

## 📈 Data Flow Diagram

### Market Overview Data Flow

```mermaid
flowchart LR
    subgraph "External Sources"
        YF[Yahoo Finance API]
        KRX[KRX API]
        RSS[RSS Feeds]
    end

    subgraph "Data Collection"
        FETCH[fetch_market.py]
        DB[(SQLite DB<br/>60 days history)]
    end

    subgraph "Processing"
        AGENT1[US Analyzer]
        AGENT2[KR Analyzer]
        AGENT3[Macro Analyzer]
        SYNTH[Synthesizer]
    end

    subgraph "Output"
        JSON[market_data.json]
        HTML[dashboard.html]
    end

    YF -->|REST API| FETCH
    KRX -->|pykrx| FETCH
    RSS -->|feedparser| FETCH

    FETCH --> DB
    FETCH --> JSON

    JSON --> AGENT1
    JSON --> AGENT2
    JSON --> AGENT3

    AGENT1 --> SYNTH
    AGENT2 --> SYNTH
    AGENT3 --> SYNTH

    SYNTH --> HTML

    style FETCH fill:#e3f2fd
    style SYNTH fill:#fff3e0
    style HTML fill:#e8f5e9
```

### Value Investing Data Flow

```mermaid
flowchart LR
    subgraph "Data Source"
        YF[yfinance API]
    end

    subgraph "MCP Layer"
        MCP[Stock MCP Server<br/>9 Tools]
        CACHE[MCP Cache]
    end

    subgraph "Analysis Tools"
        GRAHAM[Graham Calculator]
        LYNCH[Lynch Screener]
        DEEP[Deep Dive]
    end

    subgraph "Output"
        TABLE[Markdown Tables]
        JSON_OUT[JSON Files]
    end

    YF -->|Fundamental Data| MCP
    MCP --> CACHE

    CACHE --> GRAHAM
    CACHE --> LYNCH
    CACHE --> DEEP

    GRAHAM --> TABLE
    LYNCH --> TABLE
    DEEP --> TABLE

    TABLE --> JSON_OUT

    style MCP fill:#e3f2fd
    style DEEP fill:#fce4ec
    style JSON_OUT fill:#e8f5e9
```

---

## 🎯 Decision Tree: Scope Selection

```mermaid
graph TD
    Request[사용자 요청] --> Parse{트리거 문구 분석}

    Parse -->|시장 분석<br/>market overview| OVERVIEW[Scope: overview]
    Parse -->|미국 시장| US[Scope: us]
    Parse -->|한국 시장| KR[Scope: kr]
    Parse -->|크립토| CRYPTO[Scope: crypto]
    Parse -->|워치리스트| WATCH[Scope: watchlist]
    Parse -->|가치투자 분석<br/>안전마진<br/>PEG 스크리닝| VALUE[Scope: value]
    Parse -->|딥 다이브| DEEP[Scope: deep]

    OVERVIEW --> MultiAgent[Multi-Agent<br/>3 Agents Parallel]
    US --> SingleUS[Single Agent<br/>US Only]
    KR --> SingleKR[Single Agent<br/>KR Only]
    CRYPTO --> SingleCrypto[Single Agent<br/>Crypto/Macro]
    WATCH --> DisplayWatch[Display Only<br/>No Agents]
    VALUE --> ValueAnalysis[Value Analysis<br/>CLI Tools]
    DEEP --> MultiAgentDeep[Multi-Agent<br/>+ Watchlist + News]

    style Parse fill:#fff4e1
    style MultiAgent fill:#e8f5e9
    style ValueAnalysis fill:#fce4ec
```

---

## ⚙️ Technology Stack

```mermaid
graph TB
    subgraph "Backend"
        Python[Python 3.11+]
        YF[yfinance]
        KRX_LIB[pykrx]
        YAML_LIB[PyYAML]
        FEED[feedparser]
    end

    subgraph "Data Storage"
        SQLite[SQLite 3]
        JSON_STORE[JSON Files]
    end

    subgraph "AI/Agent"
        Claude[Claude Sonnet 4.5]
        MCP_PROTO[MCP Protocol]
        Multi_Agent[Multi-Agent System]
    end

    subgraph "Frontend"
        HTML5[HTML5]
        CSS3[CSS3<br/>FT Style]
        ChartJS[Chart.js 4.4]
    end

    Python --> YF
    Python --> KRX_LIB
    Python --> YAML_LIB
    Python --> FEED

    Python --> SQLite
    Python --> JSON_STORE

    Claude --> Multi_Agent
    Python --> MCP_PROTO

    Python --> HTML5
    HTML5 --> CSS3
    HTML5 --> ChartJS

    style Python fill:#3776ab,color:#fff
    style Claude fill:#6b46c1,color:#fff
    style ChartJS fill:#ff6384,color:#fff
```

---

## 📊 Performance Metrics

| Component | Execution Time | Notes |
|-----------|----------------|-------|
| Data Fetching | 15-45 seconds | Depends on scope |
| Phase 1 (3 Agents Parallel) | 30-60 seconds | Concurrent execution |
| Phase 2 (Synthesis) | 10-20 seconds | Haiku model |
| HTML Generation | 2-5 seconds | Local processing |
| **Total (Overview)** | **1-2 minutes** | End-to-end |
| Value Analysis (Safety Margin) | 10-20 seconds | Per 10 stocks |
| Value Analysis (GARP) | 10-20 seconds | Per 10 stocks |
| Deep Dive (Single Stock) | 15-30 seconds | 8 perspectives |

---

## 🔐 Security & Data Privacy

- ✅ **No Authentication Required**: Uses free public APIs only
- ✅ **Local Storage**: All data stored locally (SQLite, JSON files)
- ✅ **No External Tracking**: No analytics or telemetry
- ✅ **Open Source**: Fully auditable code
- ⚠️ **API Rate Limits**: Respects yfinance and pykrx rate limits
- ⚠️ **Delayed Data**: 15-20 minute delay (free tier limitation)

---

## 📝 Version History

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| **1.0.0** | 2026-01-15 | MVP: Multi-agent market analysis, HTML dashboard |
| **1.5.0** | 2026-02-01 | Phase 1: SQLite DB, 60-day history, technical indicators |
| **2.0.0** | 2026-02-12 | Phase 2.5: Value investing (Graham, Lynch, 8-perspective) |

---

## 🔮 Roadmap

### Phase 3: Advanced Analytics (Q2 2026)
- [ ] Backtesting engine
- [ ] Portfolio tracking
- [ ] Alert system
- [ ] ML-based predictions

### Phase 4: Monetization (Q3 2026)
- [ ] REST API for external integration
- [ ] Pro tier ($9.99/month)
- [ ] Enterprise features
- [ ] Community marketplace

---

**문서 작성일**: 2026-02-12
**작성자**: Market-Pulse Team
**버전**: 2.0.0

---
name: market-research-methods
description: TAM/SAM/SOM calculation frameworks, Korean data sources, WebSearch query patterns
version: 1.0.0
---

# Market Research Methods

## Market Sizing Framework

### TAM (Total Addressable Market) - Top-Down
**Formula:** `Total population × % target demographic × avg. spending per capita`

**Example (온라인 학습):**
- Korea population: 51M
- Target (20-40 age): 35% = 17.85M
- Avg. online edu spending: 50,000 KRW/year
- **TAM = 892B KRW**

### SAM (Serviceable Addressable Market) - Bottom-Up
**Formula:** `Number of potential customers × avg. revenue per customer`

**Example:**
- Potential customers (직장인 + 대학생): 5M
- Revenue per customer: 180,000 KRW/year
- **SAM = 900B KRW**

### SOM (Serviceable Obtainable Market)
**Formula:** `SAM × realistic market share (1-5% typical for new entrant)`

**Example:**
- SAM: 900B KRW
- Market share assumption: 3% by year 3
- **SOM = 27B KRW**

## Data Sources

### Korea-Specific
| Source | URL Pattern | Data Type |
|--------|-------------|-----------|
| 통계청 KOSIS | kosis.kr | 인구, 소비, 산업 통계 |
| 중소벤처기업부 | mss.go.kr | 창업, 중소기업 현황 |
| 산업통상자원부 | motie.go.kr | 산업 동향, 수출입 |
| 한국인터넷진흥원 (KISA) | kisa.or.kr | 디지털/인터넷 시장 |
| 금융감독원 전자공시 | dart.fss.or.kr | 상장사 재무제표 |

### Global Sources
| Source | Type | Access |
|--------|------|--------|
| Statista | Market reports | Partial free |
| IBISWorld | Industry analysis | Paid (use snippets) |
| Crunchbase | Startup funding | Limited free |
| CB Insights | Tech trends | Email-gated reports |
| Google Trends | Search volume | Free |

## WebSearch Query Patterns

### Market Size Queries
```
"{desire category} market size Korea 2024"
"{industry} TAM SAM SOM analysis"
"한국 {산업} 시장 규모 통계청"
"{category} revenue forecast statista"
```

### Trend Queries
```
"{industry} trends 2024 2025"
"{category} growth drivers headwinds"
"한국 {산업} 성장률 전망"
"{technology} adoption rate report"
```

### Competitor Queries
```
"top {category} platforms Korea"
"{industry} competitive landscape analysis"
"한국 {카테고리} 서비스 비교"
"{competitor name} revenue pricing model"
```

## Validation Heuristics

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| Source diversity | ≥2 sources | Flag as "low confidence" |
| TAM/SAM ratio | SAM = 10-30% of TAM | Recalculate SAM |
| SOM feasibility | SOM < 10% of SAM | Adjust market share assumption |
| Year-over-year growth | <50% CAGR | Accept; >50% = verify hype cycle |

## Proxy Market Technique

When direct data unavailable:

1. **Japan proxy:** Korea ≈ 60% of Japan market size (similar culture, smaller pop)
2. **US proxy:** Korea ≈ 8% of US market (tech adoption parity)
3. **Adjacent category:** Use similar market + adjustment factor

**Example:** No data on "AI 글쓰기 도구" → Use "온라인 편집 도구" × 0.3 (penetration rate)

---
name: market-research-by-desire
description: Start desire-based market research with guided interview
version: 1.0.0
---

# /market-research-by-desire

Initiates the 3-round interview and 5-agent market research pipeline.

## Usage

```
/market-research-by-desire
```

Or use trigger phrases:
- English: "market research by desire", "desire research"
- Korean: "욕망 기반 시장조사", "욕망 리서치", "욕망에서 시장 찾기"

## What Happens

1. **Round 1:** Select desire category (생존과안전, 성장과성취, etc.)
2. **Round 2:** Select sub-category (전문성개발, 재정안정, etc.)
3. **Round 3:** Provide context (target market, solo-dev preference, budget, industry)
4. **Phase 1 (Parallel):** desire-cartographer + market-trend-researcher analyze desire structure and market trends
5. **Phase 2 (Sequential):** competitive-scanner → gap-opportunity-analyzer map competitive landscape
6. **Phase 3 (Solo):** revenue-model-architect designs 3-5 revenue models
7. **Output:** 3 documents generated in `~/.market-research-by-desire/projects/{slug}/`

## Output Files

- `market-analysis.md`: Market size, trends, desire mapping
- `competitive-analysis.md`: Competitor SWOT, gaps, positioning
- `revenue-model-draft.md`: Revenue models, unit economics, recommendations

## Estimated Time

12-18 minutes

## Cost Estimate

$1-2 USD (depends on WebSearch volume)

## Configuration

Edit `config/settings.yaml` to adjust:
- Search result limits
- Output language (Korean/English)
- Timeout per agent
- Fallback data sources

## Troubleshooting

- **No market data found:** Plugin uses proxy markets and estimates
- **Few/no competitors:** Marked as "blue ocean", includes validation guidance
- **WebSearch quota exceeded:** Falls back to cached examples from knowledge base

---
name: opportunity-assessment
description: Gap analysis framework, desire intersection opportunities, solo-dev feasibility filter
version: 1.0.0
---

# Opportunity Assessment

## Gap Analysis Framework

### Gap Types
| Type | Definition | Detection Method |
|------|------------|------------------|
| **Feature gap** | Desired feature absent in all competitors | User reviews + desire-map intersection |
| **Pricing gap** | Underserved price segment | Pricing analysis (e.g., no $10-20 tier) |
| **Segment gap** | Demographic/psychographic ignored | Market trends vs. competitor targeting |
| **Experience gap** | Poor UX despite feature parity | Low ratings + complaint analysis |
| **Desire gap** | Core desire unaddressed | Desire-map Level 3 vs. competitor value props |

### Gap Scoring
**Attractiveness Score (1-10):**
- Market size potential (30%): How many users affected?
- Competitor difficulty (20%): How hard to fill gap?
- Monetization clarity (25%): Clear willingness to pay?
- Desire intensity (25%): How painful is the unmet need?

**Example:**
- Gap: "No AI-driven personalized learning paths for busy professionals"
- Market size: 7 (15% of SAM)
- Difficulty: 8 (requires ML, data)
- Monetization: 9 (premium feature, clear value)
- Intensity: 8 (high frustration in reviews)
- **Score: 8.05**

## Desire Intersection Opportunities

### Why Intersections Matter
Single-desire solutions = commoditized. Intersections = unique positioning.

**Example:**
- 성장과성취 alone → 온라인 강의 (crowded)
- 성장과성취 + 연결과소속 → 학습 커뮤니티 + 경쟁 (스터디 매칭, 챌린지) = differentiated

### Intersection Discovery Process
1. Read desire-map.json → primary + secondary desires
2. Check competitive-landscape.json → do competitors combine both?
3. If NO combination exists → flag as high-opportunity intersection
4. If YES but poorly executed → flag as "improvement opportunity"

### High-Potential Intersections (Pre-Validated)
| Intersection | Market Evidence | Opportunity |
|--------------|-----------------|-------------|
| 성장 + 연결 | 프립, 탈잉, 스터디파이 | Community learning, peer accountability |
| 성장 + 즐거움 | Duolingo, 챌린저스 | Gamified skill-building |
| 자유 + 재정안정 | 토스, 뱅크샐러드 | Automated wealth management |
| 연결 + 즐거움 | 당근마켓 모임 | Hobby-based social networks |
| 건강 + 즐거움 | 링피트, 닌텐도 스위치 스포츠 | Fitness gaming |

## Solo-Dev Feasibility Filter

### Scoring Criteria (1-10 scale)
| Factor | Weight | High Score (8-10) | Low Score (1-3) |
|--------|--------|-------------------|-----------------|
| **Tech complexity** | 25% | CRUD, API integration | ML training, real-time video |
| **Ops overhead** | 30% | Fully automated | Needs moderation, manual ops |
| **Content requirements** | 20% | User-generated | High editorial/production |
| **Distribution** | 15% | Organic (SEO, community) | Paid ads, partnerships |
| **Support burden** | 10% | Self-serve, docs | High-touch onboarding |

### Feasibility Tiers
- **8-10:** Ideal for solo dev (SaaS tools, info products, niche marketplaces)
- **5-7:** Possible with automation (community platforms, curated content)
- **1-4:** Requires team (two-sided marketplaces, operations-heavy)

### Auto-Disqualifiers for Solo Dev
- Two-sided marketplace requiring liquidity
- Physical inventory
- 24/7 customer support (unless fully automated)
- Heavy regulatory compliance (fintech, healthtech)

## Go/No-Go Decision Matrix

| Criterion | Threshold | Weight |
|-----------|-----------|--------|
| Market size (SOM) | >500M KRW (year 3) | 20% |
| Gap attractiveness | >7.0 | 25% |
| Competitive intensity | <7 direct competitors | 15% |
| Solo-dev feasibility | >6.0 (if solo-dev preferred) | 20% |
| Desire intensity | >6.0 | 20% |

**Weighted score >7.0 = GO**
**Score 5-7 = GO WITH CAUTION (validate first)**
**Score <5 = NO-GO (pivot or abandon)**

## Validation Experiments (Before Full Build)

| Gap Type | Validation Method | Success Metric |
|----------|-------------------|----------------|
| Feature gap | Landing page + waitlist | 100 emails in 2 weeks |
| Pricing gap | Pre-sale (50% discount) | 10 paying customers |
| Segment gap | 20 user interviews | 60% confirm pain point |
| Desire intersection | MVP (single intersection) | 30% retention week 2 |

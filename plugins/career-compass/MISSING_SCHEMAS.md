# Career Compass - Missing Data Schemas

> **Purpose**: 이 파일은 PLANNING.md에서 누락된 TypeScript 인터페이스를 정의합니다.
> **Status**: PLANNING.md 개선 시 통합 필요

---

## Phase 1 Results

### Resume Analysis Result

```typescript
interface ResumeAnalysisResult {
  total_years: number
  domains: Record<string, number> // { "frontend": 4, "ai_ml": 2 }

  skills: {
    expert: string[]      // 5+ years or primary expertise
    advanced: string[]    // 2-5 years
    learning: string[]    // < 2 years or actively learning
  }

  strengths: string[]     // Top 5 skills
  weaknesses: string[]    // Missing critical skills

  transition_pattern: string // e.g., "Frontend → AI Product Engineer"

  career_highlights: {
    title: string
    company: string
    duration_months: number
    key_achievements: string[]
  }[]

  metadata: {
    analyzed_at: string   // ISO timestamp
    profile_source: string // path to profile.yaml
    confidence: number    // 0-100
  }
}
```

---

### JD Market Analysis Result

```typescript
interface JDMarketAnalysisResult {
  total_jds_analyzed: number

  top_demanded_skills: {
    skill: string
    frequency: number     // How many JDs mentioned this
    avg_priority: number  // 1-5 (required vs nice-to-have)
  }[]

  matched_skills: string[]  // User's skills found in JDs
  gap_skills: string[]      // Missing skills

  market_trends: {
    trend: string           // e.g., "AI/ML demand +35% YoY"
    data_source: string     // e.g., "100 JDs from LinkedIn"
    confidence: number      // 0-100
  }[]

  common_requirements: {
    category: string        // "Education", "Experience", "Tech Stack"
    items: string[]
  }[]

  metadata: {
    analyzed_at: string
    jds_source: string      // path to jds.json
    date_range: string      // "2026-01 to 2026-02"
  }
}
```

---

### Career Trend Research Result

```typescript
interface CareerTrendResearchResult {
  transition_cases: {
    id: string
    from_role: string
    to_role: string
    duration_months: number

    key_skills_learned: string[]
    learning_path: string     // e.g., "Bootcamp → Side projects → Job"

    success_factors: string[]
    challenges: string[]

    source: {
      url: string
      type: "blog" | "interview" | "case_study"
      credibility: number     // 0-100
    }
  }[]

  learning_resources: {
    title: string
    url: string
    type: "course" | "tutorial" | "book" | "bootcamp"
    estimated_hours: number
    cost_usd: number
    rating: number            // 0-5
  }[]

  industry_insights: {
    insight: string           // e.g., "FastAPI replacing Flask in 2026"
    relevance: number         // 0-100
    source: string
  }[]

  metadata: {
    searched_at: string
    search_queries: string[]
    sources_count: number
  }
}
```

---

## Phase 2 Results

### Skill Gap Analysis Result

```typescript
interface SkillGapAnalysisResult {
  critical_gaps: {
    skill: string
    reason: string            // Why it's critical
    difficulty: number        // 1-5 (1=easy, 5=hard)
    demand_score: number      // 0-100 (from JD analysis)
    learning_hours: number    // Estimated hours to learn
    roi_score: number         // demand / (difficulty * hours)
  }[]

  nice_to_have_gaps: {
    skill: string
    benefit: string
    priority: number          // 1-5
  }[]

  learning_priority: string[] // Ordered list of skills to learn

  quick_wins: {
    skill: string
    reason: string            // "High demand + Low difficulty"
    estimated_weeks: number
  }[]

  metadata: {
    phase1_inputs: {
      resume_analysis: boolean
      jd_market_analysis: boolean
      career_trend_research: boolean
    }
    confidence: number
  }
}
```

---

### Career Path Option

```typescript
interface CareerPathOption {
  id: string                  // "path-1", "path-2", etc.
  title: string               // "Direct AI Engineer Transition"

  from_role: string
  to_role: string

  steps: {
    phase: number             // 1, 2, 3, etc.
    title: string
    skills_to_learn: string[]
    duration_weeks: number
    milestones: string[]
  }[]

  total_duration_months: number

  success_probability: number // 0-100
  difficulty: number          // 1-5

  pros: string[]
  cons: string[]

  prerequisites: {
    skill: string
    current_level: "none" | "basic" | "intermediate"
    required_level: "basic" | "intermediate" | "advanced"
  }[]

  risks: {
    risk: string
    likelihood: "low" | "medium" | "high"
    mitigation: string
  }[]

  metadata: {
    generated_by: string      // "claude-opus-4-5"
    generated_at: string
    creativity_score: number  // How creative/unconventional this path is
  }
}
```

---

### Salary Projection Result

```typescript
interface SalaryProjectionResult {
  path_projections: {
    path_id: string

    current_salary: {
      median_usd: number
      range_usd: [number, number]
      source: string
    }

    target_salary: {
      median_usd: number
      range_usd: [number, number]
      timeframe_months: number  // When to expect this
      source: string
    }

    salary_increase: {
      absolute_usd: number
      percentage: number
    }

    roi_analysis: {
      learning_cost_usd: number     // Courses, bootcamps
      opportunity_cost_usd: number  // Lost income during learning
      total_investment_usd: number

      payback_period_months: number // When investment is recovered
      roi_5year_usd: number         // Total gain over 5 years
      roi_rating: "low" | "medium" | "high" | "very_high"
    }

    regional_comparison: {
      region: string
      median_usd: number
      cost_of_living_index: number
      adjusted_value: number        // Salary / COL
    }[]
  }[]

  metadata: {
    data_sources: string[]
    reliability: number           // 0-100
    last_updated: string
    region_focus: string          // "US", "Korea", "Global"
  }
}
```

---

## Phase 3 Outputs

### Learning Roadmap

```typescript
interface LearningRoadmap {
  path_id: string
  path_title: string

  overview: {
    total_duration_months: number
    total_learning_hours: number
    weekly_commitment_hours: number
    difficulty: number            // 1-5
  }

  phases: {
    phase_number: number
    title: string
    duration_weeks: number

    weeks: {
      week_number: number
      focus: string

      learning_tasks: {
        task: string
        type: "course" | "practice" | "project" | "reading"
        estimated_hours: number
        resources: {
          title: string
          url: string
          cost_usd: number
        }[]
      }[]

      milestones: {
        milestone: string
        validation: string          // How to verify completion
      }[]

      deliverables: string[]
    }[]
  }[]

  portfolio_projects: {
    title: string
    description: string
    skills_demonstrated: string[]
    estimated_hours: number
    priority: number                // 1-5
    why_important: string
  }[]

  checkpoints: {
    month: number
    goals: string[]
    success_criteria: string[]
  }[]

  metadata: {
    generated_at: string
    based_on_path: string
    customized_for: string          // User name
  }
}
```

---

### Career Strategy Report

```typescript
interface CareerStrategyReport {
  executive_summary: {
    current_state: string
    target_state: string
    recommended_path: string
    timeline: string
    confidence: number              // 0-100
  }

  weekly_actions: {
    week: number
    priority_actions: {
      action: string
      category: "learning" | "networking" | "portfolio" | "job_search"
      estimated_hours: number
      why_important: string
    }[]
  }[]

  monthly_milestones: {
    month: number
    milestone: string
    success_criteria: string[]
    deliverables: string[]
  }[]

  networking_strategy: {
    target_people: string[]         // e.g., "AI Engineers at FAANG"
    platforms: string[]             // "LinkedIn", "Twitter", "Conferences"
    messaging_templates: {
      scenario: string
      template: string
    }[]
    weekly_goals: string[]
  }

  portfolio_strategy: {
    must_have_projects: {
      title: string
      why_critical: string
      skills_shown: string[]
      estimated_weeks: number
    }[]

    portfolio_review: {
      current_strength: string
      gaps: string[]
      improvement_actions: string[]
    }
  }

  risk_management: {
    risk: string
    likelihood: "low" | "medium" | "high"
    impact: "low" | "medium" | "high"
    mitigation_strategy: string
    contingency_plan: string
  }[]

  market_positioning: {
    unique_value_proposition: string
    target_companies: string[]
    competitive_advantages: string[]
    areas_to_develop: string[]
  }

  success_metrics: {
    metric: string
    current_value: string
    target_value: string
    measurement_frequency: string
  }[]

  metadata: {
    generated_at: string
    generated_by: string            // "claude-opus-4-5"
    inputs_used: string[]
  }
}
```

---

## Validation Functions (Required)

```typescript
// Phase 1 → Phase 2 validation
function validatePhase1Results(
  resume: ResumeAnalysisResult,
  jdMarket: JDMarketAnalysisResult,
  careerTrend: CareerTrendResearchResult
): { valid: boolean; errors: string[] } {
  const errors: string[] = []

  // Resume validation
  if (resume.total_years < 1) {
    errors.push("Resume analysis: insufficient career history")
  }

  if (resume.strengths.length < 3) {
    errors.push("Resume analysis: too few strengths identified")
  }

  // JD Market validation
  if (jdMarket.total_jds_analyzed < 10) {
    errors.push("JD Market: insufficient data (need 10+ JDs)")
  }

  if (jdMarket.top_demanded_skills.length < 5) {
    errors.push("JD Market: insufficient skill data")
  }

  // Career Trend validation
  if (careerTrend.transition_cases.length < 2) {
    errors.push("Career Trend: too few transition cases (need 2+)")
  }

  return {
    valid: errors.length === 0,
    errors
  }
}

// Phase 2 → User Selection validation
function validateCareerPaths(
  paths: CareerPathOption[]
): { valid: boolean; errors: string[] } {
  const errors: string[] = []

  if (paths.length < 2) {
    errors.push("Need at least 2 path options")
  }

  if (paths.length > 5) {
    errors.push("Too many paths (max 5 for user clarity)")
  }

  const lowSuccessPaths = paths.filter(p => p.success_probability < 30)
  if (lowSuccessPaths.length === paths.length) {
    errors.push("All paths have low success probability (<30%)")
  }

  return {
    valid: errors.length === 0,
    errors
  }
}
```

---

## Integration with jd-analyzer

```typescript
// jds.json schema (from jd-analyzer)
interface JDDocument {
  id: string
  title: string
  company: string
  location: string
  posted_date: string
  url: string

  extracted_skills: {
    skill: string
    category: "required" | "preferred" | "mentioned"
    confidence: number
  }[]

  requirements: {
    type: "education" | "experience" | "skill" | "other"
    text: string
  }[]
}

// matches.json schema
interface MatchResult {
  jd_id: string
  jd_title: string
  company: string

  match_score: number               // 0-100

  matched_skills: string[]
  missing_skills: string[]

  recommendation: "strong" | "medium" | "weak" | "skip"
}

// How career-compass uses jd-analyzer data
function loadJDAnalyzerData(jdsPath: string, matchesPath: string): {
  jds: JDDocument[]
  matches: MatchResult[]
} {
  // Read files
  const jds = JSON.parse(fs.readFileSync(jdsPath, 'utf-8'))
  const matches = JSON.parse(fs.readFileSync(matchesPath, 'utf-8'))

  return { jds, matches }
}
```

---

## Next Steps for PLANNING.md

1. ✅ Copy relevant schemas into PLANNING.md
2. ✅ Add "Data Schemas" section after "Agent 상세 설계"
3. ✅ Add "Validation" section before "Performance 예상"
4. ✅ Add "jd-analyzer Integration" section
5. ✅ Reference these schemas in agent specs

---

Generated: 2026-02-14
Purpose: Supplement PLANNING.md with missing implementation details

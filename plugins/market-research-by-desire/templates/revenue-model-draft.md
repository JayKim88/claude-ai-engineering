# 수익 모델 설계서

**프로젝트:** {project_name}  
**작성일:** {date}  
**분석 모델 수:** {model_count}

---

## 1. Executive Summary

### 권장 모델
- **모델명:** {recommended_model_name}
- **Year 3 예상 매출:** {recommended_revenue} {currency}
- **솔로 개발 적합도:** {solo_dev_score}/10
- **핵심 근거:** {recommendation_rationale}

### 시장 맥락
- **가격 민감도:** {price_sensitivity}
- **지불 의사 (Willingness to Pay):** {wtp}
- **경쟁사 평균 가격:** {competitor_avg_price} {currency}

---

## 2. Revenue Model Options

{revenue_models_details}

---

## 3. 모델 비교 매트릭스

| 모델명 | Year 3 매출 | LTV/CAC | Gross Margin | 솔로 적합도 | 리스크 수준 | 추천도 |
|--------|------------|---------|--------------|------------|------------|--------|
{comparison_matrix_table}

---

## 4. 가격 벤치마크

### 시장: {market_category}

| 경쟁사 | 가격 Tier | 가격 ({currency}) | 타겟 세그먼트 | 비고 |
|--------|-----------|---------------------|--------------|------|
{pricing_benchmarks_table}

### 가격 포지셔닝 권장사항
{pricing_positioning_recommendation}

---

## 5. Unit Economics 상세

### CAC (Customer Acquisition Cost) 구성
{cac_breakdown}

### LTV (Lifetime Value) 계산
```
LTV = ARPU × Gross Margin × (1 / Churn Rate)
    = {arpu} × {gross_margin} × (1 / {churn_rate})
    = {ltv} {currency}
```

### Break-Even Analysis
- **고정비 (월):** {fixed_cost_monthly} {currency}
- **변동비율:** {variable_cost_rate}%
- **손익분기 사용자 수:** {breakeven_users}
- **손익분기 시점:** {breakeven_timeline}

---

## 6. 리스크 평가

| 리스크 유형 | 설명 | 가능성 | 영향도 | 완화 전략 |
|------------|------|--------|--------|----------|
{risk_assessment_table}

---

## 7. 권장 모델 상세

### 모델: {recommended_model_name}

#### 선정 이유
{recommendation_detailed_rationale}

#### Go-to-Market 전략
{gtm_strategy_list}

#### 검증 마일스톤
| Milestone | 목표 | 기한 | 성공 기준 |
|-----------|------|------|----------|
{validation_milestones_table}

#### 확장 경로 (Scaling Path)
{scaling_path_list}

---

## 8. 민감도 분석

### 핵심 변수 영향도
| 변수 | 기준값 | -20% 시나리오 | +20% 시나리오 | 영향도 |
|------|--------|--------------|--------------|--------|
{sensitivity_analysis_table}

---

## 9. 실행 체크리스트

### Phase 1: 검증 (1-3개월)
{phase1_checklist}

### Phase 2: MVP (3-6개월)
{phase2_checklist}

### Phase 3: 확장 (6-12개월)
{phase3_checklist}

---

**작성자:** Claude Code - Market Research by Desire Plugin  
**재검토 주기:** {review_frequency}  
**다음 업데이트:** {next_update_date}

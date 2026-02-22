# Unit Economics: {{PROJECT_NAME}}

**Version:** {{VERSION}}
**Date:** {{DATE}}
**Finance Lead:** {{FINANCE_LEAD}}

---

## Customer Acquisition Cost (CAC)

### CAC Breakdown

| Channel | Cost | Customers Acquired | CAC |
|---------|------|---------------------|-----|
| {{CHANNEL_1}} | {{CHANNEL_1_COST}} | {{CHANNEL_1_CUSTOMERS}} | {{CHANNEL_1_CAC}} |
| {{CHANNEL_2}} | {{CHANNEL_2_COST}} | {{CHANNEL_2_CUSTOMERS}} | {{CHANNEL_2_CAC}} |
| {{CHANNEL_3}} | {{CHANNEL_3_COST}} | {{CHANNEL_3_CUSTOMERS}} | {{CHANNEL_3_CAC}} |
| {{CHANNEL_4}} | {{CHANNEL_4_COST}} | {{CHANNEL_4_CUSTOMERS}} | {{CHANNEL_4_CAC}} |
| **Total/Average** | {{TOTAL_COST}} | {{TOTAL_CUSTOMERS}} | {{AVG_CAC}} |

### CAC Formula

```
CAC = (Total Sales & Marketing Expenses) / (Number of New Customers Acquired)
```

**Current Blended CAC:** {{CURRENT_CAC}}
**Target CAC:** {{TARGET_CAC}}

---

## Lifetime Value (LTV)

### LTV Calculation

**Formula:**
```
LTV = (ARPU × Gross Margin %) / Churn Rate
```

**Variables:**
- ARPU: {{ARPU}}
- Gross Margin: {{GROSS_MARGIN}}%
- Monthly Churn Rate: {{CHURN_RATE}}%

**Calculated LTV:** {{CALCULATED_LTV}}

---

### LTV by Tier

| Tier | ARPU | Churn Rate | Avg Lifetime (months) | LTV |
|------|------|------------|----------------------|-----|
| {{TIER_1}} | {{T1_ARPU}} | {{T1_CHURN}}% | {{T1_LIFETIME}} | {{T1_LTV}} |
| {{TIER_2}} | {{T2_ARPU}} | {{T2_CHURN}}% | {{T2_LIFETIME}} | {{T2_LTV}} |
| {{TIER_3}} | {{T3_ARPU}} | {{T3_CHURN}}% | {{T3_LIFETIME}} | {{T3_LTV}} |
| **Weighted Avg** | {{AVG_ARPU}} | {{AVG_CHURN}}% | {{AVG_LIFETIME}} | {{AVG_LTV}} |

---

## LTV:CAC Ratio

**Current Ratio:** {{CURRENT_LTV_CAC_RATIO}}:1
**Target Ratio:** {{TARGET_LTV_CAC_RATIO}}:1

**Interpretation:**
{{LTV_CAC_INTERPRETATION}}

**Benchmark:**
- < 1:1 = {{BENCHMARK_LESS_THAN_1}}
- 1:1 - 3:1 = {{BENCHMARK_1_TO_3}}
- 3:1 - 5:1 = {{BENCHMARK_3_TO_5}}
- > 5:1 = {{BENCHMARK_GREATER_THAN_5}}

---

## Payback Period

**Formula:**
```
Payback Period = CAC / (ARPU × Gross Margin %)
```

**Current Payback Period:** {{CURRENT_PAYBACK}} months
**Target Payback Period:** {{TARGET_PAYBACK}} months

**By Tier:**

| Tier | CAC | Monthly Margin | Payback Period |
|------|-----|----------------|----------------|
| {{TIER_1}} | {{T1_CAC}} | {{T1_MONTHLY_MARGIN}} | {{T1_PAYBACK}} months |
| {{TIER_2}} | {{T2_CAC}} | {{T2_MONTHLY_MARGIN}} | {{T2_PAYBACK}} months |
| {{TIER_3}} | {{T3_CAC}} | {{T3_MONTHLY_MARGIN}} | {{T3_PAYBACK}} months |

---

## Gross Margin

**Revenue per Customer:** {{REVENUE_PER_CUSTOMER}}

**Direct Costs per Customer:**
- {{DIRECT_COST_1}}: {{DC_1_AMOUNT}}
- {{DIRECT_COST_2}}: {{DC_2_AMOUNT}}
- {{DIRECT_COST_3}}: {{DC_3_AMOUNT}}
- {{DIRECT_COST_4}}: {{DC_4_AMOUNT}}
- **Total Direct Costs:** {{TOTAL_DIRECT_COSTS}}

**Gross Profit per Customer:** {{GROSS_PROFIT_PER_CUSTOMER}}
**Gross Margin %:** {{GROSS_MARGIN_PERCENT}}%

---

## Contribution Margin

**Revenue per Customer:** {{REVENUE_PER_CUSTOMER}}

**Variable Costs:**
- Direct Costs: {{VARIABLE_DIRECT_COSTS}}
- Support Costs: {{VARIABLE_SUPPORT_COSTS}}
- Transaction Fees: {{VARIABLE_TRANSACTION_FEES}}
- Other Variable: {{VARIABLE_OTHER}}
- **Total Variable Costs:** {{TOTAL_VARIABLE_COSTS}}

**Contribution Margin:** {{CONTRIBUTION_MARGIN}}
**Contribution Margin %:** {{CONTRIBUTION_MARGIN_PERCENT}}%

---

## Key Assumptions

### Revenue Assumptions

- **ARPU Growth:** {{ARPU_GROWTH_ASSUMPTION}}
- **Customer Growth:** {{CUSTOMER_GROWTH_ASSUMPTION}}
- **Conversion Rate:** {{CONVERSION_RATE_ASSUMPTION}}
- **Upgrade Rate:** {{UPGRADE_RATE_ASSUMPTION}}

### Cost Assumptions

- **CAC Trend:** {{CAC_TREND_ASSUMPTION}}
- **Gross Margin Trend:** {{GM_TREND_ASSUMPTION}}
- **Churn Rate Trend:** {{CHURN_TREND_ASSUMPTION}}
- **Support Cost per Customer:** {{SUPPORT_COST_ASSUMPTION}}

### Market Assumptions

- **Market Size:** {{MARKET_SIZE_ASSUMPTION}}
- **Penetration Rate:** {{PENETRATION_RATE_ASSUMPTION}}
- **Competitive Landscape:** {{COMPETITIVE_ASSUMPTION}}

---

## Sensitivity Analysis

### LTV Sensitivity to Churn Rate

| Churn Rate | LTV | LTV:CAC Ratio |
|------------|-----|---------------|
| {{CHURN_SCENARIO_1}}% | {{LTV_SCENARIO_1}} | {{RATIO_SCENARIO_1}}:1 |
| {{CHURN_SCENARIO_2}}% | {{LTV_SCENARIO_2}} | {{RATIO_SCENARIO_2}}:1 |
| {{CHURN_SCENARIO_3}}% (Current) | {{LTV_SCENARIO_3}} | {{RATIO_SCENARIO_3}}:1 |
| {{CHURN_SCENARIO_4}}% | {{LTV_SCENARIO_4}} | {{RATIO_SCENARIO_4}}:1 |
| {{CHURN_SCENARIO_5}}% | {{LTV_SCENARIO_5}} | {{RATIO_SCENARIO_5}}:1 |

### LTV Sensitivity to ARPU

| ARPU | LTV | LTV:CAC Ratio |
|------|-----|---------------|
| {{ARPU_SCENARIO_1}} | {{LTV_ARPU_1}} | {{RATIO_ARPU_1}}:1 |
| {{ARPU_SCENARIO_2}} | {{LTV_ARPU_2}} | {{RATIO_ARPU_2}}:1 |
| {{ARPU_SCENARIO_3}} (Current) | {{LTV_ARPU_3}} | {{RATIO_ARPU_3}}:1 |
| {{ARPU_SCENARIO_4}} | {{LTV_ARPU_4}} | {{RATIO_ARPU_4}}:1 |
| {{ARPU_SCENARIO_5}} | {{LTV_ARPU_5}} | {{RATIO_ARPU_5}}:1 |

---

## Cohort Analysis

### Month 1 Cohort

| Month | Customers Remaining | Revenue | Cumulative Revenue | Cumulative Margin |
|-------|---------------------|---------|-------------------|-------------------|
| M1 | {{M1_C1_CUSTOMERS}} | {{M1_C1_REVENUE}} | {{M1_C1_CUM_REV}} | {{M1_C1_CUM_MARGIN}} |
| M2 | {{M2_C1_CUSTOMERS}} | {{M2_C1_REVENUE}} | {{M2_C1_CUM_REV}} | {{M2_C1_CUM_MARGIN}} |
| M3 | {{M3_C1_CUSTOMERS}} | {{M3_C1_REVENUE}} | {{M3_C1_CUM_REV}} | {{M3_C1_CUM_MARGIN}} |
| M6 | {{M6_C1_CUSTOMERS}} | {{M6_C1_REVENUE}} | {{M6_C1_CUM_REV}} | {{M6_C1_CUM_MARGIN}} |
| M12 | {{M12_C1_CUSTOMERS}} | {{M12_C1_REVENUE}} | {{M12_C1_CUM_REV}} | {{M12_C1_CUM_MARGIN}} |

---

## Optimization Opportunities

### Increase LTV

1. **{{LTV_OPP_1}}**
   Impact: {{LTV_OPP_1_IMPACT}}
   Effort: {{LTV_OPP_1_EFFORT}}

2. **{{LTV_OPP_2}}**
   Impact: {{LTV_OPP_2_IMPACT}}
   Effort: {{LTV_OPP_2_EFFORT}}

3. **{{LTV_OPP_3}}**
   Impact: {{LTV_OPP_3_IMPACT}}
   Effort: {{LTV_OPP_3_EFFORT}}

### Decrease CAC

1. **{{CAC_OPP_1}}**
   Impact: {{CAC_OPP_1_IMPACT}}
   Effort: {{CAC_OPP_1_EFFORT}}

2. **{{CAC_OPP_2}}**
   Impact: {{CAC_OPP_2_IMPACT}}
   Effort: {{CAC_OPP_2_EFFORT}}

3. **{{CAC_OPP_3}}**
   Impact: {{CAC_OPP_3_IMPACT}}
   Effort: {{CAC_OPP_3_EFFORT}}

---

## Monitoring & KPIs

**Weekly Metrics:**
- New Customers
- CAC (7-day rolling average)
- ARPU
- Churn Rate

**Monthly Metrics:**
- LTV
- LTV:CAC Ratio
- Payback Period
- Cohort Retention

**Quarterly Metrics:**
- Unit Economics by Channel
- Gross Margin Trend
- Contribution Margin Trend

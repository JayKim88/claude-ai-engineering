# analyze-stock

Deep-dive stock analysis with comprehensive scorecard

## Trigger

When the user says:
- "analyze TICKER"
- "analyze stock TICKER"
- "/analyze-stock TICKER"
- "give me analysis of TICKER"
- "score TICKER"
- "evaluate TICKER stock"

## Description

Performs comprehensive stock analysis including:
- Financial health scoring (profitability, growth, stability)
- Valuation analysis (P/E, P/B vs sector/historical)
- Technical momentum indicators (MA, RSI, MACD)
- Overall investment grade (A+ to D)

## Instructions

When triggered:

1. **Parse ticker symbol** from user input (e.g., "analyze AAPL" → "AAPL")

2. **Run scorecard analysis**:
   ```bash
   cd plugins/investment-analyzer/scripts
   python3 scorecard.py TICKER
   ```

3. **Display results** to the user with the formatted scorecard output

4. **Provide context**:
   - Explain what the scores mean
   - Highlight strengths and weaknesses
   - Note any data limitations (if financial metrics are 0%)

5. **Offer next steps**:
   - Add to portfolio: `python3 portfolio_manager.py add TICKER SHARES PRICE`
   - Compare with other stocks
   - View portfolio: `python3 portfolio_manager.py show`

## Examples

### Example 1: Simple Analysis

**User**: analyze AAPL

**Assistant**:
```
I'll analyze Apple (AAPL) for you.

[Runs scorecard.py AAPL]

Key Insights:
- Overall Score: 7.3/10 (Good, B+ grade)
- Valuation: Trading at a discount to sector average
- Financial Health: Strong debt management (D/E: 102.6)
- Momentum: Neutral technical setup

Would you like to:
- Add AAPL to your portfolio?
- Compare with other tech stocks (MSFT, GOOGL)?
- See your current portfolio?
```

### Example 2: Multiple Stocks

**User**: analyze MSFT and NVDA

**Assistant**:
```
I'll analyze both Microsoft and NVIDIA for you.

[Runs scorecard for MSFT]
[Runs scorecard for NVDA]

Comparison:
- MSFT: 3.9/10 (Poor) - Better valuation but weaker momentum
- NVDA: 6.6/10 (Fair) - Higher valuation premium but stronger fundamentals

Would you like a detailed comparison or to add either to your portfolio?
```

## Notes

- If ticker is invalid, inform user and suggest checking the symbol
- If data is incomplete, explain which metrics are missing
- Always provide actionable next steps
- Keep analysis objective and data-driven

## Related Skills

- portfolio-review: View current holdings
- find-opportunities: Discover investment ideas
- portfolio-chat: Conversational portfolio advisor (Phase 3)

#!/usr/bin/env python3
"""
Test script for fetch_market.py with DB integration
"""

from fetch_market import MarketDataFetcher

print('Testing MarketDataFetcher with DB integration...')
fetcher = MarketDataFetcher()

print('\nFetching US indices (60 days + DB storage)...')
indices = fetcher.fetch_us_indices()
print(f'✅ Fetched {len(indices)} indices')

for symbol, data in list(indices.items())[:2]:
    if 'error' not in data:
        print(f'  {symbol}: {data.get("name")}, ${data.get("value")}, {data.get("change_pct")}%')

# Check DB coverage
if fetcher.db:
    symbol = list(indices.keys())[0]
    coverage = fetcher.db.get_data_coverage(symbol)
    print(f'\n📊 DB Coverage for {symbol}:')
    print(f'  Total records: {coverage.get("count")}')
    print(f'  Date range: {coverage.get("earliest_date")} to {coverage.get("latest_date")}')
    print(f'  Days covered: {coverage.get("days_covered")}')

print('\n✅ Test completed!')

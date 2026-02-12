#!/usr/bin/env python3
"""
Test historical trends in JSON output
"""

from fetch_market import MarketDataFetcher
import json

print('Testing historical trends in fetch_all()...')
fetcher = MarketDataFetcher()

print('\nFetching all data with historical trends...')
data = fetcher.fetch_all(scope="overview")

if "historical_trends" in data["data"]:
    print('✅ Historical trends found in data!')
    trends = data["data"]["historical_trends"]
    print(f'\nSymbols with historical data: {list(trends.keys())}')

    # Check first symbol
    first_symbol = list(trends.keys())[0]
    first_data = trends[first_symbol]
    print(f'\n{first_symbol} historical data:')
    print(f'  Records: {first_data["count"]}')
    print(f'  Date range: {first_data["dates"][0]} to {first_data["dates"][-1]}')
    print(f'  Price range: ${min(first_data["prices"]):.2f} to ${max(first_data["prices"]):.2f}')
    print(f'  First 5 dates: {first_data["dates"][:5]}')
    print(f'  First 5 prices: {[f"${p:.2f}" for p in first_data["prices"][:5]]}')
else:
    print('❌ No historical trends in data')
    print('Available keys:', list(data["data"].keys()))

print('\n✅ Test completed!')

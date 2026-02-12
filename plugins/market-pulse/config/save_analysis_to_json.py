#!/usr/bin/env python3
"""
Save AI analysis results to market data JSON
Usage: python3 save_analysis_to_json.py <json_file> <us_analysis> <kr_analysis> <crypto_analysis> <synthesis>
"""

import json
import sys
from pathlib import Path


def save_analysis(json_path: str, us_market: str, kr_market: str, crypto_macro: str, synthesis: str):
    """Add analysis results to JSON file."""

    # Read existing JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Add analysis section
    data['analysis'] = {
        'us_market': us_market,
        'kr_market': kr_market,
        'crypto_macro': crypto_macro,
        'synthesis': synthesis
    }

    # Save updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Analysis saved to {json_path}")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 save_analysis_to_json.py <json_file> <us_analysis> <kr_analysis> <crypto_analysis> <synthesis>")
        sys.exit(1)

    json_file = sys.argv[1]
    us_analysis = sys.argv[2]
    kr_analysis = sys.argv[3]
    crypto_analysis = sys.argv[4]
    synthesis = sys.argv[5]

    save_analysis(json_file, us_analysis, kr_analysis, crypto_analysis, synthesis)

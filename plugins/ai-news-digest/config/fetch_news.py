#!/usr/bin/env python3
"""
AI News Fetcher
Fetches and scores AI news from RSS feeds
"""

import feedparser
import yaml
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re
from urllib.parse import urlparse
import sys
from pathlib import Path

class AINewsFetcher:
    def __init__(self, config_path: str = None, categories: str = 'all'):
        if config_path is None:
            config_path = Path(__file__).parent / "feeds.yaml"

        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.feeds = []
        for category, feed_list in self.config['feeds'].items():
            self.feeds.extend(feed_list)

        # Filter by category if specified
        if categories != 'all':
            allowed = [c.strip() for c in categories.split(',')]
            self.feeds = [f for f in self.feeds if f['category'] in allowed]

    def fetch_all_feeds(self, days: int = 7) -> List[Dict[str, Any]]:
        """Fetch entries from all feeds within the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        all_entries = []

        for feed_config in self.feeds:
            try:
                # Download RSS content first (feedparser.parse(url) doesn't work reliably)
                import urllib.request
                import ssl

                # Create SSL context that doesn't verify certificates (for development)
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE

                req = urllib.request.Request(
                    feed_config['url'],
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
                    content = response.read()

                # Parse the downloaded content
                feed = feedparser.parse(content)

                for entry in feed.entries:
                    # Parse published date
                    pub_date = self._parse_date(entry)

                    if pub_date and pub_date > cutoff_date:
                        entry_data = {
                            'title': entry.get('title', 'No title'),
                            'link': entry.get('link', ''),
                            'published': pub_date.isoformat(),
                            'summary': self._clean_html(entry.get('summary', entry.get('description', ''))),
                            'source': feed_config['name'],
                            'category': feed_config['category'],
                            'base_weight': feed_config['weight']
                        }
                        all_entries.append(entry_data)
            except Exception as e:
                print(f"Error fetching {feed_config['name']}: {e}", file=sys.stderr)
                continue

        return all_entries

    def _parse_date(self, entry) -> datetime:
        """Parse date from entry"""
        # Try published_parsed first
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                return datetime(*entry.published_parsed[:6])
            except:
                pass

        # Try updated_parsed
        if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            try:
                return datetime(*entry.updated_parsed[:6])
            except:
                pass

        # Default to now
        return datetime.now()

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and clean text"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def score_entry(self, entry: Dict[str, Any]) -> float:
        """Calculate importance score for an entry"""
        score = entry['base_weight']

        # Keyword boosting
        text = (entry['title'] + ' ' + entry['summary']).lower()

        for keyword in self.config['scoring']['keyword_boost']['high_priority']:
            if keyword.lower() in text:
                score += 5

        for keyword in self.config['scoring']['keyword_boost']['medium_priority']:
            if keyword.lower() in text:
                score += 3

        for keyword in self.config['scoring']['keyword_boost']['low_priority']:
            if keyword.lower() in text:
                score += 1

        # Recency boost
        pub_date = datetime.fromisoformat(entry['published'])
        age = datetime.now() - pub_date

        if age < timedelta(days=1):
            score += self.config['scoring']['recency_boost']['last_24h']
        elif age < timedelta(days=2):
            score += self.config['scoring']['recency_boost']['last_48h']
        elif age < timedelta(days=7):
            score += self.config['scoring']['recency_boost']['last_week']

        return score

    def get_top_n(self, entries: List[Dict[str, Any]], n: int = 5) -> List[Dict[str, Any]]:
        """Score and return top N entries"""
        # Add scores
        for entry in entries:
            entry['score'] = self.score_entry(entry)

        # Sort by score (descending)
        sorted_entries = sorted(entries, key=lambda x: x['score'], reverse=True)

        # Return top N
        return sorted_entries[:n]

    def remove_duplicates(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate entries based on title similarity"""
        unique_entries = []
        seen_titles = set()

        for entry in entries:
            # Normalize title for comparison
            normalized_title = re.sub(r'\W+', '', entry['title'].lower())

            if normalized_title not in seen_titles:
                seen_titles.add(normalized_title)
                unique_entries.append(entry)

        return unique_entries

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Fetch AI news from RSS feeds')
    parser.add_argument('--days', type=int, default=7, help='Number of days to look back')
    parser.add_argument('--top', type=int, default=5, help='Number of top items to return')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--category', type=str, default='all',
        help='Comma-separated categories to include (official,research,community,tech_news)')
    parser.add_argument('--output', type=str, default='json', choices=['json', 'text'], help='Output format')

    args = parser.parse_args()

    fetcher = AINewsFetcher(args.config, categories=args.category)

    # Fetch all entries
    entries = fetcher.fetch_all_feeds(days=args.days)

    # Remove duplicates
    entries = fetcher.remove_duplicates(entries)

    # Get top N
    top_entries = fetcher.get_top_n(entries, n=args.top)

    # Output
    if args.output == 'json':
        print(json.dumps(top_entries, indent=2))
    else:
        for i, entry in enumerate(top_entries, 1):
            print(f"\n{i}. {entry['title']}")
            print(f"   Source: {entry['source']} | Score: {entry['score']:.1f}")
            print(f"   Link: {entry['link']}")
            print(f"   Published: {entry['published']}")
            print(f"   Summary: {entry['summary'][:200]}...")

if __name__ == '__main__':
    main()

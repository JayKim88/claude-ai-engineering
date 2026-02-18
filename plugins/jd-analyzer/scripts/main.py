#!/usr/bin/env python3
"""
JD Analyzer - Main Orchestrator

Coordinates JD collection, skill extraction, profile matching, and report generation.
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import logging

from collectors import MarkdownParser, PlaywrightFetcher, URLFetcher
from analyzers import SkillExtractor, ProfileMatcher, TrendAnalyzer
from reporters import MarkdownReportGenerator
from utils import ConfigManager, ensure_dependencies, AskUserQuestion

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JDAnalyzerOrchestrator:
    """Main orchestrator for JD analysis pipeline."""

    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize orchestrator with config directory."""
        self.config_dir = config_dir or Path.home() / ".jd-analyzer"
        self.config_manager = ConfigManager(self.config_dir)

        # Ensure config directory exists
        self.config_manager.ensure_config_directory()

        # Initialize components
        self.skill_extractor = None
        self.profile_matcher = None
        self.trend_analyzer = None
        self.report_generator = None

    def validate_environment(self) -> bool:
        """Validate dependencies and environment setup."""
        logger.info("Validating environment...")

        # Check Python version
        if sys.version_info < (3, 9):
            logger.error("Python 3.9+ required. Current: %s", sys.version)
            return False

        # Check and install dependencies
        try:
            ensure_dependencies()
        except Exception as e:
            logger.error("Dependency check failed: %s", e)
            return False

        logger.info("✓ Environment validated")
        return True

    def load_or_create_profile(self) -> Optional[Dict]:
        """Load user profile or create template."""
        profile_path = self.config_dir / "profile.yaml"

        if not profile_path.exists():
            logger.info("No profile found. Creating template...")
            self.config_manager.create_profile_template()
            print("\n" + "="*60)
            print("Profile template created at:")
            print(f"  {profile_path}")
            print("\nPlease fill in your information and re-run.")
            print("="*60 + "\n")
            return None

        try:
            profile = self.config_manager.load_profile()
            logger.info("✓ Profile loaded: %s", profile.get("personal", {}).get("name", "Unknown"))
            return profile
        except Exception as e:
            logger.error("Failed to load profile: %s", e)
            return None

    def select_mode(self) -> int:
        """Present mode selection menu to user."""
        jds_folder = Path.cwd() / "JDs"
        jd_count = len(list(jds_folder.rglob("*.md"))) if jds_folder.exists() else 0

        menu = f"""
{'='*60}
JD Analyzer - Select Mode
{'='*60}

1. Analyze existing JDs ({jd_count} files in JDs/ folder) - Quick Win!
2. Search new JDs (LinkedIn + Wellfound automation)
3. Add single URL
4. Full analysis of all collected JDs

{'='*60}
"""
        print(menu)

        while True:
            try:
                choice = input("Choice (1-4): ").strip()
                mode = int(choice)
                if 1 <= mode <= 4:
                    return mode
                print("Invalid choice. Please enter 1-4.")
            except (ValueError, KeyboardInterrupt):
                print("\nExiting...")
                sys.exit(0)

    def analyze_existing_jds(self) -> List[Dict]:
        """Parse existing markdown JDs from JDs/ folder."""
        logger.info("Analyzing existing JDs...")

        jds_folder = Path.cwd() / "JDs"
        if not jds_folder.exists():
            logger.error("JDs/ folder not found in current directory")
            return []

        parser = MarkdownParser()
        jds = parser.parse_folder(jds_folder)

        logger.info("✓ Parsed %d JDs", len(jds))
        return jds

    def search_new_jds(self, query: str = "AI Product Engineer remote") -> List[Dict]:
        """Search for new JDs via Playwright automation."""
        logger.info("Searching new JDs with query: %s", query)

        fetcher = PlaywrightFetcher(self.config_dir)

        # LinkedIn collection
        print("\n🔍 Collecting from LinkedIn...")
        linkedin_jds = fetcher.collect_linkedin(query, count=50)
        logger.info("✓ LinkedIn: Collected %d JDs", len(linkedin_jds))

        # Wellfound collection
        print("\n🔍 Collecting from Wellfound...")
        wellfound_jds = fetcher.collect_wellfound(query, count=50)
        logger.info("✓ Wellfound: Collected %d JDs", len(wellfound_jds))

        all_jds = linkedin_jds + wellfound_jds

        # Save to data directory
        self.config_manager.save_jds(all_jds)

        logger.info("✓ Total collected: %d JDs", len(all_jds))
        return all_jds

    def add_single_url(self, url: str) -> Optional[Dict]:
        """Parse single JD URL and add to collection."""
        logger.info("Adding URL: %s", url)

        fetcher = URLFetcher()

        try:
            jd = fetcher.fetch_and_parse(url)

            # Load existing JDs
            existing_jds = self.config_manager.load_jds()
            existing_jds.append(jd)

            # Save updated collection
            self.config_manager.save_jds(existing_jds)

            logger.info("✓ JD added: %s - %s", jd["company"], jd["title"])

            # Ask if user wants to re-analyze
            if AskUserQuestion("Re-analyze all JDs?", default="yes"):
                return self.analyze_all_jds()

            return jd
        except Exception as e:
            logger.error("Failed to add URL: %s", e)
            return None

    def analyze_all_jds(self) -> Dict:
        """Full analysis pipeline on all collected JDs."""
        logger.info("Starting full analysis pipeline...")

        # Load JDs
        jds = self.config_manager.load_jds()
        if not jds:
            logger.warning("No JDs found. Run collection first.")
            return {}

        logger.info("Loaded %d JDs", len(jds))

        # Load profile
        profile = self.config_manager.load_profile()

        # Initialize components
        taxonomy_path = self.config_dir / "skill_taxonomy.yaml"
        self.skill_extractor = SkillExtractor(taxonomy_path)
        self.profile_matcher = ProfileMatcher(profile)
        self.trend_analyzer = TrendAnalyzer()

        # Step 1: Extract skills
        print("\n📊 Extracting skills...")
        for i, jd in enumerate(jds):
            print(f"  Processing JD {i+1}/{len(jds)}...", end='\r')
            jd["skills"] = self.skill_extractor.extract(jd["description"])
        print(f"✓ Extracted skills from {len(jds)} JDs" + " "*20)

        # Step 2: Match profile
        print("\n🎯 Matching profile...")
        matches = []
        for i, jd in enumerate(jds):
            print(f"  Matching JD {i+1}/{len(jds)}...", end='\r')
            match_result = self.profile_matcher.match(jd)
            matches.append(match_result)
        print(f"✓ Matched {len(matches)} JDs" + " "*20)

        # Step 3: Rank companies
        print("\n🏆 Ranking companies...")
        ranked = self.profile_matcher.rank_companies(matches, profile)
        logger.info("✓ Top matches: %d companies", len(ranked))

        # Step 4: Analyze trends
        print("\n📈 Analyzing market trends...")
        trends = self.trend_analyzer.analyze(jds, matches)
        logger.info("✓ Trends computed")

        # Step 5: Generate report
        print("\n📝 Generating report...")
        template_path = Path(__file__).parent.parent / "templates" / "report_template.jinja2"
        self.report_generator = MarkdownReportGenerator(template_path)

        report_data = {
            "jds": jds,
            "matches": matches,
            "ranked": ranked,
            "trends": trends,
            "profile": profile,
        }

        report = self.report_generator.generate(report_data)

        # Save report
        from datetime import date
        report_path = Path.cwd() / f"jd-analysis-report-{date.today()}.md"
        report_path.write_text(report)

        logger.info("✓ Report saved: %s", report_path)

        # Save matches data
        self.config_manager.save_matches(matches)

        print("\n" + "="*60)
        print(f"✅ Analysis complete!")
        print(f"   Report: {report_path}")
        print("="*60 + "\n")

        # Ask if user wants to view report
        if AskUserQuestion("View report now?", default="yes"):
            print("\n" + report)

        return report_data

    def run(self, args: argparse.Namespace):
        """Main entry point."""
        # Validate environment
        if not self.validate_environment():
            sys.exit(1)

        # Load or create profile
        profile = self.load_or_create_profile()
        if not profile:
            sys.exit(0)

        # Determine mode
        if args.mode:
            mode = args.mode
        else:
            mode = self.select_mode()

        # Execute mode
        try:
            if mode == 1:
                jds = self.analyze_existing_jds()
                if jds:
                    self.config_manager.save_jds(jds)
                    self.analyze_all_jds()
            elif mode == 2:
                query = args.query or "AI Product Engineer remote"
                self.search_new_jds(query)
                self.analyze_all_jds()
            elif mode == 3:
                if not args.url:
                    url = input("Enter JD URL: ").strip()
                else:
                    url = args.url
                self.add_single_url(url)
            elif mode == 4:
                self.analyze_all_jds()
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            logger.error("Error during execution: %s", e)
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="JD Analyzer - AI Product Engineer Career Transition Tool"
    )
    parser.add_argument(
        "--mode",
        type=int,
        choices=[1, 2, 3, 4],
        help="Mode: 1=Existing, 2=Search, 3=Add URL, 4=Analyze"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Search query for mode 2 (default: 'AI Product Engineer remote')"
    )
    parser.add_argument(
        "--url",
        type=str,
        help="JD URL for mode 3"
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        help="Config directory (default: ~/.jd-analyzer)"
    )

    args = parser.parse_args()

    # Initialize and run orchestrator
    orchestrator = JDAnalyzerOrchestrator(args.config_dir)
    orchestrator.run(args)


if __name__ == "__main__":
    main()

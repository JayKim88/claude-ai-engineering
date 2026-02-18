"""
Analysis Modules

Provides modular analyzers for JD processing:
- SkillExtractor: spaCy NLP + YAML taxonomy skill extraction
- ProfileMatcher: Weighted scoring (Required: 10pt, Nice-to-have: 3pt)
- TrendAnalyzer: Market trends, skill gaps, statistics
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import Counter, defaultdict

import yaml

# spaCy for NLP
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

logger = logging.getLogger(__name__)


class SkillExtractor:
    """Extract skills using spaCy NLP + YAML taxonomy."""

    REQUIRED_SECTIONS = [
        "requirements", "must have", "required skills",
        "qualifications", "what you need", "required"
    ]

    NICE_TO_HAVE_SECTIONS = [
        "nice to have", "preferred", "bonus", "plus",
        "desired", "optional"
    ]

    def __init__(self, taxonomy_path: Path):
        """Initialize extractor with skill taxonomy."""
        if not SPACY_AVAILABLE:
            logger.warning("spaCy not installed. Using regex-only extraction.")
            self.nlp = None
        else:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.warning("spaCy model not found. Downloading...")
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
                self.nlp = spacy.load("en_core_web_sm")

        # Load taxonomy
        if taxonomy_path.exists():
            self.taxonomy = yaml.safe_load(taxonomy_path.read_text())
        else:
            logger.warning("Taxonomy not found. Using minimal default.")
            self.taxonomy = self._get_default_taxonomy()

    def extract(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills from JD text.

        Returns:
            {
                "required": ["React", "Python"],
                "nice_to_have": ["AWS", "Docker"],
                "by_category": {
                    "frontend": ["React"],
                    "backend": ["Python"],
                    ...
                }
            }
        """
        # Split text into sections
        required_text, nice_text = self._split_by_sections(text)

        # Extract skills
        required_skills = self._extract_skills_from_text(required_text)
        nice_skills = self._extract_skills_from_text(nice_text)

        # Categorize
        by_category = self._categorize_skills(required_skills | nice_skills)

        return {
            "required": sorted(list(required_skills)),
            "nice_to_have": sorted(list(nice_skills)),
            "by_category": by_category,
        }

    def _split_by_sections(self, text: str) -> Tuple[str, str]:
        """Split text into required vs nice-to-have sections."""
        text_lower = text.lower()

        # Find section boundaries
        required_start = 0
        nice_start = len(text)

        for keyword in self.NICE_TO_HAVE_SECTIONS:
            match = re.search(rf"\n##?\s*{keyword}", text_lower)
            if match:
                nice_start = min(nice_start, match.start())

        required_text = text[required_start:nice_start]
        nice_text = text[nice_start:]

        return required_text, nice_text

    def _extract_skills_from_text(self, text: str) -> Set[str]:
        """Extract skills from text using spaCy NLP + taxonomy."""
        skills = set()

        # Lowercase for matching
        text_lower = text.lower()

        # Process with spaCy if available
        doc = None
        entities = set()
        if self.nlp:
            doc = self.nlp(text)
            # Extract entities (ORG, PRODUCT, TECH) that might be skills
            entities = {ent.text.lower() for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT"]}

        # Match against taxonomy keywords + aliases
        for category, config in self.taxonomy.get("categories", {}).items():
            keywords = config.get("keywords", [])
            aliases = config.get("aliases", {})

            for keyword in keywords:
                # Get all variants (keyword + aliases)
                variants = [keyword] + aliases.get(keyword, [])

                for variant in variants:
                    variant_lower = variant.lower()

                    # Method 1: Word boundary regex matching
                    pattern = rf"\b{re.escape(variant_lower)}\b"
                    if re.search(pattern, text_lower):
                        skills.add(keyword)
                        break

                    # Method 2: spaCy entity matching (if available)
                    if doc and variant_lower in entities:
                        skills.add(keyword)
                        break

                    # Method 3: spaCy token-based matching (if available)
                    if doc:
                        for token in doc:
                            if token.text.lower() == variant_lower or token.lemma_.lower() == variant_lower:
                                skills.add(keyword)
                                break

        return skills

    def _categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
        """Categorize skills by taxonomy categories."""
        categorized = defaultdict(list)

        for category, config in self.taxonomy.get("categories", {}).items():
            keywords = config.get("keywords", [])

            for skill in skills:
                if skill in keywords:
                    categorized[category].append(skill)

        return {k: sorted(v) for k, v in categorized.items()}

    def _get_default_taxonomy(self) -> Dict:
        """Get minimal default taxonomy."""
        return {
            "categories": {
                "frontend": {
                    "keywords": ["React", "Vue", "Angular", "TypeScript", "JavaScript"],
                    "aliases": {
                        "React": ["ReactJS", "React.js"],
                        "TypeScript": ["TS"],
                    }
                },
                "backend": {
                    "keywords": ["Python", "Node.js", "Java", "Go", "FastAPI"],
                    "aliases": {
                        "Node.js": ["Node", "NodeJS"],
                    }
                },
                "ai_ml": {
                    "keywords": ["LLM", "Machine Learning", "LangChain", "RAG", "Claude AI"],
                    "aliases": {
                        "LLM": ["Large Language Model", "GPT"],
                    }
                },
            }
        }


class ProfileMatcher:
    """Match user profile against JD requirements with weighted scoring."""

    def __init__(self, profile: Dict):
        """Initialize matcher with user profile."""
        self.profile = profile

        # Flatten user skills (all proficiency levels)
        self.user_skills = self._flatten_skills(profile.get("skills", {}))

    def match(self, jd: Dict) -> Dict:
        """
        Calculate match score for JD.

        Scoring algorithm (per spec):
        - Required skill matched: +10 points
        - Nice-to-have matched: +3 points
        - Score = (earned / total) × 100

        Returns:
            {
                "jd_id": "...",
                "jd_title": "...",
                "jd_company": "...",
                "jd_url": "...",
                "score": 75.5,
                "matched_required": ["React", "Python"],
                "matched_nice": ["AWS"],
                "missing_skills": ["Docker", "GraphQL"],
                "total_points": 53,
                "earned_points": 40,
            }
        """
        jd_skills = jd.get("skills", {})
        required = set(jd_skills.get("required", []))
        nice_to_have = set(jd_skills.get("nice_to_have", []))

        # Calculate total possible points
        total_points = len(required) * 10 + len(nice_to_have) * 3

        if total_points == 0:
            logger.warning("JD has no required/nice-to-have skills: %s", jd.get("title"))
            total_points = 1  # Avoid division by zero

        # Calculate matched skills
        matched_required = required & self.user_skills
        matched_nice = nice_to_have & self.user_skills

        # Calculate earned points
        earned_points = len(matched_required) * 10 + len(matched_nice) * 3

        # Calculate score
        score = (earned_points / total_points) * 100

        # Missing skills
        missing_skills = (required | nice_to_have) - self.user_skills

        return {
            "jd_id": jd.get("id"),
            "jd_title": jd.get("title"),
            "jd_company": jd.get("company"),
            "jd_url": jd.get("url"),
            "jd_remote": jd.get("is_remote"),
            "score": round(score, 1),
            "matched_required": sorted(list(matched_required)),
            "matched_nice": sorted(list(matched_nice)),
            "missing_skills": sorted(list(missing_skills)),
            "total_points": total_points,
            "earned_points": earned_points,
        }

    def rank_companies(self, matches: List[Dict], profile: Dict) -> List[Dict]:
        """
        Rank companies by match score and preferences.

        Filters:
        - Minimum match score (from profile)
        - Remote preference
        - Visa requirement

        Sorting:
        - Match score (descending)
        - Remote availability
        - Posted date
        """
        preferences = profile.get("preferences", {})
        min_score = preferences.get("min_match_score", 70)
        remote_only = preferences.get("remote_only", False)

        # Filter
        filtered = []
        for match in matches:
            # Score filter
            if match["score"] < min_score:
                continue

            # Remote filter
            if remote_only and not match.get("jd_remote", False):
                continue

            filtered.append(match)

        # Sort
        sorted_matches = sorted(
            filtered,
            key=lambda m: (m["score"], m.get("jd_remote", False)),
            reverse=True
        )

        return sorted_matches[:50]  # Top 50

    def _flatten_skills(self, skills: Dict) -> Set[str]:
        """Flatten skills from profile (all proficiency levels)."""
        flattened = set()

        for category, levels in skills.items():
            if not isinstance(levels, dict):
                continue

            for level, skill_list in levels.items():
                if isinstance(skill_list, list):
                    flattened.update(skill_list)

        return flattened


class TrendAnalyzer:
    """Analyze market trends and compute insights."""

    def __init__(self):
        """Initialize analyzer."""
        pass

    def analyze(self, jds: List[Dict], matches: List[Dict]) -> Dict:
        """
        Compute comprehensive market trends.

        Returns:
            {
                "top_skills": [(skill, count, pct)],
                "skills_to_learn": [(skill, count, pct)],
                "remote_stats": {
                    "remote_count": 45,
                    "remote_pct": 45.0,
                    ...
                },
                "match_distribution": {
                    "80-100%": 12,
                    "60-79%": 23,
                    ...
                },
                "platform_distribution": {...},
                "avg_match_score": 67.5,
            }
        """
        # Top skills across all JDs
        all_skills = Counter()
        for jd in jds:
            jd_skills = jd.get("skills", {})
            all_skills.update(jd_skills.get("required", []))
            all_skills.update(jd_skills.get("nice_to_have", []))

        total_jds = len(jds)
        top_skills = [
            (skill, count, round(count / total_jds * 100, 1))
            for skill, count in all_skills.most_common(20)
        ]

        # Skills to learn (missing skills ranked by demand)
        missing_skills = Counter()
        for match in matches:
            missing_skills.update(match.get("missing_skills", []))

        skills_to_learn = [
            (skill, count, round(count / total_jds * 100, 1))
            for skill, count in missing_skills.most_common(5)
        ]

        # Remote stats
        remote_count = sum(1 for jd in jds if jd.get("is_remote", False))
        remote_pct = round(remote_count / total_jds * 100, 1) if total_jds > 0 else 0

        remote_stats = {
            "remote_count": remote_count,
            "remote_pct": remote_pct,
            "onsite_count": total_jds - remote_count,
            "onsite_pct": round(100 - remote_pct, 1),
        }

        # Match distribution
        buckets = {
            "80-100%": 0,
            "60-79%": 0,
            "40-59%": 0,
            "<40%": 0,
        }

        for match in matches:
            score = match.get("score", 0)
            if score >= 80:
                buckets["80-100%"] += 1
            elif score >= 60:
                buckets["60-79%"] += 1
            elif score >= 40:
                buckets["40-59%"] += 1
            else:
                buckets["<40%"] += 1

        # Platform distribution
        platform_counts = Counter(jd.get("platform", "unknown") for jd in jds)

        # Average match score
        avg_score = round(
            sum(m.get("score", 0) for m in matches) / len(matches),
            1
        ) if matches else 0

        return {
            "top_skills": top_skills,
            "skills_to_learn": skills_to_learn,
            "remote_stats": remote_stats,
            "match_distribution": buckets,
            "platform_distribution": dict(platform_counts),
            "avg_match_score": avg_score,
            "total_jds": total_jds,
        }

"""
Utility Functions and Configuration Management

Provides:
- ConfigManager: YAML config handling, profile/taxonomy management
- ensure_dependencies: Dependency validation and auto-installation
- AskUserQuestion: User prompt helper
- Security helpers (Keyring, Fernet)
"""

import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

import yaml

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manage configuration files and data storage."""

    def __init__(self, config_dir: Path):
        """Initialize config manager."""
        self.config_dir = config_dir
        self.data_dir = config_dir / "data"
        self.cookies_dir = config_dir / "cookies"

    def ensure_config_directory(self):
        """Create config directory structure."""
        self.config_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        self.cookies_dir.mkdir(exist_ok=True)

        logger.info("✓ Config directory: %s", self.config_dir)

    def create_profile_template(self):
        """Create profile template YAML."""
        template = {
            "personal": {
                "name": "Your Name",
                "location": "City, Country",
            },
            "experience": {
                "total_years": 0,
                "frontend_years": 0,
                "backend_years": 0,
                "ai_ml_years": 0,
            },
            "skills": {
                "frontend": {
                    "expert": ["React", "TypeScript"],
                    "advanced": ["Next.js"],
                    "learning": ["Vue.js"],
                },
                "backend": {
                    "expert": ["Python"],
                    "advanced": ["FastAPI"],
                    "learning": ["Go"],
                },
                "ai_ml": {
                    "advanced": ["Claude AI", "Prompt Engineering"],
                    "learning": ["LangChain", "RAG"],
                },
                "devops": {
                    "advanced": ["Docker"],
                    "learning": ["Kubernetes"],
                },
                "database": {
                    "advanced": ["PostgreSQL"],
                    "learning": ["Redis"],
                },
                "testing": {
                    "advanced": ["Pytest"],
                    "learning": ["Playwright"],
                },
            },
            "preferences": {
                "remote_only": True,
                "visa_required": False,
                "min_match_score": 70,
            },
        }

        profile_path = self.config_dir / "profile.yaml"
        with open(profile_path, "w") as f:
            yaml.dump(template, f, default_flow_style=False, sort_keys=False)

        logger.info("✓ Profile template created: %s", profile_path)

    def load_profile(self) -> Dict:
        """Load profile YAML."""
        profile_path = self.config_dir / "profile.yaml"

        if not profile_path.exists():
            raise FileNotFoundError(f"Profile not found: {profile_path}")

        try:
            with open(profile_path) as f:
                profile = yaml.safe_load(f)

            # Validate structure
            self._validate_profile(profile)

            return profile
        except yaml.YAMLError as e:
            raise ValueError(f"YAML syntax error in profile: {e}")

    def _validate_profile(self, profile: Dict):
        """Validate profile structure."""
        required_fields = ["personal", "skills", "preferences"]

        for field in required_fields:
            if field not in profile:
                raise ValueError(f"Profile missing required field: {field}")

    def create_skill_taxonomy(self):
        """Create comprehensive skill taxonomy YAML."""
        taxonomy = {
            "categories": {
                "frontend": {
                    "keywords": [
                        "React", "Vue", "Angular", "Svelte", "Next.js", "Nuxt.js",
                        "TypeScript", "JavaScript", "HTML", "CSS", "Tailwind",
                        "Webpack", "Vite", "Redux", "MobX", "Zustand",
                    ],
                    "aliases": {
                        "React": ["ReactJS", "React.js"],
                        "TypeScript": ["TS"],
                        "JavaScript": ["JS"],
                        "Next.js": ["NextJS"],
                    },
                },
                "backend": {
                    "keywords": [
                        "Python", "Node.js", "Java", "Go", "Rust", "C++",
                        "FastAPI", "Flask", "Django", "Express", "NestJS",
                        "Spring Boot", "Ruby on Rails", "GraphQL", "REST API",
                    ],
                    "aliases": {
                        "Node.js": ["Node", "NodeJS"],
                        "Python": ["Py"],
                        "REST API": ["RESTful", "REST"],
                    },
                },
                "ai_ml": {
                    "keywords": [
                        "LLM", "Machine Learning", "Deep Learning", "NLP",
                        "LangChain", "RAG", "Claude AI", "OpenAI", "GPT",
                        "Prompt Engineering", "Fine-tuning", "Vector Database",
                        "TensorFlow", "PyTorch", "scikit-learn", "Hugging Face",
                    ],
                    "aliases": {
                        "LLM": ["Large Language Model", "Language Model"],
                        "NLP": ["Natural Language Processing"],
                        "RAG": ["Retrieval Augmented Generation"],
                        "Claude AI": ["Claude", "Anthropic"],
                    },
                },
                "devops": {
                    "keywords": [
                        "Docker", "Kubernetes", "AWS", "GCP", "Azure",
                        "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI",
                        "Terraform", "Ansible", "Nginx", "Linux", "Bash",
                    ],
                    "aliases": {
                        "Kubernetes": ["K8s"],
                        "AWS": ["Amazon Web Services"],
                        "GCP": ["Google Cloud Platform"],
                    },
                },
                "database": {
                    "keywords": [
                        "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
                        "DynamoDB", "Cassandra", "Neo4j", "SQL", "NoSQL",
                    ],
                    "aliases": {
                        "PostgreSQL": ["Postgres"],
                        "MongoDB": ["Mongo"],
                    },
                },
                "testing": {
                    "keywords": [
                        "Pytest", "Jest", "Mocha", "Cypress", "Playwright",
                        "Selenium", "Unit Testing", "Integration Testing",
                        "E2E Testing", "TDD", "BDD",
                    ],
                    "aliases": {
                        "E2E Testing": ["End-to-End Testing"],
                        "TDD": ["Test-Driven Development"],
                        "BDD": ["Behavior-Driven Development"],
                    },
                },
                "soft_skills": {
                    "keywords": [
                        "Communication", "Leadership", "Team Collaboration",
                        "Problem Solving", "Critical Thinking", "Agile",
                        "Scrum", "Project Management", "Stakeholder Management",
                    ],
                    "aliases": {
                        "Agile": ["Agile Methodology"],
                    },
                },
                "tools": {
                    "keywords": [
                        "Git", "GitHub", "GitLab", "Jira", "Confluence",
                        "Figma", "Postman", "VSCode", "Slack", "Notion",
                    ],
                    "aliases": {
                        "VSCode": ["Visual Studio Code"],
                    },
                },
            }
        }

        taxonomy_path = self.config_dir / "skill_taxonomy.yaml"
        with open(taxonomy_path, "w") as f:
            yaml.dump(taxonomy, f, default_flow_style=False, sort_keys=False)

        logger.info("✓ Skill taxonomy created: %s", taxonomy_path)

    def load_jds(self) -> List[Dict]:
        """Load JDs from data directory."""
        jds_path = self.data_dir / "jds.json"

        if not jds_path.exists():
            return []

        try:
            with open(jds_path) as f:
                jds = json.load(f)
            return jds
        except json.JSONDecodeError as e:
            logger.error("Failed to load JDs: %s", e)
            return []

    def save_jds(self, jds: List[Dict]):
        """Save JDs to data directory."""
        jds_path = self.data_dir / "jds.json"

        with open(jds_path, "w") as f:
            json.dump(jds, f, indent=2)

        logger.info("✓ Saved %d JDs to %s", len(jds), jds_path)

    def save_matches(self, matches: List[Dict]):
        """Save match results to data directory."""
        matches_path = self.data_dir / "matches.json"

        with open(matches_path, "w") as f:
            json.dump(matches, f, indent=2)

        logger.info("✓ Saved %d matches to %s", len(matches), matches_path)


def ensure_dependencies():
    """Validate and auto-install dependencies."""
    logger.info("Checking dependencies...")

    # Check spaCy
    try:
        import spacy
        try:
            spacy.load("en_core_web_sm")
            logger.info("✓ spaCy model ready")
        except OSError:
            logger.info("Downloading spaCy model...")
            import subprocess
            subprocess.run(
                ["python3", "-m", "spacy", "download", "en_core_web_sm"],
                check=True
            )
            logger.info("✓ spaCy model installed")
    except ImportError:
        logger.error("spaCy not installed. Run: pip install spacy")
        raise

    # Check Playwright
    try:
        from playwright.sync_api import sync_playwright

        # Check if browsers installed
        import subprocess
        result = subprocess.run(
            ["python3", "-m", "playwright", "install", "--dry-run", "chromium"],
            capture_output=True,
            text=True
        )

        if "is already installed" not in result.stdout:
            logger.info("Installing Playwright browsers...")
            subprocess.run(["python3", "-m", "playwright", "install", "chromium"], check=True)
            logger.info("✓ Playwright browsers installed")
        else:
            logger.info("✓ Playwright browsers ready")

    except ImportError:
        logger.warning("Playwright not installed. Run: pip install playwright")

    # Check other dependencies
    required = ["yaml", "jinja2", "bs4", "requests"]
    missing = []

    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)

    if missing:
        logger.error("Missing dependencies: %s", ", ".join(missing))
        raise ImportError(f"Install: pip install {' '.join(missing)}")

    logger.info("✓ All dependencies ready")


def AskUserQuestion(prompt: str, default: str = "yes") -> bool:
    """
    Ask user a yes/no question.

    Args:
        prompt: Question to ask
        default: Default answer ("yes" or "no")

    Returns:
        True for yes, False for no
    """
    suffix = "[Y/n]" if default == "yes" else "[y/N]"
    full_prompt = f"{prompt} {suffix}: "

    try:
        response = input(full_prompt).strip().lower()

        if not response:
            return default == "yes"

        return response in ["y", "yes"]

    except (KeyboardInterrupt, EOFError):
        print()
        return False


class SecurityHelper:
    """Security utilities for credential and cookie management."""

    @staticmethod
    def get_credentials(service: str, username_key: str, password_key: str):
        """Get credentials from OS keyring."""
        try:
            import keyring

            username = keyring.get_password(service, username_key)
            password = keyring.get_password(service, password_key)

            return username, password

        except ImportError:
            logger.warning("Keyring not available. Using prompts.")
            return None, None

    @staticmethod
    def set_credentials(service: str, username_key: str, username: str,
                       password_key: str, password: str):
        """Save credentials to OS keyring."""
        try:
            import keyring

            keyring.set_password(service, username_key, username)
            keyring.set_password(service, password_key, password)

            logger.info("✓ Credentials saved to keyring")

        except ImportError:
            logger.warning("Keyring not available. Credentials not saved.")

    @staticmethod
    def encrypt_cookie(cookie_data: str, key: Optional[bytes] = None) -> bytes:
        """Encrypt cookie with Fernet."""
        try:
            from cryptography.fernet import Fernet

            if not key:
                key = Fernet.generate_key()

            f = Fernet(key)
            encrypted = f.encrypt(cookie_data.encode())

            return encrypted

        except ImportError:
            logger.warning("cryptography not available. Cookie not encrypted.")
            return cookie_data.encode()

    @staticmethod
    def decrypt_cookie(encrypted_data: bytes, key: bytes) -> str:
        """Decrypt cookie with Fernet."""
        try:
            from cryptography.fernet import Fernet

            f = Fernet(key)
            decrypted = f.decrypt(encrypted_data)

            return decrypted.decode()

        except ImportError:
            logger.warning("cryptography not available. Using plaintext.")
            return encrypted_data.decode()

"""
Data Collection Modules

Provides modular collectors for different JD sources:
- MarkdownParser: Parse existing markdown JDs
- PlaywrightFetcher: Automated browser collection (LinkedIn, Wellfound)
- URLFetcher: BeautifulSoup-based single URL parsing
"""

import re
import time
import random
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, date
import hashlib

# BeautifulSoup for static parsing
from bs4 import BeautifulSoup
import requests

# Playwright for dynamic pages
try:
    from playwright.sync_api import sync_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

logger = logging.getLogger(__name__)


class MarkdownParser:
    """Parse existing markdown JD files."""

    # Regex patterns for metadata extraction
    COMPANY_PATTERN = re.compile(r"^#\s+(.+?)(?:\s+-\s+|\s+\||\n)", re.MULTILINE)
    TITLE_PATTERN = re.compile(r"(?:Position|Role|Title):\s*(.+)", re.IGNORECASE)
    LOCATION_PATTERN = re.compile(r"(?:Location|Based):\s*(.+)", re.IGNORECASE)

    REMOTE_KEYWORDS = ["remote", "anywhere", "distributed", "work from home", "wfh"]
    VISA_KEYWORDS = ["visa sponsorship", "visa support", "work permit", "h1b"]

    def __init__(self):
        """Initialize parser."""
        pass

    def parse_folder(self, folder: Path) -> List[Dict]:
        """Parse all markdown files in folder."""
        jd_files = list(folder.rglob("*.md"))
        logger.info("Found %d markdown files", len(jd_files))

        parsed = []
        for file in jd_files:
            try:
                jd = self.parse_file(file)
                if jd:
                    parsed.append(jd)
            except Exception as e:
                logger.warning("Failed to parse %s: %s", file.name, e)

        return parsed

    def parse_file(self, file: Path) -> Optional[Dict]:
        """Parse single markdown file."""
        content = file.read_text(encoding="utf-8")

        # Extract metadata
        company = self._extract_company(content)
        title = self._extract_title(content)
        location = self._extract_location(content)
        is_remote = self._detect_remote(content)
        visa_sponsor = self._detect_visa(content)

        # Generate unique ID
        jd_id = self._generate_id(company, title)

        return {
            "id": jd_id,
            "title": title or "Unknown Title",
            "company": company or file.stem,
            "url": "",
            "platform": "markdown",
            "location": location or "Unknown",
            "is_remote": is_remote,
            "posted_date": None,
            "scraped_date": str(date.today()),
            "description": content,
            "skills": {},
            "experience_years": None,
            "salary_range": None,
            "visa_sponsor": visa_sponsor,
        }

    def _extract_company(self, content: str) -> Optional[str]:
        """Extract company name from content."""
        match = self.COMPANY_PATTERN.search(content)
        if match:
            return match.group(1).strip()
        return None

    def _extract_title(self, content: str) -> Optional[str]:
        """Extract job title from content."""
        match = self.TITLE_PATTERN.search(content)
        if match:
            return match.group(1).strip()
        return None

    def _extract_location(self, content: str) -> Optional[str]:
        """Extract location from content."""
        match = self.LOCATION_PATTERN.search(content)
        if match:
            return match.group(1).strip()
        return None

    def _detect_remote(self, content: str) -> bool:
        """Detect if job is remote."""
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in self.REMOTE_KEYWORDS)

    def _detect_visa(self, content: str) -> bool:
        """Detect if visa sponsorship available."""
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in self.VISA_KEYWORDS)

    def _generate_id(self, company: str, title: str) -> str:
        """Generate unique ID for JD."""
        text = f"{company}_{title}_{date.today()}"
        return hashlib.md5(text.encode()).hexdigest()[:12]


class PlaywrightFetcher:
    """Automated browser-based JD collection for LinkedIn and Wellfound."""

    def __init__(self, config_dir: Path):
        """Initialize fetcher with config directory."""
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed. Run: pip install playwright && playwright install chromium")

        self.config_dir = config_dir
        self.cookies_dir = config_dir / "cookies"
        self.cookies_dir.mkdir(exist_ok=True)

    def collect_linkedin(self, query: str, count: int = 50) -> List[Dict]:
        """Collect JDs from LinkedIn via Playwright automation."""
        logger.info("Collecting from LinkedIn: %s (target: %d)", query, count)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # headless=False for CAPTCHA
            page = browser.new_page()

            try:
                # Try to load saved session
                if not self._load_linkedin_session(page):
                    # Login required
                    self._login_linkedin(page)
                    self._save_linkedin_session(page)

                # Search JDs
                jds = self._search_linkedin(page, query, count)

                return jds

            except Exception as e:
                logger.error("LinkedIn collection failed: %s", e)
                return []
            finally:
                browser.close()

    def collect_wellfound(self, query: str, count: int = 50) -> List[Dict]:
        """Collect JDs from Wellfound (no login required)."""
        logger.info("Collecting from Wellfound: %s (target: %d)", query, count)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                jds = self._search_wellfound(page, query, count)
                return jds
            except Exception as e:
                logger.error("Wellfound collection failed: %s", e)
                return []
            finally:
                browser.close()

    def _load_linkedin_session(self, page: Page) -> bool:
        """Load saved LinkedIn session cookie with Fernet decryption."""
        cookie_file = self.cookies_dir / "linkedin.enc"

        if not cookie_file.exists():
            return False

        try:
            import json
            import keyring
            from cryptography.fernet import Fernet

            # Get Fernet key from keyring
            key = keyring.get_password("jd-analyzer", "cookie_encryption_key")
            if not key:
                logger.warning("No encryption key found. Cannot load cookies.")
                return False

            # Decrypt cookies
            encrypted_data = cookie_file.read_bytes()
            f = Fernet(key.encode())
            decrypted_json = f.decrypt(encrypted_data).decode()
            cookies = json.loads(decrypted_json)

            page.context.add_cookies(cookies)

            # Verify session by navigating
            page.goto("https://www.linkedin.com/feed/", timeout=10000)
            if "login" in page.url:
                return False

            logger.info("✓ LinkedIn session loaded (encrypted)")
            return True
        except Exception as e:
            logger.warning("Failed to load session: %s", e)
            return False

    def _save_linkedin_session(self, page: Page):
        """Save LinkedIn session cookie with Fernet encryption."""
        cookie_file = self.cookies_dir / "linkedin.enc"

        try:
            import json
            import keyring
            from cryptography.fernet import Fernet

            # Get or create Fernet key
            key = keyring.get_password("jd-analyzer", "cookie_encryption_key")
            if not key:
                key = Fernet.generate_key().decode()
                keyring.set_password("jd-analyzer", "cookie_encryption_key", key)
                logger.info("✓ Generated new cookie encryption key")

            # Encrypt cookies
            cookies = page.context.cookies()
            cookies_json = json.dumps(cookies)
            f = Fernet(key.encode())
            encrypted = f.encrypt(cookies_json.encode())

            cookie_file.write_bytes(encrypted)
            logger.info("✓ LinkedIn session saved (encrypted)")
        except Exception as e:
            logger.warning("Failed to save session: %s", e)

    def _login_linkedin(self, page: Page):
        """Login to LinkedIn."""
        logger.info("LinkedIn login required...")

        page.goto("https://www.linkedin.com/login")

        # Get credentials from keyring
        try:
            import keyring
            email = keyring.get_password("jd-analyzer", "linkedin_email")
            password = keyring.get_password("jd-analyzer", "linkedin_password")

            if not email or not password:
                # Prompt user
                print("\nLinkedIn credentials not found in Keyring.")
                email = input("LinkedIn email: ").strip()
                password = input("LinkedIn password: ").strip()

                # Save to keyring
                keyring.set_password("jd-analyzer", "linkedin_email", email)
                keyring.set_password("jd-analyzer", "linkedin_password", password)

        except ImportError:
            # Keyring not available, prompt
            email = input("LinkedIn email: ").strip()
            password = input("LinkedIn password: ").strip()

        # Fill form
        page.fill("#username", email)
        page.fill("#password", password)
        page.click("button[type=submit]")

        # Wait for navigation
        try:
            page.wait_for_url("**/feed/**", timeout=30000)
            logger.info("✓ LinkedIn login successful")
        except Exception:
            # Check for CAPTCHA
            if "challenge" in page.url or page.locator("iframe[title*=CAPTCHA]").count() > 0:
                print("\n⚠️ CAPTCHA detected. Please solve manually.")
                input("Press Enter when done...")

            # Verify login
            if "login" in page.url:
                raise Exception("Login failed. Check credentials.")

    def _search_linkedin(self, page: Page, query: str, count: int) -> List[Dict]:
        """Search and collect LinkedIn JDs."""
        # Navigate to jobs search
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location=remote"
        page.goto(search_url)

        # Wait for results
        page.wait_for_selector(".jobs-search__results-list", timeout=10000)

        jds = []
        collected = 0

        # Scroll to load more results
        while collected < count:
            # Extract job cards
            cards = page.locator(".jobs-search__results-list li").all()

            for card in cards[:count]:
                try:
                    # Click to load details
                    card.click()
                    time.sleep(1)

                    # Extract data
                    title = page.locator(".job-details-jobs-unified-top-card__job-title").inner_text()
                    company = page.locator(".job-details-jobs-unified-top-card__company-name").inner_text()
                    location = page.locator(".job-details-jobs-unified-top-card__bullet").inner_text()

                    # Get JD URL
                    url = page.url

                    # Get description
                    description = page.locator(".jobs-description").inner_text()

                    jd = {
                        "id": hashlib.md5(url.encode()).hexdigest()[:12],
                        "title": title.strip(),
                        "company": company.strip(),
                        "url": url,
                        "platform": "linkedin",
                        "location": location.strip(),
                        "is_remote": "remote" in location.lower() or "remote" in query.lower(),
                        "posted_date": None,
                        "scraped_date": str(date.today()),
                        "description": description,
                        "skills": {},
                        "experience_years": None,
                        "salary_range": None,
                        "visa_sponsor": None,
                    }

                    jds.append(jd)
                    collected += 1

                    print(f"✓ LinkedIn: Collecting JD {collected}/{count}...")

                    if collected >= count:
                        break

                    # Rate limit
                    time.sleep(random.uniform(1, 3))

                except Exception as e:
                    logger.warning("Failed to parse job card: %s", e)

            # Scroll to load more
            if collected < count:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)

        return jds

    def _search_wellfound(self, page: Page, query: str, count: int) -> List[Dict]:
        """Search and collect Wellfound JDs."""
        # Navigate to search (simplified for MVP)
        page.goto("https://wellfound.com/jobs")

        # Wait for results
        page.wait_for_selector(".job-listings", timeout=10000)

        jds = []

        # Extract job cards (simplified)
        cards = page.locator(".job-listing").all()[:count]

        for i, card in enumerate(cards):
            try:
                title = card.locator(".job-title").inner_text()
                company = card.locator(".company-name").inner_text()
                location = card.locator(".location").inner_text() if card.locator(".location").count() > 0 else "Remote"

                jd = {
                    "id": hashlib.md5(f"{company}{title}".encode()).hexdigest()[:12],
                    "title": title.strip(),
                    "company": company.strip(),
                    "url": "",
                    "platform": "wellfound",
                    "location": location.strip(),
                    "is_remote": "remote" in location.lower(),
                    "posted_date": None,
                    "scraped_date": str(date.today()),
                    "description": "",
                    "skills": {},
                    "experience_years": None,
                    "salary_range": None,
                    "visa_sponsor": None,
                }

                jds.append(jd)
                print(f"✓ Wellfound: Collecting JD {i+1}/{count}...")

            except Exception as e:
                logger.warning("Failed to parse Wellfound card: %s", e)

        return jds


class URLFetcher:
    """BeautifulSoup-based single URL parser for multiple platforms."""

    PLATFORM_PATTERNS = {
        "linkedin": r"linkedin\.com/jobs",
        "wellfound": r"wellfound\.com|angel\.co",
        "lever": r"\.lever\.co",
        "greenhouse": r"boards\.greenhouse\.io",
    }

    SELECTORS = {
        "lever": {
            "title": ".posting-headline h2",
            "company": ".main-header-text a",
            "location": ".location",
            "description": ".content",
        },
        "greenhouse": {
            "title": ".app-title",
            "company": ".company-name",
            "location": ".location",
            "description": "#content",
        },
    }

    def __init__(self):
        """Initialize URL fetcher."""
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })

    def fetch_and_parse(self, url: str) -> Dict:
        """Fetch and parse single JD URL."""
        platform = self._detect_platform(url)
        logger.info("Detected platform: %s", platform)

        # Fetch HTML
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            raise Exception(f"Failed to fetch URL: {e}")

        # Parse
        soup = BeautifulSoup(html, "html.parser")

        if platform in self.SELECTORS:
            jd = self._parse_with_selectors(soup, url, platform)
        else:
            jd = self._parse_generic(soup, url)

        return jd

    def _detect_platform(self, url: str) -> str:
        """Detect platform from URL."""
        for platform, pattern in self.PLATFORM_PATTERNS.items():
            if re.search(pattern, url):
                return platform
        return "generic"

    def _parse_with_selectors(self, soup: BeautifulSoup, url: str, platform: str) -> Dict:
        """Parse using platform-specific selectors."""
        selectors = self.SELECTORS[platform]

        title = soup.select_one(selectors["title"]).get_text(strip=True) if soup.select_one(selectors["title"]) else "Unknown"
        company = soup.select_one(selectors["company"]).get_text(strip=True) if soup.select_one(selectors["company"]) else "Unknown"
        location = soup.select_one(selectors["location"]).get_text(strip=True) if soup.select_one(selectors["location"]) else "Unknown"
        description = soup.select_one(selectors["description"]).get_text(strip=True) if soup.select_one(selectors["description"]) else ""

        return {
            "id": hashlib.md5(url.encode()).hexdigest()[:12],
            "title": title,
            "company": company,
            "url": url,
            "platform": platform,
            "location": location,
            "is_remote": "remote" in location.lower() or "remote" in description.lower(),
            "posted_date": None,
            "scraped_date": str(date.today()),
            "description": description,
            "skills": {},
            "experience_years": None,
            "salary_range": None,
            "visa_sponsor": None,
        }

    def _parse_generic(self, soup: BeautifulSoup, url: str) -> Dict:
        """Fallback generic parser."""
        # Extract title from h1
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Unknown"

        # Full text as description
        description = soup.get_text(separator="\n", strip=True)

        return {
            "id": hashlib.md5(url.encode()).hexdigest()[:12],
            "title": title,
            "company": "Unknown",
            "url": url,
            "platform": "generic",
            "location": "Unknown",
            "is_remote": False,
            "posted_date": None,
            "scraped_date": str(date.today()),
            "description": description,
            "skills": {},
            "experience_years": None,
            "salary_range": None,
            "visa_sponsor": None,
        }

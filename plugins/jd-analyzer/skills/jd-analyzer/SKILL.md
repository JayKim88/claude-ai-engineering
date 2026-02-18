# JD Analyzer - Career Transition Intelligence

## Quick Reference

**Purpose**: Automate AI Product Engineer career transition with intelligent JD analysis
**Primary Use**: Collect 100+ JDs, extract skills, match profile, generate actionable insights
**Key Features**: Playwright automation, spaCy NLP, weighted scoring (10pt/3pt), Jinja2 reports
**Performance**: < 10 min full pipeline, < 2 min skill extraction

## Execution Algorithm

### Step 1: Environment Validation

**Goal**: Ensure all dependencies and configurations are ready

**Process**:
1. Check Python version (3.9+)
2. Verify dependencies installed (8 packages from requirements.txt)
3. Check spaCy model availability (auto-download `en_core_web_sm` if missing)
4. Validate Playwright browsers (auto-install if needed)
5. Check config directory `~/.jd-analyzer/` exists

**Error Handling**:
- **Missing spaCy model**: Auto-run `python -m spacy download en_core_web_sm`
- **Missing Playwright browsers**: Auto-run `playwright install chromium`
- **Old Python version**: Error with upgrade instructions
- **Missing config dir**: Auto-create with templates

**Pseudocode**:
```python
def validate_environment():
    if sys.version_info < (3, 9):
        raise Error("Python 3.9+ required")

    missing = check_dependencies()
    if missing:
        suggest_pip_install(missing)

    if not spacy_model_exists("en_core_web_sm"):
        auto_download_spacy_model()

    if not playwright_browser_installed():
        auto_install_playwright()

    ensure_config_directory()
```

---

### Step 2: Profile Setup Check

**Goal**: Load or create user profile for matching

**Process**:
1. Check if `~/.jd-analyzer/profile.yaml` exists
2. If missing: Create template, prompt user to fill it
3. If exists: Load and validate structure
4. Validate skill categories match taxonomy
5. Extract user skills (all proficiency levels: expert, advanced, learning)

**Error Handling**:
- **No profile**: Create template, exit with instructions
- **Invalid YAML syntax**: Show line number, provide fix guide
- **Missing required fields**: List missing fields
- **Unknown skill categories**: Suggest valid categories from taxonomy

**Profile Template Structure**:
```yaml
personal:
  name: "Your Name"
  location: "City, Country"

experience:
  total_years: 0
  frontend_years: 0
  backend_years: 0
  ai_ml_years: 0

skills:
  frontend:
    expert: ["React", "TypeScript"]
    advanced: ["Next.js"]
    learning: ["Vue.js"]
  backend:
    expert: ["Python"]
    advanced: ["FastAPI"]
  ai_ml:
    advanced: ["Claude AI", "Prompt Engineering"]
    learning: ["LangChain", "RAG"]

preferences:
  remote_only: true
  visa_required: false
  min_match_score: 70
```

**Pseudocode**:
```python
def load_or_create_profile():
    profile_path = Path.home() / ".jd-analyzer" / "profile.yaml"

    if not profile_path.exists():
        create_profile_template(profile_path)
        print("Profile template created. Please fill and re-run.")
        sys.exit(0)

    try:
        profile = yaml.safe_load(profile_path.read_text())
        validate_profile_structure(profile)
        return profile
    except yaml.YAMLError as e:
        raise Error(f"YAML syntax error: {e}")
```

---

### Step 3: Mode Selection

**Goal**: Determine which analysis mode to run

**Modes**:
1. **Analyze Existing**: Parse 24 JDs from `JDs/` folder (Quick Win, 30-60 sec)
2. **Search New**: Automated search via Playwright (LinkedIn 50 + Wellfound 50)
3. **Add Single URL**: Parse one URL (Lever, Greenhouse, etc.)
4. **Full Analysis**: Re-analyze all collected JDs

**User Interaction**:
Use `AskUserQuestion` to present mode menu:
```
Select mode:
1. Analyze existing JDs (24 files in JDs/ folder) - Quick Win!
2. Search new JDs (LinkedIn + Wellfound automation)
3. Add single URL
4. Full analysis of all collected JDs

Choice (1-4):
```

**Routing Logic**:
- Mode 1 → Go to Step 4a
- Mode 2 → Go to Step 4b
- Mode 3 → Go to Step 4c
- Mode 4 → Go to Step 5 (skip collection)

**Pseudocode**:
```python
def select_mode():
    jds_count = count_existing_jds()

    menu = f"""
    1. Analyze existing JDs ({jds_count} files)
    2. Search new JDs (LinkedIn + Wellfound)
    3. Add single URL
    4. Full analysis
    """

    choice = AskUserQuestion(menu, type="choice")
    return choice
```

---

### Step 4a: Analyze Existing JDs

**Goal**: Parse markdown JDs from `JDs/` folder

**Process**:
1. Scan `JDs/**/*.md` for all markdown files
2. For each file:
   - Read content
   - Extract metadata (company, title, location)
   - Detect sections (## Requirements, ## Qualifications)
   - Parse requirements text
   - Detect remote status (keywords: "remote", "anywhere", "distributed")
   - Detect visa sponsorship (keywords: "visa", "sponsorship")
3. Convert to `JobDescription` dataclass
4. Save to `~/.jd-analyzer/data/jds.json`

**Regex Patterns**:
```python
COMPANY_PATTERN = r"^#\s+(.+?)(?:\s+-\s+|\s+\|)"
TITLE_PATTERN = r"(?:Position|Role|Title):\s*(.+)"
LOCATION_PATTERN = r"(?:Location|Based):\s*(.+)"
REMOTE_KEYWORDS = ["remote", "anywhere", "distributed", "work from home"]
VISA_KEYWORDS = ["visa sponsorship", "visa support", "work permit"]
```

**Error Handling**:
- **Malformed markdown**: Log warning, extract what's possible
- **Missing sections**: Use full content as description
- **File read error**: Skip file, continue with others

**Pseudocode**:
```python
def parse_existing_jds(jds_folder: Path):
    jd_files = list(jds_folder.rglob("*.md"))
    parsed = []

    for file in jd_files:
        try:
            content = file.read_text()
            jd = parse_markdown_jd(content, file)
            parsed.append(jd)
        except Exception as e:
            logger.warning(f"Failed to parse {file}: {e}")

    return parsed

def parse_markdown_jd(content: str, file: Path):
    company = extract_company(content)
    title = extract_title(content)
    location = extract_location(content)
    is_remote = detect_remote(content)

    return JobDescription(
        id=generate_id(company, title),
        company=company,
        title=title,
        location=location,
        is_remote=is_remote,
        description=content,
        ...
    )
```

---

### Step 4b: Search New JDs (Playwright Automation)

**Goal**: Collect 100 JDs (LinkedIn 50 + Wellfound 50)

**Phase 1: LinkedIn Collection (3-5 min)**

1. **Launch Playwright browser** (headless=False for CAPTCHA visibility)
2. **Check for saved session**:
   - Load encrypted cookie from `~/.jd-analyzer/cookies/linkedin.enc`
   - Decrypt with Fernet key
   - If valid: Skip login
3. **Login flow** (if no session):
   - Navigate to `linkedin.com/login`
   - Get credentials from Keyring
   - Fill email/password, submit
   - Handle CAPTCHA: Detect and prompt user
   - Save session cookie (encrypted)
4. **Search JDs**:
   - Navigate to `/jobs/search/?keywords={query}&location=remote`
   - Scroll to load 50 results (human-like delays)
   - Extract JD URLs
5. **Parse each JD**:
   - Navigate to URL
   - Extract: title, company, location, description
   - Rate limit: 1 request/sec
   - Progress: "✓ LinkedIn: Collecting JD 1/50..."

**Phase 2: Wellfound Collection (2-3 min)**

1. **Launch browser** (no login required)
2. **Search**:
   - Navigate to `wellfound.com/jobs`
   - Apply filters: Role type, Remote
   - Scroll to load 50 results
3. **Parse JDs**:
   - Extract from search results page
   - Progress: "✓ Wellfound: Collecting JD 1/50..."

**Error Handling**:
- **Login failure**: Re-prompt credentials, retry 3x
- **CAPTCHA detected**: Pause, prompt user to solve, resume
- **Session expired**: Delete cookie, re-login
- **Rate limit (429)**: Wait 5 min, resume
- **Browser crash**: Save progress, resume from checkpoint
- **Network error**: Retry 3x with exponential backoff

**Security**:
- **Credentials**: Store in OS Keyring (never plaintext)
- **Cookies**: Encrypt with Fernet before saving
- **Rate limiting**: 1 req/sec, random delays 1-3 sec

**Pseudocode**:
```python
def collect_linkedin_jds(query: str, count: int = 50):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # Session management
    if has_saved_cookie():
        cookie = decrypt_cookie(load_cookie())
        page.context.add_cookies(cookie)
    else:
        login_to_linkedin(page)
        save_encrypted_cookie(page.context.cookies())

    # Search
    page.goto(f"linkedin.com/jobs/search/?keywords={query}")
    jd_urls = scroll_and_extract_urls(page, count)

    # Parse each JD
    jds = []
    for i, url in enumerate(jd_urls):
        print(f"✓ LinkedIn: Collecting JD {i+1}/{count}...")
        jd = parse_linkedin_jd(page, url)
        jds.append(jd)
        time.sleep(random.uniform(1, 3))  # Rate limit

    return jds

def login_to_linkedin(page):
    page.goto("linkedin.com/login")

    email, password = get_credentials_from_keyring()
    page.fill("#username", email)
    page.fill("#password", password)
    page.click("button[type=submit]")

    if detect_captcha(page):
        input("⚠️ CAPTCHA detected. Solve manually, press Enter...")

    page.wait_for_url("linkedin.com/feed")
```

---

### Step 4c: Add Single URL

**Goal**: Parse one JD URL and add to collection

**Supported Platforms**:
- LinkedIn Jobs
- Wellfound (AngelList)
- Lever (company.lever.co)
- Greenhouse (boards.greenhouse.io)
- Generic (fallback to BeautifulSoup)

**Process**:
1. Detect platform from URL
2. Select appropriate parser
3. Fetch HTML (requests or Playwright if dynamic)
4. Extract fields using platform-specific selectors
5. Save to JSON + Markdown
6. Prompt: "Re-analyze all JDs? [Y/n]"

**Platform Detection**:
```python
PLATFORM_PATTERNS = {
    "linkedin": r"linkedin\.com/jobs",
    "wellfound": r"wellfound\.com|angel\.co",
    "lever": r"\.lever\.co",
    "greenhouse": r"boards\.greenhouse\.io",
}
```

**Error Handling**:
- **404 Not Found**: "JD deleted or invalid URL"
- **Platform not supported**: Prompt for manual text input
- **Parsing failed**: Save raw HTML, mark for manual review

**Pseudocode**:
```python
def add_single_url(url: str):
    platform = detect_platform(url)

    if platform in ["linkedin", "wellfound"]:
        jd = parse_with_playwright(url, platform)
    else:
        jd = parse_with_beautifulsoup(url, platform)

    save_jd(jd)

    if AskUserQuestion("Re-analyze all JDs?", type="yes/no"):
        analyze_all_jds()
```

---

### Step 5: Skill Extraction (spaCy + YAML)

**Goal**: Extract and categorize skills from JD descriptions

**Taxonomy-Driven Extraction**:

1. **Load skill taxonomy** (`~/.jd-analyzer/skill_taxonomy.yaml`):
   - 8 categories: Frontend, Backend, AI/ML, DevOps, Database, Testing, Soft Skills, Tools
   - 200+ skills with aliases
   - Example:
     ```yaml
     categories:
       frontend:
         keywords: ["React", "Vue", "Angular", "Next.js"]
         aliases:
           React: ["ReactJS", "React.js"]
       ai_ml:
         keywords: ["LLM", "RAG", "LangChain", "Prompt Engineering"]
         aliases:
           LLM: ["Large Language Model", "GPT"]
     ```

2. **spaCy NLP Processing**:
   - Load `en_core_web_sm` model
   - Tokenize JD description
   - Extract noun phrases
   - Match against taxonomy keywords + aliases
   - Case-insensitive matching

3. **Categorization**:
   - Assign each skill to category
   - Track frequency across all JDs
   - Separate Required vs Nice-to-have (detect sections)

**Required vs Nice-to-have Detection**:
```python
REQUIRED_SECTIONS = [
    "requirements", "must have", "required skills",
    "qualifications", "what you need"
]
NICE_TO_HAVE_SECTIONS = [
    "nice to have", "preferred", "bonus", "plus"
]
```

**Error Handling**:
- **No skills extracted**: Log warning, add to "Uncategorized"
- **Unknown skill**: Save to "Other" category for review
- **spaCy model missing**: Auto-download

**Pseudocode**:
```python
class SkillExtractor:
    def __init__(self, taxonomy_path: Path):
        self.nlp = spacy.load("en_core_web_sm")
        self.taxonomy = yaml.safe_load(taxonomy_path.read_text())

    def extract(self, text: str) -> Dict[str, List[str]]:
        doc = self.nlp(text.lower())
        skills = {"required": set(), "nice_to_have": set()}

        # Detect sections
        required_text, nice_text = split_by_sections(text)

        # Extract from each section
        for category, config in self.taxonomy["categories"].items():
            for keyword in config["keywords"]:
                aliases = config.get("aliases", {}).get(keyword, [])
                all_variants = [keyword] + aliases

                for variant in all_variants:
                    if variant.lower() in required_text.lower():
                        skills["required"].add(keyword)
                    elif variant.lower() in nice_text.lower():
                        skills["nice_to_have"].add(keyword)

        return {k: sorted(list(v)) for k, v in skills.items()}
```

---

### Step 6: Profile Matching (Weighted Scoring)

**Goal**: Calculate match score using weighted algorithm

**Algorithm** (per spec):
- **Required skill matched**: +10 points
- **Nice-to-have matched**: +3 points
- **Match score**: (earned points / total points) × 100

**Process**:
1. Load user profile skills (flatten all proficiency levels)
2. For each JD:
   - Calculate total possible points
   - Calculate earned points
   - Compute percentage
   - Identify missing skills
   - Store result

**Example Calculation**:
```
JD Requirements:
  Required: [React, TypeScript, Python, Docker]  → 4 × 10 = 40 pts
  Nice-to-have: [AWS, GraphQL, Redis]             → 3 × 3 = 9 pts
  Total possible: 49 pts

User Skills: [React, TypeScript, AWS, PostgreSQL]
  Matched Required: React (10), TypeScript (10)   → 20 pts
  Matched Nice-to-have: AWS (3)                   → 3 pts
  Earned: 23 pts

Match Score: (23 / 49) × 100 = 46.9%

Missing Skills: [Python, Docker, GraphQL, Redis]
```

**Error Handling**:
- **No required skills in JD**: Score = 0%, log warning
- **Empty user profile**: Error with instructions

**Pseudocode**:
```python
class ProfileMatcher:
    def __init__(self, profile: Dict):
        self.user_skills = self._flatten_skills(profile["skills"])

    def match(self, jd: JobDescription) -> MatchResult:
        required = set(jd.skills.get("required", []))
        nice_to_have = set(jd.skills.get("nice_to_have", []))

        # Calculate points
        total_points = len(required) * 10 + len(nice_to_have) * 3

        matched_required = required & self.user_skills
        matched_nice = nice_to_have & self.user_skills

        earned_points = len(matched_required) * 10 + len(matched_nice) * 3

        # Compute score
        score = (earned_points / total_points * 100) if total_points > 0 else 0

        missing = (required | nice_to_have) - self.user_skills

        return MatchResult(
            score=score,
            matched_required=matched_required,
            matched_nice=matched_nice,
            missing_skills=missing
        )
```

---

### Step 7: Company Ranking

**Goal**: Sort companies by match score and preferences

**Filters**:
1. **Minimum match score**: `profile.preferences.min_match_score` (default 70%)
2. **Remote preference**: If `remote_only=true`, filter `is_remote=true`
3. **Visa requirement**: If `visa_required=true`, filter `visa_sponsor=true`

**Sorting Priority**:
1. Match score (descending)
2. Remote availability (remote first if preferred)
3. Posted date (recent first)

**Output**: Top 50 companies with metadata

**Pseudocode**:
```python
def rank_companies(matches: List[MatchResult], profile: Dict):
    # Filter
    filtered = [
        m for m in matches
        if m.score >= profile["preferences"]["min_match_score"]
    ]

    if profile["preferences"]["remote_only"]:
        filtered = [m for m in filtered if m.jd.is_remote]

    # Sort
    sorted_matches = sorted(
        filtered,
        key=lambda m: (m.score, m.jd.is_remote, m.jd.posted_date),
        reverse=True
    )

    return sorted_matches[:50]
```

---

### Step 8: Trend Analysis

**Goal**: Compute market trends and insights

**Metrics**:
1. **Top 20 Most Required Skills**: Frequency + percentage
2. **Top 5 Skills to Learn**: Skills you're missing, ranked by demand
3. **Remote Work Stats**: Fully remote vs Hybrid vs On-site distribution
4. **Salary Range**: By experience level (if available)
5. **Match Distribution**: Buckets (80-100%, 60-79%, 40-59%, <40%)
6. **Platform Distribution**: LinkedIn, Wellfound, Lever, Greenhouse counts
7. **Experience Requirements**: Entry, Mid, Senior distribution

**Pseudocode**:
```python
class TrendAnalyzer:
    def analyze(self, jds: List[JobDescription], matches: List[MatchResult]):
        # Skill frequency
        all_skills = Counter()
        for jd in jds:
            all_skills.update(jd.skills["required"])
            all_skills.update(jd.skills["nice_to_have"])

        top_skills = all_skills.most_common(20)

        # Skills to learn
        missing_skills = Counter()
        for match in matches:
            missing_skills.update(match.missing_skills)

        skills_to_learn = missing_skills.most_common(5)

        # Remote stats
        remote_count = sum(1 for jd in jds if jd.is_remote)
        remote_pct = remote_count / len(jds) * 100

        # Match distribution
        buckets = {
            "80-100%": 0,
            "60-79%": 0,
            "40-59%": 0,
            "<40%": 0
        }
        for match in matches:
            if match.score >= 80:
                buckets["80-100%"] += 1
            elif match.score >= 60:
                buckets["60-79%"] += 1
            elif match.score >= 40:
                buckets["40-59%"] += 1
            else:
                buckets["<40%"] += 1

        return TrendReport(
            top_skills=top_skills,
            skills_to_learn=skills_to_learn,
            remote_pct=remote_pct,
            buckets=buckets,
            ...
        )
```

---

### Step 9: Report Generation (Jinja2)

**Goal**: Create actionable markdown report

**Template Structure**:
```markdown
# JD Analysis Report - {date}

## Executive Summary
- **Total JDs Analyzed**: {count}
- **Average Match Score**: {avg_score}%
- **Top Match**: {best_company} ({best_score}%)

## 🎯 Actionable Insights

### Top 5 Skills to Learn
1. **Python** - Required in 78 JDs (78%)
2. **Docker** - Required in 65 JDs (65%)
...

### Top 10 Companies to Apply
1. **{company}** - {match_score}% match
   - Missing: {missing_skills}
   - Remote: {remote}
   - URL: {url}
...

## 📊 Market Trends

### Top 20 Most Required Skills
| Skill | Frequency | Percentage |
|-------|-----------|------------|
| React | 85 | 85% |
...

### Remote Work Statistics
- Fully Remote: {remote_count} ({remote_pct}%)
- Hybrid: {hybrid_count}
- On-site: {onsite_count}

### Match Score Distribution
- 80-100%: {count} JDs
- 60-79%: {count} JDs
...

## 💼 Your Profile Match

### Strong Matches (70%+)
- {company} - {score}%
...

### Skill Gap Analysis
Top 5 missing skills:
1. Python (needed for 78 JDs)
...

## 📈 Next Steps
1. Learn {top_skill} (highest ROI)
2. Apply to {top_company}
...
```

**Jinja2 Implementation**:
```python
class MarkdownReportGenerator:
    def __init__(self, template_path: Path):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path.parent))
        self.template = env.get_template(template_path.name)

    def generate(self, data: Dict) -> str:
        return self.template.render(**data)
```

---

### Step 10: Follow-up Actions

**Goal**: Save outputs and prompt next steps

**Outputs**:
1. **Report**: `jd-analysis-report-{date}.md` in current directory
2. **Data**: `~/.jd-analyzer/data/jds.json` (all JDs)
3. **Matches**: `~/.jd-analyzer/data/matches.json` (scores)

**User Prompts**:
- "View report now? [Y/n]"
- "Export to CSV? [y/N]"
- "Schedule next search? [y/N]"

**Pseudocode**:
```python
def finalize(report: str, data: Dict):
    # Save report
    report_path = Path.cwd() / f"jd-analysis-report-{date.today()}.md"
    report_path.write_text(report)

    # Save data
    data_dir = Path.home() / ".jd-analyzer" / "data"
    (data_dir / "jds.json").write_text(json.dumps(data["jds"]))
    (data_dir / "matches.json").write_text(json.dumps(data["matches"]))

    print(f"\n✅ Report saved: {report_path}")

    if AskUserQuestion("View report now?", type="yes/no"):
        print(report)
```

---

## Error Handling Scenarios

| Error | Detection | Recovery | User Message |
|-------|-----------|----------|--------------|
| **LinkedIn login failure** | HTTP 401 after submit | Re-prompt credentials 3x | "⚠️ Login failed. Check email/password" |
| **CAPTCHA detected** | Detect CAPTCHA iframe | Pause, wait for user | "⚠️ CAPTCHA detected. Solve manually, press Enter..." |
| **Session expired** | Redirect to login | Delete cookie, re-login | "⚠️ Session expired. Re-logging in..." |
| **Browser crash** | Process exit code | Save progress, resume | "⚠️ Browser crashed. Progress saved ({count}/100). Resume? [Y/n]" |
| **Rate limit (429)** | HTTP status 429 | Wait 5 min, retry | "⚠️ Rate limited. Waiting 5 min..." |
| **Network timeout** | Request timeout | 3 retries, exponential backoff | "⚠️ Network error. Retrying..." |
| **404 on JD URL** | HTTP 404 | Skip, log | "⚠️ JD deleted: {url}" |
| **Unsupported platform** | Unknown domain | Prompt for manual input | "⚠️ Platform not supported: {platform}" |
| **YAML parse error** | YAMLError exception | Show line, suggest fix | "⚠️ YAML syntax error (line {n}): {msg}" |
| **No skills extracted** | Empty skill list | Log warning, continue | "⚠️ No skills found in: {title}" |
| **Missing spaCy model** | Model not found | Auto-download | "⏳ Downloading spaCy model..." |
| **Invalid profile** | Missing required fields | List fields, exit | "⚠️ Profile incomplete. Missing: {fields}" |
| **Disk space low** | Check before save | Warn, ask to continue | "⚠️ Low disk space ({mb} MB). Continue? [y/N]" |
| **Duplicate JD** | URL already exists | Skip, log | "⏭️ Skipping duplicate: {company}" |
| **Cookie encryption fail** | Fernet error | Delete, re-login | "⚠️ Cookie corrupted. Re-login required" |
| **Platform API change** | Parse failure | Fallback parser, log | "⚠️ {platform} layout changed. Using fallback parser" |

---

## Performance Benchmarks

| Task | Target | Typical | Notes |
|------|--------|---------|-------|
| LinkedIn collection (50 JDs) | < 3 min | 2.5 min | Network-dependent |
| Wellfound collection (50 JDs) | < 2 min | 1.5 min | No login faster |
| Existing JD parsing (24 files) | < 30 sec | 15 sec | I/O-bound |
| Skill extraction (100 JDs) | < 2 min | 1 min | CPU-bound (spaCy) |
| Profile matching (100 JDs) | < 30 sec | 10 sec | Simple math |
| Report generation | < 10 sec | 5 sec | Jinja2 template |
| **Full pipeline** | **< 10 min** | **~6 min** | **Primary metric** |

---

## Configuration Files

### skill_taxonomy.yaml
Located at `~/.jd-analyzer/skill_taxonomy.yaml`, user-editable for custom skills.

### profile.yaml
User profile at `~/.jd-analyzer/profile.yaml`, created on first run.

### settings.yaml
Optional advanced settings at `~/.jd-analyzer/settings.yaml`:
```yaml
rate_limits:
  linkedin: 1  # requests per second
  default: 2

timeouts:
  page_load: 30
  request: 10

performance:
  max_jds_per_search: 100
  cache_ttl: 86400  # 24 hours
```

---

## Security Considerations

### Credential Storage
- **OS Keyring**: macOS Keychain, Windows Credential Manager, Linux Secret Service
- **No plaintext**: Never store credentials in .env or config files
- **Git-safe**: Keyring data never committed

### Cookie Encryption
- **Fernet (symmetric)**: Encrypt session cookies before saving
- **Key storage**: Store Fernet key in Keyring
- **Rotation**: Cookies auto-refresh when expired

### Rate Limiting
- **Prevent bans**: 1 request/second max
- **Human-like**: Random delays 1-3 sec between requests
- **Backoff**: Exponential backoff on errors

### Data Privacy
- **Local only**: All data in `~/.jd-analyzer/`, never transmitted
- **User control**: Easy to delete all data
- **Transparency**: JSON + Markdown readable formats

---

## Quick Start Examples

### Example 1: Analyze Existing JDs (Quick Win)
```bash
/jd-analyzer
# Select option 1
# Output: Report in 30-60 sec
```

### Example 2: Automated LinkedIn Search
```bash
/jd-analyzer
# Select option 2
# Enter LinkedIn credentials (first time only)
# Wait ~6 min for 100 JDs
# View report
```

### Example 3: Add Single URL
```bash
/jd-analyzer
# Select option 3
# Paste URL: https://boards.greenhouse.io/company/jobs/123
# Output: JD parsed and added
```

### Example 4: Full Re-analysis
```bash
/jd-analyzer
# Select option 4
# Output: Re-analyze all collected JDs
```

---

## Model Selection Rationale

### spaCy (en_core_web_sm)
- **Why**: Fast, accurate NLP for skill extraction
- **Alternative considered**: Regex-only (less accurate)
- **Trade-off**: 40 MB model download vs accuracy

### Playwright
- **Why**: Handles dynamic LinkedIn/Wellfound pages
- **Alternative considered**: BeautifulSoup (can't handle JS)
- **Trade-off**: Heavier dependency vs functionality

### Jinja2
- **Why**: Flexible, customizable report templates
- **Alternative considered**: String formatting (less flexible)
- **Trade-off**: Extra dependency vs customization

---

## Extensibility Hooks

### Add New Platform
1. Add platform pattern to `PLATFORM_PATTERNS`
2. Implement parser in `collectors.py`
3. Add selectors to `config/selectors.yaml`

### Add New Skill Category
1. Edit `~/.jd-analyzer/skill_taxonomy.yaml`
2. Add category with keywords
3. Re-analyze JDs

### Customize Report Template
1. Edit `templates/report_template.jinja2`
2. Add new sections or metrics
3. Re-generate report

---

## Troubleshooting

### "spaCy model not found"
**Solution**: Run `python -m spacy download en_core_web_sm`

### "Playwright browsers not installed"
**Solution**: Run `playwright install chromium`

### "LinkedIn login keeps failing"
**Issue**: 2FA enabled or wrong credentials
**Solution**:
1. Disable 2FA temporarily
2. Check credentials in Keyring
3. Try manual login first

### "CAPTCHA appears every time"
**Issue**: IP flagged for bot activity
**Solution**:
1. Reduce rate limit in settings.yaml
2. Add random delays
3. Try different IP/VPN

### "No skills extracted from JD"
**Issue**: JD uses non-standard terminology
**Solution**: Add synonyms to `skill_taxonomy.yaml`

---

## Maintenance

### Update Skill Taxonomy
- Add new skills as market evolves
- Review "Uncategorized" skills
- Merge synonyms

### Clean Old Data
- Archive JDs older than 90 days
- Prune matches.json

### Monitor Performance
- Check pipeline time stays < 10 min
- Profile spaCy processing if slow

---

## Version History

- **v1.0.0**: Initial release with Playwright, spaCy, weighted scoring, Jinja2 reports

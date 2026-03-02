# Business Avengers

## Purpose

AI partner organization for solo entrepreneurs. 23 AI agents + You as CEO (24 roles) that plan, research, design, develop, market, monetize, grow, automate, and exit your online service from idea to acquisition — with sprint cycles for continuous improvement. Powered by the MAKE (Indie Maker Handbook) methodology for the complete business lifecycle.

## Trigger Phrases

**English:**
- "business avengers"
- "/business-avengers"
- "start a business"
- "build a service"
- "launch a product"

**Korean:**
- "business avengers (Korean)"
- "start a business (Korean)"
- "build a service (Korean)"
- "launch a product (Korean)"

## Model Selection

- **Recommended**: `claude-opus-4-6` for orchestration (strategic decision routing)
- **Agents**: `claude-sonnet-4-5` for all 23 AI agents (quality + speed balance)

## Algorithm

### Step 0: Resolve Plugin Directory

Before executing any step, resolve the plugin root directory:

```python
# The SKILL.md is loaded from ~/.claude/skills/business-avengers/SKILL.md (symlink)
# Resolve the actual plugin root by following the symlink
SKILL_PATH = Bash("readlink ~/.claude/skills/business-avengers").strip()
# SKILL_PATH = .../plugins/business-avengers/skills/business-avengers
PLUGIN_DIR = SKILL_PATH + "/../.."  # Go up 2 levels to plugin root

# Alternatively, use Glob to find the plugin root:
# PLUGIN_DIR = Glob("**/plugins/business-avengers/config/init-project.py")[0].replace("/config/init-project.py", "")

# Set derived paths
TEMPLATE_DIR = f"{PLUGIN_DIR}/templates"
KNOWLEDGE_DIR = f"{PLUGIN_DIR}/knowledge"
AGENTS_DIR = f"{PLUGIN_DIR}/agents"
CONFIG_DIR = f"{PLUGIN_DIR}/config"
```

### Step 1: Parse Command & Determine Mode

Parse the user's trigger to determine operating mode:

```
INPUT PATTERNS:
  /business-avengers new "{idea}"                    → ORCHESTRA mode (idea-first)
  /business-avengers new --mode market-first "{q}"   → ORCHESTRA mode (market-first)
  /business-avengers new --mode mvp-build "{idea}"   → ORCHESTRA mode (mvp-build)
  /business-avengers phase {phase-name}              → SINGLE PHASE mode
  /business-avengers sprint "{goal}"                 → SPRINT mode
  /business-avengers ask {agent} "{question}"        → ASK mode
  /business-avengers status                          → STATUS mode
  /business-avengers resume                          → RESUME mode
  /business-avengers history                         → HISTORY mode
  "business avengers" + free text                      → ORCHESTRA mode (detect intent)
```

**Set mode variables:**
```python
is_sprint = (mode == "SPRINT")
sprint_goal = user_input if is_sprint else ""

# H5: Extract project_slug for non-ORCHESTRA modes (skip Step 2)
# For SPRINT: /business-avengers sprint "{goal}" — ask if not in command
# For SINGLE PHASE: /business-avengers phase {phase-name} — ask if not in command
# For RESUME: /business-avengers resume — ask if not in command
if mode in ["SPRINT", "SINGLE_PHASE", "RESUME"]:
    project_slug = extract_from_command(user_input) or AskUserQuestion(
        "Which project would you like to work on? (enter slug, e.g.: my-app)",
        allow_freeform=true
    )
    current_version = "v1.0"  # H4: default; updated from project.yaml in Step 3
```

**Mode routing:**
- If mode = STATUS → Go to Step 17
- If mode = HISTORY → Go to Step 18
- If mode = ASK → Go to Step 19
- If mode = RESUME → Go to Step 3 (load project, continue from last phase)
- If mode = SINGLE PHASE → Go to Step 3 (load project, run specific phase)
- If mode = SPRINT → Go to Step 3 (load project, enter sprint mode)
- If mode = ORCHESTRA → Go to Step 2

---

### Step 2: Initialize New Project

```python
# 2.1 Get project name from user if not provided
AskUserQuestion(
  "Please name your project. (e.g.: 'Food Review Curation App')",
  options=["Enter manually"],
  allow_freeform=true
)

# 2.2 Generate slug from name
project_slug = slugify(project_name)  # "food-review-curation"

# 2.3 Select workflow mode
if not specified:
  AskUserQuestion(
    "Which mode would you like to start with?",
    options=[
      "Idea First (Recommended) - use this mode if you already have an idea",
      "Market First - explore market opportunities first",
      "MVP Build - move fast with minimum viable features",
      "Indie Maker Mode - move fast with minimum steps (Idea→Market→Launch→Monetize→Growth→Automate) | Powered by MAKE methodology",
      "Full Lifecycle - all 13 phases from idea to acquisition",
      "Post-Launch - growth/automation/exit strategy for an already launched service",
      "Custom - select phases manually"
    ]
  )

# 2.4 Post-launch onboarding: collect existing service context (UX2)
if workflow_mode == "post-launch":
    """
    [COO] You are in Post-Launch mode. We will continue with growth/automation/exit phases for your already launched service.
    Please provide information about your existing service so agents can build strategies with accurate context.
    """
    AskUserQuestion("Please share your service URL.", allow_freeform=true)
    service_url = last_answer
    AskUserQuestion("Please briefly describe the 3 main features of your service.", allow_freeform=true)
    service_features = last_answer
    AskUserQuestion("What is your current monthly revenue (or earnings)?", allow_freeform=true)
    service_revenue = last_answer
    AskUserQuestion("What is your current active user count (MAU/DAU)?", allow_freeform=true)
    service_users = last_answer
    AskUserQuestion("Please briefly describe your current tech stack.", allow_freeform=true)
    service_tech = last_answer

    # Generate bootstrap context documents as substitutes for Phase 0-9 outputs
    Task(
        subagent_type="product-manager",
        model="sonnet",
        description="Generate post-launch context documents",
        prompt=f"""
        You are Business Avengers' Product Manager.
        Generate context documents for the existing service entering Post-Launch mode.

        Service information:
        - URL: {service_url}
        - Main features: {service_features}
        - Monthly revenue/earnings: {service_revenue}
        - Active users: {service_users}
        - Tech stack: {service_tech}

        Task:
        1. Read template: {TEMPLATE_DIR}/idea-canvas.md
        2. Write the idea-canvas based on the above information (used as a PRD substitute)
        3. Save with Write:
           - {PROJECT_DIR}/phase-0-ideation/idea-canvas.md
           - Save the same content to {PROJECT_DIR}/phase-2-product-planning/prd.md as well (referenced by phases 10-11)
        """
    )

# 2.5 Initialize project
Bash("python3 {PLUGIN_DIR}/config/init-project.py create '{project_name}' '{project_slug}' '{workflow_mode}'")
```

**Variables set:**
```
# PLUGIN_DIR, TEMPLATE_DIR, KNOWLEDGE_DIR, AGENTS_DIR, CONFIG_DIR → resolved in Step 0
PROJECT_DIR = ~/.business-avengers/projects/{project_slug}
current_version = "v1.0"  # H4: initial version for backup filenames
```

---

### Step 3: Load Existing Project

```python
# Load project.yaml (init-project.py outputs JSON to stdout)
result = Bash("python3 {CONFIG_DIR}/init-project.py load '{project_slug}'")
# result is JSON: {"status": "loaded", "data": {...}} or {"status": "not_found", ...}

# Handle project not found
if "not_found" in result:
  AskUserQuestion(
    f"Project '{project_slug}' could not be found.",
    options=["Create new project → Go to Step 2", "Enter a different project name"]
  )

# Extract project data from JSON output
project = result  # The JSON data from init-project.py

# Determine which phases to run based on mode:
if mode == ORCHESTRA:
  phases_to_run = WORKFLOW_PRESETS[workflow_mode]
  # UX4: Inform CEO about skipped phases for non-linear presets
  if workflow_mode == "make":
      """
      [CPO] Starting in Indie Maker mode.
      Taking the lean path — skipping Phase 2(PRD), 3(Design), 4(Tech Planning), 5(Dev Guide), 6(QA), 9(Operations)
      and proceeding in order: Phase 0→1→7→8→10→11. (This is not an error.)
      If PRD does not exist, Idea Canvas will be used as a substitute.
      """
  elif workflow_mode == "post-launch":
      """
      [COO] You are in Post-Launch mode.
      Proceeding through Phase 10→11→12 without Phase 0-9 outputs from the existing service.
      Service information entered during onboarding will be used as context.
      """
  elif workflow_mode == "mvp-build":
      """
      [CPO] You are in MVP Build mode.
      Proceeding in order: Phase 0→2→4→5→7.
      Skipping Phase 1(Market Research), 3(Design), 6(QA), 8-12. (This is not an error.)
      """
elif mode == SINGLE_PHASE:
  # M8: Bounds check for phase number
  if requested_phase_number not in range(0, 13):
      """
      [COO] Error: Phase number must be between 0 and 12.
      Requested Phase: {requested_phase_number}
      Supported Phases: 0(Ideation), 1(Market Research), 2(Product Planning), 3(Design),
                        4(Tech Planning), 5(Dev Guide), 6(QA), 7(GTM), 8(Monetization),
                        9(Operations), 10(Growth), 11(Automation), 12(Scale/Exit)
      """
  else:
      phases_to_run = [requested_phase_number]
elif mode == SPRINT:
  # Ask CEO which phases need updating (UX5: all 13 phases, grouped, terminology unified)
  AskUserQuestion(
    "Which phases need to be updated in this sprint?\n"
    "📋 Planning: Phase 0(Ideation), 1(Market Research), 2(PRD)\n"
    "🎨 Development: Phase 3(Design), 4(Tech Planning), 5(Dev Guide), 6(QA)\n"
    "🚀 Launch: Phase 7(GTM), 8(Monetization), 9(Operations)\n"
    "📈 Growth: Phase 10(Growth), 11(Automation), 12(Scale/Exit)",
    options=[
      "Phase 0 Update - Idea Canvas",
      "Phase 1 Update - Market Research (Market Analysis, Competitors, Revenue Model)",
      "Phase 2 Update - PRD / Feature Priority",
      "Phase 3 Update - Design System / Wireframes",
      "Phase 4 Update - Tech Architecture / API / DB",
      "Phase 5 Update - Dev Guide / Deployment Strategy",
      "Phase 6 Update - Test Plan / QA Checklist",
      "Phase 7 Update - GTM Strategy / Content Plan",
      "Phase 8 Update - Pricing Strategy / Financial Projections",
      "Phase 9 Update - CS Playbook / Metrics",
      "Phase 10 Update - Growth Strategy / Organic Growth",
      "Phase 11 Update - Automation Audit / Robot Specs",
      "Phase 12 Update - Scale vs Exit Analysis"
    ],
    multiSelect=true
  )
  phases_to_run = selected_phases
elif mode == RESUME:
  # I8: Load workflow from saved project data (workflow variable not defined in Step 3 otherwise)
  workflow = WORKFLOW_PRESETS.get(project.workflow_mode, WORKFLOW_PRESETS["idea-first"])
  # Find first incomplete phase
  phases_to_run = [p for p in workflow if project.phases[p].status != "completed"]
```

**Phase Execution Loop (I10):**
```
# Execute each phase in phases_to_run in order.
# For each phase N in phases_to_run, execute the corresponding Step:
#   Phase 0  → Step 4    Phase 1  → Step 5    Phase 2  → Step 6    Phase 3  → Step 7
#   Phase 4  → Step 8    Phase 5  → Step 9    Phase 6  → Step 10   Phase 7  → Step 11
#   Phase 8  → Step 12   Phase 9  → Step 13   Phase 10 → Step 14   Phase 11 → Step 15
#   Phase 12 → Step 16
#
# After completing all phases in phases_to_run (I11 - completion routing):
#   If is_sprint: Go to Step 20 (Sprint Completion)
#   If mode == ORCHESTRA: Go to Step 21 (Project Completion)
#   Otherwise: Display summary of completed phases and return.
```

---

### Step 4: Execute Phase 0 - Ideation

**Condition**: Only runs if Phase 0 is in phases_to_run

**Lead**: CPO + Product Manager
**CEO Interaction**: Dialogue (interactive Q&A or document input)

```python
# 4.1 CPO introduces the ideation process
# Display as CPO speaking:
"""
[CPO] Hello, CEO. Let's start a new project.
"""

# 4.2a Market-first: read Phase 1 outputs to provide market context during ideation (M7)
market_first_context = ""
if workflow_mode == "market-first":
    mkt_f = Glob("{PROJECT_DIR}/phase-1-market-research/market-analysis.md")
    comp_f = Glob("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md")
    rev_f = Glob("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md")
    if mkt_f or comp_f or rev_f:
        market_first_context = (
            "Market research results (refer to these when refining your idea):\n"
            + (f"Market Analysis:\n{Read(mkt_f[0])}\n" if mkt_f else "")
            + (f"Competitive Analysis:\n{Read(comp_f[0])}\n" if comp_f else "")
            + (f"Revenue Model Draft:\n{Read(rev_f[0])}\n" if rev_f else "")
        )

# 4.2 Sprint mode: backup existing idea-canvas before overwriting
sprint_context = ""
if is_sprint:
    existing = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
    if existing:
        Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-0-ideation idea-canvas.md {current_version}")
        existing_canvas = Read(existing[0])
        sprint_context = f"Update the existing Idea Canvas. Change goal: {sprint_goal}\nExisting content:\n{existing_canvas}"

# 4.3 Document availability check — ask BEFORE starting Q&A
has_doc = AskUserQuestion(
  "[CPO] Do you have any documents or notes where you've already organized your idea?",
  options=[
    "Yes - I'll provide the file path or content directly",
    "No - let's organize it together with Q&A"
  ]
)

if "Yes" in has_doc:
    # 4.3a Document input flow: get file path or pasted text
    idea_input = AskUserQuestion(
        "[CPO] Please paste the file path (.md/.txt, etc.) or the content directly.",
        allow_freeform=True
    )
    # Smart detection: file path (contains "/" and ends with extension) vs pasted text
    stripped = idea_input.strip()
    is_file_path = ("/" in stripped or "\\" in stripped) and any(
        stripped.endswith(ext) for ext in (".md", ".txt", ".pdf", ".docx")
    )
    if is_file_path:
        doc_files = Glob(stripped)
        idea_doc = Read(doc_files[0]) if doc_files else stripped  # fallback to treating as text if not found
        if not doc_files:
            """[CPO] File not found — treating the input as plain text."""
    else:
        idea_doc = stripped  # treat as pasted content

    all_qa_responses = f"[CEO-provided idea document]\n{idea_doc}"

else:
    # 4.3b Interactive Q&A flow (original behavior)
    """[CPO] I'll ask you a few questions to help refine your idea."""
    questions = [
      "What specific problem does this service solve?",
      "Who are the main target users? (age, occupation, situation, etc.)",
      "How are users currently solving this problem? (existing alternatives)",
      "What is the core differentiation of our service compared to existing alternatives?",
      "How do you expect to generate the first revenue?",
    ]

    for q in questions:
      AskUserQuestion(q, allow_freeform=True)

    # all_qa_responses is collected from the Q&A above

# 4.4 Product Manager synthesizes into Idea Canvas
Task(
  subagent_type="product-manager",
  model="sonnet",
  description="Create Idea Canvas",
  prompt=f"""
  You are Business Avengers' Product Manager.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/product-manager.md

  Conversation with CEO:
  {all_qa_responses}

  {market_first_context}

  {sprint_context}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/extended/problem-validation-deep.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 0 section)

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read problem-validation-deep.md — apply Mom Test and JTBD criteria to the problem framing
  3. Read template: {TEMPLATE_DIR}/idea-canvas.md
  4. Apply Mom Test: problem framing must contain zero solution language — specific person + specific situation + quantified pain
  5. Write JTBD statement: "When [X], I want [Y], so I can [Z]"
  6. Include revenue hypothesis with basis (comparable product price, interview signal, or cost-of-current-solution)
  7. List ≥3 core assumptions with validation methods in an Assumption Register
  8. State "Why Now" if applicable (technology / regulatory / behavioral trigger)
  9. Check phase-rubrics.md Phase 0 checklist, fix any unmet items
  10. Add Quality Self-Assessment block at top of output
  11. Save with Write: {PROJECT_DIR}/phase-0-ideation/idea-canvas.md

  Write professionally and concretely. No vague expressions.
  """
)

# 4.4 Present to CEO for approval
idea_canvas = Read("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
# Display idea canvas content to CEO

gate_0 = AskUserQuestion(
  "[CPO] Please review the Idea Canvas. How would you like to proceed?",
  options=[
    "Approve - proceed to the next step",
    "Request revision - rework after incorporating feedback",
    "Stop - put the project on hold"
  ]
)

if "Approve" in gate_0:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 0 completed {current_version}")
elif "Request revision" in gate_0:
    revision_feedback = AskUserQuestion("Which parts should be revised? Please be specific.", allow_freeform=true)
    # INSTRUCTION: Re-run the Product Manager Task() from step 4.4 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
    # After re-run, loop back to this gate.
elif "Stop" in gate_0:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 0 cancelled {current_version}")
    # Exit pipeline - no further phases
```

---

### Step 5: Execute Phase 1 - Market Research

**Condition**: Only runs if Phase 1 is in phases_to_run

**Lead**: CFO
**Agents**: business-analyst + marketing-strategist + revenue-strategist (PARALLEL)
**CEO Interaction**: Approve

```python
# 5.1 Read previous phase outputs for context (check existence with Glob first)
idea_canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
idea_canvas = Read(idea_canvas_files[0]) if idea_canvas_files else ""

# 5.2 Sprint mode: read existing docs for update context
sprint_context_market = ""
sprint_context_competitive = ""
sprint_context_revenue = ""
if is_sprint:
  existing_files = Glob("{PROJECT_DIR}/phase-1-market-research/*.md")
  if existing_files:
    # Backup all 3 files before overwriting (H3)
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-1-market-research market-analysis.md {current_version}")
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-1-market-research competitive-analysis.md {current_version}")
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-1-market-research revenue-model-draft.md {current_version}")
    market_f = Glob("{PROJECT_DIR}/phase-1-market-research/market-analysis.md")
    existing_market = Read(market_f[0]) if market_f else ""
    competitive_f = Glob("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md")
    existing_competitive = Read(competitive_f[0]) if competitive_f else ""
    revenue_f = Glob("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md")
    existing_revenue = Read(revenue_f[0]) if revenue_f else ""
    sprint_context_market = f"Update the existing document. Change goal: {sprint_goal}\nExisting content:\n{existing_market}"
    sprint_context_competitive = f"Update the existing document. Change goal: {sprint_goal}\nExisting content:\n{existing_competitive}"
    sprint_context_revenue = f"Update the existing document. Change goal: {sprint_goal}\nExisting content:\n{existing_revenue}"

# 5.3 Launch 3 agents in PARALLEL (CRITICAL: all in single response block)
Task(
  subagent_type="business-analyst",
  model="sonnet",
  description="Market size analysis",
  prompt=f"""
  You are Business Avengers' Business Analyst.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/business-analyst.md

  Project Context:
  {idea_canvas}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/business-models.md
  - {KNOWLEDGE_DIR}/startup-best-practices.md
  - {KNOWLEDGE_DIR}/extended/market-research-advanced.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 1 section)

  Template (Read this file):
  - {TEMPLATE_DIR}/market-analysis.md

  Task:
  1. Read market-research-advanced.md to internalize the Why Now framework and Beachhead criteria
  2. Use WebSearch to research real market data (Tier 1/2 sources: Gartner, Forrester, IDC, etc.)
     - Required query: "[industry] market size [year] billion"
     - Required query: "[industry] CAGR forecast 2024 2025 2026"
     - Required query: "[industry] growth drivers regulatory trends [year]"
  3. Estimate TAM/SAM/SOM (must include at least 2 external source URLs)
  4. Write the "Why Now" section: specify the relevant technology/regulatory/behavioral changes
  5. Define the Beachhead market: "[country], [occupation/industry], [size] — approx. X reachable customers"
  6. Add a reverse-calculation validation for SOM Year 3: target $XM ÷ ACV $Y = Z customers needed
  7. Check the Phase 1 checklist in phase-rubrics.md and fix any unmet items
  8. Add a Quality Self-Assessment block at the very top of the output
  9. Fill the template and save with Write: {PROJECT_DIR}/phase-1-market-research/market-analysis.md

  {sprint_context_market}
  Cite a source URL for every key figure. The output is incomplete without Why Now and Beachhead.
  """
)

Task(
  subagent_type="marketing-strategist",
  model="sonnet",
  description="Competitive analysis",
  prompt=f"""
  You are Business Avengers' Marketing Strategist.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/marketing-strategist.md

  Project Context:
  {idea_canvas}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/marketing-playbooks.md

  Template (Read this file):
  - {TEMPLATE_DIR}/competitive-analysis.md

  Task:
  1. Use WebSearch + WebFetch to research 5 competitors
  2. Analyze each competitor's features, pricing, and strengths/weaknesses
  3. Write a SWOT analysis and positioning map
  4. Fill the template and save with Write: {PROJECT_DIR}/phase-1-market-research/competitive-analysis.md

  {sprint_context_competitive}
  Include real URLs and data.
  """
)

Task(
  subagent_type="revenue-strategist",
  model="sonnet",
  description="Revenue model analysis",
  prompt=f"""
  You are Business Avengers' Revenue Strategist.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/revenue-strategist.md

  Project Context:
  {idea_canvas}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/business-models.md
  - {KNOWLEDGE_DIR}/pricing-strategies.md

  Template (Read this file):
  - {TEMPLATE_DIR}/revenue-model-draft.md

  Task:
  1. Use WebSearch to research the pricing policies of similar services
  2. Propose 3-5 revenue models
  3. Analyze the expected revenue, pros and cons of each model
  4. Present the recommended model with rationale
  5. Fill the template and save with Write: {PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md

  {sprint_context_revenue}
  """
)

# 5.4 Wait for all agents, then present summary to CEO
market = Read("{PROJECT_DIR}/phase-1-market-research/market-analysis.md")
competitive = Read("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md")
revenue = Read("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md")

# Display summary
"""
[CFO] Here is the market research report:

📊 Market Analysis: {market_summary}
🏢 Competitive Analysis: {competitive_summary}
💰 Revenue Model: {revenue_summary}

Detailed documents have been saved to the project folder.
"""

gate_1 = AskUserQuestion(
  "[CFO] Please review the market research results.",
  options=[
    "Approve - market validated, proceed to next step",
    "Request revision - additional research needed",
    "Pivot - change direction (back to Phase 0)",
    "Stop - insufficient market viability"
  ]
)

if "Approve" in gate_1:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 1 completed {current_version}")
elif "Request revision" in gate_1:
    revision_feedback = AskUserQuestion("What areas need additional research?", allow_freeform=true)
    # INSTRUCTION: Re-run the 3 Phase 1 agents from step 5.3 above,
    # setting sprint_context_* = f"CEO revision feedback: {revision_feedback}"
    # After re-run, loop back to this gate.
elif "Pivot" in gate_1:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 1 revision {current_version}")
    # Return to Phase 0 - re-run Ideation (Step 4)
elif "Stop" in gate_1:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 1 cancelled {current_version}")
    # Exit pipeline
```

---

### Step 6: Execute Phase 2 - Product Planning

**Condition**: Only runs if Phase 2 is in phases_to_run
**Lead**: CPO
**Agents**: product-manager + ux-researcher (PARALLEL → synthesis)

```python
# 6.1 Read all previous phase outputs for context
idea_canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
idea_canvas = Read(idea_canvas_files[0]) if idea_canvas_files else ""
market_files = Glob("{PROJECT_DIR}/phase-1-market-research/*.md")
market_analysis = Read("{PROJECT_DIR}/phase-1-market-research/market-analysis.md") if market_files else ""
competitive = Read("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md") if market_files else ""
revenue_draft = Read("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md") if market_files else ""

# 6.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-2-product-planning/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-2-product-planning prd.md {current_version}")
    existing_prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting PRD:\n{existing_prd}"

# 6.3 Launch 2 agents in PARALLEL
Task(
  subagent_type="product-manager",
  model="sonnet",
  description="Write PRD, user stories, feature priority",
  prompt=f"""
  You are Business Avengers' Product Manager.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/product-manager.md

  Project Context:
  - Idea Canvas: {idea_canvas}
  - Market Analysis: {market_analysis}
  - Competitive Analysis: {competitive}
  - Revenue Model Draft: {revenue_draft}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/startup-best-practices.md

  Template (Read these files):
  - {TEMPLATE_DIR}/prd.md
  - {TEMPLATE_DIR}/user-stories.md
  - {TEMPLATE_DIR}/feature-priority.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read the Knowledge Base for reference
  3. Write the PRD incorporating market analysis findings
  4. Write User Stories following the INVEST principle
  5. Organize feature priority using the MoSCoW framework
  6. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-2-product-planning/prd.md
     - {PROJECT_DIR}/phase-2-product-planning/user-stories.md
     - {PROJECT_DIR}/phase-2-product-planning/feature-priority.md
  """)

Task(
  subagent_type="ux-researcher",
  model="sonnet",
  description="Create user personas",
  prompt=f"""
  You are Business Avengers' UX Researcher.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/ux-researcher.md

  Project Context:
  - Idea Canvas: {idea_canvas}
  - Market Analysis: {market_analysis}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/ux-principles.md

  Template (Read this file):
  - {TEMPLATE_DIR}/user-personas.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Use WebSearch to research the target users
  3. Write 2-3 detailed personas (name, age, occupation, goals, pain points, scenarios)
  4. Include a user journey map for each persona
  5. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-2-product-planning/user-personas.md
  """)

# 6.4 CEO reviews PRD + does MoSCoW prioritization
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")
personas = Read("{PROJECT_DIR}/phase-2-product-planning/user-personas.md")

gate_2 = AskUserQuestion(
  "[CPO] Please review the PRD and feature priority.",
  options=[
    "Approve - proceed to the next step",
    "Request revision - rework after incorporating feedback",
    "Pivot - change direction"
  ]
)

if "Approve" in gate_2:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 2 completed {current_version}")
elif "Request revision" in gate_2:
    revision_feedback = AskUserQuestion("Which parts should be revised? (feature scope, priority, personas, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run Phase 2 agents from step 6.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
    # After re-run, loop back to this gate.
elif "Pivot" in gate_2:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 2 revision {current_version}")
    # Return to Phase 0 - re-run Ideation (Step 4)
```

---

### Step 7: Execute Phase 3 - Design

**Condition**: Only runs if Phase 3 is in phases_to_run
**Lead**: CPO (Design Lead)
**Agents**: design-lead → ui-designer (SEQUENTIAL)

```python
# 7.1 Read previous phase outputs
prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
if prd_files:
    prd = Read(prd_files[0])
else:
    canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
    prd = Read(canvas_files[0]) if canvas_files else ""
personas_files = Glob("{PROJECT_DIR}/phase-2-product-planning/user-personas.md")
personas = Read(personas_files[0]) if personas_files else ""

# 7.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-3-design/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-3-design design-system.md {current_version}")
    existing_design = Read("{PROJECT_DIR}/phase-3-design/design-system.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting design system:\n{existing_design}"

# 7.3 SEQUENTIAL: Design Lead FIRST, then UI Designer
Task(
  subagent_type="design-lead",
  model="sonnet",
  description="Create design system",
  prompt=f"""
  You are Business Avengers' Design Lead.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/design-lead.md

  Project Context:
  - PRD: {prd}
  - Personas: {personas}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/ux-principles.md
  - {KNOWLEDGE_DIR}/extended/design-advanced.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 3 section)

  Template (Read this file):
  - {TEMPLATE_DIR}/design-system.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read design-advanced.md — apply Nielsen's 10 heuristics, conversion design patterns, and state design standards
  3. Design a design system suited to the service's characteristics (all 9 required elements)
  4. Define color tokens, typography scale (6+ levels with exact px), 8px spacing system, component states
  5. Incorporate accessibility (WCAG 2.1 AA) — document contrast ratios for all text/background combos
  6. Design empty states, error states, and loading states for all data-dependent screens
  7. Check phase-rubrics.md Phase 3 checklist, fix any unmet items
  8. Add Quality Self-Assessment block at top of output
  9. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-3-design/design-system.md
  """)

# 7.4 WAIT for design-lead, then read output for ui-designer
design_system = Read("{PROJECT_DIR}/phase-3-design/design-system.md")

Task(
  subagent_type="ui-designer",
  model="sonnet",
  description="Create wireframes and UI specs",
  prompt=f"""
  You are Business Avengers' UI Designer.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/ui-designer.md

  Project Context:
  - PRD: {prd}
  - Personas: {personas}
  - Design System: {design_system}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/ux-principles.md
  - {KNOWLEDGE_DIR}/extended/design-advanced.md

  Template (Read these files):
  - {TEMPLATE_DIR}/wireframes.md
  - {TEMPLATE_DIR}/ui-specifications.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read design-advanced.md — apply friction audit methodology and conversion CTA standards
  3. Create wireframes for key screens based on the design system
  4. For each screen: verify empty state, error state, and loading state are designed
  5. Apply above-the-fold standard for landing/marketing screens: headline + CTA + trust signal visible
  6. Define component specs and interaction patterns for each screen
  7. Verify all core features from PRD are reflected in wireframes
  8. Add Quality Self-Assessment block at top of output
  9. Fill in {{PLACEHOLDER}} in the templates and save with Write:
     - {PROJECT_DIR}/phase-3-design/wireframes.md
     - {PROJECT_DIR}/phase-3-design/ui-specifications.md
  """)

# 7.5 CEO reviews design
gate_3 = AskUserQuestion(
  "[CPO] Please review the design system and wireframes.",
  options=[
    "Approve - proceed to the next step",
    "Request revision - rework after incorporating feedback",
    "Pivot - change direction"
  ]
)

if "Approve" in gate_3:
    pass  # proceed to update-phase below
elif "Request revision" in gate_3:
    revision_feedback = AskUserQuestion("Which parts should be revised? (design system, wireframes, UI components, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run Design Lead and UI Designer Tasks from step 7.3-7.4 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
    # After re-run, loop back to this gate.
elif "Pivot" in gate_3:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 3 revision {current_version}")
    # Return to Phase 0

Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 3 completed v1.0")
```

---

### Step 8: Execute Phase 4 - Technical Planning

**Condition**: Only runs if Phase 4 is in phases_to_run
**Lead**: CTO
**Agents**: tech-lead (single)
**CEO Interaction**: Delegate + Report (CTO makes decisions)

```python
# 8.1 Read previous phase outputs
prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
if prd_files:
    prd = Read(prd_files[0])
else:
    canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
    prd = Read(canvas_files[0]) if canvas_files else ""
ui_specs_files = Glob("{PROJECT_DIR}/phase-3-design/ui-specifications.md")
ui_specs = Read(ui_specs_files[0]) if ui_specs_files else ""

# 8.2 Sprint mode
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-4-tech-planning/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-4-tech-planning tech-architecture.md {current_version}")
    existing_arch = Read("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting architecture:\n{existing_arch}"

# 8.3 Tech Lead designs architecture
Task(
  subagent_type="tech-lead",
  model="sonnet",
  description="Design technical architecture",
  prompt=f"""
  You are Business Avengers' Tech Lead.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/tech-lead.md

  Project Context:
  - PRD: {prd}
  - UI Specs: {ui_specs}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md
  - {KNOWLEDGE_DIR}/extended/tech-architecture-advanced.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 4 section)

  Template (Read these files):
  - {TEMPLATE_DIR}/tech-architecture.md
  - {TEMPLATE_DIR}/api-design.md
  - {TEMPLATE_DIR}/database-schema.md
  - {TEMPLATE_DIR}/tech-stack-decision.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read tech-architecture-advanced.md — apply boring tech principle, ADR format, and OWASP security checklist
  3. Apply stack selection decision tree: use known tech unless switching saves >40 hours
  4. Write ≥5 ADRs (frontend, backend, database, auth, hosting) with Context → Decision → Rationale → Alternatives
  5. Design system architecture based on PRD functional requirements (C4 Context + Container diagrams)
  6. Design RESTful API with consistent error format and versioning
  7. Design database schema with indexes and constraint rationale
  8. Address all 10 OWASP categories (status: addressed / not applicable / deferred)
  9. Perform no-code/low-code assessment for each core feature
  10. Check phase-rubrics.md Phase 4 checklist, fix any unmet items
  11. Add Quality Self-Assessment block at top of each output
  12. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md
     - {PROJECT_DIR}/phase-4-tech-planning/api-design.md
     - {PROJECT_DIR}/phase-4-tech-planning/database-schema.md
     - {PROJECT_DIR}/phase-4-tech-planning/tech-stack-decision.md
  """)

# 8.4 CTO reports to CEO (lighter review - delegate level)
tech_arch = Read("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")

"""
[CTO] Technical design is complete. Please check the project folder for details.
"""

gate_4 = AskUserQuestion("[CTO] Technical design report. Please review.",
  options=["Confirm - proceed", "I have a question", "Request revision"])

if "I have a question" in gate_4:
    follow_up = AskUserQuestion("What would you like to know? Please enter your question about the technical design.", allow_freeform=true)
    # Display relevant section from tech_arch / api_design / database-schema based on follow_up
elif "Request revision" in gate_4:
    revision_feedback = AskUserQuestion("Which parts should be revised? (architecture, API, DB schema, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run Tech Lead Task from step 8.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 4 completed {current_version}")
```

---

### Step 9: Execute Phase 5 - Development Guide

**Condition**: Only runs if Phase 5 is in phases_to_run
**Lead**: CTO
**Agents**: frontend-dev + backend-dev + devops-engineer (PARALLEL)
**CEO Interaction**: Delegate + Report (CTO manages)

```python
# 9.1 Read previous phase outputs
tech_arch_files = Glob("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")
tech_arch = Read(tech_arch_files[0]) if tech_arch_files else ""
api_design_files = Glob("{PROJECT_DIR}/phase-4-tech-planning/api-design.md")
api_design = Read(api_design_files[0]) if api_design_files else ""
db_schema_files = Glob("{PROJECT_DIR}/phase-4-tech-planning/database-schema.md")
db_schema = Read(db_schema_files[0]) if db_schema_files else ""
ui_specs_files = Glob("{PROJECT_DIR}/phase-3-design/ui-specifications.md")
ui_specs = Read(ui_specs_files[0]) if ui_specs_files else ""
prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
if prd_files:
    prd = Read(prd_files[0])
else:
    canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
    prd = Read(canvas_files[0]) if canvas_files else ""

# 9.2 Sprint mode: backup existing docs (I3: per-agent sprint_context with existing content)
sprint_context = ""
sprint_context_frontend = ""
sprint_context_backend = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-5-development/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-5-development frontend-guide.md {current_version}")
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-5-development backend-guide.md {current_version}")
    frontend_f = Glob("{PROJECT_DIR}/phase-5-development/frontend-guide.md")
    existing_frontend = Read(frontend_f[0]) if frontend_f else ""
    backend_f = Glob("{PROJECT_DIR}/phase-5-development/backend-guide.md")
    existing_backend = Read(backend_f[0]) if backend_f else ""
    sprint_context_frontend = f"Update the existing document. Change goal: {sprint_goal}\nExisting frontend guide:\n{existing_frontend}"
    sprint_context_backend = f"Update the existing document. Change goal: {sprint_goal}\nExisting backend guide:\n{existing_backend}"
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}"  # for devops

# 9.3 Launch 3 agents in PARALLEL (CRITICAL: all in single response block)
Task(
  subagent_type="frontend-dev",
  model="sonnet",
  description="Frontend implementation guide",
  prompt=f"""
  You are Business Avengers' Frontend Developer.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/frontend-dev.md

  Project Context:
  - PRD: {prd}
  - Tech Architecture: {tech_arch}
  - UI Specs: {ui_specs}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  Template (Read this file):
  - {TEMPLATE_DIR}/frontend-guide.md

  {sprint_context_frontend}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Confirm the frontend stack selected in the tech architecture
  3. Design the project structure (directory and file organization)
  4. Define the list of core components and the role of each component
  5. Design state management strategy, routing, and API communication patterns
  6. Break down each screen from the UI specs into components
  7. Include performance optimization strategies (code splitting, lazy loading, etc.)
  8. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-5-development/frontend-guide.md
  """)

Task(
  subagent_type="backend-dev",
  model="sonnet",
  description="Backend implementation guide",
  prompt=f"""
  You are Business Avengers' Backend Developer.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/backend-dev.md

  Project Context:
  - PRD: {prd}
  - Tech Architecture: {tech_arch}
  - API Design: {api_design}
  - DB Schema: {db_schema}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  Template (Read this file):
  - {TEMPLATE_DIR}/backend-guide.md

  {sprint_context_backend}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Confirm the backend stack selected in the tech architecture
  3. Design the project structure (directory, modules, layers)
  4. Write implementation guides per API endpoint (controller, service, repository)
  5. Describe the authentication/authorization implementation strategy in detail
  6. Include DB migration strategy and ORM model design
  7. Define error handling, logging, and monitoring patterns
  8. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-5-development/backend-guide.md
  """)

Task(
  subagent_type="devops-engineer",
  model="sonnet",
  description="Deployment strategy and implementation roadmap",
  prompt=f"""
  You are Business Avengers' DevOps Engineer.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/devops-engineer.md

  Project Context:
  - Tech Architecture: {tech_arch}
  - PRD: {prd}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  Template (Read these files):
  - {TEMPLATE_DIR}/deployment-strategy.md
  - {TEMPLATE_DIR}/implementation-roadmap.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Design the CI/CD pipeline (build, test, deploy stages)
  3. Design the infrastructure architecture (cloud services, serverless, etc.)
  4. Define environment configuration (development/staging/production)
  5. Establish monitoring, alerting, and log management strategy
  6. Include security configuration (HTTPS, firewall, secret management)
  7. Write the full implementation roadmap in sprint units
  8. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-5-development/deployment-strategy.md
     - {PROJECT_DIR}/phase-5-development/implementation-roadmap.md
  """)

# 9.4 CTO reports to CEO (delegate level - light confirmation)
"""
[CTO] Development guide is complete:
- Frontend implementation guide
- Backend implementation guide
- Deployment strategy & implementation roadmap

Please check the project folder for details.
"""

gate_5 = AskUserQuestion("[CTO] Development guide is complete.", options=["Confirm - proceed", "I have a question", "Request revision"])

if "I have a question" in gate_5:
    follow_up = AskUserQuestion("Please enter your question about the development guide.", allow_freeform=true)
    # Display relevant section from frontend-guide / backend-guide / deployment-strategy based on follow_up
elif "Request revision" in gate_5:
    revision_feedback = AskUserQuestion("Which parts should be revised? (frontend, backend, deployment strategy, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run the relevant dev agent Task(s) from step 9.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 5 completed {current_version}")
```

---

### Step 10: Execute Phase 6 - QA Planning

**Condition**: Only runs if Phase 6 is in phases_to_run
**Lead**: CTO
**Agents**: qa-lead (single)
**CEO Interaction**: Delegate + Report

```python
# 10.1 Read previous phase outputs
prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
if prd_files:
    prd = Read(prd_files[0])
else:
    canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
    prd = Read(canvas_files[0]) if canvas_files else ""
user_stories_files = Glob("{PROJECT_DIR}/phase-2-product-planning/user-stories.md")
user_stories = Read(user_stories_files[0]) if user_stories_files else ""
tech_arch_files = Glob("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")
tech_arch = Read(tech_arch_files[0]) if tech_arch_files else ""
api_design_files = Glob("{PROJECT_DIR}/phase-4-tech-planning/api-design.md")
api_design = Read(api_design_files[0]) if api_design_files else ""
frontend_guide_files = Glob("{PROJECT_DIR}/phase-5-development/frontend-guide.md")
frontend_guide = Read(frontend_guide_files[0]) if frontend_guide_files else ""

# 10.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-6-qa/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-6-qa test-plan.md {current_version}")
    existing_test = Read("{PROJECT_DIR}/phase-6-qa/test-plan.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting test plan:\n{existing_test}"

# 10.3 QA Lead creates test plan
Task(
  subagent_type="qa-lead",
  model="sonnet",
  description="Create test plan and QA checklist",
  prompt=f"""
  You are Business Avengers' QA Lead.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/qa-lead.md

  Project Context:
  - PRD: {prd}
  - User Stories: {user_stories}
  - Tech Architecture: {tech_arch}
  - API Design: {api_design}
  - Frontend Guide: {frontend_guide}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/tech-stack-guide.md

  Template (Read these files):
  - {TEMPLATE_DIR}/test-plan.md
  - {TEMPLATE_DIR}/qa-checklist.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Derive test cases from the PRD and user stories
  3. Establish functional testing, integration testing, and E2E testing strategies
  4. Write test scenarios per API endpoint
  5. Define performance test criteria (response time, concurrent connections, etc.)
  6. Include a security test checklist (OWASP Top 10)
  7. Write the QA checklist separated into pre-launch and post-launch sections
  8. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-6-qa/test-plan.md
     - {PROJECT_DIR}/phase-6-qa/qa-checklist.md
  """)

# 10.4 CTO reports to CEO
gate_6 = AskUserQuestion("[CTO] QA plan is complete. Test plan and QA checklist have been generated.",
  options=["Confirm - proceed", "I have a question", "Request revision"])

if "I have a question" in gate_6:
    follow_up = AskUserQuestion("Please enter your question about the QA plan.", allow_freeform=true)
    # Display relevant section from test-plan / qa-checklist based on follow_up
elif "Request revision" in gate_6:
    revision_feedback = AskUserQuestion("Which parts should be revised? (test cases, performance criteria, E2E scenarios, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run QA Lead Task from step 10.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 6 completed {current_version}")
```

---

### Step 11: Execute Phase 7 - Launch Strategy

**Condition**: Only runs if Phase 7 is in phases_to_run
**Lead**: CMO
**Agents**: marketing-strategist + content-creator + growth-hacker + pr-manager (PARALLEL)
**CEO Interaction**: Strategic Approval

```python
# 11.1 Read previous phase outputs
idea_canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
idea_canvas = Read(idea_canvas_files[0]) if idea_canvas_files else ""
prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
if prd_files:
    prd = Read(prd_files[0])
else:
    prd = idea_canvas  # make/mvp-build preset fallback: use idea-canvas when PRD does not exist
personas_files = Glob("{PROJECT_DIR}/phase-2-product-planning/user-personas.md")
personas = Read(personas_files[0]) if personas_files else ""
market_analysis_files = Glob("{PROJECT_DIR}/phase-1-market-research/market-analysis.md")
market_analysis = Read(market_analysis_files[0]) if market_analysis_files else ""
competitive_files = Glob("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md")
competitive = Read(competitive_files[0]) if competitive_files else ""

# 11.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-7-launch-strategy/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-7-launch-strategy gtm-strategy.md {current_version}")
    existing_gtm = Read("{PROJECT_DIR}/phase-7-launch-strategy/gtm-strategy.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting GTM strategy:\n{existing_gtm}"

# 11.3 Launch 4 agents in PARALLEL (CRITICAL: all in single response block)
Task(
  subagent_type="marketing-strategist",
  model="sonnet",
  description="GTM strategy",
  prompt=f"""
  You are Business Avengers' Marketing Strategist.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/marketing-strategist.md

  Project Context:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - Personas: {personas}
  - Market Analysis: {market_analysis}
  - Competitive Analysis: {competitive}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/marketing-playbooks.md
  - {KNOWLEDGE_DIR}/extended/gtm-advanced.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 7 section)

  Template (Read this file):
  - {TEMPLATE_DIR}/gtm-strategy.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read gtm-advanced.md — apply Beachhead, First 1000 Users, and Repeated Launch frameworks
  3. Define ICP with specificity: role + company size + problem + buying trigger (not just "SMB")
  4. Select max 2 primary acquisition channels for 90-day focus — justify each choice
  5. Write First 100 Users plan: channel + specific tactic + target number (e.g., 40 from PH, 40 from Reddit, 20 from cold outreach)
  6. Write Pre-launch warm-up plan (≥2 weeks before launch): waitlist, community contribution, hunter identification
  7. Write the pre-launch/launch-day/post-launch timeline with launch platform rationale
  8. Plan Repeated Launch calendar: 3 milestones with re-launch venue
  9. Estimate marketing budget allocation and expected ROI
  10. Check phase-rubrics.md Phase 7 checklist, fix any unmet items
  11. Add Quality Self-Assessment block at top of output
  12. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-7-launch-strategy/gtm-strategy.md
  """)

Task(
  subagent_type="content-creator",
  model="sonnet",
  description="Content marketing plan",
  prompt=f"""
  You are Business Avengers' Content Creator.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/content-creator.md

  Project Context:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - Personas: {personas}
  - Market Analysis: {market_analysis}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/marketing-playbooks.md

  Template (Read this file):
  - {TEMPLATE_DIR}/content-plan.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Establish content strategy per persona
  3. Write a content calendar per channel (blog, social media, newsletter, video)
  4. Define core messages and tone of voice
  5. Include SEO keyword strategy
  6. Define the content creation workflow and quality standards
  7. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-7-launch-strategy/content-plan.md
  """)

Task(
  subagent_type="growth-hacker",
  model="sonnet",
  description="Growth strategy",
  prompt=f"""
  You are Business Avengers' Growth Hacker.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/growth-hacker.md

  Project Context:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - Personas: {personas}
  - Market Analysis: {market_analysis}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/growth-tactics.md
  - {KNOWLEDGE_DIR}/extended/growth-engineering.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 7 section)

  Template (Read this file):
  - {TEMPLATE_DIR}/growth-strategy.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read growth-engineering.md — apply NSM framework, growth loop selection, and Aha Moment identification
  3. Define the North Star Metric (NOT revenue, NOT signups — must capture value delivery)
  4. Identify primary growth loop type (viral / SEO content / paid / PLG) with rationale
  5. Define Aha Moment: specific user action + target timeframe (e.g., "complete first X within 7 days")
  6. Apply AARRR framework — address all 5 stages with specific tactics
  7. Design viral loop if applicable: K-factor calculation, 2-sided incentive structure
  8. Propose ≥3 ICE-scored growth experiments for first 90 days
  9. Write strategy for acquiring first 1,000 users with channel + tactic + target breakdown
  10. Check phase-rubrics.md Phase 7 checklist, fix any unmet items
  11. Add Quality Self-Assessment block at top of output
  12. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-7-launch-strategy/growth-strategy.md
  """)

Task(
  subagent_type="pr-manager",
  model="sonnet",
  description="PR plan and launch checklist",
  prompt=f"""
  You are Business Avengers' PR Manager.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/pr-manager.md

  Project Context:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - Market Analysis: {market_analysis}
  - Competitive Analysis: {competitive}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/marketing-playbooks.md

  Template (Read these files):
  - {TEMPLATE_DIR}/pr-plan.md
  - {TEMPLATE_DIR}/launch-checklist.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Establish a PR strategy (media list, press releases, interviews, etc.)
  3. Develop 3-5 launch story angles
  4. Write a media target list (journalists, bloggers, influencers)
  5. Prepare crisis response scenarios and Q&A
  6. Divide the launch checklist into D-30, D-7, D-1, D-Day, D+7
  7. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-7-launch-strategy/pr-plan.md
     - {PROJECT_DIR}/phase-7-launch-strategy/launch-checklist.md
  """)

# 11.4 CMO presents to CEO for strategic approval
"""
[CMO] Launch strategy is complete:
- GTM Strategy: marketing plan per channel
- Content Plan: content calendar and production plan
- Growth Strategy: AARRR funnel and growth hacking strategy
- PR Plan: media strategy and launch checklist

Detailed documents have been saved to the project folder.
"""

gate_7 = AskUserQuestion("[CMO] Please review the launch strategy.",
  options=["Approve - confirm launch strategy", "Request revision - incorporate feedback", "Budget adjustment needed", "Re-evaluate - reset direction"])

if "Approve" in gate_7:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 7 completed {current_version}")
elif "Request revision" in gate_7 or "Budget adjustment" in gate_7:
    revision_feedback = AskUserQuestion("Which parts should be revised? (GTM channels, content strategy, budget allocation, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run the relevant Phase 7 agent Task(s) from step 11.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
    # After re-run, loop back to this gate.
elif "Re-evaluate" in gate_7:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 7 revision {current_version}")
    # Return to Phase 0 for full re-ideation
```

---

### Step 12: Execute Phase 8 - Monetization

**Condition**: Only runs if Phase 8 is in phases_to_run
**Lead**: CFO
**Agents**: revenue-strategist + business-analyst (PARALLEL)
**CEO Interaction**: Strategic Approval (pricing decisions)

```python
# 12.1 Read previous phase outputs
idea_canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
idea_canvas = Read(idea_canvas_files[0]) if idea_canvas_files else ""
prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
if prd_files:
    prd = Read(prd_files[0])
else:
    prd = idea_canvas  # make preset fallback: use idea-canvas when PRD does not exist
market_analysis_files = Glob("{PROJECT_DIR}/phase-1-market-research/market-analysis.md")
market_analysis = Read(market_analysis_files[0]) if market_analysis_files else ""
competitive_files = Glob("{PROJECT_DIR}/phase-1-market-research/competitive-analysis.md")
competitive = Read(competitive_files[0]) if competitive_files else ""
revenue_draft_files = Glob("{PROJECT_DIR}/phase-1-market-research/revenue-model-draft.md")
revenue_draft = Read(revenue_draft_files[0]) if revenue_draft_files else ""
feature_priority_files = Glob("{PROJECT_DIR}/phase-2-product-planning/feature-priority.md")
feature_priority = Read(feature_priority_files[0]) if feature_priority_files else ""

# 12.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-8-monetization/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-8-monetization pricing-strategy.md {current_version}")
    existing_pricing = Read("{PROJECT_DIR}/phase-8-monetization/pricing-strategy.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting pricing strategy:\n{existing_pricing}"

# 12.3 Launch 2 agents in PARALLEL
Task(
  subagent_type="revenue-strategist",
  model="sonnet",
  description="Pricing strategy",
  prompt=f"""
  You are Business Avengers' Revenue Strategist.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/revenue-strategist.md

  Project Context:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - Market Analysis: {market_analysis}
  - Competitive Analysis: {competitive}
  - Revenue Model Draft (Phase 1): {revenue_draft}
  - Feature Priority: {feature_priority}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/pricing-strategies.md
  - {KNOWLEDGE_DIR}/business-models.md
  - {KNOWLEDGE_DIR}/extended/saas-metrics-bible.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 8 section)

  Template (Read this file):
  - {TEMPLATE_DIR}/pricing-strategy.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read saas-metrics-bible.md — apply Goldilocks 3-tier pricing structure and value metric selection guide
  3. Build on the Phase 1 revenue model draft to establish a concrete pricing strategy
  4. Design 3-tier Goldilocks pricing (Starter/Free → Pro/Core → Business/Enterprise):
     - Tier 1: Feature-limited, upsell bait — do NOT make this tier appealing
     - Tier 2: PRIMARY revenue tier — most visually prominent and best value
     - Tier 3: Anchor that makes Tier 2 look reasonable by comparison
     - Annual pricing: ~2 months free (16.7% discount); target 30–50% on annual
  5. Include a competitive pricing comparison analysis
  6. Write feature mapping per tier with clear upgrade triggers
  7. Present price sensitivity analysis and optimal price points
  8. Establish discount/promotion strategies
  9. Check phase-rubrics.md Phase 8 checklist, fix any unmet items
  10. Add Quality Self-Assessment block at top of output
  11. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-8-monetization/pricing-strategy.md
  """)

Task(
  subagent_type="business-analyst",
  model="sonnet",
  description="Financial projections and unit economics",
  prompt=f"""
  You are Business Avengers' Business Analyst.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/business-analyst.md

  Project Context:
  - Idea Canvas: {idea_canvas}
  - PRD: {prd}
  - Market Analysis: {market_analysis}
  - Revenue Model Draft: {revenue_draft}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/business-models.md
  - {KNOWLEDGE_DIR}/pricing-strategies.md
  - {KNOWLEDGE_DIR}/extended/saas-metrics-bible.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 8 section)

  Template (Read these files):
  - {TEMPLATE_DIR}/financial-projections.md
  - {TEMPLATE_DIR}/unit-economics.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read saas-metrics-bible.md — apply LTV:CAC thresholds, Gross Margin benchmarks, and 3-scenario framework
  3. Write 3-year financial projections (revenue, costs, profit)
  4. Include monthly cash flow projections
  5. Calculate Unit Economics (CAC, LTV, LTV/CAC, Payback Period) — compare each to saas-metrics-bible.md benchmarks
  6. If LTV:CAC < 3:1 → flag business model viability to CEO explicitly in the document
  7. If Gross Margin < 70% → include COGS breakdown + roadmap to reach 70%+
  8. Perform break-even point (BEP) analysis — state Breakeven MRR + projected month (M+N format)
  9. Include scenario analysis — 3 mandatory scenarios: Best (×1.5) / Base / Worst (×0.5); each with key assumption stated
  10. Present initial investment requirements and funding strategy
  11. Check phase-rubrics.md Phase 8 checklist, fix any unmet items
  12. Add Quality Self-Assessment block at top of each output
  13. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-8-monetization/financial-projections.md
     - {PROJECT_DIR}/phase-8-monetization/unit-economics.md
  """)

# 12.4 CFO presents to CEO for strategic approval
"""
[CFO] Monetization strategy is complete:
- Pricing Strategy: pricing and feature mapping per tier
- Financial Projections: 3-year revenue/cost/profit outlook
- Unit Economics: CAC, LTV, break-even analysis

Detailed documents have been saved to the project folder.
"""

gate_8 = AskUserQuestion("[CFO] Please review the monetization strategy.",
  options=["Approve - confirm pricing", "Request revision - pricing adjustment needed", "Re-evaluate - change revenue model"])

if "Approve" in gate_8:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 8 completed {current_version}")
elif "Request revision" in gate_8:
    revision_feedback = AskUserQuestion("Which parts should be adjusted? (pricing tier, revenue model, Unit Economics, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run Phase 8 agents from step 12.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
    # After re-run, loop back to this gate.
elif "Re-evaluate" in gate_8:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 8 revision {current_version}")
    # Return to Phase 1 for market re-research or Phase 0 for re-ideation
```

---

### Step 13: Execute Phase 9 - Operations

**Condition**: Only runs if Phase 9 is in phases_to_run
**Lead**: COO
**Agents**: cs-manager + legal-advisor + data-analyst (PARALLEL)
**CEO Interaction**: Delegate + Report

```python
# 13.1 Read previous phase outputs (I2: added Phase 7 gtm-strategy.md per inputs_from: [2,4,7,8])
prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
if prd_files:
    prd = Read(prd_files[0])
else:
    canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
    prd = Read(canvas_files[0]) if canvas_files else ""
personas_files = Glob("{PROJECT_DIR}/phase-2-product-planning/user-personas.md")
personas = Read(personas_files[0]) if personas_files else ""
pricing_files = Glob("{PROJECT_DIR}/phase-8-monetization/pricing-strategy.md")
pricing = Read(pricing_files[0]) if pricing_files else ""
tech_arch_files = Glob("{PROJECT_DIR}/phase-4-tech-planning/tech-architecture.md")
tech_arch = Read(tech_arch_files[0]) if tech_arch_files else ""
gtm_files = Glob("{PROJECT_DIR}/phase-7-launch-strategy/gtm-strategy.md")
gtm = Read(gtm_files[0]) if gtm_files else ""

# 13.2 Sprint mode: backup existing docs
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-9-operations/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-9-operations cs-playbook.md {current_version}")
    existing_cs = Read("{PROJECT_DIR}/phase-9-operations/cs-playbook.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting CS playbook:\n{existing_cs}"

# 13.3 Launch 3 agents in PARALLEL (CRITICAL: all in single response block)
Task(
  subagent_type="cs-manager",
  model="sonnet",
  description="CS playbook and FAQ",
  prompt=f"""
  You are Business Avengers' CS Manager.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/cs-manager.md

  Project Context:
  - PRD: {prd}
  - Personas: {personas}
  - Pricing Strategy: {pricing}
  - GTM Strategy (launch/channel context): {gtm}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/startup-best-practices.md

  Template (Read these files):
  - {TEMPLATE_DIR}/cs-playbook.md
  - {TEMPLATE_DIR}/faq-template.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Write response scenarios per customer inquiry type
  3. Define the escalation process (tier 1 → tier 2 → CEO)
  4. Write 30+ FAQ items organized by category
  5. Define customer satisfaction measurement methods (NPS, CSAT)
  6. Present efficient CS operation plans suitable for a solo business
  7. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-9-operations/cs-playbook.md
     - {PROJECT_DIR}/phase-9-operations/faq-template.md
  """)

Task(
  subagent_type="legal-advisor",
  model="sonnet",
  description="Legal documentation",
  prompt=f"""
  You are Business Avengers' Legal Advisor.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/legal-advisor.md

  Project Context:
  - PRD: {prd}
  - Pricing Strategy: {pricing}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/legal-templates.md

  Template (Read this file):
  - {TEMPLATE_DIR}/legal-docs.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Read the Legal Compliance Knowledge Base for reference
  3. Write the Terms of Service
  4. Write the Privacy Policy
  5. Write the Refund Policy
  6. Include mandatory legal notices specific to the service's characteristics
  7. Check compliance requirements for applicable laws (privacy protection, e-commerce, etc.)
  8. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-9-operations/legal-docs.md
  """)

Task(
  subagent_type="data-analyst",
  model="sonnet",
  description="Metrics dashboard and feedback loop",
  prompt=f"""
  You are Business Avengers' Data Analyst.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/data-analyst.md

  Project Context:
  - PRD: {prd}
  - Tech Architecture: {tech_arch}
  - Pricing Strategy: {pricing}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/data-metrics-guide.md

  Template (Read these files):
  - {TEMPLATE_DIR}/metrics-dashboard.md
  - {TEMPLATE_DIR}/feedback-loop.md

  {sprint_context}

  Task:
  1. Read the agent definition and internalize your role and expert frameworks
  2. Define core KPIs (business, product, technical metrics)
  3. Design the dashboard layout (real-time/daily/weekly/monthly)
  4. Write data collection points and event tracking plan
  5. Include analytics tool recommendations and setup guides
  6. Design the user feedback collection → analysis → implementation process
  7. Present a data-driven decision-making framework
  8. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-9-operations/metrics-dashboard.md
     - {PROJECT_DIR}/phase-9-operations/feedback-loop.md
  """)

# 13.4 COO reports to CEO
"""
[COO] Operations plan is complete:
- CS Playbook: customer response scenarios and FAQ
- Legal Documents: Terms of Service, Privacy Policy, Refund Policy
- Metrics Dashboard: KPI definitions and data collection plan
- Feedback Loop: user feedback collection → implementation process

Detailed documents have been saved to the project folder.
"""

gate_9 = AskUserQuestion("[COO] Operations plan is complete. Please review.",
  options=["Confirm - proceed", "I have a question", "Request revision"])

if "I have a question" in gate_9:
    follow_up = AskUserQuestion("Please enter your question about the operations plan.", allow_freeform=true)
    # Display relevant section from cs-playbook / legal-docs / metrics-dashboard based on follow_up
elif "Request revision" in gate_9:
    revision_feedback = AskUserQuestion("Which parts should be revised? (CS playbook, legal docs, metrics, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run the relevant Phase 9 agent Task(s) from step 13.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 9 completed {current_version}")
```

---

### Step 14: Execute Phase 10 - Growth (MAKE Methodology)

**Condition**: Only runs if Phase 10 is in phases_to_run
**Lead**: CMO
**Agents**: growth-hacker + content-creator + data-analyst (PARALLEL)
**CEO Interaction**: Approve (growth strategy selection)
**Knowledge Base**: knowledge/growth-tactics.md

```python
# 14.1 Read previous phase outputs
gtm_files = Glob("{PROJECT_DIR}/phase-7-launch-strategy/gtm-strategy.md")
gtm = Read(gtm_files[0]) if gtm_files else ""
pricing_files = Glob("{PROJECT_DIR}/phase-8-monetization/pricing-strategy.md")
pricing = Read(pricing_files[0]) if pricing_files else ""
metrics_files = Glob("{PROJECT_DIR}/phase-9-operations/metrics-dashboard.md")
metrics = Read(metrics_files[0]) if metrics_files else ""
prd_files = Glob("{PROJECT_DIR}/phase-2-product-planning/prd.md")
if prd_files:
    prd = Read(prd_files[0])
else:
    canvas_files = Glob("{PROJECT_DIR}/phase-0-ideation/idea-canvas.md")
    prd = Read(canvas_files[0]) if canvas_files else ""

# 14.2 Sprint mode
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-10-growth/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-10-growth growth-execution-plan.md {current_version}")
    existing_growth = Read("{PROJECT_DIR}/phase-10-growth/growth-execution-plan.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting growth plan:\n{existing_growth}"

# 14.3 Launch 3 agents in PARALLEL
Task(
  subagent_type="growth-hacker",
  model="sonnet",
  description="Growth execution plan and organic growth playbook",
  prompt=f"""
  You are Business Avengers' Growth Hacker.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/growth-hacker.md

  Project Context:
  - PRD: {prd}
  - GTM Strategy: {gtm}
  - Pricing Strategy: {pricing}
  - Metrics Dashboard: {metrics}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/growth-tactics.md
  - {KNOWLEDGE_DIR}/extended/growth-engineering.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 10 section)

  Template (Read these files):
  - {TEMPLATE_DIR}/growth-execution-plan.md
  - {TEMPLATE_DIR}/organic-growth-playbook.md
  - {TEMPLATE_DIR}/user-retention-plan.md

  {sprint_context}

  Task:
  1. Read the agent definition and growth-engineering.md — internalize PMF signals, growth loops, and Aha Moment framework
  2. State PMF evidence (Sean Ellis score or retention curve result) — if no signal, recommend fixing retention before scaling
  3. Define North Star Metric (not revenue, not signups) + 3–5 input metrics that drive it
  4. Identify primary growth loop (viral / SEO / paid / PLG) — design loop mechanics with input → output → reinforcement
  5. Define Aha Moment: exact action + target timeframe; include activation funnel optimization tactics
  6. Establish a quarterly growth execution plan (MAKE organic growth-first principle)
  7. Write organic growth playbook: SEO loop, API distribution, social sharing triggers, Repeated Launch calendar
  8. Design retention strategy: Hook Model application, Win-back email sequence, churn prevention triggers
  9. Propose ≥3 ICE-scored experiments for Q1 with hypothesis + metric + success threshold
  10. Check phase-rubrics.md Phase 10 checklist, fix any unmet items
  11. Add Quality Self-Assessment block at top of each output
  12. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-10-growth/growth-execution-plan.md
     - {PROJECT_DIR}/phase-10-growth/organic-growth-playbook.md
     - {PROJECT_DIR}/phase-10-growth/user-retention-plan.md
  """)

Task(
  subagent_type="content-creator",
  model="sonnet",
  description="Build in Public plan",
  prompt=f"""
  You are Business Avengers' Content Creator.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/content-creator.md

  Project Context:
  - PRD: {prd}
  - GTM Strategy: {gtm}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/growth-tactics.md

  Template (Read this file):
  - {TEMPLATE_DIR}/build-in-public-plan.md

  {sprint_context}

  Task:
  1. Establish a Build in Public strategy (transparency, community building, trust building)
  2. Define metrics to share, frequency, channels, and tone of voice
  3. Milestone-based sharing strategy (including revenue, user count, failure experiences)
  4. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-10-growth/build-in-public-plan.md
  """)

Task(
  subagent_type="data-analyst",
  model="sonnet",
  description="Growth metrics report",
  prompt=f"""
  You are Business Avengers' Data Analyst.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/data-analyst.md

  Project Context:
  - Metrics Dashboard: {metrics}
  - Pricing Strategy: {pricing}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/growth-tactics.md

  Template (Read this file):
  - {TEMPLATE_DIR}/growth-metrics-report.md

  {sprint_context}

  Task:
  1. Design the growth KPI dashboard (including organic vs. paid traffic ratio)
  2. Write weekly/monthly/quarterly report templates
  3. Include a growth experiment tracking framework
  4. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-10-growth/growth-metrics-report.md
  """)

# 14.4 CMO presents to CEO
"""
[CMO] Growth strategy is complete:
- Quarterly growth execution plan
- Build in Public strategy
- Organic growth playbook (SEO, API, social, repeat launching)
- Retention & churn prevention strategy
- Growth KPI dashboard

Detailed documents have been saved to the project folder.
"""

gate_10 = AskUserQuestion("[CMO] Please review the growth strategy.",
  options=["Approve - confirm growth strategy", "Request revision - adjust strategy", "Re-evaluate - reset growth direction"])

if "Approve" in gate_10:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 10 completed {current_version}")
elif "Request revision" in gate_10:
    revision_feedback = AskUserQuestion("Which parts should be adjusted? (channel strategy, BIP, retention, growth KPIs, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run Phase 10 agents from step 14.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}"
    # After re-run, loop back to this gate.
elif "Re-evaluate" in gate_10:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 10 revision {current_version}")
    # Return to Phase 7 for GTM strategy revision
```

---

### Step 15: Execute Phase 11 - Automation (MAKE Methodology)

**Condition**: Only runs if Phase 11 is in phases_to_run
**Lead**: COO + CTO
**Agents**: devops-engineer + business-analyst (PARALLEL)
**CEO Interaction**: Approve (automation priorities)
**Knowledge Base**: knowledge/automation-guide.md

```python
# 15.1 Read previous phase outputs
deployment_files = Glob("{PROJECT_DIR}/phase-5-development/deployment-strategy.md")
deployment = Read(deployment_files[0]) if deployment_files else ""
cs_files = Glob("{PROJECT_DIR}/phase-9-operations/cs-playbook.md")
cs_playbook = Read(cs_files[0]) if cs_files else ""
growth_files = Glob("{PROJECT_DIR}/phase-10-growth/growth-execution-plan.md")
growth_plan = Read(growth_files[0]) if growth_files else ""

# 15.2 Sprint mode
sprint_context = ""
if is_sprint:
  existing = Glob("{PROJECT_DIR}/phase-11-automation/*.md")
  if existing:
    Bash("python3 {CONFIG_DIR}/init-project.py backup '{project_slug}' phase-11-automation automation-audit.md {current_version}")
    existing_automation = Read("{PROJECT_DIR}/phase-11-automation/automation-audit.md")
    sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting automation audit:\n{existing_automation}\nOnly reflect the changes — preserve the existing analysis."

# 15.3 Launch agents in PARALLEL
Task(
  subagent_type="devops-engineer",
  model="sonnet",
  description="Automation audit, robot specs, and monitoring",
  prompt=f"""
  You are Business Avengers' DevOps Engineer.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/devops-engineer.md

  Project Context:
  - Deployment Strategy: {deployment}
  - CS Playbook: {cs_playbook}
  - Growth Plan: {growth_plan}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/automation-guide.md
  - {KNOWLEDGE_DIR}/extended/automation-scale.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 11 section)

  Template (Read these files):
  - {TEMPLATE_DIR}/automation-audit.md
  - {TEMPLATE_DIR}/robot-specs.md
  - {TEMPLATE_DIR}/monitoring-setup.md

  {sprint_context}

  Task:
  1. Read the agent definition and automation-scale.md — apply ROI formula, Bus Test, and 3-tier monitoring
  2. Audit all repetitive tasks — calculate ROI for each: (time saved/week × hourly value × 52) ÷ build cost
  3. Prioritize automations by payback period (< 8 weeks = automate)
  4. Calculate Bus Test score (target ≥8/10) — if below, include steps to reach ≥8
  5. Write automation specifications (cron jobs, webhooks, Zapier/n8n triggers + actions)
  6. Every critical automation must have a failure notification path defined
  7. Design 3-tier monitoring: uptime + error rate (Sentry) + business metrics (MRR drop, churn spike)
  8. Check phase-rubrics.md Phase 11 checklist, fix any unmet items
  9. Add Quality Self-Assessment block at top of each output
  10. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-11-automation/automation-audit.md
     - {PROJECT_DIR}/phase-11-automation/robot-specs.md
     - {PROJECT_DIR}/phase-11-automation/monitoring-setup.md
  """)

Task(
  subagent_type="business-analyst",
  model="sonnet",
  description="Contractor playbook and autonomous org design",
  prompt=f"""
  You are Business Avengers' Business Analyst.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/business-analyst.md

  Project Context:
  - CS Playbook: {cs_playbook}
  - Growth Plan: {growth_plan}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/automation-guide.md

  Template (Read these files):
  - {TEMPLATE_DIR}/contractor-playbook.md
  - {TEMPLATE_DIR}/autonomous-org-design.md

  {sprint_context}

  Task:
  1. Write a contractor management guide (hiring, autonomy, compensation, communication)
  2. Include a contractor vs. automation decision matrix
  3. Write a Bus Test checklist (can the business run without the founder?)
  4. Write the autonomous organization design (robot + contractor + founder role separation)
  5. Design the minimal maintenance model
  6. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-11-automation/contractor-playbook.md
     - {PROJECT_DIR}/phase-11-automation/autonomous-org-design.md
  """)

# 15.4 COO reports to CEO
"""
[COO] Automation strategy is complete:
- Automation Audit: repetitive task analysis and ROI-based automation opportunities
- Robot Specs: cron job, webhook, workflow automation design
- Contractor Management: hiring, operations, evaluation guide
- Autonomous Org Design: Bus Test checklist, minimal maintenance model
- Monitoring Setup: UptimeRobot configuration and alert system

Detailed documents have been saved to the project folder.
"""

gate_11 = AskUserQuestion("[COO] Please review the automation strategy.",
  options=["Approve - confirm automation priorities", "Request revision - adjust priorities", "I have a question"])

if "Approve" in gate_11:
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 11 completed {current_version}")
elif "I have a question" in gate_11:
    follow_up = AskUserQuestion("Please enter your question about the automation strategy.", allow_freeform=true)
    # Display relevant section from automation-audit / robot-specs based on follow_up
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 11 completed {current_version}")
elif "Request revision" in gate_11 or "adjust priorities" in gate_11:
    revision_feedback = AskUserQuestion("Which parts should be adjusted? (automation priorities, robot specs, contractor guide, etc.)", allow_freeform=true)
    # INSTRUCTION: Re-run Phase 11 agents from step 15.3 above,
    # setting sprint_context = f"CEO revision feedback: {revision_feedback}\nOnly reflect the changes — preserve the existing analysis."
    Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 11 completed {current_version}")
```

---

### Step 16: Execute Phase 12 - Scale & Exit (MAKE Methodology)

**Condition**: Only runs if Phase 12 is in phases_to_run
**Lead**: CFO
**Agents**: revenue-strategist + business-analyst + legal-advisor (PARALLEL)
**CEO Interaction**: Deep Dialogue (strategic conversation)
**Knowledge Base**: knowledge/exit-guide.md

```python
# 16.1 Read previous phase outputs
pricing_files = Glob("{PROJECT_DIR}/phase-8-monetization/pricing-strategy.md")
pricing = Read(pricing_files[0]) if pricing_files else ""
financial_files = Glob("{PROJECT_DIR}/phase-8-monetization/financial-projections.md")
financials = Read(financial_files[0]) if financial_files else ""
growth_files = Glob("{PROJECT_DIR}/phase-10-growth/growth-execution-plan.md")
growth = Read(growth_files[0]) if growth_files else ""
automation_files = Glob("{PROJECT_DIR}/phase-11-automation/autonomous-org-design.md")
automation = Read(automation_files[0]) if automation_files else ""

# 16.2 Sprint mode: backup all existing phase-12 docs before overwriting
sprint_context = ""
if is_sprint:
    existing = Glob("{PROJECT_DIR}/phase-12-scale-exit/*.md")
    if existing:
        for f in ["scale-vs-exit-analysis.md", "valuation-report.md", "exit-readiness-checklist.md", "acquisition-playbook.md", "fire-plan.md"]:
            Bash(f"python3 {{CONFIG_DIR}}/init-project.py backup '{{project_slug}}' phase-12-scale-exit {f} {{current_version}}")
        existing_scale = Glob("{PROJECT_DIR}/phase-12-scale-exit/scale-vs-exit-analysis.md")
        existing_scale_content = Read(existing_scale[0]) if existing_scale else ""
        sprint_context = f"Update the existing document. Change goal: {sprint_goal}\nExisting content:\n{existing_scale_content}"

# 16.3 Strategic dialogue with CEO
"""
[CFO] CEO, this stage requires a strategic conversation.
Let's discuss the future direction of the business (continue growing vs. exit vs. maintain).
"""

AskUserQuestion(
  "[CFO] What is the current state of the business? (UX8: timing assessment criteria)",
  options=[
    "Growing - revenue/users are continuously increasing",
    "Stagnant - growth has stopped or slowed",
    "Burned out - the business is fine but I'm exhausted",
    "Declining - revenue/users are decreasing"
  ]
)
ceo_business_state = selected_option

AskUserQuestion(
  "[CFO] What is the long-term goal for the business?",
  options=[
    "Continue growing - I want to scale up",
    "Lifestyle business - I want to maintain the current level and enjoy freedom",
    "Considering exit - I'm open to selling at the right time",
    "Not sure yet - please analyze all scenarios"
  ]
)
ceo_goal = selected_option  # CEO's selected long-term goal

# 16.4 Launch 3 agents in PARALLEL
Task(
  subagent_type="revenue-strategist",
  model="sonnet",
  description="Scale vs exit analysis and valuation",
  prompt=f"""
  You are Business Avengers' Revenue Strategist.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/revenue-strategist.md

  Project Context:
  - Pricing Strategy: {pricing}
  - Financial Projections: {financials}
  - Growth Plan: {growth}
  - Autonomous Org Design: {automation}
  - CEO Current Business State: {ceo_business_state}
  - CEO Long-Term Goal: {ceo_goal}

  Knowledge Base (must Read — refer to valuation/exit strategy):
  - {KNOWLEDGE_DIR}/exit-guide.md
  - {KNOWLEDGE_DIR}/extended/exit-strategy.md

  Quality Rubric (Read this file):
  - {PLUGIN_DIR}/quality/phase-rubrics.md  (refer to Phase 12 section)

  Template (Read these files):
  - {TEMPLATE_DIR}/scale-vs-exit-analysis.md
  - {TEMPLATE_DIR}/valuation-report.md

  {sprint_context}

  Task:
  1. Read the agent definition and exit-strategy.md — apply Acquire.com multiples, acquisition readiness checklist, and FIRE formula
  2. Calculate current estimated valuation using benchmarked MRR multiples (Acquire.com / Quiet Light standards)
  3. State multiple drivers and killers present in this business
  4. Make explicit Scale vs. Sell recommendation (not "it depends") with key reasoning
  5. If Scale: identify top 3 levers to increase acquisition multiple
  6. If Exit: list acquisition readiness gaps and estimated time to close them
  7. Analyze 3 scenarios: continue growing vs. exit vs. maintain (FIRE calculation for each)
  8. Include FIRE number calculation: annual expenses × 25 = FIRE target; MRR needed at 70% margin
  9. Check phase-rubrics.md Phase 12 checklist, fix any unmet items
  10. Add Quality Self-Assessment block at top of each output
  11. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-12-scale-exit/scale-vs-exit-analysis.md
     - {PROJECT_DIR}/phase-12-scale-exit/valuation-report.md
  """)

Task(
  subagent_type="business-analyst",
  model="sonnet",
  description="FIRE plan",
  prompt=f"""
  You are Business Avengers' Business Analyst.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/business-analyst.md

  Project Context:
  - Financial Projections: {financials}
  - Growth Plan: {growth}
  - CEO Current Business State: {ceo_business_state}
  - CEO Long-Term Goal: {ceo_goal}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/exit-guide.md

  Template (Read this file):
  - {TEMPLATE_DIR}/fire-plan.md

  {sprint_context}

  Task:
  1. Analyze the FIRE (Financial Independence, Retire Early) scenario
  2. Calculate the required assets based on the 4% rule
  3. Present an investment strategy for the sale proceeds
  4. Include psychological preparation for post-exit (identity loss warning)
  5. Fill in {{PLACEHOLDER}} in the template and save with Write:
     - {PROJECT_DIR}/phase-12-scale-exit/fire-plan.md
  """)

Task(
  subagent_type="legal-advisor",
  model="sonnet",
  description="Exit readiness checklist and acquisition playbook",
  prompt=f"""
  You are Business Avengers' Legal Advisor.

  Agent Definition (Read this file):
  - {AGENTS_DIR}/legal-advisor.md

  Project Context:
  - Pricing Strategy: {pricing}
  - Financial Projections: {financials}
  - CEO Current Business State: {ceo_business_state}
  - CEO Long-Term Goal: {ceo_goal}

  Knowledge Base (Read these files):
  - {KNOWLEDGE_DIR}/exit-guide.md

  Template (Read these files):
  - {TEMPLATE_DIR}/exit-readiness-checklist.md
  - {TEMPLATE_DIR}/acquisition-playbook.md

  {sprint_context}

  Task:
  1. Write the exit readiness checklist (accounting, code licenses, legal preparation)
  2. Include negotiation strategies per buyer type
  3. Guide through LOI, due diligence, and deal structure (cash vs. stock vs. earnout)
  4. Cover key contract terms such as breakup fee and non-compete clause
  5. Fill in {{PLACEHOLDER}} in each template and save with Write:
     - {PROJECT_DIR}/phase-12-scale-exit/exit-readiness-checklist.md
     - {PROJECT_DIR}/phase-12-scale-exit/acquisition-playbook.md
  """)

# 16.4 CFO presents to CEO for deep dialogue
"""
[CFO] Strategic analysis is complete:
- Continue growing vs. exit vs. maintain scenario comparison
- Business valuation
- Exit readiness checklist
- Acquisition playbook (negotiation strategy, deal structure)
- FIRE scenario analysis

These documents will serve as the foundation for future strategic decisions.
You can update them at any time with '/business-avengers sprint'.
"""

gate_12 = AskUserQuestion("[CFO] Please review the strategic analysis.",
  options=["Confirm - analysis complete", "Request additional scenarios", "Request deep-dive analysis on specific scenario"])

if "additional scenarios" in gate_12 or "deep-dive" in gate_12:
    follow_up = AskUserQuestion("Which scenario or analysis do you need?", allow_freeform=true)
    # INSTRUCTION: Re-run the relevant Phase 12 agent Task(s) from step 16.4 above,
    # setting sprint_context = f"CEO additional request: {follow_up}"
Bash("python3 {CONFIG_DIR}/init-project.py update-phase '{project_slug}' 12 completed {current_version}")
```

---

### Step 17: Status Mode

```python
result = Bash("python3 {PLUGIN_DIR}/config/init-project.py load '{project_slug}'")
project = parse_json(result)

# Display formatted status
"""
📋 Project: {project.name}
🔄 Current Sprint: #{project.current_sprint}
📊 Progress:

| Phase | Name | Status | Version |
|-------|------|--------|---------|
| 0 | Ideation | ✅ Completed | v1.0 |
| 1 | Market Research | ✅ Completed | v1.1 |
| 2 | Product Planning | 🔄 In Progress | v1.2 |
| 3 | Design | ⏳ Pending | - |
...
"""
```

---

### Step 18: History Mode

```python
# Read all changelogs
for phase_dir in project_dirs:
  changelog = Read("{phase_dir}/changelog.md") if exists

# Read sprint history
for sprint_file in sprints_dir:
  sprint = Read(sprint_file)

# Display formatted history
"""
📜 Project History: {project.name}

Sprint 1 (2026-02-21): Initial E2E
  - Phase 0-8 completed
  - CEO decision: narrowed target to users in their 20s-30s

Sprint 2 (2026-03-01): Onboarding improvements
  - Phase 2 v1.1: revised PRD onboarding section
  - Phase 3 v1.1: updated onboarding wireframes

Sprint 3 (in progress): Adding social login
  - Phase 2 v1.2: added social login feature
  - Phase 4 v1.1: added OAuth architecture
"""
```

---

### Step 19: Ask Mode (Direct Agent Conversation)

```python
# Parse: /business-avengers ask {agent_or_team} "{question}"

# Map team names to agents
TEAM_MAP = {
  "cto": "cto",
  "cfo": "cfo",
  "cmo": "cmo",
  "cpo": "cpo",
  "coo": "coo",
  "marketing": "marketing-strategist",
  "product": "product-manager",
  "design": "design-lead",
  "tech": "tech-lead",
  "legal": "legal-advisor",
  "data": "data-analyst",
  "qa": "qa-lead",
  "cs": "cs-manager",
  "growth": "growth-hacker",
  "pr": "pr-manager",
  "content": "content-creator",
  "finance": "business-analyst",
  "revenue": "revenue-strategist",
  "frontend": "frontend-dev",
  "backend": "backend-dev",
  "devops": "devops-engineer",
  "ux": "ux-researcher",
  "ui": "ui-designer",
}

agent_id = TEAM_MAP.get(agent_or_team, agent_or_team)

# Load project context if exists
project_context = ""
if project_exists:
  project_context = f"Current project: {project.name}\n"
  # Include relevant phase outputs based on agent's domain

Task(
  subagent_type=agent_id,
  model="sonnet",
  description=f"Direct question to {agent_id}",
  prompt=f"""
  You are Business Avengers' {agent_title}.
  The CEO is asking you directly.

  {project_context}

  CEO Question: {question}

  Answer concretely and actionably as an expert.
  If necessary, use WebSearch to research the latest information.
  """
)
```

---

### Step 20: Sprint Completion

After all sprint phases are executed:

```python
# Update sprint record
sprint_data = {
  "goal": sprint_goal,
  "phases": phases_updated,
  "completed": current_date,
  "changes": changelog_entries
}
Write("{PROJECT_DIR}/sprints/sprint-{N}.yaml", yaml.dump(sprint_data))

# Update project.yaml current_sprint
Bash("python3 ... update sprint number")

# I7: Generate sprint review document using template
sprint_review_template = Glob("{TEMPLATE_DIR}/sprint-review.md")
if sprint_review_template:
    Task(
        subagent_type="data-analyst",
        model="sonnet",
        description="Generate sprint review",
        prompt=f"""
        Write a sprint completion report.
        Template (Read this file): {TEMPLATE_DIR}/sprint-review.md
        Sprint goal: {sprint_goal}
        Updated phases: {phases_list}
        Changes summary: {changes_summary}
        Updated date: {current_date}
        Fill in all {{PLACEHOLDER}} and save with Write:
        {PROJECT_DIR}/sprints/sprint-{N}-review.md
        """
    )

# Sprint review
"""
[COO] Sprint #{N} completion report:

🎯 Goal: {sprint_goal}
📝 Updated Phases: {phases_list}
📊 Changes: {changes_summary}
📄 Sprint Review: {PROJECT_DIR}/sprints/sprint-{N}-review.md

Would you like to plan the next sprint?
"""

AskUserQuestion(
  "Please select the next action.",
  options=[
    "Start a new sprint",
    "Keep current state",
    "Project complete"
  ]
)
```

---

### Step 21: Project Completion (Orchestra Mode)

When all phases are completed:

```python
# Generate executive summary
"""
🎉 Project Complete: {project.name}

📁 Generated Deliverables:
├── Phase 0: Idea Canvas (problem validation, micro-niche strategy included)
├── Phase 1: Market Analysis, Competitive Analysis, Revenue Model
├── Phase 2: PRD, Personas, User Stories, Feature Priority (MVP build strategy included)
├── Phase 3: Design System, Wireframes, UI Specs
├── Phase 4: Tech Architecture, API Design, DB Schema
├── Phase 5: Frontend/Backend Guides, Deployment Strategy
├── Phase 6: Test Plan, QA Checklist
├── Phase 7: GTM Strategy, Content Plan, Growth Strategy, PR (indie maker launch playbook included)
├── Phase 8: Pricing Strategy, Financial Projections, Unit Economics (business model experiments included)
├── Phase 9: CS Playbook, Legal Docs, Metrics Dashboard (self-service dashboard included)
├── Phase 10: Growth Execution Plan, Build in Public, Organic Growth, Retention (MAKE)
├── Phase 11: Automation Audit, Robot Specs, Contractor Management, Autonomous Org (MAKE)
└── Phase 12: Scale vs Exit Analysis, Valuation, Acquisition Playbook, FIRE Plan (MAKE)

📂 Project folder: {PROJECT_DIR}

💡 Next steps:
1. Review deliverables and verify alignment with the CEO's vision
2. Start actual development based on the Dev Guide (Phase 5)
3. When needed, start a sprint with '/business-avengers sprint "goal"'
"""
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Project not found | Invalid slug or no project | Guide user to create new project |
| Agent timeout | Complex analysis | Retry with simplified prompt |
| Phase output missing | Previous phase not completed | Warn user, offer to skip or run missing phase |
| WebSearch fails | Network issue | Proceed with available data, mark [TODO] |
| project.yaml corrupted | File system issue | Recreate from existing phase outputs |
| Permission denied | Directory access | Check ~/.business-avengers permissions |

## Key Design Decisions

1. **Structured documents over free dialogue**: Following MetaGPT's proven pattern, agents communicate through structured output files, not natural language conversations between agents.

2. **Phase-level parallelism**: Within each phase, agents run in parallel where possible. Between phases, execution is sequential with CEO gates.

3. **Version control via file system**: Each document has a history/ folder for backups and a changelog.md for tracking changes across sprints.

4. **Knowledge base grounding**: Every agent has access to domain-specific knowledge files, ensuring consistent quality regardless of the model's training data.

5. **Hybrid autonomy**: Strategic decisions (phases 0,1,2,7,8) require CEO approval. Tactical decisions (phases 4,5,6) are delegated to C-Level with reporting.

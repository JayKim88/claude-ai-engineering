---
name: rich-guide
description: Use when user says "부자 되는 법", "재테크 가이드", "rich guide", "wealth strategy", "재테크 시작", "투자 방법", "부업 추천", or wants personalized wealth strategy. Conducts financial interview, runs 6-agent pipeline, and generates weekly action checklist.
version: 2.0.0
model: claude-sonnet-4-5-20250929
---

# Rich Guide Skill

Personalized Korean personal finance guidance via 6-agent multi-agent pipeline.

## Trigger Phrases

- "부자 되는 법"
- "재테크 가이드"
- "rich guide"
- "wealth strategy"
- "재테크 시작"
- "투자 방법 알려줘"
- "부업 추천"
- "/rich-guide"

## Execution Algorithm

### Step 1: Environment Setup & Config Load

```python
import subprocess, os, json
from datetime import datetime

DB_DIR = os.path.expanduser("~/.claude/skills/rich-guide/data")
DB_PATH = f"{DB_DIR}/profiles.db"
ROADMAP_DIR = os.path.expanduser("~/.claude/skills/rich-guide/roadmaps")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

# Create directories
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(ROADMAP_DIR, exist_ok=True)

# Init DB using absolute path (os.path.dirname(__file__) does not resolve in skill context)
init_script = os.path.expanduser("~/.claude/skills/rich-guide/config/init_db.py")
subprocess.run(["python3", init_script, DB_PATH], check=True)
os.chmod(DB_PATH, 0o600)

# Load agent-config.yaml for timeout/retry values
config_path = os.path.expanduser("~/.claude/skills/rich-guide/config/agent-config.yaml")
agent_config = {}
try:
    import yaml
    with open(config_path) as f:
        agent_config = yaml.safe_load(f) or {}
except Exception:
    # Fallback defaults if yaml unavailable or config missing
    agent_config = {
        "timeouts": {
            "wealth_strategist": 120,
            "action_plan_generator": 120,
            "financial_diagnostician": 60,
            "market_context_analyzer": 60,
            "risk_reward_evaluator": 60,
            "info_curator": 90,
        },
        "retry": {"max_attempts": 2, "fallback_on_fail": True},
        "interview": {"cache_hours": 24, "refresh_days": 30},
    }

TIMEOUT_STRATEGIST = agent_config.get("timeouts", {}).get("wealth_strategist", 120)
TIMEOUT_EVALUATOR = agent_config.get("timeouts", {}).get("risk_reward_evaluator", 60)
TIMEOUT_ACTION = agent_config.get("timeouts", {}).get("action_plan_generator", 120)
CACHE_HOURS = agent_config.get("interview", {}).get("cache_hours", 24)
REFRESH_DAYS = agent_config.get("interview", {}).get("refresh_days", 30)

# Check existing profile
result = subprocess.run(
    ["python3", "-c", f"""
import sqlite3, json
conn = sqlite3.connect('{DB_PATH}')
row = conn.execute("SELECT *, (julianday('now') - julianday(updated_at)) as age_days FROM profiles ORDER BY updated_at DESC LIMIT 1").fetchone()
if row:
    cols = [d[0] for d in conn.execute("PRAGMA table_info(profiles)").fetchall()]
    d = dict(zip(cols, row[:-1]))
    age = row[-1]
    print(json.dumps({{"exists": True, "age_days": age, "data": d}}))
else:
    print(json.dumps({{"exists": False}}))
conn.close()
"""],
    capture_output=True, text=True
)
try:
    existing = json.loads(result.stdout.strip())
except json.JSONDecodeError:
    existing = {"exists": False}
profile = None
```

Decide data strategy based on loaded config thresholds:
- `existing["exists"]` AND `existing["age_days"] < CACHE_HOURS/24` -> offer reuse
- `existing["exists"]` AND `CACHE_HOURS/24 <= existing["age_days"] <= REFRESH_DAYS` -> offer refresh
- Otherwise -> new interview

---

### Step 2: Financial Interview (or Reuse / Refresh Existing)

```python
if existing.get("exists") and existing["age_days"] < (CACHE_HOURS / 24):
    reuse_choice = AskUserQuestion(questions=[{
        "question": f"기존 재무 데이터({existing['data']['updated_at'][:10]} 작성)를 사용할까요?",
        "header": "기존 데이터 활용",
        "options": [
            {"label": "기존 데이터 사용", "description": "빠르게 전략 분석 시작"},
            {"label": "새로 입력", "description": "최신 재무 정보로 다시 시작"}
        ]
    }])
    if reuse_choice["기존 데이터 활용"] == "기존 데이터 사용":
        profile = existing["data"]

elif existing.get("exists") and (CACHE_HOURS / 24) <= existing["age_days"] <= REFRESH_DAYS:
    # 1-30 day refresh branch
    refresh_choice = AskUserQuestion(questions=[{
        "question": f"재무 데이터가 {int(existing['age_days'])}일 전 것입니다. 어떻게 할까요?",
        "header": "데이터 갱신",
        "options": [
            {"label": "기존 데이터 사용", "description": f"{existing['data']['updated_at'][:10]} 데이터로 계속 진행"},
            {"label": "일부 항목 업데이트", "description": "수입/지출 등 변경된 항목만 수정"},
            {"label": "처음부터 다시 입력", "description": "최신 재무 정보로 전체 재입력"}
        ]
    }])
    refresh_answer = refresh_choice.get("데이터 갱신", "처음부터 다시 입력")
    if refresh_answer == "기존 데이터 사용":
        profile = existing["data"]
    elif refresh_answer == "일부 항목 업데이트":
        # Pre-fill with existing, ask only for key fields
        partial_responses = AskUserQuestion(questions=[
            {
                "question": f"월 세후 수입 (현재: {existing['data'].get('monthly_income', '?')}만원)",
                "header": "월수입_갱신",
                "options": [
                    {"label": "변경 없음", "description": "기존 값 유지"},
                    {"label": "200만원 미만", "description": ""},
                    {"label": "200-300만원", "description": ""},
                    {"label": "300-400만원", "description": ""},
                    {"label": "400-500만원", "description": ""},
                    {"label": "500만원 이상", "description": ""}
                ]
            },
            {
                "question": f"월 지출 (현재: {existing['data'].get('monthly_expense', '?')}만원)",
                "header": "월지출_갱신",
                "options": [
                    {"label": "변경 없음", "description": "기존 값 유지"},
                    {"label": "100만원 미만", "description": ""},
                    {"label": "100-150만원", "description": ""},
                    {"label": "150-250만원", "description": ""},
                    {"label": "250만원 이상", "description": ""}
                ]
            }
        ])
        income_map = {
            "200만원 미만": 150, "200-300만원": 250, "300-400만원": 350,
            "400-500만원": 450, "500만원 이상": 550
        }
        expense_map = {
            "100만원 미만": 80, "100-150만원": 130, "150-250만원": 200, "250만원 이상": 280
        }
        profile = dict(existing["data"])
        new_income = partial_responses.get("월수입_갱신", "변경 없음")
        new_expense = partial_responses.get("월지출_갱신", "변경 없음")
        if new_income != "변경 없음":
            profile["monthly_income"] = income_map.get(new_income, profile["monthly_income"])
        if new_expense != "변경 없음":
            profile["monthly_expense"] = expense_map.get(new_expense, profile["monthly_expense"])
    # else: fall through to new interview below

if profile is None:
    # Conduct 7-field interview
    responses = AskUserQuestion(questions=[
        {
            "question": "월 세후 수입은 얼마인가요? (만원 단위)",
            "header": "월수입",
            "options": [
                {"label": "200만원 미만", "description": ""},
                {"label": "200-300만원", "description": ""},
                {"label": "300-400만원", "description": ""},
                {"label": "400-500만원", "description": ""},
                {"label": "500만원 이상", "description": ""},
                {"label": "잘 모르겠어요", "description": "기본값 적용 (300만원)"}
            ]
        },
        {
            "question": "월 지출은 얼마인가요? (고정비+변동비 합계)",
            "header": "월지출",
            "options": [
                {"label": "100만원 미만", "description": ""},
                {"label": "100-150만원", "description": ""},
                {"label": "150-250만원", "description": ""},
                {"label": "250만원 이상", "description": ""},
                {"label": "잘 모르겠어요", "description": "기본값 적용 (180만원)"}
            ]
        },
        {
            "question": "현재 예금/저축액은 총 얼마인가요?",
            "header": "예금액",
            "options": [
                {"label": "500만원 미만", "description": ""},
                {"label": "500-1000만원", "description": ""},
                {"label": "1000-3000만원", "description": ""},
                {"label": "3000만원 이상", "description": ""},
                {"label": "잘 모르겠어요", "description": "기본값 적용 (500만원)"}
            ]
        },
        {
            "question": "투자 자산(주식, 펀드, 코인 등)은 얼마인가요?",
            "header": "투자자산",
            "options": [
                {"label": "없음", "description": "투자 경험 없음"},
                {"label": "500만원 미만", "description": ""},
                {"label": "500-2000만원", "description": ""},
                {"label": "2000만원 이상", "description": ""},
                {"label": "잘 모르겠어요", "description": "기본값 적용 (0원)"}
            ]
        },
        {
            "question": "대출/부채 총액은 얼마인가요?",
            "header": "대출",
            "options": [
                {"label": "없음", "description": ""},
                {"label": "1000만원 미만", "description": ""},
                {"label": "1000-5000만원", "description": ""},
                {"label": "5000만원 이상", "description": ""},
                {"label": "잘 모르겠어요", "description": "기본값 적용 (0원)"}
            ]
        },
        {
            "question": "리스크 성향은 어떻게 되세요?",
            "header": "리스크성향",
            "options": [
                {"label": "저위험", "description": "원금 보전 최우선, 예금/채권 선호"},
                {"label": "중위험", "description": "적당한 수익, 인덱스 펀드 등"},
                {"label": "고위험", "description": "고수익 추구, 개별주식/코인 등 가능"}
            ]
        },
        {
            "question": "재테크 목표를 선택해주세요",
            "header": "목표",
            "options": [
                {"label": "긴급자금 마련 (1년 내)", "description": "당장 돈이 필요한 상황"},
                {"label": "내 집 마련 (3-5년)", "description": "주택 구매 준비"},
                {"label": "노후 준비 (10년+)", "description": "연금/장기 투자"},
                {"label": "부업 소득 창출", "description": "N잡러 목표"},
                {"label": "조기 은퇴 (FIRE)", "description": "경제적 자유 추구"}
            ]
        }
    ])

    # Map responses to numeric defaults
    income_map = {
        "200만원 미만": 150, "200-300만원": 250, "300-400만원": 350,
        "400-500만원": 450, "500만원 이상": 550, "잘 모르겠어요": 300
    }
    expense_map = {
        "100만원 미만": 80, "100-150만원": 130, "150-250만원": 200,
        "250만원 이상": 280, "잘 모르겠어요": 180
    }
    savings_map = {
        "500만원 미만": 250, "500-1000만원": 750, "1000-3000만원": 2000,
        "3000만원 이상": 5000, "잘 모르겠어요": 500
    }
    invest_map = {
        "없음": 0, "500만원 미만": 250, "500-2000만원": 1000,
        "2000만원 이상": 3000, "잘 모르겠어요": 0
    }
    debt_map = {
        "없음": 0, "1000만원 미만": 500, "1000-5000만원": 3000,
        "5000만원 이상": 7000, "잘 모르겠어요": 0
    }
    risk_map = {"저위험": "low", "중위험": "medium", "고위험": "high"}

    profile = {
        "monthly_income": income_map.get(responses["월수입"], 300),
        "monthly_expense": expense_map.get(responses["월지출"], 180),
        "savings": savings_map.get(responses["예금액"], 500),
        "investment_assets": invest_map.get(responses["투자자산"], 0),
        "debt": debt_map.get(responses["대출"], 0),
        "risk_tolerance": risk_map.get(responses["리스크성향"], "medium"),
        "goal": responses.get("목표", "내 집 마련 (3-5년)")
    }

    # Save to DB
    subprocess.run(["python3", "-c", f"""
import sqlite3, json
conn = sqlite3.connect('{DB_PATH}')
d = {json.dumps(profile)}
conn.execute('''INSERT INTO profiles
    (monthly_income, monthly_expense, savings, investment_assets, debt, risk_tolerance, goal)
    VALUES (?, ?, ?, ?, ?, ?, ?)''',
    (d['monthly_income'], d['monthly_expense'], d['savings'],
     d['investment_assets'], d['debt'], d['risk_tolerance'], d['goal']))
conn.commit()
conn.close()
print("saved")
"""], check=True)

print("재무 정보 저장 완료")
print(f"월 저축 가능액: 약 {profile['monthly_income'] - profile['monthly_expense']}만원")
```

---

### Step 3: Phase 1 - Parallel Diagnosis

Launch all 3 Phase 1 agents simultaneously. All three Task() calls must appear in a single response block so Claude Code executes them in parallel. Results are read after all three complete.

```python
print("Phase 1: 진단 시작 (3개 에이전트 병렬 실행)...")

# CRITICAL: All 3 Task calls must be in a single response for parallel execution
Task(
    subagent_type="financial-diagnostician",
    model="claude-sonnet-4-5-20250929",
    description="재무 건강도 진단",
    prompt=f"""
    사용자 재무 프로필을 분석하여 재무 건강도를 진단하세요.

    프로필:
    - 월수입: {profile['monthly_income']}만원
    - 월지출: {profile['monthly_expense']}만원
    - 예금: {profile['savings']}만원
    - 투자자산: {profile['investment_assets']}만원
    - 대출: {profile['debt']}만원
    - 리스크성향: {profile['risk_tolerance']}
    - 목표: {profile.get('goal', '미지정')}

    다음 JSON을 /tmp/rich-guide-diagnostician-{TS}.json 에 저장하세요:
    {{
      "status": "success",
      "agent": "financial-diagnostician",
      "health_score": 0-100점,
      "monthly_surplus": 월 잉여금(만원),
      "savings_rate": 저축률(%),
      "debt_ratio": 부채비율(%),
      "emergency_fund_months": 비상금 버팀 개월수,
      "diagnosis": "재무 상태 요약 (2-3문장)",
      "strengths": ["강점1", "강점2"],
      "weaknesses": ["약점1", "약점2"],
      "recommended_investment_ratio": 투자 가능 비율(%)
    }}

    Write 도구로 파일을 저장하세요.
    """
)

Task(
    subagent_type="info-curator",
    model="claude-haiku-4-5",
    description="재테크 정보 큐레이션",
    prompt=f"""
    사용자 목표 "{profile.get('goal', '재테크')}"와 리스크성향 "{profile['risk_tolerance']}"에 맞는
    신뢰할 수 있는 재테크 정보를 수집하세요.

    신뢰 도메인 우선순위:
    1. hankyung.com (한국경제)
    2. sedaily.com (서울경제)
    3. finance.naver.com (네이버증권)
    4. fss.or.kr (금융감독원)

    WebSearch로 최신 재테크 트렌드, ISA/연금저축 혜택, 인덱스펀드 등을 검색하고
    다음 JSON을 /tmp/rich-guide-curator-{TS}.json 에 저장하세요:
    {{
      "status": "success",
      "agent": "info-curator",
      "curated_info": [
        {{
          "title": "기사 제목",
          "source": "도메인",
          "url": "URL",
          "summary": "핵심 내용 1-2문장",
          "verified": true/false,
          "relevance": "high/medium/low"
        }}
      ],
      "key_insights": ["핵심 인사이트1", "핵심 인사이트2", "핵심 인사이트3"],
      "tax_benefits": ["ISA 세제혜택", "연금저축 세액공제 등 해당되는 것들"]
    }}

    Write 도구로 파일을 저장하세요.
    """
)

Task(
    subagent_type="market-context-analyzer",
    model="claude-sonnet-4-5-20250929",
    description="시장 상황 분석",
    prompt=f"""
    현재 한국 및 글로벌 투자 시장 상황을 분석하세요.

    분석 대상:
    1. 현재 기준금리 환경 (예금 매력도)
    2. KOSPI/S&P500 밸류에이션 (인덱스 투자 적정성)
    3. 부동산 시장 동향 (내 집 마련 타이밍)
    4. 인플레이션 환경 (실질 수익률 관점)

    portfolio-copilot 데이터 확인 시도 (선택적):
    - ~/.claude/plugins/portfolio-copilot/data/portfolio.db 존재 여부 확인 후 활용
    - 파일이 없으면 경고 없이 WebSearch로 대체

    다음 JSON을 /tmp/rich-guide-market-{TS}.json 에 저장하세요:
    {{
      "status": "success",
      "agent": "market-context-analyzer",
      "market_summary": "현재 시장 상황 2-3문장 요약",
      "interest_rate_env": "high/medium/low (예금 매력도)",
      "equity_valuation": "overvalued/fair/undervalued",
      "key_opportunities": ["기회1", "기회2"],
      "key_risks": ["리스크1", "리스크2"],
      "recommended_asset_allocation": {{
        "deposits": 예금 비중(%),
        "bonds": 채권 비중(%),
        "domestic_equity": 국내주식 비중(%),
        "global_equity": 해외주식 비중(%),
        "real_estate": 부동산 비중(%),
        "alternatives": 대안투자 비중(%)
      }}
    }}

    Write 도구로 파일을 저장하세요.
    """
)

# Read Phase 1 results — called AFTER all Task() calls above have completed
def read_agent_output(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

diag = read_agent_output(f"/tmp/rich-guide-diagnostician-{TS}.json",
    {"status": "failed", "health_score": 50, "monthly_surplus": profile['monthly_income'] - profile['monthly_expense'],
     "diagnosis": "진단 데이터 없음", "strengths": [], "weaknesses": [], "recommended_investment_ratio": 20})

curator = read_agent_output(f"/tmp/rich-guide-curator-{TS}.json",
    {"status": "failed", "curated_info": [], "key_insights": [], "tax_benefits": []})

market = read_agent_output(f"/tmp/rich-guide-market-{TS}.json",
    {"status": "failed", "market_summary": "시장 데이터 없음", "key_opportunities": [], "key_risks": [],
     "recommended_asset_allocation": {"deposits": 40, "bonds": 10, "domestic_equity": 20, "global_equity": 20, "real_estate": 10, "alternatives": 0}})

# Save Phase 1 combined
phase1 = {"diagnostician": diag, "curator": curator, "market": market, "profile": profile}
with open(f"/tmp/rich-guide-phase1-{TS}.json", "w") as f:
    json.dump(phase1, f, ensure_ascii=False, indent=2)

print(f"Phase 1 완료 - 재무건강점수: {diag.get('health_score', 'N/A')}점")
```

---

### Step 4: Phase 2 - Sequential Strategy then Evaluation

wealth-strategist runs first so it produces real strategy IDs. risk-reward-evaluator then runs with those actual strategies, enabling grounded per-strategy suitability scoring.

```python
print("Phase 2-A: 전략 생성 중 (wealth-strategist)...")

Task(
    subagent_type="wealth-strategist",
    model="claude-opus-4-6",
    description="개인화 부자 전략 생성",
    prompt=f"""
    Phase 1 진단 결과를 바탕으로 3-5개의 다양한 부자 전략을 생성하세요.

    재무 프로필:
    {json.dumps(phase1['profile'], ensure_ascii=False)}

    재무 진단:
    {json.dumps(phase1['diagnostician'], ensure_ascii=False)}

    시장 상황:
    {json.dumps(phase1['market'], ensure_ascii=False)}

    큐레이션 인사이트:
    {json.dumps(phase1['curator'].get('key_insights', []), ensure_ascii=False)}

    세금 혜택:
    {json.dumps(phase1['curator'].get('tax_benefits', []), ensure_ascii=False)}

    전략 다양성 필수 요건:
    - 리스크 범위: 저위험(예금/채권) + 중위험(인덱스) + 고위험(개별주식) 포함
    - 시간 범위: 단기(1년) + 중기(3년) + 장기(10년) 고루 포함
    - 분야: 투자 / 부업 / 커리어 성장 / 비용 절감 중 최소 2개 이상

    다음 JSON을 /tmp/rich-guide-strategist-{TS}.json 에 저장하세요:
    {{
      "status": "success",
      "agent": "wealth-strategist",
      "strategies": [
        {{
          "id": "S1",
          "title": "전략명",
          "category": "investment/side-hustle/career/cost-saving",
          "risk_level": "low/medium/high",
          "time_horizon": "short/mid/long",
          "expected_return": "연 X%",
          "initial_capital": 초기 자본(만원),
          "monthly_commitment": "월 X시간 또는 X만원",
          "description": "전략 설명 (3-4문장)",
          "pros": ["장점1", "장점2", "장점3"],
          "cons": ["단점1", "단점2"],
          "first_step": "당장 할 수 있는 첫 번째 행동",
          "sources": []
        }}
      ]
    }}

    Write 도구로 파일을 저장하세요.
    """
)

# Read strategist output before launching evaluator
strategist = read_agent_output(f"/tmp/rich-guide-strategist-{TS}.json",
    {"status": "failed", "strategies": [
        {"id": "S1", "title": "ISA 인덱스 ETF 적립식", "category": "investment", "risk_level": "medium",
         "time_horizon": "long", "expected_return": "연 7-10%", "initial_capital": 0,
         "monthly_commitment": "월 30만원", "description": "ISA 계좌를 통해 국내외 인덱스 ETF에 매월 자동 적립하는 방법입니다.",
         "pros": ["세제 혜택", "복리 효과", "간단함"], "cons": ["장기 투자 필요"],
         "first_step": "증권사 ISA 계좌 개설", "sources": []}
    ]})

strategies = strategist.get("strategies", [])
print(f"전략 생성 완료 - {len(strategies)}개 전략")

print("Phase 2-B: 리스크/보상 평가 중 (risk-reward-evaluator)...")

Task(
    subagent_type="risk-reward-evaluator",
    model="claude-sonnet-4-5-20250929",
    description="전략별 리스크/보상 평가",
    prompt=f"""
    사용자 재무 상황에서 아래에 실제 생성된 전략들의 리스크/보상을 평가하세요.

    재무 프로필:
    {json.dumps(phase1['profile'], ensure_ascii=False)}

    재무 건강도 점수: {phase1['diagnostician'].get('health_score', 50)}
    월 잉여금: {phase1['diagnostician'].get('monthly_surplus', 100)}만원
    리스크 성향: {phase1['profile']['risk_tolerance']}

    실제 생성된 전략 목록 (각 전략의 id와 title을 evaluations에서 그대로 사용하세요):
    {json.dumps(strategies, ensure_ascii=False)}

    다음 JSON을 /tmp/rich-guide-evaluator-{TS}.json 에 저장하세요:
    {{
      "status": "success",
      "agent": "risk-reward-evaluator",
      "user_risk_capacity": "실제 감당 가능 리스크 수준 평가",
      "evaluations": [
        {{
          "strategy_id": "strategist가 생성한 실제 id (예: S1)",
          "strategy_title": "전략 제목 (strategist와 동일)",
          "risk_score": 1-10,
          "reward_potential": "연 예상 수익률 범위",
          "suitable_for_user": true/false,
          "suitability_reason": "적합/부적합 이유",
          "max_allocation": "최대 권장 비중(%)"
        }}
      ],
      "overall_recommendation": "전반적 포트폴리오 방향성 2-3문장"
    }}

    Write 도구로 파일을 저장하세요.
    """
)

# Read evaluator output
evaluator = read_agent_output(f"/tmp/rich-guide-evaluator-{TS}.json",
    {"status": "failed", "overall_recommendation": "리스크 분산을 통한 균형 포트폴리오 구성을 권장합니다.", "evaluations": []})

phase2 = {"strategist": strategist, "evaluator": evaluator}
with open(f"/tmp/rich-guide-phase2-{TS}.json", "w") as f:
    json.dump(phase2, f, ensure_ascii=False, indent=2)

print(f"Phase 2 완료 - {len(strategies)}개 전략 평가 완료")
```

---

### Step 5: Strategy Selection

```python
# Display strategies with risk/reward summary
strategy_options = []
for s in strategies:
    risk_label = {"low": "저위험", "medium": "중위험", "high": "고위험"}.get(s.get("risk_level"), "중위험")
    horizon_label = {"short": "단기(1년)", "mid": "중기(3년)", "long": "장기(10년+)"}.get(s.get("time_horizon"), "중기")
    strategy_options.append({
        "label": s.get("title", f"전략 {s.get('id', '?')}"),
        "description": f"{risk_label} | {horizon_label} | {s.get('expected_return', 'N/A')}"
    })

selected = AskUserQuestion(questions=[{
    "question": "어떤 전략을 먼저 실행하시겠어요?",
    "header": "전략 선택",
    "options": strategy_options
}])

selected_title = selected.get("전략 선택")
chosen_strategy = next(
    (s for s in strategies if s.get("title") == selected_title),
    strategies[0] if strategies else {"title": "기본 전략", "description": "ISA 인덱스 ETF 적립식"}
)
print(f"선택된 전략: {chosen_strategy.get('title')}")
```

---

### Step 6: Phase 3 - Action Plan Generation

The action-plan-generator reads the roadmap template and populates it.

```python
print("Phase 3: 실행 계획 생성 중...")

roadmap_path = f"{ROADMAP_DIR}/roadmap-{TS}.md"
template_path = os.path.expanduser("~/.claude/skills/rich-guide/templates/roadmap-template.md")

# Read template so action-plan-generator can populate placeholders
template_content = ""
try:
    with open(template_path) as f:
        template_content = f.read()
except FileNotFoundError:
    template_content = "(템플릿 파일 없음 - 아래 형식으로 직접 생성하세요)"

Task(
    subagent_type="action-plan-generator",
    model="claude-opus-4-6",
    description="주간 실행 체크리스트 생성",
    prompt=f"""
    선택된 전략에 대한 구체적인 주간 실행 계획을 작성하세요.

    선택된 전략:
    {json.dumps(chosen_strategy, ensure_ascii=False)}

    사용자 재무 상황:
    - 월 잉여금: {phase1['diagnostician'].get('monthly_surplus', 100)}만원
    - 리스크 성향: {phase1['profile']['risk_tolerance']}
    - 목표: {phase1['profile'].get('goal', '재테크')}
    - 재무 건강도: {phase1['diagnostician'].get('health_score', 50)}점
    - 주요 강점: {json.dumps(phase1['diagnostician'].get('strengths', []), ensure_ascii=False)}
    - 개선 사항: {json.dumps(phase1['diagnostician'].get('weaknesses', []), ensure_ascii=False)}
    - 순자산: {phase1['diagnostician'].get('savings', 0) + phase1['profile'].get('investment_assets', 0) - phase1['profile'].get('debt', 0)}만원

    시장 상황: {phase1['market'].get('market_summary', '')}

    평가 요약: {phase2['evaluator'].get('overall_recommendation', '')}

    큐레이션 출처:
    {json.dumps(phase1['curator'].get('curated_info', [])[:3], ensure_ascii=False)}

    로드맵 템플릿 (아래 플레이스홀더를 실제 값으로 채워서 최종 마크다운을 작성하세요):
    {template_content}

    위 템플릿의 모든 {{PLACEHOLDER}} 를 실제 내용으로 채워 완성된 마크다운을 {roadmap_path} 에 저장하세요.

    Write 도구를 사용해 파일을 저장하세요.
    반드시 파일 경로 {roadmap_path} 에 저장하세요.
    """
)

print(f"Phase 3 완료")
```

---

### Step 7: Display Final Report & Cleanup

```python
print("\n" + "="*60)
print("부자 로드맵 생성 완료!")
print("="*60)

print(f"""
면책 조항
이 분석은 AI가 생성한 참고용 정보입니다.
투자 결정은 본인의 판단과 책임 하에 이루어져야 하며,
중요한 재무 결정 전에는 전문 재무설계사와 상담하시기 바랍니다.
""")

print(f"재무 건강 점수: {phase1['diagnostician'].get('health_score', 'N/A')}점")
print(f"월 잉여금: 약 {phase1['diagnostician'].get('monthly_surplus', 'N/A')}만원")
print()
print(f"선택된 전략: {chosen_strategy.get('title')}")
print(f"기대 수익: {chosen_strategy.get('expected_return', 'N/A')}")
print(f"리스크: {chosen_strategy.get('risk_level', 'N/A')}")
print()
print(f"생성된 로드맵: {roadmap_path}")
print()

# Show verified sources
sources = [s for s in phase1['curator'].get('curated_info', []) if s.get('verified')]
if sources:
    print("참고 자료:")
    for src in sources[:3]:
        print(f"  - {src.get('source', '')}: {src.get('title', '')} ({src.get('url', '')})")

print()
print("다음 단계:")
print("1. 위 로드맵 파일을 열어 1주차 체크리스트 확인")
print("2. 재무설계사 상담: https://www.fpsb.or.kr/")
print("3. 소액 테스트 시작 (첫 달은 월 10만원 이하 권장)")

# Cleanup /tmp files for this session
import glob
for tmp_file in glob.glob(f"/tmp/rich-guide-*-{TS}.json"):
    try:
        os.remove(tmp_file)
    except OSError:
        pass
```

---

## Error Handling

| Error | Response |
|-------|----------|
| DB init 실패 | "데이터베이스 초기화 실패. python3 설치 여부 확인 후 재시도하세요." |
| agent-config.yaml 없음 | 하드코딩된 기본값으로 계속 진행 (경고 표시 없음) |
| 에이전트 결과 파일 없음 | 기본값 fallback 적용, 경고 메시지 표시 후 계속 진행 |
| 모든 에이전트 실패 | "네트워크 연결을 확인하고 다시 시도하세요. 기본 전략을 제공합니다." |
| json.loads 파싱 실패 | JSONDecodeError 캐치 → {"exists": False} 기본값 사용 |

## Model Selection

| Agent | Model | Reason |
|-------|-------|--------|
| financial-diagnostician | claude-sonnet-4-5-20250929 | 수치 분석 |
| info-curator | claude-haiku-4-5 | 정보 수집 속도 우선 |
| market-context-analyzer | claude-sonnet-4-5-20250929 | 시장 분석 |
| wealth-strategist | claude-opus-4-6 | 창의적 전략 생성 |
| risk-reward-evaluator | claude-sonnet-4-5-20250929 | 정량적 리스크 평가 |
| action-plan-generator | claude-opus-4-6 | 구체적 계획 작성 |

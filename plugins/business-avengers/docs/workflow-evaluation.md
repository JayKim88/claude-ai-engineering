# Business Avengers 전체 워크플로우 평가

**Date**: 2026-02-22
**Evaluator**: Claude Opus 4.6
**Scope**: SKILL.md(~1970줄), org-structure.yaml, init-project.py, 23개 에이전트 정의, 49개 템플릿, 11개 KB

평가 방법: 아키텍처 → UX → 데이터 무결성 → 확장성 → MAKE 통합 순으로 평가.
이미 알려진 TODO-v2.1-audit.md (31개 항목) 외의 구조적/설계적 관점에 집중.

---

## 1. 아키텍처 평가

### 1.1 잘 설계된 부분

- **Orchestrator/Worker 분리**: Opus가 지휘, Sonnet 서브에이전트가 실행 — 모델 비용 최적화
- **Document-as-Code**: 모든 산출물이 마크다운 → 버전 관리, 비교, 편집 용이
- **org-structure.yaml 단일 진실 원천**: Phase 파이프라인, 조직도, 워크플로우가 한 곳에
- **init-project.py 분리**: 프로젝트 CRUD를 Python CLI로 격리 → SKILL.md가 비즈니스 로직에만 집중
- **에이전트 프롬프트 일관성**: 역할→정의→컨텍스트→KB→템플릿→작업 구조가 모든 Phase에서 동일

### 1.2 구조적 문제

#### A. Pseudocode의 실행 불확실성 (HIGH)

SKILL.md는 Python처럼 보이지만 실제 코드가 아닌 **LLM이 해석하는 의사코드**.

```python
for q in questions:
    AskUserQuestion(q, allow_freeform=true)
```

이 루프가 실제로 5번 반복될지, 3번에서 끊길지, LLM 판단에 의존.
비슷하게 `if is_sprint:` 분기, 변수 할당, Glob 결과 조건부 처리 모두
**LLM의 정확한 해석에 의존하는 implicit contract**.

**위험**: 모델 버전 업데이트, 컨텍스트 길이 변화, 프롬프트 순서에 따라
동일 입력에 다른 실행 경로가 나올 수 있음.

#### B. 명시적 실행 루프 부재 (HIGH)

Step 4~16이 각각 `**Condition**: Only runs if Phase X is in phases_to_run`이라는
텍스트 조건을 가지지만, **실제 for/while 루프 구문이 없음**.

LLM이 phases_to_run = [0,1,7,8,10,11] 이면:
- Step 4 (Phase 0) 실행 ✓
- Step 5 (Phase 1) 실행 ✓
- Step 6 (Phase 2) ... 건너뛰어야 함
- ...
- Step 11 (Phase 7) 실행 ✓

**13개 Step의 조건부 실행을 LLM이 순서대로 추론**해야 함.
장문의 SKILL.md를 읽은 후반부에서 Phase 건너뛰기를 놓칠 위험.

#### C. 모놀리식 SKILL.md (~1970줄) (MEDIUM)

하나의 파일에 모든 오케스트레이션 로직이 있음:
- Step 0-3: 초기화 + 모드 라우팅
- Step 4-16: 13개 Phase 실행 (각 80-150줄)
- Step 17-21: 유틸리티 모드

LLM이 1970줄을 읽고 실행해야 하므로:
- 후반 Phase(10-12)에서 초반 패턴(Step 0의 변수 설정)을 잊을 수 있음
- 디버깅이 어려움 (어느 Step에서 오동작했는지 추적 불가)
- 유지보수 시 하나 수정하면 side effect 예측 어려움

#### D. C-Level 임원 = 텍스트 역할극 (MINOR)

5명의 C-Level (CPO, CTO, CMO, CFO, COO)은 별도 Task()로 호출되지 않음.
오케스트레이터가 `[CFO] 시장 조사 결과를 보고드립니다`처럼 텍스트로 흉내 냄.

"23개 AI 에이전트"라고 소개하지만 실제 서브프로세스로 동작하는 건 **18개**.
C-Level에게 별도 에이전트 정의(.md)도, KB도, 전용 모델도 없음.

이것 자체는 합리적 설계(C-Level은 판단/라우팅이고 실무가 아니므로) 이지만,
사용자 기대치와 불일치.

---

## 2. UX 평가

### 2.1 CEO 인터랙션 플로우

| 이슈 | 심각도 | 설명 |
|------|--------|------|
| **승인 게이트 dead-end** | CRITICAL | 12개 AskUserQuestion에서 "수정 요청"/"피봇"/"중단" 선택 시 분기 없이 바로 `update-phase completed` 실행. CEO 피드백 완전 무시. |
| **Phase 0 Q&A 강제 5회** | MEDIUM | `for q in questions` (5개) 강제 실행. CEO가 3번째에서 "충분하다"고 해도 멈출 수 없음. |
| **승인 옵션 비일관** | MINOR | Phase 4,5,6,9: "확인/질문/수정" vs Phase 1,2,3,7,8: "승인/수정/피봇/중단" — delegate vs approve 구분은 의도적이나, "질문 있음" 선택 시 어떻게 되는지 미정의 |
| **Phase 12 Deep Dialogue** | 좋음 | 에이전트 실행 전 CEO 전략 대화 — 유일하게 CEO 입력이 에이전트 프롬프트에 반영되는 패턴 |

### 2.2 워크플로우 프리셋 UX

| 프리셋 | 실행 Phase | 문제 |
|--------|-----------|------|
| idea-first | [0..9] | **안전**. 모든 의존성 충족. |
| market-first | [1,0,2..9] | Phase 0이 Phase 1 결과를 읽지 않음 (M7). 순서 반전의 실질적 효과 없음. |
| mvp-build | [0,2,4,5,7] | Phase 2가 Phase 1 없이 실행 → 시장 데이터 없는 PRD. 의도적이면 OK. |
| **make** | [0,1,7,8,10,11] | **위험**. Phase 2 스킵 → Phase 7,8,10,11이 PRD 없이 실행. 빈 컨텍스트로 마케팅/가격/성장 전략 생성. |
| **post-launch** | [10,11,12] | **위험**. 이전 Phase 산출물 전무. 기존 서비스 임포트 온보딩 없음. |
| full-lifecycle | [0..12] | **안전**하나 ~33 에이전트 호출 = 높은 비용 + 긴 실행시간. |
| custom | [] | CEO 선택 — 의존성 검증 없음. |

**핵심 문제**: 프리셋은 "어떤 Phase를 실행할지"만 정의하고,
"스킵된 Phase의 산출물을 누가 대체하는지"는 정의하지 않음.

### 2.3 Sprint UX

| 이슈 | 심각도 |
|------|--------|
| 옵션 8개 flat list, 그루핑 없음 | MEDIUM |
| "수정" vs "업데이트" vs "분석" 용어 혼재 | MINOR |
| Phase 0,1,5,6,8,9 스프린트 옵션 누락 (선택 불가) | MEDIUM |
| 백업이 Phase당 주요 파일 1개만 (나머지 2-4개 유실) | HIGH |
| sprint_goal이 Phase 11 sprint_context에 누락 | MEDIUM |

---

## 3. 데이터 무결성 평가

### 3.1 변수 미정의

| 변수 | 사용 위치 | 상태 |
|------|----------|------|
| `current_version` | 12개 backup 호출 | **정의 안 됨**. 항상 undefined. |
| `project_slug` | RESUME/SPRINT/SINGLE 모드 | Step 2 건너뛰면 **미정의** |
| `workflow` | RESUME 모드 (line 166) | **미정의**. phases_to_run 계산 불가 |
| `sprint` vs `is_sprint` | Phase 1 (lines 285, 312, 341) | **이름 불일치**. `sprint` 사용하나 변수는 `is_sprint` |
| `selected_option` | Phase 12 (line 1656) | AskUserQuestion 반환값 참조인데 **Claude Code의 실제 반환 메커니즘과 무관** |

### 3.2 파일 읽기 안전성

| 패턴 | 사용 횟수 | 안전 |
|------|----------|------|
| `Glob() + 조건부 Read` | ~12회 | 안전 (파일 없으면 빈 문자열) |
| `직접 Read()` | ~14회 | **위험** (파일 없으면 크래시) |

직접 Read()의 대부분은 Phase 2 PRD를 읽는 패턴.
`make`/`post-launch` 프리셋에서 Phase 2 미실행 시 크래시.

### 3.3 버전 관리

- `update-phase` 호출 시 항상 `v1.0` 하드코딩: `update-phase '{slug}' 0 completed v1.0`
- Sprint 모드에서도 `v1.0` → 버전 추적이 실질적으로 불가능
- backup 파일명: `{name}-{current_version}-{date}.md`인데 current_version이 undefined

---

## 4. 확장성 평가

### 4.1 컨텍스트 윈도우 압박

| 모드 | 예상 오케스트레이터 컨텍스트 사용량 |
|------|--------------------------------|
| idea-first (10 Phase) | SKILL.md ~1970줄 + Phase 산출물 누적 읽기 + CEO 대화 → **~50K 토큰** |
| full-lifecycle (13 Phase) | 위 + Phase 10-12 입력/출력 → **~70K 토큰** |
| Sprint (1-3 Phase) | SKILL.md + 기존 문서 + sprint_context → **~30K 토큰** |

Phase 후반(10-12)에서 오케스트레이터가 이전 Phase 산출물을 변수에 Read하여 축적.
Phase 12는 pricing + financials + growth + automation 4개 파일을 동시에 메모리에 보유.

**위험**: 컨텍스트 압축이 발생하면 초기 Step의 변수 정의나 조건 패턴을 잃을 수 있음.

### 4.2 비용 효율성

| 항목 | idea-first | full-lifecycle | make |
|------|-----------|----------------|------|
| 에이전트 Task() 호출 | ~24 | ~32 | ~16 |
| 에이전트당 Read() 평균 | 3-4 | 3-4 | 3-4 |
| CEO AskUserQuestion | ~15 | ~19 | ~10 |
| 예상 총 API 호출 | ~40 | ~52 | ~27 |

각 에이전트 Task()는 별도 Sonnet 세션 = 별도 과금.
에이전트 내부 Read()도 각각 도구 호출 = 라운드트립.

### 4.3 에이전트 컨텍스트 효율성

현재 패턴: 오케스트레이터가 파일을 Read → 변수에 저장 → 에이전트 프롬프트에 f-string으로 주입

```python
prd = Read("{PROJECT_DIR}/phase-2-product-planning/prd.md")  # 오케스트레이터가 읽음
...
prompt=f"프로젝트 컨텍스트:\n- PRD: {prd}"  # 에이전트에 전달
```

**동시에** 에이전트는 `에이전트 정의 (Read로 읽으세요)`, `KB (Read로 읽으세요)`,
`템플릿 (Read로 읽으세요)`를 **자기가 Read**.

즉 같은 정보가 두 곳에서 읽힘:
- 프로젝트 컨텍스트: 오케스트레이터가 읽어서 변수로 전달 (주입)
- 에이전트 정의/KB/템플릿: 에이전트가 직접 Read (경로만 전달)

이 **하이브리드 패턴**은 합리적이나 (프로젝트 데이터는 확실히 전달, 정적 참조는 에이전트가),
문서화되지 않아 유지보수 시 혼동 가능.

---

## 5. MAKE 통합 평가

### 5.1 콘텐츠 충실도

| KB 파일 | MAKE 책 챕터 | 충실도 | 평가 |
|---------|-------------|--------|------|
| growth-tactics.md (1521줄) | Grow | 높음 | Organic First, BIP, Repeated Launch 정확 반영 |
| automation-guide.md (1524줄) | Automate | 높음 | Robots > Hiring, Bus Test 철학 정확 |
| exit-guide.md (1611줄) | Exit | 높음 | 5 Buyer Types, FIRE, Post-Sale Psychology 포함 |

KB 품질은 전체적으로 우수. 책의 핵심 철학을 잘 추출.

### 5.2 에이전트 통합 품질

| 에이전트 | 추가된 MAKE 전문성 | 평가 |
|---------|-------------------|------|
| cpo.md | Own Problem, Micro-Niche, Idea Source | 적절 — 핵심 원칙 |
| product-manager.md | MVP-First, No-Code Assessment | 적절 |
| growth-hacker.md | Organic Growth, BIP, Repeated Launch, API Growth | 적절 |
| marketing-strategist.md | Repeated Launch Strategy | 1줄 추가 — 다른 에이전트 대비 빈약 |
| pr-manager.md | Indie Press, Side Project Marketing, BIP PR | 적절 |
| revenue-strategist.md | Biz Model Experimentation, Payment Platform, Refund | 적절 |
| devops-engineer.md | Automation Architecture | 1줄 추가 — 다른 에이전트 대비 빈약 |

**marketing-strategist와 devops-engineer의 MAKE 통합이 불균형.**
다른 에이전트는 전문성 3-4개 + 실행 전략 8-10단계를 추가했는데,
이 둘은 Expert Frameworks에 1줄만 추가.

### 5.3 make 프리셋 설계 결함

`make: [0, 1, 7, 8, 10, 11]`

MAKE 책의 철학: **Idea → Build → Launch → Grow → Monetize → Automate → Exit**

| MAKE 단계 | 매핑된 Phase | 문제 |
|-----------|------------|------|
| Idea | Phase 0 ✓ | OK |
| Build | **없음** (Phase 2-6 전부 스킵) | **MAKE 책은 "Build"가 핵심**. "Build it yourself" 를 건너뜀 |
| Launch | Phase 7 ✓ | PRD 없이 GTM 전략 작성 → 제품 컨텍스트 부재 |
| Monetize | Phase 8 ✓ | PRD 없이 가격 전략 → 기능 tier 매핑 불가 |
| Grow | Phase 10 ✓ | Phase 9 metrics 없이 성장 전략 |
| Automate | Phase 11 ✓ | Phase 5 deployment, Phase 9 cs-playbook 없이 자동화 감사 |
| Exit | **없음** (Phase 12 미포함) | MAKE 전체 생명주기에서 Exit 누락 |

**make 프리셋이 MAKE 책의 Build를 완전히 빠뜨리고, Exit도 빠뜨림.**
이것은 이름(MAKE)과 내용의 불일치.

---

## 6. 종합 평가

### 점수

| 영역 | 점수 | 근거 |
|------|------|------|
| 아키텍처 설계 | 7/10 | Orchestrator/Worker 분리 우수, 단 실행 불확실성과 모놀리식 구조가 약점 |
| UX 플로우 | 4/10 | 승인 게이트 dead-end, 프리셋 의존성 미검증, Sprint 옵션 미완성 |
| 데이터 무결성 | 3/10 | 5개 변수 미정의, 14개 unsafe Read, 버전 관리 미작동 |
| 확장성 | 6/10 | 비용 합리적이나 컨텍스트 윈도우 압박 우려 |
| MAKE 통합 | 7/10 | KB 우수, 에이전트 적절, 단 make 프리셋 설계 결함 |
| 콘텐츠 품질 | 8/10 | 템플릿과 KB 모두 실용적이고 상세 |
| **종합** | **5.8/10** | **골격은 좋으나 런타임 안정성과 UX가 미완성** |

### 핵심 결론

**강점**: 아이디어 → 매각까지의 비즈니스 파이프라인을 23개 AI 에이전트로 자동화한다는
컨셉 자체가 독창적이고 야심적. org-structure.yaml 중심 설계, KB/Template/Agent 분리,
Sprint 기반 반복 구조가 확장 가능한 기반을 제공.

**약점**: 실행 레이어가 "LLM의 선의"에 의존. 변수 미정의, 안전하지 않은 Read,
승인 게이트 무시, 워크플로우 의존성 미검증 등 런타임 크래시 요소가 다수.
현재 상태로는 idea-first 모드만 안정적으로 실행 가능하며,
make/post-launch/market-first 프리셋은 실질적으로 사용 불가.

---

## 7. 권장 개선 우선순위

### Tier 1: 실행 가능성 확보 (없으면 크래시)
1. C3 — 14개 unsafe Read를 Glob+조건부로 전환
2. C4 — sprint vs is_sprint 변수명 통일
3. H4 — current_version 변수 정의
4. H5 — project_slug 모든 모드에서 정의
5. C2 — KB 파일 참조 오류 수정

### Tier 2: UX 핵심 결함 수정 (없으면 사용자 혼란)
6. C1 — 승인 게이트 분기 로직 추가
7. make 프리셋 재설계 (Phase 2 포함 또는 fallback 컨텍스트)
8. post-launch 온보딩 플로우 추가
9. I10 — 명시적 Phase 실행 루프 추가
10. I11 — 완료 Step으로의 라우팅 추가

### Tier 3: 품질 향상 (없어도 동작하지만 경험 저하)
11. Sprint 옵션 그루핑 + 누락 Phase 추가
12. market-first 모드에서 Phase 0이 Phase 1 결과 참조
13. 에이전트 출력 검증 (파일 생성 확인)
14. 버전 자동 증가 로직
15. marketing-strategist / devops-engineer MAKE 통합 보강

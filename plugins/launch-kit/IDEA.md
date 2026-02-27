# launch-kit — Idea Document

**Status:** Concept (Pre-PRD)
**Date:** 2026-02-27
**Next step:** planning-interview로 PRD 생성

---

## 한 줄 정의

아이디어 → 바로 시장에 낼 수 있는 콘텐츠 재료 일체를 생성하는 Claude Code 플러그인.

---

## 문제

인디해커가 아이디어를 검증하려면 랜딩페이지, 커뮤니티 포스트, 이메일이 필요하다.
코드는 AI로 빠르게 만들 수 있지만, **"뭘 써야 하나"** — 카피/포스트 작성에 수 시간이 소요된다.

---

## 솔루션

5분 인터뷰 → 검증에 필요한 모든 콘텐츠를 한 번에 생성.

---

## 타겟 사용자

인디해커 / 솔로 빌더 — AI 도구로 제품을 빠르게 만들고, 시장 반응을 먼저 테스트하려는 사람.

---

## 핵심 출력물

| 출력 | 내용 |
|------|------|
| **랜딩페이지 카피** | Headline, Subheadline, 핵심 기능 3가지, CTA, FAQ (5개) |
| **커뮤니티 포스트** | Indie Hackers 형식 + Reddit r/SideProject 형식 |
| **이메일 시퀀스** | 웰컴 이메일 + 3일 후 팔로업 |
| **선판매 오퍼** | Founding Plan 카피 (50% 할인, 얼리어답터 혜택 문구) |

모든 출력은 하나의 마크다운 파일로 저장: `{product-slug}/launch-kit.md`

---

## 인터뷰 구조 (4문항)

planning-interview Solo Mode Phase 1 질문을 그대로 재사용:

1. **문제** — "이 제품이 해결하는 구체적인 문제는? 타겟 사용자가 이 문제를 겪는 실제 상황을 설명해주세요."
2. **솔루션** — "한 문장으로 솔루션을 설명해주세요. 기존 대안과 비교했을 때 무엇이 다른가요?"
3. **타겟** — "주요 타겟 사용자는 누구인가요? 역할, 필요한 것, 현재 사용하는 대안을 구체적으로."
4. **MVP 범위** — "MVP에서 반드시 필요한 기능 3가지는? 그리고 v2로 미룰 수 있는 것은?"

---

## 플러그인 아키텍처

**Pattern:** Simple Skill (에이전트 불필요)

```
plugins/launch-kit/
├── IDEA.md                          ← 이 파일
├── skills/launch-kit/SKILL.md       ← 핵심 로직
├── templates/launch-kit-output.md   ← 출력 템플릿
├── .claude-plugin/plugin.json
├── README.md
└── CLAUDE.md
```

**흐름:**
```
트리거 감지
    → 4문항 인터뷰 (자유응답)
    → 콘텐츠 생성 (랜딩 + 포스트 + 이메일 + 오퍼)
    → {product-slug}/launch-kit.md 저장
    → 다음 단계 안내 (planning-interview 연계)
```

---

## planning-interview와의 관계

```
launch-kit         →  아이디어 검증 재료 생성  (검증 전)
planning-interview →  PRD / 기술 명세 생성    (검증 후, 빌드 전)
```

launch-kit 완료 후 자동으로 안내:
> "시장 반응을 확인한 후 `planning-interview`로 PRD를 작성하세요."

---

## 트리거 문구 (예상)

- `launch-kit`
- `아이디어 검증`
- `랜딩페이지 만들어줘`
- `validate my idea`
- `검증 키트`

---

## 결정된 사항

| 항목 | 결정 |
|------|------|
| 커뮤니티 포스트 범위 | Indie Hackers + Reddit r/SideProject (Slack 제외) |
| 이메일 시퀀스 | 2통 — 웰컴 이메일 + D+3 팔로업 |
| 선판매 오퍼 | 항상 포함 (Founding Plan 카피) |
| 다국어 | 트리거 언어 자동 감지 (한국어/영어) |
| 출력 경로 | `{cwd}/{product-slug}/launch-kit.md` |

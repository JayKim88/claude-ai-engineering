# LinguaRAG Planning Docs - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/claude-ai-engineering`
> **Scope**: `projects/lingua-rag/` — planning-interview로 생성한 기획 문서 (개발 작업과 분리)

## Session: 2026-02-25 18:15

> **Context**: planning-interview v2.0 E2E 테스트 — LinguaRAG를 대상으로 4종 기획 문서 생성 (PRD, User Journey Map, Tech Spec, Wireframe Spec)

### Done

- docs(lingua-rag): planning-interview v2.0 Startup 모드로 4종 기획 문서 생성
  - `projects/lingua-rag/prd.md` — Product Brief (기존 Product Brief 임포트 → GTM 1개 질문만 추가)
  - `projects/lingua-rag/user-journey-map.md` — 3 Journey (첫 방문/온보딩, 일반 Q&A, 단원 전환), 온보딩 6단계 ~2분, 리텐션 루프
  - `projects/lingua-rag/tech-spec.md` — 아키텍처(Next.js 15 + FastAPI + PostgreSQL + Railway/Vercel), 6 FR, 3-Phase 구현 계획, NFR
  - `projects/lingua-rag/wireframe-spec.md` — 4 화면 ASCII 레이아웃 (레벨 선택, 교재 선택, 메인 채팅, 단원 전환 모달), 반응형/접근성

### Decisions

- **단원 패널 UI**: 트리 구조 (교재 > Band > 단원 펼치기/접기) — 드롭다운 대비 단원 간 컨텍스트 가시성 우수
- **입력창 문자 카운터**: 우하단 실시간 표시 ("48/500") — 초과 시에만 표시보다 예측 가능성 높음
- **v0.1 Auth 전략**: 없음(단일 사용자 private) → v0.3에서 NextAuth.js 이메일 Magic Link 추가 예정
- **컨텍스트 윈도우**: 최근 10개 메시지 sliding window — 단순성 우선, v0.2에서 요약 압축 검토

### Next

- [ ] tech-spec.md 기반 Phase 1 구현 착수 (FastAPI POST /api/chat SSE)
  - [ ] 독독독 A1 단원 JSON 데이터 작성 (`system_prompt_context` 포함)
  - [ ] Claude API 연동 + 스트리밍 테스트
- [ ] wireframe-spec.md 기반 채팅 UI 구현 (Next.js 15)
- [ ] tech-spec.md Open Questions 해결
  - [ ] Railway 무료 티어 PostgreSQL 512MB 용량 베타 기간 충분한지 확인
  - [ ] v0.3 이메일 Auth: NextAuth.js vs Supabase Auth 비교 검토

---

## 생성된 기획 문서 현황

| 문서 | 경로 | 생성 방식 |
|------|------|---------|
| PRD (Product Brief) | `projects/lingua-rag/prd.md` | planning-interview v2.0 Startup |
| User Journey Map | `projects/lingua-rag/user-journey-map.md` | planning-interview v2.0 Startup |
| Tech Spec | `projects/lingua-rag/tech-spec.md` | planning-interview v2.0 Startup |
| Wireframe Spec | `projects/lingua-rag/wireframe-spec.md` | planning-interview v2.0 Startup |

# LinguaRAG - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/claude-ai-engineering`
> **Scope**: `projects/lingua-rag/`

## Session: 2026-02-25 17:16

> **Context**: lingua-rag 리포 README 다이어그램 추가 + docs/ 이전, competitive-agents SKILL.md Step 11.5 개선 검증

### Done

- docs: README.md에 Mermaid 다이어그램 3개 추가
  - 시스템 아키텍처 (`graph TB`): 브라우저 → Vercel → Railway → DB → Claude 전체 구성
  - SSE 채팅 흐름 (`sequenceDiagram`): 사용자 입력 → Hook → Proxy → FastAPI → session_lock → DB → Claude → SSE 스트리밍 전체 흐름
  - DB 스키마 (`erDiagram`): sessions ↔ conversations ↔ messages 관계도
- docs: `projects/lingua-rag/docs/` 3개 파일 lingua-rag repo `/docs/` 로 이전 및 push
  - `decisions.md` (ADR-001~004: pgvector, FastAPI, 임베딩 모델 보류, Vercel+Railway)
  - `f1-streaming-qa-spec.md` (F1 기능 상세 스펙)
  - `dev-log.md` (개발 일지 템플릿)
- chore: competitive-agents SKILL.md Step 11.5 개선 완료 검증 (grep으로 4개 편집 모두 확인)

### Next

- [ ] dev-log.md에 첫 개발 세션 기록 (로컬 환경 세팅 시작 시 작성)

---

## Session: 2026-02-25 14:52

> **Context**: F1 Competitive Agents 파이프라인 전체 완료 — Alpha vs Beta 2라운드 경쟁 후 Fuse, lingua-rag 리포 초기 push

### Done

- feat: F1 spec-interview 완료 → `projects/lingua-rag/docs/f1-streaming-qa-spec.md` 생성 (from previous Next)
- feat: Competitive Agents 파이프라인 7단계 전체 실행
  - Phase 1: Alpha (Pragmatist) v1, Beta (Architect) v1 병렬 생성
  - Phase 2: 크로스 리뷰 R1 — Alpha 71.5/100, Beta 62.5/100
  - Phase 3: 개선 R1 → v2
  - Phase 4: 크로스 리뷰 R2 — Alpha 82.5/100, Beta 82.5/100
  - Phase 5: 개선 R2 → v3 (Beta v3 agent 출력 누락으로 수동 복구)
  - Phase 6: Judge — Alpha 74.0 / Beta 67.0 (Alpha 승, 결정적 차이: Beta에 프론트엔드 없음)
  - Phase 7: "Fuse A + B" 선택 → `tempo/competitive-agents/lingua-rag-f1/fused/` 생성
- feat: Fused 구현 (39 files) — Beta 백엔드 아키텍처 + Alpha 프론트엔드 + 핵심 병합
  - `backend/app/main.py`: 고아 메시지 정리 SQL (Alpha) 추가
  - `backend/app/routers/chat.py`: history fetch + user persist를 `session_lock` 내부로 이동 (Alpha), LRU 1,000-entry cap
  - `backend/app/core/constants.py`: SESSION_COOKIE 상수 분리 (Beta)
  - `frontend/hooks/useChat.ts`: truncated 이벤트 처리 추가 (Beta 백엔드 기능 연동)
  - `frontend/components/MessageList.tsx`: truncated 경고 UI 추가
- feat: GitHub repo `lingua-rag` 클론 → fused 40개 파일 복사 → push (from previous Next)
- docs: `README.md` 작성 (기술 스택, 로컬 개발 가이드, 환경 변수, 배포 가이드, API 엔드포인트, 설계 결정)

### Decisions

- **Fuse 전략**: Alpha 승리했으나 Beta의 레이어드 아키텍처(routers/services/repositories) 품질이 우수 → 백엔드는 Beta, 프론트엔드는 Alpha 채택
- **asyncio.Lock 스코프**: 히스토리 fetch와 user message persist 모두 lock 내부에 배치 (race condition 방지) — 크로스 리뷰에서 발견된 Critical 이슈
- **--workers 1 고정**: asyncio.Lock은 단일 프로세스 내에서만 유효. Railway v0.1 배포 기준으로 단일 워커 유지
- **LRU 1,000 cap**: OrderedDict + popitem(last=False) 방식. Railway 트래픽 기준 보수적 설정

### Next

- [ ] 로컬 개발 환경 세팅 및 동작 확인 (backend + frontend 연결 테스트)
  - [ ] PostgreSQL 로컬 설정 → `schema.sql` 실행
  - [ ] `.env` 설정 후 `uvicorn` 실행
  - [ ] `npm run dev` 후 채팅 UI 테스트
- [ ] Railway 백엔드 배포
  - [ ] PostgreSQL 플러그인 추가
  - [ ] 환경 변수 설정 (ANTHROPIC_API_KEY, FRONTEND_URL)
- [ ] Vercel 프론트엔드 배포
  - [ ] Root Directory: `frontend` 설정
  - [ ] BACKEND_URL 환경 변수 설정
- [ ] Open Questions 해결 (이전 세션에서 이월)
  - [ ] #1: 독독독 A1 단원 데이터 저작권 확인 (텍스트 목록 내장 vs 별도 처리)
  - [ ] #2: v0.1 Auth 없이 복수 유저 구분 전략 — 세션 쿠키로 구현 완료, 다중 기기 시나리오 검토 필요
- [ ] 베타 테스터 모집 글 작성 (네이버 카페 "독일어 스터디" + Reddit r/German)
- [ ] F2~F8 기능 구현 계획 수립 (Product Brief 기준)

---

## Session: 2026-02-25 01:34

> **Context**: AI Product Engineer 킬러 프로젝트 LinguaRAG 기획 완성 — Lean Canvas → Product Brief (Startup 모드) → 독독독 A1 구조 반영

### Done

- docs: `projects/lingua-rag/lean-canvas-lingua-rag-20260225.md` 생성 (planning-interview Solo 모드)
  - 핵심 인사이트: 유저 가치 = 패턴 기반 반복 듣기/말하기 훈련 (단순 Q&A 아님)
  - 기존 대안: 독독독 플랫폼 (수동 학습 중심, 능동 훈련 부재)
  - North Star Metric: 연습 문장 세트 반복 완료 횟수
- docs: `projects/lingua-rag/product-brief-lingua-rag-v01-20260225.md` 생성 (planning-interview Startup 모드)
  - 범위: v0.1 (Week 1-4) — PDF 없이 독일어 Q&A + 단원 대시보드 + 레벨 매핑
  - 화면 구조: 좌측 Band/단원 네비게이션 + 우측 Streaming Q&A
  - 기능 목록: F1~F8 (Must/Should/Could 우선순위)
  - API 설계, DB 스키마, 시스템 프롬프트 동적 조합 로직, 에러 상태 상세화
  - 베타 테스터 설문 3가지 가설 정의 (독일어 AI 튜터 니즈 / 교재 연계 수요 / 연습 기능 수요)
- refactor(product-brief): Netzwerk A1 → 독독독 A1 구조로 단원 데이터 전면 교체
  - 56개 단원 / 8개 Band / 4가지 유형 (grammar/vocabulary/conversation/practice) 전체 하드코딩
  - 완료 단원 ✅ 표시 (Jay의 실제 진행: A1-1 ~ A1-20 완료)
  - Band 아코디언 네비게이션 + 단원 유형 아이콘 UI 설계
  - v0.2 3-패널 레이아웃 미리 설계 (구현은 v0.2)
- refactor(PROJECT_BRIEF): v0.2 섹션을 독독독 PDF 연동 중심으로 업데이트
  - 독독독 A1 Band/단원 경계 보존 chunking 전략
  - 교재 원본 페이지뷰 + 🔊 반복 듣기 + Q&A 3-패널 레이아웃
  - 저작권 처리: 유저 업로드 → 처리 후 서버 삭제 (개인 벡터 DB만 유지)

### Decisions

- **독독독 단원 구조를 v0.1 기준으로 채택**: Netzwerk가 아닌 독독독이 실제 타겟 유저 기반. v0.1에서 하드코딩 → v0.2에서 실제 PDF로 대체하는 점진적 전략
- **PDF는 기획에만 반영, 파일 제공은 v0.2 개발 시작 전**: 구조 파악은 사용자 텍스트 목록으로 충분. PDF 실제 파싱은 v0.2 시작 시점
- **단원 유형(type) 분류 도입**: grammar/vocabulary/conversation/practice로 분류 → 시스템 프롬프트를 유형에 따라 최적화 가능 (문법 단원 → 예외 패턴 강조, 회화 단원 → 대화문 중심)
- **v0.1 범위 확장**: 원래 PROJECT_BRIEF의 v0.1(Streaming Q&A만) → Product Brief에서 단원 네비게이션 + 레벨 매핑 포함. 4주 일정 타이트하므로 Week 1-2 Q&A 우선, Week 3-4 대시보드 추가 권장
- **저작권 전략**: 독독독 PDF = 유료 교재. "유저가 직접 구매한 PDF 업로드" 방식으로 저작권 문제 회피. 서버 영구 저장 금지

### Next

- [x] spec-interview로 F1(Claude Streaming Q&A) 상세 기능 스펙 작성 → competitive-agents에게 구현 의뢰
- [ ] Open Questions 해결 (v0.1 개발 시작 전)
  - [ ] #1: 독독독 A1 단원 데이터 저작권 확인 (텍스트 목록 내장 vs 별도 처리)
  - [ ] #2: v0.1 Auth 없이 복수 유저 구분 전략 결정 → 세션 쿠키로 구현 (다중 기기 검토 필요)
  - [x] #3: Fly.io 무료 티어 PostgreSQL + FastAPI 가능 여부 확인 → Railway로 변경 결정
- [ ] 경쟁사 분석 `[TODO]` 완료 (Product Brief Section 11)
  - [ ] ChatGPT Custom GPTs 중 독일어 튜터 특화 서비스 조사
  - [ ] AI 독일어 학습 스타트업 현황 조사
- [x] GitHub repo `lingua-rag` 생성 (public) → 초기 커밋 push 완료
- [x] FastAPI Hello World + Claude API Streaming → 전체 F1 구현으로 대체 (competitive agents 결과물)
- [ ] 네이버 카페 "독일어 스터디" + Reddit r/German 베타 테스터 모집 글 작성 (Week 2)
- [ ] (선택) A2 이후 교재 단원 목록 확보 → 다음 기획 확장 시 사용

---

## 생성된 문서 현황

| 문서 | 경로 | 상태 |
|------|------|------|
| PROJECT_BRIEF | `projects/lingua-rag/PROJECT_BRIEF.md` | ✅ 완료 (v0.2 섹션 업데이트) |
| Lean Canvas | `projects/lingua-rag/lean-canvas-lingua-rag-20260225.md` | ✅ 완료 |
| Product Brief (v0.1) | `projects/lingua-rag/product-brief-lingua-rag-v01-20260225.md` | ✅ 완료 (독독독 구조 반영) |
| Feature Spec (v0.1) | `projects/lingua-rag/docs/f1-streaming-qa-spec.md` | ✅ 완료 |
| F1 구현 (fused) | `tempo/competitive-agents/lingua-rag-f1/fused/` | ✅ 완료 (39 files) |
| lingua-rag 리포 | `github.com/JayKim88/lingua-rag` | ✅ 초기 push 완료 |

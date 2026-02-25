# Truth Checker - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/ai-learning`
> **Scope**: `truth-checker-service-idea.md` (아이디어 문서)

## Session: 2026-02-25 20:30

> **Context**: 거짓 내용 분석 사이트 아이디어 도출 및 종합 문서 작성

### Done
- feat: Truth Checker 서비스 아이디어 도출
  - 구름 DeepDive 참고 분석
  - AI Hub 낚시성 기사 탐지 데이터셋 (71,338건) 확인
- feat: 실행 가능성 분석
  - 사용자 기술 스택 매칭 (React, Claude API, Recharts, Supabase)
  - 카탈로그 #22 "가짜 뉴스 탐지" 확장 버전으로 접근
- docs: 종합 아이디어 문서 작성 (`truth-checker-service-idea.md`, 30+ 섹션)
  - Executive Summary (한 줄 요약, 핵심 가치, 타겟 사용자)
  - Problem (허위정보 범람, 팩트체크 도구 부족, 시장 규모)
  - Solution (5단계 검증 파이프라인)
  - Core Features (7가지 핵심 기능)
    1. 다양한 입력 형식 (URL, 텍스트, 이미지)
    2. 클레임 추출 및 검증 (Claude API)
    3. 출처 신뢰도 분석 (언론사 등급 A-D)
    4. 낚시성 패턴 탐지 (AI Hub 데이터 기반)
    5. 유사 오보 검색 (Sentence Transformers)
    6. 신뢰도 점수 알고리즘 (0-100점)
    7. 시각화 대시보드 (Recharts 게이지, React Flow 네트워크)
  - Tech Stack (Frontend: React+TS+Recharts, Backend: Node.js+Supabase, AI: Claude+KoBERT)
  - Market Analysis (글로벌 $15B, 한국 성장 초기)
  - Competition (SNU 팩트체크, 뉴스톱, 구름 DeepDive)
  - Business Model (Freemium $0/$10/$30, B2B $500-2k)
  - Roadmap (Phase 1: 4주 MVP, Phase 2: 2개월 Beta, Phase 3: 3개월 Launch, Phase 4: 6개월 Growth)
  - Success Metrics (MAU 10k, MRR $30k 목표)
  - UX/UI Design (사용자 플로우, 와이어프레임)
  - Technical Challenges (한국어 Fact DB 부족, 검증 속도, 저작권, AI 환각)

### Decisions
- **서비스명**: Truth Checker (거짓 내용 분석 서비스)
- **MVP 기간**: 4주 (Week 1: 클레임 추출 + 출처 검증, Week 2: Fact Checking 엔진, Week 3: 시각화 대시보드, Week 4: AI Hub 데이터 통합)
- **핵심 차별화**:
  1. 한국어 특화 (AI Hub 71,338건 데이터)
  2. 모든 콘텐츠 지원 (URL + 텍스트 + 이미지, 경쟁사는 뉴스만)
  3. 시각화 대시보드 (Recharts + React Flow)
  4. 빠른 검증 (10-30초 vs SNU 팩트체크 수일)
- **기술 스택 최종 확정**:
  - Frontend: React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui
  - Data Viz: Recharts (게이지, 차트), React Flow (네트워크 그래프)
  - Backend: Node.js 20 + Express + TypeScript + Supabase (PostgreSQL)
  - AI: Claude API (클레임 추출, 논리 분석), Sentence Transformers (유사 오보), KoBERT fine-tuned (낚시성 분류)
  - External API: 네이버 뉴스, Google Fact Check, 한국언론진흥재단
  - Infra: Vercel (프론트), Railway/Render (백엔드)
- **신뢰도 점수 공식**: 출처(30%) + 교차검증(40%) + 논리(30%) = 100점
- **타겟 MAU**: Phase 3 (1,000), Phase 4 (10,000)
- **예상 MRR**: Phase 3 ($1,000), Phase 4 ($30,000)

### Next
- [ ] Claude API 키 발급 (https://console.anthropic.com/)
- [ ] AI Hub 낚시성 기사 데이터셋 다운로드 신청 (회원가입 → 승인 1-2일 소요)
- [ ] React 프로젝트 초기화
  ```bash
  npm create vite@latest truth-checker -- --template react-ts
  cd truth-checker
  npm install recharts react-flow zustand react-query
  ```
- [ ] MVP Week 1 개발 시작
  - URL 입력폼 UI
  - Cheerio 웹 크롤링
  - Claude API 클레임 추출
  - 출처 메타데이터 분석
- [ ] 베타 테스터 모집 전략 수립
  - 타겟: 기자(20), 팩트체커(10), 연구자(10), 일반(10) = 총 50명
  - 채널: SNU 팩트체크 커뮤니티, 기자협회, 언론학과
- [ ] 경쟁사 심층 분석
  - 구름 DeepDive 기능 테스트
  - SNU 팩트체크 검증 프로세스 분석
- [ ] MVP 스펙 상세화 (planning-interview 스킬 활용 고려)

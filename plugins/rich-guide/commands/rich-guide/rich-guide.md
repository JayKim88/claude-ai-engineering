---
description: 개인화된 부자 전략 시스템. 재무 인터뷰 후 6개 AI 에이전트가 협력하여 맞춤형 부자 전략과 12주 실행 로드맵을 생성합니다. Personalized Korean wealth strategy system with 6-agent pipeline.
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# /rich-guide Command

한국 재테크 초보자를 위한 개인화 부자 전략 시스템입니다.

## 사용법

```bash
# 기본 실행 (재무 인터뷰 후 전략 생성)
/rich-guide

# 한국어 트리거
부자 되는 법
재테크 가이드
재무 분석
투자 전략

# 영문 트리거
rich guide
wealth strategy
financial planning
```

## 실행 내용

이 명령어가 실행되면 `skills/rich-guide/SKILL.md` 스킬이 자동으로 호출됩니다.

1. **환경 설정**: SQLite DB(`~/.claude/skills/rich-guide/data/profiles.db`) 초기화 및 기존 프로필 확인
2. **재무 인터뷰**: 7개 필드 (월수입 / 월지출 / 예금 / 투자자산 / 부채 / 리스크성향 / 목표)
3. **Phase 1 병렬 분석**: 재무진단 + 정보수집 + 시장분석 (3개 에이전트 동시 실행)
4. **Phase 2 순차 생성**: 전략생성 → 리스크평가 (실제 생성된 전략 ID 기반 평가)
5. **전략 선택**: 3-5개 전략 중 선택 (리스크/시간/분야 다양)
6. **Phase 3 실행 계획**: 월별 주간 체크리스트 생성 (템플릿 기반, 순차)
7. **로드맵 파일 저장**: `~/.claude/skills/rich-guide/roadmaps/roadmap-{timestamp}.md`

## 출력 결과

- 재무 건강도 점수 및 진단 요약
- 개인화된 부자 전략 3-5개 (리스크/시간/분야 다양화)
- 주간 실행 체크리스트 (예상 소요 시간 포함)
- 마크다운 로드맵 파일 (면책 조항 + 출처 + 전문가 상담 링크 포함)

## 소요 시간

- 첫 실행: 약 3-5분 (병렬 에이전트 최적화)
- 캐시 재실행 (24h 이내): 약 90-120초
- 갱신 재실행 (1-30일): 부분 업데이트 후 약 2-3분

## 주의사항

- 모든 재무 데이터는 로컬 DB에만 저장됩니다 (외부 전송 없음)
- AI 생성 참고용 정보이므로 투자 결정 전 전문가 상담을 권장합니다
- 인터넷 연결이 필요합니다 (시장 데이터 조회 및 정보 수집)
- Python 3가 필요합니다 (SQLite 초기화)

## 관련 플러그인

더 정확한 분석을 위해 먼저 실행하면 좋습니다:
- `/market-pulse`: 시장 데이터 사전 수집
- `/portfolio-copilot`: 기존 포트폴리오 등록

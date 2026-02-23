# Save Improve Points - Wrap Up

> **Project**: `/Users/jaykim/Documents/Projects/claude-ai-engineering`
> **Scope**: `plugins/save-improve-points/` (planned)

## Session: 2026-02-23

### Done
- feat: initial concept design for save-improve-points plugin
  - 세션 중 발생한 에러/수정사항/교훈을 축적하여 Claude 성능 향상에 활용하는 플러그인 구상
  - 저장 구조 설계 방향 논의: 프로젝트별 `.claude/lessons-learned.md` + 글로벌 `~/.claude/lessons-learned.md`
  - 각 항목 포맷 제안: Category / Rule (행동 지침) / Context (배경)
- docs: 핵심 우려사항 및 설계 방향 정리
  - 노이즈 축적, 일반화 품질, 저장 위치, 중복 관리 이슈 식별

### Decisions
- 플러그인 이름: `save-improve-points` (기존 `improve-wrap-up`에서 변경)
- `/improve-wrap-up` 커맨드로 세션 종료 시 트리거하는 방식

### Next
- [ ] 미결정 사항 확정: 저장 대상 (CLAUDE.md append vs 별도 파일), 추출 방식 (자동 vs 수동 지목), scope (프로젝트 전용 vs 범용)
- [ ] 플러그인 디렉토리 구조 및 SKILL.md 작성
- [ ] 교훈 추출 프롬프트 설계 (세션 분석 → 일반화된 규칙 생성)
- [ ] 중복 감지 및 병합 로직 설계
- [ ] 카테고리별 상한선 및 정리 메커니즘 설계

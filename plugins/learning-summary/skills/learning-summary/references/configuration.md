# Learning Summary Configuration Guide

`config.yaml` 상세 설정 가이드

---

## 기본 설정

```yaml
# Learning Summary Configuration

# AI Learning Repository (absolute path to your dedicated learning repo)
learning_repo: "/Users/jaykim/Documents/Projects/ai-learning"

# Output directory for generated documents (relative to learning_repo)
output_dir: "learnings"

# Filename pattern (will be auto-generated based on date and topic)
filename_pattern: "YYYY-MM-DD-topic.md"

# Auto-commit generated documents to git (if in a git repo)
auto_commit: false

# Auto-push to remote after commit (requires auto_commit: true)
auto_push: false

# Default sections to include
sections:
  - key_concepts
  - new_learnings
  - practical_examples
  - misconceptions
  - references
  - next_steps

# Language preference (auto-detect based on conversation, or set to 'ko' or 'en')
language: auto
```

---

## 옵션 상세 설명

### learning_repo

**타입**: `string` (절대 경로)
**필수**: No (기본값: 현재 디렉토리)
**설명**: 학습 노트를 저장할 전용 레포지토리 경로

**예시**:
```yaml
# macOS/Linux
learning_repo: "/Users/jaykim/Documents/Projects/ai-learning"

# Windows
learning_repo: "C:/Users/jaykim/Documents/Projects/ai-learning"

# 상대 경로는 지원하지 않음 ❌
learning_repo: "../ai-learning"  # 작동하지 않음
```

**트러블슈팅**:
- 디렉토리가 존재하지 않으면 에러
- 해결: `mkdir -p /path/to/learning_repo`
- 권한 문제: `chmod 755 /path/to/learning_repo`

---

### output_dir

**타입**: `string` (상대 경로)
**필수**: No (기본값: `"learnings"`)
**설명**: learning_repo 내부의 출력 디렉토리

**예시**:
```yaml
# 기본값
output_dir: "learnings"
# → /Users/jaykim/Documents/Projects/ai-learning/learnings/

# 서브디렉토리
output_dir: "notes/daily"
# → /Users/jaykim/Documents/Projects/ai-learning/notes/daily/

# 루트에 직접 저장
output_dir: "."
# → /Users/jaykim/Documents/Projects/ai-learning/
```

**주의**:
- 절대 경로는 지원하지 않음
- 자동으로 디렉토리 생성되지 않음 (수동 생성 필요)

---

### filename_pattern

**타입**: `string`
**필수**: No (기본값: `"YYYY-MM-DD-topic.md"`)
**설명**: 파일명 형식 (현재는 자동 생성, 패턴은 참고용)

**지원 예정 패턴**:
```yaml
# 날짜-주제 (기본)
filename_pattern: "YYYY-MM-DD-topic.md"
# → 2026-01-17-claude-code-marketplace.md

# 주제-날짜
filename_pattern: "topic-YYYY-MM-DD.md"
# → claude-code-marketplace-2026-01-17.md

# 카테고리/날짜-주제
filename_pattern: "category/YYYY-MM-DD-topic.md"
# → claude-code/2026-01-17-marketplace.md
```

**Current version**: Auto-generated, this option is for documentation purposes

---

### auto_commit

**타입**: `boolean`
**필수**: No (기본값: `false`)
**설명**: 문서 생성 후 자동으로 git commit 실행

**사용 예**:
```yaml
# 수동 커밋 (기본)
auto_commit: false

# 자동 커밋
auto_commit: true
```

**작동 방식**:
```bash
# auto_commit: true일 때 실행되는 명령어
cd "$learning_repo"
git add "learnings/2026-01-17-topic.md"
git commit -m "Add learning: topic

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

**전제 조건**:
- learning_repo가 git 레포지토리여야 함
- git이 설치되어 있어야 함
- 커밋할 변경사항이 있어야 함

**에러 처리**:
- git이 없으면: 경고 출력, 문서는 저장됨
- git repo가 아니면: 경고 출력, 문서는 저장됨
- 커밋 실패: 경고 출력, 문서는 저장됨

---

### auto_push

**타입**: `boolean`
**필수**: No (기본값: `false`)
**설명**: 커밋 후 자동으로 git push 실행

**사용 예**:
```yaml
# 커밋만 (기본)
auto_commit: true
auto_push: false

# 커밋 + 푸시
auto_commit: true
auto_push: true
```

**주의**:
- `auto_commit: false`이면 `auto_push`는 무시됨
- remote가 설정되어 있어야 함
- 인증 정보가 캐시되어 있어야 함 (패스워드 프롬프트 불가)

**작동 방식**:
```bash
# auto_push: true일 때 추가로 실행
git push
```

**권장 설정**:
```yaml
# 로컬 백업용 (추천)
auto_commit: true
auto_push: false

# GitHub 자동 백업용
auto_commit: true
auto_push: true

# 완전 수동
auto_commit: false
auto_push: false
```

---

### sections

**타입**: `list of strings`
**필수**: No (기본값: 모든 섹션 포함)
**설명**: 문서에 포함할 섹션 목록

**사용 가능한 섹션**:
```yaml
sections:
  - key_concepts        # Main topics and definitions
  - new_learnings       # Before/after understanding
  - practical_examples  # Code, commands, real examples
  - misconceptions      # Clarified misunderstandings
  - references          # Files, URLs, documentation
  - next_steps          # Follow-up actions
```

**커스터마이징 예시**:
```yaml
# 최소 구성
sections:
  - key_concepts
  - practical_examples

# 학습 중심
sections:
  - key_concepts
  - new_learnings
  - misconceptions
  - next_steps

# 참고 자료 중심
sections:
  - practical_examples
  - references
```

**현재 버전**: 이 설정은 미래를 위한 것, 현재는 모든 섹션 포함

---

### language

**타입**: `string`
**필수**: No (기본값: `"auto"`)
**설명**: 문서 언어 설정

**옵션**:
```yaml
# 자동 감지 (기본, 추천)
language: auto

# 한국어 강제
language: ko

# 영어 강제
language: en
```

**작동 방식**:
- `auto`: 대화 언어를 분석하여 자동 결정
- `ko`: 섹션 제목과 설명을 한국어로
- `en`: 섹션 제목과 설명을 영어로

**예시**:
```yaml
language: ko
```
→ 문서 출력:
```markdown
## 핵심 개념
## 새로 알게된 것
```

```yaml
language: en
```
→ 문서 출력:
```markdown
## Key Concepts
## New Learnings
```

---

## 시나리오별 권장 설정

### 시나리오 1: 개인 학습 노트 (로컬만)

```yaml
learning_repo: "/Users/jaykim/Documents/Projects/ai-learning"
output_dir: "learnings"
auto_commit: true
auto_push: false
language: auto
```

**장점**: 로컬 git 히스토리 유지, 푸시는 수동

---

### 시나리오 2: 팀 공유 학습 노트

```yaml
learning_repo: "/Users/jaykim/work/team-learnings"
output_dir: "notes"
auto_commit: true
auto_push: true
language: en
```

**장점**: 자동으로 팀과 공유, 영어로 통일

---

### 시나리오 3: 블로그 초안 생성

```yaml
learning_repo: "/Users/jaykim/blog/drafts"
output_dir: "posts"
auto_commit: false
auto_push: false
language: ko
```

**장점**: 수동 리뷰 후 커밋, 한국어 블로그용

---

### 시나리오 4: 빠른 메모 (최소 설정)

```yaml
learning_repo: "/Users/jaykim/quick-notes"
output_dir: "."
auto_commit: false
language: auto
```

**장점**: 최소 설정, 빠른 저장

---

## 설정 파일 위치

### 전역 설정

```
~/.claude/skills/learning-summary/config.yaml
```

모든 프로젝트에서 사용

### 프로젝트별 설정 (미지원, 계획 중)

```
.claude/skills/learning-summary/config.yaml
```

현재 프로젝트만 적용 (전역 설정 오버라이드)

---

## 트러블슈팅

### 문제 1: "Config file not found"

**원인**: config.yaml이 없음

**해결**:
```bash
# 템플릿 복사
cp ~/.claude/skills/learning-summary/config.yaml.example \
   ~/.claude/skills/learning-summary/config.yaml

# 또는 수동 생성
nano ~/.claude/skills/learning-summary/config.yaml
```

---

### 문제 2: "Directory not found"

**원인**: learning_repo 경로가 존재하지 않음

**해결**:
```bash
mkdir -p /Users/jaykim/Documents/Projects/ai-learning/learnings
```

---

### 문제 3: "Git commit failed"

**원인**: git repo가 아니거나 변경사항 없음

**해결**:
```bash
cd /path/to/learning_repo
git init
git add .
git commit -m "Initial commit"
```

---

### 문제 4: "Permission denied"

**원인**: 쓰기 권한 없음

**해결**:
```bash
chmod 755 /path/to/learning_repo
```

---

## YAML 문법 주의사항

### 올바른 형식

```yaml
✅ 올바름:
learning_repo: "/Users/jaykim/path"
auto_commit: true
sections:
  - key_concepts
  - new_learnings

❌ 틀림:
learning_repo: /Users/jaykim/path  # 따옴표 없음 (공백 있으면 필수)
auto_commit: yes  # true 사용 권장
sections: [key_concepts, new_learnings]  # 리스트 형식 일관성
```

### 주석

```yaml
# 이것은 주석입니다
learning_repo: "/path"  # 줄 끝 주석도 가능
```

---

## 설정 검증

### 수동 검증

```bash
# YAML 문법 체크
python3 -c "import yaml; yaml.safe_load(open('~/.claude/skills/learning-summary/config.yaml'))"

# 경로 존재 확인
ls -la /Users/jaykim/Documents/Projects/ai-learning/learnings/
```

### Claude Code에서 확인

```
"learning-summary 설정 확인해줘"
```

Claude가 config.yaml을 읽고 현재 설정 표시

---

## 버전 히스토리

### v1.0.0 (현재)

- 기본 설정 옵션
- auto_commit, auto_push 지원
- language: auto 지원

### 계획 중 (v1.1.0)

- 프로젝트별 설정 오버라이드
- sections 동적 선택
- 커스텀 템플릿 지원
- category/tags 지원

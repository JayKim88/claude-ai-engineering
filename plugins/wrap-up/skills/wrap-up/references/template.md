# Wrap Up Document Template

## New File Structure

When creating a wrap-up file for the first time:

```markdown
# {Project Name} - Wrap Up

## Session: 2026-02-23

### Done
- feat: 사용자 인증 모듈 구현
- fix: 로그인 실패 시 에러 메시지 수정
- refactor: API 라우터 구조 개선

### Decisions
- JWT 대신 세션 기반 인증 채택 (서버사이드 렌더링 환경)

### Issues
- OAuth 연동 시 CORS 문제 발생 → 추후 해결 필요

### Next
- [ ] OAuth 2.0 소셜 로그인 연동
- [ ] 비밀번호 재설정 기능
- [ ] 세션 만료 처리 로직
```

---

## Appended Session Structure

When adding to an existing file, append after a `---` separator:

```markdown
---

## Session: 2026-02-24

### Done
- feat: OAuth 2.0 소셜 로그인 연동 (completed from previous Next)
- feat: Google, GitHub 프로바이더 지원
- fix: 세션 만료 후 리다이렉트 버그 수정

### Next
- [ ] 비밀번호 재설정 기능
- [ ] Apple 로그인 프로바이더 추가
- [ ] 로그인 실패 횟수 제한 구현
```

Note: **Decisions** and **Issues** are omitted when there are none for the session.

---

## Done Item Prefixes

Use conventional commit prefixes for categorization:

| Prefix | Usage |
|--------|-------|
| `feat:` | New feature or functionality |
| `fix:` | Bug fix |
| `refactor:` | Code restructuring without behavior change |
| `docs:` | Documentation changes |
| `chore:` | Build, config, dependency updates |
| `test:` | Test additions or fixes |
| `style:` | Formatting, naming changes |

---

## Next Item Format

Always use checkbox format for tracking:

```markdown
### Next
- [ ] Uncompleted task
- [x] Completed in this session (when referencing previous Next items in Done)
```

---

## Continuity Between Sessions

When appending, check previous session's Next items:

**Previous session:**
```markdown
### Next
- [ ] OAuth 2.0 소셜 로그인 연동
- [ ] 비밀번호 재설정 기능
```

**Current session (if OAuth was completed):**
```markdown
### Done
- feat: OAuth 2.0 소셜 로그인 연동 (from previous Next)
```

This linkage provides clear continuity across sessions.

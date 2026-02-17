# Career Compass - Developer Guide

Comprehensive developer documentation.

## Architecture

8-agent pipeline:
- Phase 1: resume-analyzer + jd-market-analyzer + career-trend-researcher
- Phase 2: skill-gap-analyzer + career-path-generator + salary-projector
- Phase 3: roadmap-generator → strategy-advisor

## Implementation

- SKILL.md: 10-step orchestration
- Agents: 8 specialized analyzers and generators
- Templates: Output format standardization
- Config: Tunable parameters

## Testing

```bash
/career-compass
```

Follow prompts and verify outputs.

## Model Selection

- 5 × Sonnet (analytical work)
- 3 × Opus (creative/strategic work)

Total cost: ~$1.50 per run
Total time: 5-7 minutes

## Troubleshooting

- Check `~/.jd-analyzer/profile.yaml` exists
- Verify internet connection for web research
- Adjust timeouts in config if needed

## Contributing

- Add new agents in `agents/`
- Update SKILL.md orchestration
- Test end-to-end workflow
- Document changes

## License

MIT

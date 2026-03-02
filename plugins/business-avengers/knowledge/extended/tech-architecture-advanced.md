# Tech Architecture Advanced Knowledge Base

Expert technical architecture frameworks for Phase 4 (Tech Planning).
Source: AWS Well-Architected Framework, Kelsey Hightower, Martin Fowler,
Dan McKinley (Choose Boring Technology), Pieter Levels (MAKE stack principles).

---

## 1. Indie Maker / Early-Stage Stack Principles

### Choose Boring Technology (Dan McKinley)
**Rule:** Use the technology you already know unless the new tech saves >40 hours over the project lifetime.

Boring technology has solved its problems. New technology creates new problems.

**Stack selection decision tree:**
```
Does the team know this technology?
  YES → Use it (unless better alternative saves >40h)
  NO  → Does learning it provide enough value?
         YES → Only if the team has runway to learn it
         NO  → Use what you know
```

**Recommended "boring" defaults (2025):**
| Layer | Default | When to deviate |
|-------|---------|----------------|
| Frontend | Next.js (React) | Mobile-only app → React Native |
| Backend | Node.js/TypeScript or Python (FastAPI) | High compute → Go |
| Database | PostgreSQL | Document-heavy → MongoDB; cache layer → Redis |
| Auth | Clerk or Auth0 | Simple JWT → roll your own |
| Payments | Stripe | Enterprise billing → Chargebee |
| Email | Resend or SendGrid | - |
| Hosting | Vercel (FE) + Railway/Render (BE) | Heavy compute → AWS |
| Storage | Cloudflare R2 or AWS S3 | - |

### Minimal Viable Architecture (MAKE Principle)
Start with a monolith. Split only when there's evidence you need to.

**Architecture evolution path:**
```
Stage 1 (0–$10K MRR): Monolith
  Single codebase, one deployment, one database
  Optimize for: speed to ship, simplicity, team comprehension

Stage 2 ($10K–$100K MRR): Modular Monolith
  Separate modules by domain, shared DB
  Optimize for: maintainability, feature isolation

Stage 3 ($100K+ MRR): Selective Microservices
  Split only high-traffic or independent services (e.g., notifications, billing)
  Optimize for: scalability of specific bottlenecks

Anti-pattern: Microservices on day 1 → infrastructure complexity kills velocity
```

---

## 2. AWS Well-Architected Framework (5 Pillars)

Even for non-AWS stacks, these 5 pillars define a good architecture.

### Pillar 1: Operational Excellence
- Can you deploy changes without downtime? (Blue/green or rolling deploys)
- Do you have runbooks for common failure scenarios?
- Are you monitoring the right things (not just uptime — also key user flows)?

### Pillar 2: Security
**OWASP Top 10 Checklist (mandatory for any web product):**

| # | Risk | Fix |
|---|------|-----|
| A01 | Broken Access Control | Verify permissions server-side; never trust client |
| A02 | Cryptographic Failures | TLS everywhere; bcrypt passwords; encrypt PII at rest |
| A03 | Injection (SQL, NoSQL, Command) | Parameterized queries; ORMs with sanitization |
| A04 | Insecure Design | Threat model before building; don't store what you don't need |
| A05 | Security Misconfiguration | Default credentials changed; debug off in prod; env vars not exposed |
| A06 | Vulnerable Components | `npm audit`; keep dependencies updated |
| A07 | Auth & Session Management | Short-lived tokens; secure cookie flags; rate-limit auth endpoints |
| A08 | Software & Data Integrity | Signed releases; verified supply chain |
| A09 | Security Logging | Log auth events, access failures; alerting on anomalies |
| A10 | SSRF | Validate and whitelist URLs for server-side requests |

**Auth implementation checklist:**
- [ ] Passwords: bcrypt with cost factor ≥12 (never MD5/SHA1)
- [ ] JWTs: short expiry (15min access token) + refresh token rotation
- [ ] Rate limiting: auth endpoints max 5 attempts / 15 min per IP
- [ ] MFA available (TOTP minimum for B2B products)
- [ ] HTTPS everywhere (HSTS header required)
- [ ] Session invalidation on logout (server-side token blacklist)

### Pillar 3: Reliability
- **Stateless services** → horizontal scaling without sticky sessions
- **Database connections** → connection pooling (PgBouncer for PostgreSQL)
- **Graceful degradation** → if service X fails, core product still works
- **Timeout + retry** → every external API call has timeout + max 3 retries with backoff

**SLA targets for early-stage (pragmatic):**
| Metric | Target | Notes |
|--------|--------|-------|
| Uptime | 99.5% (43h/year downtime ok) | 99.9% requires >3× infrastructure cost |
| API latency (p99) | < 2s | p50 < 500ms |
| Error rate | < 0.1% of requests | Measure 5xx, not 4xx |

### Pillar 4: Performance Efficiency
**When to optimize (premature optimization rule):**
1. First, make it work
2. Then, make it correct
3. Only then, make it fast (and only the parts that are actually slow — use profiler data)

**Caching decision matrix:**
| Data type | Cache? | TTL | Strategy |
|-----------|--------|-----|----------|
| User profile | Yes | 5 min | Invalidate on update |
| Product catalog | Yes | 1 hour | Refresh on change |
| User-specific data | Careful | 1 min | Invalidate on write |
| Real-time data | No | - | Direct DB |
| Static assets | Yes | 1 year | Content-hash filenames |

**Database indexing guide:**
- Index every foreign key
- Index columns used in WHERE, ORDER BY, GROUP BY
- Composite index: most selective column first
- Maximum 5–7 indexes per table (write performance trade-off)
- Use `EXPLAIN ANALYZE` before adding index in production

### Pillar 5: Cost Optimization
**Early-stage cost priorities:**
1. Start on cheapest tier that handles current load
2. Use managed services (RDS, S3) — saves ops time worth more than cost
3. Budget alerts at 80% of expected monthly spend
4. Database is usually the highest cost — optimize queries before scaling vertically

---

## 3. Architecture Decision Records (ADR)

Every significant technical decision gets an ADR. Format:

```markdown
# ADR-[NUMBER]: [Title]

**Status:** Proposed / Accepted / Deprecated / Superseded

**Context:**
[Why was this decision needed? What problem does it solve?]

**Decision:**
[What was decided?]

**Rationale:**
[Why this option over alternatives?]

**Consequences:**
- Positive: [Benefits]
- Negative: [Trade-offs accepted]

**Alternatives Considered:**
- [Option A]: Rejected because [reason]
- [Option B]: Rejected because [reason]
```

**Required ADRs for Phase 4:**
1. ADR-001: Frontend framework choice
2. ADR-002: Backend framework choice
3. ADR-003: Database selection
4. ADR-004: Authentication approach
5. ADR-005: Hosting/deployment strategy
6. ADR-006: Monolith vs. services decision

---

## 4. Scalability Milestone Planning

Design for current scale + 10×. Not 100×. Over-engineering kills startups.

**Scale planning triggers:**
| Trigger | Action |
|---------|--------|
| > 100 concurrent users | Add connection pooling; check indexes |
| > 1,000 req/min | Add Redis caching for hot paths |
| > 10,000 users | Consider read replicas; CDN for assets |
| > $100K MRR | SLA review; dedicated DevOps; disaster recovery plan |

---

## 5. Tech Architecture Quality Standards (Phase 4)

**Architecture Document Completeness Checklist:**
- [ ] Technology stack decisions documented with rationale (ADR format)
- [ ] C4 Context diagram showing user + system + external services
- [ ] C4 Container diagram showing all deployment units
- [ ] Security section: OWASP Top 10 addressed, auth mechanism specified
- [ ] Database schema with indexes and constraint rationale
- [ ] API design: RESTful, versioned, consistent error format
- [ ] Environment strategy: dev / staging / prod separation
- [ ] No-code/low-code assessment: did we check if Supabase/Clerk/Stripe handles it?
- [ ] Scalability: designed for 10× current load, not 100×

**Self-Assessment Block (add at top of tech document before saving):**
```markdown
---
**Tech Architecture Quality Check**
- Depth: [1–3] — [ADRs with rationale vs. just stack listing]
- Evidence: [1–3] — [team skills considered, boring tech principle applied]
- Specificity: [1–3] — [exact technology versions, deployment plan, DB schema]
- Security: [OWASP Top 10 addressed: yes/partial/no]
- Stack appropriateness: [boring tech principle: applied/violated]
- Scalability scope: [10× planning: yes/over-engineered/under-planned]
- Unmet criteria: [list or "none"]
---
```

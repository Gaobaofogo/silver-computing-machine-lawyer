# Stage 9: Implementation Readiness Test (Direct Dispatch)
File: judis-advocacia/GLOSSARY.md (FeatureRange = full; DetailedRange = N/A — no separate implementation plan)
Reviewers: egm-implementation-readiness, egm-codebase-details, egm-style

## Implementation readiness — findings (no Implementation Plan to validate against)

Since there is no `## Detailed Implementation Plan` / `## Work Breakdown` section, Stage 9 evaluates whether the feature specification (GLOSSARY.md) is precise enough to begin implementation.

1. Table-to-code traceability: The 4.1.2 attribute table (`| Atributo | Tipo | Mult. | Range | Descrição |`) provides sufficient data to create SQLModel/SQLAlchemy columns (`clienteId: UUID`, `cpf: String` or embedded, `nomeCompleto: String`, `endereco: Endereco` embedded, etc.). However, `Endereco` and `Cpf` are Value Objects embedded in `CadastroCliente`; the database schema is not explicitly defined (no `structure-pastas.md` linked for DB schema). Implementation will need a design decision: embedded JSON/JSONB vs normalized tables for VO.

2. `money` implementation: PostgreSQL `money` requires SQLAlchemy `Numeric(precision=...)` or `Numeric(scale=2)` with `DECIMAL` mapping, not native `money`. The UML says `money` but the DB layer will translate to `NUMERIC(10,2)` or equivalent. This gap is acceptable for a spec document but must be noted in implementation notes.
3. `StatusProcesso` state machine (section 4.1.3): The Mermaid diagram defines states (`CADASTRADO`, `EM_ANDAMENTO`, `SUSPENSO`, `CONCLUIDO`) but no transition rules (e.g., which roles can transition `CADASTRADO` → `EM_ANDAMENTO`?). Implementation needs transition guard rules not present in spec.
4. LGPD / security: The document states `Cpf` is encrypted with AES-256 via pgcrypto, but no key management or rotation policy is specified in spec. Implementation will need a separate security design.
5. Persona rules (`Assistente` cannot alter `valorCausa`): This is an access-control rule that belongs in middleware (FastAPI dependency or row-level security), not in the domain model. The spec documents it correctly, but implementation needs middleware specs (not present here).

## Verdict — Implementation Readiness

Not fully ready. The feature spec is clear on vocabulary, associations, and basic rules, but lacks:
- DB schema mapping (embedded vs normalized for VOs)
- State-transition guard rules
- Security / key-management design
- Middleware / access-control design for persona rules
- ADR file for domain changes made in-session

Recommendation: Before `implement` or `to-tickets`, complete the ADR and produce a minimal `spec.md` or `implementation-readiness.md` that maps UML attributes to SQLModel fields.

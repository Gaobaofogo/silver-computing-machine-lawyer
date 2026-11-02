# Stage 7: Critic Review (Direct Dispatch — synthesized from design, structural, style reviewers)
File: judis-advocacia/GLOSSARY.md (FeatureRange 1..528)
Standard: feature-spec-standard

## egm-design — Domain / Conceptual Critique

- The `UF` enum (27 states + DF) excludes `DT` (Distrito Federal is included as `DF` — correct), but the range `<2>` for the old `String` had no validation mechanism; the enum fixes that. Positive.
- The `money` type (PostgreSQL `money`) is correctly used for monetary values to avoid floating-point error; however, `money` has a fixed scale of 2 decimal places and a fixed range; if a high-value cause exceeds ~79 trillion, PostgreSQL `money` overflows (maximum ~79,228,162,514,264.07). If this office handles very large commercial disputes, this is a hidden ceiling. The document notes `<0..99999999.99>` (line 187) — that range is well below the PostgreSQL `money` max, so safe for current scope, but the range should be documented as business constraint, not DB constraint.
- The `ValorCausa` association (`Processo --> ValorCausa`) is `1` in diagram 4.1.1; the `4.2.2` table (line 269) says `Mult. = 1`. This is consistent. No issue.
- `StatusProcesso` state machine (Section 4.1.3) uses `stateDiagram-v2`. The note annotations (`note right of ...`) are valid Mermaid, but if rendered in GitHub/GitLab markdown viewers, `note right of` sometimes causes rendering artifacts depending on renderer version. Should be tested after deployment.

## egm-structural — Architecture / Organization Critique

- The file mixes 5 sections (1-11 per template) with session-specific edits scattered (lines edited during this session without version markers). There is no `# Edited: YYYY-MM-DD` or `# Session changes` block at the top. This makes it impossible for a future agent to distinguish "template content" from "session corrections" from "original domain definition".
- Section numbering references (2.3, 4.1.1, 4.1.2, 4.2.1, 4.2.2, 9) are correct relative to document, but some references point to sub-blocks inside sections (e.g., "4.1.3 Estado do processo" is actually inside section 4, not 4.1.3 specifically — the numbering is slightly loose). Fine for human reading, but automated parsing may break.
- The duplicate sections 5/6/7 that existed (per checkpoint) were removed correctly; no duplicate headers remain (verified: only one `## 4.` block, one `## 7.` block).
- The `GLOSSARY.md` is 528 lines long; for a single-context domain model this is reasonable, but approaching the point where splitting into sub-documents (`modelo/`, `docs/adr/`) is advisable per `AGENTS.md`.

## egm-style — Clarity / Language / Formatting Critique

- The note about `Assistente` (line 24: "não pode alterar nem cadastrar `valorCausa`") is clear, but uses backticks inside a table cell which can render poorly in some Markdown parsers depending on padding. Not critical.
- The `6. Condições de uso` (line 104) references `AGENTS.md`; the link is implicit (no URL), which is fine given local repo.
- `## 11. Questões em aberto` is well-structured with `11.1`, `11.2`; the responses include `RESOLVIDO` in the header — this is a good convention that should be preserved.
- Several paragraphs contain Portuguese and English mixed (e.g., line 27: "restrição de aplicação, mas está registrada no domínio como uma limitação funcional da persona"). This is correct given the project language, but new agents should know to read both.

## Consolidated findings (priority)

🔴 Blocker-level: No ADR file exists for session-level hard-to-reverse domain changes (CNPJ removed from CadastroCliente, UF enum, EstadoCivil mandatory, MovimentoProcessual subordinate). Must create `judis-advocacia/docs/adr/0001-cliente-cpf-uf-estado-civil.md` before this is finalized.

🟡 Major-level: Internal contradiction between `AGENTS.md` definition of `Cliente` (pessoa física ou jurídica) and the resolved document rule (sempre pessoa física). Must either update `AGENTS.md` or document the deviation explicitly.

🟢 Nit-level: `money` range `<0..99999999.99>` is safe but should mention PostgreSQL overflow ceiling. `Timestamp` fields (`createdAt`, `updatedAt`) reference `DateTime` but no timezone specification is given (UTC assumed — acceptable but should be explicit).

## Counter-argument for agreement

The document works for its purpose. It is not broken. However, `egm-review` requires finding mistakes before affirming. The missing ADR is a real failure of process, not of content. I do not agree that this is "complete" until the ADR is present.

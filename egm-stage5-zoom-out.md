# Stage 5: Initial Zoom Out Review
File: judis-advocacia/GLOSSARY.md
Mode: Direct dispatch (no Goldfish subagent available)
Reviewer: egm-zoom-out simulated
Standard: feature-spec-standard

## Critical finding (lead first)

1. The document title was changed from "Modelo UML" to "Modelo geral do domínio" per user request, but `AGENTS.md` still defines it as a UML template-based artifact (`templates/uml-template.md`). There is a tension: is this a UML spec or a domain glossary? The content mixes UML diagrams (Mermaid), DDD aggregates, LGPD rules, scenario descriptions, and open questions. A single document serving all these roles is risky: it lacks a clear separation between "design spec" (what the system is) and "domain glossary" (vocabulary). A future reader will not know whether Section 9 (Diagrama) overrides Section 3 (Conceitos) or vice versa.

2. The `Reclamado` definition changed in-session from "mantenho como referência" to "pode ser pessoa física ou jurídica" (per 11.3 response), but `CadastroCliente` (author) is strictly pessoa física (`Cpf` obrigatório, sem `CNPJ`). This is a significant domain simplification (only single-party author) that deviates from `AGENTS.md` which states "Cliente: parte autora (pessoa física ou jurídica)". The document's note (line 11) tries to document this, but it creates an internal contradiction with `AGENTS.md`. This is hard to reverse and should have been an ADR.

3. `EstadoCivil` was changed from `[0..1]` to `1` (obrigatório) per user confirmation (11.3), but `CadastroCliente` is a `AggregateRoot` with `estadoCivilId` mapped. The diagram reflection was applied (`+estadoCivilId: UUID` without optional). This is correct in the diagram but the attribute table description (`4.2.2`) says "Referência à `EstadoCivil`; obrigatório só para PF" (line 412 after edit) — the phrase "só para PF" is now redundant since the aggregate itself is always PF. This is minor but shows language drift.

## Positive observation

- The model captures LGPD requirements clearly (`Cpf` criptografado AES-256, pseudonimização para assistente via middleware, `Observacao` logada, `ValorCausa` como `money` para precisão decimal). These constraints are explicit, which prevents future implementation from ignoring security.
- The namespace division (`SistemaCore`, `Processos`, `Clientes`, `ValueObjects`, `Enumerações`) is consistent and aligns with the `templates/uml-template.md` sections. The Mermaid diagrams render syntactically (after fixes applied in-session).

## Risk / missing

- No `docs/adr/` file was created for the three hard-to-reverse decisions made in-session: (a) removal of `CNPJ` from `CadastroCliente`, (b) change from `String` to enum `UF`, (c) `EstadoCivil` from optional to mandatory, (d) `MovimentoProcessual` subordinated (11.2). Without ADRs, future agents will not understand why these deviations from the base template (`spec.md` / `AGENTS.md`) exist.
- The open questions (11.1, 11.2) are marked RESOLVIDO but there is no `ADRs` reference linking them to the document changes. This breaks the `domain-modeling` skill invariant (update GLOSSARY.md inline + offer ADR when hard-to-reverse).
- `AGENTS.md` references `GLOSSARY.md` as both "vocabulário do domínio" and "template de modelagem UML". The document blends both roles without clear markers.

## Counter-argument

The user explicitly asked for speed ("transferir parte de negócios", "rebuild as complete UML domain model") and resisted formal ADR creation. However, `egm-review` requires stress-testing regardless of speed. The risk is that in 4 weeks, when `spec.md` is updated or a new agent joins, the rationale for "Cliente = sempre pessoa física" will be lost, and someone will re-add `CNPJ` assuming it was an accident.

## Conclusion

Survives basic structure check, but fails the hard-to-reverse decision tracking requirement. Must add at least a minimal ADR or inline reference before this model can be considered production-ready.

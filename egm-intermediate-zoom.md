# Stage 8: Intermediate Zoom Out
File: judis-advocacia/GLOSSARY.md (post-stage 5 + 7 edits referenced)
Review focus: additions/mitigations since Stage 5 (ADR requirements, contradictions documented)
Result: none applied yet (reports point out required fixes; user has not edited file since stage outputs)

## What changed since Stage 5

Nothing in the file itself. The session produced:
- `egm-stage5-zoom-out.md`
- `egm-comprehension.md`
- `egm-critic.md`
No edits to `GLOSSARY.md` have occurred since the user's last edit (UF enum, EstadoCivil mandatory, CNPJ removal, title change, 11.1/11.2 resolution). The intermediate review confirms that the gaps identified in Stage 5 and 7 remain unaddressed in the file.

## Architecture verification after stage inputs

- No structural split (Feature vs Implementation) was added. The document remains pure feature spec.
- No ADR directory created (`judis-advocacia/docs/adr/` does not exist — confirmed by absence of directory list).
- The `GLOSSARY.md` title remains correct (`Modelo geral do domínio`).
- All 5 mermaid diagrams still present (verified by grep count = 5 block starts ` ```mermaid` in file).

## What should be applied before finalizing

Per Stage 7 findings:
1. Create `judis-advocacia/docs/adr/0001-cliente-cpf-uf-estado-civil.md`
2. Add inline note or link in GLOSSARY.md section 11 pointing to ADR
3. Optionally update `AGENTS.md` line 7 (Cliente definition) to clarify "pessoa física" only, or document exception
4. Add `money` overflow note in 4.1.2 / 4.2.2

This stage confirms the review loop is working (find → document → propose fix → verify not applied). The document is stable but not finalized.

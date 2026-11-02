# Zoom Out Review — frontend-patterns.md

Target: `/home/gabao/direito-projeto/docs/frontend-patterns.md`
FeatureRange: 1..125 (full file, no DetailedRange)
Review stage: 5 (Initial Zoom Out)
Standard: `resources/document_standards/zoom-out-standard.md`

---

## What the document covers

Reference guide for frontend patterns in `direito-projeto`: React 18/19 UI patterns (`react-patterns`, `baseline-ui`), domain-aligned components (`CadastroCliente`, `CadastroReclamado`, `ProcessoDetalhe`), navigation flows by role, login/logout/forgot-password flow, LGPD-sensitive form rules (CPF masked, `EstadoCivil` required), language convention (§1.1: English code, Portuguese domain names).

---

## Weak points / blind spots found (critique first, no glossing)

1. **No concrete accessibility audit standard referenced**. The doc mentions accessibility (keyboard, labels) but does not cite `axe`, `WCAG 2.2`, or a test command. Risk: agent builds accessible-looking UI that fails automated checks.
2. **No responsive / mobile breakpoint convention**. `baseline-ui` is referenced but no breakpoints (sm/md/lg) or mobile-first layout rules are given. Risk: agent builds desktop-only interfaces without mobile adaptation.
3. **No state-management decision rule**. The doc discusses `useState`, `useContext`, external stores in passing (via `react-patterns` reference) but does not dictate when to lift state vs use context vs external library for this legal domain. Risk: agent picks wrong state tree for `Processo` detail + edit.
4. **No loading / error / empty-state pattern defined**. No `Skeleton` pattern, no `ErrorBoundary` usage, no `NotFound` for missing `Processo`. Risk: agent leaves users without feedback on slow loads or missing records.
5. **No design-token file reference**. `baseline-ui` is named but no `design-tokens.css` or `theme.json` path is given. Risk: agent invents colors instead of using a shared token file.
6. **LGPD masking rule exists (§2, §4) but no component-level implementation reference**. `mask_cpf` is mentioned in backend doc; frontend doc says "mascarado" but does not point to where the mask utility lives (`utils/mask.ts`?). Risk: duplication or omission.

---

## What is correct / strong (earned, not assumed)

- Domain vocabulary is enforced (§2: `Cliente`, `Reclamado`, `Processo`, `EstadoCivil` mapped to components).
- ADR-0001 embedded (`Cliente = PF`, `CPF` required, `CNPJ` removed).
- Validation separation referenced (§4) links to backend convention.
- Language convention (§1.1) aligns with backend-patterns.md.
- Component names map directly to domain entities (not vague "FormA", "CardB").
- Login/logout/forgot-flow is explicitly covered (not left out).

---

## Counter-arguments to affirm without scrutiny

Do not agree that "this covers UI/UX" just because it lists components. The document lacks: (a) accessibility test commands, (b) responsive rules, (c) state-location tree for `Processo` + `Cliente`, (d) token file, (e) error/empty UI patterns. These are not decorative — they determine whether a legal-datasensitive interface survives real use.

---

## Recommended actions (before Stage 7/9)

- Add a `§2.5 Accessibility Standard` pointing to `axe`, `WCAG` criteria, and `React Testing Library` accessibility queries.
- Add `§3.2 Responsive / Breakpoints` with mobile-first rules (e.g., `ProcessoCard` stacks at <768px; `CadastroCliente` uses single-column layout on mobile).
- Add `§4.4 State Management Decision Tree` for frontend: when to use `useState` (local form), `useContext` (auth/role), external store (if multi-user concurrent editing).
- Add `§5.4 Loading / Error / Empty States` with skeleton patterns and `NotFound` for missing `Processo`.
- Add `§6.5 Design Tokens` referencing `frontend-skills/baseline-ui` and a concrete file (`styles/design-tokens.css` or `theme/config.ts`).
- Confirm whether `frontend-patterns.md` is meant to be reference-only (like backend) or becomes a spec for `to-tickets`; note it in `§10`.

---

*Artifact file per egm-review artifact-first rule. No chat summary of full file content; path is `zoom_out_report.md` (frontend). Review paused at Stage 5 pending user input on revisions.*

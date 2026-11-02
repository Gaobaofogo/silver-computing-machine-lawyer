# Zoom Out Review — backend-patterns.md

Target: `/home/gabao/direito-projeto/docs/backend-patterns.md`
FeatureRange: 1..217 (full file, no implementation plan section)
Review stage: 5 (Initial Zoom Out)
Standard: `resources/document_standards/zoom-out-standard.md`

---

## What the document covers

Reference guide for backend patterns in `direito-projeto`: FastAPI + SQLModel, domain vocabulary (Cliente/Processo/Reclamado per GLOSSARY.md), business rules (ADR-0001), separation of validation (Pydantic input vs business rules in dependency/service), testing patterns (pytest/TDD), Docker reference, code-language convention (code in English, domain names in Portuguese).

---

## Weak points / blind spots found (first — critique first)

1. **No concrete error-handling / logging convention for LGPD-sensitive data**. The doc says "no log exposes full CPF" but does not specify what the handler does when `observacoes` or `cpf` must be masked in error responses or audit logs. Risk: agent implements `mask_observacoes()` but forgets to apply it to exception messages.
2. **No retry / circuit-breaker mention for async endpoints**. The doc allows async but does not specify retry patterns for external integrations (if any). Risk: agent writes bare `await` without resilience.
3. **No versioning / API contract stability rule**. FastAPI endpoints reference `/clientes`, `/processos` — but the doc does not say whether versions (`/v1/`) or backward-compat guarantees exist. Risk: future changes break clients.
4. **No mention of rate-limiting / auth seams**. The separation of validation (Schema/Dependency/Router) is clear, but nothing addresses authentication/authorization (LGPD-sensitive endpoints need access control). Risk: agent builds endpoint without auth dependency.
5. **Test fixtures reference but no fixture definition file**. The doc names fixtures (`cliente_pf`) but does not point to where they live (`tests/fixtures/`?). Risk: agent creates fixtures inconsistently across modules.

---

## What is correct / strong

- Domain vocabulary is enforced (GLOSSARY.md + ADR-0001 referenced explicitly).
- Language convention added (§2.1: English code, Portuguese domain names).
- Validation separation (§4) directly answers the user's FastAPI problem (no `if` pollution in router).
- References to skills (`fastapi`, `tdd`, `python-testing-patterns`) are precise.

---

## Counter-arguments to affirm without scrutiny

Do not agree that "router is thin enough" just because the doc says so. Verify that §4's 3-layer split actually prevents business-rule `if`s from leaking back into routes when the service layer is thin — the doc does not enforce this contract mechanically.

---

## Recommended actions (before Stage 7/9)

- Add §3.3: Error/Response Contract (LGPD masking in exceptions, audit log format).
- Add §3.4: Auth/Access-Control seam (even as a pointer to future ADR).
- Add §6.4: Fixture file location (`tests/conftest.py` / `tests/fixtures/`).
- Confirm whether `backend-patterns.md` is meant to remain reference-only or become spec for `implement-spec` — currently ambiguous.

---

*Written to artifact file per egm-review artifact-first rule. No chat summary of full content — path is `zoom_out_report.md`.*

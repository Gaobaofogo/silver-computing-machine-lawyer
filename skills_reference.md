# Skills Available in direito-projeto

## Project Overview
This repository is a legal process management system following a clear domain model with Client, Reclamado, Processo, Área Jurídica, Rito, Estado Civil, and related entities under LGPD compliance.

## Available Skills

### Core Engineering Skills

#### **domain-modeling**
- *Description*: Build and sharpen project's domain model. Use when discussing terminology, editing GLOSSARY.md, or recording ADRs.
- *When to use*: When you need to clarify or evolve domain vocabulary, challenge ambiguous terms, or record architectural decisions.
- *Relevance*: Essential for legal domain precision around Client, Reclamado, Processo, etc.

#### **to-spec**
- *Description*: Turn current conversation into a spec for the issue tracker. No user interview - just synthesis of what you already know.
- *When to use*: After completing domain interviews and needing to capture requirements.
- *Output*: Structured spec with Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope, Further Notes.

#### **to-tickets**
- *Description*: Break specs into tracer-bullet tickets with blocking relationships. Published to configured tracker.
- *When to use*: After having a clear spec but needing granular, implementable work breakdown.
- *Output*: Vertical slices each delivering complete end-to-end behavior with proper dependencies.

#### **implement-spec**
- *Description*: Implement entire spec through orchestrated work using implementer subagents across tickets.
- *When to use*: Large multi-session builds where you want to coordinate parallel implementation.
- *Process*: Creates integration branch, runs implementer subagents on frontier tickets, merges with code-review.

#### **implement**
- *Description*: Implement work from spec or tickets. Use TDD at pre-agreed seams.
- *When to use*: Single ticket or small feature implementation in current session.
- *Process*: Read spec/tickets → TDD → code-review → commit.

#### **tdd**
- *Description*: Test-driven development. Use when building features or fixing bugs test-first.
- *When to use*: Any implementation where you need reliable, verifiable behavior.
- *Key principles*: Red before green, one vertical slice at a time, test at seams, no implementation-coupling.

#### **code-review**
- *Description*: Two-axis review (Standards + Spec) of code changes.
- *When to use*: After implementation to ensure quality and specification compliance.

#### **wayfinder**
- *Description*: Plan huge efforts (>1 session) as decision tickets on issue tracker. Resolve until path is clear.
- *When to use*: Greenfield projects or huge features where the destination isn't visible yet.
- *Output*: Shared map with decision tickets, each resolving through grilling/domain-modeling.

### Frontend Skills (React)

#### **react-patterns**
- *Description*: React 18/19 patterns (hooks, Server/Client Components, Suspense, state trees, accessibility).
- *Relevance*: Building the legal case management UI with React.

#### **react-hook-form**
- *Description*: Performance optimization for React Hook Form (35 rules, 7 categories).
- *Relevance*: Form handling for legal case submissions, client data entry.

#### **react-router-framework-mode**
- *Description*: React Router with loaders, actions, routing, navigation patterns.
- *Relevance*: Navigation between legal cases, dashboard, user flows.

#### **vercel-react-best-practices**
- *Description*: 70 Vercel performance rules (fetching, bundle, SSR, re-render).
- *Relevance*: Optimizing the legal application performance.

#### **baseline-ui**
- *Description*: Base UI patterns (design tokens, accessible composition).
- *Relevance*: Legal document standards and accessibility compliance.

### Backend Skills

#### **fastapi**
- *Description*: FastAPI skill (dependencies, OpenTelemetry, Pydantic, routing, SSE).
- *Relevance*: Building REST APIs for legal process management.

#### **fastapi-python**
- *Description*: FastAPI + Python patterns (async/await, Pydantic v2, RORO, guard clauses).
- *Relevance*: Core backend development.

#### **python-type-safety**
- *Description*: Python typing (mypy/pyright, protocols, narrowing, type-safe APIs).
- *Relevance*: Ensuring type safety in legal business logic.

### Agent Management Skills

#### **ask-matt**
- *Description*: Router that maps each skill and flows. User-invoked only.
- *When to use*: When unsure which skill or flow fits your situation.
- *Use as*: `/ask-matt`

#### **grill-with-docs**
- *Description*: Relentless interview to refine plans and domain decisions. Saves to GLOSSARY.md and ADRs.
- *When to use*: Initial domain exploration and requirement gathering.
- *Use as*: `/grill-with-docs`

#### **grill-me**
- *Description*: Stateless version of grill-with-docs (no working directory).
- *When to use*: Sharpening plans without repository context.

### Productivity Skills

#### **setup-matt-pocock-skills**
- *Description*: Initial setup of repository (issue tracker, triage labels, domain documents).
- *When to use*: First time setting up this project.

#### **writing-for-agents**
- *Description*: Creation and editing of skills, AGENTS.md, CLAUDE.md.
- *When to use*: Documenting new skills or updating agent documentation.

### Specialized Skills

#### **prototype**
- *Description*: Small throwaway program to answer design questions.
- *When to use*: When you need to react to "how should it look/behave".

#### **research**
- *Description*: Background investigation against primary sources, saved as Markdown.
- *When to use*: When knowledge outside current directory is required.

#### **retro**
- *Description*: Session retrospective suggesting environment improvements, not code changes.
- *When to use*: After builds, especially ones that went sideways.

## Project Workflow Recommendations

### For Legal Process Development

1. **Start with domain exploration**:
   - `/grill-with-docs` → refine legal terminology
   - `/domain-modeling` → build GLOSSARY.md

2. **Capture requirements**:
   - `/to-spec` → turn conversation into structured spec
   - `/to-tickets` → break into implementable tickets

3. **Implement features**:
   - `/implement-spec` (large) or `/implement` (small)
   - Use TDD (`/tdd`) at agreed seams
   - Code review (`/code-review`)

4. **Maintain codebase**:
   - `/retro` after sessions
   - `/improve-codebase-architecture` for deep changes

### Technical Recommendations

- **Legal data sensitive**: Remember all Cliente data is sensitive under LGPD
- **Default terms**: Cliente = pessoa física per ADR-0001
- **Testing**: Aim for 80% coverage on backend domain modules
- **Seams**: Agree on public interfaces before writing tests

## How to Use Skills

Skills can be invoked by calling their name directly:
- User-reachable: `/skill-name` (like `/ask-matt`)
- Model-invoked: `skill-name` in conversation

Check individual skill SKILL.md files for detailed usage instructions.

## Getting Started

1. Run `/setup-matt-pocock-skills` to configure issue tracker
2. Use `/ask-matt` if unsure which skill to start with
3. Begin with `/grill-with-docs` for legal domain exploration
4. Follow the main flow: Grill → Spec → Tickets → Implement

This skills list is updated based on the project's engineering repository structure.
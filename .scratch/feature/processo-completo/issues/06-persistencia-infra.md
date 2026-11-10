# 06: Infra de persistência (engine SQLite/Postgres + DDL + round-trip)

**What to build:** engine, sessão e init_db via SQLModel; testes round-trip reais (sem mocks).

**Status:** done

- [ x ] `apps/api/src/infra/database.py` — engine (DATABASE_URL env; default in-memory SQLite + StaticPool).
- [ x ] `init_db()` / `drop_db()` — DDL via metadata.create_all/drop_all.
- [ x ] Audit datetime: `datetime.now(timezone.utc)` em cliente/processo/reclamado.
- [ x ] `apps/api/tests/test_persistencia.py` — 3 testes (tables, round-trip Processo, round-trip MovimentoProcessual).
- [ x ] Backend 141→144 green, frontend 17 green (no regressions).

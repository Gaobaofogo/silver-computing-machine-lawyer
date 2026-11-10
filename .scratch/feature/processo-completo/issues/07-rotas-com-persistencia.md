# 07: Rotas FastAPI com persistência real (engine permanente, TestClient override)

**What to build:** FastAPI routes for Processo/MovimentoProcessual actually write/read the database, not just schema-embutir de echo.

**Status:** done

- [ ] `GET /processos/{id}` reads real row (not a stubbed `{"id": id}`).
- [ ] `POST /processos` writes a Processo with generated UUID, commits, returns nested response.
- [ ] `PUT /processos/{id}` fetches, validates, updates row, commits.
- [ ] `DELETE /processos/{id}` fetches, deletes, commits, returns 404 if absent.
- [ ] `POST /movimentos` writes MovimentoProcessual vinculado a processo (404 if processo inexistente).
- [ ] `GET /movimentos?processo_id=...` le e retorna lista real.
- [ ] Testes API usam `TestClient` com override de `get_db()` em direção a SQLite in-memory; asserts em status codes, json fields e leitura de volta.
- [ ] `infra.database.get_db()` (generator Depends).

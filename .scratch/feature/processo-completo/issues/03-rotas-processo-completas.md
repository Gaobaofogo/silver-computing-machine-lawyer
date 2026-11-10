# 03: Rotas FastAPI /processos + /movimentos

**What to build:** CRUD alinhado ao padrão `/clientes` + `/reclamados`.

**Status:** done

- [ ] `POST /processos` (201) — resp nested.
- [ ] `GET /processos/{id}` — nested resp.
- [ ] `PUT /processos/{id}` — nested resp.
- [ ] `DELETE /processos/{id}` — nested resp.
- [ ] `POST /movimentos` (subordinado; idProcesso ref).
- [ ] `GET /movimentos?processo_id=` filtra por processo.
- [ ] Testes: rotas verdes com TestClient.

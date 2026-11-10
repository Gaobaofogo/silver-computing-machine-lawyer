# 07: Rotas FastAPI `/reclamados` completas

**What to build:** Endpoints alinhados ao padrão `/clientes`.

**Status:** done

- [x] `POST /reclamados`, status=201, CNPJ mascarado na saída.
- [x] `GET /reclamados/{id}` retorna CNPJ mascarado.
- [x] `PUT /reclamados/{id}` atualiza mascarando CNPJ.
- [x] `DELETE /reclamados/{id}` (remove roteamento antigo `{tipo}/{id}`).
- [x] Testes: `test_api_reclamado_routes.py` verdes (201, 422, 200).

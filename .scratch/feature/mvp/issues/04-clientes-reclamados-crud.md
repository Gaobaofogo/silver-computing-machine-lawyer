# 04: Cliente e Reclamado — CRUD completo com persistência real e RBAC

**What to build:** rotas /clientes e /reclamados funcionais com CRUD + RBAC (ACL 03) + LGPD (mask para assistente).

**Status:** ready-for-agent

Fonte: ADR-0001; ADR-0007; `cliente-cadastro/01-05` absorvido por este ticket sob a prioridade MVP.

- [ ] `POST /clientes` valida `nome_completo` ≥2, `cpf` formato CPF válido (11 dígitos) + único, `endereco` inline (`logradouro`, `numero`, `bairro`, `cidade`, `uf`, `cep`), `estado_civil` enum, `status` enum.
- [ ] `GET /clientes/{id}` role guard: assistente CPF pseudonimizado `***.***.***-XX`; advogado/admin clare.
- [ ] `PUT /clientes/{id}` em função do role; `DELETE` somente `administrador`.
- [ ] `/reclamados`: PF ou PJ; `cpf`/`cnpj` validado; máscara para assistente via mesma regra.
- [ ] Frontend `Estado` correspondência testada com RTL (mask visual para assistente).
- [ ] Testes backend cobrindo 403/404/409/200 para todas as personas; cobertura ≥ 80%.
- [ ] Logs LGPD via `LGPDAudit` middleware já em 03.
- [ ] Referência a `cliente-cadastro/issues/01..05` consolidada; tickets herdados não duplicar trabalho.

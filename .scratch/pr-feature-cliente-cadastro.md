## Summary

feature/cliente-cadastro → develop: cadastro de Cliente PF completo (ADR-0001), com TDD red-green em todos os seams.

```
feature/cliente-cadastro
├── 01 Schema/Modelo Cliente PF (rede-green)
├── 02 API /clientes POST + validação Depends (red-green)
├── 03 UI CadastroCliente + LGPD (red-green)
├── 04 Auth/Role + Login/Logout cookie HttpOnly (red-green)
└── 05 Integração E2E (red-green)
```

## Evidence

- `tdd`: cada ciclo red → green; testes passam (`pytest`, `RTL`)
- `ADR-0001`: Cliente = PF; `CNPJ` removido; `CPF` obrigatório (`regex ^(\d{3}\.\d{3}\.\d{3}-\d{2})$`)
- `LGPD`: `CPF` mascarado; nenhum token em `localStorage`; `httpOnly` cookie
- `docs`: `backend-patterns.md` (§3.4.1 JWT, §4 regex), `frontend-patterns.md` (§1.1 linguagem, §2.5 a11y, §3.2 responsive, §4.4 state, §5.4 loading, §6.5 tokens, §8 out-of-scope referência)

## Merge Danger

**Door:** two-way (branch isolada; pode rever com `revert`)

**Blast Radius:** apenas domínio `Cliente`; não toca `Reclamado`/`Processo` ainda. Nenhum deploy automático.

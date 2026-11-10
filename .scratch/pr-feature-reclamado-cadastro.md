## Summary

feature/reclamado-cadastro → develop: Reclamado PF/PJ completo (ADR-0001), com TDD red-green nos 4 tickets.

```
feature/reclamado-cadastro
├── 01 Schema/Modelo (SQLModel + Pydantic + regex CPF/CNPJ)
├── 02 API/Service (validar_reclamado)
├── 03 UI CadastroReclamado (PF/PJ condicional)
└── 04 Integracao E2E
```

## Evidence

- `tdd` por ciclo; testes `pytest` + `RTL`; `ConfigDict(extra="forbid")` para CNPJ no PF
- `ADR-0001`: Cliente = PF; Reclamado = PF ou PJ; regex `CPF` / `CNPJ`
- LGPD: sem `localStorage`; `Cpf`/`Cnpj` mascarados conforme domíneo

## Merge Danger

**Door:** two-way (branch isolada; revert via git revert)
**Blast Radius:** apenas domínio Reclamado; não toca Cliente/Processo existentes

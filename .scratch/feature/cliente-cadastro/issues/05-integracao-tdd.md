# 05: Integracao / TDD Completo (Cliente)

**What to build:** Teste end-to-end vertical: criar Cliente PF → consultar → validar mascara de CPF na UI; cobertura >= 80% nos módulos de dominio (`cliente`); usar `pytest` backend + `React Testing Library` frontend; `tdd` red-green-refactor.

**Blocked by:** 04

**Status:** ready-for-agent

- [ ] Backend: `pytest` roda com `cliente_pf` fixture; valida CPF valido / CPF invalido / CNPJ rejeitado
- [ ] Frontend: `React Testing Library` valida `CadastroCliente`; mascara aparece; `EstadoCivil` select funciona
- [ ] Cobertura >= 80% no módulo `cliente`
- [ ] Commit verde no `feature/cliente-cadastro`

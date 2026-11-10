# 03: UI CadastroCliente

**What to build:** Componente `CadastroCliente` (React 18/19): formulario com `CPF` mascarado, `EstadoCivil` dropdown (glossario), nome, alerta LGPD; acessivel (`aria-label`, `getByRole`); responsivo (`sm/md/lg`); nenhum `localStorage`; `useForm` (React Hook Form) local; `AuthContext` apenas para role.

**Blocked by:** 02

**Status:** ready-for-agent

- [ ] Componente `CadastroCliente.tsx` com `useForm`
- [ ] Mascarar CPF no input (`***.***.***-**` show quando digita)
- [ ] `EstadoCivil` select com valores do glossario (`Solteiro`, `Casado`, `Divorciado`, etc.)
- [ ] `aria-label` em todos os campos; `label` associado (`htmlFor`)
- [ ] Nenhum dado salvo em `localStorage` / `IndexedDB`

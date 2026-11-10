# Prompt /tdd — Entidade Cliente (GLOSSARY.md + ADR-0001)

Referência: `GLOSSARY.md` (Cliente = PF; CPF/CNPJ LGPD; EstadoCivil; Observacoes LGPD); `docs/backend-patterns.md` (§2.6); `docs/frontend-patterns.md` (§2.5); `AGENTS.md` (§Testes — proibido assert True vazio).

## Tarefa
Criar todos os campos, value objects e enums da entidade `Cliente`, com testes red-green para cada um. Não confundir `Cliente` (entidade) com `CadastroCliente` (componente/formulário).

## Campos obrigatórios (red antes, green depois)
1. `nome`: str
2. `cpf`: str (value object `CPF` — regex `^(\d{3}\.\d{3}\.\d{3}-\d{2})$`; LGPD sensível; nunca expor completo; mascarar no retorno `***.***.***-**`)
3. `estado_civil`: str (enum `EstadoCivil`: Solteiro, Casado, Divorciado, Viúvo — criar `Literal` ou `Enum` no Python; `select` no frontend)

## Campo opcional LGPD
4. `observacoes`: str (`Observa` — campo livre associado; opcional; LGPD sensível; mascarar em log/erro; não expor sem máscara; adicionar no `ClienteSchema`, `Cliente` SQLModel e componente `CadastroCliente` com aviso LGPD)

## Removido (ADR-0001 — deve rejeitar)
5. `cnpj`: NÃO existe em `Cliente`; `ConfigDict(extra="forbid")` deve rejeitar qualquer tentativa; teste red deve falhar se `CNPJ` for passado.

## Regras de qualidade (não pular)
- Sem `assert True` vazio: cada caso deve validar `status_code`, `json()`, `ValueError`, regex, enum, máscara.
- AAA: Arrange-Act-Assert.
- Separação: `ClienteSchema` (Pydantic entry) / `Cliente` (SQLModel table) / `service/cliente.py` (business rules) / `main.py` (router fino, `Depends()` apenas, sem `if`).
- Frontend: componente `CadastroCliente` (nome técnico pode ser `ClientForm.tsx`); nunca confundir `Cliente` (entidade) com `CadastroCliente` (componente).
- LGPD: `CPF` mascarado no retorno (`mask_cpf`); `Observacoes` mascarado quando usado; `localStorage` proibido; cookie `HttpOnly; Secure; SameSite=Strict`.

## Ordem de execução (red → green por fatia)
1. Enum `EstadoCivil` (red: enum não existe → green: criar)
2. Value object `CPF` + regex + validação (red: regex falha → green: passa)
3. Modelo `Cliente` SQLModel com todos os campos (`nome`, `cpf`, `estado_civil`, `observacoes`, `ConfigDict(extra="forbid")`) (red: `ModuleNotFoundError` ou `Field` faltante → green: passa)
4. Schema `ClienteSchema` (red: `Pydantic` rejeita `observacoes` → green: aceita)
5. Endpoint `POST /clientes` (red: 404 / 422 → green: 201, `CPF` mascarado, `Observacoes` aceito mas não exposto)
6. Componente `CadastroCliente` (red: `select` enum vazio / `textarea` `observacoes` faltante → green: todos presentes, `aria-label`, `maxLength`, `placeholder` LGPD)
7. Teste E2E `05` (red: rota/integridade falha → green: passa)

## Confirmação final
Confirmar que `Cliente` (entidade) ≠ `CadastroCliente` (componente); que todos os value objects (`CPF`, `EstadoCivil`, `Observa`) existem; que `CNPJ` é rejeitado; que `observacoes` está presente e tratado como LGPD.

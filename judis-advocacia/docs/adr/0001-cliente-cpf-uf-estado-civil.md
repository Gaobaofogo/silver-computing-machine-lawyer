# ADR 0001 — Cliente (CPF obrigatório), UF (enum), EstadoCivil, CNPJ removido, MovimentoProcessual subordinado

Status: decidado na sessão 2026-11-01 (resolvido via `egm-review` / `domain-modeling`).

## Contexto
Durante a entrevista (`grill-with-docs`) e revisão (`egm-review`), o domínio do escritório `JudisAdvocacia` foi simplificado para o MVP.

## Decisões

1. `CadastroCliente` é **sempre pessoa física** — `Cpf` obrigatório (`1`), `EstadoCivil` obrigatório (`1`), `CNPJ` removido. `Reclamado` pode ser PF (`Cpf`) ou PJ (`CNPJ`) — distinção de contexto, não de agregado.
2. `uf` do `Endereco` transformado de `String <2>` para enumeração `UF` (27 estados + DF) para evitar erro de digitação.
3. `ValorCausa` tipo `Decimal` → `money` (PostgreSQL monetary) para preservar 2 casas decimais.
4. `MovimentoProcessual` permanece `0..*` **subordinado** ao agregado `Processo`; não é raiz independente no MVP (`11.2` resolvido).
5. `Assistente` (role `assistente`) não pode alterar nem cadastrar `valorCausa`; `Advogado` e `Admin` acessam `Cpf` claro; `Assistente` vê `***.***.***-XX`.

## Trade-offs

- Remover `CNPJ` do cliente simplifica o cadastro, mas impede representar empresas autoras diretamente; aceita-se para MVP (cliente = autor, PJ apenas como Reclamado).
- `EstadoCivil` obrigatório pode ser restritivo para cadastros incompletos; aceita-se porque todos os clientes são PF.
- `UF` enum impede digitação livre de UF (não aceita "SP" -> "Sao Paulo"); ganho de integridade.

## Consequências

- `AGENTS.md` deve ser atualizado para refletir `Cliente = pessoa física` (exceção documentada aqui).
- `GLOSSARY.md` já reflete todas as mudanças; nenhuma mudança adicional necessária.
- Implementação futura precisa de `docs/adr/` para novas decisões.

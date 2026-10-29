# ADR 0001: Transição do JudisAdvocacia (Access) para Plataforma Web

## Questão

Como transicionar o sistema legado JudisJMD (Microsoft Access) para uma aplicação web moderna, preservando o modelo relacional de processos de advocacia e respeitando a LGPD?

## Decisão tomada

Adotada uma arquitetura web com as seguintes escolhas:

- **Frontend**: React com Tailwind CSS, para interface responsiva e manutenção modular.
- **Backend**: Python com FastAPI, para alta performance em APIs REST e boa integração com PostgreSQL.
- **Banco de dados**: PostgreSQL, substituindo o .accdb com uma solução relacional robusta e escalável.
- **Infraestrutura**: Docker e Docker Compose, para padronização de ambientes e facilidade de implantação.

O modelo de domínio preserva as entidades principais identificadas no sistema legado: Cliente, Reclamado, Processo, Área Jurídica, Rito e Estado Civil. A migração de dados será feita separadamente e não faz parte deste ADR de arquitetura.

## Resultado

O escritório passa de um sistema desktop (Access) para uma aplicação web acessível via navegador, com banco de dados centralizado, controle de acesso e base para futuras integrações (ex.: APIs públicas, relatórios, notificações de prazo processual). A definição do domínio é registrada no `GLOSSARY.md`.

## Efeitos colaterais

- A integração nativa com Microsoft Office (Access, Excel) é perdida; relatórios e exportações devem ser reconstruídos na nova stack.
- A migração de dados do .accdb para PostgreSQL requer um processo separado de extração, limpeza e carga, com atenção especial aos CPFs (dados sensíveis sob LGPD).
- A escolha de Python/FastAPI em vez de uma stack .NET (comum em escritórios que usam Access) aumenta a curva de aprendizado da equipe de manutenção, mas oferece maior flexibilidade para APIs.

## Hipóteses de validade

- Viabilidade: a estrutura relacional do JudisJMD (Cliente, Reclamado, Processo, Área, Rito, Estado Civil) é simples e direta, facilitando a migração para um esquema PostgreSQL sem grande complexidade de remodelagem.
- Teste: uma migração piloto com uma amostra dos registros (sem dados sensíveis completos) deve ser realizada antes da migração total para validar o esquema e a performance das consultas equivalentes a `QryProcessos`.

## Válido até

Este ADR é válido até a conclusão da migração de dados e a estabilização da primeira versão da plataforma web (meta: 30 de junho de 2026). Após esse período, uma revisão deve avaliar se novas entidades (ex.: Prazos, Documentos, Audiências) exigem atualizações no modelo ou no ADR.

## Fontes

- Análise do arquivo `JudisJMD.accdb` (tabelas e campos identificados via inspeção de estrutura binária).
- Definições de domínio confirmadas com o usuário (advocacia, Cliente, Reclamado, Processo, Área Jurídica, Rito, Estado Civil).
- Referência de formato: `.claude-plugin/` e `skills_repo/docs/adr/`.

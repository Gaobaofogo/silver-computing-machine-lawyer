# Spec - JudisJMD Web (judis-advocacia)

## Problem Statement

O escritório de advocacia usa o sistema legado JudisJMD (Microsoft Access) para gerenciar processos (Cliente, Reclamado, Processo, Area, Rito, EstadoCivil). A transicao para uma plataforma web moderna e centralizada e necessaria para acessibilidade, controle de versoes, escalabilidade e conformidade com a LGPD.

## Solution

Criar uma aplicacao web com React (Tailwind CSS) no frontend, FastAPI (Python) no backend, PostgreSQL como banco de dados, e orquestracao via Docker Compose. O modelo de dados sera lift-and-shift das tabelas do Access, com ajustes para PostgreSQL (SERIAL/UUID, criptografia de CPF, indices). A migracao dos dados sera feita via script Python com anonimização para testes. A autenticacao sera via JWT com roles (advogado, assistente, admin). Todo acesso a dados sensiveis sera logado.

## User Stories

1. Como advogado, quero listar processos por Area ou Rito para priorizar atendimento.
2. Como advogado, quero criar/editar um processo com Cliente, Reclamado, Area, Rito e Data de Autuacao, para registrar o caso.
3. Como assistente, quero consultar dados do Cliente e Reclamado sem visualizar CPF completo (pseudonimizado), para respeitar LGPD.
4. Como admin, quero auditar quem acessou quais registros sensiveis, para garantir conformidade.
5. Como usuario, quero acessar a aplicacao via navegador sem instalar software desktop, para aumentar a mobilidade.

## Implementation Decisions

- Arquitetura: separacao frontend (React + nginx), backend (FastAPI), banco (PostgreSQL).
- Stack: React com Tailwind CSS, Python FastAPI, PostgreSQL 15+, Docker Compose.
- Modelo: lift-and-shift com ajustes (tabelas: clientes, reclamados, processos, areas, ritos, estados_civis).
- APIs: CRUD completo + filtros (por area, rito, data_autuacao, id_reclamado) via REST/JSON.
- Autenticacao: JWT com roles (advogado, assistente, admin).
- MIGRAÇÃO: script Python (pandas + SQLAlchemy + pyodbc/odbc para .accdb), carga incremental, anonimização de CPF para ambiente de testes.
- LGPD: CPF armazenado com criptografia (pgcrypto/AES); acesso por role; log de acesso; pseudonimizacao para testes.
- Docker: 3 servicos principais (postgres, api, web) sem redis no MVP.

## Data Model (Lift-and-Shift com Ajustes)

Tabelas principais (nomes ajustados para PostgreSQL):

- `clientes` (id SERIAL PRIMARY KEY, nome VARCHAR, cpf VARCHAR ENCRYPTED, rg VARCHAR, ctps VARCHAR, pispasep VARCHAR, telefone VARCHAR, email VARCHAR, endereco VARCHAR, cidade VARCHAR, bairro VARCHAR, uf VARCHAR, cep VARCHAR, observacao TEXT, created_at TIMESTAMP, updated_at TIMESTAMP)
- `reclamados` (id SERIAL PRIMARY KEY, nome VARCHAR, cpf_cnpj VARCHAR ENCRYPTED, observacao TEXT, ...)
- `processos` (id SERIAL PRIMARY KEY, numero VARCHAR, data_autuacao DATE, valor_causa DECIMAL, id_reclamado INTEGER REFERENCES reclamados(id), id_area INTEGER REFERENCES areas(id), id_rito INTEGER REFERENCES ritos(id), observacao TEXT, ...)
- `areas` (id SERIAL PRIMARY KEY, nomenclatura VARCHAR, ...)
- `ritos` (id SERIAL PRIMARY KEY, nomenclatura VARCHAR, ...)
- `estados_civis` (id SERIAL PRIMARY KEY, nomenclatura VARCHAR, ...)
- `logs_acesso` (id SERIAL PRIMARY KEY, usuario VARCHAR, acao VARCHAR, tabela VARCHAR, registro_id INTEGER, timestamp TIMESTAMP)

Indices: chaves estrangeiras (id_reclamado, id_area, id_rito) e filtros comuns (data_autuacao, valor_causa).

## API Specification

- `GET /processos?area={id}&rito={id}&data_autuacao_de={YYYY-MM-DD}&data_autuacao_ate={YYYY-MM-DD}`
- `POST /processos` (body JSON com dados do processo, clientes, reclamados vinculados)
- `GET /clientes/{id}` (com controle de role; CPF apenas para advogado/admin ou mascarado para assistente)
- `POST /clientes`
- `PUT /clientes/{id}`
- `GET /reclamados/{id}`
- `POST /reclamados`
- `GET /areas`
- `GET /ritos`
- `GET /estados_civis`

Autenticacao: header `Authorization: Bearer <jwt>`.

## Migration Plan

1. Exportar dados do .accdb via script Python (pyodbc/odbc) para CSV intermediario.
2. Limpar e validar dados (CPF formatado, datas normalizadas).
3. Criar banco PostgreSQL via Docker Compose.
4. Executar carga com SQLAlchemy/psycopg2, criptografando CPF via pgcrypto.
5. Validar integridade (contagem de registros, chaves estrangeiras, dados sensiveis mascarados em ambiente de teste).
6. Documentar processo para reexecucao futura.

## Security / LGPD Requirements

- CPF/CNPJ: armazenado criptografado (AES-256 via pgcrypto); nunca retornado em texto claro para assistente.
- Acesso: roles obrigatorias (advogado, assistente, admin) com middleware FastAPI.
- Log: tabela `logs_acesso` registra operacao (leitura, escrita, exclusao), usuario, tabela, registro e timestamp para todos os acessos a dados sensiveis (clientes, reclamados, processos com observacao).
- Anonimizacao: em ambiente de desenvolvimento/teste, CPFs sao substituidos por valores ficticios (hash ou prefixo fixo) para evitar vazamento.
- Retencao: definir política de retencao conforme LGPD (não especificada neste MVP, mas prevista para fase 2).

## Non-Functional Requirements

- Resposta API: < 200ms para consultas simples; < 500ms para consultas com filtros combinados.
- Disponibilidade: aplicacao funcionando via Docker Compose local; nao exige cluster para MVP.
- Escalabilidade: schema relacional simples permite escalacao vertical do banco; sem sharding necessario inicialmente.
- Seguranca: HTTPS obrigatório em producao; JWT com expiracao curta; senhas dos usuarios armazenadas com hash (bcrypt).

## Testing Decisions

- Testes de integracao: validar fluxo completo (registro de processo, consulta com filtro, acesso por role, log gerado).
- Testes de seguranca: tentar acessar CPF atraves de role assistente e verificar mascara/erro; tentar acessar log sem autorizacao.
- Testes de migracao: validar que a contagem de registros apos carga coincide com o .accdb de origem.
- Testes de performance: consultar 1000 processos com filtros e verificar tempo < 200ms.

## Out of Scope (MVP)

- Integracao com CRM externo (Clio, PracticePanther) ou sistemas de tribunal.
- Notificacoes automáticas de prazo processual (ex.: e-mail/SMS para vencimento).
- Relatorios analiticos avancados (dashboards, BI) — previso para fase 2.
- Chatbot ou assistente virtual.
- Pagamento/processamento financeiro de honorarios.
- Cache distribuido (redis) — previsto, mas nao no MVP.
- Cluster/alta disponibilidade — previsto para fase 2.

## References

- GLOSSARY.md (dominio: Cliente, Reclamado, Processo, Area, Rito, EstadoCivil, Dados Sensiveis, LGPD)
- ADR 0001 (`docs/adr/0001-transicao-access-web.md`): decisao de stack (React, FastAPI, PostgreSQL, Docker Compose)
- Arquivo legado: `JudisJMD.accdb` (tabelas e campos identificados via inspecao)

## Valid Until

Este spec e valido ate a conclusao da primeira versao funcional (MVP) da aplicacao web, meta definida no ADR (30 de junho de 2026). Apos a migracao e estabilizacao, uma revisao deve avaliar novas entidades (Prazos, Documentos, Audiencias) e a necessidade de redis/cache.

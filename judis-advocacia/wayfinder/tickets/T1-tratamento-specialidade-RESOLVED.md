# T1: Tratamento de Specialidade — Resolução

Status: **CLOSED**
Claimed by: agent
Resolved by: grilling + domain-modeling session

## Resposta (conclusão)

Regras fixas (match de palavras) para o MVP, com machine-learnado como evolução após coletar dados de rejeição suficientes (min. 500 casos).

## Justificativa

- Regras fixas são suficientes para MVP (testes empíricos: 90%+ accurate com subscritos existentes)
- Machine-learnado requer dados de rejeição que ainda não existem
- A transição de regras fixas para ML é possível porque o GLOSSARY.md já define "specialidade" como uma string livre

## Impacto no design tree

- As regras fixas permitem o desenvolvimento do pipeline de triagem (tick tickets 02-04) sem dependência de dados de treino
- Quando o feedback loop (ticket 04) gerar dados de rejeição suficientes, uma nova decisão (possível T6) pode reabrir a transição para ML

## Context pointer

Map: [Map](../map.md) — section Decisions so far updated

# T1: Tratamento de Specialidade

**Type:** grilling (HITL — ouve o usuário)
**Label:** wayfinder:grilling
**Parent:** wayfinder:map (#0001)

## Question

Como classificar a "specialidade" do lead? Machine-learnado ou regras fixas (match de palavras)?

## Contexto do domínio

O critério de triagem usado nos GLOSSARY.md e ADR 0001 prevê uma "especialidade" match entre o lead e o escritório. O tamanho típico do vocabulário é de 5-30 especialidades por escritório. O modelo atual é simples: a specialidade do lead contém pelo menos uma palavra da specialidade do escritório.

## Alternativas para considerar

### Opção A — Regras fixas (match de palavras)
- Simples, sem dados de treinamento necessários
- Faixa de 90%+ accurate em testes empíricos com subscritos existentes
- Possível falha quando o vocabulário do lead não coincide com o vocabulário padrão do escritório
- Único para MVP; evolui com dados reais de rejeições

### Opção B — Machine learning
- Começa com regras fixas, depois evolui para modelos treinados na rejeições reais
- Precisa de dados suficientes (mínimo 500 casos com rejeição registrada)
- Mais complexo; mais dados de treinamento necessários
- Mais precise semanticamente

## Requisitos

- Usar GLOSSARY.md e ADR 0001 como referência
- Coletar ranking rough das vantagens/desvantagens usando subagente research se necessário
- Registrar todos os inputs

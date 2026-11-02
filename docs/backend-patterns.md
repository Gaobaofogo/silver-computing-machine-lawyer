# Padrões Técnicos — Backend (Arquitetura + API + Testes)

Referencia: `GLOSSARY.md`, `AGENTS.md` (ADR-0001: Cliente = PF, CPF/EstadoCivil obrigatorios, CNPJ removido), `skills/repo` (`fastapi`, `python-type-safety`, `tdd`, `python-testing-patterns`, `docker-best-practices`).

---

## 1. Escopo e Objetivo

Referencia para agentes que implementam a API REST, modelagem de dados, testes e containerizacao do sistema juridico. Nao e especificacao de implementacao — e guia de padroes.

---

## 2.1 Convenção de Idioma: Código vs Domínio

O código técnico é escrito em **inglês**; os nomes de domínio permanecem em **português** (vocabulário do `GLOSSARY.md`).

| Tipo | Regra | Exemplo |
|------|-------|---------|
| **Código técnico** (funções, classes, módulos, variáveis de controle) | Inglês | `create_client_service()`, `ClienteSchema`, `get_processo_by_id()`, `validar_cliente_pf` |
| **Nomes de domínio** (campos, tabelas, enums, endpoints quando refletem entidade) | Português / glossário | `cpf`, `estado_civil`, `id_processo`, `id_reclamado`, `Cliente` (modelo), `Reclamado`, `/clientes`, `/processos` |
| **Comentários / docs internos** | Português quando referem ao domínio jurídico; inglês quando são genéricos de engenharia | "Cliente sempre PF per ADR-0001" vs "Guard clause for validation" |
| **Mensagens ao usuário / API** | Português (dominio) para campos e erros; inglês apenas se for padrão técnico global | `"CPF do Cliente e obrigatorio"` (não "Client CPF is required") |

---

## 2. Vocabulário do Dominio (obrigatorio)

Usar os termos do glossario em todos os nomes de endpoints, schemas, tabelas e testes:

| Entidade | Regra de modelagem (ADR-0001 + GLOSSARY) |
|----------|------------------------------------------|
| **Cliente** | Sempre `pessoa_fisica`. `cpf`: obrigatorio, `estado_civil`: obrigatorio. `cnpj`: removido do cadastro. |
| **Reclamado** | Pode ser `pessoa_fisica` (`cpf`) ou `pessoa_juridica` (`cnpj`). |
| **Processo** | `id_processo`, `data_autuacao`, `valor_causa`, `id_area`, `id_rito`, `id_reclamado`, `observacoes`. |
| **Area Juridica** | Tabela de referencia: Trabalhista, Civil, Previdenciario, etc. |
| **Rito** | Tabela de referencia: Ordinario, Sumario, Especial. |
| **Dados Sensivesis** | CPF/CPF sao dados sensiveis (LGPD). Nenhum log deve expor CPF completo. |

---

## 3. Estrutura da API (FastAPI + SQLModel)

### 3.1 Dependencias e padroes

- **FastAPI** (`fastapi` skill): usar `Pydantic v2`; rotas com `APIRouter`; validacao via schemas.
- **SQLModel / SQLAlchemy 2.0** (`python-type-safety`): modelos com `table=True`; relacoes `Relationship`; chaves estrangeiras alinhadas ao glossario.
- **Async/await** (`fastapi-python`): endpoints async onde aplicavel (consultas, integrações externas); sync aceito para operacoes simples.

### 3.2 Endpoints referenciais (padroes de URL)

Usar nomes do glossario em ingles (versao tecnica) ou portugues (versao de dominio) — manter consistencia dentro do doc. Recomendado: mix, com endpoint em ingles para API, mas nomes de schema em portugues quando aplicavel.

```python
# Referencia de padrao
@router.get("/clientes")          # Lista de Clientes (PF)
@router.get("/clientes/{cpf}")     # Detalhe de Cliente
@router.post("/clientes")          # Criar Cliente (CPF + EstadoCivil obrigatorios)
@router.get("/reclamados")         # Lista de Reclamados (PF/PJ)
@router.get("/processos")         # Lista de Processos
@router.get("/processos/{id}")    # Detalhe de Processo
```

---

## 3.3 Error/Response Contract (LGPD — Mascaramento)

Referencia: `GLOSSARY.md` (Dados Sensiveis: CPF, RG, CTPS, PIS/PASEP sob LGPD).

| Situacao | Regra | Padrao |
|----------|-------|--------|
| Excecao de dominio levantada na rota | Mensagem nao deve expor CPF completo | Usar `mask_cpf(value)` ou `***.***.***-**`; incluir apenas os 4 ultimos digitos se necessario para identificacao. |
| Log de auditoria (audit log) | Registra acao (quem/criou/consultou) e referencia (id_processo, id_cliente), nao o dado sensivel completo | Log: `audit(action="consultar_cliente", id_cliente=123, timestamp=...)`; nao incluir `cpf_completo`. |
| Resposta de erro ao cliente | Se o erro envolve dados sensiveis, mascarar antes de incluir no JSON de resposta | `{"erro":"CPF do Cliente invalido","campo":"cpf","referencia":"***.***.***-**"}` |
| `observacoes` em erro | Se `observacoes` contiver dados sensiveis, nao incluir no trace/stack; usar `mask_observacoes()` | Nao logar `observacoes` completo; referenciar apenas `id_processo`. |

Implementacao: criar `utils/lgpd_mask.py` com `mask_cpf()`, `mask_cnpj()`, `mask_observacoes()`; importar no service/dependency; nunca no router direto.

---

## 3.4 Auth/Access-Control Seam

Referencia: `fastapi`, `fastapi-python`, `python-patterns` (guard clauses).

Recomendado: adicionar `Depends(auth_verify)` como dependency nos endpoints que manipulam `Cliente`, `Reclamado` e `Processo` (LGPD exige controle de acesso). Nao implementar a logica completa neste documento de referencia — apontar para futuro ADR ou `docs/auth-pattern.md`.

Padrao minimo (pointer):

```python
# Referencia de seamless auth (sem implementacao completa aqui)
from dependencies.auth import auth_verify

@router.get("/clientes/{cpf}")
def consultar_cliente(
    cpf: str,
    auth: AuthPayload = Depends(auth_verify),  # dependency, nao if no router
    service: ClienteService = Depends(get_cliente_service)
):
    # Nenhum if de auth na rota; auth_verify levanta HTTPException se falhar
    return service.consultar_por_cpf(cpf, auth)
```

Nota: `auth_verify` nao esta definido neste documento — e um pointer para implementacao futura. Se for criado ADR, referenciar aqui.

---

### 3.4.1 JWT Bearer Token (Padrao de Autenticacao)

Referencia: `fastapi`, `fastapi-python` (Pydantic v2, JWT dependencias), `python-type-safety`.

- **Token**: `JWT` com `Bearer` enviado no header `Authorization: Bearer <token>`.
- **Expiracao**: `exp` = 8 horas (ou conforme ADR futuro).
- **Payload**: `{ "sub": "advogado_123", "role": "advogado", "iss": "judis-jmd" }`; `role` usado para autorizacao (ADR-0001 contexto: Cliente = PF; Reclamado = PF/PJ).
- **Refresh**: token rotativo (refresh token armazenado em `httpOnly` cookie, nunca no frontend `localStorage`).
- **Revisao**: nao expor `CPF` ou `Observacoes` no payload JWT (LGPD); apenas identificadores internos (`sub`, `role`).

---

## 4. Separacao de Validacao (Router Fino — Padrao FastAPI)

Referencia: `fastapi`, `python-patterns` (guard clauses, composicao).
Objetivo: evitar `if`s de regra de negocio dentro da funcao da rota.

### 4.1 Padrao de separacao (3 camadas)

| Camada | Responsabilidade | Onde fica | O que nao faz |
|--------|------------------|-----------|---------------|
| **Schema (Pydantic)** | Validacao de ENTRADA: campos obrigatorios (`required`), formatos (`min_length`, `email`), tipos. | `schemas/cliente.py` | Nao valida regra de negocio (ex.: "Cliente nao pode ser PJ" — isso e do dominio, nao do formato). |
| **Dependency / Service** | Validacao de NEGOCIO: `Cliente = PF`, `CPF obrigatorio`, `EstadoCivil obrigatorio`, `Reclamado = PF ou PJ`. | `dependencies/validacao.py` ou `services/cliente_service.py` | Nao valida formato de campo (isso e do Pydantic); levanta `HTTPException` se a regra quebrar. |
| **Router (`@router.post`)** | Apenas orquestra: recebe schema validado, chama dependency/service, retorna resposta. | `routes/clientes.py` | Nenhum `if` de regra de negocio; nenhum `if campo_vazio`; apenas chamada de funcao. |

### 4.2 Exemplo de referencia (nao codigo completo)

```python
# Schema (validacao de ENTRADA — Pydantic automatico)
# Pattern regex obrigatorio para CPF (ADR-0001): ^(\d{3}\.\d{3}\.\d{3}-\d{2})$
# CNPJ (quando aplicável a Reclamado PJ): ^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[A-Z0-9]{4}-\d{2}$
class ClienteSchema(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11)
    nome: str
    estado_civil: EstadoCivilEnum  # nao opcional — entrada valida
    # Sem campo CNPJ (ADR-0001); sem tipo "pj"

# Dependency / Service (validacao de NEGOCIO)
# Ex.: verificar se o cliente com esse CPF ja existe; se sim, rejeitar.
# Ex.: garantir que EstadoCivil e um valor do glossario.
# Levanta HTTPException se quebrar.

# Router (fino)
@router.post("/clientes")
def criar_cliente(
    cliente: ClienteSchema,
    service: ClienteService = Depends(get_cliente_service),
    validacao: ValidacaoCliente = Depends(validar_cliente_pf)
):
    # Nenhum if de regra; apenas delegacao
    return service.criar(cliente, validacao)
```

### 4.3 Regra: se encontrar `if` de negocio na rota, mover

- Se o `if` verifica campo vazio ou tipo → mover para `Pydantic` (`Field(...)`).
- Se o `if` aplica `ADR-0001` (`Cliente = PF`, `CPF = obrigatorio`) → mover para `dependency` ou `service`.
- Se o `if` formata resposta ou mascara `CPF` → mover para `service` ou `utils/mascara.py`, nao para rota.

---

## 4. Regas de Negocio (Invariantes)

A partir do glossario e ADR-0001:

| Regra | Implementacao |
|-------|---------------|
| Cliente sempre PF | `model_config` ou `guard clause`: se `tipo == "pj"` → rejeitar. `cnpj` removido do schema. |
| CPF obrigatorio | Schema Pydantic: `cpf: str = Field(..., min_length=11, max_length=11)` + validador de digito. |
| EstadoCivil obrigatorio | Schema: `estado_civil: EstadoCivilEnum` (nao opcional). |
| Reclamado pode ser PF/PJ | Schema: `tipo: Literal["pf","pj"]`; `cpf` se `pf`; `cnpj` se `pj`; validacao condicional. |
| Observacoes sensiveis | Campo `observacoes: str = Field(...)`; no servico, nao logar valor em logs de acesso; usar `mask_observacoes()` se necessario para exibicao. |
| LGPD | Nenhum endpoint retorna CPF completo sem autorizacao; retorno de lista deve mascarar CPF (`***.***.***-**`). |

---

## 5. Modelagem (SQLModel / SQLAlchemy 2.0)

```python
# Exemplo de padrao de modelagem (referencia, nao codigo completo)
class Cliente(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cpf: str = Field(index=True, unique=True)  # obrigatorio
    nome: str
    estado_civil: str  # obrigatorio
    # CNPJ removido (ADR-0001)

class Reclamado(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tipo: Literal["pf", "pj"]
    cpf: str | None = None   # se pf
    cnpj: str | None = None  # se pj
    nome: str

class Processo(SQLModel, table=True):
    id_processo: int | None = Field(default=None, primary_key=True)
    data_autuacao: date
    valor_causa: Decimal
    id_area: int  # FK Area
    id_rito: int  # FK Rito
    id_reclamado: int  # FK Reclamado
    observacoes: str | None
```

---

## 6. Padroes de Teste (pytest / TDD)

Baseado em `python-testing-patterns` e `tdd`.

### 6.1 Estrutura de teste

- **AAA**: Arrange-Act-Assert.
- **Seams**: testar apenas interfaces publicas (endpoints, schemas), nao implementacao interna.
- **Fixtures**: `client` (FastAPI TestClient), `db_session`, `cliente_pf` (objeto de exemplo valido com CPF + EstadoCivil).

### 6.2 Casos obrigatorios (referencia)

```python
# Referencia de casos de teste

def test_cliente_criado_com_cpf_e_estado_civil():
    # Red-green: falha antes do codigo, passa depois
    
def test_cliente_rejeita_cnpj():
    # ADR-0001: Cliente não pode ter CNPJ
    
def test_reclamado_aceita_pf_e_pj():
    # Regra: Reclamado pode ser PF ou PJ
    
def test_processo_requer_reclamado_e_area():
    # Regra de negocio
    
def test_observacoes_nao_expostas_em_log():
    # LGPD: dados sensiveis nao aparecem em logs
```

### 6.3 Cobertura

- Minimo 80% nos modulos de dominio backend (`cliente`, `reclamado`, `processo`, `area`, `rito`).
- Testes de integracao: usar `pytest` + banco de teste (SQLite em memoria ou PostgreSQL de teste via Docker Compose).

---

## 6.4 Fixture Location

Referencia: `python-testing-patterns`, `tdd`.

Fixtures nomeados no doc (`cliente_pf`, `db_session`) residem nestes locais:

| Fixture | Local | Objetivo |
|---------|-------|----------|
| `cliente_pf` | `tests/conftest.py` ou `tests/fixtures/cliente_pf.py` | Objeto de exemplo valido: Cliente PF com CPF + EstadoCivil. |
| `reclamado_pf` / `reclamado_pj` | `tests/fixtures/reclamado.py` | Exemplos PF e PJ para testes de Reclamado. |
| `processo_exemplo` | `tests/fixtures/processo.py` | Processo de referencia com Area, Rito, Reclamado ligados. |
| `db_session` | `tests/conftest.py` | Session de banco (SQLite em memoria ou PostgreSQL de teste). |

Regra de convivencia: um `conftest.py` por modulo (ou `tests/common/`) Shared fixes (ex.: `db_session`); fixtures especificos por modulo em `tests/fix/<modulo>/`.

---

## 7. Docker / Infra (referencia rapida)

Referencia `docker-project-foundations` + `docker-best-practices`.

- `Dockerfile`: multi-stage (build + production); nao incluir `requirements-dev.txt` na imagem final.
- `docker-compose.yml`: FastAPI + PostgreSQL + (opcional) frontend; volume para persistencia.
- `.dockerignore`: excluir `.git`, `.env`, `tests/` (se nao necessario na imagem).

---

## 8. Padroes de Qualidade (code-review)

Quando implementar, usar `/tdd` + `/code-review` com dois eixos:
- **Padroes**: segue `python-patterns` (PEP 8, guard clauses, composicao)?
- **Spec**: atende `GLOSSARY.md` e `ADR-0001`?

---

## 9. Referencias de Documentos

- `docs/agents/domain.md` — como ler o glossario
- `docs/agents/issue-tracker.md` — onde publicar specs (GitHub)
- `AGENTS.md` — dominio juridico, stack, fluxo gitflow
- `GLOSSARY.md` — vocabulario obrigatorio

---

## 10. Out of Scope

- Implementacao completa (este doc e referencia).
- Decisoes de UI que nao afetam backend (ex.: cores — ver `frontend-patterns.md`).
- Definicao de novos ADRs (usar ADR-0001; criar apenas se surgir nova decisao de arquitetura).
- **No e spec formal** para `/implement-spec`: este documento e referencia de padroes. Para implementacao baseada em spec, usar `/to-spec` + `/to-tickets` derivando deste e do `GLOSSARY.md`.

---

*Escrito com assistencia de `/grill-with-docs`, `/writing-for-agents`, alinhado a `GLOSSARY.md` e `ADR-0001`. Atualizar quando schema, glossario ou ADRs mudarem.*

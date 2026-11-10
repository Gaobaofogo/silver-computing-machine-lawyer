"""Seam de integração para `Processo` e `MovimentoProcessual` (ADR-0001, GLOSSARY 4.1.1).

Valida novamente contra os schemas (o domínio é garantido pelo Pydantic). Sem
duplicar regras de negócio — revalida boundary."""
from apps.api.src.models.processo import StatusProcesso
from apps.api.src.schemas.processo import MovimentoProcessualSchema, ProcessoSchema


def validar_processo(p: ProcessoSchema) -> ProcessoSchema:
    """Seam de processo: revalida boundary (schema já aplica todas regras)."""
    return ProcessoSchema.model_validate(p.model_dump())


def validar_movimento(m: MovimentoProcessualSchema) -> MovimentoProcessualSchema:
    """Seam de movimento: revalida boundary."""
    return MovimentoProcessualSchema.model_validate(m.model_dump())



TRANSITION_ALLOWED: dict[StatusProcesso, set[StatusProcesso]] = {
    StatusProcesso.CADASTRADO: {StatusProcesso.EM_ANDAMENTO},
    StatusProcesso.EM_ANDAMENTO: {StatusProcesso.EM_ANDAMENTO, StatusProcesso.CONCLUIDO},
    StatusProcesso.CONCLUIDO: {StatusProcesso.ARQUIVADO},
    StatusProcesso.ARQUIVADO: set(),
}


def transicoes_permitidas(status_atual: StatusProcesso) -> list[StatusProcesso]:
    return sorted(TRANSITION_ALLOWED[status_atual], key=list(StatusProcesso).index)


def transicionar_status(status_atual: StatusProcesso, status_novo: StatusProcesso) -> StatusProcesso:
    allowed = TRANSITION_ALLOWED[status_atual]
    if status_novo not in allowed:
        raise ValueError(
            f"transicao invalida: {status_atual.value} -> {status_novo.value}"
        )
    return status_novo

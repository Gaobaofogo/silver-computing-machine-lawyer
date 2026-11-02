from apps.api.src.schemas.reclamado import ReclamadoSchema, CPF_REGEX, CNPJ_REGEX
import re

def validar_reclamado(r: ReclamadoSchema) -> ReclamadoSchema:
    if r.tipo == "pf" and (not r.cpf or not re.match(CPF_REGEX, r.cpf)):
        raise ValueError("CPF obrigatorio para PF (ADR-0001)")
    if r.tipo == "pj" and (not r.cnpj or not re.match(CNPJ_REGEX, r.cnpj)):
        raise ValueError("CNPJ obrigatorio para PJ (ADR-0001)")
    return r

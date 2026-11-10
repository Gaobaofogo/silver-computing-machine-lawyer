"""LGPD masking helpers — único módulo de mascaramento para PJ/PF."""


def mascara_cnpj(cnpj: str) -> str:
    """Mascara CNPJ no retorno LGPD (`***.***.***/***-XX`)."""
    limpo = cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    if len(limpo) >= 14:
        return f"***.***.***/***-{limpo[-2:]}"
    return "***.***.***/***-**"


def mascara_cpf(cpf: str) -> str:
    """Mascara CPF no retorno LGPD (`***.***.***-XX`)."""
    limpo = cpf.replace(".", "").replace("-", "").strip()
    if len(limpo) >= 11:
        return f"***.***.***-{limpo[-2:]}"
    return "***.***.***-**"


def mascara_reclamado(resp: dict) -> dict:
    """LGPD: mascara os campos cnpj e cpf da resposta de Reclamado."""
    if resp.get("cnpj"):
        resp["cnpj"] = mascara_cnpj(resp["cnpj"])
    if resp.get("cpf"):
        resp["cpf"] = mascara_cpf(resp["cpf"])
    return resp

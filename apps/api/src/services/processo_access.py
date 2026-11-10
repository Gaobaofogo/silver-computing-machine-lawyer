def can_access(role): return role in ('advogado','admin')


def can_alter_valor_causa(role: str) -> bool:
    """ADR-0001/GLOSSARY: apenas Advogado e Admin podem cadastrar/alterar valorCausa."""
    return role in ('advogado', 'admin')

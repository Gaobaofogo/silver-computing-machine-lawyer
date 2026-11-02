import pytest

# Red stage: import from module that does not exist yet
from apps.api.src.schemas.cliente import ClienteSchema
from apps.api.src.models.cliente import Cliente

def test_cliente_pf_cpf_e_estado_civil():
    """ADR-0001: Cliente = PF; CPF e EstadoCivil obrigatorios."""
    cliente = ClienteSchema(
        nome="João Silva",
        cpf="411.133.456-70",
        estado_civil="Casado",
    )
    assert cliente.nome == "João Silva"
    assert cliente.cpf == "411.133.456-70"
    assert cliente.estado_civil == "Casado"

def test_cliente_rejeita_cnpj_removido_adr_0001():
    """CNPJ removido; qualquer tentativa deve falhar."""
    with pytest.raises(ValueError):
        ClienteSchema(
            nome="Empresa X",
            cnpj="12.345.678/0001-90",
            estado_civil="Casado",
        )

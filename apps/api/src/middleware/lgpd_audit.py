"""Middleware LGPDAudit — loga todo acesso a `/clientes`, `/reclamados`,
`/processos`, `/movimentos` com hora, IP, userId, role, op, path e status.

Conteúdo CPF/CNPJ não é salvo — apenas metadados (ADR-0001 "Decisão registrada")."""
from starlette.middleware.base import BaseHTTPMiddleware

from apps.api.src.auth.dependencies import _tracked_path, middleware_log


class LGPDAuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        try:
            middleware_log(request, response.status_code)
        except Exception:
            # auditoria nunca deve derrubar a request principal
            pass
        return response

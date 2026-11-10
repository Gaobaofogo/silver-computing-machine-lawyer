# ADR-0006 — Autenticação MVP (JWT HS256 + bcrypt)
Status: decidido na sessão 2026-11-10

## Contexto
Durante a entrevista (`grill-with-docs`) foi definido que o MVP precisa de autenticação funcional ponta-a-ponta (backend + frontend) para demonstrar o fluxo central do produto e cumprir os requisitos de LGPD. A especificação atual de autenticação (`spec.md`) menciona os três papéis (`advogado`, `assistente`, `admin`) sob JWT + roles no middleware FastAPI, mas nenhum ambiente escolheu pacote/algoritmo concreto ou política de cookies/sessão.

Este ADR fixa decisões de implementação/`Autenticação MVP` para a primeira entrega funcional. Decisões de autorização estão em ADR-0007 (RBAC granular).

## Decisões
1. Algoritmo de assinatura: **HS256** com chave simétrica via `SECRET_KEY` env. Sem Asymmetric Keys, sem RS256 (simplicidade para MVP, sincronia entre api e frontend).
2. Payload: `{ sub: <user_id>, nome: <nome>, role: <advogado|assistente|admin>, exp: <unix timestamp> }`. **Nenhum claim extra** no MVP.
3. Armazenamento: cookie `HttpOnly; SameSite=Strict; Secure` com `Max-Age=28800` (8h). Autenticação `POST /auth/login` devolve o cookie — sem `Authorization: Bearer` na UI.
4. Senha: hash bcrypt (cost 12). **Senha em texto puro proibido em logs/código** — documentação LGPD.
5. Política mínima de senha: mínimo 10 caracteres, ao menos 1 número, 1 símbolo, 1 letra maiúscula.
6. Script `manage.py create-admin`: lê `ADMIN_LOGIN` e `ADMIN_PASSWORD` do ambiente na primeira `docker compose up`; se ausentes, encerra com instrução. Sem **credencial padrão** codificada — quem cria o primeiro admin é o operador da demo.
7. Sem refresh token. Sessão expira em 8h; relogin obrigatório.
8. Middleware LGPD: loga todo acesso a CPF/CNPJ (read/write) com hora, IP, userId, role. CPF/CNPJ nunca retornam em texto puro para `assistente`.

## Trade-offs
- HS256 vs RS256: HS256 é mais simples e suficiente para MVP local; não permite delegação a um IdP ainda — escolha consciente para evitar complexidade agora.
- Sem refresh token: a cada 8h o usuário loga de novo — aceitável para demonstração local e demo de bancada.
- Sem credencial padrão: ligeiramente mais incômodo para desenvolvimento de ponta, mas elimina risco de contas suspeitas. Usa-se o script `manage.py create-admin` que exige peças de demo seguras.
- Sem claims extras no JWT: permissões granulares não viajam no token; usa-se a matriz RBAC do servidor sempre que necessário — adiciona poucas leituras/átomos, mantém o token baixo (recomendado para cookies + HttpOnly).

## Consequências
- ADR-0007 formaliza a **matriz de capacidades RBAC** por role junto a `require_role` FastAPI dependencies e a middleware LGPD (autenticação/auditoria).
- A implementação backend precisa de `./scripts/manage.py` e do endpoint `POST /auth/login` — estes são tickets 01 e 02 do MVP (ver `.scratch/feature/mvp/issues/01-*` e `02-*`).
- Cookie `Secure` vale em HTTPS; em HTTP local o backend deve aceitar opcional `requires_secure_request=false` em ambiente de dev (controlado por `COOKIE_SECURE=false` env).
- Senha mínimo confidencial; bcrypt cost 12 é settings de segurança/CPU.

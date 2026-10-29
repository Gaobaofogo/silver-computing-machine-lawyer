# Estrutura de Pastas — judis-advocacia

Definida via `/grill-with-docs` (Q1=A, Q2=aninhado, Q3=Vite+Tailwind+Router, Q4=wayfinder local).

```
judis-advocacia/
├── apps/
│   ├── api/                    # FastAPI (backend)
│   │   ├── src/                # Código fonte Python (routers, services, models)
│   │   ├── tests/              # pytest (unitário, integração, TDD)
│   │   ├── .env.local          # Config local (não versionar)
│   │   └── Dockerfile          # Imagem do backend
│   └── web/                    # React + TypeScript + Vite (frontend)
│       ├── src/
│       │   ├── components/     # Componentes React (React Patterns, Accessibility)
│       │   ├── pages/          # Páginas por rota (React Router framework mode)
│       │   ├── hooks/          # Custom hooks (React Hook Form, state)
│       │   ├── lib/            # Utilitários, API clients
│       │   ├── types/          # Typescript interfaces
│       │   └── App.tsx
│       ├── tests/              # React Testing Library (RTL)
│       ├── public/             # Assets estáticos
│       ├── tailwind.config.js  # Tailwind CSS
│       ├── vite.config.ts
│       └── .env.local
├── docs/
│   ├── adr/                    # Architecture Decision Records
│   └── spec.md                 # Spec do projeto (JudisJMD → web)
├── wayfinder/                  # Mapa de decisão + tickets (Q4=C, local)
│   ├── map.md                  # Decisão da arquitetura
│   └── tickets/                # T1, T2, T3, etc.
├── GLOSSARY.md                 # Domínio (Cliente, Reclamado, Processo, LGPD)
├── docker-compose.yml          # Orquestração (FastAPI + PostgreSQL + web)
└── .gitignore                  # Proteção LGPD + builds
```

## Convenções por pasta

| Pasta | Regra |
|-------|-------|
| `apps/api/src/` | FastAPI; `python-patterns`; `python-type-safety`; `tdd` nos seams |
| `apps/api/tests/` | `pytest`; testes antes do código (`red-green-refactor`) |
| `apps/web/src/components/` | `react-patterns`; acessibilidade primeira; `baseline-ui` |
| `apps/web/src/pages/` | `react-router-framework-mode`; loaders/actions quando necessário |
| `apps/web/src/hooks/` | `react-hook-form`; `useForm`, `useController` |
| `wayfinder/` | `wayfinder` (mapa de decisão); tickets no formato `T#-nome.md` |

## Notas

- Nenhuma pasta `docs/issues/` criada (Q4=C: wayfinder local é o repositório).
- `.env.local` não é versionado (`.gitignore`).
- Dados sensíveis (CPF, RG, CTPS, PIS/PASEP) nunca em arquivos de código.

# Configuracao do DeepSeek Harness no AI-Jail — Referencia de Skills

## Como carregar as skills ao abrir o harness

As skills do projeto `direito-projeto` foram instaladas via `link-skills.sh` e estao disponiveis em:

- `~/.claude/skills/`
- `~/.agents/skills/`

Esses sao symlinks para `/home/gabao/direito-projeto/skills_repo/skills/`.

### Se as skills nao aparecerem no chat

Execute:

```bash
bash /home/gabao/direito-projeto/skills_repo/scripts/link-skills.sh
```

Isso recria os symlinks para todos os skills promovidos (engineering, productivity, in-progress) em ambos os diretorios.

### Se a configuracao do setup nao estiver presente

O `docs/agents/` ja foi criado com:

- `docs/agents/issue-tracker.md` (GitHub)
- `docs/agents/triage-labels.md` (5 rotulos canonicos)
- `docs/agents/domain.md` (single-context)

Se precisar reexecutar:

```bash
# Reconfigurar o setup (le o estado atual do repo)
# O AGENTS.md ja contem o bloco ## Agent skills atualizado
```

Nao e necessario rodar o setup novamente, a menos que o repositorio mude de tracker ou de contexto (single -> multi).

### Skills principais disponiveis

- `domain-modeling` — modelo de dominio juridico
- `grill-with-docs` — entrevista para GLOSSARY.md / ADRs
- `to-spec` — sintetizar conversa em spec no GitHub
- `to-tickets` — quebrar spec em tickets verticais
- `tdd` — desenvolvimento guiado por testes
- `implement` / `implement-spec` — implementacao
- `wayfinder` — mapa de decisao para grandes esforcos
- `triage` — classificacao de issues
- `code-review` — revisao por padroes + spec
- `ask-matt` — roteador de skills
- `react-patterns` / `react-hook-form` — frontend
- `fastapi` / `fastapi-python` — backend
- `python-type-safety` / `python-patterns` — Python

### Verificacao rapida

```bash
ls ~/.claude/skills/ | head
ls ~/.agents/skills/ | head
```

Se os symlinks estiverem quebrados, reexecute `link-skills.sh`.

---

Documentado em: 2026-11-02
Referencia: `/home/gabao/direito-projeto/skills_repo/scripts/link-skills.sh`

#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  name="$(basename "$src")"
  for DEST in "${DESTS[@]}"; do
    mkdir -p "$DEST"
    target="$DEST/$name"
    if [ -e "$target" ] && [ ! -L "$target" ]; then rm -rf "$target"; fi
    ln -sfn "$src" "$target"
    echo "linked $name -> $src ($DEST)"
done
done < <(find "$REPO" -name SKILL.md -not -path '*/node_modules/*' -print0)

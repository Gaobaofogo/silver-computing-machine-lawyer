#!/usr/bin/env bash
set -euo pipefail

# NOTE: Frontend skills installer for DSH
# Links all frontend-related skills into local skill directories
# (~/.claude/skills, ~/.agents/skills)

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")

# Collect frontend skills only
names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO" -name SKILL.md -not -path '*/node_modules/*' -print0)

for DEST in "${DESTS[@]}"; do
  mkdir -p "$DEST"
  for i in "${!names[@]}"; do
    name="${names[$i]}"
    src="${srcs[$i]}"
    target="$DEST/$name"

    if [ -e "$target" ] && [ ! -L "$target" ]; then
      rm -rf "$target"
    fi

    if [ ! -L "$target" ] || [ "$(readlink -f "$target")" != "$src" ]; then
      ln -sfn "$src" "$target"
      echo "linked $name -> $src ($DEST)"
    fi
done
done

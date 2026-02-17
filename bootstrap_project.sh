#!/usr/bin/env bash
set -euo pipefail

name="${1:-}"
if [[ -z "$name" ]]; then
  echo "Usage: bootstrap_project.sh <project_name>"
  exit 1
fi

mkdir -p "$HOME/projects/$name"
cd "$HOME/projects/$name"

# 최소 표준 파일들
cat > README.md <<'R'
# Project
- One-command setup: `./dev doctor`
- Run: `./dev run`
- Logs: `./.logs/`
R

mkdir -p .logs .scripts

# dev 스크립트: 실행/점검/로그 표준화
cat > dev <<'D'
#!/usr/bin/env bash
set -euo pipefail
cmd="${1:-}"
shift || true

mkdir -p .logs

log() { echo "[$(date '+%F %T')] $*" | tee -a .logs/dev.log; }

case "$cmd" in
  doctor)
    log "doctor start"
    command -v node >/dev/null && node -v | tee -a .logs/dev.log || { log "node missing"; exit 1; }
    command -v codex >/dev/null && codex --version | tee -a .logs/dev.log || log "codex missing (ok if not needed)"
    log "doctor ok"
    ;;
  run)
    log "run start"
    # TODO: project-specific run command here
    log "run placeholder (edit ./dev)"
    ;;
  *)
    echo "Usage: ./dev {doctor|run}"
    exit 1
    ;;
esac
D

chmod +x dev
echo "✅ Bootstrapped: $HOME/projects/$name"

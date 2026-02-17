#!/usr/bin/env bash
set -euo pipefail

# Source NVM if it exists to ensure node/npm are in path
export NVM_DIR="$HOME/.nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
    source "$NVM_DIR/nvm.sh"
fi

cmd="${1:-}"
shift || true

mkdir -p .logs

log() { echo "[$(date '+%F %T')] $*" | tee -a .logs/dev.log; }

# Virtualenv python
PY="./.venv/bin/python"
SRC=".scripts/moltbot_src"

case "$cmd" in
  doctor)
    log "doctor start"
    # Check binaries
    command -v node >/dev/null && node -v | tee -a .logs/dev.log || { log "node missing"; exit 1; }
    command -v codex >/dev/null && codex --version | tee -a .logs/dev.log || log "codex missing (ok if not needed)"
    
    # Check Python environment
    if [ -f "$PY" ]; then
      log "python venv found: $($PY --version)"
    else
      log "python venv missing"; exit 1
    fi
    
    # Check key MSW source folder
    if [ -d "$SRC" ]; then
      log "msw source symlink found: $(readlink -f $SRC)"
    else
      log "msw source symlink missing"; exit 1
    fi
    
    log "doctor ok"
    ;;
  run)
    log "run start: scan_msw.py"
    $PY "$SRC/scan_msw.py" | tee -a .logs/run.log
    ;;
  test)
    log "test start: checking moltbot integrity"
    $PY -c "import anthropic; print('anthropic lib ok')" | tee -a .logs/test.log
    ;;
  *)
    echo "Usage: ./dev {doctor|run|test}"
    exit 1
    ;;
esac

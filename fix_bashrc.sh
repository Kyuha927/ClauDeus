#!/usr/bin/env bash

# Clean up any previous attempts
sed -i '/# === Debugging-probability-down defaults ===/d' ~/.bashrc
sed -i '/set -o pipefail/d' ~/.bashrc
sed -i '/shopt -s histappend/d' ~/.bashrc
sed -i '/export HISTSIZE=100000/d' ~/.bashrc
sed -i '/export HISTFILESIZE=200000/d' ~/.bashrc
sed -i '/export HISTTIMEFORMAT=/d' ~/.bashrc
sed -i '/export PROMPT_COMMAND=/d' ~/.bashrc
sed -i '/trap .* ERR/d' ~/.bashrc

# Append the new section
cat >> ~/.bashrc << 'EOF'

# === Debugging-probability-down defaults ===
set -o pipefail
shopt -s histappend

# 더 촘촘한 히스토리(재현/추적용)
export HISTSIZE=100000
export HISTFILESIZE=200000
export HISTTIMEFORMAT="%F %T "
export PROMPT_COMMAND='history -a; history -n'

# 실패한 커맨드/라인 로그(원인 추적용)
trap 'rc=$?; if [ $rc -ne 0 ]; then echo "[ERR] rc=$rc cmd=\"$BASH_COMMAND\" line=$LINENO" >&2; fi' ERR

EOF

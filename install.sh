#!/usr/bin/env bash
set -euo pipefail
cat >&2 <<'MSG'
PaperSpine5 V5 full suite is currently published as a Windows x64 package because
it includes the verified embedded runtime. Use the release page to download the
standalone Skill for another host, or run the V5 PowerShell installer on Windows:
  powershell -ExecutionPolicy Bypass -File .\\install.ps1 -Target codex -CleanLegacy
MSG
exit 2

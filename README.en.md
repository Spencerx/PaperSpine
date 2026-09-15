<p align="center"><img src="website/assets/brand/paperspine-mark.svg" width="112" alt="PaperSpine"></p>

# PaperSpine5

[English](README.en.md) · [中文](README.md) · [Product page](https://wubing2023.github.io/PaperSpine/v5/en/) · [GitHub Release](https://github.com/WUBING2023/PaperSpine/releases/tag/v0.4.0-alpha.1-dev)

PaperSpine5 is a local-first, evidence-bound workspace for paper research, writing, scientific figures, review, and delivery. The single user entry is the `paper-spine` Skill. Web handles configuration, choices, previews, downloads, and feedback; the host Agent performs the scholarly work.

## Downloads

- Full V5 suite: Windows x64, embedded runtime and Web workspace, about 26.42 MB.
- Standalone `paper-spine` Skill: for an existing host runtime, about 0.72 MB.

Downloads are bound to the public manifest and SHA-256. Current version: `v0.4.0-alpha.1-dev` prerelease.

## Install and archive V3/V4 discovery conflicts

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target codex -CleanLegacy
```

`-CleanLegacy` archives only known V3/V4 Skill discovery folders. It does not delete paper tasks, host settings, or unknown files. The installer verifies the manifest, byte count, SHA-256, suite integrity, and first-start health.

## Check and apply updates

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -CheckOnly
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target codex
```

When a profile exists, the second command uses transactional `update`, retains task data, and runs first-start. Automatic update is disabled by default.

## Boundaries

- The self-contained full suite is currently verified only on Windows x64.
- This is an alpha prerelease without an independent cryptographic signature.
- Publishing the product never authorizes manuscript submission, private-data upload, payment, or external contact.
- The support surface is voluntary, unlocks no feature, and reads no payment state.

## Public repository layout

- `dist/codex/skills/paper-spine`, `dist/claude/skills/paper-spine`, and `dist/openclaw/skills/paper-spine`: host projections.
- `dist/claude/commands/paperspine.md`: Claude command entry.
- `install.ps1` and `install.sh`: installation boundaries.
- Key methods/tools: `writing_rationale_matrix`, `citation_support_bank`, `translation_package`, `artifact_check.py`, `reference_inventory.py`, `citation_bank_check.py`, `latex_guard.py`, and `word_guard.py`.

## Development

`src/` is the Skill source of truth and `dist/` contains public host projections. The public repository keeps source and tests, not local tasks, clinical data, caches, or development run logs.

MIT License.

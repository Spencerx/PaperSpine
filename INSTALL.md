# PaperSpine5 V5 installation

The V5 full suite is a Windows x64 package with a self-contained runtime. From a
fresh clone of this repository, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target codex -CleanLegacy
```

Use `-Target claude-code` or `-Target both` as appropriate. The installer verifies
the release manifest, ZIP byte count and SHA-256 before activation. It archives
the existing canonical `paper-spine` Skill and, with `-CleanLegacy`, archives
known V3/V4 discovery folders such as `PaperSpine`, `paper-spine-research` and
`paperspine5-workspace`. It does not delete task data, settings, or unknown
folders. A new host session is required after installation.

The full suite profile is stored under `%USERPROFILE%\\.paperspine5\\profiles\\default`
unless `-ProfileRoot` is provided. The embedded runtime is about 26 MB compressed;
the standalone Skill is about 0.7 MB compressed.

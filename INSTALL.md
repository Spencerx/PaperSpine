# PaperSpine5 V5 installation

PaperSpine5 publishes separate self-contained suites for Windows x64, Linux
x86_64 with glibc, Apple Silicon Macs, and Intel Macs. Do not interchange
platform packages. Every suite includes its matching Python runtime, the Web
workspace, the canonical `paper-spine` Skill, and transactional profile
update/rollback.

## Windows x64

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target codex -CleanLegacy
```

Use `-Target claude-code` or `-Target both` as appropriate.

## macOS and Linux

```sh
sh ./install.sh --target codex --clean-legacy
```

Use `--target claude-code` or `--target both` as appropriate. The installer
auto-detects the OS and CPU, downloads only the matching suite, verifies its
exact byte count and SHA-256, verifies the suite internally, installs the Skill,
activates the profile, and requires first-start REST/MCP readiness.

To check without changing the installation:

```sh
sh ./install.sh --check-only
```

To verify a previously downloaded package without downloading it again:

```sh
sh ./install.sh --bundle /path/to/platform-suite.zip --target codex --clean-legacy
```

Both installers archive the existing canonical `paper-spine` Skill. Cleanup of
known V3/V4 discovery names happens only when `-CleanLegacy` or
`--clean-legacy` is supplied. They do not delete paper task data, host settings,
or unknown folders. Restart the host after installation.

The default profile is `%USERPROFILE%\.paperspine5\profiles\default` on
Windows and `~/.paperspine5/profiles/default` on macOS/Linux. Automatic update
is disabled by default; rerunning the platform installer performs an explicit
transactional update and retains task data.

macOS packages in this prerelease are unsigned and not notarized. Linux support
is limited to glibc x86_64; Linux arm64 and musl/Alpine are not claimed.

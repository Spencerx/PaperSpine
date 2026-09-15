<p align="center"><img src="website/assets/brand/paperspine-mark.svg" width="112" alt="PaperSpine"></p>

# PaperSpine5

[English](README.en.md) · [中文](README.md) · [发布页](https://wubing2023.github.io/PaperSpine/v5/) · [GitHub Release](https://github.com/WUBING2023/PaperSpine/releases/tag/v0.4.0-alpha.1-dev)

PaperSpine5 是本地优先、证据约束的论文研究、写作、科研制图、审阅和交付工作区。唯一用户入口是 `paper-spine` Skill；Web 负责配置、选择、预览、下载和反馈，宿主 Agent 负责真实科研工作。

## 下载

- Windows x64 suite：约 26.4 MB。
- Linux glibc x86_64 suite：约 56.2 MB。
- macOS Apple Silicon suite：约 40.5 MB。
- macOS Intel x86_64 suite：约 40.5 MB。
- 独立 `paper-spine` Skill：适用于已有宿主运行环境，约 0.72 MB。

所有下载由公开 manifest 和 SHA-256 约束。完整版本号为 `v0.4.0-alpha.1-dev` prerelease。

## 安装与旧版本迁移

Windows x64：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target codex -CleanLegacy
```

macOS / Linux：

```sh
sh ./install.sh --target codex --clean-legacy
```

`-CleanLegacy` 只归档已知 V3/V4 Skill 发现目录，不删除论文任务数据、宿主设置或未知文件。两个平台安装器都会验证字节数、SHA-256、suite 内部完整性和 first-start health。

## 检查与应用更新

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File .\install.ps1 -CheckOnly
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Target codex
```

```sh
# macOS / Linux
sh ./install.sh --check-only
sh ./install.sh --target codex
```

存在 profile 时，第二条命令走事务性 `update`，保留任务数据并运行 first-start。自动更新默认关闭。

## 边界

- 自包含 suite 已在 Windows x64、Linux glibc x86_64、macOS arm64 和 macOS x86_64 验证；Linux arm64、musl/Alpine 未声明支持。
- macOS 包尚未签名或 notarize，首次运行可能需要用户明确允许。
- 当前为 alpha prerelease，无独立密码学签名。
- 产品发布不授权投稿、上传私有材料、付款或外部联系。
- 支持入口是自愿维护支持，不解锁功能，不读取支付状态。

## 公开仓库结构

- `dist/codex/skills/paper-spine`、`dist/claude/skills/paper-spine`、`dist/openclaw/skills/paper-spine`：宿主投影。
- `dist/claude/commands/paperspine.md`：Claude 命令入口。
- `install.ps1`、`install.sh`：安装边界。
- 关键方法/工具：`writing_rationale_matrix`、`citation_support_bank`、`translation_package`、`artifact_check.py`、`reference_inventory.py`、`citation_bank_check.py`、`latex_guard.py`、`word_guard.py`。

## 开发

`src/` 是 Skill 真源，`dist/` 是各宿主公开投影。公开仓库保留源代码和测试，不保留本地任务、临床数据、缓存或开发运行日志。

MIT License。

---
date created: 2024-06-13 01:08
date updated: 2026-08-05 00:00
---

# Windows 配置

## Windows 配置笔记

> Winget 管系统自带包管理和安装器类应用；Scoop 管便携应用、开发工具、字体和终端环境。

---

### Winget

#### 管理

```powershell
winget source update
winget list
winget upgrade
winget upgrade --all --include-unknown
```

---

### Scoop

#### 基础配置

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

scoop install git

scoop bucket add extras
scoop bucket add nerd-fonts
scoop bucket add games
scoop bucket add nonportable

scoop checkup
```

#### 网络工具

```powershell
scoop install sing-box aria2
scoop config aria2-warning-enabled false
```

#### 系统调试工具（可选）

```powershell
scoop install vivetool
```

#### 桌面应用

```powershell
scoop install dropbox-np obsidian notion vscode zed notepad3 everything draw.io sharex wpsoffice googlechrome
```

> `dropbox-np` 来自 nonportable bucket，可能触发 UAC 或安装到 Scoop 目录外。

#### 游戏工具

```powershell
scoop install steam epic-games-launcher
```

> Linux/Steam 游戏环境配置见 [[setup-linux|DNF + Flatpak + Steam]]

#### ROG 轻量控制工具（可选）

```powershell
scoop install windowsdesktop-runtime g-helper
```

> [G-Helper](https://github.com/seerge/g-helper) 是轻量 Armoury Crate 替代方案；需要 .NET Desktop Runtime 和 ASUS System Control Interface。ASUS System Control Interface 通常出厂已带，缺失或损坏时再从 ASUS 支持页安装。

#### 多媒体和图形工具

```powershell
scoop install obs-studio mpv ffmpeg imagemagick resvg poppler-utils
```

#### 开发工具

```powershell
scoop install rustup uv llvm
```

#### Nerd Fonts 和常用字体

```powershell
scoop install IBMPlexMono IBMPlexMono-NF IBMPlexMono-NF-Propo IBMPlexMono-NF-Mono
scoop install IBMPlexSans IBMPlexSans-Condensed IBMPlexSans-JP IBMPlexSans-KR IBMPlexSans-Thai IBMPlexSans-Thai-Looped IBMPlexSans-Arabic IBMPlexSans-Devanagari IBMPlexSans-Hebrew
scoop install IBMPlexSerif
scoop install JetBrains-Mono JetBrainsMono-NF JetBrainsMono-NF-Propo JetBrainsMono-NF-Mono
scoop install Source-Han-Sans-SC Source-Han-Sans-TC Source-Han-Sans-HC Source-Han-Sans-J Source-Han-Sans-K
scoop install Source-Han-Serif-SC Source-Han-Serif-TC Source-Han-Serif-HC Source-Han-Serif-J Source-Han-Serif-K
scoop install Source-Han-Mono-SC LXGWWenKai
```

#### PowerShell 终端配置

```powershell
scoop install pwsh posh-git terminal-icons oh-my-posh

New-Item -Path (Split-Path $PROFILE) -ItemType Directory -Force
New-Item -Path $PROFILE -ItemType File -Force
notepad3 $PROFILE
```

```powershell
$themes = @("neko", "bubbles")
$selectedTheme = Get-Random -InputObject $themes

oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\$selectedTheme.omp.json" | Invoke-Expression

Import-Module posh-git
Import-Module Terminal-Icons
```

```powershell
. $PROFILE
```

#### WezTerm 配置

```powershell
scoop install wezterm

$weztermConfig = Join-Path $env:USERPROFILE ".config\wezterm"
New-Item -Path $weztermConfig -ItemType Directory -Force
New-Item -Path (Join-Path $weztermConfig "wezterm.lua") -ItemType File -Force
notepad3 (Join-Path $weztermConfig "wezterm.lua")
```

```lua
local wezterm = require("wezterm")

local config = wezterm.config_builder()

config.color_scheme = "OneHalfDark"
config.front_end = "WebGpu"
config.enable_tab_bar = false
config.default_prog = { "pwsh.exe" }

return config
```

#### Helix 配置

```powershell
scoop install helix

$helixConfig = Join-Path $env:APPDATA "helix"
New-Item -Path $helixConfig -ItemType Directory -Force
New-Item -Path (Join-Path $helixConfig "config.toml") -ItemType File -Force
notepad3 (Join-Path $helixConfig "config.toml")
```

```toml
theme = "onedark"

[editor]
true-color = true
line-number = "relative"
mouse = true
cursorline = true
cursorcolumn = false
auto-format = true
bufferline = "never"
auto-pairs = true

[editor.statusline]
left = ["mode", "spinner", "file-name", "read-only-indicator", "file-modification-indicator"]
center = []
right = ["diagnostics", "selections", "register", "position", "file-encoding", "file-line-ending", "file-type"]
separator = "💤"
mode.normal = "🥳"
mode.insert = "🤯"
mode.select = "🤔"

[editor.lsp]
enable = true
display-messages = true
auto-signature-help = true
display-inlay-hints = true
display-signature-help-docs = true
snippets = true
goto-reference-include-declaration = true

[editor.cursor-shape]
insert = "bar"
normal = "block"
select = "underline"

[editor.file-picker]
hidden = false
follow-symlinks = true
deduplicate-links = true
parents = true
ignore = true
git-ignore = true
git-global = true
git-exclude = true

[editor.search]
smart-case = true
wrap-around = true

[editor.whitespace]
render = "none"

[editor.indent-guides]
render = false

[editor.gutters]
layout = ["diff", "diagnostics", "line-numbers", "spacer"]

[editor.gutters.line-numbers]
min-width = 3

[editor.soft-wrap]
enable = true
max-wrap = 20
max-indent-retain = 40
wrap-indicator = ""
wrap-at-text-width = false

[editor.smart-tab]
enable = true
supersede-menu = false
```

#### 高级命令

```powershell
scoop install gsudo           # sudo
scoop install btop            # top
scoop install bat             # cat
scoop install eza             # ls
scoop install fd              # find
scoop install ripgrep         # grep
scoop install procs           # ps
scoop install zoxide          # cd
scoop install duf             # df
scoop install ncdu            # du
scoop install tealdeer        # man
scoop install jq              # json
scoop install fzf             # fuzzy finder
scoop install xh              # curl
scoop install rsync           # sync
scoop install socat           # network
scoop install 7zip            # archive
scoop install yazi
```

> Windows 11 24H2 自带 `sudo`，需要更完整的提权体验时用 `gsudo`。

#### 管理

```powershell
scoop list
scoop bucket list
scoop status
scoop update
scoop update *
scoop cleanup *
scoop cache rm *
scoop checkup
```

---

## 注意事项

- GUI 应用如 VS Code、Zed、Chrome 尽量交给 Scoop 更新，不要和应用内自更新混用
- nonportable bucket 的应用可能触发 UAC，也可能写入 Scoop 目录外的位置
- G-Helper 不建议和 Armoury Crate 服务同时使用，避免互相覆盖性能、风扇、显卡、刷新率等设置

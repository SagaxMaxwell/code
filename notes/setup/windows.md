---
date created: 2024-06-13 01:08
date updated: 2026-07-13 00:00
---

# Windows 配置笔记

#### Winget 管理

```powershell
winget list
winget upgrade --all
```

#### Scoop 基础配置

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

scoop install git

scoop bucket add extras
scoop bucket add versions
scoop bucket add nerd-fonts
scoop bucket add java
scoop bucket add games
scoop bucket add nonportable
```

#### Scoop 网络工具

```powershell
scoop install sing-box
scoop install aria2
```

#### Scoop 可选系统调试工具

```powershell
scoop install vivetool
```

#### Scoop 桌面应用

```powershell
scoop install dropbox-np
scoop install obsidian
scoop install notion
scoop install vscode
scoop install zed
scoop install notepad3
scoop install everything
scoop install draw.io
scoop install snipaste
scoop install wpsoffice
scoop install googlechrome
```

#### Scoop 游戏工具

```powershell
scoop install steam
scoop install epic-games-launcher
```

#### Scoop 多媒体工具

```powershell
scoop install obs-studio
scoop install mpv
```

#### Scoop 开发工具

```powershell
scoop install rustup
rustup-init

scoop install main/uv
scoop install llvm
scoop install dotnet-sdk
scoop install dotnet-script
```

#### Scoop Nerd Fonts 和常用字体

```powershell
scoop install IBMPlexMono
scoop install IBMPlexMono-NF
scoop install IBMPlexMono-NF-Propo
scoop install IBMPlexMono-NF-Mono
scoop install IBMPlexSans
scoop install IBMPlexSans-Condensed
scoop install IBMPlexSans-JP
scoop install IBMPlexSans-KR
scoop install IBMPlexSans-Thai
scoop install IBMPlexSans-Thai-Looped
scoop install IBMPlexSans-Arabic
scoop install IBMPlexSans-Devanagari
scoop install IBMPlexSans-Hebrew
scoop install IBMPlexSerif
scoop install JetBrains-Mono
scoop install JetBrainsMono-NF
scoop install JetBrainsMono-NF-Propo
scoop install JetBrainsMono-NF-Mono
scoop install Source-Han-Sans-SC
scoop install Source-Han-Sans-TC
scoop install Source-Han-Sans-HC
scoop install Source-Han-Sans-J
scoop install Source-Han-Sans-K
scoop install Source-Han-Serif-SC
scoop install Source-Han-Serif-TC
scoop install Source-Han-Serif-HC
scoop install Source-Han-Serif-J
scoop install Source-Han-Serif-K
scoop install Source-Han-Mono-SC
scoop install LXGWWenKai
```

#### PowerShell 终端配置

```powershell
scoop install pwsh
scoop install posh-git
scoop install terminal-icons
scoop install oh-my-posh
scoop update oh-my-posh

New-Item -Path $PROFILE -Type File -Force
notepad3 $PROFILE
```

```powershell
# Define the themes
$themes = @("neko", "bubbles")

# Randomly select one theme
$selectedTheme = Get-Random -InputObject $themes

# Initialize oh-my-posh with the selected theme
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\$selectedTheme.omp.json" | Invoke-Expression

Import-Module PSReadLine
Import-Module posh-git
Import-Module -Name Terminal-Icons
```

```powershell
. $PROFILE
```

#### 终端和编辑器配置

```powershell
scoop install wezterm

mkdir -p $env:USERPROFILE\.config\wezterm
New-Item -Path $env:USERPROFILE\.config\wezterm\wezterm.lua -ItemType File
notepad3 $env:USERPROFILE\.config\wezterm\wezterm.lua
```

```lua
local wezterm = require("wezterm")

-- Build configuration
local config = wezterm.config_builder()

-- Use a fixed color scheme
config.color_scheme = "OneHalfDark"

-- Prefer GPU rendering for better performance
config.front_end = "WebGpu"

-- Disable tab bar for slightly lower overhead
config.enable_tab_bar = false
config.default_prog = { "pwsh.exe" }

-- Return the configuration to wezterm
return config
```

```powershell
scoop install helix

New-Item -Path $env:USERPROFILE\AppData\Roaming\helix\config.toml -Type File -Force
notepad3 $env:USERPROFILE\AppData\Roaming\helix\config.toml
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

#### Scoop 高级命令

```powershell
scoop install sudo            # sudo
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
scoop install ffmpeg          # media
scoop install resvg           # svg
scoop install imagemagick     # image
scoop install poppler-utils   # pdf
scoop install 7zip            # archive
scoop install yazi
```

#### Scoop 管理

```powershell
scoop list
scoop bucket list
scoop status
scoop update *
scoop cleanup *
```

---
date created: 2024-06-13 01:08
date updated: 2026-05-08 23:53
---

# Windows 配置笔记

#### 安装 DotNet

```bash
winget search Microsoft.DotNet
winget install --id Microsoft.DotNet.SDK.8
winget install --id Microsoft.DotNet.Runtime.8
winget install --id Microsoft.DotNet.HostingBundle.8
winget install --id Microsoft.DotNet.Framework.DeveloperPack_4
winget install --id Microsoft.DotNet.DesktopRuntime.8
winget install --id Microsoft.DotNet.AspNetCore.8
```

#### 安装 EADesktop

```bash
winget install --id ElectronicArts.EADesktop
```

#### Winget 查看软件列表

```bash
winget list
```

#### Winget 更新软件

```bash
winget upgrade --all
```

#### 安装 Scoop

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
iex "& {$(irm get.scoop.sh)} -RunAsAdmin" 
```

#### 安装 Git

```bash
scoop install git
```

#### 添加 Bucket

```bash
scoop bucket add extras
scoop bucket add versions
scoop bucket add nerd-fonts
scoop bucket add java
scoop bucket add games
scoop bucket add nonportable
```

#### 安装 Aria2

```bash
scoop install aria2
```

#### 安装 Vivetool

```bash
scoop install vivetool
```

#### 安装 Dropbox

```bash
scoop install dropbox-np
```

#### 安装 Obsidian

```bash
scoop install obsidian
```

#### 安装 Notion

```bash
scoop install notion
```

#### 安装 VisualStudioCode

```bash
scoop install vscode
```

#### 安装 Zed Nightly

```bash
scoop install zed-nightly
```

#### 安装 Notepad3

```bash
scoop install notepad3
```

#### 安装 JDK

```bash
scoop install openjdk
```

#### 安装 Rustup

```bash
# install
scoop install rustup

# choice version
rustup install stable
rustup install beta
rustup install nightly

# add component
rustup component add rustfmt-preview
rustup component add rls-preview
rustup component add clippy-preview
rustup component add rust-src
rustup component list

# set default toolchain
rustup install stable-x86_64-pc-windows-gnu
rustup set default-host x86_64-pc-windows-gnu
rustup default stable-x86_64-pc-windows-gnu
rustup show

# cross compile
cargo install cross

# update
rustup update

# delete path
rustup show
rustup uninstall nightly
rustup uninstall beta
rustup uninstall stable
rm ~/.rustup
rm ~/.cargo
```

#### 安装 Node

```bash
scoop install nodejs
```

#### 安装 Python

```bash
scoop install python
```

#### 安装 Gcc

```bash
scoop install gcc
```

#### 安装 DotNet

```bash
scoop install dotnet-sdk
scoop install dotnet-script
```

#### 安装 IBMPlex

```bash
scoop install IBMPlexMono
scoop install IBMPlexMono-NF
scoop install IBMPlexMono-NF-Propo
scoop install IBMPlexMono-NF-Mono
scoop install IBMPlexSans
scoop install IBMPlexSerif
```

#### 安装 SourceCodePro

```bash
scoop install SourceCodePro-NF-Mono
scoop install SourceCodePro-NF-Propo
scoop install SourceCodePro-NF
```

#### 安装 PWSH

```bash
scoop install pwsh
```

#### 安装 PSReadLine

```bash
scoop install PSReadLine
```

#### 安装 Posh-git

```bash
scoop install posh-git
Add-PoshGitToProfile -Force
```

#### 安装 Terminal-icons

```bash
scoop install terminal-icons
```

#### 安装 Oh-my-posh

```bash
scoop install oh-my-posh
scoop update oh-my-posh

# 编辑当前终端配置
New-Item -Path $PROFILE -Type File -Force
notepad3 $PROFILE

%%
# Define the themes
$themes = @("neko", "bubbles")

# Randomly select one theme
$selectedTheme = Get-Random -InputObject $themes

# Initialize oh-my-posh with the selected theme
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\$selectedTheme.omp.json" | Invoke-Expression

Import-Module PSReadLine
Import-Module posh-git
Import-Module -Name Terminal-Icons
%%

. $PROFILE
```

#### 安装 Wezterm

```bash
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

-- Prefer GPU rendering for better performance (macOS)
config.front_end = "WebGpu"

-- Disable tab bar for slightly lower overhead
config.enable_tab_bar = false

config.default_prog = { "pwsh.exe" }
config.default_cursor_style = "BlinkingUnderline"
config.cursor_blink_rate = 500
config.enable_tab_bar = false
config.use_fancy_tab_bar = false
config.color_scheme = color_scheme

-- Return the configuration to wezterm
return config
```

#### 安装 Helix

```bash
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

#### 安装 Everything

```bash
scoop install everything
```

#### 安装 Draw IO

```bash
scoop install draw.io
```

#### 安装 Snipaste

```bash
scoop install snipaste
```

#### 安装 WPS Office

```bash
scoop install wpsoffice
```

#### 安装 WeChat

```bash
scoop install wechat
```

#### 安装 GoogleChrome

```bash
scoop install googlechrome
```

#### 安装 Steam

```bash
scoop install steam
```

#### 安装 Epic-games-launcher

```bash
scoop install epic-games-launcher
```

#### 安装高级命令

```zsh
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
scoop install poppler-utils   # pdf
scoop install 7zip            # archive
scoop install yazi
```

#### Scoop 查看软件列表

```bash
scoop list
```

#### Scoop 查看源列表

```bash
scoop bucket list
```

#### Scoop 更新软件

```bash
scoop status
scoop update *
```

#### Scoop 删除旧版本

```bash
scoop cleanup *
```

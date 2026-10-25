---
date created: 2024-05-02 14:29
date updated: 2026-08-05 00:00
---

# Linux 配置


> Fedora 用 DNF 管系统层、驱动、硬件控制和命令行工具；Flatpak 管桌面应用、Steam 与游戏工具；SteamOS 只记录 Steam 游戏模式和掌机场景专用配置。

---

## DNF

### 基础配置

```zsh
sudo dnf install -y dnf5-plugins
sudo dnf config-manager setopt max_parallel_downloads=10

sudo dnf upgrade --refresh -y
reboot
```

### RPM Fusion

```zsh
sudo dnf install -y \
  https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

sudo dnf upgrade --refresh -y
```

> 不再单独启用 `fedora-cisco-openh264`，主线以 RPM Fusion + FFmpeg 为准；OpenH264 只在 Firefox/WebRTC 场景按需处理。

### 固件、多媒体和图形测试

```zsh
fwupdmgr refresh --force
fwupdmgr get-updates
fwupdmgr update

sudo dnf swap ffmpeg-free ffmpeg --allowerasing
sudo dnf group install multimedia --with-optional
sudo dnf install -y vainfo mesa-demos vulkan-tools
```

### NVIDIA 驱动（可选）

```zsh
sudo dnf install -y akmod-nvidia xorg-x11-drv-nvidia-cuda
```

### Intel GPU 工具（可选）

```zsh
sudo dnf install -y intel-gpu-tools
```

### ROG 轻量控制工具（ASUS Linux/Terra，可选）

> Fedora 旧的 `lukenukem/asus-linux` COPR 已不维护；Fedora 现在用 Terra repo 发布 `asusctl` 和 `asusctl-rog-gui`。`asusctl` 是命令行和后端控制工具，`asusctl-rog-gui` 是图形界面；需要 dGPU 热切换时再评估 Cardwire。

```zsh
# 仅旧 COPR 用户需要先移除旧仓库。
sudo dnf copr remove lukenukem/asus-linux

sudo dnf install --nogpgcheck --repofrompath 'terra,https://repos.fyralabs.com/terra$releasever' terra-release
sudo dnf install -y asusctl asusctl-rog-gui

sudo dnf swap tuned-ppd power-profiles-daemon --allowerasing
sudo systemctl enable --now asusd.service power-profiles-daemon.service

asusctl armoury list
```

### 掌机 HHD 控制（Fedora/COPR，可选）

> Fedora 下的掌机控制层，用于手柄映射、TDP/性能配置和 RGB。`openrgb` 不放在 HHD 主流程里，需要单独调灯效时再装。

```zsh
sudo dnf copr enable hhd-dev/hhd
sudo dnf install -y hhd adjustor hhd-ui

sudo systemctl enable --now hhd@$USER
systemctl status hhd@$USER
```

### GNOME 工具

```zsh
sudo dnf install -y gnome-software-plugin-flatpak
sudo dnf install -y gnome-shell-extension-appindicator
```

### 输入法

```zsh
sudo dnf install -y fcitx5 fcitx5-chinese-addons fcitx5-configtool fcitx5-autostart fcitx5-gtk fcitx5-qt

reboot
fcitx5-configtool
```

### 网络工具

```zsh
sudo dnf config-manager addrepo --from-repofile=https://sing-box.app/sing-box.repo
sudo dnf install -y sing-box
```

### 开发和终端工具

```zsh
sudo dnf install -y openssl-devel openssl git rustup clang uv helix
rustup-init

mkdir -p ~/.config/helix
gnome-text-editor ~/.config/helix/config.toml
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

### Nerd Fonts 和常用字体

```zsh
sudo dnf install -y ibm-plex-fonts-all jetbrains-mono-fonts adobe-source-sans-pro-fonts adobe-source-serif-pro-fonts adobe-source-code-pro-fonts
sudo dnf install -y adobe-source-han-sans-cn-fonts adobe-source-han-sans-jp-fonts adobe-source-han-sans-kr-fonts adobe-source-han-sans-tw-fonts
sudo dnf install -y adobe-source-han-serif-cn-fonts adobe-source-han-serif-jp-fonts adobe-source-han-serif-kr-fonts adobe-source-han-serif-tw-fonts
sudo dnf install -y adobe-source-han-mono-fonts texlive-lxgw-fonts

fc-cache -fv
```

### 高级命令

```zsh
sudo dnf install -y btop            # top
sudo dnf install -y bat             # cat
sudo dnf install -y eza             # ls
sudo dnf install -y fd              # find
sudo dnf install -y ripgrep         # grep
sudo dnf install -y procs           # ps
sudo dnf install -y zoxide          # cd
sudo dnf install -y duf             # df
sudo dnf install -y ncdu            # du
sudo dnf install -y tealdeer        # man
sudo dnf install -y jq              # json
sudo dnf install -y fzf             # fuzzy finder
sudo dnf install -y xh              # curl
sudo dnf install -y wl-clipboard    # clipboard
sudo dnf install -y rsync           # sync
sudo dnf install -y iproute2        # ip/ss
sudo dnf install -y socat           # network
sudo dnf install -y poppler-utils   # pdf
sudo dnf install -y 7zip            # archive
```

### 终端文件管理器（COPR）

```zsh
sudo dnf copr enable lihaohong/yazi
sudo dnf install -y yazi
```

### 清理

```zsh
sudo dnf autoremove
sudo dnf remove --oldinstallonly
```

---

## Flatpak

### 基础配置

```zsh
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak remote-modify --enable flathub
```

### 输入法权限

```zsh
flatpak override --user --filesystem=xdg-run/fcitx
```

### GNOME 和管理工具

```zsh
flatpak install -y flathub org.gnome.Tweaks com.mattjakeman.ExtensionManager com.github.tchx84.Flatseal io.github.flattool.Warehouse
```

### Steam 和游戏工具

```zsh
flatpak install -y flathub com.vysp3r.ProtonPlus com.valvesoftware.Steam com.heroicgameslauncher.hgl
```

### 多媒体工具

```zsh
flatpak install -y flathub com.obsproject.Studio com.dec05eba.gpu_screen_recorder io.mpv.Mpv
```

### 桌面应用

```zsh
flatpak install -y flathub com.google.Chrome md.obsidian.Obsidian com.wps.Office com.jgraph.drawio.desktop org.flameshot.Flameshot
```

> Chrome Flatpak 是 Flathub wrapper，不是 Google 官方发布。

### 开发和桌面终端工具

```zsh
flatpak install -y flathub dev.zed.Zed com.visualstudio.code com.mitchellh.ghostty
```

> Visual Studio Code 和 Zed 的 Flatpak 是社区 wrapper，不是上游官方支持版本。

### 更新和清理

```zsh
flatpak update
flatpak uninstall --unused
```

---

## SteamOS

### 基础原则

> SteamOS 使用 Flatpak 管理普通应用；不要把 Fedora 的 DNF/COPR 流程照搬到 SteamOS。  
> Decky 插件安装不需要默认关闭只读系统。

### 只读系统

```zsh
steamos-readonly status

steamos-readonly disable
steamos-readonly enable
```

### 输入设备服务

```zsh
sudo systemctl enable --now inputplumber.service
sudo systemctl enable --now inputplumber-suspend.service
```

### 游戏模式设置

> 安装 SteamOS 后，先用热点连接，再安装软件。  
> 陀螺仪设备大概率识别不到。  
> 显示和游戏模式设置：禁用帧率限制、禁用垂直同步、启用强制合成、启用 gamescope 合成、启用 CEF 调试、系统缩放设置 150%。

### Decky 插件

```zsh
curl -L -o /tmp/decky-loader-install.sh https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh
less /tmp/decky-loader-install.sh
sh /tmp/decky-loader-install.sh
```

> Decky-Loader 启用开发者模式、CEF 远程调试。  
> Decky LSFG-VK 启用 Performance Mode、WSI。  
> 常用插件：Decky Clash、Decky-Undervolt、Pause Games、Decky-Framegen、Colores。

---

## 注意事项

- GNOME 下虚拟键盘无法正确填充界面
- Intel CPU 功耗只能通过命令行设置
- Intel GPU 在 Linux 下没有对应调整功耗的驱动
- DNF/COPR 的 ROG 和 HHD 配置是 Fedora 系统层方案，不直接照搬到 SteamOS
- Flatpak 应用使用自己的运行时和沙箱权限，系统层 codec、输入法和驱动配置不一定自动传进沙箱

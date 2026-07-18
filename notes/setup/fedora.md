---
date created: 2024-05-02 14:29
date updated: 2026-07-13 00:00
---

# Fedora 配置笔记

#### DNF 基础配置

```zsh
gnome-text-editor /etc/dnf/dnf.conf
```

```ascii
[main]
max_parallel_downloads=10
```

```zsh
dnf upgrade --refresh -y
dnf install -y gnome-software-plugin-flatpak # 非 Workstation/GNOME Software 默认环境需要
reboot

dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
dnf config-manager setopt fedora-cisco-openh264.enabled=1
dnf upgrade --refresh -y
```

#### DNF 固件和多媒体

```zsh
fwupdmgr refresh --force
fwupdmgr get-updates
fwupdmgr update

dnf group install multimedia --with-optional
dnf swap ffmpeg-free ffmpeg --allowerasing
dnf install -y vainfo mesa-demos vulkan-tools
```

#### DNF NVIDIA 驱动（可选）

```zsh
dnf install -y akmod-nvidia xorg-x11-drv-nvidia-cuda
```

#### DNF Intel GPU 工具（可选）

```zsh
dnf install -y intel-gpu-tools
```

#### DNF 硬件管理

```zsh
dnf copr enable lukenukem/asus-linux
dnf install -y asusctl supergfxd rog-gui

systemctl enable --now asusd.service supergfxd.service

supergfxctl -s
supergfxctl -g

dnf copr enable hhd-dev/hhd
dnf install -y adjustor hhd hhd-ui openrgb

systemctl enable --now hhd@$USER
systemctl status hhd@$USER
```

> 尝试不安装 HHD
> 如重复安装 HHD 后需要删除旧设备映射
> Linux 下的 powersave 就是指 intel_pastate active
> tuned(Linux)、thermald(Intel)、asusctl(ROG) 工具最现代，降压技术已过时

#### DNF GNOME 工具

```zsh
dnf install -y gnome-shell-extension-appindicator # 可选托盘图标兼容
```

#### SteamOS 基础配置（专用场景）

```zsh
steamos-readonly disable
steamos-readonly status

systemctl enable inputplumber.service
systemctl enable inputplumber-suspend.service
```

> [SteamOS](https://steamdeck-images.steamos.cloud/steamdeck/) 使用 Flatpak 现代方式管理软件
> 安装 SteamOS 后，先用热点连接，再安装软件
> 陀螺仪设备大概率识别不到
> Xess 技术大概率不能使用
> 禁用帧率限制
> 禁用垂直同步
> 启用强制合成
> 启用 gamescope 合成
> 启用 CEF 调试

#### SteamOS 插件（专用场景）

```zsh
curl -L -o /tmp/decky-loader-install.sh https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh
less /tmp/decky-loader-install.sh
sh /tmp/decky-loader-install.sh

curl -L -o /tmp/simpledeckytdp-install.sh https://github.com/aarron-lee/SimpleDeckyTDP/raw/main/install.sh
less /tmp/simpledeckytdp-install.sh
sh /tmp/simpledeckytdp-install.sh
```

> Decky-Loader 启用开发者模式
> Decky-Loader 启用 CEF 远程调试
> Decky LSFG-VK，启用 Performance Mode、WSI、MangoHud Workaround，根据硬件决定是否开启 HDR Mode、vkBasalt，其余选项禁用
> Decky Clash
> Decky-Undervolt
> Fantastic
> Pause Games
> Speed Test
> Decky-Framegen

#### DNF 输入法

```zsh
sudo dnf install -y fcitx5 fcitx5-chinese-addons fcitx5-configtool fcitx5-autostart fcitx5-gtk fcitx5-qt
flatpak override --user --filesystem=xdg-run/fcitx

reboot
fcitx5-configtool
```

#### DNF 网络工具

```zsh
dnf config-manager addrepo --from-repofile=https://sing-box.app/sing-box.repo
dnf install -y sing-box
```

#### DNF 开发和终端工具

```zsh
dnf install -y openssl-devel openssl git rustup clang uv helix
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

#### DNF Nerd Fonts 和常用字体

```zsh
dnf install -y ibm-plex-fonts-all jetbrains-mono-fonts adobe-source-sans-pro-fonts adobe-source-serif-pro-fonts adobe-source-code-pro-fonts
dnf install -y adobe-source-han-sans-cn-fonts adobe-source-han-sans-jp-fonts adobe-source-han-sans-kr-fonts adobe-source-han-sans-tw-fonts
dnf install -y adobe-source-han-serif-cn-fonts adobe-source-han-serif-jp-fonts adobe-source-han-serif-kr-fonts adobe-source-han-serif-tw-fonts
dnf install -y adobe-source-han-mono-fonts texlive-lxgw-fonts

fc-cache -fv
```

#### DNF 高级命令

```zsh
dnf install -y btop            # top
dnf install -y bat             # cat
dnf install -y eza             # ls
dnf install -y fd              # find
dnf install -y ripgrep         # grep
dnf install -y procs           # ps
dnf install -y zoxide          # cd
dnf install -y duf             # df
dnf install -y ncdu            # du
dnf install -y tealdeer        # man
dnf install -y jq              # json
dnf install -y fzf             # fuzzy finder
dnf install -y xh              # curl
dnf install -y wl-clipboard    # clipboard
dnf install -y rsync           # sync
dnf install -y iproute2        # ip/ss
dnf install -y socat           # network
dnf install -y poppler-utils   # pdf
dnf install -y 7zip            # archive
```

#### DNF 终端文件管理器（COPR）

```zsh
dnf install -y dnf-plugins-core # 如 dnf copr 不可用
dnf copr enable lihaohong/yazi
dnf install -y yazi
```

#### DNF 清理

```zsh
dnf autoremove
```

#### DNF 旧内核清理（可选）

```zsh
dnf remove --oldinstallonly
```

#### Flatpak 基础配置

```zsh
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak remote-modify --enable flathub
```

#### Flatpak GNOME 和管理工具

```zsh
flatpak install -y flathub org.gnome.Tweaks com.mattjakeman.ExtensionManager com.github.tchx84.Flatseal io.github.flattool.Warehouse
```

#### Flatpak 游戏工具

```zsh
flatpak install -y flathub com.vysp3r.ProtonPlus com.valvesoftware.Steam com.heroicgameslauncher.hgl
```

#### Flatpak 多媒体工具

```zsh
flatpak install -y flathub com.obsproject.Studio com.dec05eba.gpu_screen_recorder io.mpv.Mpv
```

#### Flatpak 桌面应用

```zsh
flatpak install -y flathub com.google.Chrome md.obsidian.Obsidian com.wps.Office com.jgraph.drawio.desktop org.flameshot.Flameshot
```

> Chrome Flatpak 是 Flathub wrapper，不是 Google 官方发布。

#### Flatpak 开发和桌面终端工具

```zsh
flatpak install -y flathub dev.zed.Zed com.visualstudio.code com.mitchellh.ghostty
```

> Visual Studio Code 和 Zed 的 Flatpak 是社区 wrapper，不是上游官方支持版本。

#### Flatpak 更新

```zsh
flatpak update --appstream
flatpak update
```

#### 注意事项

- Gnome 下虚拟键盘无法正确填充界面
- Intel CPU 功耗只能通过命令行设置
- Intel GPU 在 Linux 下没有对应调整功耗的驱动

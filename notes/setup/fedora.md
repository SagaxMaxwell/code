---
date created: 2024-05-02 14:29
date updated: 2026-05-08 23:53
---

# Fedora 配置笔记

#### 配置 DNF5

```zsh
gnome-text-editor /etc/dnf/dnf.conf
```

```ascii
[main]
max_parallel_downloads=10
fastestmirror=True
keepcache=True
```

```
```zsh
dnf upgrade --refresh -y
dnf install gnome-software-plugin-flatpak
reboot

dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
dnf install -y https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
dnf config-manager setopt fedora-cisco-openh264.enabled=1
dnf upgrade --refresh -y
```

#### 更新固件 + 驱动

```zsh
fwupdmgr refresh --force 
fwupdmgr get-updates 
fwupdmgr update
dnf group install multimedia --with-optional
dnf swap ffmpeg-free ffmpeg --allowerasing
dnf install vainfo
dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda
dnf install mesa-demos vulkan-tools intel-gpu-tools
reboot
nvidia-smi
vainfo
lspci -k | grep -A3 -E "VGA|Display"
glxinfo -B
vulkaninfo --summary
```

#### 安装 ASUS 套件

```zsh
dnf copr enable lukenukem/asus-linux
dnf install asusctl supergfxd rog-gui
systemctl enable --now asusd.service supergfxd.service

supergfxctl -s
supergfxctl -g
```

> 如果 ROG-Control-GUI GPU 的模式下拉框置灰，说明不允许修改

#### 安装 HHD

```zsh
dnf copr enable hhd-dev/hhd
dnf install adjustor hhd hhd-ui

systemctl enable --now hhd@$USER
systemctl status hhd@$USER
```

> 尝试不安装 HHD
> 如重复安装 HHD 后需要删除旧设备映射
> Linux 下的 powersave 就是指 intel_pastate active
> tuned(Linux)、thermald(Intel)、asusctl(ROG) 工具最现代，降压技术已过时

#### SteamOS

```zsh
steamos-readonly disable
starmos-readonly status

systemctl enable inputplumber.service
systemctl enable inputplumber-suspend.service
```

> [SteamOS](https://steamdeck-images.steamos.cloud/steamdeck/)
> SteamOS 使用 Flatpak 现代方式管理软件
> 安装 SteamOS 后，先用热点连接，再安装软件
> 陀螺仪设备大概率识别不到
> Xess 技术大概率不能使用
> 禁用帧率限制
> 禁用垂直同步
> 启用强制合成
> 启用 gamescope 合成
> 启用 CEF 调试

#### 安装 Decky-loader

```zsh
curl -L https://www.mhhf.com/Deck/install.sh | sh
curl -L https://github.com/aarron-lee/SimpleDeckyTDP/raw/main/install.sh | sh
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

#### 配置 Fcitx5

```zsh
sudo dnf install fcitx5 fcitx5-chinese-addons fcitx5-configtool fcitx5-autostart fcitx5-gtk fcitx5-qt gnome-shell-extension-appindicator
flatpak override --user --filesystem=xdg-run/fcitx

mkdir -p ~/.config/environment.d 
cat << 'EOF' > ~/.config/environment.d/fcitx5.conf
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS=@im=fcitx
EOF

reboot
fcitx5-configtool
```

#### 安装 OpenSSL

```zsh
dnf install openssl-devel
dnf install openssl
```

#### 配置 SSH

```zsh
cd ~
ssh-keygen -t ed25519
```

#### 安装 Powerline-fonts

```zsh
dnf install powerline-fonts
fc-cache -fv
```

#### 安装 IBMPlex

```zsh
dnf install ibm-plex-mono-fonts
dnf install ibm-plex-sans-fonts
dnf install ibm-plex-serif-fonts
fc-cache -fv
```

#### 安装高级命令

```zsh
dnf install btop            # top
dnf install bat             # cat
dnf install eza             # ls
dnf install fd              # find
dnf install ripgrep         # grep
dnf install procs           # ps
dnf install zoxide          # cd
dnf install duf             # df
dnf install ncdu            # du
dnf install tealdeer        # man
dnf install jq              # json
dnf install fzf             # fuzzy finder
dnf install xh              # curl
dnf install wl-clipboard    # clipboard
dnf install rsync           # sync
dnf install iproute2        # ip/ss
dnf install socat           # network
dnf install poppler-utils   # pdf
dnf install 7zip            # archive
```

#### 删除旧内核

```zsh
dnf remove --oldinstallonly
```

#### 删除无用依赖

```zsh
dnf autoremove
```

#### 配置 Flatpak

```zsh
flatpak remote-modify --enable flathub
```

#### 安装插件管理程序

```zsh
flatpak install flathub org.gnome.Tweaks
flatpak install flathub com.mattjakeman.ExtensionManager
```

#### 安装 ProtonPlus

```zsh
flatpak install flathub com.vysp3r.ProtonPlus
```

#### 安装 RGB

```zsh
flatpak install flathub org.openrgb.OpenRGB
flatpak run org.openrgb.OpenRGB
```

#### 安装 Flatseal

```zsh
flatpak install flathub com.github.tchx84.Flatseal
```

#### 安装 Warehouse

```zsh
flatpak install flathub io.github.flattool.Warehouse
```

#### 安装 OBS

```zsh
flatpak install flathub com.obsproject.Studio
```

#### 安装 GPU Screen Recorder

```zsh
flatpak install flathub io.github.dec05eba.gpu_screen_recorder
```

#### 安装 MPV

```zsh
flatpak install flathub io.mpv.Mpv
```

#### 安装 GoogleChrome

```zsh
flatpak install flathub com.google.Chrome
flatpak run com.google.Chrome
```

#### 安装 Obsidian

```zsh
flatpak install flathub md.obsidian.Obsidian
flatpak run md.obsidian.Obsidian
```

#### 安装 Steam

```zsh
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.valvesoftware.Steam
flatpak run com.valvesoftware.Steam
```

#### 安装 WPSOffice

```zsh
flatpak install flathub com.wps.Office
flatpak run com.wps.Office
```

#### 安装 VisualStudioCode

```zsh
flatpak install flathub com.visualstudio.code
flatpak run com.visualstudio.code
```

#### 安装 Dropbox

```zsh
flatpak install flathub com.dropbox.Client
flatpak run com.dropbox.Client
```

#### 安装 Yazi

```zsh
flatpak install flathub io.github.sxyazi.yazi
flatpak run io.github.sxyazi.yazi
```

#### 安装 Helix

```zsh
flatpak install flathub com.helix_editor.Helix
flatpak run com.helix_editor.Helix
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

#### 安装 WezTerm

```zsh
flatpak install flathub org.wezfurlong.wezterm
flatpak run org.wezfurlong.wezterm

mkdir -p ~/.config/wezterm
touch ~/.config/wezterm/wezterm.lua
gnome-text-editor ~/.config/wezterm/wezterm.lua
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

-- Return configuration
return config
```

#### 注意事项

- Gnome 下虚拟键盘无法正确填充界面
- Intel CPU 功耗只能通过命令行设置
- Intel GPU 在 Linux 下没有对应调整功耗的驱动


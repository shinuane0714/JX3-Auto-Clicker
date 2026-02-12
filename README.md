# macOS 智能连点器 🖱️⌨️

一款专为 macOS 设计的智能连点/按键工具，支持全局快捷键控制，特别适合剑网3等游戏场景。

![Platform](https://img.shields.io/badge/platform-macOS-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ 功能特性

- 🎮 **智能窗口识别**：仅在指定应用程序处于前台时触发连点
- ⌨️ **全局快捷键**：即使在游戏中也能通过 F9/F10 启停（可自定义）
- 🖱️ **双模式支持**：鼠标连点 / 键盘按键连点
- 🎯 **精准控制**：可调节点击间隔（最低 0.01 秒）
- 🔇 **静默运行**：无 Dock 图标，不干扰游戏

## 📦 下载安装

### 方式一：直接下载（推荐）

1. 前往 [Releases](../../releases) 页面
2. 下载最新版本的 `连点器.app.zip`
3. 解压后将 `连点器.app` 拖入「应用程序」文件夹
4. 首次运行时需右键点击选择「打开」

### 方式二：从源码构建

```bash
# 克隆仓库
git clone https://github.com/shinuane0714/auto-clicker.git
cd auto-clicker

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install flask flask-cors pynput pywebview pyinstaller pyobjc

# 打包应用
pyinstaller autoclicker.spec --clean

# 应用程序将生成在 dist/连点器.app
```

## 🔧 使用方法

1. 双击打开 `连点器.app`
2. 设置目标软件（如「剑网3无界」）
3. 选择连点模式（鼠标/键盘）
4. 设置点击间隔
5. 点击「开始运行」或使用快捷键 F9 启动
6. 使用 F10 停止

### 默认快捷键

| 功能 | 快捷键 |
|------|--------|
| 启动连点 | F9 |
| 停止连点 | F10 |

> 💡 快捷键可在界面中自定义

## ⚠️ 权限设置

首次使用需要授予以下权限：

1. **辅助功能权限**（必需）
   - 系统设置 → 隐私与安全性 → 辅助功能
   - 添加并启用「连点器」

2. **输入监控权限**（必需）
   - 系统设置 → 隐私与安全性 → 输入监控
   - 添加并启用「连点器」

## 🎮 针对剑网3优化

- 默认配置已针对剑网3优化，也可以自己选择需要的软件（未测试其他软件）
- 支持在游戏内使用自定义按键（默认为 F9/F10）全局后台控制

## 🛠️ 技术栈

- **后端**: Python + Flask
- **前端**: HTML + CSS + JavaScript  
- **键鼠控制**: pynput
- **窗口管理**: PyObjC (AppKit)
- **打包**: PyInstaller + pywebview

## 📄 开源协议

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

Made with ❤️ for macOS gamers

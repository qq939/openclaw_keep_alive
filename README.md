# KeepAliveControl

本项目用于确保 OpenClaw Gateway 和 ComfyUI 在 Windows 环境下长期稳定运行，提供自动监控、重启与远程控制功能。

---

## 1. OpenClaw Gateway

### 1.1 什么是 OpenClaw？

OpenClaw 是一个基于 Node.js 的网关服务，提供 AI Agent 的核心调度能力。

### 1.2 启动原理

当检测到 OpenClaw Gateway 进程（包含 `openclaw gateway` 或 `openclaw index.js` 的 node.exe）未运行时：

1. 脚本尝试通过 `%APPDATA%\npm\openclaw.cmd gateway` 直接启动。
2. 若启动失败，则执行 `openclaw doctor --fix` 进行自我修复。
3. 修复后再次尝试启动。
4. 所有操作以 **隐藏窗口** 模式运行，不弹窗干扰用户。

---

## 2. ComfyUI

### 2.1 什么是 ComfyUI？

ComfyUI 是一个基于 Python 的 AI 绘画工作流界面。

### 2.2 启动原理

当检测到 ComfyUI 进程（路径包含 `ComfyUI` 或命令行包含 `main.py --listen` 的 python.exe）未运行时：

1. 脚本尝试通过 `F:\ComfyUI\run.bat` 启动 ComfyUI。
2. 以 **隐藏窗口** 模式运行批处理文件。

---

## 3. 控制开关 (Keep-Alive Switch)

### 3.1 Web 控制面板

访问 `http://localhost:7861` 查看控制面板：

| 路由 | 功能 |
|------|------|
| `/` | 显示当前状态及操作链接 |
| `/on` | 开启保活 (自动重启功能启用) |
| `/off` | 关闭保活 (仅监控，不重启) |
| `/toggle` | 切换开/关状态 |
| `/status` | 返回原始状态 (`on` 或 `off`) |

### 3.2 工作机制

1. **控制中心 (Docker/Flask)**：在端口 `7861` (内部 8079) 运行一个 Web 服务，存储当前保活状态 (`on`/`off`)。
2. **监控脚本 (PowerShell)**：每 60 秒检查一次 `/status` API：
   - 若返回 `on`：执行进程检测与自动重启。
   - 若返回 `off`：仅记录状态，不执行任何操作。

---

## 4. 快速启动

### 4.1 启动控制中心 (Docker)

```bash
docker-compose up -d
# 访问 http://localhost:7861 查看状态
```

### 4.2 启动监控脚本 (Windows)

双击 `OpenClaw_Launcher.vbs`，或者在 PowerShell 中执行：

```powershell
powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File OpenClaw_KeepAlive.ps1
```

---

## 5. 文件结构

| 文件 | 说明 |
|------|------|
| `app.py` | Flask 控制中心源码 |
| `OpenClaw_KeepAlive.ps1` | PowerShell 监控脚本 |
| `OpenClaw_Launcher.vbs` | VBS 隐藏启动器 |
| `Dockerfile` | 控制中心容器镜像 |
| `docker-compose.yml` | 容器编排配置 |
| `REQUIREMENTS.md` | 完整需求文档 |
| `OpenClaw_KeepAlive.log` | 监控日志 |

---

## 6. 日志

所有监控和重启操作会记录到 `OpenClaw_KeepAlive.log`，格式如下：

```
[ 2026-03-05 05:15:35 ] OpenClaw Gateway NOT running. Attempting to start...
[ 2026-03-05 05:15:40 ] Status Check: Keep-Alive is ON
```
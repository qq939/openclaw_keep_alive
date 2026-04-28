# 项目需求文档 (KeepAliveControl)

## 1. 项目背景
在长期运行 OpenClaw (openclaw gateway) 和 ComfyUI (F:\ComfyUI\run.bat) 时，这些进程可能会因为内存泄漏、系统资源不足或其他不可预见的错误而意外退出。本项目旨在提供一个自动化的保活 (Keep-Alive) 机制，确保这些核心服务在崩溃后能够自动重启，并提供远程控制开关。

## 2. 核心功能需求

### 2.1 服务自动监控与重启 (Backend)
- **监控对象**：
  - **OpenClaw Gateway**：监控 node.js 进程中包含 `openclaw` 关键字的进程。
  - **ComfyUI**：监控包含 `ComfyUI` 路径或 `F:\ComfyUI\run.bat` 参数的 python 进程。
- **自动修复**：
  - 若检测到服务未运行，应自动后台静默启动。
  - 对于 OpenClaw，若直接启动失败，应尝试执行 `openclaw doctor --fix` 进行自我修复后再尝试启动。
- **静默运行**：
  - 所有启动操作必须以隐藏窗口模式运行，不干扰用户当前桌面操作。

### 2.2 远程控制中心 (Web Control)
- **状态管理**：
  - 提供一个基于 Flask 的 Web 服务。
  - 支持通过 Web API (`/on`, `/off`, `/toggle`) 控制保活机制的开启与关闭。
- **开关逻辑**：
  - 当保活开关为 `OFF` 时，后端监控脚本仅检查状态，不执行重启操作。
  - 默认为 `ON` 状态。

### 2.3 系统集成与部署
- **容器化部署**：控制中心通过 Docker 部署，确保环境隔离和跨平台一致性。
- **本地化执行**：监控脚本在 Windows 环境下通过 PowerShell 运行，直接操作本地进程。
- **无感启动**：提供 VBS 启动脚本，实现 PowerShell 监控脚本的开机自启或静默启动。

## 3. 技术栈
- **后端监控**：PowerShell 5.1+ (Windows Management Instrumentation)
- **控制中心**：Python 3.9 + Flask
- **部署方案**：Docker / Docker Compose
- **脚本封装**：VBScript (用于 Windows 隐藏启动)

## 4. 接口定义 (Web API)
- `GET /`：显示当前状态及控制链接。
- `GET /status`：返回原始状态字符串 (`on` 或 `off`)。
- `GET/POST /on`：开启保活机制。
- `GET/POST /off`：关闭保活机制。
- `GET/POST /toggle`：切换当前状态。

## 5. 约束与安全
- **网络访问**：控制中心容器内部端口 `8079` 映射至宿主机 `7861` 端口。
- **日志记录**：监控脚本需记录所有检查记录及重启操作至 `OpenClaw_KeepAlive.log`。
- **资源消耗**：监控频率设定为 60 秒/次，以平衡实时性与 CPU 占用。

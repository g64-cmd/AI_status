# AI Project Status Log Tool (AI 项目状态日志工具)

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

### Project Overview
The **AI Project Status Log Tool** is a lightweight, zero-dependency CLI utility designed to facilitate collaboration between AI agents (like Gemini, Claude) and human developers. It provides a structured way to track tasks, bugs, and features with a strict priority system.

### Features
*   **3-Tier Sorting Logic**: Automatically sorts tasks by Status (Pending > Completed) -> Priority (Tier0 > Tier3) -> Time (Oldest > Newest).
*   **Atomic Storage**: Uses atomic file writes to ensure data integrity, preventing corruption even if the process crashes.
*   **Agent-Friendly**: Supports a `--json` flag for all commands, providing structured machine-readable output for AI agents to parse.
*   **Zero Dependencies**: Built entirely with the Python standard library. No `pip install` required.

### Installation
Simply clone the repository. No external dependencies are needed.
```bash
git clone <repository-url>
cd AI_status
```

### Usage

#### 1. Add a Task
Add a new task to the log.
```bash
# Human readable output
python -m agent_sync.src.main add --desc "Fix memory leak" --priority tier0 --user gemini --role engineer

# JSON output (for agents)
python -m agent_sync.src.main --json add --desc "Fix memory leak" --priority tier0 --user gemini --role engineer
```

#### 2. Read Tasks
View all tasks, automatically sorted by the 3-tier logic.
```bash
python -m agent_sync.src.main read
```

#### 3. Complete a Task
Mark a task as completed by its ID.
```bash
python -m agent_sync.src.main complete --id <task_uuid> --user claude --role engineer
```

---

<a name="chinese"></a>
## 中文 (Chinese)

### 项目简介
**AI 项目状态日志工具** 是一个轻量级、零依赖的命令行工具，旨在促进 AI Agent（如 Gemini, Claude）与人类开发者之间的协作。它提供了一种结构化的方式来跟踪任务、Bug 和功能特性，并强制执行严格的优先级系统。

### 功能特性
*   **三级排序逻辑**：自动按照 状态 (待处理 > 已完成) -> 优先级 (Tier0 > Tier3) -> 时间 (最早 > 最新) 进行排序。
*   **原子存储**：使用原子文件写入操作确保数据完整性，即使进程崩溃也能防止数据损坏。
*   **Agent 友好**：所有命令均支持 `--json` 标志，提供结构化的机器可读输出，便于 AI Agent 解析。
*   **零依赖**：完全使用 Python 标准库构建。无需 `pip install` 任何第三方库。

### 安装指南
只需克隆仓库即可。无需安装任何外部依赖。
```bash
git clone <repository-url>
cd AI_status
```

### 使用指南

#### 1. 添加任务 (Add)
向日志中添加新任务。
```bash
# 人类可读输出
python -m agent_sync.src.main add --desc "修复内存泄漏" --priority tier0 --user gemini --role engineer

# JSON 输出 (供 Agent 使用)
python -m agent_sync.src.main --json add --desc "修复内存泄漏" --priority tier0 --user gemini --role engineer
```

#### 2. 查看任务 (Read)
查看所有任务，自动应用三级排序逻辑。
```bash
python -m agent_sync.src.main read
```

#### 3. 完成任务 (Complete)
通过 ID 将任务标记为已完成。
```bash
python -m agent_sync.src.main complete --id <task_uuid> --user claude --role engineer
```
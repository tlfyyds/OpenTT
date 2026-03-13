<p align="center">
  <a href="https://github.com/tlfyyds/OpenTT/blob/main/README.md">English</a> | 
  <a href="https://github.com/tlfyyds/OpenTT/blob/main/README_CN.md">中文</a>
</p>

------

# 🚀 OpenTT: 你的终极自主 AI 桌面智能体 (Agent)

**OpenTT (Open Task-oriented Tool)** 是一款基于 **ReAct (Reasoning and Acting)** 架构的高级进化版 AI 桌面 Agent。它不仅是一个聊天机器人，更是一个拥有“手”和“大脑”的本地助手，能够直接操控你的 Windows/macOS 系统，自主编写代码并执行复杂的跨应用流。

通过 OpenTT，你可以将 **GPT-4o、Claude 3.5、DeepSeek** 或本地的 **Ollama** 实例转化为运行在你桌面上的强大“代码解释器”与“任务执行官”。

------

## 🌟 为什么选择 OpenTT？

| **功能特性**     | **传统对话 AI (ChatGPT/Claude)** | **OpenTT (自主 Agent)**               |
| ---------------- | -------------------------------- | ------------------------------------- |
| **系统控制权**   | ❌ 仅限于对话和上传文件           | ✅ 直接读写文件、重命名、批量处理      |
| **代码执行**     | ❌ 受限的云端沙箱                 | ✅ 无限的本地 Python 解释器            |
| **浏览器自动化** | ❌ 无法实时操作网页               | ✅ 深度集成 Playwright (模拟真人操作)  |
| **模型灵活性**   | ❌ 厂商锁定                       | ✅ 自由切换 GPT、DeepSeek、私有 Ollama |
| **隐私保护**     | ❌ 数据上传云端处理               | ✅ 核心逻辑与工具调用全部本地化        |

------

## 🔥 核心亮点

- **🛠️ 通用引擎适配器**：深度兼容 OpenAI 标准协议。一键切换顶尖云端模型或私有化本地模型 (**Ollama/vLLM**)。
- **💻 自主代码解释器**：当预设插件无法满足需求时，AI 会在 `workspace/` 沙箱中**自主编写并运行 Python 脚本**，赋予 OpenTT 近乎无限的扩展性。
- **🌐 深度浏览器操控**：基于 Playwright 驱动。AI 可以像真人一样打开浏览器、执行搜索、点击特定 ID 元素、提取数据，甚至处理多页面复杂任务。
- **🛡️ 安全沙箱架构**：
  - `mcps/`：存放经过验证的专业插件（如资产侦察、Nmap 集成）。
  - `workspace/`：AI 的专属实验室。所有生成的临时脚本都在此运行，**绝不污染系统路径**。
- **👁️ 可视化思维链**：现代化的 CustomTkinter UI，实时侧边栏展示 AI 的 **“思考 (Thought) -> 行动 (Action) -> 观察 (Observation)”** 闭环推理过程。

------

## 📂 项目结构

Plaintext

```
OpenTT/
├── main.py                 # 程序启动入口 (GUI)
├── config.json             # 动态配置文件 (API Key, 模型参数等)
├── workspace/              # AI 沙箱：所有生成的 .py 脚本和临时数据存放于此
├── ollamaka/               # Agent 核心：负责逻辑规划、记忆持久化与工具调度
├── mcps/                   # 专业插件库 (Fixed Plugins)
│   ├── base.py             # 插件基类
│   ├── browser_tool.py     # 高性能浏览器控制插件
│   └── code_executor.py    # 核心代码解释器插件
└── ui/                     # 桌面 GUI 组件
```

------

## 🚀 快速上手

### 1. 环境准备

确保你的系统中已安装 Python 3.10 或更高版本。

Bash

```
# 克隆仓库
git clone https://github.com/dabao/OpenTT.git
cd OpenTT

# 安装依赖
pip install -r requirements.txt
playwright install  # 浏览器自动化功能所需
```

### 2. 启动 OpenTT

Bash

```
python main.py
```

### 3. 配置 AI 引擎

点击 UI 右上角的 **⚙️ 设置 (Settings)** 图标，输入：

- **Base URL**: 如 `https://api.openai.com/v1` 或你的本地 Ollama 地址。
- **API Key**: 你的 API 密钥。
- **Model Name**: 如 `gpt-4o`、`deepseek-chat` 或 `qwen2.5:7b`。

------

## 💡 实战场景展示

### 📁 场景一：自动化文件审计

> **用户指令**: "检查桌面文件夹里所有的 .log 文件，提取包含 'CRITICAL' 的行并汇总成一个 Excel。"
>
> **AI 规划**:
>
> 1. **思考**: 我需要扫描文件。没有现成工具，我将调用 `execute_python_code` 编写审计脚本。
> 2. **行动**: 在沙箱中生成并运行 `audit_logs.py`。
> 3. **观察**: 脚本成功提取了 42 条记录并生成了 csv。
> 4. **响应**: 汇总数据并告知用户文件已生成在桌面。

### 🌐 场景二：智能网页情报收集

> **用户指令**: "去百度搜索 '2026年最新国产大语言模型对比'，把前三篇文章的核心观点总结给我。"
>
> **AI 规划**: 调用 `browser_control` -> `goto` -> `snapshot` (观察元素) -> 提取内容 -> 汇总生成简报。

------

## 🤝 贡献与反馈

我们非常欢迎开发者贡献新的 **MCP (Model Context Protocol)** 插件！

- 如果你有新的工具创意，请提交 **Issue**。
- 如果你想优化 Agent 的推理逻辑，请提交 **Pull Request**。

------

## ⚠️ 免责声明

OpenTT 仅用于授权的安全研究、行政自动化及教育目的。开发者对 AI 生成脚本导致的任何数据丢失、系统故障或法律风险不承担责任。**请始终在受控环境下使用 AI 的代码执行功能。**

------

### ⭐ 如果这个项目对你有帮助，请点一个 Star！这是我们持续更新的动力！
# OpenTT (Open Task-oriented Tool)

**OpenTT** 是一款基于 **ReAct (Reasoning and Acting)** 架构构建的自主化 AI 桌面智能体。它打破了传统 AI 只能“聊天”的局限，赋予了模型操控本地系统、编写并执行代码以及处理复杂多步任务的能力。

通过 OpenTT，你可以将 **GPT-4、Grok、DeepSeek** 或本地 **Ollama** 转化为一个运行在桌面的“代码解释器”与“任务执行官”。

## 🚀 项目核心亮点

- **全引擎适配**：深度兼容 OpenAI 标准协议。支持一键切换云端顶级模型或本地私有化模型。
- **自主代码解释器 (Code Interpreter)**：当预设插件无法满足需求时，AI 会自主在沙盒中编写 Python 脚本并运行。这意味着 OpenTT 具有无限的可扩展性。
- **物理隔离安全沙盒**：
  - `mcps/`：存放经过人工验证的固定专业插件（如资产探测、漏洞扫描接口）。
  - `workspace/`：AI 的专属实验室。所有动态生成的临时脚本和中间数据均在此运行，确保不污染系统路径。
- **可视化推理轨迹**：采用 CustomTkinter 打造的现代化 UI，侧边栏实时展示 AI 的“思考过程 -> 动作选择 -> 结果观察”完整闭环。

------

## 📂 文件结构

Plaintext

```
OpenTT/
├── main.py                 # 程序启动入口
├── config.json             # 动态配置文件 (存储 API Key, Base URL 等)
├── workspace/              # AI 脚本执行沙盒 (所有临时生成的 .py 和数据都在这里)
├── ollamaka/               # Agent 核心逻辑 (负责规划、迭代与工具分发)
├── mcps/                   # 专业工具库 (存放固定的、标准化的插件)
│   ├── base.py             # 插件基类
│   └── code_executor.py    # 核心执行器插件
└── ui/                     # 桌面交互界面
```

------

## 🛠️ 快速开始

1. **克隆仓库**

   Bash

   ```
   git clone https://github.com/dabao/OpenTT.git
   cd OpenTT
   ```

2. **安装必要依赖**

   Bash

   ```
   pip install -r requirements.txt
   ```

3. **启动 OpenTT**

   Bash

   ```
   python main.py
   ```

4. **配置 AI 引擎** 点击界面右上角的 **⚙️ 设置** 按钮，填入你的 `API Key`、`Base URL`（如 `https://api.openai.com/v1`）以及模型名称。

------

## 💡 实战场景演示

### 自动化文件审计

- **用户指令**：“检查桌面 `C:\Users\dabao\Desktop` 下所有的 .txt 文件，统计它们的总行数。”
- **AI 规划**：
  1. **思考**：没有直接统计行数的工具，我需要编写 Python 脚本。
  2. **行动**：调用 `execute_python_code`，在 `workspace/` 生成并运行审计脚本。
  3. **观察**：获取脚本输出结果。
  4. **反馈**：整理数据并向用户汇报。

### 安全辅助测试

- **用户指令**：“扫描 192.168.1.1 的常用端口，并尝试识别开启服务的版本。”
- **AI 规划**：调用 `mcps/` 中的 Nmap 插件执行任务，若遇到未知服务，自主编写脚本进行协议指纹识别。

------

## ⚠️ 免责声明

OpenTT 仅用于授权的安全研究、行政自动化及教育目的。开发者不对因 AI 自主生成的脚本而导致的任何数据损坏、系统故障或法律问题承担责任。请在受控环境中使用 AI 的代码执行能力。

------

## 🤝 贡献与反馈

如果你有更好的 MCP 插件想法，或者对 Agent 的逻辑规划有优化建议，欢迎提交 Issue 或 Pull Request！
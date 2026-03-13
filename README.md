

<p align="center">
  <a href="https://github.com/tlfyyds/OpenTT/blob/main/README.md">English</a> | 
  <a href="https://github.com/tlfyyds/OpenTT/blob/main/README_CN.md">中文</a>
</p>

# 🚀 OpenTT: Your Ultimate Autonomous AI Desktop Agent

**OpenTT (Open Task-oriented Tool)** is an advanced evolutionary AI Desktop Agent built on the **ReAct (Reasoning and Acting)** architecture. Unlike traditional chatbots, OpenTT is equipped with "hands" and a "brain" that allow it to directly manipulate your Windows/macOS environment, write and execute code on-the-fly, and automate complex cross-application workflows.

------

## 🌟 Why OpenTT?

| **Feature**            | **Traditional Chatbots (ChatGPT/Claude)** | **OpenTT (Autonomous Agent)**                   |
| ---------------------- | ----------------------------------------- | ----------------------------------------------- |
| **System Control**     | ❌ Limited to uploads/downloads            | ✅ Direct file R/W, renaming, & management       |
| **Code Execution**     | ❌ Restricted cloud sandboxes              | ✅ Infinite local Python Interpreter             |
| **Browser Automation** | ❌ Cannot interact with live pages         | ✅ Deep Playwright integration (Real human-like) |
| **Model Flexibility**  | ❌ Vendor lock-in                          | ✅ GPT-4o                                        |
| **Privacy**            | ❌ Data processed on cloud servers         | ✅ Core logic & tools run on your machine        |

------

## 🔥 Key Features

- **🛠️ Universal Engine Adapter**: Fully compatible with the OpenAI API standard. Switch between top-tier cloud models and private local models (**Ollama/vLLM**) with one click.
- **💻 Autonomous Code Interpreter**: When built-in plugins aren't enough, the AI autonomously writes and runs Python scripts within the  sandbox.`workspace/`
- **🌐 Browser-Use Integration**: Powered by Playwright. The AI can open browsers, search, click specific element IDs, extract data, and even handle complex multi-page tasks.
- **🛡️ Sandboxed Security**:
  - `mcps/`: Houses verified, standardized plugins (e.g., Asset Reconnaissance, Nmap integration).
  - `workspace/`: The AI's private laboratory. All dynamically generated scripts run here to ensure no pollution of your system paths.
- **👁️ Visualized Thought Trace**: A modern UI powered by CustomTkinter, featuring a real-time display of the AI's **"Thought -> Action -> Observation"** reasoning loop.

------

## 📂 Project Structure

Plaintext

```
OpenTT/
├── main.py                 # Application Entry Point (GUI)
├── config.json             # Dynamic Configuration (API Keys, Base URL, etc.)
├── workspace/              # AI Sandbox (Temporary scripts and data stay here)
├── ollamaka/               # Agent Core (Planning, persistence, and tool dispatching)
├── mcps/                   # Professional Plugin Library (Fixed plugins)
│   ├── base.py             # Plugin base class
│   ├── browser_tool.py     # High-performance browser controller
│   └── code_executor.py    # Core Code Interpreter
└── ui/                     # Desktop GUI Components
```

------

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have Python 3.10 or higher installed.

Bash

```
git clone https://github.com/dabao/OpenTT.git
cd OpenTT
pip install -r requirements.txt
playwright install  # Required for browser automation
```

### 2. Launch

Bash

```
python main.py
```

### 3. Configure AI Engine

Click the **⚙️ Settings** icon in the top-right corner:

- **Base URL**:  (or your local Ollama address)`https://api.openai.com/v1`
- **API Key**: Your provider's key
- **Model Name**: e.g.,  or `gpt-4o``qwen2.5:7b`

------

## 💡 Showcase: Real-world Scenarios

### 📁 Scenario 1: Automated File Audit

> **User Prompt**: "Check all .log files in , extract lines containing 'ERROR', and save them to a summary file."`C:\Users\dabao\Desktop`
>
> **AI Planning**:
>
> 1. **Thought**: I need to scan the directory. I will call  to write a custom auditor.`execute_python_code`
> 2. **Action**: Generates and runs  in the sandbox.`log_audit.py`
> 3. **Observation**: Script identifies 24 error entries.
> 4. **Response**: Reports the summary and saves  to your desktop.`error_report.csv`

### 🌐 Scenario 2: Smart Web Intelligence

> **User Prompt**: "Go to Google, search for the latest AI Agent frameworks, and give me a comparison summary of the top 3 results."
>
> **AI Planning**: Calls  ->  ->  -> Extract Content -> Generate Intelligence Report.`browser_control``goto``snapshot`

------

## 🤝 Contribution & Feedback

We are actively looking for contributors to expand our **MCP (Model Context Protocol)** library!

- Have a new tool idea? Open an **Issue**.
- Want to optimize the reasoning logic? Submit a **Pull Request**.

------

## ⚠️ Disclaimer

OpenTT is intended for authorized security research, administrative automation, and educational purposes only. The developer is not responsible for any data loss, system failure, or legal issues arising from AI-generated scripts. Always monitor the AI's execution in a controlled environment.

------

### ⭐ If you find this project useful, please give it a Star! It keeps us going!
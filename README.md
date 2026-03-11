
# OpenTT (Open Task-oriented Tool)

**OpenTT** is an advanced autonomous AI Desktop Agent built on the **ReAct (Reasoning and Acting)** architecture. It transcends the limitations of traditional chatbots by empowering Large Language Models (LLMs) to manipulate local systems, write and execute code on-the-fly, and handle complex, multi-step workflows.

With OpenTT, you can transform **GPT-4, Grok, DeepSeek**, or local **Ollama** instances into a powerful "Code Interpreter" and "Task Executor" residing on your desktop.

## 🚀 Key Highlights

- **Universal Engine Adapter**: Deeply compatible with the OpenAI standard protocol. Switch between top-tier cloud models and private local models with one click.
- **Autonomous Code Interpreter**: When built-in plugins are insufficient, the AI autonomously writes and runs Python scripts within a sandbox. This grants OpenTT near-infinite extensibility.
- **Sandboxed Security Architecture**:
  - `mcps/`: Houses verified, fixed professional plugins (e.g., asset reconnaissance, Nmap integration).
  - `workspace/`: The AI's private laboratory. All dynamically generated scripts and temporary data run here, ensuring no pollution of your system paths.
- **Visualized Thought Trace**: A modern UI powered by CustomTkinter, featuring a real-time sidebar that displays the AI's "Thought -> Action -> Observation" closed-loop reasoning.

------

## 📂 File Structure

Plaintext

```
OpenTT/
├── main.py                 # Application entry point
├── config.json             # Dynamic configuration (API Keys, Base URL, etc.)
├── workspace/              # AI Sandbox (All temporary .py scripts and data stay here)
├── ollamaka/               # Agent Core (Planning, iteration, and tool dispatching)
├── mcps/                   # Professional Toolset (Fixed, standardized plugins)
│   ├── base.py             # Plugin base class
│   └── code_executor.py    # Core Interpreter plugin
└── ui/                     # Desktop GUI
```

------

## 🛠️ Quick Start

1. **Clone the Repository**

   Bash

   ```
   git clone https://github.com/dabao/OpenTT.git
   cd OpenTT
   ```

2. **Install Dependencies**

   Bash

   ```
   pip install -r requirements.txt
   ```

3. **Launch OpenTT**

   Bash

   ```
   python main.py
   ```

4. **Configure AI Engine** Click the **⚙️ Settings** icon in the top-right corner and enter your `API Key`, `Base URL` (e.g., `https://api.openai.com/v1`), and the `Model Name`.

------

## 💡 Showcase: Real-world Scenarios

### Automated File Audit

- **User Prompt**: "Check all .txt files in `C:\Users\dabao\Desktop` and count their total lines."
- **AI Planning**:
  1. **Thought**: No direct line-counting tool available. I need to write a Python script.
  2. **Action**: Call `execute_python_code` to generate and run an audit script in `workspace/`.
  3. **Observation**: Receive the output from the script.
  4. **Response**: Summarize the data and report back to the user.

### Security-Assisted Reconnaissance

- **User Prompt**: "Scan common ports on 192.168.1.1 and attempt to identify service versions."
- **AI Planning**: Calls the Nmap plugin in `mcps/`. If an unknown service is encountered, it autonomously writes a script for custom banner grabbing or fingerprinting.

------

## ⚠️ Disclaimer

OpenTT is intended for authorized security research, administrative automation, and educational purposes only. The developer is not responsible for any data loss, system failure, or legal issues arising from AI-generated scripts. Always use the AI's code execution capabilities in a controlled environment.

------

## 🤝 Contribution & Feedback


Have ideas for a new MCP plugin or suggestions for the Agent's reasoning logic? Feel free to submit an Issue or a Pull Request!

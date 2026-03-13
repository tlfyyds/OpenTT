<p align="center">
  <a href="https://github.com/tlfyyds/OpenTT/blob/main/README.md">English</a> | 
  <a href="https://github.com/tlfyyds/OpenTT/blob/main/README_CN.md">中文</a>
</p>
🚀 OpenTT: Your Ultimate Autonomous AI Desktop AgentOpenTT (Open Task-oriented Tool) is an advanced evolutionary AI Desktop Agent built on the ReAct (Reasoning and Acting) architecture. Unlike traditional chatbots, OpenTT is equipped with "hands" and a "brain" that allow it to directly manipulate your Windows/macOS environment, write and execute code on-the-fly, and automate complex cross-application workflows.🌟 Why OpenTT?FeatureTraditional Chatbots (ChatGPT/Claude)OpenTT (Autonomous Agent)System Control❌ Limited to uploads/downloads✅ Direct file R/W, renaming, & managementCode Execution❌ Restricted cloud sandboxes✅ Infinite local Python InterpreterBrowser Automation❌ Cannot interact with live pages✅ Deep Playwright integration (Real human-like)Model Flexibility❌ Vendor lock-in✅ GPT-4o, Claude 3.5, Ollama, DeepSeekPrivacy❌ Data processed on cloud servers✅ Core logic & tools run on your machine🔥 Key Features🛠️ Universal Engine Adapter: Fully compatible with the OpenAI API standard. Switch between top-tier cloud models and private local models (Ollama/vLLM) with one click.💻 Autonomous Code Interpreter: When built-in plugins aren't enough, the AI autonomously writes and runs Python scripts within the  sandbox.workspace/🌐 Browser-Use Integration: Powered by Playwright. The AI can open browsers, search, click specific element IDs, extract data, and even handle complex multi-page tasks.🛡️ Sandboxed Security:mcps/: Houses verified, standardized plugins (e.g., Asset Reconnaissance, Nmap integration).workspace/: The AI's private laboratory. All dynamically generated scripts run here to ensure no pollution of your system paths.👁️ Visualized Thought Trace: A modern UI powered by CustomTkinter, featuring a real-time display of the AI's "Thought -> Action -> Observation" reasoning loop.📂 Project StructurePlaintextOpenTT/
├── main.py                 # Application Entry Point (GUI)
├── config.json             # Dynamic Configuration (API Keys, Base URL, etc.)
├── workspace/              # AI Sandbox (Temporary scripts and data stay here)
├── ollamaka/               # Agent Core (Planning, persistence, and tool dispatching)
├── mcps/                   # Professional Plugin Library (Fixed plugins)
│   ├── base.py             # Plugin base class
│   ├── browser_tool.py     # High-performance browser controller
│   └── code_executor.py    # Core Code Interpreter
└── ui/                     # Desktop GUI Components
🚀 Quick Start1. PrerequisitesEnsure you have Python 3.10 or higher installed.Bashgit clone https://github.com/dabao/OpenTT.git
cd OpenTT
pip install -r requirements.txt
playwright install  # Required for browser automation
2. LaunchBashpython main.py
3. Configure AI EngineClick the ⚙️ Settings icon in the top-right corner:Base URL:  (or your local Ollama address)https://api.openai.com/v1API Key: Your provider's keyModel Name: e.g.,  or gpt-4oqwen2.5:7b💡 Showcase: Real-world Scenarios📁 Scenario 1: Automated File AuditUser Prompt: "Check all .log files in , extract lines containing 'ERROR', and save them to a summary file."C:\Users\dabao\DesktopAI Planning:Thought: I need to scan the directory. I will call  to write a custom auditor.execute_python_codeAction: Generates and runs  in the sandbox.log_audit.pyObservation: Script identifies 24 error entries.Response: Reports the summary and saves  to your desktop.error_report.csv🌐 Scenario 2: Smart Web IntelligenceUser Prompt: "Go to Google, search for the latest AI Agent frameworks, and give me a comparison summary of the top 3 results."AI Planning: Calls  ->  ->  -> Extract Content -> Generate Intelligence Report.browser_controlgotosnapshot🤝 Contribution & FeedbackWe are actively looking for contributors to expand our MCP (Model Context Protocol) library!Have a new tool idea? Open an Issue.Want to optimize the reasoning logic? Submit a Pull Request.⚠️ DisclaimerOpenTT is intended for authorized security research, administrative automation, and educational purposes only. The developer is not responsible for any data loss, system failure, or legal issues arising from AI-generated scripts. Always monitor the AI's execution in a controlled environment.⭐ If you find this project useful, please give it a Star! It keeps us going!






import os
import sys
import subprocess
import traceback
from .base import MCPTool

class CodeExecutorTool(MCPTool):
    def __init__(self):
        # 自动定位并创建 workspace 目录
        self.workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'workspace'))
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)

    def get_definition(self):
        return {
            "type": "function",
            "function": {
                "name": "execute_python_code",
                "description": "通用代码解释器。当没有预设插件可用时，编写 Python 脚本解决问题。脚本将在 workspace 目录运行，结果必须通过 print() 输出。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "script_name": {"type": "string", "description": "建议的文件名，如 analyze_log.py"},
                        "code": {"type": "string", "description": "完整的 Python 源代码"}
                    },
                    "required": ["script_name", "code"]
                }
            }
        }

    def execute(self, script_name, code):
        file_path = os.path.join(self.workspace, os.path.basename(script_name))
        
        try:
            # 1. 将 AI 生成的代码写入 workspace
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            
            # 2. 调用子进程运行，并将 cwd 设置为 workspace
            # 这样 AI 在代码里写 open('result.txt', 'w') 会自动存入 workspace
            process = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                cwd=self.workspace,
                timeout=60
            )
            
            # 3. 整合输出和错误信息
            response = ""
            if process.stdout:
                response += f"--- 运行输出 ---\n{process.stdout}\n"
            if process.stderr:
                response += f"--- 错误详情 ---\n{process.stderr}\n"
            
            return response if response else "✅ 脚本执行成功，但没有产生 print 输出。"

        except subprocess.TimeoutExpired:
            return "❌ 脚本执行超时（超过 60 秒），请优化逻辑。"
        except Exception:
            return f"❌ 系统级异常:\n{traceback.format_exc()}"
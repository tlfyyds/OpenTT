import subprocess
import os
import time
from .base import MCPTool

class DirsearchTool(MCPTool):
    def __init__(self):
        self.script_path = r"C:\Users\dabao\Desktop\dirserch\dirsearch-0.4.3\dirsearch-0.4.3\dirsearch.py"
        self.python_exe = "python"
        # 结果临时存储路径
        self.output_file = "scan_result.txt"

    def get_definition(self):
        return {
            "type": "function",
            "function": {
                "name": "dir_search",
                "description": "使用 dirsearch 扫描 Web 目录。返回发现的 200/301 状态码路径。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "目标 URL (如 https://8.222.185.91:5553/)"}
                    },
                    "required": ["url"]
                }
            }
        }

    def execute(self, url):
        if not os.path.exists(self.script_path):
            return f"错误：未找到 dirsearch 脚本: {self.script_path}"

        # 每次执行前，如果旧文件存在就删除，确保结果不混淆
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

        try:
            # 参考你提供的成功参数
            cmd = [
                self.python_exe,
                self.script_path,
                "-u", url,
                "-t", "100",
                "-i", "200,301",
                "--format", "plain",
                "-o", self.output_file,
            ]

            print(f"\n[MCP] 正在执行目录扫描: {url}")
            
            # 执行扫描 (设置超时 5 分钟)
            subprocess.run(cmd, check=True, timeout=300, capture_output=True)

            # 扫描完后读取文件
            if os.path.exists(self.output_file):
                with open(self.output_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                # 过滤掉注释行（以 # 开头的行）
                results = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
                
                if results:
                    summary = "目录扫描成功，发现以下路径：\n" + "\n".join(results)
                    print(f"[MCP Debug] 成功提取到 {len(results)} 条结果")
                    return summary
                else:
                    return "扫描完成，但未发现有效的 200 或 301 路径。"
            else:
                return "扫描异常：未生成结果文件。"

        except subprocess.TimeoutExpired:
            return "错误：扫描执行超时。"
        except Exception as e:
            return f"插件执行出错: {str(e)}"
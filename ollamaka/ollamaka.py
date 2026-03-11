import requests
import json
import os
from .manager import MCPManager

class AIClient:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.mcp = MCPManager()
        self.max_iter = 10
        self.config = self.load_config()

    def load_config(self):
        default = {"api_key": "ollama", "base_url": "http://localhost:11434/v1", "model": "qwen2.5:7b"}
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default

    def chat(self, user_input, status_callback=None):
        base_url = self.config['base_url'].rstrip('/')
        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        
        # 1. 强化 System Prompt，强制 GPT 意识到自己有“手”
        messages = [
            {
                "role": "system", 
                "content": (
                    "你拥有本地物理权限。你的目标是解决用户问题。\n"
                    "1. 只要用户提供了路径或任务，优先检查可用工具。\n"
                    "2. 如果没有直接工具，必须调用 'execute_python_code' 编写脚本来操作。\n"
                    "3. 严禁回答'我无法访问'，你应该说'我将编写脚本来访问'并立即行动。\n"
                    "4. 每次工具执行后，分析输出并决定下一步，直到任务完成。"
                )
            },
            {"role": "user", "content": user_input}
        ]

        for step in range(self.max_iter):
            if status_callback: status_callback(f"[第 {step+1} 步] 正在逻辑规划...")
            
            payload = {
                "model": self.config["model"],
                "messages": messages,
                "tools": self.mcp.get_all_definitions(),
                "tool_choice": "auto"
            }

            try:
                response = requests.post(url, headers=headers, json=payload, timeout=120)
                res_json = response.json()
                
                if "error" in res_json:
                    return f"❌ API 错误: {res_json['error'].get('message')}"

                msg = res_json["choices"][0]["message"]
                
                # 必须将完整的 message 对象推入历史，包含 tool_calls 字段
                messages.append(msg)

                # 2. 核心逻辑：处理 GPT 的工具调用请求
                if "tool_calls" in msg and msg["tool_calls"]:
                    for tool_call in msg["tool_calls"]:
                        t_id = tool_call["id"]
                        name = tool_call["function"]["name"]
                        # 转换参数
                        args_str = tool_call["function"].get("arguments", "{}")
                        try:
                            args = json.loads(args_str)
                        except:
                            args = {}

                        if status_callback: status_callback(f"➔ 正在执行: {name}")
                        
                        # 执行工具
                        result = self.mcp.dispatch(name, args)

                        # 3. 关键：回传 tool 角色时必须带上 tool_call_id
                        messages.append({
                            "role": "tool",
                            "tool_call_id": t_id,
                            "name": name,
                            "content": str(result)
                        })
                    
                    # 继续循环，让 GPT 根据工具结果进行“第 2 步”思考
                    continue 
                
                else:
                    # 如果没有 tool_calls，说明 GPT 思考完了
                    return msg.get("content", "任务处理完毕。")

            except Exception as e:
                return f"⚠️ 运行异常: {str(e)}"
        

        return "⚠️ 已达到最大尝试次数。"

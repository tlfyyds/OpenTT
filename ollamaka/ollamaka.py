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

    def save_config(self, api_key, base_url, model):
        self.config = {"api_key": api_key, "base_url": base_url, "model": model}
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def chat(self, user_input, status_callback=None, check_stop=None):
        base_url = self.config['base_url'].rstrip('/')
        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json"
        }
        
        messages = [
            {
                "role": "system", 
                "content": (
                    "你拥有本地物理权限的人工智能。你的目标是解决用户问题。\n"
                    "1. 如果浏览器工具无法直接完成任务，必须立即调用 'execute_python_code' 编写脚本。\n"
                    "2. 严禁回答'我无法访问'，你应该说'我将编写脚本来访问'并立即行动。\n"
                    "3. 每次工具执行后，分析输出并决定下一步，直到任务完成。"
                )
            },
            {"role": "user", "content": user_input}
        ]

        for step in range(self.max_iter):
            # 每一轮思考前检查是否要终止
            if check_stop and check_stop():
                return "🛑 任务已被手动终止。"

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
                messages.append(msg)

                if "tool_calls" in msg and msg["tool_calls"]:
                    for tool_call in msg["tool_calls"]:
                        # 执行具体工具前再次检查终止
                        if check_stop and check_stop():
                            return "🛑 任务在工具执行前终止。"

                        t_id = tool_call["id"]
                        name = tool_call["function"]["name"]
                        args_str = tool_call["function"].get("arguments", "{}")
                        try:
                            args = json.loads(args_str)
                        except:
                            args = {}

                        if status_callback: status_callback(f"➔ 执行工具: {name}")
                        result = self.mcp.dispatch(name, args)

                        messages.append({
                            "role": "tool",
                            "tool_call_id": t_id,
                            "name": name,
                            "content": str(result)
                        })
                    continue 
                else:
                    return msg.get("content", "处理完毕。")
            except Exception as e:
                return f"⚠️ 运行异常: {str(e)}"
        
        return "⚠️ 已达到最大尝试次数。"
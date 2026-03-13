import importlib
import os
import inspect
import sys
from mcps.base import MCPTool

class MCPManager:
    def __init__(self):
        self.tools = {}
        self.load_tools()

    def load_tools(self):
        """自动从项目根目录下的 mcps 文件夹加载所有工具类"""
        # 定位到项目根目录下的 mcps 文件夹
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mcps_path = os.path.abspath(os.path.join(current_dir, '..', 'mcps'))
        
        # 将 mcps 路径加入系统路径，确保 importlib 能找到模块
        project_root = os.path.abspath(os.path.join(current_dir, '..'))
        if project_root not in sys.path:
            sys.path.append(project_root)

        print(f"[MCP Host] 正在从 {mcps_path} 加载插件...")

        for filename in os.listdir(mcps_path):
            if filename.endswith('.py') and filename not in ['base.py', '__init__.py']:
                # 模块名格式为 mcps.文件名
                module_name = f"mcps.{filename[:-3]}"
                try:
                    # 热更新：强制重新加载模块
                    if module_name in sys.modules:
                        module = importlib.reload(sys.modules[module_name])
                    else:
                        module = importlib.import_module(module_name)
                    
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, MCPTool) and obj is not MCPTool:
                            tool_instance = obj()
                            definition = tool_instance.get_definition()
                            tool_name = definition["function"]["name"]
                            self.tools[tool_name] = tool_instance
                            print(f"[MCP Host] 已就绪: {tool_name}")
                except Exception as e:
                    print(f"[MCP Error] 插件 {filename} 加载失败: {e}")

    def reload_tools(self):
        """清除缓存并重新加载，供 AI 自动进化使用"""
        self.tools.clear()
        self.load_tools()
        return "✅ 插件库已成功热更新，新生成的工具已上线。"

    def get_all_definitions(self):
        return [tool.get_definition() for tool in self.tools.values()]

    def dispatch(self, tool_name, args):
        if tool_name in self.tools:
            return self.tools[tool_name].execute(**args)
        return f"未知工具: {tool_name}"
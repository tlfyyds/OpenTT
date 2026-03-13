class MCPTool:
    def get_definition(self):
        """返回符合 OpenAI/Ollama 格式的工具定义"""
        raise NotImplementedError
        
    def execute(self, **kwargs):
        """执行工具逻辑"""
        raise NotImplementedError
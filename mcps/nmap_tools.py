import nmap
from .base import MCPTool

class NmapScanTool(MCPTool):
    def get_definition(self):
        return {
            "type": "function",
            "function": {
                "name": "nmap_scan",
                "description": "执行网络端口扫描，获取指定IP的开放状态。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ip": {"type": "string", "description": "目标 IP 地址"}
                    },
                    "required": ["ip"]
                }
            }
        }

    def execute(self, ip):
        nm = nmap.PortScanner()
        try:
            nm.scan(ip, arguments='-F')
            if ip not in nm.all_hosts(): return "主机不在线。"
            res = []
            for proto in nm[ip].all_protocols():
                for port in nm[ip][proto]:
                    state = nm[ip][proto][port]['state']
                    res.append(f"Port {port}/{proto}: {state}")
            return "\n".join(res) if res else "无开放端口。"
        except Exception as e:
            return f"扫描失败: {e}"
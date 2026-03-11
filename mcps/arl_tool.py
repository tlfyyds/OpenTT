import requests
import urllib3
import tldextract
import re
from .base import MCPTool

# 禁用 HTTPS 安全警告（针对灯塔自签名证书）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ARLScanTool(MCPTool):
    def __init__(self):
        # --- 请修改为你真实的灯塔 API 地址和 Token ---
        self.base_url = ""
        self.api_token = "" 

    def get_definition(self):
        return {
            "type": "function",
            "function": {
                "name": "arl_lighthouse_scan",
                "description": "向 ARL 灯塔下发扫描任务。会自动从 URL 中提取主域名或 IP 进行全量侦察。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "raw_target": {"type": "string", "description": "目标 URL、域名或 IP"}
                    },
                    "required": ["raw_target"]
                }
            }
        }

    def _extract_target(self, raw_target):
        """
        核心优化：智能识别并提取主域名或 IP
        案例: https://sub.example.com/login -> example.com
        """
        # 1. 预处理：去掉协议头、路径、端口
        host = raw_target.replace("http://", "").replace("https://", "").split('/')[0].split(':')[0]
        
        # 2. 判断是否为纯 IP 地址
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if ip_pattern.match(host):
            return host
            
        # 3. 如果是域名，提取主域 (e.g., mail.google.com -> google.com)
        ext = tldextract.extract(host)
        if ext.domain and ext.suffix:
            main_domain = f"{ext.domain}.{ext.suffix}"
            return main_domain
            
        return host # 兜底返回

    def execute(self, raw_target):
        # 提取主域或 IP
        clean_target = self._extract_target(raw_target)
        api_url = f"{self.base_url}/api/task/"
        
        # 构造请求头
        headers = {
            "Token": self.api_token,
            "Content-Type": "application/json"
        }

        # 构造任务 Payload (使用提取后的 clean_target)
        payload = {
            "name": f"AI_Task_{clean_target}",
            "target": clean_target,
            "domain_brute_type": "big",
            "port_scan_type": "all",
            "domain_brute": True,
            "alt_dns": True,
            "dns_query_plugin": True,
            "arl_search": True,
            "port_scan": True,
            "service_detection": True,
            "os_detection": False,
            "ssl_cert": False,
            "skip_scan_cdn_ip": True,
            "site_identify": True,
            "search_engines": True,
            "site_spider": True,
            "site_capture": True,
            "file_leak": True,
            "findvhost": True,
            "nuclei_scan": True,
            "web_info_hunter": True
        }

        # --- 控制台调试打印 ---
        print(f"\n[ARL Debug] 原始输入: {raw_target}")
        print(f"[ARL Debug] 提取目标: {clean_target}")
        # ---------------------

        try:
            response = requests.post(
                api_url, 
                headers=headers, 
                json=payload, 
                verify=False, 
                timeout=15
            )

            print(f"[ARL Debug] 响应状态码: {response.status_code}")

            if response.status_code == 200:
                res_json = response.json()
                # 兼容不同版本的 ARL 返回结构
                task_id = res_json.get("data", {}).get("task_id", "Success")
                return f"✅ 任务成功下发！\n目标主域: {clean_target}\n任务ID: {task_id}"
            
            elif response.status_code == 401:
                return "❌ ARL 认证失败：请在脚本中检查你的 api_token。"
            
            else:
                return f"❌ 任务下发失败 ({response.status_code}): {response.text[:200]}"
        
        except Exception as e:

            return f"⚠️ 联动 ARL 异常: {str(e)}"

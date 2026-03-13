import traceback
import time
import json
import os
from playwright.sync_api import sync_playwright
from .base import MCPTool

# 全局单例
_playwright = None
_browser = None
_page = None

class BrowserTool(MCPTool):
    def __init__(self):
        self.workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'workspace'))
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)

    def get_definition(self):
        return {
            "type": "function",
            "function": {
                "name": "browser_control",
                "description": "高级浏览器控制器。支持唯一 ID 打点观察、强制点击、输入并回车。遇到新页面必须先执行 snapshot。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["goto", "snapshot", "click", "fill", "press", "scroll"],
                            "description": "动作。建议流程：goto -> snapshot -> 根据 ID 执行 click/fill。"
                        },
                        "target": {
                            "type": "string",
                            "description": "URL、元素 ID (数字字符串) 或按键名。"
                        },
                        "value": {
                            "type": "string",
                            "description": "输入内容 (仅 fill 使用)。"
                        }
                    },
                    "required": ["action"]
                }
            }
        }

    def _log(self, message):
        print(f"\033[92m[Observe-Act Engine]\033[0m {message}")

    def execute(self, action, target="", value=""):
        global _playwright, _browser, _page
        self._log(f"指令: {action} | 目标: {target} | 值: {value}")

        if _page is None:
            try:
                _playwright = sync_playwright().start()
                _browser = _playwright.chromium.launch(headless=False)
                _page = _browser.new_page(viewport={'width': 1280, 'height': 800})
            except Exception as e:
                return f"❌ 启动失败: {str(e)}"

        try:
            if action == "goto":
                url = target if target.startswith("http") else f"https://{target}"
                # 优化：采用 domcontentloaded 提升响应速度
                _page.goto(url, wait_until="domcontentloaded", timeout=30000)
                time.sleep(1) 
                return "✅ 页面已加载。请执行 'snapshot' 以获取可操作元素列表。"

            elif action == "snapshot":
                self._log("正在跨框架建立语义地图...")
                # 核心逻辑：给所有交互元素注入 ai-id 属性
                mark_js = """(startId) => {
                    const selectors = 'button, input, textarea, a, [role="button"], .j-flag';
                    const list = [];
                    document.querySelectorAll(selectors).forEach((el, i) => {
                        const rect = el.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0 && window.getComputedStyle(el).display !== 'none') {
                            const id = (startId + i).toString();
                            el.setAttribute('ai-id', id);
                            list.push({
                                id: id,
                                tag: el.tagName.toLowerCase(),
                                label: (el.innerText || el.placeholder || el.value || el.title || "交互件").substring(0, 20).trim()
                            });
                        }
                    });
                    return list;
                }"""

                all_elements = []
                for frame in _page.frames:
                    try:
                        res = frame.evaluate(mark_js, len(all_elements))
                        all_elements.extend(res)
                    except: continue

                # 构建给 AI 的观察报告
                report = "### 👁️ 当前页面可操作 ID 列表\n"
                for el in all_elements[:40]: # 限制数量防止 Token 溢出
                    report += f"- **ID: {el['id']}** | `<{el['tag']}>` | 语义: {el['label']}\n"
                
                return report

            elif action == "click":
                # 增强：全框架搜索并强制点击（处理 label 遮挡）
                for frame in _page.frames:
                    loc = frame.locator(f'[ai-id="{target}"]').first
                    if loc.count() > 0:
                        loc.click(force=True, timeout=3000)
                        return f"✅ 已通过强力模式点击 ID: {target}"
                return f"❌ 找不到 ID 为 {target} 的元素。"

            elif action == "fill":
                # 增强：输入后自动附加回车，满足搜索习惯
                for frame in _page.frames:
                    loc = frame.locator(f'[ai-id="{target}"]').first
                    if loc.count() > 0:
                        loc.fill(value, timeout=3000)
                        loc.press("Enter")
                        return f"✅ 已在 ID {target} 输入并执行回车。"
                return f"❌ ID {target} 定位失败。"

            elif action == "press":
                # 容错：处理 AI 误将 ID 传给 press 的情况
                if target.isdigit():
                    for frame in _page.frames:
                        loc = frame.locator(f'[ai-id="{target}"]').first
                        if loc.count() > 0:
                            loc.press(value or "Enter")
                            return f"✅ 针对 ID {target} 按下了 {value or 'Enter'}"
                _page.keyboard.press(target)
                return f"✅ 键盘按键 {target} 已触发。"

            elif action == "scroll":
                _page.mouse.wheel(0, 600 if target == "down" else -600)
                return "✅ 页面已滚动。"

        except Exception as e:
            self._log(f"异常: {str(e)}")
            return f"❌ 操作异常: {str(e)}"
# =================================================================
# PROJECT: PTVoice (Shensist Pro Tools Agent)
# VERSION: 1.0.0 (Antigravity Production Edition)
# OWNER: Shensist-Agent Architect
# COPYRIGHT: © 2026 Shensist Matrix. All Rights Reserved.
# OFFICIAL: https://shensist.top/
# =================================================================

import subprocess
import requests
import time
import platform

def force_get_clipboard():
    """暴力抓取系统剪贴板信号，绕过所有沙箱"""
    sys_type = platform.system()
    try:
        if sys_type == "Darwin": # Mac
            result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        elif sys_type == "Linux": # Linux (Wayland 优先, X11 备份)
            try:
                result = subprocess.run(['wl-paste'], capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except:
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], capture_output=True, text=True, check=True)
                return result.stdout.strip()
    except Exception:
        return ""

def start_listening():
    print(f"🚀 [PTVoice-{platform.system()}] 暴力监听模式启动 (已绕过系统沙箱)...")
    last_text = ""
    while True:
        try:
            current_text = force_get_clipboard()
            if current_text != last_text and current_text:
                print(f"📋 捕获指令: {current_text}")
                try:
                    # 转发给本地 PTVoice 大脑
                    requests.post("http://127.0.0.1:5000/pt", json={"text": current_text}, timeout=1)
                    last_text = current_text
                except:
                    pass
        except Exception as e:
            print(f"⚠️ 监听异常: {e}")
            
        time.sleep(0.3)

if __name__ == "__main__":
    start_listening()

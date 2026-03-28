# =================================================================
# PROJECT: PTVoice (Shensist Pro Tools Agent)
# SMOKE TEST SUITE
# =================================================================

import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000/pt"
COMMANDS = [
    "播放",
    "停止",
    "新建轨道",
    "添加混响",
    "开始录音",
    "播放刚才的片段",
    "停一下",
    "创建一个人声轨道",
    "开启总线混响",
    "最后一次停止"
]

def run_smoke_test():
    print("🧪 [Shensist-Audit] Starting Smoke Test Suite (10 Intents)...")
    success_count = 0
    
    for i, cmd in enumerate(COMMANDS):
        print(f"[{i+1}/10] Sending Intent: {cmd}")
        try:
            response = requests.post(BASE_URL, json={"text": cmd}, timeout=2)
            if response.status_code == 200:
                print(f"   ✅ Success: {response.json().get('engine_res')}")
                success_count += 1
            elif response.status_code == 403:
                print(f"   🚫 Locked: {response.json().get('reason')}")
            else:
                print(f"   ❌ Failed: Status {response.status_code}")
        except Exception as e:
            print(f"   💥 Connection Error: {e}")
        
        time.sleep(0.5)
    
    print(f"\n📊 [Shensist-Audit] Test Complete. Passed: {success_count}/10")

if __name__ == "__main__":
    run_smoke_test()

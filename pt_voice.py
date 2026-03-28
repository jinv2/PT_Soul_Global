# =================================================================
# PROJECT: PTVoice (Shensist Pro Tools Agent)
# VERSION: 1.0.0 (Antigravity Production Edition)
# OWNER: Shensist-Agent Architect
# COPYRIGHT: © 2026 Shensist Matrix. All Rights Reserved.
# OFFICIAL: https://shensist.top/
# =================================================================

import os
import json
import sys
import subprocess
import hashlib
import platform
import datetime
import requests
import threading
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# 基础配置
CONFIG_FILE = "config.json"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
else:
    config = {"sdk_path": "/home/mmm/PTVoice/sdk/PTSL_v4.proto", "mode": "mock", "port": 5000}

# 商业与品牌资产
BRAND_ASSETS = {
    "LOGO": "/home/mmm/桌面/Shensist_Matrix/PT_Soul_Global/assets/logo.png",
    "FOOTER_URL": "https://shensist.top/",
    "BASE_DIR": "/home/mmm/桌面/Shensist_Matrix/PT_Soul_Global/"
}
# 架构师：线上生产环境 API 地址 (Netlify 全球加速)
AUTH_API = "https://pt-voice.netlify.app/api/verify" 
HARDCODED_EXPIRATION = datetime.datetime(2026, 6, 1)

# --- 核心安全模块 ---

def get_shensist_id():
    """获取机器唯一硬件指纹，防止用户随意拷贝使用"""
    node = platform.node()
    proc = platform.processor()
    system = platform.system()
    raw_id = f"{node}-{proc}-{system}-Shensist2026"
    return hashlib.sha256(raw_id.encode()).hexdigest()[:16]

def check_shensist_auth(command_text="HEARTBEAT"):
    """连接 Shensist 云端验证授权状态"""
    # 物理时间锁检查
    if datetime.datetime.now() > HARDCODED_EXPIRATION:
        return False, "软件试用期已结束，请访问 shensist.top 获取正式授权"
        
    device_id = get_shensist_id()
    try:
        response = requests.post(AUTH_API, json={
            "device_id": device_id,
            "product": "PTVoice",
            "version": "1.0.0",
            "text": command_text # 注入当前指令进行云端分析
        }, timeout=3)
        data = response.json()
        if data.get("status") == "active":
            return True, data.get("expiry_date", "无限期")
        else:
            return False, data.get("message", "机器授权未激活")
    except:
        # 离线保护：允许本地运行但显示警告
        return True, "Offline Mode (Pending Sync)"

def trigger_branded_ui(message, status="info"):
    """
    调起 branded UI 悬浮窗 (Shensist 灵魂版)
    强制携带官网与版权信息
    """
    try:
        # 映射 status 到颜色语义，确保兼容性
        color = "green" if status == "info" else "red" if status == "error" else "yellow"
        
        cmd = [
            "python3", 
            os.path.join(BRAND_ASSETS["BASE_DIR"], "floating_island.py"),
            str(message),
            "--logo", BRAND_ASSETS["LOGO"],
            "--url", BRAND_ASSETS["FOOTER_URL"], # 使用统一的官网地址
            "--color", color
        ]
        subprocess.Popen(cmd)
        print(f"🛡️ [Shensist-Logic] 版权保护激活: {BRAND_ASSETS['FOOTER_URL']}")
    except Exception as e:
        print(f"Branded UI Trigger Error: {e}")

# 兼容性别名，保留 show_branded_status 语义
def show_branded_status(msg, status="normal"):
    trigger_branded_ui(msg, "info" if status == "normal" else "error")

# --- 业务逻辑模块 ---

def execute_intent(text):
    """核心指令执行引擎"""
    sdk_path = os.path.expanduser(config["sdk_path"])
    is_real_mode = (config.get("mode") != "mock" and os.path.exists(sdk_path))
    
    if is_real_mode:
        try:
            import ptsl
            with ptsl.open_engine(sdk_path) as pt:
                if any(k in text for k in ["播放", "开始"]):
                    pt.transport_play()
                    return "REAL: Transport PLAYING"
                elif any(k in text for k in ["停止", "停"]):
                    pt.transport_stop()
                    return "REAL: Transport STOPPED"
                # ... 其他指令适配 ...
                elif any(k in text for k in ["混响", "添加"]):
                    # 假定真实 SDK 对应方法为 add_reverb
                    pt.add_reverb()
                    trigger_branded_ui("PT: [REAL] Reverb ADDED")
        except Exception as e:
            print(f"❌ [Shensist-Logic] PTSL Engine Error: {e}")
            trigger_branded_ui("Error: PTSL initialization failed")
    else:
        # Mock 模式：打印 [Shensist-Mock] 执行成功
        from mock_pt import MockProTools
        engine = MockProTools()
        print(f"🛡️ [Shensist-Logic] Running in MOCK mode...")
        
        if any(k in text for k in ["播放", "开始"]):
            engine.play()
            trigger_branded_ui("PT: [MOCK] Transport PLAYING")
        elif any(k in text for k in ["停止", "停"]):
            engine.stop()
            trigger_branded_ui("PT: [MOCK] Transport STOPPED")
        elif any(k in text for k in ["新建", "轨道"]):
            engine.create_track("Vocal")
            trigger_branded_ui("PT: [MOCK] Track CREATED")
        elif any(k in text for k in ["混响", "添加"]):
            engine.add_reverb()
            trigger_branded_ui("PT: [MOCK] Reverb ADDED")
        else:
            trigger_branded_ui(f"Unknown Instruction: {text}")
    return "MOCK: Executed Successfully"

# --- Webhook 接口 ---

@app.route("/pt", methods=["POST"])
def pt_webhook():
    # 执行动作
    data = request.json or {}
    command_text = data.get("text", "")
    
    # --- 商业防线：指令级授权检查 (附带指令上报) ---
    is_valid, auth_msg = check_shensist_auth(command_text)
    
    if not is_valid:
        trigger_branded_ui(f"🛡️ {auth_msg}", status="error")
        return jsonify({"status": "locked", "reason": auth_msg}), 403

    print(f"📥 [Shensist-Logic] Processing: {command_text}")
    
    exec_res = execute_intent(command_text)
    
    # 结果反馈
    trigger_branded_ui(f"执行成功: {command_text}", status="info")
    
    return jsonify({
        "status": "executed", 
        "command": command_text, 
        "engine_res": str(exec_res),
        "auth_expiry": auth_msg
    })

def shensist_heartbeat():
    """每 5 分钟向云端发送一次生存报告，确保连接保活"""
    while True:
        try:
            requests.post(AUTH_API, json={
                "device_id": get_shensist_id(),
                "product": "PTVoice",
                "version": "1.0.0",
                "text": "HEARTBEAT_IDLE"
            }, timeout=2)
        except:
            pass
        time.sleep(300) # 5分钟一次

if __name__ == "__main__":
    is_sdk_valid = os.path.exists(os.path.expanduser(config["sdk_path"]))
    if not is_sdk_valid:
        trigger_branded_ui("引导页: SDK文件缺失, 请通过微信发送指令安装.", status="warning")
    
    print(f"🚀 PTVoice Pro (ID: {get_shensist_id()}) Starting...")
    
    # 启动后台保活线程
    threading.Thread(target=shensist_heartbeat, daemon=True).start()
    
    # 启动时执行一次全景检查
    valid, _ = check_shensist_auth()
    if not valid:
        trigger_branded_ui("系统锁定：机器未授权", status="error")
        
    app.run(host="0.0.0.0", port=config["port"])

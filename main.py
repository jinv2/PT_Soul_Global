from flask import Flask, request, jsonify
from brain_parser import parse_command
from mock_engine import MockProTools
import subprocess, sys, os

app = Flask(__name__)
pt = MockProTools()
UI_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "floating_island.py")

@app.route("/webhook/wechat", methods=["POST"])
def handle_wechat():
    text = request.json.get("text", "")
    print(f"🎙️ [Shensist 收到指令]: {text}")
    
    # 唤醒灵动之眼 (悬浮窗)
    subprocess.Popen([sys.executable, UI_SCRIPT, f"🔴 Shensist执行中: {text}"])
    
    # 大脑解析并执行
    res = parse_command(text, pt)
    
    return jsonify({"status": "success", "action": res})

if __name__ == "__main__":
    print("🔥 PT-Soul 商业版后端 (含视觉引擎) 已就绪")
    app.run(host="0.0.0.0", port=5000)
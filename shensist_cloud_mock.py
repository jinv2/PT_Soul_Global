import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 模拟数据库：存储设备指纹与授权状态 ---
USER_DATABASE = {
    "default_device": {
        "status": "denied",
        "expiry_date": "2026-12-31",
        "message": "Shensist Pro 授权正常"
    }
}

# --- 模拟心跳日志存储 ---
ACTIVE_USERS = {} # 格式: { device_id: { "last_seen": timestamp, "total_calls": 10, "ips": set(), "last_cmd": "" } }

@app.route("/api/v1/verify", methods=["POST"])
def verify_auth():
    data = request.json or {}
    device_id = data.get("device_id", "unknown_device")
    ip_addr = request.remote_addr
    cmd_text = data.get("text", "HEARTBEAT")

    # --- 监测逻辑 ---
    if device_id not in ACTIVE_USERS:
        ACTIVE_USERS[device_id] = {
            "first_seen": time.ctime(),
            "total_calls": 0,
            "ips": set()
        }
    
    ACTIVE_USERS[device_id]["last_seen"] = time.ctime()
    ACTIVE_USERS[device_id]["total_calls"] += 1
    ACTIVE_USERS[device_id]["ips"].add(ip_addr)
    ACTIVE_USERS[device_id]["last_cmd"] = cmd_text

    # 如果数据库没有该 ID，自动注册为 active 以便测试
    if device_id not in USER_DATABASE:
        USER_DATABASE[device_id] = {
            "status": "denied",
            "expiry_date": "2026-06-01",
            "message": "Trial Period Expired - Contact Shensist"
        }

    user_info = USER_DATABASE[device_id]
    
    if user_info["status"] == "active":
        return jsonify({
            "status": "active",
            "expiry_date": user_info["expiry_date"],
            "message": user_info["message"]
        })
    elif user_info["status"] == "denied":
        return jsonify({
            "status": "denied",
            "message": "❌ 您的授权已被架构师停用，请联系 shensist.top"
        }), 403
    else:
        return jsonify({"status": "maintenance", "message": "🚧 系统维护中"}), 503

@app.route("/admin")
def shensist_admin_panel():
    """架构师专属管理界面：支持手机访问"""
    rows = ""
    for uid, data in ACTIVE_USERS.items():
        # 获取实时数据库状态
        db_status = USER_DATABASE.get(uid, {}).get("status", "unknown")
        color = "#00ff00" if db_status == "active" else "#ff4444"
        btn_text = "停用" if db_status == "active" else "激活"
        
        rows += f"""
        <tr style="border-bottom: 1px solid #333;">
            <td style="padding:10px; color:{color}">{uid}</td>
            <td style="padding:10px;">{data['last_seen']}</td>
            <td style="padding:10px;">{data['total_calls']}</td>
            <td style="padding:10px;"><button style="padding:5px 10px; background:#444; color:#fff; border:none; border-radius:3px;" onclick="toggleUser('{uid}')">{btn_text}</button></td>
        </tr>
        """
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shensist Control Center</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ background:#111; color:#0f0; font-family:'Courier New', monospace; padding:10px; }}
            table {{ width:100%; border-collapse:collapse; background:#1a1a1a; }}
            th {{ text-align:left; padding:10px; background:#222; border-bottom:2px solid #0f0; }}
            h2 {{ text-shadow: 0 0 10px #0f0; }}
        </style>
    </head>
    <body>
        <h2>🛡️ Shensist PTVoice 监测中枢</h2>
        <div style="overflow-x:auto;">
            <table>
                <tr><th>设备ID</th><th>活跃时间</th><th>调用</th><th>操作</th></tr>
                {rows if rows else "<tr><td colspan='4' style='padding:20px; text-align:center;'>等待设备接入...</td></tr>"}
            </table>
        </div>
        <script>
            function toggleUser(id) {{ 
                if(confirm('确认修改设备 [' + id + '] 的授权状态？')) {{
                    fetch('/admin/toggle/' + id).then(() => location.reload()); 
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.route("/admin/toggle/<device_id>")
def toggle_user(device_id):
    """一键封禁/解封"""
    if device_id in USER_DATABASE:
        current = USER_DATABASE[device_id]["status"]
        USER_DATABASE[device_id]["status"] = "denied" if current == "active" else "active"
        return "OK"
    return "Not Found", 404

if __name__ == "__main__":
    print("🌍 Shensist 云端管理中枢已启动 (Port: 5001)")
    print("💡 手机管理入口: http://127.0.0.1:5001/admin")
    app.run(host="0.0.0.0", port=5001)

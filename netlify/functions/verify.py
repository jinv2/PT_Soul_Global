import json
import time

# --- 模拟云端数据库 (生产环境请连接 MongoDB/Supabase) ---
USER_DATABASE = {
    "default_device": {
        "status": "active",
        "expiry_date": "2026-12-31"
    }
}

def handler(event, context):
    """Netlify Function 处理函数"""
    if event['httpMethod'] != 'POST':
        return {
            "statusCode": 405,
            "body": "Method Not Allowed"
        }

    try:
        data = json.loads(event['body'])
        device_id = data.get("device_id", "unknown")
        cmd_text = data.get("text", "HEARTBEAT")
        
        # 简单判定逻辑 (演示用)
        # 实际生产中在此处查询数据库
        status = "active"
        if device_id == "blocked_id":
            status = "denied"
            
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": status,
                "expiry_date": "2026-12-31",
                "message": "Verified by Shensist Cloud",
                "cloud_sync_time": time.ctime()
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

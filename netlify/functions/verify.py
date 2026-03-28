# © 2026 Shensist Matrix | https://shensist.top/
import json
import time

def handler(event, context):
    # 【0元试用阶段】核心逻辑：记录并全员放行
    try:
        if event['httpMethod'] != 'POST':
            return {"statusCode": 405, "body": "Method Not Allowed"}
            
        body = json.loads(event['body'])
        device_id = body.get("device_id", "unknown")
        
        # 记录日志：你在 Netlify 控制台能看到谁在用
        print(f"📈 [Shensist-Growth] 发现新用户: {device_id} | 状态: 0元试用激活")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "active",
                "expiry": "2027-01-01", # 给一个超长有效期
                "message": "Shensist Pro 已激活 (0元试用版)。访问 https://shensist.top/ 了解更多。"
            })
        }
    except Exception as e:
        return {"statusCode": 400, "body": str(e)}

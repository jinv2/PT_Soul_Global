# © 2026 Shensist Matrix | https://shensist.top/
import json

def handler(event, context):
    # 模拟数据库：实际可连接 Netlify KV 或外部 DB
    # 这里存储你需要“封杀”或“激活”的硬件指纹
    AUTHORIZED_DEVICES = ["default_test_id"] 

    if event['httpMethod'] != 'POST':
        return {"statusCode": 405, "body": "Method Not Allowed"}

    try:
        body = json.loads(event['body'])
        device_id = body.get("device_id")
        
        # 核心判定逻辑
        if device_id in AUTHORIZED_DEVICES:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": "active",
                    "expiry": "2026-12-31",
                    "message": "Welcome to Shensist Matrix. Official: https://shensist.top/"
                })
            }
        else:
            return {
                "statusCode": 403,
                "body": json.dumps({
                    "status": "denied",
                    "message": "🛡️ 授权未激活。请访问 https://shensist.top/ 获取准入许可。"
                })
            }
    except:
        return {"statusCode": 400, "body": "Invalid Request"}
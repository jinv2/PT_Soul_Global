# -*- coding: utf-8 -*-
import itchat
import requests

# 你的本地后端地址
BACKEND_URL = "http://127.0.0.1:5000/webhook/wechat"

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # 只响应发给“文件传输助手”或包含特定关键词的消息
    if msg['ToUserName'] == 'filehelper':
        print(f"📥 [微信收到指令]: {msg['Text']}")
        
        # 转发给我们的 PT 灵魂大脑
        try:
            res = requests.post(BACKEND_URL, json={"text": msg['Text']})
            print(f"🚀 [大脑响应]: {res.json().get('action')}")
        except Exception as e:
            print(f"❌ 转发失败: {e}")

print("🔥 Shensist 微信穿透模式启动...")
itchat.auto_login(hotReload=True) # 第一次运行需扫码登录
itchat.run()
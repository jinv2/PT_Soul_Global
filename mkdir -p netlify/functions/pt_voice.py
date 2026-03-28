# =================================================================
# 🛡️ SHENSIST MATRIX - CLOUD GATEWAY CONFIGURATION
# OFFICIAL: https://shensist.top/
# AGENT: PTVoice Pro
# =================================================================

# 🚀 终极云端鉴权地址：永久绑定 Shensist 品牌二级域名
AUTH_API = "https://PTVoice.shensist.top/api/verify"

def check_auth_final():
    """
    通过 PTVoice.shensist.top 进行全球实时鉴权
    """
    try:
        # 发送硬件指纹到你的专属二级域名
        res = requests.post(AUTH_API, json={"device_id": get_shensist_id()}, timeout=5)
        # ... 后续逻辑 ...
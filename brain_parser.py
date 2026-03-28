import re

def parse_command(text, pt):
    # 统一清洗文本
    text = text.replace(" ", "").lower()
    
    # 场景一：人声录音场景
    if any(k in text for k in ["录音", "人声", "开工", "录制"]):
        print("🎤 [Shensist 场景] 正在配置人声录音链...")
        pt.create_track("Vocal_Main", "Mono_Audio")
        pt.create_aux("Reverb_Bus", "Stereo")
        pt.insert_plugin("Reverb_Bus", "D-Verb")
        print("🔴 [执行] 轨道 Vocal_Main 已进入待录音状态")
        return "SCENE_VOCAL_READY"

    # 场景二：走带控制
    if any(k in text for k in ["播放", "开始", "走起"]):
        pt.transport_play()
        return "TRANSPORT_PLAY"
    
    if any(k in text for k in ["停止", "停", "住手"]):
        pt.transport_stop()
        return "TRANSPORT_STOP"

    # 场景三：清理
    if "清理" in text:
        print("🧹 [维护] 正在清理工程冗余文件...")
        return "PROJECT_CLEANUP"

    return "UNKNOWN_INTENT"

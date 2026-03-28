class MockProTools:
    def __init__(self):
        print("🔧 [Shensist 引擎] MockProTools 模拟底层已挂载。")

    def create_track(self, name, track_type):
        print(f"🎚️ [PT 动作] 创建轨道 -> 名称: {name} | 类型: {track_type}")

    def create_aux(self, name, track_type):
        print(f"🎛️ [PT 动作] 创建 Aux 轨道 -> 名称: {name} | 类型: {track_type}")

    def insert_plugin(self, track_name, plugin_name):
        print(f"🔌 [PT 动作] 插入插件 -> 轨道: {track_name} | 插件: {plugin_name}")

    def transport_play(self):
        print("▶️ [PT 动作] 走带控制：播放启动")

    def transport_stop(self):
        print("⏹️ [PT 动作] 走带控制：全工程停止")

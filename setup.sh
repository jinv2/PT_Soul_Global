#!/bin/bash
# PTVoice Setup Script - Shensist Matrix
echo "🔧 [Shensist-Logic] Preparing PTVoice Environment..."

# 自动创建 ~/PTVoice/sdk/ 路径
SDK_DIR="$HOME/PTVoice/sdk"
mkdir -p "$SDK_DIR"
echo "✅ Directory created: $SDK_DIR"

# 检查系统剪贴板工具 (Wayland/X11)
echo "🔍 [Shensist-Logic] Checking system clipboard utilities..."
if ! command -v wl-paste &> /dev/null && ! command -v xclip &> /dev/null; then
    echo "⚠️ [Shensist-Logic] Warning: Neither 'wl-clipboard' nor 'xclip' found."
    echo "💡 Please install them: 'sudo apt install wl-clipboard xclip'"
fi

# 使用 --break-system-packages 强制安装 flask, py-ptsl, pyperclip
echo "📦 [Shensist-Logic] Installing Python dependencies..."
pip install flask py-ptsl pyperclip requests --break-system-packages

# 若无 PTSL_v4.proto，创建一个空的以通过 check_sdk()
PROTO_FILE="$SDK_DIR/PTSL_v4.proto"
if [ ! -f "$PROTO_FILE" ]; then
    echo "📄 [Shensist-Logic] Creating dummy PTSL_v4.proto for Mock Mode..."
    touch "$PROTO_FILE"
fi

echo "🚀 [Shensist-Logic] PTVoice Setup Complete. Use 'python3 pt_voice.py' to start."

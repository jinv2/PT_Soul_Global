#!/bin/bash
# Shensist PTVoice Mac Deployment Script
# PROJECT: PTVoice (Shensist Pro Tools Agent)
# COPYRIGHT: © 2026 Shensist Matrix. All Rights Reserved.

echo "🛡️ Starting PTVoice (Mac Edition) Branded Setup..."

# 1. 目录合规化检查
TARGET_DIR="/home/mmm/桌面/Shensist_Matrix/PT_Soul_Global/"
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

# 2. 品牌资产校验 (兼容 logo.png 和 logo_ts.webp)
LOGO_PATH="${TARGET_DIR}assets/logo.png"
if [ ! -f "$LOGO_PATH" ]; then
    echo "❌ ERROR: Branded logo not found in $TARGET_DIR/assets/"
    echo "Please place the logo file to maintain Shensist branding."
    # exit 1
else
    echo "✅ Branding asset (logo) verified."
fi

# 3. 安装 Mac 生产环境依赖 (增加 Pillow 用于 branded UI)
echo "📦 Installing Professional SDK Dependencies..."
pip install flask py-ptsl pyperclip requests Pillow --break-system-packages

# 4. 写入版权保护文件
echo "© 2026 Shensist Matrix. https://shensist.top/" > "${TARGET_DIR}NOTICE.txt"

echo "✅ Branded Setup Complete. Ready for Pro Tools Integration."

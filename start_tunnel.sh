#!/bin/bash
echo "🚀 启动 Shensist 虫洞 (内网穿透)..."
# 如果没有 cpolar，就自动下载安装
if ! command -v cpolar &> /dev/null; then
    curl -L https://www.cpolar.com/static/downloads/install-release-cpolar.sh | sudo bash
fi
# 开启映射本地 5000 端口的隧道
cpolar http 5000

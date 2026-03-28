# PT-Soul Automation Makefile

PYTHON = python3
PIP = pip3

help:
	@echo "PT-Soul Global 自动化管理工具"
	@echo "  make setup        - 安装所有依赖 (Flask, PySide6, PyYAML)"
	@echo "  make mock-test    - 在当前 Ubuntu 环境运行 Mock 测试 (核心反馈)"
	@echo "  make build-mac    - 调用 PyInstaller 打包为 .app (需在 Mac 或通过工具链运行)"
	@echo "  make clean        - 清理临时文件"

setup:
	$(PIP) install flask pyside6 pyyaml pyinstaller

mock-test:
	@echo "\033[95m>>> 启动 PT-Soul Mock 运行演示... <<<\033[0m"
	# 先运行解析测试
	$(PYTHON) brain_parser.py
	# 启动 Mock 引擎独立测试
	$(PYTHON) mock_engine.py
	# 提示用户启动 Web 监听
	@echo "\033[92m[Success] Mock 逻辑校验通过。如需完整交互体验，请运行: python3 main.py\033[0m"

clean:
	rm -rf __pycache__
	rm -rf build/
	rm -rf dist/
	rm -rf *.spec

#!/usr/bin/env python3
"""
macOS 智能连点器 - 主入口
打包后双击即可运行
"""

import threading
import time
import os
import sys

# 获取应用程序所在目录
if getattr(sys, 'frozen', False):
    # 打包后的路径
    APP_DIR = os.path.dirname(sys.executable)
    if APP_DIR.endswith('MacOS'):
        # .app bundle 结构
        APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(APP_DIR)))
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

# 设置工作目录
os.chdir(APP_DIR)

def run_backend():
    """在后台线程运行 Flask 服务"""
    # 导入后端模块
    sys.path.insert(0, os.path.join(APP_DIR, 'backend'))
    from backend.app import app
    
    # 禁用 Flask 的日志输出到控制台（生产模式）
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(port=5005, use_reloader=False, threaded=True)

def run_webview():
    """运行原生窗口界面"""
    import webview
    
    # 等待后台服务启动
    time.sleep(1.5)
    
    # 创建原生窗口
    window = webview.create_window(
        'macOS 智能连点器',
        'http://localhost:5005/static/index.html',
        width=500,
        height=750,
        resizable=True,
        min_size=(400, 600)
    )
    
    # 启动窗口
    webview.start()

def main():
    # 启动后台线程
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # 启动前端窗口（主线程）
    run_webview()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
macOS 智能连点器 - 主入口
打包后双击即可运行
"""

import os
import sys
import threading
import time

# 获取资源目录
def get_resource_dir():
    if getattr(sys, 'frozen', False):
        # PyInstaller .app bundle:
        # 可执行文件: Contents/MacOS/连点器
        # 资源文件: Contents/Resources/
        exe_dir = os.path.dirname(sys.executable)        # Contents/MacOS
        contents_dir = os.path.dirname(exe_dir)           # Contents
        return os.path.join(contents_dir, 'Resources')    # Contents/Resources
    else:
        return os.path.dirname(os.path.abspath(__file__))

RESOURCE_DIR = get_resource_dir()
os.environ['APP_RESOURCE_DIR'] = RESOURCE_DIR

sys.path.insert(0, RESOURCE_DIR)

def run_backend():
    """在后台线程运行 Flask 服务"""
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    from backend.app import app
    app.run(port=5005, use_reloader=False, threaded=True)

def main():
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    time.sleep(1.5)
    
    import webview
    window = webview.create_window(
        '剑三连点器',
        'http://127.0.0.1:5005/static/index.html',
        width=480,
        height=1020,
        resizable=True,
        min_size=(400, 700)
    )
    webview.start()

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import tkinter as tk
import sys
import argparse
import os
from PIL import Image, ImageTk

def show_island(msg, logo_path=None, footer_url=None, status="info"):
    root = tk.Tk()
    # 无边框、窗口置顶
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    
    # 状态配色方案
    # info: 绿字黑底; warning: 黑字黄底; error: 白字红底
    schemes = {
        "info": {"bg": "#1E1E1E", "fg": "#00FF00", "footer": "#555555"},
        "warning": {"bg": "#FFCC00", "fg": "#000000", "footer": "#333333"},
        "error": {"bg": "#CC0000", "fg": "#FFFFFF", "footer": "#EEEEEE"}
    }
    theme = schemes.get(status, schemes["info"])
    
    root.configure(bg=theme["bg"])
    
    # 动态计算屏幕居中，并在顶部悬浮
    width = 500
    height = 65
    screen_width = root.winfo_screenwidth()
    x = int((screen_width - width) / 2)
    root.geometry(f"{width}x{height}+{x}+20")
    
    # 主容器
    main_frame = tk.Frame(root, bg=theme["bg"])
    main_frame.pack(expand=True, fill="both", padx=10, pady=5)
    
    # 左侧 Logo (如果存在)
    if logo_path and os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)
            img = img.resize((40, 40), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(main_frame, image=logo_img, bg=theme["bg"])
            logo_label.image = logo_img # 保持引用
            logo_label.pack(side="left", padx=(0, 10))
        except Exception:
            pass
            
    # 中间信息
    msg_label = tk.Label(main_frame, text=msg, fg=theme["fg"], bg=theme["bg"], font=("Helvetica", 12, "bold"))
    msg_label.pack(side="left", expand=True)
    
    # 底部 Footer (版权链接 或 授权信息)
    if footer_url:
        footer_label = tk.Label(root, text=footer_url, fg=theme["footer"], bg=theme["bg"], font=("Helvetica", 8))
        footer_label.pack(side="bottom", pady=(0, 5))
    
    # 2500 毫秒后自动销毁窗口
    root.after(2500, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("message", nargs="?", default="PT-Soul 视觉引擎已就绪")
    parser.add_argument("--logo", help="Path to logo icon")
    parser.add_argument("--footer", "--url", help="Footer URL or copyright text")
    parser.add_argument("--status", "--color", choices=["info", "warning", "error", "normal", "red", "green"], default="info", help="UI status theme")
    
    args = parser.parse_args()
    
    # Alias mapping
    status_map = {
        "normal": "info",
        "green": "info",
        "red": "error"
    }
    status = status_map.get(args.status, args.status)
    
    show_island(args.message, args.logo, args.footer, status)
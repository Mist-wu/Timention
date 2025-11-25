import tkinter as tk
from tkinter import simpledialog
import time
import threading
import sys

class TimentionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        self.interval_minutes = self.get_user_interval()
        
        if self.interval_minutes is None:
            self.root.destroy()
            return

        self.interval_seconds = self.interval_minutes * 60
        self.is_running = True

        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()

        self.root.mainloop()

    def get_user_interval(self):
        return simpledialog.askinteger(
            "Timention 设置", 
            "请输入提醒间隔（分钟）:",
            parent=self.root,
            minvalue=1,
            maxvalue=1440
        )

    def run_timer(self):
        while self.is_running:
            # 模拟计时（检测 self.is_running 以便能及时退出）
            for _ in range(self.interval_seconds):
                if not self.is_running: return
                time.sleep(1)
            
            if not self.is_running: return

            self.root.after(0, self.show_reminder)
            self.wait_for_dismiss()

    def wait_for_dismiss(self):
        self.reminder_active = True
        while self.reminder_active and self.is_running:
            time.sleep(0.5)

    def show_reminder(self):
        """显示全屏提醒"""
        self.top = tk.Toplevel(self.root)
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-topmost", True)
        self.top.configure(bg="black")

        # 更新提示文案
        label = tk.Label(
            self.top, 
            text="喝水", 
            font=("Microsoft YaHei", 40, "bold"), # 使用微软雅黑显示中文更友好
            fg="white",
            bg="black"
        )
        label.pack(expand=True)

        # 绑定按键事件到新的处理函数
        self.top.bind("<Key>", self.handle_keypress)
        self.top.focus_force()

    def handle_keypress(self, event):
        """处理按键逻辑"""
        if event.keysym == 'Escape':
            # 如果按下 ESC，彻底退出
            self.quit_app()
        else:
            # 其他按键，仅仅关闭窗口并重置
            self.dismiss_reminder()

    def dismiss_reminder(self):
        if hasattr(self, 'top') and self.top:
            self.top.destroy()
            self.top = None
        self.reminder_active = False
        print("提醒关闭，计时器重置。")

    def quit_app(self):
        """彻底退出程序"""
        print("程序退出。")
        self.is_running = False
        self.reminder_active = False
        if hasattr(self, 'top') and self.top:
            self.top.destroy()
        self.root.destroy()
        sys.exit() # 确保强制退出

if __name__ == "__main__":
    app = TimentionApp()
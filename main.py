import tkinter as tk
from tkinter import simpledialog
import time
import threading

class TimentionApp:
    def __init__(self):
        # 创建一个隐藏的根窗口用于对话框和后续的全屏窗口
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口，保持后台运行的感觉

        # 1. 启动时提示用户设置间隔
        self.interval_minutes = self.get_user_interval()
        
        if self.interval_minutes is None:
            print("未设置时间，程序退出。")
            self.root.destroy()
            return

        self.interval_seconds = self.interval_minutes * 60
        self.is_running = True

        # 开始后台计时线程
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()

        # 进入 Tkinter 主循环
        self.root.mainloop()

    def get_user_interval(self):
        """弹出输入框获取用户设定的分钟数"""
        # 临时显示 root 以便对话框有父级（虽然不显示也能工作，但这更稳健）
        return simpledialog.askinteger(
            "Timention 设置", 
            "请输入提醒间隔（分钟）:",
            parent=self.root,
            minvalue=1,
            maxvalue=1440
        )

    def run_timer(self):
        """后台计时逻辑"""
        while self.is_running:
            print(f"计时开始: {self.interval_minutes} 分钟后提醒...")
            time.sleep(self.interval_seconds)
            
            # 时间到，在主线程中调度显示提醒窗口
            # Tkinter 不是线程安全的，必须通过 after 在主线程操作 GUI
            self.root.after(0, self.show_reminder)
            
            # 等待提醒窗口关闭的信号（这里我们使用一个简单的 Event 或者让 show_reminder 阻塞）
            # 但由于我们是循环，show_reminder 关闭后，循环会继续
            # 为了防止在显示窗口时计时器继续跑，我们需要等待窗口关闭
            # 这里使用一个简单的锁机制：在这个循环里等待，直到窗口关闭标志被重置
            self.wait_for_dismiss()

    def wait_for_dismiss(self):
        """阻塞计时线程，直到提醒窗口被关闭"""
        self.reminder_active = True
        while self.reminder_active and self.is_running:
            time.sleep(0.5)

    def show_reminder(self):
        """显示全屏无边框提醒窗口"""
        self.top = tk.Toplevel(self.root)
        self.top.title("Timention 提醒")
        
        # 设置全屏且无边框
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-topmost", True) # 确保在最上层
        
        # 黑色背景，白色文字
        self.top.configure(bg="black")

        # 提醒内容
        label = tk.Label(
            self.top, 
            text="是时候休息一下了！\n\n(按任意键继续)", 
            font=("Helvetica", 40, "bold"),
            fg="white",
            bg="black"
        )
        label.pack(expand=True)

        # 绑定任意按键事件来关闭窗口
        self.top.bind("<Key>", self.dismiss_reminder)
        
        # 强制获取焦点，确保按键能被捕获
        self.top.focus_force()

    def dismiss_reminder(self, event=None):
        """关闭提醒窗口并重置状态"""
        if hasattr(self, 'top') and self.top:
            self.top.destroy()
            self.top = None
        
        # 允许计时器线程继续下一次循环
        self.reminder_active = False
        print("提醒关闭，计时器重置。")

if __name__ == "__main__":
    app = TimentionApp()
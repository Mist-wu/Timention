import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QInputDialog, QDesktopWidget)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

class ReminderOverlay(QWidget):
    """全屏提醒遮罩层"""
    # 定义一个信号，当提醒被忽略（非ESC键）时触发
    dismissed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置窗口标志：无边框、置顶、工具窗口(不在任务栏显示)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # 设置全屏
        self.showFullScreen()
        
        # 美化：使用现代深色背景
        self.setStyleSheet("background-color: #1e1e2e;")

        # 布局管理器
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 提示标签
        self.label = QLabel("💧 该喝水了")
        self.label.setAlignment(Qt.AlignCenter)
        
        # 美化：设置字体 (使用微软雅黑或系统无衬线字体)
        font = QFont("Microsoft YaHei", 72, QFont.Bold)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #cdd6f4;") # 柔和的淡紫色/白色

        # 副标题提示
        self.sub_label = QLabel("按 ESC 退出程序，按任意键继续工作")
        self.sub_label.setAlignment(Qt.AlignCenter)
        sub_font = QFont("Microsoft YaHei", 14)
        self.sub_label.setFont(sub_font)
        self.sub_label.setStyleSheet("color: #a6adc8; margin-top: 20px;")

        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.sub_label)
        layout.addStretch()

    def keyPressEvent(self, event):
        """处理按键逻辑"""
        if event.key() == Qt.Key_Escape:
            # ESC 彻底退出
            QApplication.quit()
        else:
            # 其他按键，隐藏窗口并发送信号
            self.hide()
            self.dismissed.emit()

class TimentionApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.apply_global_style()
        
        self.timer = QTimer()
        self.timer.setSingleShot(True) # 触发一次后停止，等待手动重启
        self.timer.timeout.connect(self.show_reminder)

        # 初始化提醒窗口
        self.overlay = ReminderOverlay()
        self.overlay.dismissed.connect(self.restart_timer)

        # 获取用户输入
        self.interval_minutes = self.get_user_interval()
        
        if self.interval_minutes:
            self.start_timer()
            sys.exit(self.app.exec_())
        else:
            sys.exit()

    def apply_global_style(self):
        """设置输入框的全局样式"""
        self.app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 46))
        palette.setColor(QPalette.WindowText, QColor(205, 214, 244))
        palette.setColor(QPalette.Button, QColor(49, 50, 68))
        palette.setColor(QPalette.ButtonText, QColor(205, 214, 244))
        palette.setColor(QPalette.Base, QColor(24, 24, 37))
        palette.setColor(QPalette.AlternateBase, QColor(30, 30, 46))
        palette.setColor(QPalette.ToolTipBase, QColor(205, 214, 244))
        palette.setColor(QPalette.ToolTipText, QColor(205, 214, 244))
        palette.setColor(QPalette.Text, QColor(205, 214, 244))
        palette.setColor(QPalette.Button, QColor(49, 50, 68))
        palette.setColor(QPalette.ButtonText, QColor(205, 214, 244))
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(137, 180, 250))
        palette.setColor(QPalette.Highlight, QColor(137, 180, 250))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.app.setPalette(palette)

    def get_user_interval(self):
        """弹出输入框"""
        # QInputDialog 默认样式比较简陋，这里依赖全局样式表美化
        num, ok = QInputDialog.getInt(
            None, 
            "Timention 设置", 
            "请输入提醒间隔（分钟）:", 
            value=30, 
            min=1, 
            max=1440
        )
        if ok:
            return num
        return None

    def start_timer(self):
        # QTimer 单位是毫秒
        ms = self.interval_minutes * 60 * 1000
        print(f"计时开始，将在 {self.interval_minutes} 分钟后提醒...")
        self.timer.start(ms)

    def show_reminder(self):
        """显示全屏提醒"""
        self.overlay.showFullScreen()
        self.overlay.raise_()
        self.overlay.activateWindow()

    def restart_timer(self):
        """重置计时器"""
        print("提醒关闭，计时器重置。")
        self.start_timer()

if __name__ == "__main__":
    TimentionApp()
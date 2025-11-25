import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QDialog, QSpinBox, QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

# 定义箭头图标的 SVG 数据 (无需外部图片文件)
# 向上箭头 (颜色: #cdd6f4)
UP_ARROW_SVG = """
data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23cdd6f4' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M18 15l-6-6-6 6'/%3E%3C/svg%3E
"""
# 向下箭头 (颜色: #cdd6f4)
DOWN_ARROW_SVG = """
data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23cdd6f4' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E
"""

class ReminderOverlay(QWidget):
    """全屏提醒遮罩层"""
    dismissed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet("background-color: #1e1e2e;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("💧 该喝水了")
        self.label.setAlignment(Qt.AlignCenter)
        
        font = QFont("Microsoft YaHei", 72, QFont.Bold)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #cdd6f4;")

        self.sub_label = QLabel("按 ESC 退出程序，按任意键继续工作")
        self.sub_label.setAlignment(Qt.AlignCenter)
        sub_font = QFont("Microsoft YaHei", 14)
        self.sub_label.setFont(sub_font)
        self.sub_label.setStyleSheet("color: #a6adc8; margin-top: 20px;")

        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.sub_label)
        layout.addStretch()

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        else:
            self.hide()
            self.dismissed.emit()


class SettingsDialog(QDialog):
    """自定义美化版设置界面"""
    def __init__(self):
        super().__init__()
        self.value = None
        self.init_ui()

    def init_ui(self):
        # 1. 界面尺寸：进一步放大，更加宽敞
        self.setFixedSize(700, 520)
        self.setWindowTitle("Timention 设置")
        
        # 移除默认帮助按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # 2. 样式表：核心美化逻辑
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #1e1e2e;
            }}
            QLabel {{
                color: #cdd6f4;
                font-family: "Microsoft YaHei";
            }}
            /* 调整框整体样式 */
            QSpinBox {{
                background-color: #313244;
                color: #cdd6f4;
                border: 3px solid #45475a;
                border-radius: 16px;
                padding: 0px 20px; /* 左右内边距 */
                font-size: 64px;   /* 超大字体显示数字 */
                font-family: "Segoe UI", "Microsoft YaHei";
                font-weight: bold;
                selection-background-color: #585b70;
            }}
            QSpinBox:focus {{
                border: 3px solid #89b4fa; /* 聚焦时高亮边框 */
                background-color: #363a4f;
            }}
            
            /* 绘制上下调节按钮 */
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 60px;  /* 按钮加宽 */
                background: #45475a;
                border-radius: 6px;
                margin: 5px; /* 按钮与边框的间距 */
                border: none;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background: #585b70;
            }}
            QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {{
                background: #89b4fa;
            }}

            /* 使用 SVG 绘制图标 */
            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                image: url("{UP_ARROW_SVG.strip()}"); /* 引用上方定义的SVG */
                padding: 4px;
            }}
            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                image: url("{DOWN_ARROW_SVG.strip()}");
                padding: 4px;
            }}

            /* 底部操作按钮 */
            QPushButton {{
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 12px;
                font-family: "Microsoft YaHei";
                font-size: 24px; /* 按钮字体放大 */
                font-weight: bold;
                padding: 16px 32px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #b4befe;
            }}
            QPushButton:pressed {{
                background-color: #74c7ec;
            }}
            QPushButton#cancelBtn {{
                background-color: #45475a;
                color: #cdd6f4;
            }}
            QPushButton#cancelBtn:hover {{
                background-color: #585b70;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(40)
        self.setLayout(layout)

        # 标题
        title_label = QLabel("专注时长设置")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 60px; font-weight: bold; color: #89b4fa; letter-spacing: 2px;")
        layout.addWidget(title_label)

        # 说明文字
        desc_label = QLabel("请设置提醒的时间间隔 (分钟)")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("font-size: 30px; color: #bac2de;")
        layout.addWidget(desc_label)

        # 输入框容器
        input_container = QHBoxLayout()
        input_container.addStretch()
        
        self.spin_box = QSpinBox()
        self.spin_box.setRange(1, 2000)
        self.spin_box.setValue(20)
        self.spin_box.setFixedSize(430, 100)
        self.spin_box.setAlignment(Qt.AlignCenter)
        
        input_container.addWidget(self.spin_box)
        input_container.addStretch()
        layout.addLayout(input_container)

        layout.addStretch()

        # 底部按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)
        
        self.cancel_btn = QPushButton("退 出")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.ok_btn = QPushButton("开始专注")
        self.ok_btn.setCursor(Qt.PointingHandCursor)
        self.ok_btn.clicked.connect(self.accept_value)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)

    def accept_value(self):
        self.value = self.spin_box.value()
        self.accept()


class TimentionApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        self.overlay = None
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_reminder)

        # 启动时显示自定义设置框
        self.interval_minutes = self.get_user_interval()
        
        if self.interval_minutes:
            self.overlay = ReminderOverlay()
            self.overlay.dismissed.connect(self.restart_timer)
            self.start_timer()
            sys.exit(self.app.exec_())
        else:
            sys.exit()

    def get_user_interval(self):
        dialog = SettingsDialog()
        if dialog.exec_() == QDialog.Accepted:
            return dialog.value
        return None

    def start_timer(self):
        ms = self.interval_minutes * 60 * 1000
        print(f"计时开始，将在 {self.interval_minutes} 分钟后提醒...")
        self.timer.start(ms)

    def show_reminder(self):
        if self.overlay:
            self.overlay.showFullScreen()
            self.overlay.raise_()
            self.overlay.activateWindow()
            self.overlay.setFocus()

    def restart_timer(self):
        print("提醒关闭，计时器重置。")
        self.start_timer()

if __name__ == "__main__":
    TimentionApp()
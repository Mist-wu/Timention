import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QDialog, QPushButton, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QPen, QPainterPath


class CustomSpinBox(QWidget):
    """自定义数字调节控件，完全自绘"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 20
        self._min = 1
        self._max = 2000
        self.init_ui()
    
    def init_ui(self):
        self.setFixedSize(430, 100)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 5, 5, 5)
        layout.setSpacing(10)
        self.setLayout(layout)
        
        # 数字显示标签
        self.value_label = QLabel(str(self._value))
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("""
            QLabel {
                color: #cdd6f4;
                font-size: 64px;
                font-family: "Segoe UI", "Microsoft YaHei";
                font-weight: bold;
                background: transparent;
            }
        """)
        layout.addWidget(self.value_label, 1)
        
        # 按钮容器
        btn_container = QVBoxLayout()
        btn_container.setSpacing(6)
        btn_container.setContentsMargins(0, 5, 10, 5)
        
        # 向上按钮
        self.up_btn = ArrowButton("up")
        self.up_btn.setFixedSize(50, 38)
        self.up_btn.clicked.connect(self.increment)
        
        # 向下按钮
        self.down_btn = ArrowButton("down")
        self.down_btn.setFixedSize(50, 38)
        self.down_btn.clicked.connect(self.decrement)
        
        btn_container.addWidget(self.up_btn)
        btn_container.addWidget(self.down_btn)
        
        layout.addLayout(btn_container)
        
        # 整体样式
        self.setStyleSheet("""
            CustomSpinBox {
                background-color: #313244;
                border: 3px solid #45475a;
                border-radius: 16px;
            }
            CustomSpinBox:focus {
                border: 3px solid #89b4fa;
                background-color: #363a4f;
            }
        """)
    
    def value(self):
        return self._value
    
    def setValue(self, val):
        self._value = max(self._min, min(self._max, val))
        self.value_label.setText(str(self._value))
    
    def setRange(self, min_val, max_val):
        self._min = min_val
        self._max = max_val
    
    def increment(self):
        self.setValue(self._value + 1)
    
    def decrement(self):
        self.setValue(self._value - 1)
    
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.increment()
        else:
            self.decrement()


class ArrowButton(QPushButton):
    """带箭头图标的按钮"""
    def __init__(self, direction="up", parent=None):
        super().__init__(parent)
        self.direction = direction
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: #45475a;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background: #585b70;
            }
            QPushButton:pressed {
                background: #89b4fa;
            }
        """)
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 设置画笔
        pen = QPen(QColor("#cdd6f4"))
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        # 计算箭头位置
        w = self.width()
        h = self.height()
        cx = w // 2
        cy = h // 2
        size = 8  # 箭头大小
        
        # 绘制箭头路径
        path = QPainterPath()
        if self.direction == "up":
            path.moveTo(cx - size, cy + size // 2)
            path.lineTo(cx, cy - size // 2)
            path.lineTo(cx + size, cy + size // 2)
        else:
            path.moveTo(cx - size, cy - size // 2)
            path.lineTo(cx, cy + size // 2)
            path.lineTo(cx + size, cy - size // 2)
        
        painter.drawPath(path)
        painter.end()


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
        self.setFixedSize(700, 520)
        self.setWindowTitle("Timention 设置")
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cdd6f4;
                font-family: "Microsoft YaHei";
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 12px;
                font-family: "Microsoft YaHei";
                font-size: 24px;
                font-weight: bold;
                padding: 16px 32px;
                border: none;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton:pressed {
                background-color: #74c7ec;
            }
            QPushButton#cancelBtn {
                background-color: #45475a;
                color: #cdd6f4;
            }
            QPushButton#cancelBtn:hover {
                background-color: #585b70;
            }
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

        # 使用自定义 SpinBox
        input_container = QHBoxLayout()
        input_container.addStretch()
        
        self.spin_box = CustomSpinBox()
        self.spin_box.setRange(1, 2000)
        self.spin_box.setValue(20)
        
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
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class DarkDialogBase(QDialog):
    """Base class for custom dark themed dialogs"""
    def __init__(self, parent=None, title="", width=300, height=160):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(width, height)
        
        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # Container
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: #2D2D33;
                border: 1px solid #555;
                border-radius: 10px;
            }
        """)
        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.container.setGraphicsEffect(shadow)
        
        self.container_layout = QVBoxLayout(self.container)
        self.layout.addWidget(self.container)
        
        # Title
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("color: #FFD700; font-size: 16px; font-weight: bold; border: none;")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.addWidget(self.lbl_title)

class ConfirmationDialog(DarkDialogBase):
    def __init__(self, parent=None, title="Confirm", message="Are you sure?", yes_label="Yes", no_label="No"):
        super().__init__(parent, title, width=320, height=180)
        
        self.result_ok = False
        
        # Message
        self.lbl_msg = QLabel(message)
        self.lbl_msg.setStyleSheet("color: #DDD; font-size: 14px; margin-top: 10px; margin-bottom: 10px; border: none;")
        self.lbl_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_msg.setWordWrap(True)
        self.container_layout.addWidget(self.lbl_msg)
        
        self.container_layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton(no_label)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: #FFF;
                border-radius: 4px;
                padding: 6px 15px;
                min-width: 60px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #555; }
        """)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_ok = QPushButton(yes_label)
        self.btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #FF5722; /* Warning Color by default for confirmation */
                color: #FFF;
                border-radius: 4px;
                padding: 6px 15px;
                min-width: 60px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E64A19; }
        """)
        self.btn_ok.clicked.connect(self.accept_confirm)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addStretch()
        
        self.container_layout.addLayout(btn_layout)
        
    def accept_confirm(self):
        self.result_ok = True
        self.accept()
        
    @staticmethod
    def confirm(parent, title, message, yes_label="确定", no_label="取消"):
        dialog = ConfirmationDialog(parent, title, message, yes_label, no_label)
        dialog.exec()
        return dialog.result_ok


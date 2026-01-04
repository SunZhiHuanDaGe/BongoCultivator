from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QHBoxLayout, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class DarkInputDialog(QDialog):
    def __init__(self, parent=None, title="Input", label="Please enter:"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(300, 160)
        
        self.result_text = ""
        self.result_ok = False
        
        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
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
        
        container_layout = QVBoxLayout(self.container)
        layout.addWidget(self.container)
        
        # Title
        self.lbl_title = QLabel(title)
        self.lbl_title.setStyleSheet("color: #FFD700; font-size: 16px; font-weight: bold; border: none;")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.lbl_title)
        
        # Process Label (Message)
        self.lbl_msg = QLabel(label)
        self.lbl_msg.setStyleSheet("color: #DDD; font-size: 14px; margin-top: 5px; border: none;")
        container_layout.addWidget(self.lbl_msg)
        
        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #1E1E22;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #FFD700;
            }
        """)
        container_layout.addWidget(self.input_field)
        self.input_field.setFocus()
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: #FFF;
                border-radius: 4px;
                padding: 6px;
                min-width: 60px;
            }
            QPushButton:hover { background-color: #555; }
        """)
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_ok = QPushButton("确定")
        self.btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #FFF;
                border-radius: 4px;
                padding: 6px;
                min-width: 60px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        self.btn_ok.clicked.connect(self.accept_input)
        # Allow Enter key
        self.input_field.returnPressed.connect(self.accept_input)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_ok)
        container_layout.addLayout(btn_layout)
        
    def accept_input(self):
        self.result_text = self.input_field.text()
        self.result_ok = True
        self.accept()
        
    @staticmethod
    def get_text(parent, title, label):
        dialog = DarkInputDialog(parent, title, label)
        dialog.exec()
        return dialog.result_text, dialog.result_ok

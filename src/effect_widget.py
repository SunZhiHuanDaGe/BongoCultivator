from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QBrush

class EffectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) # 点击穿透
        self.active = False
        self.phase = 0
        
        # 动画定时器
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_anim)
        
    def start_fire(self):
        self.active = True
        self.anim_timer.start(50) # 20fps
        self.show()
        
    def stop(self):
        self.active = False
        self.anim_timer.stop()
        self.hide()
        
    def update_anim(self):
        self.phase += 0.2
        self.update() # 触发重绘
        
    def paintEvent(self, event):
        if not self.active:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 模拟火焰/光效位置 (假设在图片中间偏下)
        cx = self.width() / 2
        cy = self.height() / 2 + 20 
        
        # 动态半径
        import math
        radius = 40 + math.sin(self.phase) * 5
        alpha = 100 + math.sin(self.phase * 2) * 40
        
        # 径向渐变：中心亮紫 -> 边缘透明
        gradient = QRadialGradient(cx, cy, radius)
        gradient.setColorAt(0, QColor(138, 43, 226, int(alpha))) # 紫罗兰
        gradient.setColorAt(0.6, QColor(75, 0, 130, int(alpha * 0.5))) # 靛蓝
        gradient.setColorAt(1, QColor(0, 0, 0, 0)) # 透明
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(cx - radius), int(cy - radius), int(radius * 2), int(radius * 2))
        
        # 再加一个小一点的核心高光
        core_radius = radius * 0.5
        core_gradient = QRadialGradient(cx, cy + 5, core_radius)
        core_gradient.setColorAt(0, QColor(255, 215, 0, int(alpha + 50))) # 金色核心
        core_gradient.setColorAt(1, QColor(255, 140, 0, 0))
        
        painter.setBrush(QBrush(core_gradient))
        painter.drawEllipse(int(cx - core_radius), int(cy - core_radius + 5), int(core_radius * 2), int(core_radius * 2))

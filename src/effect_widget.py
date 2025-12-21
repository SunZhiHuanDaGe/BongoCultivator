from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPoint, QPointF
from PyQt6.QtGui import QPainter, QColor, QRadialGradient, QBrush
import random
import math

class Particle:
    def __init__(self, x, y, mode):
        self.x = x
        self.y = y
        self.mode = mode # 'work', 'read', 'combat', 'idle'
        self.size = random.uniform(2, 5)
        self.life = 1.0 # 1.0 -> 0.0
        
        # 初始速度
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # 如果是“吸入”模式(WORK)，我们会给它一个向心的加速度，
        # 所以这初始速度其实是生成时的扰动

class EffectWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) # 点击穿透
        self.active = True
        self.current_mode = "idle"
        
        self.particles = []
        
        # 动画定时器
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_anim)
        self.anim_timer.start(33) # ~30fps
        
    def start_fire(self):
        # 兼容旧接口，开启炼丹特效 (Work or Combat?) 
        # 炼丹用 'work' 凑合，或者加个 'alchemy'
        self.set_mode("work")
        
    def set_mode(self, mode):
        self.current_mode = mode
        if mode == "idle":
            self.show()
        else:
            self.show()
            
    def stop(self):
        self.active = False
        self.hide()
        
    def update_anim(self):
        if not self.active:
            return
            
        # 1. 生成新粒子
        self.spawn_particles()
        
        # 2. 更新粒子位置
        target_x = self.width() / 2
        target_y = self.height() / 2 + 20 # 身体中心
        
        dead_particles = []
        for p in self.particles:
            p.life -= 0.02
            
            if self.current_mode == "work":
                # 吸入模式: 强力向心移动
                dx = target_x - p.x
                dy = target_y - p.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 5:
                    p.x += dx * 0.1
                    p.y += dy * 0.1
                else:
                    p.life = 0 # 吸进去了，消失
                    
            elif self.current_mode == "combat":
                # 爆发模式: 向外扩散 + 震动
                p.x += p.vx * 2
                p.y += p.vy * 2
                pass
                
            elif self.current_mode == "read":
                # 漂浮模式: 向上飘（文字气泡感）
                p.y -= 0.5
                p.x += math.sin(p.y * 0.1) * 0.5
                
            else: # idle
                # 缓慢漂浮
                p.x += p.vx * 0.2
                p.y += p.vy * 0.2
            
            if p.life <= 0:
                dead_particles.append(p)
                
        for p in dead_particles:
            self.particles.remove(p)
            
        self.update() # 触发重绘
        
    def spawn_particles(self):
        # 根据模式决定生成速率
        rate = 0.1 # idle
        if self.current_mode == "work": rate = 0.8
        elif self.current_mode == "read": rate = 0.3
        elif self.current_mode == "combat": rate = 1.0
        
        if random.random() < rate:
            # 生成位置
            w, h = self.width(), self.height()
            
            if self.current_mode == "work":
                # 从边缘生成
                if random.random() < 0.5:
                    x = random.choice([0, w])
                    y = random.uniform(0, h)
                else:
                    x = random.uniform(0, w)
                    y = random.choice([0, h])
            else:
                # 从中心附近生成
                x = w/2 + random.uniform(-30, 30)
                y = h/2 + random.uniform(-30, 30)
                
            self.particles.append(Particle(x, y, self.current_mode))
            
            # 限制数量
            if len(self.particles) > 100:
                self.particles.pop(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for p in self.particles:
            alpha = int(p.life * 255)
            
            color = QColor(255, 255, 255, alpha)
            if self.current_mode == "work":
                color = QColor(100, 200, 255, alpha) # 蓝光
            elif self.current_mode == "read":
                color = QColor(200, 255, 200, alpha) # 绿意
            elif self.current_mode == "combat":
                color = QColor(255, 100, 100, alpha) # 红光
            else: # idle
                color = QColor(255, 215, 0, alpha) # 金光
                
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(p.x, p.y), p.size, p.size)

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QBrush
import random
import math

class Particle:
    def __init__(self, x, y, vx, vy, color, size, life, behavior=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.behavior = behavior  # function(particle, widget_width, widget_height)

    def update(self, w, h):
        self.x += self.vx
        self.y += self.vy
        self.life -= 0.02
        if self.behavior:
            self.behavior(self, w, h)

class EffectWidget(QWidget):
    # Signal to request screen shake (intensity, duration_ms)
    request_shake = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # Click through
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)
        self.setStyleSheet("background: transparent;")
        self.active = True
        self.current_mode = "idle"
        
        self.particles = []
        
        # Animation timer
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_anim)
        self.anim_timer.start(33)  # ~30fps

    def set_mode(self, mode):
        self.current_mode = mode
        self.show()

    def stop(self):
        # Don't completely stop updating (we might have one-shot particles like clicks alive)
        # Just set mode to None or similar if we want to stop background generation
        self.current_mode = "none"
        # self.hide() # Don't hide, or particles disappear instantly

    def start_fire(self):
        self.set_mode("alchemy")

    def emit_click_effect(self, x, y):
        """Spawns a burst of particles at x, y."""
        for _ in range(8):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Simple expanding particle
            p = Particle(
                x=x, y=y,
                vx=vx, vy=vy,
                color=QColor(255, 255, 255),
                size=random.uniform(2, 4),
                life=1.0
            )
            self.particles.append(p)

    def emit_heart_effect(self, x, y):
        """Spawns floating heart-colored bubbles."""
        for _ in range(5):
            vx = random.uniform(-1, 1)
            vy = random.uniform(-1, -3)
            p = Particle(
                x=x, y=y,
                vx=vx, vy=vy,
                color=QColor(255, 105, 180), # HotPink
                size=random.uniform(4, 8),
                life=1.5,
                behavior=lambda p, w, h: setattr(p, 'y', p.y + p.vy) # simple float up
            )
            self.particles.append(p)

    def trigger_tribulation(self):
        """Lightning and shake effects for tribulation."""
        self.set_mode("tribulation")
        self.request_shake.emit(10, 500) # Shake intensity 10, 500ms
        
        # Spawn some immediate lightning bolts (simulated by lines or fast particles)
        # For now, just chaotic particles
        for _ in range(20):
            self.spawn_particle(force_mode="tribulation")

    def trigger_breakthrough_success(self):
        """Golden aura explosion."""
        self.request_shake.emit(5, 300)
        c_x, c_y = self.width() / 2, self.height() / 2
        for _ in range(50):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            p = Particle(
                x=c_x, y=c_y,
                vx=vx, vy=vy,
                color=QColor(255, 215, 0), # Gold
                size=random.uniform(3, 6),
                life=1.5
            )
            self.particles.append(p)

    def update_anim(self):
        if not self.isVisible():
            return
            
        # 1. Spawn background particles based on mode
        self.spawn_background_particles()
        
        # 2. Update all particles
        w, h = self.width(), self.height()
        alive_particles = []
        for p in self.particles:
            p.update(w, h)
            if p.life > 0:
                alive_particles.append(p)
        self.particles = alive_particles
        
        if not self.particles and self.current_mode == "none":
             pass # Could hide here if needed

        self.update()

    def spawn_background_particles(self):
        mode = self.current_mode
        rate = 0.0
        if mode == "idle": rate = 0.1
        elif mode == "work": rate = 0.8
        elif mode == "read": rate = 0.3
        elif mode == "combat": rate = 1.0
        elif mode == "alchemy": rate = 0.8
        elif mode == "tribulation": rate = 2.0
        
        if random.random() < rate:
            self.spawn_particle(mode)

    def spawn_particle(self, force_mode=None):
        mode = force_mode or self.current_mode
        w, h = self.width(), self.height()
        cx, cy = w/2, h/2 + 20

        if mode == "work" or mode == "alchemy":
            # Implode (suck in)
            if random.random() < 0.5:
                x = random.choice([0, w])
                y = random.uniform(0, h)
            else:
                x = random.uniform(0, w)
                y = random.choice([0, h])
            
            # Velocity towards center already handled in update? 
            # Let's set initial velocity to 0 and handle logic in behavior if we want complexity,
            # but simpler to just set velocity here.
            
            # Allow logic to be in valid 'behavior' callbacks or keep simple logic here.
            # To obtain the 'suck in' effect, we need dynamic velocity updates (acceleration).
            # So we attach a behavior.
            
            def suck_behavior(p, w, h):
                tx, ty = w/2, h/2 + 20
                dx = tx - p.x
                dy = ty - p.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < 10:
                    p.life = 0
                else:
                    p.x += dx * 0.05
                    p.y += dy * 0.05

            p = Particle(x, y, 0, 0, QColor(100, 200, 255), random.uniform(2, 4), 1.0, suck_behavior)
            if mode == "alchemy":
                p.color = QColor(255, 100, 50) # Orange fire
            self.particles.append(p)

        elif mode == "read":
            # Float up
            x = cx + random.uniform(-30, 30)
            y = cy + random.uniform(-30, 30)
            
            def float_behavior(p, w, h):
                p.x += math.sin(p.y * 0.1) * 0.5
            
            p = Particle(x, y, 0, -0.5, QColor(200, 255, 200), random.uniform(2, 4), 1.0, float_behavior)
            self.particles.append(p)

        elif mode == "combat":
            # Chaos / Spark
            x = cx + random.uniform(-20, 20)
            y = cy + random.uniform(-20, 20)
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(1, 3)
            p = Particle(x, y, math.cos(angle)*speed, math.sin(angle)*speed, QColor(255, 100, 100), random.uniform(2, 5), 0.8)
            self.particles.append(p)

        elif mode == "idle":
            # Gentle float
            x = cx + random.uniform(-30, 30)
            y = cy + random.uniform(-30, 30)
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(0.2, 0.5)
            p = Particle(x, y, math.cos(angle)*speed, math.sin(angle)*speed, QColor(255, 215, 0), random.uniform(2, 4), 1.0)
            self.particles.append(p)

        elif mode == "tribulation":
            # Lightning bolts? Just fast blue/purple particles for now
            x = random.uniform(0, w)
            y = 0
            # Strike down
            p = Particle(x, y, random.uniform(-2, 2), random.uniform(10, 20), QColor(200, 200, 255), random.uniform(1, 3), 0.5)
            self.particles.append(p)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for p in self.particles:
            # Fade out
            alpha = int(p.life * 255)
            if alpha < 0: alpha = 0
            
            c = p.color
            c.setAlpha(alpha)
            
            painter.setBrush(QBrush(c))
            painter.setPen(Qt.PenStyle.NoPen)
            
            # If tribulation, maybe draw lines? For now circles are fine.
            painter.drawEllipse(QPointF(p.x, p.y), p.size, p.size)

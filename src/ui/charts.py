from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QPainterPath

class SimpleChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_values = []
        self.data_labels = []
        self.bar_color = QColor(255, 215, 0) # Gold
        self.text_color = QColor(136, 136, 136) # #888
        self.grid_color = QColor(68, 68, 68) # #444
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Important if parent is transparent

    def set_data(self, values, labels=None):
        self.data_values = values
        self.data_labels = labels if labels else []
        self.update() # Trigger repaint

class BarChartWidget(SimpleChartWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # Margins
        margin_left = 30
        margin_bottom = 20
        margin_top = 10
        margin_right = 10
        
        draw_w = w - margin_left - margin_right
        draw_h = h - margin_bottom - margin_top
        
        if not self.data_values:
            return

        max_val = max(self.data_values) if self.data_values else 1
        if max_val == 0: max_val = 1
        
        count = len(self.data_values)
        if count == 0: return
        
        bar_width = draw_w / count
        gap = bar_width * 0.2
        real_bar_width = bar_width - gap
        
        # Draw Axes
        pen_grid = QPen(self.grid_color)
        pen_grid.setWidth(1)
        painter.setPen(pen_grid)
        
        # Y Axis Line
        painter.drawLine(margin_left, margin_top, margin_left, h - margin_bottom)
        # X Axis Line
        painter.drawLine(margin_left, h - margin_bottom, w - margin_right, h - margin_bottom)
        
        # Draw Bars
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.bar_color))
        
        for i, val in enumerate(self.data_values):
            bar_h = (val / max_val) * draw_h
            
            x = margin_left + (i * bar_width) + (gap / 2)
            y = h - margin_bottom - bar_h
            
            painter.drawRect(int(x), int(y), int(real_bar_width), int(bar_h))
            
        # Draw Labels (X Axis) - Optional: Sparse labels
        painter.setPen(self.text_color)
        font = painter.font()
        font.setPixelSize(10)
        painter.setFont(font)
        
        # Only show a few labels
        step = 1
        if count > 10:
            step = count // 6 + 1
            
        if self.data_labels:
            for i in range(0, count, step):
                if i < len(self.data_labels):
                    lbl = str(self.data_labels[i])
                    x = margin_left + (i * bar_width)
                    y = h - 2 
                    # Draw text centered on bar slot
                    rect = painter.boundingRect(int(x), int(y - 15), int(bar_width), 15, Qt.AlignmentFlag.AlignCenter, lbl)
                    painter.drawText(int(x + bar_width/2 - rect.width()/2), int(h - 5), lbl)

class LineChartWidget(SimpleChartWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_color = QColor(0, 255, 127) # SpringGreen
        self.fill_color = QColor(0, 255, 127, 40) # Semi-transparent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        margin_left = 30
        margin_bottom = 20
        margin_top = 10
        margin_right = 10
        
        draw_w = w - margin_left - margin_right
        draw_h = h - margin_bottom - margin_top
        
        if not self.data_values:
            return

        max_val = max(self.data_values) if self.data_values else 1
        if max_val == 0: max_val = 1
        
        count = len(self.data_values)
        if count < 2: return # Need at least 2 points for a line
        
        step_x = draw_w / (count - 1)
        
        # Calculate Points
        points = []
        for i, val in enumerate(self.data_values):
            x = margin_left + (i * step_x)
            y = h - margin_bottom - ((val / max_val) * draw_h)
            points.append(QPointF(x, y))
            
        # Draw Area (Fill)
        path = QPainterPath()
        path.moveTo(margin_left, h - margin_bottom) # Start bottom-left
        for p in points:
            path.lineTo(p)
        path.lineTo(points[-1].x(), h - margin_bottom) # End bottom-right
        path.closeSubpath()
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.fill_color))
        painter.drawPath(path)
        
        # Draw Line
        pen_line = QPen(self.line_color)
        pen_line.setWidth(2)
        painter.setPen(pen_line)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPolyline(points)
        
        # Draw Points
        painter.setBrush(QBrush(self.line_color))
        for p in points:
            painter.drawEllipse(p, 3, 3)
            
        # Axis lines (Simple)
        pen_grid = QPen(self.grid_color)
        pen_grid.setWidth(1)
        painter.setPen(pen_grid)
        painter.drawLine(margin_left, margin_top, margin_left, h - margin_bottom)
        painter.drawLine(margin_left, h - margin_bottom, w - margin_right, h - margin_bottom)
        
        # Labels
        painter.setPen(self.text_color)
        font = painter.font()
        font.setPixelSize(10)
        painter.setFont(font)
        
        step = 1
        if count > 8:
            step = count // 5 + 1
            
        if self.data_labels:
            for i in range(0, count, step):
                if i < len(self.data_labels):
                    lbl = str(self.data_labels[i])
                    x = margin_left + (i * step_x) - 15
                    painter.drawText(int(x), int(h - 5), 30, 15, Qt.AlignmentFlag.AlignCenter, lbl)

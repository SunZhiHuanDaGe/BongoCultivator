from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QHBoxLayout, QMessageBox, QGraphicsDropShadowEffect, QListWidgetItem
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QAction
from src.logger import logger

class InventoryWindow(QWidget):
    def __init__(self, cultivator, parent=None):
        super().__init__(parent)
        
        self.setWindowFlags(
            Qt.WindowType.Tool | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.cultivator = cultivator
        self.item_manager = cultivator.item_manager
        self.resize(260, 350)
        
        self.init_ui()

    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 顶部：灵石显示
        self.money_label = QLabel(f"灵石: {self.cultivator.money}")
        self.money_label.setStyleSheet("color: #FFD700; font-size: 14px; font-weight: bold; font-family: 'Microsoft YaHei';")
        self.money_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.money_label)
        
        # 中部：物品列表
        self.item_list = QListWidget()
        self.item_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 0, 0, 50);
                border: 1px solid rgba(255, 215, 0, 50);
                border-radius: 4px;
                color: white;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid rgba(255, 255, 255, 20);
            }
            QListWidget::item:selected {
                background-color: rgba(255, 215, 0, 40);
                color: #FFD700;
            }
        """)
        self.refresh_list()
        self.item_list.itemClicked.connect(self.show_item_detail)
        main_layout.addWidget(self.item_list)
        
        # 底部：详情与操作
        self.detail_label = QLabel("选择物品...")
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("color: #DDD; font-size: 12px; padding: 5px; min-height: 40px;")
        main_layout.addWidget(self.detail_label)
        
        btn_layout = QHBoxLayout()
        
        self.use_btn = QPushButton("使用")
        self.use_btn.setEnabled(False)
        self.use_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 215, 0, 20);
                border: 1px solid #FFD700;
                color: #FFD700;
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 215, 0, 60);
            }
            QPushButton:disabled {
                border-color: #666;
                color: #666;
                background-color: transparent;
            }
        """)
        self.use_btn.clicked.connect(self.use_item)
        
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #AAA;
                color: #AAA;
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton:hover {
                border-color: white;
                color: white;
            }
        """)
        close_btn.clicked.connect(self.hide)
        
        btn_layout.addWidget(self.use_btn)
        btn_layout.addWidget(close_btn)
        main_layout.addLayout(btn_layout)
        
        self.setLayout(main_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制半透明背景
        bg_color = QColor(30, 30, 35, 230) # 深色背景
        border_color = QColor(255, 215, 0, 180) # 金色边框
        
        rect = self.rect().adjusted(2, 2, -2, -2)
        
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(border_color, 1.5))
        painter.drawRoundedRect(rect, 10, 10)

    def refresh_list(self):
        self.item_list.clear()
        # cultivator.inventory store keys as item_id now
        for item_id, count in self.cultivator.inventory.items():
            if count > 0:
                item_data = self.item_manager.get_item(item_id)
                name = item_data["name"] if item_data else item_id
                
                list_item = QListWidgetItem(f"{name} x{count}")
                list_item.setData(Qt.ItemDataRole.UserRole, item_id) # Store ID
                self.item_list.addItem(list_item)
                
        self.money_label.setText(f"灵石: {self.cultivator.money}")

    def show_item_detail(self, item):
        item_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_selected_id = item_id
        
        info = self.item_manager.get_item(item_id)
        if not info:
            return
            
        name = info.get("name", "未知")
        desc = info.get("desc", "没有描述")
        item_type = info.get("type", "misc")
        
        type_str = ""
        if item_type == "material": type_str = "[材料]"
        elif item_type == "consumable": type_str = "[消耗品]"
        elif item_type == "junk": type_str = "[杂物]"
        elif item_type == "breakthrough": type_str = "[珍稀]"
        
        self.detail_label.setText(f"【{name}】{type_str}\n{desc}")
        
        # 只有 consumable 和 breakthrough 可以使用
        can_use = item_type in ["consumable", "breakthrough", "buff"]
        self.use_btn.setEnabled(can_use)

    def use_item(self):
        if not hasattr(self, 'current_selected_id'):
            return
            
        item_id = self.current_selected_id
        if self.cultivator.inventory.get(item_id, 0) <= 0:
            return

        info = self.item_manager.get_item(item_id)
        if not info: return
        
        item_type = info.get("type", "misc")
        effects = info.get("effect", {})
        
        msg = ""
        used_success = False
        
        if item_type == "consumable" or item_type == "buff":
            # 处理各类效果
            if "exp" in effects:
                val = effects["exp"]
                self.cultivator.gain_exp(val)
                msg = f"服用了 {info['name']}, 修为增加 {val}!"
                used_success = True
                
            elif "heal" in effects:
                val = effects["heal"]
                msg = f"恢复了 {val} 点状态 (暂无实效)"
                used_success = True
                
            elif "buff" in effects:
                buff_name = effects["buff"]
                duration = effects.get("duration", 0)
                msg = f"获得了增益 [{buff_name}] 持续 {duration//60} 分钟 (开发中)"
                used_success = True
                
            elif "stat_body" in effects:
                val = effects["stat_body"]
                self.cultivator.modify_stat("body", val)
                msg = f"体魄增加了 {val} 点 (永久)"
                used_success = True
                
            elif "mind_heal" in effects:
                val = effects["mind_heal"]
                self.cultivator.modify_stat("mind", -val)
                msg = f"心魔减少了 {val} 点"
                used_success = True
                
            elif "affection" in effects:
                val = effects["affection"]
                self.cultivator.modify_stat("affection", val)
                msg = f"宠物好感度增加 {val} 点"
                used_success = True
                
            elif "action" in effects:
                action = effects["action"]
                if action == "reset_talent":
                    self.cultivator.modify_stat("reset_talent", 0)
                    msg = "已洗髓伐骨，天赋点已重置！"
                    used_success = True
                
            # Fallback
            if not used_success:
                 msg = "物品已使用，但好像没发生什么。"
                 used_success = True
                 
        elif item_type == "breakthrough":
             # 突破逻辑
             chance_percent = effects.get("chance", 0)
             base_rate = chance_percent / 100.0
             
             success, res_msg = self.cultivator.attempt_breakthrough(base_rate)
             msg = res_msg
             
             # 如果成功，consumable 逻辑下面会自动减1; 
             # 但如果 "can_breakthrough" 返回 False (修为不够)，虽然 used_success=True 会导致扣减，这不太合理。
             # 我们应该只在尝试了突破（无论成败）时才扣减。
             # 如果返回 "修为不足"，则不扣减。
             
             if not success and "修为" in res_msg: #  有点蹩脚的判断，但暂时有效
                 msg = res_msg
                 used_success = False # 不扣物品
             else:
                 used_success = True # 尝试了，扣物品
             
        if used_success:
            self.cultivator.inventory[item_id] -= 1
            logger.info(f"使用了物品: {info['name']}")
            
            self.detail_label.setText(msg)
            self.refresh_list()
            
            if self.cultivator.inventory[item_id] <= 0:
                self.detail_label.setText("物品已用完")
                self.use_btn.setEnabled(False)

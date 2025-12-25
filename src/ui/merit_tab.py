from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QGridLayout, 
                             QTabWidget, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from src.services.achievement_manager import achievement_manager

class MeritTab(QWidget):
    def __init__(self, cultivator, parent=None):
        super().__init__(parent)
        self.cultivator = cultivator
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. Header with Equipped Title
        self.header_frame = QFrame()
        self.header_frame.setStyleSheet("background-color: rgba(0, 0, 0, 50); border-radius: 8px;")
        header_layout = QHBoxLayout(self.header_frame)
        
        self.lbl_title_preview = QLabel("当前法相: 无")
        self.lbl_title_preview.setStyleSheet("color: #FFD700; font-size: 14px; font-weight: bold;")
        
        self.btn_unequip = QPushButton("卸下")
        self.btn_unequip.setFixedSize(60, 24)
        self.btn_unequip.clicked.connect(self.on_unequip_clicked)
        self.btn_unequip.setStyleSheet("background-color: #555; color: white; border: none; border-radius: 4px;")
        
        header_layout.addWidget(self.lbl_title_preview)
        header_layout.addWidget(self.btn_unequip)
        layout.addWidget(self.header_frame)
        
        # 2. Categories (TabWidget inside Tab? Or just filter buttons?)
        # Achievement lists can be long. Let's use filter buttons.
        filter_layout = QHBoxLayout()
        self.btn_all = self.create_filter_btn("全部", True)
        self.btn_action = self.create_filter_btn("行道")
        self.btn_time = self.create_filter_btn("岁月")
        self.btn_chance = self.create_filter_btn("机缘")
        self.btn_fortune = self.create_filter_btn("财阀")
        
        filter_layout.addWidget(self.btn_all)
        filter_layout.addWidget(self.btn_action)
        filter_layout.addWidget(self.btn_time)
        filter_layout.addWidget(self.btn_chance)
        filter_layout.addWidget(self.btn_fortune)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # 3. Scroll Area for List
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.card_layout = QVBoxLayout(self.scroll_content)
        self.card_layout.setSpacing(10)
        self.card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll.setWidget(self.scroll_content)
        layout.addWidget(self.scroll)
        
        self.current_filter = "all"
        self.refresh_list()
        
    def create_filter_btn(self, text, active=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(active)
        btn.setFixedSize(60, 24)
        btn.setStyleSheet(self.get_btn_style(active))
        btn.clicked.connect(lambda: self.on_filter_clicked(btn))
        return btn
        
    def get_btn_style(self, active):
        if active:
            return "QPushButton { background-color: #FFD700; color: #000; border: none; border-radius: 12px; font-weight: bold; }"
        return "QPushButton { background-color: rgba(255, 255, 255, 20); color: #AAA; border: none; border-radius: 12px; } QPushButton:hover { color: #FFF; }"

    def on_filter_clicked(self, sender):
        # Reset all
        for btn in [self.btn_all, self.btn_action, self.btn_time, self.btn_chance, self.btn_fortune]:
            btn.setChecked(False)
            btn.setStyleSheet(self.get_btn_style(False))
        
        # Set active
        sender.setChecked(True)
        sender.setStyleSheet(self.get_btn_style(True))
        
        # Map text to category code
        txt = sender.text()
        map_code = {"全部": "all", "行道": "action", "岁月": "time", "机缘": "chance", "财阀": "fortune"}
        self.current_filter = map_code.get(txt, "all")
        
        self.refresh_list()
        
    def on_unequip_clicked(self):
        if self.cultivator:
            self.cultivator.unequip_title()
            self.refresh_header()
            self.refresh_list() # Re-enable equip button

    def refresh_header(self):
        if not self.cultivator: return
        t_id = self.cultivator.equipped_title
        if t_id:
            eff = achievement_manager.get_title_effect(t_id)
            name = eff.get('name', t_id) if eff else t_id
            self.lbl_title_preview.setText(f"当前法相: {name}")
            self.btn_unequip.setVisible(True)
        else:
            self.lbl_title_preview.setText("当前法相: 无")
            self.btn_unequip.setVisible(False)

    def refresh_list(self):
        # Clear existing
        while self.card_layout.count():
            item = self.card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        self.refresh_header()
        
        achievements = achievement_manager.get_all_achievements()
        
        for ach in achievements:
            # Filter
            if self.current_filter != 'all' and ach['category'] != self.current_filter:
                continue
                
            # Render Card
            card = AchievementCard(ach, self.cultivator)
            card.claim_clicked.connect(self.on_claim)
            card.equip_clicked.connect(self.on_equip)
            self.card_layout.addWidget(card)

    def on_claim(self, ach_id):
        success, msg = achievement_manager.claim_reward(self.cultivator, ach_id)
        if success:
            QMessageBox.information(self, "天道赐福", msg)
            self.refresh_list()
        else:
            QMessageBox.warning(self, "领取失败", msg)

    def on_equip(self, title_id):
        self.cultivator.equip_title(title_id)
        self.refresh_list()


class AchievementCard(QFrame):
    claim_clicked = pyqtSignal(str)
    equip_clicked = pyqtSignal(str)
    
    def __init__(self, data, cultivator):
        super().__init__()
        self.data = data
        self.cultivator = cultivator
        
        # Style based on status
        # 0: Locked, 1: Unlocked, 2: Claimed
        status = data['status']
        
        bg_color = "rgba(40, 40, 45, 150)"
        border_color = "#555"
        
        if status == 1: # Unlocked but not claimed
            border_color = "#FFD700"
            bg_color = "rgba(60, 50, 20, 180)"
        elif status == 2: # Claimed
            bg_color = "rgba(30, 30, 30, 100)"
            border_color = "#333"
            
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 6px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        
        # Icon / Status
        lbl_icon = QLabel("🔒")
        if status >= 1: lbl_icon.setText("✨")
        if status == 2: lbl_icon.setText("✅")
        lbl_icon.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        layout.addWidget(lbl_icon)
        
        # Info
        info_layout = QVBoxLayout()
        name_txt = data['name']
        if data['is_hidden'] and status == 0:
            name_txt = "???"
        
        lbl_name = QLabel(name_txt)
        lbl_name.setStyleSheet("color: #DDD; font-weight: bold; font-size: 14px; border: none; background: transparent;")
        
        desc_txt = data['desc']
        if data['is_hidden'] and status == 0:
            desc_txt = "此成就包含天机，除此之外不可言说。"
            
        lbl_desc = QLabel(desc_txt)
        lbl_desc.setStyleSheet("color: #888; font-size: 12px; border: none; background: transparent;")
        lbl_desc.setWordWrap(True)
        
        info_layout.addWidget(lbl_name)
        info_layout.addWidget(lbl_desc)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        
        # Progress / Action
        action_layout = QVBoxLayout()
        
        # Progress text (Mock for now, actual progress needs fetch from achievements table or stats)
        # We did not pass current stats to this widget, so we can't show "53/100".
        # We can only show threshold.
        if status == 0 and not data['is_hidden']:
            lbl_prog = QLabel(f"目标: {data['threshold']}")
            lbl_prog.setStyleSheet("color: #666; font-size: 10px; border: none; background: transparent;")
            action_layout.addWidget(lbl_prog)
            
        if status == 1:
            btn_claim = QPushButton("领取")
            btn_claim.setFixedSize(60, 24)
            btn_claim.setStyleSheet("background-color: #FFD700; color: black; border-radius: 4px; font-weight: bold;")
            btn_claim.clicked.connect(lambda: self.claim_clicked.emit(data['id']))
            action_layout.addWidget(btn_claim)
            
        elif status == 2 and data['reward_type'] == 'title':
            # Equip button
            is_equipped = (self.cultivator.equipped_title == data['reward_value'])
            btn_equip = QPushButton("已佩戴" if is_equipped else "佩戴")
            btn_equip.setFixedSize(60, 24)
            btn_equip.setEnabled(not is_equipped)
            
            style = "background-color: #4CAF50; color: white; border-radius: 4px;"
            if is_equipped:
                 style = "background-color: #333; color: #888; border-radius: 4px;"
                 
            btn_equip.setStyleSheet(style)
            if not is_equipped:
                btn_equip.clicked.connect(lambda: self.equip_clicked.emit(data['reward_value']))
            action_layout.addWidget(btn_equip)
            
        elif status == 2:
            lbl_done = QLabel("已领取")
            lbl_done.setStyleSheet("color: #555; font-size: 11px; border: none; background: transparent;")
            action_layout.addWidget(lbl_done)
            
        layout.addLayout(action_layout)

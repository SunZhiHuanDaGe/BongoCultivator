from enum import Enum

class PetState(Enum):
    IDLE = 0      # 闭关/打坐 (No Input)
    WORK = 1      # 历练 (Keyboard Activity)
    READ = 2      # 悟道 (Mouse Activity)
    COMBAT = 3    # 斗法 (High Intensity)
    ALCHEMY = 4   # 炼丹
    ASCEND = 5    # 渡劫

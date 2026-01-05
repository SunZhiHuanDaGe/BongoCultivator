"""
进度导出/导入管理器 - "轮回转世"功能
Plan 46: 实现版本无关的进度迁移
"""
import json
import time
from datetime import datetime
from typing import Tuple
from src.logger import logger


class ProgressExporter:
    """进度导出/导入管理器"""
    
    EXPORT_VERSION = "1.0"
    GAME_VERSION = "0.46.0"  # 可以后续从配置读取
    
    @staticmethod
    def export_progress(cultivator, filepath: str) -> Tuple[bool, str]:
        """
        导出进度到 JSON 文件
        :param cultivator: Cultivator 实例
        :param filepath: 导出文件路径
        :return: (success, message)
        """
        try:
            from src.database import db_manager
            from src.models import Achievement
            from sqlmodel import select
            
            current_time = int(time.time())
            readable_time = datetime.fromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S")
            
            # 构建导出数据
            export_data = {
                "meta": {
                    "version": ProgressExporter.EXPORT_VERSION,
                    "game_version": ProgressExporter.GAME_VERSION,
                    "export_time": current_time,
                    "export_time_readable": readable_time
                },
                "player": {
                    "layer_index": cultivator.layer_index,
                    "exp": cultivator.exp,
                    "money": cultivator.money,
                    "body": cultivator.body,
                    "mind": cultivator.mind,
                    "luck": cultivator.affection,
                    "talent_points": cultivator.talent_points,
                    "talents": cultivator.talents.copy(),
                    "death_count": cultivator.death_count,
                    "legacy_points": cultivator.legacy_points,
                    "equipped_title": cultivator.equipped_title,
                    "daily_reward_claimed": cultivator.daily_reward_claimed
                },
                "inventory": cultivator.inventory.copy(),
                "used_once_items": list(cultivator.used_once_items),
                "market": []
            }
            
            # 导出坊市数据
            for goods in cultivator.market_goods:
                export_data["market"].append({
                    "id": goods.get("id"),
                    "price": goods.get("price"),
                    "discount": goods.get("discount")
                })
            
            # 从数据库导出成就数据
            achievements_list = []
            try:
                with db_manager.get_session() as session:
                    achievements = session.exec(select(Achievement)).all()
                    for ach in achievements:
                        # 只导出状态不为0的（已解锁或进行中）
                        if ach.status > 0:
                            achievements_list.append({
                                "id": ach.id,
                                "status": ach.status,
                                "unlocked_at": ach.unlocked_at
                            })
            except Exception as e:
                logger.warning(f"导出成就数据失败: {e}")
            
            export_data["achievements"] = achievements_list
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"轮回留痕完成: {filepath}")
            return True, f"轮回之力已封印！\n进度已保存至:\n{filepath}"
            
        except Exception as e:
            logger.error(f"导出进度失败: {e}")
            return False, f"封印失败！\n错误: {str(e)}"
    
    @staticmethod
    def validate_import_data(data: dict) -> Tuple[bool, str]:
        """
        验证导入数据的基本结构
        :return: (is_valid, message)
        """
        # 检查必需的顶层键
        required_keys = ["meta", "player"]
        for key in required_keys:
            if key not in data:
                return False, f"数据格式错误：缺少 '{key}' 字段"
        
        # 检查 meta 信息
        if "version" not in data.get("meta", {}):
            return False, "数据格式错误：缺少版本信息"
        
        # 检查 player 必需字段
        player = data.get("player", {})
        player_required = ["layer_index", "exp", "money"]
        for key in player_required:
            if key not in player:
                return False, f"数据格式错误：缺少玩家属性 '{key}'"
        
        return True, "验证通过"
    
    @staticmethod
    def import_progress(cultivator, filepath: str) -> Tuple[bool, str]:
        """
        从 JSON 文件导入进度
        :param cultivator: Cultivator 实例
        :param filepath: 导入文件路径
        :return: (success, message)
        """
        try:
            # 读取文件
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 验证数据结构
            is_valid, msg = ProgressExporter.validate_import_data(data)
            if not is_valid:
                return False, msg
            
            from src.database import db_manager
            from src.models import (
                PlayerStatus, PlayerInventory, MarketStock, 
                Achievement, UsedOnceItem
            )
            from sqlmodel import select, delete
            
            player_data = data.get("player", {})
            meta = data.get("meta", {})
            
            logger.info(f"开始导入存档 (版本 {meta.get('version')}, 导出时间 {meta.get('export_time_readable')})")
            
            # 更新 Cultivator 实例属性
            cultivator.layer_index = player_data.get("layer_index", 0)
            cultivator.exp = player_data.get("exp", 0)
            cultivator.money = max(0, player_data.get("money", 0))
            cultivator.body = max(1, player_data.get("body", 10))
            cultivator.mind = max(0, min(100, player_data.get("mind", 0)))
            cultivator.affection = max(0, min(100, player_data.get("luck", 0)))
            cultivator.talent_points = player_data.get("talent_points", 0)
            cultivator.talents = player_data.get("talents", {"exp": 0, "drop": 0})
            cultivator.death_count = player_data.get("death_count", 0)
            cultivator.legacy_points = player_data.get("legacy_points", 0)
            cultivator.equipped_title = player_data.get("equipped_title")
            cultivator.daily_reward_claimed = player_data.get("daily_reward_claimed")
            
            # 导入背包
            cultivator.inventory = data.get("inventory", {})
            
            # 导入一面之缘物品
            cultivator.used_once_items = set(data.get("used_once_items", []))
            
            # 导入坊市
            cultivator.market_goods = []
            for market_item in data.get("market", []):
                cultivator.market_goods.append({
                    "id": market_item.get("id"),
                    "price": market_item.get("price"),
                    "discount": market_item.get("discount", 1.0)
                })
            
            # 如果没有坊市数据，刷新一下
            if not cultivator.market_goods:
                cultivator.refresh_market()
            
            # 更新数据库 - 成就
            achievements_data = data.get("achievements", [])
            if achievements_data:
                try:
                    with db_manager.get_session() as session:
                        for ach_data in achievements_data:
                            ach_id = ach_data.get("id")
                            if not ach_id:
                                continue
                            
                            ach = session.get(Achievement, ach_id)
                            if ach:
                                ach.status = ach_data.get("status", 0)
                                ach.unlocked_at = ach_data.get("unlocked_at")
                                session.add(ach)
                            else:
                                logger.warning(f"成就 {ach_id} 在当前版本中不存在，已跳过")
                        
                        session.commit()
                except Exception as e:
                    logger.warning(f"导入成就失败: {e}")
            
            # 保存所有数据到数据库
            cultivator.save_data()
            
            logger.info("轮回归来完成！")
            return True, "轮回成功！\n道友已返归本源。"
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}")
            return False, f"文件格式错误！\n无法解析 JSON 数据"
        except FileNotFoundError:
            logger.error(f"文件不存在: {filepath}")
            return False, f"文件不存在！\n请检查文件路径"
        except Exception as e:
            logger.error(f"导入进度失败: {e}")
            return False, f"转世失败！\n错误: {str(e)}"
    
    @staticmethod
    def get_default_filename() -> str:
        """
        获取默认的导出文件名
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"BongoCultivator_Save_{timestamp}.json"

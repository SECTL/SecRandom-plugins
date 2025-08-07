#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例插件主模块
提供插件的核心功能和初始化逻辑
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# 配置日志
logger = logging.getLogger(__name__)


class ExamplePlugin:
    """示例插件主类"""
    
    def __init__(self, plugin_dir: str):
        """初始化插件
        
        Args:
            plugin_dir: 插件目录路径
        """
        self.plugin_dir = plugin_dir
        self.config_file = os.path.join(plugin_dir, 'config.json')
        self.data_file = os.path.join(plugin_dir, 'data.json')
        
        # 插件配置
        self.config = self._load_config()
        
        # 插件数据
        self.data = self._load_data()
        
        # 插件状态
        self.is_enabled = True
        self.initialized_time = datetime.now()
        
        logger.info(f"示例插件初始化完成: {self.plugin_dir}")
    
    def _load_config(self) -> Dict[str, Any]:
        """加载插件配置"""
        default_config = {
            "version": "1.0.0",
            "auto_start": True,
            "debug_mode": False,
            "max_items": 100,
            "theme": "default",
            "notifications": {
                "enabled": True,
                "sound": True,
                "duration": 3000
            },
            "features": {
                "feature1": True,
                "feature2": False,
                "feature3": True
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
        
        return default_config
    
    def _load_data(self) -> Dict[str, Any]:
        """加载插件数据"""
        default_data = {
            "usage_count": 0,
            "last_used": None,
            "user_preferences": {},
            "statistics": {
                "total_operations": 0,
                "success_count": 0,
                "error_count": 0
            },
            "cache": {}
        }
        
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    default_data.update(data)
        except Exception as e:
            logger.error(f"加载数据文件失败: {e}")
        
        return default_data
    
    def save_config(self) -> bool:
        """保存插件配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            logger.info("配置保存成功")
            return True
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            return False
    
    def save_data(self) -> bool:
        """保存插件数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            logger.info("数据保存成功")
            return True
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
            return False
    
    def get_info(self) -> Dict[str, Any]:
        """获取插件信息"""
        return {
            "name": "示例插件",
            "version": self.config.get("version", "1.0.0"),
            "author": "SecRandom Team",
            "description": "这是一个功能完整的示例插件",
            "enabled": self.is_enabled,
            "initialized_time": self.initialized_time.isoformat(),
            "usage_count": self.data.get("usage_count", 0)
        }
    
    def execute_operation(self, operation: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """执行插件操作
        
        Args:
            operation: 操作名称
            params: 操作参数
            
        Returns:
            操作结果
        """
        params = params or {}
        
        # 更新使用统计
        self.data["usage_count"] += 1
        self.data["last_used"] = datetime.now().isoformat()
        self.data["statistics"]["total_operations"] += 1
        
        try:
            if operation == "hello":
                result = self._hello_operation(params)
                self.data["statistics"]["success_count"] += 1
            elif operation == "calculate":
                result = self._calculate_operation(params)
                self.data["statistics"]["success_count"] += 1
            elif operation == "process_text":
                result = self._process_text_operation(params)
                self.data["statistics"]["success_count"] += 1
            else:
                result = {"error": f"未知操作: {operation}"}
                self.data["statistics"]["error_count"] += 1
        except Exception as e:
            result = {"error": str(e)}
            self.data["statistics"]["error_count"] += 1
            logger.error(f"执行操作失败: {operation}, 错误: {e}")
        
        # 保存数据
        self.save_data()
        
        return result
    
    def _hello_operation(self, params: Dict) -> Dict[str, Any]:
        """Hello操作示例"""
        name = params.get("name", "用户")
        return {
            "message": f"你好, {name}! 欢迎使用示例插件",
            "timestamp": datetime.now().isoformat(),
            "operation": "hello"
        }
    
    def _calculate_operation(self, params: Dict) -> Dict[str, Any]:
        """计算操作示例"""
        try:
            a = float(params.get("a", 0))
            b = float(params.get("b", 0))
            operation = params.get("operation", "add")
            
            if operation == "add":
                result = a + b
            elif operation == "subtract":
                result = a - b
            elif operation == "multiply":
                result = a * b
            elif operation == "divide":
                result = a / b if b != 0 else "除数不能为零"
            else:
                result = "未知操作"
            
            return {
                "result": result,
                "expression": f"{a} {operation} {b}",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": f"计算错误: {str(e)}"}
    
    def _process_text_operation(self, params: Dict) -> Dict[str, Any]:
        """文本处理操作示例"""
        text = params.get("text", "")
        operation = params.get("operation", "uppercase")
        
        if not text:
            return {"error": "文本不能为空"}
        
        if operation == "uppercase":
            result = text.upper()
        elif operation == "lowercase":
            result = text.lower()
        elif operation == "reverse":
            result = text[::-1]
        elif operation == "word_count":
            result = str(len(text.split()))
        elif operation == "char_count":
            result = str(len(text))
        else:
            result = "未知文本操作"
        
        return {
            "result": result,
            "original_text": text,
            "operation": operation,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取使用统计"""
        return {
            "usage_count": self.data.get("usage_count", 0),
            "last_used": self.data.get("last_used", "从未使用"),
            "statistics": self.data.get("statistics", {}),
            "config": self.config
        }
    
    def reset_statistics(self) -> bool:
        """重置统计数据"""
        try:
            self.data["usage_count"] = 0
            self.data["last_used"] = None
            self.data["statistics"] = {
                "total_operations": 0,
                "success_count": 0,
                "error_count": 0
            }
            return self.save_data()
        except Exception as e:
            logger.error(f"重置统计数据失败: {e}")
            return False
    
    def cleanup(self):
        """清理资源"""
        try:
            # 保存所有数据
            self.save_config()
            self.save_data()
            logger.info("插件资源清理完成")
        except Exception as e:
            logger.error(f"清理资源失败: {e}")


# 插件入口函数
def create_plugin(plugin_dir: str) -> ExamplePlugin:
    """创建插件实例
    
    Args:
        plugin_dir: 插件目录路径
        
    Returns:
        插件实例
    """
    return ExamplePlugin(plugin_dir)


# 插件信息
def get_plugin_info() -> Dict[str, Any]:
    """获取插件信息"""
    return {
        "name": "示例插件",
        "version": "1.0.0",
        "author": "SecRandom Team",
        "description": "这是一个功能完整的示例插件，展示了插件开发的最佳实践",
        "features": [
            "配置管理",
            "数据存储",
            "操作执行",
            "统计功能",
            "UI界面"
        ],
        "requirements": [],
        "api_version": "1.0"
    }
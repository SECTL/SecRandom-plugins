#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例插件页面模块
提供完整的插件界面和交互功能
"""

import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qfluentwidgets import *

# 导入插件主模块
import importlib.util
spec = importlib.util.spec_from_file_location("main", os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py"))
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)
ExamplePlugin = main_module.ExamplePlugin


class PluginPage(QWidget):
    """示例插件页面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 初始化插件
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugin = ExamplePlugin(plugin_dir)
        
        # 窗口设置
        self.setWindowTitle("示例插件")
        self.setWindowIcon(QIcon("./app/resource/icon/SecRandom.png"))
        self.resize(800, 600)
        
        # 设置UI
        self.setup_ui()
        
        # 加载初始数据
        self.load_initial_data()
    
    def setup_ui(self):
        """设置UI界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # === 头部区域 ===
        header_widget = self.create_header_widget()
        main_layout.addWidget(header_widget)
        
        # === 标签页区域 ===
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabPosition(QTabWidget.North)
        
        # 添加各个功能页面
        self.tab_widget.addTab(self.create_basic_page(), "基础功能")
        self.tab_widget.addTab(self.create_calculator_page(), "计算器")
        self.tab_widget.addTab(self.create_text_processor_page(), "文本处理")
        self.tab_widget.addTab(self.create_settings_page(), "设置")
        self.tab_widget.addTab(self.create_statistics_page(), "统计")
        
        main_layout.addWidget(self.tab_widget)
        
        # === 底部按钮区域 ===
        bottom_widget = self.create_bottom_widget()
        main_layout.addWidget(bottom_widget)
    
    def create_header_widget(self) -> QWidget:
        """创建头部区域"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题
        title_label = TitleLabel("示例插件")
        title_label.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # 状态指示器
        self.status_label = BodyLabel("状态: 正常")
        self.status_label.setStyleSheet("color: green;")
        header_layout.addWidget(self.status_label)
        
        return header_widget
    
    def create_basic_page(self) -> QWidget:
        """创建基础功能页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 欢迎区域
        welcome_card = SimpleCardWidget()
        welcome_layout = QVBoxLayout(welcome_card)
        welcome_layout.setContentsMargins(15, 15, 15, 15)
        
        welcome_title = SubtitleLabel("欢迎使用示例插件")
        welcome_layout.addWidget(welcome_title)
        
        welcome_desc = BodyLabel(
            "这是一个功能完整的示例插件，展示了插件开发的最佳实践。\n"
            "包含配置管理、数据存储、多种操作功能和丰富的UI组件。"
        )
        welcome_desc.setWordWrap(True)
        welcome_layout.addWidget(welcome_desc)
        
        layout.addWidget(welcome_card)
        
        # 快速操作区域
        operations_card = SimpleCardWidget()
        operations_layout = QFormLayout(operations_card)
        operations_layout.setContentsMargins(15, 15, 15, 15)
        
        operations_title = SubtitleLabel("快速操作")
        operations_layout.addRow(operations_title)
        
        # Hello操作
        hello_layout = QHBoxLayout()
        self.name_input = LineEdit()
        self.name_input.setPlaceholderText("请输入您的名字")
        self.name_input.setText("用户")
        hello_layout.addWidget(self.name_input)
        
        hello_btn = PrimaryPushButton("打个招呼")
        hello_btn.clicked.connect(self.on_hello_clicked)
        hello_layout.addWidget(hello_btn)
        
        operations_layout.addRow("Hello操作:", hello_layout)
        
        # 结果显示区域
        self.result_text = TextEdit()
        self.result_text.setPlaceholderText("操作结果将显示在这里...")
        self.result_text.setMaximumHeight(150)
        operations_layout.addRow("结果:", self.result_text)
        
        layout.addWidget(operations_card)
        
        layout.addStretch()
        
        return page
    
    def create_calculator_page(self) -> QWidget:
        """创建计算器页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        calculator_card = SimpleCardWidget()
        calc_layout = QFormLayout(calculator_card)
        calc_layout.setContentsMargins(15, 15, 15, 15)
        
        calc_title = SubtitleLabel("简易计算器")
        calc_layout.addRow(calc_title)
        
        # 数字输入
        num_layout = QHBoxLayout()
        self.num1_input = SpinBox()
        self.num1_input.setRange(-999999, 999999)
        self.num1_input.setValue(10)
        num_layout.addWidget(self.num1_input)
        
        num_layout.addWidget(QLabel("+"))
        
        self.num2_input = SpinBox()
        self.num2_input.setRange(-999999, 999999)
        self.num2_input.setValue(5)
        num_layout.addWidget(self.num2_input)
        
        calc_layout.addRow("数字:", num_layout)
        
        # 操作选择
        self.operation_combo = ComboBox()
        self.operation_combo.addItems(["加法", "减法", "乘法", "除法"])
        calc_layout.addRow("操作:", self.operation_combo)
        
        # 计算按钮
        calc_btn = PrimaryPushButton("计算")
        calc_btn.clicked.connect(self.on_calculate_clicked)
        calc_layout.addRow("", calc_btn)
        
        # 计算结果
        self.calc_result = LineEdit()
        self.calc_result.setReadOnly(True)
        calc_layout.addRow("结果:", self.calc_result)
        
        layout.addWidget(calculator_card)
        layout.addStretch()
        
        return page
    
    def create_text_processor_page(self) -> QWidget:
        """创建文本处理页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        text_card = SimpleCardWidget()
        text_layout = QVBoxLayout(text_card)
        text_layout.setContentsMargins(15, 15, 15, 15)
        
        text_title = SubtitleLabel("文本处理工具")
        text_layout.addWidget(text_title)
        
        # 文本输入
        text_layout.addWidget(BodyLabel("输入文本:"))
        self.text_input = TextEdit()
        self.text_input.setPlaceholderText("请输入要处理的文本...")
        self.text_input.setMaximumHeight(100)
        text_layout.addWidget(self.text_input)
        
        # 操作按钮
        operations_layout = QHBoxLayout()
        
        text_ops = [
            ("转大写", "uppercase"),
            ("转小写", "lowercase"),
            ("反转", "reverse"),
            ("词数统计", "word_count"),
            ("字符统计", "char_count")
        ]
        
        for op_name, op_value in text_ops:
            btn = PushButton(op_name)
            btn.clicked.connect(lambda checked, op=op_value: self.on_text_process_clicked(op))
            operations_layout.addWidget(btn)
        
        text_layout.addLayout(operations_layout)
        
        # 处理结果
        text_layout.addWidget(BodyLabel("处理结果:"))
        self.text_result = TextEdit()
        self.text_result.setReadOnly(True)
        self.text_result.setMaximumHeight(100)
        text_layout.addWidget(self.text_result)
        
        layout.addWidget(text_card)
        layout.addStretch()
        
        return page
    
    def create_settings_page(self) -> QWidget:
        """创建设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        settings_card = SimpleCardWidget()
        settings_layout = QFormLayout(settings_card)
        settings_layout.setContentsMargins(15, 15, 15, 15)
        
        settings_title = SubtitleLabel("插件设置")
        settings_layout.addRow(settings_title)
        
        # 自动启动
        self.auto_start_check = CheckBox("自动启动")
        self.auto_start_check.setChecked(self.plugin.config.get("auto_start", True))
        settings_layout.addRow("自动启动:", self.auto_start_check)
        
        # 调试模式
        self.debug_check = CheckBox("调试模式")
        self.debug_check.setChecked(self.plugin.config.get("debug_mode", False))
        settings_layout.addRow("调试模式:", self.debug_check)
        
        # 最大项目数
        self.max_items_spin = SpinBox()
        self.max_items_spin.setRange(1, 1000)
        self.max_items_spin.setValue(self.plugin.config.get("max_items", 100))
        settings_layout.addRow("最大项目数:", self.max_items_spin)
        
        # 主题选择
        self.theme_combo = ComboBox()
        self.theme_combo.addItems(["默认", "深色", "浅色"])
        current_theme = self.plugin.config.get("theme", "default")
        theme_map = {"default": "默认", "dark": "深色", "light": "浅色"}
        self.theme_combo.setCurrentText(theme_map.get(current_theme, "默认"))
        settings_layout.addRow("主题:", self.theme_combo)
        
        # 功能开关
        features_group = QGroupBox("功能开关")
        features_layout = QVBoxLayout(features_group)
        
        features = self.plugin.config.get("features", {})
        self.feature1_check = CheckBox("功能1")
        self.feature1_check.setChecked(features.get("feature1", True))
        features_layout.addWidget(self.feature1_check)
        
        self.feature2_check = CheckBox("功能2")
        self.feature2_check.setChecked(features.get("feature2", False))
        features_layout.addWidget(self.feature2_check)
        
        self.feature3_check = CheckBox("功能3")
        self.feature3_check.setChecked(features.get("feature3", True))
        features_layout.addWidget(self.feature3_check)
        
        settings_layout.addRow(features_group)
        
        # 保存按钮
        save_btn = PrimaryPushButton("保存设置")
        save_btn.clicked.connect(self.on_save_settings_clicked)
        settings_layout.addRow("", save_btn)
        
        layout.addWidget(settings_card)
        layout.addStretch()
        
        return page
    
    def create_statistics_page(self) -> QWidget:
        """创建统计页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        stats_card = SimpleCardWidget()
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(15, 15, 15, 15)
        
        stats_title = SubtitleLabel("使用统计")
        stats_layout.addWidget(stats_title)
        
        # 统计信息
        self.stats_text = TextEdit()
        self.stats_text.setReadOnly(True)
        stats_layout.addWidget(self.stats_text)
        
        # 重置按钮
        reset_btn = PushButton("重置统计")
        reset_btn.clicked.connect(self.on_reset_stats_clicked)
        stats_layout.addWidget(reset_btn)
        
        layout.addWidget(stats_card)
        layout.addStretch()
        
        return page
    
    def create_bottom_widget(self) -> QWidget:
        """创建底部按钮区域"""
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        
        bottom_layout.addStretch()
        
        # 保存数据按钮
        save_btn = PrimaryPushButton("保存数据")
        save_btn.clicked.connect(self.on_save_data_clicked)
        bottom_layout.addWidget(save_btn)
        
        # 刷新按钮
        refresh_btn = PushButton("刷新")
        refresh_btn.clicked.connect(self.on_refresh_clicked)
        bottom_layout.addWidget(refresh_btn)
        
        # 关闭按钮
        close_btn = PushButton("关闭页面")
        close_btn.clicked.connect(self.close)
        bottom_layout.addWidget(close_btn)
        
        return bottom_widget
    
    def load_initial_data(self):
        """加载初始数据"""
        self.update_statistics()
    
    def on_hello_clicked(self):
        """Hello按钮点击事件"""
        name = self.name_input.text().strip()
        if not name:
            name = "用户"
        
        result = self.plugin.execute_operation("hello", {"name": name})
        
        if "error" in result:
            InfoBar.error(
                title="错误",
                content=result["error"],
                duration=3000,
                parent=self
            )
        else:
            self.result_text.setText(
                f"时间: {result['timestamp']}\n"
                f"消息: {result['message']}"
            )
            InfoBar.success(
                title="成功",
                content="Hello操作执行成功",
                duration=2000,
                parent=self
            )
    
    def on_calculate_clicked(self):
        """计算按钮点击事件"""
        a = self.num1_input.value()
        b = self.num2_input.value()
        
        operation_map = {
            "加法": "add",
            "减法": "subtract", 
            "乘法": "multiply",
            "除法": "divide"
        }
        
        operation = operation_map.get(self.operation_combo.currentText(), "add")
        
        result = self.plugin.execute_operation("calculate", {
            "a": a,
            "b": b,
            "operation": operation
        })
        
        if "error" in result:
            InfoBar.error(
                title="错误",
                content=result["error"],
                duration=3000,
                parent=self
            )
        else:
            self.calc_result.setText(str(result["result"]))
            InfoBar.success(
                title="计算完成",
                content=f"{result['expression']} = {result['result']}",
                duration=2000,
                parent=self
            )
    
    def on_text_process_clicked(self, operation):
        """文本处理按钮点击事件"""
        text = self.text_input.toPlainText().strip()
        if not text:
            InfoBar.warning(
                title="警告",
                content="请输入要处理的文本",
                duration=2000,
                parent=self
            )
            return
        
        result = self.plugin.execute_operation("process_text", {
            "text": text,
            "operation": operation
        })
        
        if "error" in result:
            InfoBar.error(
                title="错误",
                content=result["error"],
                duration=3000,
                parent=self
            )
        else:
            self.text_result.setText(result["result"])
            InfoBar.success(
                title="处理完成",
                content=f"文本{operation}操作完成",
                duration=2000,
                parent=self
            )
    
    def on_save_settings_clicked(self):
        """保存设置按钮点击事件"""
        # 更新配置
        self.plugin.config["auto_start"] = self.auto_start_check.isChecked()
        self.plugin.config["debug_mode"] = self.debug_check.isChecked()
        self.plugin.config["max_items"] = self.max_items_spin.value()
        
        # 主题映射
        theme_map = {"默认": "default", "深色": "dark", "浅色": "light"}
        self.plugin.config["theme"] = theme_map.get(self.theme_combo.currentText(), "default")
        
        # 功能开关
        self.plugin.config["features"] = {
            "feature1": self.feature1_check.isChecked(),
            "feature2": self.feature2_check.isChecked(),
            "feature3": self.feature3_check.isChecked()
        }
        
        if self.plugin.save_config():
            InfoBar.success(
                title="成功",
                content="设置保存成功",
                duration=2000,
                parent=self
            )
        else:
            InfoBar.error(
                title="错误",
                content="设置保存失败",
                duration=3000,
                parent=self
            )
    
    def on_reset_stats_clicked(self):
        """重置统计按钮点击事件"""
        dialog = MessageBox(
            "确认重置",
            "确定要重置所有统计数据吗？此操作不可撤销。",
            self
        )
        
        if dialog.exec_():
            if self.plugin.reset_statistics():
                self.update_statistics()
                InfoBar.success(
                    title="成功",
                    content="统计数据重置成功",
                    duration=2000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title="错误",
                    content="统计数据重置失败",
                    duration=3000,
                    parent=self
                )
    
    def on_save_data_clicked(self):
        """保存数据按钮点击事件"""
        if self.plugin.save_data():
            InfoBar.success(
                title="成功",
                content="数据保存成功",
                duration=2000,
                parent=self
            )
        else:
            InfoBar.error(
                title="错误",
                content="数据保存失败",
                duration=3000,
                parent=self
            )
    
    def on_refresh_clicked(self):
        """刷新按钮点击事件"""
        self.update_statistics()
        InfoBar.info(
            title="刷新",
            content="数据已刷新",
            duration=1500,
            parent=self
        )
    
    def update_statistics(self):
        """更新统计信息显示"""
        stats = self.plugin.get_statistics()
        
        stats_text = f"""使用统计信息:

使用次数: {stats['usage_count']}
最后使用: {stats['last_used'] or '从未使用'}

操作统计:
  总操作数: {stats['statistics']['total_operations']}
  成功次数: {stats['statistics']['success_count']}
  失败次数: {stats['statistics']['error_count']}

配置信息:
  自动启动: {stats['config'].get('auto_start', True)}
  调试模式: {stats['config'].get('debug_mode', False)}
  最大项目数: {stats['config'].get('max_items', 100)}
  主题: {stats['config'].get('theme', 'default')}
"""
        
        self.stats_text.setText(stats_text)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 清理插件资源
        self.plugin.cleanup()
        super().closeEvent(event)
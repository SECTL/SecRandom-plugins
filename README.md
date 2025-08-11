# SecRandom 插件系统

## 📖 概述

SecRandom 插件系统为应用程序提供了灵活的扩展机制。通过插件系统，开发者可以轻松地添加新功能、扩展现有功能，并与主系统深度集成。

### 🎯 核心优势

- **模块化设计**：每个插件都是独立的模块，便于开发和维护
- **配置灵活**：支持动态配置，用户可以自定义插件行为
- **界面统一**：使用 qfluentwidgets 保持界面风格一致
- **错误处理**：完善的异常处理和日志记录机制

## 📁 项目结构

```
SecRandom-plugins/
├── README.md          # 插件使用说明
├── main.py            # 插件主程序
├── service.py         # 后台服务
├── plugin.json        # 插件配置文件
└── icon.png      # 插件图标
```

## 💡 开发建议

### 📋 最佳实践

- **使用内置库**：建议使用SecRandom已有的内置库，避免安装额外的依赖库
- **版本兼容**：建议使用开发SecRandom的Python版本（或更高版本），避免版本冲突
- **日志管理**：建议使用SecRandom的日志库(loguru)，方便记录插件运行日志（建议存储在插件目录下的log文件中）
- **配置管理**：建议使用SecRandom的配置库(json)，方便读取插件配置文件（建议存储在插件目录下的config文件中）

### ⚠️ 注意事项

- 确保插件目录结构符合规范
- 遵循命名约定和代码风格
- 添加适当的错误处理和日志记录
- 提供完整的文档和使用说明

## 🔧 插件开发指南

### 📄 必需文件

每个插件必须包含以下文件：

- **`plugin.json`**：插件配置文件，定义插件的基本信息
- **`main.py`**：插件主程序，包含插件的核心功能
- **`README.md`**：插件说明文档，提供使用指南
- **`icon.png`**：插件图标文件（可选，建议提供）

### ⚙️ 插件配置文件 (plugin.json)

```json
{
  "name": "插件名称",
  "version": "v1.0.0",
  "description": "插件功能描述",
  "author": "插件作者",
  "url": "https://github.com/username/plugin-repo",
  "entry_point": "main.py",
  "background_service": "service.py",
  "min_app_version": "v1.0.0.0",
  "dependencies": [],
  "enabled": true,
  "autostart": false
}
```

**配置项说明：**
- `name`：插件显示名称
- `version`：插件版本号（建议使用语义化版本，如 v1.0.0）
- `description`：插件功能描述
- `author`：插件作者
- `url`：插件主页或仓库URL（必选！要做为对比插件的用处，提供GitHub仓库链接）
- `entry_point`：插件入口文件（通常是 main.py）
- `background_service`：插件后台服务文件（可选）
- `min_app_version`：兼容的最低应用版本（格式：v1.0.0.0）
- `dependencies`：依赖列表（可选）
- `enabled`：是否默认启用
- `autostart`：是否自动启动（建议默认为 false）

### 💻 插件主程序 (main.py)

```python
# 导入必要的库
import json
import os
from typing import Dict, List, Optional
from qfluentwidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from loguru import logger


class MyPlugin:
    """插件主类"""
    
    def __init__(self):
        """初始化插件"""
        self.config_path = "app/plugin/my_plugin/config.json"
        self.config = {}
        self.load_config()
        
    def load_config(self):
        """加载插件配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
            
    def save_config(self):
        """保存插件配置"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            
    def get_info(self) -> Dict:
        """获取插件信息"""
        return {
            "name": "我的插件",
            "version": "v1.0.0",
            "description": "插件描述"
        }
        
    def execute(self, *args, **kwargs):
        """执行插件功能"""
        try:
            # 插件主要逻辑
            return "插件执行成功"
        except Exception as e:
            logger.error(f"插件执行失败: {e}")
            return "插件执行失败"


# API 接口函数
def show_dialog(parent=None):
    """显示插件界面"""
    try:
        dialog = __MyPluginDialog(parent)  # 示例
        dialog.exec_()
    except Exception as e:
        logger.error(f"显示界面失败: {e}")
    

def get_plugin_info() -> Dict:
    """获取插件信息"""
    try:
        plugin = MyPlugin()
        return plugin.get_info()
    except Exception as e:
        logger.error(f"获取插件信息失败: {e}")
        return {"error": "获取插件信息失败"}


# 测试代码
if __name__ == "__main__":
    app = QApplication([])
    dialog = MyDialog()  # 示例
    dialog.show()
    app.exec_()
```

### 🔄 插件服务 (service.py)

如果插件需要在后台运行服务，应在 `service.py` 文件中实现：

```python
import threading
import time
from loguru import logger


class MyPluginService:
    """插件后台服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.is_running = False
        self.service_thread = None
        logger.info("插件服务初始化完成")
        
    def start(self):
        """启动服务"""
        if self.is_running:
            logger.warning("服务已在运行中")
            return False
            
        try:
            self.is_running = True
            self.service_thread = threading.Thread(target=self._service_loop)
            self.service_thread.daemon = True
            self.service_thread.start()
            logger.info("插件服务启动成功")
            return True
        except Exception as e:
            logger.error(f"启动服务失败: {e}")
            self.is_running = False
            return False
        
    def stop(self):
        """停止服务"""
        if not self.is_running:
            logger.warning("服务未在运行")
            return False
            
        try:
            self.is_running = False
            if self.service_thread and self.service_thread.is_alive():
                self.service_thread.join(timeout=5)
            logger.info("插件服务停止成功")
            return True
        except Exception as e:
            logger.error(f"停止服务失败: {e}")
            return False
            
    def _service_loop(self):
        """服务主循环"""
        while self.is_running:
            try:
                # 在这里实现服务的具体逻辑
                self._do_service_work()
                time.sleep(1)  # 避免CPU占用过高
            except Exception as e:
                logger.error(f"服务循环出错: {e}")
                time.sleep(5)  # 出错后等待一段时间再继续
                
    def _do_service_work(self):
        """执行服务工作"""
        # 在这里实现具体的服务逻辑
        pass
```

## 🚀 系统特性

### 🛠️ 技术栈

- **框架**: 基于 PyQt5 桌面应用框架
- **UI库**: 使用 qfluentwidgets 保持界面风格统一
- **日志**: 集成 loguru 日志库，便于调试和监控
- **配置**: JSON 格式的配置文件，易于编辑和备份
- **类型**: 使用 Python 类型提示，提高代码质量

### 🔍 高级特性

- **依赖管理**: 自动安装和管理插件依赖库
- **版本控制**: 支持插件版本兼容性检查
- **热加载**: 支持插件的动态加载和卸载
- **错误隔离**: 插件错误不会影响主系统运行
- **资源管理**: 智能管理插件资源，避免内存泄漏

## 📚 开发环境

### 🔧 环境要求

- **Python**: 3.8.10+
- **PyQt5**: 桌面应用框架
- **qfluentwidgets**: UI组件库
- **loguru**: 日志库

### 📋 开发流程

1. **📁 创建插件目录**: 在 `app/plugin/` 下创建插件目录
2. **⚙️ 编写配置文件**: 创建 `plugin.json` 定义插件信息
3. **💻 实现主程序**: 编写 `main.py` 实现插件功能
4. **🔄 实现服务**: 如果需要后台服务，编写 `service.py`
5. **🎨 添加界面**: 创建图形界面（如需要）
6. **📝 编写文档**: 创建 `README.md` 说明插件用法
7. **🧪 测试调试**: 测试插件功能并调试问题
8. **📦 打包发布**: 打包插件为 zip 文件，发布到插件广场

### 🎯 开发规范

#### 命名约定
- **类名**: 使用驼峰命名法（如 `MyPlugin`）
- **函数名**: 使用下划线命名法（如 `show_dialog`）
- **常量**: 使用大写字母（如 `MAX_COUNT`）
- **文件名**: 使用小写字母和下划线（如 `main.py`）

#### 代码质量
- **注释**: 为复杂的逻辑添加清晰的注释
- **错误处理**: 添加适当的异常处理机制
- **日志记录**: 记录重要的操作和错误信息
- **类型提示**: 使用 Python 类型提示提高代码可读性
- **代码风格**: 遵循 PEP 8 代码风格指南

### 🐛 调试技巧

```python
# 在 main.py 末尾添加测试代码
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # 测试插件功能
    try:
        dialog = MyDialog()  # 替换为你的对话框类
        dialog.show()
        logger.info("插件测试启动成功")
    except Exception as e:
        logger.error(f"插件测试启动失败: {e}")
        
    sys.exit(app.exec_())
```

## 📦 依赖管理

### 🔄 依赖声明

如果插件需要额外的Python库，需要在 `plugin.json` 文件中添加 `dependencies` 字段：

```json
{
  "name": "插件名称",
  "version": "v1.0.0",
  "description": "插件功能描述",
  "author": "插件作者",
  "entry_point": "main.py",
  "min_app_version": "v1.0.0.0",
  "dependencies": ["transformers", "torch", "numpy"],
  "enabled": true
}
```

### ⚙️ 自动安装机制

SecRandom 程序在启动时会自动检查插件目录下的 `plugin.json` 文件，根据 `dependencies` 字段安装插件依赖的库：

1. **检查依赖**: 程序会检查每个插件声明的依赖库
2. **自动安装**: 如果库不存在，程序会自动从 PyPI 下载并安装
3. **版本管理**: 支持指定版本号（如 `numpy>=1.20.0`）
4. **错误处理**: 安装失败时会记录错误日志，但不会影响程序启动

### 🗂️ 依赖隔离

插件的依赖库采用隔离管理机制：

- **独立环境**: 每个插件的依赖库安装在独立的 `site-packages` 目录下
- **避免冲突**: 不同插件的依赖库不会相互冲突
- **版本控制**: 支持不同插件使用不同版本的同一个库
- **清理机制**: 插件卸载时会自动清理对应的依赖库

### 📋 常用依赖库

以下是一些常用的Python库，可以在插件中使用：

```json
{
  "dependencies": [
    "requests",      # HTTP请求
    "numpy",        # 数值计算
    "pandas",       # 数据处理
    "pillow",       # 图像处理
    "opencv-python", # 计算机视觉
    "matplotlib",   # 数据可视化
    "scikit-learn", # 机器学习
    "beautifulsoup4", # 网页解析
    "selenium",     # 浏览器自动化
    "schedule"      # 任务调度
  ]
}
```

## 📖 示例插件

### 🎯 SecRandom 插件

本项目提供了一个完整的示例插件实现：

- **功能**: 演示插件系统的完整功能和工作流程
- **位置**: `SecRandom-plugins/` 目录
- **组成**: 包含主程序、后台服务、配置文件和文档
- **用途**: 提供插件开发的完整示例和最佳实践

### 📋 插件组成

```
SecRandom-plugins/
├── main.py         # 插件主程序
├── service.py      # 后台服务
├── plugin.json     # 插件配置
├── SecRandom.png   # 插件图标
└── README.md       # 使用说明
```

## ❓ 常见问题

### 🚀 快速开始

**Q: 如何快速创建一个新的插件？**
A: 复制 `SecRandom-plugins` 目录，重命名为你的插件名称，然后修改其中的文件来实现你的功能。

**Q: 插件开发的基本流程是什么？**
A: 创建目录 → 编写配置 → 实现功能 → 添加界面 → 测试调试 → 打包发布

### 🔧 技术问题

**Q: 插件如何与主系统通信？**
A: 目前可以通过信号槽机制和配置文件与主系统进行简单的数据交换。更复杂的集成功能正在开发中。

**Q: 如何处理插件的配置？**
A: 使用 JSON 格式的配置文件，在插件初始化时加载，修改时保存。建议将配置文件存储在插件目录下的 `config` 文件夹中。

**Q: 插件的界面如何保持一致？**
A: 使用 `qfluentwidgets` 库创建界面，遵循主系统的设计规范，支持深色/浅色主题切换。

### 🐛 调试问题

**Q: 插件无法加载怎么办？**
A: 检查 `plugin.json` 格式是否正确，确保必需文件存在，查看日志文件了解具体错误信息。

**Q: 依赖库安装失败怎么办？**
A: 检查网络连接，确认库名称正确，尝试手动安装，或联系技术支持。

**Q: 插件运行出错如何调试？**
A: 在 `main.py` 末尾添加测试代码，使用 `logger` 记录调试信息，检查异常处理逻辑。

## 📞 技术支持

### 📚 相关资源

- **SecRandom 主系统文档**: 了解主系统的架构和API
- **PyQt5 官方文档**: 学习桌面应用开发
- **qfluentwidgets 项目文档**: 掌握UI组件使用
- **loguru 日志库文档**: 了解日志记录最佳实践

### 🤝 社区支持

- **GitHub Issues**: 报告问题或提出建议
- **讨论区**: 与其他开发者交流经验
- **示例代码**: 参考现有插件的实现

### 📧 联系方式

如有问题或建议，请通过以下方式联系：

- **GitHub**: [SecRandom-plugins](https://github.com/your-repo/SecRandom-plugins)
- **邮件**: support@secrandom.com
- **社区**: 加入我们的开发者社区

---

© 2025 SecRandom Team. All rights reserved.

[🔝 返回顶部](#secrandom-插件系统)
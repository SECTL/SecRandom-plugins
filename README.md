# SecRandom 插件系统

## 概述
SecRandom 支持插件系统，允许用户扩展应用功能。插件可以包含自定义界面和功能。

## 插件结构

每个插件应该包含以下文件：

```
具体应该根据示例插件的结构进行修改
app/plugins/your_plugin_name/
├── plugin.json      # 插件配置文件
├── assets/          # 插件资源文件夹
│   └── icon.png     # 插件图标文件
│── main.py          # 插件主文件
│── page.py          # 插件页面文件（可选）
```

## 插件配置文件 (plugin.json)

```json
{
  "name": "插件名称",
  "version": "1.0.0",
  "author": "作者名称",
  "description": "插件描述",
  "icon": "plugins/插件名称/assets/icon.png"
}
```

### 配置字段说明

- `name`: 插件显示名称
- `version`: 插件版本号
- `author`: 插件作者
- `description`: 插件描述
- `icon`: 插件图标(使用相对路径-插件文件夹根目录下的assets文件夹,名称要为'icon.png', 'icon.ico', 'icon.svg'其中之一)

## 插件页面文件 (page.py)

如果插件需要显示界面，需要创建 `page.py` 文件并包含 `PluginPage` 类：

```python
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qfluentwidgets import *


class PluginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("插件页面")
        self.setup_ui()
    
    def setup_ui(self):
        # 在这里设置你的界面
        layout = QVBoxLayout(self)
        
        title_label = TitleLabel("我的插件")
        layout.addWidget(title_label)
        
        # 添加更多界面元素...
```

## 插件管理

### 1. 通过设置界面管理

1. 打开主应用
2. 点击设置按钮
3. 选择"插件管理"选项卡
4. 在插件管理界面中，你可以：
   - 查看已安装的插件
   - 导入新的插件包（.zip 文件）
   - 删除现有插件
   - 打开插件页面（如果插件有页面文件）

### 2. 通过托盘菜单快速访问

右键点击系统托盘图标，选择"打开插件管理"可以直接进入插件管理界面。

### 3. 导入插件

1. 点击"导入"按钮
2. 选择插件包文件（.zip 格式）
3. 插件包必须包含 `plugin.json` 配置文件
4. 系统会自动解压并加载插件

### 4. 删除插件

1. 在插件卡片中点击"删除"按钮
2. 确认删除操作
3. 插件将被完全移除

## 插件包格式

插件包是一个 .zip 文件，包含以下结构：

```
plugin_name.zip
├── plugin.json
├── page.py (可选)
└── 其他资源文件 (可选)
```

## 示例插件

系统提供了一个示例插件 `example_plugin`，你可以参考它的结构来创建自己的插件。

## 注意事项

1. 插件目录位于 `app/plugins/`
2. 插件名称必须唯一，不能重复
3. 插件页面类必须命名为 `PluginPage`
4. 插件可以使用 qfluentwidgets 的所有组件
5. 插件页面会在独立的窗口中打开

## 常用 Fluent Icon

- 可以看app\resource\assets路径下的图标
- 如需增加需要自行添加到assets路径下(需要按照格式添加暗色和亮色图标)
- 或者您可以自己在插件路径下添加图标文件(需要自己在插件中自行写图标的相对路径)

## 开发建议

1. 保持插件简单和专注
2. 提供清晰的描述和作者信息
3. 测试插件在不同主题下的显示效果
4. 遵循现有的 UI 风格和交互模式
5. 添加适当的错误处理和日志记录




# 插件依赖离线缓存目录

此目录用于存放插件依赖的离线wheel文件，支持插件在没有网络连接的情况下安装依赖。

## 使用方法

### 1. 下载wheel文件
```bash
# 下载指定包的wheel文件
pip download package_name==version -d resources/wheels/

# 下载多个包的wheel文件
pip download -r requirements.txt -d resources/wheels/
```

### 2. 支持的包类型
- **ollama**: 用于大语言模型交互
- **transformers**: 用于自然语言处理
- **torch**: 深度学习框架
- **numpy**: 数值计算
- **pandas**: 数据处理
- **requests**: HTTP请求
- 其他常用Python包

### 3. 目录结构
```
resources/wheels/
├── ollama-0.1.0-py3-none-any.whl
├── transformers-4.20.0-py3-none-any.whl
├── torch-1.12.0-cp39-cp39-win_amd64.whl
├── numpy-1.21.0-cp39-cp39-win_amd64.whl
└── ...
```

### 4. 插件依赖安装流程
1. 插件加载时检查 `__requirements__.txt` 文件
2. 在插件目录下创建 `site-packages` 目录
3. 使用以下命令安装依赖：
   ```bash
   pip install --target <plugin_dir>/site-packages -r __requirements__.txt --find-links resources/wheels
   ```
4. 将 `site-packages` 目录添加到 `sys.path`
5. 依赖安装成功后加载插件

### 5. 注意事项
- wheel文件应该与目标Python版本兼容
- 建议定期更新wheel文件以获取最新版本
- 某些包可能需要额外的系统依赖
- 在Windows环境下，优先下载 `.whl` 文件而非源码包

## 维护建议

### 定期更新wheel文件
```bash
# 批量更新常用包
pip download --upgrade ollama transformers torch numpy pandas requests -d resources/wheels/
```

### 清理旧版本
```bash
# 删除指定包的旧版本
find resources/wheels/ -name "package_name-*" -not -name "package_name-latest-version*" -delete
```

### 验证wheel文件完整性
```bash
# 检查wheel文件是否损坏
for file in resources/wheels/*.whl; do
    if unzip -t "$file" > /dev/null 2>&1; then
        echo "✓ $file is valid"
    else
        echo "✗ $file is corrupted"
    fi
done
```
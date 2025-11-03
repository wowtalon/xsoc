# XSOC - 可扩展安全运营中心

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](https://github.com/wowtalon/xsoc)

中文版本 | [English](README.md)

## 概述

XSOC（可扩展安全运营中心）是一个现代化的、基于插件的安全运营平台，旨在提供全面的安全监控、事件响应和威胁管理能力。采用 Python 构建，具有灵活的插件架构，XSOC 允许组织根据其特定需求定制和扩展安全运营。

## 特性

- **🔌 插件架构**: 可扩展的插件系统，支持内置和自定义插件
- **🌐 Web 界面**: 现代化的 Web 仪表板，具有响应式设计
- **⚙️ 工作流引擎**: 支持 YAML 配置和 Jinja2 模板的自动化工作流处理
- **🔧 工具集成**: 动态工具加载和执行框架
- **📊 实时监控**: 实时安全事件监控和告警
- **🛡️ SOC 运营**: 全面的安全运营中心功能
- **⚡ 多线程**: 高效的并发插件执行
- **🔄 优雅关闭**: 合理的资源清理和线程管理
- **🎨 彩色日志**: 增强的带颜色编码输出级别的日志系统

## 架构

```
xsoc/
├── app.py                 # 主应用程序入口点
├── main.py               # 备用入口点
├── xplugin/              # 插件框架
│   ├── plugin.py         # 基础插件类
│   ├── plugin_manager.py # 插件管理系统
│   └── main.py          # 插件框架入口
├── plugins/              # 插件目录
│   ├── builtin/         # 内置插件
│   │   ├── web/         # Web 界面插件
│   │   └── workflow/    # 工作流引擎插件
│   └── custom/          # 自定义用户插件
├── data/                # 数据存储
└── example/            # 示例配置
```

## 快速开始

### 前置要求

- Python 3.12 或更高版本
- pip 或 uv 包管理器

### 安装

1. **克隆仓库:**
   ```bash
   git clone https://github.com/wowtalon/xsoc.git
   cd xsoc
   ```

2. **安装依赖:**
   ```bash
   # 使用 pip
   pip install -r requirements.txt
   
   # 使用 uv (推荐)
   uv sync
   ```

3. **配置环境:**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件进行配置
   ```

4. **运行应用程序:**
   ```bash
   python app.py
   ```

### 依赖项

当前项目依赖:
```
python-dotenv>=0.9.9    # 环境变量管理
flask>=3.1.2            # Web 框架
pyyaml>=6.0.3          # YAML 配置解析
jinja2>=3.0.0          # 工作流模板引擎
```

### 环境变量

在项目根目录创建 `.env` 文件:

```env
XSOC_HOST=localhost
XSOC_PORT=5000
XSOC_DEBUG=true
```

## 插件开发

### 创建自定义插件

1. **创建插件目录:**
   ```bash
   mkdir plugins/custom/my_plugin
   ```

2. **创建插件类:**
   ```python
   # plugins/custom/my_plugin/__init__.py
   from xplugin.plugin import Plugin
   
   class MyPlugin(Plugin):
       def __init__(self):
           super().__init__()
           self.name = "MyPlugin"
           self.description = "我的自定义安全插件"
           self.separate_process = False
           
       def run_plugin(self):
           # 你的插件逻辑在这里
           return "MyPlugin 正在运行"
   ```

### 插件配置

插件可以使用以下属性进行配置:

- `separate_process`: 在单独线程中运行插件 (默认: False)
- `continuous_run`: 保持插件持续运行 (默认: False)  
- `singleton`: 确保只有一个实例 (默认: True)

### 内置插件

#### Web 插件

提供现代化 Web 界面，包括:
- 仪表板概览
- SOC 运营面板
- 插件管理界面
- 设置配置

访问地址: `http://localhost:5000`

#### 工作流插件

支持自动化工作流处理的高级功能:
- 基于 YAML 的工作流定义
- Jinja2 模板引擎用于动态参数解析
- 上下文变量支持（环境变量和步骤结果）
- 动态工具加载和执行
- 逐步执行并带有错误处理
- 常用操作的内置实用函数

工作流配置示例:
```yaml
version: 1.0
name: 测试工作流
description: 用于测试系统功能的工作流
env:
  var1: "世界"
steps:
  - name: step1
    action: tool
    target: print_message
    parameters:
      message: "来自 {{ env.var1 }} 的问候"
  - name: step2
    action: plugin
    target: MyPlugin.my_function
    parameters:
      input: "{{ steps.step1 }}"
```

## API 参考

### 插件基类

```python
class Plugin:
    def __init__(self):
        # 插件初始化
        
    def run_plugin(self):
        # 主要插件执行方法
        
    def register_tool(self, tool: callable):
        # 注册工具函数
        
    def register_variable(self, var_name: str, value):
        # 注册变量
        
    def is_shutdown_requested(self):
        # 检查是否请求关闭
```

### 插件管理器

```python
class PluginManager:
    def register_plugin(self, plugin):
        # 注册插件实例
        
    def init_plugins_from_path(self, path: str):
        # 从目录加载插件
        
    def get_plugins(self):
        # 获取所有已注册插件
```

### 日志系统

XSOC 包含增强的日志系统，具有彩色输出以提高可见性:

```python
from xplugin.logger import xlogger

# 可用的日志级别和颜色编码
xlogger.debug("调试消息")      # 青色
xlogger.info("信息消息")        # 绿色
xlogger.warning("警告消息")  # 黄色
xlogger.error("错误消息")      # 红色
xlogger.critical("严重消息") # 洋红色
```

日志记录器提供:
- 不同日志级别的颜色编码输出
- 时间戳和记录器名称信息
- 整个应用程序的一致格式

## 配置

### 应用程序配置

主要配置存储在 `app.py` 中的 `xsoc` 字典中:

```python
xsoc = {
    "core": {
        "version": "0.1.0",
        "plugins": {
            "built-in": [],
            "custom": []
        },
        "settings": {
            "debug": True,
            "host": "localhost",
            "port": 5000
        }
    }
}
```

### 插件配置

插件可以通过 `xsoc_core` 变量访问核心配置:

```python
def run_plugin(self):
    version = self.xsoc_core["version"]
    debug_mode = self.xsoc_core["settings"]["debug"]
```

### 工作流工具

工作流插件包含一套全面的实用函数:

```python
# 条件操作
if_condition_met(condition, then_value, else_value)
case_condition_met(condition, cases_dict)

# 类型检查
is_true(value)
is_false(value) 
is_none(value)

# 类型转换
convert_to_string(value)
convert_to_int(value)

# 字符串操作
concatenate_strings(*args)

# 实用函数
print_message(message)
loop_until_condition_met(condition, timeout)
iterate_over_list(list, function)
```

这些工具可以在工作流 YAML 文件中直接调用:

```yaml
steps:
  - name: convert_step
    action: tool
    target: convert_to_int
    parameters:
      value: "{{ env.some_number }}"
```

## 开发

### 设置开发环境

1. **克隆仓库:**
   ```bash
   git clone https://github.com/wowtalon/xsoc.git
   cd xsoc
   ```

2. **创建虚拟环境:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **安装开发依赖:**
   ```bash
   pip install -r requirements.txt
   ```

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行覆盖率测试
python -m pytest --cov=xplugin

# 运行特定测试
python -m pytest xplugin/tests/test_sample.py
```

### 代码风格

本项目遵循 PEP 8 风格指南。使用以下工具格式化代码:

```bash
black .
flake8 .
```

## 贡献

1. Fork 仓库
2. 创建功能分支: `git checkout -b feature-name`
3. 进行更改并添加测试
4. 确保所有测试通过: `python -m pytest`
5. 提交更改: `git commit -am 'Add feature'`
6. 推送到分支: `git push origin feature-name`
7. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 支持

- **文档**: [Wiki](https://github.com/wowtalon/xsoc/wiki)
- **问题**: [GitHub Issues](https://github.com/wowtalon/xsoc/issues)
- **讨论**: [GitHub Discussions](https://github.com/wowtalon/xsoc/discussions)

## 更新日志

### v0.1.0 (当前版本)
- 初始版本发布
- 插件架构实现
- Web 界面插件
- 工作流引擎插件
- 多线程支持
- 优雅关闭处理

## 路线图

- [ ] 高级插件依赖管理
- [ ] 插件市场和注册表
- [ ] 增强的实时更新 Web UI
- [ ] 数据库集成以支持持久存储
- [ ] 用于外部集成的 REST API
- [ ] 容器部署支持
- [ ] 高级工作流功能
- [ ] 安全扫描和漏洞管理
- [ ] 威胁情报集成
- [ ] 事件响应自动化

---

由 XSOC 团队用 ❤️ 制作
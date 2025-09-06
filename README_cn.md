# Paper2Code: 自动化论文转代码生成系统

一个复杂的系统，使用大型语言模型（LLM）自动将研究论文转换为可执行代码。该系统实现了三阶段管道（Plan → Analyze → Code）来重现学术论文中描述的研究方法。

## 🚀 功能特性

- **三阶段管道**：Plan → Analyze → Code 方法论，实现全面的代码生成
- **多格式支持**：支持JSON和LaTeX (.tex) 论文格式
- **LLM集成**：支持多种LLM提供商，包括Azure OpenAI和Zhipu AI
- **模块化架构**：清晰的关注点分离和可扩展设计
- **配置驱动**：基于YAML的配置，便于自定义
- **输出组织**：结构化输出，包含规划文档、分析文件和生成的源代码

## 📁 项目结构

```
paper-code/
├── src/
│   └── paper2code/
│       ├── __init__.py
│       ├── config.py              # 系统提示和配置模板
│       ├── paper_planning.py      # 规划阶段实现
│       ├── paper_analyzing.py     # 分析阶段实现  
│       ├── paper_coding.py        # 代码生成阶段实现
│       ├── register.py            # NAT函数注册
│       ├── tex2json.py           # LaTeX转JSON转换工具
│       └── configs/
│           └── config.yml         # 默认配置文件
├── outputs/                       # 生成的代码和分析输出目录
└── README.md
```

## 🏗️ 架构概览

### 三阶段处理流程

1. **规划阶段**（`paper_planning.py`）
   - 分析研究论文的方法论
   - 创建全面的实现计划
   - 生成包含数据结构和接口的架构设计
   - 产生带依赖分析的任务列表

2. **分析阶段**（`paper_analyzing.py`）
   - 对每个组件进行详细的逻辑分析
   - 创建详细的实现指导
   - 确保与论文方法论的一致性
   - 为每个代码文件生成分析文档

3. **代码生成阶段**（`paper_coding.py`）
   - 编写模块化、可维护的Python代码
   - 遵循Google风格编码指南
   - 实现完整、可重用的代码片段
   - 生成带有适当导入和类型提示的可执行源代码

### 核心组件

- **配置系统**（`config.py`）：包含系统提示和输出格式一致的模板
- **LaTeX处理**（`tex2json.py`）：将LaTeX论文转换为JSON格式以便处理
- **NAT集成**（`register.py`）：与NVIDIA AI Agent Toolkit框架注册
- **LLM抽象**：通过统一接口支持多个LLM提供商

## 🔧 设置和安装

### 前置要求

- Python 3.12+
- NVIDIA AI Agent Toolkit
- uv包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd paper-code
```

2. **设置虚拟环境**
```bash
uv venv .venv -p python3.12
source .venv/bin/activate
```

3. **安装NVIDIA AI Agent Toolkit**
```bash
git clone https://github.com/NVIDIA/NeMo-Agent-Toolkit aiqtoolkit --recursive
cd aiqtoolkit 
uv pip install ".[langchain]"
```

4. **安装Paper2Code包**
```bash
cd <this_git_repo_root_path>
uv pip install -e .
```

## 🎯 使用方法

### 基本使用

```bash
nat run --config_file src/paper2code/configs/config.yml --input "path/to/paper.tex"
```

### 配置

系统使用YAML配置文件来定义：

- **LLM设置**：模型选择和参数
- **输出目录**：生成文件的位置
- **工作流参数**：可自定义的处理选项

示例配置（`src/paper2code/configs/config.yml`）：
```yaml
general:
  use_uvloop: true
  logging:
    console:
      level: WARN

llms:
  azure_openai_llm:
    _type: azure_openai
    model_name: gpt-4o
    azure_deployment: gpt-4o
  zhipu_llm:
    _type: openai
    base_url: https://open.bigmodel.cn/api/paas/v4
    model_name: glm-4.5

workflow:
  _type: paper2code
  llm_name: azure_openai_llm
  output_directory: outputs
  # file_list_msg:  文件列表提示词
  # task_list_msg:  任务列表提示词
  # config_msg:  配置提示词
```

### 输入格式

系统支持两种输入格式：

1. **JSON格式**：论文内容的直接JSON表示
2. **LaTeX格式**：LaTeX格式的学术论文（自动转换为JSON）

## 📊 输出结构

输出日志：

```
> nat run --config_file src/paper2code/configs/config.yml --input paper.tex
2025-09-06 17:00:49,968 - nat.cli.commands.start - INFO - Starting NAT from config file: 'src/paper2code/configs/config.yml'

Configuration Summary:
--------------------
Workflow Type: paper2code
Number of Functions: 0
Number of LLMs: 2
Number of Embedders: 0
Number of Memory: 0
Number of Object Stores: 0
Number of Retrievers: 0
Number of TTC Strategies: 0
Number of Authentication Providers: 0

2025-09-06 17:00:50,443 - paper2code.paper_planning - INFO - Start planning.
2025-09-06 17:00:50,443 - paper2code.paper_planning - INFO - [PLANNING] (1/4): Overall plan.
2025-09-06 17:01:16,203 - paper2code.paper_planning - INFO - [PLANNING] (2/4): Architecture design.
2025-09-06 17:01:25,494 - paper2code.paper_planning - INFO - [PLANNING] (3/4): Logic design.
2025-09-06 17:01:33,035 - paper2code.paper_planning - INFO - [PLANNING] (4/4): Configuration file generation.
2025-09-06 17:01:38,397 - paper2code.paper_planning - INFO - ✅ Paper planning finished.
2025-09-06 17:01:38,397 - paper2code.paper_analyzing - INFO - Start analyzing.
2025-09-06 17:01:38,397 - paper2code.paper_analyzing - INFO - [ANALYSIS] (1/6): utils.py.
2025-09-06 17:01:59,252 - paper2code.paper_analyzing - INFO - [ANALYSIS] (2/6): dataset_loader.py.
2025-09-06 17:02:21,041 - paper2code.paper_analyzing - INFO - [ANALYSIS] (3/6): model.py.
2025-09-06 17:02:46,550 - paper2code.paper_analyzing - INFO - [ANALYSIS] (4/6): trainer.py.
2025-09-06 17:03:09,380 - paper2code.paper_analyzing - INFO - [ANALYSIS] (5/6): evaluation.py.
2025-09-06 17:03:32,340 - paper2code.paper_analyzing - INFO - [ANALYSIS] (6/6): main.py.
2025-09-06 17:03:52,493 - paper2code.paper_analyzing - INFO - ✅ Paper analyzing finished.
2025-09-06 17:03:52,493 - paper2code.paper_coding - INFO - Start coding.
2025-09-06 17:03:52,494 - paper2code.paper_coding - INFO - [CODING](1/6): outputs/code/utils.py
2025-09-06 17:04:11,233 - paper2code.paper_coding - INFO - [CODING](2/6): outputs/code/dataset_loader.py
2025-09-06 17:04:33,644 - paper2code.paper_coding - INFO - [CODING](3/6): outputs/code/model.py
2025-09-06 17:04:54,248 - paper2code.paper_coding - INFO - [CODING](4/6): outputs/code/trainer.py
2025-09-06 17:05:09,493 - paper2code.paper_coding - INFO - [CODING](5/6): outputs/code/evaluation.py
2025-09-06 17:05:25,770 - paper2code.paper_coding - INFO - [CODING](6/6): outputs/code/main.py
2025-09-06 17:05:40,277 - paper2code.paper_coding - INFO - ✅ Paper coding finished.
2025-09-06 17:05:40,278 - nat.front_ends.console.console_front_end_plugin - INFO - 
--------------------------------------------------
Workflow Result:
['Source code generated Successfully in path: outputs/code.']
--------------------------------------------------
2025-09-06 17:05:40,278 - paper2code.register - INFO - Cleaning up paper2code workflow.
```

系统在指定目录中生成组织化的输出：

```
outputs/
├── planning.md                    # 整体实现计划
├── file_list.txt                 # 系统架构设计
├── task_list.json                # 详细任务分解和逻辑分析
├── planning_config.yaml          # 配置参数
├── [filename]_simple_analysis.txt  # 每个组件的逻辑分析
└── code/                         # 生成的源代码目录
    ├── main.py
    ├── dataset_loader.py
    ├── model.py
    ├── trainer.py
    └── evaluation.py
```

## 🌟 高级功能

### 多LLM支持

系统支持多种LLM提供商：
- **Azure OpenAI**：GPT-4、GPT-4o模型
- **Zhipu AI**：GLM-4.5模型
- 通过配置可扩展到其他提供商

### 错误处理和日志记录

- 每个处理阶段的全面日志记录
- 无效输入格式的错误处理
- 整个管道的进度跟踪

### 代码质量保证

- 遵循Google Python风格指南
- 强类型提示和显式变量声明
- 完整的导入语句和错误处理
- 模块化、可维护的代码架构

## 🔍 环境变量

对于Azure OpenAI模型，设置以下环境变量：

```bash
export AZURE_OPENAI_ENDPOINT="your_endpoint"
export AZURE_OPENAI_API_KEY="your_api_key"
```

对于Zhipu 类OpenAI API，设置以下环境变量：

```bash
export OPENAI_API_KEY="zhipu_api_key"
```

## 🛠️ 自定义

### 添加新的LLM提供商

1. 扩展`config.yml`中的配置
2. 添加提供商特定参数
3. 使用示例论文测试

### 自定义提示

修改`config.py`中的系统提示，以：
- 调整输出风格和格式
- 包含领域特定要求
- 自定义规划和分析深度

### 输出自定义

修改配置中的输出目录结构和文件命名模式，以匹配您的项目要求。

## 📈 性能考虑

- **并行处理**：使用async/await进行高效的LLM API调用
- **内存管理**：大文档分块处理
- **缓存**：针对类似论文的重复处理进行优化
- **资源利用**：可配置的超时和重试机制

## 🔗 依赖项

- **NVIDIA AI Agent Toolkit**：核心框架集成
- **LangChain**：LLM编排和提示管理
- **PyYAML**：配置文件解析
- **Python标准库**：核心功能

## 🤝 贡献

该系统设计为可扩展的。增强的关键领域包括：

- 额外的输入格式支持
- 新的LLM提供商集成
- 增强的代码质量指标
- 多语言支持
- 自动化测试框架

## 📝 许可证

此项目是NVIDIA AI Agent Toolkit生态系统的一部分，遵循相同的许可条款。

---

*使用NVIDIA AI Agent Toolkit和大型语言模型构建❤️*

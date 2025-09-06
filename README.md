# Paper2Code: Automatic Paper-to-Code Generation System

A sophisticated system that automatically converts research papers into executable code using Large Language Models (LLMs). This system implements a three-stage pipeline (Plan → Analyze → Code) to reproduce research methodologies described in academic papers.

## 🚀 Features

- **Three-Stage Pipeline**: Plan → Analyze → Code methodology for comprehensive code generation
- **Multi-Format Support**: Handles both JSON and LaTeX (.tex) paper formats
- **LLM Integration**: Supports various LLM providers including Azure OpenAI and Zhipu AI
- **Modular Architecture**: Clean separation of concerns with extensible design
- **Configuration-Driven**: YAML-based configuration for easy customization
- **Output Organization**: Structured output with planning documents, analysis files, and generated source code

## 📁 Project Structure

```
paper-code/
├── src/
│   └── paper2code/
│       ├── __init__.py
│       ├── config.py              # System prompts and configuration templates
│       ├── paper_planning.py      # Planning stage implementation
│       ├── paper_analyzing.py     # Analysis stage implementation  
│       ├── paper_coding.py        # Code generation stage implementation
│       ├── register.py            # NAT function registration
│       ├── tex2json.py           # LaTeX to JSON conversion utility
│       └── configs/
│           └── config.yml         # Default configuration file
├── outputs/                       # Generated code and analysis output directory
└── README.md
```

## 🏗️ Architecture Overview

### Three-Stage Process

1. **Planning Stage** (`paper_planning.py`)
   - Analyzes the research paper methodology
   - Creates comprehensive implementation plan
   - Generates architecture design with data structures and interfaces
   - Produces task list with dependency analysis

2. **Analysis Stage** (`paper_analyzing.py`)
   - Conducts detailed logic analysis for each component
   - Creates detailed implementation guidance
   - Ensures alignment with paper methodology
   - Generates analysis documents for each code file

3. **Code Generation Stage** (`paper_coding.py`)
   - Writes modular, maintainable Python code
   - Follows Google-style coding guidelines
   - Implements complete, reusable code snippets
   - Generates executable source code with proper imports and type hints

### Key Components

- **Configuration System** (`config.py`): Contains system prompts and templates for consistent output formatting
- **LaTeX Processing** (`tex2json.py`): Converts LaTeX papers to JSON format for easier processing
- **NAT Integration** (`register.py`): Registers with NVIDIA AI Agent Toolkit framework
- **LLM Abstraction**: Supports multiple LLM providers through unified interface

## 🔧 Setup and Installation

### Prerequisites

- Python 3.12+
- NVIDIA AI Agent Toolkit
- uv package manager

### Installation Steps

1. **Clone the project**
```bash
git clone <repository-url>
cd paper-code
```

2. **Set up virtual environment**
```bash
uv venv .venv -p python3.12
source .venv/bin/activate
```

3. **Install NVIDIA AI Agent Toolkit**
```bash
git clone https://github.com/NVIDIA/NeMo-Agent-Toolkit aiqtoolkit --recursive
cd aiqtoolkit 
uv pip install ".[langchain]"
```

4. **Install Paper2Code package**
```bash
cd <this_git_repo_root_path>
uv pip install -e .
```

## 🎯 Usage

### Basic Usage

```bash
nat run --config_file src/paper2code/configs/config.yml --input "path/to/paper.tex"
```

### Configuration

The system uses YAML configuration files to define:

- **LLM Settings**: Model selection and parameters
- **Output Directory**: Location for generated files
- **Workflow Parameters**: Customizable processing options

Example configuration (`src/paper2code/configs/config.yml`):
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
```

### Input Formats

The system supports two input formats:

1. **JSON Format**: Direct JSON representation of paper content
2. **LaTeX Format**: Academic papers in LaTeX format (automatically converted to JSON)

## 📊 Output Structure

The system generates organized output in the specified directory:

```
outputs/
├── planning.md                    # Overall implementation plan
├── file_list.txt                 # System architecture design
├── task_list.json                # Detailed task breakdown with logic analysis
├── planning_config.yaml          # Configuration parameters
├── [filename]_simple_analysis.txt  # Logic analysis for each component
└── code/                         # Generated source code directory
    ├── main.py
    ├── dataset_loader.py
    ├── model.py
    ├── trainer.py
    └── evaluation.py
```

## 🌟 Advanced Features

### Multi-LLM Support

The system supports multiple LLM providers:
- **Azure OpenAI**: GPT-4, GPT-4o models
- **Zhipu AI**: GLM-4.5 model
- Extensible to other providers through configuration

### Error Handling and Logging

- Comprehensive logging for each processing stage
- Error handling for invalid input formats
- Progress tracking throughout the pipeline

### Code Quality Assurance

- Follows Google Python Style Guide
- Strong type hints and explicit variable declarations
- Complete import statements and error handling
- Modular, maintainable code architecture

## 🔍 Environment Variables

For Azure OpenAI integration, set the following environment variables:

```bash
export AZURE_OPENAI_ENDPOINT="your_endpoint"
export AZURE_OPENAI_API_KEY="your_api_key"
```

For Zhipu OpenAI api integration, set the following environment variables:

```bash
export OPENAI_API_KEY="zhipu_api_key"
```

## 🛠️ Customization

### Adding New LLM Providers

1. Extend the configuration in `config.yml`
2. Add provider-specific parameters
3. Test with sample papers

### Custom Prompts

Modify system prompts in `config.py` to:
- Adjust output style and format
- Include domain-specific requirements
- Customize planning and analysis depth

### Output Customization

Modify the output directory structure and file naming patterns in the configuration to match your project requirements.

## 📈 Performance Considerations

- **Parallel Processing**: Uses async/await for efficient LLM API calls
- **Memory Management**: Processes papers in chunks for large documents
- **Caching**: Optimized for repeated processing with similar papers
- **Resource Utilization**: Configurable timeout and retry mechanisms

## 🔗 Dependencies

- **NVIDIA AI Agent Toolkit**: Core framework integration
- **LangChain**: LLM orchestration and prompt management
- **PyYAML**: Configuration file parsing
- **Python Standard Library**: Core functionality

## 🤝 Contributing

The system is designed to be extensible. Key areas for enhancement include:

- Additional input format support
- New LLM provider integrations
- Enhanced code quality metrics
- Multi-language support
- Automated testing framework

## 📝 License

This project is part of the NVIDIA AI Agent Toolkit ecosystem and follows the same licensing terms.

---

*Built with ❤️ using NVIDIA AI Agent Toolkit and Large Language Models*


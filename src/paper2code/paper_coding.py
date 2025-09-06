from typing import Any
from langchain_core.messages import HumanMessage
from langchain_core.prompts import SystemMessagePromptTemplate
import json
import os
import re
from .config import planning_docs, planning_config, planning_file, planning_task

import logging
logger = logging.getLogger(__name__)

code_msg = """You are an expert researcher and software engineer with a deep understanding of experimental design and reproducibility in scientific research.
You will receive a research paper in {paper_format} format, an overview of the plan, a Design in JSON format consisting of "Implementation approach", "File list", "Data structures and interfaces", and "Program call flow", followed by a Task in JSON format that includes "Required packages", "Required other language third-party packages", "Logic Analysis", and "Task list", along with a configuration file named "config.yaml". 
Your task is to write code to reproduce the experiments and methodologies described in the paper. 

The code you write must be elegant, modular, and maintainable, adhering to Google-style guidelines. 
The code must strictly align with the paper's methodology, experimental setup, and evaluation metrics. 
Write code with triple quoto."""

done_file_lst = ['config.yaml']
done_file_dict = {}

def get_write_msg(todo_file_name, todo_file_desc, output_dir, paper_content):
    code_files = ""
    planning_docs_content = open(f'{output_dir}/{planning_docs}').read()
    config_yaml = open(f'{output_dir}/{planning_config}').read()
    planning_file_content = open(f'{output_dir}/{planning_file}').read()
    planning_task_content = open(f'{output_dir}/{planning_task}').read()
    for done_file in done_file_lst:
        if done_file.endswith(".yaml"):
            continue
        code_files += f"""
```python
{done_file_dict[done_file]}
```

"""

    write_msg=f"""# Context
## Paper
{paper_content}

-----

## Overview of the plan
{planning_docs_content}

-----

## Design
{planning_file_content}

-----

## Task
{planning_task_content}

-----

## Configuration file
```yaml
{config_yaml}
```
-----

## Code Files
{code_files}

-----

# Format example
## Code: {todo_file_name}
```python
## {todo_file_name}
...
```

-----

# Instruction
Based on the paper, plan, design, task and configuration file(config.yaml) specified previously, follow "Format example", write the code. 

We have {done_file_lst}.
Next, you must write only the "{todo_file_name}".
1. Only One file: do your best to implement THIS ONLY ONE FILE.
2. COMPLETE CODE: Your code will be part of the entire project, so please implement complete, reliable, reusable code snippets.
3. Set default value: If there is any setting, ALWAYS SET A DEFAULT VALUE, ALWAYS USE STRONG TYPE AND EXPLICIT VARIABLE. AVOID circular import.
4. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
5. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THIS FILE.
6. Before using a external variable/module, make sure you import it first.
7. Write out EVERY CODE DETAIL, DON'T LEAVE TODO.
8. REFER TO CONFIGURATION: you must use configuration from "config.yaml". DO NOT FABRICATE any configuration values.

{todo_file_desc}

## Code: {todo_file_name}"""
    return write_msg



analysis_system_msg_template = SystemMessagePromptTemplate.from_template("""You are an expert researcher, strategic analyzer and software engineer with a deep understanding of experimental design and reproducibility in scientific research.
You will receive a research paper in {paper_format} format, an overview of the plan, a design in JSON format consisting of "Implementation approach", "File list", "Data structures and interfaces", and "Program call flow", followed by a task in JSON format that includes "Required packages", "Required other language third-party packages", "Logic Analysis", and "Task list", along with a configuration file named "config.yaml". 

Your task is to conduct a comprehensive logic analysis to accurately reproduce the experiments and methodologies described in the research paper. 
This analysis must align precisely with the paper’s methodology, experimental setup, and evaluation criteria.

1. Align with the Paper: Your analysis must strictly follow the methods, datasets, model configurations, hyperparameters, and experimental setups described in the paper.
2. Be Clear and Structured: Present your analysis in a logical, well-organized, and actionable format that is easy to follow and implement.
3. Prioritize Efficiency: Optimize the analysis for clarity and practical implementation while ensuring fidelity to the original experiments.
4. Follow design: YOU MUST FOLLOW "Data structures and interfaces". DONT CHANGE ANY DESIGN. Do not use public member functions that do not exist in your design.
5. REFER TO CONFIGURATION: Always reference settings from the config.yaml file. Do not invent or assume any values—only use configurations explicitly provided.
     
""")


async def code_paper(paper_content: str, llm: Any, output_dir: str) -> str:
    logic_analysis_dict = {}
    logger.info('Start coding.')
    with open(f'{output_dir}/{planning_task}', "r") as f:
        task_json = json.load(f)
        todo_list = task_json.get("Task list", [])
        logic_analysis = task_json.get("Logic Analysis", [])
        for desc in logic_analysis:
            logic_analysis_dict[desc[0]] = desc[1]
 
    source_path = f'{output_dir}/code'
    os.makedirs(source_path, exist_ok=True)
    for todo_idx, todo_file_name in enumerate(todo_list):
        msgs = [analysis_system_msg_template.format(paper_format='json')]
        current_stage = f"[CODING]({todo_idx+1}/{len(todo_list)}): {source_path}/{todo_file_name}"
        logger.info(current_stage)
    
        if todo_file_name == "config.yaml":
            continue
        with open(f'{output_dir}/{todo_file_name}_simple_analysis.txt', 'r') as f:
            instruction_msg = get_write_msg(todo_file_name, f.read(), output_dir, paper_content)
        msgs.append(HumanMessage(instruction_msg))
    
        res = await llm.ainvoke(msgs)  
        done_file_lst.append(todo_file_name)
    
        # save
        save_todo_file_name = todo_file_name.replace("/", "_")
    
    
        # extract code save 
        py_match = re.search(r"```python\n(.*?)\n```", res, re.DOTALL)
        if py_match:
            code = py_match.group(1)
            if len(code) == 0:
                code = res
    
        done_file_dict[todo_file_name] = code
        if save_todo_file_name != todo_file_name:
            todo_file_dir = '/'.join(todo_file_name.split("/")[:-1])
            os.makedirs(f"{source_path}/{todo_file_dir}", exist_ok=True)
    
        with open(f"{source_path}/{todo_file_name}", 'w') as f:
            f.write(code)
    logger.info('✅ Paper coding finished.')
    return f"Source code generated Successfully in path: {source_path}."

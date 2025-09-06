from typing import Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import SystemMessagePromptTemplate
import json
from .config import planning_docs, planning_config, planning_file, planning_task

import logging
logger = logging.getLogger(__name__)

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

def get_write_msg(todo_file_name, todo_file_desc, output_dir, paper_content):
    
    draft_desc = f"Write the logic analysis in '{todo_file_name}', which is intended for '{todo_file_desc}'."
    if len(todo_file_desc.strip()) == 0:
        draft_desc = f"Write the logic analysis in '{todo_file_name}'."
    planning_docs_content = open(f'{output_dir}/{planning_docs}').read()
    config_yaml = open(f'{output_dir}/{planning_config}').read()
    planning_file_content = open(f'{output_dir}/{planning_file}').read()
    planning_task_content = open(f'{output_dir}/{planning_task}').read()
    write_msg=f"""## Paper
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

## Instruction
Conduct a Logic Analysis to assist in writing the code, based on the paper, the plan, the design, the task and the previously specified configuration file (config.yaml). 
You DON'T need to provide the actual code yet; focus on a thorough, clear analysis.

{draft_desc}

-----

## Logic Analysis: {todo_file_name}"""
    return write_msg



async def analyze_paper(paper_content: str, llm: Any, output_dir: str):
    logic_analysis_dict = {}
    logger.info('Start analyzing.')
    with open(f'{output_dir}/{planning_task}', "r") as f:
        logger.info(f"file:{output_dir}/{planning_task}")
        task_json = json.load(f)
        todo_list = task_json.get("Task list", [])
        logic_analysis = task_json.get("Logic Analysis", [])
        for desc in logic_analysis:
            logic_analysis_dict[desc[0]] = desc[1]
    for i, todo_file_name in enumerate(todo_list):
        logger.info(f'[ANALYSIS] ({i+1}/{len(todo_list)}): {output_dir}/{todo_file_name}.')
        msgs = [analysis_system_msg_template.format(paper_format='json')]
        if todo_file_name == "config.yaml":
            continue
        
        if todo_file_name not in logic_analysis_dict:
            logic_analysis_dict[todo_file_name] = ""
            
        instruction_msg = get_write_msg(todo_file_name, logic_analysis_dict[todo_file_name], output_dir, paper_content)
        msgs.append(HumanMessage(instruction_msg))
        # response
        res = await llm.ainvoke(msgs)
        
        msgs.append(AIMessage(res))
    
    
        # save
        with open(f'{output_dir}/{todo_file_name}_simple_analysis.txt', 'w') as f:
            f.write(res)
    logger.info('✅ Paper analyzing finished.')

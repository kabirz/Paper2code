from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from typing import Any
import re
import logging
from .config import (
    SYSTEM_MSG_TEMPLATE, PLAN_MSG_TEMPLATE,
    planning_docs, planning_config, planning_file, planning_task, Paper2CodeFunctionConfig
)

logger = logging.getLogger(__name__)

async def plan_paper(paper_content: str, chain: Any, config: Paper2CodeFunctionConfig):
    system_msg_template = SystemMessagePromptTemplate.from_template(SYSTEM_MSG_TEMPLATE)
    plan_msg_template = HumanMessagePromptTemplate.from_template(PLAN_MSG_TEMPLATE)
    msgs = [system_msg_template.format(paper_format='json')]    
    steps = [
        {planning_docs: plan_msg_template.format(paper_content=paper_content)}, 
        {planning_file: HumanMessage(config.file_list_msg)},
        {planning_task: HumanMessage(config.task_list_msg)},
        {planning_config: HumanMessage(config.config_msg)},
    ]

    titles = ['Overall plan', 'Architecture design', 'Logic design', 'Configuration file generation']
    logger.info('Start planning.')
    for i, step in enumerate(steps):
        for name, msg in step.items():
            msgs.append(msg)
            logger.info(f'[PLANNING] ({i+1}/{len(steps)}): {titles[i]}.')
            res = await chain.ainvoke(msgs)
            if name == planning_config:
                yaml_match = re.search(r"```yaml\n(.*?)\n```", res, re.DOTALL)
                if yaml_match:
                    res = yaml_match.group(1)
            elif name == planning_task:
                json_match = re.search(r"\[CONTENT\]\n(.*?)\n\[/CONTENT\]", res, re.DOTALL)
                if json_match:
                    res = json_match.group(1)
                

            with open(f'{config.output_directory}/{name}', 'w') as f:
                f.write(res)
            msgs.append(AIMessage(content=res))

    logger.info('✅ Paper planning finished.')

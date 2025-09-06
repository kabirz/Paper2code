# pylint: disable=unused-import
# flake8: noqa

# Import any tools which need to be automatically registered here
import logging

from nat.builder.builder import Builder
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.builder.framework_enum import LLMFrameworkEnum
from langchain_core.output_parsers import StrOutputParser
from .paper_planning import plan_paper
from .paper_analyzing import analyze_paper
from .paper_coding import code_paper
from .config import Paper2CodeFunctionConfig
from .tex2json import parse_tex_section
import pathlib
import os
import sys
import json

logger = logging.getLogger(__name__)


@register_function(config_type=Paper2CodeFunctionConfig, framework_wrappers=[LLMFrameworkEnum.LANGCHAIN])
async def paper2code_function(config: Paper2CodeFunctionConfig, builder: Builder):
    llm = await builder.get_llm(config.llm_name, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    chain = llm | StrOutputParser()
    pathlib.Path(config.output_directory).mkdir(parents=True, exist_ok=True)

    # Implement your function logic here
    async def _response_fn(input_message: str) -> str:
        if os.path.isfile(input_message) and os.path.splitext(input_message)[1] not in ['.tex', '.json']:
            logger.error('Input file is not a Json file.')
            sys.exit(1)
        with open(input_message, 'r') as f:
            if os.path.splitext(input_message)[1] == '.tex':
                paper_content = parse_tex_section(f.read())
            else:
                paper_content = json.load(f)
        # Process the input_message and generate output
        await plan_paper(paper_content, chain, config)
        await analyze_paper(paper_content, chain, config.output_directory) 
        return await code_paper(paper_content, chain, config.output_directory)

    try:
        yield FunctionInfo.create(single_fn=_response_fn)
    except GeneratorExit:
        logger.warning("Function exited early!")
    finally:
        logger.info("Cleaning up paper2code workflow.")


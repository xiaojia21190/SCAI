from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from typing import Dict, Any, List
from config.llm_config import LLM_CONFIG
import autogen


class BaseAgent:
    def __init__(self, name: str, system_message: str):
        self.agent = autogen.AssistantAgent(
            name=name, system_message=system_message, llm_config=LLM_CONFIG
        )

    def get_agent(self) -> autogen.AssistantAgent:
        return self.agent

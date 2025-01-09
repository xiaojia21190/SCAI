from typing import Dict, Any, List
import autogen

class BaseAgent:
    def __init__(self, name: str, system_message: str):
        self.agent = autogen.AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config={
                "temperature": 0.3,
                "model": "gpt-4",
            }
        )
    
    def get_agent(self) -> autogen.AssistantAgent:
        return self.agent
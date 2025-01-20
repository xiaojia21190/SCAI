from .base import BaseAgent


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="planner",
            system_message="""You are a research planning agent. Your role is to:
1. Break down research queries into clear sub-tasks
2. Coordinate with other agents to execute the research plan
3. Ensure comprehensive coverage of the topic
4. Maintain scientific rigor in the research process""",
        )

    def get_agent(self, str=""):
        """get agent"""
        self.agent.update_system_message(f"""You are a research planning agent. Your role is to:
1. Break down research queries into clear sub-tasks
2. Coordinate with other agents to execute the research plan
3. Ensure comprehensive coverage of the topic
4. Maintain scientific rigor in the research proces. 
here are some background knowledge {str}""")
        return self.agent

from .base import BaseAgent


class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="critic",
            system_message="""You are a scientific critic. Your role is to:
1. Evaluate research proposals for feasibility
2. Identify potential methodological issues
3. Assess the novelty of research ideas
4. Suggest improvements to research approaches""",
        )

    def get_agent(self, str=""):
        """get agent"""
        self.agent.update_system_message(
            f"""You are a scientific critic. Your role is to:
1. Evaluate research proposals for feasibility
2. Identify potential methodological issues
3. Assess the novelty of research ideas
4. Suggest improvements to research approaches
here are some background knowledge {str}"""
        )
        return self.agent

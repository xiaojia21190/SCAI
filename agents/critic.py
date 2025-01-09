from .base import BaseAgent

class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="critic",
            system_message="""You are a scientific critic. Your role is to:
1. Evaluate research proposals for feasibility
2. Identify potential methodological issues
3. Assess the novelty of research ideas
4. Suggest improvements to research approaches"""
        )
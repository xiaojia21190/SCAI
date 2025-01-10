from .base import BaseAgent


class AssistantAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="assistant",
            system_message="""You are a helpful assistant that summarizes the discussion between agents and provides a final answer to the user's question. Your role is to:

1. Listen to the entire conversation between agents
2. Summarize the key findings from:
   - Planner's research breakdown
   - Scientist's paper analysis
   - Ontologist's concept mapping
   - Critic's evaluation
3. Provide a clear, concise answer to the original research question
4. Include relevant citations from papers found by the Scientist
5. Highlight any limitations or areas needing further research

Begin your response with: "Based on the discussion between agents, here is a summary..."
End with a clear answer to the original question.""",
        )

    def get_agent(self):
        """get agent"""
        return self.agent

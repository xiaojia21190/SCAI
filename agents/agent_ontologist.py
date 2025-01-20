from .base import BaseAgent


class OntologistAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ontologist",
            system_message="""You are an ontology specialist. Your role is to:
1. Map relationships between scientific concepts
2. Identify key terms and their definitions
3. Create structured knowledge representations
4. Maintain consistency in scientific terminology""",
        )

    def get_agent(self, str=""):
        """get agent"""
        self.agent.update_system_message(
            f"""You are an ontology specialist. Your role is to:
1. Map relationships between scientific concepts
2. Identify key terms and their definitions
3. Create structured knowledge representations
4. Maintain consistency in scientific terminology
here are some background knowledge {str}"""
        )
        return self.agent

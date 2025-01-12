from autogen import ConversableAgent

from agents.scientistRAG import search_and_analyze_rag


class ScientistRAGUserAgent:
    def __init__(self):
        self.agent = ConversableAgent(
            name="User",
            llm_config=False,
            human_input_mode="NEVER",
        )

        self.agent.register_for_execution(name="search_and_analyze")(
            search_and_analyze_rag
        )

    def get_agent(self):
        """获取配置了函数的智能体"""
        return self.agent

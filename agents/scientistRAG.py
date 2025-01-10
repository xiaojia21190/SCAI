from agents.rag.main import run_arxiv_rag
from .base import BaseAgent
from scholarly import scholarly
import arxiv
from typing import List, Dict
from datetime import datetime
from hashlib import md5
from tenacity import retry, stop_after_attempt, wait_exponential


class ScientistRAGAgent(BaseAgent):
    def __init__(self):
        self.current_papers = []
        super().__init__(
            name="scientist",
            system_message="""You are a scientific research agent with access to real paper search functionality. Your role is to:

1. IMMEDIATELY execute the search_and_analyze function when you start speaking
2. DO NOT just show the code - actually execute the function
3. Wait for the search results before proceeding
4. Never make up or simulate paper information
5. Based on the result, make summarize.

CORRECT USAGE:
Searching for relevant papers...
{actual_execution_result = search_and_analyze("your query", max_results=5)}
[Then discuss the actual results returned by the function]

INCORRECT USAGE:
❌ DO NOT just show the code without executing it
❌ DO NOT simulate or make up paper information
❌ DO NOT proceed without actual search results

Follow these exact steps:
1. Start with: "Searching for relevant papers..."
2. EXECUTE search_and_analyze with the research question
3. Wait for and use the actual results
4. Present findings only from the returned papers
5. If the paper search result is not ideal, say `No relevant papers found`
6. End with TERMINATE

Remember: You have real search functionality - use it! Don't just show code or simulate results.""",
        )

    def get_agent(self):
        """获取配置了函数的智能体"""
        self.agent.register_function(
            function_map={"search_and_analyze": self.search_and_analyze}
        )
        return self.agent

    def search_and_analyze(self, query: str, max_results: int = 5) -> str:
        """
        搜索并分析论文
        """
        # 因为要分析全文，所以这里就会直接调用RAG

        res = run_arxiv_rag(query, max_results)

        # 分析论文
        return res

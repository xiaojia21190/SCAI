from dataclasses import dataclass
from typing import List
from config.llm_config import LLM_CONFIG, MODEL
from autogen import ConversableAgent

LLM_KEY = {
    "role": "system",
    "content": """You are a program, you direct ouput the required datatype, without any human language and extra infomation. You will be given a sentence, extract no more than 5 keyword, output in json format, example: [`keyword1`, `keyword2`, .. ].
    """,
}


def chat_intent(query: str) -> str:
    LLM_INTENT = """You are a program, you direct ouput the required datatype, without any human language and extra infomation. You will be given a sentence, judge, and return one of the 4 catalogy, which are [`discussion`, `search`, `chat`, `sensitive`]. [discussion]: The user intent to ask question about philosophy/technology/acadamic topics. [search]: The user want to obtian special papers for full page knowledge. [chat]: The user intent to have conversation based on common sense/daily life. [sensitive]: The user intent to talk about violence, politic or other sensitive content."""

    agent = ConversableAgent(
        "chatbot",
        llm_config=LLM_CONFIG,
        code_execution_config=False,  # Turn off code execution, by default it is off.
        function_map=None,  # No registered functions, by default it is None.
        human_input_mode="NEVER",  # Never ask for human input.
        system_message=LLM_INTENT,
    )
    reply = agent.generate_reply(messages=[{"content": query, "role": "user"}])
    print(reply)
    return reply


# def chat_key(query: str) -> str:

#     # Use Ollama to get a response based on initial memory
#     response = ollama.chat(
#         model="gemma2:2b",
#         messages=[
#             LLM_KEY,
#             {
#                 "role": "user",
#                 "content": query,
#             },
#         ],
#     )
#     return response["message"]["content"]


@dataclass
class Query:
    text: str
    intent: str
    keywords: List[str]


class InputParser:
    def __init__(self):
        self.intents = [
            "search",
            "discussion",
            "chat",
            "sensitive",
        ]

    def parse_query(self, text: str) -> Query:
        # Basic keyword extraction (in production, use proper NLP)
        # TODO: use NLP
        keywords = [
            word.lower() for word in text.split() if len(word) > 3 and word.isalnum()
        ]

        # Simple intent classification
        intent = self._classify_intent(text)

        return Query(text=text, intent=intent, keywords=keywords)

    def _classify_intent(self, text: str) -> str:
        # Simple rule-based classification
        # TODO: LLM intent
        while True:
            res: str = chat_intent(text)
            if res.__contains__("discussion"):
                return "discussion"
            elif res.__contains__("search"):
                return "search"
            elif res.__contains__("chat"):
                return "chat"
            elif res.__contains__("sensitive"):
                return "sensitive"
            else:
                res = "repeat"

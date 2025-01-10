from dataclasses import dataclass
from typing import List, Optional

import ollama

LLM_INTENT = {
    """You are a program, you direct ouput the required datatype, without any human language and extra infomation. You will be given a sentence, judge, and return one of the 4 catalogy, which are [`paper_search`, `topic_exploration`, `chat`, `sensitive`].

    [paper_search]: The user intent to fetch knowledge from the very detail of the papers. Only when user have to access the detail of special full paper will trigger this item.
    [topic_exploration]: The user intent to discuss about acadamic topics.
    [chat]: The user intent to have conversation based on common sense/daily life.
    [sensitive]: The user intent to talk about violence, politic or other sensitive content.
    """
}

LLM_KEY = {
    """You are a program, you direct ouput the required datatype, without any human language and extra infomation. You will be given a sentence, extract no more than 5 keyword, output in json format, example: [`keyword1`, `keyword2`, .. ].
    """
}


@dataclass
class Query:
    text: str
    intent: str
    keywords: List[str]


class InputParser:
    def __init__(self):
        self.intents = [
            "paper_search",
            "topic_exploration",
            "methodology_question",
            "chat",
            "sensitive",
        ]

    def chat_intent(query: str) -> str:

        # Use Ollama to get a response based on initial memory
        response = ollama.chat(
            model="gemma2:2b",
            messages=[
                LLM_INTENT,
                {
                    "role": "user",
                    "content": query,
                },
            ],
        )
        return response["message"]["content"]

    def chat_key(query: str) -> str:

        # Use Ollama to get a response based on initial memory
        response = ollama.chat(
            model="gemma2:2b",
            messages=[
                LLM_KEY,
                {
                    "role": "user",
                    "content": query,
                },
            ],
        )
        return response["message"]["content"]

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
            res: str = self.chat_intent(text)
            if res.__contains__("paper_search"):
                return "paper_search"
            elif res.__contains__("topic_exploration"):
                return "topic_exploration"
            elif res.__contains__("chat"):
                return "chat"
            elif res.__contains__("sensitive"):
                return "sensitive"
            else:
                res = "repeat"

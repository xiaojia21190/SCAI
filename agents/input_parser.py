from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Query:
    text: str
    intent: str
    keywords: List[str]

class InputParser:
    def __init__(self):
        self.intents = ["paper_search", "topic_exploration", "methodology_question"]
    
    def parse_query(self, text: str) -> Query:
        # Basic keyword extraction (in production, use proper NLP)
        keywords = [word.lower() for word in text.split() 
                   if len(word) > 3 and word.isalnum()]
        
        # Simple intent classification
        intent = self._classify_intent(text)
        
        return Query(text=text, intent=intent, keywords=keywords)
    
    def _classify_intent(self, text: str) -> str:
        # Simple rule-based classification
        if any(word in text.lower() for word in ["how", "method", "technique"]):
            return "methodology_question"
        elif any(word in text.lower() for word in ["latest", "recent", "new"]):
            return "paper_search"
        else:
            return "topic_exploration"
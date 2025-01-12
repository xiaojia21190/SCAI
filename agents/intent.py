from .base import BaseAgent

LLM_INTENT = {
    "role": "system",
    "content": "You are a program, you direct ouput the required datatype, without any human language and extra infomation. You will be given a sentence, judge, and return one of the 4 catalogy, which are [`discussion`, `search`, `chat`, `sensitive`]. [discussion]: The user intent to ask question about philosophy/technology/acadamic topics. [search]: The user want to obtian special papers for full page knowledge. [chat]: The user intent to have conversation based on common sense/daily life. [sensitive]: The user intent to talk about violence, politic or other sensitive content.",
}


class IntentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="planner",
            system_message=LLM_INTENT,
        )

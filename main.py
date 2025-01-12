import os
import autogen
from agents.input_parser import InputParser
from agents.planner import PlannerAgent
from agents.scientist import ScientistAgent
from agents.scientistRAG import ScientistRAGAgent
from agents.ontologist import OntologistAgent
from agents.critic import CriticAgent
from agents.assistant import AssistantAgent
from agents.charmer import ChatAgent
from agents.scientistRAGUser import ScientistRAGUserAgent
from agents.scientistUser import ScientistUserAgent
from config.agent_config import AGENT_CONFIG


def main():
    # 创建用户代理
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=AGENT_CONFIG["max_consecutive_auto_reply"],
        is_termination_msg=lambda x: "TERMINATE" in str(x.get("content", "")),
        code_execution_config={
            "use_docker": False,
            "last_n_messages": 2,
            "work_dir": "workspace",
        },
    )

    # 示例查询
    # question = "What are the latest findings on dark matter?"
    # question = "What are attention mechanisms in LLMs?"
    # question = "When will quantum computing break hash algorithm (sha256)?"
    question = (
        "What hardfork will Bitcoin have to prevent quantum computing from breaking it?"
    )
    # question = "Find me some paper about robot price"

    parser = InputParser()
    query = parser.parse_query(question)

    print(f"The classification result is: {query.intent}")

    if query.intent == "sensitive":
        print("I can't help you with this question, it was beyond my grasp.")
        return

    if query.intent == "chat":
        charmer = ChatAgent().get_agent()
        # 设置发言顺序
        groupchat = autogen.GroupChat(
            agents=[user_proxy, charmer],
            messages=[],
            max_round=AGENT_CONFIG["max_round"],
            speaker_selection_method="round_robin",
            allow_repeat_speaker=True,
        )

        # 创建管理器
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=AGENT_CONFIG["llm_config"],
        )

        message = f"""Users Start With: {question}, End with TERMINATE when complete."""

        user_proxy.initiate_chat(manager, message=message)
    else:
        # Initialize agents
        planner = PlannerAgent().get_agent()
        if query.intent == "search":
            scientistUser = ScientistRAGUserAgent().get_agent()
            scientist = ScientistRAGAgent().get_agent()
        else:
            scientistUser = ScientistUserAgent().get_agent()
            scientist = ScientistAgent().get_agent()
        ontologist = OntologistAgent().get_agent()
        critic = CriticAgent().get_agent()
        assistant = AssistantAgent().get_agent()

        # 设置发言顺序
        groupchat = autogen.GroupChat(
            agents=[
                user_proxy,
                planner,
                scientist,
                scientistUser,
                ontologist,
                critic,
                assistant,
            ],
            messages=[],
            max_round=AGENT_CONFIG["max_round"],
            speaker_selection_method="round_robin",
            allow_repeat_speaker=True,
        )

        # 创建管理器
        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=AGENT_CONFIG["llm_config"],
            system_message="You help select the next speaker based on the conversation context.",
        )

        ##question = "What are the latest findings on zk proof systems?"
        message = f"""Research Question: {question}

    IMPORTANT GUIDELINES:
    1. Scientist must search for papers using the [search_and_analyze] function
    2. Only cite papers from actual search results
    3. Never make up or modify paper information
    4. Use exact paper details from search results
    5. Clearly state if no relevant papers are found

    Process:
    1. Planner: Break down the research question
    2. Scientist: Use search_and_analyze to find papers, Include source (ARXIV/SCHOLAR), IDs/DOIs for all citations
    3. Ontologist: Map concepts from verified papers
    4. Critic: Evaluate the findings and check citations
    5. Assistant: Summarize all findings and provide final answer to the research question

    Please proceed with the analysis. End with TERMINATE when complete."""

        user_proxy.initiate_chat(manager, message=message)


if __name__ == "__main__":
    os.makedirs("workspace", exist_ok=True)
    main()

from .llm_config import LLM_CONFIG

AGENT_CONFIG = {
    "max_consecutive_auto_reply": 5,
    "max_round": 50,
    "llm_config": {
        "config_list": [{
            "model": "gpt-4",
            "api_key": LLM_CONFIG["api_key"]
        }],
        "temperature": 0.3,
        "max_tokens": 500
    },
    "system_message": {
        "planner": """You are a research planning agent. Break down research queries into clear sub-tasks and coordinate with other agents.""",
        "scientist": """You are a scientific research agent. 
CRITICAL RULES:
- ONLY cite papers that have been verified to exist
- Always include paper IDs/DOIs
- Never make up or imagine papers
- Clearly state when information is unavailable
- Base all analysis on verified sources only""",
        "ontologist": """You are an ontology specialist. Map relationships between scientific concepts.""",
        "critic": """You are a scientific critic. Evaluate research proposals and suggest improvements."""
    }
}
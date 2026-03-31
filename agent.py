"""LangGraph agent runner using gemini-3.1-flash-lite-preview."""

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent


MODEL_NAME = "gemini-3.1-flash-lite-preview"


def build_agent(system_prompt: str | None = None):
    """Build a LangGraph ReAct agent backed by gemini-3.1-flash-lite-preview."""
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME)
    agent = create_react_agent(llm, tools=[], prompt=system_prompt)
    return agent


def run_agent(query: str, agent_definition: str | None = None) -> str:
    """Run the agent with the given query.

    Args:
        query: The user question or instruction.
        agent_definition: Optional system prompt / instructions read from the
                          uploaded agent file.

    Returns:
        The agent's final response as a string.
    """
    agent = build_agent(system_prompt=agent_definition if agent_definition else None)
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    messages = result.get("messages", [])
    if messages:
        return messages[-1].content
    return ""

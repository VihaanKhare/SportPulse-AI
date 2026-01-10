from smolagents import ToolCallingAgent,DuckDuckGoSearchTool,CodeAgent
from model.load_model import load_model
from live_updates_agent.visit_webpage import visit_webpage

web_agent=CodeAgent(
    tools=[DuckDuckGoSearchTool(),visit_webpage],
    model=load_model(),
    max_steps=10,
    name="web_search_agent",
    description="Runs web searches for you. Your expected output would be markdown content of the webpage.",
)
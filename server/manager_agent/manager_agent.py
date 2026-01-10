from smolagents import (CodeAgent,ToolCallingAgent,HfApiModel,DuckDuckGoSearchTool,LiteLLMModel)
from model.load_model import load_model
from live_updates_agent.web_agent import web_agent
from live_commentary.football.agent import football_live_commentary_agent
from live_commentary.cricket.agent import cricket_live_commentary_agent
from live_scores.cricket.agent import cricket_live_scores_agent
from live_scores.football.agent import football_live_scores_agent

manager_agent=CodeAgent(
    tools=[],
    model=load_model(),
    managed_agents=[cricket_live_commentary_agent,cricket_live_scores_agent,football_live_scores_agent],
    additional_authorized_imports=["time","numpy","pandas","requests", "bs4"],
)
from smolagents import ToolCallingAgent,DuckDuckGoSearchTool,CodeAgent
from model.load_model import load_model
from pipeline.cricket.live_scores_cricket import cricket_live_scores_pipeline


cricket_live_scores_agent = CodeAgent(
    tools=[cricket_live_scores_pipeline],
    model=load_model(),
    max_steps=10,
    name="cricket_live_scores_agent",
    description="""
    A specialized agent that scrapes and processes live cricket match scores from Cricbuzz.
    
    This agent continuously monitors Cricbuzz's website for live cricket match updates and extracts
    structured data using BeautifulSoup. It can:
    
    - Collect real-time score data from multiple ongoing cricket matches
    - Parse match cards to extract teams, scores, and match status
    - Filter out duplicate updates to provide only fresh information
    - Output structured data to a JSONL file for further processing
    
    The agent uses Pathway's data pipeline framework to establish a continuous data flow,
    ensuring you always have the latest cricket scores without manual intervention.
    
    Perfect for cricket enthusiasts, sports apps, or data analysis projects requiring
    up-to-date cricket match information.
    """,
)
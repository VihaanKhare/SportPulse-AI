from smolagents import ToolCallingAgent,DuckDuckGoSearchTool,CodeAgent
from model.load_model import load_model
from pipeline.football.live_scores_fifa import football_live_scores_pipeline

football_live_scores_agent = CodeAgent(
    tools=[football_live_scores_pipeline],
    model=load_model(),
    max_steps=10,
    name="football_live_scores_agent",
    description="""
    A specialized agent that scrapes and processes live FIFA football match data from ESPN.
    
    This agent leverages Selenium and BeautifulSoup to extract match information from
    JavaScript-rendered content on ESPN's football scoreboard pages. It can:
    
    - Access dynamic content that requires JavaScript rendering
    - Extract information from FIFA World Cup Qualifier matches and other competitions
    - Process and structure football match data in a consistent format
    - Output structured match data to a JSONL file at regular intervals
    
    The agent uses Pathway's data pipeline framework with a custom connector subject to
    maintain a continuous flow of up-to-date football match information.
    
    Ideal for football fans, sports analytics platforms, or applications that need real-time
    FIFA match data without the complexity of implementing custom web scrapers.
    """,
)
from smolagents import CodeAgent
from model.load_model import load_model
from pipeline.cricket.live_commentary_cricket import cricket_live_commentary_pipeline

cricket_live_commentary_agent = CodeAgent(
    tools=[cricket_live_commentary_pipeline],
    model=load_model(),
    max_steps=10,
    name="cricket_live_commentary_agent",
    description="""
    A specialized agent that fetches real-time ball-by-ball cricket commentary from live matches.
    
    This agent connects to Cricbuzz, identifies active cricket matches, and extracts
    detailed play-by-play commentary for the most recent match in progress. It can:
    
    - Find all currently active cricket matches
    - Select and follow a specific match
    - Extract detailed commentary including wickets, boundaries, and key moments
    - Save the commentary to a text file for further analysis
    
    The agent uses Selenium for JavaScript rendering and BeautifulSoup for HTML parsing
    to ensure accurate and up-to-date commentary is retrieved even from dynamic content.
    
    Perfect for cricket enthusiasts who want to follow matches through text commentary
    or build applications that analyze cricket match events.
    """,
)
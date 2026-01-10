from smolagents import CodeAgent
from model.load_model import load_model

football_live_commentary_agent=CodeAgent(
    tools=[],
    model=load_model(),
    max_steps=10,
    name="football_live_commentary_agent",
    description="Returns football live commentary to you.",
)
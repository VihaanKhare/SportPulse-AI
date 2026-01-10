from crewai import LLM, Agent, Crew, Task, Process
from crewai.project import CrewBase, agent,task, crew, after_kickoff
from crewai_tools import WebsiteSearchTool,SerplyWebSearchTool,BraveSearchTool

@CrewBase
class SportsChatbotCrew:
    
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
 
        
    @agent
    def sports_data_collector(self) -> Agent:
            return Agent(
                config=self.agents_config['sports_data_collector'],
                verbose=True,
                tools=[WebsiteSearchTool,SerplyWebSearchTool,BraveSearchTool],
                llm='gemini/gemini-1.5-pro'
            )
            
    @agent 
    def input_processor(self) -> Agent:
        return Agent(
            config=self.agents_config['input_processor'],
            llm=LLM('gemini/gemini-1.5-pro',temperature=0),
            verbose=True,
        )
        
    @task
    def structure_player_query(self) -> Task:
        return Task(
            config=self.agents_config['structure_player_query']
        )
    
    @task
    def fetch_player_info_task(self) -> Task:
        return Task(
            config=self.agents_config['fetch_player_info'],
            context=["structure_player_query"]
        )
        
    @after_kickoff
    def after_kickoff_function(self):
        print(f"Hope u are satisfied by the results")
    
    @crew
    def crew(self)->Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            planning=True
        )
        
    # @task
    # def live_match_updates_task():
        

    # @task
    # def cricket_tournament_standings_task():
        
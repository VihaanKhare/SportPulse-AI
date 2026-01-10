import sys
from dotenv import load_dotenv
import os
import warnings

from datetime import datetime

from crew import  SportsChatbotCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run():
    """ Run the crew """
    
    inputs ={
        "query":"Give me information about Virat Kohli, who plays cricket"
    }
    
    SportsChatbotCrew().crew().kickoff(inputs=inputs)
    

    
    
    

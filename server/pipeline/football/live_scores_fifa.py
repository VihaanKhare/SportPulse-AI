from bs4 import BeautifulSoup
import json
import time
import pathway as pw
from pathway.io.python import ConnectorSubject
# from pipeline.football.utils.fifa_parser import parse_fifa_matches
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from smolagents import tool

import re

def parse_fifa_matches(match_results):
    """
    Parse FIFA match results from raw text data into structured format.
    
    This function processes an array of text strings containing FIFA match results,
    extracting team names, scores, match status, and win/draw/loss records.
    It handles the specific format of ESPN football match results.
    
    Args:
        match_results (list): List of strings containing raw FIFA match result data,
                             typically scraped from ESPN's website.
        
    Returns:
        list: List of dictionaries, each containing structured information about
              a FIFA match with the following structure:
              {
                  "status": str,  # Usually "FT" for Full Time
                  "team1": {
                      "name": str,
                      "record": {
                          "wins": int,
                          "draws": int,
                          "losses": int
                      },
                      "score": int
                  },
                  "team2": {
                      "name": str,
                      "record": {
                          "wins": int,
                          "draws": int,
                          "losses": int
                      },
                      "score": int
                  },
                  "winner": str or None  # Name of winning team, "Draw..." or None
              }
    
    Raises:
        ValueError: If scores cannot be extracted from the result string.
        Various exceptions may be caught internally with error messages printed.
    """
    parsed_results = []
    
    for result in match_results:
        try:
            # Extract status code (usually 'FT' for Full Time)
            status = re.match(r'^([A-Z]+)', result).group(1)
            status = status[:2]
            
            # Remove status code from the beginning
            result = result[len(status):]
            
            # Find positions of key elements
            first_paren_open = result.find('(')
            first_paren_close = result.find(')', first_paren_open)
            
            # Extract team1 information
            team1_name = result[:first_paren_open].strip()
            team1_record = result[first_paren_open+1:first_paren_close].split('-')
            team1_wins = int(team1_record[0])
            team1_draws = int(team1_record[1])
            team1_losses = int(team1_record[2])
            
            # Find team1 score - it's the digit right after the closing parenthesis
            score_pattern = re.compile(r'\)(\d+)')
            scores = score_pattern.findall(result)
            
            if len(scores) >= 2:
                team1_score = int(scores[0])
                team2_score = int(scores[1])
            else:
                raise ValueError(f"Could not extract scores from: {result}")
            
            # Find the second team's data
            second_paren_open = result.find('(', first_paren_close)
            second_paren_close = result.find(')', second_paren_open)
            
            # Extract team2 name - it's between team1's score and team2's opening parenthesis
            # First get the position of team1's score digit
            team1_score_pos = result.find(str(team1_score), first_paren_close)
            team1_score_end = team1_score_pos + len(str(team1_score))
            
            team2_name = result[team1_score_end:second_paren_open].strip()
            
            # Extract team2 record
            team2_record = result[second_paren_open+1:second_paren_close].split('-')
            team2_wins = int(team2_record[0])
            team2_draws = int(team2_record[1])
            team2_losses = int(team2_record[2])
            
            # Determine winner only if the match is finished (FT)
            winner = None
            if status == "FT":
                if team1_score > team2_score:
                    winner = team1_name
                elif team2_score > team1_score:
                    winner = team2_name
                elif team1_score == team2_score:
                    winner = "Draw between " + team1_name + " and " + team2_name
                # If scores are equal, it's a draw
            
            # Create the match object
            match_obj = {
                "status": status,
                "team1": {
                    "name": team1_name,
                    "record": {
                        "wins": team1_wins,
                        "draws": team1_draws,
                        "losses": team1_losses
                    },
                    "score": team1_score
                },
                "team2": {
                    "name": team2_name,
                    "record": {
                        "wins": team2_wins,
                        "draws": team2_draws,
                        "losses": team2_losses
                    },
                    "score": team2_score
                },
                "winner": winner
            }
            
            parsed_results.append(match_obj)
            
        except Exception as e:
            print(f"Error parsing result: {result}")
            print(f"Error details: {str(e)}")
    
    return parsed_results

class ConnectorSchema(pw.Schema):
    """
    Schema definition for the FIFA data pipeline.
    
    This schema defines the structure of the data flowing through
    the Pathway pipeline, including primary keys and field types.
    
    Attributes:
        url (str): The URL of the scraped website, used as the primary key.
        data (dict): The parsed FIFA match data.
        metadata (dict): Additional information about the scraping process.
    """
    url: str = pw.column_definition(primary_key=True)
    data: dict
    metadata: dict

def live_sports_data_json(website):
    """
    Scrape live FIFA match data from the specified website and convert it to structured format.
    
    This function uses Selenium to render JavaScript content from the website,
    extracts FIFA match information using BeautifulSoup, and returns structured data after parsing.
    
    Args:
        website (str): URL of the ESPN football website to scrape data from.
        
    Returns:
        list: List of dictionaries containing parsed FIFA match information.
    """
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    driver.get(website)
    dom = driver.page_source
    
    with open("html_dom.html", "w") as f:
        f.write(dom)
    
    driver.quit()
    
    soup = BeautifulSoup(dom, "html.parser")
    cards = soup.find_all(
        'div',
        class_='ScoreboardScoreCell pa4 FIFA.WORLDQ.AFC soccer ScoreboardScoreCell--post ScoreboardScoreCell--tabletPlus'
    )
    
    cardContent = [card.get_text() for card in cards]
    
    livedata = parse_fifa_matches(cardContent)
    return livedata

def scrape_espn(website_url, refresh_interval):
    """
    Continuously scrape FIFA data from ESPN at specified intervals.
    
    This generator function repeatedly retrieves FIFA match data, filters out
    previously seen entries, and yields new data with metadata.
    
    Args:
        website_url (str): URL of the ESPN football website to scrape data from.
        refresh_interval (int): Time in seconds to wait between scraping attempts.
        
    Yields:
        dict: A dictionary containing the URL, scraped data, and metadata for new FIFA match entries.
    """
    indexed_set = set()
    
    while True:
        jsonDataSet = live_sports_data_json(website_url)
        for dataEntry in jsonDataSet:
            dataEntryStr = json.dumps(dataEntry, sort_keys=True)
            if dataEntryStr in indexed_set:
                continue
            
            metadata = {
                "url": website_url,
                "timestamp": time.time(),
            }
            
            indexed_set.add(dataEntryStr)
            yield {
                "url": website_url,
                "data": dataEntry,
                "metadata": metadata,
            }
        
        time.sleep(refresh_interval)

class FifaScraperSubject(ConnectorSubject):
    """
    A Pathway connector subject for scraping FIFA match data.
    
    This class manages the process of scraping FIFA match information
    and feeding it into a Pathway data pipeline.
    
    Args:
        website_urls (str): URL of the ESPN football website to scrape data from.
        refresh_interval (int): Time in seconds to wait between scraping attempts.
    """
    def __init__(self, website_urls, refresh_interval):
        super().__init__()
        self._website_urls = website_urls
        self._refresh_interval = refresh_interval
    
    def run(self):
        """
        Execute the FIFA data scraping process.
        
        This method retrieves FIFA match data continuously and
        passes it to the Pathway connector for processing.
        """
        for live_football_data in scrape_espn(
            self._website_urls,
            refresh_interval=self._refresh_interval,
        ):
            self.next(
                url=live_football_data["url"],
                data=live_football_data["data"],
                metadata=live_football_data["metadata"]
            )

@tool
def football_live_scores_pipeline(
    website_url: str = "https://www.espn.in/football/scoreboard/_/league/fifa.worldq.afc",
    refresh_interval: int = 25,
    output_file: str = "scraped_live_fifa.jsonl"
)->None:
    """
    Create and run a data pipeline for scraping live FIFA football scores.
    
    This function sets up a complete Pathway pipeline that scrapes FIFA match
    data from the specified ESPN website at regular intervals and writes the results
    to a JSONL file. It uses Selenium for rendering JavaScript content and
    BeautifulSoup for HTML parsing.
    
    Args:
        website_url (str, optional): URL of the ESPN football website to scrape.
            Defaults to "https://www.espn.in/football/scoreboard/_/league/fifa.worldq.afc".
        refresh_interval (int, optional): Time in seconds to wait between
            scraping attempts. Defaults to 25.
        output_file (str, optional): Path to the output JSONL file.
            Defaults to "scraped_live_fifa.jsonl".
    
    Returns:
        None: The function runs the pipeline until manually interrupted.
    """
    subject = FifaScraperSubject(
        website_urls=website_url,
        refresh_interval=refresh_interval,
    )
    
    espn_results = pw.io.python.read(subject, schema=ConnectorSchema)
    pw.io.jsonlines.write(espn_results, output_file)
    
    pw.run()

def football_live_scores_pipeline_api(
    website_url: str = "https://www.espn.in/football/scoreboard/_/league/fifa.worldq.afc",
    refresh_interval: int = 25,
    output_file: str = "scraped_live_fifa.jsonl"
)->None:
    """
    Create and run a data pipeline for scraping live FIFA football scores.
    
    This function sets up a complete Pathway pipeline that scrapes FIFA match
    data from the specified ESPN website at regular intervals and writes the results
    to a JSONL file. It uses Selenium for rendering JavaScript content and
    BeautifulSoup for HTML parsing.
    
    Args:
        website_url (str, optional): URL of the ESPN football website to scrape.
            Defaults to "https://www.espn.in/football/scoreboard/_/league/fifa.worldq.afc".
        refresh_interval (int, optional): Time in seconds to wait between
            scraping attempts. Defaults to 25.
        output_file (str, optional): Path to the output JSONL file.
            Defaults to "scraped_live_fifa.jsonl".
    
    Returns:
        None: The function runs the pipeline until manually interrupted.
    """
    subject = FifaScraperSubject(
        website_urls=website_url,
        refresh_interval=refresh_interval,
    )
    
    espn_results = pw.io.python.read(subject, schema=ConnectorSchema)
    pw.io.jsonlines.write(espn_results, output_file)
    
    pw.run()

if __name__=="__main__":
    football_live_scores_pipeline_api()
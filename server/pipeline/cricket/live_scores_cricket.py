import requests
from bs4 import BeautifulSoup
import json
import time
import pathway as pw
from pathway.io.python import ConnectorSubject
# from pipeline.cricket.utils.cricket_parser import parse_cricket_matches
from smolagents import tool

websites = "https://www.cricbuzz.com/"
import re

def parse_cricket_matches(data_array):
    """
    Parse cricket match data from an array of text strings into structured format.
    
    This function processes raw text data from cricket match websites,
    extracting detailed information about each match including teams, scores,
    tournament details, and results.
    
    Args:
        data_array (list): List of strings containing raw cricket match data,
                          typically scraped from a website.
        
    Returns:
        list: List of dictionaries, each containing structured information about
              a cricket match with the following structure:
              {
                  "matchNumber": int,
                  "tournament": {
                      "name": str,
                      "shortName": str,
                      "format": str
                  },
                  "status": str,  # "completed" or "upcoming"
                  "teams": {
                      "team1": {
                          "name": str,
                          "shortName": str,
                          "score": int or None,
                          "wickets": int or None,
                          "overs": float or None
                      },
                      "team2": {
                          "name": str,
                          "shortName": str,
                          "score": int or None,
                          "wickets": int or None,
                          "overs": float or None
                      }
                  },
                  "result": {
                      "winner": str or None,
                      "margin": str or None,
                      "winningMethod": str or None
                  },
                  "links": list of str
              }
    """
    # Initialize the results array
    matches = []
    
    for match_data in data_array:
        # Remove extra spaces
        match_data = ' '.join(match_data.split())
        
        # Extract match number, tournament and format
        match_info_pattern = r'(\d+)(?:st|nd|rd|th) Match • (.*?) (T20)'
        match_info = re.search(match_info_pattern, match_data)
        
        if not match_info:
            continue
            
        match_number = int(match_info.group(1))
        tournament_name = match_info.group(2)
        format_type = match_info.group(3)
        
        # Determine tournament short name
        if "Indian Premier League" in tournament_name:
            short_name = "IPL 2025"
        elif "Pakistan Super League" in tournament_name:
            short_name = "PSL 2025"
        else:
            short_name = tournament_name
        
        # Create tournament info
        tournament_info = {
            "name": tournament_name,
            "shortName": short_name,
            "format": format_type
        }
        
        # Extract team and score information
        score_pattern = r'([A-Z]+)(\d+)(?:-(\d+))? \((\d+\.\d+|\d+)\)'
        score_matches = list(re.finditer(score_pattern, match_data))
        
        # Check if match is completed or upcoming
        if len(score_matches) >= 2:
            status = "completed"
            
            # Team 1 info
            team1_short = score_matches[0].group(1)
            team1_score = int(score_matches[0].group(2))
            team1_wickets = int(score_matches[0].group(3)) if score_matches[0].group(3) else None
            team1_overs = float(score_matches[0].group(4))
            
            # Team 2 info
            team2_short = score_matches[1].group(1)
            team2_score = int(score_matches[1].group(2))
            team2_wickets = int(score_matches[1].group(3)) if score_matches[1].group(3) else None
            team2_overs = float(score_matches[1].group(4))
            
            # Extract full team names and result
            result_pattern = r'([A-Za-z ]+) won by ([0-9]+ (?:runs|wkts))'
            result_match = re.search(result_pattern, match_data)
            
            if result_match:
                winner_name = result_match.group(1)
                margin = result_match.group(2)
                winning_method = "runs" if "runs" in margin else "wickets"
                
                # Determine full team names
                if winner_name in match_data.split(str(match_number)):
                    team1_name = winner_name
                    # Try to extract team2 name from the match data
                    remaining_text = match_data.replace(team1_name, "", 1)
                    team2_name = extract_team_name(remaining_text, team2_short)
                else:
                    team2_name = winner_name
                    # Try to extract team1 name from the match data
                    remaining_text = match_data.replace(team2_name, "", 1)
                    team1_name = extract_team_name(remaining_text, team1_short)
            else:
                # If we can't extract result, use placeholders
                team1_name = get_full_team_name(team1_short)
                team2_name = get_full_team_name(team2_short)
                winner_name = None
                margin = None
                winning_method = None
            
            # Extract links
            links = re.findall(r'fantasy|table|schedule|points table', match_data.lower())
            
            # Create the match object
            match_obj = {
                "matchNumber": match_number,
                "tournament": tournament_info,
                "status": status,
                "teams": {
                    "team1": {
                        "name": team1_name,
                        "shortName": team1_short,
                        "score": team1_score,
                        "wickets": team1_wickets,
                        "overs": team1_overs
                    },
                    "team2": {
                        "name": team2_name,
                        "shortName": team2_short,
                        "score": team2_score,
                        "wickets": team2_wickets,
                        "overs": team2_overs
                    }
                },
                "result": {
                    "winner": winner_name,
                    "margin": margin,
                    "winningMethod": winning_method
                },
                "links": links
            }
        else:
            # This is an upcoming match
            status = "upcoming"
            
            # Extract team names for upcoming matches
            parts = match_data.split('•')[1].strip()
            team_parts = parts.split()
            
            # Remove format and match number
            clean_parts = [p for p in team_parts if p.strip() and not re.match(r'T20|fantasy|table|schedule|points', p.lower())]
            
            # Extract team names - they're usually the last distinct words before links section
            if len(clean_parts) >= 2:
                team1_name = clean_parts[0]
                team2_name = clean_parts[1]
                
                # Handle multi-word team names
                for i in range(2, len(clean_parts)):
                    if clean_parts[i] in ["fantasy", "table", "schedule", "points"]:
                        break
                    if i % 2 == 0:  # Even indices belong to team2
                        team2_name += " " + clean_parts[i]
                    else:  # Odd indices belong to team1
                        team1_name += " " + clean_parts[i]
            else:
                team1_name = "Unknown Team 1"
                team2_name = "Unknown Team 2"
            
            # Extract links
            links = re.findall(r'fantasy|table|schedule|points table', match_data.lower())
            
            # Create the match object for upcoming matches
            match_obj = {
                "matchNumber": match_number,
                "tournament": tournament_info,
                "status": status,
                "teams": {
                    "team1": {
                        "name": team1_name,
                        "shortName": get_short_name(team1_name),
                        "score": None,
                        "wickets": None,
                        "overs": None
                    },
                    "team2": {
                        "name": team2_name,
                        "shortName": get_short_name(team2_name),
                        "score": None,
                        "wickets": None,
                        "overs": None
                    }
                },
                "result": None,
                "links": links
            }
        
        # Add match to results array
        matches.append(match_obj)
    
    return matches

def extract_team_name(text, short_name):
    """
    Extract the full team name based on team abbreviation.
    
    Args:
        text (str): The text to search for team names (not used in current implementation).
        short_name (str): Abbreviation of the team name (e.g., "PBKS", "KKR").
        
    Returns:
        str: Full team name corresponding to the short name, or a placeholder if unknown.
    """
    if short_name == "PBKS":
        return "Punjab Kings"
    elif short_name == "KKR":
        return "Kolkata Knight Riders"
    elif short_name == "LSG":
        return "Lucknow Super Giants"
    elif short_name == "CSK":
        return "Chennai Super Kings"
    elif short_name == "LHQ":
        return "Lahore Qalandars"
    elif short_name == "KRK":
        return "Karachi Kings"
    elif short_name == "ISU":
        return "Islamabad United"
    elif short_name == "PSZ":
        return "Peshawar Zalmi"
    elif short_name == "DC":
        return "Delhi Capitals"
    elif short_name == "RR":
        return "Rajasthan Royals"
    elif short_name == "MS":
        return "Multan Sultans"
    return f"Unknown Team ({short_name})"

def get_full_team_name(short_name):
    """
    Get the full team name from a team abbreviation.
    
    This is a wrapper around extract_team_name that doesn't require text input.
    
    Args:
        short_name (str): Abbreviation of the team name (e.g., "PBKS", "KKR").
        
    Returns:
        str: Full team name corresponding to the short name, or a placeholder if unknown.
    """
    return extract_team_name("", short_name)

def get_short_name(full_name):
    """
    Generate team abbreviation from the full team name.
    
    This function maps common cricket team names to their official abbreviations,
    or generates an abbreviation using the first letter of each word in the team name.
    
    Args:
        full_name (str): Full name of the cricket team (e.g., "Punjab Kings").
        
    Returns:
        str: Team abbreviation (e.g., "PBKS") if the team is recognized,
             otherwise a generated abbreviation using first letters of each word.
    """
    team_mapping = {
        # IPL Teams
        "Punjab Kings": "PBKS",
        "Kolkata Knight Riders": "KKR",
        "Lucknow Super Giants": "LSG",
        "Chennai Super Kings": "CSK",
        "Delhi Capitals": "DC",
        "Rajasthan Royals": "RR",   
        "Mumbai Indians": "MI",
        "Royal Challengers Bangalore": "RCB",
        "Sunrisers Hyderabad": "SRH",
        "Gujarat Titans": "GT",

        # PSL Teams
        "Lahore Qalandars": "LHQ",
        "Karachi Kings": "KRK",
        "Islamabad United": "ISU",
        "Peshawar Zalmi": "PSZ",
        "Multan Sultans": "MS",
        "Quetta Gladiators": "QG"
    }
    
    return team_mapping.get(full_name, ''.join(word[0] for word in full_name.split()))

def live_sports_data_json(website):
    """
    Scrape live cricket match data from the specified website and convert it to JSON format.
    
    This function retrieves the HTML content of the provided website, extracts cricket match
    information from it, and returns structured data after parsing.
    
    Args:
        website (str): URL of the cricket website to scrape data from.
        
    Returns:
        list: List of dictionaries containing parsed cricket match information.
    """
    dom = requests.get(website)
    
    with open("html_dom.html", "w") as f:
        f.write(dom.text)
    
    soup = BeautifulSoup(dom.text, "html.parser")
    cards = soup.find_all('li', class_='cb-view-all-ga cb-match-card cb-bg-white')
    
    cardContent = []
    
    for card in cards:
        cardContent.append(card.text)
    
    livedata = parse_cricket_matches(cardContent)
    return livedata

def scrape_cricbuzz(website_url, refresh_interval):
    """
    Continuously scrape cricket data from Cricbuzz at specified intervals.
    
    This generator function repeatedly retrieves cricket match data, filters out
    previously seen entries, and yields new data with metadata.
    
    Args:
        website_url (str): URL of the cricket website to scrape data from.
        refresh_interval (int): Time in seconds to wait between scraping attempts.
        
    Yields:
        dict: A dictionary containing the URL, scraped data, and metadata for new cricket match entries.
    """
    indexed_set = set()
    
    while True:
        jsonDataSet = live_sports_data_json(website_url)
        for dataEntry in jsonDataSet:
            dataEntryStr = json.dumps(dataEntry, sort_keys=True)
            if dataEntryStr in indexed_set:
                continue
            
            url = website_url
            data = dataEntry
            metadata = {
                "url": url,
                "timestamp": time.time(),
            }
            
            yield {"url": url, "data": data, "metadata": dict(metadata)}
        
        time.sleep(refresh_interval)

class CricketScraperSubject(ConnectorSubject):
    """
    A Pathway connector subject for scraping cricket data.
    
    This class manages the process of scraping cricket match information
    and feeding it into a Pathway data pipeline.
    
    Args:
        website_urls (str): URL of the cricket website to scrape data from.
        refresh_interval (int): Time in seconds to wait between scraping attempts.
    """
    def __init__(self, website_urls, refresh_interval):
        super().__init__()
        self._website_urls = website_urls
        self._refresh_interval = refresh_interval
    
    def run(self):
        """
        Execute the cricket data scraping process.
        
        This method retrieves cricket match data continuously and
        passes it to the Pathway connector for processing.
        """
        for live_cricket_data in scrape_cricbuzz(
            self._website_urls,
            refresh_interval=self._refresh_interval,
        ):
            url = live_cricket_data["url"]
            data = live_cricket_data["data"]
            metadata = live_cricket_data["metadata"]
            
            self.next(url=url, data=data, metadata=metadata)

class ConnectorSchema(pw.Schema):
    """
    Schema definition for the cricket data pipeline.
    
    This schema defines the structure of the data flowing through
    the Pathway pipeline, including primary keys and field types.
    
    Attributes:
        url (str): The URL of the scraped website, used as the primary key.
        data (dict): The parsed cricket match data.
        metadata (dict): Additional information about the scraping process.
    """
    url: str = pw.column_definition(primary_key=True)
    data: dict
    metadata: dict

@tool
def cricket_live_scores_pipeline(
    website_url: str = "https://www.cricbuzz.com/",
    refresh_interval: int = 25,
    output_file: str = "scraped_live_cricket.jsonl"
)-> None:
    """
    Create and run a data pipeline for scraping live cricket scores.
    
    This function sets up a complete Pathway pipeline that scrapes cricket match
    data from the specified website at regular intervals and writes the results
    to a JSONL file.
    
    Args:
        website_url (str, optional): URL of the cricket website to scrape.
            Defaults to "https://www.cricbuzz.com/".
        refresh_interval (int, optional): Time in seconds to wait between
            scraping attempts. Defaults to 25.
        output_file (str, optional): Path to the output JSONL file.
            Defaults to "scraped_live_cricket.jsonl".
    
    Returns:
        None: The function runs the pipeline until manually interrupted.
    """
    subject = CricketScraperSubject(
        website_urls=website_url,
        refresh_interval=refresh_interval,
    )
    
    cricbuzz_results = pw.io.python.read(subject, schema=ConnectorSchema)
    
    pw.io.jsonlines.write(cricbuzz_results, output_file)
    
    pw.run()

def cricket_live_scores_pipeline_api(
    website_url: str = "https://www.cricbuzz.com/",
    refresh_interval: int = 25,
    output_file: str = "scraped_live_cricket.jsonl"
)-> None:
    """
    Create and run a data pipeline for scraping live cricket scores.
    
    This function sets up a complete Pathway pipeline that scrapes cricket match
    data from the specified website at regular intervals and writes the results
    to a JSONL file.
    
    Args:
        website_url (str, optional): URL of the cricket website to scrape.
            Defaults to "https://www.cricbuzz.com/".
        refresh_interval (int, optional): Time in seconds to wait between
            scraping attempts. Defaults to 25.
        output_file (str, optional): Path to the output JSONL file.
            Defaults to "scraped_live_cricket.jsonl".
    
    Returns:
        None: The function runs the pipeline until manually interrupted.
    """
    subject = CricketScraperSubject(
        website_urls=website_url,
        refresh_interval=refresh_interval,
    )
    
    cricbuzz_results = pw.io.python.read(subject, schema=ConnectorSchema)
    
    pw.io.jsonlines.write(cricbuzz_results, output_file)
    print("writing to file cricket json")
    pw.run()

if __name__=="__main__":
    cricket_live_scores_pipeline_api()
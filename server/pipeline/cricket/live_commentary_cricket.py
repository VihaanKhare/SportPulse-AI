import requests
import json
import time
from bs4 import BeautifulSoup
import pathway as pw
from pathway.io.python import ConnectorSubject
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from smolagents import tool

def fetch_live_commentary_urls(website):
    """
    Scrape URLs of live cricket match commentaries from the specified website.
    
    This function retrieves the HTML content of the provided cricket website,
    extracts links to full commentary pages, and returns them as a list of URLs.
    
    Args:
        website (str): URL of the cricket website to scrape commentary links from,
                      typically the live scores page.
        
    Returns:
        list: List of complete URLs to active cricket match commentary pages.
    """
    dom = requests.get(website)
    with open("html_dom.html", "w") as f:
        f.write(dom.text)
    
    soup = BeautifulSoup(dom.text, "html.parser")
    cards = soup.find_all('a', title='Full Commentary')
    
    active_urls = [
        "https://www.cricbuzz.com" + card.get('href') for card in cards
    ]
    return active_urls

# actieveUrls = fetch_live_commentary_urls(website)
# print("active urls: ", actieveUrls)

def fetch_commentary(website):
    """
    Retrieve the live ball-by-ball commentary for cricket matches.
    
    This function first finds URLs of active commentary pages, then uses Selenium
    to load the JavaScript content of the first available commentary page,
    and extracts the textual commentary using BeautifulSoup.
    
    Args:
        website (str): URL of the cricket website's live scores page.
        
    Returns:
        list: List of commentary text lines from the most recent cricket match,
              or an empty list if no active matches are found.
    """
    active_urls = fetch_live_commentary_urls(website)
    if not active_urls:
        print("No active commentary URLs found.")
        return []
    
    # Initialize WebDriver inside function
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    driver.get(active_urls[0])
    dom = driver.page_source
    
    with open("html_dom.html", "w") as f:
        f.write(dom)
    
    driver.quit()
    
    soup = BeautifulSoup(dom, "html.parser")
    cards = soup.find_all(
        'p',
        class_='cb-com-ln ng-binding ng-scope cb-col cb-col-90'
    )
    
    commentary_list = [card.text for card in cards]
    return commentary_list

@tool
def cricket_live_commentary_pipeline(
    root_url: str = "https://www.cricbuzz.com/cricket-match/live-scores",
    output_file: str = "cricbuzz_commentary.txt"
)->None:
    """
    Run a pipeline to fetch and save live cricket match commentary.
    
    This function extracts ball-by-ball commentary from an active cricket match
    on Cricbuzz and writes it to a text file. It handles the entire process from
    finding active matches to saving the commentary text.
    
    Args:
        root_url (str, optional): URL of the cricket website's live scores page.
            Defaults to "https://www.cricbuzz.com/cricket-match/live-scores".
        output_file (str, optional): Path to the output text file where commentary
            will be saved. Defaults to "cricbuzz_commentary.txt".
    
    Returns:
        None: The function either writes commentary to the specified file or
              prints a message if no commentary is available.
    """
    commentary_list = fetch_commentary(root_url)
        
    if commentary_list:
        with open(output_file, "w", encoding="utf-8") as f:
            for line in commentary_list:
                f.write(line + "\n")
        print(f"Commentary written to {output_file}")
    else:
        print("No commentary fetched.")

def cricket_live_commentary_pipeline_api(
    root_url: str = "https://www.cricbuzz.com/cricket-match/live-scores",
    output_file: str = "cricbuzz_commentary.txt"
)->None:
    """
    Run a pipeline to fetch and save live cricket match commentary.
    
    This function extracts ball-by-ball commentary from an active cricket match
    on Cricbuzz and writes it to a text file. It handles the entire process from
    finding active matches to saving the commentary text.
    
    Args:
        root_url (str, optional): URL of the cricket website's live scores page.
            Defaults to "https://www.cricbuzz.com/cricket-match/live-scores".
        output_file (str, optional): Path to the output text file where commentary
            will be saved. Defaults to "cricbuzz_commentary.txt".
    
    Returns:
        None: The function either writes commentary to the specified file or
              prints a message if no commentary is available.
    """
    commentary_list = fetch_commentary(root_url)
        
    if commentary_list:
        with open(output_file, "w", encoding="utf-8") as f:
            for line in commentary_list:
                f.write(line + "\n")
        print(f"Commentary written to {output_file}")
    else:
        print("No commentary fetched.")

if __name__=="__main__":
    cricket_live_commentary_pipeline_api()
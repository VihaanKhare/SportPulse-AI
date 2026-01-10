"""
Cricket Player Information Scraper

This module provides functionality to scrape and extract information about
cricket players by first searching Google for the player and then extracting
their details from ESPNcricinfo using Selenium to bypass anti-scraping measures.
"""

import time
from typing import Dict, List, Optional, Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

player_name = "Virat Kohli"


def configure_chrome_driver() -> webdriver.Chrome:
    """
    Configure and initialize a Chrome WebDriver with anti-detection settings.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    chrome_options = ChromeOptions()
    
    # Basic browser configuration
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless")  # Uncomment for headless operation
    
    # Anti-detection settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Add a user agent to appear more like a regular browser
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
    
    # Initialize driver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Apply additional anti-detection techniques
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    
    return driver


def google_search(query: str, target_domain: str = "www.espncricinfo.com") -> Tuple[str, List[str]]:
    """
    Perform a Google search and find links related to a specific domain.
    
    Args:
        query (str): The search query string
        target_domain (str, optional): Domain to prioritize in search results. 
                                      Defaults to "www.espncricinfo.com".
    
    Returns:
        Tuple[str, List[str]]: A tuple containing the first link matching the target domain 
                              and a list of all found links
    """
    driver = configure_chrome_driver()
    
    try:
        # Format query for URL
        formatted_query = "+".join(str(query).split())
        search_url = f"https://www.google.com/search?q={formatted_query}"
        
        # Execute search
        print(f"Searching Google for: {query}")
        driver.get(search_url)
        time.sleep(3)  # Wait for page to load
        
        # Save the raw HTML data
        data = driver.page_source
        with open('chrome_output.html', 'w', encoding='utf-8') as f:
            f.write(data)
        print(f"Chrome Title: {driver.title}")
        print("Chrome data saved to chrome_output.html")
        
        # Process search results
        return extract_links_from_search(data, target_domain)
        
    finally:
        driver.quit()


def extract_links_from_search(html_content: str, target_domain: str) -> Tuple[str, List[str]]:
    """
    Extract links from Google search results HTML, prioritizing a specific domain.
    
    Args:
        html_content (str): HTML content from Google search results
        target_domain (str): Domain to prioritize in search results
    
    Returns:
        Tuple[str, List[str]]: A tuple containing the first link matching the target domain 
                              and a list of all found links
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_list = soup.find_all('h3')
    
    target_link = ""
    all_links = []
    
    for h3 in h3_list:
        if h3.parent and h3.parent.name == "a":
            href = h3.parent.get('href', '')
            if href:
                all_links.append(href)
                
                if target_domain in href and not target_link:
                    target_link = href
                    print(f"Found target link: {target_link}")
    
    print(f"Total links found: {len(all_links)}")
    return target_link, all_links


def fetch_player_page_with_selenium(url: str) -> str:
    """
    Fetch the HTML content of a player's profile page using Selenium to bypass blocks.
    
    Args:
        url (str): URL of the player's profile page
    
    Returns:
        str: HTML content of the player's profile page
    """
    driver = configure_chrome_driver()
    
    try:
        print(f"Fetching player data from: {url}")
        driver.get(url)
        
        # Wait for the page to load properly
        time.sleep(4)
        
        # Save the HTML for debugging
        html_content = driver.page_source
        with open('player_page.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Player page data saved to player_page.html")
        
        return html_content
        
    except Exception as e:
        print(f"Error fetching player page with Selenium: {e}")
        return ""
    finally:
        driver.quit()


def extract_player_image(soup: BeautifulSoup) -> str:
    """
    Extract the player's image URL from their profile page.
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object of the player's profile page
    
    Returns:
        str: URL of the player's image
    """
    # First attempt: Look for img tags with specific size attributes
    for image in soup.find_all("img"):
        href = image.get("href", "")
        alt = image.get("alt","")
        
        img_url = href
        print(img_url)
      
        if "img1.hscicdn.com" in img_url and player_name.lower() in alt.lower() :
            return img_url
    
    # Second attempt: Look for player profile image classes
    # profile_img = soup.find('img', class_='ds-block')
    # if profile_img and profile_img.get('src'):
    #     return profile_img.get('src')
    
    # # Third attempt: Look for any image that might contain the player
    # for image in soup.find_all("img"):
    #     src = image.get("src", "")
    #     if src and ("player" in src.lower() or "profile" in src.lower()):
    #         return src
            
    return ""


def extract_player_details(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Extract detailed information about a player from their profile page.
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object of the player's profile page
    
    Returns:
        Dict[str, str]: Dictionary containing player details
    """
    player_info = {
        "full_name": "",
        "age": "",
        "born": "",
        "batting_style": "",
        "bowling_style": "",
        "playing_role": "",
        "fielding_position": "",
        "bio": "",
        "image_url": "",
        "teams": []
    }
    
    # Extract the player's image
    player_info["image_url"] = extract_player_image(soup)
    
    # Extract basic player information
    p_list = soup.find_all("p")
    for p in p_list:
        text = p.get_text()
        if text == "Full Name":
          player_info["full_name"] = p.next_sibling.child.get_text()
        elif text == "Born":
          player_info["born"] = p.next_sibling.child.get_text()
        elif text == "Age":
          player_info["age"] = p.next_sibling.child.get_text()
        elif text == "Batting Style":
          player_info["batting_style"] = p.next_sibling.child.get_text()
        elif text == "Bowling Style":
          player_info["bowling_style"] = p.next_sibling.child.get_text()
        elif text == "Playing Role":
          player_info["playing_role"] = p.next_sibling.child.get_text()
        elif text == "Fielding Position":
          player_info["fielding_position"] = p.next_sibling.child.get_text()
        
    bio_div = soup.find_all('div', class_='ci-player-bio-context')
    if bio_div:
        player_info["bio"] = bio_div[0].get_text().strip()
    else:
        # Try alternative bio selectors
        bio_elements = soup.find_all(['p', 'div'], class_=lambda c: c and ('bio' in c.lower() or 'description' in c.lower()))
        if bio_elements:
            player_info["bio"] = bio_elements[0].get_text().strip()
    
    # Extract teams
    player_info["teams"] = extract_player_teams(soup)
    
    # If player name is empty, try to get it from title
    if not player_info["full_name"]:
        title_elem = soup.find('title')
        if title_elem:
            title_text = title_elem.get_text()
            if ' - ' in title_text:
                player_info["full_name"] = title_text.split(' - ')[0].strip()
    
    return player_info


def extract_player_teams(soup: BeautifulSoup) -> List[str]:
    """
    Extract the list of teams a player has been part of.
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object of the player's profile page
    
    Returns:
        List[str]: List of team names
    """
    teams_list = []
    
    # First method - look for team profile links
    for a in soup.find_all('a'):
        if a.get('title', '') and "cricket team profile" in a.get('title', ''):
            try:
                spans = a.find_all('span')
                if spans and len(spans) > 0:
                    inner_spans = spans[0].find_all('span')
                    if inner_spans and len(inner_spans) > 0:
                        team = inner_spans[0].get_text().strip()
                        if team and team not in teams_list:
                            teams_list.append(team)
            except Exception as e:
                print(f"Error extracting team: {e}")
    
    # Second method - look for team sections
    team_sections = soup.find_all(['div', 'section'], string=lambda s: s and 'TEAMS' in s)
    for section in team_sections:
        next_elem = section.find_next(['ul', 'div'])
        if next_elem:
            team_items = next_elem.find_all(['li', 'a'])
            for item in team_items:
                team = item.get_text().strip()
                if team and team not in teams_list:
                    teams_list.append(team)
    
    return teams_list


def display_player_info(player_info: Dict[str, str]) -> None:
    """
    Save formatted player information to a file.

    Args:
        player_info (Dict[str, str]): Dictionary containing player details
    """
    lines = []
    lines.append("=" * 50)
    lines.append("PLAYER INFORMATION")
    lines.append("=" * 50)
    lines.append(f"Full Name: {player_info['full_name']}")

    if player_info['age']:
        lines.append(f"Age: {player_info['age']}")
    if player_info['born']:
        lines.append(f"Born: {player_info['born']}")
    if player_info['batting_style']:
        lines.append(f"Batting Style: {player_info['batting_style']}")
    if player_info['bowling_style']:
        lines.append(f"Bowling Style: {player_info['bowling_style']}")
    if player_info['playing_role']:
        lines.append(f"Playing Role: {player_info['playing_role']}")
    if player_info['fielding_position']:
        lines.append(f"Fielding Position: {player_info['fielding_position']}")
    if player_info['bio']:
        lines.append("\nBio:")
        lines.append(player_info['bio'])
    if player_info['teams']:
        lines.append("\nTeams:")
        for team in player_info['teams']:
            lines.append(f"- {team}")
    if player_info['image_url']:
        lines.append(f"\nImage URL: {player_info['image_url']}")

    # Write to file
    with open("player_info.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Player information saved to player_info.txt")


def get_cricket_player_info(player_name: str) -> Optional[Dict[str, str]]:
    """
    Main function to search for and extract information about a cricket player.
    
    Args:
        player_name (str): Name of the cricket player to search for
    
    Returns:
        Optional[Dict[str, str]]: Dictionary containing player details or None if not found
    """
    try:
        # Search Google for player
        target_link, _ = google_search(f"{player_name} cricket player espncricinfo")
        
        if not target_link:
            print(f"Could not find ESPNcricinfo profile for {player_name}")
            return None
        
        # Fetch and parse player page with Selenium to bypass blocking
        player_html = fetch_player_page_with_selenium(target_link)
        if not player_html:
            return None
            
        player_soup = BeautifulSoup(player_html, "html.parser")
        
        # Extract player information
        player_info = extract_player_details(player_soup)
        
        return player_info
        
    except Exception as e:
        print(f"Error getting player info: {e}")
        return None

def player_info_api(player_name):
    print(f"Searching for information about {player_name}...")
    
    player_info = get_cricket_player_info(player_name)
    
    if player_info:
        display_player_info(player_info)
        
    else:
        print(f"Could not retrieve information for {player_name}")

# if __name__ == "__main__":
#     player_info_api()
#     # Example usage
#     player_name = "Virat Kohli"

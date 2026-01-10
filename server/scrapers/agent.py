from typing import Optional, Type, List
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional, Tuple, Any
from bs4 import BeautifulSoup
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


from google import genai


load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


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
    chrome_options.add_argument("--headless")  # Uncomment for headless operation
    
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


def google_search(query: str, target_domain: str = "www.wikipedia.com") -> str:
    """
    Perform a Google search and find links related to a specific domain.
    
    Args:
        query (str): The search query string
        target_domain (str, optional): Domain to prioritize in search results. 
                                      Defaults to "www.wikipedia.com".
    
    Returns:
        str: The first link matching the target domain
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


def extract_links_from_search(html_content: str, target_domain: str = "wikipedia") -> str:
    """
    Extract links from Google search results HTML, prioritizing a specific domain.
    
    Args:
        html_content (str): HTML content from Google search results
        target_domain (str): Domain to prioritize in search results
    
    Returns:
        str: The first link matching the target domain
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    h3_list = soup.find_all('h3')
    
    target_link = ""
    all_links = []
    
    for h3 in h3_list:
        if h3.parent and h3.parent.name == "a":
            href = h3.parent.get('href', '')
            print(href)
            all_links.append(href)
            if target_domain in href:
                print("in the if condition")
                target_link = href
                print(f"Found target link: {target_link}")
                break
    
    return target_link


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


def search_and_fetch_html(query: str, target_domain: str = "wikipedia") -> str:
    """
    Run a Google search for the query, find a relevant link containing the target domain,
    and fetch the HTML content of that page.
    
    Args:
        query (str): The search query string
        target_domain (str, optional): Domain to prioritize in search results.
                                      Defaults to "wikipedia".
    
    Returns:
        str: HTML content of the found page
    """
    try:
        # First, perform a Google search for the query
        print(f"Starting search for: {query} with target domain: {target_domain}")
        link = google_search(query, target_domain)
        
        # Check if we found a valid link
        if not link:
            print("No relevant links found")
            return ""
        
        # Extract the first link
        target_url = link
        print(f"Using URL: {target_url}")
        
        # Fetch the HTML content of the page
        html_content = fetch_player_page_with_selenium(target_url)
        
        return html_content
        
    except Exception as e:
        print(f"Error in search_and_fetch_html: {e}")
        return ""


def extract_and_clean_bio(p_list) -> str:
    """
    Extract text from paragraph elements, clean it by removing citation numbers,
    and write it to a file with proper formatting.
    
    Args:
        p_list: List of BeautifulSoup paragraph elements
    
    Returns:
        str: Formatted and cleaned text containing the biography
    """
    cleaned_text = []
    
    for p in p_list:
        # Check if we should stop processing paragraphs
        if p.next_sibling and (p.next_sibling.name == 'meta' or p.next_sibling.name == 'div'):
            break
        
        # Get the text and clean it
        text = p.get_text()
        
        # Remove citation numbers like [1], [2], etc.
        cleaned = re.sub(r'\[\d+\]', '', text)
        
        # Add to our collection if there's actual content
        if cleaned.strip():
            cleaned_text.append(cleaned)
    
    # Join paragraphs with proper spacing (blank line between paragraphs)
    formatted_text = '\n\n'.join(cleaned_text)
    
    # Write to file
    with open('bio.txt', 'w', encoding='utf-8') as f:
        f.write(formatted_text)
    
    print(f"Extracted and cleaned {len(cleaned_text)} paragraphs to bio.txt")
    
    return formatted_text


def extract_career_statistics(soup) -> Dict[str, Any]:
    """
    Extract career statistics from a player page into a dictionary.
    
    Args:
        soup: BeautifulSoup object containing the HTML
    
    Returns:
        Dict[str, Any]: Dictionary containing the career statistics
    """
    table_list = soup.find_all('table')
    current_header = None
    
    # Find the Career statistics section and the corresponding table
    for table in table_list:
        headers = table.find_all('th', class_='infobox-header')
        for header in headers:
            if "Career statistics" in header.get_text():
                current_header = "Career statistics"
                break
        
        if current_header == "Career statistics":
            break
    
    if current_header != "Career statistics":
        print("Career statistics section not found")
        return {}
    
    # Find the actual statistics table (usually the next table after the header is found)
    # Check if there's another table in the document
    if len(table_list) > 1:
        # Get index of current table and use the next one
        current_index = table_list.index(table)
        if current_index + 1 < len(table_list):
            career_table = table_list[current_index + 1]
        else:
            # If there isn't a next table, use the current one
            career_table = table
    else:
        career_table = table
    
    # Extract table headers (from the first row)
    headers = []
    first_row = career_table.find('tr')
    if first_row:
        for th in first_row.find_all('th'):
            headers.append(th.get_text().strip())
    
    # If no headers were found, try other approaches
    if not headers:
        # Try to find headers from all th elements
        headers = [th.get_text().strip() for th in career_table.find_all('th')]
    
    # Extract data rows
    rows = []
    for tr in career_table.find_all('tr')[1:]:  # Skip the header row
        row_data = []
        
        # Get all th and td elements in this row
        cells = tr.find_all(['th', 'td'])
        for cell in cells:
            row_data.append(cell.get_text().strip())
        
        if row_data:  # Only add non-empty rows
            rows.append(row_data)
    
    # Create DataFrame
    if headers and rows:
        # Make sure all rows have the same length as headers
        max_len = max(len(headers), max(len(row) for row in rows))
        
        # Extend headers if needed
        if len(headers) < max_len:
            headers.extend([f'Column {i+1}' for i in range(len(headers), max_len)])
        
        # Extend rows if needed
        for row in rows:
            if len(row) < max_len:
                row.extend([''] * (max_len - len(row)))
            elif len(row) > max_len:
                row = row[:max_len]
        
        # Create and clean DataFrame
        df = pd.DataFrame(rows, columns=headers)
        
        # Clean up the DataFrame
        # Remove entirely empty columns
        df = df.dropna(axis=1, how='all')
        
        # Remove entirely empty rows
        df = df.dropna(axis=0, how='all')
        
        print("\nCareer Statistics:")
        print("=" * 80)
        print(df)
        print("=" * 80)
        
        # Save to CSV for convenience
        df.to_csv('career_statistics.csv', index=False)
        print("Career statistics saved to career_statistics.csv")
        
        # Convert DataFrame to dictionary
        stats_dict = {}
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            # Use first column as key if available
            if len(row_dict) > 0:
                key = list(row_dict.keys())[0]
                value = row_dict[key]
                # Use first value as key if it's not empty
                if value:
                    stats_dict[value] = {k: v for k, v in row_dict.items() if k != key}
                else:
                    stats_dict[f"Row {index}"] = row_dict
            else:
                stats_dict[f"Row {index}"] = row_dict
        
        return stats_dict
    
    print("Failed to extract career statistics - table structure not recognized")
    return {}


def parse_infobox_table(soup) -> Dict[str, Dict[str, str]]:
    """
    Parse an infobox table (commonly found on Wikipedia) and extract structured data.
    
    Args:
        soup: BeautifulSoup object containing the HTML
    
    Returns:
        Dict[str, Dict[str, str]]: Dictionary of header/value pairs from the table
    """
    print("Parsing infobox table...")
    career_reached = True
    table_list = soup.find_all('table')
    if not table_list:
        print("No tables found in the HTML")
        return {}
    
    main_table = table_list[0]
    info_dict = {}
    current_header = "General"
    
    print("Beginning table parsing...")
    
    for tr in main_table.find_all('tr'):
        cells = list(tr.find_all(['th', 'td']))
        
        if not cells:
            continue
            
        if len(cells) == 1 and 'infobox-header' in cells[0].get('class', []):
            current_header = cells[0].get_text().strip()
            if current_header == 'Career statistics':
              career_reached = False
            else:
              print(f"\n{'=' * 40}")
              print(f"HEADER: {current_header}")
              print(f"{'=' * 40}")
              
        # Otherwise, this is a data row
        elif len(cells) >= 2 and career_reached:
            header = cells[0].get_text().strip()
            value = cells[1].get_text().strip()
            
            # Store in dictionary
            if current_header not in info_dict:
                info_dict[current_header] = {}
            info_dict[current_header][header] = value
            
            print(f"{header}")
            print(f"{'-' * 20}")
            print(f"{value}\n")
    career_reached = True
    return info_dict


def run_scraper(query: str) -> Dict[str, Any]:
    """
    Main function to run the web scraper. Takes a user query, performs a Google search,
    fetches the page content, and extracts structured information.
    
    Args:
        query (str): The search query string (e.g., a person's name)

    
    Returns:
        Dict[str, Any]: A structured dictionary containing all scraped information
        with the following schema:
        {
            'bio': str,                  # Biography text
            'infobox': Dict[str, Dict],  # Structured information from infobox
            'career_statistics': Dict,    # Career statistics data
            'url': str                    # URL of the scraped page
        }
    """
    target_domain = "wikipedia"
    result = {
        'bio': '',
        'infobox': {},
        'career_statistics': {},
        'url': ''
    }
    
    # Perform search and fetch HTML
    html = search_and_fetch_html(query, target_domain)
    
    if html:
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract biography
        p_list = soup.find_all('p')
        result['bio'] = extract_and_clean_bio(p_list)
        
        # Extract structured information from infobox
        result['infobox'] = parse_infobox_table(soup)
        
        # Extract career statistics
        result['career_statistics'] = extract_career_statistics(soup)

    return result

def llm_call(query:str) -> str:
  client = genai.Client(api_key=GOOGLE_API_KEY)

  response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"from this text, {query}, find the cricket player name and return only the name of that cricket player",
  )
  
  return response.text

def player_info_api(player_name):
    query = f"Give me details about ${player_name}"
    response = llm_call(query=query)
    print(response)
    result = run_scraper(query=response)
    return result

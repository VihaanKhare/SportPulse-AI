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
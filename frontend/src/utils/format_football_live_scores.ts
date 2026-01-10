export function format_football_live_scores(rawData) {
    // Split data into individual matches using the URL pattern
    const matches = rawData.split(/\"url\":\"https:\/\/www\.espn\.in\/football/).filter(match => match.trim());
    
    const formattedMatches = [];
    
    for (let match of matches) {
      try {
        // Extract match data using regex
        const statusMatch = match.match(/\"status\":\"([^\"]+)\"/);
        const team1NameMatch = match.match(/\"team1\":.*?\"name\":\"([^\"]+)\"/);
        const team1RecordMatch = match.match(/\"team1\":.*?\"record\":.*?\"wins\":(\d+),\"draws\":(\d+),\"losses\":(\d+)/);
        const team1ScoreMatch = match.match(/\"team1\":.*?\"score\":(\d+)/);
        
        const team2NameMatch = match.match(/\"team2\":.*?\"name\":\"([^\"]+)\"/);
        const team2RecordMatch = match.match(/\"team2\":.*?\"record\":.*?\"wins\":(\d+),\"draws\":(\d+),\"losses\":(\d+)/);
        const team2ScoreMatch = match.match(/\"team2\":.*?\"score\":(\d+)/);
        
        const winnerMatch = match.match(/\"winner\":\"([^\"]+)\"/);
        
        // Extract values with null/undefined handling
        const status = statusMatch ? statusMatch[1] : "Unknown";
        
        const team1Name = team1NameMatch ? team1NameMatch[1] : "Team 1";
        const team1Wins = team1RecordMatch ? team1RecordMatch[1] : "?";
        const team1Draws = team1RecordMatch ? team1RecordMatch[2] : "?";
        const team1Losses = team1RecordMatch ? team1RecordMatch[3] : "?";
        const team1Score = team1ScoreMatch ? team1ScoreMatch[1] : "?";
        
        const team2Name = team2NameMatch ? team2NameMatch[1] : "Team 2";
        const team2Wins = team2RecordMatch ? team2RecordMatch[1] : "?";
        const team2Draws = team2RecordMatch ? team2RecordMatch[2] : "?";
        const team2Losses = team2RecordMatch ? team2RecordMatch[3] : "?";
        const team2Score = team2ScoreMatch ? team2ScoreMatch[1] : "?";
        
        const winner = winnerMatch ? winnerMatch[1] : "No winner declared";
        
        // Format match data with reduced spacing
        let formattedMatch = `⚽ ${status}: ${team1Name} vs ${team2Name}\n`;
        formattedMatch += `${team1Name} ${team1Score}-${team2Score} ${team2Name}\n`;
        
        // Add result with icon
        if (winner.startsWith("Draw")) {
          formattedMatch += `🤝 ${winner}`;
        } else if (winner === team1Name) {
          formattedMatch += `🏆 ${team1Name} wins`;
        } else if (winner === team2Name) {
          formattedMatch += `🏆 ${team2Name} wins`;
        } else {
          formattedMatch += `ℹ️ ${winner}`;
        }
        
        // Add team records in compact format
        formattedMatch += `\n📊 ${team1Name}: ${team1Wins}W ${team1Draws}D ${team1Losses}L | ${team2Name}: ${team2Wins}W ${team2Draws}D ${team2Losses}L`;
        
        formattedMatches.push(formattedMatch);
      } catch (e) {
        // Fallback for parsing errors
        formattedMatches.push("Match data processing error: " + e.message);
      }
    }
    
    return formattedMatches.join("\n\n----------------------------\n\n");
  }
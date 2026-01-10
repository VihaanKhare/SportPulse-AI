interface Tournament {
  name: string;
  shortName: string;
  format: string;
}

interface TeamData {
  name: string;
  shortName: string;
  score: number | null;
  wickets: number | null;
  overs: number | null;
}

interface MatchResult {
  winner: string | null;
  margin: string | null;
  winningMethod: string | null;
}

interface Match {
  matchNumber: number;
  tournament: Tournament;
  status: 'upcoming' | 'completed' | 'live';
  teams: {
    team1: TeamData;
    team2: TeamData;
  };
  result: MatchResult | null;
  links: string[];
  metadata?: {
    url: string;
    timestamp: number;
  };
  diff?: number;
  time?: number;
}

export function format_cricket_live_scores(matches: Match[]): string {
  const currentDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  
  let report = `# Cricket Update Report - ${currentDate}\n\n`;
  
  // Group matches by status
  const completedMatches = matches.filter(match => match.status === 'completed');
  const upcomingMatches = matches.filter(match => match.status === 'upcoming');
  const liveMatches = matches.filter(match => match.status === 'live');
  
  // Add completed matches
  if (completedMatches.length > 0) {
    report += `## Recent Results\n\n`;
    completedMatches.forEach(match => {
      const { tournament, teams, result, matchNumber } = match;
      const { team1, team2 } = teams;
      
      report += `### ${tournament.shortName} Match #${matchNumber}: `;
      
      if (result?.winner) {
        const winnerTeam = result.winner.trim() === team1.name.trim() ? team1 : team2;
        const loserTeam = result.winner.trim() === team1.name.trim() ? team2 : team1;
        report += `${winnerTeam.name} triumph over ${loserTeam.shortName}\n`;
        report += `**${winnerTeam.name}** defeated **${loserTeam.name}** by **${result.margin}**\n`;
      } else {
        report += `Thrilling tie between ${team1.shortName} and ${team2.shortName}\n`;
        report += `**${team1.name}** tied with **${team2.name}**\n`;
      }
      
      if (team1.score !== null) {
        report += `- ${team1.shortName}: ${team1.score}/${team1.wickets} (${team1.overs} overs)\n`;
      }
      
      if (team2.score !== null) {
        report += `- ${team2.shortName}: ${team2.score}/${team2.wickets} (${team2.overs} overs)\n`;
      }
      
      // Add a comment about the match
      if (result?.winner && result?.winningMethod === 'wickets') {
        const winnerTeam = result.winner.trim() === team1.name.trim() ? team1 : team2;
        const loserTeam = result.winner.trim() === team1.name.trim() ? team2 : team1;
        
        if (team2.overs && winnerTeam === team2) {
          const fullOvers = 20;
          const remainingBalls = Math.round((fullOvers - team2.overs) * 6);
          if (remainingBalls > 0) {
            report += `${winnerTeam.shortName} chased down the target with ${remainingBalls} ball${remainingBalls !== 1 ? 's' : ''} to spare.\n`;
          }
        }
      } else if (!result?.winner) {
        report += `A perfectly matched contest with both teams scoring identical totals!\n`;
      }
      
      report += '\n';
    });
  }
  
  // Add live matches if any
  if (liveMatches.length > 0) {
    report += `## Live Matches\n\n`;
    liveMatches.forEach(match => {
      const { tournament, teams, matchNumber } = match;
      const { team1, team2 } = teams;
      
      report += `### ${tournament.shortName} Match #${matchNumber}: ${team1.name} vs ${team2.name}\n`;
      report += `- Tournament: ${tournament.name} (${tournament.format})\n`;
      report += `- Status: In Progress\n`;
      
      if (team1.score !== null) {
        report += `- ${team1.shortName}: ${team1.score}/${team1.wickets} (${team1.overs} overs)\n`;
      }
      
      if (team2.score !== null) {
        report += `- ${team2.shortName}: ${team2.score}/${team2.wickets} (${team2.overs} overs)\n`;
      }
      
      report += '\n';
    });
  }
  
  // Add upcoming matches
  if (upcomingMatches.length > 0) {
    report += `## Upcoming Fixtures\n\n`;
    upcomingMatches.forEach(match => {
      const { tournament, teams, matchNumber } = match;
      const { team1, team2 } = teams;
      
      report += `### ${tournament.shortName} Match #${matchNumber}\n`;
      report += `**${team1.name}** vs **${team2.name}**\n`;
      report += `- Tournament: ${tournament.name} (${tournament.format})\n`;
      report += `- Status: Upcoming\n\n`;
    });
  }
  
  // Add footer about links
  const allLinks = [...new Set(matches.flatMap(match => match.links))];
  if (allLinks.length > 0) {
    report += `*${allLinks.join(' and ')} available online for ${
      matches.map(m => m.tournament.shortName).filter((v, i, a) => a.indexOf(v) === i).join(' and ')
    } matches.*\n`;
  }
  
  return report;
}

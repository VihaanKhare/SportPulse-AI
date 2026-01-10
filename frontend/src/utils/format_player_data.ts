import { PlayerApiResponse } from "@/types/types";

export const formatPlayerData = (data:PlayerApiResponse) => {
    const lineBreak = '\n\n';
  
    const bio = data.bio.replace(/\\n/g, '\n').replace(/\\/g, ' ');
  
    let stats = 'Career Statistics:\n';
    for (const [category, formats] of Object.entries(data.career_statistics)) {
      stats += `\n${category}\n`;
      for (const [format, value] of Object.entries(formats)) {
        stats += `  - ${format}: ${value}\n`;
      }
    }
  
    let info = 'Personal & Sports Info:\n';
    for (const [section, details] of Object.entries(data.infobox)) {
      info += `\n${section}\n`;
      for (const [label, value] of Object.entries(details)) {
        info += `  - ${label}: ${value}\n`;
      }
    }
  
    return `${bio}${lineBreak}${stats}${lineBreak}${info}`;
  }
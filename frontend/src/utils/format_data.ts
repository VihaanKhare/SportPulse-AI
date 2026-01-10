export function smartFormatText(input: string): string {
    const matchChunks = input.split(/(?="url":")/); // Split by each new "match"
    const cleanedParts: string[] = [];
  
    for (let chunk of matchChunks) {
      const cleaned = chunk
        .replace(/\\n/g, '\n')                    
        .replace(/\\"/g, '"')                    
        .replace(/,\s*/g, ',\n')                 
        .replace(/(?<=[:\]])\s*(?=")/g, '\n')     
        .replace(/(?<=[\}\]])\s*/g, '\n')         
        .replace(/\n{2,}/g, '\n')                
        .trim();
  
      if (cleaned.length > 0) {
        cleanedParts.push(cleaned);
      }
    }
  
    return cleanedParts.join('\n\n--- MATCH ---\n\n');
  }
  
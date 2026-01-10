import { GEMINI_API_KEY } from "../../constants";
import { GoogleGenAI } from "@google/genai";
import live_scores_cricket from "../api/live_scores_cricket";
import live_scores_football from "../api/live_scores_football";
import live_commentary_cricket from "../api/live_commentary_cricket";
import player_info from "../api/player_info";
import { formatPlayerData } from "../../utils/format_player_data";
import { format_cricket_live_scores } from "../../utils/format_cricket_live_scores";
import { smartFormatText } from "../../utils/format_data";

const ai = new GoogleGenAI({ apiKey: GEMINI_API_KEY });

const beautify=async(response:string)=>{
  const res=await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: `Remove all escape characters and quotes from the following string and add spacing and newlines wherever required and format it and beautify it and then return it. Only return the text response.

    The string is as follows : ${response}`
  })
  return res.text
}
const gemini=async (query:string) =>{
  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: `From this query check for the following conditions:
    1.if the user asks for cricket live scores return live_scores_cricket
    2.if the user asks for football live scores return live_scores_football
    3.if the user asks for cricket live commentary return live_commentary_cricket
    4.if the user asks for player info return player_info along with the name of the player asked as player_info-player_name
    Make sure you only send these one word only as the response in the above scenarios. If in case the user does not ask for the above then start the response with other_response along with your response as follows other_respone-your_response.
    The query is as follows: ${query}
    `,
  });
  console.log(response.text);
  if(response.text?.includes('live_scores_cricket')){
    const result =await live_scores_cricket();
    // const formatted=format_cricket_live_scores(result);
    const formatted = result.replace(/{/g, '\n\n\n').replace(/}/g, '\n\n\n');
    const formatted_=smartFormatText(formatted)
    const format=beautify(formatted_)
    return format
    // const res= await beautify(result)
    // console.log(res)
    // return result
  }else if(response.text?.includes('live_scores_football')){
    const result=await live_scores_football();
    // const res= await beautify(result)
    // console.log(res)
    const formatted = result.replace(/{/g, '\n\n\n').replace(/}/g, '\n\n\n');
    const formatted_=smartFormatText(formatted)
    const format=beautify(formatted_)
    return format

  }else if(response.text?.includes('live_commentary_cricket')){
    const result=await live_commentary_cricket();
    // const res= await beautify(result)
    // console.log(res)
    const formatted= result.replace(/{/g, '\n\n\n').replace(/}/g, '\n\n\n');
    // const format=beautify(formatted)
    return formatted
  }else if(response.text?.includes('player_info')){
    const player_name=response.text.split('-')[1]
    const result=await player_info(player_name);
    // console.log(result);
    // console.log(typeof result); 
    // const res= await beautify(result)
    // console.log(res)
    const formatted = formatPlayerData(result);
    return formatted
    // return JSON.parse(result);
    // console.log(result);
    // console.log(typeof result); 
    // const res= await beautify(result)
    // console.log(res)
    const formatted = formatPlayerData(result);
    return formatted
    // return JSON.parse(result);
  }else{
    const result=response.text?.split("-")[1]
    return result?result:""
    const result=response.text?.split("-")[1]
    return result?result:""
  }
}

export default gemini
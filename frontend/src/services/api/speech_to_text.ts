import axios from 'axios';
import { API_BASE_URL } from '../../constants';

const speech_to_text=async (audio_url:string)=>{
    try {
        const response = await axios.get(`${API_BASE_URL}/speech_to_text?audio_url=${audio_url}`);
        return response.data; 
    } catch (error) {
        throw error|| "Failed to convert speech to text";
    }
}

export default speech_to_text;
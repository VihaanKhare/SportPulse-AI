import axios from 'axios';
import { API_BASE_URL } from '../../constants';

const live_scores_football=async ()=>{
    try {
        const response = await axios.get(`${API_BASE_URL}/live_scores/football`);
        return response.data; 
    } catch (error) {
        throw error || "Failed to fetch live scores";
    }
}

export default live_scores_football;
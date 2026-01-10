import axios from 'axios';
import { API_BASE_URL } from '../../constants';

const player_info=async (player_name:string)=>{
    try {
        const response = await axios.get(`${API_BASE_URL}/player_info?player_name=${player_name}`);
        return response.data; 
    } catch (error) {
        throw error|| "Failed to fetch live scores";
    }
}

export default player_info;
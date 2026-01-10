import axios from 'axios';
import { API_BASE_URL } from '../../constants';

const live_commentary_cricket=async ()=>{
    try {
        const response = await axios.get(`${API_BASE_URL}/live_commentary/cricket`);
        return response.data; 
    } catch (error) {
        throw error|| "Failed to fetch live commentary";
    }
}

export default live_commentary_cricket;
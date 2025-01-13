import axios from 'axios';
import { API_URL } from './constants';

const apiInstance = axios.create({
    baseURL: API_URL,
    timeout: 1000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
});

export default apiInstance;
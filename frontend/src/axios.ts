import axios from 'axios';

const getAPI = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Ensure this matches your backend URL
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    
  },
});

export { getAPI };

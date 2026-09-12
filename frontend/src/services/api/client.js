import axios from 'axios';
import { setupInterceptors } from './interceptors';

// Create a centralized Axios client
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Apply interceptors
setupInterceptors(apiClient);

export default apiClient;

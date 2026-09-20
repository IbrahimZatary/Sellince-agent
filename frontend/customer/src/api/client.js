import axios from "axios";

const API_REQUEST_TIMEOUT_MS = 10000;

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "",
  timeout: API_REQUEST_TIMEOUT_MS,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
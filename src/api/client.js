import axios from "axios";

// Connection boundary for the backend team. UI components do not call it yet.
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "",
  timeout: 30000,
});

export async function authenticateCustomer(credentials) {
  const response = await apiClient.post("/api/v1/customer-auth/login", credentials);
  return response.data;
}

export async function initializeConversation(customerDetails, options = {}) {
  const response = await apiClient.post("/api/v1/agent/start-session", customerDetails, options);
  return response.data;
}

export async function requestAssistantReply(customerMessage, options = {}) {
  const response = await apiClient.post("/api/v1/chat", customerMessage, options);
  return response.data;
}

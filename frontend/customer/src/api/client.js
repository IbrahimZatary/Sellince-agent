/**
 * API Client & Network Boundary
 *
 * Configured Axios HTTP client for communicating with the Sellince backend services.
 * Base URL is driven by Vite environment variable `VITE_API_BASE_URL`.
 */

import axios from "axios";

const API_REQUEST_TIMEOUT_MS = 10000;

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "",
  timeout: API_REQUEST_TIMEOUT_MS,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Register a new user account.
 * @param {Object} registrationDetails
 * @returns {Promise<any>} Raw response data from backend
 */
export async function registerUser(registrationDetails) {
  // TODO: When the backend team supplies the official response contract,
  // add token extraction, session persistence, and response mapping here.
  const response = await apiClient.post("/auth/register", registrationDetails);
  return response.data;
}

/**
 * Authenticate an existing user with credentials.
 * @param {Object} loginCredentials
 * @returns {Promise<any>} Raw response data from backend
 */
export async function authenticateUser(loginCredentials) {
  // TODO: When the backend team supplies the official response contract,
  // add token extraction, session persistence, and response mapping here.
  const response = await apiClient.post("/auth/login", loginCredentials);
  return response.data;
}

/**
 * Send a customer message to the assistant and retrieve the reply.
 * @param {Object} customerMessage
 * @returns {Promise<any>} Raw response data from backend
 */
export async function requestAssistantReply(customerMessage) {
  // TODO: When the backend team supplies the official chat endpoint response contract,
  // add message mapping and state synchronization here.
  const response = await apiClient.post("/api/chat", customerMessage);
  return response.data;
}

export default apiClient;

import apiClient from "./client";

export const requestAssistantReply = async (customerMessage) => {
  const { data } = await apiClient.post("/api/v1/chat", customerMessage);
  return data;
};
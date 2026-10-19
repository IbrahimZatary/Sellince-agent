import apiClient from './client';

export const sendChatMessage = async (customerId, message) => {
  const { data } = await apiClient.post('/chat', { customer_id: customerId, message });
  return data;
};
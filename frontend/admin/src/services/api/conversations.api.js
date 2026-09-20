import apiClient from './client';

export const getConversations = async () => {
  const { data } = await apiClient.get('/conversations');
  return data;
};

export const getConversation = async (id) => {
  const { data } = await apiClient.get(`/conversations/${id}`);
  return data;
};
import apiClient from './client';

export const getCustomers = async () => {
  const { data } = await apiClient.get('/customers');
  return data;
};
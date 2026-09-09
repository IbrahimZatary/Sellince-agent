import apiClient from './client';

export const login = async (credentials) => {
  // return apiClient.post('/auth/login', credentials);
  
  // Mock response for now
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ data: { token: 'mock-jwt-token', user: { name: 'Admin', email: credentials.email } } });
    }, 1000);
  });
};

export const signup = async (data) => {
  // return apiClient.post('/auth/signup', data);
  
  // Mock response for now
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ data: { success: true } });
    }, 1000);
  });
};

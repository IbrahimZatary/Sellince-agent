import apiClient from './client';

export const login = async (credentials) => {
  const { data } = await apiClient.post('/auth/login', credentials);
  return data; // { access_token, token_type }
};

export const signup = async (form) => {
  // Map the signup form fields to the backend RegisterRequest contract.
  // sector/subscription_tier/full_name aren't collected by the form yet:
  // they default (industry picker will PATCH /auth/me later).
  const { data } = await apiClient.post('/auth/register', {
    company_name: form.companyName,
    full_name: form.fullName || form.email.split('@')[0],
    email: form.email,
    password: form.password,
    sector: 'telecom',
    subscription_tier: 'standard',
  });
  return data; // { access_token, token_type }
};

export const me = async () => {
  const { data } = await apiClient.get('/auth/me');
  return data;
};

export const logout = async () => {
  await apiClient.post('/auth/logout');
};

export const updateMe = async (payload) => {
  const { data } = await apiClient.patch('/auth/me', payload);
  return data;
};
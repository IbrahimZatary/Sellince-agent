import { tokenStore } from './tokenStore';

export const setupInterceptors = (apiClient) => {
  // Request Interceptor: attach the access token to every call
  apiClient.interceptors.request.use(
    (config) => {
      const token = tokenStore.get();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response Interceptor: on 401 try to refresh the session once, then retry
  apiClient.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error) => {
      const original = error.config;
      const skipRetry =
        error.response?.status !== 401 ||
        original?._retry ||
        original?.url?.includes('/auth/login') ||
        original?.url?.includes('/auth/refresh');

      if (skipRetry) {
        return Promise.reject(error);
      }

      original._retry = true;
      try {
        const { data } = await apiClient.post('/auth/refresh');
        tokenStore.set(data.access_token);
        original.headers.Authorization = `Bearer ${data.access_token}`;
        return apiClient(original);
      } catch (refreshError) {
        tokenStore.clear();
        window.location.assign('/login');
        return Promise.reject(refreshError);
      }
    }
  );
};
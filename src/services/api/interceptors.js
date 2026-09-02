export const setupInterceptors = (apiClient) => {
  // Request Interceptor
  apiClient.interceptors.request.use(
    (config) => {
      // Future JWT injection:
      // const token = localStorage.getItem('token');
      // if (token) {
      //   config.headers.Authorization = `Bearer ${token}`;
      // }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Response Interceptor
  apiClient.interceptors.response.use(
    (response) => {
      return response;
    },
    (error) => {
      // Centralized error normalization
      // if (error.response?.status === 401) {
      //   // Handle unauthorized (e.g., clear token, redirect to login)
      // }
      return Promise.reject(error);
    }
  );
};

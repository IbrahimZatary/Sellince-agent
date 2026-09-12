const ACCESS_TOKEN_KEY = 'sellince_access_token';

export const tokenStore = {
  get() {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },
  set(token) {
    localStorage.setItem(ACCESS_TOKEN_KEY, token);
  },
  clear() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
  },
};
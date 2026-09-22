import apiClient from "./client";

export const loginCustomer = async (credentials) => {
  const { data } = await apiClient.post("/api/v1/customer-auth/login", credentials);
  return data;
};

import apiClient from "./client";

export const login = async (credentials) => {
  const { data } = await apiClient.post("/api/v1/auth/login", credentials);
  return data;
};

export const signup = async (form) => {
  const payload = {
    sector: mapSector(form.sector),
    company_name: form.companyName,
    subscription_tier: "pilot",
    full_name: form.name,
    email: form.email,
    password: form.password,
  };
  const { data } = await apiClient.post("/api/v1/auth/register", payload);
  return data;
};

export const me = async () => {
  const { data } = await apiClient.get("/api/v1/auth/me");
  return data;
};

export const logout = async () => {
  await apiClient.post("/api/v1/auth/logout");
};

export const updateMe = async (payload) => {
  const { data } = await apiClient.patch("/api/v1/auth/me", payload);
  return data;
};

function mapSector(sector) {
  const sectorMap = {
    technology: "telecom",
    ecommerce: "telecom",
    finance: "banking",
    healthcare: "telecom",
    education: "telecom",
    manufacturing: "telecom",
    other: "telecom",
  };
  return sectorMap[sector] || "telecom";
}
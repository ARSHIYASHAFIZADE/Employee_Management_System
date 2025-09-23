import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; 

export const registerUser = async (email: string, password: string) => {
  const res = await axios.post(`${API_URL}/employees/auth/register`, {
    email,
    password,
  });
  console.log("Registration response: ", res.data)
  return res.data;
};

export const loginUser = async (email: string, password: string) => {
  const res = await axios.post(`${API_URL}/employees/auth/login`, {
    email,
    password,
  });
  if (res.data.access_token) {
    localStorage.setItem("token", res.data.access_token);
  }
  console.log("Login response: ", res.data)
  return res.data;
};

export const logoutUser = () => {
  localStorage.removeItem("token");
};

export const getCurrentUser = async () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("No token found");

  const res = await axios.get(`${API_URL}/employees/users/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};

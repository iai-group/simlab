// Constants to send requests to the backend

import axios from "axios";

const baseURL = "https://localhost/api"; // TODO: Replace with environment variable

const APIAuth = axios.create({
  baseURL: baseURL,
  withCredentials: true,
  validateStatus: () => true,
});

export { APIAuth, baseURL };

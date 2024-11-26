// Constants to send requests to the backend

import axios from "axios";

const baseURL = "https://127.0.0.1/api"; // TODO: Replace with environment variable

const APIAuth = axios.create({
  baseURL: baseURL,
  withCredentials: true,
});

export { APIAuth, baseURL };

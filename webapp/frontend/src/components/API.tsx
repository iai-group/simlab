// Constants to send requests to the backend

import axios from "axios";

const host = process.env.REACT_APP_SIMLAB_HOSTNAME || "localhost";
const baseURL = `https://${host}/api`;

const APIAuth = axios.create({
  baseURL: baseURL,
  withCredentials: true,
  validateStatus: () => true,
});

export { APIAuth, baseURL, host };

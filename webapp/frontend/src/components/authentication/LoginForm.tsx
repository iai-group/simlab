// Log in form component

import { MDBBtn, MDBContainer, MDBInput } from "mdb-react-ui-kit";
import { useContext, useState } from "react";

import { Alert } from "react-bootstrap";
import { AuthContext } from "../../contexts/AuthContext";
import axios from "axios";
import { baseURL } from "../API";
import { useNavigate } from "react-router-dom";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async () => {
    console.log("Login");
    axios
      .post(`${baseURL}/login`, {
        username: username,
        password: password,
      })
      .then((response) => {
        setUser({ username: username });
        navigate("/");
      })
      .catch((error) => {
        console.error(error);
        setErrorMessage(error.message || "An unknown error occurred.");
      });
  };

  return (
    <MDBContainer className="p-3 my-5 d-flex flex-column w-50">
      {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
      <MDBInput
        wrapperClass="mb-4"
        label="Username"
        id="formUsername"
        type="text"
        onChange={(e) => setUsername(e.target.value)}
      />
      <MDBInput
        wrapperClass="mb-4"
        label="Password"
        id="formPassword"
        type="password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <div className="d-flex justify-content-between mx-3 mb-4">
        <a href="/reset-password">Forgot password?</a>
      </div>

      <MDBBtn className="mb-4" onClick={handleLogin}>
        Sign in
      </MDBBtn>

      <div className="text-center">
        <p>
          Not a member? <a href="/register">Register</a>
        </p>
      </div>
    </MDBContainer>
  );
};

export default LoginForm;

// Register form component

import { MDBBtn, MDBContainer, MDBInput } from "mdb-react-ui-kit";
import { useContext, useState } from "react";

import { Alert } from "react-bootstrap";
import { AuthContext } from "../../contexts/AuthContext";
import axios from "axios";
import { baseURL } from "../API";
import { useNavigate } from "react-router-dom";

const RegisterForm = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleRegister = async () => {
    console.log("Register");
    axios
      .post(`${baseURL}/register`, {
        email: email,
        username: username,
        password: password,
      })
      .then((response) => {
        console.log(response);
        setUser({ username: username });
        navigate("/auth");
      })
      .catch((error) => {
        console.error(error);
        setErrorMessage(
          error.response.data.message || "An unknown error occurred."
        );
      });
  };

  return (
    <MDBContainer className="p-3 my-5 d-flex flex-column w-50">
      {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
      <MDBInput
        wrapperClass="mb-4"
        label="Email"
        id="formEmail"
        type="email"
        onChange={(e) => setEmail(e.target.value)}
      />
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

      <MDBBtn className="mb-4" onClick={handleRegister}>
        Register
      </MDBBtn>

      <div className="text-center">
        <p>
          Already a member? <a href="/auth">Login</a>
        </p>
      </div>
    </MDBContainer>
  );
};
export default RegisterForm;

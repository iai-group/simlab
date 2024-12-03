// Reset password form component

import { Alert, Button, Col, Container, Form, Row } from "react-bootstrap";

import axios from "axios";
import { baseURL } from "../API";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

const ResetPasswordForm = () => {
  const [username, setUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const handleResetPassword = () => {
    axios
      .post(`${baseURL}/reset-password`, {
        username: username,
        password: newPassword,
      })
      .then(
        (response) => {
          navigate("/auth", { replace: true });
        },
        (error) => {
          setErrorMessage(error.response.data.message);
        }
      );
  };

  return (
    <Container className="mt-5 d-flex justify-content-center align-items-center">
      <Form className="w-50">
        {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
        <Form.Group className="mb-3" controlId="formUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="test"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formNewPassword">
          <Form.Label>New Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
        </Form.Group>
        <Row className="justify-content-center">
          <Col xs="auto" className="me-2">
            <Button onClick={handleResetPassword}>Reset Password</Button>
          </Col>
        </Row>
      </Form>
    </Container>
  );
};

export default ResetPasswordForm;

// Home page for logged in users

import { AuthContext } from "../../contexts/AuthContext";
import { Container } from "react-bootstrap";
import { useContext } from "react";

const UserHome = () => {
  const { user } = useContext(AuthContext);

  return (
    <Container>
      <h1>Home for {user?.username}</h1>
    </Container>
  );
};

export default UserHome;

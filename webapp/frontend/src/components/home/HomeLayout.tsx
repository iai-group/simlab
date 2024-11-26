// Home page

import { AuthContext } from "../../contexts/AuthContext";
import LoginForm from "../authentication/LoginForm";
import UserHome from "./UserHome";
import { useContext } from "react";

const HomeLayout = () => {
  const { user } = useContext(AuthContext);

  return user ? <UserHome /> : <LoginForm />;
};

export default HomeLayout;

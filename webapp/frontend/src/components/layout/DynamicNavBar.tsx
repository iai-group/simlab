import {
  MDBBtn,
  MDBCollapse,
  MDBContainer,
  MDBIcon,
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarItem,
  MDBNavbarLink,
  MDBNavbarNav,
  MDBNavbarToggler,
} from "mdb-react-ui-kit";
import { useContext, useState } from "react";

import { APIAuth } from "../API";
import { AuthContext } from "../../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

const DynamicNavBar = () => {
  const [openBasic, setOpenBasic] = useState(false);
  const { user, setUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSignOut = async () => {
    APIAuth.post("/logout")
      .then((response) => {
        setUser(null);
        navigate("/");
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <MDBNavbar expand="lg" light bgColor="light">
      <MDBContainer fluid>
        <MDBNavbarBrand href="/">SimLab</MDBNavbarBrand>

        <MDBNavbarToggler
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
          onClick={() => setOpenBasic(!openBasic)}
        >
          <MDBIcon icon="bars" fas />
        </MDBNavbarToggler>

        <MDBCollapse navbar open={openBasic}>
          <MDBNavbarNav className="mr-auto mb-2 mb-lg-0">
            {user ? (
              <MDBNavbarItem>
                <MDBNavbarLink href="/experiment">Experiment</MDBNavbarLink>
              </MDBNavbarItem>
            ) : null}
            <MDBNavbarItem>
              <MDBNavbarLink href="/documentation">Documentation</MDBNavbarLink>
            </MDBNavbarItem>
            <MDBNavbarItem>
              <MDBNavbarLink href="/leaderboard">Leaderboard</MDBNavbarLink>
            </MDBNavbarItem>

            {user ? (
              <MDBBtn rounded onClick={handleSignOut}>
                Sign Out
              </MDBBtn>
            ) : (
              <>
                <MDBBtn rounded href="/auth">
                  Log In
                </MDBBtn>
                <MDBBtn rounded href="/register">
                  Register
                </MDBBtn>
              </>
            )}
          </MDBNavbarNav>
        </MDBCollapse>
      </MDBContainer>
    </MDBNavbar>
  );
};

export default DynamicNavBar;

import DynamicNavBar from "./DynamicNavBar";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <>
      <DynamicNavBar />
      <br />
      <Outlet />
    </>
  );
};

export default Layout;

import "./App.css";

import { Route, Routes } from "react-router-dom";

import HomeLayout from "./components/home/HomeLayout";
import Layout from "./components/layout/Layout";
import Leaderboard from "./components/Leaderboard";
import LoginForm from "./components/authentication/LoginForm";
import NotFound from "./components/NotFound";
import RegisterForm from "./components/authentication/RegisterForm";
import ResetPasswordForm from "./components/authentication/ResetPasswordForm";
import RunHome from "./components/run/RunHome";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomeLayout />} />
          <Route path="/experiment" element={<RunHome />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/auth" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/reset-password" element={<ResetPasswordForm />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </>
  );
}

export default App;

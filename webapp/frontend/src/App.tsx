import "./App.css";

import { Route, Routes } from "react-router-dom";

import HomeLayout from "./components/home/HomeLayout";
import Layout from "./components/layout/Layout";
import Leaderboard from "./components/Leaderboard";
import LoginForm from "./components/authentication/LoginForm";
import NotFound from "./components/NotFound";
import RegisterForm from "./components/authentication/RegisterForm";
import ResetPasswordForm from "./components/authentication/ResetPasswordForm";
import RunSubmissionForm from "./components/run/SubmitRunForm";
import TaskList from "./components/task/TaskList";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomeLayout />} />
          <Route path="/tasks" element={<TaskList />} />
          <Route path="/submit-run" element={<RunSubmissionForm />} />
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

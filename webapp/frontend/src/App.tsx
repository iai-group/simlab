import "./App.css";

import { Route, Routes } from "react-router-dom";

import HomeLayout from "./components/home/HomeLayout";
import Layout from "./components/layout/Layout";
import LoginForm from "./components/authentication/LoginForm";
import NotFound from "./components/NotFound";
import RegisterForm from "./components/authentication/RegisterForm";
import ResetPasswordForm from "./components/authentication/ResetPasswordForm";
import ResultsDashboard from "./components/dashboard/ResultsDashboard";
import RunSubmissionForm from "./components/run/SubmitRunForm";
import SystemHome from "./components/system/SystemHome";
import TaskDashboard from "./components/dashboard/TaskDashboard";
import TaskList from "./components/task/TaskList";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomeLayout />} />
          <Route path="/experiment" element={<TaskList />} />
          <Route path="/system" element={<SystemHome />} />
          <Route path="/submit-run" element={<RunSubmissionForm />} />
          <Route path="/leaderboard" element={<ResultsDashboard />} />
          <Route path="/results" element={<TaskDashboard />} />
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

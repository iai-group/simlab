import { Container, Toast, ToastContainer } from "react-bootstrap";
import { useEffect, useState } from "react";

import Form from "react-bootstrap/Form";
import { Task } from "../../types";
import axios from "axios";
import { baseURL } from "../API";
import { useNavigate } from "react-router-dom";

const ResultsDashboard = () => {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const fetchTasks = async (): Promise<Task[]> => {
    try {
      const response = await axios.get(`${baseURL}/tasks`);

      const fetchedTasks = response.data.map((task: any) => {
        const metrics = task.arguments.metrics.map((metric: any) => ({
          id: metric.id || "",
          name: metric.arguments?.name || "",
          description: metric.description || "",
          arguments: Object.entries(metric.arguments || {}).map(
            ([key, value]) => ({
              name: key,
              type: typeof value,
              value,
            })
          ),
        }));

        const args = Object.entries(task.arguments || {})
          .filter(([key]) => key !== "metrics")
          .map(([key, value]) => {
            if (
              typeof value === "object" &&
              value !== null &&
              !Array.isArray(value)
            ) {
              return {
                name: key,
                type: "object",
                value: value,
              };
            }
            return {
              name: key,
              type: typeof value,
              value: value,
            };
          });

        return {
          id: task._id,
          name: task.name,
          description: task.description,
          arguments: args,
          metrics: metrics,
        };
      });

      return fetchedTasks;
    } catch (error) {
      console.error("Error fetching tasks:", error);
      setToastMessage("Error fetching tasks. Please contact the admin.");
      return [];
    }
  };

  useEffect(() => {
    fetchTasks().then((data) => setTasks(data));
  }, []);

  const showTaskResults = (e: any) => {
    const selectedTask = tasks.find((task) => task.id === e.target.value);
    console.log(selectedTask);
    navigate(`/results`, { state: { task: selectedTask } });
  };

  return (
    <Container>
      <h3>Dashboard</h3>

      {/* Select task */}
      <Form.Select className="mb-3" onChange={showTaskResults}>
        <option>Select a task</option>
        {tasks.map((task) => (
          <option key={task.id} value={task.id}>
            {task.name}
          </option>
        ))}
      </Form.Select>

      {/* Toast Notifications */}
      <ToastContainer className="p-3" position="top-end" style={{ zIndex: 1 }}>
        <Toast
          onClose={() => setToastMessage(null)}
          show={!!toastMessage}
          delay={5000}
          autohide
          bg="danger"
        >
          <Toast.Header>
            <strong className="me-auto">SimLab Error</strong>
          </Toast.Header>
          <Toast.Body>{toastMessage}</Toast.Body>
        </Toast>
      </ToastContainer>
    </Container>
  );
};

export default ResultsDashboard;

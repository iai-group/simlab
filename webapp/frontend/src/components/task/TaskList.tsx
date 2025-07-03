// Component to display the list of available tasks

import { Button, Container, Form, InputGroup } from "react-bootstrap";
import { MDBBtn, MDBListGroup, MDBListGroupItem } from "mdb-react-ui-kit";
import { useEffect, useState } from "react";

import { Task } from "../../types";
import TaskDescription from "./TaskDescription";
import ToastNotification from "../ToastNotification";
import axios from "axios";
import { baseURL } from "../API";
import { useNavigate } from "react-router-dom";

const TaskList = () => {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const tasksPerPage = 20; // Number of tasks per page

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
          name: args.find((arg) => arg.name === "name")?.value,
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

  // Handle search
  const filteredTasks = tasks.filter((task) =>
    task.name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Pagination logic
  const indexOfLastTask = currentPage * tasksPerPage;
  const indexOfFirstTask = indexOfLastTask - tasksPerPage;
  const currentTasks = filteredTasks.slice(indexOfFirstTask, indexOfLastTask);
  const totalPages = Math.ceil(filteredTasks.length / tasksPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  const handlePrevPage = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  if (selectedTask) {
    return (
      <Container>
        <MDBBtn onClick={() => setSelectedTask(null)} className="m-3">
          Back to Task List
        </MDBBtn>
        <MDBBtn
          className="m-3"
          onClick={() =>
            navigate("/submit-run", { state: { task: selectedTask } })
          }
        >
          Add new system to public leaderboard
        </MDBBtn>
        <TaskDescription task={selectedTask} />
      </Container>
    );
  }

  return (
    <Container>
      <h3>Available Tasks</h3>

      {/* Search Bar */}
      <InputGroup className="mb-3">
        <Form.Control
          placeholder="Search tasks by name..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button variant="outline-secondary" onClick={() => setSearchTerm("")}>
          Clear
        </Button>
      </InputGroup>

      {/* Tasks List */}
      <MDBListGroup style={{ minWidth: "22rem" }} light>
        {currentTasks.map((task: Task) => (
          <MDBListGroupItem
            key={task.id}
            onClick={() => setSelectedTask(task)}
            tag="button"
            action
            type="button"
          >
            {task.name}
          </MDBListGroupItem>
        ))}
      </MDBListGroup>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="d-flex justify-content-between align-items-center">
          <Button
            variant="secondary"
            onClick={handlePrevPage}
            disabled={currentPage === 1}
          >
            Previous
          </Button>
          <span>
            Page {currentPage} of {totalPages}
          </span>
          <Button
            variant="secondary"
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
          >
            Next
          </Button>
        </div>
      )}

      {/* Toast Notifications */}
      <ToastNotification
        message={toastMessage}
        type="error"
        setMessage={setToastMessage}
      />
    </Container>
  );
};

export default TaskList;

import { Alert, Button, Container } from "react-bootstrap";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { APIAuth } from "../API";

const TaskDashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const task = location.state?.task;
  const [runs, setRuns] = useState([]);

  if (!task) {
    return (
      <Alert variant="danger" className="m-3">
        <p>
          No task selected. Please go back to the dashboard home and select a
          task.
        </p>
        <hr />
        <div className="d-flex justify-content-end">
          <Button
            onClick={() => navigate("/leaderboard")}
            variant="outline-danger"
          >
            Ok
          </Button>
        </div>
      </Alert>
    );
  }

  const fetchRuns = async () => {
    APIAuth.get(`/list-runs/${task.id}`)
      .then((response) => {
        console.log(response.data.runs);
        setRuns(response.data.runs);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  useEffect(() => {
    fetchRuns();
  }, []);

  const downloadResults = () => {
    // TODO: Implement download results
    // The CSV file should contain the following columns:
    // Conversational agent id, user simulation id, [metric name 1], [metric name 2], ...
  };

  return (
    <Container>
      <h2>{task.name}</h2>
      <p>{task.description}</p>

      {/* Add option to download all results in a CSV file */}
      <Button variant="primary" className="mb-3" onClick={downloadResults}>
        Download all results as CSV
      </Button>

      {/* Select metric to build result matrix */}
    </Container>
  );
};

export default TaskDashboard;

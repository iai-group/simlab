import { Alert, Button, Container } from "react-bootstrap";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { APIAuth } from "../API";

const TaskDashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const task = location.state?.task;
  const [resultRecords, setResultRecords] = useState<any[]>([]);

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

  const fetchResultRecords = async () => {
    APIAuth.get(`/results/${task.id}`)
      .then((response) => {
        console.log(response.data.results);
        setResultRecords(response.data.results);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  useEffect(() => {
    fetchResultRecords();
  }, []);

  const downloadResults = () => {
    const data = JSON.stringify(resultRecords, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${task.name}_results.json`;
    a.click();
  };

  return (
    <Container>
      <h2>{task.name}</h2>
      <p>{task.description}</p>

      {/* Add option to download all results in a JSON file */}
      <Button variant="primary" className="mb-3" onClick={downloadResults}>
        Download detailed results as JSON
      </Button>

      {/* Select metric to build result matrix */}
      <h3>Results</h3>
      {resultRecords.length > 0 ? (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Conversational Agent ID</th>
              <th>User Simulation ID</th>
              {Object.keys(resultRecords[0]?.metrics || {}).map(
                (metricName) => (
                  <th key={metricName}>{metricName}</th>
                )
              )}
            </tr>
          </thead>
          <tbody>
            {resultRecords.map((record: any) => (
              <tr key={record.run_name}>
                <td>{record.agent_id}</td>
                <td>{record.user_simulator_id}</td>
                {Object.values(record.metrics || {}).map((metric: any, idx) => (
                  <td key={idx}>{metric.mean.toFixed(2)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No results available</p>
      )}
    </Container>
  );
};

export default TaskDashboard;

import { Alert, Button, Container } from "react-bootstrap";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
} from "@mui/material";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { APIAuth } from "../API";

const TaskDashboard = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const task = location.state?.task;
  const [resultRecords, setResultRecords] = useState<any[]>([]);
  const [order, setOrder] = useState<"asc" | "desc">("asc");
  const [orderBy, setOrderBy] = useState<string>("run_name");

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
    APIAuth.get(`/results/${task.name}`)
      .then((response) => {
        if (response.status !== 200) {
          return;
        }
        console.log(response.data);
        setResultRecords(response.data.results);
      })
      .catch((error) => {
        console.error("error", error);
      });
  };

  useEffect(() => {
    fetchResultRecords();
  }, [task?.name]);

  const downloadResults = () => {
    const data = JSON.stringify(resultRecords, null, 2);
    const blob = new Blob([data], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${task.name}_results.json`;
    a.click();
  };

  // Sorting
  const handleSort = (column: string) => {
    if (orderBy === column) {
      setOrder(order === "asc" ? "desc" : "asc");
    } else {
      setOrderBy(column);
      setOrder("asc");
    }
  };

  const sortNumeric = (a: number, b: number, order: "asc" | "desc") => {
    return order === "asc" ? a - b : b - a;
  };

  const sortString = (a: string, b: string, order: "asc" | "desc") => {
    return order === "asc"
      ? a.localeCompare(b, undefined, { sensitivity: "base" })
      : b.localeCompare(a, undefined, { sensitivity: "base" });
  };

  const sortedResults = resultRecords.slice().sort((a, b) => {
    let valueA = orderBy in a ? a[orderBy] : a.metrics?.[orderBy]?.mean;
    let valueB = orderBy in b ? b[orderBy] : b.metrics?.[orderBy]?.mean;

    if (valueA == null || valueB == null) return 0;

    // Detect if it's a number (allowing for numeric metrics)
    const isNumeric = !isNaN(parseFloat(valueA)) && !isNaN(parseFloat(valueB));

    return isNumeric
      ? sortNumeric(parseFloat(valueA), parseFloat(valueB), order)
      : sortString(valueA.toString(), valueB.toString(), order);
  });

  return (
    <Container>
      <h2>{task.name}</h2>
      <p>{task.description}</p>

      {/* Add option to download all results in a JSON file */}
      <Button
        variant="primary"
        className="mb-3"
        onClick={downloadResults}
        disabled={resultRecords.length === 0}
      >
        Download detailed results as JSON
      </Button>

      {/* Select metric to build result matrix */}
      <h3>Results</h3>
      {resultRecords.length > 0 ? (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>
                  <TableSortLabel
                    active={orderBy === "run_name"}
                    direction={orderBy === "run_name" ? order : "asc"}
                    onClick={() => handleSort("run_name")}
                  >
                    <strong>Run Name</strong>
                  </TableSortLabel>
                </TableCell>

                <TableCell>
                  <TableSortLabel
                    active={orderBy === "agent_id"}
                    direction={orderBy === "agent_id" ? order : "asc"}
                    onClick={() => handleSort("agent_id")}
                  >
                    <strong>Conv. Agent ID</strong>
                  </TableSortLabel>
                </TableCell>

                <TableCell>
                  <TableSortLabel
                    active={orderBy === "user_simulator_id"}
                    direction={orderBy === "user_simulator_id" ? order : "asc"}
                    onClick={() => handleSort("user_simulator_id")}
                  >
                    <strong>User Sim. ID</strong>
                  </TableSortLabel>
                </TableCell>

                {Object.keys(resultRecords[0]?.metrics || {}).map(
                  (metricName) => (
                    <TableCell key={metricName} align="center">
                      <TableSortLabel
                        active={orderBy === metricName}
                        direction={orderBy === metricName ? order : "asc"}
                        onClick={() => handleSort(metricName)}
                      >
                        <strong>{metricName}</strong>
                      </TableSortLabel>
                    </TableCell>
                  )
                )}
              </TableRow>
            </TableHead>
            <TableBody>
              {sortedResults.map((record: any) => (
                <TableRow key={record._id}>
                  <TableCell>{record.run_name}</TableCell>
                  <TableCell>{record.agent_id}</TableCell>
                  <TableCell>{record.user_simulator_id}</TableCell>
                  {Object.values(record.metrics || {}).map(
                    (metric: any, idx) => (
                      <TableCell key={idx} align="center">
                        {typeof metric.mean === "number"
                          ? metric.mean.toFixed(3)
                          : metric.mean}
                      </TableCell>
                    )
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <p>No results available</p>
      )}
    </Container>
  );
};

export default TaskDashboard;

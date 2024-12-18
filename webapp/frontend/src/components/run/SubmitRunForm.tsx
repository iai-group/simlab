// Run submission form

import { Agent, Metric, Simulator, Task } from "../../types";
import {
  MDBBtn,
  MDBInput,
  MDBProgress,
  MDBProgressBar,
} from "mdb-react-ui-kit";
import { useEffect, useState } from "react";

import { Container } from "react-bootstrap";
import axios from "axios";
import { baseURL } from "../API";

const RunSubmissionForm = () => {
  const [page, setPage] = useState(1);
  const [runName, setRunName] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState("");
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [selectedMetrics, setSelectedMetrics] = useState<string[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [userSimulators, setUserSimulators] = useState<Simulator[]>([]);
  const [selectedUserSimulators, setSelectedUserSimulators] = useState<
    string[]
  >([]);

  const handleNext = () => {
    if (page < 5) {
      setPage(page + 1);
    }
  };

  const handleBack = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  const fetchTasks = async (): Promise<Task[]> => {
    try {
      const response = await axios.get(`${baseURL}/tasks`);
      console.log("Fetched tasks:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching tasks:", error);
      return []; // Return an empty array if there's an error
    }
  };

  const fetchMetrics = async (): Promise<Metric[]> => {
    try {
      const response = await axios.get(`${baseURL}/metrics`);
      console.log("Fetched metrics:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching metrics:", error);
      return []; // Return an empty array if there's an error
    }
  };

  const fetchAgents = async (): Promise<Agent[]> => {
    try {
      const response = await axios.get(`${baseURL}/agents`);
      console.log("Fetched agents:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching agents:", error);
      return []; // Return an empty array if there's an error
    }
  };

  const fetchUserSimulators = async (): Promise<Simulator[]> => {
    try {
      const response = await axios.get(`${baseURL}/simulators`);
      console.log("Fetched simulators:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching simulators:", error);
      return []; // Return an empty array if there's an error
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      if (page === 1) {
        const data = await fetchTasks();
        setTasks(data);
      } else if (page === 2) {
        const data = await fetchMetrics();
        setMetrics(data);
      } else if (page === 3) {
        const data = await fetchAgents();
        setAgents(data);
      } else if (page === 4) {
        const data = await fetchUserSimulators();
        setUserSimulators(data);
      }
    };

    fetchData();
  }, [page]);

  const handleSubmit = () => {
    const formData = {
      run: runName,
      task: selectedTask,
      metrics: selectedMetrics,
      agents: selectedAgents,
      userSimulators: selectedUserSimulators,
    };
    console.log(formData);

    // TODO: Call the API to submit the run
  };

  const renderPage = () => {
    switch (page) {
      case 1:
        return (
          <div>
            <MDBInput
              wrapperClass="mb-4"
              label="Run name"
              id="formRunName"
              type="text"
              onChange={(e) => setRunName(e.target.value)}
            />
            {tasks.length === 0 ? (
              <p>Loading tasks...</p>
            ) : (
              tasks.map((task) => (
                <div key={task.id}>
                  <input
                    type="radio"
                    value={task.id}
                    checked={selectedTask === task.id}
                    onChange={() => setSelectedTask(task.id)}
                  />
                  {task.name}
                </div>
              ))
            )}
          </div>
        );
      case 2:
        return (
          <div>
            {metrics.length === 0 ? (
              <p>Loading metrics...</p>
            ) : (
              metrics.map((metric) => (
                <div key={metric.id}>
                  <input
                    type="checkbox"
                    value={metric.id}
                    checked={selectedMetrics.includes(metric.id)}
                    onChange={() => {
                      if (selectedMetrics.includes(metric.id)) {
                        setSelectedMetrics(
                          selectedMetrics.filter((m) => m !== metric.id)
                        );
                      } else {
                        setSelectedMetrics([...selectedMetrics, metric.id]);
                      }
                    }}
                  />
                  {metric.name}
                </div>
              ))
            )}
          </div>
        );
      case 3:
        return (
          <div>
            {agents.length === 0 ? (
              <p>Loading agents...</p>
            ) : (
              agents.map((agent) => (
                <div key={agent.id}>
                  <input
                    type="checkbox"
                    value={agent.id}
                    checked={selectedAgents.includes(agent.id)}
                    onChange={() => {
                      if (selectedAgents.includes(agent.id)) {
                        setSelectedAgents(
                          selectedAgents.filter((a) => a !== agent.id)
                        );
                      } else {
                        setSelectedAgents([...selectedAgents, agent.id]);
                      }
                    }}
                  />
                  {agent.name}
                </div>
              ))
            )}
          </div>
        );
      case 4:
        return (
          <div>
            {userSimulators.length === 0 ? (
              <p>Loading user simulators...</p>
            ) : (
              userSimulators.map((simulator) => (
                <div key={simulator.id}>
                  <input
                    type="checkbox"
                    value={simulator.id}
                    checked={selectedUserSimulators.includes(simulator.id)}
                    onChange={() => {
                      if (selectedUserSimulators.includes(simulator.id)) {
                        setSelectedUserSimulators(
                          selectedUserSimulators.filter(
                            (s) => s !== simulator.id
                          )
                        );
                      } else {
                        setSelectedUserSimulators([
                          ...selectedUserSimulators,
                          simulator.id,
                        ]);
                      }
                    }}
                  />
                  {simulator.name}
                </div>
              ))
            )}
          </div>
        );
      case 5:
        return (
          <div>
            <p>Review your run details:</p>
            <p>Run name: {runName}</p>
            <p>Task: {selectedTask}</p>
            <p>Metrics: {selectedMetrics.join(", ")}</p>
            <p>Agents: {selectedAgents.join(", ")}</p>
            <p>User simulators: {selectedUserSimulators.join(", ")}</p>

            <MDBBtn onClick={handleSubmit}>Submit run</MDBBtn>
          </div>
        );
    }
  };

  return (
    <Container>
      <h3>Submit a new run</h3>
      <Container>
        <MDBProgress height="20">
          <MDBProgressBar width={(page / 5) * 100} valuemin={1} valuemax={5}>
            {Math.round((page / 5) * 100)}%
          </MDBProgressBar>
        </MDBProgress>
        <br />
        {renderPage()}
        <br />
        <MDBBtn onClick={handleBack} disabled={page === 1} className="me-2">
          Back
        </MDBBtn>
        <MDBBtn onClick={handleNext} disabled={page === 5}>
          Next
        </MDBBtn>
      </Container>
    </Container>
  );
};

export default RunSubmissionForm;

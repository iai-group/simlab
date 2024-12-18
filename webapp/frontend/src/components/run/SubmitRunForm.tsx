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
import ResourcesCheckBoxList from "./ResourcesCheckBoxList";
import ResourcesRadioList from "./ResourcesRadioList";
import axios from "axios";
import { baseURL } from "../API";

const RunSubmissionForm = () => {
  const [page, setPage] = useState(1);
  const [runName, setRunName] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task>({} as Task);
  const [metrics, setMetrics] = useState<Metric[]>([]);
  const [selectedMetrics, setSelectedMetrics] = useState<Metric[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedAgents, setSelectedAgents] = useState<Agent[]>([]);
  const [userSimulators, setUserSimulators] = useState<Simulator[]>([]);
  const [selectedUserSimulators, setSelectedUserSimulators] = useState<
    Simulator[]
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

  const convertPythonTypetoJSType = (arg: any) => {
    // Convert argument Python types to TypeScript types
    let type: string;
    if (arg["type"] === "str") {
      type = "string";
    } else if (arg["type"] === "int") {
      type = "number";
    } else {
      type = "unknown";
    }
    return type;
  };

  const fetchTasks = async (): Promise<Task[]> => {
    try {
      const response = await axios.get(`${baseURL}/tasks`);
      const fetchedTasks = response.data.map((d: any) => {
        const args = Object.entries(d["arguments"])
          .map(([name, arg]: [string, any]) => {
            if (arg["configurable"] === true) {
              let type: string = convertPythonTypetoJSType(arg);
              return {
                name,
                type: type,
              };
            }
          })
          .filter((arg: any) => arg !== undefined);

        return {
          id: d["_id"],
          name: d["name"],
          description: d["description"],
          arguments: args,
        };
      });
      return fetchedTasks;
    } catch (error) {
      console.error("Error fetching tasks:", error); // TODO: Display error as a toast
      return []; // Return an empty array if there's an error
    }
  };

  const fetchMetrics = async (): Promise<Metric[]> => {
    try {
      const response = await axios.get(`${baseURL}/metrics`);

      const fetchedMetrics = response.data.map((d: any) => {
        const args = Object.entries(d["arguments"])
          .map(([name, arg]: [string, any]) => {
            if (arg["configurable"] === true) {
              let type: string = convertPythonTypetoJSType(arg);
              return {
                name,
                type: type,
              };
            }
          })
          .filter((arg: any) => arg !== undefined);
        return {
          id: d["_id"],
          name: d["name"],
          description: d["description"],
          arguments: args,
        };
      });
      return fetchedMetrics;
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
      switch (page) {
        case 1:
          setTasks(await fetchTasks());
          break;
        case 2:
          setMetrics(await fetchMetrics());
          break;
        case 3:
          setAgents(await fetchAgents());
          break;
        case 4:
          setUserSimulators(await fetchUserSimulators());
          break;
        default:
          break;
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
              <ResourcesRadioList<Task>
                items={tasks}
                selectedItem={selectedTask}
                setSelectedItem={setSelectedTask}
              />
            )}
          </div>
        );
      case 2:
        return (
          <div>
            {metrics.length === 0 ? (
              <p>Loading metrics...</p>
            ) : (
              <ResourcesCheckBoxList<Metric>
                items={metrics}
                selectedItems={selectedMetrics}
                setSelectedItems={setSelectedMetrics}
              />
            )}
          </div>
        );
      case 3:
        return (
          <div>
            {agents.length === 0 ? (
              <p>Loading agents...</p>
            ) : (
              <ResourcesCheckBoxList
                items={agents}
                selectedItems={selectedAgents}
                setSelectedItems={setSelectedAgents}
              />
            )}
          </div>
        );
      case 4:
        return (
          <div>
            {userSimulators.length === 0 ? (
              <p>Loading user simulators...</p>
            ) : (
              <ResourcesCheckBoxList
                items={userSimulators}
                selectedItems={selectedUserSimulators}
                setSelectedItems={setSelectedUserSimulators}
              />
            )}
          </div>
        );
      case 5:
        return (
          <div>
            <p>Review your run details:</p>
            <p>Run name: {runName}</p>
            <p>Task: {selectedTask.name}</p>
            <p>Metrics: {selectedMetrics.map((m) => m.name).join(", ")}</p>
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

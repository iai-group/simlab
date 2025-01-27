// Run submission form to add new system to public leaderboard

import { APIAuth, baseURL } from "../API";
import {
  Alert,
  Button,
  Container,
  Toast,
  ToastContainer,
} from "react-bootstrap";
import { MDBInput, MDBRadio, MDBTextArea } from "mdb-react-ui-kit";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { Form } from "react-bootstrap";
import { System } from "../../types";

const RunSubmissionForm = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const task = location.state?.task;
  const [runName, setRunName] = useState("");
  const [agentEvaluated, setAgentEvaluated] = useState<boolean | null>(null);
  const [system, setSystem] = useState<System>({} as System);
  const [parameters, setParameters] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [participants, setParticipants] = useState<string[] | null>(null);

  // If no task are provided, redirect to the tasks page
  if (!task) {
    return (
      <Alert variant="danger" className="m-3">
        <p>
          No task selected. Please go back to the tasks page and select a task.
        </p>
        <hr />
        <div className="d-flex justify-content-end">
          <Button onClick={() => navigate("/tasks")} variant="outline-danger">
            Ok
          </Button>
        </div>
      </Alert>
    );
  }

  const handleSubmit = () => {
    if (!runName || !system || !system.image) {
      setToastMessage("Please fill in all required fields.");
      return;
    }

    if (parameters) {
      try {
        const parsedParameters = JSON.parse(parameters);
        system.parameters = parsedParameters;
      } catch (e) {
        setToastMessage("Invalid JSON configuration.");
        return;
      }
    }

    const formData = {
      run_name: runName,
      public: true,
      task_id: task.id,
      system: system,
    };

    APIAuth.post(`${baseURL}/run-request`, formData)
      .then((response) => {
        console.log(response.data);
        setToastMessage("Run submitted successfully!");
      })
      .catch((error) => {
        setToastMessage("Error submitting run. Please reach out to the admin.");
        console.error(error);
      });
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.id;
    if (value === "agent") {
      setAgentEvaluated(true);
      setSystem({ ...system, type: "agent" });
    } else if (value === "simulator") {
      setAgentEvaluated(false);
      setSystem({ ...system, type: "simulator" });
    }
  };

  const fetchSystemImage = async (systemImageName: string) => {
    const response = await APIAuth.post(`${baseURL}/image`, {
      image: systemImageName,
    }).then((response) => response.data);
    return response;
  };

  const fetchAgents = async () => {
    const response = await fetch(`${baseURL}/agents`).then((response) =>
      response.json()
    );
    return response;
  };

  const fetchSimulators = async () => {
    const response = await fetch(`${baseURL}/simulators`).then((response) =>
      response.json()
    );
    return response;
  };

  useEffect(() => {
    if (agentEvaluated !== null) {
      if (agentEvaluated) {
        fetchAgents().then((response) => {
          setParticipants(response.map((agent: any) => agent.tags[0]));
        });
      } else {
        fetchSimulators().then((response) => {
          setParticipants(response.map((simulator: any) => simulator.tags[0]));
        });
      }
    }
  }, [agentEvaluated]);

  return (
    <Container>
      <h3>Submit a new run</h3>
      <p>
        Selected Task:{" "}
        {task
          ? task.name
          : "No task selected. Please go back and select a task."}
      </p>

      {/* Run Name */}
      <p>Run name*</p>
      <MDBInput
        wrapperClass="mb-4"
        label="Run name"
        id="formRunName"
        type="text"
        onChange={(e) => setRunName(e.target.value)}
      />

      {/* System to evaluate (either agent or simulator) */}
      <p>Are you evaluating a conversational agent or a user simulator?*</p>
      <div className="d-flex">
        <MDBRadio
          name="system"
          label="Conversational Agent"
          id="agent"
          onChange={handleChange}
          className="me-3"
        />
        <MDBRadio
          name="system"
          label="User Simulator"
          id="simulator"
          onChange={handleChange}
          className="me-3"
        />
      </div>

      {/* System Configuration */}
      {agentEvaluated !== null ? (
        <>
          <p className="mt-4">
            {agentEvaluated ? "Conversational Agent" : "User Simulator"} image*
          </p>
          <Form.Select
            className="m-4"
            aria-label="Default select example"
            onChange={(e) => {
              const systemImageName = e.target.value;
              fetchSystemImage(systemImageName).then((response) => {
                setSystem({
                  ...system,
                  image: response.image,
                  arguments: response.arguments ? response.arguments : [],
                  class_name: response.class_name,
                });
              });
            }}
          >
            <option>Select an image</option>
            {participants?.map((participant) => (
              <option key={participant} value={participant}>
                {participant}
              </option>
            ))}
          </Form.Select>

          {/* Additional configuration as a JSON file (optional) */}
          <p>
            {agentEvaluated ? "Conversational Agent" : "User Simulator"}{" "}
            configuration
          </p>
          <MDBTextArea
            wrapperClass="m-4"
            label="Configuration (JSON format)"
            id="formSystemConfig"
            onChange={(e) => {
              setParameters(e.target.value);
            }}
            rows={5}
          />
        </>
      ) : (
        <></>
      )}

      {/* Submit Button */}
      <Button variant="primary" type="submit" onClick={handleSubmit}>
        Submit run request
      </Button>

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

export default RunSubmissionForm;

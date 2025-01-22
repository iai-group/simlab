// Run submission form

import { APIAuth, baseURL } from "../API";
import {
  Alert,
  Button,
  Container,
  Toast,
  ToastContainer,
} from "react-bootstrap";
import { MDBInput, MDBRadio, MDBTextArea } from "mdb-react-ui-kit";
import { useLocation, useNavigate } from "react-router-dom";

import { System } from "../../types";
import { useState } from "react";

const RunSubmissionForm = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const task = location.state?.task;
  const [runName, setRunName] = useState("");
  const [agentEvaluated, setAgentEvaluated] = useState<boolean | null>(null);
  const [system, setSystem] = useState<System>({} as System);
  const [config, setConfig] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

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
    if (!runName || !system.id || !system.image) {
      setToastMessage("Please fill in all required fields.");
      return;
    }

    if (config) {
      try {
        const parsedConfig = JSON.parse(config);
        setSystem({ ...system, config: parsedConfig });
      } catch (e) {
        setToastMessage("Invalid JSON configuration.");
        return;
      }
    }

    const formData = {
      run_name: runName,
      task_id: task.id,
      system: system,
    };

    APIAuth.post(`${baseURL}/run-request`, formData)
      .then((response) => {
        console.log(response);
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
    } else if (value === "simulator") {
      setAgentEvaluated(false);
    }
  };

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
          <MDBInput
            wrapperClass="m-4"
            label="Image"
            id="formSystemImage"
            type="text"
            onChange={(e) => setSystem({ ...system, image: e.target.value })}
          />
          <p>
            {agentEvaluated ? "Conversational Agent" : "User Simulator"} ID*
          </p>
          <MDBInput
            wrapperClass="m-4"
            label="ID"
            id="formSystemID"
            type="text"
            onChange={(e) => setSystem({ ...system, id: e.target.value })}
          />

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
              setConfig(e.target.value);
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

// Run submission form

import {
  MDBBtn,
  MDBFile,
  MDBInput,
  MDBModal,
  MDBModalBody,
  MDBModalContent,
  MDBModalDialog,
  MDBModalHeader,
  MDBModalTitle,
} from "mdb-react-ui-kit";

import { APIAuth } from "../API";
import { Alert } from "react-bootstrap";
import { useState } from "react";

type SubmitRunFormProps = {
  isOpen: boolean;
  toggle: () => void;
};

const SubmitRunForm = ({ isOpen, toggle }: SubmitRunFormProps) => {
  const [runName, setRunName] = useState("");
  const [runConfigurationFile, setRunConfigurationFile] = useState<File | null>(
    null
  );
  const [errorMessage, setErrorMessage] = useState("");

  const handleRunSubmission = async () => {
    const formData = new FormData();
    formData.append("run_name", runName);
    if (runConfigurationFile) {
      formData.append("run_configuration_file", runConfigurationFile);
    }

    console.log(formData);

    APIAuth.post("/run-request", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
      .then((response) => {
        console.log(response);
        // TODO: Display a success message in Alert and close the modal
        toggle();
      })
      .catch((error) => {
        setErrorMessage(error.message || "An unknown error occurred.");
      });
  };

  return (
    <MDBModal open={isOpen} onClose={toggle} tabIndex="-1">
      <MDBModalDialog>
        <MDBModalContent>
          <MDBModalHeader>
            <MDBModalTitle>Submit a new run request</MDBModalTitle>
            <MDBBtn
              className="btn-close"
              color="none"
              onClick={toggle}
            ></MDBBtn>
          </MDBModalHeader>
          <MDBModalBody>
            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
            <MDBInput
              wrapperClass="mb-4"
              label="Run name"
              id="formRunName"
              type="text"
              onChange={(e) => setRunName(e.target.value)}
            />
            <MDBFile
              label="Run configuration file"
              onChange={(e) =>
                setRunConfigurationFile(e.target.files?.[0] || null)
              }
              id="runConfigurationFile"
            />
            <br />
            <MDBBtn onClick={handleRunSubmission}>Submit run request</MDBBtn>
          </MDBModalBody>
        </MDBModalContent>
      </MDBModalDialog>
    </MDBModal>
  );
};

export default SubmitRunForm;

import { Container } from "react-bootstrap";
import { MDBBtn } from "mdb-react-ui-kit";
import SubmitRunForm from "./SubmitRunForm";
import { useState } from "react";

const RunHome = () => {
  const [isSubmitRunModalOpen, setIsSubmitRunModalOpen] = useState(false);

  const toggleSubmitRunModal = () => {
    setIsSubmitRunModalOpen(!isSubmitRunModalOpen);
  };

  return (
    <Container>
      <h1>Runs</h1>
      {/* TODO
        - Display a list of experiments
          - Link to the experiment detail page
          - Add a button to delete the experiment
      */}
      <MDBBtn onClick={toggleSubmitRunModal}>Submit Run</MDBBtn>
      <SubmitRunForm
        isOpen={isSubmitRunModalOpen}
        toggle={toggleSubmitRunModal}
      />
    </Container>
  );
};

export default RunHome;

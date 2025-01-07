import { Col, Nav, Row } from "react-bootstrap";

import RunSubmissionForm from "./SubmitRunForm";
import { useState } from "react";

const RunHome = () => {
  const [activeTab, setActiveTab] = useState("submitRun");

  const renderContent = () => {
    switch (activeTab) {
      case "submitRun":
        return <RunSubmissionForm />;
      case "userRuns":
        return <p>Display a list of runs submitted by the user.</p>;
      default:
        return <p>Runs section.</p>;
    }
  };

  /* TODO
    - Create a new component to display a list of experiments
      - Link to the experiment detail page
      - Add a button to delete the experiment
  */

  return (
    <>
      <Row>
        <Col xs={3} className="bg-light p-3">
          <Nav className="flex-column">
            <Nav.Link
              onClick={() => setActiveTab("submitRun")}
              style={{ fontWeight: "bold" }}
              active={activeTab === "submitRun"}
            >
              Submit a Run
            </Nav.Link>
            <Nav.Link
              onClick={() => setActiveTab("userRuns")}
              style={{ fontWeight: "bold" }}
              active={activeTab === "userRuns"}
            >
              Your Runs
            </Nav.Link>
          </Nav>
        </Col>
        <Col xs={9}>{renderContent()}</Col>
      </Row>
    </>
  );
};

export default RunHome;

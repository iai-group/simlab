import { Col, Container, Nav, Row } from "react-bootstrap";
import React, { useState } from "react";

import AddSystemTutorial from "./tutorials/AddSystemTutorial";
import DocIndex from "./DocIndex";
import SubmitRunTutorial from "./tutorials/SubmitRunTutorial";
import SwaggerUIComponent from "./SwaggerUIComponent";
import { baseURL } from "../API";

const Documentation = () => {
  const [activeTab, setActiveTab] = useState("");
  const [isTemplateAPIOpen, setIsTemplateAPIOpen] = useState(false);
  const [isTutorialOpen, setIsTutorialOpen] = useState(false);
  const [isSystemsOpen, setIsSystemsOpen] = useState(false);

  const urlTemplateAgentAPI = `${baseURL}/template-agent-api`;
  const urlTemplateSimulatorAPI = `${baseURL}/template-simulator-api`;

  const renderContent = () => {
    switch (activeTab) {
      case "templateAPI":
        return (
          <p>
            The template APIs provide the communication interface for the
            conversational agents and user simulators. The APIs are defined in
            the OpenAPI specification and can be accessed using the Swagger UI.
          </p>
        );
      case "agentAPI":
        return <SwaggerUIComponent swaggerUrl={urlTemplateAgentAPI} />;
      case "simulatorAPI":
        return <SwaggerUIComponent swaggerUrl={urlTemplateSimulatorAPI} />;
      case "tutorials":
        return <p>Here you can add tutorials on how to use the application.</p>;
      case "addSystem":
        return <AddSystemTutorial />;
      case "submitRun":
        return <SubmitRunTutorial />;
      case "tasks":
        return (
          <p>
            List of available tasks, including name, description, and metrics.
          </p>
        );
      case "simulators":
        return (
          <p>
            List of user simulators, including name, description, tasks
            supported, and Docker images.
          </p>
        );
      case "recommenderSystems":
        return (
          <p>
            List of conversational recommender systems, including name,
            description, tasks supported, and Docker images.
          </p>
        );
      case "metrics":
        return <p>Evaluation metrics: name and description.</p>;
      default:
        return <DocIndex />;
    }
  };

  return (
    <>
      <Row>
        <Col xs={3} className="bg-light p-3">
          <Nav className="flex-column">
            {/* Template API Menu */}
            <Nav.Link
              onClick={() => setIsTemplateAPIOpen(!isTemplateAPIOpen)}
              style={{ fontWeight: "bold" }}
              active={activeTab === "templateAPI"}
            >
              Template API
            </Nav.Link>
            {isTemplateAPIOpen && (
              <Nav className="flex-column ms-3">
                <Nav.Link
                  onClick={() => setActiveTab("agentAPI")}
                  active={activeTab === "agentAPI"}
                >
                  Agent API
                </Nav.Link>
                <Nav.Link
                  onClick={() => setActiveTab("simulatorAPI")}
                  active={activeTab === "simulatorAPI"}
                >
                  Simulator API
                </Nav.Link>
              </Nav>
            )}
            {/* Tutorial Menu */}
            <Nav.Link
              onClick={() => setIsTutorialOpen(!isTutorialOpen)}
              style={{ fontWeight: "bold" }}
              active={activeTab === "tutorials"}
            >
              Tutorials
            </Nav.Link>
            {isTutorialOpen && (
              <Nav className="flex-column ms-3">
                <Nav.Link
                  onClick={() => setActiveTab("addSystem")}
                  active={activeTab === "addSystem"}
                >
                  Add a System
                </Nav.Link>
                <Nav.Link
                  onClick={() => setActiveTab("submitRun")}
                  active={activeTab === "submitRun"}
                >
                  Submit a Run
                </Nav.Link>
              </Nav>
            )}
            {/* Other Menu Items */}
            <Nav.Link
              onClick={() => setActiveTab("tasks")}
              active={activeTab === "tasks"}
            >
              Tasks
            </Nav.Link>
            <Nav.Link
              onClick={() => setActiveTab("metrics")}
              active={activeTab === "metrics"}
            >
              Evaluation Metrics
            </Nav.Link>
            {/* Systems Menu */}
            <Nav.Link
              onClick={() => setIsSystemsOpen(!isSystemsOpen)}
              style={{ fontWeight: "bold" }}
              active={activeTab === "systems"}
            >
              Systems
            </Nav.Link>
            {isSystemsOpen && (
              <Nav className="flex-column ms-3">
                <Nav.Link
                  onClick={() => setActiveTab("simulators")}
                  active={activeTab === "simulators"}
                >
                  User Simulators
                </Nav.Link>
                <Nav.Link
                  onClick={() => setActiveTab("recommenderSystems")}
                  active={activeTab === "recommenderSystems"}
                >
                  Recommender Systems
                </Nav.Link>
              </Nav>
            )}
          </Nav>
        </Col>
        <Col xs={9}>{renderContent()}</Col>
      </Row>
    </>
  );
};

export default Documentation;

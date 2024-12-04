import { Container } from "react-bootstrap";
import SwaggerUIComponent from "./docs/SwaggerUIComponent";
import { baseURL } from "./API";

const Documentation = () => {
  const urlTemplateAgentAPI = `${baseURL}/template-agent-api`;
  const urlTemplateSimulatorAPI = `${baseURL}/template-simulator-api`;

  return (
    <Container>
      <h1>Documentation</h1>
      {/* TOOD
        - Add tutorials on how to use the application
        - Add list of available
          - Tasks (incl. name, description, and metrics available)
          - User simulators (incl. name, description, tasks supported, and Docker images)
          - Conversation recommender systems  (incl. name, description, tasks supported, and Docker images)
          - Evaluation metrics (incl. name and description)
      */}
      <h2>APIs</h2>
      <h3>Swagger UI for Template Agent API</h3>
      <SwaggerUIComponent swaggerUrl={urlTemplateAgentAPI} />

      <h3>Swagger UI for Template Simulation API</h3>
      <SwaggerUIComponent swaggerUrl={urlTemplateSimulatorAPI} />
    </Container>
  );
};

export default Documentation;

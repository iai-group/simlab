import "swagger-ui-react/swagger-ui.css";

import SwaggerUI from "swagger-ui-react";

interface SwaggerUIComponentProps {
  swaggerUrl: string;
}

const SwaggerUIComponent = ({ swaggerUrl }: SwaggerUIComponentProps) => {
  return <SwaggerUI url={swaggerUrl} supportedSubmitMethods={[]} />;
};

export default SwaggerUIComponent;

import { APIAuth, baseURL } from "../API";
import { Button, ListGroup } from "react-bootstrap";

import ToastNotification from "../ToastNotification";
import { useState } from "react";

const SystemRow = ({ system }: { system: any }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const downloadSystemImage = () => {
    if (!system.image_name) {
      setToastMessage("Image cannot be downloaded.");
      return;
    }

    APIAuth.post(`${baseURL}/download-image`, {
      image: system.image_name,
    })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <>
      <ListGroup.Item>
        <div className="d-flex justify-content-between align-items-center">
          <Button variant="light" onClick={() => setShowDetails(!showDetails)}>
            {showDetails ? (
              <i className="bi bi-caret-down-fill"></i>
            ) : (
              <i className="bi bi-caret-right-fill"></i>
            )}
          </Button>
          <p>{system.id}</p>
          <p>{system.author}</p>
          <Button variant="primary" onClick={downloadSystemImage}>
            Download <i className="bi bi-download"></i>
          </Button>
        </div>
        {showDetails && <div>{system.description}</div>}
      </ListGroup.Item>
      {/* Toast Notifications */}
      <ToastNotification
        message={toastMessage}
        type="error"
        setMessage={setToastMessage}
      />
    </>
  );
};

export default SystemRow;

import { Button, Col, ListGroup, Row, Spinner } from "react-bootstrap";

import ToastNotification from "../ToastNotification";
import { useState } from "react";

const SystemRow = ({ system }: { system: any }) => {
  const [showDetails, setShowDetails] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);

  const downloadSystemImage = async () => {
    if (!system.image_name) {
      setToastMessage("Image cannot be downloaded.");
      return;
    }

    setIsDownloading(true);

    try {
      const response = await fetch("/api/download-image", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image_name: system.image_name.trim() }),
      });

      if (!response.ok) {
        throw new Error("Failed to download image");
      }

      const contentDisposition = response.headers.get("Content-Disposition");
      const filenameMatch = contentDisposition?.match(/filename="?([^"]+)"?/);
      const filename = filenameMatch ? filenameMatch[1] : "download.tar";

      const reader = response.body?.getReader();
      let downloaded = 0;

      const stream = new ReadableStream({
        start(controller) {
          const push = () => {
            reader?.read().then(({ done, value }) => {
              if (done) {
                controller.close();
                return;
              }

              downloaded += value.length;

              controller.enqueue(value);
              push();
            });
          };

          push();
        },
      });

      const newResponse = new Response(stream);
      const blob = await newResponse.blob();

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Download error:", error);
      setToastMessage("Failed to download image.");
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <>
      <ListGroup.Item>
        <div className="d-flex justify-content-between align-items-center">
          <Row className="w-100">
            <Col
              xs={12}
              sm={1}
              className="d-flex justify-content-center align-items-center"
            >
              <Button
                variant="light"
                onClick={() => setShowDetails(!showDetails)}
              >
                {showDetails ? (
                  <i className="bi bi-caret-down-fill"></i>
                ) : (
                  <i className="bi bi-caret-right-fill"></i>
                )}
              </Button>
            </Col>
            <Col xs={6} sm={5} className="text-left">
              <p className="mb-0">{system.image_name}</p>
            </Col>
            <Col xs={6} sm={4} className="text-left">
              <p className="mb-0">{system.author}</p>
            </Col>

            <Col
              xs={12}
              sm={2}
              className="d-flex justify-content-end align-items-center"
            >
              {isDownloading ? (
                <Button variant="primary" disabled>
                  <span className="ml-2">Downloading...</span>
                  <Spinner
                    animation="border"
                    variant="light"
                    size="sm"
                    role="status"
                    aria-hidden="true"
                  />
                </Button>
              ) : (
                <Button variant="primary" onClick={downloadSystemImage}>
                  Download <i className="bi bi-download"></i>
                </Button>
              )}
            </Col>
          </Row>
        </div>
        {showDetails && <div className="text-left">{system.description}</div>}
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

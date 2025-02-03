import {
  Alert,
  Button,
  Col,
  Container,
  Form,
  Row,
  Spinner,
} from "react-bootstrap";

import { APIAuth } from "../API";
import { useState } from "react";

const DownloadDockerImage = () => {
  const [imageName, setImageName] = useState<string>("");
  const [status, setStatus] = useState<{
    message: string;
    type: "success" | "danger" | "";
  }>({
    message: "",
    type: "",
  });
  const [loading, setLoading] = useState<boolean>(false);

  // Handle input change
  const handleImageNameChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setImageName(event.target.value);
  };

  // Handle Docker image download
  const handleDownload = async () => {
    if (!imageName.trim()) {
      setStatus({
        message: "Please enter a valid image name.",
        type: "danger",
      });
      return;
    }

    setLoading(true);
    setStatus({ message: "", type: "" });

    try {
      const response = await APIAuth.post("/download-image", {
        image_name: imageName.trim(),
      });
      console.log(response);
      setStatus({ message: "Image downloaded successfully.", type: "success" });
    } catch (error: any) {
      console.error(error);
      setStatus({
        message: error.response?.data?.message || "Failed to download image.",
        type: "danger",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-4">
      <Row className="justify-content-md-center">
        <Col md={6}>
          <h3 className="text-center mb-4">Download Docker Image</h3>
          {status.message && (
            <Alert variant={status.type}>{status.message}</Alert>
          )}

          <Form>
            <Form.Group controlId="imageName">
              <Form.Label>Docker Image Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter image name (e.g., my-image:latest)"
                value={imageName}
                onChange={handleImageNameChange}
              />
            </Form.Group>

            <Button
              variant="primary"
              className="w-100 mt-3"
              onClick={handleDownload}
              disabled={loading}
            >
              {loading ? (
                <>
                  <Spinner animation="border" size="sm" className="me-2" />
                  Downloading...
                </>
              ) : (
                "Download Image"
              )}
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default DownloadDockerImage;

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

const UploadDockerImage: React.FC<UploadDockerImageProps> = ({ onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);
  const [imageName, setImageName] = useState("");
  const [status, setStatus] = useState({ message: "", type: "" });
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleImageNameChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setImageName(event.target.value);
  };

  const handleUpload = async () => {
    if (!file) {
      setStatus({ message: "Please select a file.", type: "danger" });
      return;
    }
    if (!imageName.trim()) {
      setStatus({
        message: "Please enter a valid image name.",
        type: "danger",
      });
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("image_name", imageName.trim());

    setLoading(true);
    setStatus({ message: "", type: "" });

    APIAuth.post("/upload-image", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
      .then((response) => {
        console.log(response);
        setStatus({ message: "Upload started.", type: "info" });
        onUploadSuccess();
      })
      .catch((error) => {
        console.error(error);
        setStatus({
          message: "Failed to upload image.",
          type: "danger",
        });
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <Container className="mt-4">
      <Row className="justify-content-md-center">
        <Col md={6}>
          {status.message && (
            <Alert variant={status.type}>{status.message}</Alert>
          )}
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Select Docker Image (.tar, .tar.gz, .tgz)</Form.Label>
              <Form.Control
                type="file"
                accept=".tar,.tar.gz,.tgz"
                onChange={handleFileChange}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Image Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter Image Name"
                value={imageName}
                onChange={handleImageNameChange}
              />
            </Form.Group>
            <Button
              variant="primary"
              onClick={handleUpload}
              disabled={loading}
              className="w-100"
            >
              {loading ? (
                <Spinner as="span" animation="border" size="sm" role="status" />
              ) : (
                "Upload"
              )}
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default UploadDockerImage;

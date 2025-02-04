import {
  Button,
  Card,
  Col,
  Container,
  Dropdown,
  DropdownButton,
  Form,
  InputGroup,
  Modal,
  Pagination,
  Row,
} from "react-bootstrap";
import { useEffect, useState } from "react";

import { System } from "../../types";
import ToastNotification from "../ToastNotification";
import UploadDockerImage from "./UploadDockerImage";
import { baseURL } from "../API";

const SystemHome = () => {
  const [search, setSearch] = useState<string>("");
  const [filterType, setFilterType] = useState<string>("all");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [agents, setAgents] = useState<System[]>([]);
  const [simulators, setSimulators] = useState<System[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const itemsPerPage = 10;
  const [showModal, setShowModal] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Fetch agents and simulators on initial load
  useEffect(() => {
    const fetchSystems = async () => {
      setLoading(true);
      try {
        const agentsResponse = await fetch(`${baseURL}/agents`);
        const simulatorsResponse = await fetch(`${baseURL}/simulators`);
        const agentsData = await agentsResponse.json();
        const simulatorsData = await simulatorsResponse.json();
        setAgents(agentsData);
        setSimulators(simulatorsData);
      } catch (err) {
        console.error(err);
        setToastMessage("Error fetching systems. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchSystems();
  }, []);

  const systemsData = [...agents, ...simulators];

  const filteredSystems = systemsData
    .filter((system) => {
      if (filterType !== "all" && system.type !== filterType) return false;
      return system.image.toLowerCase().includes(search.toLowerCase());
    })
    .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  const totalPages = Math.ceil(filteredSystems.length / itemsPerPage);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(event.target.value);
  };

  const handleFilterTypeChange = (eventKey: string | null) => {
    setFilterType(eventKey || "all");
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  const handlePrevPage = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  if (loading) {
    return <Container className="mt-5 text-center">Loading...</Container>;
  }

  return (
    <Container className="mt-5 text-center">
      <h2 className="mb-4">Systems Repository</h2>

      <Button
        variant="primary"
        className="mb-3"
        onClick={() => setShowModal(true)}
      >
        Add New System
      </Button>

      <InputGroup className="mb-3">
        <Form.Control
          placeholder="Search for a system..."
          value={search}
          onChange={handleSearchChange}
        />
      </InputGroup>

      <DropdownButton
        variant="outline-secondary"
        title={`Filter by Type: ${filterType === "all" ? "All" : filterType}`}
        onSelect={handleFilterTypeChange}
        className="mb-3"
      >
        <Dropdown.Item eventKey="all">All</Dropdown.Item>
        <Dropdown.Item eventKey="agent">Agent</Dropdown.Item>
        <Dropdown.Item eventKey="simulator">Simulator</Dropdown.Item>
      </DropdownButton>

      {/* Systems List */}
      {filteredSystems.length === 0 ? (
        <p className="text-muted">No systems found.</p>
      ) : (
        <>
          <Row>
            {filteredSystems.map((system) => (
              <Col md={4} key={system.id} className="mb-4">
                <Card>
                  <Card.Body>
                    <Card.Title>{system.image}</Card.Title>
                    <Card.Text>{system.type}</Card.Text>
                    <Button variant="info" className="me-2">
                      View Details
                    </Button>
                    <Button variant="success">Download</Button>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="d-flex justify-content-between align-items-center">
              <Button
                variant="secondary"
                onClick={handlePrevPage}
                disabled={currentPage === 1}
              >
                Previous
              </Button>
              <span>
                Page {currentPage} of {totalPages}
              </span>
              <Button
                variant="secondary"
                onClick={handleNextPage}
                disabled={currentPage === totalPages}
              >
                Next
              </Button>
            </div>
          )}
        </>
      )}

      {/* Upload Docker Image Modal */}
      <Modal
        show={showModal}
        onHide={() => setShowModal(false)}
        size="lg"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Upload Docker Image</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <UploadDockerImage />
        </Modal.Body>
      </Modal>

      {/* Toast Notifications */}
      <ToastNotification
        message={toastMessage}
        type="error"
        setMessage={setToastMessage}
      />
    </Container>
  );
};

export default SystemHome;

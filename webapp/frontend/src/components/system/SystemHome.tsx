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
import UploadDockerImage from "./UploadDockerImage";
import { baseURL } from "../API";

const SystemHome = () => {
  const [search, setSearch] = useState<string>("");
  const [filterType, setFilterType] = useState<string>("all");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [agents, setAgents] = useState<System[]>([]);
  const [simulators, setSimulators] = useState<System[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const itemsPerPage = 10;
  const [showModal, setShowModal] = useState<boolean>(false);

  // Fetch agents and simulators on initial load
  useEffect(() => {
    const fetchSystems = async () => {
      setLoading(true);
      setError(null);
      try {
        const agentsResponse = await fetch(`${baseURL}/agents`);
        const simulatorsResponse = await fetch(`${baseURL}/simulators`);
        const agentsData = await agentsResponse.json();
        const simulatorsData = await simulatorsResponse.json();
        setAgents(agentsData);
        setSimulators(simulatorsData);
      } catch (err) {
        console.error(err);
        setError("Failed to fetch systems data.");
      } finally {
        setLoading(false);
      }
    };

    fetchSystems();
  }, []);

  // Combine agents and simulators into one list
  const systemsData = [...agents, ...simulators];

  // Filter and paginate systems
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
    // Ensure that null doesn't get passed, use 'all' as fallback
    setFilterType(eventKey || "all");
  };

  const handlePaginationClick = (page: number) => {
    setCurrentPage(page);
  };

  if (loading) {
    return <Container className="mt-5 text-center">Loading...</Container>;
  }

  //   if (error) {
  //     return <Container className="mt-5 text-center">{error}</Container>;
  //   }

  const handleShowModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);

  return (
    <Container className="mt-5 text-center">
      <h2 className="mb-4">Systems Repository</h2>

      {/* Add System Button */}
      <Button variant="primary" className="mb-3" onClick={handleShowModal}>
        Add New System
      </Button>

      {/* Search Bar */}
      <InputGroup className="mb-3">
        <Form.Control
          placeholder="Search for a system..."
          value={search}
          onChange={handleSearchChange}
        />
      </InputGroup>

      {/* Filter Dropdown */}
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

      {/* List of Systems */}
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

      {/* Pagination */}
      <Pagination>
        {Array.from({ length: totalPages }, (_, index) => (
          <Pagination.Item
            key={index + 1}
            active={index + 1 === currentPage}
            onClick={() => handlePaginationClick(index + 1)}
          >
            {index + 1}
          </Pagination.Item>
        ))}
      </Pagination>

      {/* Modal for UploadDockerImage */}
      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Upload Docker Image</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <UploadDockerImage />
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default SystemHome;

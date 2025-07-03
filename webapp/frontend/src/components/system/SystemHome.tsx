import {
  Button,
  Container,
  Dropdown,
  DropdownButton,
  Form,
  InputGroup,
  ListGroup,
  Modal,
} from "react-bootstrap";
import { useEffect, useState } from "react";

import SystemRow from "./SystemRow";
import ToastNotification from "../ToastNotification";
import UploadDockerImage from "./UploadDockerImage";
import axios from "axios";
import { baseURL } from "../API";

const SystemHome = () => {
  const [search, setSearch] = useState<string>("");
  const [filterType, setFilterType] = useState<string>("all");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [agents, setAgents] = useState<Object[]>([]);
  const [simulators, setSimulators] = useState<Object[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const itemsPerPage = 10;
  const [showModal, setShowModal] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  // Fetch agents and simulators on initial load
  useEffect(() => {
    const fetchSystems = async () => {
      setLoading(true);

      axios
        .get(`${baseURL}/agents`)
        .then((response) => {
          if (Array.isArray(response.data)) {
            setAgents(response.data);
          }
        })
        .catch((error) => {
          console.error(error);
          setToastMessage("Error fetching systems. Please try again later.");
        });
      axios
        .get(`${baseURL}/simulators`)
        .then((response) => {
          if (Array.isArray(response.data)) {
            setSimulators(response.data);
          }
        })
        .catch((error) => {
          console.error(error);
          setToastMessage("Error fetching systems. Please try again later.");
        });
      setLoading(false);
    };

    fetchSystems();
  }, []);

  const systemsData = [...agents, ...simulators];

  const filteredSystems = systemsData
    .filter((system) => {
      if (filterType !== "all" && system.type !== filterType) return false;
      return (
        system.id?.toLowerCase().includes(search.toLowerCase()) ||
        system.image_name?.toLowerCase().includes(search.toLowerCase())
      );
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
          <ListGroup>
            {filteredSystems.map((system) => (
              <SystemRow system={system} />
            ))}
          </ListGroup>

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
          <UploadDockerImage onUploadSuccess={() => setShowModal(false)} />
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

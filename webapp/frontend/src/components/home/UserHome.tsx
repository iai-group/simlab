// Home page for logged in users

import {
  Button,
  Container,
  Form,
  InputGroup,
  Toast,
  ToastContainer,
} from "react-bootstrap";
import { MDBListGroup, MDBListGroupItem } from "mdb-react-ui-kit";
import { useContext, useEffect, useState } from "react";

import { APIAuth } from "../API";
import { AuthContext } from "../../contexts/AuthContext";

const UserHome = () => {
  const { user } = useContext(AuthContext);
  const [runs, setRuns] = useState([]);
  const [toastMessage, setToastMessage] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [currentPage, setCurrentPage] = useState<number>(1);
  const runsPerPage = 20;

  const fetchUserRuns = async () => {
    APIAuth.get("/list-runs-user")
      .then((response) => {
        console.log(response.data.runs);
        setRuns(response.data.runs);
      })
      .catch((error) => {
        setToastMessage("Error fetching runs. Please reach out to the admin.");
        console.error(error);
      });
  };

  // Handle search
  const filteredRuns = runs.filter((run: any) =>
    run.run_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Pagination logic
  const indexOfLastRun = currentPage * runsPerPage;
  const indexOfFirstRun = indexOfLastRun - runsPerPage;
  const currentRuns = filteredRuns.slice(indexOfFirstRun, indexOfLastRun);
  const totalPages = Math.ceil(filteredRuns.length / runsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  const handlePrevPage = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  useEffect(() => {
    fetchUserRuns();
  }, []);

  return (
    <Container>
      <h1>Home for {user?.username}</h1>

      <h6>Your experiments</h6>

      {currentRuns.length === 0 ? (
        <p>You have no experiments yet.</p>
      ) : (
        <>
          {/* Search Bar */}
          <InputGroup className="mb-3">
            <Form.Control
              placeholder="Search experiments by name..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Button
              variant="outline-secondary"
              onClick={() => setSearchTerm("")}
            >
              Clear
            </Button>
          </InputGroup>

          {/* Tasks List */}
          <MDBListGroup style={{ minWidth: "22rem" }} light>
            {currentRuns.map((run: any) => (
              <MDBListGroupItem
                key={run._id}
                onClick={() => console.log("Clicked on run", run._id)} // TODO: Implement function that display run details
                tag="button"
                action
                type="button"
              >
                {run.run_name}
              </MDBListGroupItem>
            ))}
          </MDBListGroup>

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
      {/* Toast Notifications */}
      <ToastContainer className="p-3" position="top-end" style={{ zIndex: 1 }}>
        <Toast
          onClose={() => setToastMessage(null)}
          show={!!toastMessage}
          delay={5000}
          autohide
          bg="danger"
        >
          <Toast.Header>
            <strong className="me-auto">SimLab Error</strong>
          </Toast.Header>
          <Toast.Body>{toastMessage}</Toast.Body>
        </Toast>
      </ToastContainer>
    </Container>
  );
};

export default UserHome;

import { Argument, Resource } from "../../types";
import { Col, Container, Row } from "react-bootstrap";
import { Dispatch, SetStateAction, useState } from "react";
import {
  MDBBtn,
  MDBInput,
  MDBListGroup,
  MDBListGroupItem,
  MDBModal,
  MDBModalBody,
  MDBModalContent,
  MDBModalDialog,
  MDBModalFooter,
  MDBModalHeader,
} from "mdb-react-ui-kit";

interface ResourcesCheckBoxListProps<Resource> {
  resourceType: string;
  items: Resource[];
  selectedItems: Resource[];
  setSelectedItems: Dispatch<SetStateAction<Resource[]>>;
}

const AddResourcesList = ({
  resourceType,
  items,
  selectedItems,
  setSelectedItems,
}: ResourcesCheckBoxListProps<Resource>) => {
  const [showModal, setShowModal] = useState(false);
  const [selectedResource, setSelectedResource] = useState<Resource | null>(
    null
  );
  const [resourceName, setResourceName] = useState<string>("");
  const [argumentValues, setArgumentValues] = useState<Argument[] | null>(null);

  const handleAddResource = (resource: Resource) => {
    setSelectedResource(resource);
    setResourceName(resource.name);
    // Initialize arguments with empty values
    setArgumentValues(
      resource.arguments.map((arg) => ({
        ...arg,
        value: arg.value,
      }))
    );
    setShowModal(true);
  };

  const handleArgumentChange = (name: string, value: string | number) => {
    setArgumentValues(
      (prevValues) =>
        prevValues
          ? prevValues.map((arg) =>
              arg.name === name ? { ...arg, value } : arg
            )
          : [] // In case prevValues is null, ensure an empty array is returned
    );
  };

  const handleSave = () => {
    if (selectedResource && argumentValues) {
      const updatedResource = {
        ...selectedResource,
        arguments: argumentValues,
        name: resourceName,
      };

      // Check if a resource with the same name and id already exists
      const isDuplicate = selectedItems.some(
        (item) =>
          item.id === updatedResource.id && item.name === updatedResource.name
      );
      if (isDuplicate) {
        // If a duplicate is found, show an alert or handle it accordingly
        alert(
          `A resource with the name "${updatedResource.name}" already exists.`
        );
        return;
      }

      const updatedSelectedItems = [
        ...selectedItems,
        updatedResource as Resource,
      ];

      setSelectedItems(updatedSelectedItems);
      setShowModal(false);
      setResourceName(""); // Reset resource name after saving
      setArgumentValues(null); // Reset argument values after saving
    }
  };

  const handleRemoveResource = (resourceToRemove: Resource) => {
    // Removal based on id and arguments. One metric can have multiple
    // configurations;
    const updatedSelectedItems = selectedItems.filter(
      (item) =>
        item.id !== resourceToRemove.id ||
        JSON.stringify(item.arguments) !==
          JSON.stringify(resourceToRemove.arguments)
    );
    setSelectedItems(updatedSelectedItems);
  };

  return (
    <Container>
      <Row>
        <Col xs={6}>
          <Container>
            <h5>Available {resourceType}</h5>
            <MDBListGroup style={{ minWidth: "22rem" }} light>
              {items.map((item: Resource) => (
                <MDBListGroupItem key={item.id}>
                  <div style={{ display: "flex", alignItems: "center" }}>
                    <div style={{ marginRight: "1rem" }}>
                      <MDBBtn onClick={() => handleAddResource(item)}>+</MDBBtn>
                    </div>

                    <div>
                      <b>{item.name}</b>
                      <br />
                      <p style={{ margin: 0 }}>{item.description}</p>
                    </div>
                  </div>
                </MDBListGroupItem>
              ))}
            </MDBListGroup>
          </Container>
        </Col>
        <Col xs={6}>
          <Container>
            <h5>Selected {resourceType}</h5>
            <MDBListGroup style={{ minWidth: "22rem" }} light>
              {selectedItems.map((resource) => (
                <MDBListGroupItem key={resource.id}>
                  <div style={{ display: "flex", alignItems: "center" }}>
                    <div style={{ marginRight: "1rem" }}>
                      <b>{resource.name}</b>
                      <br />
                      <p style={{ margin: 0 }}>
                        {resource.arguments
                          .map((arg) => `${arg.name}: ${arg.value}`)
                          .join(", ")}
                      </p>
                    </div>
                    <MDBBtn
                      color="danger"
                      onClick={() => handleRemoveResource(resource)}
                      size="sm"
                    >
                      -
                    </MDBBtn>
                  </div>
                </MDBListGroupItem>
              ))}
            </MDBListGroup>
          </Container>
        </Col>
      </Row>

      {/* Modal for configuring the arguments */}
      {selectedResource && argumentValues && (
        <MDBModal
          open={showModal}
          onClose={() => setShowModal(false)}
          tabIndex="-1"
        >
          <MDBModalDialog>
            <MDBModalContent>
              <MDBModalHeader>
                Configure Arguments for {selectedResource.name}
                <MDBBtn
                  className="btn-close"
                  color="none"
                  onClick={() => setShowModal(false)}
                ></MDBBtn>
              </MDBModalHeader>
              <MDBModalBody>
                <div key="name" style={{ marginBottom: "1rem" }}>
                  <label htmlFor="name">Name</label>
                  <MDBInput
                    id="name"
                    type="text"
                    value={resourceName}
                    onChange={(e) => setResourceName(e.target.value)}
                  />
                </div>
                {selectedResource.arguments.map((arg) => (
                  <div key={arg.name} style={{ marginBottom: "1rem" }}>
                    <label htmlFor={arg.name}>
                      {arg.name} ({arg.type})
                    </label>
                    <MDBInput
                      id={arg.name}
                      type={arg.type === "number" ? "number" : "text"}
                      value={
                        argumentValues.find((a) => a.name === arg.name)
                          ?.value || ""
                      }
                      onChange={(e) =>
                        handleArgumentChange(arg.name, e.target.value)
                      }
                    />
                  </div>
                ))}
              </MDBModalBody>
              <MDBModalFooter>
                <MDBBtn color="primary" onClick={handleSave}>
                  Save Changes
                </MDBBtn>
              </MDBModalFooter>
            </MDBModalContent>
          </MDBModalDialog>
        </MDBModal>
      )}
    </Container>
  );
};

export default AddResourcesList;

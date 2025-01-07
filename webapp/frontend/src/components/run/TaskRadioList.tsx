import { Argument, Task } from "../../types";
import { Dispatch, SetStateAction, useState } from "react";
import {
  MDBBtn,
  MDBInput,
  MDBListGroup,
  MDBListGroupItem,
} from "mdb-react-ui-kit";

import { Container } from "react-bootstrap";

interface TaskRadioListProps<Task> {
  items: Task[];
  selectedTask: Task;
  setSelectedTask: Dispatch<SetStateAction<Task>>;
}

const TaskRadioList = ({
  items,
  selectedTask,
  setSelectedTask,
}: TaskRadioListProps<Task>) => {
  const [argumentValues, setArgumentValues] = useState<Argument[]>([]);
  const [editing, setEditing] = useState(false); // Tracks if arguments are being edited

  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const itemId = e.target.value;
    const selected = items.find((item) => item.id === itemId);
    if (selected) {
      setSelectedTask(selected);
      setArgumentValues(
        selected.arguments.map((arg) => ({
          ...arg,
          value: arg.value,
        }))
      );
      setEditing(true); // Show the form on task selection
    }
  };

  const handleArgumentChange = (name: string, value: string) => {
    setArgumentValues((prevValues) =>
      prevValues.map((arg) => (arg.name === name ? { ...arg, value } : arg))
    );
  };

  const handleSaveArguments = () => {
    if (selectedTask) {
      const updatedTask = {
        ...selectedTask,
        arguments: argumentValues,
      };
      setSelectedTask(updatedTask);
      setEditing(false); // Exit edit mode after saving
    }
  };

  const handleEditArguments = () => {
    setEditing(true); // Show the form when the Edit button is clicked
  };

  return (
    <Container>
      <MDBListGroup style={{ minWidth: "22rem" }} light>
        {items.map((item: Task) => (
          <MDBListGroupItem key={item.id}>
            <div style={{ display: "flex", alignItems: "center" }}>
              <div style={{ marginRight: "1rem" }}>
                <input
                  type="radio"
                  value={item.id}
                  checked={selectedTask.id === item.id}
                  onChange={handleSelect}
                />
              </div>

              <div>
                <b>{item.name}</b>
                <br />
                <p style={{ margin: 0 }}>{item.description}</p>
              </div>
            </div>
            {/* Display arguments or Edit button */}
            {selectedTask.id === item.id && !editing && (
              <div
                style={{
                  backgroundColor: "#f8f9fa",
                  borderRadius: "8px",
                  padding: "10px",
                  marginTop: "10px",
                }}
              >
                <p>Task arguments:</p>
                {selectedTask.arguments.map((arg) => (
                  <p key={arg.name}>
                    <b>{arg.name}:</b> {arg.value}
                  </p>
                ))}
                <MDBBtn size="sm" onClick={handleEditArguments}>
                  Edit Arguments
                </MDBBtn>
              </div>
            )}
          </MDBListGroupItem>
        ))}
      </MDBListGroup>

      {/* Display argument configuration form when a task is selected or editing */}
      {selectedTask && editing && argumentValues.length > 0 && (
        <div style={{ marginTop: "1rem" }}>
          <h5>Configure arguments for {selectedTask.name}</h5>
          {argumentValues.map((arg) => (
            <div key={arg.name} style={{ marginBottom: "1rem" }}>
              <label htmlFor={arg.name}>
                {arg.name} ({arg.type})
              </label>
              <MDBInput
                id={arg.name}
                type={arg.type === "number" ? "number" : "text"}
                value={arg.value}
                onChange={(e) => handleArgumentChange(arg.name, e.target.value)}
              />
            </div>
          ))}
          <MDBBtn color="primary" onClick={handleSaveArguments}>
            Save Arguments
          </MDBBtn>
        </div>
      )}
    </Container>
  );
};

export default TaskRadioList;

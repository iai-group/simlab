import { Dispatch, SetStateAction } from "react";
import { MDBListGroup, MDBListGroupItem } from "mdb-react-ui-kit";

import { Container } from "react-bootstrap";
import { Task } from "../../types";

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
  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const itemId = e.target.value;
    const selected = items.find((item) => item.id === itemId);
    if (selected) {
      setSelectedTask(selected);
    }
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
          </MDBListGroupItem>
        ))}
      </MDBListGroup>
    </Container>
  );
};

export default TaskRadioList;

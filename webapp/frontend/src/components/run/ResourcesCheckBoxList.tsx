import { Dispatch, SetStateAction } from "react";
import { MDBListGroup, MDBListGroupItem } from "mdb-react-ui-kit";

import { Resource } from "../../types";

interface ResourcesCheckBoxListProps<T extends Resource> {
  items: T[];
  selectedItems: T[];
  setSelectedItems: Dispatch<SetStateAction<T[]>>;
}

const ResourcesCheckBoxList = <T extends Resource>({
  items,
  selectedItems,
  setSelectedItems,
}: ResourcesCheckBoxListProps<T>) => {
  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const itemId = e.target.value;
    if (selectedItems.some((item) => item.id === itemId)) {
      setSelectedItems(selectedItems.filter((item) => item.id !== itemId));
    } else {
      const selected = items.find((item) => item.id === itemId);
      if (selected) {
        setSelectedItems([...selectedItems, selected]);
      }
    }
  };

  return (
    <MDBListGroup style={{ minWidthL: "22rem" }} light>
      {items.map((item: Resource) => (
        <MDBListGroupItem key={item.id}>
          <div style={{ display: "flex", alignItems: "center" }}>
            <div style={{ marginRight: "1rem" }}>
              <input
                type="checkbox"
                value={item.id}
                checked={selectedItems.some(
                  (selected) => selected.id === item.id
                )}
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
  );
};

export default ResourcesCheckBoxList;

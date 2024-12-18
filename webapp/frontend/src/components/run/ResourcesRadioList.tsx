import { Dispatch, SetStateAction } from "react";
import { MDBListGroup, MDBListGroupItem } from "mdb-react-ui-kit";

import { Resource } from "../../types";

interface ResourcesRadioListProps<T extends Resource> {
  items: T[];
  selectedItem: T;
  setSelectedItem: Dispatch<SetStateAction<T>>;
}

const ResourcesRadioList = <T extends Resource>({
  items,
  selectedItem,
  setSelectedItem,
}: ResourcesRadioListProps<T>) => {
  const handleSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const itemId = e.target.value;
    const selected = items.find((item) => item.id === itemId);
    if (selected) {
      setSelectedItem(selected);
    }
  };

  return (
    <MDBListGroup style={{ minWidthL: "22rem" }} light>
      {items.map((item: Resource) => (
        <MDBListGroupItem key={item.id}>
          <div style={{ display: "flex", alignItems: "center" }}>
            <div style={{ marginRight: "1rem" }}>
              <input
                type="radio"
                value={item.id}
                checked={selectedItem.id === item.id}
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

export default ResourcesRadioList;

import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div>
      <h1>404 Not Found</h1>
      <p>
        Sorry, the page you are looking for does not exist. Go back to the{" "}
        <Link to="/home">Home</Link> page.
      </p>
    </div>
  );
};

export default NotFound;

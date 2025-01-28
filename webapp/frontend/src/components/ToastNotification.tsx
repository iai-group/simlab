import { Toast, ToastContainer } from "react-bootstrap";

import React from "react";

interface ToastNotificationProps {
  message: string | null;
  type: "success" | "error" | "info";
  setMessage: (message: string | null) => void;
}

const ToastNotification: React.FC<ToastNotificationProps> = ({
  message,
  type,
  setMessage,
}) => {
  if (!message) return null;

  return (
    <ToastContainer className="p-3" position="top-end" style={{ zIndex: 1 }}>
      <Toast
        onClose={() => setMessage(null)}
        show={!!message}
        delay={5000}
        autohide
        bg={
          type === "success"
            ? "success"
            : type === "error"
            ? "danger"
            : "primary"
        }
      >
        <Toast.Header>
          <strong className="me-auto">
            {type === "success"
              ? "Success"
              : type === "error"
              ? "Error"
              : "Info"}
          </strong>
        </Toast.Header>
        <Toast.Body>{message}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
};

export default ToastNotification;
